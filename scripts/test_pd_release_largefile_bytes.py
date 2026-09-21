"""Offline adversarial tests for exact-commit readback capability only."""
import base64
from copy import deepcopy
import hashlib
import unittest

from pd_release_controller import exact_repository_bytes

MERGE = '01df48e335d07d0f1068381a294f6b65917f1248'
PATH = 'assets/visuals/eg745-working-20260920/l1.png'


def metadata(raw, encoding='base64'):
    sha = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    return {'type': 'file', 'sha': sha, 'size': len(raw), 'encoding': encoding,
            'content': base64.encodebytes(raw).decode() if encoding == 'base64' else ''}


class FakeAPI:
    def __init__(self, contents, blob=None):
        self.contents, self.blob, self.calls = contents, blob, []

    def request(self, path):
        self.calls.append(path)
        if path == 'contents/'+PATH+'?ref='+MERGE:
            return deepcopy(self.contents)
        if path == 'git/blobs/'+self.contents['sha']:
            return deepcopy(self.blob)
        raise AssertionError('Unexpected API path: '+path)


class ExactBytesTests(unittest.TestCase):
    def test_small_and_empty_files_need_no_fallback(self):
        for raw in (b'', b'small file\n', b'\x00\xff\n'):
            api = FakeAPI(metadata(raw))
            self.assertEqual(raw, exact_repository_bytes(api, PATH, MERGE))
            self.assertEqual(len(api.calls), 1)

    def test_large_binary_uses_only_exact_git_blob(self):
        raw = b'\x00\xffbinary\n' * 200000
        api = FakeAPI(metadata(raw, 'none'), metadata(raw))
        self.assertEqual(raw, exact_repository_bytes(api, PATH, MERGE))
        self.assertEqual(api.calls, ['contents/'+PATH+'?ref='+MERGE,
                                    'git/blobs/'+metadata(raw)['sha']])

    def test_corrupt_content_rejected(self):
        value = metadata(b'expected')
        value['content'] = base64.b64encode(b'wrong!!!').decode()
        with self.assertRaisesRegex(ValueError, 'byte verification failed'):
            exact_repository_bytes(FakeAPI(value), PATH, MERGE)

    def test_size_mismatch_rejected(self):
        value = metadata(b'data'); value['size'] += 1
        with self.assertRaisesRegex(ValueError, 'byte verification failed'):
            exact_repository_bytes(FakeAPI(value), PATH, MERGE)

    def test_blob_identity_and_size_mismatch_rejected(self):
        contents = metadata(b'data', 'none')
        for key, replacement in [('sha', 'f'*40), ('size', 99)]:
            blob = metadata(b'data'); blob[key] = replacement
            with self.assertRaisesRegex(ValueError, 'metadata mismatch'):
                exact_repository_bytes(FakeAPI(contents, blob), PATH, MERGE)

    def test_invalid_blob_sha_cannot_construct_arbitrary_url(self):
        for bad in ('../x', 'https://example.invalid', 'g'*40, None):
            value = metadata(b'data', 'none'); value['sha'] = bad
            api = FakeAPI(value)
            with self.assertRaisesRegex(ValueError, 'identity/size'):
                exact_repository_bytes(api, PATH, MERGE)
            self.assertEqual(len(api.calls), 1)

    def test_missing_or_unknown_encoding_fails_closed(self):
        for encoding in (None, 'utf-8', 'unknown'):
            value = metadata(b'data'); value['encoding'] = encoding
            api = FakeAPI(value)
            with self.assertRaisesRegex(ValueError, 'bytes unavailable'):
                exact_repository_bytes(api, PATH, MERGE)
            self.assertEqual(len(api.calls), 1)

    def test_blob_without_bytes_fails_closed(self):
        value = metadata(b'data', 'none')
        with self.assertRaisesRegex(ValueError, 'bytes unavailable'):
            exact_repository_bytes(FakeAPI(value, value), PATH, MERGE)

    def test_invalid_base64_rejected(self):
        for bad in ('????', 'A', '\u2603'):
            value = metadata(b'data'); value['content'] = bad
            with self.assertRaisesRegex(ValueError, 'Invalid exact-file base64'):
                exact_repository_bytes(FakeAPI(value), PATH, MERGE)

    def test_symlink_submodule_and_directory_rejected(self):
        for addition in ({'target':'x'}, {'submodule_git_url':'https://example.invalid'}, {'type':'dir'}):
            value = metadata(b'data'); value.update(addition)
            with self.assertRaisesRegex(ValueError, 'regular repository file'):
                exact_repository_bytes(FakeAPI(value), PATH, MERGE)

    def test_unsupported_or_malformed_size_rejected(self):
        for size in (-1, 100*1024*1024+1, True, '5', None):
            value = metadata(b'data'); value['size'] = size
            with self.assertRaisesRegex(ValueError, 'identity/size'):
                exact_repository_bytes(FakeAPI(value), PATH, MERGE)

    def test_unsafe_repository_path_rejected_before_api(self):
        api = FakeAPI(metadata(b'data'))
        with self.assertRaises(ValueError):
            exact_repository_bytes(api, '../secret', MERGE)
        self.assertEqual(api.calls, [])


if __name__ == '__main__':
    unittest.main()
