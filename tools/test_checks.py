"""Checker regression tests. SPDX-License-Identifier: GPL-3.0-only"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class PublicationChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'tools').mkdir()
        shutil.copyfile(Path(__file__).with_name('check_public.py'), self.root / 'tools/check_public.py')
        self.patch = 'diff --git a/example.kt b/example.kt\n'
        (self.root / 'example.patch').write_text(self.patch, encoding='utf-8')
        self.manifest = {'patch': 'example.patch', 'patch_sha256': hashlib.sha256((self.root / 'example.patch').read_bytes()).hexdigest(),
                         'files': [{'path': 'example.kt', 'sha256': '0' * 64}]}

    def run_check(self, optimized=False):
        (self.root / 'manifest.json').write_text(json.dumps(self.manifest), encoding='utf-8')
        return subprocess.run([sys.executable, *(['-O'] if optimized else []), str(self.root / 'tools/check_public.py')], capture_output=True)

    def test_clean(self):
        for optimized in (False, True):
            self.assertEqual(self.run_check(optimized).returncode, 0)

    def test_bad_hash_even_when_optimized(self):
        self.manifest['patch_sha256'] = '0' * 64
        for optimized in (False, True):
            self.assertNotEqual(self.run_check(optimized).returncode, 0)

    def test_forbidden_artifact(self):
        (self.root / 'unexpected.apk').write_bytes(b'not-a-real-apk')
        self.assertNotEqual(self.run_check().returncode, 0)

    def test_manifest_mismatch(self):
        self.manifest['files'][0]['path'] = 'other.kt'
        self.assertNotEqual(self.run_check().returncode, 0)

    def test_traversal(self):
        self.manifest['patch'] = '../outside.patch'
        self.assertNotEqual(self.run_check().returncode, 0)

    def test_private_key_marker(self):
        marker = '-----BEGIN ' + 'PRIVATE KEY-----'
        (self.root / 'accidental.txt').write_text(marker, encoding='utf-8')
        self.assertNotEqual(self.run_check().returncode, 0)


if __name__ == '__main__':
    unittest.main()
