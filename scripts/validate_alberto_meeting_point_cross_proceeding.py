#!/usr/bin/env python3
"""Validate the Magistrate López Villarrubia / Meeting Point criminal-first module.

The control is deliberately structural. It validates the finite specialist
caret census, its separation from the unitary census, the typed evidence graph,
the rendered six-field rows and their hashes, and links in both directions.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ROOT_RESOLVED = ROOT.resolve()

ES = ROOT / "es/alberto-lopez-villarrubia-meeting-point-357-masa-activa/index.html"
EN = ROOT / "en/alberto-lopez-villarrubia-meeting-point-357-active-estate/index.html"
MATRIX_PATH = ROOT / "assets/data/alberto-meeting-point-357-multidirectional-evidence-v1.json"
CARET_PATH = ROOT / "assets/data/caepr-caret-alberto-meeting-point-357-v1.json"
FIRST_HOP_CARET_PATH = ROOT / "assets/data/caepr-caret-alberto-meeting-point-first-hop-v1.json"
UNITARY_CARET_PATH = ROOT / "assets/data/caepr-caret-unitary-digest-v1.json"
REGISTRY_PATH = ROOT / "assets/data/matter-identity-registry-v1.json"
AUDIT_PATH = ROOT / "archive/ALBERTO_MEETING_POINT_357_CROSS_PROCEEDING_CARET_AUDIT_26AUG2026.md"
HUMAN_MATRIX_PATH = ROOT / "archive/ALBERTO_MEETING_POINT_357_MULTIDIRECTIONAL_CRIMINAL_FIRST_MATRIX_27AUG2026.md"
TITLE_CONTROL_PATH = ROOT / "archive/ALBERTO_LOPEZ_VILLARRUBIA_JUDICIAL_TITLE_AND_COURT_REORGANISATION_CONTROL_27AUG2026.md"
PLAN_PATH = ROOT / "ops/ALBERTO_MEETING_POINT_357_AUTHORITY_SUBMISSION_PLAN_26AUG2026.md"
MANIFEST_PATH = ROOT / "publication-manifests/alberto-meeting-point-multidirectional-criminal-first-20260827.json"
CURRENT_DIGEST_MD_PATH = ROOT / "CURRENT_REVERSE_ENGINEERED_DIGEST.md"
CURRENT_DIGEST_JSON_PATH = ROOT / "ops/CURRENT_REVERSE_ENGINEERED_DIGEST.json"

CONTROL_ID = "PD-ALV-MP357-MULTI-20260827-01"
CARET_CONTROL_ID = "PD-ALV-MP357-CARET-20260827-01"
FIRST_HOP_CARET_CONTROL_ID = "PD-ALV-MP357-FIRST-HOP-CARET-20260827-01"
UNITARY_SCOPE_CONTROL_ID = "PD-UNITARY-REDIGEST-20260827-01"
CANONICAL_UNITARY_CARET_CONTROL_ID = "PD-CAEPR-CARET-UNITARY-DIGEST-20260826-01"
NODE_IDS = tuple(f"AM357-N{number:02d}" for number in range(1, 10))
NODE_ID_SET = set(NODE_IDS)
MATRIX_FIELDS = (
    "source-supported-fact",
    "supported-investigative-inference",
    "criminal-first-element-gate",
    "strongest-counterevidence",
    "falsification-production-target",
    "reciprocal-links",
)
EVIDENCE_KEYS = {
    "source_refs",
    "attributed_statement_refs",
    "adverse_procedural_refs",
    "control_refs",
    "missing_evidence_refs",
    "integrity_refs",
    "external_sources",
    "source_registers",
}
EDGE_CONTRACT_FIELDS = {
    "edge_id",
    "from",
    "to",
    "evidence_lane",
    "support_level",
    "source_refs",
    "forward_inference",
    "reverse_falsification",
    "strongest_contrary_evidence",
    "confirm_or_falsify_production",
}

EXPECTED_CONFIRMED = {
    "PD-SP-P-0001": "PERSON",
    "PD-SP-P-0057": "PERSON",
    "PD-SP-P-0010": "PERSON",
    "PD-SP-P-0087": "PERSON",
    "PD-SP-O-0001": "ORGANISATION",
    "PD-SP-O-0002": "ORGANISATION",
    "PD-SP-O-0007": "ORGANISATION",
    "PD-SP-O-0005": "ORGANISATION",
    "PD-SP-O-0006": "ORGANISATION",
    "PD-SP-O-0038": "ORGANISATION",
    "PD-SP-O-0040": "ORGANISATION",
    "PD-SP-O-0067": "ORGANISATION",
    "PD-SP-O-0068": "ORGANISATION",
    "PD-SP-O-0069": "ORGANISATION",
    "PD-SP-O-0070": "ORGANISATION",
    "PD-SP-O-0046": "ORGANISATION",
    "PD-SP-O-0071": "ORGANISATION",
    "PD-SP-O-0075": "ORGANISATION",
    "PD-SP-O-0076": "ORGANISATION",
    "PD-SP-I-0001": "INSTITUTION",
    "PD-SP-I-0016": "INSTITUTION",
    "PD-SP-I-0017": "INSTITUTION",
    "PD-SP-I-0018": "INSTITUTION",
    "PD-SP-I-0002": "INSTITUTION",
    "PD-SP-I-0005": "INSTITUTION",
    "PD-SP-I-0019": "INSTITUTION",
    "PD-SP-I-0020": "INSTITUTION",
    "PD-SP-I-0022": "INSTITUTION",
    "PD-SP-R-0001": "PROCEEDING",
    "PD-SP-R-0018": "PROCEEDING",
    "PD-SP-R-0019": "PROCEEDING",
}
EXPECTED_PENDING = {}
SPECIALIST_SPAN_KEYS = {
    "FTI_COMMERCIAL_GROUP_PERIMETER",
    "ONA_FUNDED_EXIT_ACTOR",
    "CLUBOTEL_ENTITY",
    "COMPETENT_TSJ_ROUTE",
    "LAS_PALMAS_PROVINCIAL_PROSECUTOR",
    "TRIBUNAL_DE_CUENTAS",
    "CGPJ_ALZADA_286_2026",
}
NEW_SPECIALIST_IDS = {"PD-SP-O-0075", "PD-SP-O-0076", "PD-SP-I-0019", "PD-SP-I-0020", "PD-SP-I-0022", "PD-SP-R-0019"}
EXPECTED_LINKED_CONFIRMED = set(EXPECTED_CONFIRMED) - NEW_SPECIALIST_IDS
EXPECTED_CARET_TYPE_COUNTS = {
    "PERSON": {"eligible": 4, "confirmed": 4, "pending": 0},
    "ORGANISATION": {"eligible": 15, "occurrence_rows": 16, "confirmed": 15, "confirmed_occurrence_rows": 16, "pending": 0},
    "INSTITUTION": {"eligible": 9, "confirmed": 9, "pending": 0},
    "PROCEEDING": {"eligible": 3, "confirmed": 3, "pending": 0},
}
EXPECTED_REGISTRY_COUNTS = {
    "total": 336,
    "PERSON": 157,
    "ORGANISATION": 83,
    "STRUCTURE": 11,
    "INSTITUTION": 43,
    "PROCEEDING": 43,
}
CURRENT_CANONICAL_REGISTRY_COUNTS = {
    "total": 342,
    "PERSON": 162,
    "ORGANISATION": 83,
    "STRUCTURE": 11,
    "INSTITUTION": 43,
    "PROCEEDING": 43,
}
EXPECTED_SPECIALIST_LIVE_REGISTRY_COUNTS = {
    "total": 204,
    "PERSON": 87,
    "ORGANISATION": 71,
    "STRUCTURE": 10,
    "INSTITUTION": 18,
    "PROCEEDING": 18,
}
EXPECTED_EDGE_ENDPOINTS = {
    "AM357-E01": ("AM357-N01", "AM357-N02"),
    "AM357-E02": ("AM357-N02", "AM357-N03"),
    "AM357-E03": ("AM357-N08", "AM357-N03"),
    "AM357-E04": ("AM357-N02", "AM357-N04"),
    "AM357-E05": ("AM357-N03", "AM357-N05"),
    "AM357-E06": ("AM357-N05", "AM357-N04"),
    "AM357-E07": ("AM357-N05", "AM357-N06"),
    "AM357-E08": ("AM357-N05", "AM357-N07"),
    "AM357-E09": ("AM357-N01", "AM357-N07"),
    "AM357-E10": ("AM357-N06", "AM357-N07"),
    "AM357-E11": ("AM357-N07", "AM357-N09"),
    "AM357-E12": ("AM357-N04", "AM357-N09"),
    "AM357-E13": ("AM357-N03", "AM357-N04"),
}

SEPI_RELEASE = "https://www.sepi.es/es/sala-de-prensa/noticias/el-consejo-de-ministros-autoriza-nuevas-ayudas-con-cargo-al-fondo-de-apoyo"
SEPI_ACCOUNTS = "https://www.sepi.es/sites/default/files/2024-08/FASEE_Cuentas%20anuales_2023.pdf"


def fs(*items: str) -> frozenset[str]:
    return frozenset(items)


# Category membership is evidential meaning, not merely formatting. Exact
# allowlists stop a source, allegation, adverse act, control or missing item
# silently changing lane.
EXPECTED_EVIDENCE = {
    "AM357-N01": {
        "source_refs": fs("C36-JUD-2012-06-06-001", "C36-JUD-2018-04-16-001", "C36-JUD-2020-05-12-001", "C36-JUD-2021-02-24-001", "C36-JUD-2021-05-12-001", "C36-JUD-2021-05-18-001"),
        "adverse_procedural_refs": fs("C36-JUD-2018-06-26-001", "C36-JUD-2019-10-24-001", "C36-JUD-2019-10-24-002"),
        "missing_evidence_refs": fs("archive/MISSING_EVIDENCE_REGISTER.md#ME-012", "archive/MISSING_EVIDENCE_REGISTER.md#ME-058"),
        "external_sources": fs("https://www.boe.es/buscar/act.php?id=BOE-A-1995-25444#a446", "https://www.boe.es/buscar/act.php?id=BOE-A-1995-25444#a447"),
        "source_registers": fs("archive/CONCURSO_36_2012_JUDICIAL_LAJ_ACTS_MASTER_REGISTER_17AUG2026.md", "archive/CONCURSO_36_2012_CANONICAL_COURT_BINARY_REGISTER_17AUG2026.md", "archive/MISSING_EVIDENCE_REGISTER.md"),
    },
    "AM357-N02": {
        "source_refs": fs("C36-JUD-2018-04-16-001", "C36-JUD-2020-05-12-001", "C36-JUD-2021-02-24-001"),
        "adverse_procedural_refs": fs("C36-JUD-2018-06-26-001", "C36-JUD-2019-10-24-001", "C36-JUD-2019-10-24-002"),
        "missing_evidence_refs": fs("archive/MISSING_EVIDENCE_REGISTER.md#ME-074", "archive/MISSING_EVIDENCE_REGISTER.md#ME-075"),
        "source_registers": fs("archive/CONCURSO_36_2012_JUDICIAL_LAJ_ACTS_MASTER_REGISTER_17AUG2026.md", "archive/CONCURSO_36_2012_CANONICAL_COURT_BINARY_REGISTER_17AUG2026.md", "archive/MISSING_EVIDENCE_REGISTER.md"),
    },
    "AM357-N03": {
        "source_refs": fs("OA-07", "OA-09", "OA-10", "OA-11", "OA-12"),
        "attributed_statement_refs": fs("J7-09", "J7-10"),
        "adverse_procedural_refs": fs("LZ-JUD-003", "LZ-APP-004"),
        "missing_evidence_refs": fs(
            "archive/MISSING_EVIDENCE_REGISTER.md#ME-044", "archive/MISSING_EVIDENCE_REGISTER.md#ME-045", "archive/MISSING_EVIDENCE_REGISTER.md#ME-046", "archive/MISSING_EVIDENCE_REGISTER.md#ME-048", "archive/MISSING_EVIDENCE_REGISTER.md#ME-050",
            "archive/MISSING_EVIDENCE_REGISTER_CAM_7JUNE_CRIMINAL_LEAD_ADDENDUM_23AUG2026.md#ME-CAM7J-003", "archive/MISSING_EVIDENCE_REGISTER_CAM_7JUNE_CRIMINAL_LEAD_ADDENDUM_23AUG2026.md#ME-CAM7J-004", "archive/MISSING_EVIDENCE_REGISTER_CAM_7JUNE_CRIMINAL_LEAD_ADDENDUM_23AUG2026.md#ME-CAM7J-005", "archive/MISSING_EVIDENCE_REGISTER_CAM_7JUNE_CRIMINAL_LEAD_ADDENDUM_23AUG2026.md#ME-CAM7J-006", "archive/MISSING_EVIDENCE_REGISTER_CAM_7JUNE_CRIMINAL_LEAD_ADDENDUM_23AUG2026.md#ME-CAM7J-009", "archive/MISSING_EVIDENCE_REGISTER_CAM_7JUNE_CRIMINAL_LEAD_ADDENDUM_23AUG2026.md#ME-CAM7J-010", "archive/MISSING_EVIDENCE_REGISTER_CAM_7JUNE_CRIMINAL_LEAD_ADDENDUM_23AUG2026.md#ME-CAM7J-012", "archive/MISSING_EVIDENCE_REGISTER_CAM_7JUNE_CRIMINAL_LEAD_ADDENDUM_23AUG2026.md#ME-CAM7J-013", "archive/MISSING_EVIDENCE_REGISTER_CAM_7JUNE_CRIMINAL_LEAD_ADDENDUM_23AUG2026.md#ME-CAM7J-014",
        ),
        "source_registers": fs(
            "archive/SUN_PARK_PRE_7JUN2018_ONSITE_APPROACHES_EVIDENCE_REGISTER_20AUG2026.md",
            "archive/SUN_PARK_7JUN2018_RUNUP_SOURCE_INGEST_17AUG2026.md",
            "archive/SUN_PARK_COMUNIDAD_PROCEEDINGS_REGISTER_CANARY_ISLANDS_15AUG2026.md",
            "archive/MISSING_EVIDENCE_REGISTER.md",
            "archive/MISSING_EVIDENCE_REGISTER_CAM_7JUNE_CRIMINAL_LEAD_ADDENDUM_23AUG2026.md",
        ),
    },
    "AM357-N04": {
        "source_refs": fs("C36-JUD-2021-05-12-001", "C36-JUD-2021-05-18-001"),
        "adverse_procedural_refs": fs("C36-JUD-2018-06-26-001", "C36-JUD-2019-10-24-001"),
        "missing_evidence_refs": fs("archive/MISSING_EVIDENCE_REGISTER.md#ME-008", "archive/MISSING_EVIDENCE_REGISTER.md#ME-011", "archive/MISSING_EVIDENCE_REGISTER.md#ME-012"),
        "external_sources": fs("https://www.boe.es/buscar/act.php?id=BOE-A-1995-25444#a250", "https://www.boe.es/buscar/act.php?id=BOE-A-1995-25444#a446", "https://www.boe.es/buscar/act.php?id=BOE-A-1995-25444#a447"),
        "source_registers": fs("archive/CONCURSO_36_2012_JUDICIAL_LAJ_ACTS_MASTER_REGISTER_17AUG2026.md", "archive/CONCURSO_36_2012_CANONICAL_COURT_BINARY_REGISTER_17AUG2026.md", "archive/MISSING_EVIDENCE_REGISTER.md"),
    },
    "AM357-N05": {
        "source_refs": fs("LV-01", "LV-02", "LV-03", "LV-04", "LV-05", "LV-08", "LV-09"),
        "attributed_statement_refs": fs("LV-06", "LV-07"),
        "control_refs": fs("CR-023"),
        "missing_evidence_refs": fs("archive/MISSING_EVIDENCE_REGISTER.md#ME-049"),
        "source_registers": fs("archive/LAVA_VERDE_CLUB_SEI_MEETING_POINT_PUBLICATION_BASIS_15AUG2026.md", "archive/CORRECTION_REGISTER.md", "archive/MISSING_EVIDENCE_REGISTER.md"),
    },
    "AM357-N06": {
        "control_refs": fs("CR-101"),
        "missing_evidence_refs": fs("archive/MISSING_EVIDENCE_REGISTER.md#ME-049"),
        "external_sources": fs(SEPI_RELEASE, SEPI_ACCOUNTS),
        "source_registers": fs("archive/FTI_MEETING_POINT_INSOLVENCY_PREINSOLVENCY_BLUESEA_PUBLICATION_BASIS_21AUG2026.md", "archive/CORRECTION_REGISTER.md", "archive/MISSING_EVIDENCE_REGISTER.md"),
    },
    "AM357-N07": {
        "source_refs": fs("GC-CONT-025", "LV-12"),
        "control_refs": fs("CR-100", "CR-108", "CR-109"),
        "missing_evidence_refs": fs("archive/MISSING_EVIDENCE_REGISTER.md#ME-049"),
        "external_sources": fs("https://www.boe.es/buscar/act.php?id=BOE-A-1995-25444#a446", "https://www.boe.es/buscar/act.php?id=BOE-A-1995-25444#a447", "https://www.boe.es/buscar/act.php?id=BOE-A-1985-12666#a219"),
        "source_registers": fs("archive/SUN_PARK_COMUNIDAD_PROCEEDINGS_REGISTER_CANARY_ISLANDS_15AUG2026.md", "archive/FTI_MEETING_POINT_INSOLVENCY_PREINSOLVENCY_BLUESEA_PUBLICATION_BASIS_21AUG2026.md", "archive/LAVA_VERDE_CLUB_SEI_MEETING_POINT_PUBLICATION_BASIS_15AUG2026.md", "archive/CORRECTION_REGISTER.md", "archive/MISSING_EVIDENCE_REGISTER.md"),
    },
    "AM357-N08": {
        "source_refs": fs("ONA-FX-001", "ONA-FX-002", "ONA-FX-003", "ONA-FX-005", "ONA-FX-006", "ONA-FX-007", "ONA-FX-008", "ONA-FX-009"),
        "attributed_statement_refs": fs("ONA-FX-004"),
        "control_refs": fs("PD-ONA-FX-20260826-01"),
        "missing_evidence_refs": fs("archive/MISSING_EVIDENCE_REGISTER.md#ME-084", "archive/MISSING_EVIDENCE_REGISTER_CAM_7JUNE_CRIMINAL_LEAD_ADDENDUM_23AUG2026.md#ME-CAM7J-007"),
        "source_registers": fs("archive/evidence/ONA_FUNDED_EXIT_UNITARY_FACT_RECORD_20260826.md", "archive/ONA_COMMERCIAL_EXIT_OPERATIONAL_NORMALISATION_PACKAGE_2018_16AUG2026.md", "archive/MISSING_EVIDENCE_REGISTER.md", "archive/MISSING_EVIDENCE_REGISTER_CAM_7JUNE_CRIMINAL_LEAD_ADDENDUM_23AUG2026.md"),
    },
    "AM357-N09": {
        "source_refs": fs("C36-JUD-2021-05-12-001", "C36-JUD-2021-05-18-001", "SP-PRV-LCTR-GM-DB9D2197E93B05C8AF7B", "LV-12"),
        "control_refs": fs("CR-101"),
        "missing_evidence_refs": fs("archive/MISSING_EVIDENCE_REGISTER.md#ME-008", "archive/MISSING_EVIDENCE_REGISTER.md#ME-011", "archive/MISSING_EVIDENCE_REGISTER.md#ME-012", "archive/MISSING_EVIDENCE_REGISTER.md#ME-049", "archive/MISSING_EVIDENCE_REGISTER.md#ME-058"),
        "external_sources": fs(SEPI_RELEASE, SEPI_ACCOUNTS),
        "source_registers": fs("archive/CONCURSO_36_2012_JUDICIAL_LAJ_ACTS_MASTER_REGISTER_17AUG2026.md", "archive/CAM_2022_ADJUDICATION_TRANSACTION_IDENTITY_AND_CONSIDERATION_CONTROL_19AUG2026.md", "archive/LAVA_VERDE_CLUB_SEI_MEETING_POINT_PUBLICATION_BASIS_15AUG2026.md", "archive/FTI_MEETING_POINT_INSOLVENCY_PREINSOLVENCY_BLUESEA_PUBLICATION_BASIS_21AUG2026.md", "archive/CORRECTION_REGISTER.md", "archive/MISSING_EVIDENCE_REGISTER.md"),
    },
}

EXPECTED_LATERAL = {
    "es": {
        "J-LATERAL": ("/es/concurso-36-2012-magistrado-juez/", fs("/es/concurso-36-2012-masa-activa-2018-2021/#contradiccion")),
        "M-LATERAL": ("/es/concurso-36-2012-masa-activa-2018-2021/", fs("/es/concurso-36-2012-magistrado-juez/#ledger", "/es/lava-verde-club-sei-meeting-point/#cadena")),
        "C-LATERAL": ("/es/lava-verde-club-sei-meeting-point/", fs("/es/concurso-36-2012-masa-activa-2018-2021/#contradiccion", "/es/fti-touristik-meeting-point-insolvencia-preconcurso-bluesea/#sepi")),
        "T-LATERAL": ("/es/cuaderno-juridico/meeting-point-357-2024-trazabilidad-judicial/", fs("/es/fti-touristik-meeting-point-insolvencia-preconcurso-bluesea/#sepi")),
        "U-LATERAL": ("/es/reconstruccion-unitaria-autoridades-publicas/", fs("/es/ingenieria-inversa-criminal-unitaria/")),
        "R-LATERAL": ("/es/ingenieria-inversa-criminal-unitaria/", fs("/es/reconstruccion-unitaria-autoridades-publicas/#sala-limpia", "/es/hipotesis-criminal-unitaria-2011-presente/", "/es/verificacion-caepr-caret-digest-unitario/")),
        "H-LATERAL": ("/es/hipotesis-criminal-unitaria-2011-presente/", fs("/es/ingenieria-inversa-criminal-unitaria/")),
        "I-LATERAL": ("/es/registro-identidad-materia/", fs("/es/verificacion-caepr-caret-digest-unitario/")),
    },
    "en": {
        "J-LATERAL": ("/en/insolvency-36-2012-mercantile-court-1/", fs("/en/insolvency-36-2012-active-estate-2018-2021/#contradiction")),
        "M-LATERAL": ("/en/insolvency-36-2012-active-estate-2018-2021/", fs("/en/insolvency-36-2012-mercantile-court-1/#ledger", "/en/lava-verde-club-sei-meeting-point/#chain")),
        "C-LATERAL": ("/en/lava-verde-club-sei-meeting-point/", fs("/en/insolvency-36-2012-active-estate-2018-2021/#contradiction", "/en/fti-touristik-meeting-point-insolvency-preinsolvency-bluesea/#sepi")),
        "T-LATERAL": ("/en/legal-notebook/meeting-point-357-2024-judicial-traceability/", fs("/en/fti-touristik-meeting-point-insolvency-preinsolvency-bluesea/#sepi")),
        "U-LATERAL": ("/en/public-authority-unitary-case-reconstruction/", fs("/en/unitary-criminal-reverse-engineering/")),
        "R-LATERAL": ("/en/unitary-criminal-reverse-engineering/", fs("/en/public-authority-unitary-case-reconstruction/#clean-room", "/en/unitary-criminal-hypothesis-2011-present/", "/en/caepr-caret-unitary-digest/")),
        "H-LATERAL": ("/en/unitary-criminal-hypothesis-2011-present/", fs("/en/unitary-criminal-reverse-engineering/")),
        "I-LATERAL": ("/en/matter-identity-registry/", fs("/en/caepr-caret-unitary-digest/")),
    },
}

ALLOWED_LIFECYCLE = (
    "DRAFT",
    "PREPARED_PENDING_MERGE",
    "REMOTE_SOURCE",
    "PR_OPEN",
    "CI_GREEN",
    "MERGED",
    "DEPLOYED",
    "LIVE_VERIFIED",
    "DELETION_SAFE",
)
BLOCKED_LIFECYCLE = "BLOCKED_RECOVERY"

EXPECTED_STATUS_BY_STATE = {
    "DRAFT": "not_live",
    "PREPARED_PENDING_MERGE": "release_candidate_not_yet_verified_live",
    "REMOTE_SOURCE": "remote_source_not_merged",
    "PR_OPEN": "pull_request_open_not_merged",
    "CI_GREEN": "pull_request_checks_green_not_merged",
    "MERGED": "merged_awaiting_pages_deployment",
    "DEPLOYED": "deployed_awaiting_exact_live_closeout",
    "LIVE_VERIFIED": "live_verified",
    "DELETION_SAFE": "deletion_safe_live_verified",
    BLOCKED_LIFECYCLE: "blocked_recovery",
}


def is_full_sha(value: object) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value) is not None


class Element:
    """Small stdlib DOM node sufficient for containment and rendered text."""

    def __init__(self, tag: str, attrs: dict[str, str], parent: Element | None = None) -> None:
        self.tag = tag
        self.attrs = attrs
        self.parent = parent
        self.children: list[Element | str] = []

    def walk(self, include_self: bool = True):
        if include_self:
            yield self
        for child in self.children:
            if isinstance(child, Element):
                yield from child.walk()

    def text_content(self) -> str:
        return " ".join(child.text_content() if isinstance(child, Element) else child for child in self.children)


class DOMParser(HTMLParser):
    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Element("__root__", {})
        self.stack = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = Element(tag, {key: value or "" for key, value in attrs}, self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = Element(tag, {key: value or "" for key, value in attrs}, self.stack[-1])
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                return

    def handle_data(self, data: str) -> None:
        self.stack[-1].children.append(data)


errors: list[str] = []
parse_cache: dict[Path, tuple[str, Element]] = {}


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def normalize_text(value: str) -> str:
    return " ".join(value.split())


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"cannot load {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{path.relative_to(ROOT)} root is not an object")
        return {}
    return value


def parse(path: Path) -> tuple[str, Element]:
    resolved = path.resolve()
    if resolved in parse_cache:
        return parse_cache[resolved]
    try:
        text = resolved.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"cannot read {path.relative_to(ROOT)}: {exc}")
        return "", Element("__root__", {})
    parser = DOMParser()
    parser.feed(text)
    parser.close()
    parse_cache[resolved] = (text, parser.root)
    return text, parser.root


def elements(root: Element, *, tag: str | None = None, attribute: str | None = None) -> list[Element]:
    return [node for node in root.walk() if (tag is None or node.tag == tag) and (attribute is None or attribute in node.attrs)]


def descendant_elements(root: Element, *, tag: str | None = None, attribute: str | None = None) -> list[Element]:
    return [node for node in root.walk(include_self=False) if (tag is None or node.tag == tag) and (attribute is None or attribute in node.attrs)]


def safe_repo_path(reference: str, label: str) -> tuple[Path | None, str]:
    parts = urlsplit(reference)
    if parts.scheme or parts.netloc or parts.query:
        errors.append(f"{label} is not a safe repository path: {reference}")
        return None, parts.fragment
    decoded = unquote(parts.path)
    if not decoded or "\x00" in decoded:
        errors.append(f"{label} has an empty or invalid path: {reference}")
        return None, parts.fragment
    try:
        candidate = (ROOT / decoded.lstrip("/")).resolve()
        candidate.relative_to(ROOT_RESOLVED)
    except ValueError:
        errors.append(f"{label} escapes the repository: {reference}")
        return None, parts.fragment
    return candidate, unquote(parts.fragment)


def resolved_local_route(reference: str, label: str, base_route: str | None = None) -> tuple[str, Path | None, str]:
    resolved_route = urljoin(base_route or "", reference)
    parts = urlsplit(resolved_route)
    if parts.scheme or parts.netloc or parts.query or not parts.path.startswith("/"):
        errors.append(f"{label} is not a safe root-relative route: {resolved_route}")
        return resolved_route, None, unquote(parts.fragment)
    suffix = ("#" + parts.fragment) if parts.fragment else ""
    path, fragment = safe_repo_path(parts.path + suffix, label)
    if path is not None and parts.path.endswith("/"):
        path /= "index.html"
    return resolved_route, path, fragment


def check_local_target(route: str, label: str, base_route: str | None = None) -> tuple[str, Path | None, str]:
    resolved, target, fragment = resolved_local_route(route, label, base_route)
    if target is None:
        return resolved, None, fragment
    check(target.is_file(), f"{label} target missing: {resolved}")
    if target.is_file() and fragment:
        _, target_dom = parse(target)
        ids = [node.attrs["id"] for node in elements(target_dom, attribute="id")]
        check(fragment in ids, f"{label} target fragment missing: {resolved}")
    return resolved, target, fragment


def route_for_html(path: Path) -> str:
    relative = path.relative_to(ROOT).as_posix()
    check(relative.endswith("index.html"), f"cannot derive public route from {relative}")
    return "/" + relative.removesuffix("index.html")


def route_file(route: str, label: str) -> str | None:
    _, target, _ = resolved_local_route(route, label)
    if target is None:
        return None
    try:
        return target.relative_to(ROOT).as_posix()
    except ValueError:
        errors.append(f"{label} target escapes repository: {route}")
        return None


required_files = (
    ES, EN, MATRIX_PATH, CARET_PATH, FIRST_HOP_CARET_PATH, UNITARY_CARET_PATH, REGISTRY_PATH,
    AUDIT_PATH, HUMAN_MATRIX_PATH, TITLE_CONTROL_PATH, PLAN_PATH, MANIFEST_PATH,
    CURRENT_DIGEST_MD_PATH, CURRENT_DIGEST_JSON_PATH,
)
for required in required_files:
    check(required.is_file(), f"missing {required.relative_to(ROOT)}")

matrix = load_json(MATRIX_PATH)
caret = load_json(CARET_PATH)
first_hop_caret = load_json(FIRST_HOP_CARET_PATH)
unitary_caret = load_json(UNITARY_CARET_PATH)
registry = load_json(REGISTRY_PATH)
manifest = load_json(MANIFEST_PATH)
current_digest = load_json(CURRENT_DIGEST_JSON_PATH)
es_text, es_dom = parse(ES)
en_text, en_dom = parse(EN)

# Machine matrix and explicit scope separation.
check(matrix.get("schema") == "por-derecho.alberto-meeting-point-multidirectional-evidence.v1", "matrix schema drift")
check(matrix.get("control_id") == CONTROL_ID, "matrix control ID drift")
check(matrix.get("analysis_order") == ["CRIMINAL_FIRST", "INSOLVENCY", "CIVIL_RECOVERY", "INSTITUTIONAL_PUBLIC_FUNDS"], "matrix analysis order is not the controlled criminal-first order")
check(matrix.get("hub_routes") == {"es": "/es/alberto-lopez-villarrubia-meeting-point-357-masa-activa/", "en": "/en/alberto-lopez-villarrubia-meeting-point-357-active-estate/"}, "matrix hub routes drift")

unitary_scope = (matrix.get("scope_separation") or {}).get("unitary_caret_scope") or {}
specialist_scope = (matrix.get("scope_separation") or {}).get("specialist_caret_scope") or {}
first_hop_scope = (matrix.get("scope_separation") or {}).get("first_hop_caret_scope") or {}
check(unitary_scope.get("control_id") == UNITARY_SCOPE_CONTROL_ID, "matrix unitary-scope reference drift")
check((unitary_scope.get("confirmed"), unitary_scope.get("denominator"), unitary_scope.get("pending")) == (21, 24, 3), "matrix unitary caret scope is not 21/24/3")
check(unitary_scope.get("changed_by_this_module") is True, "matrix does not record the propagated unitary-scope update")
check(specialist_scope.get("control_id") == CARET_CONTROL_ID, "matrix specialist caret control ID drift")
check((specialist_scope.get("confirmed"), specialist_scope.get("denominator"), specialist_scope.get("pending"), specialist_scope.get("confirmed_occurrence_rows")) == (31, 31, 0, 32), "matrix specialist caret scope is not 31/31 unique and 32/32 occurrence rows")
check(specialist_scope.get("verdict") == "ALL_IS_VERIFIED_FOR_STATED_SCOPE", "matrix specialist caret verdict drift")
check(first_hop_scope == {
    "control_id": FIRST_HOP_CARET_CONTROL_ID,
    "confirmed": 61,
    "pending": 69,
    "denominator": 130,
    "verdict": "FULL_FIRST_HOP_CENSUS_PARTIAL_NOT_ALL_IS",
    "changed_by_this_module": True,
}, "matrix first-hop caret scope is not the controlled 61/130/69 result")

# Nine bilingual typed nodes and their exact evidence lanes.
nodes = matrix.get("nodes") or []
check(isinstance(nodes, list), "matrix nodes is not a list")
node_map = {node.get("node_id"): node for node in nodes if isinstance(node, dict)}
check(len(nodes) == 9 and len(node_map) == 9 and set(node_map) == NODE_ID_SET, "matrix node census is not exactly AM357-N01..N09")
for node_id in NODE_IDS:
    node = node_map.get(node_id, {})
    for field in ("source_supported_fact", "supported_investigative_inference", "criminal_first_element_gate", "strongest_counterevidence", "falsification_production_target"):
        value = node.get(field)
        check(isinstance(value, dict) and set(value) == {"es", "en"} and all(isinstance(item, str) and normalize_text(item) for item in value.values()), f"{node_id}.{field} lacks exact non-empty ES/EN content")
    routes = node.get("primary_routes") or {}
    check(set(routes) == {"es", "en"}, f"{node_id} lacks paired primary routes")
    for language, route in routes.items():
        check_local_target(route, f"{node_id} {language} primary route")

    evidence = node.get("evidence")
    check(isinstance(evidence, dict), f"{node_id}.evidence is not an object")
    if not isinstance(evidence, dict):
        continue
    check(set(evidence) == EVIDENCE_KEYS, f"{node_id}.evidence keys drift: {sorted(set(evidence) ^ EVIDENCE_KEYS)}")
    expected = EXPECTED_EVIDENCE[node_id]
    for category in EVIDENCE_KEYS:
        actual_values = evidence.get(category, [])
        check(isinstance(actual_values, list) and all(isinstance(item, str) and item for item in actual_values), f"{node_id}.{category} is not a non-null string list")
        if not isinstance(actual_values, list):
            actual_values = []
        check(len(actual_values) == len(set(actual_values)), f"{node_id}.{category} contains duplicates")
        check(set(actual_values) == set(expected.get(category, fs())), f"{node_id}.{category} semantic allowlist drift: actual={sorted(set(actual_values))}, expected={sorted(expected.get(category, fs()))}")
    check(bool(evidence.get("source_refs") or evidence.get("external_sources")), f"{node_id} has neither a source reference nor an external source")

    register_texts: list[str] = []
    for reference in evidence.get("source_registers", []):
        path, fragment = safe_repo_path(reference, f"{node_id} source register")
        check(not fragment, f"{node_id} source register must name a file, not a fragment: {reference}")
        if path is not None:
            check(path.is_file(), f"{node_id} source register missing: {reference}")
            if path.is_file():
                register_texts.append(path.read_text(encoding="utf-8"))
    register_corpus = "\n".join(register_texts)
    for category in ("source_refs", "attributed_statement_refs", "adverse_procedural_refs", "control_refs"):
        for reference in evidence.get(category, []):
            check(not reference.startswith("ME-"), f"{node_id}.{category} misclassifies missing-evidence reference {reference}")
            check(reference in register_corpus, f"{node_id}.{category} reference is absent from its declared source registers: {reference}")
    for reference in evidence.get("missing_evidence_refs", []):
        path, fragment = safe_repo_path(reference, f"{node_id} missing-evidence reference")
        check(bool(fragment) and fragment.startswith("ME-"), f"{node_id} missing-evidence reference lacks an ME fragment: {reference}")
        if path is not None:
            check(path.is_file(), f"{node_id} missing-evidence register missing: {reference}")
            if path.is_file() and fragment:
                check(fragment in path.read_text(encoding="utf-8"), f"{node_id} missing-evidence token absent from declared register: {reference}")
    for reference in evidence.get("integrity_refs", []):
        check(re.fullmatch(r"SHA256:[0-9a-f]{64}", reference) is not None, f"{node_id} malformed integrity reference: {reference}")
    for reference in evidence.get("external_sources", []):
        parts = urlsplit(reference)
        try:
            port = parts.port
        except ValueError:
            port = -1
        check(parts.scheme == "https" and parts.hostname in {"www.sepi.es", "www.boe.es"} and parts.username is None and parts.password is None and port is None, f"{node_id} external source is outside the controlled HTTPS BOE/SEPI allowlist: {reference}")

n07_public_custody_boundary = (
    "For AM357-N07, public Git preserves aggregate source controls but not the "
    "signed Auto 97/2025 binary or a reproducible per-copy full-hash custody "
    "manifest for the three notices; do not claim public-binary integrity closure."
)
check(n07_public_custody_boundary in (matrix.get("boundaries") or []), "AM357-N07 lacks the explicit public-custody-partial boundary")

# The thirteen bridge tests define direct adjacency. Transitive or inferred
# relationships must not be smuggled into upstream/downstream arrays.
edges = matrix.get("edges") or []
edge_map = {edge.get("edge_id"): (edge.get("from"), edge.get("to")) for edge in edges if isinstance(edge, dict)}
check(len(edges) == 13 and len(edge_map) == 13, "matrix must contain 13 unique bridge tests")
check(edge_map == EXPECTED_EDGE_ENDPOINTS, f"matrix edge endpoint map drift: {edge_map}")
direct_upstream: dict[str, set[str]] = defaultdict(set)
direct_downstream: dict[str, set[str]] = defaultdict(set)
edge_contrary_values: list[str] = []
edge_production_values: list[str] = []
for edge in edges:
    if not isinstance(edge, dict):
        continue
    edge_id, source, target = edge.get("edge_id"), edge.get("from"), edge.get("to")
    check(set(edge) == EDGE_CONTRACT_FIELDS, f"{edge_id} edge-contract key drift: {sorted(set(edge) ^ EDGE_CONTRACT_FIELDS)}")
    check(source in NODE_ID_SET and target in NODE_ID_SET and source != target, f"{edge_id} has an invalid endpoint")
    for field in (
        "evidence_lane",
        "support_level",
        "forward_inference",
        "reverse_falsification",
        "strongest_contrary_evidence",
        "confirm_or_falsify_production",
    ):
        check(isinstance(edge.get(field), str) and normalize_text(edge.get(field, "")), f"{edge_id}.{field} missing")
    check(re.fullmatch(r"[A-Z][A-Z_]+_UNPROVED", edge.get("support_level", "")) is not None, f"{edge_id}.support_level is not a controlled UNPROVED level")
    source_refs = edge.get("source_refs")
    check(isinstance(source_refs, list) and len(source_refs) >= 2 and len(source_refs) == len(set(source_refs)) and all(isinstance(item, str) and item for item in source_refs), f"{edge_id}.source_refs is not a unique non-empty edge source set")
    endpoint_refs: set[str] = set()
    for endpoint in (source, target):
        endpoint_evidence = (node_map.get(endpoint, {}).get("evidence") or {})
        for category in EVIDENCE_KEYS - {"source_registers"}:
            endpoint_refs.update(endpoint_evidence.get(category, []))
    if isinstance(source_refs, list):
        check(set(source_refs).issubset(endpoint_refs), f"{edge_id}.source_refs contains a reference outside its two endpoint evidence controls: {sorted(set(source_refs) - endpoint_refs)}")
    edge_contrary_values.append(normalize_text(edge.get("strongest_contrary_evidence", "")))
    edge_production_values.append(normalize_text(edge.get("confirm_or_falsify_production", "")))
    if source in NODE_ID_SET and target in NODE_ID_SET:
        direct_downstream[source].add(target)
        direct_upstream[target].add(source)
check(len(set(edge_contrary_values)) == 13, "edge-specific strongest contrary evidence is duplicated")
check(len(set(edge_production_values)) == 13, "edge-specific confirm-or-falsify production is duplicated")
for node_id in NODE_IDS:
    upstream = node_map.get(node_id, {}).get("upstream", [])
    downstream = node_map.get(node_id, {}).get("downstream", [])
    check(isinstance(upstream, list) and len(upstream) == len(set(upstream)), f"{node_id}.upstream is not a duplicate-free list")
    check(isinstance(downstream, list) and len(downstream) == len(set(downstream)), f"{node_id}.downstream is not a duplicate-free list")
    check(set(upstream) == direct_upstream[node_id], f"{node_id}.upstream is not direct edge adjacency: actual={sorted(set(upstream))}, expected={sorted(direct_upstream[node_id])}")
    check(set(downstream) == direct_downstream[node_id], f"{node_id}.downstream is not direct edge adjacency: actual={sorted(set(downstream))}, expected={sorted(direct_downstream[node_id])}")

# Finite specialist caret census and registry admission.
check(caret.get("control_id") == CARET_CONTROL_ID, "specialist caret machine-control ID drift")
check(caret.get("status") == "ALL_IS_VERIFIED_FOR_STATED_SCOPE", "specialist caret status is not all-is for stated scope")
check(caret.get("verdict") == "ALL IS^ — VERIFIED FOR THE STATED SIX-SURFACE SCOPE; 31/31 UNIQUE IDENTITIES AND 32/32 OCCURRENCE ROWS CARET_CONFIRMED; 0 PENDING", "specialist caret verdict drift")
counts = caret.get("counts") or {}
check((counts.get("eligible"), counts.get("occurrence_rows"), counts.get("confirmed"), counts.get("confirmed_occurrence_rows"), counts.get("pending"), counts.get("suspended"), counts.get("coverage_percent")) == (31, 32, 31, 32, 0, 0, 100), "specialist caret counts are not 31/31 unique and 32/32 occurrence rows")
check(counts.get("by_type") == EXPECTED_CARET_TYPE_COUNTS, "specialist caret typed census drift")
records = caret.get("records") or []
check(isinstance(records, list) and len(records) == 32, "specialist caret does not enumerate exactly 32 records")
check([record.get("ordinal") for record in records if isinstance(record, dict)] == list(range(1, 33)), "specialist caret ordinals are not exactly 1..32")
object_keys = [record.get("object_key") for record in records if isinstance(record, dict)]
check(len(object_keys) == len(set(object_keys)) == 32, "specialist caret object keys are not 32 unique values")
confirmed_records = [record for record in records if isinstance(record, dict) and record.get("state") == "CARET_CONFIRMED"]
pending_records = [record for record in records if isinstance(record, dict) and record.get("state") == "CARET_PENDING"]
check(len(confirmed_records) == 32 and len(pending_records) == 0, "specialist caret state split is not 32 confirmed occurrence rows / 0 pending")
check(not [record for record in records if isinstance(record, dict) and record.get("state") not in {"CARET_CONFIRMED", "CARET_PENDING"}], "specialist caret contains a state outside confirmed/pending")
check(
    all(isinstance(record.get("next_source_needed"), str) and record["next_source_needed"].strip() for record in pending_records),
    "every pending specialist caret object must state the next identity source needed",
)
confirmed_types = {record.get("caepr_id"): record.get("type") for record in confirmed_records}
check(confirmed_types == EXPECTED_CONFIRMED, "specialist confirmed caret IDs/types drift")
pending_map = {record.get("object_key"): (record.get("type"), record.get("candidate_caepr_id")) for record in pending_records}
check(pending_map == EXPECTED_PENDING, "specialist pending caret object/type/candidate map drift")
for record in records:
    if not isinstance(record, dict):
        continue
    labels = record.get("public_labels") or {}
    check(set(labels) == {"es", "en"} and all(isinstance(value, str) and normalize_text(value) for value in labels.values()), f"caret {record.get('object_key')} lacks exact ES/EN labels")
    if record.get("state") == "CARET_CONFIRMED":
        check("candidate_caepr_id" not in record, f"confirmed caret {record.get('object_key')} improperly retains candidate_caepr_id")
        check(all("^" in normalize_text(value) for value in labels.values()), f"confirmed caret {record.get('object_key')} public label lacks caret")
    else:
        check("caepr_id" not in record, f"pending caret {record.get('object_key')} improperly has caepr_id")
        check(all("pending" in value.lower() or "pendiente" in value.lower() for value in labels.values()), f"pending caret {record.get('object_key')} lacks visible pending label")
        check(not any(normalize_text(value).endswith("^") for value in labels.values()), f"pending caret {record.get('object_key')} is rendered as confirmed")

caret_unitary_ref = caret.get("unitary_scope_reference") or {}
check(caret_unitary_ref == {"control_id": UNITARY_SCOPE_CONTROL_ID, "confirmed": 21, "pending": 3, "denominator": 24, "changed_by_this_module": True}, "specialist caret unitary-scope reference drift")
check(
    registry.get("counts") == CURRENT_CANONICAL_REGISTRY_COUNTS,
    "canonical source registry counts do not equal 341/162/83/11/42/43",
)

registry_records: dict[str, dict] = {}
registry_seen: list[str] = []
for part in registry.get("parts", []):
    if not isinstance(part, dict) or not isinstance(part.get("path"), str):
        errors.append("registry contains malformed part descriptor")
        continue
    part_path, fragment = safe_repo_path("assets/data/" + part["path"], f"registry part {part.get('path')}")
    check(not fragment, f"registry part has fragment: {part.get('path')}")
    if part_path is None or not part_path.is_file():
        check(False, f"registry part missing: {part.get('path')}")
        continue
    payload = load_json(part_path)
    part_records = payload.get("records", [])
    check(len(part_records) == part.get("count"), f"registry part-count drift: {part['path']}")
    for record in part_records:
        if isinstance(record, dict) and isinstance(record.get("id"), str):
            registry_seen.append(record["id"])
            registry_records[record["id"]] = record
check(len(registry_seen) == len(set(registry_seen)), "canonical registry contains duplicate immutable IDs")

# Full first-hop caret census for the eighteen reciprocal evidence routes. It
# is a separate, larger denominator and must never be substituted for either
# the six-surface all-is control or its dated repository-wide 21/24 reference.
check(first_hop_caret.get("schema") == "por-derecho.caepr-caret-first-hop-finite-scope.v1", "first-hop caret schema drift")
check(first_hop_caret.get("control_id") == FIRST_HOP_CARET_CONTROL_ID, "first-hop caret control ID drift")
check(first_hop_caret.get("status") == "PARTIAL_NOT_ALL_IS", "first-hop caret status drift")
check(first_hop_caret.get("verdict") == "FULL FIRST-HOP CENSUS COMPLETE; 61/130 CARET_CONFIRMED; 69 CARET_PENDING; 0 CARET_SUSPENDED; PARTIAL — NOT ALL IS^", "first-hop caret verdict drift")
first_hop_counts = first_hop_caret.get("counts") or {}
check((first_hop_counts.get("eligible"), first_hop_counts.get("confirmed"), first_hop_counts.get("pending"), first_hop_counts.get("suspended")) == (130, 61, 69, 0), "first-hop caret count is not 130/61/69/0")
check(first_hop_counts.get("by_type") == {
    "PERSON": {"eligible": 27, "confirmed": 12, "pending": 15, "suspended": 0},
    "ORGANISATION_OR_PERIMETER": {"eligible": 64, "confirmed": 30, "pending": 34, "suspended": 0},
    "INSTITUTION_OR_SUBORGAN": {"eligible": 25, "confirmed": 13, "pending": 12, "suspended": 0},
    "PROCEEDING": {"eligible": 14, "confirmed": 6, "pending": 8, "suspended": 0},
}, "first-hop caret typed count drift")
first_hop_records = first_hop_caret.get("records") or []
check(isinstance(first_hop_records, list) and len(first_hop_records) == 130, "first-hop caret does not enumerate 130 records")
check([record.get("ordinal") for record in first_hop_records if isinstance(record, dict)] == list(range(1, 131)), "first-hop caret ordinals are not exactly 1..130")
first_hop_keys = [record.get("object_key") for record in first_hop_records if isinstance(record, dict)]
check(len(first_hop_keys) == len(set(first_hop_keys)) == 130, "first-hop caret object keys are not unique")
first_hop_confirmed = [record for record in first_hop_records if isinstance(record, dict) and record.get("state") == "CARET_CONFIRMED"]
first_hop_pending = [record for record in first_hop_records if isinstance(record, dict) and record.get("state") == "CARET_PENDING"]
check(len(first_hop_confirmed) == 61 and len(first_hop_pending) == 69, "first-hop caret split is not 61 confirmed / 69 pending")
check(not [record for record in first_hop_records if isinstance(record, dict) and record.get("state") not in {"CARET_CONFIRMED", "CARET_PENDING"}], "first-hop caret contains an uncontrolled state")
check(all(isinstance(record.get("boundary"), str) and record["boundary"].strip() for record in first_hop_records), "every first-hop object must state its identity boundary")
check(all(isinstance(record.get("next_source_needed"), str) and record["next_source_needed"].strip() for record in first_hop_pending), "every pending first-hop object must state its exact next source")
check(all(record.get("caepr_id") in registry_records for record in first_hop_confirmed), "a confirmed first-hop object lacks an immutable current CAEPR record")
check(all("caepr_id" not in record for record in first_hop_pending), "a pending first-hop object improperly carries an admitted CAEPR ID")
route_scope = first_hop_caret.get("route_scope") or []
check(len(route_scope) == 9 and {item.get("node_id") for item in route_scope if isinstance(item, dict)} == NODE_ID_SET, "first-hop route scope is not nine unique node pairs")
for item in route_scope:
    if not isinstance(item, dict):
        continue
    node_id = item.get("node_id")
    for language in ("es", "en"):
        route = item.get(language, "")
        check(route == (node_map.get(node_id, {}).get("primary_routes") or {}).get(language, "").split("#", 1)[0], f"first-hop {node_id} {language} route differs from the graph primary route")
        check_local_target(route, f"first-hop {node_id} {language} route")
check((first_hop_caret.get("core_32_overlap") or {}).get("visible_in_first_hop") == 31, "first-hop/core overlap is not 31")
first_hop_unitary = first_hop_caret.get("unitary_scope_reference") or {}
check((first_hop_unitary.get("confirmed"), first_hop_unitary.get("pending"), first_hop_unitary.get("denominator"), first_hop_unitary.get("changed_by_this_control")) == (21, 3, 24, True), "first-hop control misstates the unitary 21/24 scope")

for caepr_id, expected_type in EXPECTED_CONFIRMED.items():
    check(caepr_id in registry_records, f"confirmed specialist caret ID absent from registry: {caepr_id}")
    if caepr_id in registry_records:
        check(registry_records[caepr_id].get("type") == expected_type, f"confirmed specialist caret type mismatch: {caepr_id}")

if "PD-SP-O-0070" in registry_records:
    check(registry_records["PD-SP-O-0070"].get("name") == "AUREN REESTRUCTURACIONES SLP", "exact Auren record drift")
if "PD-SP-O-0046" in registry_records:
    check(registry_records["PD-SP-O-0046"].get("name") == "Auren professional perimeter", "generic Auren perimeter drift")
for caepr_id in ("PD-SP-O-0067", "PD-SP-O-0068", "PD-SP-O-0069"):
    if caepr_id in registry_records:
        aliases = registry_records[caepr_id].get("aliases", [])
        check(not any("S.L." in alias and "S.L.U." not in alias for alias in aliases), f"{caepr_id} silently aliases an unreconciled S.L. literal")
if "PD-SP-O-0071" in registry_records:
    check(registry_records["PD-SP-O-0071"].get("legal_personality") is False, "FASEE legal-personality boundary missing")
    check(registry_records["PD-SP-O-0071"].get("managed_by") == "PD-SP-I-0017", "FASEE/SEPI management link missing")
if "PD-SP-O-0038" in registry_records:
    check("commercial" in registry_records["PD-SP-O-0038"].get("identity_boundary", "").lower(), "Meeting Point commercial-perimeter boundary missing")
if "PD-SP-I-0018" in registry_records:
    check("not authentication" in registry_records["PD-SP-I-0018"].get("identity_boundary", "").lower(), "Public Insolvency Register authenticity boundary missing")

# Canonical current 21/24 unitary caret remains a separate, unresolved control.
unitary_result = unitary_caret.get("result") or {}
check(unitary_caret.get("control_id") == CANONICAL_UNITARY_CARET_CONTROL_ID, "canonical unitary caret control ID drift")
check((unitary_result.get("confirmed"), unitary_result.get("denominator"), unitary_result.get("pending"), unitary_result.get("suspended")) == (21, 24, 3, 0), "canonical unitary caret is not 21/24/3/0")
check(unitary_result.get("verdict") == "PARTIAL_NOT_ALL_IS_CARET", "canonical unitary caret verdict drift")
unitary_confirmed_ids = {item.get("id") for item in unitary_caret.get("confirmed_objects", []) if isinstance(item, dict)}
unitary_pending_by_id = {item.get("existing_id"): item for item in unitary_caret.get("exceptions", []) if isinstance(item, dict)}
check(len(unitary_caret.get("confirmed_objects", [])) == 21 and len(unitary_caret.get("exceptions", [])) == 3, "canonical unitary caret enumeration is not 21 confirmed records plus 3 exceptions")
check("PD-SP-O-0075" in unitary_confirmed_ids, "Clubotel exact record is absent from canonical confirmed objects")
check("PD-SP-O-0033" not in unitary_confirmed_ids, "Ona Hotels / ONA perimeter was improperly collapsed into a confirmed object")
check((unitary_pending_by_id.get("PD-SP-O-0033") or {}).get("state") == "CARET_PENDING", "Ona Hotels / ONA perimeter is not preserved as CARET_PENDING")

# Hub DOM: exact rows, contained six fields, per-row render hashes, exact
# confirmed/pending caret render, safe outbound links and language parity.
render_hash = matrix.get("public_render_sha256") or {}
check(render_hash.get("algorithm") == "sha256(normalized six-field row joined by newline in declared field order)", "public render hash algorithm drift")
check(render_hash.get("field_order") == list(MATRIX_FIELDS), "public render hash field order drift")
record_by_id = {record.get("caepr_id"): record for record in confirmed_records}
record_by_key = {record.get("object_key"): record for record in confirmed_records}
hub_node_sets: dict[str, set[str]] = {}
hub_caret_sets: dict[str, set[str]] = {}
hub_pending_sets: dict[str, set[str]] = {}
for label, text, dom, language in (("Spanish", es_text, es_dom, "es"), ("English", en_text, en_dom, "en")):
    all_ids = [node.attrs["id"] for node in elements(dom, attribute="id")]
    duplicate_ids = sorted(key for key, count in Counter(all_ids).items() if count > 1)
    check(not duplicate_ids, f"{label} hub has duplicate HTML IDs: {duplicate_ids}")
    check(CONTROL_ID in text, f"{label} hub lacks matrix control ID")
    check(CARET_CONTROL_ID in text, f"{label} hub lacks specialist caret control ID")
    check(FIRST_HOP_CARET_CONTROL_ID in text, f"{label} hub lacks first-hop caret control ID")

    rows = elements(dom, attribute="data-node-id")
    row_ids = [row.attrs.get("data-node-id") for row in rows]
    hub_node_sets[language] = set(row_ids)
    check(len(rows) == 9 and len(set(row_ids)) == 9 and set(row_ids) == NODE_ID_SET, f"{label} hub row set is not exactly nine unique nodes")
    stored_hashes = render_hash.get(language) or {}
    check(set(stored_hashes) == NODE_ID_SET, f"{label} public render hash map is not exactly nine nodes")
    for row in rows:
        node_id = row.attrs.get("data-node-id", "")
        check(row.tag == "tr", f"{label} {node_id} node marker is not on its table row")
        check(row.attrs.get("id") == f"am357-{node_id[-3:].lower()}", f"{label} {node_id} HTML fragment drift")
        field_elements = descendant_elements(row, attribute="data-matrix-field")
        field_map: dict[str, list[Element]] = defaultdict(list)
        for field_element in field_elements:
            field_map[field_element.attrs.get("data-matrix-field", "")].append(field_element)
        check(set(field_map) == set(MATRIX_FIELDS), f"{label} {node_id} six-field key set drift: {sorted(set(field_map) ^ set(MATRIX_FIELDS))}")
        for field in MATRIX_FIELDS:
            check(len(field_map.get(field, [])) == 1, f"{label} {node_id} has {len(field_map.get(field, []))} instances of {field}")
        if all(len(field_map.get(field, [])) == 1 for field in MATRIX_FIELDS):
            normalized_fields = [normalize_text(field_map[field][0].text_content()) for field in MATRIX_FIELDS]
            check(all(normalized_fields), f"{label} {node_id} contains an empty matrix field")
            calculated = hashlib.sha256("\n".join(normalized_fields).encode("utf-8")).hexdigest()
            check(stored_hashes.get(node_id) == calculated, f"{label} {node_id} six-field render hash mismatch: stored={stored_hashes.get(node_id)}, calculated={calculated}")
        outbound = descendant_elements(row, tag="a", attribute="data-am357-outbound")
        check(len(outbound) == 1, f"{label} {node_id} row has {len(outbound)} contained primary outbound links")
        reciprocal_fields = field_map.get("reciprocal-links", [])
        if len(outbound) == 1:
            check(outbound[0].attrs.get("data-am357-outbound") == node_id, f"{label} {node_id} outbound marker points to another node")
            check(any(outbound[0] in list(field.walk()) for field in reciprocal_fields), f"{label} {node_id} outbound link is not contained in reciprocal-links")
            if node_id in node_map:
                resolved, _, _ = check_local_target(outbound[0].attrs.get("href", ""), f"{label} {node_id} outbound", matrix["hub_routes"][language])
                check(resolved == node_map[node_id]["primary_routes"][language], f"{label} {node_id} outbound route drift: {resolved}")

    caret_anchors = elements(dom, tag="a", attribute="data-caepr-id")
    caret_ids = [anchor.attrs.get("data-caepr-id") for anchor in caret_anchors]
    hub_caret_sets[language] = set(caret_ids)
    check(len(caret_ids) == 25 and len(set(caret_ids)) == 25 and set(caret_ids) == EXPECTED_LINKED_CONFIRMED, f"{label} hub linked confirmed caret set is not the exact legacy 25-object set")
    registry_route = f"/{language}/" + ("registro-identidad-materia/" if language == "es" else "matter-identity-registry/")
    for anchor in caret_anchors:
        caepr_id = anchor.attrs.get("data-caepr-id", "")
        check(anchor.attrs.get("data-caret-state") == "CARET_CONFIRMED", f"{label} {caepr_id} has a non-confirmed caret state")
        record = record_by_id.get(caepr_id, {})
        check(normalize_text(anchor.text_content()) == normalize_text((record.get("public_labels") or {}).get(language, "")), f"{label} {caepr_id} visible caret label differs from machine control")
        resolved, target, _ = resolved_local_route(anchor.attrs.get("href", ""), f"{label} {caepr_id} caret link", matrix["hub_routes"][language])
        check(target is not None and target.is_file(), f"{label} {caepr_id} caret registry route is missing")
        check(caepr_id in registry_records, f"{label} {caepr_id} caret fragment is not an admitted registry ID")
        check(resolved == registry_route + f"#{caepr_id}", f"{label} {caepr_id} caret href drift: {resolved}")

    span_elements = elements(dom, attribute="data-caret-object-key")
    span_keys = [item.attrs.get("data-caret-object-key") for item in span_elements]
    hub_pending_sets[language] = set(span_keys)
    check(len(span_keys) == 7 and len(set(span_keys)) == 7 and set(span_keys) == SPECIALIST_SPAN_KEYS, f"{label} hub resolved span set is not the exact seven occurrence-row set")
    for item in span_elements:
        object_key = item.attrs.get("data-caret-object-key", "")
        check(item.tag == "span", f"{label} resolved occurrence {object_key} is not a span")
        check(item.attrs.get("data-caret-state") == "CARET_CONFIRMED", f"{label} resolved occurrence {object_key} has wrong state")
        check("href" not in item.attrs, f"{label} resolved occurrence {object_key} unexpectedly carries a link")
        record = record_by_key.get(object_key, {})
        check(normalize_text(item.text_content()) == normalize_text((record.get("public_labels") or {}).get(language, "")), f"{label} resolved occurrence {object_key} visible label differs from machine control")

    check("31/31" in text and "32/32" in text and "21/24" in text, f"{label} hub lacks specialist/unitary denominator separation")
    first_hop_sections = elements(dom, attribute="data-caret-first-hop-control")
    check(len(first_hop_sections) == 1, f"{label} hub must contain exactly one first-hop caret section")
    if len(first_hop_sections) == 1:
        first_hop_section = first_hop_sections[0]
        check(first_hop_section.attrs.get("data-caret-first-hop-control") == FIRST_HOP_CARET_CONTROL_ID, f"{label} first-hop section control ID drift")
        first_hop_visible = normalize_text(first_hop_section.text_content())
        check("61/130" in first_hop_visible and ("69 pending" in first_hop_visible.lower() or "69 pendientes" in first_hop_visible.lower()), f"{label} first-hop section lacks the exact 61/130 with 69 pending result")
        first_hop_links = [
            anchor for anchor in descendant_elements(first_hop_section, tag="a")
            if urljoin(matrix["hub_routes"][language], anchor.attrs.get("href", ""))
            == "/assets/data/caepr-caret-alberto-meeting-point-first-hop-v1.json"
        ]
        # urljoin on root-relative public routes retains the root path; compare
        # through the repository resolver instead of relying on host context.
        if not first_hop_links:
            first_hop_links = [
                anchor for anchor in descendant_elements(first_hop_section, tag="a")
                if resolved_local_route(anchor.attrs.get("href", ""), f"{label} first-hop machine link", matrix["hub_routes"][language])[1] == FIRST_HOP_CARET_PATH
            ]
        check(len(first_hop_links) == 1, f"{label} first-hop section lacks one exact machine-control link")
    partial_boundary = "NO TODO ES^" if language == "es" else "NOT ALL IS^"
    check(partial_boundary in text, f"{label} hub lacks the localized partial/not-all-is boundary")

check(hub_node_sets.get("es") == hub_node_sets.get("en") == NODE_ID_SET, "ES/EN hub node parity failed")
check(hub_caret_sets.get("es") == hub_caret_sets.get("en") == EXPECTED_LINKED_CONFIRMED, "ES/EN linked confirmed caret parity failed")
check(hub_pending_sets.get("es") == hub_pending_sets.get("en") == SPECIALIST_SPAN_KEYS, "ES/EN resolved occurrence-span parity failed")

# Each primary dossier must contain exactly one backlink block and the unique
# matching hub link must be inside that block, not merely elsewhere on the page.
for node_id in NODE_IDS:
    node = node_map.get(node_id, {})
    for language in ("es", "en"):
        source_route = (node.get("primary_routes") or {}).get(language, "")
        _, source_path, _ = resolved_local_route(source_route, f"{node_id} {language} backlink source")
        if source_path is None or not source_path.is_file():
            continue
        _, source_dom = parse(source_path)
        inbound_blocks = [item for item in elements(source_dom, attribute="data-am357-inbound") if item.attrs.get("data-am357-inbound") == node_id]
        check(len(inbound_blocks) == 1, f"{node_id} {language} primary route has {len(inbound_blocks)} exact inbound blocks")
        expected_hub = matrix["hub_routes"][language] + f"#am357-{node_id[-3:].lower()}"
        global_matches = [anchor for anchor in elements(source_dom, tag="a") if urljoin(source_route, anchor.attrs.get("href", "")) == expected_hub]
        check(len(global_matches) == 1, f"{node_id} {language} primary route has {len(global_matches)} total links to {expected_hub}")
        if len(inbound_blocks) == 1:
            contained = [anchor for anchor in descendant_elements(inbound_blocks[0], tag="a") if urljoin(source_route, anchor.attrs.get("href", "")) == expected_hub]
            check(len(contained) == 1, f"{node_id} {language} backlink is not uniquely contained in its inbound block")
        check_local_target(expected_hub, f"{node_id} {language} backlink destination")

# Every direct graph edge must be visible as a true endpoint-to-endpoint link
# at both endpoints in both languages. A hub backlink is not reciprocity.
edge_endpoint_occurrences: dict[str, dict[str, set[str]]] = {
    "es": defaultdict(set),
    "en": defaultdict(set),
}
project_safe_edge_href_count = 0
for node_id in NODE_IDS:
    incident = {
        edge_id: (target if source == node_id else source)
        for edge_id, (source, target) in EXPECTED_EDGE_ENDPOINTS.items()
        if node_id in {source, target}
    }
    for language in ("es", "en"):
        source_route = (node_map[node_id].get("primary_routes") or {}).get(language, "")
        _, source_path, _ = resolved_local_route(source_route, f"{node_id} {language} reciprocal-edge source")
        if source_path is None or not source_path.is_file():
            continue
        _, source_dom = parse(source_path)
        blocks = [item for item in elements(source_dom, attribute="data-am357-edge-endpoint") if item.attrs.get("data-am357-edge-endpoint") == node_id]
        check(len(blocks) == 1, f"{node_id} {language} primary route has {len(blocks)} reciprocal endpoint blocks")
        if len(blocks) != 1:
            continue
        anchors = descendant_elements(blocks[0], tag="a", attribute="data-am357-edge-id")
        actual_ids = [anchor.attrs.get("data-am357-edge-id") for anchor in anchors]
        check(len(actual_ids) == len(set(actual_ids)) == len(incident) and set(actual_ids) == set(incident), f"{node_id} {language} reciprocal edge set drift: actual={actual_ids}, expected={sorted(incident)}")
        for anchor in anchors:
            edge_id = anchor.attrs.get("data-am357-edge-id", "")
            peer = incident.get(edge_id)
            check(anchor.attrs.get("data-am357-edge-peer") == peer, f"{node_id} {language} {edge_id} peer marker drift")
            if peer:
                raw_href = anchor.attrs.get("href", "")
                parsed_href = urlsplit(raw_href)
                check(
                    bool(raw_href)
                    and not raw_href.startswith(("/", "//"))
                    and not parsed_href.scheme
                    and not parsed_href.netloc,
                    f"{node_id} {language} {edge_id} href is not project-safe relative navigation: {raw_href!r}",
                )
                project_safe_edge_href_count += 1
                expected_peer_route = node_map[peer]["primary_routes"][language]
                resolved, _, _ = check_local_target(raw_href, f"{node_id} {language} {edge_id} reciprocal target", source_route)
                check(resolved == expected_peer_route, f"{node_id} {language} {edge_id} does not link directly to {peer}: {resolved}")
                edge_endpoint_occurrences[language][edge_id].add(node_id)
check(project_safe_edge_href_count == 52, f"project-safe reciprocal href census is {project_safe_edge_href_count}, expected 52")
for language in ("es", "en"):
    check(set(edge_endpoint_occurrences[language]) == set(EXPECTED_EDGE_ENDPOINTS), f"{language} reciprocal edge census is not all 13 edges")
    for edge_id, endpoints in EXPECTED_EDGE_ENDPOINTS.items():
        check(edge_endpoint_occurrences[language].get(edge_id) == set(endpoints), f"{language} {edge_id} is not linked from both exact endpoints")

# Exact lateral topology, including location, containment and safe targets.
lateral_found: dict[str, dict[str, tuple[str, set[str]]]] = {"es": {}, "en": {}}
for language in ("es", "en"):
    for page in (ROOT / language).rglob("index.html"):
        raw = page.read_text(encoding="utf-8")
        if "data-am357-lateral" not in raw:
            continue
        _, dom = parse(page)
        source_route = route_for_html(page)
        for block in elements(dom, attribute="data-am357-lateral"):
            marker = block.attrs.get("data-am357-lateral", "")
            if marker in lateral_found[language]:
                errors.append(f"{language} duplicate lateral block marker {marker}")
                continue
            anchors = descendant_elements(block, tag="a")
            targets = {urljoin(source_route, anchor.attrs.get("href", "")) for anchor in anchors}
            check(len(targets) == len(anchors), f"{language} {marker} lateral block contains duplicate targets")
            for target in targets:
                check_local_target(target, f"{language} {marker} lateral target")
            lateral_found[language][marker] = (source_route, targets)
    check(set(lateral_found[language]) == set(EXPECTED_LATERAL[language]), f"{language} lateral marker set drift: actual={sorted(lateral_found[language])}, expected={sorted(EXPECTED_LATERAL[language])}")
    for marker, expected_value in EXPECTED_LATERAL[language].items():
        expected_pair = (expected_value[0], set(expected_value[1]))
        check(lateral_found[language].get(marker) == expected_pair, f"{language} {marker} lateral source/targets drift: actual={lateral_found[language].get(marker)}, expected={expected_pair}")
check(set(lateral_found["es"]) == set(lateral_found["en"]), "ES/EN lateral marker parity failed")
for marker in set(lateral_found["es"]) & set(lateral_found["en"]):
    check(len(lateral_found["es"][marker][1]) == len(lateral_found["en"][marker][1]), f"ES/EN lateral target-count parity failed for {marker}")

# Candidate manifest: finite route/source manifest plus monotonic publication
# lifecycle. Communication remains closed at every publication state.
check(manifest.get("schema") == "por-derecho.publication-manifest.v1", "candidate manifest schema drift")
check(manifest.get("control_id") == CONTROL_ID, "candidate manifest control ID drift")
check(manifest.get("analysis_order") == matrix.get("analysis_order"), "candidate manifest analysis order differs from matrix")
check(manifest.get("hub_routes") == matrix.get("hub_routes"), "candidate manifest hub routes differ from matrix")
manifest_unitary = manifest.get("unitary_caret_scope") or {}
manifest_specialist = manifest.get("specialist_caret_scope") or {}
manifest_first_hop = manifest.get("first_hop_caret_scope") or {}
check(manifest_unitary == {"control_id": UNITARY_SCOPE_CONTROL_ID, "confirmed": 21, "pending": 3, "denominator": 24, "changed_by_this_module": True}, "candidate manifest unitary scope drift")
check((manifest_specialist.get("control_id"), manifest_specialist.get("confirmed"), manifest_specialist.get("denominator"), manifest_specialist.get("pending"), manifest_specialist.get("suspended"), manifest_specialist.get("verdict"), manifest_specialist.get("identity_only"), manifest_specialist.get("confirmed_occurrence_rows")) == (CARET_CONTROL_ID, 31, 31, 0, 0, "ALL_IS_VERIFIED_FOR_STATED_SCOPE", True, 32), "candidate manifest specialist scope is not controlled 31/31 unique and 32/32 occurrence rows")
check((manifest_first_hop.get("control_id"), manifest_first_hop.get("confirmed"), manifest_first_hop.get("denominator"), manifest_first_hop.get("pending"), manifest_first_hop.get("suspended"), manifest_first_hop.get("verdict"), manifest_first_hop.get("identity_only")) == (FIRST_HOP_CARET_CONTROL_ID, 61, 130, 69, 0, "FULL_FIRST_HOP_CENSUS_PARTIAL_NOT_ALL_IS", True), "candidate manifest first-hop scope is not controlled 61/130/69 partial identity-only")
check(manifest.get("communication_authorized") is False, "candidate manifest improperly authorises communication")
check(manifest.get("email_or_filing_action") == "HOLD_NOT_AUTHORISED", "candidate manifest action state is not HOLD_NOT_AUTHORISED")

state = manifest.get("current_state")
check(state in set(ALLOWED_LIFECYCLE) | {BLOCKED_LIFECYCLE}, f"candidate manifest has unknown lifecycle state: {state}")
rank = ALLOWED_LIFECYCLE.index(state) if state in ALLOWED_LIFECYCLE else -1
check(manifest.get("status") == EXPECTED_STATUS_BY_STATE.get(state), f"{state} candidate manifest status drift")
if state in {"DRAFT", BLOCKED_LIFECYCLE}:
    check(manifest.get("publication_authorized") is False, f"{state} candidate improperly authorises publication")
    check(not manifest.get("publication_authorization"), f"{state} candidate must not contain publication authorization evidence")
else:
    check(manifest.get("publication_authorized") is True, f"{state} candidate lacks explicit publication authorization")
    authorization = manifest.get("publication_authorization") or {}
    check(isinstance(authorization, dict), f"{state} publication_authorization must be an object")
    check(authorization.get("scope_control_id") == CONTROL_ID, f"{state} publication authorization is not bound to this control ID")
    check(authorization.get("repository_and_website_only") is True, f"{state} publication authorization is not limited to repository and website")
    check(authorization.get("email_authorized") is False and authorization.get("filing_authorized") is False, f"{state} publication authorization improperly extends to email or filing")
    check(bool(authorization.get("user_instruction")) and bool(authorization.get("recorded_at")), f"{state} publication authorization lacks instruction/time evidence")

if state == "DRAFT":
    validation = manifest.get("validation") or {}
    check(validation.get("live_readback") == "not_run_not_authorised", "DRAFT manifest must record that live readback was not run and not authorised")
    for forbidden_key in ("merge_sha", "deployment_evidence", "live_urls", "live_readback"):
        check(not manifest.get(forbidden_key), f"DRAFT manifest contains premature {forbidden_key}")

if rank >= ALLOWED_LIFECYCLE.index("MERGED"):
    check(is_full_sha(manifest.get("merge_sha")), f"{state} candidate lacks a full 40-hex merge_sha")

if rank >= ALLOWED_LIFECYCLE.index("DEPLOYED"):
    deployment = manifest.get("deployment_evidence") or {}
    check(isinstance(deployment, dict), f"{state} deployment_evidence must be an object")
    check(deployment.get("workflow") == "pages build and deployment", f"{state} deployment evidence names the wrong workflow")
    check(deployment.get("conclusion") == "success", f"{state} deployment did not conclude successfully")
    check(isinstance(deployment.get("run_id"), int) and deployment.get("run_id", 0) > 0, f"{state} deployment evidence lacks a positive run ID")
    check(deployment.get("head_sha") == manifest.get("merge_sha"), f"{state} Pages head SHA does not equal merge SHA")

if rank >= ALLOWED_LIFECYCLE.index("LIVE_VERIFIED"):
    expected_hub_urls = [
        "https://sbu001monterecco.github.io/por-derecho" + route
        for route in (manifest.get("hub_routes") or {}).values()
    ]
    check(manifest.get("live_urls") == expected_hub_urls, f"{state} live URL set is not the exact bilingual hub set")
    readback = manifest.get("live_readback") or {}
    check(isinstance(readback, dict), f"{state} live_readback must be a structured object")
    check(readback.get("result") == "PASS_EXACT_BYTES", f"{state} live readback is not an exact-byte pass")
    check(readback.get("head_sha") == manifest.get("merge_sha"), f"{state} live readback SHA does not equal merge SHA")
    check(isinstance(readback.get("workflow_run_id"), int) and readback.get("workflow_run_id", 0) > 0, f"{state} live readback lacks a positive workflow run ID")
    hashes = readback.get("sha256_by_route") or {}
    check(isinstance(hashes, dict) and len(hashes) >= 37, f"{state} live readback lacks the finite route hash map")
    for route, digest in hashes.items():
        check(isinstance(route, str) and route.startswith("/"), f"{state} live hash map has an unsafe route")
        check(isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest) is not None, f"{state} live hash map has an invalid SHA-256")
    closeout = manifest.get("closeout_control") or {}
    check(isinstance(closeout, dict), f"{state} closeout_control must be an object")
    check(closeout.get("kind") == "SEPARATE_WORKFLOW_ARTIFACT", f"{state} closeout is not a separate workflow artifact")
    check(closeout.get("result") == "LIVE_VERIFIED", f"{state} closeout control is not a live-verification result")
    check(closeout.get("head_sha") == manifest.get("merge_sha"), f"{state} closeout SHA does not equal merge SHA")
    check(isinstance(closeout.get("workflow_run_id"), int) and closeout.get("workflow_run_id", 0) > 0, f"{state} closeout lacks a positive workflow run ID")
    check(isinstance(closeout.get("artifact_id"), int) and closeout.get("artifact_id", 0) > 0, f"{state} closeout lacks a positive artifact ID")
    check(bool(closeout.get("artifact_name")), f"{state} closeout lacks an artifact name")
    check(closeout.get("communication_authorized") is False and closeout.get("filing_authorized") is False, f"{state} closeout improperly opens communication or filing")

if state == "DELETION_SAFE":
    check(bool(manifest.get("deletion_audit")), "DELETION_SAFE manifest lacks a deletion-audit reference")

# A public PR or main push is itself a publication operation. A DRAFT or
# recovery-blocked candidate may validate locally, but must fail closed in CI.
if os.environ.get("GITHUB_ACTIONS") == "true" and os.environ.get("GITHUB_EVENT_NAME") in {"pull_request", "push"}:
    check(state not in {"DRAFT", BLOCKED_LIFECYCLE}, f"CI publication event cannot carry lifecycle state {state}")

expected_route_files: dict[str, list[str]] = {}
for language in ("es", "en"):
    routes = [matrix.get("hub_routes", {}).get(language, "")] + [node_map.get(node_id, {}).get("primary_routes", {}).get(language, "") for node_id in NODE_IDS]
    files = [route_file(route, f"manifest expected {language} route") for route in routes]
    expected_route_files[language] = [file for file in files if file is not None]
check(manifest.get("expected_routes") == expected_route_files, f"candidate manifest expected-route census drift: actual={manifest.get('expected_routes')}, expected={expected_route_files}")
for reference in manifest.get("expected_source_files", []):
    path, fragment = safe_repo_path(reference, "candidate manifest source file")
    check(not fragment, f"candidate manifest source file has a fragment: {reference}")
    if path is not None:
        check(path.is_file(), f"candidate manifest source file missing: {reference}")

manifest_evidence = manifest.get("multidirectional_evidence") or {}
check((manifest_evidence.get("nodes"), manifest_evidence.get("forward_reverse_bridge_tests"), manifest_evidence.get("primary_source_routes")) == (9, 13, 18), "candidate manifest graph census drift")
check(manifest_evidence.get("required_fields_per_node") == [field.replace("-", "_") for field in MATRIX_FIELDS], "candidate manifest six-field declaration drift")

# Human controls, current digest and stale finite-scope assertions.
audit_text = AUDIT_PATH.read_text(encoding="utf-8")
human_matrix_text = HUMAN_MATRIX_PATH.read_text(encoding="utf-8")
plan_text = PLAN_PATH.read_text(encoding="utf-8")
current_digest_md = CURRENT_DIGEST_MD_PATH.read_text(encoding="utf-8")
six_surface_text = "\n".join((es_text, en_text, MATRIX_PATH.read_text(encoding="utf-8"), human_matrix_text, audit_text, plan_text))
for forbidden in (r"\b20/20\b", r"\b9/20\b", r"\bFinite 20-object\b", r"ALL_IS_VERIFIED_FOR_STATED_SCOPE_ONLY"):
    check(re.search(forbidden, six_surface_text, flags=re.IGNORECASE) is None, f"six-surface specialist scope retains forbidden stale/affirmative marker: {forbidden}")
for marker in ("Eligible named objects: **32**", "`CARET_CONFIRMED`: **25**", "`CARET_PENDING`: **7**", "25/32 = 78.125%", "19/24 confirmed, 5 pending", "PD-SP-O-0070", "PD-SP-I-0018", "**Total** | **204**"):
    check(marker in audit_text, f"specialist audit missing marker {marker!r}")
for marker in ("**56** | **74** | **0** | **130**", "56/130 = 43.076923", "assets/data/caepr-caret-alberto-meeting-point-first-hop-v1.json"):
    check(marker in audit_text, f"first-hop audit missing marker {marker!r}")
for marker in (CONTROL_ID, "forward:", "backward:", "AM357-N01", "AM357-N09", "31/31", "32/32", "61/130", "21/24", "PARTIAL, NOT ALL IS^"):
    check(marker in human_matrix_text, f"human matrix missing marker {marker!r}")
human_rows = [line for line in human_matrix_text.splitlines() if re.match(r"^\| `AM357-N\d{2}`", line)]
check(len(human_rows) == 9, "human node matrix does not contain exactly nine visible node rows")
check("| Reciprocal endpoint links |" in human_matrix_text, "human node matrix lacks the visible sixth reciprocal-links field")
for node_id in NODE_IDS:
    matching_rows = [line for line in human_rows if line.startswith(f"| `{node_id}`")]
    check(len(matching_rows) == 1, f"human node matrix lacks one exact row for {node_id}")
    if len(matching_rows) != 1:
        continue
    cells = matching_rows[0].split("|")
    check(len(cells) == 9, f"human node matrix {node_id} does not have node plus six evidence fields")
    reciprocal_cell = cells[-2] if len(cells) >= 2 else ""
    incident = {
        edge_id: (target if source == node_id else source)
        for edge_id, (source, target) in EXPECTED_EDGE_ENDPOINTS.items()
        if node_id in {source, target}
    }
    for edge_id, peer in incident.items():
        short_edge_id = edge_id.removeprefix("AM357-")
        check(reciprocal_cell.count(f"[{short_edge_id} ↔ {peer[-3:]} ES]") == 1, f"human node matrix {node_id} lacks one visible {edge_id} reciprocal label")
        for language in ("es", "en"):
            target = ".." + node_map[peer]["primary_routes"][language]
            check(reciprocal_cell.count(f"]({target})") == 1, f"human node matrix {node_id} {edge_id} lacks the exact {language.upper()} peer target")
check("31/31 unique identities" in current_digest_md and "61 confirmed, 69 pending" in current_digest_md and "repository-wide 21/24" in current_digest_md, "current digest does not keep specialist all-is, 61/130 and unitary 21/24 scopes separate")

digest_identity = current_digest.get("identity_registry") or {}
digest_caret = current_digest.get("caret_scope") or {}
check({key: digest_identity.get(key) for key in EXPECTED_REGISTRY_COUNTS} == EXPECTED_REGISTRY_COUNTS, "current digest source/static identity registry is not 336/157/83/11/42/43")
check((digest_caret.get("confirmed"), digest_caret.get("denominator"), digest_caret.get("pending")) == (21, 24, 3), "current digest unitary caret scope is not 21/24/3")
check(digest_caret.get("control_id") == CANONICAL_UNITARY_CARET_CONTROL_ID, "current digest unitary caret control ID drift")
digest_modules = {module.get("module_id"): module for module in current_digest.get("specialist_modules", []) if isinstance(module, dict)}
digest_specialist = digest_modules.get(CONTROL_ID, {})
check(digest_specialist.get("first_hop_caret_control") == "assets/data/caepr-caret-alberto-meeting-point-first-hop-v1.json", "current digest lacks the first-hop machine control")
check(digest_specialist.get("first_hop_caret_scope") == {"confirmed": 61, "pending": 69, "suspended": 0, "denominator": 130, "verdict": "FULL_FIRST_HOP_CENSUS_PARTIAL_NOT_ALL_IS"}, "current digest first-hop caret scope drift")
if rank < ALLOWED_LIFECYCLE.index("LIVE_VERIFIED"):
    check((digest_identity.get("last_live_verified_counts") or {}).get("total") in {194, 204}, "pre-live candidate digest lacks an explicit prior live denominator")
else:
    check(digest_identity.get("last_live_verified_counts") == EXPECTED_SPECIALIST_LIVE_REGISTRY_COUNTS, "specialist LIVE_VERIFIED snapshot no longer preserves its exact 204-record readback")

# Judicial title and court-reorganisation controls.
title_control_text = TITLE_CONTROL_PATH.read_text(encoding="utf-8")
normalized_title_control = normalize_text(title_control_text)
check(
    title_control_text.startswith(
        "# Ilmo. Sr. D. Alberto López Villarrubia, Magistrado-Juez del entonces Juzgado de lo Mercantil n.º 1 de Las Palmas de Gran Canaria"
    ),
    "judicial-title control itself lacks the capacity-correct first-reference heading",
)
for marker in (
    "31 December 2025",
    "plaza n.º 1",
    "plaza n.º 3",
    "Sección de lo Mercantil del Tribunal de Instancia de Las Palmas de Gran Canaria",
    "signed original and allocation trail",
    "el Ilmo. Sr. D. Alberto López Villarrubia, Magistrado-Juez del entonces Juzgado de lo Mercantil n.º 1 de Las Palmas de Gran Canaria",
    "Magistrate-Judge Alberto López Villarrubia of the then Commercial Court No. 1 of Las Palmas de Gran Canaria",
):
    check(marker in normalized_title_control, f"judicial-title control missing {marker!r}")

es_visible = normalize_text(es_dom.text_content()).replace("^,", ",").replace("^ of", " of")
en_visible = normalize_text(en_dom.text_content()).replace("^,", ",").replace("^ of", " of")
check("Ilmo. Sr. D. Alberto López Villarrubia, Magistrado-Juez del entonces Juzgado de lo Mercantil n.º 1 de Las Palmas de Gran Canaria" in es_visible, "Spanish hub lacks the controlled historical first reference")
check("plaza n.º 1 de la Sección de lo Mercantil del Tribunal de Instancia de Las Palmas de Gran Canaria" in es_visible, "Spanish hub lacks the current position-no.-1 designation")
check("Magistrate-Judge Alberto López Villarrubia of the then Commercial Court No. 1 of Las Palmas de Gran Canaria" in en_visible, "English hub lacks the controlled historical first reference")
check("judicial position No. 1 in the Commercial Section of the Court of Instance of Las Palmas de Gran Canaria" in en_visible, "English hub lacks the current position-no.-1 designation")
check("<title>Magistrado-Juez D. Alberto López Villarrubia:" in es_text, "Spanish hub HTML title lacks Magistrado-Juez")
check("<title>Magistrate-Judge Alberto López Villarrubia:" in en_text, "English hub HTML title lacks Magistrate-Judge")

controlled_heading_prefixes = (
    "# Ilmo. Sr. D. Alberto López Villarrubia, Magistrado-Juez del entonces Juzgado de lo Mercantil n.º 1 de Las Palmas de Gran Canaria / Meeting Point 357/2024",
    "# Magistrate-Judge Alberto López Villarrubia of the then Commercial Court No. 1 of Las Palmas de Gran Canaria / Meeting Point 357/2024",
)
for path, content in ((AUDIT_PATH, audit_text), (HUMAN_MATRIX_PATH, human_matrix_text), (PLAN_PATH, plan_text)):
    first_line = content.splitlines()[0] if content.splitlines() else ""
    check(first_line.startswith(controlled_heading_prefixes), f"{path.relative_to(ROOT)} lacks a capacity-correct first-reference heading")
    check(not re.search(r"^#\s+(?:Alberto|Judge Alberto|Juez Alberto|Magistrado Alberto)\b", first_line), f"{path.relative_to(ROOT)} uses a prohibited bare judicial heading")

crosslink_counts = {"es": 0, "en": 0}
for language in ("es", "en"):
    expected_hub = matrix.get("hub_routes", {}).get(language, "")
    required_label = "magistrado López Villarrubia / Meeting Point" if language == "es" else "Magistrate López Villarrubia / Meeting Point"
    required_current_title = (
        "magistrado D. Alberto López Villarrubia, titular de la plaza n.º 1 de la Sección de lo Mercantil del Tribunal de Instancia de Las Palmas de Gran Canaria"
        if language == "es"
        else "Magistrate Alberto López Villarrubia, holder of judicial position No. 1 in the Commercial Section of the Court of Instance of Las Palmas de Gran Canaria"
    )
    for page in (ROOT / language).rglob("index.html"):
        raw = page.read_text(encoding="utf-8")
        if "data-am357-crosslink" not in raw:
            continue
        _, dom = parse(page)
        source_route = route_for_html(page)
        for block in elements(dom, attribute="data-am357-crosslink"):
            crosslink_counts[language] += 1
            visible = normalize_text(block.text_content())
            check(required_label.lower() in visible.lower(), f"{language} {source_route} crosslink lacks the controlled Magistrate López Villarrubia / Meeting Point label")
            check(required_current_title in visible, f"{language} {source_route} crosslink lacks the full current judicial title")
            check("Alberto / Meeting Point" not in visible and "Alberto López Villarrubia / Meeting Point" not in visible, f"{language} {source_route} crosslink uses a bare Alberto label")
            hub_links = [anchor for anchor in descendant_elements(block, tag="a") if urljoin(source_route, anchor.attrs.get("href", "")).split("#", 1)[0] == expected_hub]
            check(len(hub_links) == 1, f"{language} {source_route} crosslink does not contain exactly one specialist-hub link")
            if hub_links:
                check_local_target(hub_links[0].attrs.get("href", ""), f"{language} {source_route} crosslink target", source_route)
check(crosslink_counts["es"] == crosslink_counts["en"] and crosslink_counts["es"] > 0, f"ES/EN title-controlled crosslink count parity failed: {crosslink_counts}")

check("HOLD" in plan_text and "No email" in plan_text, "authority plan must remain HOLD and prohibit email action")
check(CONTROL_ID in plan_text and "AM357-N01" in plan_text and "AM357-N09" in plan_text, "authority plan lacks node-controlled attachment rule")

for phrase in (
    "Alberto signed the 24 October",
    "Alberto firmó el 24 de octubre",
    "concealed the conflict as established fact",
    "Meeting Point committed a crime",
    "Meeting Point cometió un delito",
):
    check(phrase not in es_text and phrase not in en_text, f"forbidden overstatement: {phrase}")

for rel in ("sitemap.xml", "sitemap-meeting-point.xml", "sitemap-judicial-spine.xml"):
    sitemap_path = ROOT / rel
    check(sitemap_path.is_file(), f"missing {rel}")
    if not sitemap_path.is_file():
        continue
    sitemap_text = sitemap_path.read_text(encoding="utf-8")
    for slug in ("alberto-lopez-villarrubia-meeting-point-357-masa-activa", "alberto-lopez-villarrubia-meeting-point-357-active-estate"):
        check(slug in sitemap_text, f"{rel} missing {slug}")

if errors:
    raise SystemExit("\n".join(f"- {error}" for error in errors))

print("MAGISTRATE-JUDGE LÓPEZ VILLARRUBIA / MEETING POINT CROSS-PROCEEDING: PASS")
print(" - specialist caret census: 31/31 unique identities and 32/32 occurrence rows; ALL IS^ for stated scope")
print(" - first-hop evidence-corpus caret census: 61/130 confirmed; 69 pending; PARTIAL — NOT ALL IS^")
print(" - repository-wide unitary caret census: separately 21/24; 3 pending")
print(" - graph: 9 bilingual six-field nodes; 13 direct forward/reverse bridges")
print(" - primary backlinks: 18/18 contained; direct incident reciprocity: 26/26 per language; legacy lateral topology: 8/8 per language")
print(" - dated digest source registry: 336 / 157 / 83 / 11 / 42 / 43; prior exact-live snapshot remains historical")
print(" - current canonical source registry: 342 / 162 / 83 / 11 / 43 / 43")
print(f" - candidate publication state: {state}; communication and filing remain HOLD")
