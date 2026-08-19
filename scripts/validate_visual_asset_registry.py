#!/usr/bin/env python3
"""Validate Por Derecho's canonical visual-asset identity registry.

The validator deliberately does not perform facial recognition. It verifies repository
identity mappings, byte locks, actor-directory coverage, sidecar slot maps and textual
references to actor assets.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "assets" / "visual-asset-registry.json"
ACTORS_DIR = ROOT / "assets" / "actors"
COMPOSITES_DIR = ROOT / "assets" / "composites"

ACTIVE_STATUS = "LOCKED_CANONICAL_REPOSITORY_ASSET"
PENDING_STATUSES = {
    "USER_CONFIRMED_PENDING_REPOSITORY_IMPORT",
    "PENDING_IDENTITY_VERIFICATION",
    "PENDING_PROVENANCE_VERIFICATION",
}
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}
TEXT_SUFFIXES = {".html", ".htm", ".js", ".mjs", ".css", ".md", ".json", ".xml", ".yml", ".yaml"}
ACTOR_REFERENCE_RE = re.compile(
    r"(?:/por-derecho/|(?:\.\./|\./)*)?assets/actors/([A-Za-z0-9._-]+\.(?:jpg|jpeg|png|webp|gif|avif))",
    re.IGNORECASE,
)


def load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"Missing required file: {path.relative_to(ROOT)}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()  # noqa: S324 - Git object identity uses SHA-1.


def iter_text_files() -> list[Path]:
    excluded_parts = {".git", "node_modules", "vendor"}
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in excluded_parts for part in path.parts):
            continue
        files.append(path)
    return files


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        registry = load_json(REGISTRY_PATH)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    assets = registry.get("assets")
    if not isinstance(assets, dict) or not assets:
        errors.append("Registry must contain a non-empty object named 'assets'.")
        assets = {}

    registered_paths: dict[str, str] = {}
    canonical_names: dict[str, str] = {}

    for asset_id, entry in assets.items():
        if not isinstance(entry, dict):
            errors.append(f"{asset_id}: entry must be an object.")
            continue

        subject_type = entry.get("subject_type")
        canonical_name = entry.get("canonical_name")
        status = entry.get("identity_status")
        path_value = entry.get("path")

        if subject_type not in {"person", "place", "document", "institution", "object"}:
            errors.append(f"{asset_id}: unsupported or missing subject_type: {subject_type!r}.")
        if not isinstance(canonical_name, str) or not canonical_name.strip():
            errors.append(f"{asset_id}: canonical_name is required.")
        elif subject_type == "person":
            previous = canonical_names.get(canonical_name)
            if previous and not entry.get("variant_of"):
                errors.append(
                    f"{asset_id}: duplicate canonical person name also used by {previous}; "
                    "declare variant_of for legitimate variants."
                )
            canonical_names[canonical_name] = asset_id

        if status == ACTIVE_STATUS:
            if not isinstance(path_value, str) or not path_value:
                errors.append(f"{asset_id}: active asset requires a repository path.")
                continue
            rel_path = Path(path_value)
            if rel_path.is_absolute() or ".." in rel_path.parts:
                errors.append(f"{asset_id}: path must be repository-relative and traversal-free.")
                continue
            full_path = ROOT / rel_path
            if not full_path.is_file():
                errors.append(f"{asset_id}: active file missing: {path_value}.")
                continue
            expected_blob = entry.get("git_blob_sha")
            actual_blob = git_blob_sha(full_path)
            if not isinstance(expected_blob, str) or len(expected_blob) != 40:
                errors.append(f"{asset_id}: active asset requires a 40-character git_blob_sha.")
            elif actual_blob != expected_blob:
                errors.append(
                    f"{asset_id}: byte lock mismatch for {path_value}: "
                    f"registry={expected_blob}, actual={actual_blob}. "
                    "Do not overwrite an identity asset silently; create a new variant or update the lock with provenance."
                )
            if path_value in registered_paths:
                errors.append(
                    f"{asset_id}: path {path_value} is already assigned to {registered_paths[path_value]}."
                )
            registered_paths[path_value] = asset_id

            if subject_type == "person" and not path_value.startswith("assets/actors/"):
                errors.append(f"{asset_id}: active named-person image must live under assets/actors/.")
            if subject_type == "person":
                if not entry.get("identity_basis"):
                    errors.append(f"{asset_id}: person asset requires identity_basis.")
                if not entry.get("alt_en") or not entry.get("alt_es"):
                    errors.append(f"{asset_id}: person asset requires bilingual alt text.")

        elif status in PENDING_STATUSES:
            if path_value is not None:
                errors.append(
                    f"{asset_id}: pending asset must keep path=null until repository import and byte lock are complete."
                )
            if entry.get("git_blob_sha") is not None:
                errors.append(f"{asset_id}: pending asset must keep git_blob_sha=null.")
            if not entry.get("publication_rule"):
                warnings.append(f"{asset_id}: pending asset should state an explicit publication_rule.")
        else:
            errors.append(f"{asset_id}: unknown identity_status {status!r}.")

        exclusions = entry.get("do_not_confuse_with", [])
        if exclusions is not None and not isinstance(exclusions, list):
            errors.append(f"{asset_id}: do_not_confuse_with must be a list.")
        elif isinstance(exclusions, list):
            for excluded_id in exclusions:
                if excluded_id not in assets:
                    errors.append(f"{asset_id}: unknown do_not_confuse_with asset ID {excluded_id!r}.")

    # Every actor image in the canonical directory must be registered.
    if not ACTORS_DIR.is_dir():
        errors.append("Missing assets/actors directory.")
    else:
        for path in sorted(ACTORS_DIR.iterdir()):
            if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
                continue
            rel = path.relative_to(ROOT).as_posix()
            if rel not in registered_paths:
                errors.append(f"Unregistered named-person image: {rel}.")

    # Composite slot maps are identity contracts.
    if COMPOSITES_DIR.is_dir():
        for sidecar in sorted(COMPOSITES_DIR.glob("*.asset-map.json")):
            try:
                mapping = load_json(sidecar)
            except ValueError as exc:
                errors.append(str(exc))
                continue
            slots = mapping.get("slots")
            status = mapping.get("publication_status")
            if not isinstance(slots, dict) or not slots:
                errors.append(f"{sidecar.relative_to(ROOT)}: non-empty slots object required.")
                continue
            unresolved: list[str] = []
            for slot_name, asset_id in slots.items():
                if asset_id not in assets:
                    errors.append(
                        f"{sidecar.relative_to(ROOT)}: slot {slot_name!r} uses unknown asset ID {asset_id!r}."
                    )
                    continue
                if assets[asset_id].get("identity_status") != ACTIVE_STATUS:
                    unresolved.append(f"{slot_name}={asset_id}")
            if status == "READY" and unresolved:
                errors.append(
                    f"{sidecar.relative_to(ROOT)}: READY composite has unresolved assets: "
                    + ", ".join(unresolved)
                )
            if status != "READY" and not unresolved:
                warnings.append(
                    f"{sidecar.relative_to(ROOT)}: all assets are active; consider changing publication_status to READY."
                )

    # Text references may use only registered actor paths.
    for path in iter_text_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for match in ACTOR_REFERENCE_RE.finditer(text):
            rel = f"assets/actors/{match.group(1)}"
            if rel not in registered_paths:
                errors.append(
                    f"{path.relative_to(ROOT)} references unregistered actor asset {rel}."
                )

    # Critical reciprocal confusion lock for Borja and Eduardo.
    borja_id = "person.francisco-de-borja-rodriguez-batllori.primary"
    eduardo_id = "person.eduardo-sanchez-san-telmo.primary"
    if borja_id in assets and eduardo_id in assets:
        if eduardo_id not in assets[borja_id].get("do_not_confuse_with", []):
            errors.append("Borja registry entry must explicitly exclude the Eduardo asset ID.")
        if borja_id not in assets[eduardo_id].get("do_not_confuse_with", []):
            errors.append("Eduardo registry entry must explicitly exclude the Borja asset ID.")

    if warnings:
        print("WARNINGS:")
        for warning in sorted(set(warnings)):
            print(f"  - {warning}")

    if errors:
        print("ERRORS:")
        for error in sorted(set(errors)):
            print(f"  - {error}")
        print(f"Visual asset identity validation failed with {len(set(errors))} error(s).")
        return 1

    active_count = sum(1 for entry in assets.values() if entry.get("identity_status") == ACTIVE_STATUS)
    pending_count = sum(1 for entry in assets.values() if entry.get("identity_status") in PENDING_STATUSES)
    print(
        "Visual asset identity validation passed: "
        f"{active_count} active byte-locked assets, {pending_count} pending asset(s), "
        f"{len(registered_paths)} registered repository paths."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
