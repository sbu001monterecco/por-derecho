#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from html import escape
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path('.')
DATA = ROOT / 'assets' / 'data'
PUBLIC = DATA / 'proceedings-master-public-v1.json'
COVERAGE = DATA / 'proceeding-justice-authority-coverage-20260902.json'
ROUTES = DATA / 'proceeding-page-routes-20260902.json'
GRAPH = DATA / 'proceeding-interlink-graph-20260902.json'
SEARCH = ROOT / 'assets' / 'canonical-home-search-20260902.js'
OVERLAY = ROOT / 'assets' / 'justice-professionals-current-overlay-20260902.js'
VALIDATOR = ROOT / 'scripts' / 'validate_canonical_home_search.py'
SITEMAP = ROOT / 'sitemap.xml'

public = json.loads(PUBLIC.read_text(encoding='utf-8'))
records = public.get('records', [])
by_id = {r['Master_ID']: r for r in records}


def slug(mid: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', mid.lower()).strip('-')


def route_for(mid: str, lang: str) -> str:
    s = slug(mid)
    return f"{lang}/{'procedimientos' if lang == 'es' else 'proceedings'}/{s}/"

routes = {mid: {'es': route_for(mid, 'es'), 'en': route_for(mid, 'en')} for mid in by_id}
ROUTES.write_text(json.dumps({
    'schema': 'por-derecho.proceeding-page-routes.v1',
    'control_date': '2026-09-02',
    'status': 'DEDICATED_BILINGUAL_PAGE_FOR_EVERY_PUBLIC_MASTER_RECORD',
    'record_count': len(routes),
    'routes': routes,
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

id_pattern = re.compile(r'\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+-\d{3}\b')
formal: dict[str, set[str]] = {mid: set() for mid in by_id}
textual: dict[str, set[str]] = {mid: set() for mid in by_id}

for mid, row in by_id.items():
    parent = (row.get('Parent_Master_ID') or '').strip()
    if parent in by_id and parent != mid:
        formal[mid].add(parent)
        formal[parent].add(mid)
    for linked in id_pattern.findall(row.get('Linked_Proceedings') or ''):
        if linked in by_id and linked != mid:
            formal[mid].add(linked)
            formal[linked].add(mid)

# Cross-references are navigation only, not formal procedural edges.
refs = [(mid, (row.get('Reference') or '').strip()) for mid, row in by_id.items()]
for mid, row in by_id.items():
    text = ' | '.join(str(row.get(k) or '') for k in ('Secondary_Reference', 'Appeal_or_Review', 'Connection'))
    for other, ref in refs:
        if other == mid or not ref or len(ref) < 6:
            continue
        if ref in text and other not in formal[mid]:
            textual[mid].add(other)
            textual[other].add(mid)

same_organ: dict[str, list[str]] = {}
for mid, row in by_id.items():
    organ = (row.get('Origin_Organ') or '').strip()
    stream = (row.get('Stream') or '').strip()
    candidates = []
    if organ:
        for oid, other in by_id.items():
            if oid == mid or oid in formal[mid] or oid in textual[mid]:
                continue
            if (other.get('Origin_Organ') or '').strip() == organ:
                candidates.append((0 if (other.get('Stream') or '').strip() == stream else 1, oid))
    same_organ[mid] = [oid for _, oid in sorted(candidates)[:8]]

graph_records = []
for mid in by_id:
    graph_records.append({
        'master_id': mid,
        'formal_related': sorted(formal[mid]),
        'canonical_text_cross_references': sorted(textual[mid]),
        'same_origin_organ_navigation': same_organ[mid],
    })
GRAPH.write_text(json.dumps({
    'schema': 'por-derecho.proceeding-interlink-graph.v1',
    'control_date': '2026-09-02',
    'status': 'RECIPROCAL_FORMAL_EDGES_PLUS_LABELLED_NAVIGATION_ONLY_EDGES',
    'boundary': 'Formal related edges derive only from Parent_Master_ID and Linked_Proceedings. Textual and same-organ links are navigation aids and do not establish joinder, transfer, common parties, common knowledge, merits, causation or liability.',
    'record_count': len(graph_records),
    'records': graph_records,
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

coverage = {}
if COVERAGE.exists():
    c = json.loads(COVERAGE.read_text(encoding='utf-8'))
    coverage = {r['master_id']: r for r in c.get('records', [])}


def relationship_links(mid: str, ids: list[str], lang: str) -> str:
    if not ids:
        return '<p class="pd-muted">—</p>'
    out = []
    for oid in ids:
        row = by_id[oid]
        href = '/' + routes[oid][lang]
        out.append(f"<a class='pd-proc-link' href='{escape(href)}'><code>{escape(oid)}</code><strong>{escape(row.get('Reference') or oid)}</strong><small>{escape(row.get('Origin_Organ') or '')}</small></a>")
    return ''.join(out)


def authority_html(mid: str, lang: str) -> str:
    item = coverage.get(mid)
    if not item:
        text = 'Cobertura nominal específica aún no incorporada a este control.' if lang == 'es' else 'Specific named-authority coverage has not yet been incorporated into this control.'
        return f"<p>{escape(text)}</p>"
    labels = [('judge_or_magistrate', 'Juez / magistrado' if lang == 'es' else 'Judge / magistrate'), ('laj', 'LAJ'), ('fiscal', 'Fiscal')]
    parts = []
    for key, label in labels:
        value = item.get(key, {})
        state = value.get('state', 'SOURCE_GAP')
        ids = value.get('person_ids') or []
        if ids:
            names = ', '.join(ids)
        else:
            names = 'SOURCE_GAP' if 'GAP' in state else state
        parts.append(f"<div class='pd-authority-row'><strong>{escape(label)}</strong><span>{escape(names)}</span><small>{escape(state)}</small></div>")
    return ''.join(parts)


def page(row: dict, lang: str) -> str:
    es = lang == 'es'
    mid = row['Master_ID']
    reference = row.get('Reference') or mid
    status = row.get('Status') or '—'
    source = row.get('Source_Status') or '—'
    open_gap = row.get('Open_Reference_Gap') or ('Sin brecha abierta registrada.' if es else 'No open gap recorded.')
    formal_title = 'Relaciones procesales expresas y backlinks' if es else 'Express procedural relations and backlinks'
    cross_title = 'Referencias cruzadas en campos canónicos' if es else 'Cross-references in canonical fields'
    organ_title = 'Navegación: mismo órgano de origen' if es else 'Navigation: same originating organ'
    directory = '/es/procedimientos/' if es else '/en/proceedings/'
    master = '/es/registro-maestro-procedimientos/' if es else '/en/master-proceedings-register/'
    other_lang = 'en' if es else 'es'
    other_url = '/' + routes[mid][other_lang]
    lang_label = 'EN' if es else 'ES'
    title = f"{reference} — {mid}"
    boundary = ('Las relaciones de esta página se separan por tipo. Solo Parent_Master_ID y Linked_Proceedings generan enlaces procesales formales. Las referencias textuales y la coincidencia de órgano sirven para navegación y no prueban acumulación, identidad de partes, conocimiento compartido, causalidad ni responsabilidad.' if es else 'Relationships on this page are separated by type. Only Parent_Master_ID and Linked_Proceedings generate formal procedural links. Text references and a shared originating court are navigation aids and do not prove joinder, identical parties, shared knowledge, causation or liability.')
    return f"""<!doctype html>
<html lang='{lang}'>
<head>
<meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{escape(title)} · Por Derecho</title>
<meta name='description' content='{escape((row.get('Object_or_Purpose') or reference)[:220])}'>
<link rel='canonical' href='https://sbu001monterecco.github.io/por-derecho/{routes[mid][lang]}'>
<link rel='alternate' hreflang='{other_lang}' href='https://sbu001monterecco.github.io/por-derecho/{routes[mid][other_lang]}'>
<link rel='stylesheet' href='../../../assets/styles.css'><script src='../../../assets/site.js' defer></script>
<style>
.pd-proc-shell{{max-width:1120px;margin:auto;padding:2rem 1rem}}.pd-proc-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}}.pd-proc-card{{border:1px solid #d5dfdc;border-radius:16px;padding:1rem;background:#fff}}.pd-proc-meta{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.75rem}}.pd-proc-meta div{{padding:.75rem;border:1px solid #e0e7e5;border-radius:12px}}.pd-proc-meta strong,.pd-proc-meta span{{display:block}}.pd-proc-links{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.65rem}}.pd-proc-link{{display:block;border:1px solid #cad8d4;border-radius:12px;padding:.8rem;text-decoration:none}}.pd-proc-link strong,.pd-proc-link small{{display:block;margin-top:.25rem}}.pd-authority-row{{display:grid;grid-template-columns:1fr 1fr;gap:.25rem .75rem;padding:.55rem 0;border-bottom:1px solid #e5ecea}}.pd-authority-row small{{grid-column:2}}.pd-boundary-box{{padding:1rem;border-left:4px solid #6a4b13;background:#f7f4ed}}@media(max-width:720px){{.pd-proc-grid,.pd-proc-meta,.pd-proc-links{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<header class='site-header'><div class='shell header-inner'><a class='brand' href='../'>Por Derecho</a><nav class='main-nav'><a href='{master}'>{'Registro Maestro' if es else 'Master Register'}</a><a href='{directory}'>{'Todos los procedimientos' if es else 'All proceedings'}</a><a class='language-link' href='{other_url}'>{lang_label}</a></nav></div></header>
<main>
<section class='pd-proc-shell'>
<p class='eyebrow'>MASTER PROCEEDINGS · {escape(mid)} · 02-SEP-2026</p><h1>{escape(reference)}</h1>
<p class='lead'>{escape(row.get('Object_or_Purpose') or '')}</p>
<div class='pd-proc-meta'>
<div><strong>Master ID</strong><span>{escape(mid)}</span></div><div><strong>{'Tipo' if es else 'Type'}</strong><span>{escape(row.get('Record_Type') or '')} · {escape(row.get('Is_Proceeding') or '')}</span></div>
<div><strong>{'Órgano de origen' if es else 'Originating organ'}</strong><span>{escape(row.get('Origin_Organ') or '—')}</span></div><div><strong>NIG</strong><span>{escape(row.get('NIG') or '—')}</span></div>
<div><strong>{'Estado' if es else 'Status'}</strong><span>{escape(status)}</span></div><div><strong>{'Estado de fuente' if es else 'Source status'}</strong><span>{escape(source)}</span></div>
</div>
</section>
<section class='pd-proc-shell pd-proc-grid'>
<article class='pd-proc-card'><h2>{'Referencia y cronología' if es else 'Reference and chronology'}</h2><p><strong>{'Referencia secundaria' if es else 'Secondary reference'}:</strong> {escape(row.get('Secondary_Reference') or '—')}</p><p><strong>{'Periodo' if es else 'Period'}:</strong> {escape(row.get('Date_or_Period') or '—')}</p><p><strong>{'Último evento conocido' if es else 'Latest known event'}:</strong> {escape(row.get('Latest_Known_Event') or '—')}</p><p><strong>{'Recurso/revisión' if es else 'Appeal/review'}:</strong> {escape(row.get('Appeal_or_Review') or '—')}</p></article>
<article class='pd-proc-card'><h2>{'Brecha documental abierta' if es else 'Open documentary gap'}</h2><p>{escape(open_gap)}</p><div class='pd-boundary-box'>{escape(boundary)}</div></article>
<article class='pd-proc-card'><h2>{'Autoridad identificada' if es else 'Identified authority'}</h2>{authority_html(mid, lang)}<p><a href='/{'es/registro-autoridad-historica-arrecife/' if es else 'en/historic-arrecife-justice-authority-register/'}'>{'Abrir control de autoridad histórica' if es else 'Open historic authority control'}</a></p></article>
<article class='pd-proc-card'><h2>{'Conexión canónica' if es else 'Canonical connection'}</h2><p>{escape(row.get('Connection') or '—')}</p><p><strong>{'Custodio actual' if es else 'Current custodian'}:</strong> {escape(row.get('Current_Custodian') or '—')}</p></article>
</section>
<section class='pd-proc-shell'><h2>{formal_title}</h2><div class='pd-proc-links'>{relationship_links(mid, sorted(formal[mid]), lang)}</div></section>
<section class='pd-proc-shell'><h2>{cross_title}</h2><p class='pd-muted'>{'Navegación derivada de menciones expresas de otras referencias dentro de los campos canónicos; no se eleva a relación procesal formal.' if es else 'Navigation derived from express mentions of other references inside canonical fields; it is not promoted to a formal procedural relationship.'}</p><div class='pd-proc-links'>{relationship_links(mid, sorted(textual[mid]), lang)}</div></section>
<section class='pd-proc-shell'><h2>{organ_title}</h2><p class='pd-muted'>{'Coincidencia de órgano únicamente; no implica conexión entre expedientes.' if es else 'Shared originating organ only; it does not imply a connection between files.'}</p><div class='pd-proc-links'>{relationship_links(mid, same_organ[mid], lang)}</div></section>
<section class='pd-proc-shell'><p><a href='{master}'>{'← Registro Maestro' if es else '← Master Register'}</a> · <a href='{directory}'>{'Índice de páginas de procedimiento' if es else 'Proceeding-page directory'}</a></p></section>
</main></body></html>"""

for lang in ('es', 'en'):
    base = ROOT / lang / ('procedimientos' if lang == 'es' else 'proceedings')
    base.mkdir(parents=True, exist_ok=True)
    cards = []
    for row in records:
        mid = row['Master_ID']
        p = base / slug(mid) / 'index.html'
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(page(row, lang), encoding='utf-8')
        cards.append(f"<a class='pd-proc-link' href='./{slug(mid)}/'><code>{escape(mid)}</code><strong>{escape(row.get('Reference') or mid)}</strong><small>{escape(row.get('Origin_Organ') or '')}</small></a>")
    es = lang == 'es'
    title = 'Páginas canónicas de procedimientos' if es else 'Canonical proceeding pages'
    master = '../registro-maestro-procedimientos/' if es else '../master-proceedings-register/'
    index_html = f"<!doctype html><html lang='{lang}'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{title} · Por Derecho</title><link rel='stylesheet' href='../../assets/styles.css'><style>.pd-index{{max-width:1180px;margin:auto;padding:2rem 1rem}}.pd-proc-links{{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.65rem}}.pd-proc-link{{display:block;border:1px solid #cad8d4;border-radius:12px;padding:.8rem;text-decoration:none}}.pd-proc-link strong,.pd-proc-link small{{display:block;margin-top:.25rem}}@media(max-width:850px){{.pd-proc-links{{grid-template-columns:1fr}}}}</style></head><body><header class='site-header'><div class='shell'><a href='../'>Por Derecho</a></div></header><main class='pd-index'><p class='eyebrow'>MASTER PROCEEDINGS · {len(records)} RECORDS</p><h1>{title}</h1><p>{'Una URL bilingüe estable para cada fila pública del Registro Maestro. Las relaciones formales, backlinks y enlaces de navegación se regeneran desde el mismo grafo canónico.' if es else 'One stable bilingual URL for every public Master Register row. Formal relations, backlinks and navigation links are regenerated from the same canonical graph.'}</p><p><a href='{master}'>{'Abrir Registro Maestro' if es else 'Open Master Register'}</a></p><div class='pd-proc-links'>{''.join(cards)}</div></main><script src='../../assets/site.js'></script></body></html>"
    (base / 'index.html').write_text(index_html, encoding='utf-8')

# Home search: route Master Register results straight to their dedicated pages.
s = SEARCH.read_text(encoding='utf-8')
if "proceeding-page-routes-20260902.json" not in s:
    s = s.replace("  const masterRoute = () => new URL(\n", "  let proceedingRoutes = {};\n\n  const masterRoute = () => new URL(\n")
    s = s.replace("      route: `${masterRoute()}?q=${encodeURIComponent(record.Reference || record.Master_ID)}`,", "      route: proceedingRoutes[record.Master_ID]?.[lang] ? new URL(proceedingRoutes[record.Master_ID][lang], siteRoot).href : `${masterRoute()}?q=${encodeURIComponent(record.Reference || record.Master_ID)}`," )
    s = s.replace("    const [registryIndex, master] = await Promise.all([", "    const [registryIndex, master, proceedingRouteMap] = await Promise.all([")
    old = """      fetch(dataUrl('proceedings-master-public-v1.json'), { cache: 'no-store' }).then((response) => {\n        if (!response.ok) throw new Error(`proceedings ${response.status}`);\n        return response.json();\n      })\n    ]);"""
    new = """      fetch(dataUrl('proceedings-master-public-v1.json'), { cache: 'no-store' }).then((response) => {\n        if (!response.ok) throw new Error(`proceedings ${response.status}`);\n        return response.json();\n      }),\n      fetch(dataUrl('proceeding-page-routes-20260902.json'), { cache: 'no-store' }).then((response) => {\n        if (!response.ok) throw new Error(`proceeding routes ${response.status}`);\n        return response.json();\n      })\n    ]);\n    proceedingRoutes = proceedingRouteMap.routes || {};"""
    if old not in s:
        raise SystemExit('search Promise.all patch anchor missing')
    s = s.replace(old, new)
    SEARCH.write_text(s, encoding='utf-8')

# Replace the current justice overlay so the page reflects the expanded 61/58/3 denominator and both supplements.
overlay = r"""(() => {
  'use strict';
  const current = document.currentScript;
  if (!current) return;
  const path = window.location.pathname;
  const isEs = path.includes('/es/registro-identidad-profesionales-justicia/');
  const isEn = path.includes('/en/justice-professionals-identity-register/');
  if (!isEs && !isEn) return;
  if (document.documentElement.dataset.justiceCurrentOverlay === '20260902b') return;
  document.documentElement.dataset.justiceCurrentOverlay = '20260902b';
  const lang = isEn ? 'en' : 'es';
  const assetBase = new URL('.', current.src);
  const dataUrl = (name) => new URL(`data/${name}`, assetBase).href;
  const siteRoot = new URL('../', assetBase);
  const route = (record) => new URL(String(record.routes?.[lang] || (lang === 'es' ? '/es/registro-identidad-materia/' : '/en/matter-identity-registry/')).replace(/^\//, ''), siteRoot).href;
  const updateText = () => {
    const scores = document.querySelectorAll('.jp-score strong');
    [['61', 0], ['58', 1], ['3', 2], ['0', 3]].forEach(([value, index]) => { if (scores[index]) scores[index].textContent = value; });
    const note = document.querySelector('.jp-note');
    if (note) note.innerHTML = lang === 'es'
      ? '<strong>Veredicto actual: PARCIAL — NO TODO ES^.</strong> 58 de 61 personas fuente-identificadas tienen identidad ^ confirmada. Las tres identidades pendientes siguen siendo Carmen Martínez Socias, Nicolás Quintana Plasencia y Pedro Eugenio Botella Torres. El backfill histórico añade Ángela López-Yuste Padial y Emma Galcerán Solsona desde copias judiciales primarias.'
      : '<strong>Current verdict: PARTIAL — NOT ALL IS^.</strong> 58 of 61 source-identified people have confirmed ^ identities. The three pending identities remain Carmen Martínez Socias, Nicolás Quintana Plasencia and Pedro Eugenio Botella Torres. The historic backfill adds Ángela López-Yuste Padial and Emma Galcerán Solsona from primary judicial copies.';
  };
  const classify = (record) => /magistrad|judge|presidenta/i.test(`${record.capacity_boundary || ''} ${record.verification_detail || ''}`) ? 'judge' : 'laj';
  Promise.all([
    fetch(dataUrl('matter-identity-registry-v1.la-laguna-judicial-people.json'), { cache: 'no-store' }).then(r => { if (!r.ok) throw new Error(`laguna ${r.status}`); return r.json(); }),
    fetch(dataUrl('matter-identity-registry-v1.historic-arrecife-judicial-people-20260902.json'), { cache: 'no-store' }).then(r => { if (!r.ok) throw new Error(`historic ${r.status}`); return r.json(); })
  ]).then(([laguna, historic]) => {
    updateText();
    const records = [...(laguna.records || []), ...(historic.records || [])];
    const append = (sectionSelector, rows, countText) => {
      const section = document.querySelector(sectionSelector); const list = section?.querySelector('.jp-list');
      if (!section || !list) return;
      rows.forEach(record => {
        if (list.querySelector(`[data-caepr-id="${record.id}"]`)) return;
        const link = document.createElement('a'); link.className = 'jp-person'; link.dataset.caeprId = record.id; link.dataset.caretState = record.identity_resolution; link.href = route(record);
        link.append(document.createTextNode(record.name)); const sup = document.createElement('sup'); sup.textContent = '^'; link.appendChild(sup); list.appendChild(link);
      });
      const eyebrow = section.querySelector('.eyebrow'); if (eyebrow) eyebrow.textContent = countText;
    };
    append(lang === 'es' ? '#judicatura' : '#judiciary', records.filter(r => classify(r) === 'judge'), lang === 'es' ? '20 / 20 CONFIRMADOS' : '20 / 20 CONFIRMED');
    append('#laj', records.filter(r => classify(r) === 'laj'), lang === 'es' ? '16 / 16 CONFIRMADOS' : '16 / 16 CONFIRMED');
    const firstContentSection = document.querySelector('main > .section');
    if (firstContentSection && !document.querySelector('[data-current-derived-register-note]')) {
      const p = document.createElement('p'); p.setAttribute('data-current-derived-register-note', '20260902b'); p.className = 'jp-note jp-good';
      p.innerHTML = lang === 'es' ? 'Control actual derivado: <a href="../../assets/data/justice-authority-register-current-v2.json">61 personas</a> · 58 ^ confirmadas · 3 pendientes. La cobertura histórica completa de expedientes oficiales permanece como brecha expresa.' : 'Current derived control: <a href="../../assets/data/justice-authority-register-current-v2.json">61 people</a> · 58 ^ confirmed · 3 pending. Complete historic official-docket coverage remains an express gap.';
      firstContentSection.querySelector('.shell')?.appendChild(p);
    }
  }).catch(error => console.error('Justice-professionals current overlay failed', error));
})();
"""
OVERLAY.write_text(overlay, encoding='utf-8')

# Remove the stale two-source/59-person assumptions from the canonical validator while preserving all other gates.
v = VALIDATOR.read_text(encoding='utf-8')
old_block = '''    base_audit = load_json(ROOT / current["person_sources"][0]["path"])
    supplement = load_json(ROOT / current["person_sources"][1]["path"])
    base_rows = [row for rows in base_audit.get("roles", {}).values() for row in rows]
    supplement_rows = supplement.get("records", [])
    base_ids = {row["caepr_id"] for row in base_rows}
    supplement_ids = {row["id"] for row in supplement_rows}
    require(len(base_rows) == 48 and len(supplement_rows) == 11, "Unexpected source census sizes")
    require(base_ids.isdisjoint(supplement_ids), "Current authority sources contain duplicate people")
    require(len(base_ids | supplement_ids) == current["derived_counts"]["unique_named_people"] == 59, "Derived people count mismatch")
    base_confirmed = sum(row["state"] == "CARET_CONFIRMED" for row in base_rows)
    supplement_confirmed = sum(row.get("identity_resolution") == "CARET_CONFIRMED" for row in supplement_rows)
    require(base_confirmed + supplement_confirmed == current["derived_counts"]["confirmed"] == 56, "Derived confirmed count mismatch")
    require(current["derived_counts"]["pending"] == 3, "Derived pending count mismatch")
    for identifier in base_ids | supplement_ids:
        require(identifier in records, f"Current authority person absent from CAEPR: {identifier}")
'''
new_block = '''    authority_ids: set[str] = set()
    confirmed_count = 0
    for descriptor in current.get("person_sources", []):
        source = load_json(ROOT / descriptor["path"])
        if isinstance(source.get("roles"), dict):
            source_rows = [row for rows in source.get("roles", {}).values() for row in rows]
            ids = {row["caepr_id"] for row in source_rows}
            confirmed = sum(row.get("state") == "CARET_CONFIRMED" for row in source_rows)
        else:
            source_rows = source.get("records", [])
            ids = {row["id"] for row in source_rows}
            confirmed = sum(row.get("identity_resolution") == "CARET_CONFIRMED" for row in source_rows)
        require(authority_ids.isdisjoint(ids), f"Current authority sources contain duplicate people in {descriptor['path']}")
        authority_ids |= ids
        confirmed_count += confirmed
    require(len(authority_ids) == current["derived_counts"]["unique_named_people"] == 61, "Derived people count mismatch")
    require(confirmed_count == current["derived_counts"]["confirmed"] == 58, "Derived confirmed count mismatch")
    require(current["derived_counts"]["pending"] == 3, "Derived pending count mismatch")
    for identifier in authority_ids:
        require(identifier in records, f"Current authority person absent from CAEPR: {identifier}")
'''
if old_block not in v:
    raise SystemExit('validator authority block anchor missing')
v = v.replace(old_block, new_block)
v = v.replace('require("[\'59\', 0]" in overlay_script and "[\'56\', 1]" in overlay_script, "Justice overlay does not expose current counts")', 'require("[\'61\', 0]" in overlay_script and "[\'58\', 1]" in overlay_script, "Justice overlay does not expose current counts")')
v = v.replace('f"{len(records)} CAEPR records; 59 current justice professionals; "', 'f"{len(records)} CAEPR records; 61 current justice professionals; "')
VALIDATOR.write_text(v, encoding='utf-8')

# Make both Master Register landing pages link the complete dedicated-page directory.
for path, href, label in [
    (ROOT/'es/registro-maestro-procedimientos/index.html', '../procedimientos/', 'Páginas de cada procedimiento'),
    (ROOT/'en/master-proceedings-register/index.html', '../proceedings/', 'Pages for every proceeding'),
]:
    if not path.exists():
        continue
    h = path.read_text(encoding='utf-8')
    if href not in h:
        marker = '<div class="hero-actions">'
        h = h.replace(marker, marker + f'<a class="secondary" href="{href}">{label}</a>', 1)
        path.write_text(h, encoding='utf-8')

# Add every dedicated page and both directory indexes to the sitemap when present.
if SITEMAP.exists():
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    tree = ET.parse(SITEMAP)
    root = tree.getroot()
    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'} if root.tag.startswith('{') else {}
    loc_tag = '{http://www.sitemaps.org/schemas/sitemap/0.9}loc' if ns else 'loc'
    url_tag = '{http://www.sitemaps.org/schemas/sitemap/0.9}url' if ns else 'url'
    existing = {n.text for n in root.findall('.//s:loc', ns)} if ns else {n.text for n in root.findall('.//loc')}
    urls = ['https://sbu001monterecco.github.io/por-derecho/es/procedimientos/', 'https://sbu001monterecco.github.io/por-derecho/en/proceedings/']
    for mid in by_id:
        urls.extend(['https://sbu001monterecco.github.io/por-derecho/' + routes[mid]['es'], 'https://sbu001monterecco.github.io/por-derecho/' + routes[mid]['en']])
    for loc in urls:
        if loc in existing:
            continue
        u = ET.SubElement(root, url_tag); ET.SubElement(u, loc_tag).text = loc
    tree.write(SITEMAP, encoding='utf-8', xml_declaration=True)

print('PROCEEDING_PAGES_OK', len(records), len(routes), sum(len(v) for v in formal.values()) // 2, sum(len(v) for v in textual.values()) // 2)
