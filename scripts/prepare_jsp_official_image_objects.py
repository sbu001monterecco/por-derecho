#!/usr/bin/env python3
"""Read-only evidence preparation; outputs only under /tmp, never commits or pushes.
The connected publisher must separately admit verified image bytes and provenance.
No OCR, retyped notice, invented image, private source or remote execution input.
"""
from __future__ import annotations
import base64
import hashlib
import io
import json
from pathlib import Path
import urllib.error
import urllib.request
import fitz
from PIL import Image

URL = 'https://www.boe.es/borme/dias/2017/08/10/pdfs/BORME-C-2017-7368.pdf'
OUT = Path('/tmp/jsp-official-image-objects')
OUT.mkdir(parents=True, exist_ok=True)
request = urllib.request.Request(URL, headers={'User-Agent': 'PorDerecho-OfficialSourceReview/1.0'})
with urllib.request.urlopen(request, timeout=45) as response:
    raw = response.read(2_000_001)
assert raw.startswith(b'%PDF-') and len(raw) <= 2_000_000, 'Invalid source bytes'
(OUT / 'BORME-C-2017-7368.pdf').write_bytes(raw)
pdf = fitz.open(stream=raw, filetype='pdf')
assert len(pdf) == 1, 'Source must be one page'
page = pdf[0]
text = page.get_text()
assert all(value in text for value in ['Quinto:', 'Explobeach', 'Sun Park', 'JOSILAC']), 'Wrong source'
first = page.search_for('Quinto:')
next_item = page.search_for('Sexto:')
assert len(first) == len(next_item) == 1, 'Ambiguous source anchors'
clip = fitz.Rect(110, first[0].y0 - 8, page.rect.width - 75, next_item[0].y0 - 8)
assert clip.height > 20 and clip.width > 300
source_hash = hashlib.sha256(raw).hexdigest()
records = []
for name, rect, scale in [
    ('borme-c-2017-7368-full-page.webp', page.rect, 1.5),
    ('borme-c-2017-7368-item-five.webp', clip, 2.5),
]:
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), clip=rect, alpha=False, colorspace=fitz.csRGB)
    image = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    buffer = io.BytesIO()
    image.save(buffer, format='WEBP', lossless=True, method=6, exact=True)
    data = buffer.getvalue()
    # Lossless encoding must preserve the exact rendered pixels.
    decoded = Image.open(io.BytesIO(data)).convert('RGB')
    assert decoded.size == image.size and decoded.tobytes() == image.tobytes()
    (OUT / name).write_bytes(data)
    git_sha = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    record = {
        'source_id': 'JSP-2017-S01', 'file': name,
        'repository_path': 'assets/evidence/jsp-2017/' + name,
        'operation': 'Unannotated pixel rendering from official PDF, lossless WebP encoding; not a certified original',
        'source_url': URL, 'source_sha256': source_hash, 'source_bytes': len(raw),
        'pdf_page': 1, 'printed_page': '8556', 'clip_points': list(rect),
        'scale': scale, 'width': image.width, 'height': image.height,
        'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
        'git_blob_sha': git_sha, 'pixels_verified_lossless': True,
    }
    records.append(record)
    encoded = base64.b64encode(data).decode('ascii')
    (OUT / (name + '.base64.txt')).write_text(encoded + '\n')
    print('IMAGE_METADATA ' + json.dumps(record, ensure_ascii=False))
    print('BEGIN_BASE64 ' + name)
    print(encoded)
    print('END_BASE64 ' + name)
manifest = {'control_id': 'PD-JSP-2017-OFFICIAL-IMAGES-20260905',
            'source': {'id': 'JSP-2017-S01', 'url': URL, 'sha256': source_hash, 'bytes': len(raw)},
            'derivatives': records, 'not_proof_of': ['meeting occurred', 'sale terms', 'criminal liability'],
            'publication_state': 'PREPARED_OBJECTS_NOT_COMMITTED_OR_DEPLOYED'}
(OUT / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
print('MANIFEST ' + json.dumps(manifest, ensure_ascii=False))
# Report real-host responses separately from local candidate or source-image tests.
for route in ['es/jsp-montelanza-concurso-liquidacion/', 'en/jsp-montelanza-insolvency-liquidation/']:
    target = 'https://sbu001monterecco.github.io/por-derecho/' + route
    try:
        with urllib.request.urlopen(urllib.request.Request(target, headers={'Cache-Control': 'no-cache'}), timeout=30) as r:
            content = r.read(2_000_000)
            print('LIVE_PROBE ' + json.dumps({'url': target, 'status': r.status, 'bytes': len(content), 'sha256': hashlib.sha256(content).hexdigest(), 'notice_marker': b'BORME-C-2017-7368' in content, 'image_marker': b'borme-c-2017-7368-item-five.webp' in content}))
    except (urllib.error.URLError, TimeoutError) as error:
        print('LIVE_PROBE ' + json.dumps({'url': target, 'error': str(error), 'status': getattr(error, 'code', None)}))
