#!/usr/bin/env python3
"""Capture the public Hackathon microsite; Python standard library + curl."""
import hashlib
import json
import re
import subprocess
import tempfile
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urldefrag, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://www.banxico.org.mx/hackathonspei/'
CSS_URL = re.compile(r'url\(\s*[\'\"]?([^\)\'\"]+)[\'\"]?\s*\)', re.I)
SOURCE_MAP = re.compile(r'sourceMappingURL=([^\s*]+)')

class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.external = set()
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if not value:
                continue
            if key in ('src', 'href', 'poster'):
                if value.startswith(('https://', 'http://')) and not value.startswith(BASE):
                    self.external.add(value)
                else:
                    self.refs.append(value)
            if key == 'style':
                self.refs.extend(CSS_URL.findall(value))

def references(path, data):
    text = data.decode('latin-1')
    if path.endswith('.html'):
        parser = References()
        parser.feed(text)
        return parser.refs, parser.external
    if path.endswith('.css'):
        return CSS_URL.findall(text) + re.findall(r'@import\s+[\'\"]([^\'\"]+)', text) + SOURCE_MAP.findall(text), set()
    if path.endswith('.js'):
        return SOURCE_MAP.findall(text), set()
    return [], set()

def local_path(url):
    if not url.startswith(BASE):
        return None
    relative = unquote(urlsplit(url).path[len(urlsplit(BASE).path):]) or 'index.html'
    path = ROOT / relative
    if not path.resolve().is_relative_to(ROOT) or relative.startswith(('.', 'scripts/', 'archive/')):
        raise ValueError(f'Unsafe path: {relative}')
    return relative

def main():
    queue = [BASE]
    visited, external, files, failures = set(), set(), [], []
    while queue:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)
        relative = local_path(url)
        if relative is None:
            external.add(url)
            continue
        if any(f['path'] == relative for f in files):
            continue
        with tempfile.TemporaryDirectory() as temp:
            dest = Path(temp) / 'body'
            result = subprocess.run(['curl', '--fail', '--silent', '--show-error', '--location',
                '--retry', '2', '--max-time', '60', '--output', str(dest),
                '--write-out', '%{content_type}', quote(url, safe=':/?=&%')], capture_output=True, text=True)
            if result.returncode:
                failures.append({'url': url, 'path': relative, 'error': result.stderr.strip()})
                print(f'FAILED {relative}', flush=True)
                continue
            data = dest.read_bytes()
        if 'text/html' in result.stdout and not relative.endswith('.html'):
            failures.append({'url': url, 'path': relative, 'error': 'Unexpected HTML response'})
            continue
        target = ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        files.append({'url': url, 'path': relative, 'bytes': len(data),
                      'sha256': hashlib.sha256(data).hexdigest(), 'content_type': result.stdout})
        print(f'OK {relative} ({len(data)} bytes)', flush=True)
        refs, links = references(relative, data)
        external.update(links)
        for ref in refs:
            if ref.startswith(('#', 'data:', 'mailto:', 'javascript:')):
                continue
            resolved = urldefrag(urljoin(url, ref))[0]
            if resolved not in visited:
                queue.append(resolved)
    manifest = {'source': BASE, 'captured_at': datetime.now(timezone.utc).isoformat(),
                'files': sorted(files, key=lambda f: f['path']),
                'external_links': sorted(external), 'failures': failures}
    (ROOT / 'archive').mkdir(exist_ok=True)
    (ROOT / 'archive/manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    print(f'{len(files)} files; {len(failures)} unavailable resources')
    if any(not f['path'].endswith('.map') for f in failures):
        raise SystemExit(1)

if __name__ == '__main__':
    main()
