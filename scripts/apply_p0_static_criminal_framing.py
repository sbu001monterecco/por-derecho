#!/usr/bin/env python3
"""Apply the 20-Aug-2026 P0 static-source and criminal-framing corrections.

This script deliberately edits the static HTML itself. It does not rely on the
runtime journey layer to correct materially important wording for no-JS readers,
search indexes, archives or copied snippets.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CHANGED: list[str] = []


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def write(rel: str, text: str) -> None:
    path = ROOT / rel
    old = path.read_text(encoding="utf-8")
    if old != text:
        path.write_text(text, encoding="utf-8")
        CHANGED.append(rel)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"{label}: expected source text not found")
    return text.replace(old, new, 1)


def replace_all_required(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"{label}: expected source text not found")
    return text.replace(old, new)


def insert_after(text: str, marker: str, insert: str, label: str) -> str:
    if insert.strip() in text:
        return text
    idx = text.find(marker)
    if idx < 0:
        raise RuntimeError(f"{label}: marker not found")
    idx += len(marker)
    return text[:idx] + insert + text[idx:]


def insert_before_after_marker(text: str, marker: str, target: str, insert: str, label: str) -> str:
    if insert.strip() in text:
        return text
    start = text.find(marker)
    if start < 0:
        raise RuntimeError(f"{label}: section marker not found")
    idx = text.find(target, start)
    if idx < 0:
        raise RuntimeError(f"{label}: target not found after marker")
    return text[:idx] + insert + text[idx:]


def replace_section_containing(text: str, marker: str, new_section: str, label: str) -> str:
    m = text.find(marker)
    if m < 0:
        raise RuntimeError(f"{label}: unique marker not found")
    start = text.rfind("<section", 0, m)
    if start < 0:
        raise RuntimeError(f"{label}: opening section not found")
    end = text.find("</section>", m)
    if end < 0:
        raise RuntimeError(f"{label}: closing section not found")
    end += len("</section>")
    return text[:start] + new_section + text[end:]


def patch_updates_es() -> None:
    rel = "es/actualizaciones/index.html"
    t = read(rel)
    t = replace_once(
        t,
        '<span>Última actualización material</span><strong>14 agosto 2026</strong>',
        '<span>Última actualización material</span><strong>18 agosto 2026</strong>',
        "updates ES hero date",
    )
    if 'id="ricpe-series-fg-18ago"' not in t:
        marker = '</section>\n\n    <section class="updates-section">'
        insert = '''

    <section class="updates-section"><div class="shell"><section class="date-group" aria-labelledby="ricpe-series-fg-date"><h2 id="ricpe-series-fg-date">18 agosto 2026 · RICPE / MYND Yaiza</h2><div class="update-stream"><article class="material-update institutional" id="ricpe-series-fg-18ago"><div class="update-meta"><span class="new">Nuevo</span><span>Series F/G</span><span>Idoneidad RIC</span><span>Uso de fondos</span></div><h3>Series F/G y Decreto 224/2022: el expediente debe identificar qué autorizó cada acto y qué financió cada euro</h3><p>Las cuentas auditadas 2023 identifican una Serie F vinculada al proyecto Hotel MYND Yaiza por 1.598.849,32 € y una Serie G vinculada a creación de empleo por 4.974.853,78 €. El folleto de 20 de septiembre de 2023 contiene una suma distinta de sus dos componentes —6.570.713,56 €— frente a 6.573.703,10 € en la reconstrucción separada de cuentas. La diferencia de 2.989,54 € queda abierta y atribuida a sus fuentes.</p><p><strong>Cuestión pública:</strong> si el Decreto 224/2022 y el informe vinculante AEAT de 17 de noviembre de 2022 cubrieron F, G, ambas o una modificación posterior; y qué facturas, pagos, empleo u obligación financiaron realmente cada instrumento. No se publica como fraude ni como doble financiación probada.</p><div class="update-actions"><a class="button" href="../ricpe-idoneidad-series-f-g/">Abrir Series F/G →</a><a class="button secondary" href="../cnmv-ricpe-verificacion/">Puerta CNMV</a><a class="button secondary" href="../mismo-hotel-multiples-vidas-financieras/">Conciliación financiera</a></div></article></div></section></div></section>

    <section class="updates-section"><div class="shell"><section class="date-group" aria-labelledby="ricpe-filing-date"><h2 id="ricpe-filing-date">17 agosto 2026 · comunicación formal RICPE</h2><div class="update-stream"><article class="material-update institutional" id="ricpe-formal-prefiling-17aug"><div class="update-meta"><span class="new">Presentada</span><span>Canal Ético</span><span>Acuse de plataforma</span></div><h3>La comunicación formal a RICPE consta presentada; los estados posteriores siguen abiertos</h3><p>La pantalla final y un correo nativo de plataforma de 17 agosto 2026, 22:51:17 UTC, corroboran la presentación y la asignación de un código privado de seguimiento. Un registro Gmail contemporáneo conserva además un PDF firmado de 22 páginas, 447.975 bytes, SHA-256 <code>b455075ceda7841471ef5f4ebfbb784ccd00357439aa8bf282e736fe4757832c</code>, cuya firma criptográfica valida.</p><p><strong>Límite:</strong> la identidad byte a byte de ese PDF con el adjunto exacto del Canal permanece abierta; tampoco constan todavía admisión, investigación, control de conflictos, preservación, tratamiento por el Consejo ni decisión sobre el fondo. Las credenciales permanecen privadas.</p><div class="update-actions"><a class="button" href="../ric-private-equity-sun-park/">Abrir expediente RICPE →</a><a class="button secondary" href="../ricpe-responsabilidad-documental/">Controles documentales</a></div></article></div></section></div></section>'''
        idx = t.find(marker)
        if idx < 0:
            raise RuntimeError("updates ES insertion point not found")
        t = t[:idx + len('</section>')] + insert + t[idx + len('</section>'):]
    write(rel, t)


def patch_updates_en() -> None:
    rel = "en/updates/index.html"
    t = read(rel)
    t = replace_once(
        t,
        '<span>Latest material update</span><strong>14 August 2026</strong>',
        '<span>Latest material update</span><strong>18 August 2026</strong>',
        "updates EN hero date",
    )
    if 'id="ricpe-series-fg-18aug"' not in t:
        marker = '</section>\n\n    <section class="updates-section">'
        insert = '''

    <section class="updates-section"><div class="shell"><section class="date-group" aria-labelledby="ricpe-series-fg-date"><h2 id="ricpe-series-fg-date">18 August 2026 · RICPE / MYND Yaiza</h2><div class="update-stream"><article class="material-update institutional" id="ricpe-series-fg-18aug"><div class="update-meta"><span class="new">New</span><span>Series F/G</span><span>RIC suitability</span><span>Use of funds</span></div><h3>Series F/G and Decree 224/2022: the file should identify what each act authorised and what each euro financed</h3><p>The 2023 audited accounts identify Series F linked to the Hotel MYND Yaiza project at €1,598,849.32 and Series G linked to employment creation at €4,974,853.78. The 20 September 2023 prospectus produces a different sum from its two components — €6,570,713.56 — compared with €6,573,703.10 in the separate accounts reconstruction. The €2,989.54 difference remains open and source-attributed.</p><p><strong>Public question:</strong> whether Decree 224/2022 and the binding AEAT report of 17 November 2022 covered F, G, both or a later modification, and which invoices, payments, employment or obligation each instrument actually financed. It is not published as fraud or proved duplicate funding.</p><div class="update-actions"><a class="button" href="../ricpe-idoneidad-series-f-g/">Open Series F/G →</a><a class="button secondary" href="../cnmv-ricpe-verification/">CNMV gateway</a><a class="button secondary" href="../same-hotel-multiple-financial-lives/">Financial reconciliation</a></div></article></div></section></div></section>

    <section class="updates-section"><div class="shell"><section class="date-group" aria-labelledby="ricpe-filing-date"><h2 id="ricpe-filing-date">17 August 2026 · formal RICPE communication</h2><div class="update-stream"><article class="material-update institutional" id="ricpe-formal-prefiling-17aug"><div class="update-meta"><span class="new">Submitted</span><span>Ethical Channel</span><span>Platform acknowledgment</span></div><h3>The formal RICPE communication is established as submitted; later procedural states remain open</h3><p>The final platform screen and a native platform email dated 17 August 2026 at 22:51:17 UTC corroborate submission and assignment of a private follow-up code. A contemporaneous Gmail record also preserves a signed 22-page PDF, 447,975 bytes, SHA-256 <code>b455075ceda7841471ef5f4ebfbb784ccd00357439aa8bf282e736fe4757832c</code>, whose cryptographic signature validates.</p><p><strong>Boundary:</strong> byte-for-byte identity between that recovered PDF and the exact Channel attachment remains open; admission, investigation, conflict review, preservation, Board treatment and merits are also not established. Credentials remain private.</p><div class="update-actions"><a class="button" href="../ric-private-equity-sun-park/">Open RICPE record →</a><a class="button secondary" href="../ricpe-documentary-accountability/">Documentary controls</a></div></article></div></section></div></section>'''
        idx = t.find(marker)
        if idx < 0:
            raise RuntimeError("updates EN insertion point not found")
        t = t[:idx + len('</section>')] + insert + t[idx + len('</section>'):]
    write(rel, t)


def patch_ricpe(rel: str, en: bool) -> None:
    t = read(rel)
    if en:
        t = replace_once(t, '<p class="eyebrow">Unitary record · updated 14 August 2026</p>', '<p class="eyebrow">Formal communication submitted · 17 August 2026 · unitary record updated 20 August 2026</p>', "RICPE EN eyebrow")
        old_actions = '''          <div class="actions">\n            <a class="button" href="#unitary-question">Understand the central question</a>\n            <a class="button secondary" href="#what-the-2021-alert-communicated">See the 2021 alert</a>\n            <a class="button secondary" href="#title-control-2018-pwc-units">Creditor, OB REM and title</a>\n            <a class="button secondary" href="../sun-park-takeover-7-june-2018/">7 June: full dossier</a>\n            <a class="button secondary" href="#three-ricpe-realities">See the on-camera claims</a>\n            <a class="button secondary" href="#jsp-units">JSP / Montelanza, S.L. units</a>\n            <a class="button secondary" href="#alert-legal-defence-2021">2021 alert / Sony Ganwani</a>\n            <a class="button secondary" href="#ricpe-audience-map">Audiences and notification</a>\n            <a class="button secondary" href="#harm-perimeter">Patrimonial perimeter</a>\n            <a class="button secondary" href="#boundaries">See evidentiary boundaries</a>\n          </div>'''
        new_actions = '''          <div class="actions">\n            <a class="button" href="#unitary-question">Central question</a>\n            <a class="button secondary" href="#psr-ricpe-five-docs">What changed?</a>\n            <a class="button secondary" href="../ricpe-documentary-accountability/">RICPE controls</a>\n            <a class="button secondary" href="../cnmv-ricpe-verification/">CNMV gateway</a>\n            <a class="button secondary" href="../ricpe-idoneidad-series-f-g/">Series F/G · suitability</a>\n            <a class="button secondary" href="#response">Response / status</a>\n          </div>'''
        t = replace_once(t, old_actions, new_actions, "RICPE EN actions")
        t = replace_once(t, '<div><span>Status</span><strong>No merits finding against RIC located</strong></div>', '<div><span>Communication</span><strong>Submitted 17 Aug 2026 · platform acknowledgment established</strong></div>\n          <div><span>Open status</span><strong>Admission · investigation · conflict review · preservation · Board treatment · merits not established</strong></div>', "RICPE EN status")
        bridge = '''\n      <div class="shell"><aside class="pressure-maxim" id="ricpe-series-fg-control" role="note" aria-label="Series F/G and suitability control"><strong>2022–2023 control node:</strong><span> the later financing layer is now separated into source-specific Series F/G records. The 20-September-2023 prospectus components total €6,570,713.56; a separate audited-accounts reconstruction totals €6,573,703.10. The €2,989.54 difference remains open. The dedicated record asks whether Decree 224/2022 and the binding AEAT report covered Series F, Series G, both or a later modification, and what each instrument actually financed. <a href="../ricpe-idoneidad-series-f-g/">Open the Series F/G control →</a></span></aside></div>'''
        t = insert_after(t, '</div>\n    </section>\n\n\n\n    <section class="section" id="ground-zero-minutes-2011-2022"', bridge + '\n\n    <section class="section" id="ground-zero-minutes-2011-2022"', "RICPE EN Series F/G bridge") if 'id="ricpe-series-fg-control"' not in t else t
    else:
        t = replace_once(t, '<p class="eyebrow">Registro unitario · actualizado 14 agosto 2026</p>', '<p class="eyebrow">Comunicación formal presentada · 17 agosto 2026 · registro unitario actualizado 20 agosto 2026</p>', "RICPE ES eyebrow")
        old_actions = '''          <div class="actions">\n            <a class="button" href="#pregunta-unitaria">Entender la cuestión central</a>\n            <a class="button secondary" href="#alerta-2021-que-se-comunico">Ver alerta 2021</a>\n            <a class="button secondary" href="#control-titulo-2018-pwc-unidades">Acreedor, OB REM y título</a>\n            <a class="button secondary" href="../toma-control-sun-park-7-junio-2018/">7 junio: dossier completo</a>\n            <a class="button secondary" href="#tres-realidades-ricpe">Ver lo dicho ante cámara</a>\n            <a class="button secondary" href="#unidades-jsp">Unidades JSP / Montelanza, S.L.</a>\n            <a class="button secondary" href="#alerta-defensa-2021">Alerta 2021 / Sony Ganwani</a>\n            <a class="button secondary" href="#mapa-audiencias-ricpe">Audiencias y notificación</a>\n            <a class="button secondary" href="#perimetro-dano">Perímetro patrimonial</a>\n            <a class="button secondary" href="#limites">Ver límites probatorios</a>\n          </div>'''
        new_actions = '''          <div class="actions">\n            <a class="button" href="#pregunta-unitaria">Pregunta central</a>\n            <a class="button secondary" href="#psr-ricpe-five-docs">¿Qué cambió?</a>\n            <a class="button secondary" href="../ricpe-responsabilidad-documental/">Controles RICPE</a>\n            <a class="button secondary" href="../cnmv-ricpe-verificacion/">Puerta CNMV</a>\n            <a class="button secondary" href="../ricpe-idoneidad-series-f-g/">Series F/G · idoneidad</a>\n            <a class="button secondary" href="#respuesta">Respuesta / estado</a>\n          </div>'''
        t = replace_once(t, old_actions, new_actions, "RICPE ES actions")
        t = replace_once(t, '<div><span>Estado</span><strong>Sin resolución de fondo localizada contra RIC</strong></div>', '<div><span>Comunicación</span><strong>Presentada 17 ago 2026 · acuse de plataforma establecido</strong></div>\n          <div><span>Estado abierto</span><strong>Admisión · investigación · conflictos · preservación · Consejo · fondo no establecidos</strong></div>', "RICPE ES status")
        if 'id="ricpe-series-fg-control"' not in t:
            marker = '\n\n\n\n    <section class="section" id="punto-cero-actas-2011-2022"'
            idx = t.find(marker)
            if idx < 0:
                raise RuntimeError("RICPE ES Series F/G insertion point not found")
            bridge = '''\n      <div class="shell"><aside class="pressure-maxim" id="ricpe-series-fg-control" role="note" aria-label="Control Series F/G e idoneidad"><strong>Nodo de control 2022–2023:</strong><span> la financiación posterior se separa ahora por fuente. Los componentes del folleto de 20-sep-2023 suman 6.570.713,56 €; una reconstrucción separada de cuentas auditadas suma 6.573.703,10 €. La diferencia de 2.989,54 € permanece abierta. El registro específico pregunta si el Decreto 224/2022 y el informe vinculante AEAT cubrieron la Serie F, la Serie G, ambas o una modificación posterior, y qué financió realmente cada instrumento. <a href="../ricpe-idoneidad-series-f-g/">Abrir el control Series F/G →</a></span></aside></div>'''
            t = t[:idx] + bridge + t[idx:]
    write(rel, t)


def patch_community(rel: str, en: bool) -> None:
    t = read(rel)
    if en:
        t = replace_once(t, '<title>Sun Park minutes 2011–2022 — debt, voting and authority</title>', '<title>Sun Park minutes 2011–2022 — debt, voting, authority and investigative element test</title>', "community EN title")
        t = replace_once(t, '<meta name="description" content="Documented chronology of Sun Park meetings and minutes from 2011 to 2022, the named actors, notice to the insolvency administrator, and the alleged production and propagation of authority.">', '<meta name="description" content="Documented chronology of Sun Park meetings and minutes from 2011 to 2022, with a fact-first actor, knowledge, use, reliance and investigative-element test before any offence characterisation.">', "community EN description")
        t = replace_once(t, '<a href="#criminal-theory">Criminal Code</a>', '<a href="#criminal-theory">Criminal / investigative test</a>', "community EN nav")
        t = replace_once(t, '<a class="button secondary" href="#criminal-theory">See the alleged criminal-law characterisation</a>', '<a class="button secondary" href="#criminal-theory">See the criminal / investigative element test</a>', "community EN hero action")
        t = replace_once(t, '<div><span>Status</span><strong>Express criminal-law theory; no final conviction</strong></div>', '<div><span>Status</span><strong>Attributed investigative hypothesis; no competent criminal finding establishing a concerted plan located</strong></div>', "community EN status")
        t = replace_once(t, '<div><p class="kicker">Public characterisation by Gil Marer · no conviction</p><h2 id="criminal-theory-title">The allegation is criminal; proof must be element by element.</h2></div>', '<div><p class="kicker">Attributed investigative hypothesis · no competent criminal finding</p><h2 id="criminal-theory-title">Facts, actor, knowledge, use and reliance come before offence labels.</h2></div>', "community EN criminal heading")
        t = replace_once(t, '<p>The minutes are invoked as a unitary patrimonial hypothesis of potential criminal relevance, pending judicial determination. A debatable meeting, disputed debt or adverse outcome is not automatically a crime.</p>', '<p>The records justify an investigative test, not an offence-first conclusion. For each event the page must identify the actor, authority, contemporaneous knowledge, contrary notice, document or omission, recipient, reliance, benefit/harm and strongest lawful explanation before considering any possible criminal characterisation.</p>', "community EN criminal intro")
        insert = '''        <div class="control-table-wrap" id="criminal-event-matrix">\n          <table class="control-table document-status">\n            <thead><tr><th>Event / conversion</th><th>What the current record establishes</th><th>Knowledge / use / reliance to test</th><th>Strongest lawful alternative</th><th>Status</th></tr></thead>\n            <tbody>\n              <tr><td><strong>22 Jun 2011 · debt → voting → office/custody</strong></td><td>LPB appeared with a large percentage but was recorded without a vote because of attributed debt; administration, custody, claims and maintenance were concentrated within the same documentary architecture.</td><td>Who calculated/certified the debt, who knew the title/vote basis, which later recipient relied on the resulting authority and what consequence followed.</td><td>Valid Community debt, lawful voting restriction and properly appointed office-holders.</td><td><span class="evidence-badge question-badge">Investigative / native package incomplete</span></td></tr>\n              <tr><td><strong>26 Apr / 11 Jun 2016 · professional knowledge anchor</strong></td><td>The controlled PwC source family records detailed discussion of private units, Community/exploitation distinctions, accounts, debt/voting, access and the insolvency, including direct interaction with FMMM.</td><td>Any later mandate, actual file access, conflict/KYC checks, information barriers, work product, use or transmission involving the same Sun Park asset.</td><td>Different later team/entity, no access or use, adequate information barriers, no causal role.</td><td><span class="evidence-badge document">Prior knowledge documented; later bridge open</span></td></tr>\n              <tr><td><strong>18 May / 7 Jun 2018 · authority → security/access → material control</strong></td><td>Community/security and AC-authorisation material supports a material access/control transition; AP 804/2018 upheld provisional dismissal and supplied an adverse civil/lawful explanation.</td><td>Who instructed each lock/key/security act, exact finca/common-element perimeter, whether authority was exceeded and what later project benefit depended on the access.</td><td>Lawful preservation, maintenance or security within LPB/common-element authority.</td><td><span class="evidence-badge outcome">Material control supported; criminal characterisation open</span></td></tr>\n              <tr><td><strong>2020 · project representation</strong></td><td>Sun Park was presented to investors before later formal LPB title events.</td><td>Exact speaker/document, contemporaneous title knowledge, qualifications, recipient reliance and any corrective communication.</td><td>Preliminary/project-stage language adequately qualified and later conditions properly satisfied.</td><td><span class="evidence-badge inference-badge">Documentary contradiction test</span></td></tr>\n              <tr><td><strong>20/21 Jul 2021 · internal position → court use</strong></td><td>RICPE documented 54 CAM / 190 LPB / 18 third-party properties, conditional acquisition, unsigned LOI and incomplete DD; CAM filed that certification in Insolvency 36/2012 the next day.</td><td>Who requested/approved external use, its procedural purpose, whether the IA/Court relied on it, and how the narrower position was reconciled before later re-entry.</td><td>Accurate cautionary certification used for a legitimate procedural purpose and later superseded by independently verified facts.</td><td><span class="evidence-badge document">Two events verified; reliance/bridge open</span></td></tr>\n              <tr><td><strong>2022–2023 · title/re-entry → Series F/G → public support → MYND</strong></td><td>Later title, HNT/RICPE finance, a Regional Incentives award and ERDF identification are distinct later layers.</td><td>Which asset/cost/invoice/job each layer used; whether Series F/G and administrative suitability covered the same or distinct phases; who independently verified title and use of funds.</td><td>Lawful later title, distinct eligible costs, authorised finance and non-overlapping employment/support.</td><td><span class="evidence-badge question-badge">Reconciliation required</span></td></tr>\n            </tbody>\n          </table>\n        </div>\n        <p class="pressure-maxim"><strong>Only after this matrix:</strong> possible offence categories are tested against event-specific elements and the law applicable at the date. Invalidity, inconsistency, institutional repetition or later benefit do not themselves establish falsity, deception, intent, participation or a concerted plan.</p>\n\n'''
        t = insert_before_after_marker(t, 'id="criminal-theory"', '        <div class="control-table-wrap">', insert, "community EN fact-first matrix")
        t = replace_once(t, '<strong>Disclaimer:</strong> the minutes establish that certain statements and resolutions were recorded; they do not by themselves establish their intrinsic truth, validity, implementation, offence or intent. Criminal characterisations are express allegations by Gil Marer pending determination. All persons and entities retain the presumption of innocence and right of reply.', '<strong>Disclaimer:</strong> the minutes establish that certain statements and resolutions were recorded; they do not by themselves establish intrinsic truth, validity, implementation, offence or intent. Criminal characterisations remain attributed investigative allegations unless a competent authority determines otherwise. No concerted plan is inferred from association, sequence or later benefit alone. All persons and entities retain the presumption of innocence and right of reply.', "community EN disclaimer")
    else:
        t = replace_once(t, '<title>Actas Sun Park 2011–2022 — deuda, voto, autoridad y relevancia penal</title>', '<title>Actas Sun Park 2011–2022 — deuda, voto, autoridad y test penal/investigativo</title>', "community ES title")
        t = replace_once(t, '<meta name="description" content="Cronología documentada de las juntas y actas de Sun Park entre 2011 y 2022, sus actores, el aviso al administrador concursal y la hipótesis penal de fabricación y propagación de autoridad.">', '<meta name="description" content="Cronología documentada de las juntas y actas de Sun Park entre 2011 y 2022, con test primero de hecho, actor, conocimiento, uso y dependencia, y sólo después de posible relevancia penal.">', "community ES description")
        t = replace_once(t, '<a href="#hipotesis-penal">Código Penal</a>', '<a href="#hipotesis-penal">Test penal / investigativo</a>', "community ES nav")
        t = replace_once(t, '<a class="button secondary" href="#hipotesis-penal">Ver la calificación penal alegada</a>', '<a class="button secondary" href="#hipotesis-penal">Ver el test penal / investigativo</a>', "community ES hero action")
        t = replace_once(t, '<div><span>Estado</span><strong>Hipótesis penal expresa; sin condena firme</strong></div>', '<div><span>Estado</span><strong>Hipótesis investigativa atribuida; no hallazgo penal competente que establezca un plan concertado</strong></div>', "community ES status")
        t = replace_once(t, '<div><p class="kicker">Calificación pública de Gil Marer · no condena</p><h2 id="titulo-hipotesis-penal">La alegación es penal; la prueba debe ser elemento por elemento.</h2></div>', '<div><p class="kicker">Hipótesis investigativa atribuida · sin hallazgo penal competente</p><h2 id="titulo-hipotesis-penal">Primero hecho, actor, conocimiento, uso y dependencia; después la etiqueta penal.</h2></div>', "community ES criminal heading")
        t = replace_once(t, '<p>Las actas se invocan como una hipótesis patrimonial unitaria de posible relevancia penal, pendiente de determinación judicial. Una junta discutible, una deuda controvertida o un resultado adverso no son automáticamente delitos.</p>', '<p>Los documentos justifican un test investigativo, no una conclusión penal de partida. Para cada evento deben identificarse actor, autoridad, conocimiento contemporáneo, aviso contrario, documento u omisión, destinatario, dependencia, beneficio/perjuicio y explicación lícita más fuerte antes de considerar cualquier posible caracterización penal.</p>', "community ES criminal intro")
        insert = '''        <div class="control-table-wrap" id="matriz-evento-penal">\n          <table class="control-table document-status">\n            <thead><tr><th>Evento / conversión</th><th>Qué establece el registro actual</th><th>Conocimiento / uso / dependencia a probar</th><th>Explicación lícita más fuerte</th><th>Estado</th></tr></thead>\n            <tbody>\n              <tr><td><strong>22 jun 2011 · deuda → voto → cargo/custodia</strong></td><td>LPB comparece con un porcentaje mayoritario pero figura sin voto por deuda atribuida; administración, custodia, reclamaciones y mantenimiento quedan concentrados en una misma arquitectura documental.</td><td>Quién calculó/certificó la deuda, quién conocía la base dominical y de voto, qué receptor posterior confió en la autoridad resultante y qué consecuencia produjo.</td><td>Deuda comunitaria válida, restricción de voto lícita y cargos correctamente nombrados.</td><td><span class="evidence-badge question-badge">Investigativo / paquete nativo incompleto</span></td></tr>\n              <tr><td><strong>26 abr / 11 jun 2016 · ancla de conocimiento profesional</strong></td><td>La familia de fuentes PwC controlada documenta discusión detallada de fincas privadas, Comunidad/explotación, cuentas, deuda/voto, acceso y concurso, incluida interacción directa con FMMM.</td><td>Mandato posterior, acceso real al expediente, conflictos/KYC, barreras de información, producto de trabajo, uso o transmisión respecto del mismo activo Sun Park.</td><td>Equipo/entidad posterior distinta, sin acceso ni uso, barreras adecuadas y sin papel causal.</td><td><span class="evidence-badge document">Conocimiento previo documentado; puente posterior abierto</span></td></tr>\n              <tr><td><strong>18 may / 7 jun 2018 · autoridad → seguridad/acceso → control material</strong></td><td>El material Comunidad/seguridad y autorizaciones del AC apoya un cambio material de acceso/control; AP 804/2018 confirmó el archivo provisional y aportó una explicación adversa civil/lícita.</td><td>Quién ordenó cada llave/cerradura/seguridad, perímetro finca/elemento común, exceso de autoridad y qué beneficio posterior del proyecto dependió del acceso.</td><td>Preservación, mantenimiento o seguridad lícitos dentro del perímetro LPB/común.</td><td><span class="evidence-badge outcome">Control material apoyado; caracterización penal abierta</span></td></tr>\n              <tr><td><strong>2020 · representación del proyecto</strong></td><td>Sun Park se presentó a inversores antes de los posteriores actos formales de título LPB.</td><td>Autor y documento exactos, conocimiento dominical contemporáneo, reservas, dependencia del receptor y corrección posterior.</td><td>Lenguaje preliminar/de proyecto suficientemente cualificado y condiciones cumplidas después.</td><td><span class="evidence-badge inference-badge">Test de contradicción documental</span></td></tr>\n              <tr><td><strong>20/21 jul 2021 · posición interna → uso judicial</strong></td><td>RICPE documentó 54 CAM / 190 LPB / 18 terceros, adquisición condicionada, LOI sin firma y DD incompleta; CAM aportó la certificación al Concurso al día siguiente.</td><td>Quién pidió/aprobó el uso externo, finalidad procesal, dependencia del AC/Juzgado y conciliación de la posición restrictiva antes de la reentrada.</td><td>Certificación cautelar correcta, uso procesal legítimo y hechos posteriores verificados de forma independiente.</td><td><span class="evidence-badge document">Dos eventos verificados; dependencia/puente abiertos</span></td></tr>\n              <tr><td><strong>2022–2023 · título/reentrada → Series F/G → apoyo público → MYND</strong></td><td>Título posterior, financiación HNT/RICPE, incentivo regional e identificación FEDER son capas posteriores distintas.</td><td>Qué activo/coste/factura/empleo usó cada capa; si Series F/G e idoneidad cubrieron fases iguales o distintas; quién verificó independientemente título y uso de fondos.</td><td>Título posterior lícito, costes elegibles distintos, financiación autorizada y empleo/apoyos no solapados.</td><td><span class="evidence-badge question-badge">Conciliación requerida</span></td></tr>\n            </tbody>\n          </table>\n        </div>\n        <p class="pressure-maxim"><strong>Sólo después de esta matriz:</strong> las posibles categorías penales se contrastan con elementos propios del evento y con la ley aplicable en su fecha. Invalidez, inconsistencia, repetición institucional o beneficio posterior no acreditan por sí solos falsedad, engaño, dolo, participación ni plan concertado.</p>\n\n'''
        t = insert_before_after_marker(t, 'id="hipotesis-penal"', '        <div class="control-table-wrap">', insert, "community ES fact-first matrix")
        t = replace_once(t, '<strong>Aviso:</strong> las actas acreditan que determinadas manifestaciones y acuerdos fueron registrados; no acreditan por sí solas su verdad intrínseca, validez, ejecución, delito o intención. Las calificaciones penales son alegaciones expresas de Gil Marer pendientes de decisión. Todas las personas y entidades conservan presunción de inocencia y derecho de respuesta.', '<strong>Aviso:</strong> las actas acreditan que determinadas manifestaciones y acuerdos fueron registrados; no acreditan por sí solas verdad intrínseca, validez, ejecución, delito o intención. Las caracterizaciones penales permanecen como hipótesis investigativas atribuidas salvo decisión de autoridad competente. No se infiere plan concertado por asociación, secuencia o beneficio posterior. Todas las personas y entidades conservan presunción de inocencia y derecho de respuesta.', "community ES disclaimer")
    write(rel, t)


def patch_funding(rel: str, en: bool) -> None:
    t = read(rel)
    if en:
        t = replace_once(t, '<meta name="description" content="Substantiated allegation of double or triple funding and multiple financial lives of the same Sun Park/MYND Yaiza hotel, inside and outside Insolvency 36/2012.">', '<meta name="description" content="Source-controlled reconciliation record for Project Sun Rock’s substantiated allegation of possible duplicate or overlapping funding across the same Sun Park/MYND Yaiza assets, works, costs and employment.">', "funding EN meta")
        t = replace_once(t, 'Project Sun Rock alleges double or triple funding and multiple parallel lives of the same hotel project.', 'Project Sun Rock alleges possible double or triple funding and multiple parallel lives of the same hotel project.', "funding EN allegation qualifier")
        old_row = '<tr><td>RICPE / HNT Series F–G</td><td><strong>€6,573,703.10</strong> total attributed to the controlled audited accounts; exact split open</td><td><span class="status verified">Attributed total</span></td><td>What was approved, drawn and spent; which works, assets, jobs and security supported it?</td></tr>'
        new_rows = '<tr><td>RICPE / HNT · 20-Sep-2023 prospectus</td><td>Works €1,598,849.78 + employment €4,971,863.78 = <strong>€6,570,713.56</strong></td><td><span class="status verified">Source-specific total</span></td><td>What exactly did each component finance, and how does it map to invoices, assets and employment?</td></tr>\n<tr><td>RICPE / HNT · separate audited-accounts reconstruction</td><td>Series F €1,598,849.32 + Series G €4,974,853.78 = <strong>€6,573,703.10</strong>; difference from prospectus <strong>€2,989.54</strong></td><td><span class="status open">Reconciliation open</span></td><td>The difference may have a legitimate accounting/date/classification explanation. It must not be silently normalised. <a href="../ricpe-idoneidad-series-f-g/">Open Series F/G control →</a></td></tr>'
        t = replace_once(t, old_row, new_rows, "funding EN F/G rows")
    else:
        t = replace_once(t, '<meta name="description" content="Alegación sustentada de doble o triple financiación y múltiples vidas financieras del mismo Hotel Sun Park/MYND Yaiza, dentro y fuera del Concurso 36/2012.">', '<meta name="description" content="Registro de conciliación fuente-controlado sobre la alegación sustentada de posible doble o triple financiación o solapamiento económico del mismo Hotel Sun Park/MYND Yaiza.">', "funding ES meta")
        t = replace_once(t, 'Project Sun Rock alega doble o triple financiación y varias vidas paralelas del mismo proyecto hotelero.', 'Project Sun Rock alega posible doble o triple financiación y varias vidas paralelas del mismo proyecto hotelero.', "funding ES allegation qualifier")
        old_row = '<tr><td>RICPE / HNT Series F–G</td><td><strong>€6.573.703,10</strong> total atribuido a las cuentas auditadas controladas; desglose exacto abierto</td><td><span class="status verified">Total atribuido</span></td><td>¿Qué se aprobó, desembolsó y gastó; qué obras, activos, empleos y garantías lo sustentaron?</td></tr>'
        new_rows = '<tr><td>RICPE / HNT · folleto 20-sep-2023</td><td>Obras 1.598.849,78 € + empleo 4.971.863,78 € = <strong>6.570.713,56 €</strong></td><td><span class="status verified">Total específico de fuente</span></td><td>¿Qué financió exactamente cada componente y cómo se enlaza con facturas, activos y empleo?</td></tr>\n<tr><td>RICPE / HNT · reconstrucción separada de cuentas auditadas</td><td>Serie F 1.598.849,32 € + Serie G 4.974.853,78 € = <strong>6.573.703,10 €</strong>; diferencia frente al folleto <strong>2.989,54 €</strong></td><td><span class="status open">Conciliación abierta</span></td><td>La diferencia puede tener una explicación legítima contable, temporal o de clasificación. No debe normalizarse en silencio. <a href="../ricpe-idoneidad-series-f-g/">Abrir control Series F/G →</a></td></tr>'
        t = replace_once(t, old_row, new_rows, "funding ES F/G rows")
    write(rel, t)


def patch_cleanroom(rel: str, en: bool) -> None:
    t = read(rel)
    if en:
        old_marker = '<p class="eyebrow">FIRST FIVE SOURCES / TARGETS</p>'
        new_section = '''<section class="section alt" id="keystone-conversions"><div class="shell pa"><p class="eyebrow">SIX KEYSTONE NODES · READ BACKWARDS AND FORWARDS</p><h2>The first screen should follow the conversions that can change several branches at once.</h2><div class="grid3"><article class="card"><span class="status hyp">2008–2011</span><h3>Ownership → debt → voting → authority</h3><p>Reconstruct title, participation, notice, proxies, coefficients, debt, voting restriction, offices, custody and litigation from the native package.</p></article><article class="card"><span class="status limited">2016</span><h3>Professional knowledge and private units</h3><p>The controlled PwC source family records detailed knowledge of private units, Community/exploitation, accounts, debt/voting, access and insolvency. Later mandate/use/conflict questions remain open.</p></article><article class="card"><span class="status limited">2017–2018</span><h3>Authority → security/access → material control</h3><p>Material access/control is source-supported subject to exact perimeter; AP 804/2018 supplies adverse lawful/civil context. Instructions, excess and actor-specific intent remain to prove.</p></article><article class="card"><span class="status neutral">2020</span><h3>Project representations</h3><p>Compare each investor-facing title/acquisition/encumbrance statement with contemporaneous title, control and qualification evidence.</p></article><article class="card"><span class="status verified">20–21 Jul 2021</span><h3>Internal position → judicial use</h3><p>RICPE documents 54 CAM / 190 LPB / 18 third-party properties, conditional acquisition, unsigned LOI and incomplete DD; CAM files the certification the next day. Purpose, authorisation and reliance remain finite questions.</p></article><article class="card"><span class="status open">2022–2023</span><h3>Re-entry → title → Series F/G → public support → MYND</h3><p>Identify the re-entry record, title perimeter, use of Series F/G, Regional Incentives and ERDF by asset, invoice, payment and job. <a href="../ricpe-idoneidad-series-f-g/">Series F/G control →</a></p></article></div><div class="warning"><strong>Criminal/investigative rule:</strong> no node becomes an offence because it is irregular, adverse or later beneficial. The question is whether a specific actor knowingly made, used or omitted a materially relevant proposition; who relied; what result followed; and what lawful alternative explains the same event.</div></div></section>'''
        t = replace_section_containing(t, old_marker, new_section, "cleanroom EN keystone section")
        matrix = '''\n<section class="section" id="conversion-matrix"><div class="shell pa"><p class="eyebrow">UNITARY CONVERSION MATRIX</p><h2>Do not prosecute the narrative. Prove or reject each conversion.</h2><div class="table-wrap"><table class="matrix"><thead><tr><th>Conversion</th><th>Actor / function</th><th>Primary evidence / present status</th><th>Knowledge / notice</th><th>Recipient / reliance</th><th>Benefit / harm</th><th>Strongest lawful alternative</th><th>Dependency</th></tr></thead><tbody><tr><td>Ownership → vote</td><td>Owners / Community organs</td><td>Title, attendance, proxies, coefficients and debt/voting package incomplete</td><td>Who knew the true title and voting base?</td><td>Later minutes / certificates / litigation</td><td>Governance and voting effect</td><td>Valid title and lawful restriction</td><td><span class="status open">BROKEN / OPEN</span></td></tr><tr><td>Debt → authority/document</td><td>Administrator / officers / certifiers</td><td>2011 architecture source-supported; calculation/custody package incomplete</td><td>Who created or approved the debt and certificate?</td><td>Owners, IA, courts and later actors</td><td>Voting, claims and documentary authority</td><td>Accurate debt and valid office</td><td><span class="status open">DEPENDENT</span></td></tr><tr><td>Authority → access/control</td><td>Community / IA / security / private actors</td><td>2018 material-control transition supported; exact finca reach open</td><td>Who knew limits of LPB/common-element authority?</td><td>Security, owners, operators, later project</td><td>Access, exclusion and practical availability</td><td>Lawful preservation/maintenance</td><td><span class="status limited">DEPENDENT / CONTESTED</span></td></tr><tr><td>Control → project availability</td><td>CAM / project sponsors / advisers</td><td>Pre-title project chronology documented; exact rights and independent verification vary by date</td><td>What title/access limits were known?</td><td>RICPE, investors, advisers</td><td>Project progression and valuation</td><td>Preliminary project subject to conditions</td><td><span class="status open">DEPENDENT</span></td></tr><tr><td>Internal RICPE position → re-entry</td><td>RICPE governance/control functions</td><td>20-Jul-2021 restrictive position verified; re-entry bridge still to produce</td><td>Who received and approved the change?</td><td>Committee/Board/investors</td><td>Funding eligibility and project continuation</td><td>New independently verified facts / valid waiver</td><td><span class="status open">BROKEN</span></td></tr><tr><td>Re-entry/title → finance/public support → MYND</td><td>RICPE/HNT and competent public bodies</td><td>Later title, F/G, award and ERDF identification verified at different levels</td><td>What asset/cost/job basis did each decision-maker know?</td><td>Investors, AEAT, Regional Incentives, ERDF controls</td><td>Finance, support, operation, income and value</td><td>Distinct costs, lawful cumulation and valid title</td><td><span class="status open">RECONCILIATION OPEN</span></td></tr></tbody></table></div><div class="principle"><strong>2016 knowledge bridge:</strong> PwC/Carlos is presently a knowledge, former-client, conflict and records inquiry. The later bridge requires an actual mandate, file access, conflict/KYC result, information barrier, work product, use, reliance and causation before any participation theory is upgraded.</div></div></section>'''
        t = insert_before_after_marker(t, 'id="by-institution"', '<section class="section" id="by-institution"', matrix + '\n', "cleanroom EN conversion matrix")
    else:
        old_marker = '<p class="eyebrow">PRIMERAS CINCO PRUEBAS / OBJETIVOS</p>'
        new_section = '''<section class="section alt" id="nodos-conversion"><div class="shell pa"><p class="eyebrow">SEIS NODOS CLAVE · LEER HACIA ATRÁS Y HACIA DELANTE</p><h2>La primera pantalla debe seguir las conversiones capaces de cambiar varias ramas a la vez.</h2><div class="grid3"><article class="card"><span class="status hyp">2008–2011</span><h3>Propiedad → deuda → voto → autoridad</h3><p>Reconstruir título, participación, convocatoria, poderes, coeficientes, deuda, restricción de voto, cargos, custodia y litigio desde el paquete nativo.</p></article><article class="card"><span class="status limited">2016</span><h3>Conocimiento profesional y fincas privadas</h3><p>La familia de fuentes PwC controlada documenta conocimiento detallado de fincas privadas, Comunidad/explotación, cuentas, deuda/voto, acceso y concurso. Mandato/uso/conflicto posterior permanece abierto.</p></article><article class="card"><span class="status limited">2017–2018</span><h3>Autoridad → seguridad/acceso → control material</h3><p>El acceso/control material está apoyado sujeto a perímetro; AP 804/2018 aporta contexto adverso civil/lícito. Instrucciones, exceso y dolo actor-específico siguen por probar.</p></article><article class="card"><span class="status neutral">2020</span><h3>Representaciones del proyecto</h3><p>Comparar cada manifestación a inversores sobre adquisición, título y cargas con el título/control contemporáneo y sus reservas.</p></article><article class="card"><span class="status verified">20–21 jul 2021</span><h3>Posición interna → uso judicial</h3><p>RICPE documenta 54 CAM / 190 LPB / 18 terceros, adquisición condicionada, LOI sin firma y DD incompleta; CAM aporta la certificación al día siguiente. Finalidad, autorización y dependencia son preguntas finitas.</p></article><article class="card"><span class="status open">2022–2023</span><h3>Reentrada → título → Series F/G → apoyo público → MYND</h3><p>Identificar documento de reentrada, perímetro de título, uso de Series F/G, Incentivos Regionales y FEDER por activo, factura, pago y empleo. <a href="../ricpe-idoneidad-series-f-g/">Control Series F/G →</a></p></article></div><div class="warning"><strong>Regla penal/investigativa:</strong> ningún nodo se convierte en delito por ser irregular, adverso o beneficioso después. La pregunta es si un actor concreto conoció y realizó, usó u omitió una proposición material; quién dependió de ella; qué resultado siguió; y qué explicación lícita describe el mismo evento.</div></div></section>'''
        t = replace_section_containing(t, old_marker, new_section, "cleanroom ES keystone section")
        matrix = '''\n<section class="section" id="matriz-conversiones"><div class="shell pa"><p class="eyebrow">MATRIZ UNITARIA DE CONVERSIONES</p><h2>No perseguir penalmente la narrativa. Probar o descartar cada conversión.</h2><div class="table-wrap"><table class="matrix"><thead><tr><th>Conversión</th><th>Actor / función</th><th>Prueba primaria / estado</th><th>Conocimiento / aviso</th><th>Destinatario / dependencia</th><th>Beneficio / daño</th><th>Explicación lícita más fuerte</th><th>Dependencia</th></tr></thead><tbody><tr><td>Propiedad → voto</td><td>Propietarios / órganos comunitarios</td><td>Título, asistencia, poderes, coeficientes y deuda/voto incompletos</td><td>¿Quién conocía el título y base real de voto?</td><td>Actas / certificados / litigios posteriores</td><td>Gobernanza y efecto de voto</td><td>Título válido y restricción lícita</td><td><span class="status open">BROKEN / OPEN</span></td></tr><tr><td>Deuda → autoridad/documento</td><td>Administrador / cargos / certificadores</td><td>Arquitectura 2011 apoyada; cálculo/custodia incompletos</td><td>¿Quién creó o aprobó deuda y certificado?</td><td>Propietarios, AC, juzgados y actores posteriores</td><td>Voto, reclamación y autoridad documental</td><td>Deuda correcta y cargo válido</td><td><span class="status open">DEPENDENT</span></td></tr><tr><td>Autoridad → acceso/control</td><td>Comunidad / AC / seguridad / actores privados</td><td>Transición material 2018 apoyada; alcance finca por finca abierto</td><td>¿Quién conocía límites de autoridad LPB/comunes?</td><td>Seguridad, propietarios, operadores, proyecto posterior</td><td>Acceso, exclusión y disponibilidad práctica</td><td>Preservación/mantenimiento lícitos</td><td><span class="status limited">DEPENDENT / CONTESTED</span></td></tr><tr><td>Control → disponibilidad del proyecto</td><td>CAM / promotores / asesores</td><td>Proyecto pre-título documentado; derechos y verificación varían por fecha</td><td>¿Qué límites de título/acceso se conocían?</td><td>RICPE, inversores, asesores</td><td>Progresión y valoración del proyecto</td><td>Proyecto preliminar sujeto a condiciones</td><td><span class="status open">DEPENDENT</span></td></tr><tr><td>Posición interna RICPE → reentrada</td><td>Gobierno / control RICPE</td><td>Posición restrictiva 20-jul-2021 verificada; puente de reentrada por producir</td><td>¿Quién recibió y aprobó el cambio?</td><td>Comité/Consejo/inversores</td><td>Elegibilidad financiera y continuidad</td><td>Nuevos hechos verificados / dispensa válida</td><td><span class="status open">BROKEN</span></td></tr><tr><td>Reentrada/título → financiación/apoyo → MYND</td><td>RICPE/HNT y órganos públicos competentes</td><td>Título posterior, F/G, concesión e identificación FEDER verificados a distintos niveles</td><td>¿Qué base de activo/coste/empleo conoció cada decisor?</td><td>Inversores, AEAT, Incentivos, controles FEDER</td><td>Financiación, apoyo, operación, ingreso y valor</td><td>Costes distintos, acumulación lícita y título válido</td><td><span class="status open">CONCILIACIÓN ABIERTA</span></td></tr></tbody></table></div><div class="principle"><strong>Puente de conocimiento 2016:</strong> PwC/Carlos se trata actualmente como cuestión de conocimiento, antiguo cliente, conflicto y registros. Para elevar una teoría de participación se necesitan mandato posterior, acceso real, resultado de conflictos/KYC, barrera de información, producto de trabajo, uso, dependencia y causalidad.</div></div></section>'''
        t = insert_before_after_marker(t, 'id="por-institucion"', '<section class="section" id="por-institucion"', matrix + '\n', "cleanroom ES conversion matrix")
    write(rel, t)


def add_series_link(rel: str, en: bool, marker: str) -> None:
    t = read(rel)
    href = '../ricpe-idoneidad-series-f-g/'
    if href in t:
        return
    label = 'Series F/G · suitability →' if en else 'Series F/G · idoneidad →'
    insert = f'<p class="ok-boundary"><strong>{"Series F/G control:" if en else "Control Series F/G:"}</strong> <a href="{href}">{label}</a> {"separates the 2022–2023 administrative authorisation, source-specific amounts and use-of-funds questions without treating them as a fraud finding." if en else "separa la autorización administrativa 2022–2023, los importes por fuente y el uso de fondos sin tratarlos como hallazgo de fraude."}</p>'
    idx = t.find(marker)
    if idx < 0:
        raise RuntimeError(f"{rel}: marker for Series F/G link not found")
    t = t[:idx] + insert + t[idx:]
    write(rel, t)


def validate_static() -> None:
    required = {
        "es/actualizaciones/index.html": ["18 agosto 2026", "ricpe-series-fg-18ago", "ricpe-formal-prefiling-17aug"],
        "en/updates/index.html": ["18 August 2026", "ricpe-series-fg-18aug", "ricpe-formal-prefiling-17aug"],
        "es/ric-private-equity-sun-park/index.html": ["Comunicación formal presentada · 17 agosto 2026", "Series F/G · idoneidad", "Admisión · investigación"],
        "en/ric-private-equity-sun-park/index.html": ["Formal communication submitted · 17 August 2026", "Series F/G · suitability", "Admission · investigation"],
        "es/comunidad-instrumentalizacion/actas-2011-2022/index.html": ["Test penal / investigativo", "matriz-evento-penal", "no hallazgo penal competente"],
        "en/community-instrumentalisation/minutes-2011-2022/index.html": ["Criminal / investigative test", "criminal-event-matrix", "no competent criminal finding"],
        "es/mismo-hotel-multiples-vidas-financieras/index.html": ["6.570.713,56", "6.573.703,10", "2.989,54", "ricpe-idoneidad-series-f-g"],
        "en/same-hotel-multiple-financial-lives/index.html": ["€6,570,713.56", "€6,573,703.10", "€2,989.54", "ricpe-idoneidad-series-f-g"],
        "es/reconstruccion-unitaria-autoridades-publicas/index.html": ["SEIS NODOS CLAVE", "matriz-conversiones", "Puente de conocimiento 2016"],
        "en/public-authority-unitary-case-reconstruction/index.html": ["SIX KEYSTONE NODES", "conversion-matrix", "2016 knowledge bridge"],
    }
    banned = {
        "es/comunidad-instrumentalizacion/actas-2011-2022/index.html": ["Hipótesis penal expresa; sin condena firme", ">Código Penal<", "Ver la calificación penal alegada"],
        "en/community-instrumentalisation/minutes-2011-2022/index.html": ["Express criminal-law theory; no final conviction", ">Criminal Code<", "See the alleged criminal-law characterisation"],
        "es/actualizaciones/index.html": ["<span>Última actualización material</span><strong>14 agosto 2026</strong>"],
        "en/updates/index.html": ["<span>Latest material update</span><strong>14 August 2026</strong>"],
    }
    for rel, markers in required.items():
        text = read(rel)
        for marker in markers:
            if marker not in text:
                raise RuntimeError(f"validation: {rel} missing {marker!r}")
    for rel, markers in banned.items():
        text = read(rel)
        for marker in markers:
            if marker in text:
                raise RuntimeError(f"validation: {rel} still contains banned {marker!r}")


def main() -> int:
    patch_updates_es()
    patch_updates_en()
    patch_ricpe("es/ric-private-equity-sun-park/index.html", False)
    patch_ricpe("en/ric-private-equity-sun-park/index.html", True)
    patch_community("es/comunidad-instrumentalizacion/actas-2011-2022/index.html", False)
    patch_community("en/community-instrumentalisation/minutes-2011-2022/index.html", True)
    patch_funding("es/mismo-hotel-multiples-vidas-financieras/index.html", False)
    patch_funding("en/same-hotel-multiple-financial-lives/index.html", True)
    patch_cleanroom("es/reconstruccion-unitaria-autoridades-publicas/index.html", False)
    patch_cleanroom("en/public-authority-unitary-case-reconstruction/index.html", True)

    # Series F/G should be directly discoverable from the specialist regulatory routes too.
    add_series_link("es/cnmv-ricpe-verificacion/index.html", False, '<section class="section alt"><div class="shell cnmv"><p class="ok-kicker">DEPENDENCIAS</p>')
    add_series_link("en/cnmv-ricpe-verification/index.html", True, '<section class="section alt"><div class="shell cnmv"><p class="ok-kicker">DEPENDENCIES</p>')
    add_series_link("es/incentivos-regionales-gc836-p06/index.html", False, '<section class="section alt"><div class="shell ir"><p class="ok-kicker">RUTAS CONECTADAS</p>')
    add_series_link("en/regional-incentives-gc836-p06/index.html", True, '<section class="section alt"><div class="shell ir"><p class="ok-kicker">CONNECTED ROUTES</p>')
    add_series_link("es/snca-fondos-europeos-trazabilidad/index.html", False, '<section class="section"><div class="shell eu"><p class="ok-kicker">RUTAS CONECTADAS</p>')
    add_series_link("en/snca-eu-funds-traceability/index.html", True, '<section class="section"><div class="shell eu"><p class="ok-kicker">CONNECTED ROUTES</p>')

    validate_static()
    print("P0 STATIC / CRIMINAL-FRAMING PATCH PASSED")
    print(f"Changed files: {len(CHANGED)}")
    for rel in CHANGED:
        print(f"- {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
