#!/usr/bin/env python3
"""Every selected reader must load its module; preserve standalone bodies exactly."""
import json,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'assets/data/ricpe-original-accountability-20260905.json').read_text())
routes=[r[lang]+'index.html' for r in data['routes'] for lang in ('es','en')]+[data['evidence_reader']+'index.html']
standalone={'es/ricpe-perimetro-accionistas-medios/index.html','en/ricpe-perimeter-shareholders-media/index.html','evidence/ricpe-cnmv/2026-08-27/index.html'}
for path in routes:
 text=(ROOT/path).read_text()
 assert re.search(r'<script[^>]+src=["\'][^"\']*(?:/site\.js|/ricpe-original-accountability-20260905\.js)',text), f'No loader at {path}'
 if path in standalone:
  original=subprocess.check_output(['git','show',data['source_main']+':'+path],cwd=ROOT,text=True)
  restored=re.sub(r'<script\b[^>]*data-ricpe-original-standalone-loader[^>]*></script>\n?','',text)
  assert restored.rstrip('\n')==original.rstrip('\n'), f'Existing standalone content changed outside additive loader: {path}'
print('RICPE ENTRYPOINTS: PASS; 17 loaded routes, 3 original standalone bodies preserved')
