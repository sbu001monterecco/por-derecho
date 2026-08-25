(() => {
  if (window.__pdCgpjTsjParity20260820) return;
  window.__pdCgpjTsjParity20260820 = true;

  const path = window.location.pathname;
  const isEn = /\/en\//.test(path);
  const html = (node, where, value) => node && node.insertAdjacentHTML(where, value);

  const style = document.createElement('style');
  style.textContent = `
    .pd-parity-note{margin:1rem 0;padding:1rem 1.15rem;border-left:6px solid #245c49;background:#edf3ee;border-radius:14px;color:#13252d}
    .pd-parity-note.warning{border-left-color:#c89432;background:#fff8e8}
    .pd-parity-note.knowledge{border-left-color:#315c7b;background:#f2f7fb}
    .pd-parity-note strong,.pd-parity-note a{font-weight:900}
    .pd-parity-update{scroll-margin-top:5rem}
    .pd-rubio-reply{margin-top:1.4rem}
    .pd-rubio-reply .pd-source-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.9rem;margin:1rem 0}
    .pd-rubio-reply .pd-source-card{background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:14px;padding:1rem}
    .pd-rubio-reply .pd-source-card strong{display:block;margin-bottom:.35rem}
    .pd-rubio-reply table{width:100%;border-collapse:collapse;background:#fff;margin-top:1rem}
    .pd-rubio-reply th,.pd-rubio-reply td{padding:.75rem;border:1px solid #dde2e3;vertical-align:top;text-align:left}
    .pd-rubio-reply th{background:#13252d;color:#fff}
    @media(max-width:800px){.pd-rubio-reply .pd-source-grid{grid-template-columns:1fr}}
  `;
  document.head.appendChild(style);

  const canonicalTsj = /\/(es|en)\/tsj-canarias-exp-gub-38-2026\/?(?:index\.html)?$/.test(path);
  if (canonicalTsj) {
    const meta = document.querySelector('meta[name="description"]');
    if (meta) meta.content = isEn
      ? 'Source-controlled record of Government File 38/2026: signed archive decision, same-day response, Carlos Víctor Rubio Faure final reply, ATLANTE, CGPJ transmission reconciliation and filed hierarchical appeal.'
      : 'Registro fuente-controlado del Exp. Gub. 38/2026: resolución firmada de archivo, respuesta del mismo día, respuesta final de Carlos Víctor Rubio Faure, ATLANTE, conciliación de transmisión CGPJ y alzada presentada.';

    const status = document.querySelector('.hero .status');
    if (status) status.textContent = isEn
      ? 'First-level archive · final institutional reply recorded · appeal filed · forwarding and admission pending'
      : 'Archivo de primera instancia · respuesta institucional final registrada · alzada presentada · remisión y admisión pendientes';

    const alert = document.querySelector('.hero .alert');
    if (alert) alert.innerHTML = isEn
      ? '<strong>Reference control · resolved.</strong> The notification email subject said <strong>EXP. GUB 28/2026</strong>, while the body, attached PDF and signed decision said <strong>38/2026</strong>. In his later reply of 20 August 2026, Carlos Víctor Rubio Faure expressly confirmed that <strong>38/2026 is the correct proceeding</strong>. The historical subject-line discrepancy is retained as source history and is not treated as evidence of bad faith.'
      : '<strong>Control de referencia · resuelto.</strong> El asunto del correo de notificación decía <strong>EXP. GUB 28/2026</strong>, mientras que el cuerpo, el PDF adjunto y la resolución firmada decían <strong>38/2026</strong>. En su respuesta posterior de 20 de agosto de 2026, Carlos Víctor Rubio Faure confirmó expresamente que <strong>38/2026 es el procedimiento correcto</strong>. La divergencia histórica del asunto se conserva como parte de la fuente y no se presenta como prueba de mala fe.';

    const anchor = alert || status;
    if (anchor && !document.querySelector('[data-tsj-filed-parity]')) {
      html(anchor, 'afterend', `<div class="pd-parity-note" data-tsj-filed-parity><strong>${isEn ? 'Procedural update · 20 August 2026.' : 'Actualización procesal · 20 de agosto de 2026.'}</strong> ${isEn ? 'The hierarchical appeal has been filed and registered as' : 'El recurso de alzada ha sido presentado y registrado como'} <strong>REGAGE26e00074355631</strong>. ${isEn ? 'Filing proves presentation, destination, timestamp and the submitted-file integrity record; it does not prove admission, forwarding or outcome.' : 'La presentación acredita destino, fecha, hora e integridad del archivo aportado; no acredita admisión, remisión ni resultado.'} <a href="${isEn ? '../tsj-canarias-exp-gub-38-2026-appeal-filed/' : '../tsj-canarias-exp-gub-38-2026-alzada-presentada/'}">${isEn ? 'Verified filing record →' : 'Registro verificado de presentación →'}</a></div>`);
    }

    const nav = document.querySelector('.main-nav');
    if (nav && !nav.querySelector('a[href="#respuesta-final"]')) {
      html(nav, 'beforeend', `<a href="#respuesta-final">${isEn ? 'Final reply' : 'Respuesta final'}</a>`);
    }

    const main = document.querySelector('main');
    if (main && !document.querySelector('[data-rubio-final-reply]')) {
      const section = isEn ? `
<section class="section alt pd-rubio-reply" id="respuesta-final" data-rubio-final-reply>
  <div class="shell record">
    <p class="kicker">FINAL INSTITUTIONAL REPLY · 20 AUGUST 2026</p>
    <h2>Carlos Víctor Rubio Faure: six source-controlled propositions and an institutional knowledge checkpoint</h2>
    <p>The later reply from the Secretary of Government is a distinct source from the signed archive decision. It closes the reference-number discrepancy and adds several attributable institutional statements. It is recorded as a <strong>knowledge checkpoint</strong>, not as agreement with, admission of, or a merits finding on the matters raised.</p>
    <div class="pd-source-grid">
      <article class="pd-source-card"><strong>1 · Controlling reference</strong>Rubio Faure expressly confirmed that <strong>Government File 38/2026</strong> is the correct proceeding. The earlier “28/2026” subject-line discrepancy is therefore historically preserved but resolved.</article>
      <article class="pd-source-card"><strong>2 · General file-content representation</strong>He stated that the governmental file includes the various acts or proceedings of different kinds carried out within it. This is an attributable institutional representation; it is not item-level certification that every requested email, attachment, visual, metadata field or record is individually incorporated and indexed.</article>
      <article class="pd-source-card"><strong>3 · No item-specific confirmation</strong>He expressly declined to confirm one way or the other the requested particulars concerning the content of the governmental file. Controlled consequence: <em>general inclusion statement → no item-level confirmation → certified/indexed file can resolve the question</em>.</article>
      <article class="pd-source-card"><strong>4 · Ley 39/2015 / hierarchical appeal</strong>He stated that the Secretariat did not need to provide a separate assurance that it would comply with Law 39/2015 in relation to the hierarchical appeal. This is recorded as a procedural position, not as a refusal to comply with the law.</article>
      <article class="pd-source-card"><strong>5 · CGPJ DI 169/2026</strong>He again stated that, as of 20 August 2026, receipt of the Promotor communication was not recorded at the Government Secretariat. This does not prove non-dispatch or loss; the finite reconciliation remains dispatch date/channel → recipient → receipt → internal registration → present custody.</article>
      <article class="pd-source-card"><strong>6 · Institutional knowledge checkpoint</strong>He stated that the remainder of the preceding email was taken into account / knowledge was taken of it. That establishes notice of the matters actually set out in that email from that point onward. <strong>Receipt / taking knowledge ≠ agreement ≠ admission ≠ acceptance of factual allegations.</strong></article>
    </div>
    <table>
      <thead><tr><th>What the final reply proves</th><th>What it does not prove</th><th>Finite verification still available</th></tr></thead>
      <tbody><tr><td>Correct reference 38/2026; the Secretariat's general representation about the governmental file; express non-confirmation of item-specific contents; the stated Law 39/2015 position; no recorded receipt of the CGPJ communication as of that date; and institutional notice of the rest of the email.</td><td>Complete item-level incorporation; agreement with the sender; admission; a CGPJ dispatch failure; a High Court loss; ATLANTE event-level production; appeal forwarding, admission, examination or outcome; or wrongdoing by any person.</td><td>Certified/indexed Government File 38/2026; incorporation record for the 20-August email and visuals; forwarding report; superior reference; ATLANTE event/index production; CGPJ outgoing and TSJ receiving/register records; reasoned appeal decision.</td></tr></tbody>
    </table>
    <div class="pd-parity-note knowledge"><strong>Institutional knowledge checkpoint · 20 August 2026.</strong> The evidential consequence is deliberately bounded: the communication creates a date-stamped record against which later production, non-production, routing, certification and explanations can be compared. It does not convert notice into agreement or liability.</div>
  </div>
</section>` : `
<section class="section alt pd-rubio-reply" id="respuesta-final" data-rubio-final-reply>
  <div class="shell record">
    <p class="kicker">RESPUESTA INSTITUCIONAL FINAL · 20 DE AGOSTO DE 2026</p>
    <h2>Carlos Víctor Rubio Faure: seis proposiciones controladas por fuente y un punto de conocimiento institucional</h2>
    <p>La respuesta posterior del Secretario de Gobierno es una fuente distinta de la resolución firmada de archivo. Cierra la divergencia del número de expediente y añade varias manifestaciones institucionales atribuibles. Se registra como <strong>punto de conocimiento</strong>, no como acuerdo, admisión ni pronunciamiento sobre el fondo de las cuestiones planteadas.</p>
    <div class="pd-source-grid">
      <article class="pd-source-card"><strong>1 · Referencia controlante</strong>Rubio Faure confirmó expresamente que el procedimiento correcto es el <strong>Exp. Gub. 38/2026</strong>. La divergencia histórica “28/2026” del asunto del correo se conserva, pero queda resuelta.</article>
      <article class="pd-source-card"><strong>2 · Representación general sobre el contenido del expediente</strong>Manifestó que el expediente gubernativo incluye las actuaciones de diversa naturaleza realizadas en el mismo. Es una representación institucional atribuible; no es una certificación elemento por elemento de que cada correo, anexo, visual, metadato o registro solicitado esté individualmente incorporado e indexado.</article>
      <article class="pd-source-card"><strong>3 · Sin confirmación elemento por elemento</strong>Declinó expresamente confirmar en un sentido u otro los extremos solicitados sobre el contenido del expediente gubernativo. Consecuencia controlada: <em>manifestación general de inclusión → no confirmación individualizada → un expediente certificado/indexado puede resolver la cuestión</em>.</article>
      <article class="pd-source-card"><strong>4 · Ley 39/2015 / recurso de alzada</strong>Manifestó que la Secretaría no tenía que ofrecer una confirmación separada de que cumpliría la Ley 39/2015 en relación con el recurso de alzada. Se registra como posición procesal, no como negativa a cumplir la ley.</article>
      <article class="pd-source-card"><strong>5 · CGPJ DI 169/2026</strong>Reiteró que, a 20 de agosto de 2026, no constaba en la Secretaría de Gobierno la recepción de la comunicación del Promotor. Esto no acredita falta de envío ni pérdida; sigue abierta la conciliación finita: fecha/canal de salida → destinatario → recepción → registro interno → custodia actual.</article>
      <article class="pd-source-card"><strong>6 · Punto de conocimiento institucional</strong>Manifestó que se tomaba conocimiento del resto del correo precedente. Eso fija, desde ese momento, la puesta en conocimiento de las materias realmente expuestas en dicho correo. <strong>Recepción / toma de conocimiento ≠ acuerdo ≠ admisión ≠ aceptación de alegaciones fácticas.</strong></article>
    </div>
    <table>
      <thead><tr><th>Lo que acredita la respuesta final</th><th>Lo que no acredita</th><th>Verificación finita todavía disponible</th></tr></thead>
      <tbody><tr><td>Referencia correcta 38/2026; representación general de la Secretaría sobre el expediente gubernativo; negativa expresa a confirmar contenidos de forma individualizada; posición sobre Ley 39/2015; no constancia de recepción de la comunicación CGPJ a esa fecha; y conocimiento institucional del resto del correo.</td><td>Incorporación íntegra elemento por elemento; acuerdo con el remitente; admisión; fallo de envío del CGPJ; pérdida por el TSJ; producción de eventos ATLANTE; remisión, admisión, examen o resultado de la alzada; o ilicitud de persona alguna.</td><td>Expediente Gubernativo 38/2026 certificado/indexado; constancia de incorporación del correo y visuales del 20 de agosto; informe de remisión; referencia superior; producción de eventos/índices ATLANTE; registros de salida CGPJ y recepción/registro TSJ; decisión motivada de la alzada.</td></tr></tbody>
    </table>
    <div class="pd-parity-note knowledge"><strong>Punto de conocimiento institucional · 20 de agosto de 2026.</strong> La consecuencia probatoria se mantiene deliberadamente acotada: la comunicación crea un registro fechado frente al cual pueden contrastarse posteriormente producción, no producción, remisión, certificación y explicaciones. No convierte el conocimiento en acuerdo ni responsabilidad.</div>
  </div>
</section>`;
      const state = document.querySelector('#estado');
      if (state) state.insertAdjacentHTML('beforebegin', section);
      else main.insertAdjacentHTML('beforeend', section);
    }
  }

  const appealPage = /\/(es\/tsj-canarias-exp-gub-38-2026-alzada-presentada|en\/tsj-canarias-exp-gub-38-2026-appeal-filed)\/?(?:index\.html)?$/.test(path);
  if (appealPage) {
    const hero = document.querySelector('.hero .shell') || document.querySelector('.hero');
    if (hero && !document.querySelector('[data-rubio-appeal-crosslink]')) {
      html(hero, 'beforeend', `<div class="pd-parity-note knowledge" data-rubio-appeal-crosslink><strong>${isEn ? 'Underlying institutional record.' : 'Registro institucional subyacente.'}</strong> ${isEn ? 'Before the hierarchical appeal was filed, Carlos Víctor Rubio Faure expressly confirmed 38/2026 as the correct reference, represented generally that the governmental file includes the acts carried out within it, declined item-specific confirmation, reiterated that receipt of the CGPJ communication was not recorded, and took knowledge of the remainder of the preceding email.' : 'Antes de presentarse la alzada, Carlos Víctor Rubio Faure confirmó expresamente 38/2026 como referencia correcta, manifestó con carácter general que el expediente gubernativo incluye las actuaciones realizadas en él, declinó la confirmación individualizada, reiteró que no constaba la recepción de la comunicación CGPJ y tomó conocimiento del resto del correo precedente.'} <a href="${isEn ? '../tsj-canarias-exp-gub-38-2026/#respuesta-final' : '../tsj-canarias-exp-gub-38-2026/#respuesta-final'}">${isEn ? 'Canonical final-reply record →' : 'Registro canónico de la respuesta final →'}</a></div>`);
    }
  }

  if (/\/(es\/mensaje-abierto-cgpj|en\/open-message-cgpj)\/?(?:index\.html)?$/.test(path)) {
    const shell = document.querySelector('#caso .shell');
    if (shell && !document.querySelector('[data-cgpj-tsj-reconciliation]')) {
      html(shell, 'beforeend', `<div class="pd-parity-note warning" data-cgpj-tsj-reconciliation><strong>${isEn ? '20 August 2026 · CGPJ → TSJ transmission reconciliation.' : '20 de agosto de 2026 · reconciliación de transmisión CGPJ → TSJ.'}</strong> ${isEn ? 'The Promotor’s 14 May agreement ordered communication to the Canary Islands High Court. On 20 August, the High Court Government Secretariat stated that receipt was not recorded there as of that date. In the same final reply, the Secretary confirmed Government File 38/2026 as the correct reference, gave a general representation about the file, declined item-level confirmation and took knowledge of the remainder of the preceding email. None of this establishes a CGPJ dispatch failure, a High Court loss, agreement with allegations or wrongdoing. The finite reconciliation remains dispatch date/channel → recipient → receipt → internal registration → present custody.' : 'El acuerdo del Promotor de 14 de mayo ordenó comunicación al TSJ de Canarias. El 20 de agosto, la Secretaría de Gobierno manifestó que no constaba allí su recepción a esa fecha. En esa misma respuesta final, el Secretario confirmó el Exp. Gub. 38/2026 como referencia correcta, efectuó una manifestación general sobre el expediente, declinó la confirmación elemento por elemento y tomó conocimiento del resto del correo precedente. Nada de ello acredita fallo de envío del CGPJ, pérdida por el TSJ, acuerdo con alegaciones o ilicitud. La conciliación finita sigue siendo fecha/canal de salida → destinatario → recepción → registro interno → custodia actual.'} <a href="${isEn ? '../tsj-canarias-exp-gub-38-2026/#respuesta-final' : '../tsj-canarias-exp-gub-38-2026/#respuesta-final'}">${isEn ? 'TSJ final-reply record →' : 'Respuesta final TSJ →'}</a></div>`);
    }
  }

  if (/\/(es\/registros-institucionales|en\/institutional-records)\/?(?:index\.html)?$/.test(path)) {
    const lead = document.querySelector('.ir-hero .lead');
    if (lead) lead.textContent = isEn
      ? 'Thirteen stable records consolidate key communications and bounded technical references concerning public bodies and statutory professional corporations on the accountability map. Each separates competence, traceable events, evidential limits and one finite outstanding action.'
      : 'Trece registros estables consolidan comunicaciones clave y referencias técnicas delimitadas relativas a los organismos públicos y corporaciones profesionales de derecho público del mapa de control. Cada uno separa competencia, hitos trazables, límites probatorios y una acción finita pendiente.';
    const scope = document.querySelector('.ir-status div:first-child strong');
    if (scope) scope.textContent = isEn ? 'Thirteen public-body and statutory professional-corporation records' : 'Trece registros de organismos públicos y corporaciones profesionales de derecho público';
    const nav = document.querySelector('.main-nav a[href="#records"]');
    if (nav) nav.textContent = isEn ? 'Thirteen records' : 'Trece registros';
    const index = document.querySelector('.ir-index');
    if (index && !index.querySelector('a[href="#tsj-canarias"]')) html(index, 'beforeend', `<a href="#tsj-canarias"><span>13</span> ${isEn ? 'Canary Islands High Court' : 'TSJ de Canarias'}</a>`);

    const cgpj = document.querySelector('#cgpj');
    if (cgpj) {
      const meta = cgpj.querySelectorAll('.ir-meta strong');
      if (meta[0]) meta[0].textContent = isEn ? '20 August 2026' : '20 agosto 2026';
      if (meta[1]) meta[1].textContent = isEn ? 'DI 169/2026 closed; Appeal 286/2026 in processing' : 'DI 169/2026 archivada; Alzada 286/2026 en tramitación';
      const tbody = cgpj.querySelector('tbody');
      if (tbody && !tbody.textContent.includes('286/2026')) html(tbody, 'beforeend', `<tr><td>16 ${isEn ? 'Jul' : 'jul'} 2026</td><td>${isEn ? 'CGPJ Appeals Section → contributor' : 'Sección de Recursos CGPJ → aportante'}</td><td><strong>${isEn ? 'Appeal' : 'Alzada'} 286/2026</strong></td><td>${isEn ? 'Direct communication confirmed the appeal file and expressly confirmed joinder of the 15 July filing. It does not prove joinder or merits examination of every other supplement.' : 'Comunicación directa confirmó el expediente de alzada y la unión expresa del escrito de 15 de julio. No acredita la unión o examen sustantivo de todas las demás aportaciones.'}</td></tr>`);
    }

    const records = document.querySelector('#records .shell');
    if (records && !document.querySelector('#tsj-canarias')) {
      html(records, 'beforeend', `<article class="ir-record" id="tsj-canarias"><div class="ir-record-head"><div><span class="ir-number">13</span><h2>${isEn ? 'Canary Islands High Court · Government Secretariat' : 'Tribunal Superior de Justicia de Canarias · Secretaría de Gobierno'}</h2><p><strong>${isEn ? 'Competence:' : 'Competencia:'}</strong> ${isEn ? 'government-secretariat and Administration-of-Justice functions concerning court-office/LAJ services, record preservation, routing and hierarchical review. It does not replace judicial appeals or determine criminal responsibility.' : 'funciones de Secretaría de Gobierno y Administración de Justicia sobre servicios LAJ/Oficina Judicial, preservación, remisión y revisión jerárquica. No sustituye recursos jurisdiccionales ni determina responsabilidad penal.'}</p></div><div class="ir-meta"><div><span>${isEn ? 'Last verified' : 'Última verificación'}</span><strong>20 ${isEn ? 'August' : 'agosto'} 2026</strong></div><div><span>${isEn ? 'Status' : 'Estado'}</span><strong>${isEn ? 'Government File 38/2026 archived at first level; final institutional reply recorded; hierarchical appeal filed' : 'Exp. Gub. 38/2026 archivado en primer nivel; respuesta institucional final registrada; alzada presentada'}</strong></div></div></div><div class="ir-table-wrap"><table class="ir-table"><thead><tr><th>${isEn ? 'Date' : 'Fecha'}</th><th>${isEn ? 'Direction' : 'Dirección'}</th><th>${isEn ? 'Reference' : 'Referencia'}</th><th>${isEn ? 'Subject / state' : 'Objeto / estado'}</th></tr></thead><tbody><tr><td>20 ${isEn ? 'Aug' : 'ago'} 2026</td><td>${isEn ? 'Government Secretariat → contributor' : 'Secretaría de Gobierno → aportante'}</td><td><strong>Exp. Gub. 38/2026</strong></td><td>${isEn ? 'First-level archive notified; correct reference later expressly confirmed as 38/2026. Final reply recorded the Secretariat’s general file-content representation, declined item-specific confirmation, reiterated no recorded receipt of the Promotor communication, and took knowledge of the rest of the preceding email.' : 'Archivo de primer nivel notificado; referencia correcta posteriormente confirmada de forma expresa como 38/2026. La respuesta final registró la manifestación general de la Secretaría sobre el expediente, declinó la confirmación individualizada, reiteró la no constancia de recepción de la comunicación del Promotor y tomó conocimiento del resto del correo precedente.'}</td></tr><tr><td>20 ${isEn ? 'Aug' : 'ago'} 2026</td><td>${isEn ? 'Contributor → Government Secretariat / superior route' : 'Aportante → Secretaría de Gobierno / vía superior'}</td><td><strong>REGAGE26e00074355631</strong></td><td>${isEn ? 'Hierarchical appeal filed; forwarding, admission, superior reference and outcome pending.' : 'Recurso de alzada presentado; remisión, admisión, referencia superior y resultado pendientes.'}</td></tr></tbody></table></div><div class="ir-controls"><div class="ir-control proves"><strong>${isEn ? 'Proves' : 'Acredita'}</strong>${isEn ? 'First-level archive, the 20 August institutional statements, the final knowledge checkpoint and the registered appeal filing.' : 'El archivo de primer nivel, las manifestaciones institucionales de 20 de agosto, el punto final de conocimiento y la presentación registrada de la alzada.'}</div><div class="ir-control limit"><strong>${isEn ? 'Does not prove' : 'No acredita'}</strong>${isEn ? 'Agreement, item-level incorporation, a CGPJ dispatch failure, a High Court loss, or admission/forwarding/outcome of the appeal.' : 'Acuerdo, incorporación elemento por elemento, fallo de envío del CGPJ, pérdida por el TSJ o admisión/remisión/resultado de la alzada.'}</div><div class="ir-control action"><strong>${isEn ? 'Outstanding finite action' : 'Acción finita pendiente'}</strong>${isEn ? 'Verify the certified file/index, reconcile dispatch and receipt records and verify forwarding report, superior reference, ATLANTE traceability and the reasoned appeal decision.' : 'Verificar expediente/índice certificado, conciliar salida y recepción y comprobar informe de remisión, referencia superior, trazabilidad ATLANTE y decisión motivada de la alzada.'}</div></div><div class="ir-links"><a href="${isEn ? '../tsj-canarias-exp-gub-38-2026/#respuesta-final' : '../tsj-canarias-exp-gub-38-2026/#respuesta-final'}">${isEn ? 'Full Government File and final reply →' : 'Expediente completo y respuesta final →'}</a><a href="${isEn ? '../tsj-canarias-exp-gub-38-2026-appeal-filed/' : '../tsj-canarias-exp-gub-38-2026-alzada-presentada/'}">${isEn ? 'Verified appeal filing →' : 'Alzada verificada →'}</a></div></article>`);
    }

    const tsj = document.querySelector('#tsj-canarias');
    if (tsj && !tsj.querySelector('[data-rubio-final-institutional]')) {
      html(tsj, 'beforeend', `<div class="pd-parity-note knowledge" data-rubio-final-institutional><strong>${isEn ? 'Final institutional reply · 20 August 2026.' : 'Respuesta institucional final · 20 de agosto de 2026.'}</strong> ${isEn ? 'The Secretary’s later reply is separately controlled: 38/2026 confirmed; general file-content representation; item-specific confirmation declined; Law 39/2015 assurance not separately given; CGPJ receipt still not recorded; remainder of the preceding email taken into account. Knowledge is not treated as agreement or admission.' : 'La respuesta posterior del Secretario queda controlada separadamente: 38/2026 confirmado; manifestación general sobre el expediente; confirmación individualizada declinada; no se ofrece confirmación separada sobre Ley 39/2015; sigue sin constar la recepción CGPJ; y se toma conocimiento del resto del correo precedente. El conocimiento no se trata como acuerdo ni admisión.'} <a href="${isEn ? '../tsj-canarias-exp-gub-38-2026/#respuesta-final' : '../tsj-canarias-exp-gub-38-2026/#respuesta-final'}">${isEn ? 'Canonical source-controlled record →' : 'Registro canónico controlado por fuente →'}</a></div>`);
    }
  }

  const home = /\/por-derecho\/(es|en)\/?(?:index\.html)?$/.test(path) || /^\/(es|en)\/?(?:index\.html)?$/.test(path);
  if (home) {
    const cgpj = document.querySelector('.authority-card[data-search*="unidad de registro y archivo del consejo general del poder judicial"]');
    if (cgpj) {
      const state = cgpj.querySelector('footer strong');
      if (state) state.textContent = isEn ? 'Appeal 286/2026 in processing; later supplements require file-level reconciliation' : 'Alzada 286/2026 en tramitación; aportaciones posteriores requieren conciliación de expediente';
      const first = cgpj.querySelector('dl div:first-child dd');
      if (first && !first.textContent.includes('286/2026')) html(first, 'beforeend', isEn ? ' The Appeals Section later identified Appeal 286/2026 and expressly confirmed joinder of the 15 July filing.' : ' La Sección de Recursos identificó después la Alzada 286/2026 y confirmó expresamente la unión del escrito de 15 de julio.');
      if (!document.querySelector('[data-tsj-authority-card]')) html(cgpj, 'afterend', `<article class="authority-card" data-tsj-authority-card data-cluster="judicial_protection_and_court_governance" data-effect="appeal" data-search="secretaría de gobierno del tribunal superior de justicia de canarias"><header><span class="authority-rank">TSJ</span><span class="authority-tile" aria-hidden="true">SG</span><div><h4>${isEn ? 'Canary Islands High Court · Government Secretariat' : 'TSJ de Canarias · Secretaría de Gobierno'}</h4><p>${isEn ? 'Court-office / LAJ traceability and hierarchical review' : 'Trazabilidad LAJ/Oficina Judicial y revisión jerárquica'}</p></div></header><dl><div><dt>${isEn ? 'Recorded' : 'Lo que consta'}</dt><dd>${isEn ? 'Government File 38/2026 was archived at first level on 20 August; Rubio Faure’s final reply expressly confirmed the reference, recorded a general file-content representation, declined item-level confirmation, reiterated no recorded receipt of the CGPJ communication and took knowledge of the rest of the preceding email. The hierarchical appeal was filed the same day under REGAGE26e00074355631.' : 'El Exp. Gub. 38/2026 fue archivado en primer nivel el 20 de agosto; la respuesta final de Rubio Faure confirmó expresamente la referencia, registró una manifestación general sobre el expediente, declinó la confirmación elemento por elemento, reiteró la no constancia de recepción de la comunicación CGPJ y tomó conocimiento del resto del correo precedente. La alzada se presentó ese mismo día bajo REGAGE26e00074355631.'}</dd></div><div><dt>${isEn ? 'Does not decide' : 'No decide'}</dt><dd>${isEn ? 'Knowledge is not agreement; the general inclusion statement is not item-level certification; filing does not establish admission, forwarding or outcome; and the TSJ non-receipt statement does not prove a CGPJ dispatch failure.' : 'El conocimiento no equivale a acuerdo; la manifestación general de inclusión no es certificación elemento por elemento; la presentación no acredita admisión, remisión o resultado; y la no constancia de recepción TSJ no prueba un fallo de envío del CGPJ.'}</dd></div><div><dt>${isEn ? 'Outstanding action' : 'Acción pendiente'}</dt><dd>${isEn ? 'Verify certified incorporation/indexing, reconcile CGPJ dispatch/TSJ receipt and verify forwarding, superior reference, ATLANTE traceability and reasoned decision.' : 'Verificar incorporación/indexado certificado, conciliar salida CGPJ/recepción TSJ y comprobar remisión, referencia superior, trazabilidad ATLANTE y decisión motivada.'}</dd></div></dl><footer><span>Exp. Gub. 38/2026</span><strong>${isEn ? 'Final reply recorded · appeal filed' : 'Respuesta final registrada · alzada presentada'}</strong></footer></article>`);
    }
  }

  if (/\/(es\/actualizaciones|en\/updates)\/?(?:index\.html)?$/.test(path)) {
    const latest = document.querySelector('.update-status strong');
    if (latest) latest.textContent = isEn ? '20 August 2026' : '20 agosto 2026';
    const first = document.querySelector('.updates-section');
    if (first && !document.querySelector('[data-update-20aug-cgpj-tsj]')) {
      html(first, 'beforebegin', `<section class="updates-section pd-parity-update" data-update-20aug-cgpj-tsj><div class="shell"><section class="date-group"><h2>20 ${isEn ? 'August' : 'agosto'} 2026 · ${isEn ? 'judicial governance' : 'gobierno judicial'}</h2><div class="update-stream"><article class="material-update institutional"><div class="update-meta"><span class="new">${isEn ? 'New' : 'Nuevo'}</span><span>TSJ Canarias</span><span>${isEn ? 'Final institutional reply + hierarchical appeal' : 'Respuesta institucional final + alzada'}</span></div><h3>${isEn ? 'Government File 38/2026: final reply source-controlled; hierarchical appeal filed and registered' : 'Exp. Gub. 38/2026: respuesta final controlada por fuente; alzada presentada y registrada'}</h3><p>${isEn ? 'Rubio Faure’s later 20-August reply expressly confirmed 38/2026 as the correct reference, represented generally that the governmental file includes the acts carried out within it, declined item-specific confirmation, reiterated that receipt of the CGPJ communication was not recorded, and took knowledge of the remainder of the preceding email. That creates a bounded institutional knowledge checkpoint; it is not agreement or admission.' : 'La respuesta posterior de Rubio Faure de 20 de agosto confirmó expresamente 38/2026 como referencia correcta, manifestó con carácter general que el expediente gubernativo incluye las actuaciones realizadas en él, declinó la confirmación individualizada, reiteró que no constaba la recepción de la comunicación CGPJ y tomó conocimiento del resto del correo precedente. Esto crea un punto de conocimiento institucional acotado; no es acuerdo ni admisión.'}</p><p>${isEn ? 'REGAGE registered the same-day appeal filing as REGAGE26e00074355631. Filing proves presentation, destination, timing and submitted-file integrity; forwarding, admission, superior reference and outcome remain pending.' : 'REGAGE registró la presentación de la alzada ese mismo día como REGAGE26e00074355631. El justificante acredita presentación, destino, hora e integridad del archivo; remisión, admisión, referencia superior y resultado siguen pendientes.'}</p><p>${isEn ? 'The same chain contains a finite CGPJ→TSJ reconciliation question. No dispatch failure or loss is inferred.' : 'La misma cadena contiene una cuestión finita de conciliación CGPJ→TSJ. No se infiere fallo de envío ni pérdida.'}</p><div class="update-links"><a href="${isEn ? '../tsj-canarias-exp-gub-38-2026/#respuesta-final' : '../tsj-canarias-exp-gub-38-2026/#respuesta-final'}">${isEn ? 'Final institutional reply →' : 'Respuesta institucional final →'}</a><a href="${isEn ? '../tsj-canarias-exp-gub-38-2026-appeal-filed/' : '../tsj-canarias-exp-gub-38-2026-alzada-presentada/'}">${isEn ? 'Verified filing record →' : 'Registro verificado de presentación →'}</a><a href="${isEn ? '../open-message-cgpj/' : '../mensaje-abierto-cgpj/'}">CGPJ →</a></div></article><article class="material-update institutional"><div class="update-meta"><span>${isEn ? 'Professional custodians' : 'Custodios profesionales'}</span><span>PwC · Grant Thornton · RSM</span></div><h3>${isEn ? 'Current preservation and reconciliation status' : 'Estado actual de preservación y reconciliación'}</h3><p>${isEn ? 'The three firms have received separate source-controlled updates. Their relevance here is evidential custody: possible conflict, engagement, access, referral, time, billing and file-separation records. No firm is treated as liable merely because of a professional relationship, and no current response period is treated as expired.' : 'Las tres firmas han recibido actualizaciones separadas y controladas por fuentes. Su relevancia aquí es la custodia probatoria: posibles registros de conflicto, encargo, acceso, referral, tiempos, facturación y separación de expedientes. Ninguna firma se trata como responsable por la mera relación profesional, ni se considera vencido ningún plazo de respuesta actual.'}</p></article></div></section></div></section>`);
    }
  }

  const professional = [
    [/\/pwc-canarias-carlos-saavedra-sun-park\//, 'pwc'],
    [/\/grant-thornton\/2024-04\//, 'gt'],
    [/\/rsm\/nnr4-1025c2f66\//, 'rsm']
  ].find(([re]) => re.test(path));
  if (professional) {
    const hero = document.querySelector('.hero .shell') || document.querySelector('.hero');
    if (hero && !hero.querySelector('[data-professional-20aug-status]')) {
      const type = professional[1];
      let copy;
      if (type === 'pwc') copy = isEn
        ? '<strong>19–20 August 2026 status.</strong> The institutional escalation and preservation request is source-controlled, including six finite former-client/confidentiality/conflict/information-governance questions. No later substantive PwC response has been located; no admission is inferred.'
        : '<strong>Estado 19–20 agosto 2026.</strong> La escalación institucional y la petición de preservación quedan controladas por fuentes, incluidas seis preguntas finitas sobre antiguo cliente, confidencialidad, conflicto y gobierno de información. No se ha localizado una respuesta sustantiva posterior de PwC; no se infiere admisión.';
      if (type === 'gt') copy = isEn
        ? '<strong>18–20 August 2026 status.</strong> A supplemental reconciliation notice has been sent concerning the 2020 conflict/confidentiality memory, the later Canary professional/commercial relationship and the San Telmo source as an institutional-memory question. No adverse inference is drawn from the absence of a new substantive response.'
        : '<strong>Estado 18–20 agosto 2026.</strong> Se ha remitido una actualización de reconciliación sobre la memoria de conflicto/confidencialidad de 2020, la posterior relación profesional/comercial canaria y la fuente San Telmo como cuestión de memoria institucional. No se extrae inferencia adversa de la ausencia de nueva respuesta sustantiva.';
      if (type === 'rsm') copy = isEn
        ? '<strong>19–20 August 2026 status.</strong> The San Telmo source has been added to ethics review NNR4-1025C2F66. RSM’s communicated September 2026 conclusion window remains operative; RSM is not treated as overdue and current silence is not treated as substantive refusal.'
        : '<strong>Estado 19–20 agosto 2026.</strong> La fuente San Telmo ha sido incorporada a la revisión ética NNR4-1025C2F66. La ventana comunicada por RSM para conclusiones en septiembre de 2026 sigue vigente; RSM no se trata como fuera de plazo ni el silencio actual como negativa sustantiva.';
      copy += ` <a href="${isEn ? '../tsj-canarias-exp-gub-38-2026/#respuesta-final' : '../tsj-canarias-exp-gub-38-2026/#respuesta-final'}">${isEn ? 'TSJ institutional checkpoint →' : 'Punto institucional TSJ →'}</a>`;
      html(hero, 'beforeend', `<div class="pd-parity-note" data-professional-20aug-status>${copy}</div>`);
    }
  }

  const concursoPage = /\/(es\/concurso-36-2012-(?:magistrado-juez|administrador-concursal)|en\/insolvency-36-2012-(?:mercantile-court-1|insolvency-administrator))\/?(?:index\.html)?$/.test(path);
  if (concursoPage) {
    const hero = document.querySelector('.hero .shell') || document.querySelector('.hero');
    if (hero && !document.querySelector('[data-tsj-document-chain-crosslink]')) {
      html(hero, 'beforeend', `<div class="pd-parity-note knowledge" data-tsj-document-chain-crosslink><strong>${isEn ? 'LAJ / Office-of-the-Court traceability checkpoint.' : 'Punto de trazabilidad LAJ / Oficina Judicial.'}</strong> ${isEn ? 'The separate Government File 38/2026 record now includes the Secretary of Government’s final 20-August reply: the correct reference was confirmed, a general representation was made about the governmental file, item-level confirmation was declined, CGPJ receipt remained unrecorded and the remainder of the preceding email was taken into account. This is relevant to the documentary-chain questions here without converting institutional notice into agreement or any finding of wrongdoing.' : 'El registro separado del Exp. Gub. 38/2026 incorpora ahora la respuesta final del Secretario de Gobierno de 20 de agosto: se confirmó la referencia correcta, se efectuó una manifestación general sobre el expediente gubernativo, se declinó la confirmación individualizada, seguía sin constar la recepción CGPJ y se tomó conocimiento del resto del correo precedente. Es relevante para las cuestiones de cadena documental aquí tratadas sin convertir el conocimiento institucional en acuerdo ni en conclusión de ilicitud.'} <a href="${isEn ? '../tsj-canarias-exp-gub-38-2026/#respuesta-final' : '../tsj-canarias-exp-gub-38-2026/#respuesta-final'}">${isEn ? 'Canonical TSJ record →' : 'Registro canónico TSJ →'}</a></div>`);
    }
  }
})();