#!/usr/bin/env python3
"""Run the P0 static patch with two robustness fixes kept separate for auditability."""

from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("p0patch", HERE / "apply_p0_static_criminal_framing.py")
assert SPEC and SPEC.loader
m = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)


def robust_insert_before_after_marker(text: str, marker: str, target: str, insert: str, label: str) -> str:
    """Insert before target whether the unique marker sits before or inside target."""
    if insert.strip() in text:
        return text
    start = text.find(marker)
    if start < 0:
        raise RuntimeError(f"{label}: section marker not found")
    idx = text.find(target, start)
    if idx < 0:
        idx = text.rfind(target, 0, start + len(marker))
    if idx < 0:
        raise RuntimeError(f"{label}: target not found around marker")
    return text[:idx] + insert + text[idx:]


m.insert_before_after_marker = robust_insert_before_after_marker


def patch_ricpe(rel: str, en: bool) -> None:
    t = m.read(rel)
    if en:
        t = m.replace_once(t, '<p class="eyebrow">Unitary record · updated 14 August 2026</p>', '<p class="eyebrow">Formal communication submitted · 17 August 2026 · unitary record updated 20 August 2026</p>', "RICPE EN eyebrow")
        old_actions = '''          <div class="actions">\n            <a class="button" href="#unitary-question">Understand the central question</a>\n            <a class="button secondary" href="#what-the-2021-alert-communicated">See the 2021 alert</a>\n            <a class="button secondary" href="#title-control-2018-pwc-units">Creditor, OB REM and title</a>\n            <a class="button secondary" href="../sun-park-takeover-7-june-2018/">7 June: full dossier</a>\n            <a class="button secondary" href="#three-ricpe-realities">See the on-camera claims</a>\n            <a class="button secondary" href="#jsp-units">JSP / Montelanza, S.L. units</a>\n            <a class="button secondary" href="#alert-legal-defence-2021">2021 alert / Sony Ganwani</a>\n            <a class="button secondary" href="#ricpe-audience-map">Audiences and notification</a>\n            <a class="button secondary" href="#harm-perimeter">Patrimonial perimeter</a>\n            <a class="button secondary" href="#boundaries">See evidentiary boundaries</a>\n          </div>'''
        new_actions = '''          <div class="actions">\n            <a class="button" href="#unitary-question">Central question</a>\n            <a class="button secondary" href="#three-ricpe-realities">What changed?</a>\n            <a class="button secondary" href="../ricpe-documentary-accountability/">RICPE controls</a>\n            <a class="button secondary" href="../cnmv-ricpe-verification/">CNMV gateway</a>\n            <a class="button secondary" href="../ricpe-idoneidad-series-f-g/">Series F/G · suitability</a>\n            <a class="button secondary" href="#response">Response / status</a>\n          </div>'''
        t = m.replace_once(t, old_actions, new_actions, "RICPE EN actions")
        t = m.replace_once(t, '<div><span>Status</span><strong>No merits finding against RIC located</strong></div>', '<div><span>Communication</span><strong>Submitted 17 Aug 2026 · platform acknowledgment established</strong></div>\n          <div><span>Open status</span><strong>Admission · investigation · conflict review · preservation · Board treatment · merits not established</strong></div>', "RICPE EN status")
        if 'id="ricpe-series-fg-control"' not in t:
            marker = '\n\n\n\n    <section class="section" id="ground-zero-minutes-2011-2022"'
            idx = t.find(marker)
            if idx < 0:
                raise RuntimeError("RICPE EN Series F/G insertion point not found")
            bridge = '''\n      <div class="shell"><aside class="pressure-maxim" id="ricpe-series-fg-control" role="note" aria-label="Series F/G and suitability control"><strong>2022–2023 control node:</strong><span> the later financing layer is separated by source. The 20-September-2023 prospectus components total €6,570,713.56; a separate audited-accounts reconstruction totals €6,573,703.10. The €2,989.54 difference remains open. The dedicated record asks whether Decree 224/2022 and the binding AEAT report covered Series F, Series G, both or a later modification, and what each instrument actually financed. <a href="../ricpe-idoneidad-series-f-g/">Open the Series F/G control →</a></span></aside></div>'''
            t = t[:idx] + bridge + t[idx:]
    else:
        t = m.replace_once(t, '<p class="eyebrow">Registro unitario · actualizado 14 agosto 2026</p>', '<p class="eyebrow">Comunicación formal presentada · 17 agosto 2026 · registro unitario actualizado 20 agosto 2026</p>', "RICPE ES eyebrow")
        old_actions = '''          <div class="actions">\n            <a class="button" href="#pregunta-unitaria">Entender la cuestión central</a>\n            <a class="button secondary" href="#alerta-2021-que-se-comunico">Ver alerta 2021</a>\n            <a class="button secondary" href="#control-titulo-2018-pwc-unidades">Acreedor, OB REM y título</a>\n            <a class="button secondary" href="../toma-control-sun-park-7-junio-2018/">7 junio: dossier completo</a>\n            <a class="button secondary" href="#tres-realidades-ricpe">Ver lo dicho ante cámara</a>\n            <a class="button secondary" href="#unidades-jsp">Unidades JSP / Montelanza, S.L.</a>\n            <a class="button secondary" href="#alerta-defensa-2021">Alerta 2021 / Sony Ganwani</a>\n            <a class="button secondary" href="#mapa-audiencias-ricpe">Audiencias y notificación</a>\n            <a class="button secondary" href="#perimetro-dano">Perímetro patrimonial</a>\n            <a class="button secondary" href="#limites">Ver límites probatorios</a>\n          </div>'''
        new_actions = '''          <div class="actions">\n            <a class="button" href="#pregunta-unitaria">Pregunta central</a>\n            <a class="button secondary" href="#tres-realidades-ricpe">¿Qué cambió?</a>\n            <a class="button secondary" href="../ricpe-responsabilidad-documental/">Controles RICPE</a>\n            <a class="button secondary" href="../cnmv-ricpe-verificacion/">Puerta CNMV</a>\n            <a class="button secondary" href="../ricpe-idoneidad-series-f-g/">Series F/G · idoneidad</a>\n            <a class="button secondary" href="#respuesta">Respuesta / estado</a>\n          </div>'''
        t = m.replace_once(t, old_actions, new_actions, "RICPE ES actions")
        t = m.replace_once(t, '<div><span>Estado</span><strong>Sin resolución de fondo localizada contra RIC</strong></div>', '<div><span>Comunicación</span><strong>Presentada 17 ago 2026 · acuse de plataforma establecido</strong></div>\n          <div><span>Estado abierto</span><strong>Admisión · investigación · conflictos · preservación · Consejo · fondo no establecidos</strong></div>', "RICPE ES status")
        if 'id="ricpe-series-fg-control"' not in t:
            marker = '\n\n\n\n    <section class="section" id="punto-cero-actas-2011-2022"'
            idx = t.find(marker)
            if idx < 0:
                raise RuntimeError("RICPE ES Series F/G insertion point not found")
            bridge = '''\n      <div class="shell"><aside class="pressure-maxim" id="ricpe-series-fg-control" role="note" aria-label="Control Series F/G e idoneidad"><strong>Nodo de control 2022–2023:</strong><span> la financiación posterior se separa por fuente. Los componentes del folleto de 20-sep-2023 suman 6.570.713,56 €; una reconstrucción separada de cuentas auditadas suma 6.573.703,10 €. La diferencia de 2.989,54 € permanece abierta. El registro específico pregunta si el Decreto 224/2022 y el informe vinculante AEAT cubrieron la Serie F, la Serie G, ambas o una modificación posterior, y qué financió realmente cada instrumento. <a href="../ricpe-idoneidad-series-f-g/">Abrir el control Series F/G →</a></span></aside></div>'''
            t = t[:idx] + bridge + t[idx:]
    m.write(rel, t)


m.patch_ricpe = patch_ricpe

if __name__ == "__main__":
    raise SystemExit(m.main())
