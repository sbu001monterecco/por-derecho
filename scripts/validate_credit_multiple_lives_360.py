#!/usr/bin/env python3
"""Validate the 26-Aug-2026 multiple-credit-lives/NPL/notarial 360 package."""

from __future__ import annotations

import json
import re
from decimal import Decimal
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

FILES = {
    "control": ROOT / "archive/BANKIA_SAREB_PH122_CAM_CREDIT_MULTIPLE_LIVES_BANKING_CRIME_360_CONTROL_26AUG2026.md",
    "prompt": ROOT / "archive/prompts/BANKIA_SAREB_PH122_CAM_CREDIT_MULTIPLE_LIVES_CRIMINAL_360_PROMPT_26AUG2026.md",
    "declaration": ROOT / "archive/declarations/016_GIL_CREDIT_MULTIPLE_LIVES_NPL_NOTARIAL_ALLEGATION_20260826.md",
    "declaration_index": ROOT / "archive/declarations/INDEX.md",
    "declaration_readme": ROOT / "archive/declarations/README.md",
    "start": ROOT / "CHATGPT_START_HERE.md",
    "prompt_library": ROOT / "archive/CHATGPT_PROMPT_LIBRARY.md",
    "allegations_gate": ROOT / "archive/knowledge-project/ALLEGATIONS_RETRIEVAL_GATE_16AUG2026.md",
    "allegations_crosswalk": ROOT / "archive/knowledge-project/ALLEGATIONS_CROSSWALK_AN2023_DP1901_DP1956_CONTROL24_16AUG2026.md",
    "redigest": ROOT / "archive/SUN_PARK_UNITARY_REPOSITORY_WEBSITE_REDIGEST_21AUG2026.md",
    "maintenance": ROOT / "archive/CONTINUOUS_MAINTENANCE_MATRIX.md",
    "gaps": ROOT / "archive/MISSING_EVIDENCE_REGISTER.md",
    "corrections": ROOT / "archive/CORRECTION_REGISTER.md",
    "multiple_lives": ROOT / "research/lender-of-record-liability/data/multiple-credit-lives.json",
    "lender_manifest": ROOT / "research/lender-of-record-liability/data/manifest.json",
    "transfers": ROOT / "research/lender-of-record-liability/data/transfers.json",
    "sources": ROOT / "research/lender-of-record-liability/data/sources.json",
    "complete_record": ROOT / "archive/CONCURSO36_COMPLETE_RECORD_EXECUTION_DIGEST_23AUG2026.md",
    "primary_autos": ROOT / "archive/concurso36-primary-autos-21aug2026/FORENSIC_SCAN_CRITICAL_AUTOS_CONCURSO_36_2012_21AUG2026.md",
    "handover": ROOT / "CURRENT_HANDOVER_DP1956_DP1901_JUDICIAL_ROUTES_21AUG2026.md",
    "dp1956_control": ROOT / "archive/knowledge-project/DP1956_STATUS_REOPENING_CORRECTION_18AUG2026.md",
    "recovery_ledger": ROOT / "archive/RECOVERY_CAUSATION_MATRIX_CONCURSO36_15AUG2026.md",
    "valencia_ledger": ROOT / "archive/VALENCIA_BANKING_CONCURSAL_RECONCILIATION_LEDGER_16AUG2026.md",
    "adjudication_activation": ROOT / "operations/ADJUDICACION_2022_RECONSTRUCTION_ACTIVATION_2026-08-19.md",
    "old_audit": ROOT / "archive/THREAD_DELETION_REAUDIT_PRESERVE_ALL_CASE_INFORMATION_ARCHITECTURE_20AUG2026.md",
    "old_manifest": ROOT / "publication-manifests/adjudicacion-2022-reconstruction-2026-08-19.json",
    "complete_record_manifest": ROOT / "publication-manifests/concurso36-complete-record-20260823.json",
    "manifest": ROOT / "publication-manifests/credit-multiple-lives-npl-notarial-360-20260826.json",
    "audit": ROOT / "docs/deletion-audits/2026-08-26-credit-multiple-lives-npl-notarial-360-thread.md",
    "audit_index": ROOT / "docs/deletion-audits/README.md",
    "styles": ROOT / "assets/styles.css",
    "architecture": ROOT / "assets/case-information-architecture-20260819.js",
    "criminal_data": ROOT / "research/unitary-criminal-reverse-engineering/data/top_points.json",
}

