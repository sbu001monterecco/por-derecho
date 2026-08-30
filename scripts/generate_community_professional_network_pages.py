#!/usr/bin/env python3
"""Generate the bilingual Community/professional/corporate identity pages.

The JSON file is the publication data spine. Generated HTML is intentionally
static: evidence labels, corrections, source links and the complete fifteen-node
navigation remain available without JavaScript.
"""

from __future__ import annotations

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "assets/data/community-professional-corporate-network-v1.json"
STYLE_PATH = "../../assets/community-professional-corporate-network-20260825.css"
BASE_URL = "https://sbu001monterecco.github.io/por-derecho"


TEXT = {
    "es": {
        "skip": "Saltar al contenido principal",
        "archive": "Archivo de identidades y relaciones",
        "actors": "Actores y representantes",
        "community": "Comunidad",
        "flagship": "JV 1260",
        "other_lang": "EN",
        "other_lang_code": "en",
        "home_label": "Por Derecho",
        "home_small": "LPB · Concurso 36/2012",
        "record": "Ficha individual",
        "verified": "Documentado",
        "attributed": "Relato atribuido",
        "open": "Prueba abierta",
        "method_kicker": "MÉTODO DE LECTURA",
        "method_title": "Una cronología, tres carriles probatorios",
        "method_copy": "La ficha no convierte proximidad profesional, coincidencia societaria o sucesión temporal en mandato, conocimiento, conflicto, acuerdo o responsabilidad. Cada proposición conserva fecha, fuente y límite.",
        "boundary_title": "Límite de publicación",
        "boundary_copy": "Los hechos oficiales e internos se exponen como hechos documentados. Las afirmaciones de la declarante se atribuyen expresamente. Una alegación no es una resolución; una pregunta abierta no es una insinuación de culpabilidad.",
        "timeline_kicker": "CRONOLOGÍA CONTROLADA",
        "timeline_title": "Qué consta, cuándo y con qué alcance",
        "source_jump": "Ver fuente",
        "relations_kicker": "RELACIONES",
        "relations_title": "Vínculos de esta ficha dentro de la red",
        "relation": "Relación",
        "period": "Periodo",
        "status": "Estado",
        "proposition": "Proposición controlada y límite",
        "limit": "Límite",
        "corrections_title": "Correcciones activas",
        "questions_kicker": "PRUEBA PENDIENTE",
        "questions_title": "Preguntas finitas que pueden confirmar, limitar o refutar",
        "sources_kicker": "FUENTES",
        "sources_title": "Fuentes oficiales, internas y atribuidas",
        "sources_intro": "Las fuentes oficiales prueban el contenido de su publicación, no hechos ajenos a ella. Los controles internos resumen el corpus Sun Park y deben leerse con sus límites y fuentes subyacentes.",
        "network_kicker": "NAVEGACIÓN DE RED",
        "network_title": "Las quince fichas, conectadas sin fusionar identidades",
        "person": "Persona",
        "entity": "Persona jurídica",
        "core_title": "Volver al expediente principal",
        "right_title": "Derecho de respuesta y corrección",
        "right_copy": "La persona o entidad identificada puede aportar una corrección de identidad, contexto, documentos exculpatorios o una respuesta. El silencio no equivale a admisión. Toda actualización debe conservar la fuente anterior, la corrección y su fecha.",
        "privacy": "Aviso legal y privacidad",
        "footer": "Por Derecho · Archivo público de trazabilidad documental.",
        "updated": "Revisión pública de fuentes: 25 de agosto de 2026.",
        "class_labels": {"official": "Registro oficial", "internal": "Control interno", "secondary": "Fuente secundaria", "attributed": "Relato atribuido", "open": "Resultado limitado"},
        "core_links": [
            ("../actores-partes-abogados-representantes/", "Actores, partes, abogados y representantes"),
            ("../comunidad-instrumentalizacion/", "Comunidad e instrumentalización"),
            ("../caso-insignia-jv1260-2011-ap89-2014/", "Caso insignia JV 1260/2011 → AP 89/2014"),
        ],
        "privacy_route": "../aviso-legal-privacidad/",
    },
    "en": {
        "skip": "Skip to main content",
        "archive": "Identity and relationship archive",
        "actors": "Actors and representatives",
        "community": "Community",
        "flagship": "JV 1260",
        "other_lang": "ES",
        "other_lang_code": "es",
        "home_label": "Project Sun Rock",
        "home_small": "LPB · Insolvency 36/2012",
        "record": "Individual record",
        "verified": "Documented",
        "attributed": "Attributed account",
        "open": "Open proof",
        "method_kicker": "READING METHOD",
        "method_title": "One chronology, three evidence lanes",
        "method_copy": "This record does not convert professional proximity, a shared corporate office or chronological succession into a mandate, knowledge, conflict, agreement or responsibility. Every proposition retains its date, source and limit.",
        "boundary_title": "Publication boundary",
        "boundary_copy": "Official and internal facts are presented as documented facts. The declarant's statements are expressly attributed. An allegation is not a ruling; an open question is not an insinuation of guilt.",
        "timeline_kicker": "CONTROLLED CHRONOLOGY",
        "timeline_title": "What is recorded, when and with what scope",
        "source_jump": "See source",
        "relations_kicker": "RELATIONSHIPS",
        "relations_title": "This record's links within the network",
        "relation": "Relationship",
        "period": "Period",
        "status": "Status",
        "proposition": "Controlled proposition and limit",
        "limit": "Limit",
        "corrections_title": "Active corrections",
        "questions_kicker": "OUTSTANDING PROOF",
        "questions_title": "Finite questions capable of confirming, limiting or refuting",
        "sources_kicker": "SOURCES",
        "sources_title": "Official, internal and attributed sources",
        "sources_intro": "Official sources prove the content of their publication, not facts outside it. Internal controls summarise the Sun Park corpus and must be read with their limits and underlying sources.",
        "network_kicker": "NETWORK NAVIGATION",
        "network_title": "All fifteen records, connected without merging identities",
        "person": "Person",
        "entity": "Legal person",
        "core_title": "Return to the principal file",
        "right_title": "Right of reply and correction",
        "right_copy": "The identified person or entity may provide an identity correction, context, exculpatory documents or a reply. Silence is not admission. Any update must preserve the earlier source, the correction and its date.",
        "privacy": "Legal notice and privacy",
        "footer": "Project Sun Rock · Public documentary traceability archive.",
        "updated": "Public source review: 25 August 2026.",
        "class_labels": {"official": "Official record", "internal": "Internal control", "secondary": "Secondary source", "attributed": "Attributed account", "open": "Bounded result"},
        "core_links": [
            ("../actors-parties-lawyers-representatives/", "Actors, parties, lawyers and representatives"),
            ("../community-instrumentalisation/", "Community and instrumentalisation"),
            ("../flagship-case-jv1260-2011-ap89-2014/", "Flagship case JV 1260/2011 → AP 89/2014"),
        ],
        "privacy_route": "../legal-privacy/",
    },
}


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def local(value: object, lang: str) -> str:
    if isinstance(value, dict):
        return str(value[lang])
    return str(value)


