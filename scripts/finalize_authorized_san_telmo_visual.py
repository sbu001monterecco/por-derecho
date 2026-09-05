#!/usr/bin/env python3
"""Finalize the authorized Eduardo–Sun Park–Borja visual.

This script assumes the exact user-authorized binaries have been decoded and
SHA-256 verified by import_authorized_san_telmo_assets.py. It locks them into the
canonical visual registry, marks the composite READY, wires the shared website
loader, and records the activation in the governance files.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "assets/visual-asset-registry.json"
SIDECAR = ROOT / "assets/composites/san-telmo-ricpe-sun-park-stamp-v1.asset-map.json"
LOADER = ROOT / "assets/ricpe-identity-correction-20260815.js"
GOVERNANCE = ROOT / "archive/knowledge-project/VISUAL_ASSET_IDENTITY_GOVERNANCE_19AUG2026.md"
CONTINUITY = ROOT / "archive/knowledge-project/THREAD_CONTINUITY_VISUAL_SURFACES_ADDENDUM_19AUG2026.md"
REJECTED = ROOT / "archive/knowledge-project/VISUAL_ASSET_REJECTED_OUTPUTS_LOG.md"
GATE = ROOT / "archive/knowledge-project/SAN_TELMO_PHOTO_STAMP_IMPLEMENTATION_GATE_19AUG2026.md"

EDUARDO = ROOT / "assets/actors/eduardo-sanchez-san-telmo.webp"
SUNPARK = ROOT / "assets/places/sun-park-mynd-yaiza--user-authorized-20260819.jpg"
BORJA = ROOT / "assets/actors/francisco-de-borja-rodriguez-batllori.jpg"
COMPOSITE = ROOT / "assets/composites/san-telmo-ricpe-sun-park-stamp-v1.svg"
PHOTO_MODULE = ROOT / "assets/san-telmo-authorized-photo-stamp-20260819.js"

EXPECTED_SHA256 = {
    EDUARDO: "a46afb994e6fa0fb309d43fff45b72923a75db39680abc01e10a0c13a52af7d6",
    SUNPARK: "91fb8e8bff10b76296d2abdb27f2733bd6faa99666941d0c22a2d631c369110d",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()  # noqa: S324


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_once(path: Path, marker: str, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    if marker not in text:
        path.write_text(text.rstrip() + "\n\n" + block.strip() + "\n", encoding="utf-8")


def main() -> int:
    for path in (EDUARDO, SUNPARK, BORJA, COMPOSITE, PHOTO_MODULE):
        if not path.is_file():
            raise RuntimeError(f"Required visual asset missing: {path.relative_to(ROOT)}")
    for path, expected in EXPECTED_SHA256.items():
        actual = sha256(path)
        if actual != expected:
            raise RuntimeError(f"SHA-256 mismatch for {path.relative_to(ROOT)}: {actual} != {expected}")

    registry = load_json(REGISTRY)
    assets = registry.setdefault("assets", {})

    eduardo_id = "person.eduardo-sanchez-san-telmo.primary"
    eduardo = assets[eduardo_id]
    eduardo.update({
        "path": "assets/actors/eduardo-sanchez-san-telmo.webp",
        "git_blob_sha": git_blob_sha(EDUARDO),
        "sha256": sha256(EDUARDO),
        "identity_status": "LOCKED_CANONICAL_REPOSITORY_ASSET",
        "identity_basis": "Gil Marer expressly identified the uploaded image as Eduardo Sánchez and authorized its Por Derecho website, visualization, email and document use on 19 August 2026. Identity is user-supplied and not inferred from facial appearance.",
        "authorization_record": "archive/knowledge-project/SAN_TELMO_AUTHORIZED_IMAGE_USE_RECORD_19AUG2026.md",
        "dimensions": "800x600",
        "format": "webp",
        "approved_contexts": [
            "San Telmo / RICPE / Sun Park same-asset visualization",
            "dedicated Eduardo Sánchez / San Telmo evidence context",
            "institutional emails and documents carrying the controlled statement"
        ],
    })
    eduardo.pop("pending_source", None)
    eduardo.pop("publication_rule", None)
    eduardo.pop("approved_contexts_after_import", None)

    sun_id = "place.sun-park-mynd-yaiza.user-authorized-20260819"
    assets[sun_id] = {
        "subject_type": "place",
        "canonical_name": "Sun Park / MYND Yaiza",
        "short_label": "Sun Park — the same hotel — user-authorized aerial",
        "path": "assets/places/sun-park-mynd-yaiza--user-authorized-20260819.jpg",
        "git_blob_sha": git_blob_sha(SUNPARK),
        "sha256": sha256(SUNPARK),
        "identity_status": "LOCKED_CANONICAL_REPOSITORY_ASSET",
        "identity_basis": "Gil Marer expressly authorized the uploaded aerial image for Por Derecho use as Sun Park / MYND Yaiza — the same hotel — on 19 August 2026.",
        "authorization_record": "archive/knowledge-project/SAN_TELMO_AUTHORIZED_IMAGE_USE_RECORD_19AUG2026.md",
        "dimensions": "294x220",
        "format": "jpg",
        "approved_contexts": [
            "San Telmo / RICPE / Sun Park same-asset visualization",
            "same-hotel documents and institutional email exports"
        ],
        "alt_en": "Aerial view of Sun Park / MYND Yaiza, the same hotel",
        "alt_es": "Vista aérea de Sun Park / MYND Yaiza, el mismo hotel",
        "variant_of": "place.sun-park-mynd-yaiza.aerial-primary"
    }

    composite_id = "composite.san-telmo-ricpe-sun-park-stamp-v1"
    assets[composite_id] = {
        "subject_type": "document",
        "canonical_name": "San Telmo / RICPE / Sun Park documentary collision stamp",
        "short_label": "Eduardo → Sun Park → Borja / AC",
        "path": "assets/composites/san-telmo-ricpe-sun-park-stamp-v1.svg",
        "git_blob_sha": git_blob_sha(COMPOSITE),
        "sha256": sha256(COMPOSITE),
        "identity_status": "LOCKED_CANONICAL_REPOSITORY_ASSET",
        "identity_basis": "Deterministic composite generated from the user-authorized Eduardo and Sun Park assets and the pre-existing canonical Borja repository asset under the fixed slot map.",
        "slot_map": "assets/composites/san-telmo-ricpe-sun-park-stamp-v1.asset-map.json",
        "approved_contexts": [
            "Por Derecho website",
            "institutional emails",
            "PDF, Word and presentation exports"
        ],
        "alt_en": "Eduardo Sánchez, Sun Park and Francisco de Borja Rodríguez-Batllori Laffitte in the source-controlled San Telmo and RICPE documentary collision",
        "alt_es": "Eduardo Sánchez, Sun Park y Francisco de Borja Rodríguez-Batllori Laffitte en la colisión documental San Telmo y RICPE controlada por fuentes"
    }

    dump_json(REGISTRY, registry)

    sidecar = load_json(SIDECAR)
    sidecar["publication_status"] = "READY"
    sidecar["rendered_asset_id"] = composite_id
    sidecar["rendered_path"] = "assets/composites/san-telmo-ricpe-sun-park-stamp-v1.svg"
    sidecar["slots"] = {
        "left_portrait_eduardo_sanchez": eduardo_id,
        "centre_same_asset_sun_park": sun_id,
        "right_portrait_borja_ac": "person.francisco-de-borja-rodriguez-batllori.primary"
    }
    sidecar["activation_condition"] = "SATISFIED: every slot resolves to an active byte-locked registry asset and the validator must pass before merge."
    dump_json(SIDECAR, sidecar)

    loader = LOADER.read_text(encoding="utf-8")
    load_line = "  load('san-telmo-authorized-photo-stamp-20260819.js?v=20260819a');"
    if load_line not in loader:
        marker = "  load('san-telmo-parallel-lives-red-20260819.js?v=20260819b');"
        if marker not in loader:
            raise RuntimeError("Could not locate San Telmo visual loader marker")
        loader = loader.replace(marker, marker + "\n\n  // Authorized Eduardo → Sun Park → Borja photo stamp, governed by the canonical asset registry.\n" + load_line)
        LOADER.write_text(loader, encoding="utf-8")

    activation = """
