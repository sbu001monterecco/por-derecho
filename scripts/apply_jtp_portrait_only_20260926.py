#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import io
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
PARTS = sorted((ROOT / "ops/jtp").glob("jtp-approved-small-20260926.part*"))
BASE = ROOT / "assets/jtp-payment-actor-composite-real-sources-20260925.png"
OUT = ROOT / "assets/jtp-payment-actor-composite-real-sources-20260926.png"
PORTRAIT = ROOT / "assets/actors/juan-tomas-parrilla-user-approved-20260926.jpg"
LOCK = ROOT / "ops/jtp/JTP_ACTOR_IMAGE_SOURCE_LOCK_20260925.json"
REGISTRY = ROOT / "assets/visual-asset-registry.json"
PROV = ROOT / "assets/data/jtp-payment-actor-composite-user-approved-jtp-20260926.json"
ASSET_MAP = ROOT / "assets/composites/jtp-payment-actor-context-user-approved-jtp-20260926.asset-map.json"

EXPECTED_BASE_SHA256 = "77895f4078ac3d3cad61077f5c33ac1865f95834e1d794014f024e00dd3587cc"
EXPECTED_PORTRAIT_SHA256 = "fdd0308df79312e1c666e48ba651eb5e34800057b62a0486c21bfa1cdf837489"
JTP_BOX = (390, 195, 640, 470)
CONTROL_ID = "PD-JTP-ACTOR-COMPOSITE-20260926-02"
JTP_VARIANT = "person.juan-tomas-parrilla.approved-20260926"
COMPOSITE_VARIANT = "composite.jtp-payment-actor-context-approved-jtp-20260926"

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def sha256_file(p: Path) -> str:
    return sha256_bytes(p.read_bytes())

if not PARTS:
    raise SystemExit("approved portrait chunks missing")
raw_b64 = "".join(p.read_text().strip() for p in PARTS)
portrait_bytes = base64.b64decode(raw_b64, validate=True)
if sha256_bytes(portrait_bytes) != EXPECTED_PORTRAIT_SHA256:
    raise SystemExit("approved JTP portrait hash mismatch")
PORTRAIT.write_bytes(portrait_bytes)

if sha256_file(BASE) != EXPECTED_BASE_SHA256:
    raise SystemExit("published base composite hash changed")

lock = json.loads(LOCK.read_text())
base = Image.open(BASE).convert("RGB")
portrait = Image.open(io.BytesIO(portrait_bytes)).convert("RGB")
before = np.asarray(base).copy()
out = base.copy()

x0, y0, x1, y1 = JTP_BOX
fitted = ImageOps.fit(
    portrait,
    (x1 - x0, y1 - y0),
    method=Image.Resampling.LANCZOS,
    centering=(0.50, 0.50),
)
out.paste(fitted, (x0, y0))
after = np.asarray(out)

diff = np.any(before != after, axis=2)
mask = np.zeros(diff.shape, dtype=bool)
mask[y0:y1, x0:x1] = True
outside = int(np.logical_and(diff, ~mask).sum())
changed = int(diff.sum())
if outside != 0:
    raise SystemExit(f"pixels changed outside JTP box: {outside}")
if changed == 0:
    raise SystemExit("JTP region did not change")

# Explicitly prove the other four actor rectangles are pixel-identical.
for key in ("borja", "jdam", "lpam", "alberto"):
    bx0, by0, bx1, by1 = lock["actors"][key]["box"]
    if not np.array_equal(before[by0:by1, bx0:bx1], after[by0:by1, bx0:bx1]):
        raise SystemExit(f"non-JTP actor changed: {key}")

OUT.parent.mkdir(parents=True, exist_ok=True)
out.save(OUT, format="PNG", optimize=True)
# Reopen saved bytes and re-prove lossless boundary.
saved = np.asarray(Image.open(OUT).convert("RGB"))
if not np.array_equal(before[~mask], saved[~mask]):
    raise SystemExit("saved PNG changed pixels outside JTP region")