def source_anchor(source_id: str) -> str:
    return "source-" + source_id.lower().replace("_", "-")


def source_link(source: dict, source_id: str, lang: str, label: str | None = None) -> str:
    url = source["url"]
    external = url.startswith("http")
    attrs = ' rel="external noopener"' if external else ""
    text = label or local(source["title"], lang)
    return f'<a href="{esc(url)}"{attrs}>{esc(text)}</a>'


def render_page(data: dict, node: dict, lang: str) -> str:
    t = TEXT[lang]
    other = "en" if lang == "es" else "es"
    slug = node["routes"][lang]
    other_slug = node["routes"][other]
    canonical = f"{BASE_URL}/{lang}/{slug}/"
    es_url = f"{BASE_URL}/es/{node['routes']['es']}/"
    en_url = f"{BASE_URL}/en/{node['routes']['en']}/"
    title = local(node["headline"], lang)
    lead = local(node["lead"], lang)
    description = lead if len(lead) <= 158 else lead[:155].rsplit(" ", 1)[0] + "…"
    nodes_by_id = {entry["id"]: entry for entry in data["nodes"]}

    lanes = []
    for lane in ("verified", "attributed", "open"):
        lanes.append(
            f'<article class="cpn-status-card" data-lane="{lane}">'
            f'<span class="cpn-pill" data-status="{lane}">{esc(t[lane])}</span>'
            f'<h2>{esc(t[lane])}</h2><p>{esc(local(node["lanes"][lane], lang))}</p></article>'
        )

    timeline = []
    for event in node["timeline"]:
        first_source = event["sources"][0]
        timeline.append(
            '<article class="cpn-event">'
            f'<div><time>{esc(event["date"])}</time></div><div>'
            f'<span class="cpn-pill" data-status="{esc(event["status"])}">{esc(t["class_labels"][event["status"]])}</span>'
            f'<h3>{esc(local(event["title"], lang))}</h3><p>{esc(local(event["body"], lang))}</p>'
            f'<a class="cpn-source-jump" href="#{source_anchor(first_source)}">{esc(t["source_jump"])} ↓</a>'
            '</div></article>'
        )

    incident = [edge for edge in data["edges"] if node["id"] in (edge["from"], edge["to"])]
    relation_rows = []
    for edge in incident:
        other_id = edge["to"] if edge["from"] == node["id"] else edge["from"]
        other_node = nodes_by_id[other_id]
        other_href = f'../{other_node["routes"][lang]}/'
        citations = ", ".join(
            source_link(data["sources"][sid], sid, lang, str(index + 1))
            for index, sid in enumerate(edge["sources"])
        )
        relation_rows.append(
            '<tr>'
            f'<td><a href="{esc(other_href)}">{esc(other_node["canonical_name"])}</a></td>'
            f'<td>{esc(edge["period"])}</td>'
            f'<td><span class="cpn-pill" data-status="{esc(edge["status"])}">{esc(t["class_labels"][edge["status"]])}</span></td>'
            f'<td>{esc(local(edge["proposition"], lang))}<small><strong>{esc(t["limit"])}:</strong> {esc(local(edge["limit"], lang))} · {citations}</small></td>'
            '</tr>'
        )

    corrections = "".join(f"<li>{esc(item)}</li>" for item in node["corrections"][lang])
    questions = "".join(f"<li>{esc(item)}</li>" for item in node["questions"][lang])

    source_cards = []
    source_classes = set()
    for source_id in node["source_ids"]:
        source = data["sources"][source_id]
        source_classes.add(source["class"])
        source_cards.append(
            f'<article class="cpn-source-card" id="{source_anchor(source_id)}">'
            f'<span class="cpn-pill" data-status="{esc(source["class"])}">{esc(t["class_labels"][source["class"]])}</span>'
            f'<h3>{source_link(source, source_id, lang)}</h3>'
            f'<p>{esc(local(source["description"], lang))}</p></article>'
        )
    if "internal" not in source_classes:
        raise ValueError(f"{node['id']} ({lang}) must expose an internal source")
    if "official" not in source_classes and not node.get("official_gap"):
        raise ValueError(f"{node['id']} ({lang}) must expose an official source or an explicit official gap")

    network_links = []
    for entry in data["nodes"]:
        current = ' aria-current="page"' if entry["id"] == node["id"] else ""
        network_links.append(
            f'<a class="cpn-network-link" href="../{esc(entry["routes"][lang])}/"{current}>'
            f'<strong>{esc(entry["canonical_name"])}</strong>'
            f'<span>{esc(t[entry["kind"]])}</span></a>'
        )
    core_links = "".join(f'<a class="button" href="{esc(href)}">{esc(label)}</a>' for href, label in t["core_links"])
    aliases = " · ".join(esc(alias) for alias in node["aliases"])
    review_note = local(node["review_note"], lang) if node.get("review_note") else t["updated"]

    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{esc(title)} | {esc(t["home_label"])}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{esc(canonical)}">
  <link rel="alternate" hreflang="es" href="{esc(es_url)}">
  <link rel="alternate" hreflang="en" href="{esc(en_url)}">
  <link rel="alternate" hreflang="x-default" href="{esc(es_url)}">
  <link rel="stylesheet" href="../../assets/styles.css">
  <link rel="stylesheet" href="{STYLE_PATH}">
  <script src="../../assets/site.js" defer></script>
