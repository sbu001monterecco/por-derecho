#!/usr/bin/env python3
"""Build the bilingual dedicated Autos/decisions pages from the corpus manifest."""

from __future__ import annotations

import argparse
import html
import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets/data/concurso36-autos-fulltext-v1.json"
COMPLETE_CATALOG = ROOT / "assets/data/concurso36-complete-record-v1.json"
TEXT_ROOT = ROOT / "evidence/insolvency-36-2012/concurso-autos/full-text"
ES_OUTPUT = ROOT / "es/concurso-36-2012-autos-resoluciones/index.html"
EN_OUTPUT = ROOT / "en/insolvency-36-2012-orders-decisions/index.html"


KEY_IDS = ("R05", "R09", "F13", "R30")


def format_date(value: str, lang: str) -> str:
    parsed = date.fromisoformat(value)
    months = {
        "es": ("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"),
        "en": ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"),
    }
    if lang == "es":
        return f"{parsed.day} {months[lang][parsed.month - 1]} {parsed.year}"
    return f"{parsed.day} {months[lang][parsed.month - 1]} {parsed.year}"


def repo_link(path: str) -> str:
    return "../../" + path.lstrip("/")


def full_text(record: dict) -> str:
    source = (TEXT_ROOT / record["href"]).read_text(encoding="utf-8")
    blocks = re.findall(r"```text\n(.*?)\n```", source, flags=re.DOTALL)
    if not blocks:
        return "[Texto no extraído]"
    if len(blocks) == 1:
        return blocks[0]
    return "\n\n".join(f"──────── Página {number} ────────\n{block}" for number, block in enumerate(blocks, start=1))


def document_links(record: dict, lang: str) -> str:
    text_label = "Texto íntegro" if lang == "es" else "Full text"
    pdf_label = "PDF público" if lang == "es" else "Public PDF"
    links = [f'<a class="button text" href="{repo_link("evidence/insolvency-36-2012/concurso-autos/full-text/" + record["href"])}">{text_label}</a>']
    if record.get("public_pdf"):
        links.append(f'<a class="button pdf" href="{repo_link(record["public_pdf"])}">{pdf_label}</a>')
    return "".join(links)


def key_cards(records: list[dict], lang: str) -> str:
    by_id = {record["id"]: record for record in records}
    if lang == "es":
        labels = {
            "R05": ("Auto 1377/2025", "Separación: desestimación por legitimación; fondo no examinado."),
            "R09": ("Auto · 11/11/2025", "Reposiciones desestimadas; apelación no suspensiva abierta."),
            "F13": ("Sentencia 4/2026", "Honorarios: desestimación por legitimación; legalidad material no decidida."),
            "R30": ("Auto 223/2026", "Acumula las dos apelaciones; no resuelve el fondo."),
        }
    else:
        labels = {
            "R05": ("Order 1377/2025", "Removal dismissed on standing; the merits were not examined."),
            "R09": ("Order · 11 Nov 2025", "Reconsideration rejected; non-suspensive appeals opened."),
            "F13": ("Judgment 4/2026", "Fees action dismissed on standing; fee legality was not decided."),
            "R30": ("Order 223/2026", "Combines both appeals; does not decide the merits."),
        }
    cards = []
    for record_id in KEY_IDS:
        record = by_id[record_id]
        title, summary = labels[record_id]
        cards.append(
            f'<article class="key-card"><span>{format_date(record["date"], lang)}</span><h3>{title}</h3>'
            f'<p>{summary}</p><a href="#{record_id}">{"Ver decisión" if lang == "es" else "View decision"} →</a></article>'
        )
    return "".join(cards)


