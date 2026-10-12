"""Lossless transport of one pinned existing recovery ZIP; never creates a backup.

Only ``export`` uses the network, with the existing Actions read token. The
original artifact is retained. ``reassemble`` is offline and verifies against
an independently supplied original digest/size before creating its output.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SOURCE = {
    "repository": "sbu001monterecco/por-derecho",
    "artifact_id": 11746464203,
    "name": "por-derecho-repository-recovery-bundle",
    "run_id": 38247928668,
    "head_sha": "7e7fc75da126b0218da7d5c337708ad841ed5bd3",
    "bytes": 691152334,
    "sha256": "5940080108e52b01c8fe899abf47c2c773f8ca56220b73ff1df9ba4079cd92d4",
}
CHUNK_BYTES = 192 * 1024 * 1024
BLOCK = 1024 * 1024
SCHEMA = "por-derecho.existing-backup-transport.v1"


def require(ok: bool, label: str) -> None:
    if not ok:
        raise ValueError(label)


def integer(value: object) -> bool:
    return type(value) is int and value > 0


def digest(path: Path) -> tuple[int, str]:
    require(path.is_file() and not path.is_symlink(), "regular_file_required")
    total, h = 0, hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(BLOCK), b""):
            total += len(block)
            h.update(block)
    return total, h.hexdigest()


def write_json(path: Path, value: dict) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, sort_keys=True, indent=2)
        stream.write("\n")


def split_archive(source: Path, output: Path, expected_bytes: int,
                  expected_sha256: str, chunk_bytes: int = CHUNK_BYTES) -> dict:
    require(integer(expected_bytes), "invalid_original_size")
    require(isinstance(expected_sha256, str) and
            bool(re.fullmatch(r"[0-9a-f]{64}", expected_sha256)), "invalid_digest")
    require(integer(chunk_bytes) and chunk_bytes <= CHUNK_BYTES, "invalid_chunk_size")
    require((expected_bytes + chunk_bytes - 1) // chunk_bytes <= 64, "too_many_parts")
    require(digest(source) == (expected_bytes, expected_sha256), "original_mismatch")
    output.mkdir(parents=False, exist_ok=False)
    parts = []
    with source.open("rb") as stream:
        for index in range(1, (expected_bytes + chunk_bytes - 1) // chunk_bytes + 1):
            name = f"archive.part{index:04d}"
            remaining = min(chunk_bytes, expected_bytes - (index - 1) * chunk_bytes)
            size, h = 0, hashlib.sha256()
            with (output / name).open("xb") as target:
                while remaining:
                    block = stream.read(min(BLOCK, remaining))
                    require(bool(block), "source_truncated")
                    target.write(block)
                    h.update(block)
                    size += len(block)
                    remaining -= len(block)
            parts.append({"name": name, "bytes": size, "sha256": h.hexdigest()})
        require(stream.read(1) == b"", "source_grew")
    require(digest(source) == (expected_bytes, expected_sha256), "source_changed")
    manifest = {"schema": SCHEMA, "original_bytes": expected_bytes,
                "original_sha256": expected_sha256, "chunk_bytes": chunk_bytes,
                "parts": parts, "independent_custody": "NOT_PROVEN_BY_EXPORT"}
    write_json(output / "manifest.json", manifest)
    return manifest


def reassemble(manifest_path: Path, output: Path, expected_bytes: int,
               expected_sha256: str) -> None:
    require(integer(expected_bytes), "invalid_original_size")
    require(isinstance(expected_sha256, str) and
            bool(re.fullmatch(r"[0-9a-f]{64}", expected_sha256)), "invalid_digest")
    require(manifest_path.is_file() and not manifest_path.is_symlink(), "manifest_required")
    require(manifest_path.stat().st_size <= BLOCK, "oversized_manifest")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    require(isinstance(manifest, dict), "invalid_manifest")
    require(manifest.get("schema") == SCHEMA, "schema_mismatch")
    require(integer(manifest.get("original_bytes")) and
            manifest.get("original_bytes") == expected_bytes and
            manifest.get("original_sha256") == expected_sha256, "untrusted_original_pin")
    chunk = manifest.get("chunk_bytes")
    require(integer(chunk) and chunk <= CHUNK_BYTES, "invalid_chunk_size")
    parts = manifest.get("parts")
    require(isinstance(parts, list) and 0 < len(parts) <= 64, "invalid_parts")
    require(len(parts) == (expected_bytes + chunk - 1) // chunk, "part_count_mismatch")
    for i, part in enumerate(parts, 1):
        require(isinstance(part, dict), "invalid_part")
        require(part.get("name") == f"archive.part{i:04d}", "part_name_or_order")
        require(integer(part.get("bytes")) and
                part.get("bytes") == min(chunk, expected_bytes - (i - 1) * chunk),
                "part_size_mismatch")
        require(isinstance(part.get("sha256"), str) and
                bool(re.fullmatch(r"[0-9a-f]{64}", part["sha256"])), "invalid_part_digest")
    require(not output.exists() and not output.is_symlink(), "output_exists")
    temporary = None
    try:
        fd, temporary = tempfile.mkstemp(prefix=".backup-assembly-", dir=output.parent)
        total, whole = 0, hashlib.sha256()
        with os.fdopen(fd, "wb") as target:
            for part in parts:
                path = manifest_path.parent / part["name"]
                require(path.is_file() and not path.is_symlink(), "part_missing_or_symlink")
                size, h = 0, hashlib.sha256()
                with path.open("rb") as stream:
                    for block in iter(lambda: stream.read(BLOCK), b""):
                        size += len(block)
                        require(size <= part["bytes"], "oversized_part")
                        h.update(block)
                        whole.update(block)
                        target.write(block)
                require((size, h.hexdigest()) == (part["bytes"], part["sha256"]),
                        "part_integrity_mismatch")
                total += size
            require((total, whole.hexdigest()) == (expected_bytes, expected_sha256),
                    "original_integrity_mismatch")
            target.flush()
            os.fsync(target.fileno())
        # Atomic no-overwrite publication; output and temporary share a filesystem.
        os.link(temporary, output)
    finally:
        if temporary is not None:
            Path(temporary).unlink(missing_ok=True)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def approved_download_url(url: str) -> bool:
    parsed = urllib.parse.urlsplit(url)
    host = (parsed.hostname or "").lower()
    return (parsed.scheme == "https" and parsed.username is None and
            parsed.password is None and parsed.port in (None, 443) and
            (host.endswith(".blob.core.windows.net") or
             host.endswith(".actions.githubusercontent.com")))


def verify_metadata(meta: dict) -> None:
    require(isinstance(meta, dict), "invalid_metadata")
    run = meta.get("workflow_run", {})
    require(isinstance(run, dict), "invalid_source_run")
    require(meta.get("id") == SOURCE["artifact_id"] and
            meta.get("name") == SOURCE["name"] and meta.get("expired") is False and
            meta.get("size_in_bytes") == SOURCE["bytes"] and
            meta.get("digest") == "sha256:" + SOURCE["sha256"] and
            run.get("id") == SOURCE["run_id"] and
            run.get("head_sha") == SOURCE["head_sha"] and
            run.get("head_branch") == "main" and
            run.get("repository_id") == 1289596840 and
            run.get("head_repository_id") == 1289596840,
            "provider_metadata_mismatch")


def download_original(target: Path, token: str) -> dict:
    require(bool(token) and "\n" not in token and "\r" not in token, "token_missing")
    base = ("https://api.github.com/repos/" + SOURCE["repository"] +
            "/actions/artifacts/" + str(SOURCE["artifact_id"]))
    headers = {"Authorization": "Bearer " + token, "Accept": "application/vnd.github+json",
               "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "PD-backup-transport"}
    opener = urllib.request.build_opener(NoRedirect())
    with opener.open(urllib.request.Request(base, headers=headers), timeout=60) as response:
        payload = response.read(BLOCK + 1)
        require(len(payload) <= BLOCK, "oversized_metadata")
    metadata = json.loads(payload)
    verify_metadata(metadata)
    try:
        response = opener.open(urllib.request.Request(base + "/zip", headers=headers), timeout=60)
    except urllib.error.HTTPError as error:
        try:
            require(error.code == 302, "download_redirect_required")
            location = error.headers.get("Location", "")
            require(approved_download_url(location), "unapproved_download_origin")
        finally:
            error.close()
        # Deliberately no Authorization header on the signed storage request.
        response = opener.open(urllib.request.Request(location, headers={
            "User-Agent": "PD-backup-transport"}), timeout=60)
    with response, target.open("xb") as stream:
        size, h = 0, hashlib.sha256()
        for block in iter(lambda: response.read(BLOCK), b""):
            size += len(block)
            require(size <= SOURCE["bytes"], "oversized_original")
            h.update(block)
            stream.write(block)
    require((size, h.hexdigest()) == (SOURCE["bytes"], SOURCE["sha256"]),
            "download_integrity_mismatch")
    # Do not retain response headers or signed URLs.
    return metadata


def export(output: Path) -> None:
    require(os.environ.get("GITHUB_REPOSITORY") == SOURCE["repository"], "repository_mismatch")
    require(os.environ.get("GITHUB_REF") == "refs/heads/main", "main_required")
    require(os.environ.get("GITHUB_EVENT_NAME") in ("push", "workflow_dispatch"), "event_rejected")
    with tempfile.TemporaryDirectory(prefix="pd-original-transport-") as work:
        original = Path(work) / "original.zip"
        download_original(original, os.environ.get("GH_TOKEN", ""))
        manifest = split_archive(original, output, SOURCE["bytes"], SOURCE["sha256"])
        require(len(manifest["parts"]) == 4, "fixed_transport_count_mismatch")
        # Local runner reconstruction verifies losslessness; off-platform custody stays open.
        reassemble(output / "manifest.json", Path(work) / "reassembled.zip",
                   SOURCE["bytes"], SOURCE["sha256"])
        write_json(output / "source_receipt.json", {
            "source": SOURCE, "export_run_id": os.environ.get("GITHUB_RUN_ID"),
            "export_code_sha": os.environ.get("GITHUB_SHA"),
            "original_download": "HASH_AND_SIZE_VERIFIED",
            "runner_reassembly": "EXACT_ORIGINAL_HASH_VERIFIED",
            "source_artifact_mutated": False,
            "independent_custody": "NOT_PROVEN_BY_EXPORT"})
    print("TRANSPORT_READY parts=4 original_sha256=" + SOURCE["sha256"])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    ex = commands.add_parser("export")
    ex.add_argument("output", type=Path)
    ra = commands.add_parser("reassemble")
    ra.add_argument("manifest", type=Path)
    ra.add_argument("output", type=Path)
    ra.add_argument("--expected-bytes", type=int, default=SOURCE["bytes"])
    ra.add_argument("--expected-sha256", default=SOURCE["sha256"])
    args = parser.parse_args()
    try:
        if args.command == "export":
            export(args.output)
        else:
            reassemble(args.manifest, args.output, args.expected_bytes, args.expected_sha256)
            print("REASSEMBLY_HASH_VERIFIED")
    except (OSError, ValueError, KeyError, TypeError, RuntimeError):
        # Network exceptions can contain signed URLs; never print exception detail.
        print("TRANSPORT_BLOCKED: validation_or_access_failure")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