</head>
<body class="dossier-page cpn-page">
<a class="skip-link" href="#main-content">{esc(t["skip"])}</a>
<header class="site-header">
  <div class="shell header-inner">
    <a class="brand" href="../"><span class="brand-mark">PD</span><span class="brand-copy"><strong>{esc(t["home_label"])}</strong><small>{esc(t["home_small"])}</small></span></a>
    <nav class="main-nav" aria-label="{esc(t["archive"])}">
      <a href="../{'actores-partes-abogados-representantes' if lang == 'es' else 'actors-parties-lawyers-representatives'}/">{esc(t["actors"])}</a>
      <a href="../{'comunidad-instrumentalizacion' if lang == 'es' else 'community-instrumentalisation'}/">{esc(t["community"])}</a>
      <a href="../{'caso-insignia-jv1260-2011-ap89-2014' if lang == 'es' else 'flagship-case-jv1260-2011-ap89-2014'}/">{esc(t["flagship"])}</a>
      <a class="language-link" href="../../{other}/{esc(other_slug)}/" lang="{other}" hreflang="{other}">{esc(t["other_lang"])}</a>
    </nav>
  </div>
</header>
<main id="main-content">
  <section class="hero">
    <div class="shell cpn-record">
      <nav class="cpn-breadcrumbs" aria-label="Breadcrumb"><a href="../">{esc(t["home_label"])}</a><span aria-hidden="true">/</span><a href="../{'actores-partes-abogados-representantes' if lang == 'es' else 'actors-parties-lawyers-representatives'}/">{esc(t["archive"])}</a><span aria-hidden="true">/</span><span>{esc(t["record"])}</span></nav>
      <p class="eyebrow">{esc(local(node["kicker"], lang))}</p>
      <h1>{esc(title)}</h1>
      <p class="lead">{esc(lead)}</p>
      <p class="cpn-aliases"><strong>{'Variantes de búsqueda' if lang == 'es' else 'Search variants'}:</strong> {aliases}. {'No sustituyen la identidad canónica.' if lang == 'es' else 'They do not replace the canonical identity.'}</p>
      <div class="cpn-status-grid" aria-label="{'Carriles de estado probatorio' if lang == 'es' else 'Evidence-status lanes'}">{''.join(lanes)}</div>
    </div>
  </section>

  <section class="cpn-section">
    <div class="shell cpn-record cpn-method">
      <div><p class="eyebrow">{esc(t["method_kicker"])}</p><h2>{esc(t["method_title"])}</h2><p class="cpn-intro">{esc(t["method_copy"])}</p></div>
      <aside class="cpn-boundary"><strong>{esc(t["boundary_title"])}</strong><p>{esc(t["boundary_copy"])}</p></aside>
    </div>
  </section>

  <section class="cpn-section cpn-alt">
    <div class="shell cpn-record"><p class="eyebrow">{esc(t["timeline_kicker"])}</p><h2>{esc(t["timeline_title"])}</h2><div class="cpn-timeline">{''.join(timeline)}</div></div>
  </section>

  <section class="cpn-section">
    <div class="shell cpn-record">
      <p class="eyebrow">{esc(t["relations_kicker"])}</p><h2>{esc(t["relations_title"])}</h2>
      <div class="cpn-table-wrap"><table class="cpn-table"><thead><tr><th scope="col">{esc(t["relation"])}</th><th scope="col">{esc(t["period"])}</th><th scope="col">{esc(t["status"])}</th><th scope="col">{esc(t["proposition"])}</th></tr></thead><tbody>{''.join(relation_rows)}</tbody></table></div>
      <aside class="cpn-correction"><strong>{esc(t["corrections_title"])}</strong><ul>{corrections}</ul></aside>
    </div>
  </section>

  <section class="cpn-section cpn-alt">
    <div class="shell cpn-record"><p class="eyebrow">{esc(t["questions_kicker"])}</p><h2>{esc(t["questions_title"])}</h2><ol class="cpn-question-list">{questions}</ol></div>
  </section>

  <section class="cpn-section">
    <div class="shell cpn-record"><p class="eyebrow">{esc(t["sources_kicker"])}</p><h2>{esc(t["sources_title"])}</h2><p class="cpn-intro">{esc(t["sources_intro"])}</p><div class="cpn-source-grid">{''.join(source_cards)}</div><p class="cpn-source-note">{esc(review_note)}</p></div>
  </section>

  <section class="cpn-section cpn-alt">
    <div class="shell cpn-record"><p class="eyebrow">{esc(t["network_kicker"])}</p><h2>{esc(t["network_title"])}</h2><nav class="cpn-network-grid" aria-label="{esc(t["network_title"])}">{''.join(network_links)}</nav><h3>{esc(t["core_title"])}</h3><div class="cpn-core-links">{core_links}</div><aside class="cpn-reply"><strong>{esc(t["right_title"])}</strong><p>{esc(t["right_copy"])} <a href="{esc(t["privacy_route"])}">{esc(t["privacy"])} →</a></p></aside></div>
  </section>
