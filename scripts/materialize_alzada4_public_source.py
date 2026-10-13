#!/usr/bin/env python3
"""One-shot, create-only admission of an authorised public five-page facsimile.

No private source is fetched. No main, tag, secret, permission, release or unrelated
path is written. A branch lease and exact size/SHA checks fail closed. The source
PNG comprises the five real, privacy-reviewed document pages, not a hidden payload.
"""
from __future__ import annotations
import base64
import hashlib
import json
import os
import struct
import subprocess
import time
import urllib.request
import zlib

REPO = 'sbu001monterecco/por-derecho'
BRANCH = 'publication/alzada4-source-perimeter-20261013'
ROOT = 'evidence/public/2026-10-13-alzada4'
SOURCE = 'https://share.carryo.io/GD9EDba1RzJRPP2x/_assets/images/alzada4-source-strip.png?v=1'
PNG_HASH = '96a3863a425dfac2cb4e0d792b34e284df08a41a6b99889226d530afa6cc8dc8'
PDF_HASH = '67d1343d0992890d7564d08ca640d206b42292d0bdcbccf8a196944708195eea'
PNG_BYTES = 1581748
PDF_BYTES = 1583908
ALLOWED = {ROOT + '/source-strip.png', ROOT + '/decision-full-public-facsimile.pdf', ROOT + '/admission-receipt.json'}


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def gh(endpoint: str, method: str = 'GET', payload: dict | None = None) -> dict:
    args = ['gh', 'api', '--method', method, 'repos/' + REPO + '/' + endpoint]
    data = None
    if payload is not None:
        args += ['--input', '-']
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    done = subprocess.run(args, input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90, check=False)
    if done.returncode:
        raise RuntimeError('GitHub operation failed: ' + endpoint + ': ' + done.stderr.decode('utf-8', 'replace')[:700])
    return json.loads(done.stdout)