PAIR_SPECS = [
    ("es/index.html", "en/index.html"),
    ("es/reclamacion-caixabank-valencia/index.html", "en/caixabank-valencia-claim/index.html"),
    ("es/acreedor-de-registro/responsabilidad/index.html", "en/lender-of-record/liability/index.html"),
    ("es/perimetro-ph122-cerberus-haya-bankia-externo/index.html", "en/ph122-cerberus-haya-bankia-external-perimeter/index.html"),
    ("es/ingenieria-forense-criminal-sun-park/index.html", "en/sun-park-criminal-engineering-investigation/index.html"),
    ("es/implementacion-notarial-protocolo-457/index.html", "en/notarial-implementation-protocol-457/index.html"),
    ("es/dp-1956-2026/index.html", "en/dp-1956-2026/index.html"),
    ("es/actualizaciones/index.html", "en/updates/index.html"),
    ("es/pacto-comisorio-arquitectura-credito-titulo/index.html", "en/pacto-comisorio-credit-to-title-architecture/index.html"),
]

REQUIRED = {
    "control": [
        "ALG-NPL-019",
        "Promontoria Holding 122 B.V. (PH122)",
        "€13,065,186.68",
        "€102,895.34",
        "no internal €30 error",
        "not a judicial finding",
        "CP 130.2",
        "single-satisfaction ledger",
    ],
    "prompt": [
        "ALG-NPL-019",
        "Promontoria Holding 122 B.V.",
        "Protocol 870",
        "Protocol 457",
        "CP 130.2",
        "never authorises an email",
    ],
    "declaration": [
        "# DECLARATION 016",
        "Renumbering note",
        "D016-P10",
        "ALG-NPL-019",
        "direct party allegation",
        "not a finding",
        "€13,065,186.68",
        "€102,895.34",
    ],
    "declaration_index": ["| 016 | 2026-08-26 |", "siguiente declaración disponible es **017**"],
    "declaration_readme": ["Declaration 016", "016_GIL_CREDIT_MULTIPLE_LIVES_NPL_NOTARIAL_ALLEGATION_20260826.md"],
    "start": ["ALG-NPL-019", "BANKIA_SAREB_PH122_CAM_CREDIT_MULTIPLE_LIVES_BANKING_CRIME_360_CONTROL_26AUG2026.md"],
    "prompt_library": ["ALG-NPL-019", "BANKIA_SAREB_PH122_CAM_CREDIT_MULTIPLE_LIVES_CRIMINAL_360_PROMPT_26AUG2026.md"],
    "allegations_gate": ["ALG-NPL-019", "direct attribution to Gil Marer and Aweswell"],
    "allegations_crosswalk": ["ALG-NPL-019", "Promontoria Holding 122 B.V."],
    "redigest": ["ALG-NPL-019", "Bankia → SAREB → PH122 → CAM"],
    "maintenance": ["ALG-NPL-019", "ME-093", "CR-099"],
    "gaps": ["| ME-093 |", "Protocol 2,248", "single-satisfaction"],
    "corrections": ["| CR-099 |", "€13,065,186.68", "€102,895.34"],
    "audit": ["Declaration 016", "ALG-NPL-019", "THREAD_REASONING_CONTINUITY", "PRIMARY_EVIDENCE_COMPLETENESS"],
    "audit_index": ["credit-multiple-lives-npl-notarial-360-thread.md"],
    "styles": ["#credit-procedural-lives .button.secondary", "#vidas-procesales-credito .button.secondary"],
    "architecture": ["13.065.186,68", "102.895,34"],
}

PUBLIC_FORBIDDEN = [
    "Promontoria Holding 1112",
    "Promotoria Holding 122",
    "The burden has shifted",
    "La carga ha cambiado",
    "was the economic beneficiary of every collection",
    "fue el beneficiario económico de todo cobro",
]