def decision_rows(records: list[dict], lang: str) -> str:
    rows = []
    for record in (item for item in records if item["record_class"] == "court"):
        merits = record["merits_scope"]
        rows.append(
            "<tr>"
            f'<td><time datetime="{record["date"]}">{format_date(record["date"], lang)}</time><small>{record["id"]}</small></td>'
            f'<td><strong>{html.escape(record["instrument"])}</strong><br>{html.escape(record["actor"])}</td>'
            f'<td>{html.escape(record["title"])}</td>'
            f'<td>{html.escape(record["outcome"] or ("Trámite procesal; véase texto." if lang == "es" else "Procedural step; see source text."))}'
            f'<small>{html.escape(merits)}</small></td>'
            f'<td class="actions">{document_links(record, lang)}<a class="button view" href="#{record["id"]}">{"Mostrar" if lang == "es" else "Show"}</a></td>'
            "</tr>"
        )
    return "".join(rows)


def inline_decisions(records: list[dict], lang: str) -> str:
    pieces = []
    for record in (item for item in records if item["record_class"] == "court"):
        is_open = " open" if record["id"] == "R05" else ""
        source_text = html.escape(full_text(record))
        source_note = "Texto oficial en español, íntegro y redactado" if lang == "es" else "Official Spanish text, complete and redacted"
        pieces.append(
            f'<details class="decision" id="{record["id"]}"{is_open}>'
            f'<summary><span class="decision-id">{record["id"]}</span><span><strong>{html.escape(record["title"])}</strong>'
            f'<small>{format_date(record["date"], lang)} · {html.escape(record["actor"])}</small></span>'
            f'<span class="chevron" aria-hidden="true">＋</span></summary>'
            f'<div class="decision-body"><div class="decision-meta"><p><strong>{"Efecto:" if lang == "es" else "Effect:"}</strong> '
            f'{html.escape(record["outcome"] or ("Trámite procesal." if lang == "es" else "Procedural step."))}</p>'
            f'<p><strong>{"Alcance:" if lang == "es" else "Scope:"}</strong> {html.escape(record["merits_scope"])}</p>'
            f'<div>{document_links(record, lang)}</div></div>'
            f'<p class="source-note">{source_note}</p><pre lang="es">{source_text}</pre></div></details>'
        )
    return "".join(pieces)


def filing_rows(records: list[dict], lane: str, lang: str) -> str:
    rows = []
    for record in (item for item in records if item["lane"] == lane and item["record_class"] == "party"):
        status = html.escape(record["copy_status"])
        rows.append(
            f'<li><time datetime="{record["date"]}">{format_date(record["date"], lang)}</time>'
            f'<div><span class="doc-id">{record["id"]}</span><h3>{html.escape(record["title"])}</h3>'
            f'<p>{html.escape(record["actor"])} · {html.escape(record["instrument"])} · {html.escape(record["procedure"])}</p>'
            f'<small>{status}</small></div><div class="actions">{document_links(record, lang)}</div></li>'
        )
    return "".join(rows)