</main>
<footer class="site-footer"><div class="shell"><p>{esc(t["footer"])}</p></div></footer>
</body>
</html>
'''


def validate_data(data: dict) -> None:
    nodes = data.get("nodes", [])
    if len(nodes) != 15:
        raise ValueError(f"expected 15 nodes, found {len(nodes)}")
    ids = [node["id"] for node in nodes]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate node id")
    for lang in ("es", "en"):
        routes = [node["routes"][lang] for node in nodes]
        if len(routes) != len(set(routes)):
            raise ValueError(f"duplicate {lang} route")
    sources = data.get("sources", {})
    for edge in data.get("edges", []):
        if edge["from"] not in ids or edge["to"] not in ids:
            raise ValueError(f"edge references unknown node: {edge}")
        for source_id in edge["sources"]:
            if source_id not in sources:
                raise ValueError(f"edge references unknown source: {source_id}")
    for node in nodes:
        for required in ("verified", "attributed", "open"):
            if required not in node["lanes"]:
                raise ValueError(f"{node['id']} missing {required} lane")
        for source_id in node["source_ids"]:
            if source_id not in sources:
                raise ValueError(f"{node['id']} references unknown source: {source_id}")


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    validate_data(data)
    written = []
    for node in data["nodes"]:
        for lang in ("es", "en"):
            target = ROOT / lang / node["routes"][lang] / "index.html"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render_page(data, node, lang), encoding="utf-8")
            written.append(target.relative_to(ROOT))
    print(f"generated {len(written)} pages from {DATA_PATH.relative_to(ROOT)}")
    for path in written:
        print(path)


if __name__ == "__main__":
    main()
