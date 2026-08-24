#!/usr/bin/env python3
"""Validate the bilingual Cuatrecasas invoice/finance/outcome audit."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "assets/data/cuatrecasas-invoice-audit-v1.json"

CUATRECASAS_ROUTES = (
    ROOT / "en/cuatrecasas-sun-park/index.html",
    ROOT / "es/cuatrecasas-sun-park/index.html",
)
ONA_ROUTES = (
    ROOT / "en/ona-hotels-insolvency-exit-36-2012/index.html",
    ROOT / "es/ona-hotels-salida-concurso-36-2012/index.html",
)
PUBLIC_ROUTES = CUATRECASAS_ROUTES + ONA_ROUTES

REMATE_VISUALS = (
    ROOT / "assets/cuatrecasas-remate-disclosure-dilemma-en.svg",
    ROOT / "assets/cuatrecasas-remate-disclosure-dilemma-es.svg",
    ROOT / "assets/cuatrecasas-remate-disclosure-dilemma-en.png",
    ROOT / "assets/cuatrecasas-remate-disclosure-dilemma-es.png",
)

EXPECTED_ROLLUP = {
    "invoice_count": Decimal("22"),
    "aweswell_invoice_count": Decimal("20"),
    "lpb_invoice_count": Decimal("2"),
    "matkator_invoice_count": Decimal("0"),
    "pdf_face_total": Decimal("327608.32"),
    "firm_schedule_amount_total": Decimal("326608.32"),
    "zero_pending_count": Decimal("16"),
    "zero_pending_schedule_amount": Decimal("189777.60"),
    "zero_pending_pdf_face_amount": Decimal("190777.60"),
    "outstanding_count": Decimal("6"),
    "outstanding_amount": Decimal("136830.72"),
    "not_issued_or_estimated_amount": Decimal("152424.95"),
    "work_level_time_entry_invoice_count": Decimal("3"),
    "work_level_time_entry_face_amount": Decimal("93586.05"),
    "work_level_hours_total": Decimal("343.75"),
    "fee_headline_plus_expenses_no_timecards_count": Decimal("11"),
    "fee_headline_plus_expenses_no_timecards_face_amount": Decimal("157799.99"),
    "headline_only_count": Decimal("8"),
    "headline_only_face_amount": Decimal("76222.28"),
}

EXPECTED_GROUPS = {
    "WORK_LEVEL_TIME_ENTRIES": (3, Decimal("93586.05")),
    "FEE_HEADLINE_PLUS_EXPENSES_NO_TIMECARDS": (11, Decimal("157799.99")),
    "HEADLINE_ONLY": (8, Decimal("76222.28")),
}

PRIVATE_PUBLIC_PATTERNS = (
    re.compile(r"\bsuccess[ -]?fee\b", re.I),
    re.compile(r"\bfinder(?:'s)?[ -]?fee\b", re.I),
    re.compile(r"\bintroducer compensation\b", re.I),
    re.compile(r"\bcomisi[oó]n\s+(?:a|para)\b", re.I),
    re.compile(r"\b(?:iban|swift)\b", re.I),
    re.compile(r"\bmessage-id\b", re.I),
    re.compile(r"\bgmail\b", re.I),
    re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I),
)


def money(value: object) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"))


def total(rows: list[dict[str, object]], key: str) -> Decimal:
    return sum((money(row.get(key, 0)) for row in rows), Decimal("0.00"))


def formatted_amount(value: object, language: str) -> str:
    amount = f"{money(value):,.2f}"
    if language == "es":
        amount = amount.replace(",", "_").replace(".", ",").replace("_", ".")
        return f"{amount} EUR"
    return f"EUR {amount}"


def main() -> int:
    errors: list[str] = []

    if not DATA_PATH.is_file():
        print(f"CUATRECASAS INVOICE AUDIT GATE: FAIL\n - missing {DATA_PATH.relative_to(ROOT)}")
        return 1

    data = json.loads(DATA_PATH.read_text(encoding="utf-8"), parse_float=Decimal)
    invoices = data.get("invoices", [])
    rollup = data.get("rollup", {})

    for key, expected in EXPECTED_ROLLUP.items():
        actual = Decimal(str(rollup.get(key, "NaN")))
        if actual != expected:
            errors.append(f"rollup {key}: expected {expected}, got {actual}")

    invoice_numbers = [str(row.get("invoice_no", "")) for row in invoices]
    duplicate_numbers = [number for number, count in Counter(invoice_numbers).items() if count > 1]
    if duplicate_numbers:
        errors.append(f"duplicate invoice numbers: {', '.join(duplicate_numbers)}")
    if len(invoices) != 22:
        errors.append(f"invoice population: expected 22, got {len(invoices)}")

    if total(invoices, "pdf_face_amount") != Decimal("327608.32"):
        errors.append("invoice face amounts do not sum to EUR 327,608.32")
    if total(invoices, "schedule_amount") != Decimal("326608.32"):
        errors.append("schedule amounts do not sum to EUR 326,608.32")
    if total(invoices, "schedule_pending") != Decimal("136830.72"):
        errors.append("pending amounts do not sum to EUR 136,830.72")

    zero_pending = [row for row in invoices if row.get("schedule_status") == "ZERO_PENDING"]
    outstanding = [row for row in invoices if row.get("schedule_status") == "OUTSTANDING"]
    if len(zero_pending) != 16 or total(zero_pending, "schedule_amount") != Decimal("189777.60"):
        errors.append("zero-pending count or schedule-basis amount is inconsistent")
    if total(zero_pending, "pdf_face_amount") != Decimal("190777.60"):
        errors.append("zero-pending PDF-face amount is inconsistent")
    if len(outstanding) != 6 or total(outstanding, "schedule_pending") != Decimal("136830.72"):
        errors.append("outstanding count or amount is inconsistent")

    client_counts = Counter(str(row.get("client")) for row in invoices)
    if client_counts != Counter({"Aweswell Limited": 20, "Luchy Playa Blanca, S.L.": 2}):
        errors.append(f"unexpected client population: {dict(client_counts)}")

    for group, (expected_count, expected_amount) in EXPECTED_GROUPS.items():
        rows = [row for row in invoices if row.get("itemisation_group") == group]
        if len(rows) != expected_count or total(rows, "pdf_face_amount") != expected_amount:
            errors.append(
                f"itemisation group {group}: expected {expected_count}/EUR {expected_amount}, "
                f"got {len(rows)}/EUR {total(rows, 'pdf_face_amount')}"
            )
    work_rows = [row for row in invoices if row.get("itemisation_group") == "WORK_LEVEL_TIME_ENTRIES"]
    if total(work_rows, "work_level_hours") != Decimal("343.75"):
        errors.append("work-level hours do not sum to 343.75")

    reissues = data.get("predecessor_reissues", [])
    if len(reissues) != 6 or total(reissues, "amount") != Decimal("102223.52"):
        errors.append("predecessor reissue population or total is inconsistent")
    if money(data.get("predecessor_reissue_total")) != Decimal("102223.52"):
        errors.append("declared predecessor reissue total is inconsistent")

    cuatrecasas_markers = (
        "Varia Structured Opportunities S.A.",
        "Oferta Vinculante",
        "One Lagune / Elaia reciprocal standby-acquisition package",
        "1410112954",
        "1410219014",
        "EUR 327,608.32",
        "EUR 326,608.32",
        "EUR 102,223.52",
        "343.75",
        "Actual double receipt",
    )
    cuatrecasas_markers_es = (
        "Varia Structured Opportunities S.A.",
        "Oferta Vinculante",
        "Un paquete recíproco Lagune / Elaia de adquisición de respaldo",
        "1410112954",
        "1410219014",
        "327.608,32 EUR",
        "326.608,32 EUR",
        "102.223,52 EUR",
        "343,75",
        "Doble percepción real",
    )
    route_controls = zip(
        CUATRECASAS_ROUTES,
        (cuatrecasas_markers, cuatrecasas_markers_es),
        ("en", "es"),
    )
    for path, markers, language in route_controls:
        if not path.is_file():
            errors.append(f"missing route: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        rows = re.findall(r"<tr\b[^>]*>.*?</tr>", text, flags=re.I | re.S)
        for invoice in invoices:
            invoice_no = str(invoice["invoice_no"])
            matching_rows = [row for row in rows if invoice_no in row]
            if not matching_rows:
                errors.append(f"{path.relative_to(ROOT)}: invoice {invoice_no} missing from full register")
                continue
            expected_amount = formatted_amount(invoice["pdf_face_amount"], language)
            if not any(expected_amount in row for row in matching_rows):
                errors.append(
                    f"{path.relative_to(ROOT)}: invoice {invoice_no} missing face amount {expected_amount}"
                )
        for marker in markers:
            if marker not in text:
                errors.append(f"{path.relative_to(ROOT)}: missing audit marker {marker!r}")

    remate_route_markers = {
        CUATRECASAS_ROUTES[0]: (
            'id="remate-disclosure-dilemma"',
            "Aweswell was the documented client",
            "Matkator was not the invoice debtor shown in that table",
            "expressly reserved the possibility of ceding the remate to a third party",
            "Silence is not proof",
            "cuatrecasas-remate-disclosure-dilemma-en.svg",
            "cuatrecasas-remate-disclosure-dilemma-en.png",
        ),
        CUATRECASAS_ROUTES[1]: (
            'id="dilema-cesion-remate"',
            "Aweswell era la cliente documentada",
            "Matkator no era la deudora de factura que mostraba esa tabla",
            "reservó expresamente la posibilidad de ceder el remate a un tercero",
            "El silencio no es prueba",
            "cuatrecasas-remate-disclosure-dilemma-es.svg",
            "cuatrecasas-remate-disclosure-dilemma-es.png",
        ),
    }
    for path, markers in remate_route_markers.items():
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        for marker in markers:
            if marker not in text:
                errors.append(f"{path.relative_to(ROOT)}: missing remate visual marker {marker!r}")

    for path in REMATE_VISUALS:
        if not path.is_file() or path.stat().st_size < 1_000:
            errors.append(f"missing or empty remate visual: {path.relative_to(ROOT)}")
    for path, markers in {
        REMATE_VISUALS[0]: ("EXECUTED DEBTOR / PARTY", "NO ASSIGNEE / CESSION YET PROVED"),
        REMATE_VISUALS[1]: ("DEUDORA / PARTE EJECUTADA", "SIN CESIONARIO / CESIÓN PROBADOS"),
    }.items():
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        for marker in markers:
            if marker not in text:
                errors.append(f"{path.relative_to(ROOT)}: missing visual boundary {marker!r}")

    route_markers = {
        ONA_ROUTES[0]: (
            "Security was a closing mechanism, not a catch-22",
            "ONA-sourced Stoneweg route / VSO offer",
            "does not justify calling it a Stoneweg subsidiary",
            "One reciprocal Lagune / Elaia EUR 26m standby-acquisition package",
        ),
        ONA_ROUTES[1]: (
            "La garantía era mecánica de cierre, no un catch-22",
            "Vía Stoneweg originada por ONA / oferta VSO",
            "no permite llamarla filial de Stoneweg",
            "Un solo paquete recíproco Lagune / Elaia de adquisición de respaldo por 26 M EUR",
        ),
    }
    for path, markers in route_markers.items():
        if not path.is_file():
            errors.append(f"missing route: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{path.relative_to(ROOT)}: missing finance marker {marker!r}")

    for path in PUBLIC_ROUTES:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in PRIVATE_PUBLIC_PATTERNS:
            if pattern.search(text):
                errors.append(f"{path.relative_to(ROOT)}: public/private boundary match {pattern.pattern!r}")

    canonical = ROOT / "archive/CUATRECASAS_INVOICE_FINANCE_OUTCOME_AUDIT_24AUG2026.md"
    if not canonical.is_file():
        errors.append(f"missing canonical control: {canonical.relative_to(ROOT)}")
    for rel, markers in {
        "archive/CORRECTION_REGISTER.md": ("CR-083", "CR-084", "CR-085", "CR-086"),
        "archive/MISSING_EVIDENCE_REGISTER.md": ("ME-083", "ME-084", "ME-085"),
    }.items():
        path = ROOT / rel
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        for marker in markers:
            if marker not in text:
                errors.append(f"{rel}: missing marker {marker}")

    for rel in (
        "archive/CUATRECASAS_2014_ONWARD_BILLING_PACKAGE_RECONSTRUCTION_PROMPT_24AUG2026.md",
        "archive/CUATRECASAS_BILLING_CLARIFICATION_EMAIL_DRAFT_24AUG2026.md",
        "archive/LINKEDIN_CUATRECASAS_REMATE_DISCLOSURE_DILEMMA_POST_24AUG2026.md",
        "archive/CUATRECASAS_REMATE_DISCLOSURE_VISUAL_CONTROL_24AUG2026.md",
    ):
        if not (ROOT / rel).is_file():
            errors.append(f"missing prepared deliverable: {rel}")

    linkedin_path = ROOT / "archive/LINKEDIN_CUATRECASAS_REMATE_DISCLOSURE_DILEMMA_POST_24AUG2026.md"
    linkedin_text = linkedin_path.read_text(encoding="utf-8") if linkedin_path.is_file() else ""
    linkedin_sections = (
        (
            "English",
            "## English feed post — publication-ready\n",
            "\n## Publicación en español",
        ),
        (
            "Spanish",
            "## Publicación en español — lista para LinkedIn\n",
            "\n## English long-form",
        ),
    )
    for language, start, end in linkedin_sections:
        if start not in linkedin_text or end not in linkedin_text:
            errors.append(f"LinkedIn draft: missing {language} feed-post boundary")
            continue
        section = linkedin_text.split(start, 1)[1].split(end, 1)[0].strip()
        if len(section) > 3_000:
            errors.append(f"LinkedIn draft: {language} feed post exceeds 3,000 characters ({len(section)})")

    if errors:
        print("CUATRECASAS INVOICE AUDIT GATE: FAIL")
        for error in errors:
            print(f" - {error}")
        return 1

    print(
        "CUATRECASAS INVOICE AUDIT GATE: PASS "
        "(22 invoices; EUR 327,608.32 face; 3/11/8 itemisation; EN/ES parity and public boundary checked)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
