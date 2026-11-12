"""Offline acceptance for exact-original transport. No production credentials/network."""
from __future__ import annotations

import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from email.message import Message
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "repository_backup_transport", ROOT / "scripts/repository_backup_transport.py")
m = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)


def sha(value):
    return hashlib.sha256(value).hexdigest()


def metadata(source=None):
    source = m.SOURCE if source is None else source
    return {"id": source["artifact_id"], "name": source["name"],
            "expired": False, "size_in_bytes": source["bytes"],
            "digest": "sha256:" + source["sha256"], "workflow_run": {
                "id": source["run_id"], "head_sha": source["head_sha"],
                "head_branch": "main", "repository_id": 1289596840,
                "head_repository_id": 1289596840}}


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.data = bytes(range(256)) * 9 + b"\x00\xfforiginal-zip-bytes\n"
        self.source = self.root / "original.zip"
        self.source.write_bytes(self.data)
        self.size, self.hash = len(self.data), sha(self.data)
        self.parts = self.root / "parts"
        self.manifest = m.split_archive(self.source, self.parts, self.size, self.hash, 1024)
        self.output = self.root / "assembled.zip"

    def assemble(self):
        m.reassemble(self.parts / "manifest.json", self.output, self.size, self.hash)

    def edit_manifest(self, operation):
        value = copy.deepcopy(self.manifest)
        operation(value)
        (self.parts / "manifest.json").write_text(json.dumps(value))

    def assertBlocked(self):
        with self.assertRaises((ValueError, OSError)):
            self.assemble()
        self.assertFalse(self.output.exists())
        self.assertEqual(list(self.root.glob(".backup-assembly-*")), [])
        self.assertEqual(self.source.read_bytes(), self.data)

    def test_exact_binary_roundtrip(self):
        self.assemble()
        self.assertEqual(self.output.read_bytes(), self.data)
        self.assertEqual(m.digest(self.output), (self.size, self.hash))
        self.assertEqual(self.manifest["independent_custody"], "NOT_PROVEN_BY_EXPORT")

    def test_split_does_not_change_source(self):
        self.assertEqual(self.source.read_bytes(), self.data)
        self.assertEqual(sum(p["bytes"] for p in self.manifest["parts"]), self.size)

    def test_original_pin_mismatch_blocks_before_split(self):
        for size, digest in [(self.size+1, self.hash), (self.size, "0"*64)]:
            with self.subTest(size=size, digest=digest):
                out = self.root / "rejected"
                with self.assertRaises(ValueError):
                    m.split_archive(self.source, out, size, digest, 1024)
                self.assertFalse(out.exists())

    def test_invalid_sizes_and_digests_rejected(self):
        for size, digest, chunk in [(True,self.hash,1024),(0,self.hash,1024),
                 (self.size,None,1024),(self.size,"F"*64,1024),
                 (self.size,self.hash,True),(self.size,self.hash,0),
                 (self.size,self.hash,m.CHUNK_BYTES+1),(self.size,self.hash,1)]:
            with self.subTest(size=size,digest=digest,chunk=chunk):
                with self.assertRaises(ValueError):
                    m.split_archive(self.source,self.root/"rejected",size,digest,chunk)

    def test_existing_split_directory_never_replaced(self):
        with self.assertRaises(FileExistsError):
            m.split_archive(self.source, self.parts, self.size, self.hash, 1024)
        self.assemble()

    def test_source_symlink_rejected(self):
        link = self.root / "source-link"
        link.symlink_to(self.source)
        with self.assertRaises(ValueError):
            m.split_archive(link,self.root/"new",self.size,self.hash,1024)

    def test_manifest_pin_is_not_authority(self):
        self.edit_manifest(lambda x: x.update(original_sha256="0"*64))
        self.assertBlocked()

    def test_manifest_non_object_blocked(self):
        (self.parts/"manifest.json").write_text("[]")
        self.assertBlocked()

    def test_manifest_wrong_schema_blocked(self):
        self.edit_manifest(lambda x: x.update(schema="other"))
        self.assertBlocked()

    def test_manifest_oversize_blocked(self):
        (self.parts/"manifest.json").write_bytes(b" "*(m.BLOCK+1))
        self.assertBlocked()

    def test_manifest_symlink_blocked(self):
        (self.parts/"manifest.json").unlink()
        source = self.root/"manifest-external.json"
        source.write_text(json.dumps(self.manifest))
        (self.parts/"manifest.json").symlink_to(source)
        self.assertBlocked()

    def test_missing_part_blocked(self):
        (self.parts/"archive.part0002").unlink()
        self.assertBlocked()

    def test_corrupt_part_blocked(self):
        part = self.parts/"archive.part0001"
        data = bytearray(part.read_bytes()); data[7] ^= 1; part.write_bytes(data)
        self.assertBlocked()

    def test_corrupt_part_and_rewritten_part_hash_still_blocked(self):
        part = self.parts/"archive.part0001"
        data = bytearray(part.read_bytes()); data[7] ^= 1; part.write_bytes(data)
        self.edit_manifest(lambda x: x["parts"][0].update(sha256=sha(data)))
        self.assertBlocked()

    def test_truncated_part_blocked(self):
        part = self.parts/"archive.part0001"; part.write_bytes(part.read_bytes()[:-1])
        self.assertBlocked()

    def test_oversized_part_blocked(self):
        part = self.parts/"archive.part0001"; part.write_bytes(part.read_bytes()+b"x")
        self.assertBlocked()

    def test_reordered_manifest_blocked(self):
        self.edit_manifest(lambda x: x["parts"].reverse())
        self.assertBlocked()

    def test_duplicate_part_blocked(self):
        self.edit_manifest(lambda x: x["parts"].__setitem__(1,x["parts"][0]))
        self.assertBlocked()

    def test_path_traversal_blocked(self):
        self.edit_manifest(lambda x: x["parts"][0].update(name="../original.zip"))
        self.assertBlocked()

    def test_wrong_part_count_blocked(self):
        self.edit_manifest(lambda x: x["parts"].pop())
        self.assertBlocked()

    def test_wrong_part_size_blocked(self):
        self.edit_manifest(lambda x: x["parts"][0].update(bytes=1023))
        self.assertBlocked()

    def test_invalid_part_digest_blocked(self):
        self.edit_manifest(lambda x: x["parts"][0].update(sha256="not-a-digest"))
        self.assertBlocked()

    def test_part_symlink_blocked(self):
        part=self.parts/"archive.part0001"; original=self.root/"external-part"
        part.rename(original); part.symlink_to(original)
        self.assertBlocked()

    def test_existing_output_never_overwritten(self):
        self.output.write_bytes(b"KEEP")
        with self.assertRaises(ValueError): self.assemble()
        self.assertEqual(self.output.read_bytes(), b"KEEP")

    def test_dangling_output_symlink_never_overwritten(self):
        self.output.symlink_to(self.root/"not-existing")
        with self.assertRaises(ValueError): self.assemble()
        self.assertTrue(self.output.is_symlink())

    def test_cli_error_sanitized(self):
        secret="SECRET_OR_SIGNED_URL_MUST_NOT_APPEAR"
        with mock.patch.object(sys,"argv",["transport","reassemble","file","output"]), \
             mock.patch.object(m,"reassemble",side_effect=OSError(secret)), \
             contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(m.main(),1)
        self.assertNotIn(secret,out.getvalue())
        self.assertIn("TRANSPORT_BLOCKED",out.getvalue())