composite_sha = sha256_file(OUT)
portrait_sha = sha256_file(PORTRAIT)

PROV.write_text(json.dumps({
    "schema": "por-derecho.jtp-real-actor-composite-provenance.v2",
    "control_id": CONTROL_ID,
    "date": "2026-09-26",
    "status": "DETERMINISTIC_JTP_ONLY_REPLACEMENT_USER_APPROVED",
    "path": str(OUT.relative_to(ROOT)),
    "supersedes": "PD-JTP-ACTOR-COMPOSITE-20260925-01",
    "base_composite_sha256": EXPECTED_BASE_SHA256,
    "sha256": composite_sha,
    "dimensions": list(out.size),
    "jtp_box": list(JTP_BOX),
    "verification": {
        "changed_pixels": changed,
        "changed_pixels_outside_jtp_box": outside,
        "borja_region_unchanged": True,
        "jdam_region_unchanged": True,
        "lpam_region_unchanged": True,
        "alberto_region_unchanged": True
    },
    "jtp_source": {
        "asset_id": JTP_VARIANT,
        "path": str(PORTRAIT.relative_to(ROOT)),
        "sha256": portrait_sha,
        "basis": "User supplied a real conference photograph in-chat on 26-Sep-2026; a faithful portrait derivative was generated from that photograph and the user explicitly confirmed the derivative as the correct JTP image and authorised its use in the existing composite.",
        "facial_recognition_used": False,
        "other_actor_generation_used": False
    }
}, ensure_ascii=False, indent=2) + "\n")

ASSET_MAP.write_text(json.dumps({
    "schema": "por-derecho.visual-asset-slot-map.v1",
    "composite_path": str(OUT.relative_to(ROOT)),
    "publication_status": "READY",
    "control_id": CONTROL_ID,
    "supersedes": "assets/composites/jtp-payment-actor-context-real-source-20260925.asset-map.json",
    "slots": {
        "jtp": JTP_VARIANT,
        "borja": "person.francisco-de-borja-rodriguez-batllori.primary",
        "jdam": "person.jose-daniel-acosta-matos.primary",
        "lpam": "person.laura-patricia-acosta-matos.primary",
        "alberto": "person.alberto-lopez-villarrubia.primary"
    }
}, ensure_ascii=False, indent=2) + "\n")

