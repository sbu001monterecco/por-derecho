#!/usr/bin/env python3
"""Validate the draft Sun Park dossiers, including the 2016–2021 court file."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ES = ROOT / "es/concurso-36-2012-masa-activa-2018-2021/index.html"
EN = ROOT / "en/insolvency-36-2012-active-estate-2018-2021/index.html"
SPINE_ES = ROOT / "es/concurso-36-2012-columna-judicial/index.html"
SPINE_EN = ROOT / "en/concurso-36-2012-judicial-spine/index.html"
FLAGSHIP_ES = ROOT / "es/caso-insignia-jv1260-2011-ap89-2014/index.html"
FLAGSHIP_EN = ROOT / "en/flagship-case-jv1260-2011-ap89-2014/index.html"
MANIFEST = ROOT / "assets/data/sun-park-28-upload-source-manifest-v1.json"
PROVENANCE = ROOT / "evidence/insolvency-36-2012/masa-activa-2017-2021/provenance.md"
REGISTER = ROOT / "archive/SUN_PARK_28_UPLOAD_SOURCE_DIGITISATION_AND_PUBLICATION_CONTROL_23AUG2026.md"
PROMPT = ROOT / "archive/prompts/SUN_PARK_28_SOURCE_DIGITISATION_SCAN_PUBLICATION_CONTINUATION_PROMPT_23AUG2026.md"
SUPPLEMENT = ROOT / "archive/SUN_PARK_ACTIVE_ESTATE_2018_2021_EIGHT_SOURCE_SUPPLEMENT_23AUG2026.md"
MISSING = ROOT / "archive/MISSING_EVIDENCE_REGISTER.md"
CROSS_THREAD = ROOT / "archive/CROSS_THREAD_REPOSITORY_WEBSITE_EMAIL_RESCAN_AND_ACTION_REGISTER_23AUG2026.md"
COURT_ACTS = ROOT / "archive/CONCURSO_36_2012_MISSING_ORIGINAL_COURT_ACTS_REGISTER_17AUG2026.md"
AP89 = ROOT / "evidence/jv-1260-2011/full-text/AP89-2014-JV1260-sentencia-redacted.md"
ROUTES = ROOT / "assets/data/unitary-route-registry-v1.json"
SPINE_DATA = ROOT / "assets/data/concurso36-judicial-spine-v1.json"
FLAGSHIP_DATA = ROOT / "assets/data/flagship-case-1260-2011.json"
FLAGSHIP_CONTROL = ROOT / "archive/SUN_PARK_FLAGSHIP_CASE_JV1260_AP89_CANONICAL_CONTROL_17AUG2026.md"
COURT_FILE_DATA = ROOT / "assets/data/concurso36-court-file-v1.json"
COURT_FILE_ROOT = ROOT / "evidence/insolvency-36-2012/court-file-2016-2021"
COURT_FILE_README = COURT_FILE_ROOT / "README.md"
COURT_FILE_ES = COURT_FILE_ROOT / "DIGITISED_DIGEST_ES.md"
COURT_FILE_EN = COURT_FILE_ROOT / "DIGITISED_DIGEST_EN.md"
CONVENIO_OCR = COURT_FILE_ROOT / "full-text/C36-CF-2017-04-27-convenio-proposal-ocr-redacted.md"
COURT_FILE_CONTROL = ROOT / "archive/CONCURSO_36_2012_UNITARY_COURT_FILE_RECONSTRUCTION_24AUG2026.md"
COURT_FILE_PROMPT = ROOT / "archive/prompts/CONCURSO_36_2012_COMPLETE_COURT_FILE_CONTINUATION_PROMPT_24AUG2026.md"

SITEMAPS = {
    "sitemap.xml": ROOT / "sitemap.xml",
    "sitemap-unitary-shell.xml": ROOT / "sitemap-unitary-shell.xml",
    "sitemap-judicial-spine.xml": ROOT / "sitemap-judicial-spine.xml",
    "sitemap-flagship-case.xml": ROOT / "sitemap-flagship-case.xml",
}

EXPECTED_ROUTE_PAIRS = {
    "active-estate": {
        "es/concurso-36-2012-masa-activa-2018-2021/",
        "en/insolvency-36-2012-active-estate-2018-2021/",
    },
    "judicial-spine": {
        "es/concurso-36-2012-columna-judicial/",
        "en/concurso-36-2012-judicial-spine/",
    },
    "flagship-case": {
        "es/caso-insignia-jv1260-2011-ap89-2014/",
        "en/flagship-case-jv1260-2011-ap89-2014/",
    },
}

TRANSCRIPTS = {
    # filename: (source pages, conservative minimum word count, SHA-256)
    "C36-JUD-2017-12-19-001-apertura-liquidacion-redacted.md": (
        3,
        900,
        "3f1a239121e213ee26e4abaaa7a50940107389117c7c7ba73d83e6f149cf49f1",
    ),
    "C36-JUD-2018-04-16-001-plan-liquidacion-redacted.md": (
        7,
        3200,
        "6a64515f3504762bc6f44747d64d61d9a7ec99e7367d6bd3ae9ade9ebe9eaacf",
    ),
    "MAT-005-auto-12may2020-reposicion-redacted.md": (
        2,
        550,
        "2caa1492433a74c603efedf9662ca1057eda863cadb81474cf05a8b7a5cfbbfa",
    ),
    "C36-JUD-2021-02-24-001-preservacion-inspeccion-redacted.md": (
        4,
        1600,
        "3b02a944ae5becb154bdc2109935d060de80bb9e862f10ab055582696e5ee40f",
    ),
    "C36-JUD-2021-02-24-002-prorroga-liquidacion-redacted.md": (
        2,
        580,
        "9841c9aa91e2fa0cf49eeff249928b0ac66dc54912853e77b83d9b1b73bbd27d",
    ),
}

errors: list[str] = []


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: list[str] = []
        self.ids: list[str] = []
        self.alternates: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if data.get("id"):
            self.ids.append(str(data["id"]))
        if tag == "a" and data.get("href"):
            self.hrefs.append(str(data["href"]))
        if tag == "link" and data.get("rel") == "alternate" and data.get("hreflang") and data.get("href"):
            self.alternates.append((str(data["hreflang"]), str(data["href"])))


def read(path: Path) -> str:
    if not path.is_file():
        errors.append(f"missing file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


for path in (
    ES,
    EN,
    SPINE_ES,
    SPINE_EN,
    FLAGSHIP_ES,
    FLAGSHIP_EN,
    MANIFEST,
    PROVENANCE,
    REGISTER,
    PROMPT,
    SUPPLEMENT,
    MISSING,
    CROSS_THREAD,
    COURT_ACTS,
    AP89,
    ROUTES,
    SPINE_DATA,
    FLAGSHIP_DATA,
    FLAGSHIP_CONTROL,
    COURT_FILE_DATA,
    COURT_FILE_README,
    COURT_FILE_ES,
    COURT_FILE_EN,
    CONVENIO_OCR,
    COURT_FILE_CONTROL,
    COURT_FILE_PROMPT,
    *SITEMAPS.values(),
):
    read(path)

try:
    manifest = json.loads(read(MANIFEST))
except Exception as exc:
    errors.append(f"manifest invalid JSON: {exc}")
    manifest = {}

records = manifest.get("records", [])
counts = manifest.get("counts", {})
if len(records) != 28 or counts != {"supplied_filenames": 28, "unique_binaries": 26, "documentary_items": 25}:
    errors.append(f"manifest corpus counts disagree: records={len(records)} counts={counts}")

hashes: list[str] = []
for n, record in enumerate(records, start=1):
    digest = record.get("sha256", "")
    if not re.fullmatch(r"[0-9a-f]{64}", digest):
        errors.append(f"manifest record {n}: invalid SHA-256")
    hashes.append(digest)
    if not all(k in record for k in ("id", "supplied_filename", "bytes", "pages", "source_class", "treatment", "relation")):
        errors.append(f"manifest record {n}: missing required key")
if len(set(hashes)) != 26:
    errors.append(f"manifest expected 26 unique hashes, found {len(set(hashes))}")

by_id = {record.get("id"): record for record in records}
for required in (
    "MAT-008",
    "C36-JUD-2021-02-24-002",
    "AP89-2014-JV1260",
    "PROC-1260-2011-INIT-ALIAS",
    "VAL-ORD1859-2023-EX07-LA-CAJA-2008-RECEIPTS",
):
    if required not in by_id:
        errors.append(f"manifest missing control {required}")
if by_id.get("MAT-008", {}).get("sha256") == by_id.get("C36-JUD-2021-02-24-002", {}).get("sha256"):
    errors.append("same-date 24-Feb-2021 orders were conflated")

try:
    court_file = json.loads(read(COURT_FILE_DATA))
except Exception as exc:
    errors.append(f"court-file inventory invalid JSON: {exc}")
    court_file = {}

court_records = court_file.get("records", [])
court_counts = court_file.get("counts", {})
if len(court_records) != 66 or court_counts.get("docket_items") != 65 or court_counts.get("connected_external_items") != 1:
    errors.append(f"court-file denominator disagrees: records={len(court_records)} counts={court_counts}")
court_ids = [record.get("id") for record in court_records]
if len(court_ids) != len(set(court_ids)):
    errors.append("court-file inventory has duplicate stable IDs")
connected = [record for record in court_records if record.get("kind") == "connected_external_complaint"]
if len(connected) != 1 or connected[0].get("id") != "C36-EXT-2021-02-10-DESTRUCTION-COMPLAINT":
    errors.append("connected external complaint is not separately typed")
core_records = [record for record in court_records if record.get("kind") != "connected_external_complaint"]
core_statuses = Counter(record.get("status") for record in core_records)
expected_core_statuses = {"primary_text": 24, "party_text": 38, "ocr_redacted": 1, "scan_pending": 2}
if dict(core_statuses) != expected_core_statuses:
    errors.append(f"court-file text-status counts disagree: {dict(core_statuses)}")
for record in court_records:
    if not all(key in record for key in ("id", "date", "kind", "lane", "status", "locator", "title", "effect")):
        errors.append(f"court-file record missing required key: {record.get('id')}")
if "C36-JUD-2019-07-23-AP" not in court_ids or "C36-JUD-2019-07-29-AP" in court_ids:
    errors.append("23-Jul-2019 AP date correction is not canonical")
if len([record for record in court_records if record.get("date") == "2018-04-16" and record.get("kind") == "judicial_order"]) != 2:
    errors.append("two distinct 16-Apr-2018 orders are not preserved")
if len([record for record in court_records if record.get("date") == "2021-10-15" and record.get("kind") == "judicial_order"]) != 2:
    errors.append("two distinct 15-Oct-2021 orders are not preserved")

full_root = ROOT / "evidence/insolvency-36-2012/masa-activa-2017-2021/full-text"
actual = {path.name for path in full_root.glob("*.md")}
if actual != set(TRANSCRIPTS):
    errors.append(f"active-estate transcript set mismatch: {sorted(actual ^ set(TRANSCRIPTS))}")
for name, (expected_pages, min_words, expected_hash) in TRANSCRIPTS.items():
    text = read(full_root / name)
    for marker in ("SHA-256", "Página", "omitid"):
        if marker not in text:
            errors.append(f"{name}: missing marker {marker}")
    if expected_hash not in text:
        errors.append(f"{name}: source hash mismatch")
    pages = re.findall(r"^## Página(?: PDF)? (\d+)", text, flags=re.M)
    if pages != [str(n) for n in range(1, expected_pages + 1)]:
        errors.append(f"{name}: page markers disagree: {pages}")
    word_count = len(re.findall(r"\b\w[\w.’'-]*\b", text, flags=re.UNICODE))
    if word_count < min_words:
        errors.append(f"{name}: transcription unexpectedly short ({word_count} < {min_words})")

ap89_text = read(AP89)
ap89_pages = re.findall(r"^## Página PDF (\d+) de 7$", ap89_text, flags=re.M)
if ap89_pages != [str(n) for n in range(1, 8)]:
    errors.append(f"AP89 transcript page markers disagree: {ap89_pages}")
if len(re.findall(r"\b\w[\w.’'-]*\b", ap89_text, flags=re.UNICODE)) < 2400:
    errors.append("AP89 transcript unexpectedly short")
if "1bce9ad6111645393ee2f23915b7df05a9a879181f2c19fad83f6b3e8989c1ec" not in ap89_text:
    errors.append("AP89 transcript source hash mismatch")

convenio_text = read(CONVENIO_OCR)
convenio_pages = re.findall(r"^## Página PDF (\d+)$", convenio_text, flags=re.M)
if convenio_pages != [str(number) for number in range(1, 8)]:
    errors.append(f"convenio OCR page markers disagree: {convenio_pages}")
if "b248a22148503d6c9d9f8c3dc473ed54ad9862f60de5fde3622713f4313999b5" not in convenio_text:
    errors.append("convenio OCR source hash mismatch")
if len(re.findall(r"\b\w[\w.’'-]*\b", convenio_text, flags=re.UNICODE)) < 1000:
    errors.append("convenio OCR derivative unexpectedly short")

for path, lang, title in (
    (ES, "es", "Estado y conservación de la masa activa"),
    (EN, "en", "Condition and preservation of the active estate"),
):
    text = read(path)
    parser = Links()
    parser.feed(text)
    if f'<html lang="{lang}">' not in text or title not in text:
        errors.append(f"{path.relative_to(ROOT)}: language/title marker missing")
    duplicate_ids = sorted(value for value, count in Counter(parser.ids).items() if count > 1)
    if duplicate_ids:
        errors.append(f"{path.relative_to(ROOT)}: duplicate HTML ids {duplicate_ids}")
    expected_alternates = {"es", "en", "x-default"}
    actual_alternates = {hreflang for hreflang, _ in parser.alternates}
    if actual_alternates != expected_alternates:
        errors.append(f"{path.relative_to(ROOT)}: hreflang set disagrees: {sorted(actual_alternates)}")
    for anchor in ("orders" if lang == "en" else "autos", "contradiction" if lang == "en" else "contradiccion", "selection" if lang == "en" else "seleccion", "corrections" if lang == "en" else "correcciones", "gaps" if lang == "en" else "vacios"):
        if anchor not in parser.ids:
            errors.append(f"{path.relative_to(ROOT)}: missing anchor {anchor}")
    linked_transcripts = {Path(urlsplit(h).path).name for h in parser.hrefs if h.endswith("-redacted.md")}
    if linked_transcripts != set(TRANSCRIPTS):
        errors.append(f"{path.relative_to(ROOT)}: transcript links mismatch")
    for href in parser.hrefs:
        parts = urlsplit(href)
        if parts.scheme or parts.netloc or href.startswith("#"):
            continue
        candidate = (path.parent / unquote(parts.path)).resolve()
        try:
            candidate.relative_to(ROOT)
        except ValueError:
            errors.append(f"{path.relative_to(ROOT)}: link escapes root: {href}")
            continue
        # Existing shared site routes are not copied into this focused worktree.
        if href.startswith("../") and not href.startswith("../../"):
            continue
        if parts.path.endswith("/"):
            candidate /= "index.html"
        if not candidate.exists():
            errors.append(f"{path.relative_to(ROOT)}: broken draft-artifact link {href}")

es_text, en_text = read(ES), read(EN)
for marker in ("28", "26", "25", "C36-JUD-2021-02-24-001", "C36-JUD-2021-02-24-002", "ME-PDFSCAN-030–031"):
    if marker not in es_text or marker not in en_text:
        errors.append(f"bilingual parity marker missing: {marker}")
for marker_es, marker_en in (
    ("Razonamiento adverso y limitado", "Adverse, limited reasoning"),
    ("escombros comunes", "common-area rubble"),
    ("demora imputable", "delay attributable"),
):
    if marker_es not in es_text or marker_en not in en_text:
        errors.append(f"active-estate adverse-reasoning parity missing: {marker_es} / {marker_en}")
if "purports to record" not in read(PROVENANCE):
    errors.append("rendered email print is not qualified as unauthenticated/purporting to record")

for path, lang in (
    (SPINE_ES, "es"),
    (SPINE_EN, "en"),
    (FLAGSHIP_ES, "es"),
    (FLAGSHIP_EN, "en"),
):
    parser = Links()
    text = read(path)
    parser.feed(text)
    duplicate_ids = sorted(value for value, count in Counter(parser.ids).items() if count > 1)
    if duplicate_ids:
        errors.append(f"{path.relative_to(ROOT)}: duplicate HTML ids {duplicate_ids}")
    alternate_langs = {hreflang for hreflang, _ in parser.alternates}
    if alternate_langs != {"es", "en", "x-default"}:
        errors.append(f"{path.relative_to(ROOT)}: hreflang set disagrees: {sorted(alternate_langs)}")
    if f'<html lang="{lang}">' not in text:
        errors.append(f"{path.relative_to(ROOT)}: html language marker missing")

spine_es_text, spine_en_text = read(SPINE_ES), read(SPINE_EN)
for marker_es, marker_en in (
    ("65 elementos del expediente", "65-item docket inventory"),
    ("De los textos definitivos al resultado de 2021", "From definitive texts to the 2021 result"),
    ("Alegación atribuida", "Attributed allegation"),
    ("23-jul-2019", "23-Jul-2019"),
    ("no convalidó", "refused to validate"),
):
    if marker_es not in spine_es_text or marker_en not in spine_en_text:
        errors.append(f"court-file website parity missing: {marker_es} / {marker_en}")

flagship_es_text, flagship_en_text = read(FLAGSHIP_ES), read(FLAGSHIP_EN)
for marker_es, marker_en in (
    ("Ratio adversa", "Adverse ratio"),
    ("poseía los apartamentos y sus llaves", "possessed the apartments and keys"),
    ("levantamiento del velo", "veil lifting"),
    ("constituida en un 88,96% por los apartamentos", "constituted 88.96% by the apartments"),
    ("Hipótesis investigativa abierta del proyecto", "Open project investigative hypothesis"),
):
    if marker_es not in flagship_es_text or marker_en not in flagship_en_text:
        errors.append(f"flagship adverse/scope parity missing: {marker_es} / {marker_en}")

parsed_data: dict[Path, object] = {}
for data_path in (SPINE_DATA, FLAGSHIP_DATA, ROUTES, COURT_FILE_DATA):
    try:
        parsed_data[data_path] = json.loads(read(data_path))
    except Exception as exc:
        errors.append(f"{data_path.relative_to(ROOT)} invalid JSON: {exc}")

spine_data = parsed_data.get(SPINE_DATA, {})
if isinstance(spine_data, dict):
    acts = spine_data.get("acts", [])
    dated = [act.get("date") for act in acts if isinstance(act, dict) and act.get("date")]
    date_keys = [tuple(int(part) for part in date.split("-")) for date in dated]
    if date_keys != sorted(date_keys):
        errors.append("judicial-spine acts are not chronological")
    source_crosswalk = {
        "C36-JA-2017-12-19": {"C36-JUD-2017-12-19-001"},
        "C36-JA-2018-TRANSACTION": {"C36-JUD-2018-04-16-001"},
        "C36-JA-2020-05-12": {"MAT-005"},
        "C36-JA-2021-02-24-A": {"C36-JUD-2021-02-24-001", "MAT-008"},
        "C36-JA-2021-02-24-B": {"C36-JUD-2021-02-24-002"},
    }
    acts_by_id = {act.get("id"): act for act in acts if isinstance(act, dict)}
    for act_id, source_ids in source_crosswalk.items():
        if set(acts_by_id.get(act_id, {}).get("source_ids", [])) != source_ids:
            errors.append(f"judicial-spine source crosswalk missing for {act_id}")
    group = spine_data.get("presentation_groups", {}).get("C36-JA-2021-10-15-FAMILY", {})
    if set(group.get("member_ids", [])) != {"C36-JA-2021-10-15-A", "C36-JA-2021-10-15-B"}:
        errors.append("15-Oct-2021 analytical/page aggregation is not controlled")

flagship_data = parsed_data.get(FLAGSHIP_DATA, {})
if isinstance(flagship_data, dict):
    if "nig" in flagship_data.get("firstInstance", {}):
        errors.append("flagship JSON exposes NIG instead of withholding it")
    ap_sources = [item for item in flagship_data.get("sourceManifest", []) if item.get("evidenceId") == "EVID-2014-AP89"]
    if len(ap_sources) != 1 or "AP89-2014-JV1260" not in ap_sources[0].get("aliases", []):
        errors.append("AP89 stable-ID crosswalk missing")

try:
    route_records = json.loads(read(ROUTES))
except Exception:
    route_records = []
route_paths = [record.get("path") for record in route_records if isinstance(record, dict)]
for pair_name, expected_paths in EXPECTED_ROUTE_PAIRS.items():
    for route_path in expected_paths:
        count = route_paths.count(route_path)
        if count != 1:
            errors.append(f"route registry {pair_name}: {route_path} occurs {count} times")

site_root = "https://sbu001monterecco.github.io/por-derecho/"
sitemap_expectations = {
    "sitemap.xml": set().union(*EXPECTED_ROUTE_PAIRS.values()),
    "sitemap-unitary-shell.xml": set().union(*EXPECTED_ROUTE_PAIRS.values()),
    "sitemap-judicial-spine.xml": EXPECTED_ROUTE_PAIRS["active-estate"] | EXPECTED_ROUTE_PAIRS["judicial-spine"],
    "sitemap-flagship-case.xml": EXPECTED_ROUTE_PAIRS["flagship-case"],
}
ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
for name, path in SITEMAPS.items():
    try:
        root = ET.parse(path).getroot()
    except Exception as exc:
        errors.append(f"{name}: invalid XML: {exc}")
        continue
    locs = [element.text or "" for element in root.findall("sm:url/sm:loc", ns)]
    duplicate_locs = sorted(value for value, count in Counter(locs).items() if count > 1)
    if duplicate_locs:
        errors.append(f"{name}: duplicate loc entries {duplicate_locs}")
    for route_path in sitemap_expectations[name]:
        url = site_root + route_path
        if locs.count(url) != 1:
            errors.append(f"{name}: expected route occurs {locs.count(url)} times: {route_path}")

privacy_patterns = {
    "personal email": r"\b[A-Z0-9._%+-]+@(?!example\.)[A-Z0-9.-]+\.[A-Z]{2,}\b",
    "Spanish ID": r"\b\d{8}[A-Z]\b",
    "verification code": r"A05003250-[0-9a-f]{20,}",
    "bank account": r"\b\d{4}[ -]\d{4}[ -]\d{2}[ -]\d{10}\b",
    "private photo-subject identity": r"\bJOAN\s+CRUZ\b",
    "possible 19-digit case identifier": r"\b\d{19}\b",
}
missing_tail = read(MISSING).split("| ME-074", 1)[-1]
public_text = "\n".join(read(path) for path in [ES, EN, SPINE_ES, SPINE_EN, FLAGSHIP_ES, FLAGSHIP_EN, MANIFEST, PROVENANCE, REGISTER, PROMPT, SUPPLEMENT, CROSS_THREAD, COURT_ACTS, AP89, ROUTES, SPINE_DATA, FLAGSHIP_DATA, FLAGSHIP_CONTROL, COURT_FILE_DATA, COURT_FILE_README, COURT_FILE_ES, COURT_FILE_EN, CONVENIO_OCR, COURT_FILE_CONTROL, COURT_FILE_PROMPT, *sorted(full_root.glob("*.md"))]) + "\n" + missing_tail
for label, pattern in privacy_patterns.items():
    if re.search(pattern, public_text, flags=re.I):
        errors.append(f"possible {label} leakage")

register = read(REGISTER)
for marker in ("twenty-six unique binaries", "ME-PDFSCAN-031", "Two separate Autos on 24-February-2021", "overreads the located Auto"):
    if marker not in register:
        errors.append(f"source register missing marker: {marker}")

prompt = read(PROMPT)
for marker in (
    "AUDIT_ONLY",
    "ACQUIRE_AND_DIGITISE",
    "PREPARE_PUBLIC_SAFE",
    "PUBLISH_AFTER_REVIEW",
    "AE-12",
    "Do not send email",
    "full criminal instrumentalisation of proceedings",
    "Yehuda Marer — identity and no-role lock",
    "ME-PDFSCAN-017",
):
    if marker not in prompt:
        errors.append(f"continuation prompt missing marker: {marker}")

court_prompt = read(COURT_FILE_PROMPT)
for marker in (
    "65 located docket items",
    "Adverse-evidence control",
    "full criminal instrumentalisation",
    "ME-PDFSCAN-032",
    "Do not contact courts",
):
    if marker not in court_prompt and marker not in read(COURT_ACTS):
        errors.append(f"court-file continuation control missing marker: {marker}")

flagship_control = read(FLAGSHIP_CONTROL)
for marker in (
    "strongest source-supported criticism",
    "full criminal instrumentalisation of proceedings operating both inside and outside Concurso 36/2012",
    "Yehuda Marer was his retired father",
    "NO FORMAL OR CONTINUING ROLE ESTABLISHED",
):
    if marker not in flagship_control:
        errors.append(f"flagship allegation/capacity control missing marker: {marker}")

if errors:
    print("active-estate dossier validation: FAIL", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("active-estate dossier validation: PASS")
