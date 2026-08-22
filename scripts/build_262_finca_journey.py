#!/usr/bin/env python3
"""Build the public-safe 262-finca journey projection.

The source register remains immutable.  This script deliberately emits a derivative:
it excludes acquisition-sheet financial fields and retains source status/limitations so
that a physical row, a working-sheet label and a Registry conclusion cannot be
silently conflated by the public UI.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "research/sun-park-262-fincas/sun-park-262-fincas.csv"
OVERLAY = ROOT / "research/sun-park-262-fincas/acquisition-overlay.csv"
EVIDENCE = ROOT / "research/sun-park-262-fincas/finca-journey-evidence-v1.json"
DEFAULT_OUTPUT = ROOT / "assets/data/sun-park-262-finca-journey-v1.json"


def bilingual(en: str, es: str) -> dict[str, list[str]]:
    return {"en": [en], "es": [es]}


def block_or_zone(row: dict[str, str]) -> str:
    if row["type"] == "SOLARIUM":
        return "CENTRAL"
    if row["type"] != "APARTMENT":
        return "FRONT"
    try:
        apartment = int(row["apt_number"])
    except (TypeError, ValueError):
        return "UNKNOWN"
    ranges = {
        "1": ((102, 114), (151, 164)),
        "2": ((201, 210), (251, 260)),
        "3": ((301, 314), (351, 364)),
        "4": ((401, 408), (451, 458)),
        "5": ((501, 514), (551, 564)),
        "6": ((601, 616), (651, 666)),
        "7": ((701, 716), (751, 766)),
        "8": ((801, 811), (851, 862)),
        "9": ((901, 914),),
    }
    for block, block_ranges in ranges.items():
        if any(start <= apartment <= end for start, end in block_ranges):
            return block
    return "UNKNOWN"


def event_source_ids(record: dict) -> set[str]:
    ids: set[str] = set()
    for event in record.get("events", []):
        ids.update(event.get("source_ids", []))
    for conflict in record.get("identifier_conflicts", []):
        ids.update(conflict.get("source_ids", []))
    return ids


def build() -> dict:
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    source_records = evidence.get("property_records", {})
    source_ids = {source["id"] for source in evidence["source_ledger"]}

    with MASTER.open(newline="", encoding="utf-8") as handle:
        master_rows = list(csv.DictReader(handle))
    with OVERLAY.open(newline="", encoding="utf-8") as handle:
        overlay_rows = list(csv.DictReader(handle))

    if len(master_rows) != 262:
        raise ValueError(f"Expected 262 master rows, found {len(master_rows)}")
    finca_ids = [row["registry_finca"] for row in master_rows]
    if len(set(finca_ids)) != len(finca_ids):
        raise ValueError("The master register contains duplicate registry_finca values")
    unknown_records = set(source_records) - set(finca_ids)
    if unknown_records:
        raise ValueError(f"Evidence record refers to an unknown finca: {sorted(unknown_records)}")

    overlay = {row["registry_finca"]: row for row in overlay_rows}
    if len(overlay) != len(overlay_rows):
        raise ValueError("The acquisition overlay contains duplicate registry_finca values")
    unknown_overlay = set(overlay) - set(finca_ids)
    if unknown_overlay:
        raise ValueError(f"Overlay refers to an unknown finca: {sorted(unknown_overlay)}")

    properties = []
    for row in sorted(master_rows, key=lambda item: int(item["registry_finca"])):
        finca = row["registry_finca"]
        record = source_records.get(finca, {})
        current_overlay = overlay.get(finca)
        overlay_public = current_overlay.get("matkator_acquisition_status") if current_overlay else None
        property_source_ids = event_source_ids(record)
        unknown_source_ids = property_source_ids - source_ids
        if unknown_source_ids:
            raise ValueError(f"{finca}: unknown source ID(s): {sorted(unknown_source_ids)}")

        coverage_state = record.get("coverage_state", "NOT_YET_RECONSTRUCTED")
        properties.append(
            {
                "finca_id": f"FINCA-{finca}",
                "registry_finca": finca,
                "unit": int(row["unit"]),
                "physical": {
                    "type": row["type"],
                    "horizontal_number": row["horizontal_number"] or None,
                    "apartment_or_local": row["apt_number"] or None,
                    "area_m2": float(row["area_m2"]),
                    "block_or_zone": block_or_zone(row),
                },
                "historic_source_label": row["owner_as_listed_gesvalt"],
                "acquisition_overlay": overlay_public,
                "coverage_state": coverage_state,
                "events": record.get("events", []),
                "identifier_conflicts": record.get("identifier_conflicts", []),
                "open_questions": record.get("open_questions"),
                "next_document_needed": record.get("next_document_needed"),
            }
        )

    coverage_counts = Counter(property_["coverage_state"] for property_ in properties)
    properties_with_events = sum(bool(property_["events"]) for property_ in properties)
    projection = {
        "schema_version": "sun-park-262-finca-journey/v1",
        "control_date": evidence["control_date"],
        "generated_from": {
            "master_register": str(MASTER.relative_to(ROOT)),
            "acquisition_overlay": str(OVERLAY.relative_to(ROOT)),
            "evidence_ledger": str(EVIDENCE.relative_to(ROOT)),
        },
        "publication_boundary": evidence["publication_boundary"],
        "defaults": {
            "historic_source_caution": {
                "en": "Historical GESVALT source label only — not a statement of present registered title.",
                "es": "Sólo etiqueta histórica de fuente GESVALT; no es una afirmación de titularidad registral actual.",
            },
            "open_questions": bilingual(
                "No property-specific historical chain has yet been reconstructed. Recover the title, Registry, possession/operation and accounting tracks separately.",
                "Aún no se ha reconstruido una cadena histórica específica de finca. Recuperar por separado las vías de título, Registro, posesión/explotación y contabilidad.",
            ),
            "next_document_needed": {
                "en": "Historic/current certified Registry records, causal title, presentation/qualification history and a physical-unit crosswalk.",
                "es": "Certificaciones registrales históricas/actuales, título causal, historial de presentación/calificación y cruce con unidad física.",
            },
        },
        "coverage": {
            "total_properties": len(properties),
            "properties_with_property_specific_events": properties_with_events,
            "coverage_by_state": dict(sorted(coverage_counts.items())),
            "rule": {
                "en": "Every row is visible. A row without a source-bound property event is explicitly marked as not yet reconstructed or source-pointer-only; complex-wide context is not duplicated as an individual legal event.",
                "es": "Cada fila es visible. Una fila sin evento de finca vinculado a fuente se marca expresamente como no reconstruida todavía o sólo puntero de fuente; el contexto global no se duplica como hecho jurídico individual.",
            },
        },
        "source_ledger": evidence["source_ledger"],
        "complex_context_events": evidence["complex_context_events"],
        "properties": properties,
    }
    return projection


def serialise(data: dict) -> bytes:
    return (json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=False) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="fail if the public projection is not current")
    args = parser.parse_args()

    try:
        content = serialise(build())
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"262-FINCA JOURNEY BUILD: FAIL — {exc}", file=sys.stderr)
        return 1

    output = args.output if args.output.is_absolute() else ROOT / args.output
    if args.check:
        if not output.is_file() or output.read_bytes() != content:
            print(f"262-FINCA JOURNEY BUILD: FAIL — generated projection is stale: {output.relative_to(ROOT)}", file=sys.stderr)
            return 1
        print("262-FINCA JOURNEY BUILD: PASS — generated projection is current")
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(content)
    print(f"262-FINCA JOURNEY BUILD: wrote {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
