#!/usr/bin/env python3
"""Offline publication checks; no uploads. SPDX-License-Identifier: GPL-3.0-only"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
    patch = ROOT / manifest['patch']
    assert hashlib.sha256(patch.read_bytes()).hexdigest() == manifest['patch_sha256'], 'Patch hash mismatch'
    content = patch.read_text(encoding='utf-8')
    paths = re.findall(r'^diff --git a/(\S+) b/(\S+)$', content, re.M)
    assert paths and all(a == b for a, b in paths)
    assert sorted(a for a, _ in paths) == sorted(f['path'] for f in manifest['files'])
    assert 'GIT binary patch' not in content
    forbidden = {'.apk', '.aab', '.zip', '.jks', '.keystore', '.pk8', '.p7b', '.pem', '.p12', '.pfx', '.key', '.so', '.jar', '.aar'}
    for path in ROOT.rglob('*'):
        if not path.is_file() or '.git' in path.relative_to(ROOT).parts or '__pycache__' in path.parts:
            continue
        assert path.suffix.lower() not in forbidden, f'Forbidden artifact: {path.name}'
        data = path.read_bytes()
        assert b'\0' not in data, f'Unexpected binary: {path.name}'
        text = data.decode('utf-8')
        assert not re.search(r'-----BEGIN (?:RSA |EC |OPENSSH |ENCRYPTED )?PRIVATE KEY-----', text), f'Private key: {path.name}'
        assert not re.search(r'[A-Za-z]:[\\/]Users[\\/]', text, re.I), f'Personal path: {path.name}'
        assert not re.search(r'gh[pousr]_[A-Za-z0-9]{30,}', text), f'Token: {path.name}'
    print(f'PASS: patch hash, {len(paths)} source paths, public artifact and common secret checks')


if __name__ == '__main__':
    main()
