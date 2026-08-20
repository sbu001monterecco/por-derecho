#!/usr/bin/env python3
"""Finish the P0 static pass after the deterministic source patch.

This keeps current-feed dates aligned, improves the public prose, wraps compact
cross-links in valid page sections, and adds direct Series F/G discovery from the
home reverse-chronology path.
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHANGED: list[str] = []


def get(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def put(rel: str, text: str) -> None:
    p = ROOT / rel
    old = p.read_text(encoding="utf-8")
    if old != text:
        p.write_text(text, encoding="utf-8")
        CHANGED.append(rel)


def one(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"{label}: source text not found")
    return text.replace(old, new, 1)


def updates(rel: str, en: bool) -> None:
    t = get(rel)
    if en:
        t = one(t, '<span>Latest material update</span><strong>18 August 2026</strong>', '<span>Latest material update</span><strong>20 August 2026</strong>', 'updates EN date')
        if 'id="architecture-node-20aug"' not in t:
            anchor = '    <section class="updates-section"><div class="shell"><section class="date-group" aria-labelledby="ricpe-series-fg-date">'
            entry = '''    <section class="updates-section"><div class="shell"><section class="date-group" aria-labelledby="architecture-node-date"><h2 id="architecture-node-date">20 August 2026 · architecture / documentary chain</h2><div class="update-stream"><article class="material-update institutional" id="architecture-node-20aug"><div class="update-meta"><span class="new">New</span><span>Architecture</span><span>COALZ / COAGC</span><span>Documentary chain</span></div><h3>The 25 February 2022 visado is analysed as a documentary node, not as a stand-alone finding</h3><p>The new bilingual source-controlled record places the visado within a wider sequence of apparent authority, commission, project, Yaiza, tourism, investment, finance, RIC/REF, public support, operation and judicial evidence. It records COALZ entries 26/008230, 26/008474 and 26/008476 with their limits, the unresolved COAGC professional-data discrepancy and the contextual PwC–Grant Thornton–San Telmo/RICPE–RSM chronology.</p><p><strong>Boundary:</strong> registration, forwarding, distribution or professional involvement does not itself establish an investigation, breach, complicity or merits finding. The page identifies the records and the finite questions each competent body can resolve.</p><div class="update-actions"><a class="button" href="../architecture-documentary-node-jdam/">Open documentary node →</a><a class="button secondary" href="../public-authority-unitary-case-reconstruction/">Independent clean room</a></div></article></div></section></div></section>\n\n'''
            idx = t.find(anchor)
            if idx < 0:
                raise RuntimeError('updates EN 20-Aug insertion point not found')
            t = t[:idx] + entry + t[idx:]
    else:
        t = one(t, '<span>Última actualización material</span><strong>18 agosto 2026</strong>', '<span>Última actualización material</span><strong>20 agosto 2026</strong>', 'updates ES date')
        if 'id="arquitectura-nodo-20ago"' not in t:
            anchor = '    <section class="updates-section"><div class="shell"><section class="date-group" aria-labelledby="ricpe-series-fg-date">'
            entry = '''    <section class="updates-section"><div class="shell"><section class="date-group" aria-labelledby="arquitectura-nodo-date"><h2 id="arquitectura-nodo-date">20 agosto 2026 · arquitectura / cadena documental</h2><div class="update-stream"><article class="material-update institutional" id="arquitectura-nodo-20ago"><div class="update-meta"><span class="new">Nuevo</span><span>Arquitectura</span><span>COALZ / COAGC</span><span>Cadena documental</span></div><h3>El visado de 25 de febrero de 2022 se analiza como nodo documental, no como hallazgo autónomo</h3><p>El nuevo registro bilingüe source-controlled sitúa el visado dentro de una secuencia más amplia de autoridad aparente, encargo, proyecto, Yaiza, turismo, inversión, financiación, RIC/REF, apoyo público, operación y prueba judicial. Registra las entradas COALZ 26/008230, 26/008474 y 26/008476 con sus límites, la discrepancia profesional COAGC todavía abierta y la cronología contextual PwC–Grant Thornton–San Telmo/RICPE–RSM.</p><p><strong>Límite:</strong> registro, traslado, distribución o intervención profesional no establecen por sí solos investigación, infracción, complicidad ni decisión de fondo. La página identifica los documentos y las preguntas finitas que puede resolver cada órgano competente.</p><div class="update-actions"><a class="button" href="../arquitectura-nodo-documental-jdam/">Abrir nodo documental →</a><a class="button secondary" href="../reconstruccion-unitaria-autoridades-publicas/">Sala limpia independiente</a></div></article></div></section></div></section>\n\n'''
            idx = t.find(anchor)
            if idx < 0:
                raise RuntimeError('updates ES 20-Aug insertion point not found')
            t = t[:idx] + entry + t[idx:]
    put(rel, t)


def community(rel: str, en: bool) -> None:
    t = get(rel)
    if en:
        t = one(t, 'Chronological dossier · updated 13 August 2026', 'Chronological dossier · updated 20 August 2026', 'community EN date')
        t = one(t, 'Attributed investigative hypothesis; no competent criminal finding establishing a concerted plan located', 'Attributed investigative hypothesis; no competent criminal finding establishing a concerted plan has been located', 'community EN status grammar')
    else:
        t = one(t, 'Dossier cronológico · actualizado 13 agosto 2026', 'Dossier cronológico · actualizado 20 agosto 2026', 'community ES date')
        t = one(t, 'Hipótesis investigativa atribuida; no hallazgo penal competente que establezca un plan concertado', 'Hipótesis investigativa atribuida; no se ha localizado una resolución penal competente que establezca un plan concertado', 'community ES status grammar')
    put(rel, t)


def cleanroom(rel: str, en: bool) -> None:
    t = get(rel)
    if en:
        t = one(t, '<h2>The first screen should follow the conversions that can change several branches at once.</h2>', '<h2>Six conversions that can change several branches at once.</h2>', 'cleanroom EN heading')
        t = one(t, '<h2>Do not prosecute the narrative. Prove or reject each conversion.</h2>', '<h2>Do not convert the narrative into a criminal conclusion. Prove or reject each conversion.</h2>', 'cleanroom EN matrix heading')
    else:
        t = one(t, '<h2>La primera pantalla debe seguir las conversiones capaces de cambiar varias ramas a la vez.</h2>', '<h2>Seis conversiones que pueden cambiar varias ramas a la vez.</h2>', 'cleanroom ES heading')
        t = one(t, '<h2>No perseguir penalmente la narrativa. Probar o descartar cada conversión.</h2>', '<h2>No convertir la narrativa en conclusión penal. Probar o descartar cada conversión.</h2>', 'cleanroom ES matrix heading')
    put(rel, t)


def wrap_series_link(rel: str, shell_class: str, en: bool, alt: bool = False) -> None:
    t = get(rel)
    lead = '<p class="ok-boundary"><strong>Series F/G control:' if en else '<p class="ok-boundary"><strong>Control Series F/G:'
    idx = t.find(lead)
    if idx < 0:
        raise RuntimeError(f'{rel}: Series F/G compact link not found')
    end = t.find('</p>', idx)
    if end < 0:
        raise RuntimeError(f'{rel}: Series F/G paragraph end not found')
    end += 4
    paragraph = t[idx:end]
    if t[max(0, idx-80):idx].find('series-fg-static-link') >= 0:
        return
    section_class = 'section alt' if alt else 'section'
    wrapped = f'<section class="{section_class}" data-series-fg-static-link><div class="shell {shell_class}">{paragraph}</div></section>'
    t = t[:idx] + wrapped + t[end:]
    put(rel, t)


def ricpe_bridge(rel: str, en: bool) -> None:
    t = get(rel)
    marker = '<div class="shell"><aside class="pressure-maxim" id="ricpe-series-fg-control"'
    idx = t.find(marker)
    if idx < 0:
        raise RuntimeError(f'{rel}: RICPE Series F/G bridge not found')
    end = t.find('</div>', idx)
    if end < 0:
        raise RuntimeError(f'{rel}: RICPE Series F/G bridge end not found')
    end += 6
    existing = t[idx:end]
    if '<section class="section alt" data-ricpe-series-fg-static>' in t[max(0, idx-120):idx+30]:
        return
    wrapped = f'<section class="section alt" data-ricpe-series-fg-static>{existing}</section>'
    t = t[:idx] + wrapped + t[end:]
    put(rel, t)


def home_series(rel: str, en: bool) -> None:
    t = get(rel)
    if 'data-series-fg-priority' in t:
        return
    marker = '<div class="priority-links">'
    start = t.find(marker)
    if start < 0:
        raise RuntimeError(f'{rel}: priority-links container not found')
    end = t.find('</div>', start)
    if end < 0:
        raise RuntimeError(f'{rel}: priority-links closing div not found')
    link = '<a data-series-fg-priority href="ricpe-idoneidad-series-f-g/">Series F/G</a>'
    t = t[:end] + link + t[end:]
    put(rel, t)


def validate() -> None:
    checks = {
        'es/actualizaciones/index.html': ['20 agosto 2026', 'arquitectura-nodo-20ago', 'ricpe-series-fg-18ago'],
        'en/updates/index.html': ['20 August 2026', 'architecture-node-20aug', 'ricpe-series-fg-18aug'],
        'es/comunidad-instrumentalizacion/actas-2011-2022/index.html': ['actualizado 20 agosto 2026', 'no se ha localizado una resolución penal competente'],
        'en/community-instrumentalisation/minutes-2011-2022/index.html': ['updated 20 August 2026', 'has been located'],
        'es/reconstruccion-unitaria-autoridades-publicas/index.html': ['Seis conversiones que pueden cambiar', 'No convertir la narrativa en conclusión penal'],
        'en/public-authority-unitary-case-reconstruction/index.html': ['Six conversions that can change', 'Do not convert the narrative into a criminal conclusion'],
        'es/index.html': ['data-series-fg-priority'],
        'en/index.html': ['data-series-fg-priority'],
    }
    for rel, markers in checks.items():
        text = get(rel)
        for marker in markers:
            if marker not in text:
                raise RuntimeError(f'{rel}: missing {marker!r}')
    for rel in [
        'es/cnmv-ricpe-verificacion/index.html','en/cnmv-ricpe-verification/index.html',
        'es/incentivos-regionales-gc836-p06/index.html','en/regional-incentives-gc836-p06/index.html',
        'es/snca-fondos-europeos-trazabilidad/index.html','en/snca-eu-funds-traceability/index.html']:
        if 'data-series-fg-static-link' not in get(rel):
            raise RuntimeError(f'{rel}: compact Series F/G link not wrapped')
    for rel in ['es/ric-private-equity-sun-park/index.html','en/ric-private-equity-sun-park/index.html']:
        if 'data-ricpe-series-fg-static' not in get(rel):
            raise RuntimeError(f'{rel}: RICPE Series F/G bridge not wrapped')


def main() -> int:
    updates('es/actualizaciones/index.html', False)
    updates('en/updates/index.html', True)
    community('es/comunidad-instrumentalizacion/actas-2011-2022/index.html', False)
    community('en/community-instrumentalisation/minutes-2011-2022/index.html', True)
    cleanroom('es/reconstruccion-unitaria-autoridades-publicas/index.html', False)
    cleanroom('en/public-authority-unitary-case-reconstruction/index.html', True)
    wrap_series_link('es/cnmv-ricpe-verificacion/index.html', 'cnmv', False)
    wrap_series_link('en/cnmv-ricpe-verification/index.html', 'cnmv', True)
    wrap_series_link('es/incentivos-regionales-gc836-p06/index.html', 'ir', False, True)
    wrap_series_link('en/regional-incentives-gc836-p06/index.html', 'ir', True, True)
    wrap_series_link('es/snca-fondos-europeos-trazabilidad/index.html', 'eu', False)
    wrap_series_link('en/snca-eu-funds-traceability/index.html', 'eu', True)
    ricpe_bridge('es/ric-private-equity-sun-park/index.html', False)
    ricpe_bridge('en/ric-private-equity-sun-park/index.html', True)
    home_series('es/index.html', False)
    home_series('en/index.html', True)
    validate()
    print('P0 FINISH PASSED')
    print('\n'.join(f'- {x}' for x in CHANGED))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
