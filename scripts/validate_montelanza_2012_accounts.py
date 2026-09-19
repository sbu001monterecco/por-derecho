#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PDF = ROOT / "assets/documents/montelanza-accounts-2012/CCAA_MONTELANZA.pdf"
MANIFEST = ROOT / "assets/documents/montelanza-accounts-2012/digitisation-manifest.json"
README = ROOT / "assets/documents/montelanza-accounts-2012/README.md"
OCR_DIR = ROOT / "assets/documents/montelanza-accounts-2012/ocr"
ES = ROOT / "es/cuentas-monte-lanza-2012/index.html"
EN = ROOT / "en/monte-lanza-2012-accounts/index.html"
ES08 = ROOT / "es/montelanza-cuentas-2008/index.html"
EN08 = ROOT / "en/montelanza-accounts-2008/index.html"
DISCOVERY = ROOT / "assets/montelanza-accounts-discovery-20260919.js"
SITE = ROOT / "assets/site.js"
SITEMAP = ROOT / "sitemap-community-governance.xml"
START = ROOT / "CHATGPT_START_HERE.md"
HANDOVER = ROOT / "archive/CURRENT_GITHUB_ONLY_HANDOVER_19SEP2026.md"

EXPECTED_SHA = "3dcc618ee4840bcc0057c1bd4b0d65e4f30c99078d5cb09c82134623221d0baf"
EXPECTED_SIZE = 1349645
PARTS = [OCR_DIR / f"part-{i:02d}-pages-{a:02d}-{b:02d}.txt" for i,(a,b) in enumerate([(1,5),(6,10),(11,15),(16,20),(21,25),(26,30)],1)]

errors=[]

def need(cond,msg):
    if not cond: errors.append(msg)

for p in [PDF,MANIFEST,README,ES,EN,ES08,EN08,DISCOVERY,SITE,SITEMAP,START,HANDOVER,*PARTS]:
    need(p.exists(), f"missing: {p.relative_to(ROOT)}")

if PDF.exists():
    raw=PDF.read_bytes()
    need(len(raw)==EXPECTED_SIZE, f"PDF size {len(raw)} != {EXPECTED_SIZE}")
    need(hashlib.sha256(raw).hexdigest()==EXPECTED_SHA, "PDF SHA-256 mismatch")
    need(raw.startswith(b"%PDF"), "canonical source is not a PDF header")

if MANIFEST.exists():
    m=json.loads(MANIFEST.read_text(encoding="utf-8"))
    need(m.get("sha256")==EXPECTED_SHA, "manifest SHA mismatch")
    need(m.get("pages")==30, "manifest page count != 30")
    d=m.get("digitisation",{})
    need(d.get("repository_binary_copy") is True, "manifest must record repository binary copy")
    need(d.get("repository_path")=="assets/documents/montelanza-accounts-2012/CCAA_MONTELANZA.pdf", "manifest repository path mismatch")

if all(p.exists() for p in PARTS):
    joined="\n".join(p.read_text(encoding="utf-8",errors="replace") for p in PARTS)
    pages=[int(x) for x in re.findall(r"PAGE\s+(\d{2})\s*/\s*30",joined)]
    need(sorted(set(pages))==list(range(1,31)), f"OCR page markers incomplete: {sorted(set(pages))}")
    need("1.368.000" in joined and "cese en la actividad" in joined, "page-23 transition proposition absent from OCR")
    need("No hubo empleo durante el ejercicio 2.012" in joined, "2012 no-employment statement absent from OCR")

pdf_rel="../../assets/documents/montelanza-accounts-2012/CCAA_MONTELANZA.pdf"
for p,lang in [(ES,"ES"),(EN,"EN")]:
    if p.exists():
        s=p.read_text(encoding="utf-8")
        need(pdf_rel in s, f"{lang} page does not use repository-hosted PDF")
        need("3dcc618e" in s, f"{lang} page missing fingerprint")
        need("digitisation-manifest.json" in s, f"{lang} page missing manifest link")

if ES08.exists(): need("../cuentas-monte-lanza-2012/" in ES08.read_text(encoding="utf-8"), "2008 ES dossier missing 2012 cross-link")
if EN08.exists(): need("../monte-lanza-2012-accounts/" in EN08.read_text(encoding="utf-8"), "2008 EN dossier missing 2012 cross-link")
if SITE.exists(): need("MONTELANZA-ACCOUNTS-DISCOVERY-20260919" in SITE.read_text(encoding="utf-8"), "site loader missing Montelanza discovery")
if DISCOVERY.exists():
    s=DISCOVERY.read_text(encoding="utf-8")
    need("does not by itself prove" in s and "no prueba por sí sola" in s, "discovery module missing evidential boundary")
if SITEMAP.exists():
    s=SITEMAP.read_text(encoding="utf-8")
    need("/es/cuentas-monte-lanza-2012/" in s and "/en/monte-lanza-2012-accounts/" in s, "community sitemap missing bilingual routes")
if START.exists(): need("GitLab is temporarily blocked" in START.read_text(encoding="utf-8"), "GitLab outage note missing from start-here")
if HANDOVER.exists():
    s=HANDOVER.read_text(encoding="utf-8")
    need("GitLab is temporarily blocked" in s and "current GitHub main" in s, "GitHub-only handover missing outage/recovery rules")

if errors:
    print("FAIL — Monte Lanza accounts digitisation")
    for e in errors: print(" -",e)
    sys.exit(1)
print("PASS — Monte Lanza accounts digitisation: canonical PDF hash/size, 30 OCR pages, bilingual routes, provenance boundaries, cross-links and GitHub-only continuity controls.")
