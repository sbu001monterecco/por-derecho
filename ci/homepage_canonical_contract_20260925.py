#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, sys

ROOT=Path(__file__).resolve().parents[1]
CONTRACT=ROOT/"ops/HOMEPAGE_CANONICAL_CONTRACT_20260925.json"
errors=[]

cfg=json.loads(CONTRACT.read_text(encoding="utf-8"))

for locale in ("en","es"):
    meta=cfg["homepage"][locale]
    path=ROOT/meta["path"]
    if not path.is_file():
        errors.append(f"missing homepage: {meta['path']}")
        continue
    raw=path.read_bytes()
    actual=hashlib.sha256(raw).hexdigest()
    if actual != meta["sha256"]:
        errors.append(f"{meta['path']} hash drift: {actual} != {meta['sha256']}")
    if len(raw) > meta["max_bytes"]:
        errors.append(f"{meta['path']} exceeds byte budget: {len(raw)} > {meta['max_bytes']}")
    text=raw.decode("utf-8")
    for route in cfg["required_routes"][locale]:
        if f'href="{route}' not in text:
            errors.append(f"{meta['path']} missing first-level route {route}")
    for marker in cfg["required_sections"][locale]:
        if marker not in text:
            errors.append(f"{meta['path']} missing required section marker {marker!r}")
    for token in cfg["forbidden_homepage_tokens"]:
        if token in text:
            errors.append(f"{meta['path']} contains forbidden homepage token {token!r}")

for rel in cfg.get("required_assets", []):
    if not (ROOT/rel).is_file():
        errors.append(f"missing required homepage asset: {rel}")

for locale in ("en","es"):
    p=ROOT/cfg["homepage"][locale]["path"]
    if p.is_file():
        t=p.read_text(encoding="utf-8")
        for token in cfg.get("required_homepage_tokens",{}).get(locale,[]):
            if token not in t:
                errors.append(f"{p.relative_to(ROOT)} missing required homepage token: {token}")

for rel in cfg.get("required_destination_files", []):
    if not (ROOT/rel).is_file():
        errors.append(f"missing required homepage destination: {rel}")

for locale in ("en","es"):
    p=ROOT/cfg["homepage"][locale]["path"]
    if p.is_file():
        t=p.read_text(encoding="utf-8")
        canonical=cfg.get("expected_canonical",{}).get(locale)
        if canonical and f'<link rel="canonical" href="{canonical}">' not in t:
            errors.append(f"{p.relative_to(ROOT)} canonical origin drift: expected {canonical}")

for rel in cfg["preserved_archives"]:
    p=ROOT/rel
    if not p.is_file():
        errors.append(f"missing continuity archive: {rel}")
    else:
        t=p.read_text(encoding="utf-8")
        if 'noindex' not in t:
            errors.append(f"continuity archive not noindex: {rel}")

for rel in ("en/future/index.html","es/futuro/index.html"):
    if not (ROOT/rel).is_file():
        errors.append(f"missing standalone Future route: {rel}")

if errors:
    print("HOMEPAGE CANONICAL CONTRACT: FAIL")
    for e in errors: print("-",e)
    sys.exit(1)

print("HOMEPAGE CANONICAL CONTRACT: PASS")
print(json.dumps({"schema":cfg["schema"],"canonical_public_origin":cfg["canonical_public_origin"],"mirror_origin":cfg["mirror_origin"]},sort_keys=True))
