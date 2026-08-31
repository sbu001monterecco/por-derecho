#!/usr/bin/env python3
"""Structural/evidential audit for the proceedings map and Case Prism."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    ".github/governance/UNITARY_PROCEEDINGS_INTERCONNECTIVITY_MAP_PROTOCOL_30AUG2026.md",
    ".github/governance/A_SCAN_360_CASE_PRISM_AND_READER_LENS_PROTOCOL_30AUG2026.md",
    "archive/PROCEEDINGS_ANTI_FRAGMENTATION_CONVERGENCE_RULE_30AUG2026.md",
    "archive/INSTITUTIONAL_READER_UNITARY_PROCEEDINGS_RULE_30AUG2026.md",
    "archive/CAIXABANK_VALENCIA_01859_2023_REGISTRATION_GAP_30AUG2026.md",
    "archive/PROCEEDINGS_MASTER_REGISTER_VALENCIA_1859_2023_OVERLAY_30AUG2026.md",
    "archive/GC_548_2023_PLAZA2_T1_CARET_CONTINUITY_CONTROL_30AUG2026.md",
    "archive/DP3205_2014_ARRECIFE_SOURCE_TRANSLATION_AUTHORITY_ALLEGATIONS_CONTROL_30AUG2026.md",
    "archive/ARRECIFE_4009_2015_CARET_INTERLINK_CONTROL_30AUG2026.md",
    "archive/ARRECIFE_1103_1132_1010_804_CARET_INTERLINK_CONTROL_30AUG2026.md",
    "archive/TESORO_TRANSPARENCIA_7_2026_CONTINUITY_AUDIT_28AUG2026.md",
    "archive/MISSING_EVIDENCE_REGISTER.md",
    "archive/PROCEEDINGS_CASE_PRISM_V1_SEED_30AUG2026.json",
    "archive/knowledge-project/DP1956_STATUS_REOPENING_CORRECTION_18AUG2026.md",
    "archive/PROCEEDINGS_MASTER_REGISTER.csv",
    "assets/data/proceedings-interconnectivity-schema-v1.json",
    "assets/data/proceedings-case-prism-v1.json",
    "assets/data/proceedings-master-public-v1.json",
    "assets/data/proceedings-interlinkability-v1.json",
    "assets/data/fiscalia-response-correspondence.json",
    "assets/data/caepr-caret-alberto-meeting-point-first-hop-v1.json",
    "assets/data/counsel-procurador-gap-register-v1.json",
    "assets/data/dp3205-2014-arrecife-v1.json",
    "assets/data/treasury-transparency-7-2026-v1.json",
    "assets/proceedings-interconnectivity-map-20260830.js",
    "assets/proceedings-interconnectivity-map-20260830.css",
    "assets/master-proceedings-publication-20260830.js",
    "en/proceedings-map/index.html", "es/mapa-procedimientos/index.html",
    "en/master-proceedings-register/index.html", "es/registro-maestro-procedimientos/index.html",
    "en/public-authority-unitary-case-reconstruction/index.html",
    "es/reconstruccion-unitaria-autoridades-publicas/index.html",
    "en/calificacion-rpl-2523-evidence-map/index.html",
    "es/calificacion-rpl-2523-mapa-prueba/index.html",
    "en/insolvency-36-2012-administrator-removal-fees/index.html",
    "es/concurso-36-2012-separacion-ac-honorarios/index.html",
    "en/insolvency-36-2012-ap-section-4/index.html",
    "es/concurso-36-2012-ap-seccion-4/index.html",
    "en/insolvency-36-2012-insolvency-administrator/index.html",
    "es/concurso-36-2012-administrador-concursal/index.html",
    "en/insolvency-classification-parallel-lives/index.html",
    "es/calificacion-concurso-36-2012-vidas-paralelas/index.html",
    "en/fiscalia-dip-2-2026/index.html",
    "es/fiscalia-dip-2-2026/index.html",
    "en/public-prosecution-inspection-exp-gub-745-2026/index.html",
    "es/fiscalia-inspeccion-exp-gub-745-2026/index.html",
    "en/dp-3205-2014-arrecife/index.html",
    "es/dp-3205-2014-arrecife/index.html",
    "en/arrecife-1103-2018-procedural-lineage/index.html",
    "es/arrecife-1103-2018-cadena-procesal/index.html",
    "scripts/build_proceedings_case_prism_v2.py",
    "publication-manifests/gc-548-2023-plaza2-t1-caret-20260830.json",
    "publication-manifests/arrecife-1304-2014-identity-interlink-20260830.json",
    "docs/deletion-audits/2026-08-30-arrecife-1304-2014-identity-interlink-continuity.md",
    "publication-manifests/master-proceedings-publication-20260830.json",
    "publication-manifests/dp3205-2014-arrecife-caret-interlink-20260830.json",
    "publication-manifests/arrecife-4009-2015-caret-interlink-20260830.json",
    "publication-manifests/arrecife-1103-2018-caret-interlink-20260830.json",
    "publication-manifests/treasury-transparency-7-2026-20260830.json",
    "scripts/audit_arrecife_1103_caret_interlink.py",
    ".github/workflows/audit-arrecife-1103-caret-interlink.yml",
    "scripts/build_public_proceedings_projection.py",
    "scripts/build_proceedings_interlinkability_v1.py",
    "publication-manifests/all-proceedings-interlinkability-20260830.json",
    "docs/deletion-audits/2026-08-30-all-proceedings-interlinkability-continuity.md",
    "publication-manifests/case-prism-substantive-gap-closure-20260831.json",
    "docs/deletion-audits/2026-08-31-case-prism-substantive-gap-closure-continuity.md",
]

# The institutional-reader audit is intentionally an identified-route
# denominator, not a claim that every historical narrative page has a single
# proceeding mapping.  Exact routes use only existing controlled Master IDs;
# multi-file pages remain generic to avoid fabricating a docket connection.
INSTITUTIONAL_MULTI_FILE_ROUTES = (
    "en/cgpj-public-prosecution-routing-update-20-august-2026/index.html",
    "en/credit-classification-control-art-93-97-310/index.html",
    "en/insolvency-administrator-credit-to-title-gatekeeper/index.html",
    "en/insolvency-administrator-loyalty-breakpoint/index.html",
    "en/insolvency-administrator-security-request-sun-park-27-february-2018/index.html",
    "en/insolvency-classification-parallel-lives/hearing-evidence-witnesses/index.html",
    "en/insolvency-classification-parallel-lives/hearing-evidence-witnesses/verification-requests/index.html",
    "en/insolvency-classification-parallel-lives/prior-judicial-knowledge-rescue/index.html",
    "en/ona-hotels-insolvency-exit-36-2012/carlos-sanz-insolvency-administrator/index.html",
    "en/open-letter-public-prosecution-service/addressees.html",
    "en/open-letter-public-prosecution-service/index.html",
    "en/prosecutorial-professional-evidence-pwc-grant-thornton-rsm/index.html",
    "es/actualizacion-cgpj-fiscalia-20-agosto-2026/index.html",
    "es/administrador-concursal-puerta-credito-titulo/index.html",
    "es/administrador-concursal-punto-quiebre-lealtad/index.html",
    "es/calificacion-concurso-36-2012-vidas-paralelas/conocimiento-previo-rescate/index.html",
    "es/calificacion-concurso-36-2012-vidas-paralelas/vista-prueba-testigos/index.html",
    "es/calificacion-concurso-36-2012-vidas-paralelas/vista-prueba-testigos/solicitudes-verificacion/index.html",
    "es/carta-abierta-ministerio-fiscal/destinatarios.html",
    "es/carta-abierta-ministerio-fiscal/index.html",
    "es/control-clasificacion-credito-art-93-97-310/index.html",
    "es/fiscalia-evidencia-profesional-pwc-grant-thornton-rsm/index.html",
    "es/ona-hotels-salida-concurso-36-2012/carlos-sanz-administrador-concursal/index.html",
    "es/solicitud-seguridad-administracion-concursal-sun-park-27-febrero-2018/index.html",
)
INSTITUTIONAL_EXACT_ROUTE_IDS = {
    "en/fiscalia-tenerife-eg95-2026/index.html": ("TF-FIS-008",),
    "en/insolvency-classification-criminal-misuse-thesis/index.html": ("GC-APP-004",),
    "en/prosecution-di273-2013-complaint-gil-patricia/index.html": ("GC-FIS-011",),
    "en/public-prosecution-745-parallel-actions/index.html": ("NAT-FIS-004",),
    "en/public-prosecution-inspection-exp-gub-745-2026/action-diary-29-august-2026.html": ("NAT-FIS-004",),
    "en/public-prosecution-inspection-exp-gub-745-2026/continuity-errors-omissions-31-august-2026.html": ("NAT-FIS-004",),
    "en/public-prosecution-inspection-exp-gub-745-2026/index.html": ("NAT-FIS-004",),
    "en/public-prosecution-inspection-exp-gub-745-2026/open-prosecution-transparency-31-august-2026.html": ("NAT-FIS-004",),
    "en/public-prosecution-inspection-exp-gub-745-2026/response-package-29-august-2026.html": ("NAT-FIS-004",),
    "en/public-prosecution-inspection-exp-gub-745-2026/visual-facsimile-31-august-2026.html": ("NAT-FIS-004",),
    "es/fiscalia-745-acciones-paralelas/index.html": ("NAT-FIS-004",),
    "es/fiscalia-di273-2013-querella-gil-patricia/index.html": ("GC-FIS-011",),
    "es/fiscalia-inspeccion-exp-gub-745-2026/continuidad-errores-omisiones-31-agosto-2026.html": ("NAT-FIS-004",),
    "es/fiscalia-inspeccion-exp-gub-745-2026/diario-actuaciones-29-agosto-2026.html": ("NAT-FIS-004",),
    "es/fiscalia-inspeccion-exp-gub-745-2026/facsimil-visual-31-agosto-2026.html": ("NAT-FIS-004",),
    "es/fiscalia-inspeccion-exp-gub-745-2026/index.html": ("NAT-FIS-004",),
    "es/fiscalia-inspeccion-exp-gub-745-2026/paquete-respuesta-29-agosto-2026.html": ("NAT-FIS-004",),
    "es/fiscalia-inspeccion-exp-gub-745-2026/persecucion-abierta-transparencia-31-agosto-2026.html": ("NAT-FIS-004",),
    "es/fiscalia-tenerife-dp748/index.html": ("TF-CRI-003",),
    "es/fiscalia-tenerife-eg95-2026/index.html": ("TF-FIS-008",),
    "es/tesis-uso-criminal-procedimiento-calificacion/index.html": ("GC-APP-004",),
}
MATERIAL_DOSSIER_ROUTE_IDS = {
    "en/arrecife-1103-2018-procedural-lineage/index.html": ("LZ-JUD-003", "LZ-APP-004"),
    "es/arrecife-1103-2018-cadena-procesal/index.html": ("LZ-JUD-003", "LZ-APP-004"),
    "en/dp-3205-2014-arrecife/index.html": ("LZ-JUD-043",),
    "es/dp-3205-2014-arrecife/index.html": ("LZ-JUD-043",),
    "en/rollo-1010-2018-order-804-2018/index.html": ("LZ-JUD-003", "LZ-APP-004"),
    "es/rollo-1010-2018-auto-804-2018/index.html": ("LZ-JUD-003", "LZ-APP-004"),
}
INSTITUTIONAL_WORKFLOW_PATTERNS = (
    "en/cgpj-public-prosecution-*/**", "en/credit-classification-control-*/**",
    "en/fiscalia-*/**", "en/insolvency-administrator-*/**",
    "en/insolvency-classification-*/**", "en/ona-hotels-insolvency-exit-36-2012/**",
    "en/open-letter-public-prosecution-service/**", "en/prosecution-di273-2013-complaint-gil-patricia/**",
    "en/prosecutorial-professional-evidence-*/**", "en/public-prosecution-*/**",
    "es/actualizacion-cgpj-fiscalia-*/**", "es/administrador-concursal-*/**",
    "es/calificacion-concurso-36-2012-vidas-paralelas/**", "es/carta-abierta-ministerio-fiscal/**",
    "es/control-clasificacion-credito-*/**", "es/fiscalia-*/**",
    "es/ona-hotels-salida-concurso-36-2012/**", "es/solicitud-seguridad-administracion-concursal-*/**",
    "es/tesis-uso-criminal-procedimiento-calificacion/**",
)
REQUIRED.extend(INSTITUTIONAL_MULTI_FILE_ROUTES)
REQUIRED.extend(INSTITUTIONAL_EXACT_ROUTE_IDS)
REQUIRED.extend(MATERIAL_DOSSIER_ROUTE_IDS)
errors: list[str] = []

# Current canonical/public denominators after the 31-August Ministerio Fiscal
# backfill.  The separately named 30-August lifecycle manifest below remains an
# immutable deployment checkpoint and is therefore audited against its own
# historical denominators rather than these current values.
CURRENT_CANONICAL_RECORDS = 122
CURRENT_PUBLIC_RECORDS = 121
CURRENT_CANONICAL_EXACT = 98
CURRENT_PUBLIC_EXACT = 97
CURRENT_PRIVATE_EXACT = 1
CURRENT_CASE_PRISM_EXACT_COVERED = 43
CURRENT_CASE_PRISM_EXACT_UNCOVERED = 54
CURRENT_DIRECT_PAIRS = 33
CURRENT_VERIFIED_DIRECT_PAIRS = 31
CURRENT_PENDING_DIRECT_PAIRS = 2
CURRENT_DIRECT_ASSERTIONS = 40
CURRENT_VERIFIED_DIRECT_ASSERTIONS = 38
CURRENT_PENDING_DIRECT_ASSERTIONS = 2
CURRENT_FISCALIA_OFFICE_FILE_RECORDS = 24
CURRENT_FISCALIA_EXACT_RECORDS = 21
CURRENT_FISCALIA_UNRESOLVED_RECORDS = 3
CURRENT_FISCALIA_RESPONSE_EPISODES = 9
CURRENT_FISCALIA_PROFILED_MATRIX_RECORDS = 8
EXPECTED_FINITE_TEST_FAMILY_COUNTS = {
    "ADMIN_AUTHORITY_TITLE_SOURCE": 26,
    "CIVIL_FILE_DECISION": 19,
    "CRIMINAL_FILE_DECISION": 11,
    "FISCALIA_INSTITUTIONAL_MEMORY": 21,
    "OMBUDSMAN_RECONSIDERATION": 1,
    "PROFESSIONAL_SUPERVISION": 8,
    "REGULATORY_PUBLIC_ROUTE": 7,
    "TAX_CONTENTIOUS_CHAIN": 4,
}

EXPECTED_FISCALIA_EPISODE_MASTER_IDS = {
    "first-frame-2013": "GC-FIS-011",
    "di248-2018": "GC-FIS-013",
    "di113-2022": "GC-FIS-014",
    "di22-2026": "GC-FIS-016",
    "dip2-2026": "GC-FIS-017",
    "eg49-2026": "GC-FIS-018",
    "dp1901-2026": "GC-CRI-008",
    "eg745-2026": "NAT-FIS-004",
    "gub86-2026": "LZ-FIS-007",
}

INSTITUTIONAL_RECEIPT_AXES = {
    "transmission_status",
    "registration_status",
    "file_incorporation_status",
    "recipient_attribution_status",
    "substantive_examination_status",
    "decision_use_status",
}
PUBLIC_RENDERER_RECEIPT_AXES = [
    "transmission_status",
    "material_received_status",
    "referral_status",
    "registration_status",
    "file_incorporation_status",
    "recipient_attribution_status",
    "substantive_examination_status",
    "decision_use_status",
    "cross_file_acknowledgement_status",
]
PUBLIC_RENDERER_AXIS_STATUS_LOCATIONS = {
    "transmission_status": "receipt_knowledge.institutional_axes",
    "material_received_status": "receipt_knowledge.institutional_axis_basis.status",
    "referral_status": "receipt_knowledge.institutional_axis_basis.status",
    "registration_status": "receipt_knowledge.institutional_axes",
    "file_incorporation_status": "receipt_knowledge.institutional_axes",
    "recipient_attribution_status": "receipt_knowledge.institutional_axes",
    "substantive_examination_status": "receipt_knowledge.institutional_axes",
    "decision_use_status": "receipt_knowledge.institutional_axes",
    "cross_file_acknowledgement_status": "receipt_knowledge.root",
}
FISCALIA_MATRIX_AXES = set(PUBLIC_RENDERER_RECEIPT_AXES)
EXPECTED_FISCALIA_MATRIX_REFERRAL_STATUS = {
    "LZ-FIS-007": "ROUTING_DOCUMENTED",
}
EXPECTED_FISCALIA_EPISODE_REFERRAL_STATUS = {
    "dp1901-2026": "ROUTING_DOCUMENTED",
    "gub86-2026": "ROUTING_DOCUMENTED",
}
EXPECTED_FISCALIA_EPISODE_MATERIAL_STATUS = {
    "first-frame-2013": "PARTLY_DOCUMENTED",
    "di248-2018": "PARTLY_DOCUMENTED",
    "di113-2022": "PARTLY_DOCUMENTED",
    "di22-2026": "PARTLY_DOCUMENTED",
    "dip2-2026": "DOCUMENTED",
    "eg49-2026": "PARTLY_DOCUMENTED",
    "dp1901-2026": "NOT_LOCATED",
    "eg745-2026": "DOCUMENTED",
    "gub86-2026": "NOT_LOCATED",
}
EXPECTED_FISCALIA_AXIS_SOURCE_FIELDS = {
    "transmission_status": "known",
    "material_received_status": "known",
    "referral_status": "known",
    "registration_status": "known",
    "file_incorporation_status": "response",
    "recipient_attribution_status": "response",
    "substantive_examination_status": "response",
    "decision_use_status": "response",
    "cross_file_acknowledgement_status": "known",
}
EXPECTED_FISCALIA_EPISODE_AXIS_SOURCE_FIELD_OVERRIDES = {
    ("di22-2026", "recipient_attribution_status"): "known",
    ("eg49-2026", "recipient_attribution_status"): "known",
    ("dip2-2026", "substantive_examination_status"): "known",
}
EXPECTED_FISCALIA_AXIS_STATUS_PRECISION = {
    ("eg745-2026", "recipient_attribution_status"): "NOT_LOCATED",
    ("eg745-2026", "cross_file_acknowledgement_status"): "STATUS_UNRESOLVED",
    ("gub86-2026", "material_received_status"): "NOT_LOCATED",
}

HISTORICAL_30AUG_PUBLIC_RECORDS = 106
HISTORICAL_30AUG_PUBLIC_EXACT = 85
HISTORICAL_30AUG_DIRECT_PAIRS = 17
HISTORICAL_30AUG_VERIFIED_DIRECT_PAIRS = 16
HISTORICAL_30AUG_PENDING_DIRECT_PAIRS = 1
HISTORICAL_30AUG_DIRECT_ASSERTIONS = 21
HISTORICAL_30AUG_VERIFIED_DIRECT_ASSERTIONS = 20
HISTORICAL_30AUG_PENDING_DIRECT_ASSERTIONS = 1
HISTORICAL_30AUG_CONTEXT_CLUSTERS = 26


def require(condition: bool, label: str) -> None:
    if not condition:
        errors.append(label)


def require_bilingual(value: object, label: str) -> None:
    require(
        isinstance(value, dict)
        and bool(str(value.get("en", "")).strip())
        and bool(str(value.get("es", "")).strip()),
        f"{label} is not complete and bilingual",
    )


def actor_status_is_positive(status: str) -> bool:
    """Treat only an affirmative, source-bearing actor grade as positive."""
    token = str(status or "").strip().upper()
    if not token:
        return False
    negative_markers = (
        "NO_ACTOR_SPECIFIC",
        "NOT_ESTABLISHED",
        "NOT_LOCATED",
        "NOT_MODELLED",
        "UNAVAILABLE",
        "UNRESOLVED",
        "OPEN_",
        "PENDING",
    )
    return not any(marker in token for marker in negative_markers)


def expected_finite_test_family(row: dict[str, str]) -> str:
    """Audit the UI family taxonomy independently of free-text substring order."""
    stream = row.get("Stream", "").upper()
    master_id = row.get("Master_ID", "")
    record_type = row.get("Record_Type", "").upper()
    if "OMBUDSMAN" in stream or master_id.startswith("CAN-OMB-"):
        return "OMBUDSMAN_RECONSIDERATION"
    if "FISCAL" in stream or "-FIS-" in master_id:
        return "FISCALIA_INSTITUTIONAL_MEMORY"
    if (
        "AEAT" in stream
        or master_id.startswith("NAT-AEAT-")
        or master_id in {"MAD-AN-CONT-001", "MAD-AN-CONT-002"}
    ):
        return "TAX_CONTENTIOUS_CHAIN"
    if any(
        token in stream
        for token in ("CNMV", "SNCA", "TREASURY", "PUBLIC AID", "LAW 2/2023")
    ):
        return "REGULATORY_PUBLIC_ROUTE"
    if record_type == "PROFESSIONAL_DISCIPLINE":
        return "PROFESSIONAL_SUPERVISION"
    if record_type in {"ADMINISTRATIVE_FILE", "TRANSPARENCY_CLAIM"}:
        return "ADMIN_AUTHORITY_TITLE_SOURCE"
    if "CRIMINAL" in stream:
        return "CRIMINAL_FILE_DECISION"
    if "CIVIL" in stream or "INSOLVENCY" in stream:
        return "CIVIL_FILE_DECISION"
    if any(
        token in stream
        for token in (
            "ADMINISTRATIVE",
            "TOURISM",
            "MUNICIPAL",
            "TRANSPARENCY",
            "JUDICIAL GOVERNANCE",
        )
    ):
        return "ADMIN_AUTHORITY_TITLE_SOURCE"
    if "PROFESSIONAL" in stream:
        return "PROFESSIONAL_SUPERVISION"
    return "GENERAL_EXACT_FILE_DECISION_TEST"


def require_pr1235_live_migration(
    migration: dict,
    target: str,
    label: str,
    *,
    dependent_targets: list[str] | None = None,
) -> None:
    require(migration.get("target") == target, f"{label} target changed")
    if dependent_targets is not None:
        require(migration.get("dependent_targets") == dependent_targets, f"{label} dependent targets changed")
    require(migration.get("state") == "LIVE_VERIFIED", f"{label} is not LIVE_VERIFIED")
    require(migration.get("pull_request") == 1235, f"{label} PR changed")
    require(migration.get("reviewed_head_sha") == "40ccc3c699bcc1147a9ac65a52e93fec240633ce", f"{label} reviewed head changed")
    require(migration.get("reviewed_tree_sha") == "c64ae7547fed024ad0e82397f09fc5f61e2f5da7", f"{label} reviewed tree changed")
    require(migration.get("merge_sha") == "e13652bb8b3f51dd050c431a58e2bd70b83f5676", f"{label} merge SHA changed")
    require(migration.get("merge_tree_sha") == "c64ae7547fed024ad0e82397f09fc5f61e2f5da7", f"{label} merge tree changed")
    require(migration.get("pages_run_id") == 33342771113 and migration.get("pages_run_number") == 1314, f"{label} Pages evidence changed")
    require(migration.get("live_readback") == "PASS_16_OF_16_INTENDED_CRITICAL_RESOURCES", f"{label} live readback changed")
    require(
        migration.get("controlling_manifest")
        == "publication-manifests/all-proceedings-interlinkability-20260830.json",
        f"{label} controlling manifest changed",
    )


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def canonical_ids_in(value: str, candidates: set[str]) -> set[str]:
    """Return delimiter-safe canonical IDs named by one public field."""
    text = str(value or "")
    return {
        master_id
        for master_id in candidates
        if re.search(
            rf"(?<![A-Z0-9-]){re.escape(master_id)}(?![A-Z0-9-])",
            text,
            flags=re.IGNORECASE,
        )
    }


for relative in REQUIRED:
    require((ROOT / relative).is_file(), f"missing required file: {relative}")

if not errors:
    en, es = read("en/proceedings-map/index.html"), read("es/mapa-procedimientos/index.html")
    en_master, es_master = read("en/master-proceedings-register/index.html"), read("es/registro-maestro-procedimientos/index.html")
    en_clean = read("en/public-authority-unitary-case-reconstruction/index.html")
    es_clean = read("es/reconstruccion-unitaria-autoridades-publicas/index.html")
    institutional_feeders = {
        "EN Calificación": (read("en/calificacion-rpl-2523-evidence-map/index.html"), ("GC-APP-004",)),
        "ES Calificación": (read("es/calificacion-rpl-2523-mapa-prueba/index.html"), ("GC-APP-004",)),
        "EN AC": (read("en/insolvency-36-2012-administrator-removal-fees/index.html"), ("GC-APP-005", "GC-APP-006", "GC-APP-028")),
        "ES AC": (read("es/concurso-36-2012-separacion-ac-honorarios/index.html"), ("GC-APP-005", "GC-APP-006", "GC-APP-028")),
        "EN Fiscalía": (read("en/fiscalia-dip-2-2026/index.html"), ("GC-FIS-017",)),
        "ES Fiscalía": (read("es/fiscalia-dip-2-2026/index.html"), ("GC-FIS-017",)),
        "EN AP section 4": (read("en/insolvency-36-2012-ap-section-4/index.html"), ("GC-APP-004",)),
        "ES AP sección 4": (read("es/concurso-36-2012-ap-seccion-4/index.html"), ("GC-APP-004",)),
        "EN parallel lives": (read("en/insolvency-classification-parallel-lives/index.html"), ("GC-APP-004",)),
        "ES vidas paralelas": (read("es/calificacion-concurso-36-2012-vidas-paralelas/index.html"), ("GC-APP-004",)),
    }
    general_institutional_feeders = {
        "EN AC profile": read("en/insolvency-36-2012-insolvency-administrator/index.html"),
        "ES perfil AC": read("es/concurso-36-2012-administrador-concursal/index.html"),
        "EN Fiscalía inspection": read("en/public-prosecution-inspection-exp-gub-745-2026/index.html"),
        "ES Inspección Fiscalía": read("es/fiscalia-inspeccion-exp-gub-745-2026/index.html"),
    }
    js, css = read("assets/proceedings-interconnectivity-map-20260830.js"), read("assets/proceedings-interconnectivity-map-20260830.css")
    master_js = read("assets/master-proceedings-publication-20260830.js")
    gov = read(".github/governance/UNITARY_PROCEEDINGS_INTERCONNECTIVITY_MAP_PROTOCOL_30AUG2026.md")
    ascan = read(".github/governance/A_SCAN_360_CASE_PRISM_AND_READER_LENS_PROTOCOL_30AUG2026.md")
    anti = read("archive/PROCEEDINGS_ANTI_FRAGMENTATION_CONVERGENCE_RULE_30AUG2026.md")
    institutional = read("archive/INSTITUTIONAL_READER_UNITARY_PROCEEDINGS_RULE_30AUG2026.md")
    val_gap = read("archive/CAIXABANK_VALENCIA_01859_2023_REGISTRATION_GAP_30AUG2026.md")
    val_overlay = read("archive/PROCEEDINGS_MASTER_REGISTER_VALENCIA_1859_2023_OVERLAY_30AUG2026.md")
    gc_548_control = read("archive/GC_548_2023_PLAZA2_T1_CARET_CONTINUITY_CONTROL_30AUG2026.md")
    lz_4009_control = read("archive/ARRECIFE_4009_2015_CARET_INTERLINK_CONTROL_30AUG2026.md")
    missing_evidence = read("archive/MISSING_EVIDENCE_REGISTER.md")
    dp_control = read("archive/knowledge-project/DP1956_STATUS_REOPENING_CORRECTION_18AUG2026.md")
    builder = read("scripts/build_proceedings_case_prism_v2.py")
    workflow = read(".github/workflows/audit-proceedings-interconnectivity-map.yml")
    schema = json.loads(read("assets/data/proceedings-interconnectivity-schema-v1.json"))
    prism = json.loads(read("assets/data/proceedings-case-prism-v1.json"))
    public_projection = json.loads(read("assets/data/proceedings-master-public-v1.json"))
    interlinkability = json.loads(read("assets/data/proceedings-interlinkability-v1.json"))
    require(
        interlinkability.get("schema_version") == "1.1.0",
        "interlinkability public asset schema must be 1.1.0",
    )
    fiscalia_responses = json.loads(read("assets/data/fiscalia-response-correspondence.json"))
    treasury_control = json.loads(read("assets/data/treasury-transparency-7-2026-v1.json"))
    treasury_manifest = json.loads(read("publication-manifests/treasury-transparency-7-2026-20260830.json"))
    lifecycle = json.loads(read("publication-manifests/all-proceedings-interlinkability-20260830.json"))
    current_lifecycle = json.loads(read("publication-manifests/case-prism-substantive-gap-closure-20260831.json"))
    current_continuity = read(
        "docs/deletion-audits/2026-08-31-case-prism-substantive-gap-closure-continuity.md"
    )
    counsel_gaps = json.loads(read("assets/data/counsel-procurador-gap-register-v1.json"))
    gc_548_manifest = json.loads(read("publication-manifests/gc-548-2023-plaza2-t1-caret-20260830.json"))
    lz_1304_manifest = json.loads(read("publication-manifests/arrecife-1304-2014-identity-interlink-20260830.json"))
    master_publication_manifest = json.loads(read("publication-manifests/master-proceedings-publication-20260830.json"))
    lz_4009_manifest = json.loads(read("publication-manifests/arrecife-4009-2015-caret-interlink-20260830.json"))
    interlink_builder = read("scripts/build_proceedings_interlinkability_v1.py")
    with (ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    ids = [row["Master_ID"].strip() for row in rows]
    by_id = {row["Master_ID"].strip(): row for row in rows}
    public_rows = public_projection.get("records", [])
    public_ids = [row.get("Master_ID", "").strip() for row in public_rows]
    public_by_id = {row.get("Master_ID", "").strip(): row for row in public_rows}
    exact_public_rows = [row for row in public_rows if row.get("Is_Proceeding", "").strip().upper() == "TRUE"]
    exact_public_ids = {row.get("Master_ID", "").strip() for row in exact_public_rows}
    require(
        len(rows) == CURRENT_CANONICAL_RECORDS,
        f"canonical denominator: expected {CURRENT_CANONICAL_RECORDS}, found {len(rows)}",
    )
    require(len(ids) == len(set(ids)), "duplicate canonical Master_ID")
    require(public_projection.get("canonical_source_id") == "PROCEEDINGS_MASTER_REGISTER", "public projection canonical source identity changed")
    require(public_projection.get("derivation") == "DETERMINISTIC_ALLOWLIST", "public projection derivation is not allowlisted")
    require(
        public_projection.get("canonical_source_sha256")
        == hashlib.sha256((ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv").read_bytes()).hexdigest(),
        "public projection canonical-source digest mismatch",
    )
    require(public_projection.get("source_record_count") == len(rows), "public projection source denominator mismatch")
    require(public_projection.get("public_record_count") == len(public_rows), "public projection public denominator mismatch")
    require(len(public_ids) == len(set(public_ids)), "duplicate public-projection Master_ID")
    require(set(public_ids) <= set(ids), "public projection contains a non-canonical Master_ID")
    require(
        len(public_rows) == CURRENT_PUBLIC_RECORDS,
        f"public denominator: expected {CURRENT_PUBLIC_RECORDS}, found {len(public_rows)}",
    )

    # A bare user-supplied reference stays discoverable without receiving a caret
    # or a manufactured direct procedural edge.
    arrecife_1304 = by_id.get("LZ-REF-044", {})
    require(arrecife_1304.get("Record_Type") == "UNRESOLVED_REFERENCE", "LZ-REF-044 must remain an unresolved-reference object")
    require(arrecife_1304.get("Is_Proceeding") == "UNVERIFIED", "LZ-REF-044 must not receive a proceeding caret without primary identity proof")
    require(arrecife_1304.get("Reference") == "1304/2014", "LZ-REF-044 reference drift")
    require(arrecife_1304.get("Proceeding_Class") == "REGISTERED_ONLY", "LZ-REF-044 class must remain registered-only")
    require(arrecife_1304.get("Parent_Master_ID") == "" and arrecife_1304.get("Linked_Proceedings") == "" and arrecife_1304.get("Appeal_or_Review") == "", "LZ-REF-044 contains an unsupported direct procedural edge")
    require(arrecife_1304.get("Source_Status") == "USER_SUPPLIED_REFERENCE_PRIMARY_NOT_LOCATED", "LZ-REF-044 source boundary drift")
    require(arrecife_1304.get("Public_Treatment") == "PUBLIC_SUMMARY_WITH_IDENTITY_GAP", "LZ-REF-044 public identity-gap treatment missing")
    require("Signed/certified court source" in arrecife_1304.get("Open_Reference_Gap", ""), "LZ-REF-044 finite source request missing")
    require("No CAEPR proceeding admission or caret" in arrecife_1304.get("Notes", ""), "LZ-REF-044 caret-withholding control missing")
    require("| ME-114 |" in missing_evidence and "`1304/2014`" in missing_evidence, "LZ-REF-044 missing-evidence control ME-114 missing")
    lz_1304_migration = lz_1304_manifest.get("projection_migration", {})
    require(lz_1304_manifest.get("current_state") == "DELETION_SAFE" and lz_1304_manifest.get("state") == "DELETION_SAFE_LIVE_VERIFIED_WITH_OPEN_IDENTITY_EVIDENCE", "LZ-REF-044 historical live/deletion-safe lifecycle changed")
    require_pr1235_live_migration(
        lz_1304_migration,
        "assets/data/proceedings-master-public-v1.json",
        "LZ-REF-044 allowlisted-projection migration",
    )
    public_field_allowlist = set(public_projection.get("field_allowlist", []))
    forbidden_public_fields = {
        "Primary_Source_Anchor", "Repo_Canonical_Source", "Notes",
        "Public_Treatment", "Last_Scan_Date",
    }
    require(public_field_allowlist and not (public_field_allowlist & forbidden_public_fields), "public projection field allowlist admits a private/operational field")
    require(
        all(set(row) == public_field_allowlist for row in public_rows),
        "public projection records do not exactly match the field allowlist",
    )

    # An exact-proceeding denominator may never admit a synthetic family or
    # aggregate continuity object.  Such objects remain useful public nodes,
    # but they are not selectable as an exact file.
    for row in exact_public_rows:
        aggregate_markers = " ".join(
            (row.get("Record_Type", ""), row.get("Proceeding_Class", ""))
        ).upper()
        require(
            not any(marker in aggregate_markers for marker in ("FAMILY", "AGGREGATE")),
            f"aggregate/family object admitted as exact proceeding: {row.get('Master_ID')}",
        )

    # Complete exact-proceeding interlinkability denominator.  The canonical
    # source retains one excluded private exact file; neither its ID nor its
    # details may leak into the public registry.  Every one of the current public
    # exact files must then receive one controlled disposition.
    canonical_exact_ids = {
        row["Master_ID"].strip()
        for row in rows
        if row.get("Is_Proceeding", "").strip().upper() == "TRUE"
    }
    private_exact_ids = canonical_exact_ids - exact_public_ids
    require(
        len(canonical_exact_ids) == CURRENT_CANONICAL_EXACT,
        "canonical exact-proceeding denominator: expected "
        f"{CURRENT_CANONICAL_EXACT}, found {len(canonical_exact_ids)}",
    )
    require(
        len(exact_public_ids) == CURRENT_PUBLIC_EXACT,
        "public exact-proceeding denominator: expected "
        f"{CURRENT_PUBLIC_EXACT}, found {len(exact_public_ids)}",
    )
    require(
        len(private_exact_ids) == CURRENT_PRIVATE_EXACT,
        "private exact-proceeding exclusion denominator must be one",
    )
    interlink_serialised = json.dumps(interlinkability, ensure_ascii=False)
    require(not any(private_id in interlink_serialised for private_id in private_exact_ids), "private exact proceeding leaked into public interlinkability registry")
    require("archive/PROCEEDINGS_MASTER_REGISTER.csv" not in interlink_serialised, "public interlinkability registry exposes the operational canonical path")
    require(interlinkability.get("canonical_node_source_id") == "PROCEEDINGS_MASTER_REGISTER", "interlinkability canonical source identity changed")
    require(interlinkability.get("control_date") == "2026-08-31", "interlinkability control date is stale")
    require(interlinkability.get("public_node_projection") == "assets/data/proceedings-master-public-v1.json", "interlinkability public projection changed")
    require(interlinkability.get("case_prism_source") == "assets/data/proceedings-case-prism-v1.json", "interlinkability Case Prism source changed")
    require(
        "joinder" in interlinkability.get("boundary_en", "").lower()
        and "acumul" in interlinkability.get("boundary_es", "").lower(),
        "interlinkability boundary is not bilingual or omits anti-joinder language",
    )

    scope = interlinkability.get("scope", {})
    scope_ids = scope.get("public_exact_proceeding_ids", [])
    require(
        scope.get("expected_count") == len(exact_public_ids) == CURRENT_PUBLIC_EXACT,
        "interlinkability scope denominator mismatch",
    )
    require(scope_ids == [row["Master_ID"] for row in exact_public_rows], "interlinkability scope does not exactly follow the public projection")
    require(set(scope.get("excluded_aggregate_reference_ids", [])) == {"GC-APP-007"}, "aggregate appeal-family exclusion not explicit")
    navigation_contract = interlinkability.get("navigation_contract", {})
    require(navigation_contract.get("exact_id_to_master_register") == "REQUIRED", "exact-ID Master Register navigation is not required")
    require(navigation_contract.get("exact_id_to_renderer") == "REQUIRED", "exact-ID renderer navigation is not required")
    require(navigation_contract.get("dossier_route_relationship") == "NOT_INFERRED", "registry overclaims a complete exact-ID dossier relationship")
    require(navigation_contract.get("en") and navigation_contract.get("es"), "interlinkability navigation contract is not bilingual")
    aggregate = public_by_id.get("GC-APP-007", {})
    require(aggregate.get("Is_Proceeding") == "FALSE", "GC-APP-007 remains selectable as an exact proceeding")
    require(aggregate.get("Record_Type") == "APPEAL_FAMILY_REFERENCE", "GC-APP-007 record type is not an aggregate reference")
    require(aggregate.get("Proceeding_Class") == "AGGREGATE_REFERENCE_NOT_PROCEEDING", "GC-APP-007 proceeding class is not an aggregate reference")

    classifications = {
        "DIRECT_PROCEDURAL_EDGE", "CONTROLLED_CONTEXTUAL_BRIDGE",
        "INDEPENDENT_TRACK", "EXPLICIT_RELATIONSHIP_GAP",
    }
    classification_catalog = interlinkability.get("classification_catalog", {})
    require(set(classification_catalog) == classifications, "interlinkability classification vocabulary mismatch")
    require(all(meta.get("en") and meta.get("es") for meta in classification_catalog.values()), "interlinkability classifications are not bilingual")
    for catalog_name in ("relationship_type_catalog", "context_type_catalog"):
        catalog = interlinkability.get(catalog_name, {})
        require(catalog and all(meta.get("en") and meta.get("es") for meta in catalog.values()), f"{catalog_name} is not bilingual")
    finite_family_catalog = interlinkability.get("finite_test_family_catalog", {})
    receipt_status_catalog = interlinkability.get("receipt_knowledge_status_catalog", {})
    require(
        finite_family_catalog
        and all(meta.get("en") and meta.get("es") for meta in finite_family_catalog.values()),
        "finite-test family catalog is absent or not bilingual",
    )
    require(
        receipt_status_catalog
        and all(meta.get("en") and meta.get("es") for meta in receipt_status_catalog.values()),
        "receipt/knowledge status catalog is absent or not bilingual",
    )
    finite_contract = interlinkability.get("finite_test_contract", {})
    require(
        finite_contract.get("status") == "COMPLETE_FOR_PUBLIC_EXACT_DENOMINATOR"
        and finite_contract.get("family_taxonomy_effect")
        == "UI_ONLY_NO_EDGE_OR_CLUSTER_EFFECT"
        and finite_contract.get("family_assignment_rule")
        == "CANONICAL_RECORD_TYPE_BEFORE_MIXED_STREAM_SUBSTRING"
        and finite_contract.get("recorded_candidate_authority_status")
        == "NOT_COMPETENCE_OR_DUTY"
        and finite_contract.get("boundary_en")
        and finite_contract.get("boundary_es"),
        "finite-test model contract is incomplete or can alter relationship truth",
    )
    require(
        finite_contract.get("required_sequence")
        == [
            "QUESTION",
            "SOURCE_NEEDED",
            "CURRENT_SOURCE_STATUS",
            "COMPETENT_ORGAN",
            "RELATED_PROCEEDINGS",
            "PROCEDURAL_AVAILABILITY",
            "DECISION_DEPENDENCY",
            "STRONGEST_CONTRARY_EXPLANATION",
            "CONSEQUENCE_IF_CONFIRMED",
            "CONSEQUENCE_IF_REFUTED",
        ],
        "finite-test actionability sequence is incomplete or reordered",
    )
    receipt_contract = interlinkability.get("receipt_knowledge_contract", {})
    require(
        set(receipt_contract.get("institutional_axis_ids", []))
        == INSTITUTIONAL_RECEIPT_AXES
        and receipt_contract.get("public_renderer_axis_ids")
        == PUBLIC_RENDERER_RECEIPT_AXES
        and receipt_contract.get("public_renderer_axis_status_locations")
        == PUBLIC_RENDERER_AXIS_STATUS_LOCATIONS
        and receipt_contract.get("public_renderer_axis_provenance_requirement")
        == "FAIL_CLOSED_STATUS_BILINGUAL_BASIS_LIMITATION_AND_SOURCE"
        and receipt_contract.get("cross_file_acknowledgement_is_separate") is True
        and receipt_contract.get("institutional_axis_basis_required") is True
        and receipt_contract.get("positive_axis_source_field_rule")
        == "EXACT_EPISODE_FIELD_MUST_SUPPORT_AXIS_GRADE"
        and set(receipt_contract.get("institutional_axis_basis_fields", []))
        == {
            "status",
            "basis_kind",
            "basis_en",
            "basis_es",
            "limitation_en",
            "limitation_es",
            "source",
        }
        and receipt_contract.get("actor_specific_status_is_separate") is True
        and receipt_contract.get("raw_matter_reference_join") == "PROHIBITED"
        and receipt_contract.get("boundary_en")
        and receipt_contract.get("boundary_es"),
        "receipt/knowledge contract does not keep the six core axes, nine-axis public renderer and actor evidence separate",
    )
    require(
        all(
            token in receipt_contract.get("boundary_en", "")
            for token in ("material received", "referral", "cross-file acknowledgement")
        )
        and all(
            token in receipt_contract.get("boundary_es", "")
            for token in ("material recibido", "remisión", "reconocimiento entre expedientes")
        ),
        "receipt/knowledge contract boundary does not enumerate all nine public institutional grades",
    )
    fiscalia_matrix_contract = interlinkability.get(
        "fiscalia_office_file_matrix_contract", {}
    )
    require(
        fiscalia_matrix_contract.get("row_denominator")
        == CURRENT_FISCALIA_OFFICE_FILE_RECORDS
        and set(
            fiscalia_matrix_contract.get("required_independent_status_axes", [])
        )
        == FISCALIA_MATRIX_AXES
        and fiscalia_matrix_contract.get("referral_is_not_transmission") is True
        and fiscalia_matrix_contract.get("direct_context_and_assets_are_separate")
        is True
        and fiscalia_matrix_contract.get("material_summary_is_not_received_inventory")
        is True
        and fiscalia_matrix_contract.get("axis_provenance_required") is True,
        "Fiscalía matrix contract does not require the substantive independent columns",
    )

    relationships = interlinkability.get("relationships", [])
    relationship_ids = [relationship.get("id") for relationship in relationships]
    relationship_by_id = {relationship.get("id"): relationship for relationship in relationships}
    require(len(relationship_ids) == len(set(relationship_ids)), "duplicate controlled relationship ID")
    expected_direct_pairs: set[tuple[str, str]] = set()
    for row in exact_public_rows:
        source_id = row["Master_ID"]
        parent_id = row.get("Parent_Master_ID", "").strip()
        if parent_id in exact_public_ids and parent_id != source_id:
            expected_direct_pairs.add(tuple(sorted((source_id, parent_id))))
        for field in ("Linked_Proceedings", "Appeal_or_Review"):
            for target_id in canonical_ids_in(row.get(field, ""), exact_public_ids):
                if target_id != source_id:
                    expected_direct_pairs.add(tuple(sorted((source_id, target_id))))
    actual_direct_pairs = {
        tuple(sorted((relationship.get("from_master_id", ""), relationship.get("to_master_id", ""))))
        for relationship in relationships
    }
    require(len(actual_direct_pairs) == len(relationships), "multiple direct relationships silently compete for one exact-proceeding pair")
    require(actual_direct_pairs == expected_direct_pairs, "controlled direct-edge registry omits or invents an exact canonical relationship pair")
    expected_treasury_pair = tuple(sorted(("NAT-TES-001", "X-WB-005")))
    contextual_only_treasury_pairs = {
        tuple(sorted(("NAT-TES-001", related_id)))
        for related_id in ("LZ-TRA-028", "NAT-AID-001")
    }
    require(
        expected_treasury_pair in expected_direct_pairs,
        "Treasury 7/2026 documented X-WB-005 routing lineage is missing",
    )
    require(
        not (contextual_only_treasury_pairs & expected_direct_pairs),
        "Treasury 7/2026 contextual lanes were promoted into direct procedural pairs",
    )
    direct_field_by_type = {
        "PARENT_CHILD": "Parent_Master_ID",
        "LINKED_PROCEEDING": "Linked_Proceedings",
        "APPEAL_REVIEW_ID_LINK": "Appeal_or_Review",
    }
    assertion_fields = (
        "source_id", "source_record_master_id", "field", "value_token",
        "evidence_status", "assertion_relationship_type", "assertion_direction",
        "assertion_from_master_id", "assertion_to_master_id",
    )
    expected_source_assertions = []
    for source_row in exact_public_rows:
        source_id = source_row["Master_ID"]
        parent_id = source_row.get("Parent_Master_ID", "").strip()
        if parent_id in exact_public_ids and parent_id != source_id:
            expected_source_assertions.append(
                (
                    "PROCEEDINGS_MASTER_REGISTER", source_id, "Parent_Master_ID",
                    parent_id, source_row.get("Source_Status", ""), "PARENT_CHILD",
                    "FORWARD", parent_id, source_id,
                )
            )
        for field, relationship_type in (
            ("Linked_Proceedings", "LINKED_PROCEEDING"),
            ("Appeal_or_Review", "APPEAL_REVIEW_ID_LINK"),
        ):
            for target_id in sorted(canonical_ids_in(source_row.get(field, ""), exact_public_ids)):
                if target_id != source_id:
                    expected_source_assertions.append(
                        (
                            "PROCEEDINGS_MASTER_REGISTER", source_id, field, target_id,
                            source_row.get("Source_Status", ""), relationship_type,
                            "FORWARD", source_id, target_id,
                        )
                    )
    actual_source_assertions = []
    for relationship in relationships:
        rid = relationship.get("id", "<missing relationship ID>")
        source = relationship.get("source", {})
        from_id, to_id = relationship.get("from_master_id"), relationship.get("to_master_id")
        require(from_id in exact_public_ids and to_id in exact_public_ids and from_id != to_id, f"{rid} has a non-exact/private/self endpoint")
        require(relationship.get("relationship_class") == "DIRECT_PROCEDURAL_EDGE", f"{rid} is not a controlled direct edge")
        require(relationship.get("relationship_type") in direct_field_by_type, f"{rid} has an unsupported direct-edge type")
        require(relationship.get("direction") in {"FORWARD", "REVERSE_DERIVED", "BIDIRECTIONAL", "ONE_WAY"}, f"{rid} has an invalid direction")
        require(relationship.get("why_en") and relationship.get("why_es"), f"{rid} lacks bilingual why-connected text")
        require("joinder" in relationship.get("limitations_en", "").lower() and "acumul" in relationship.get("limitations_es", "").lower(), f"{rid} lacks bilingual anti-joinder limitations")
        require(relationship.get("public_safe") is True, f"{rid} is not explicitly public-safe")
        source_record_id = source.get("record_master_id")
        source_field = source.get("field")
        source_token = source.get("value_token")
        require(source.get("kind") == "MASTER_REGISTER_FIELD" and source.get("source_id") == "PROCEEDINGS_MASTER_REGISTER", f"{rid} lacks canonical-field provenance")
        require(source_field == direct_field_by_type.get(relationship.get("relationship_type")), f"{rid} source field does not match relationship type")
        source_row = by_id.get(source_record_id, {})
        require(source_record_id in {from_id, to_id} and source_token in {from_id, to_id} - {source_record_id}, f"{rid} source record/token do not match its endpoints")
        require(source_token and source_token in source_row.get(source_field, ""), f"{rid} is not supported by its claimed canonical field")
        source_assertions = relationship.get("source_assertions", [])
        require(relationship.get("supporting_assertion_count") == len(source_assertions) >= 1, f"{rid} supporting assertion count mismatch")
        for assertion in source_assertions:
            assertion_tuple = tuple(assertion.get(field) for field in assertion_fields)
            actual_source_assertions.append(assertion_tuple)
            require(
                {assertion.get("assertion_from_master_id"), assertion.get("assertion_to_master_id")}
                == {from_id, to_id},
                f"{rid} contains a source assertion for a different pair",
            )
    require(
        len(expected_source_assertions) == CURRENT_DIRECT_ASSERTIONS,
        "expected "
        f"{CURRENT_DIRECT_ASSERTIONS} canonical direct assertions, "
        f"found {len(expected_source_assertions)}",
    )
    require(
        Counter(actual_source_assertions) == Counter(expected_source_assertions),
        "direct relationship source assertions do not exactly preserve the canonical-field assertion multiset",
    )
    source_verified_statuses = {"VERIFIED_PRIMARY", "VERIFIED_PRIMARY_COPY", "VERIFIED_PROCEDURAL"}
    source_verified_pair_count = sum(
        all(
            assertion.get("evidence_status") in source_verified_statuses
            for assertion in relationship.get("source_assertions", [])
        )
        for relationship in relationships
    )
    source_reported_pending_pair_count = len(relationships) - source_verified_pair_count
    source_verified_assertion_count = sum(
        assertion[4] in source_verified_statuses
        for assertion in actual_source_assertions
    )
    source_reported_pending_assertion_count = (
        len(actual_source_assertions) - source_verified_assertion_count
    )
    require(
        (source_verified_pair_count, source_reported_pending_pair_count)
        == (CURRENT_VERIFIED_DIRECT_PAIRS, CURRENT_PENDING_DIRECT_PAIRS),
        "direct-pair source grades must remain explicit at "
        f"{CURRENT_VERIFIED_DIRECT_PAIRS} verified / "
        f"{CURRENT_PENDING_DIRECT_PAIRS} reported-primary-pending",
    )
    require(
        (source_verified_assertion_count, source_reported_pending_assertion_count)
        == (CURRENT_VERIFIED_DIRECT_ASSERTIONS, CURRENT_PENDING_DIRECT_ASSERTIONS),
        "direct-assertion source grades must remain explicit at "
        f"{CURRENT_VERIFIED_DIRECT_ASSERTIONS} verified / "
        f"{CURRENT_PENDING_DIRECT_ASSERTIONS} reported-primary-pending",
    )

    context_clusters = interlinkability.get("context_clusters", [])
    context_ids = [cluster.get("id") for cluster in context_clusters]
    context_by_id = {cluster.get("id"): cluster for cluster in context_clusters}
    require(len(context_ids) == len(set(context_ids)), "duplicate context-cluster ID")
    permitted_context_types = {"RECORDED_CONNECTION", "SOURCE_CONTROLLED_CORRIDOR", "CASE_PRISM_PROPOSITION"}
    require(set(interlinkability.get("context_type_catalog", {})) == permitted_context_types, "context catalog admits a taxonomy-only or unknown bridge")
    prism_prop_by_id = {prop.get("id"): prop for prop in prism.get("propositions", [])}
    expected_connection_groups: dict[str, set[str]] = {}
    for row in exact_public_rows:
        connection = row.get("Connection", "").strip()
        if connection:
            expected_connection_groups.setdefault(connection, set()).add(row["Master_ID"])
    expected_connection_groups = {
        connection: members
        for connection, members in expected_connection_groups.items()
        if len(members) >= 2
    }
    actual_connection_groups = {
        cluster.get("source", {}).get("value"): set(cluster.get("member_master_ids", []))
        for cluster in context_clusters
        if cluster.get("context_type") == "RECORDED_CONNECTION"
    }
    require(actual_connection_groups == expected_connection_groups, "recorded-Connection clusters omit or invent an exact public member group")

    expected_prism_groups: dict[str, set[str]] = {}
    for prop in prism.get("propositions", []):
        members = {
            mid
            for cell in prop.get("cells", {}).values()
            if cell.get("status") != "OUTSIDE"
            for mid in cell.get("master_ids", [])
            if mid in exact_public_ids
        }
        if len(members) >= 2:
            expected_prism_groups[prop.get("id")] = members
    actual_prism_groups = {
        cluster.get("source", {}).get("record_id"): set(cluster.get("member_master_ids", []))
        for cluster in context_clusters
        if cluster.get("context_type") == "CASE_PRISM_PROPOSITION"
    }
    require(actual_prism_groups == expected_prism_groups, "Case Prism context clusters omit or invent a proposition-member group")
    expected_source_corridors = {
        corridor.get("id"): set(corridor.get("member_master_ids", []))
        for corridor in treasury_control.get("proceedings_context_corridors", [])
    }
    actual_source_corridors = {
        cluster.get("source", {}).get("record_id"): set(cluster.get("member_master_ids", []))
        for cluster in context_clusters
        if cluster.get("context_type") == "SOURCE_CONTROLLED_CORRIDOR"
    }
    require(actual_source_corridors == expected_source_corridors == {"T7-COR-001": {"NAT-TES-001", "LZ-TRA-028"}}, "source-controlled Treasury corridor mismatch")
    treasury_migration = treasury_manifest.get("projection_migration", {})
    require_pr1235_live_migration(
        treasury_migration,
        "assets/data/proceedings-interlinkability-v1.json",
        "Treasury PR #1235 interlinkability migration",
        dependent_targets=[
            "assets/data/proceedings-master-public-v1.json",
            "assets/data/proceedings-case-prism-v1.json",
        ],
    )
    require(
        treasury_manifest.get("content_publication", {}).get("pull_request") == 1247
        and treasury_manifest.get("content_publication", {}).get("merge_sha")
        == "5939ed3badad20193a4aba05ca62047d6bc6ff89"
        and treasury_migration.get("merge_sha")
        == "e13652bb8b3f51dd050c431a58e2bd70b83f5676",
        "Treasury PR #1247 source publication and PR #1235 projection migration are not kept distinct",
    )
    for cluster in context_clusters:
        cid = cluster.get("id", "<missing context ID>")
        context_type = cluster.get("context_type")
        members = cluster.get("member_master_ids", [])
        source = cluster.get("source", {})
        require(context_type in permitted_context_types, f"{cid} has an unapproved context type")
        require(len(members) >= 2 and len(members) == len(set(members)) and set(members) <= exact_public_ids, f"{cid} has invalid context members")
        require(cluster.get("label_en") and cluster.get("label_es") and cluster.get("why_en") and cluster.get("why_es"), f"{cid} lacks bilingual reader text")
        limitations_en = cluster.get("limitations_en", "").lower()
        limitations_es = cluster.get("limitations_es", "").lower()
        require(limitations_en and limitations_es, f"{cid} lacks bilingual limitations")
        require(cluster.get("public_safe") is True, f"{cid} is not explicitly public-safe")
        if context_type == "RECORDED_CONNECTION":
            expected_field = "Connection"
            require(source.get("kind") == "MASTER_REGISTER_FIELD_GROUP" and source.get("source_id") == "PROCEEDINGS_MASTER_REGISTER", f"{cid} lacks canonical-group provenance")
            require(source.get("field") == expected_field and source.get("value"), f"{cid} source field/value mismatch")
            require(all(public_by_id[mid].get(expected_field) == source.get("value") for mid in members), f"{cid} invents a canonical-field grouping")
            require({item.get("master_id") for item in source.get("member_provenance", [])} == set(members), f"{cid} member provenance mismatch")
            require("joinder" in limitations_en and "acumul" in limitations_es, f"{cid} lacks bilingual anti-joinder limits")
        elif context_type == "CASE_PRISM_PROPOSITION":
            prop_id = source.get("record_id")
            prop = prism_prop_by_id.get(prop_id, {})
            admitted_members = {
                mid
                for cell in prop.get("cells", {}).values()
                if cell.get("status") != "OUTSIDE"
                for mid in cell.get("master_ids", [])
                if mid in exact_public_ids
            }
            require(source.get("kind") == "CASE_PRISM_PROPOSITION_MEMBERSHIP", f"{cid} lacks Case Prism provenance")
            require(source.get("path") == "assets/data/proceedings-case-prism-v1.json" and prop_id in prism_prop_by_id, f"{cid} references an unknown Case Prism proposition")
            require(set(members) == admitted_members, f"{cid} membership does not match its Case Prism proposition")
            require("do not prove receipt or treatment" in limitations_en and "no prueban recepción ni tratamiento" in limitations_es, f"{cid} does not preserve the proposition/file-treatment boundary")
        else:
            record_id = source.get("record_id")
            corridor = next(
                (item for item in treasury_control.get("proceedings_context_corridors", []) if item.get("id") == record_id),
                {},
            )
            require(source.get("kind") == "SPECIALIST_SOURCE_CONTEXT_CORRIDOR", f"{cid} lacks specialist-source corridor provenance")
            require(source.get("path") == "assets/data/treasury-transparency-7-2026-v1.json" and corridor, f"{cid} references an unknown specialist context corridor")
            require(set(members) == set(corridor.get("member_master_ids", [])), f"{cid} membership diverges from its specialist source control")
            require("no appeal" in limitations_en and "no acredita recurso" in limitations_es, f"{cid} does not preserve the direct/context boundary")

    dispositions = interlinkability.get("node_dispositions", [])
    disposition_ids = [disposition.get("master_id") for disposition in dispositions]
    require(len(disposition_ids) == len(set(disposition_ids)) and set(disposition_ids) == exact_public_ids, "every public exact proceeding must have exactly one controlled disposition")
    disposition_counts = Counter(disposition.get("primary_classification") for disposition in dispositions)
    finite_family_by_master = {
        disposition.get("master_id"): disposition.get("finite_test", {}).get(
            "family_template_id"
        )
        for disposition in dispositions
    }
    require(
        Counter(finite_family_by_master.values())
        == Counter(EXPECTED_FINITE_TEST_FAMILY_COUNTS),
        "finite-test family denominator no longer matches controlled record types/classes",
    )
    require(
        finite_family_by_master.get("GC-CIV-027") == "CIVIL_FILE_DECISION"
        and finite_family_by_master.get("LZ-CAB-011")
        == "ADMIN_AUTHORITY_TITLE_SOURCE"
        and finite_family_by_master.get("LZ-PRO-029")
        == "PROFESSIONAL_SUPERVISION"
        and finite_family_by_master.get("GC-GOV-019")
        == "ADMIN_AUTHORITY_TITLE_SOURCE"
        and finite_family_by_master.get("GC-GOV-020")
        == "ADMIN_AUTHORITY_TITLE_SOURCE",
        "finite-test family precedence misclassifies civil, administrative, professional or judicial-governance files",
    )
    finite_test_ids: list[str] = []
    finite_specific_values = {
        field: {"en": set(), "es": set()}
        for field in (
            "question",
            "decision_dependency",
            "contrary_explanation",
            "if_confirmed",
            "if_refuted",
        )
    }
    finite_source_route_payloads: set[str] = set()
    receipt_knowledge_classified_ids: set[str] = set()
    actor_positive_ids: set[str] = set()
    receipt_status_vocabulary = set(
        interlinkability.get("receipt_knowledge_status_catalog", {})
    )
    for disposition in dispositions:
        master_id = disposition.get("master_id", "<missing proceeding ID>")
        classification = disposition.get("primary_classification")
        direct_ids = disposition.get("relationship_ids", [])
        cluster_ids = disposition.get("context_cluster_ids", [])
        expected_disposition_relationship_ids = {
            relationship.get("id")
            for relationship in relationships
            if master_id in {
                relationship.get("from_master_id"), relationship.get("to_master_id")
            }
        }
        expected_disposition_cluster_ids = {
            cluster.get("id")
            for cluster in context_clusters
            if master_id in cluster.get("member_master_ids", [])
        }
        require(classification in classifications, f"{master_id} has an invalid interlink classification")
        require(disposition.get("why_en") and disposition.get("why_es"), f"{master_id} disposition lacks bilingual explanation")
        require("joinder" in disposition.get("limitations_en", "").lower() and "acumul" in disposition.get("limitations_es", "").lower(), f"{master_id} disposition lacks bilingual anti-joinder limitations")
        require(disposition.get("next_source_needed_en") and disposition.get("next_source_needed_es"), f"{master_id} disposition lacks a bilingual finite next-source test")
        require(disposition.get("next_source_needed_es") != "Revisar la fuente primaria indicada en Open_Reference_Gap antes de afirmar una relación adicional.", f"{master_id} disposition uses the generic Spanish next-source fallback")
        require(len(direct_ids) == len(set(direct_ids)) and set(direct_ids) == expected_disposition_relationship_ids, f"{master_id} disposition omits, duplicates or invents a direct relationship membership")
        require(len(cluster_ids) == len(set(cluster_ids)) and set(cluster_ids) == expected_disposition_cluster_ids, f"{master_id} disposition omits, duplicates or invents a material context-cluster membership")
        if public_by_id[master_id].get("Open_Reference_Gap", "").strip():
            require(disposition.get("next_source_needed_en") == public_by_id[master_id].get("Open_Reference_Gap"), f"{master_id} English next-source text diverges from the canonical finite request")
            require(
                disposition.get("next_source_needed_es")
                and disposition.get("next_source_needed_es")
                != "Revisar la fuente primaria indicada en Open_Reference_Gap antes de afirmar una relación adicional.",
                f"{master_id} uses a missing/generic Spanish next-source formulation",
            )
        require(all(rid in relationship_by_id and master_id in {relationship_by_id[rid].get("from_master_id"), relationship_by_id[rid].get("to_master_id")} for rid in direct_ids), f"{master_id} disposition has a foreign/unknown direct relationship")
        require(all(cid in context_by_id and master_id in context_by_id[cid].get("member_master_ids", []) for cid in cluster_ids), f"{master_id} disposition has a foreign/unknown context cluster")
        if classification == "DIRECT_PROCEDURAL_EDGE":
            require(bool(direct_ids) and disposition.get("basis", {}).get("kind") == "DIRECT_RELATIONSHIP_MEMBERSHIP", f"{master_id} direct classification lacks direct provenance")
        elif classification == "CONTROLLED_CONTEXTUAL_BRIDGE":
            require(not direct_ids and bool(cluster_ids) and disposition.get("basis", {}).get("kind") == "CONTEXT_CLUSTER_MEMBERSHIP", f"{master_id} context classification lacks controlled-cluster provenance")
        elif classification == "EXPLICIT_RELATIONSHIP_GAP":
            require(not direct_ids and not cluster_ids, f"{master_id} relationship gap fabricates a connection")
            require(disposition.get("next_source_needed_en") and disposition.get("next_source_needed_es"), f"{master_id} relationship gap lacks a bilingual next-source test")
            require(
                disposition.get("next_source_needed_es")
                != "Revisar la fuente primaria indicada en Open_Reference_Gap antes de afirmar una relación adicional.",
                f"{master_id} relationship gap uses the generic Spanish next-source fallback",
            )
            basis = disposition.get("basis", {})
            require(basis.get("kind") == "MASTER_REGISTER_FIELD" and basis.get("source_id") == "PROCEEDINGS_MASTER_REGISTER" and basis.get("field") == "Open_Reference_Gap", f"{master_id} relationship gap lacks canonical-field provenance")
            require(public_by_id[master_id].get("Open_Reference_Gap"), f"{master_id} relationship gap has no recorded source gap")
        else:
            require(not direct_ids and not cluster_ids and disposition.get("basis", {}).get("kind") == "NO_ADMITTED_RELATION_OR_GAP", f"{master_id} independent track fabricates a connection")

        # Exact-file actionability is a model-completeness denominator, not a
        # merits or positive-evidence denominator.  Every field is derived from
        # the same canonical row and the already audited one-hop registries.
        raw_finite_test = disposition.get("finite_test", {})
        finite_test = raw_finite_test if isinstance(raw_finite_test, dict) else {}
        finite_id = finite_test.get("id")
        finite_test_ids.append(finite_id)
        require(isinstance(raw_finite_test, dict), f"{master_id} lacks a finite_test object")
        require(finite_id == f"FT-{master_id}", f"{master_id} finite-test identity mismatch")
        for field in (
            "question",
            "source_needed",
            "procedural_availability",
            "decision_dependency",
            "contrary_explanation",
            "if_confirmed",
            "if_refuted",
        ):
            require_bilingual(finite_test.get(field), f"{master_id} finite_test.{field}")
            if field in finite_specific_values:
                finite_specific_values[field]["en"].add(
                    finite_test.get(field, {}).get("en")
                )
                finite_specific_values[field]["es"].add(
                    finite_test.get(field, {}).get("es")
                )
        canonical_row = public_by_id.get(master_id, {})
        expected_family = expected_finite_test_family(canonical_row)
        require(
            finite_test.get("family_template_id") == expected_family
            and finite_test.get("family_taxonomy_only") is True,
            f"{master_id} finite-test family misclassifies its record type/class/stream",
        )
        require(
            finite_test.get("current_source_status")
            == canonical_row.get("Source_Status"),
            f"{master_id} finite-test source status diverges from the canonical row",
        )
        require(
            finite_test.get("source_needed", {}).get("en")
            == canonical_row.get("Open_Reference_Gap"),
            f"{master_id} finite-test English source request diverges from Open_Reference_Gap",
        )
        require(
            finite_test.get("recorded_object")
            == canonical_row.get("Object_or_Purpose"),
            f"{master_id} finite-test recorded object diverges from the canonical row",
        )
        require(
            finite_test.get("status")
            and finite_test.get("family_template_id")
            and finite_test.get("family_taxonomy_only") is True
            and finite_test.get("attribution")
            and finite_test.get("source_needed_status"),
            f"{master_id} finite-test control metadata is incomplete",
        )
        require(
            isinstance(finite_test.get("source_refs"), list)
            and len(finite_test.get("source_refs")) == 2,
            f"{master_id} finite-test source-route state is absent",
        )
        source_refs = finite_test.get("source_refs", [])
        canonical_source_ref = next(
            (
                source
                for source in source_refs
                if source.get("kind") == "CANONICAL_PUBLIC_RECORD"
            ),
            {},
        )
        primary_route_gap = next(
            (
                source
                for source in source_refs
                if source.get("kind") == "PUBLIC_SOURCE_ROUTE_GAP"
            ),
            {},
        )
        require(
            canonical_source_ref.get("source_id") == master_id
            and canonical_source_ref.get("status")
            == "CANONICAL_METADATA_ONLY_NOT_PRIMARY_SOURCE"
            and canonical_source_ref.get("href_en")
            == f"en/master-proceedings-register/#record-{master_id}"
            and canonical_source_ref.get("href_es")
            == f"es/registro-maestro-procedimientos/#record-{master_id}"
            and canonical_source_ref.get("limitations_en")
            and canonical_source_ref.get("limitations_es")
            and primary_route_gap.get("status")
            == "PUBLIC_SOURCE_ROUTE_NOT_ESTABLISHED",
            f"{master_id} finite-test source routes conflate metadata with a primary file",
        )
        finite_source_route_payloads.add(
            json.dumps(source_refs, ensure_ascii=False, sort_keys=True)
        )
        competent_organ = finite_test.get("competent_organ", {})
        expected_organ = (
            canonical_row.get("Current_Custodian", "").strip()
            or canonical_row.get("Origin_Organ", "").strip()
        )
        expected_organ_basis = (
            "Current_Custodian"
            if canonical_row.get("Current_Custodian", "").strip()
            else "Origin_Organ"
        )
        require(
            competent_organ.get("recorded_candidate") == expected_organ
            and competent_organ.get("basis_field") == expected_organ_basis
            and competent_organ.get("status"),
            f"{master_id} finite-test competent-organ derivation is incomplete or stale",
        )

        expected_direct_master_ids = sorted(
            {
                relationship_by_id[rid].get("to_master_id")
                if relationship_by_id[rid].get("from_master_id") == master_id
                else relationship_by_id[rid].get("from_master_id")
                for rid in direct_ids
            }
        )
        expected_context_master_ids = sorted(
            {
                related_id
                for cid in cluster_ids
                for related_id in context_by_id[cid].get("member_master_ids", [])
                if related_id != master_id
            }
        )
        finite_related = finite_test.get("related_proceedings", {})
        require(
            finite_related.get("direct_master_ids") == expected_direct_master_ids
            and finite_related.get("direct") == expected_direct_master_ids,
            f"{master_id} finite-test direct one-hop membership mismatch",
        )
        require(
            finite_related.get("context_master_ids") == expected_context_master_ids
            and finite_related.get("context") == expected_context_master_ids
            and finite_related.get("context_cluster_ids") == cluster_ids,
            f"{master_id} finite-test contextual one-hop membership mismatch",
        )
        require(
            finite_related.get("treatment_status")
            and isinstance(finite_related.get("connection_statuses"), list)
            and bool(finite_related.get("connection_statuses")),
            f"{master_id} finite-test relationship treatment state is incomplete",
        )
        require(
            "is only the recorded custodian/organ candidate" in finite_test.get("decision_dependency", {}).get("en", "")
            and "solo el candidato registrado como custodio/órgano" in finite_test.get("decision_dependency", {}).get("es", "")
            and "strongest hypothetical innocent or contrary explanation could be" in finite_test.get("contrary_explanation", {}).get("en", "")
            and "No act is attributed by this model to the recorded candidate" in finite_test.get("contrary_explanation", {}).get("en", "")
            and "explicación inocente o contraria hipotética" in finite_test.get("contrary_explanation", {}).get("es", "")
            and "Este modelo no atribuye actuación alguna al candidato registrado" in finite_test.get("contrary_explanation", {}).get("es", "")
            and "is not treated as competent merely because" in finite_test.get("if_confirmed", {}).get("en", "")
            and "no se considera competente por el mero hecho" in finite_test.get("if_confirmed", {}).get("es", "")
            and "is not treated as competent or required to act" in finite_test.get("if_refuted", {}).get("en", "")
            and "no considera competente ni obliga a actuar" in finite_test.get("if_refuted", {}).get("es", ""),
            f"{master_id} finite-test consequence treats a recorded custodian as competent or obliged",
        )

        navigation = finite_test.get("navigation", {})
        expected_navigation = {
            "controlled_trace_fragment": f"#trace-proceeding={master_id}",
            "controlled_isolation_fragment": f"#isolation-test={master_id}",
            "master_register_route_en": f"en/master-proceedings-register/#record-{master_id}",
            "master_register_route_es": f"es/registro-maestro-procedimientos/#record-{master_id}",
            "controlled_trace_route_en": f"en/proceedings-map/#trace-proceeding={master_id}",
            "controlled_trace_route_es": f"es/mapa-procedimientos/#trace-proceeding={master_id}",
            "controlled_isolation_route_en": f"en/proceedings-map/#isolation-test={master_id}",
            "controlled_isolation_route_es": f"es/mapa-procedimientos/#isolation-test={master_id}",
            "controlled_navigation_status": "AVAILABLE",
            "dedicated_narrative_dossier_status": "PARTIAL_NOT_INFERRED",
        }
        require(
            all(navigation.get(field) == value for field, value in expected_navigation.items()),
            f"{master_id} finite-test Master/trace/isolation navigation is incomplete or invents a dossier",
        )

        receipt_knowledge = finite_test.get("receipt_knowledge", {})
        require(
            receipt_knowledge.get("classification")
            in {"SOURCE_BACKED_INSTITUTIONAL_TRACE", "EXPLICIT_SOURCE_NOT_LOCATED"},
            f"{master_id} receipt/knowledge classification is absent or uncontrolled",
        )
        if receipt_knowledge.get("classification"):
            receipt_knowledge_classified_ids.add(master_id)
        institutional_axes = receipt_knowledge.get("institutional_axes", {})
        require(
            set(institutional_axes) == INSTITUTIONAL_RECEIPT_AXES
            and all(str(value).strip() for value in institutional_axes.values()),
            f"{master_id} does not carry six independent institutional receipt/treatment axes",
        )
        require(
            set(institutional_axes.values()) <= receipt_status_vocabulary,
            f"{master_id} carries an uncatalogued institutional receipt/treatment grade",
        )
        institutional_axis_basis = receipt_knowledge.get(
            "institutional_axis_basis", {}
        )
        require(
            set(institutional_axis_basis) == FISCALIA_MATRIX_AXES,
            f"{master_id} lacks per-axis institutional provenance",
        )
        receipt_axis_statuses = {
            **institutional_axes,
            "cross_file_acknowledgement_status": receipt_knowledge.get(
                "cross_file_acknowledgement_status"
            ),
        }
        for axis, basis in institutional_axis_basis.items():
            expected_status = receipt_axis_statuses.get(axis)
            if axis in {"material_received_status", "referral_status"}:
                expected_status = basis.get("status")
            require(
                basis.get("status") == expected_status
                and basis.get("status") in receipt_status_vocabulary
                and basis.get("basis_kind")
                and basis.get("basis_en")
                and basis.get("basis_es")
                and basis.get("limitation_en")
                and basis.get("limitation_es")
                and isinstance(basis.get("source"), dict)
                and bool(basis.get("source")),
                f"{master_id} lacks a controlled basis/limitation for {axis}",
            )
        if receipt_knowledge.get("classification") == "EXPLICIT_SOURCE_NOT_LOCATED":
            require(
                set(institutional_axes.values()) == {"NOT_LOCATED"}
                and receipt_knowledge.get("cross_file_acknowledgement_status")
                == "NOT_LOCATED"
                and all(
                    basis.get("status") == "NOT_LOCATED"
                    and basis.get("basis_kind") == "EXPLICIT_SOURCE_NOT_LOCATED"
                    and basis.get("source", {}).get("kind")
                    == "PUBLIC_SOURCE_NOT_LOCATED"
                    for basis in institutional_axis_basis.values()
                ),
                f"{master_id} unprofiled institutional classification contains a positive or circular grade",
            )
        require(
            receipt_knowledge.get("cross_file_acknowledgement_status")
            and receipt_knowledge.get("limitations_en")
            and receipt_knowledge.get("limitations_es"),
            f"{master_id} receipt/knowledge boundary is incomplete",
        )
        actor_specific = receipt_knowledge.get("actor_specific", {})
        actor_source_status = actor_specific.get("source_status", "")
        require(
            actor_source_status == "NO_ACTOR_SPECIFIC_SOURCE_LOCATED"
            and actor_specific.get("receipt_status") == "NOT_ESTABLISHED"
            and actor_specific.get("knowledge_status") == "NOT_ESTABLISHED"
            and actor_specific.get("actor_ids") == [],
            f"{master_id} actor-specific source/receipt/knowledge state is not separately classified",
        )
        if actor_status_is_positive(actor_source_status):
            actor_positive_ids.add(master_id)
            actor_source_refs = (
                actor_specific.get("source_refs")
                or actor_specific.get("source_ids")
                or actor_specific.get("profile_ids")
                or []
            )
            require(
                bool(actor_specific.get("actor_ids")) and bool(actor_source_refs),
                f"{master_id} asserts positive actor-specific evidence without an actor and source",
            )

    require(
        len(finite_test_ids) == CURRENT_PUBLIC_EXACT
        and len(set(finite_test_ids)) == CURRENT_PUBLIC_EXACT,
        "finite-test identities do not cover the 97 exact public proceedings exactly once",
    )
    require(
        receipt_knowledge_classified_ids == exact_public_ids,
        "receipt/knowledge classifications do not cover all 97 exact public proceedings",
    )
    for field, languages in finite_specific_values.items():
        require(
            len(languages["en"]) == CURRENT_PUBLIC_EXACT
            and len(languages["es"]) == CURRENT_PUBLIC_EXACT,
            f"finite-test {field} is structural boilerplate rather than 97 file-specific tests",
        )
    require(
        len(finite_source_route_payloads) == CURRENT_PUBLIC_EXACT,
        "finite-test source routes are not exact-file specific",
    )

    # The reviewed episode set is an explicit source map.  It may not be
    # reconstructed from free-text matter references or silently expanded.
    source_episodes = fiscalia_responses.get("episodes", [])
    source_episode_by_id = {episode.get("id"): episode for episode in source_episodes}
    episode_profiles = interlinkability.get("fiscalia_response_episode_profiles", [])
    episode_profile_ids = [profile.get("profile_id") for profile in episode_profiles]
    actual_episode_mapping = {
        profile.get("episode_id"): profile.get("master_id")
        for profile in episode_profiles
    }
    require(
        len(source_episodes) == CURRENT_FISCALIA_RESPONSE_EPISODES
        and set(source_episode_by_id) == set(EXPECTED_FISCALIA_EPISODE_MASTER_IDS),
        "controlled Fiscalía response source no longer contains exactly the nine reviewed episodes",
    )
    require(
        len(episode_profiles) == CURRENT_FISCALIA_RESPONSE_EPISODES
        and len(set(episode_profile_ids)) == CURRENT_FISCALIA_RESPONSE_EPISODES
        and actual_episode_mapping == EXPECTED_FISCALIA_EPISODE_MASTER_IDS,
        "Fiscalía response profiles do not exactly preserve the reviewed episode-to-Master map",
    )
    require(
        actual_episode_mapping.get("dp1901-2026") == "GC-CRI-008",
        "DP 1901/2026 episode is not explicitly mapped to GC-CRI-008",
    )
    for profile in episode_profiles:
        episode_id = profile.get("episode_id")
        master_id = profile.get("master_id")
        source_episode = source_episode_by_id.get(episode_id, {})
        require(master_id in exact_public_ids, f"{episode_id} profile maps outside the exact public denominator")
        require(
            profile.get("profile_id") == f"FISCALIA-RESPONSE-{episode_id}"
            and profile.get("date") == source_episode.get("date")
            and profile.get("source", {}).get("kind")
            == "CONTROLLED_FISCALIA_RESPONSE_EPISODE"
            and profile.get("source", {}).get("path")
            == "assets/data/fiscalia-response-correspondence.json"
            and profile.get("source", {}).get("field") == "episodes[]"
            and profile.get("source", {}).get("record_id") == episode_id,
            f"{episode_id} profile lacks exact controlled-source provenance",
        )
        for profile_field, source_field in (
            ("title_en", "title_en"),
            ("title_es", "title_es"),
            ("source_authored_known_summary_en", "known_en"),
            ("source_authored_known_summary_es", "known_es"),
            ("source_authored_request_summary_en", "requested_en"),
            ("source_authored_request_summary_es", "requested_es"),
            ("institutional_response_en", "response_en"),
            ("institutional_response_es", "response_es"),
            ("open_question_en", "unresolved_en"),
            ("open_question_es", "unresolved_es"),
            ("later_event_en", "next_en"),
            ("later_event_es", "next_es"),
            ("contrary_or_limiting_record_en", "causation_en"),
            ("contrary_or_limiting_record_es", "causation_es"),
            ("causation_status", "causation_level"),
        ):
            require(
                profile.get(profile_field) == source_episode.get(source_field),
                f"{episode_id} profile {profile_field} diverges from its controlled source field",
            )
        require(
            set(profile.get("institutional_axes", {})) == INSTITUTIONAL_RECEIPT_AXES
            and all(
                str(value).strip()
                for value in profile.get("institutional_axes", {}).values()
            )
            and profile.get("cross_file_acknowledgement_status")
            and profile.get("attribution_boundary"),
            f"{episode_id} profile lacks the six-axis attribution boundary",
        )
        profile_axis_basis = profile.get("institutional_axis_basis", {})
        require(
            set(profile_axis_basis) == FISCALIA_MATRIX_AXES,
            f"{episode_id} profile lacks nine independent axis bases",
        )
        exposed_profile_statuses = {
            **profile.get("institutional_axes", {}),
            "cross_file_acknowledgement_status": profile.get(
                "cross_file_acknowledgement_status"
            ),
            "material_received_status": EXPECTED_FISCALIA_EPISODE_MATERIAL_STATUS.get(
                episode_id
            ),
            "referral_status": EXPECTED_FISCALIA_EPISODE_REFERRAL_STATUS.get(
                episode_id, "NOT_LOCATED"
            ),
        }
        for axis, basis in profile_axis_basis.items():
            expected_source_field = (
                "unresolved"
                if basis.get("status") in {"NOT_LOCATED", "STATUS_UNRESOLVED"}
                else EXPECTED_FISCALIA_EPISODE_AXIS_SOURCE_FIELD_OVERRIDES.get(
                    (episode_id, axis), EXPECTED_FISCALIA_AXIS_SOURCE_FIELDS[axis]
                )
            )
            require(
                basis.get("status") == exposed_profile_statuses[axis]
                and basis.get("status") in receipt_status_vocabulary
                and basis.get("basis_kind")
                and basis.get("basis_en")
                and basis.get("basis_es")
                and basis.get("limitation_en")
                and basis.get("limitation_es")
                and basis.get("source", {}).get("record_id") == episode_id
                and basis.get("source", {}).get("profile_id")
                == profile.get("profile_id"),
                f"{episode_id} {axis} grade lacks exact episode provenance",
            )
            require(
                basis.get("source", {}).get("field")
                == f"episodes[].{expected_source_field}_en/{expected_source_field}_es",
                f"{episode_id} {axis} grade cites the wrong source episode field",
            )
            if (episode_id, axis) in EXPECTED_FISCALIA_AXIS_STATUS_PRECISION:
                require(
                    basis.get("status")
                    == EXPECTED_FISCALIA_AXIS_STATUS_PRECISION[(episode_id, axis)],
                    f"{episode_id} {axis} overstates the controlled source",
                )
            if basis.get("status") in {"NOT_LOCATED", "STATUS_UNRESOLVED"}:
                require(
                    source_episode.get("unresolved_en", "") in basis.get("basis_en", "")
                    and source_episode.get("unresolved_es", "") in basis.get("basis_es", ""),
                    f"{episode_id} {axis} gap basis does not state the controlled unresolved source",
                )
            else:
                require(
                    basis.get("basis_en")
                    == source_episode.get(f"{expected_source_field}_en")
                    and basis.get("basis_es")
                    == source_episode.get(f"{expected_source_field}_es"),
                    f"{episode_id} {axis} positive grade text does not equal its cited source field",
                )
        require(
            "matter_references" not in profile,
            f"{episode_id} profile exposes or joins a raw matter_references field",
        )
    profile_ids_by_master: dict[str, list[str]] = {}
    for profile in episode_profiles:
        profile_ids_by_master.setdefault(profile["master_id"], []).append(
            profile["profile_id"]
        )
    disposition_by_master = {
        disposition.get("master_id"): disposition for disposition in dispositions
    }
    for master_id in exact_public_ids:
        receipt = (
            disposition_by_master.get(master_id, {})
            .get("finite_test", {})
            .get("receipt_knowledge", {})
        )
        expected_profile_ids = sorted(profile_ids_by_master.get(master_id, []))
        expected_classification = (
            "SOURCE_BACKED_INSTITUTIONAL_TRACE"
            if expected_profile_ids
            else "EXPLICIT_SOURCE_NOT_LOCATED"
        )
        require(
            sorted(receipt.get("source_profile_ids", [])) == expected_profile_ids
            and receipt.get("classification") == expected_classification,
            f"{master_id} receipt profile membership/classification diverges from the reviewed episode map",
        )
        event_profile_ids = sorted(
            event.get("profile_id") for event in receipt.get("event_refs", [])
        )
        require(
            event_profile_ids == expected_profile_ids,
            f"{master_id} institutional event references diverge from reviewed profile membership",
        )
    require(
        '.get("matter_references")' not in interlink_builder
        and "['matter_references']" not in interlink_builder,
        "interlinkability builder joins profiles from raw matter_references",
    )

    fiscalia_public_rows = [
        row for row in public_rows if "FISCAL" in row.get("Stream", "").upper()
    ]
    fiscalia_public_ids = {row["Master_ID"] for row in fiscalia_public_rows}
    fiscalia_exact_ids = {
        row["Master_ID"]
        for row in fiscalia_public_rows
        if row.get("Is_Proceeding") == "TRUE"
    }
    fiscalia_unresolved_ids = fiscalia_public_ids - fiscalia_exact_ids
    fiscalia_matrix = interlinkability.get("fiscalia_office_file_matrix", [])
    fiscalia_matrix_ids = [row.get("master_id") for row in fiscalia_matrix]
    require(
        len(fiscalia_public_ids) == CURRENT_FISCALIA_OFFICE_FILE_RECORDS
        and len(fiscalia_exact_ids) == CURRENT_FISCALIA_EXACT_RECORDS
        and len(fiscalia_unresolved_ids) == CURRENT_FISCALIA_UNRESOLVED_RECORDS,
        "canonical Fiscalía Stream denominator is not 24 rows / 21 exact / 3 unresolved",
    )
    require(
        len(fiscalia_matrix_ids) == CURRENT_FISCALIA_OFFICE_FILE_RECORDS
        and len(set(fiscalia_matrix_ids)) == CURRENT_FISCALIA_OFFICE_FILE_RECORDS
        and set(fiscalia_matrix_ids) == fiscalia_public_ids,
        "Fiscalía office/file matrix does not exactly equal every public Fiscalía Stream row",
    )
    require(
        "GC-CRI-008" not in fiscalia_matrix_ids,
        "DP 1901/2026 judicial file was incorrectly admitted to the 24-row Fiscalía Stream matrix",
    )
    profiled_matrix_ids: set[str] = set()
    profile_id_set = set(episode_profile_ids)
    profile_by_id = {
        profile["profile_id"]: profile for profile in episode_profiles
    }
    expected_direct_by_master: dict[str, set[str]] = {}
    for relationship in relationships:
        left = relationship.get("from_master_id")
        right = relationship.get("to_master_id")
        expected_direct_by_master.setdefault(left, set()).add(right)
        expected_direct_by_master.setdefault(right, set()).add(left)
    expected_context_by_master: dict[str, set[str]] = {}
    for cluster in context_clusters:
        members = set(cluster.get("member_master_ids", []))
        for member in members:
            expected_context_by_master.setdefault(member, set()).update(
                members - {member}
            )
    for matrix_row in fiscalia_matrix:
        master_id = matrix_row.get("master_id")
        canonical_row = public_by_id.get(master_id, {})
        source_profile_ids = matrix_row.get("source_profile_ids", [])
        if source_profile_ids:
            profiled_matrix_ids.add(master_id)
        require(
            matrix_row.get("reference") == canonical_row.get("Reference")
            and matrix_row.get("origin_office") == canonical_row.get("Origin_Organ")
            and matrix_row.get("current_custodian") == canonical_row.get("Current_Custodian")
            and matrix_row.get("is_proceeding") == canonical_row.get("Is_Proceeding")
            and matrix_row.get("record_type") == canonical_row.get("Record_Type")
            and matrix_row.get("source_status") == canonical_row.get("Source_Status"),
            f"{master_id} Fiscalía matrix identity/source fields diverge from the public Master row",
        )
        require(
            len(source_profile_ids) == len(set(source_profile_ids))
            and set(source_profile_ids) <= profile_id_set,
            f"{master_id} Fiscalía matrix cites an unknown or duplicate response profile",
        )
        expected_profile_status = (
            "SOURCE_CONTROLLED_PROFILE" if source_profile_ids else "EXPLICIT_PROFILE_GAP"
        )
        require(
            matrix_row.get("profile_status") == expected_profile_status,
            f"{master_id} Fiscalía matrix profile/gap status is inconsistent",
        )
        for field in (
            "received_or_known",
            "requested",
            "institutional_response",
            "material_inventory_gap",
            "related_assets_gap",
            "what_was_referred",
            "what_was_actually_examined",
            "strongest_contrary",
            "unanswered_or_source_gap",
        ):
            require_bilingual(matrix_row.get(field), f"{master_id} Fiscalía matrix {field}")
        matrix_statuses = {
            axis: matrix_row.get(axis) for axis in FISCALIA_MATRIX_AXES
        }
        require(
            set(matrix_statuses.values()) <= receipt_status_vocabulary
            and all(matrix_statuses.values())
            and matrix_row.get("unitary_acknowledgement_status") == "NOT_LOCATED"
            and matrix_row.get("boundary_en")
            and matrix_row.get("boundary_es"),
            f"{master_id} Fiscalía matrix lacks independent treatment/acknowledgement states",
        )
        expected_referral = EXPECTED_FISCALIA_MATRIX_REFERRAL_STATUS.get(
            master_id, "NOT_LOCATED"
        )
        require(
            matrix_row.get("referral_status") == expected_referral,
            f"{master_id} Fiscalía referral status was inferred from transmission",
        )
        matrix_axis_basis = matrix_row.get("institutional_axis_basis", {})
        require(
            set(matrix_axis_basis) == FISCALIA_MATRIX_AXES,
            f"{master_id} Fiscalía matrix lacks per-axis provenance",
        )
        for axis, basis in matrix_axis_basis.items():
            require(
                basis.get("status") == matrix_statuses[axis]
                and basis.get("basis_kind")
                and basis.get("basis_en")
                and basis.get("basis_es")
                and basis.get("limitation_en")
                and basis.get("limitation_es")
                and isinstance(basis.get("source"), dict)
                and bool(basis.get("source")),
                f"{master_id} Fiscalía matrix {axis} lacks source/basis/limitation",
            )
        if source_profile_ids:
            require(
                matrix_axis_basis
                == profile_by_id[source_profile_ids[0]].get(
                    "institutional_axis_basis", {}
                ),
                f"{master_id} Fiscalía matrix axis bases diverge from the controlled episode profile",
            )
        else:
            require(
                all(
                    basis.get("status") == "NOT_LOCATED"
                    and basis.get("basis_kind") == "EXPLICIT_SOURCE_NOT_LOCATED"
                    and basis.get("source", {}).get("kind")
                    == "PUBLIC_SOURCE_NOT_LOCATED"
                    for basis in matrix_axis_basis.values()
                ),
                f"{master_id} unprofiled Fiscalía row contains a positive or circular institutional grade",
            )
        expected_matrix_direct = sorted(
            expected_direct_by_master.get(master_id, set())
        )
        expected_matrix_context = sorted(
            expected_context_by_master.get(master_id, set())
        )
        expected_matrix_related = sorted(
            set(expected_matrix_direct) | set(expected_matrix_context)
        )
        require(
            matrix_row.get("related_direct_master_ids") == expected_matrix_direct
            and matrix_row.get("related_context_master_ids")
            == expected_matrix_context
            and matrix_row.get("related_master_ids") == expected_matrix_related,
            f"{master_id} Fiscalía matrix direct/context membership mismatch",
        )
        require(
            matrix_row.get("related_assets") == []
            and matrix_row.get("related_assets_status") == "NOT_LOCATED"
            and matrix_row.get("material_received") == [],
            f"{master_id} Fiscalía matrix invents a received-material or asset inventory",
        )
        material_summaries = matrix_row.get("material_allegations_evidence", [])
        require(
            len(material_summaries) == (2 if source_profile_ids else 0)
            and all(
                item.get("kind")
                and item.get("text_en")
                and item.get("text_es")
                and item.get("attribution")
                for item in material_summaries
            ),
            f"{master_id} Fiscalía material allegations/evidence are absent or unattributed",
        )
        if source_profile_ids:
            episode_ids = {
                profile_by_id[profile_id]["episode_id"]
                for profile_id in source_profile_ids
            }
            require(
                len(episode_ids) == 1
                and matrix_row.get("material_received_status")
                == EXPECTED_FISCALIA_EPISODE_MATERIAL_STATUS[next(iter(episode_ids))],
                f"{master_id} Fiscalía material-received grade is stale",
            )
        else:
            require(
                matrix_row.get("material_received_status") == "NOT_LOCATED",
                f"{master_id} unprofiled Fiscalía row asserts received material",
            )
    require(
        len(profiled_matrix_ids) == CURRENT_FISCALIA_PROFILED_MATRIX_RECORDS,
        "Fiscalía matrix must contain exactly 8 source-profiled rows and 16 explicit gaps",
    )

    interlink_coverage = interlinkability.get("coverage", {})
    case_prism_exact_ids = {
        mid
        for prop in prism.get("propositions", [])
        for cell in prop.get("cells", {}).values()
        if cell.get("status") != "OUTSIDE"
        for mid in cell.get("master_ids", [])
        if mid in exact_public_ids
    }
    require(
        interlink_coverage.get("canonical_exact_proceeding_count")
        == CURRENT_CANONICAL_EXACT,
        "canonical exact-proceeding interlink denominator mismatch",
    )
    require(
        interlink_coverage.get("public_exact_proceeding_count")
        == interlink_coverage.get("node_disposition_count")
        == CURRENT_PUBLIC_EXACT,
        "public exact-proceeding interlink denominator mismatch",
    )
    require(
        interlink_coverage.get("private_exact_excluded_count")
        == CURRENT_PRIVATE_EXACT,
        "private exact-proceeding exclusion count mismatch",
    )
    require(
        interlink_coverage.get("direct_relationship_count")
        == len(relationships)
        == CURRENT_DIRECT_PAIRS,
        "direct relationship coverage count mismatch",
    )
    require(interlink_coverage.get("direct_relationship_source_verified_pair_count") == source_verified_pair_count, "source-verified direct-pair coverage mismatch")
    require(interlink_coverage.get("direct_relationship_source_reported_pending_pair_count") == source_reported_pending_pair_count, "source-reported-pending direct-pair coverage mismatch")
    require(
        interlink_coverage.get("direct_source_assertion_count")
        == len(actual_source_assertions)
        == CURRENT_DIRECT_ASSERTIONS,
        "direct source-assertion coverage mismatch",
    )
    require(interlink_coverage.get("direct_source_verified_assertion_count") == source_verified_assertion_count, "source-verified direct-assertion coverage mismatch")
    require(interlink_coverage.get("direct_source_reported_pending_assertion_count") == source_reported_pending_assertion_count, "source-reported-pending direct-assertion coverage mismatch")
    require(interlink_coverage.get("context_cluster_count") == len(context_clusters), "context-cluster coverage count mismatch")
    require(interlink_coverage.get("source_controlled_corridor_count") == 1, "source-controlled corridor denominator mismatch")
    require(interlink_coverage.get("recorded_stream_cluster_count") == 0, "same-stream taxonomy was promoted into material reconnection context")
    require(
        interlink_coverage.get("case_prism_exact_proceeding_covered_count")
        == len(case_prism_exact_ids)
        == CURRENT_CASE_PRISM_EXACT_COVERED,
        "Case Prism exact-proceeding covered denominator mismatch",
    )
    require(
        interlink_coverage.get("case_prism_exact_proceeding_uncovered_count")
        == len(exact_public_ids - case_prism_exact_ids)
        == CURRENT_CASE_PRISM_EXACT_UNCOVERED,
        "Case Prism exact-proceeding uncovered denominator mismatch",
    )
    require(
        interlink_coverage.get("decision_dependency_exact_coverage")
        == f"VERIFIED_{CURRENT_PUBLIC_EXACT}_OF_{CURRENT_PUBLIC_EXACT}",
        "exact-file decision-dependency register coverage is incomplete",
    )
    require(
        interlink_coverage.get("decision_dependency_exact_coverage_scope")
        == "PUBLIC_EXACT_FILE_FINITE_TEST_REGISTER",
        "exact-file decision-dependency coverage has the wrong public scope",
    )
    require(
        interlink_coverage.get("shared_case_prism_proposition_membership_coverage")
        == f"GAP_{CURRENT_CASE_PRISM_EXACT_COVERED}_OF_{CURRENT_PUBLIC_EXACT}",
        "shared-proposition membership gap is overstated or concealed",
    )
    require(
        interlink_coverage.get("shared_case_prism_proposition_membership_scope")
        == "SHARED_CASE_PRISM_PROPOSITION_MEMBERSHIP_ONLY",
        "shared proposition membership is conflated with exact-file actionability",
    )
    require(
        interlink_coverage.get("finite_test_family_counts")
        == EXPECTED_FINITE_TEST_FAMILY_COUNTS,
        "finite-test family coverage denominator is stale or misclassified",
    )
    require(
        interlink_coverage.get("exact_file_decision_dependency_actionability_count")
        == CURRENT_PUBLIC_EXACT
        and interlink_coverage.get(
            "exact_file_decision_dependency_actionability_coverage"
        )
        == f"VERIFIED_{CURRENT_PUBLIC_EXACT}_OF_{CURRENT_PUBLIC_EXACT}",
        "exact-file decision-dependency actionability is not modelled 97/97",
    )
    require(
        interlink_coverage.get("bilingual_specific_next_source_count")
        == CURRENT_PUBLIC_EXACT,
        "bilingual next-source denominator does not cover every exact public proceeding",
    )
    require(
        interlink_coverage.get("bilingual_specific_next_source_coverage")
        == f"VERIFIED_{CURRENT_PUBLIC_EXACT}_OF_{CURRENT_PUBLIC_EXACT}",
        "bilingual specific next-source coverage is incomplete",
    )
    require(
        interlink_coverage.get("exact_proceeding_full_finite_test_count")
        == CURRENT_PUBLIC_EXACT,
        "exact-proceeding finite-test count does not match the 97-file denominator",
    )
    require(
        interlink_coverage.get("exact_proceeding_full_finite_test_coverage")
        == f"VERIFIED_{CURRENT_PUBLIC_EXACT}_OF_{CURRENT_PUBLIC_EXACT}",
        "exact-proceeding full finite-test model is not complete 97/97",
    )
    require(
        interlink_coverage.get("receipt_knowledge_classification_count")
        == CURRENT_PUBLIC_EXACT
        and interlink_coverage.get("receipt_knowledge_classification_coverage")
        == f"VERIFIED_{CURRENT_PUBLIC_EXACT}_OF_{CURRENT_PUBLIC_EXACT}"
        and interlink_coverage.get("receipt_knowledge_axis_provenance_count")
        == CURRENT_PUBLIC_EXACT
        and interlink_coverage.get("receipt_knowledge_axis_provenance_coverage")
        == f"VERIFIED_{CURRENT_PUBLIC_EXACT}_OF_{CURRENT_PUBLIC_EXACT}"
        and interlink_coverage.get("receipt_knowledge_positive_source_profile_count")
        == CURRENT_FISCALIA_RESPONSE_EPISODES,
        "receipt/knowledge model coverage or separate positive-profile count is stale",
    )
    require(
        not actor_positive_ids,
        "actor-specific positive evidence is asserted despite the current zero-source denominator",
    )
    require(
        interlink_coverage.get("fiscalia_office_file_matrix_count")
        == CURRENT_FISCALIA_OFFICE_FILE_RECORDS
        and interlink_coverage.get("fiscalia_office_file_matrix_coverage")
        == "VERIFIED_24_OF_24"
        and interlink_coverage.get(
            "fiscalia_office_file_matrix_substantive_column_count"
        )
        == CURRENT_FISCALIA_OFFICE_FILE_RECORDS
        and interlink_coverage.get(
            "fiscalia_office_file_matrix_substantive_column_coverage"
        )
        == "VERIFIED_24_OF_24"
        and interlink_coverage.get("fiscalia_office_file_matrix_exact_count")
        == CURRENT_FISCALIA_EXACT_RECORDS
        and interlink_coverage.get("fiscalia_office_file_matrix_unverified_count")
        == CURRENT_FISCALIA_UNRESOLVED_RECORDS
        and interlink_coverage.get("fiscalia_response_episode_profile_count")
        == CURRENT_FISCALIA_RESPONSE_EPISODES
        and interlink_coverage.get(
            "fiscalia_office_file_matrix_source_profiled_record_count"
        )
        == CURRENT_FISCALIA_PROFILED_MATRIX_RECORDS,
        "Fiscalía matrix/profile coverage denominators are stale",
    )
    require(
        interlink_coverage.get("controlled_trace_route_count")
        == interlink_coverage.get("controlled_isolation_route_count")
        == CURRENT_PUBLIC_EXACT
        and interlink_coverage.get("controlled_navigation_coverage")
        == f"VERIFIED_{CURRENT_PUBLIC_EXACT}_OF_{CURRENT_PUBLIC_EXACT}"
        and interlink_coverage.get("dedicated_narrative_dossier_coverage")
        == "PARTIAL_NOT_INFERRED",
        "97/97 controlled navigation or the separate partial dossier boundary is stale",
    )
    require("bilingual_actionability" not in interlink_coverage, "next-source coverage is mislabeled as full bilingual actionability")
    require(interlink_coverage.get("classification_counts") == {token: disposition_counts.get(token, 0) for token in classifications}, "disposition classification coverage mismatch")
    require(interlink_coverage.get("unexplained_exact_proceeding_count") == 0, "public exact proceeding remains unclassified")
    require(interlink_coverage.get("geography_only_bridge_count") == 0, "Geography-only bridge admitted")

    # Corrections must be consolidated into the runtime source, not left as overlays.
    val = by_id.get("VAL-CIV-001", {})
    expected_val = {
        "Record_Type": "JUDICIAL_PROCEEDING", "Is_Proceeding": "TRUE", "Proceeding_Class": "DIRECT",
        "Origin_Organ": "Juzgado de Primera Instancia nº 27 de Valencia",
        "Current_Custodian": "Juzgado de Primera Instancia nº 27 de Valencia",
        "Reference": "ORD 1859/2023-9", "Secondary_Reference": "Aweswell Limited v CAIXABANK, S.A.",
        "NIG": "46250-42-1-2023-0049579", "Status": "Pending and contested",
        "Source_Status": "VERIFIED_PRIMARY_DERIVED_PUBLIC_CONTROL", "Public_Treatment": "PUBLIC_CONTROLLED",
    }
    for field, value in expected_val.items():
        require(val.get(field) == value, f"VAL-CIV-001 {field} not consolidated")
    require("28 Jan 2027 at 10:00" in val.get("Latest_Known_Event", ""), "VAL-CIV-001 hearing not consolidated")
    overlay_retired = (
        "RETIRED IN CORRECTIVE SOURCE TREE" in val_overlay
        and "public/main retirement effective" in val_overlay
    ) or "RETIRED AFTER CANONICAL CONSOLIDATION" in val_overlay
    gap_consolidated = (
        "SOURCE-TREE CONSOLIDATION COMPLETE" in val_gap
        and "public/main closure effective" in val_gap
    ) or ("CLOSED" in val_gap and "physically consolidated" in val_gap)
    require(overlay_retired, "Valencia overlay retirement state missing")
    require(gap_consolidated, "Valencia reconciliation consolidation state missing")
    dp = by_id.get("GC-CRI-009", {})
    require("Provisional dismissal" in dp.get("Status", ""), "GC-CRI-009 provisional dismissal missing")
    require("no filed reform/subsidiary appeal" in dp.get("Status", ""), "GC-CRI-009 filed-appeal correction missing")
    require("No filed reform/subsidiary appeal" in dp.get("Appeal_or_Review", ""), "GC-CRI-009 appeal field stale")
    require("A draft challenge is not a filed act" in dp.get("Notes", ""), "GC-CRI-009 draft/filed boundary missing")
    require("No filed reform/subsidiary appeal" in dp_control, "DP1956 provenance correction lost")
    require(by_id.get("GC-APP-004", {}).get("Parent_Master_ID") == "GC-CAL-002", "RPL 2523 parent must be GC-CAL-002")

    # User-command caret registration: retain the lead without manufacturing identity or edges.
    gc_548 = by_id.get("GC-REF-031", {})
    expected_gc_548 = {
        "Record_Type": "UNRESOLVED_REFERENCE", "Is_Proceeding": "UNVERIFIED",
        "Proceeding_Class": "DIRECT", "Geography": "Gran Canaria",
        "Reference": "548/2023", "Secondary_Reference": "User-supplied locator: Plaza 2 · T1",
        "Source_Status": "OPEN_REFERENCE", "Public_Treatment": "PUBLIC_SUMMARY_WITH_IDENTITY_GAP",
        "Repo_Canonical_Source": "archive/GC_548_2023_PLAZA2_T1_CARET_CONTINUITY_CONTROL_30AUG2026.md",
    }
    for field, value in expected_gc_548.items():
        require(gc_548.get(field) == value, f"GC-REF-031 {field} continuity changed")
    require(not any(gc_548.get(field, "").strip() for field in ("Parent_Master_ID", "Appeal_or_Review", "Linked_Proceedings")), "GC-REF-031 must not carry an unsupported direct edge")
    require("ME-111" in missing_evidence and "GC-REF-031" in missing_evidence, "GC-REF-031 missing-evidence bridge absent")
    require("CARET_PENDING" in gc_548_control and "No source presently establishes" in gc_548_control, "GC-REF-031 identity/link boundary absent")
    require(gc_548_manifest.get("canonical_candidate_key") == "GC-REF-031", "GC-REF-031 manifest key changed")
    require(gc_548_manifest.get("identity_state") == "CARET_PENDING", "GC-REF-031 manifest identity state changed")
    require(
        gc_548_manifest.get("public_projection", {}).get("source")
        == "canonical_csv_runtime_projection",
        "GC-REF-031 historical LIVE_VERIFIED projection source changed",
    )
    gc_548_migration = gc_548_manifest.get("projection_migration", {})
    require_pr1235_live_migration(
        gc_548_migration,
        "assets/data/proceedings-master-public-v1.json",
        "GC-REF-031 allowlisted-projection migration",
    )
    require(gc_548_manifest.get("interlinking", {}).get("direct_proceeding_edges") == [], "GC-REF-031 manifest invents a direct edge")
    master_projection_migration = master_publication_manifest.get("projection_migration", {})
    require(
        master_publication_manifest.get("public_projection", {}).get("source") == "canonical_csv_runtime_projection",
        "Master Register historical projection source changed",
    )
    require_pr1235_live_migration(
        master_projection_migration,
        "assets/data/proceedings-master-public-v1.json",
        "Master Register allowlisted-projection migration",
    )

    lz_4009 = by_id.get("LZ-REF-042", {})
    expected_lz_4009 = {
        "Record_Type": "UNRESOLVED_REFERENCE",
        "Is_Proceeding": "UNVERIFIED",
        "Reference": "4009/2015",
        "Source_Status": "OPEN_REFERENCE",
        "Public_Treatment": "INTERNAL_KNOWLEDGE_REGISTER_NOT_AUTO_PUBLISHED",
        "Repo_Canonical_Source": "archive/ARRECIFE_4009_2015_CARET_INTERLINK_CONTROL_30AUG2026.md",
    }
    for field, value in expected_lz_4009.items():
        require(lz_4009.get(field) == value, f"LZ-REF-042 {field} continuity changed")
    require(not any(lz_4009.get(field, "").strip() for field in ("Parent_Master_ID", "Appeal_or_Review", "Linked_Proceedings")), "LZ-REF-042 must not carry an unsupported direct edge")
    require("CARET_PENDING" in lz_4009_control and "NOT LOCATED" in lz_4009_control, "LZ-REF-042 identity/non-location boundary absent")
    require(
        lz_4009_manifest.get("current_state") == "LIVE_VERIFIED"
        and lz_4009_manifest.get("merge_sha") == "2741dc72a05887c4bc55106b6dd69b296fc05fd1"
        and lz_4009_manifest.get("interlinking", {}).get("direct_procedural_edges") == [],
        "LZ-REF-042 live lifecycle or no-edge boundary changed",
    )
    lz_4009_migration = lz_4009_manifest.get("projection_migration", {})
    require_pr1235_live_migration(
        lz_4009_migration,
        "assets/data/proceedings-master-public-v1.json",
        "LZ-REF-042 allowlisted-projection migration",
    )
    for trace_only_id in ("GC-REF-031", "LZ-JUD-042", "LZ-REF-042", "LZ-REF-044"):
        trace_only = public_by_id.get(trace_only_id, {})
        require(trace_only.get("Master_ID") == trace_only_id, f"{trace_only_id} is missing from the controlled public trace projection")
        require(trace_only.get("Is_Proceeding") == "UNVERIFIED", f"{trace_only_id} was promoted beyond its source-pending identity state")
        require(trace_only_id not in exact_public_ids, f"{trace_only_id} was admitted to exact-file isolation")
        require(trace_only_id not in interlink_serialised, f"{trace_only_id} was admitted to an exact relationship, context cluster or disposition")

    # DP 3205/2014 is an exact, source-controlled file and a singleton Case
    # Prism coordinate.  That makes it selectable and decision-dependency
    # covered, but neither creates a procedural edge nor a contextual cluster.
    dp3205 = by_id.get("LZ-JUD-043", {})
    require(dp3205.get("Is_Proceeding") == "TRUE", "LZ-JUD-043 exact proceeding state changed")
    require(dp3205.get("Reference") == "3205/2014", "LZ-JUD-043 reference changed")
    require(
        dp3205.get("Source_Status") == "PRIMARY_COMPLAINT_AND_OFFICIAL_SUMMONS_LOCATED_OUTCOME_OPEN",
        "LZ-JUD-043 source status changed",
    )
    require(
        dp3205.get("Public_Treatment") == "PUBLIC_CONTROLLED_PRIMARY_SOURCE_DERIVATIVE_OUTCOME_OPEN",
        "LZ-JUD-043 public treatment changed",
    )
    require(not any(dp3205.get(field, "").strip() for field in ("Parent_Master_ID", "Appeal_or_Review", "Linked_Proceedings")), "LZ-JUD-043 must not carry an unsupported direct edge")
    require("LZ-JUD-043" in public_by_id and "LZ-JUD-043" in exact_public_ids, "LZ-JUD-043 is not public-traceable and isolation-eligible")
    require(
        all("LZ-JUD-043" not in {relationship.get("from_master_id"), relationship.get("to_master_id")} for relationship in relationships),
        "LZ-JUD-043 was promoted into a direct relationship",
    )
    require(
        all("LZ-JUD-043" not in cluster.get("member_master_ids", []) for cluster in context_clusters),
        "LZ-JUD-043 singleton P19 membership was promoted into a context cluster",
    )
    dp3205_dispositions = [item for item in dispositions if item.get("master_id") == "LZ-JUD-043"]
    require(
        len(dp3205_dispositions) == 1
        and dp3205_dispositions[0].get("primary_classification") == "EXPLICIT_RELATIONSHIP_GAP"
        and not dp3205_dispositions[0].get("relationship_ids")
        and not dp3205_dispositions[0].get("context_cluster_ids"),
        "LZ-JUD-043 must retain one edge-free explicit relationship-gap disposition",
    )
    p19 = prism_prop_by_id.get("P19", {})
    p19_members = {
        master_id
        for cell in p19.get("cells", {}).values()
        if cell.get("status") != "OUTSIDE"
        for master_id in cell.get("master_ids", [])
    }
    require(p19_members == {"LZ-JUD-043"}, "P19 must remain a singleton LZ-JUD-043 decision-dependency coordinate")
    require("CTX-PRISM-P19" not in context_by_id, "singleton P19 was materialised as a cross-proceeding context cluster")

    # Parent relationships must resolve and be acyclic.
    parents = {row["Master_ID"]: row["Parent_Master_ID"].strip() for row in rows if row["Parent_Master_ID"].strip()}
    for child, parent_id in parents.items():
        require(parent_id in by_id, f"unresolved parent {parent_id} for {child}")
    for start in parents:
        seen, cursor = set(), start
        while cursor in parents:
            if cursor in seen:
                errors.append(f"parent cycle from {start}: {cursor}")
                break
            seen.add(cursor)
            cursor = parents[cursor]

    statuses = {"DIRECT", "CONTEXT", "OPEN", "NOT_LOCATED", "OUTSIDE"}
    treatments = {"DIRECTLY_IN_FILE", "EXPRESSLY_ACKNOWLEDGED", "RELIED_UPON", "CONTRADICTED", "MATERIALLY_RELEVANT_CONTEXT", "NOT_RAISED_OR_NOT_LOCATED", "OUTSIDE_PROCEDURAL_SCOPE", "STATUS_UNRESOLVED"}
    expected_lanes = {"concurso", "calificacion", "removal", "fees", "arrecife", "valencia", "meetingpoint", "tenerife", "fiscalia", "supervision", "historical", "publicmoney"}
    expected_audiences = {"all", "court", "appellate", "fiscal", "supervision", "authority", "research", "owner", "professional"}
    lanes, props = prism.get("lanes", []), prism.get("propositions", [])
    lane_ids = [lane.get("id") for lane in lanes]
    lane_set = set(lane_ids)
    lane_master_ids = {lane.get("id"): set(lane.get("master_ids", [])) for lane in lanes}
    prop_ids = {prop.get("id") for prop in props}
    audience_ids = {lens.get("id") for lens in prism.get("audience_lenses", [])}
    cells = [cell for prop in props for cell in prop.get("cells", {}).values()]
    referenced_ids = {mid for lane in lanes for mid in lane.get("master_ids", [])} | {mid for cell in cells for mid in cell.get("master_ids", [])}
    require(prism.get("schema_version") == "2.0.0", "Case Prism schema must be 2.0.0")
    require(prism.get("canonical_node_source_id") == "PROCEEDINGS_MASTER_REGISTER", "Case Prism canonical source identity changed")
    require(len(lane_ids) == len(lane_set) == 12 and lane_set == expected_lanes, "Case Prism lane denominator changed")
    require(prop_ids == {f"P{i:02d}" for i in range(1, 20)}, "Case Prism proposition denominator must be P01-P19")
    require(audience_ids == expected_audiences, "Case Prism audience denominator changed")
    require(set(prism.get("statuses", {})) == statuses, "relationship vocabulary mismatch")
    require(set(prism.get("treatments", {})) == treatments, "treatment vocabulary mismatch")
    require(referenced_ids <= set(by_id), f"unknown Case Prism IDs: {sorted(referenced_ids - set(by_id))}")
    require("GC-APP-007" not in referenced_ids, "synthetic removal-family object exposed as a third exact proceeding")
    require({"GC-APP-004", "GC-APP-005", "GC-APP-006", "GC-APP-028"} <= referenced_ids, "exact appellate IDs missing")
    prism_exact_covered_ids = {
        mid
        for cell in cells
        if cell.get("status") != "OUTSIDE"
        for mid in cell.get("master_ids", [])
        if mid in exact_public_ids
    }
    prism_exact_uncovered_ids = exact_public_ids - prism_exact_covered_ids
    require(
        len(prism_exact_covered_ids) == CURRENT_CASE_PRISM_EXACT_COVERED
        and len(prism_exact_uncovered_ids) == CURRENT_CASE_PRISM_EXACT_UNCOVERED,
        "Case Prism exact-file content denominator must remain explicit at "
        f"{CURRENT_CASE_PRISM_EXACT_COVERED}/{CURRENT_PUBLIC_EXACT} covered and "
        f"{CURRENT_CASE_PRISM_EXACT_UNCOVERED}/{CURRENT_PUBLIC_EXACT} uncovered",
    )

    prop_fields = {"id", "sort", "period_en", "period_es", "title_en", "title_es", "question_en", "question_es", "source_status", "attribution", "contrary_record", "decision_dependency", "actionability", "source_ids", "audience_priority", "cells"}
    cell_fields = {"status", "treatment", "evidence_status", "note_en", "note_es", "decision_en", "decision_es", "master_ids", "representation_lineage_status", "representation_gap_ids"}
    action_fields = {"source_needed", "competent_organ", "if_confirmed", "if_refuted"}
    source_catalog = prism.get("source_catalog", {})
    evidence_tokens = (
        {prop.get("source_status") for prop in props}
        | {cell.get("evidence_status") for cell in cells}
        | {source.get("evidence_status") for source in source_catalog.values()}
    )
    evidence_catalog = prism.get("evidence_statuses", {})
    require(set(evidence_catalog) == evidence_tokens, "bilingual evidence-status catalog denominator mismatch")
    require(all(meta.get("en") and meta.get("es") for meta in evidence_catalog.values()), "evidence-status catalog is not bilingual")
    counsel_gap_rows = counsel_gaps.get("gaps", []) if isinstance(counsel_gaps, dict) else counsel_gaps
    known_gap_ids = {item.get("gap_id") for item in counsel_gap_rows}
    for prop in props:
        pid = prop.get("id")
        require(prop_fields <= set(prop), f"{pid} missing proposition fields")
        require(set(prop.get("cells", {})) == lane_set, f"{pid} does not materialise every lane")
        require(set(prop.get("audience_priority", {})) >= audience_ids, f"{pid} lacks lens priorities")
        require(action_fields <= set(prop.get("actionability", {})), f"{pid} lacks finite actionability")
        require(prop.get("period_en") and prop.get("period_es") and "period" not in prop, f"{pid} period is not bilingual")
        for source_id in prop.get("source_ids", []):
            require(source_id in source_catalog, f"{pid} references unknown source {source_id}")
        for lane_id, cell in prop.get("cells", {}).items():
            require(cell_fields <= set(cell), f"{pid}/{lane_id} missing cell fields")
            require(set(cell.get("master_ids", [])) <= lane_master_ids[lane_id], f"{pid}/{lane_id} contains a cross-lane Master ID")
            require(cell.get("status") in statuses, f"{pid}/{lane_id} invalid relationship status")
            require(cell.get("treatment") in treatments, f"{pid}/{lane_id} invalid treatment")
            require(cell.get("note_en") and cell.get("note_es"), f"{pid}/{lane_id} lacks bilingual reason")
            require(cell.get("decision_en") and cell.get("decision_es"), f"{pid}/{lane_id} lacks decision dependency")
            require(set(cell.get("representation_gap_ids", [])) <= known_gap_ids, f"{pid}/{lane_id} unknown representation gap")

    relation_counts, treatment_counts = Counter(c["status"] for c in cells), Counter(c["treatment"] for c in cells)
    require(len(cells) == len(lanes) * len(props) == 228, f"expected 228 coordinates, found {len(cells)}")
    require(set(relation_counts) == statuses, "every relationship status must be used")
    require(treatment_counts["CONTRADICTED"] >= 1, "adverse/contrary treatment not represented")
    coverage = prism.get("coverage", {})
    require(coverage.get("explicit_coordinate_count") == 228 and coverage.get("unexplained_coordinate_count") == 0, "coverage denominator mismatch")
    require(coverage.get("counsel_procurador_denominator") == "GAP", "counsel/procurador incompleteness not explicit")
    for source_id, source in source_catalog.items():
        for language in ("en", "es"):
            href = source.get(f"href_{language}", "")
            require(href and (ROOT / href / "index.html").is_file(), f"{source_id} {language} route unresolved: {href}")

    required_views = {"CONVERGENCE_CLUSTER", "FRAGMENTATION_AUDIT", "DECISION_DEPENDENCY_MATRIX", "PARALLEL_PROCEEDINGS_LANES", "ISOLATION_TEST", "AUDIENCE_LENS"}
    require(schema.get("schema_version") == "1.7.0", "interconnectivity schema must be 1.7.0")
    require(schema.get("control_date") == "2026-08-31", "interconnectivity schema control date is stale")
    require(schema.get("canonical_node_source_id") == "PROCEEDINGS_MASTER_REGISTER", "schema canonical source identity changed")
    require(
        schema.get("specialist_context_sources")
        == [
            "assets/data/treasury-transparency-7-2026-v1.json",
            "assets/data/fiscalia-response-correspondence.json",
        ],
        "schema specialist context/source registry mismatch",
    )
    require(required_views <= set(schema.get("required_views", [])), "schema required views missing")
    require(required_views <= set(schema.get("implemented_public_views", {})), "schema runtime mappings missing")
    implemented_views = schema.get("implemented_public_views", {})
    require("26 source-controlled material clusters" in implemented_views.get("CONVERGENCE_CLUSTER", "") and "1 source-controlled corridor" in implemented_views.get("CONVERGENCE_CLUSTER", ""), "schema convergence-view denominator or corridor disclosure is stale")
    require(
        f"shared-proposition membership remains {CURRENT_CASE_PRISM_EXACT_COVERED} of {CURRENT_PUBLIC_EXACT}"
        in implemented_views.get("FRAGMENTATION_AUDIT", "")
        and f"{CURRENT_CASE_PRISM_EXACT_UNCOVERED} explicit no-coordinate gaps"
        in implemented_views.get("FRAGMENTATION_AUDIT", ""),
        "schema fragmentation-view content-gap denominator is stale",
    )
    require(set(schema.get("case_prism_cell_statuses", [])) == statuses, "schema relationship vocabulary mismatch")
    schema_principles = schema.get("principles", {})
    require(
        schema_principles.get(
            "finite_test_dependencies_contrary_records_and_consequences_are_file_specific"
        )
        is True
        and schema_principles.get(
            "recorded_custodian_or_organ_does_not_establish_competence_or_duty"
        )
        is True
        and schema_principles.get(
            "finite_test_family_uses_record_type_before_mixed_stream_substrings"
        )
        is True
        and schema_principles.get(
            "contrary_explanation_is_hypothetical_and_does_not_attribute_an_act_to_recorded_candidate"
        )
        is True
        and schema_principles.get(
            "every_institutional_axis_requires_source_basis_and_limitation"
        )
        is True
        and schema_principles.get(
            "every_positive_institutional_axis_cites_the_episode_field_that_supports_its_grade"
        )
        is True
        and schema_principles.get("referral_is_independent_from_transmission")
        is True
        and schema_principles.get(
            "fiscalia_material_related_files_related_assets_and_examined_corpus_are_separate"
        )
        is True,
        "schema omits the substantive finite-test/Fiscalía separation rules",
    )
    required_matrix_fields = {
        "master_id",
        "reference",
        "origin_office",
        "current_custodian",
        "date_or_period",
        "is_proceeding",
        "record_type",
        "source_status",
        "profile_status",
        "received_or_known.en",
        "received_or_known.es",
        "material_allegations_evidence",
        "material_received",
        "material_received_status",
        "material_inventory_gap.en",
        "material_inventory_gap.es",
        "related_direct_master_ids",
        "related_context_master_ids",
        "related_assets",
        "related_assets_status",
        "related_assets_gap.en",
        "related_assets_gap.es",
        "transmission_status",
        "referral_status",
        "what_was_referred.en",
        "what_was_referred.es",
        "registration_status",
        "file_incorporation_status",
        "recipient_attribution_status",
        "substantive_examination_status",
        "what_was_actually_examined.en",
        "what_was_actually_examined.es",
        "decision_use_status",
        "institutional_response.en",
        "institutional_response.es",
        "cross_file_acknowledgement_status",
        "unitary_acknowledgement_status",
        "strongest_contrary.en",
        "strongest_contrary.es",
        "unanswered_or_source_gap.en",
        "unanswered_or_source_gap.es",
        "institutional_axis_basis",
        "boundary_en",
        "boundary_es",
    }
    require(
        set(schema.get("fiscalia_office_file_matrix_required_fields", []))
        == required_matrix_fields,
        "schema Fiscalía substantive column contract is incomplete",
    )
    require(schema.get("implementation_contract", {}).get("bilingual_evidence_status_catalog_required") is True, "schema bilingual evidence-status requirement missing")
    require(schema.get("implementation_contract", {}).get("independent_case_prism_generation_seed_required") is True, "schema independent generation-seed requirement missing")
    implementation_contract = schema.get("implementation_contract", {})
    exact_contract = {
        "public_record_trace_denominator": CURRENT_PUBLIC_RECORDS,
        "exact_interlinkability_public_asset_schema_version": "1.1.0",
        "canonical_exact_proceeding_denominator": CURRENT_CANONICAL_EXACT,
        "public_exact_proceeding_denominator": CURRENT_PUBLIC_EXACT,
        "private_exact_proceeding_excluded_denominator": CURRENT_PRIVATE_EXACT,
        "public_exact_disposition_denominator": CURRENT_PUBLIC_EXACT,
        "exact_direct_relationship_pair_denominator": len(expected_direct_pairs),
        "exact_direct_relationship_source_verified_pair_denominator": source_verified_pair_count,
        "exact_direct_relationship_source_reported_pending_pair_denominator": source_reported_pending_pair_count,
        "exact_direct_source_assertion_denominator": len(actual_source_assertions),
        "exact_direct_source_verified_assertion_denominator": source_verified_assertion_count,
        "exact_direct_source_reported_pending_assertion_denominator": source_reported_pending_assertion_count,
        "material_context_cluster_denominator": len(context_clusters),
        "case_prism_exact_proceeding_covered_denominator": len(prism_exact_covered_ids),
        "case_prism_exact_proceeding_uncovered_denominator": len(prism_exact_uncovered_ids),
        "decision_dependency_exact_coverage_status": (
            f"VERIFIED_{CURRENT_PUBLIC_EXACT}_OF_{CURRENT_PUBLIC_EXACT}"
        ),
        "decision_dependency_exact_coverage_scope": "PUBLIC_EXACT_FILE_FINITE_TEST_REGISTER",
        "shared_case_prism_proposition_membership_coverage_status": (
            f"GAP_{CURRENT_CASE_PRISM_EXACT_COVERED}_OF_{CURRENT_PUBLIC_EXACT}"
        ),
        "shared_case_prism_proposition_membership_coverage_scope": "SHARED_PROPOSITION_MATRIX_ONLY",
        "cell_treatment_source_coverage_status": "GAP_PROPOSITION_LEVEL_SOURCES_ONLY",
        "fragmentation_selector_coverage_status": (
            f"VERIFIED_{CURRENT_PUBLIC_EXACT}_OF_{CURRENT_PUBLIC_EXACT}"
        ),
        "fragmentation_content_coverage_status": (
            f"VERIFIED_{CURRENT_PUBLIC_EXACT}_OF_{CURRENT_PUBLIC_EXACT}"
            "_EXACT_FILE_ISOLATION_AUDIT"
        ),
        "bilingual_specific_next_source_denominator": CURRENT_PUBLIC_EXACT,
        "bilingual_specific_next_source_coverage_status": (
            f"VERIFIED_{CURRENT_PUBLIC_EXACT}_OF_{CURRENT_PUBLIC_EXACT}"
        ),
        "exact_proceeding_full_finite_test_denominator": CURRENT_PUBLIC_EXACT,
        "exact_proceeding_full_finite_test_coverage_status": (
            f"VERIFIED_{CURRENT_PUBLIC_EXACT}_OF_{CURRENT_PUBLIC_EXACT}"
        ),
        "exact_file_decision_dependency_actionability_coverage_status": (
            f"VERIFIED_{CURRENT_PUBLIC_EXACT}_OF_{CURRENT_PUBLIC_EXACT}"
        ),
        "recorded_candidate_authority_status": "NOT_COMPETENCE_OR_DUTY",
        "finite_test_family_counts": EXPECTED_FINITE_TEST_FAMILY_COUNTS,
        "receipt_knowledge_classification_denominator": CURRENT_PUBLIC_EXACT,
        "receipt_knowledge_classification_coverage_status": (
            f"VERIFIED_{CURRENT_PUBLIC_EXACT}_OF_{CURRENT_PUBLIC_EXACT}"
            "_POSITIVE_EVIDENCE_SEPARATELY_COUNTED"
        ),
        "receipt_knowledge_axis_provenance_denominator": CURRENT_PUBLIC_EXACT,
        "receipt_knowledge_axis_provenance_coverage_status": (
            "VERIFIED_97_OF_97_WITH_STATUS_BASIS_LIMITATION_AND_SOURCE"
        ),
        "actor_specific_knowledge_receipt_trace_status": (
            f"MODELLED_{CURRENT_PUBLIC_EXACT}_OF_{CURRENT_PUBLIC_EXACT}"
            "_WITH_EXPLICIT_NOT_ESTABLISHED_STATES"
        ),
        "fiscalia_public_master_row_denominator": CURRENT_FISCALIA_OFFICE_FILE_RECORDS,
        "fiscalia_exact_proceeding_row_denominator": CURRENT_FISCALIA_EXACT_RECORDS,
        "fiscalia_unverified_reference_row_denominator": CURRENT_FISCALIA_UNRESOLVED_RECORDS,
        "fiscalia_office_file_matrix_coverage_status": (
            "VERIFIED_24_OF_24_WITH_INDEPENDENT_MATERIAL_DIRECT_CONTEXT_ASSET_"
            "REFERRAL_EXAMINATION_RESPONSE_ACKNOWLEDGEMENT_CONTRARY_AND_GAP_COLUMNS"
        ),
        "fiscalia_referral_transmission_separation_status": "VERIFIED_INDEPENDENT_GRADES",
        "fiscalia_axis_provenance_status": "VERIFIED_NINE_AXES_PER_PROFILE_OR_EXPLICIT_GAP",
        "fiscalia_matrix_profiled_row_denominator": CURRENT_FISCALIA_PROFILED_MATRIX_RECORDS,
        "fiscalia_matrix_profiled_row_coverage_status": "VERIFIED_8_PROFILED_16_EXPLICIT_GAPS",
        "fiscalia_source_controlled_episode_profile_denominator": CURRENT_FISCALIA_RESPONSE_EPISODES,
        "fiscalia_episode_profiles_outside_matrix_denominator": 1,
        "fiscalia_episode_profile_outside_matrix_master_id": "GC-CRI-008",
        "fiscalia_source_controlled_episode_profile_coverage_status": "VERIFIED_9_OF_9",
        "exact_id_master_trace_isolation_route_coverage_status": "VERIFIED_97_OF_97",
        "exact_id_to_dossier_source_route_coverage_status": (
            "MASTER_TRACE_ISOLATION_VERIFIED_97_OF_97_"
            "DEDICATED_NARRATIVE_DOSSIER_PARTIAL_UNCLAIMED"
        ),
        "stable_exact_trace_fragment": "#trace-proceeding=<Master_ID>",
        "stable_exact_isolation_fragment": "#isolation-test=<Master_ID>",
        "aggregate_reference_excluded_from_exact_selection": "GC-APP-007",
    }
    for field, expected in exact_contract.items():
        require(implementation_contract.get(field) == expected, f"schema implementation contract mismatch: {field}")
    require(implementation_contract.get("material_context_types") == ["RECORDED_CONNECTION", "SOURCE_CONTROLLED_CORRIDOR", "CASE_PRISM_PROPOSITION"], "schema material context types changed")
    require(implementation_contract.get("taxonomy_only_context_types") == ["STREAM", "GEOGRAPHY", "CHRONOLOGY"], "schema taxonomy-only context boundary changed")
    require(
        implementation_contract.get("classification_completion_may_not_upgrade_positive_evidence") is True
        and implementation_contract.get("finite_test_structural_boilerplate_may_not_count_as_file_specific_actionability") is True
        and implementation_contract.get("dedicated_narrative_dossier_coverage_may_not_be_inferred_complete") is True,
        "schema does not separate model completeness from positive evidence/dossier completion",
    )

    lifecycle_denominator = lifecycle.get("implementation_denominator", {})
    lifecycle_completion = lifecycle.get("completion_denominator", {})
    require(lifecycle.get("current_state") == "LIVE_VERIFIED", "interlinkability lifecycle is not LIVE_VERIFIED")
    require(lifecycle.get("state") == "LIVE_VERIFIED_WITH_ACCEPTED_PUBLICATION_BOUNDARY_GAP", "interlinkability qualified lifecycle state changed")
    require(lifecycle.get("merge_sha") == "e13652bb8b3f51dd050c431a58e2bd70b83f5676", "interlinkability closeout merge SHA changed")
    require(lifecycle.get("deployment_evidence", {}).get("run_id") == 33342771113, "interlinkability Pages evidence changed")
    require(lifecycle.get("verification", {}).get("live_http_readback") is True, "interlinkability live readback is not recorded")
    require(lifecycle.get("verification", {}).get("deletion_safe") is False, "interlinkability incorrectly claims deletion safety")
    require(
        lifecycle_denominator.get("public_records_traceable")
        == HISTORICAL_30AUG_PUBLIC_RECORDS,
        "historical 30-Aug lifecycle public trace denominator changed",
    )
    require(
        lifecycle_denominator.get("public_exact_proceedings")
        == lifecycle_denominator.get("public_exact_dispositions")
        == HISTORICAL_30AUG_PUBLIC_EXACT,
        "historical 30-Aug lifecycle exact interlink denominator changed",
    )
    require(
        lifecycle_denominator.get("direct_procedural_pairs")
        == HISTORICAL_30AUG_DIRECT_PAIRS,
        "historical 30-Aug lifecycle direct-pair denominator changed",
    )
    require(
        lifecycle_denominator.get("direct_procedural_pairs_source_verified")
        == HISTORICAL_30AUG_VERIFIED_DIRECT_PAIRS
        and lifecycle_denominator.get(
            "direct_procedural_pairs_source_reported_primary_pending"
        )
        == HISTORICAL_30AUG_PENDING_DIRECT_PAIRS,
        "historical 30-Aug lifecycle direct-pair evidence grades changed",
    )
    require(
        lifecycle_denominator.get("direct_source_assertions")
        == HISTORICAL_30AUG_DIRECT_ASSERTIONS,
        "historical 30-Aug lifecycle direct-assertion denominator changed",
    )
    require(
        lifecycle_denominator.get("direct_source_assertions_verified")
        == HISTORICAL_30AUG_VERIFIED_DIRECT_ASSERTIONS
        and lifecycle_denominator.get(
            "direct_source_assertions_source_reported_primary_pending"
        )
        == HISTORICAL_30AUG_PENDING_DIRECT_ASSERTIONS,
        "historical 30-Aug lifecycle direct-assertion evidence grades changed",
    )
    require(
        lifecycle_denominator.get("controlled_material_context_clusters")
        == HISTORICAL_30AUG_CONTEXT_CLUSTERS
        and lifecycle_denominator.get("source_controlled_context_corridors") == 1,
        "historical 30-Aug lifecycle material-context denominator changed",
    )
    require(
        lifecycle_completion.get("decision_dependency_coverage") == "GAP_26_OF_85",
        "historical 30-Aug lifecycle decision-dependency coverage changed",
    )
    require(lifecycle_completion.get("contextual_convergence_edges") == "VERIFIED_26_CONTROLLED_CLUSTERS_INCLUDING_1_SOURCE_CONTROLLED_CORRIDOR", "lifecycle contextual-convergence denominator mismatch")
    require(lifecycle_completion.get("cell_treatment_source_coverage") == "GAP_PROPOSITION_LEVEL_SOURCES_ONLY", "lifecycle overstates cell-level source coverage")
    require(lifecycle_completion.get("actor_specific_knowledge_receipt_trace") == "GAP_NOT_MODELLED", "lifecycle overstates actor-specific knowledge/receipt tracing")
    require(lifecycle_completion.get("exact_id_to_dossier_source_route_coverage") == "GAP_DENOMINATOR_NOT_ESTABLISHED", "lifecycle overstates exact-ID dossier/source routing")
    require(
        lifecycle_completion.get("exact_proceeding_full_finite_test_coverage")
        == "GAP_0_OF_85_AT_DISPOSITION_LEVEL",
        "historical 30-Aug lifecycle finite-actionability status changed",
    )
    require(lifecycle_completion.get("tracked_operational_source_unpublishing") == "GAP_ACCEPTED_PUBLICLY_ACCESSIBLE", "accepted operational-source exposure gap changed")
    require(lifecycle_completion.get("deletion_safe_continuity") == "GAP_ACCEPTED_OPERATIONAL_CSV_PUBLICATION_BOUNDARY", "deletion-safe boundary changed")
    boundary_gap = lifecycle.get("accepted_publication_boundary_gap", {})
    require(boundary_gap.get("status") == "UNRESOLVED_ACCEPTED_FOR_THIS_RELEASE", "accepted publication-boundary gap state changed")
    require(boundary_gap.get("resource") == "archive/PROCEEDINGS_MASTER_REGISTER.csv", "accepted publication-boundary resource changed")
    require(boundary_gap.get("observed_http_status") == 200, "accepted publication-boundary HTTP observation changed")
    require(boundary_gap.get("release_tree_sha256") == "267b37574a8cfb96af258d0dfdbd694d506a9c03572b42f3fb1c10376516d294", "accepted release-tree CSV hash changed")
    require(boundary_gap.get("deletion_safe") is False, "accepted publication-boundary gap cannot be deletion-safe")
    recovery_companions = {
        "archive/GC_548_2023_PLAZA2_T1_CARET_CONTINUITY_CONTROL_30AUG2026.md",
        "archive/DP3205_2014_ARRECIFE_SOURCE_TRANSLATION_AUTHORITY_ALLEGATIONS_CONTROL_30AUG2026.md",
        "archive/ARRECIFE_4009_2015_CARET_INTERLINK_CONTROL_30AUG2026.md",
        "archive/ARRECIFE_1103_1132_1010_804_CARET_INTERLINK_CONTROL_30AUG2026.md",
        "archive/TESORO_TRANSPARENCIA_7_2026_CONTINUITY_AUDIT_28AUG2026.md",
        "publication-manifests/master-proceedings-publication-20260830.json",
        "publication-manifests/gc-548-2023-plaza2-t1-caret-20260830.json",
        "publication-manifests/dp3205-2014-arrecife-caret-interlink-20260830.json",
        "publication-manifests/arrecife-4009-2015-caret-interlink-20260830.json",
        "publication-manifests/arrecife-1103-2018-caret-interlink-20260830.json",
        "publication-manifests/treasury-transparency-7-2026-20260830.json",
        "assets/data/treasury-transparency-7-2026-v1.json",
        "scripts/audit_arrecife_1103_caret_interlink.py",
        ".github/workflows/audit-arrecife-1103-caret-interlink.yml",
        "en/arrecife-1103-2018-procedural-lineage/index.html",
        "es/arrecife-1103-2018-cadena-procesal/index.html",
    }
    require(recovery_companions <= set(lifecycle.get("expected_source_files", [])), "lifecycle recovery set omits a proceeding companion control")

    # The 30-August manifest above remains immutable live evidence.  This new
    # release has its own lifecycle and is intentionally only prepared until
    # exact-head CI, merge, Pages and live readback produce later evidence.
    require(
        current_lifecycle.get("schema") == "por-derecho.publication-manifest.v1"
        and current_lifecycle.get("publication_id")
        == "PD-SP-CASE-PRISM-EXACT-ACTIONABILITY-20260831-01"
        and current_lifecycle.get("control_date") == "2026-08-31"
        and current_lifecycle.get("source_base_sha")
        == "a54c74b204d6f7596d3da9e41af569c08c676736",
        "current substantive-gap lifecycle identity/source base is stale",
    )
    require(
        current_lifecycle.get("controlled_artifact_versions")
        == {
            "proceedings_interconnectivity_schema": "1.7.0",
            "proceedings_interlinkability_projection": "1.1.0",
        },
        "current substantive-gap lifecycle does not pin schema/data versions 1.7.0/1.1.0",
    )
    require(
        current_lifecycle.get("current_state") == "PREPARED_PENDING_MERGE"
        and current_lifecycle.get("state")
        == "PREPARED_PENDING_MERGE_WITH_ACCEPTED_PUBLICATION_BOUNDARY_GAP",
        "current substantive-gap lifecycle must remain PREPARED_PENDING_MERGE before publication",
    )
    current_baseline = current_lifecycle.get("baseline_denominator", {})
    expected_current_baseline = {
        "canonical_rows": CURRENT_CANONICAL_RECORDS,
        "public_rows": CURRENT_PUBLIC_RECORDS,
        "canonical_exact_proceedings": CURRENT_CANONICAL_EXACT,
        "public_exact_proceedings": CURRENT_PUBLIC_EXACT,
        "private_exact_excluded": CURRENT_PRIVATE_EXACT,
        "direct_relationship_pairs": CURRENT_DIRECT_PAIRS,
        "direct_relationship_pairs_source_verified": CURRENT_VERIFIED_DIRECT_PAIRS,
        "direct_relationship_pairs_source_reported_primary_pending": CURRENT_PENDING_DIRECT_PAIRS,
        "direct_source_assertions": CURRENT_DIRECT_ASSERTIONS,
        "direct_source_assertions_verified": CURRENT_VERIFIED_DIRECT_ASSERTIONS,
        "direct_source_assertions_source_reported_primary_pending": CURRENT_PENDING_DIRECT_ASSERTIONS,
        "material_context_clusters": len(context_clusters),
        "shared_case_prism_propositions": len(props),
        "parallel_lanes": len(lanes),
        "explicit_matrix_coordinates": len(cells),
        # Immutable baseline of the already-merged substantive-gap lifecycle.
        # The later Fiscalía interconnectivity projection expands P05 without
        # rewriting that historical publication manifest.
        "case_prism_exact_proceedings_with_shared_proposition_coordinate": 26,
        "case_prism_exact_proceedings_without_shared_proposition_coordinate": 71,
        "public_master_fiscalia_rows": CURRENT_FISCALIA_OFFICE_FILE_RECORDS,
        "public_master_fiscalia_exact_rows": CURRENT_FISCALIA_EXACT_RECORDS,
        "public_master_fiscalia_unverified_reference_rows": CURRENT_FISCALIA_UNRESOLVED_RECORDS,
        "source_controlled_fiscalia_response_episodes": CURRENT_FISCALIA_RESPONSE_EPISODES,
        "fiscalia_matrix_rows_with_episode_profiles": CURRENT_FISCALIA_PROFILED_MATRIX_RECORDS,
        "judicial_file_episode_profiles_outside_fiscalia_matrix": 1,
    }
    require(
        all(current_baseline.get(field) == value for field, value in expected_current_baseline.items()),
        "historical substantive-gap manifest baseline denominator is incomplete or stale",
    )
    current_targets = current_lifecycle.get("target_structural_coverage", {})
    require(
        current_targets.get("public_exact_dispositions") == "97_OF_97"
        and current_targets.get("exact_proceeding_full_finite_tests") == "97_OF_97"
        and current_targets.get("exact_file_specific_unique_finite_test_fields")
        == "97_OF_97"
        and current_targets.get("exact_file_decision_dependency_actionability") == "97_OF_97"
        and current_targets.get("exact_file_actionability_content_contract")
        == "UNIQUE_DECISION_DEPENDENCY_CONTRARY_CONFIRMED_REFUTED_AND_SOURCE_ROUTE_GAP"
        and current_targets.get("finite_test_family_taxonomy")
        == "CANONICAL_RECORD_TYPE_PRECEDES_MIXED_STREAM_SUBSTRING"
        and current_targets.get("finite_test_family_counts")
        == EXPECTED_FINITE_TEST_FAMILY_COUNTS
        and current_targets.get("institutional_receipt_knowledge_classifications") == "97_OF_97"
        and current_targets.get("institutional_nine_axis_provenance")
        == "97_OF_97_WITH_INDEPENDENT_STATUS_BASIS_LIMITATION_AND_SOURCE"
        and current_targets.get("master_trace_isolation_route_dispositions") == "97_OF_97"
        and current_targets.get("fiscalia_office_file_matrix") == "24_OF_24"
        and current_targets.get("fiscalia_office_file_matrix_composition")
        == "21_EXACT_PLUS_3_UNRESOLVED_REFERENCES"
        and current_targets.get("fiscalia_office_file_matrix_profiled_rows") == "8_OF_24"
        and current_targets.get("fiscalia_response_episodes")
        == "9_OF_9_INCLUDING_8_MATRIX_ROWS_PLUS_1_JUDICIAL_FILE_PROFILE"
        and current_targets.get("shared_proposition_coordinate_coverage") == "26_OF_97"
        and current_targets.get("shared_proposition_no_coordinate_gap") == "71_OF_97"
        and current_targets.get("dedicated_narrative_dossier_coverage")
        == "PARTIAL_SEPARATE_POSITIVE_COUNT",
        "current substantive-gap manifest conflates structural coverage with positive evidence",
    )
    current_meaning = current_lifecycle.get("coverage_meaning", {})
    require(
        all(
            token in current_meaning.get("finite_test", "")
            for token in (
                "exact-file-specific",
                "Generic registry-maintenance",
                "canonical public-record route",
                "primary-source route or route gap",
                "only a candidate",
                "may not be treated as legally competent, empowered or obliged to act",
                "conditional on exact competence and a lawful route",
                "contrary explanation remains hypothetical",
                "Canonical record type precedes a mixed Stream substring",
            )
        )
        and all(
            token in current_meaning.get("receipt_knowledge", "")
            for token in (
                "nine institutional axes",
                "status",
                "basis",
                "limitation",
                "Transmission and referral are independent",
                "exact episode field that supports that axis",
                "episode-and-axis overrides",
            )
        )
        and "non-positive" in current_meaning.get("actor_specific", "")
        and all(
            token in current_meaning.get("fiscalia", "")
            for token in (
                "Twenty-four",
                "21 exact and three unresolved references",
                "direct/context proceeding",
                "related-asset-gap",
                "actually-examined",
            )
        ),
        "current substantive-gap manifest does not define the substantive coverage meaning",
    )
    current_boundaries = set(current_lifecycle.get("evidential_boundaries", []))
    require(
        {
            "GENERIC_REGISTRY_MAINTENANCE_BOILERPLATE_IS_NOT_EXACT_FILE_ACTIONABILITY",
            "TRANSMISSION_AND_REFERRAL_REQUIRE_INDEPENDENT_GRADES",
            "EVERY_INSTITUTIONAL_AXIS_REQUIRES_ITS_OWN_STATUS_BASIS_LIMITATION_AND_SOURCE",
            "ACTOR_SPECIFIC_RECEIPT_OR_KNOWLEDGE_REQUIRES_ACTOR_SPECIFIC_EVIDENCE",
        }
        <= current_boundaries,
        "current substantive-gap manifest omits a required evidential boundary",
    )
    current_validation_required = set(
        current_lifecycle.get("validation", {}).get("required", [])
    )
    require(
        {
            "schema 1.7.0 and interlinkability projection 1.1.0",
            "97/97 exact-file-specific unique finite-test field sets including decision dependency, contrary explanation, confirmed/refuted consequences, canonical public-record route and explicit primary-source route gap",
            "record-type-first finite family taxonomy with 26 administrative, 19 civil, 11 criminal, 21 Fiscalia, one ombudsman, eight professional, seven regulatory and four tax/contentious files",
            "hypothetical contrary explanations and competence-conditional consequences that attribute no act or duty to a recorded candidate",
            "97/97 nine-axis provenance records with independent status, basis, limitation and source/source-gap; transmission and referral independently graded; actor-specific receipt/knowledge non-positive absent actor-specific evidence",
            "episode-and-axis source-field support for every positive institutional grade",
            "24/24 Fiscalia rows with separate material allegations/evidence, received-inventory gap, direct/context proceedings, related assets/gap, referred, actually examined, response, cross-file, unitary, contrary and unanswered controls",
        }
        <= current_validation_required,
        "current substantive-gap manifest validation list is not fail-closed on substantive coverage",
    )
    for token in (
        "schema `1.7.0`",
        "projection `1.1.0`",
        "exact-file-specific decision dependency",
        "97 / 97 nine-axis provenance",
        "Transmission and referral remain independent",
        "generic registry-maintenance boilerplate",
        "No confirmed/refuted consequence may treat the recorded candidate as legally",
        "contrary explanation remains hypothetical",
        "Family assignment follows canonical record",
        "Every positive institutional grade must cite the exact episode field",
        "allegations/evidence",
        "what was referred",
        "examined, response",
    ):
        require(
            token in current_continuity,
            f"current substantive-gap continuity record omits control: {token}",
        )
    current_boundary_gap = current_lifecycle.get("accepted_publication_boundary_gap", {})
    require(
        current_boundary_gap.get("status") == "UNRESOLVED_ACCEPTED_FOR_THIS_RELEASE"
        and current_boundary_gap.get("resource")
        == "archive/PROCEEDINGS_MASTER_REGISTER.csv"
        and current_boundary_gap.get("last_recorded_http_status") == 200
        and current_boundary_gap.get("current_source_base_sha256")
        == hashlib.sha256(
            (ROOT / "archive/PROCEEDINGS_MASTER_REGISTER.csv").read_bytes()
        ).hexdigest()
        and current_boundary_gap.get("post_deployment_http_and_hash_verification")
        == "PENDING"
        and current_boundary_gap.get("intended_live_surface") is False
        and current_boundary_gap.get("included_in_live_urls") is False
        and current_boundary_gap.get("included_in_live_markers") is False
        and current_boundary_gap.get("deletion_safe") is False,
        "current accepted CSV publication-boundary observation is incomplete or stale",
    )
    require(
        current_lifecycle.get("validation", {}).get("status")
        == "PENDING_EXACT_HEAD_CI"
        and current_lifecycle.get("pull_request") is None
        and current_lifecycle.get("reviewed_head_sha") is None
        and current_lifecycle.get("reviewed_tree_sha") is None
        and current_lifecycle.get("merge_sha") is None
        and current_lifecycle.get("deployment_evidence") is None
        and current_lifecycle.get("live_urls") == []
        and current_lifecycle.get("live_markers") == {},
        "current lifecycle claims publication evidence before PR/CI/merge/deployment",
    )
    current_required_paths = {
        "assets/data/proceedings-interlinkability-v1.json",
        "assets/data/proceedings-interconnectivity-schema-v1.json",
        "assets/data/fiscalia-response-correspondence.json",
        "assets/proceedings-interconnectivity-map-20260830.js",
        "scripts/build_proceedings_interlinkability_v1.py",
        "scripts/audit_proceedings_interconnectivity_map.py",
        "scripts/smoke_proceedings_case_prism.mjs",
        "publication-manifests/all-proceedings-interlinkability-20260830.json",
        "publication-manifests/case-prism-substantive-gap-closure-20260831.json",
        "docs/deletion-audits/2026-08-31-case-prism-substantive-gap-closure-continuity.md",
    }
    require(
        current_required_paths <= set(current_lifecycle.get("expected_source_files", []))
        and current_lifecycle.get("continuity_record")
        == "docs/deletion-audits/2026-08-31-case-prism-substantive-gap-closure-continuity.md",
        "current lifecycle omits a substantive-gap source or continuity control",
    )

    renderer_tokens = {
        "pdim-prism-table": "decision matrix", "pdim-swimlane": "stable swimlane", "data-lane-heading": "lane headings",
        "data-isolation-id": "exact-file isolation", "data-isolation-restore": "restore control", "sourceLinks": "source links",
        "contrary_record": "contrary record", "decision_dependency": "decision dependency", "actionability": "actionability",
        "representation_lineage_status": "representation gaps", "#case-prism": "hash activation",
        "role=\"tabpanel\"": "tab panel", "role=\"tab\"": "semantic tabs", "prismUnavailable": "degraded state",
        "sourceScope": "proposition-level source boundary", "outsideSelected": "accessible suppressed state",
        "evidenceStatusLabel": "bilingual evidence status",
        "revealActivePanel": "deep-link panel reveal", "mapped || 'map'": "hash back-navigation restore",
        "addEventListener('input', () => draw())": "safe filter redraw",
        "assets/data/proceedings-master-public-v1.json": "minimised public proceedings projection",
        "assets/data/proceedings-interlinkability-v1.json": "controlled interlinkability registry",
        "data-isolation-reconnection": "selected-file reconnection surface",
        "data-isolation-direct": "direct-edge reconnection section",
        "data-isolation-context": "controlled-context reconnection section",
        "data-isolation-unresolved": "independent/gap reconnection section",
        "data-interlink-disposition": "controlled node disposition",
        "#trace-proceeding=": "stable exact trace deep link",
        "#isolation-test=": "stable exact isolation deep link",
        "direct_relationship_source_verified_pair_count": "direct-edge evidence-grade denominator",
        "if (initialHash.canonicalize) replaceActiveHash();": "cold-load invalid-isolation canonicalisation",
        "if (parsed.canonicalize) replaceActiveHash();": "hashchange invalid-isolation canonicalisation",
        "data-finite-test-coverage": "finite-test audit/positive-evidence denominator",
        "data-audit-count": "finite-test audit count",
        "data-positive-evidence-count": "separate positive-evidence count",
        "data-finite-test-panel": "per-file finite-test panel",
        "data-finite-test-status": "finite-test model status",
        "data-finite-question": "finite question",
        "data-finite-source-status": "finite-test source status",
        "data-finite-source-link": "finite-test public source link",
        "data-finite-source-gap": "finite-test source-route gap",
        "data-finite-contrary": "strongest contrary explanation",
        "data-finite-competent-organ": "competent-organ candidate",
        "data-competent-organ-status": "competent-organ source status",
        "data-finite-decision-dependency": "exact-file decision dependency",
        "data-finite-related": "finite-test related-file surface",
        "data-finite-related-direct": "finite-test direct one-hop list",
        "data-finite-related-context": "finite-test contextual one-hop list",
        "data-finite-if-confirmed": "confirmed consequence",
        "data-finite-if-refuted": "refuted consequence",
        "data-institutional-receipt-treatment": "institutional receipt/treatment surface",
        "data-receipt-axis": "independent institutional axes",
        "data-${axis.key}-status": "per-axis status token",
        "data-axis-status": "per-axis rendered status",
        "data-axis-basis-status": "per-axis basis status",
        "data-axis-basis-kind": "per-axis basis kind",
        "data-receipt-axis-basis": "per-axis bilingual basis disclosure",
        "data-receipt-axis-basis-kind-value": "per-axis basis-kind value",
        "data-receipt-axis-basis-statement": "per-axis localized basis statement",
        "data-receipt-axis-limitation": "per-axis localized limitation",
        "data-receipt-axis-source-provenance": "per-axis source provenance value",
        "const disclosureName = `${copy.axisBasis} · ${copy[axis.label]}`": "axis-specific finite disclosure name",
        "aria-controls=\"${esc(disclosureContentId)}\"": "axis-scoped finite disclosure control",
        "aria-live=\"polite\" aria-atomic=\"false\"": "selected-isolation live announcement",
        "institutional_axis_basis": "nine-axis basis/provenance source",
        "finiteAxisComplete": "nine-axis runtime completeness gate",
        "canonicalLocation:'institutional_axes'": "six-core canonical status location",
        "canonicalLocation:'basis_status'": "material/referral canonical status location",
        "canonicalLocation:'receipt_root'": "cross-file canonical status location",
        "model.canonicalStatusPresent": "canonical-location fail-closed gate",
        "hasNineAxisProvenance": "nine-axis fail-closed finite-test status",
        "finiteToken(basis.status) === model.token": "axis grade and basis-status equality",
        "basis.basis_en": "English axis basis requirement",
        "basis.basis_es": "Spanish axis basis requirement",
        "basis.limitation_en": "English axis limitation requirement",
        "basis.limitation_es": "Spanish axis limitation requirement",
        "norm(basis.source.kind)": "axis provenance kind requirement",
        "norm(basis.source.record_id)": "axis provenance record-ID requirement",
        "provenanceLabel(source)": "per-axis source provenance",
        "data-receipt-event": "source-controlled institutional event",
        "data-actor-specific-knowledge": "separate actor-specific evidence surface",
        "data-personal-knowledge-status": "personal-knowledge evidence status",
        "data-actor-receipt-status": "actor-specific receipt status",
        "data-actor-source-status": "actor-specific source status",
        "data-actor-profile": "actor/source profile",
        "finiteToken(item.knowledge_status) || 'NOT_ESTABLISHED'": "fail-closed actor-profile knowledge status",
        "data-fiscalia-office-file-matrix": "Fiscalía cross-office/file matrix",
        "data-row-count": "Fiscalía matrix row denominator",
        "data-profiled-count": "Fiscalía matrix profiled-row denominator",
        "data-fiscalia-row": "Fiscalía office/file row",
    }
    for token, label in renderer_tokens.items():
        require(token in js, f"renderer missing {label}")
    require(
        "finiteToken(item.knowledge_status || item.status" not in js
        and "finiteToken(item.knowledge_status || item.evidence_status" not in js,
        "generic actor profile/source status can still be relabelled as personal knowledge",
    )
    for axis_key in (
        "transmission",
        "material-received",
        "referral",
        "registration",
        "file-incorporation",
        "recipient-attribution",
        "examination",
        "decision-use",
        "cross-file-acknowledgement",
    ):
        require(
            f"key:'{axis_key}'" in js,
            f"renderer missing independent {axis_key} receipt-axis token",
        )
    require("nonExactRelation" in master_js, "Master renderer lacks a non-exact relationship qualification")
    require("pdim-prism-dash" not in js, "renderer can emit unexplained dashes")
    require("data-isolation-lane" not in js, "aggregate-lane isolation remains")
    require("toUpperCase() === 'TRUE'" in js, "exact isolation admits unverified objects")
    require("archive/PROCEEDINGS_MASTER_REGISTER.csv" not in js, "renderer still downloads the operational canonical CSV")
    require("parseCsv" not in js, "renderer still carries client-side canonical CSV parsing")
    require(
        "return finiteToken(actor && actor.source_status);" in js
        and "norm(actor.boundary_en)" in js
        and "norm(actor.boundary_es)" in js,
        "renderer does not fail closed on the exact actor source token and bilingual actor boundary",
    )
    require(
        "values.push(finiteActor" not in js,
        "actor-specific source status can inflate the institutional positive-evidence denominator",
    )
    require(
        "item.evidence_status) || actorStatus" not in js,
        "actor profile can inherit source availability as personal knowledge",
    )
    require(
        "<summary>${esc(copy.axisBasis)}</summary>" not in js,
        "institutional-axis disclosures still use nine indistinguishable accessible names",
    )
    require(
        all(token in js for token in (
            "data-exact-decision-register",
            "data-exact-decision-entry",
            "data-exact-decision-dependency",
            "data-shared-proposition-count",
        )),
        "public exact-file Decision-Dependency Register is incomplete",
    )
    require("fallbackEdges" not in js, "renderer can infer a direct edge for a non-exact/unclassified node")
    require("if (cluster.context_type === 'CASE_PRISM_PROPOSITION')" in js and "linkedPrismPropIds.add(propositionId)" in js, "renderer does not bound a Case Prism cluster to its own proposition")
    require("['RECORDED_CONNECTION', 'SOURCE_CONTROLLED_CORRIDOR'].includes(cluster.context_type)" in js, "renderer does not reconnect both recorded Connections and source-controlled corridors")
    require("return cell.status === 'DIRECT' && cell.master_ids.some((id) => reconnectIds.has(id));" in js, "renderer lets a one-hop neighbour's contextual coordinate expand the isolation result")
    require("#trace-proceeding=${encodeURIComponent(r.Master_ID)}" in master_js, "Master Register lacks exact-ID trace links")
    require("#record-$1" in master_js and "linkMasterReferences(relation)" in master_js, "Master Register relations are not reciprocal row links")
    require(all(token in master_js for token in ("LZ-JUD-003", "LZ-APP-004", "arrecife-1103-2018-procedural-lineage", "arrecife-1103-2018-cadena-procesal")), "Master Register lacks the bilingual Arrecife 1103 lineage dossiers")
    require('id="record-${esc(r.Master_ID)}"' in master_js, "Master Register lacks stable exact-ID row anchors")
    require("archive/PROCEEDINGS_MASTER_REGISTER.csv" not in master_js and "assets/data/proceedings-master-public-v1.json" in master_js, "Master Register still consumes the operational canonical CSV")
    require('role="tabpanel" aria-live=' not in js and 'data-proceedings-map="20260830" aria-live=' not in en + es, "nested broad live regions remain")
    require(all(token in css for token in (".pdim-swimlane", ".pdim-isolation-map", ".pdim-dependency-grid", ".pdim-exact-decision-register", ".pdim-exact-decision-entry>summary{min-height:44px", ":focus-visible", "prefers-reduced-motion", ".pdim-axis-basis summary{min-height:44px}", ".pdim-axis-basis code{white-space:normal;overflow-wrap:anywhere;word-break:break-word}")), "Prism CSS/accessibility contract incomplete")
    require("json.loads(SEED.read_text" in builder and "json.loads(TARGET.read_text" not in builder, "Case Prism builder is not independent of its generated target")
    require("archive/PROCEEDINGS_CASE_PRISM_V1_SEED_30AUG2026.json" in builder, "Case Prism builder seed path missing")
    require(all(field not in js for field in ("Primary_Source_Anchor", "Repo_Canonical_Source", "Notes")), "renderer exposes non-public raw source fields")

    for page, label in [(en, "EN map"), (es, "ES map"), (en_master, "EN Master"), (es_master, "ES Master")]:
        require("public-authority-unitary-case-reconstruction" in page or "reconstruccion-unitaria-autoridades-publicas" in page, f"{label} lacks clean-room route")
    for page, label in ((en, "EN map"), (es, "ES map")):
        require("PROCEEDINGS_MASTER_REGISTER" in page and "assets/data/proceedings-master-public-v1.json" in page, f"{label} does not disclose the minimised public projection")
        require("archive/PROCEEDINGS_MASTER_REGISTER.csv" not in page, f"{label} exposes the operational canonical path")
    require("proceedings-map" in en_clean and "master-proceedings-register" in en_clean, "EN clean room lacks map/register links")
    require("mapa-procedimientos" in es_clean and "registro-maestro-procedimientos" in es_clean, "ES clean room lacks map/register links")
    for label, (page, master_ids) in institutional_feeders.items():
        for master_id in master_ids:
            require(f"#trace-proceeding={master_id}" in page, f"{label} lacks exact trace link for {master_id}")
            require(f"#isolation-test={master_id}" in page, f"{label} lacks exact isolation link for {master_id}")
    for label, page in general_institutional_feeders.items():
        require("#case-prism" in page and "#isolation-test" in page, f"{label} lacks Case Prism/isolation navigation")
        require("master-proceedings-register" in page or "registro-maestro-procedimientos" in page, f"{label} lacks Master Register navigation")
        require("public-authority-unitary-case-reconstruction" in page or "reconstruccion-unitaria-autoridades-publicas" in page, f"{label} lacks institutional clean-room navigation")

    # The identified material-route denominator is deliberately governed as a
    # closed set.  A route may either identify one controlled public record or
    # remain explicitly multi-file; it may not acquire a docket merely because
    # it sits beside a related narrative.
    def institutional_navigation_blocks(page: str, marker: str) -> list[str]:
        return [
            match.group(0)
            for match in re.finditer(
                rf'<(section|div|p)[^>]*{re.escape(marker)}[^>]*>.*?</\1>',
                page,
                flags=re.IGNORECASE | re.DOTALL,
            )
        ]

    def expected_route_tokens(path: str) -> tuple[str, str, str]:
        if path.startswith("es/"):
            return (
                "reconstruccion-unitaria-autoridades-publicas",
                "mapa-procedimientos/#case-prism",
                "registro-maestro-procedimientos",
            )
        return (
            "public-authority-unitary-case-reconstruction",
            "proceedings-map/#case-prism",
            "master-proceedings-register",
        )

    for path in INSTITUTIONAL_MULTI_FILE_ROUTES:
        page = read(path)
        blocks = institutional_navigation_blocks(page, 'data-institutional-navigation="material-route"')
        require(len(blocks) == 1, f"{path} must have exactly one material-route navigation block")
        if len(blocks) != 1:
            continue
        block = blocks[0]
        clean, prism, master = expected_route_tokens(path)
        require('data-navigation-scope="multi-file"' in block, f"{path} must remain explicitly multi-file")
        require(all(token in block for token in (clean, prism, master)), f"{path} lacks neutral clean-room/Prism/Master navigation")
        require('data-master-ids=' not in block, f"{path} invents a Master-ID mapping for a multi-file route")
        require(
            '#record-' not in block and '#trace-proceeding=' not in block and '#isolation-test=' not in block,
            f"{path} invents exact Master/trace/isolation navigation for a multi-file route",
        )

    for path, expected_ids in INSTITUTIONAL_EXACT_ROUTE_IDS.items():
        page = read(path)
        blocks = institutional_navigation_blocks(page, 'data-institutional-navigation="material-route"')
        require(len(blocks) == 1, f"{path} must have exactly one material-route navigation block")
        if len(blocks) != 1:
            continue
        block = blocks[0]
        clean, prism, master = expected_route_tokens(path)
        expected_value = " ".join(expected_ids)
        require('data-navigation-scope="exact-proceeding"' in block, f"{path} must declare exact-proceeding scope")
        require(f'data-master-ids="{expected_value}"' in block, f"{path} has an unapproved exact Master-ID mapping")
        require(set(expected_ids) <= exact_public_ids, f"{path} maps outside the public exact denominator")
        require(all(token in block for token in (clean, prism, master)), f"{path} lacks neutral clean-room/Prism/Master navigation")
        record_ids = set(re.findall(r'#record-([A-Z0-9-]+)', block))
        trace_ids = set(re.findall(r'#trace-proceeding=([A-Z0-9-]+)', block))
        isolation_ids = set(re.findall(r'#isolation-test=([A-Z0-9-]+)', block))
        require(record_ids == set(expected_ids), f"{path} has unapproved Master row anchors: {sorted(record_ids)}")
        require(trace_ids == set(expected_ids), f"{path} has unapproved trace anchors: {sorted(trace_ids)}")
        require(isolation_ids == set(expected_ids), f"{path} has unapproved isolation anchors: {sorted(isolation_ids)}")
        for master_id in expected_ids:
            require(f'#record-{master_id}' in block, f"{path} lacks Master row anchor for {master_id}")
            require(f'#trace-proceeding={master_id}' in block, f"{path} lacks exact trace link for {master_id}")
            require(f'#isolation-test={master_id}' in block, f"{path} lacks exact isolation link for {master_id}")

    for path, expected_ids in MATERIAL_DOSSIER_ROUTE_IDS.items():
        page = read(path)
        blocks = institutional_navigation_blocks(page, 'data-institutional-navigation="material-dossier"')
        require(len(blocks) == 1, f"{path} must have exactly one material-dossier navigation block")
        if len(blocks) != 1:
            continue
        block = blocks[0]
        clean, prism, master = expected_route_tokens(path)
        expected_value = " ".join(expected_ids)
        require(f'data-master-ids="{expected_value}"' in block, f"{path} has an unapproved material-dossier Master-ID mapping")
        require(set(expected_ids) <= exact_public_ids, f"{path} maps outside the public exact denominator")
        require(all(token in block for token in (clean, prism, master)), f"{path} lacks neutral clean-room/Prism/Master navigation")
        record_ids = set(re.findall(r'#record-([A-Z0-9-]+)', block))
        trace_ids = set(re.findall(r'#trace-proceeding=([A-Z0-9-]+)', block))
        isolation_ids = set(re.findall(r'#isolation-test=([A-Z0-9-]+)', block))
        require(record_ids == set(expected_ids), f"{path} has unapproved material-dossier Master row anchors: {sorted(record_ids)}")
        require(trace_ids == set(expected_ids), f"{path} has unapproved material-dossier trace anchors: {sorted(trace_ids)}")
        require(isolation_ids == set(expected_ids), f"{path} has unapproved material-dossier isolation anchors: {sorted(isolation_ids)}")
        for master_id in expected_ids:
            require(f'#record-{master_id}' in block, f"{path} lacks Master row anchor for {master_id}")
            require(f'#trace-proceeding={master_id}' in block, f"{path} lacks exact trace link for {master_id}")
            require(f'#isolation-test={master_id}' in block, f"{path} lacks exact isolation link for {master_id}")
    require("#case-prism" in en and "#case-prism" in es, "Case Prism CTA fragment missing")
    require(all(f'id="{anchor}"' in en and f'id="{anchor}"' in es for anchor in ("parallel-lanes", "isolation-test")), "deep-link anchors missing")
    require(all(f"proceedings-interconnectivity-map-20260830.{ext}?v=20260831e" in en and f"proceedings-interconnectivity-map-20260830.{ext}?v=20260831e" in es for ext in ("js", "css")), "Case Prism asset cache version not advanced to 20260831e")

    refs = ["RPL 2523/2025", "RPL 3304/2025", "RPL 3319/2025", "RPL 421/2026"]
    require(all(ref in institutional for ref in refs), "three-appellate-object correction missing")
    require("Do not describe `RPL 3319/2025` as the fees appeal" in institutional, "RPL 3319 fees correction missing")
    require("beginning → end" in gov and "end → beginning" in gov, "bidirectional governance missing")
    require("DIRECT PROCEDURAL EDGE" in gov and "CONTEXTUAL BRIDGE" in gov, "direct/context split missing")
    require("Fragmentation / atomisation audit" in gov, "fragmentation governance missing")
    require("Public renderer parity is a hard implementation denominator" in gov, "public renderer parity governance missing")
    require(all(token in gov for token in ("AUDITED", "INCOMPLETE", "For first-read institutional access")), "renderer-parity or first-read governance controls missing")
    require(all(word in ascan for word in ("Architecture", "Authority", "Attribution", "Audience", "Actionability")), "A-SCAN governance incomplete")
    require("does not prove that an organ knew" in ascan, "isolation boundary missing")
    require("procedural separateness" in anti.lower() and "patrimonial" in anti.lower(), "anti-fragmentation rule incomplete")
    for pattern in INSTITUTIONAL_WORKFLOW_PATTERNS:
        require(workflow.count(f"'{pattern}'") == 2, f"workflow must cover institutional route pattern on pull request and main push: {pattern}")
    for path in MATERIAL_DOSSIER_ROUTE_IDS:
        require(workflow.count(f"'{path}'") == 2, f"workflow must cover material dossier route on pull request and main push: {path}")

    for path in [
        "archive/PROCEEDINGS_ANTI_FRAGMENTATION_CONVERGENCE_RULE_30AUG2026.md",
        "archive/INSTITUTIONAL_READER_UNITARY_PROCEEDINGS_RULE_30AUG2026.md",
        "archive/CAIXABANK_VALENCIA_01859_2023_REGISTRATION_GAP_30AUG2026.md",
        "archive/PROCEEDINGS_MASTER_REGISTER_VALENCIA_1859_2023_OVERLAY_30AUG2026.md",
        "archive/GC_548_2023_PLAZA2_T1_CARET_CONTINUITY_CONTROL_30AUG2026.md",
        "archive/ARRECIFE_1304_2014_IDENTITY_AND_INTERLINK_GAP_30AUG2026.md",
        "archive/DP3205_2014_ARRECIFE_SOURCE_TRANSLATION_AUTHORITY_ALLEGATIONS_CONTROL_30AUG2026.md",
        "archive/ARRECIFE_4009_2015_CARET_INTERLINK_CONTROL_30AUG2026.md",
        "archive/MISSING_EVIDENCE_REGISTER.md",
        "archive/PROCEEDINGS_CASE_PRISM_V1_SEED_30AUG2026.json",
        "assets/data/proceedings-master-public-v1.json",
        "assets/data/proceedings-interlinkability-v1.json",
        "assets/master-proceedings-publication-20260830.js",
        "assets/site.js",
        "assets/data/caepr-caret-alberto-meeting-point-first-hop-v1.json",
        "publication-manifests/gc-548-2023-plaza2-t1-caret-20260830.json",
        "publication-manifests/arrecife-1304-2014-identity-interlink-20260830.json",
        "docs/deletion-audits/2026-08-30-arrecife-1304-2014-identity-interlink-continuity.md",
        "publication-manifests/master-proceedings-publication-20260830.json",
        "scripts/build_public_proceedings_projection.py",
        "scripts/build_proceedings_case_prism_v2.py",
        "scripts/build_proceedings_interlinkability_v1.py",
        "assets/data/counsel-procurador-gap-register-v1.json",
        "assets/data/dp3205-2014-arrecife-v1.json",
        "en/dp-3205-2014-arrecife/index.html",
        "es/dp-3205-2014-arrecife/index.html",
        "publication-manifests/dp3205-2014-arrecife-caret-interlink-20260830.json",
        "publication-manifests/arrecife-4009-2015-caret-interlink-20260830.json",
        "scripts/validate_dp3205_2014_publication.py",
        ".github/workflows/validate-dp3205-2014-publication.yml",
        "publication-manifests/all-proceedings-interlinkability-20260830.json",
        "docs/deletion-audits/2026-08-30-all-proceedings-interlinkability-continuity.md",
        "docs/deletion-audits/2026-08-30-dp3205-2014-arrecife-caret-interlink.md",
        "assets/data/fiscalia-response-correspondence.json",
        "publication-manifests/case-prism-substantive-gap-closure-20260831.json",
        "docs/deletion-audits/2026-08-31-case-prism-substantive-gap-closure-continuity.md",
    ]:
        require(path in workflow, f"workflow filter missing dependency: {path}")
    require("python3 scripts/build_public_proceedings_projection.py --check" in workflow, "workflow does not rebuild-check the public proceedings projection")
    require("python3 scripts/build_proceedings_interlinkability_v1.py --check" in workflow, "workflow does not rebuild-check exact-proceeding interlinkability")
    smoke = read("scripts/smoke_proceedings_case_prism.mjs")
    require("#isolation-test=GC-APP-007" in smoke and "hashchange aggregate isolation" in smoke, "browser smoke does not reject/canonicalise aggregate isolation deep links")
    for token, label in {
        "delete entire axis basis": "whole-axis-basis deletion mutation",
        "remove core canonical axis status": "core canonical-status deletion mutation",
        "remove cross-file root status": "cross-file canonical-status deletion mutation",
        "mismatch axis basis status": "axis-status mismatch mutation",
        "remove axis basis kind": "basis-kind mutation",
        "remove English axis basis": "English basis mutation",
        "remove Spanish axis basis": "Spanish basis mutation",
        "remove English axis limitation": "English limitation mutation",
        "remove Spanish axis limitation": "Spanish limitation mutation",
        "remove axis source kind": "source-kind mutation",
        "remove axis source record ID": "source-record-ID mutation",
        "remove actor receipt token": "actor-receipt mutation",
        "remove actor knowledge token": "actor-knowledge mutation",
        "remove actor source token": "actor-source mutation",
        "remove English actor boundary": "English actor-boundary mutation",
        "remove Spanish actor boundary": "Spanish actor-boundary mutation",
        "MUTATION-ACTOR-WITHOUT-KNOWLEDGE-STATUS": "actor-profile/source-separation mutation",
        "document.documentElement.scrollWidth": "390px open-disclosure document-overflow check",
        "summaryMinHeight < 44": "44px institutional-axis disclosure target check",
        "provenanceOverflowWrap": "mobile provenance wrapping check",
        "document.activeElement?.matches('[data-isolation-id]')": "isolation-select focus-preservation check",
        "summary.press('Enter')": "native disclosure Enter-key check",
        "summary.press('Space')": "native disclosure Space-key check",
    }.items():
        require(token in smoke, f"browser smoke missing {label}")

if errors:
    print("PROCEEDINGS INTERCONNECTIVITY MAP AUDIT: FAIL")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("PROCEEDINGS INTERCONNECTIVITY MAP AUDIT: PASS")
print(
    f"- canonical denominator: {CURRENT_CANONICAL_RECORDS} rows / "
    f"{CURRENT_PUBLIC_RECORDS} controlled public rows"
)
print(
    f"- exact proceedings: {CURRENT_CANONICAL_EXACT} canonical / "
    f"{CURRENT_PUBLIC_EXACT} public / {CURRENT_PRIVATE_EXACT} private exact record excluded"
)
print(
    f"- interlinkability: {CURRENT_PUBLIC_EXACT}/{CURRENT_PUBLIC_EXACT} "
    "public exact proceedings classified / 0 unexplained"
)
print(f"- controlled reconnection: {len(relationships)} exact pairs ({source_verified_pair_count} source-verified / {source_reported_pending_pair_count} source-reported pending) / {len(actual_source_assertions)} canonical assertions ({source_verified_assertion_count} verified / {source_reported_pending_assertion_count} pending) / {len(context_clusters)} material context clusters")
print(
    f"- structural exact selector/reconnection: VERIFIED "
    f"{CURRENT_PUBLIC_EXACT}/{CURRENT_PUBLIC_EXACT}; full-corpus restore available"
)
print(
    "- exact-file decision-dependency / fragmentation audit coverage: VERIFIED "
    f"{CURRENT_PUBLIC_EXACT}/{CURRENT_PUBLIC_EXACT} through the public finite-test register and isolation controls"
)
print(
    "- shared Case Prism proposition membership: GAP — "
    f"{CURRENT_CASE_PRISM_EXACT_COVERED}/{CURRENT_PUBLIC_EXACT} exact proceedings "
    f"covered; {CURRENT_CASE_PRISM_EXACT_UNCOVERED} without Case Prism coordinate"
)
print("- Stream, Geography and Chronology remain taxonomy/navigation only")
print("- aggregate appeal-family reference retained but excluded from exact selection")
print("- overlays consolidated and parent graph acyclic")
print("- Case Prism structure: 19 propositions x 12 lanes = 228 explicit coordinates / 0 structural blanks")
print("- relationship and file-treatment vocabularies structurally validated; cell-level evidentiary completeness is not inferred")
print(
    "- exact-file actionability coverage: VERIFIED "
    f"{CURRENT_PUBLIC_EXACT}/{CURRENT_PUBLIC_EXACT} file-specific questions, "
    "decision dependencies, strongest contrary explanations, confirmed/refuted "
    "consequences and canonical metadata routes; primary-source route gaps remain explicit"
)
print(
    "- finite-test family taxonomy: VERIFIED record-type-first — "
    "26 administrative / 19 civil / 11 criminal / 21 Fiscalía / 1 ombudsman / "
    "8 professional / 7 regulatory / 4 tax-contentious"
)
print(
    "- institutional classification provenance: VERIFIED "
    f"{CURRENT_PUBLIC_EXACT}/{CURRENT_PUBLIC_EXACT} classifications with nine "
    "independently graded axes, source basis and limitation; classification does not "
    "mean positive evidence; every positive grade reproduces its supporting episode field"
)
print(
    "- positive evidence/source coverage remains separate: "
    f"{CURRENT_FISCALIA_RESPONSE_EPISODES}/{CURRENT_PUBLIC_EXACT} "
    "source-controlled institutional profiles; "
    f"{len(actor_positive_ids)}/{CURRENT_PUBLIC_EXACT} actor-specific positive profiles"
)
print(
    "- Fiscalía institutional-memory matrix: VERIFIED "
    f"{CURRENT_FISCALIA_OFFICE_FILE_RECORDS}/{CURRENT_FISCALIA_OFFICE_FILE_RECORDS} "
    f"rows ({CURRENT_FISCALIA_EXACT_RECORDS} exact / "
    f"{CURRENT_FISCALIA_UNRESOLVED_RECORDS} unresolved); "
    f"{CURRENT_FISCALIA_PROFILED_MATRIX_RECORDS} matrix profiles / "
    f"{CURRENT_FISCALIA_OFFICE_FILE_RECORDS - CURRENT_FISCALIA_PROFILED_MATRIX_RECORDS} "
    "explicit profile gaps; 9 total response episodes include GC-CRI-008 outside the matrix"
)
print(
    "- Fiscalía substantive columns: source-attributed material summaries, received-material "
    "inventory gap, direct/context proceedings, asset gap, transmission, referral, actual "
    "examination, response, cross-file/unitary status, contrary record and unanswered question "
    "validated independently; transmission never substitutes for referral"
)
print("- proposition-level source routes, contrary record, decision dependency and finite actionability fields validated")
print(
    "- Master/trace/isolation navigation: VERIFIED "
    f"{CURRENT_PUBLIC_EXACT}/{CURRENT_PUBLIC_EXACT}; dedicated narrative dossier "
    "coverage remains PARTIAL and is not inferred from navigation"
)
print("- nine audience lenses and bilingual source routes validated")
print(
    "- bilingual specific next-source coverage: VERIFIED "
    f"{CURRENT_PUBLIC_EXACT}/{CURRENT_PUBLIC_EXACT}; full exact-proceeding "
    f"finite-test objects: VERIFIED {CURRENT_PUBLIC_EXACT}/{CURRENT_PUBLIC_EXACT}"
)
print("- EN/ES institutional feeders expose exact trace and isolation deep links")
print("- counsel/procurador denominator remains an explicit GAP")