## Activation update — 19 August 2026

The user-authorized image assets are now active and byte-locked:

- Eduardo Sánchez: `person.eduardo-sanchez-san-telmo.primary` → `assets/actors/eduardo-sanchez-san-telmo.webp`.
- Sun Park authorized aerial: `place.sun-park-mynd-yaiza.user-authorized-20260819` → `assets/places/sun-park-mynd-yaiza--user-authorized-20260819.jpg`.
- Borja / AC remains the pre-existing canonical asset: `person.francisco-de-borja-rodriguez-batllori.primary` → `assets/actors/francisco-de-borja-rodriguez-batllori.jpg`.
- Corrected composite: `composite.san-telmo-ricpe-sun-park-stamp-v1` → `assets/composites/san-telmo-ricpe-sun-park-stamp-v1.svg`.

The fixed visual order is Eduardo → Sun Park, the same hotel → Borja / Administrador Concursal. The earlier wrong portrait assignment remains rejected and prohibited from reuse.
"""
    append_once(GOVERNANCE, "## Activation update — 19 August 2026", activation)

    continuity = """
## Authorized San Telmo photo-stamp activation — 19 August 2026

The shared site now loads `assets/san-telmo-authorized-photo-stamp-20260819.js`, which renders the registry-controlled composite `assets/composites/san-telmo-ricpe-sun-park-stamp-v1.svg` across the relevant homepage, RICPE, RSM, AC, San Telmo, Grant Thornton and parallel-lives surfaces.

The image order is locked: Eduardo Sánchez → Sun Park / the same hotel → Francisco de Borja Rodríguez-Batllori Laffitte / Administrador Concursal. Do not regenerate or reorder the portraits from prompt context.
"""
    append_once(CONTINUITY, "## Authorized San Telmo photo-stamp activation — 19 August 2026", continuity)

    replacement = """
## Corrected replacement — 19 August 2026

The approved replacement is `assets/composites/san-telmo-ricpe-sun-park-stamp-v1.svg`, generated from the user-authorized Eduardo Sánchez and Sun Park images and the existing canonical Borja / AC repository image. Its slot map is `assets/composites/san-telmo-ricpe-sun-park-stamp-v1.asset-map.json` and its registry ID is `composite.san-telmo-ricpe-sun-park-stamp-v1`.
"""
    append_once(REJECTED, "## Corrected replacement — 19 August 2026", replacement)

    gate_text = GATE.read_text(encoding="utf-8")
    gate_text = gate_text.replace(
        "The corrected visual may move to `READY` only when all of the following are true:",
        "**Status: READY, subject to successful repository validators and merge.**\n\nThe corrected visual moved to `READY` after satisfying all of the following:"
    )
    GATE.write_text(gate_text, encoding="utf-8")

    print("Finalized authorized San Telmo visual registry, sidecar, loader and governance records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