def build_pdf(raw: bytes, count: int = 5, width_pt: float = 595.303955078125, height_pt: float = 841.8897705078125) -> bytes:
    if raw[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('Not PNG')
    k = 8
    dat = []
    W = H = None
    while k < len(raw):
        if k + 12 > len(raw):
            raise ValueError('Truncated PNG chunk')
        n = int.from_bytes(raw[k:k+4], 'big')
        typ = raw[k+4:k+8]
        data = raw[k+8:k+8+n]
        crc = int.from_bytes(raw[k+8+n:k+12+n], 'big')
        if k + n + 12 > len(raw) or zlib.crc32(typ + data) & 0xffffffff != crc:
            raise ValueError('PNG CRC mismatch')
        if typ == b'IHDR':
            W, H, depth, color, comp, flt, interlace = struct.unpack('>IIBBBBB', data)
            if (W, H, depth, color, comp, flt, interlace) != (1191, 8420, 8, 2, 0, 0, 0):
                raise ValueError('Unexpected five-page raster specification')
        elif typ == b'IDAT':
            dat.append(data)
        elif typ == b'IEND':
            break
        k += n + 12
    if not W or not H or H % count:
        raise ValueError('Bad dimensions')
    stream = b''.join(dat)
    if len(zlib.decompress(stream)) != H * (1 + W * 3):
        raise ValueError('Invalid raster length')
    s = lambda text: text.encode('ascii')
    objs = {1: b'<< /Type /Catalog /Pages 2 0 R >>'}
    kids = []
    objs[3] = s(f'<< /Type /XObject /Subtype /Image /Width {W} /Height {H} /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /FlateDecode /DecodeParms << /Predictor 15 /Colors 3 /BitsPerComponent 8 /Columns {W} >> /Length {len(stream)} >>\nstream\n') + stream + b'\nendstream'
    for i in range(count):
        pg = 4 + 2*i
        ct = pg + 1
        kids.append(f'{pg} 0 R')
        Wp = f'{width_pt:.8f}'
        Hp = f'{height_pt:.8f}'
        content = s(f'q 0 0 {Wp} {Hp} re W n {Wp} 0 0 {height_pt*count:.8f} 0 {-height_pt*(count-1-i):.8f} cm /Im0 Do Q\n')
        objs[pg] = s(f'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {Wp} {Hp}] /Resources << /XObject << /Im0 3 0 R >> >> /Contents {ct} 0 R >>')
        objs[ct] = s(f'<< /Length {len(content)} >>\nstream\n') + content + b'endstream'
    objs[2] = s(f'<< /Type /Pages /Kids [{" ".join(kids)}] /Count {count} >>')
    info = max(objs) + 1
    objs[info] = b'<< /Title (Alzada 4/2026 - full five-page privacy facsimile) /Producer (Por Derecho - deterministic public image facsimile) /Subject (13 October 2026 decision. All five pages retained. Not the digitally signed original.) >>'
    out = bytearray(b'%PDF-1.4\n')
    offs = [0]
    for i in range(1, max(objs) + 1):
        offs.append(len(out))
        out.extend(s(f'{i} 0 obj\n'))
        out.extend(objs[i])
        out.extend(b'\nendobj\n')
    pos = len(out)
    out.extend(s(f'xref\n0 {len(offs)}\n0000000000 65535 f \n'))
    for off in offs[1:]:
        out.extend(s(f'{off:010d} 00000 n \n'))
    out.extend(s(f'trailer\n<< /Size {len(offs)} /Root 1 0 R /Info {info} 0 R >>\nstartxref\n{pos}\n%%EOF\n'))
    return bytes(out)


def main() -> None:
    if os.environ.get('GITHUB_REPOSITORY') != REPO or os.environ.get('GITHUB_REF') != 'refs/heads/' + BRANCH:
        raise RuntimeError('Refusing execution outside the exact authorised non-main branch')
    expected = os.environ.get('GITHUB_SHA', '')
    if len(expected) != 40 or any(c not in '0123456789abcdef' for c in expected):
        raise RuntimeError('Invalid event SHA')
    head = gh('git/ref/heads/' + BRANCH)['object']['sha']
    if head != expected:
        raise RuntimeError('Branch moved; refresh the candidate, never force')
    commit = gh('git/commits/' + head)
    tree = gh('git/trees/' + commit['tree']['sha'] + '?recursive=1')
    if tree.get('truncated'):
        raise RuntimeError('Repository tree incomplete; no admission performed')
    existing = {x['path']: x['sha'] for x in tree['tree'] if x.get('type') == 'blob'}
    public_paths = [ROOT + '/source-strip.png', ROOT + '/decision-full-public-facsimile.pdf']
    if any(p in existing for p in public_paths):
        for p, h in zip(public_paths, [PNG_HASH, PDF_HASH]):
            if p not in existing:
                raise RuntimeError('Partial pre-existing admission requires explicit reconciliation')
            blob = gh('git/blobs/' + existing[p])
            if digest(base64.b64decode(blob['content'])) != h:
                raise RuntimeError('Different pre-existing source; refusing replacement')
        print('Exact source already admitted; no write performed')
        return
    raw = None
    for attempt in range(3):
        try:
            request = urllib.request.Request(SOURCE, headers={'User-Agent': 'PorDerecho-Exact-Public-Source-Admission', 'Cache-Control': 'no-cache'})
            with urllib.request.urlopen(request, timeout=40) as response:
                raw = response.read(PNG_BYTES + 1)
            break
        except Exception:
            if attempt == 2:
                raise
            time.sleep(3 * (attempt + 1))
    if raw is None or len(raw) != PNG_BYTES or digest(raw) != PNG_HASH:
        raise RuntimeError('Public raster size or fingerprint mismatch')
    pdf = build_pdf(raw)
    if len(pdf) != PDF_BYTES or digest(pdf) != PDF_HASH:
        raise RuntimeError('PDF differs from the locally reviewed deterministic facsimile')
    receipt = {
        'control_id': 'PD-LAJ-20-26-20260924-01', 'master_parent': 'GC-LAJ-021',
        'status': 'EXACT_PUBLIC_FACSIMILE_ADMITTED_TO_NON_MAIN_BRANCH',
        'source_event_sha': expected, 'branch': BRANCH, 'pages': 5,
        'raster': {'path': public_paths[0], 'bytes': len(raw), 'sha256': PNG_HASH, 'width': 1191, 'height': 8420},
        'pdf': {'path': public_paths[1], 'bytes': len(pdf), 'sha256': PDF_HASH},
        'source_original_sha256': '9dcb9921ca6f8c7d3487c4516e55a81285144c94f22bb21d83e2ef581c02e857',
        'privacy': 'Retrieval identifier/QR removed; all five substantive pages and adverse reasoning retained. Image facsimile, not the electronically signed original.',
        'limits': ['Not a main merge', 'Not a deployment or browser-readback certificate', 'Not signature authentication or proof of underlying allegations']
    }
    outputs = {public_paths[0]: raw, public_paths[1]: pdf, ROOT + '/admission-receipt.json': (json.dumps(receipt, ensure_ascii=False, indent=2) + '\n').encode('utf-8')}
    if set(outputs) != ALLOWED or any(p in existing for p in outputs):
        raise RuntimeError('Create-only path contract failed')
    entries = []
    for path, content in outputs.items():
        blob = gh('git/blobs', 'POST', {'content': base64.b64encode(content).decode('ascii'), 'encoding': 'base64'})
        entries.append({'path': path, 'mode': '100644', 'type': 'blob', 'sha': blob['sha']})
    new_tree = gh('git/trees', 'POST', {'base_tree': commit['tree']['sha'], 'tree': entries})
    new_commit = gh('git/commits', 'POST', {'message': 'Admit exact privacy-reviewed Alzada 4 five-page source and PDF', 'tree': new_tree['sha'], 'parents': [head]})
    if gh('git/ref/heads/' + BRANCH)['object']['sha'] != head:
        raise RuntimeError('Branch moved during preparation; unreferenced objects retained, ref not moved')
    gh('git/refs/heads/' + BRANCH, 'PATCH', {'sha': new_commit['sha'], 'force': False})
    observed = gh('git/ref/heads/' + BRANCH)['object']['sha']
    if observed != new_commit['sha']:
        raise RuntimeError('Post-write branch readback differs')
    print(json.dumps({'status': 'ADMITTED_NON_MAIN', 'new_head': observed, 'paths': sorted(outputs), 'pages': 5}, indent=2))


if __name__ == '__main__':
    main()
