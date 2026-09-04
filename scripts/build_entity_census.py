#!/usr/bin/env python3
"""Build a conservative entity/name census for Por Derecho.

The scanner discovers names; it never infers identity, mandate, knowledge, control,
conflict or liability. Promotion into the canonical register is separately gated.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"
DECISIONS = ROOT / "ops" / "legaltech-entity-evidence" / "candidate-decisions.json"
TEXT_SUFFIXES = {".html", ".md", ".json", ".js", ".txt", ".xml", ".csv", ".yml", ".yaml"}
EXCLUDED_PARTS = {".git", "node_modules", "vendor", "dist", "build", "coverage", "__pycache__"}
MAX_BYTES = 2_500_000

CANONICAL_LABEL = re.compile(
    r"(?:canonical\s+(?:entity|identity|person|name)|entidad\s+can[oó]nica|identidad\s+can[oó]nica)\s*[:·-]\s*([^<\n]{3,180})",
    re.I,
)
DATA_CANONICAL = re.compile(r"data-canonical-(?:name|entity)=[\"']([^\"']+)[\"']", re.I)
DATA_CANONICAL_ID = re.compile(r"data-canonical-id=[\"'](PD-SP-[POSIR]-\d{4})[\"']", re.I)
LEGAL_ENTITY = re.compile(
    r"\b([A-ZÁÉÍÓÚÜÑ][A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9&.,'’()\- ]{2,110}?(?:S\.?L\.?U?\.?|S\.?A\.?|S\.?L\.?P\.?|SCR,?\s*S\.?A\.?|B\.?V\.?|LIMITED|ABOGADOS))\b"
)
ROLE_PERSON = re.compile(
    r"(?:abogad[oa]s?|lawyers?|socio|partner|procurador(?:a)?|administrador(?:a)?\s+concursal|judge|juez|magistrad[oa])\s*(?:de|of|:|·|-)?\s*([A-ZÁÉÍÓÚÜÑ][\wÁÉÍÓÚÜÑáéíóúüñ'’.-]+(?:\s+[A-ZÁÉÍÓÚÜÑ][\wÁÉÍÓÚÜÑáéíóúüñ'’.-]+){1,5})",
    re.I,
)
ID_PATTERN = re.compile(r"^PD-SP-([POSIR])-(\d{4})$")


def normalise(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    text = text.lower().replace("–", "-").replace("—", "-")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def iter_text_files() -> Iterable[Path]:
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        if path.stat().st_size > MAX_BYTES:
            continue
        yield path


def load_registry() -> tuple[dict[str, dict[str, Any]], dict[str, str], dict[str, Any]]:
    index = load_json(DATA / "matter-identity-registry-v1.json")
    records: dict[str, dict[str, Any]] = {}
    alias_to_id: dict[str, str] = {}
    canonical_name_to_id: dict[str, str] = {}
    ambiguous_aliases: set[str] = set()
    counts: defaultdict[str, int] = defaultdict(int)
    total = 0
    for part in index.get("parts", []):
        shard_path = DATA / part["path"]
        if not shard_path.is_file():
            raise AssertionError(f"Missing registry shard: {part['path']}")
        shard = load_json(shard_path)
        shard_records = shard.get("records")
        if not isinstance(shard_records, list):
            raise AssertionError(f"Registry shard lacks records: {part['path']}")
        if len(shard_records) != part.get("count"):
            raise AssertionError(f"Registry shard count mismatch: {part['path']}")
        for record in shard_records:
            identifier = record.get("id")
            if not isinstance(identifier, str) or not ID_PATTERN.fullmatch(identifier):
                raise AssertionError(f"Invalid canonical ID in {part['path']}: {identifier!r}")
            if identifier in records:
                raise AssertionError(f"Duplicate canonical ID: {identifier}")
            if record.get("type") != part.get("type"):
                raise AssertionError(f"Type mismatch for {identifier}")
            records[identifier] = record
            counts[record["type"]] += 1
            total += 1
            canonical_key = normalise(record.get("name"))
            if canonical_key:
                prior_name = canonical_name_to_id.get(canonical_key)
                if prior_name and prior_name != identifier:
                    raise AssertionError(f"Duplicate canonical name {record.get('name')!r}: {prior_name} vs {identifier}")
                canonical_name_to_id[canonical_key] = identifier
                alias_to_id[canonical_key] = identifier
            for value in [*(record.get("aliases") or []), *(record.get("search_aliases") or [])]:
                key = normalise(value)
                if not key or key in ambiguous_aliases:
                    continue
                prior = alias_to_id.get(key)
                if prior and prior != identifier:
                    ambiguous_aliases.add(key)
                    if key not in canonical_name_to_id:
                        alias_to_id.pop(key, None)
                    continue
                alias_to_id[key] = identifier
    expected = index.get("counts", {})
    if total != expected.get("total"):
        raise AssertionError(f"Registry total mismatch: {total} vs {expected.get('total')}")
    for kind in ("PERSON", "ORGANISATION", "STRUCTURE", "INSTITUTION", "PROCEEDING"):
        if counts[kind] != expected.get(kind):
            raise AssertionError(f"Registry {kind} mismatch: {counts[kind]} vs {expected.get(kind)}")
    for required in index.get("coverage", {}).get("required_names", []):
        if normalise(required) not in alias_to_id:
            raise AssertionError(f"Required name is not resolvable: {required}")
    return records, alias_to_id, index


def clean_candidate(raw: str) -> str:
    value = re.sub(r"\s+", " ", raw).strip(" \t\r\n.,;:|—–-")
    value = re.split(r"\s+(?:NIF|CIF|SHA-256|status|estado)\b", value, maxsplit=1, flags=re.I)[0].strip()
    return value[:180]


def build_census(alias_to_id: dict[str, str], decisions: dict[str, Any]) -> dict[str, Any]:
    decision_by_name = {normalise(row.get("candidate_name")): row for row in decisions.get("candidates", [])}
    found: dict[str, dict[str, Any]] = {}
    controlled_id_errors: list[dict[str, str]] = []

    for path in iter_text_files():
        rel = path.relative_to(ROOT).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        ids = DATA_CANONICAL_ID.findall(text)
        for identifier in ids:
            if identifier not in alias_to_id.values():
                controlled_id_errors.append({"path": rel, "id": identifier})

        hits: list[tuple[str, str, float]] = []
        hits.extend((clean_candidate(match), "EXPLICIT_CANONICAL_LABEL", 0.98) for match in CANONICAL_LABEL.findall(text))
        hits.extend((clean_candidate(match), "DATA_CANONICAL_NAME", 0.99) for match in DATA_CANONICAL.findall(text))
        hits.extend((clean_candidate(match), "LEGAL_ENTITY_PATTERN", 0.78) for match in LEGAL_ENTITY.findall(text))
        hits.extend((clean_candidate(match), "ROLE_PERSON_PATTERN", 0.72) for match in ROLE_PERSON.findall(text))

        for raw, trigger, confidence in hits:
            key = normalise(raw)
            if len(key) < 4 or len(key.split()) > 12:
                continue
            record = found.setdefault(key, {
                "fingerprint": hashlib.sha256(key.encode("utf-8")).hexdigest()[:16],
                "candidate_name": raw,
                "normalised": key,
                "confidence": confidence,
                "triggers": set(),
                "paths": set(),
                "canonical_id": alias_to_id.get(key),
            })
            record["confidence"] = max(record["confidence"], confidence)
            record["triggers"].add(trigger)
            if len(record["paths"]) < 20:
                record["paths"].add(rel)

    candidates = []
    for key, row in found.items():
        decision = decision_by_name.get(key)
        status = "REGISTERED" if row["canonical_id"] else (decision or {}).get("decision", "MAYBE_REVIEW")
        candidates.append({
            "fingerprint": row["fingerprint"],
            "candidate_name": row["candidate_name"],
            "normalised": key,
            "confidence": round(row["confidence"], 2),
            "triggers": sorted(row["triggers"]),
            "paths": sorted(row["paths"]),
            "canonical_id": row["canonical_id"],
            "status": status,
            "boundary": "Discovery only; no identity, mandate, knowledge, control, conflict or liability inference."
        })
    candidates.sort(key=lambda row: (row["status"] == "REGISTERED", -row["confidence"], row["normalised"]))
    return {
        "schema": "por-derecho.entity-census.v1",
        "control_date": "2026-09-04",
        "scanner": "scripts/build_entity_census.py",
        "counts": {
            "discovered": len(candidates),
            "registered": sum(row["status"] == "REGISTERED" for row in candidates),
            "review": sum(row["status"] != "REGISTERED" for row in candidates),
            "controlled_id_errors": len(controlled_id_errors),
        },
        "controlled_id_errors": controlled_id_errors,
        "candidates": candidates,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="validate governance invariants and exit non-zero on controlled failures")
    parser.add_argument("--output", type=Path, help="write the generated census JSON")
    args = parser.parse_args()

    records, alias_to_id, index = load_registry()
    decisions = load_json(DECISIONS) if DECISIONS.is_file() else {"candidates": []}
    census = build_census(alias_to_id, decisions)

    unresolved_yes = [row for row in decisions.get("candidates", []) if row.get("decision") == "YES_NOW" and normalise(row.get("candidate_name")) not in alias_to_id]
    if unresolved_yes:
        raise AssertionError(f"YES_NOW candidates remain unregistered: {[row.get('candidate_name') for row in unresolved_yes]}")
    if census["controlled_id_errors"]:
        raise AssertionError(f"Unknown data-canonical-id references: {census['controlled_id_errors'][:10]}")

    uria_id = alias_to_id.get(normalise("Uría Menéndez"))
    if uria_id != "PD-SP-O-0084":
        raise AssertionError(f"Uría canonical resolution failed: {uria_id}")
    if alias_to_id.get(normalise("Uriel Abogados")) == uria_id:
        raise AssertionError("Uría / Uriel collision guard failed")

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(census, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"registry_records": len(records), "control_date": index.get("control_date"), **census["counts"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