class NetworkBoundaryTests(unittest.TestCase):
    def test_exact_source_metadata_accepted(self):
        m.verify_metadata(metadata())
        for source in m.SOURCES.values():
            m.verify_metadata(metadata(source), source)

    def test_each_metadata_pin_enforced(self):
        mutations = [lambda v: v.update(id=7), lambda v: v.update(expired=True),
            lambda v: v.update(expired=0),lambda v:v.update(name="other"),
            lambda v:v.update(size_in_bytes=1),lambda v:v.update(digest="sha256:"+"0"*64),
            lambda v:v["workflow_run"].update(id=7),
            lambda v:v["workflow_run"].update(head_sha="0"*40),
            lambda v:v["workflow_run"].update(head_branch="feature"),
            lambda v:v["workflow_run"].update(repository_id=7),
            lambda v:v["workflow_run"].update(head_repository_id=7),
            lambda v:v.update(workflow_run=None)]
        for key, source in m.SOURCES.items():
            for change in mutations:
                with self.subTest(source=key, change=change):
                    v=metadata(source); change(v)
                    with self.assertRaises(ValueError): m.verify_metadata(v, source)
        with self.assertRaises(ValueError): m.verify_metadata([])

    def test_https_storage_allowlist(self):
        self.assertTrue(m.approved_download_url("https://files.blob.core.windows.net/a?sig=redacted"))
        self.assertTrue(m.approved_download_url("https://x.actions.githubusercontent.com/a"))
        for url in ["http://x.blob.core.windows.net/a","https://api.github.com/a",
                    "https://x.blob.core.windows.net.evil.test/a","file:///tmp/file",
                    "https://evil.test/a","https://user:pass@x.blob.core.windows.net/a",
                    "https://x.blob.core.windows.net:444/a"]:
            with self.subTest(url=url): self.assertFalse(m.approved_download_url(url))

    def test_redirect_handler_never_forwards_automatically(self):
        self.assertIsNone(m.NoRedirect().redirect_request(None,None,302,"Found",{},"https://other/"))

    def download(self, body=b"archive", redirect=True, bad_url=None, source=None):
        temporary=tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        output=pathlib.Path(temporary.name)/"original.zip"
        source={**(m.SOURCE if source is None else source),
                "bytes":len(b"archive"),"sha256":sha(b"archive")}
        requests=[]
        def open_mock(req,timeout):
            requests.append(req)
            if len(requests)==1: return io.BytesIO(json.dumps(metadata(source)).encode())
            if len(requests)==2 and redirect:
                h=Message(); h["Location"]=bad_url or "https://x.blob.core.windows.net/a?sig=PRIVATE"
                raise urllib.error.HTTPError(req.full_url,302,"Found",h,io.BytesIO())
            return io.BytesIO(body)
        opener=mock.Mock(); opener.open.side_effect=open_mock
        with mock.patch.object(m.urllib.request,"build_opener",return_value=opener):
            m.download_original(output,"FAKE_TEST_TOKEN",source)
        return requests,output

    def test_selected_source_controls_download_and_validation(self):
        source=m.SOURCES["2026-10-25"]
        requests,output=self.download(source=source)
        endpoint=f'https://api.github.com/repos/{source["repository"]}/actions/artifacts/12592912872'
        self.assertEqual([r.full_url for r in requests[:2]],[endpoint,endpoint+"/zip"])
        self.assertIsNone(requests[2].get_header("Authorization"))
        self.assertEqual(output.read_bytes(),b"archive")

    def test_old_metadata_rejected_before_selected_archive_download(self):
        opener=mock.Mock()
        opener.open.return_value=io.BytesIO(json.dumps(metadata()).encode())
        with mock.patch.object(m.urllib.request,"build_opener",return_value=opener):
            with self.assertRaisesRegex(ValueError,"provider_metadata_mismatch"):
                m.download_original(pathlib.Path("unused"),"FAKE_TEST_TOKEN",m.SOURCES["2026-10-25"])
        self.assertEqual(opener.open.call_count,1)

    def test_redirect_removes_authorization(self):
        requests,output=self.download()
        self.assertEqual(len(requests),3)
        self.assertEqual(requests[0].get_header("Authorization"),"Bearer FAKE_TEST_TOKEN")
        self.assertEqual(requests[1].get_header("Authorization"),"Bearer FAKE_TEST_TOKEN")
        self.assertIsNone(requests[2].get_header("Authorization"))
        self.assertEqual(output.read_bytes(),b"archive")

    def test_direct_api_binary_supported(self):
        requests,output=self.download(redirect=False)
        self.assertEqual(len(requests),2)
        self.assertEqual(output.read_bytes(),b"archive")

    def test_unapproved_redirect_blocked(self):
        with self.assertRaises(ValueError): self.download(bad_url="https://evil.test/x")

    def test_bad_original_bytes_blocked(self):
        for body in [b"archivf",b"archiv",b"archivex"]:
            with self.subTest(body=body),self.assertRaises(ValueError): self.download(body=body)

    def test_missing_token_rejected_without_network(self):
        with mock.patch.object(m.urllib.request,"build_opener") as create:
            for token in ["","x\ny","x\ry"]:
                with self.assertRaises(ValueError): m.download_original(pathlib.Path("unused"),token)
            create.assert_not_called()

    def test_export_identity_and_event_gates_before_network(self):
        baseline={"GITHUB_REPOSITORY":m.SOURCE["repository"],"GITHUB_REF":"refs/heads/main", "GITHUB_EVENT_NAME":"push"}
        for changes in [{"GITHUB_REPOSITORY":"other/repo"},{"GITHUB_REF":"refs/heads/feature"},
                        {"GITHUB_EVENT_NAME":"pull_request"},{"GITHUB_EVENT_NAME":"issue_comment"}]:
            with self.subTest(changes=changes),mock.patch.dict(os.environ,{**baseline,**changes},clear=True), \
                    mock.patch.object(m,"download_original") as download:
                with self.assertRaises(ValueError): m.export(pathlib.Path("unused"))
                download.assert_not_called()