registry = json.loads(REGISTRY.read_text())
assets = registry["assets"]
assets[JTP_VARIANT] = {
    "subject_type": "person",
    "canonical_name": "Juan Tomás Parrilla Suárez",
    "short_label": "JTP · user-approved 26-Sep-2026 derivative",
    "path": str(PORTRAIT.relative_to(ROOT)),
    "identity_status": "USER_APPROVED_DERIVATIVE_FROM_REAL_SOURCE_PHOTO",
    "identity_basis": "The user supplied the real conference photograph in the current conversation, confirmed the generated portrait derivative as the correct JTP image, and explicitly authorised replacing only JTP in the existing composite. No automated facial recognition was used.",
    "supersedes_for_public_composite": "person.juan-tomas-parrilla.primary",
    "approved_contexts": [
        "JTP payment / AC / CAM actor-context composite",
        "counsel-payment independence reader"
    ],
    "alt_en": "Juan Tomás Parrilla Suárez — user-approved portrait derivative from supplied conference photograph",
    "alt_es": "Juan Tomás Parrilla Suárez — retrato derivado aprobado por el usuario a partir de la fotografía de conferencia aportada",
    "source_provenance": {
        "source_class": "user-supplied real conference photograph + user-approved portrait derivative",
        "approval_date": "2026-09-26",
        "sha256": portrait_sha,
        "dimensions": "320x320",
        "format": "jpg",
        "facial_recognition_used": False
    }
}
assets[COMPOSITE_VARIANT] = {
    "subject_type": "document",
    "canonical_name": "JTP payment / AC / CAM actor-context composite — JTP-only approved replacement",
    "short_label": "JTP actor-context composite · JTP-only 26-Sep replacement",
    "path": str(OUT.relative_to(ROOT)),
    "identity_status": "LOCKED_JTP_ONLY_REPLACEMENT",
    "identity_basis": "Deterministic replacement of only the JTP rectangle in the previously published composite. Borja, JDAM, LPAM and Alberto rectangles are pixel-identical to the prior approved composite.",
    "supersedes": "composite.jtp-payment-actor-context-real-source-20260925",
    "approved_contexts": [
        "JTP payment / AC / CAM actor-context composite",
        "counsel-payment independence reader",
        "public investigative/editorial visual"
    ],
    "alt_en": "Actor-context visual with user-approved JTP portrait and four unchanged actor portraits",
    "alt_es": "Visual de contexto con retrato JTP aprobado por el usuario y los otros cuatro retratos sin cambios",
    "source_provenance": {
        "sha256": composite_sha,
        "dimensions": "1055x1491",
        "format": "png",
        "control_id": CONTROL_ID,
        "asset_map": str(ASSET_MAP.relative_to(ROOT)),
        "provenance": str(PROV.relative_to(ROOT)),
        "changed_pixels_outside_jtp_box": 0,
        "other_four_actor_regions_unchanged": True
    }
}
# Preserve old entries and mark supersession without changing their image bytes.
if "person.juan-tomas-parrilla.primary" in assets:
    assets["person.juan-tomas-parrilla.primary"]["superseded_for_public_composite_by"] = JTP_VARIANT
if "composite.jtp-payment-actor-context-real-source-20260925" in assets:
    assets["composite.jtp-payment-actor-context-real-source-20260925"]["superseded_by"] = COMPOSITE_VARIANT
REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n")

old_img = "jtp-payment-actor-composite-real-sources-20260925.png"
new_img = "jtp-payment-actor-composite-real-sources-20260926.png"
old_control = "PD-JTP-ACTOR-COMPOSITE-20260925-01"
old_prov = "assets/data/jtp-payment-actor-composite-real-sources-20260925.json"
new_prov = "assets/data/jtp-payment-actor-composite-user-approved-jtp-20260926.json"

pages = [
    ROOT / "es/pago-masa-independencia-defensa/index.html",
    ROOT / "en/estate-payment-counsel-independence/index.html",
]
for page in pages:
    text = page.read_text()
    text = text.replace(old_img, new_img)
    text = text.replace(old_control, CONTROL_ID)
    text = text.replace(old_prov, new_prov)
    if page.parts[-3] == "es":
        text = text.replace(
            "<strong>Contexto de actores con fuentes reales.</strong> Los cinco retratos proceden de imágenes controladas del proyecto; no se ha generado ningún parecido sustitutivo.",
            "<strong>Contexto de actores con fuentes controladas.</strong> Los cuatro retratos distintos de JTP se conservan píxel por píxel sin modificación. El retrato de JTP es el derivado aprobado expresamente por el usuario el 26 de septiembre de 2026 a partir de la fotografía real de conferencia aportada; no se ha regenerado ningún otro actor."
        )
    else:
        text = text.replace(
            "<strong>Real-source actor context.</strong> The five named portraits come from controlled project source images; no substitute likeness is generated.",
            "<strong>Controlled-source actor context.</strong> The four non-JTP portraits are preserved pixel-for-pixel without modification. The JTP portrait is the derivative expressly approved by the user on 26 September 2026 from the supplied real conference photograph; no other actor was regenerated."
        )
    page.write_text(text)

print(json.dumps({
    "status": "PASS",
    "control_id": CONTROL_ID,
    "composite_sha256": composite_sha,
    "portrait_sha256": portrait_sha,
    "changed_pixels": changed,
    "outside_jtp": outside,
    "other_four_unchanged": True
}, sort_keys=True))
