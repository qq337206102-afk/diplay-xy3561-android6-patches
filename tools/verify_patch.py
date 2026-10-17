#!/usr/bin/env python3
"""Apply to an independent upstream checkout and verify every source hash.

SPDX-License-Identifier: GPL-3.0-only
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

from check_public import ROOT, main as check_public, require


def git(*args, cwd=None):
    return subprocess.check_output(['git', *args], cwd=cwd, stderr=subprocess.STDOUT)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--upstream', type=Path, help='Existing upstream checkout; read-only, no checkout/reset')
    args = parser.parse_args()
    check_public()
    manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
    require(manifest['upstream'] == 'https://github.com/shihabal3amri/DiPlay', 'Unexpected upstream URL')
    require(len(manifest['base_commit']) == 40 and all(c in '0123456789abcdef' for c in manifest['base_commit']), 'Invalid base commit')
    with tempfile.TemporaryDirectory(prefix='diplay-patch-check-') as folder:
        temp = Path(folder)
        upstream = args.upstream.resolve() if args.upstream else temp / 'upstream'
        if not args.upstream:
            git('clone', '--no-checkout', '--filter=blob:none', manifest['upstream'] + '.git', str(upstream))
        require(git('cat-file', '-t', manifest['base_commit'], cwd=upstream).strip() == b'commit', 'Base is not a commit')
        # A separate index and worktree avoid any mutation of an existing developer checkout.
        import os
        env = dict(os.environ, GIT_INDEX_FILE=str(temp / 'index'))
        worktree = temp / 'applied'
        worktree.mkdir()
        for command in [
            ['git', 'read-tree', manifest['base_commit']],
            ['git', '-c', 'core.autocrlf=false', 'checkout-index', '--all', '--prefix=' + worktree.as_posix() + '/'],
        ]:
            subprocess.run(command, cwd=upstream, env=env, check=True, stdout=subprocess.PIPE)
        git('init', '--quiet', cwd=worktree)
        git('config', 'core.autocrlf', 'false', cwd=worktree)
        patch = str(ROOT / manifest['patch'])
        git('apply', '--check', patch, cwd=worktree)
        git('apply', patch, cwd=worktree)
        for entry in manifest['files']:
            actual = hashlib.sha256((worktree / entry['path']).read_bytes()).hexdigest()
            require(actual == entry['sha256'], 'Applied source mismatch: ' + entry['path'])
    print(f"PASS: patch applies to {manifest['base_commit']}; all {len(manifest['files'])} source hashes match")


if __name__ == '__main__':
    main()
