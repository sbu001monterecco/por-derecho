#!/usr/bin/env python3
"""Register the bilingual Community professional/corporate profile package."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://sbu001monterecco.github.io/por-derecho/"
LASTMOD = "2026-08-25"

PAIRS = [
    (
        "alvaro-campanario-hernandez",
        "Álvaro Campanario Hernández — ficha profesional y cronología",
        "Álvaro Campanario Hernández — professional profile and chronology",
        "Ficha nominal con rastreo oficial 1995–2009, actuaciones Sun Park documentadas y relato atribuido conciliado.",
        "Named profile with the 1995–2009 official trace, documented Sun Park acts and reconciled attributed account.",
        ["Campanario", "abogado", "administrador concursal", "2011"],
        ["Campanario", "lawyer", "insolvency administrator", "2011"],
        ["Álvaro Campanario", "Alvaro Campanario Hernandez"],
    ),
    (
        "juan-carlos-prieto-puente",
        "Juan Carlos Prieto Puente — ficha profesional y societaria",
        "Juan Carlos Prieto Puente — professional and corporate profile",
        "Ficha nominal: capacidades documentadas en Sun Park, Millan and Miners y Santa Lucia Real Estate.",
        "Named profile: documented Sun Park roles, Millan and Miners and Santa Lucia Real Estate.",
        ["Prieto Puente", "abogado", "Comunidad", "Santa Lucia"],
        ["Prieto Puente", "lawyer", "Community", "Santa Lucia"],
        ["Juan Carlos Prieto", "Juan Carlos Roque Prieto", "Juan Carlos Esloque Prieto"],
    ),
    (
        "esteban-lopez-noriega",
        "Esteban López Noriega — ficha profesional y cronología",
        "Esteban López Noriega — professional profile and chronology",
        "Ficha nominal: acta de 22-jun-2011, litigios y Millan and Miners, con límites de capacidad.",
        "Named profile: 22-Jun-2011 minutes, litigation and Millan and Miners, with role limits.",
        ["López Noriega", "abogado", "22 junio 2011", "Millan and Miners"],
        ["Lopez Noriega", "lawyer", "22 June 2011", "Millan and Miners"],
        ["Esteban Noriega", "Esteban Noruega", "Esteban Muriega"],
    ),
    (
        "antonio-cogolludo-rojas",
        "Antonio Cogolludo Rojas — ficha comunitaria y societaria",
        "Antonio Cogolludo Rojas — Community and corporate profile",
        "Ficha nominal sobre apariciones comunitarias y cargos oficiales en Pamalexsha, Noalpa y Santa Lucia.",
        "Named profile covering Community appearances and official roles in Pamalexsha, Noalpa and Santa Lucia.",
        ["Cogolludo", "presidente", "Pamalexsha", "Noalpa"],
        ["Cogolludo", "president", "Pamalexsha", "Noalpa"],
        ["Antonio Cogolludo"],
    ),
    (
        "millan-and-miners-slp",
        "Millan and Miners, S.L.P. — ficha societaria",
        "Millan and Miners, S.L.P. — corporate profile",
        "Constitución, socios profesionales y administración verificados en BORME; papel Sun Park delimitado.",
        "BORME-verified formation, professional partners and management; Sun Park role delimited.",
        ["Millan and Miners", "SLP", "Prieto", "López Noriega"],
        ["Millan and Miners", "SLP", "Prieto", "Lopez Noriega"],
        ["Millen and Miners", "Millennium Miners", "Millán & Miners"],
    ),
    (
        "pamanil-sl",
        "Pamanil, S.L. — ficha comunitaria",
        "Pamanil, S.L. — Community profile",
        "Propuesta, ratificación y funciones registradas desde 2011; contrato, autoridad y prestación integral abiertos.",
        "Proposal, ratification and recorded functions from 2011; contract, authority and integrated performance remain open.",
        ["Pamanil", "Comunidad", "2011", "administración"],
        ["Pamanil", "Community", "2011", "administration"],
        ["Pamanil SL"],
    ),
    (
        "pamalexsha-servicios-integrales-sl",
        "Pamalexsha Servicios Integrales, S.L. — ficha societaria y comunitaria",
        "Pamalexsha Servicios Integrales, S.L. — corporate and Community profile",
        "Cargos BORME, presupuesto comunitario de 2016 y límites de una supuesta sucesión desde Pamanil.",
        "BORME roles, 2016 Community budget and limits on any claimed succession from Pamanil.",
        ["Pamalexsha", "Cogolludo", "Comunidad", "2016"],
        ["Pamalexsha", "Cogolludo", "Community", "2016"],
        ["Pamalexa", "Pamalexsha Servicios Integrales"],
    ),
    (
        "explotaciones-noalpa-sl",
        "Explotaciones Noalpa, S.L. — ficha societaria",
        "Explotaciones Noalpa, S.L. — corporate profile",
        "Cargos y domicilio societario verificados; vínculos profesionales alegados sometidos a prueba.",
        "Verified officers and registered office; alleged professional links kept subject to proof.",
        ["Noalpa", "Cogolludo", "Shaila", "BORME"],
        ["Noalpa", "Cogolludo", "Shaila", "BORME"],
        ["Explotaciones Noepa", "Noalpa"],
    ),
    (
        "santa-lucia-real-estate-sl",
        "Santa Lucia Real Estate, S.L. — ficha societaria",
        "Santa Lucia Real Estate, S.L. — corporate profile",
        "Vínculo societario oficial entre Juan Carlos Prieto Puente y Antonio Cogolludo Rojas desde 2017.",
        "Official corporate link between Juan Carlos Prieto Puente and Antonio Cogolludo Rojas from 2017.",
        ["Santa Lucia Real Estate", "Prieto", "Cogolludo", "BORME"],
        ["Santa Lucia Real Estate", "Prieto", "Cogolludo", "BORME"],
        ["Santa Lucía", "Inversiones Santa Lucía"],
    ),
    (
        "shaila-maria-cogolludo-ramos",
        "Shaila María Cogolludo Ramos — ficha comunitaria y societaria",
        "Shaila María Cogolludo Ramos — Community and corporate profile",
        "Comunicaciones Pamanil y poderes posteriores en Noalpa y Pamalexsha, sin retroacción ni parentesco inferido.",
        "Pamanil communications and later Noalpa and Pamalexsha powers, without backdating or inferred kinship.",
        ["Shaila Cogolludo", "Pamanil", "Noalpa", "Pamalexsha"],
        ["Shaila Cogolludo", "Pamanil", "Noalpa", "Pamalexsha"],
        ["Shaila Cogolludo", "Shayla Cogolludo"],
    ),
    (
        "francisco-mario-matos-matas",
        "Francisco Mario Matos Matas — ficha comunitaria e identidad",
        "Francisco Mario Matos Matas — Community and identity profile",
        "Funciones Comunidad/Pamanil y divergencia oficial MATA/MATAS pendiente de DNI o certificación.",
        "Community/Pamanil functions and the official MATA/MATAS divergence pending ID or certification.",
        ["FMMM", "Matos Matas", "Matos Mata", "Pamanil"],
        ["FMMM", "Matos Matas", "Matos Mata", "Pamanil"],
        ["FMMM", "Francisco Mario Matos Mata"],
    ),
    (
        "francisco-de-borja-rodriguez-batllori-laffitte",
        "Francisco de Borja Rodríguez-Batllori Laffitte — ficha concursal",
        "Francisco de Borja Rodríguez-Batllori Laffitte — insolvency profile",
        "Administrador concursal designado judicialmente en Concurso 36/2012; no actor privado ni juez.",
        "Court-appointed insolvency administrator in Insolvency 36/2012; neither private actor nor judge.",
        ["Rodríguez-Batllori", "administrador concursal", "Concurso 36/2012"],
        ["Rodriguez-Batllori", "insolvency administrator", "Insolvency 36/2012"],
        ["Francisco de Borja Rodríguez-Batllori"],
    ),
    (
        "asuncion-aizpurua-sanchez",
        "Asunción Aizpurúa Sánchez — ficha comunitaria",
        "Asunción Aizpurúa Sánchez — Community profile",
        "Presidencia y representación según actas Sun Park; coincidencia BOC similar expresamente descartada.",
        "Presidency and representation in Sun Park minutes; similar BOC match expressly rejected.",
        ["Asunción Aizpurúa", "AAS", "Comunidad", "2011"],
        ["Asuncion Aizpurua", "AAS", "Community", "2011"],
        ["AAS", "Asunción Aizpurúa"],
    ),
    (
        "montelanza-monte-lanza-sl",
        "Montelanza / MONTE LANZA — ficha histórica",
        "Montelanza / MONTE LANZA — historic profile",
        "Perímetro Sun Park con grafías BOC/BORME y puente CIF–hoja todavía pendiente.",
        "Sun Park perimeter with BOC/BORME spellings and an outstanding tax-ID/sheet bridge.",
        ["Montelanza", "Monte Lanza", "Sun Park", "GC1339"],
        ["Montelanza", "Monte Lanza", "Sun Park", "GC1339"],
        ["Montelanza, S.L.", "MONTE LANZA SOCIEDAD LIMITADA"],
    ),
    (
        "inversiones-salinetas-sl",
        "Inversiones Salinetas, S.L. — ficha de propiedad",
        "Inversiones Salinetas, S.L. — ownership profile",
        "Apariciones en actas y representación fechada; identidad pública y título finca por finca abiertos.",
        "Appearances in minutes and dated representation; public identity and unit-by-unit title remain open.",
        ["Inversiones Salinetas", "Salineras", "local 5", "Antonio Cogolludo"],
        ["Inversiones Salinetas", "Salineras", "premises 5", "Antonio Cogolludo"],
        ["Inversiones Salinetas", "Inversiones Salineras"],
    ),
]


def route_records() -> list[dict]:
    records: list[dict] = []
    for slug, es_title, en_title, es_summary, en_summary, es_tags, en_tags, aliases in PAIRS:
        records.extend(
            [
                {
                    "lang": "es",
                    "path": f"es/{slug}/",
                    "title": es_title,
                    "type": "actor-profile",
                    "summary": es_summary,
                    "tags": es_tags,
                    "aliases": aliases,
                },
                {
                    "lang": "en",
                    "path": f"en/{slug}/",
                    "title": en_title,
                    "type": "actor-profile",
                    "summary": en_summary,
                    "tags": en_tags,
                    "aliases": aliases,
                },
            ]
        )
    return records


def update_registry() -> None:
    path = ROOT / "assets/data/unitary-route-registry-v1.json"
    records = json.loads(path.read_text(encoding="utf-8"))
    new_records = route_records()
    new_paths = {record["path"] for record in new_records}
    records = [record for record in records if record.get("path") not in new_paths]
    records.extend(new_records)
    path.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sitemap_block() -> str:
    rows = ["  <!-- community-professional-corporate-network:start -->"]
    for slug, *_ in PAIRS:
        es_url = f"{BASE}es/{slug}/"
        en_url = f"{BASE}en/{slug}/"
        for loc in (es_url, en_url):
            rows.extend(
                [
                    "  <url>",
                    f"    <loc>{loc}</loc><lastmod>{LASTMOD}</lastmod>",
                    f'    <xhtml:link rel="alternate" hreflang="es" href="{es_url}"/>',
                    f'    <xhtml:link rel="alternate" hreflang="en" href="{en_url}"/>',
                    f'    <xhtml:link rel="alternate" hreflang="x-default" href="{es_url}"/>',
                    "  </url>",
                ]
            )
    rows.append("  <!-- community-professional-corporate-network:end -->")
    return "\n".join(rows)


def update_sitemap(filename: str) -> None:
    path = ROOT / filename
    text = path.read_text(encoding="utf-8")
    start = "  <!-- community-professional-corporate-network:start -->"
    end = "  <!-- community-professional-corporate-network:end -->"
    if start in text:
        before, remainder = text.split(start, 1)
        _, after = remainder.split(end, 1)
        text = before + sitemap_block() + after
    else:
        text = text.replace("</urlset>", sitemap_block() + "\n</urlset>")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    update_registry()
    update_sitemap("sitemap.xml")
    update_sitemap("sitemap-community-governance.xml")
    print(f"Registered {len(PAIRS) * 2} bilingual profile routes")


if __name__ == "__main__":
    main()
