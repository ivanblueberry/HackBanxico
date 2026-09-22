#!/usr/bin/env python3
"""Verify archive hashes and all local HTML/CSS references without network access."""
import hashlib
import json
from urllib.parse import urljoin, urldefrag
from archive_site import ROOT, BASE, local_path, references

manifest = json.loads((ROOT / 'archive/manifest.json').read_text())
recovered = json.loads((ROOT / 'archive/recovered.json').read_text())
deployment = json.loads((ROOT / 'archive/deployment.json').read_text())
files = manifest['files'] + recovered['files'] + deployment['files']
errors = []
for item in files:
    path = ROOT / item['path']
    if not path.is_file():
        errors.append(f'Missing: {item["path"]}')
        continue
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != item['sha256']:
        errors.append(f'Hash mismatch: {item["path"]}')
    refs, _ = references(item['path'], data)
    for ref in refs:
        if ref.startswith(('#', 'data:', 'mailto:', 'javascript:')):
            continue
        url = urldefrag(urljoin(item.get('url', BASE + item['path']), ref))[0]
        relative = local_path(url)
        if relative and not (ROOT / relative).is_file():
            errors.append(f'Broken reference: {item["path"]} -> {relative}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'OK: {len(files)} files verified; all local references resolve.')