PRIVATE_LOCATORS = [
    re.compile(r"/workspace/", re.I),
    re.compile(r"/tmp/", re.I),
    re.compile(r"[A-Z]:\\\\", re.I),
    re.compile(r"mail\.google\.com", re.I),
    re.compile(r"drive\.google\.com/drive/u/", re.I),
    re.compile(r"[A-Z0-9._%+-]+@gmail\.com", re.I),
]


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.sections = 0
        self.tables = 0
        self.warn_depth = 0
        self.warn_parts: list[str] = []
        self.warn_blocks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if attr.get("id"):
            self.ids.append(str(attr["id"]))
        if tag == "section":
            self.sections += 1
        if tag == "table":
            self.tables += 1
        if tag == "div":
            classes = set((attr.get("class") or "").split())
            if self.warn_depth:
                self.warn_depth += 1
            elif "warn" in classes:
                self.warn_depth = 1
                self.warn_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "div" and self.warn_depth:
            self.warn_depth -= 1
            if self.warn_depth == 0:
                self.warn_blocks.append(" ".join(" ".join(self.warn_parts).split()))
                self.warn_parts = []

    def handle_data(self, data: str) -> None:
        if self.warn_depth:
            self.warn_parts.append(data)


def text_for(path: Path, failures: list[str]) -> str:
    if not path.is_file():
        failures.append(f"missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def dec(value: object) -> Decimal:
    return Decimal(str(value))


def require_equal(actual: Decimal, expected: Decimal, label: str, failures: list[str]) -> None:
    if actual != expected:
        failures.append(f"{label}: expected {expected}, got {actual}")


def main() -> None:
    failures: list[str] = []
    cache: dict[str, str] = {}

    for key, path in FILES.items():
        cache[key] = text_for(path, failures)
    for key, markers in REQUIRED.items():
        content = cache.get(key, "")
        for marker in markers:
            if marker not in content:
                failures.append(f"{FILES[key].relative_to(ROOT)} missing marker: {marker}")

    parsed_pages: dict[str, tuple[str, PageParser]] = {}
    for es_rel, en_rel in PAIR_SPECS:
        for rel in (es_rel, en_rel):
            page = ROOT / rel
            html = text_for(page, failures)
            parser = PageParser()
            if html:
                try:
                    parser.feed(html)
                    parser.close()
                except Exception as exc:  # pragma: no cover - diagnostic guard
                    failures.append(f"{rel} HTML parser failure: {exc}")
            duplicates = sorted({value for value in parser.ids if parser.ids.count(value) > 1})
            if duplicates:
                failures.append(f"{rel} duplicate HTML ids: {', '.join(duplicates)}")
            for forbidden in PUBLIC_FORBIDDEN:
                if forbidden.casefold() in html.casefold():
                    failures.append(f"{rel} contains forbidden stale wording: {forbidden}")
            parsed_pages[rel] = (html, parser)

        es_parser = parsed_pages[es_rel][1]
        en_parser = parsed_pages[en_rel][1]
        if es_parser.sections != en_parser.sections:
            failures.append(f"section-count parity failed: {es_rel}={es_parser.sections}, {en_rel}={en_parser.sections}")
        if es_parser.tables != en_parser.tables:
            failures.append(f"table-count parity failed: {es_rel}={es_parser.tables}, {en_rel}={en_parser.tables}")

    es_caixa, es_caixa_parser = parsed_pages[PAIR_SPECS[1][0]]
    en_caixa, en_caixa_parser = parsed_pages[PAIR_SPECS[1][1]]
    for marker in ('id="vidas-procesales-credito"', "ALG-NPL-019", "13.168.082,02 €"):
        if marker not in es_caixa:
            failures.append(f"Spanish CaixaBank page missing marker: {marker}")
    for marker in ('id="credit-procedural-lives"', "ALG-NPL-019", "€13,168,082.02"):
        if marker not in en_caixa:
            failures.append(f"English CaixaBank page missing marker: {marker}")
    if not any("ALG-NPL-019" in block and ("no establece" in block.lower() or "no acredita" in block.lower()) for block in es_caixa_parser.warn_blocks):
        failures.append("Spanish CaixaBank allegation and essential non-finding are not co-located in one .warn block")
    if not any("ALG-NPL-019" in block and ("does not establish" in block.lower() or "does not prove" in block.lower()) for block in en_caixa_parser.warn_blocks):
        failures.append("English CaixaBank allegation and essential non-finding are not co-located in one .warn block")

    es_protocol, _ = parsed_pages[PAIR_SPECS[5][0]]
    en_protocol, _ = parsed_pages[PAIR_SPECS[5][1]]
    for marker in ('id="limite-concurso-arrecife"', "159", "13.065.186,68 €", "400.000 €"):
        if marker not in es_protocol:
            failures.append(f"Spanish Protocol 457 page missing marker: {marker}")
    for marker in ('id="insolvency-arrecife-boundary"', "159", "EUR 13,065,186.68", "EUR 400,000"):
        if marker not in en_protocol:
            failures.append(f"English Protocol 457 page missing marker: {marker}")

    for key in ("control", "prompt", "declaration", "redigest", "audit"):
        for locator in PRIVATE_LOCATORS:
            if locator.search(cache[key]):
                failures.append(f"{FILES[key].relative_to(ROOT)} contains private locator pattern: {locator.pattern}")

    json_paths = [
        FILES["multiple_lives"],
        FILES["lender_manifest"],
        FILES["transfers"],
        FILES["sources"],
        FILES["criminal_data"],
        FILES["old_manifest"],
        FILES["complete_record_manifest"],
        FILES["manifest"],
    ]
    parsed_json: dict[Path, object] = {}
    for path in json_paths:
        try:
            parsed_json[path] = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")

    lender_manifest = parsed_json.get(FILES["lender_manifest"])
    allowed_evidence_statuses: set[str] = set()
    allowed_publication_values: set[str] = set()
    if isinstance(lender_manifest, dict):
        status_values = lender_manifest.get("status_values", [])
        publication_values = lender_manifest.get("publication_values", [])
        if not isinstance(status_values, list) or not all(isinstance(value, str) for value in status_values):
            failures.append("lender data manifest status_values must be a list of strings")
        else:
            allowed_evidence_statuses = set(status_values)
        if not isinstance(publication_values, list) or not all(isinstance(value, str) for value in publication_values):
            failures.append("lender data manifest publication_values must be a list of strings")
        else:
            allowed_publication_values = set(publication_values)
    elif lender_manifest is not None:
        failures.append("lender data manifest must contain an object")

    sources = parsed_json.get(FILES["sources"])
    source_ids = {
        row.get("id")
        for row in sources
        if isinstance(sources, list) and isinstance(row, dict) and isinstance(row.get("id"), str)
    } if isinstance(sources, list) else set()

    lives = parsed_json.get(FILES["multiple_lives"])
    if isinstance(lives, dict):
        if lives.get("canonical_allegation_id") != "ALG-NPL-019":
            failures.append("multiple-credit-lives.json canonical allegation is not ALG-NPL-019")
        proposition_rows = lives.get("propositions", [])
        if not isinstance(proposition_rows, list):
            failures.append("multiple-credit-lives.json propositions must be a list")
            proposition_rows = []
        propositions: dict[str, dict[str, object]] = {}
        for index, row in enumerate(proposition_rows):
            where = f"multiple-credit-lives.json propositions[{index}]"
            if not isinstance(row, dict):
                failures.append(f"{where} must be an object")
                continue
            proposition_id = row.get("id")
            if not isinstance(proposition_id, str) or not proposition_id:
                failures.append(f"{where} must have a non-empty string id")
                continue
            if proposition_id in propositions:
                failures.append(f"multiple-credit-lives.json duplicate proposition id: {proposition_id}")
            propositions[proposition_id] = row
            if row.get("evidence_status") not in allowed_evidence_statuses:
                failures.append(
                    f"{proposition_id} invalid evidence_status: {row.get('evidence_status')!r}"
                )
            if row.get("publication") not in allowed_publication_values:
                failures.append(
                    f"{proposition_id} invalid publication: {row.get('publication')!r}"
                )

            def validate_source_refs(value: object, location: str) -> None:
                if isinstance(value, dict):
                    for key, nested in value.items():
                        if key == "source_refs":
                            if not isinstance(nested, list) or not all(isinstance(ref, str) for ref in nested):
                                failures.append(f"{location}.source_refs must be a list of strings")
                            else:
                                for ref in nested:
                                    if ref not in source_ids:
                                        failures.append(f"{location} has unknown source_ref: {ref}")
                        else:
                            validate_source_refs(nested, f"{location}.{key}")
                elif isinstance(value, list):
                    for nested_index, nested in enumerate(value):
                        validate_source_refs(nested, f"{location}[{nested_index}]")

            validate_source_refs(row, proposition_id)
        p869 = propositions.get("MCL-PROTOCOL-869", {}).get("arithmetic", {})
        p870 = propositions.get("MCL-PROTOCOL-870", {}).get("arithmetic", {})
        p457 = propositions.get("MCL-PROTOCOL-457-ARITHMETIC", {})
        require_equal(sum((dec(p869.get(name, 0)) for name in ("principal_eur", "ordinary_interest_eur", "default_interest_eur")), Decimal("0")), dec(p869.get("total_eur", 0)), "Protocol 869 arithmetic", failures)
        require_equal(sum((dec(p870.get(name, 0)) for name in ("principal_eur", "ordinary_interest_eur", "default_interest_eur")), Decimal("0")), Decimal("1278518.03"), "Protocol 870 arithmetic", failures)
        require_equal(dec(p869.get("total_eur", 0)) + dec(p870.get("total_eur", 0)), Decimal("13165832.36"), "Protocols 869+870", failures)
        require_equal(sum((dec(value) for value in p457.get("printed_components_eur", [])), Decimal("0")), Decimal("13065186.68"), "Protocol 457 printed components", failures)
        require_equal(dec(p457.get("default_interest_cap_eur", 0)) - Decimal("3079104.66"), Decimal("102895.34"), "Protocol 457 cap step", failures)
        require_equal(dec(p457.get("printed_components_total_eur", 0)) + dec(p457.get("cap_step_eur", 0)), dec(p457.get("stated_consideration_eur", 0)), "Protocol 457 stated consideration", failures)
        require_equal(Decimal("839441") - Decimal("839411"), Decimal("30"), "cross-source principal movement", failures)
    elif lives is not None:
        failures.append("multiple-credit-lives.json must contain an object")

    manifest = parsed_json.get(FILES["manifest"])
    if isinstance(manifest, dict):
        if manifest.get("canonical_allegation") != "ALG-NPL-019":
            failures.append("publication manifest canonical allegation mismatch")
        if manifest.get("remote_branch") != "codex/credit-multiple-lives-criminal-360-20260826":
            failures.append("publication manifest remote branch mismatch")
        reconciliation = manifest.get("authorization", {}).get("declaration_number_reconciliation", {})
        if reconciliation.get("requested_number") != "015" or reconciliation.get("repository_number") != "016":
            failures.append("publication manifest lacks the 015-to-016 collision reconciliation")
        routes = manifest.get("expected_routes", {})
        if routes.get("es") != [pair[0] for pair in PAIR_SPECS] or routes.get("en") != [pair[1] for pair in PAIR_SPECS]:
            failures.append("publication manifest route arrays do not exactly match the controlled ES/EN pairs")
        for rel in manifest.get("expected_source_files", []):
            if not isinstance(rel, str) or not (ROOT / rel).is_file():
                failures.append(f"publication manifest expected source does not exist: {rel}")
    elif manifest is not None:
        failures.append("publication manifest must contain an object")

    for key in ("old_manifest", "complete_record_manifest"):
        prior = parsed_json.get(FILES[key])
        if isinstance(prior, dict):
            correction = prior.get("later_correction", {})
            if correction.get("publication_id") != "CREDIT-MULTIPLE-LIVES-NPL-NOTARIAL-360-20260826":
                failures.append(f"{FILES[key].relative_to(ROOT)} lacks the current later-correction provenance pointer")

    if failures:
        raise SystemExit("\n".join(f"FAIL: {item}" for item in failures))
    print("PASS: credit multiple-lives / NPL / notarial 360 controls, arithmetic and ES/EN parity")


if __name__ == "__main__":
    main()
