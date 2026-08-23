#!/usr/bin/env python3
"""Build the unitary, denominator-aware Concurso 36/2012 record catalogue.

The output is an inventory and crosswalk, not a representation that the
certified court file is complete.  It combines the 2012–2023 forensic index,
the 2024–2026 removal/remuneration corpus and the separately controlled
active-estate source family without double-counting source variants.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HISTORICAL = ROOT / "archive/concurso36-primary-autos-21aug2026/FORENSIC_EVIDENCE_INDEX_CONCURSO_36_2012_21AUG2026.csv"
SPECIALIST = ROOT / "assets/data/concurso36-autos-fulltext-v1.json"
OUTPUT = ROOT / "assets/data/concurso36-complete-record-v1.json"


def infer_historical_class(row: dict[str, str]) -> str:
    issuer = row["issuer_or_actor"].lower()
    actor = f"{row['issuer_or_actor']} {row['court_or_forum']}".lower()
    kind = row["document_type"].lower()
    title = row["title_or_function"].lower()
    judicial_kind = any(
        token in kind for token in ("auto", "providencia", "sentencia", "reported")
    )
    explicit_judicial_issuer = any(
        token in issuer
        for token in ("judge", "magistrad", "audiencia provincial")
    )
    if row["record_id"] == "E071" and "auto" in kind and "decreto" in kind:
        # The source index does not resolve whether E071 is a Judge-issued
        # Auto or an LAJ-issued Decreto.  Do not force that unresolved act
        # into either authority class until the signed source is recovered.
        return "judicial_or_laj_type_unresolved"
    # A signed Auto/Providencia/Sentencia remains a judicial act when the
    # electronic copy also names the LAJ.  The LAJ is part of the copy's
    # authentication/notification layer; that co-appearance does not convert
    # the Judge-issued decision into a court-office act.
    if judicial_kind and explicit_judicial_issuer:
        return "judicial_act"
    if "laj" in actor or "court office" in actor or "diligencia" in kind or "decreto" in kind:
        return "laj_or_court_office_act"
    if any(token in actor for token in ("judge", "audiencia provincial", "court")) and judicial_kind:
        return "judicial_act"
    if any(token in kind for token in ("filing", "offer", "application", "submission", "opposition")):
        return "party_filing"
    if any(token in kind for token in ("email", "communication")) or "communication" in title:
        return "party_communication"
    if any(token in kind for token in ("deed", "protocol")):
        return "implementation_or_notarial_record"
    if any(token in kind for token in ("registry", "nota simple", "qualification")):
        return "registry_record"
    if any(token in kind for token in ("report", "inventory", "certificate")):
        return "report_inventory_or_certificate"
    return "other_evidential_record"


def historical_records() -> list[dict]:
    with HISTORICAL.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    records = []
    for row in rows:
        record = {
                "canonical_id": f"C36-{row['record_id']}",
                "aliases": [row["record_id"]],
                "period": "2012-2023",
                "date": row["date"],
                "record_class": infer_historical_class(row),
                "document_type": row["document_type"],
                "title_or_function": row["title_or_function"],
                "issuer_or_actor": row["issuer_or_actor"],
                "court_or_forum": row["court_or_forum"],
                "proceeding": row["proceeding"],
                "source_system": row["source_system"],
                "source_locator": row["source_locator"],
                "source_pages_or_units": row["pages"],
                "complete_copy_status": row["complete_copy"],
                "annex_status": row["annex_status"],
                "direct_effect_or_proposition": row["operative_or_evidential_effect"],
                "conditions_or_limits": row["conditions_or_limits"],
                "asset_scope": row["asset_scope"],
                "evidence_label": row["evidence_label"],
                "retrieval_priority": row["retrieval_priority"],
                "public_derivative": {
                    "status": "PUBLIC_ANALYTICAL_INDEX_ONLY",
                    "index": "archive/concurso36-primary-autos-21aug2026/FORENSIC_EVIDENCE_INDEX_CONCURSO_36_2012_21AUG2026.csv",
                    "page_complete_transcript": False,
                    "public_pdf": None,
                },
            }
        if row["record_id"] == "E007":
            # The imported 21-Aug analytical snapshot assigned 8 February to
            # this act. Current primary-source controls (19/23 Aug) date the
            # order to 15 February and prohibit publication of the former
            # reconstruction as fact until the complete source is re-inspected.
            record["date"] = "2018-02-15"
            record["snapshot_reported_date"] = "2018-02-08"
            record["date_layer_conflict"] = {
                "status": "SUPERSEDED_RECONSTRUCTION_REQUIRES_PRIMARY_REINSPECTION",
                "current_control": "2018-02-15",
                "superseded_snapshot": "2018-02-08 body; 2018-02-09/14 signatures",
                "rule": "Do not repeat the snapshot layers as established facts without authenticating a distinct primary act.",
            }
            record["conditions_or_limits"] = (
                "Current canonical date 15 February 2018; the source snapshot's "
                "8/9/14-February layers require direct reinspection. The act changes "
                "creditor identity/recognised-credit treatment only and does not prove "
                "assignment economics, payment, later possession or finality."
            )
        records.append(record)
    return records


def specialist_records() -> list[dict]:
    payload = json.loads(SPECIALIST.read_text(encoding="utf-8"))
    records = []
    for row in payload["documents"]:
        instrument = row["instrument"].lower()
        actor = row["actor"].lower()
        if row["record_class"] == "party":
            record_class = "party_filing"
        elif (
            any(token in instrument for token in ("auto", "providencia", "sentencia"))
            and any(token in actor for token in ("juez", "magistrad", "audiencia provincial", "sección"))
        ):
            record_class = "judicial_act"
        elif "laj" in actor or any(token in instrument for token in ("diligencia", "decreto", "cédula")):
            record_class = "laj_or_court_office_act"
        else:
            record_class = "judicial_act"
        records.append(
            {
                "canonical_id": f"C36-SPECIALIST-{row['id']}",
                "aliases": [row["id"]],
                "period": "2024-2026",
                "date": row["date"],
                "record_class": record_class,
                "lane": row["lane"],
                "document_type": row["instrument"],
                "title_or_function": row["title"],
                "issuer_or_actor": row["actor"],
                "proceeding": row["procedure"],
                "source_system": "Controlled source corpus",
                "source_locator": row["source_anchor"],
                "source_sha256": row["source_sha256"],
                "source_pages_or_units": row["source_pages_or_units"],
                "complete_copy_status": "yes",
                "filing_or_copy_status": row["copy_status"],
                "direct_effect_or_proposition": row["outcome"],
                "conditions_or_limits": row["merits_scope"],
                "evidence_label": "SOURCE COPY LOCATED; EFFECT LIMITED TO DOCUMENT CONTENT",
                "public_derivative": {
                    "status": "PUBLIC_SAFE_FULL_TEXT_TRANSCRIPT",
                    "page_complete_transcript": True,
                    "transcript": "evidence/insolvency-36-2012/concurso-autos/full-text/" + row["href"],
                    "public_pdf": row["public_pdf"],
                },
            }
        )
    return records


SUPPLEMENTAL_RECORDS = [
    {
        "canonical_id": "C36-SUP-ACSEC-2018-02-27",
        "aliases": ["SP-2018-02-27-AC-SECURITY-REQUEST"],
        "period": "2012-2023",
        "date": "2018-02-27",
        "record_class": "party_communication",
        "document_type": "Scanned email printout / public diplomatic edition",
        "title_or_function": "Insolvency-administrator request to convene an Owners' Community meeting concerning security",
        "issuer_or_actor": "Insolvency administrator of LPB",
        "source_system": "Restricted Gmail source; public-safe repository derivative",
        "source_locator": "SP-2018-02-27-AC-SECURITY-REQUEST; manifest-controlled restricted message locator",
        "source_sha256": "497ecb49495badbcee155397fe70d37d090c36c4e7998308172e7a612046dbed",
        "source_pages_or_units": 1,
        "complete_copy_status": "yes; native RFC822 and full thread absent",
        "direct_effect_or_proposition": "Records the insolvency administrator asking the Community president to convene a meeting to consider hiring security to prevent unauthorised access and deterioration/improper use of common and private areas.",
        "conditions_or_limits": "A communication, not a judicial act, Community resolution or proof of implementation. It does not establish identity of unauthorised persons, exact property scope, authority for locks/keys/exclusion, later instructions, title, possession, operation or criminal agreement.",
        "evidence_label": "PRIMARY COMMUNICATION COPY; NATIVE RFC822/AUTHENTICATION OPEN",
        "public_derivative": {
            "status": "PUBLIC_SAFE_REDACTED_SEARCHABLE_DERIVATIVE",
            "page_complete_transcript": False,
            "public_pdf": "evidence/sun-park/2018-02-27-ac-security-request/public/2018-02-27-ac-community-security-request-redacted-searchable.pdf",
            "public_pdf_sha256": "129cfdd2b74fe7f5e35b0db7890878aa10c5b81e6d4d6c9d3eaf0845eb820607",
            "transcript_es": "evidence/sun-park/2018-02-27-ac-security-request/transcript.es.md",
            "transcript_en": "evidence/sun-park/2018-02-27-ac-security-request/transcript.en.md",
            "manifest": "evidence/sun-park/2018-02-27-ac-security-request/manifest.json",
        },
    },
    {
        "canonical_id": "C36-SUP-MAT-006",
        "aliases": ["MAT-006"],
        "period": "2012-2023",
        "date": "2020-12-18",
        "record_class": "party_filing",
        "document_type": "Estate-preservation application",
        "title_or_function": "Aweswell request concerning conservation and inspection of the active estate",
        "issuer_or_actor": "Aweswell Limited",
        "source_system": "Restricted evidence custody",
        "source_locator": "MAT-006",
        "source_sha256": "8ab76545ff263d4226cff7f363ddab6daea354abde932d1ed63d920bdc9037da",
        "source_pages_or_units": 4,
        "complete_copy_status": "yes; cited annex absent",
        "evidence_label": "PARTY FILING; ALLEGATIONS NOT FINDINGS",
        "public_derivative": {"status": "PUBLIC_SAFE_SUMMARY_ONLY", "page_complete_transcript": False, "public_pdf": None},
    },
    {
        "canonical_id": "C36-SUP-MAT-007",
        "aliases": ["MAT-007", "MAT-007-ALT-01"],
        "period": "2012-2023",
        "date": "2021-02-16",
        "signature_dates": ["2021-02-17"],
        "record_class": "party_filing",
        "document_type": "Opposition",
        "title_or_function": "CAM opposition to the active-estate preservation request",
        "issuer_or_actor": "Construcciones Acosta Matos, S.A.",
        "source_system": "Restricted evidence custody",
        "source_locator": "MAT-007; alternate facsimile MAT-007-ALT-01",
        "source_sha256": "de45a090b2ffeccb7a7308cd08e1f75c8418fde3617949b2b3774697bde9742b",
        "source_pages_or_units": 4,
        "complete_copy_status": "yes; cited annex absent",
        "evidence_label": "PARTY COUNTER-POSITION; NOT A JUDICIAL FINDING",
        "public_derivative": {"status": "PUBLIC_SAFE_SUMMARY_ONLY", "page_complete_transcript": False, "public_pdf": None},
    },
    {
        "canonical_id": "C36-SUP-MAT-009",
        "aliases": ["MAT-009"],
        "period": "2012-2023",
        "date": "2021-03-08",
        "related_dates": ["2021-02-23", "2021-03-08"],
        "record_class": "party_communication",
        "document_type": "Rendered email thread",
        "title_or_function": "Expert-access request and response chronology",
        "issuer_or_actor": "Party correspondence with the insolvency administrator",
        "source_system": "Restricted evidence custody",
        "source_locator": "MAT-009",
        "source_sha256": "e542e8fddcc7f0a78782012c5f07221b9c735cb81b479d6dcac7d77819d02201",
        "source_pages_or_units": 3,
        "complete_copy_status": "rendered PDF only; native RFC822 and attachment chain missing",
        "evidence_label": "PRIMARY COMMUNICATION COPY; AUTHENTICATION/OUTCOME OPEN",
        "public_derivative": {"status": "PUBLIC_SAFE_SUMMARY_ONLY", "page_complete_transcript": False, "public_pdf": None},
    },
    {
        "canonical_id": "C36-SUP-SP18-PHOTO-01",
        "aliases": ["SP18-PHOTO-01"],
        "period": "2012-2023",
        "date": "2018-03-01",
        "record_class": "photographic_derivative",
        "document_type": "Later-compiled photographic PDF",
        "title_or_function": "Photographic sequence attributed by its cover to an alleged access event",
        "issuer_or_actor": "Compiler not independently established",
        "source_system": "Restricted evidence custody",
        "source_locator": "SP18-PHOTO-01",
        "source_sha256": "e66d1c78166595c9f3899063fdf39767339d608d4184f93cd10993f11e051abc",
        "source_pages_or_units": 18,
        "complete_copy_status": "compiled derivative; underlying photographs/metadata missing",
        "evidence_label": "VISUAL LEAD; COVER ATTRIBUTION IS NOT A FINDING",
        "public_derivative": {"status": "WITHHELD_PENDING SOURCE/PRIVACY REVIEW", "page_complete_transcript": False, "public_pdf": None},
    },
]


SOURCE_COPY_CROSSWALK = [
    {"source_id": "SP-2018-02-27-AC-SECURITY-REQUEST", "canonical_record": "C36-SUP-ACSEC-2018-02-27", "relationship": "canonical_source_copy_with_public_derivative"},
    {"source_id": "MAT-005", "canonical_record": "C36-E032", "relationship": "same_document_source_copy"},
    {"source_id": "MAT-006", "canonical_record": "C36-SUP-MAT-006", "relationship": "canonical_source_copy"},
    {"source_id": "MAT-007", "canonical_record": "C36-SUP-MAT-007", "relationship": "canonical_source_copy"},
    {"source_id": "MAT-007-ALT-01", "canonical_record": "C36-SUP-MAT-007", "relationship": "alternate_facsimile_not_new_filing"},
    {"source_id": "MAT-008", "canonical_record": "C36-E040", "relationship": "same_document_source_copy"},
    {"source_id": "MAT-009", "canonical_record": "C36-SUP-MAT-009", "relationship": "canonical_rendered_copy_native_email_missing"},
    {"source_id": "SP18-PHOTO-01", "canonical_record": "C36-SUP-SP18-PHOTO-01", "relationship": "canonical_compiled_derivative"},
]


KNOWN_GAPS = [
    "Certified chronological docket/index for every section and incident, with a sealed court export.",
    "Complete filing, service, LexNET/ATLANTE and finality chain for each material act.",
    "Complete 20 January 2026 preliminary-hearing minutes and recording.",
    "Certified 25 July 2023 hearing minutes, official audiovisual index and evidence rulings, plus the disposition of the 26 July programme.",
    "Complete 18 May 2021 third-party offer, authority, funding, bond, appearance/hearing and exact procedural treatment.",
    "Underlying AP complaint 375/22 order and reconciliation of conflicting 4/27 July 2022 recital dates.",
    "Protocol 457 five-day court-return receipt, resulting court act/mandamiento and all-finca Registry/cancellation implementation.",
    "Complete creditor assignment, final compensable-debt calculation and source-system accounting bridge.",
    "Complete EUR 400,000 premises/pools title, cash, restitution and accounting chain.",
    "AC report 5367/2022, later quarterly reports, estate ledger/bank records, final accounts and conclusion order.",
    "Signed merits outcomes in RPL 421/2026 and combined RPL 3304/2025 and 3319/2025.",
    "Native RFC822 export and full response/outcome chain for MAT-009 and filing receipts for editable specialist pleadings.",
]


def main() -> None:
    historical = historical_records()
    specialist = specialist_records()
    records = historical + specialist + SUPPLEMENTAL_RECORDS
    ids = [record["canonical_id"] for record in records]
    if len(ids) != len(set(ids)):
        raise SystemExit("duplicate canonical IDs")

    historical_copy_counts = Counter(row["complete_copy_status"] for row in historical)
    specialist_pdf_count = sum(bool(row["public_derivative"]["public_pdf"]) for row in specialist)
    supplemental_pdf_count = sum(bool(row["public_derivative"].get("public_pdf")) for row in SUPPLEMENTAL_RECORDS)
    supplemental_transcript_count = sum(bool(row["public_derivative"].get("page_complete_transcript")) for row in SUPPLEMENTAL_RECORDS)
    class_counts = Counter(row["record_class"] for row in records)
    payload = {
        "schema": "concurso36-complete-record-v1",
        "cutoff": "2026-08-23",
        "case": {
            "court": "Juzgado de lo Mercantil n.º 1 de Las Palmas de Gran Canaria",
            "proceeding": "Concurso ordinario 36/2012",
            "debtor": "Luchy Playa Blanca, S.L.U. (LPB)",
            "nig": "3501647120120000351",
        },
        "result": {
            "inventory_status": "INVENTORY PARTIAL — CERTIFIED DOCKET OR RECORDS STILL MISSING",
            "publication_status": "PUBLICATION COMPLETE FOR THE IDENTIFIED PUBLIC-SAFE CORPUS — NOT THE WHOLE COURT FILE",
            "certified_docket_obtained": False,
            "official_denominator": None,
            "discovery_lower_bound_act_families_2012_2023": 95,
            "historical_workbook_rows_reported": "600+ including filings, copies and duplicates",
            "complete_or_all_uploaded_claim_permitted": False,
        },
        "counts": {
            "canonical_records": len(records),
            "historical_forensic_records": len(historical),
            "historical_complete_copies": historical_copy_counts["yes"],
            "historical_missing_complete_copies": historical_copy_counts["no"],
            "historical_copy_status_uncertain": historical_copy_counts["not independently established"],
            "specialist_records": len(specialist),
            "specialist_public_full_text_transcripts": len(specialist),
            "specialist_public_pdfs": specialist_pdf_count,
            "supplemental_canonical_records": len(SUPPLEMENTAL_RECORDS),
            "supplemental_source_copy_entries": len(SOURCE_COPY_CROSSWALK),
            "supplemental_public_pdfs": supplemental_pdf_count,
            "supplemental_page_complete_transcripts": supplemental_transcript_count,
            "public_safe_pdfs_total": specialist_pdf_count + supplemental_pdf_count,
            "public_page_complete_source_transcripts_total": len(specialist) + supplemental_transcript_count,
            "record_classes": dict(sorted(class_counts.items())),
        },
        "authority_and_status_rules": [
            "LPB alone is the debtor; the mixed-ownership hotel is not automatically the estate.",
            "A party filing proves the representation was made, not the truth of its allegations.",
            "A receipt is not substantive examination; joinder is not acceptance; referral is not a decision.",
            "A judicial or LAJ authorisation must be kept separate from physical, registry and accounting implementation.",
            "Standing or procedural dismissal is not an adjudication of the unexamined merits.",
            "Missing from the reviewed corpus does not mean the record does not exist.",
        ],
        "current_run_source_coverage": {
            "repository_and_history": "searched and reconciled",
            "live_website": "exact-current-main readback verified before this update",
            "local_supplied_files": "three known restricted PDFs hash-matched to existing custody controls",
            "gmail": "connector returned no usable corpus in this run, including a known message locator",
            "google_drive": "connector returned no usable corpus in this run",
            "library_files": "connector returned no usable corpus in this run",
            "interpretation": "connector results are an access-coverage limitation, not evidence of non-existence or deletion",
        },
        "known_gaps": KNOWN_GAPS,
        "source_copy_crosswalk": SOURCE_COPY_CROSSWALK,
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)} with {len(records)} canonical records")


if __name__ == "__main__":
    main()
