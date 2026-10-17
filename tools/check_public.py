#!/usr/bin/env python3
"""Offline publication checks; no uploads. SPDX-License-Identifier: GPL-3.0-only"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def safe_path(value):
    require(isinstance(value, str) and value and '\\' not in value, 'Invalid repository path')
    require(not value.startswith('/') and all(part not in ('', '.', '..') for part in value.split('/')), 'Unsafe repository path')
    require((ROOT / value).resolve().is_relative_to(ROOT.resolve()), 'Path escapes repository')
    return ROOT / value


def main():
    manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
    patch = safe_path(manifest['patch'])
    require(hashlib.sha256(patch.read_bytes()).hexdigest() == manifest['patch_sha256'], 'Patch hash mismatch')
    content = patch.read_text(encoding='utf-8')
    paths = re.findall(r'^diff --git a/(\S+) b/(\S+)$', content, re.M)
    require(paths and all(a == b for a, b in paths), 'Invalid patch paths')
    require(len(paths) == len(set(a for a, _ in paths)), 'Duplicate patch path')
    require(sorted(a for a, _ in paths) == sorted(f['path'] for f in manifest['files']), 'Manifest path mismatch')
    require('GIT binary patch' not in content, 'Binary patch is forbidden')
    for entry in manifest['files']:
        safe_path(entry['path'])
        require(re.fullmatch(r'[0-9a-f]{64}', entry['sha256']), 'Invalid source hash')
    forbidden = {'.apk', '.aab', '.zip', '.jks', '.keystore', '.pk8', '.p7b', '.pem', '.p12', '.pfx', '.key', '.so', '.jar', '.aar'}
    for path in ROOT.rglob('*'):
        if not path.is_file() or '.git' in path.relative_to(ROOT).parts or '__pycache__' in path.parts:
            continue
        require(not path.is_symlink(), f'Symlink is forbidden: {path.name}')
        require(path.suffix.lower() not in forbidden, f'Forbidden artifact: {path.name}')
        data = path.read_bytes()
        require(b'\0' not in data, f'Unexpected binary: {path.name}')
        text = data.decode('utf-8')
        require(not re.search(r'-----BEGIN (?:RSA |EC |OPENSSH |ENCRYPTED )?PRIVATE KEY-----', text), f'Private key: {path.name}')
        require(not re.search(r'[A-Za-z]:[\\/]Users[\\/]', text, re.I), f'Personal path: {path.name}')
        require(not re.search(r'gh[pousr]_[A-Za-z0-9]{30,}', text), f'Token: {path.name}')
    print(f'PASS: patch hash, {len(paths)} source paths, public artifact and common secret checks')


if __name__ == '__main__':
    main()