class SourceSelectionTests(unittest.TestCase):
    def test_selected_source_roundtrip_receipt_and_legacy_pins_preserved(self):
        original_pins=copy.deepcopy(m.SOURCE)
        data=b"archive-data"
        source={**m.SOURCES["2026-10-25"],"bytes":len(data),"sha256":sha(data)}
        baseline={"GITHUB_REPOSITORY":source["repository"],"GITHUB_REF":"refs/heads/main",
                  "GITHUB_EVENT_NAME":"workflow_dispatch","GH_TOKEN":"FAKE_TEST_TOKEN"}
        split=m.split_archive
        def split_small(original,output,size,digest):
            return split(original,output,size,digest,chunk_bytes=3)
        def download(target,token,selected):
            self.assertEqual(selected,source)
            target.write_bytes(data)
        with tempfile.TemporaryDirectory() as directory:
            output=pathlib.Path(directory)/"parts"
            with mock.patch.dict(os.environ,baseline,clear=True), \
                 mock.patch.object(m,"download_original",side_effect=download), \
                 mock.patch.object(m,"split_archive",side_effect=split_small), \
                 contextlib.redirect_stdout(io.StringIO()):
                m.export(output,source)
            receipt=json.loads((output/"source_receipt.json").read_text())
            self.assertEqual(receipt["source"],source)
            self.assertEqual(receipt["independent_custody"],"NOT_PROVEN_BY_EXPORT")
            restored=pathlib.Path(directory)/"restored.zip"
            m.reassemble(output/"manifest.json",restored,len(data),sha(data))
            self.assertEqual(restored.read_bytes(),data)
        self.assertEqual(m.SOURCE,original_pins)

    def test_cli_selection_and_legacy_export_default(self):
        for extra,key in [([],"2026-10-12"),(["--source","2026-10-25"],"2026-10-25")]:
            with self.subTest(key=key), \
                 mock.patch.object(sys,"argv",["transport","export","parts",*extra]), \
                 mock.patch.object(m,"export") as export:
                self.assertEqual(m.main(),0)
                export.assert_called_once_with(pathlib.Path("parts"),m.SOURCES[key])

    def test_unknown_cli_source_rejected_without_export(self):
        with mock.patch.object(sys,"argv",["transport","export","parts","--source","latest"]), \
             mock.patch.object(m,"export") as export,contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error: m.main()
            self.assertEqual(error.exception.code,2)
            export.assert_not_called()

    def test_legacy_offline_cli_defaults_preserved(self):
        with mock.patch.object(sys,"argv",["transport","reassemble","manifest","restored"]), \
             mock.patch.object(m,"reassemble") as assemble,contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(m.main(),0)
            assemble.assert_called_once_with(pathlib.Path("manifest"),pathlib.Path("restored"),
                                            691152334,"5940080108e52b01c8fe899abf47c2c773f8ca56220b73ff1df9ba4079cd92d4")


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.text=(ROOT/".github/workflows/repository-backup-transport.yml").read_text()

    def test_no_recurring_or_comment_trigger(self):
        self.assertNotIn("schedule:",self.text)
        self.assertNotIn("issue_comment:",self.text)
        self.assertIn("workflow_dispatch:",self.text)

    def test_readonly_source_permissions_no_secrets(self):
        self.assertNotIn(": write",self.text)
        self.assertNotIn("secrets.",self.text)
        self.assertIn("actions: read",self.text)
        self.assertIn("GH_TOKEN: ${{ github.token }}",self.text)

    def test_existing_backup_and_mirror_not_invoked(self):
        self.assertNotIn("git push",self.text)
        self.assertNotIn("bundle create",self.text)
        self.assertNotIn("repository-backup-bundle.yml",self.text)

    def test_export_depends_on_tests_and_main(self):
        self.assertIn("needs: test",self.text)
        self.assertIn("github.ref == 'refs/heads/main'",self.text)
        self.assertIn("github.event_name == 'push'",self.text)
        self.assertIn("github.event_name == 'workflow_dispatch'",self.text)

    def test_part_artifacts_separate_and_below_transport_limit(self):
        self.assertIn('--source 2026-10-25',self.text)
        self.assertIn('group: existing-backup-transport-12592912872',self.text)
        self.assertIn('name: pd-backup-12592912872-manifest',self.text)
        for index in range(1,5):
            self.assertIn(f"pd-backup-12592912872-part-{index:02d}",self.text)
            self.assertIn(f"archive.part{index:04d}",self.text)
        self.assertEqual(self.text.count("compression-level: 0"),4)
        self.assertLess(m.CHUNK_BYTES + 1024*1024,536870912)
        for source in m.SOURCES.values():
            self.assertEqual((source["bytes"]+m.CHUNK_BYTES-1)//m.CHUNK_BYTES,4)

    def test_actions_exact_pinned_and_no_credential_persistence(self):
        self.assertEqual(self.text.count("persist-credentials: false"),2)
        for line in self.text.splitlines():
            if "uses:" in line:
                self.assertRegex(line,r"uses: actions/[a-z-]+@[0-9a-f]{40}(?:\s|$)")


class NativeGitFixtureTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which("git"),"native Git unavailable")
    def test_real_git_bundle_roundtrip_and_restore(self):
        with tempfile.TemporaryDirectory() as directory:
            root=pathlib.Path(directory); repo=root/"repo"; repo.mkdir()
            env={**os.environ,"GIT_CONFIG_NOSYSTEM":"1","GIT_CONFIG_GLOBAL":os.devnull}
            def git(*args,cwd=repo):
                result=subprocess.run(["git",*args],cwd=cwd,env=env,check=True,
                                      stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
                return result.stdout.strip()
            git("init","-b","main")
            (repo/"sample.txt").write_bytes(b"Synthetic acceptance fixture, not production evidence.\n")
            git("add","sample.txt")
            git("-c","user.name=Offline Fixture","-c","user.email=fixture@example.invalid", "commit","-m","fixture")
            git("tag","preserved-history")
            original=root/"fixture.bundle"
            git("bundle","create",str(original),"--all")
            before=m.digest(original)
            parts=root/"parts"; m.split_archive(original,parts,*before,chunk_bytes=1024)
            restored=root/"restored.bundle"; m.reassemble(parts/"manifest.json",restored,*before)
            self.assertEqual(m.digest(restored),before)
            git("bundle","verify",str(restored))
            mirror=root/"restored.git"
            git("clone","--mirror",str(restored),str(mirror),cwd=root)
            git("--git-dir="+str(mirror),"fsck","--full",cwd=root)
            source_refs=git("show-ref").splitlines()
            restored_refs=git("--git-dir="+str(mirror),"show-ref",cwd=root).splitlines()
            self.assertEqual(sorted(source_refs),sorted(restored_refs))


if __name__ == "__main__":
    unittest.main()