def render(records: list[dict], catalog: dict, lang: str) -> str:
    court_count = sum(record["record_class"] == "court" for record in records)
    party_count = len(records) - court_count
    catalog_counts = catalog["counts"]
    catalog_result = catalog["result"]
    if lang == "es":
        meta = {
            "title": "Corpus judicial y de parte localizado · Concurso 36/2012",
            "description": "Archivo especialista íntegro redactado de separación/honorarios y acceso al catálogo unitario parcial de las decisiones, escritos, comunicaciones e implementación actualmente localizados.",
            "canonical": "https://sbu001monterecco.github.io/por-derecho/es/concurso-36-2012-autos-resoluciones/",
            "alternate": "https://sbu001monterecco.github.io/por-derecho/en/insolvency-36-2012-orders-decisions/",
            "alternate_lang": "en",
            "brand": "Concurso 36/2012 · archivo judicial",
            "lang_link": "../../en/insolvency-36-2012-orders-decisions/",
            "lang_text": "EN",
            "eyebrow": "JUEZ · SALA · LAJ · ESCRITOS · TEXTO ÍNTEGRO",
            "h1": "Autos, decisiones y escritos localizados del Concurso 36/2012",
            "lead": "Esta ruta conserva el corpus especialista de 2024–2026 sobre separación del Administrador Concursal y honorarios: 50 transcripciones públicas íntegras y redactadas. El catálogo unitario enlazado amplía la vista a 2012–2026, pero no sustituye un índice judicial certificado ni permite afirmar que se haya obtenido o publicado todo el expediente.",
            "scope": "Regla de alcance",
            "scope_text": "La solicitud de separación y la demanda de honorarios fueron desestimadas en primera instancia por legitimación activa. Las resoluciones localizadas no decidieron el fondo de los siete motivos de separación ni la legalidad material o cuantía de los honorarios. El Auto 223/2026 acumuló las apelaciones de separación; no las resolvió sobre el fondo.",
            "nav_coverage": "Cobertura total",
            "nav_decisions": "Decisiones 2024–2026",
            "nav_text": "Texto judicial completo",
            "nav_filings": "Escritos de parte",
            "nav_gaps": "Vacíos y método",
            "decisions_kicker": "Mapa exacto de decisiones",
            "decisions_h2": "Qué decidió cada órgano — y qué no decidió",
            "decisions_intro": "La tabla separa el efecto procesal de cada resolución de cualquier valoración de fondo. Los PDF públicos son copias rasterizadas sin capa de texto ni metadatos heredados; la transcripción accesible aparece debajo.",
            "th_date": "Fecha / ID", "th_issuer": "Órgano / clase", "th_doc": "Documento", "th_effect": "Efecto y alcance", "th_access": "Acceso",
            "text_kicker": "Decisiones a la vista",
            "text_h2": "Texto íntegro de Juez, Sala y LAJ",
            "text_intro": "Abra cualquier resolución para leerla completa, página por página. La redacción no modifica los antecedentes, fundamentos ni la parte dispositiva.",
            "filings_kicker": "Corpus especialista",
            "filings_h2": "Todos los escritos localizados en estas dos vías",
            "filings_intro": "Cada enlace abre la transcripción integral redactada de las páginas de la copia localizada, con hash y estado de copia. La integridad de la transcripción no prueba que la copia sea oficial, presentada, notificada, admitida, examinada o firme. Una demanda, oposición o recurso registra una posición procesal; no prueba por sí solo sus alegaciones.",
            "removal_h3": "Separación del Administrador Concursal",
            "fees_h3": "Honorarios / responsabilidad civil",
            "gaps_kicker": "Completitud verificable",
            "gaps_h2": "Lo que falta se registra; no se inventa",
            "gaps": [
                "No se localizó como archivo autónomo el Decreto de 1 de septiembre de 2025 ni la diligencia de 17/26 de marzo de 2025 citados en el incidente de aclaración de honorarios.",
                "No se localizó acta o grabación de la audiencia previa de 20 de enero de 2026.",
                "No se localizó una resolución firmada posterior que decida el fondo del RPL 421/2026.",
                "No se localizó una resolución de fondo posterior al Auto 223/2026 en los RPL 3304/2025 y 3319/2025 acumulados.",
            ],
            "method_h3": "Redacción y fidelidad",
            "method": "Se eliminaron cabeceras administrativas repetitivas, contactos, identificadores personales, cuentas y códigos de verificación, metadatos de firma y nombres de profesionales procesales no necesarios. Las omisiones aparecen marcadas. Los desajustes internos de fecha, nombre o cita se conservan y se explican en la ficha del documento.",
            "reply_h3": "Derecho de respuesta y corrección",
            "reply": "Cualquier parte o profesional citado puede aportar una resolución posterior, señalar un error de transcripción o solicitar una revisión de minimización. La corrección se versionará sin borrar la procedencia ni reescribir retrospectivamente el expediente.",
            "back": "Volver al digesto de separación y honorarios",
            "coverage_kicker": "Denominador y trazabilidad",
            "coverage_h2": "Un catálogo unitario, con la ausencia certificada a la vista",
            "coverage_intro": "El catálogo reúne 72 registros forenses de 2012–2023, las 50 piezas especialistas de 2024–2026 y cinco fuentes adicionales únicas. Las 95 familias históricas son un mínimo de descubrimiento, no el denominador oficial.",
            "coverage_status": "INVENTARIO PARCIAL — FALTA ÍNDICE CERTIFICADO O DOCUMENTACIÓN",
            "coverage_catalog": "Abrir catálogo JSON de 127 registros",
            "coverage_index": "Abrir índice forense de 72 registros",
            "coverage_reader": "Abrir lector de autos críticos",
            "coverage_records": "registros canónicos",
            "coverage_complete": "copias históricas completas",
            "coverage_missing": "copias históricas completas pendientes",
            "coverage_pdfs": "PDF públicos seguros",
            "caption": "Decisiones localizadas en las vías especialistas de separación y honorarios",
        }
    else:
        meta = {
            "title": "Located judicial and party corpus · Insolvency 36/2012",
            "description": "Public-safe redacted specialist removal/fees archive with access to the partial unitary catalogue of currently located decisions, filings, communications and implementation records.",
            "canonical": "https://sbu001monterecco.github.io/por-derecho/en/insolvency-36-2012-orders-decisions/",
            "alternate": "https://sbu001monterecco.github.io/por-derecho/es/concurso-36-2012-autos-resoluciones/",
            "alternate_lang": "es",
            "brand": "Insolvency 36/2012 · judicial archive",
            "lang_link": "../../es/concurso-36-2012-autos-resoluciones/",
            "lang_text": "ES",
            "eyebrow": "JUDGE · APPEAL COURT · LAJ · FILINGS · FULL TEXT",
            "h1": "Located orders, decisions and filings in Insolvency 36/2012",
            "lead": "This route preserves the 2024–2026 specialist corpus on removal of the Insolvency Administrator and remuneration: 50 complete public-safe redacted transcripts. The linked unitary catalogue extends the view to 2012–2026, but it does not replace a certified court index or permit a claim that the whole file has been obtained or published.",
            "scope": "Controlling scope",
            "scope_text": "The removal application and the remuneration claim were dismissed at first instance on active-standing grounds. The located decisions did not adjudicate the seven substantive removal grounds or the material legality and amount of the remuneration. Order 223/2026 combined the removal appeals; it did not decide their merits.",
            "nav_coverage": "Whole-file coverage",
            "nav_decisions": "2024–2026 decisions",
            "nav_text": "Complete court text",
            "nav_filings": "Party filings",
            "nav_gaps": "Gaps and method",
            "decisions_kicker": "Exact decision map",
            "decisions_h2": "What each body decided — and did not decide",
            "decisions_intro": "The table separates each procedural effect from any merits determination. Public PDFs are raster-only copies without a searchable layer or inherited metadata; accessible transcripts appear below.",
            "th_date": "Date / ID", "th_issuer": "Body / class", "th_doc": "Document", "th_effect": "Effect and scope", "th_access": "Access",
            "text_kicker": "Decisions on the page",
            "text_h2": "Complete Judge, Appeal Court and LAJ text",
            "text_intro": "Open any decision to read the complete Spanish original, page by page. Redaction does not change the background, reasoning or operative part.",
            "filings_kicker": "Specialist corpus",
            "filings_h2": "Every located filing in these two lanes",
            "filings_intro": "Each link opens the complete redacted Spanish transcript of the located source-copy pages, with source hash and copy status. Transcript completeness does not establish that a copy is official, filed, served, admitted, examined or final. A claim, defence or appeal records a procedural position; it does not by itself prove its allegations.",
            "removal_h3": "Removal of the Insolvency Administrator",
            "fees_h3": "Remuneration / civil liability",
            "gaps_kicker": "Verifiable completeness",
            "gaps_h2": "Missing material is logged, not invented",
            "gaps": [
                "The 1 September 2025 Decree and the March 2025 procedural direction cited in the remuneration clarification incident were not located as standalone files.",
                "No minutes or recording of the 20 January 2026 preliminary hearing were located.",
                "No later signed merits decision in RPL 421/2026 was located.",
                "No merits decision after Order 223/2026 was located in combined RPL 3304/2025 and 3319/2025.",
            ],
            "method_h3": "Redaction and fidelity",
            "method": "Repeated administrative headers, contact and personal identifiers, bank and verification data, signature metadata and unnecessary procedural-professional names were removed. Omissions are visibly marked. Internal date, name or citation inconsistencies are preserved and explained in each record.",
            "reply_h3": "Right of response and correction",
            "reply": "Any named party or professional may provide a later decision, identify a transcription error or request a data-minimisation review. Corrections will be versioned without erasing provenance or retrospectively rewriting the record.",
            "back": "Back to the removal and remuneration digest",
            "coverage_kicker": "Denominator and traceability",
            "coverage_h2": "One unitary catalogue, with the certification gap visible",
            "coverage_intro": "The catalogue combines 72 forensic records for 2012–2023, the 50 specialist records for 2024–2026 and five additional unique sources. The 95 historical families are a discovery floor, not the official denominator.",
            "coverage_status": "INVENTORY PARTIAL — CERTIFIED DOCKET OR RECORDS STILL MISSING",
            "coverage_catalog": "Open the 127-record JSON catalogue",
            "coverage_index": "Open the 72-record forensic index",
            "coverage_reader": "Open the critical-orders reader",
            "coverage_records": "canonical records",
            "coverage_complete": "complete historical copies",
            "coverage_missing": "historical complete copies missing",
            "coverage_pdfs": "public-safe PDFs",
            "caption": "Located decisions in the specialist removal and remuneration lanes",
        }

    gaps = "".join(f"<li>{html.escape(item)}</li>" for item in meta["gaps"])
    if catalog_result["certified_docket_obtained"]:
        raise ValueError("catalog unexpectedly claims a certified docket")
    opposite_digest = "../concurso-36-2012-separacion-ac-honorarios/" if lang == "es" else "../insolvency-36-2012-administrator-removal-fees/"
    reader = "../concurso-36-2012-que-ordeno-el-juzgado/" if lang == "es" else "../concurso-36-2012-what-the-court-ordered/"
    coverage = (
        f'<section class="section" id="cobertura"><div class="shell"><p class="kicker">{meta["coverage_kicker"]}</p>'
        f'<h2>{meta["coverage_h2"]}</h2><p class="intro">{meta["coverage_intro"]}</p>'
        f'<div class="scope"><strong>{meta["coverage_status"]}</strong><br>'
        f'{catalog_counts["canonical_records"]} {meta["coverage_records"]} · '
        f'{catalog_counts["historical_complete_copies"]} {meta["coverage_complete"]} · '
        f'{catalog_counts["historical_missing_complete_copies"]} {meta["coverage_missing"]} · '
        f'{catalog_counts["public_safe_pdfs_total"]} {meta["coverage_pdfs"]}.</div>'
        f'<p><a class="button" href="../../assets/data/concurso36-complete-record-v1.json">{meta["coverage_catalog"]}</a>'
        f'<a class="button view" href="../../archive/concurso36-primary-autos-21aug2026/FORENSIC_EVIDENCE_INDEX_CONCURSO_36_2012_21AUG2026.csv">{meta["coverage_index"]}</a>'
        f'<a class="button pdf" href="{reader}">{meta["coverage_reader"]}</a></p></div></section>'
    )
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{meta["title"]}</title>
  <meta name="description" content="{meta["description"]}">
  <link rel="canonical" href="{meta["canonical"]}">
  <link rel="alternate" hreflang="{lang}" href="{meta["canonical"]}">
  <link rel="alternate" hreflang="{meta["alternate_lang"]}" href="{meta["alternate"]}">
  <link rel="alternate" hreflang="x-default" href="https://sbu001monterecco.github.io/por-derecho/es/concurso-36-2012-autos-resoluciones/">
  <link rel="stylesheet" href="../../assets/styles.css">
  <script src="../../assets/site.js" defer></script>
  <style>
    .autos-page{{--ink:#16282f;--navy:#102a35;--paper:#f4f0e8;--sand:#e5dccb;--red:#8b3028;--gold:#b7832f;--green:#245b49}}
    .autos-page .hero{{background:radial-gradient(circle at 82% 12%,rgba(183,131,47,.27),transparent 30%),linear-gradient(145deg,#0d252f,#254956);color:#fff;padding:clamp(3.5rem,7vw,6.6rem) 0 3.5rem}}
    .autos-page .hero-grid{{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(240px,.6fr);gap:2.2rem;align-items:end}}
    .autos-page h1{{font-size:clamp(2.6rem,6vw,5.4rem);line-height:.98;letter-spacing:-.045em;max-width:14ch;margin:.55rem 0 1.25rem}}
    .autos-page .lead{{font-size:clamp(1.05rem,2vw,1.28rem);line-height:1.62;max-width:66rem}}
    .autos-page .hero-stat{{padding:.85rem 0;border-top:1px solid rgba(255,255,255,.36)}}.autos-page .hero-stat strong{{display:block;font-size:1.55rem}}.autos-page .hero-stat span{{font-size:.78rem;letter-spacing:.07em;text-transform:uppercase;opacity:.78}}
    .autos-page .scope{{background:#fff;color:var(--ink);border-left:7px solid var(--gold);padding:1.15rem 1.3rem;margin-top:2.2rem;box-shadow:0 12px 28px rgba(0,0,0,.15)}}
    .autos-page .jump{{background:#fff;border-bottom:1px solid #d7d1c7;position:sticky;top:0;z-index:5}}.autos-page .jump .shell{{display:flex;gap:1.2rem;overflow:auto;padding-top:.8rem;padding-bottom:.8rem}}.autos-page .jump a{{white-space:nowrap;font-weight:900;color:var(--navy)}}
    .autos-page .section{{padding:clamp(3.4rem,7vw,6.4rem) 0}}.autos-page .section.alt{{background:var(--paper)}}
    .autos-page h2{{font-size:clamp(2rem,4.4vw,3.6rem);line-height:1.04;margin:.35rem 0 1rem;max-width:22ch}}.autos-page .intro{{font-size:1.08rem;line-height:1.62;max-width:70rem}}
    .autos-page .key-grid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1rem;margin:2rem 0}}.autos-page .key-card{{background:#fff;border-top:5px solid var(--red);padding:1.1rem;box-shadow:0 8px 22px rgba(16,42,53,.08)}}.autos-page .key-card span,.autos-page .key-card small{{display:block;font-size:.75rem;text-transform:uppercase;letter-spacing:.06em;color:#666}}.autos-page .key-card h3{{margin:.4rem 0}}.autos-page .key-card a{{font-weight:900}}
    .autos-page .table-wrap{{overflow:auto;margin-top:1.7rem;border:1px solid #d3ccbf}}.autos-page table{{border-collapse:collapse;width:100%;min-width:980px;background:#fff}}.autos-page th,.autos-page td{{padding:.8rem;vertical-align:top;text-align:left;border-bottom:1px solid #ded8cd}}.autos-page th{{background:var(--sand)}}.autos-page td small{{display:block;margin-top:.45rem;color:#626b6f}}.autos-page td:first-child{{white-space:nowrap}}
    .autos-page caption{{text-align:left;font-weight:900;padding:.75rem;background:#fff;color:var(--navy)}}
    .autos-page .button{{display:inline-block;text-decoration:none;font-weight:900;font-size:.78rem;padding:.45rem .58rem;border-radius:6px;margin:.12rem;background:var(--navy);color:#fff!important}}.autos-page .button.pdf{{background:var(--red)}}.autos-page .button.view{{background:var(--green)}}
    .autos-page .decision{{background:#fff;border:1px solid #d4cec3;margin:.8rem 0}}.autos-page .decision summary{{cursor:pointer;display:grid;grid-template-columns:58px 1fr 36px;gap:.8rem;align-items:center;padding:1rem 1.1rem;list-style:none}}.autos-page .decision summary::-webkit-details-marker{{display:none}}.autos-page .decision summary small{{display:block;margin-top:.25rem;color:#637076}}.autos-page .decision-id{{font-weight:900;color:var(--red)}}.autos-page .chevron{{font-size:1.45rem}}.autos-page .decision[open] .chevron{{transform:rotate(45deg)}}
    .autos-page .decision-body{{border-top:1px solid #ddd6ca;padding:1rem}}.autos-page .decision-meta{{background:#f5f8f7;border-left:5px solid var(--green);padding:.85rem 1rem}}.autos-page .source-note{{font-size:.83rem;color:#5f686c;margin-top:1rem}}.autos-page pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#13272f;color:#edf3f2;padding:1rem;border-radius:8px;max-height:62rem;overflow:auto;font:13px/1.55 ui-monospace,SFMono-Regular,Consolas,monospace}}
    .autos-page .filing-grid{{display:grid;grid-template-columns:1fr 1fr;gap:1.2rem;margin-top:1.6rem}}.autos-page .filing-panel{{background:#fff;padding:1.2rem;border:1px solid #d5cec2}}.autos-page .filing-list{{list-style:none;padding:0;margin:0}}.autos-page .filing-list li{{display:grid;grid-template-columns:110px 1fr auto;gap:.8rem;padding:1rem 0;border-bottom:1px solid #e1dcd2}}.autos-page .filing-list time{{font-size:.78rem;font-weight:900}}.autos-page .filing-list h3{{font-size:1rem;margin:.15rem 0}}.autos-page .filing-list p,.autos-page .filing-list small{{font-size:.82rem;margin:.2rem 0;color:#5d686c}}.autos-page .doc-id{{font-size:.72rem;font-weight:900;color:var(--red)}}
    .autos-page .method-grid{{display:grid;grid-template-columns:1fr 1fr;gap:1rem}}.autos-page .method-card{{background:#fff;border-left:6px solid var(--gold);padding:1.15rem}}.autos-page .gaps{{line-height:1.6}}.autos-page .back{{display:inline-block;margin-top:1.4rem;font-weight:900}}
    @media(max-width:980px){{.autos-page .key-grid{{grid-template-columns:1fr 1fr}}.autos-page .filing-grid,.autos-page .method-grid{{grid-template-columns:1fr}}}}
    @media(max-width:760px){{.autos-page .hero-grid,.autos-page .key-grid{{grid-template-columns:1fr}}.autos-page .filing-list li{{grid-template-columns:1fr}}.autos-page .decision summary{{grid-template-columns:48px 1fr 26px}}}}
  </style>
</head>
<body class="dossier-page autos-page">
<a class="skip-link" href="#contenido">{'Saltar al contenido' if lang == 'es' else 'Skip to content'}</a>
<header class="site-header"><div class="shell header-inner"><a class="brand" href="../"><span class="brand-mark">PD</span><span class="brand-copy"><strong>Por Derecho</strong><small>{meta["brand"]}</small></span></a><nav class="main-nav"><a href="{opposite_digest}">{meta["back"]}</a><a class="language-link" href="{meta["lang_link"]}" lang="{meta["alternate_lang"]}">{meta["lang_text"]}</a></nav></div></header>
<main id="contenido">
  <section class="hero"><div class="shell"><div class="hero-grid"><div><p class="eyebrow">{meta["eyebrow"]}</p><h1>{meta["h1"]}</h1><p class="lead">{meta["lead"]}</p></div><aside><div class="hero-stat"><strong>{len(records)}</strong><span>{'piezas especialistas digitizadas' if lang == 'es' else 'digitised specialist records'}</span></div><div class="hero-stat"><strong>{court_count}</strong><span>{'actos judiciales / LAJ' if lang == 'es' else 'court / LAJ acts'}</span></div><div class="hero-stat"><strong>{party_count}</strong><span>{'escritos de parte' if lang == 'es' else 'party filings'}</span></div><div class="hero-stat"><strong>23·08·2026</strong><span>{'corte documental' if lang == 'es' else 'record cut-off'}</span></div></aside></div><div class="scope"><strong>{meta["scope"]}:</strong> {meta["scope_text"]}</div></div></section>
  <nav class="jump" aria-label="{'En esta página' if lang == 'es' else 'On this page'}"><div class="shell"><a href="#cobertura">{meta["nav_coverage"]}</a><a href="#decisiones">{meta["nav_decisions"]}</a><a href="#texto-judicial">{meta["nav_text"]}</a><a href="#escritos">{meta["nav_filings"]}</a><a href="#metodo">{meta["nav_gaps"]}</a></div></nav>
  {coverage}
  <section class="section alt" id="decisiones"><div class="shell"><p class="kicker">{meta["decisions_kicker"]}</p><h2>{meta["decisions_h2"]}</h2><p class="intro">{meta["decisions_intro"]}</p><div class="key-grid">{key_cards(records, lang)}</div><div class="table-wrap"><table><caption>{meta["caption"]}</caption><thead><tr><th scope="col">{meta["th_date"]}</th><th scope="col">{meta["th_issuer"]}</th><th scope="col">{meta["th_doc"]}</th><th scope="col">{meta["th_effect"]}</th><th scope="col">{meta["th_access"]}</th></tr></thead><tbody>{decision_rows(records, lang)}</tbody></table></div></div></section>
  <section class="section" id="texto-judicial"><div class="shell"><p class="kicker">{meta["text_kicker"]}</p><h2>{meta["text_h2"]}</h2><p class="intro">{meta["text_intro"]}</p>{inline_decisions(records, lang)}</div></section>
  <section class="section alt" id="escritos"><div class="shell"><p class="kicker">{meta["filings_kicker"]}</p><h2>{meta["filings_h2"]}</h2><p class="intro">{meta["filings_intro"]}</p><div class="filing-grid"><article class="filing-panel"><h3>{meta["removal_h3"]}</h3><ol class="filing-list">{filing_rows(records, "separacion", lang)}</ol></article><article class="filing-panel"><h3>{meta["fees_h3"]}</h3><ol class="filing-list">{filing_rows(records, "honorarios", lang)}</ol></article></div></div></section>
  <section class="section" id="metodo"><div class="shell"><p class="kicker">{meta["gaps_kicker"]}</p><h2>{meta["gaps_h2"]}</h2><ul class="gaps">{gaps}</ul><div class="method-grid"><article class="method-card"><h3>{meta["method_h3"]}</h3><p>{meta["method"]}</p></article><article class="method-card"><h3>{meta["reply_h3"]}</h3><p>{meta["reply"]}</p></article></div><a class="back" href="{opposite_digest}">← {meta["back"]}</a></div></section>
</main>
<footer class="site-footer"><div class="shell"><p>Por Derecho · Project Sun Rock · {'Archivo judicial controlado' if lang == 'es' else 'Controlled judicial archive'}</p></div></footer>
</body>
</html>
'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    args = parser.parse_args()
    payload = json.loads(args.manifest.read_text(encoding="utf-8"))
    catalog = json.loads(COMPLETE_CATALOG.read_text(encoding="utf-8"))
    records = payload["documents"]
    for output, lang in ((ES_OUTPUT, "es"), (EN_OUTPUT, "en")):
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(render(records, catalog, lang), encoding="utf-8")
        print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
