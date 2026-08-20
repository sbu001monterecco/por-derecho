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
    .pd-parity-note strong,.pd-parity-note a{font-weight:900}
    .pd-parity-update{scroll-margin-top:5rem}
  `;
  document.head.appendChild(style);

  if (/\/(es|en)\/tsj-canarias-exp-gub-38-2026\/?(?:index\.html)?$/.test(path)) {
    const status = document.querySelector('.hero .status');
    if (status) status.textContent = isEn
      ? 'First-level archive · appeal filed · receipt verified · forwarding and admission pending'
      : 'Archivo de primera instancia · alzada presentada · justificante verificado · remisión y admisión pendientes';
    const anchor = document.querySelector('.hero .alert') || status;
    if (anchor && !document.querySelector('[data-tsj-filed-parity]')) {
      html(anchor, 'afterend', `<div class="pd-parity-note" data-tsj-filed-parity><strong>${isEn ? 'Procedural update · 20 August 2026.' : 'Actualización procesal · 20 de agosto de 2026.'}</strong> ${isEn ? 'The hierarchical appeal has been filed and registered as' : 'El recurso de alzada ha sido presentado y registrado como'} <strong>REGAGE26e00074355631</strong>. ${isEn ? 'Filing proves presentation, destination, timestamp and the submitted-file integrity record; it does not prove admission, forwarding or outcome.' : 'La presentación acredita destino, fecha, hora e integridad del archivo aportado; no acredita admisión, remisión ni resultado.'} <a href="${isEn ? '../tsj-canarias-exp-gub-38-2026-appeal-filed/' : '../tsj-canarias-exp-gub-38-2026-alzada-presentada/'}">${isEn ? 'Verified filing record →' : 'Registro verificado de presentación →'}</a></div>`);
    }
  }

  if (/\/(es\/mensaje-abierto-cgpj|en\/open-message-cgpj)\/?(?:index\.html)?$/.test(path)) {
    const shell = document.querySelector('#caso .shell');
    if (shell && !document.querySelector('[data-cgpj-tsj-reconciliation]')) {
      html(shell, 'beforeend', `<div class="pd-parity-note warning" data-cgpj-tsj-reconciliation><strong>${isEn ? '20 August 2026 · CGPJ → TSJ transmission reconciliation.' : '20 de agosto de 2026 · reconciliación de transmisión CGPJ → TSJ.'}</strong> ${isEn ? 'The Promotor’s 14 May agreement ordered communication to the Canary Islands High Court. On 20 August, the High Court Government Secretariat stated that receipt was not recorded there as of that date. This does not establish a CGPJ dispatch failure or a High Court loss. It opens a finite documentary reconciliation: dispatch date/channel → recipient → receipt → internal registration → present custody. That reconciliation is now expressly requested in the hierarchical appeal filed in Government File 38/2026.' : 'El acuerdo del Promotor de 14 de mayo ordenó comunicación al TSJ de Canarias. El 20 de agosto, la Secretaría de Gobierno manifestó que no constaba allí su recepción a esa fecha. Esto no acredita un fallo de envío del CGPJ ni una pérdida por el TSJ. Abre una conciliación documental finita: fecha/canal de salida → destinatario → recepción → registro interno → custodia actual. Esa conciliación se ha solicitado expresamente en la alzada presentada en el Exp. Gub. 38/2026.'} <a href="${isEn ? '../tsj-canarias-exp-gub-38-2026-appeal-filed/' : '../tsj-canarias-exp-gub-38-2026-alzada-presentada/'}">${isEn ? 'Verified appeal filing →' : 'Alzada verificada →'}</a></div>`);
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
      html(records, 'beforeend', `<article class="ir-record" id="tsj-canarias"><div class="ir-record-head"><div><span class="ir-number">13</span><h2>${isEn ? 'Canary Islands High Court · Government Secretariat' : 'Tribunal Superior de Justicia de Canarias · Secretaría de Gobierno'}</h2><p><strong>${isEn ? 'Competence:' : 'Competencia:'}</strong> ${isEn ? 'government-secretariat and Administration-of-Justice functions concerning court-office/LAJ services, record preservation, routing and hierarchical review. It does not replace judicial appeals or determine criminal responsibility.' : 'funciones de Secretaría de Gobierno y Administración de Justicia sobre servicios LAJ/Oficina Judicial, preservación, remisión y revisión jerárquica. No sustituye recursos jurisdiccionales ni determina responsabilidad penal.'}</p></div><div class="ir-meta"><div><span>${isEn ? 'Last verified' : 'Última verificación'}</span><strong>20 ${isEn ? 'August' : 'agosto'} 2026</strong></div><div><span>${isEn ? 'Status' : 'Estado'}</span><strong>${isEn ? 'Government File 38/2026 archived at first level; hierarchical appeal filed' : 'Exp. Gub. 38/2026 archivado en primer nivel; alzada presentada'}</strong></div></div></div><div class="ir-table-wrap"><table class="ir-table"><thead><tr><th>${isEn ? 'Date' : 'Fecha'}</th><th>${isEn ? 'Direction' : 'Dirección'}</th><th>${isEn ? 'Reference' : 'Referencia'}</th><th>${isEn ? 'Subject / state' : 'Objeto / estado'}</th></tr></thead><tbody><tr><td>20 ${isEn ? 'Aug' : 'ago'} 2026</td><td>${isEn ? 'Government Secretariat → contributor' : 'Secretaría de Gobierno → aportante'}</td><td><strong>Exp. Gub. 38/2026</strong></td><td>${isEn ? 'First-level archive notified; correct reference confirmed as 38/2026. The Secretariat stated that the Promotor communication to the High Court was not recorded as received there as of that date.' : 'Archivo de primer nivel notificado; referencia correcta confirmada como 38/2026. La Secretaría manifestó que no constaba allí recibida, a esa fecha, la comunicación del Promotor al TSJ.'}</td></tr><tr><td>20 ${isEn ? 'Aug' : 'ago'} 2026</td><td>${isEn ? 'Contributor → Government Secretariat / superior route' : 'Aportante → Secretaría de Gobierno / vía superior'}</td><td><strong>REGAGE26e00074355631</strong></td><td>${isEn ? 'Hierarchical appeal filed; forwarding, admission, superior reference and outcome pending.' : 'Recurso de alzada presentado; remisión, admisión, referencia superior y resultado pendientes.'}</td></tr></tbody></table></div><div class="ir-controls"><div class="ir-control proves"><strong>${isEn ? 'Proves' : 'Acredita'}</strong>${isEn ? 'First-level archive, the 20 August institutional statements and the registered appeal filing.' : 'El archivo de primer nivel, las manifestaciones institucionales de 20 de agosto y la presentación registrada de la alzada.'}</div><div class="ir-control limit"><strong>${isEn ? 'Does not prove' : 'No acredita'}</strong>${isEn ? 'A CGPJ dispatch failure, a High Court loss, or admission/forwarding/outcome of the appeal.' : 'Un fallo de envío del CGPJ, una pérdida por el TSJ, o admisión/remisión/resultado de la alzada.'}</div><div class="ir-control action"><strong>${isEn ? 'Outstanding finite action' : 'Acción finita pendiente'}</strong>${isEn ? 'Reconcile dispatch and receipt records and verify full incorporation, forwarding report, superior reference, ATLANTE traceability and the reasoned appeal decision.' : 'Conciliar salida y recepción y verificar incorporación íntegra, informe de remisión, referencia superior, trazabilidad ATLANTE y decisión motivada de la alzada.'}</div></div><div class="ir-links"><a href="${isEn ? '../tsj-canarias-exp-gub-38-2026/' : '../tsj-canarias-exp-gub-38-2026/'}">${isEn ? 'Full Government File record →' : 'Expediente completo →'}</a><a href="${isEn ? '../tsj-canarias-exp-gub-38-2026-appeal-filed/' : '../tsj-canarias-exp-gub-38-2026-alzada-presentada/'}">${isEn ? 'Verified appeal filing →' : 'Alzada verificada →'}</a></div></article>`);
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
      if (!document.querySelector('[data-tsj-authority-card]')) html(cgpj, 'afterend', `<article class="authority-card" data-tsj-authority-card data-cluster="judicial_protection_and_court_governance" data-effect="appeal" data-search="secretaría de gobierno del tribunal superior de justicia de canarias"><header><span class="authority-rank">TSJ</span><span class="authority-tile" aria-hidden="true">SG</span><div><h4>${isEn ? 'Canary Islands High Court · Government Secretariat' : 'TSJ de Canarias · Secretaría de Gobierno'}</h4><p>${isEn ? 'Court-office / LAJ traceability and hierarchical review' : 'Trazabilidad LAJ/Oficina Judicial y revisión jerárquica'}</p></div></header><dl><div><dt>${isEn ? 'Recorded' : 'Lo que consta'}</dt><dd>${isEn ? 'Government File 38/2026 was archived at first level on 20 August; the hierarchical appeal was filed the same day under REGAGE26e00074355631.' : 'El Exp. Gub. 38/2026 fue archivado en primer nivel el 20 de agosto; la alzada se presentó ese mismo día bajo REGAGE26e00074355631.'}</dd></div><div><dt>${isEn ? 'Does not decide' : 'No decide'}</dt><dd>${isEn ? 'Filing does not establish admission, forwarding or outcome, and the TSJ non-receipt statement does not prove a CGPJ dispatch failure.' : 'La presentación no acredita admisión, remisión o resultado, y la manifestación TSJ de no constancia de recepción no prueba un fallo de envío del CGPJ.'}</dd></div><div><dt>${isEn ? 'Outstanding action' : 'Acción pendiente'}</dt><dd>${isEn ? 'Reconcile CGPJ dispatch/TSJ receipt and verify incorporation, forwarding, superior reference and reasoned decision.' : 'Conciliar salida CGPJ/recepción TSJ y verificar incorporación, remisión, referencia superior y decisión motivada.'}</dd></div></dl><footer><span>Exp. Gub. 38/2026</span><strong>${isEn ? 'Hierarchical appeal filed' : 'Alzada presentada'}</strong></footer></article>`);
    }
  }

  if (/\/(es\/actualizaciones|en\/updates)\/?(?:index\.html)?$/.test(path)) {
    const latest = document.querySelector('.update-status strong');
    if (latest) latest.textContent = isEn ? '20 August 2026' : '20 agosto 2026';
    const first = document.querySelector('.updates-section');
    if (first && !document.querySelector('[data-update-20aug-cgpj-tsj]')) {
      html(first, 'beforebegin', `<section class="updates-section pd-parity-update" data-update-20aug-cgpj-tsj><div class="shell"><section class="date-group"><h2>20 ${isEn ? 'August' : 'agosto'} 2026 · ${isEn ? 'judicial governance' : 'gobierno judicial'}</h2><div class="update-stream"><article class="material-update institutional"><div class="update-meta"><span class="new">${isEn ? 'New' : 'Nuevo'}</span><span>TSJ Canarias</span><span>${isEn ? 'Hierarchical appeal' : 'Alzada'}</span></div><h3>${isEn ? 'Government File 38/2026: hierarchical appeal filed and registered' : 'Exp. Gub. 38/2026: alzada presentada y registrada'}</h3><p>${isEn ? 'REGAGE registered the 20 August filing as REGAGE26e00074355631. The receipt proves presentation, destination, timing and submitted-file integrity; forwarding, admission, superior reference and outcome remain pending.' : 'REGAGE registró la presentación de 20 de agosto como REGAGE26e00074355631. El justificante acredita presentación, destino, hora e integridad del archivo; remisión, admisión, referencia superior y resultado siguen pendientes.'}</p><p>${isEn ? 'The same chain contains a finite CGPJ→TSJ reconciliation question: the Promotor ordered communication to the High Court, while the High Court Government Secretariat stated on 20 August that receipt was not recorded there as of that date. No dispatch failure or loss is inferred.' : 'La misma cadena contiene una cuestión finita de conciliación CGPJ→TSJ: el Promotor ordenó comunicación al TSJ, mientras que la Secretaría de Gobierno manifestó el 20 de agosto que no constaba allí su recepción a esa fecha. No se infiere fallo de envío ni pérdida.'}</p><div class="update-links"><a href="${isEn ? '../tsj-canarias-exp-gub-38-2026-appeal-filed/' : '../tsj-canarias-exp-gub-38-2026-alzada-presentada/'}">${isEn ? 'Verified filing record →' : 'Registro verificado de presentación →'}</a><a href="${isEn ? '../open-message-cgpj/' : '../mensaje-abierto-cgpj/'}">CGPJ →</a></div></article><article class="material-update institutional"><div class="update-meta"><span>${isEn ? 'Professional custodians' : 'Custodios profesionales'}</span><span>PwC · Grant Thornton · RSM</span></div><h3>${isEn ? 'Current preservation and reconciliation status' : 'Estado actual de preservación y reconciliación'}</h3><p>${isEn ? 'The three firms have received separate source-controlled updates. Their relevance here is evidential custody: possible conflict, engagement, access, referral, time, billing and file-separation records. No firm is treated as liable merely because of a professional relationship, and no current response period is treated as expired.' : 'Las tres firmas han recibido actualizaciones separadas y controladas por fuentes. Su relevancia aquí es la custodia probatoria: posibles registros de conflicto, encargo, acceso, referral, tiempos, facturación y separación de expedientes. Ninguna firma se trata como responsable por la mera relación profesional, ni se considera vencido ningún plazo de respuesta actual.'}</p></article></div></section></div></section>`);
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
      html(hero, 'beforeend', `<div class="pd-parity-note" data-professional-20aug-status>${copy}</div>`);
    }
  }
})();
