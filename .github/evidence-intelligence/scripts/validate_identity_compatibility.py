#!/usr/bin/env python3
"""Validate the evidence-intelligence pilot against the existing PD-SP identity authority."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

IDENTITY_RE = re.compile(r"^PD-SP-(P|O|S|I|R)-[0-9]{4}$")
EXTENDED_RE = re.compile(r"^PD-SP-(SRC|DOC|MAT|EVT|PROP|ASSET|RIGHT|REC|CIT|EVAL|CUST|RUN)-[0-9]{4}$")
SHA256_RE = re.compile(r"^[a-f0-9]{64}$")
FORBIDDEN_PUBLIC_KEYS = {"gmail_message_id", "drive_file_id", "attachment_id", "message_id", "download_url", "vault_folder_id", "vault_parent_folder_id", "provider_locator", "private_locator"}
FORBIDDEN_PUBLIC_URLS = ("mail.google.com/", "drive.google.com/")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"cannot parse {path}: {exc}") from exc


def walk(value: Any, path: str = "$") -> Iterable[tuple[str, str, Any]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            yield child_path, key, child
            yield from walk(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk(child, f"{path}[{index}]")


def collect_identity_ids(repo: Path, policy: dict[str, Any], errors: list[str]) -> set[str]:
    authority = policy["authoritative_identity_registry"]
    expected_registry_id = authority["registry_id"]
    identity_ids: set[str] = set()
    root_path = repo / authority["root"]
    if not root_path.exists():
        errors.append(f"missing authoritative identity registry root: {root_path}")
    else:
        root = load_json(root_path)
        if root.get("registry_id") != expected_registry_id:
            errors.append("identity registry root ID does not match policy")
    for rel_path in authority["parts"]:
        path = repo / rel_path
        if not path.exists():
            errors.append(f"missing identity registry part: {rel_path}")
            continue
        data = load_json(path)
        if data.get("registry_id") != expected_registry_id:
            errors.append(f"registry ID mismatch in {rel_path}")
        declared_type = data.get("type")
        for record in data.get("records", []):
            identity_id = record.get("id")
            if not isinstance(identity_id, str) or not IDENTITY_RE.fullmatch(identity_id):
                errors.append(f"invalid identity ID in {rel_path}: {identity_id!r}")
                continue
            if record.get("type") != declared_type:
                errors.append(f"record type mismatch for {identity_id} in {rel_path}")
            if identity_id in identity_ids:
                errors.append(f"duplicate immutable identity ID: {identity_id}")
            identity_ids.add(identity_id)
    if "PD-SP-R-0002" not in identity_ids:
        errors.append("PD-SP-R-0002 is missing from the authoritative proceeding registry")
    return identity_ids


def validate_extension_policy(policy: dict[str, Any], errors: list[str]) -> None:
    samples = {
        "SOURCE": "PD-SP-SRC-0001", "DOCUMENT": "PD-SP-DOC-0001", "MATTER": "PD-SP-MAT-0001",
        "EVENT": "PD-SP-EVT-0001", "PROPOSITION": "PD-SP-PROP-0001", "ASSET": "PD-SP-ASSET-0001",
        "RIGHT": "PD-SP-RIGHT-0001", "RECOVERY_OBJECT": "PD-SP-REC-0001", "CITATION": "PD-SP-CIT-0001",
        "EVALUATION": "PD-SP-EVAL-0001", "CUSTODY_MANIFEST": "PD-SP-CUST-0001", "RETRIEVAL_RUN": "PD-SP-RUN-0001"
    }
    extensions = policy.get("extensions", {})
    for name, sample in samples.items():
        pattern = extensions.get(name)
        if not pattern or not re.fullmatch(pattern, sample):
            errors.append(f"invalid or missing extension pattern for {name}")
        if IDENTITY_RE.fullmatch(sample):
            errors.append(f"extension sample collides with identity namespace: {sample}")


def validate_public_json(package_root: Path, identity_ids: set[str], errors: list[str]) -> None:
    for path in sorted(package_root.rglob("*.json")):
        data = load_json(path)
        raw = path.read_text(encoding="utf-8")
        if re.search(r"\bPD-ENT-[0-9]{1,8}\b", raw):
            errors.append(f"competing PD-ENT identity detected in {path}")
        for forbidden_url in FORBIDDEN_PUBLIC_URLS:
            if forbidden_url in raw:
                errors.append(f"private provider URL detected in public file {path}")
        for value_path, key, value in walk(data):
            if key in FORBIDDEN_PUBLIC_KEYS:
                errors.append(f"private locator key {key!r} at {path}:{value_path}")
            values = [value] if isinstance(value, str) else ([item for item in value if isinstance(item, str)] if isinstance(value, list) else [])
            for item in values:
                if IDENTITY_RE.fullmatch(item) and item not in identity_ids:
                    errors.append(f"unknown identity reference {item} in {path}:{value_path}")


def validate_custody_summary(path: Path, errors: list[str]) -> None:
    data = load_json(path)
    if data.get("custody_manifest_id") != "PD-SP-CUST-0001" or data.get("proceeding_id") != "PD-SP-R-0002":
        errors.append("custody pilot identity/proceeding mismatch")
    documents = data.get("documents", [])
    if len(documents) != 4:
        errors.append(f"expected four public custody document records, found {len(documents)}")
    ids, hashes = set(), set()
    for document in documents:
        document_id, digest = document.get("document_id"), document.get("sha256")
        if not isinstance(document_id, str) or not re.fullmatch(r"^PD-SP-DOC-[0-9]{4}$", document_id):
            errors.append(f"invalid document ID: {document_id!r}")
        elif document_id in ids:
            errors.append(f"duplicate document ID: {document_id}")
        else:
            ids.add(document_id)
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            errors.append(f"invalid SHA-256 for {document_id}")
        elif digest in hashes:
            errors.append(f"duplicate canonical stored hash: {digest}")
        else:
            hashes.add(digest)
        if document.get("publication_state") != "PRIVATE_NATIVE_PUBLIC_HASH_ONLY" or document.get("source_class") != "PD_NATIVE_PRIVATE":
            errors.append(f"unsafe public state for {document_id}")
        if document.get("bytes", 0) <= 0 or document.get("pages", 0) <= 0 or not document.get("limitations"):
            errors.append(f"incomplete integrity metadata for {document_id}")


def validate_queries(path: Path, errors: list[str]) -> None:
    evaluations = load_json(path).get("evaluations", [])
    ids = set()
    if len(evaluations) < 5:
        errors.append("retrieval pilot must contain at least five evaluations")
    for evaluation in evaluations:
        evaluation_id = evaluation.get("evaluation_id")
        if not isinstance(evaluation_id, str) or not re.fullmatch(r"^PD-SP-EVAL-[0-9]{4}$", evaluation_id):
            errors.append(f"invalid evaluation ID: {evaluation_id!r}")
        elif evaluation_id in ids:
            errors.append(f"duplicate evaluation ID: {evaluation_id}")
        else:
            ids.add(evaluation_id)
        if evaluation.get("proceeding_id") != "PD-SP-R-0002" or not evaluation.get("expected_any"):
            errors.append(f"evaluation {evaluation_id} escapes the controlled matter or lacks expectations")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()
    repo = Path(args.repo_root).resolve()
    package_root = repo / ".github/evidence-intelligence"
    errors: list[str] = []
    required = [package_root / "id-extension-policy.json", package_root / "source-classes.json", package_root / "schemas/evidence-intelligence.schema.json", package_root / "pilots/rpl2523/corpus.json", package_root / "pilots/rpl2523/queries.json", package_root / "pilots/rpl2523/custody-public-summary.json"]
    for path in required:
        if not path.exists(): errors.append(f"missing required pilot file: {path}")
    if not errors:
        policy = load_json(package_root / "id-extension-policy.json")
        identity_ids = collect_identity_ids(repo, policy, errors)
        validate_extension_policy(policy, errors)
        validate_public_json(package_root, identity_ids, errors)
        validate_custody_summary(package_root / "pilots/rpl2523/custody-public-summary.json", errors)
        validate_queries(package_root / "pilots/rpl2523/queries.json", errors)
    if errors:
        print("Evidence-intelligence identity/public-boundary validation FAILED", file=sys.stderr)
        for item in errors: print(f"- {item}", file=sys.stderr)
        return 1
    print(f"Evidence-intelligence identity/public-boundary validation PASS: {len(identity_ids)} authoritative identities; PD-SP-R-0002 preserved; no competing identity namespace or private provider locators detected.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
