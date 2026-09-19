#!/usr/bin/env python3
from __future__ import annotations
import hashlib, sys, urllib.request

BASE="https://sbu001monterecco.github.io/por-derecho"
EXPECTED_SHA="3dcc618ee4840bcc0057c1bd4b0d65e4f30c99078d5cb09c82134623221d0baf"
checks=[
    ("/es/cuentas-monte-lanza-2012/", ["MONTE LANZA SOCIEDAD LIMITADA","3dcc618e","CCAA_MONTELANZA.pdf"]),
    ("/en/monte-lanza-2012-accounts/", ["MONTE LANZA SOCIEDAD LIMITADA","3dcc618e","CCAA_MONTELANZA.pdf"]),
    ("/es/montelanza-cuentas-2008/", ["cuentas 2012","cuentas-monte-lanza-2012"]),
    ("/en/montelanza-accounts-2008/", ["2012 accounts","monte-lanza-2012-accounts"]),
]
errors=[]
for route,markers in checks:
    try:
        req=urllib.request.Request(BASE+route,headers={"Cache-Control":"no-cache","User-Agent":"PorDerecho-live-verifier/1.0"})
        with urllib.request.urlopen(req,timeout=25) as resp:
            body=resp.read().decode("utf-8","replace")
        for marker in markers:
            if marker not in body: errors.append(f"{route}: missing {marker!r}")
    except Exception as exc:
        errors.append(f"{route}: {exc}")

try:
    url=BASE+"/assets/documents/montelanza-accounts-2012/CCAA_MONTELANZA.pdf"
    req=urllib.request.Request(url,headers={"Cache-Control":"no-cache","User-Agent":"PorDerecho-live-verifier/1.0"})
    with urllib.request.urlopen(req,timeout=40) as resp:
        raw=resp.read()
    if hashlib.sha256(raw).hexdigest()!=EXPECTED_SHA:
        errors.append("live PDF SHA-256 mismatch")
except Exception as exc:
    errors.append(f"live PDF: {exc}")

if errors:
    print("FAIL — Monte Lanza live verification")
    for e in errors: print(" -",e)
    sys.exit(1)
print("PASS — Monte Lanza bilingual routes, 2008 reciprocal links and canonical PDF verified at public edge.")
