(() => {
  const path = window.location.pathname;
  const isEn = /^\/por-derecho\/en\//.test(path) || /^\/en\//.test(path);
  const marker = 'cgpj-tsj-professional-parity-20260820';
  if (document.documentElement.dataset[marker]) return;
  document.documentElement.dataset[marker] = 'true';

  const style = document.createElement('style');
  style.textContent = `
    .pd-parity-note{margin:1rem 0;padding:1rem 1.15rem;border-left:6px solid #245c49;background:#edf3ee;border-radius:14px;color:#13252d}
    .pd-parity-note.warning{border-left-color:#c89432;background:#fff8e8}
    .pd-parity-note strong{font-weight:900}
    .pd-parity-note a{font-weight:850}
    .pd-parity-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.8rem;margin-top:1rem}
    .pd-parity-grid>article{background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:14px;padding:1rem}
    .pd-parity-grid h3{margin:.15rem 0 .55rem}
    .pd-parity-tag{font-size:.72rem;font-weight:900;letter-spacing:.06em;text-transform:uppercase;color:#7a571b}
    .pd-parity-update{scroll-margin-top:5rem}
    @media(max-width:850px){.pd-parity-grid{grid-template-columns:1fr}}
  `;
  document.head.appendChild(style);

  const addAfter = (node, html) => {
    if (!node) return;
    node.insertAdjacentHTML('afterend', html);
  };

  const tsjFull = /\/(es|en)\/tsj-canarias-exp-gub-38-2026\/?(?:index\.html)?$/.test(path);
  if (tsjFull) {
    const status = document.querySelector('.hero .status');
    if (status) status.textContent = isEn
      ? 'First-level archive · appeal filed · receipt verified · forwarding and admission pending'
      : 'Archivo de primera instancia · alzada presentada · justificante verificado · remisión y admisión pendientes';
    const anchor = document.querySelector('.hero .alert') || document.querySelector('.hero .status');
    if (anchor && !document.querySelector('[data-tsj-filed-parity]')) {
      addAfter(anchor, `<div class="pd-parity-note" data-tsj-filed-parity="true"><strong>${isEn ? 'Procedural update · 20 August 2026.' : 'Actualización procesal · 20 de agosto de 2026.'}</strong> ${isEn
        ? 'The hierarchical appeal has now been filed and registered as <strong>REGAGE26e00074355631</strong>. Filing proves presentation, destination, timestamp and the submitted-file integrity record; it does not prove admission, forwarding to the superior authority or outcome.'
        : 'El recurso de alzada ya ha sido presentado y registrado como <strong>REGAGE26e00074355631</strong>. La presentación acredita destino, fecha, hora e integridad del archivo aportado; no acredita admisión, remisión al órgano superior ni resultado.'} <a href="${isEn ? '../tsj-canarias-exp-gub-38-2026-appeal-filed/' : '../tsj-canarias-exp-gub-38-2026-alzada-presentada/'}">${isEn ? 'Open the verified filing record →' : 'Abrir el registro verificado de presentación →'}</a></div>`);
    }
  }

  const cgpjOpen = /\/(es\/mensaje-abierto-cgpj|en\/open-message-cgpj)\/?(?:index\.html)?$/.test(path);
  if (cgpjOpen) {
    const caseShell = document.querySelector('#caso .shell');
    if (caseShell && !document.querySelector('[data-cgpj-tsj-reconciliation]')) {
      caseShell.insertAdjacentHTML('beforeend', `<div class="pd-parity-note warning" data-cgpj-tsj-reconciliation="true"><strong>${isEn ? '20 August 2026 · CGPJ → TSJ transmission reconciliation.' : '20 de agosto de 2026 · reconciliación de transmisión CGPJ → TSJ.'}</strong> ${isEn
        ? 'The Promotor’s 14 May agreement ordered communication to the Canary Islands High Court. On 20 August, the High Court Government Secretariat stated that receipt was not recorded there as of that date. This does not establish that the CGPJ failed to send the communication or that the High Court lost it. It opens a finite documentary reconciliation: dispatch date/channel → recipient → receipt → internal registration → present custody. That reconciliation has now been expressly requested in the hierarchical appeal filed in Government File 38/2026.'
        : 'El acuerdo del Promotor de 14 de mayo ordenó comunicación al TSJ de Canarias. El 20 de agosto, la Secretaría de Gobierno del TSJ manifestó que no constaba allí su recepción a esa fecha. Esto no acredita que el CGPJ no la enviara ni que el TSJ la extraviara. Abre una reconciliación documental finita: fecha/canal de salida → destinatario → recepción → registro interno → custodia actual. Esa reconciliación ha sido solicitada expresamente en la alzada presentada en el Exp. Gub. 38/2026.'} <a href="${isEn ? '../tsj-canarias-exp-gub-38-2026-appeal-filed/' : '../tsj-canarias-exp-gub-38-2026-alzada-presentada/'}">${isEn ? 'Verified appeal-filing record →' : 'Registro verificado de la alzada →'}</a></div>`);
    }
  }

  const institutional = /\/(es\/registros-institucionales|en\/institutional-records)\/?(?:index\.html)?$/.test(path);
  if (institutional) {
    const heroLead = document.querySelector('.ir-hero .lead');
    if (heroLead) heroLead.textContent = isEn
      ? 'Thirteen stable records consolidate key communications and bounded technical references concerning public bodies and statutory professional corporations on the accountability map. Each separates competence, traceable events, evidential limits and one finite outstanding action.'
      : 'Trece registros estables consolidan comunicaciones clave y referencias técnicas delimitadas relativas a los organismos públicos y corporaciones profesionales de derecho público del mapa de control. Cada uno separa competencia, hitos trazables, límites probatorios y una acción finita pendiente.';
    const scopeStrong = document.querySelector('.ir-status div:first-child strong');
    if (scopeStrong) scopeStrong.textContent = isEn ? 'Thirteen public-body and statutory professional-corporation records' : 'Trece registros de organismos públicos y corporaciones profesionales de derecho público';
    const navRecords = document.querySelector('.main-nav a[href="#records"]');
    if (navRecords) navRecords.textContent = isEn ? 'Thirteen records' : 'Trece registros';
    const index = document.querySelector('.ir-index');
    if (index && !index.querySelector('a[href="#tsj-canarias"]')) index.insertAdjacentHTML('beforeend', `<a href="#tsj-canarias"><span>13</span> ${isEn ? 'Canary Islands High Court' : 'TSJ de Canarias'}</a>`);

    const cgpj = document.querySelector('#cgpj');
    if (cgpj) {
      const meta = cgpj.querySelectorAll('.ir-meta strong');
      if (meta[0]) meta[0].textContent = isEn ? '20 August 2026' : '20 agosto 2026';
      if (meta[1]) meta[1].textContent = isEn ? 'DI 169/2026 closed; Appeal 286/2026 in processing' : 'DI 169/2026 archivada; Alzada 286/2026 en tramitación';
      const tbody = cgpj.querySelector('tbody');
      if (tbody && !tbody.textContent.includes('286/2026')) tbody.insertAdjacentHTML('beforeend', `<tr><td>16 ${isEn ? 'Jul' : 'jul'} 2026</td><td>${isEn ? 'CGPJ Appeals Section → contributor' : 'Sección de Recursos CGPJ → aportante'}</td><td><strong>${isEn ? 'Appeal' : 'Alzada'} 286/2026</strong></td><td>${isEn ? 'Direct communication confirmed the appeal file and expressly confirmed joinder of the 15 July filing. It does not prove joinder or merits examination of every other supplement.' : 'Comunicación directa confirmó el expediente de alzada y la unión expresa del escrito de 15 de julio. No acredita la unión o examen sustantivo de todas las demás aportaciones.'}</td></tr>`);
    }

    const recordsShell = document.querySelector('#records .shell');
    if (recordsShell && !document.querySelector('#tsj-canarias')) {
      recordsShell.insertAdjacentHTML('beforeend', `<article class="ir-record" id="tsj-canarias"><div class="ir-record-head"><div><span class="ir-number">13</span><h2>${isEn ? 'Canary Islands High Court · Government Secretariat' : 'Tribunal Superior de Justicia de Canarias · Secretaría de Gobierno'}</h2><p><strong>${isEn ? 'Competence:' : 'Competencia:'}</strong> ${isEn ? 'government-secretariat and Administration-of-Justice functions concerning court-office/LAJ service, record preservation, routing and the hierarchical appeal within the applicable administrative chain. It does not replace judicial appeals or determine criminal responsibility.' : 'funciones de Secretaría de Gobierno y Administración de Justicia sobre servicios LAJ/Oficina Judicial, preservación, remisión y alzada dentro de la cadena administrativa aplicable. No sustituye recursos jurisdiccionales ni determina responsabilidad penal.'}</p></div><div class="ir-meta"><div><span>${isEn ? 'Last verified' : 'Última verificación'}</span><strong>20 ${isEn ? 'August' : 'agosto'} 2026</strong></div><div><span>${isEn ? 'Status' : 'Estado'}</span><strong>${isEn ? 'Government File 38/2026 archived at first level; hierarchical appeal filed' : 'Exp. Gub. 38/2026 archivado en primer nivel; alzada presentada'}</strong></div></div></div><div class="ir-table-wrap"><table class="ir-table"><thead><tr><th>${isEn ? 'Date' : 'Fecha'}</th><th>${isEn ? 'Direction' : 'Dirección'}</th><th>${isEn ? 'Reference' : 'Referencia'}</th><th>${isEn ? 'Subject / state' : 'Objeto / estado'}</th></tr></thead><tbody><tr><td>20 ${isEn ? 'Aug' : 'ago'} 2026</td><td>${isEn ? 'Government Secretariat → contributor' : 'Secretaría de Gobierno → aportante'}</td><td><strong>Exp. Gub. 38/2026</strong></td><td>${isEn ? 'First-level archive notified; correct reference confirmed as 38/2026. The Secretariat stated that the Promotor communication to the High Court was not recorded as received there as of that date.' : 'Archivo de primer nivel notificado; referencia correcta confirmada como 38/2026. La Secretaría manifestó que no constaba allí recibida, a esa fecha, la comunicación del Promotor al TSJ.'}</td></tr><tr><td>20 ${isEn ? 'Aug' : 'ago'} 2026</td><td>${isEn ? 'Contributor → Government Secretariat / superior route' : 'Aportante → Secretaría de Gobierno / vía superior'}</td><td><strong>REGAGE26e00074355631</strong></td><td>${isEn ? 'Hierarchical appeal filed. Receipt verified; forwarding, admission, superior reference and outcome pending.' : 'Recurso de alzada presentado. Justificante verificado; remisión, admisión, referencia superior y resultado pendientes.'}</td></tr></tbody></table></div><div class="ir-controls"><div class="ir-control proves"><strong>${isEn ? 'Proves' : 'Acredita'}</strong>${isEn ? 'First-level archive, the 20 August institutional statements and the registered filing of the hierarchical appeal.' : 'El archivo de primer nivel, las manifestaciones institucionales de 20 de agosto y la presentación registrada del recurso de alzada.'}</div><div class="ir-control limit"><strong>${isEn ? 'Does not prove' : 'No acredita'}</strong>${isEn ? 'That the CGPJ failed to dispatch anything, that the High Court lost it, or that the appeal has been admitted, forwarded or upheld.' : 'Que el CGPJ no enviara nada, que el TSJ lo extraviara, o que la alzada haya sido admitida, remitida o estimada.'}</div><div class="ir-control action"><strong>${isEn ? 'Outstanding finite action' : 'Acción finita pendiente'}</strong>${isEn ? 'Reconcile CGPJ dispatch and High Court receipt records; verify full file incorporation, forwarding report, superior reference, ATLANTE preservation/traceability and the reasoned appeal decision.' : 'Conciliar salida CGPJ y recepción TSJ; verificar incorporación íntegra, informe de remisión, referencia superior, preservación/trazabilidad ATLANTE y decisión motivada de la alzada.'}</div></div><div class="ir-links"><a href="${isEn ? '../tsj-canarias-exp-gub-38-2026/' : '../tsj-canarias-exp-gub-38-2026/'}">${isEn ? 'Full Government File record →' : 'Registro completo del expediente →'}</a><a href="${isEn ? '../tsj-canarias-exp-gub-38-2026-appeal-filed/' : '../tsj-canarias-exp-gub-38-2026-alzada-presentada/'}">${isEn ? 'Verified appeal filing →' : 'Presentación verificada de la alzada →'}</a></div></article>`);
    }
  }

  const home = /\/por-derecho\/(es|en)\/?(?:index\.html)?$/.test(path) || /^\/(es|en)\/?(?:index\.html)?$/.test(path);
  if (home) {
    const cgpjCard = document.querySelector('.authority-card[data-search*="unidad de registro y archivo del consejo general del poder judicial"]');
    if (cgpjCard) {
      const state = cgpjCard.querySelector('footer strong');
      if (state) state.textContent = isEn ? 'Appeal 286/2026 in processing; later supplements require file-level reconciliation' : 'Alzada 286/2026 en tramitación; aportaciones posteriores requieren conciliación de expediente';
      const dd = cgpjCard.querySelector('dl div:first-child dd');
      if (dd && !dd.textContent.includes('286/2026')) dd.insertAdjacentHTML('beforeend', isEn ? ' The Appeals Section later identified Appeal 286/2026 and expressly confirmed joinder of the 15 July filing.' : ' La Sección de Recursos identificó después la Alzada 286/2026 y confirmó expresamente la unión del escrito de 15 de julio.');
    }
    const grid = cgpjCard?.parentElement;
    if (grid && !grid.querySelector('[data-tsj-authority-card]')) {
      cgpjCard.insertAdjacentHTML('afterend', `<article class="authority-card" data-tsj-authority-card="true" data-cluster="judicial_protection_and_court_governance" data-effect="appeal" data-search="secretaría de gobierno del tribunal superior de justicia de canarias"><header><span class="authority-rank">TSJ</span><span class="authority-tile" aria-hidden="true">SG</span><div><h4>${isEn ? 'Canary Islands High Court · Government Secretariat' : 'TSJ de Canarias · Secretaría de Gobierno'}</h4><p>${isEn ? 'Court-office / LAJ traceability and hierarchical review' : 'Trazabilidad LAJ/Oficina Judicial y revisión jerárquica'}</p></div></header><dl><div><dt>${isEn ? 'Recorded' : 'Lo que consta'}</dt><dd>${isEn ? 'Government File 38/2026 was archived at first level on 20 August; the hierarchical appeal was filed the same day under REGAGE26e00074355631.' : 'El Exp. Gub. 38/2026 fue archivado en primer nivel el 20 de agosto; la alzada se presentó ese mismo día bajo REGAGE26e00074355631.'}</dd></div><div><dt>${isEn ? 'Does not decide' : 'No decide'}</dt><dd>${isEn ? 'Filing does not establish admission, forwarding or outcome, and the TSJ non-receipt statement does not prove a CGPJ dispatch failure.' : 'La presentación no acredita admisión, remisión o resultado, y la manifestación TSJ de no constancia de recepción no prueba un fallo de envío del CGPJ.'}</dd></div><div><dt>${isEn ? 'Outstanding action' : 'Acción pendiente'}</dt><dd>${isEn ? 'Reconcile CGPJ dispatch/TSJ receipt and verify full incorporation, forwarding, superior reference and reasoned decision.' : 'Conciliar salida CGPJ/recepción TSJ y verificar incorporación, remisión, referencia superior y decisión motivada.'}</dd></div></dl><footer><span>Exp. Gub. 38/2026</span><strong>${isEn ? 'Hierarchical appeal filed' : 'Alzada presentada'}</strong></footer></article>`);
    }
  }

  const updates = /\/(es\/actualizaciones|en\/updates)\/?(?:index\.html)?$/.test(path);
  if (updates) {
    const statusStrong = document.querySelector('.update-status strong');
    if (statusStrong) statusStrong.textContent = isEn ? '20 August 2026' : '20 agosto 2026';
    const firstSection = document.querySelector('.updates-section');
    if (firstSection && !document.querySelector('[data-update-20aug-cgpj-tsj]')) {
      firstSection.insertAdjacentHTML('beforebegin', `<section class="updates-section pd-parity-update" data-update-20aug-cgpj-tsj="true"><div class="shell"><section class="date-group"><h2>20 ${isEn ? 'August' : 'agosto'} 2026 · ${isEn ? 'judicial governance' : 'gobierno judicial'}</h2><div class="update-stream"><article class="material-update institutional"><div class="update-meta"><span class="new">${isEn ? 'New' : 'Nuevo'}</span><span>TSJ Canarias</span><span>${isEn ? 'Hierarchical appeal' : 'Alzada'}</span></div><h3>${isEn ? 'Government File 38/2026: hierarchical appeal filed and registered' : 'Exp. Gub. 38/2026: alzada presentada y registrada'}</h3><p>${isEn ? 'REGAGE registered the 20 August filing as REGAGE26e00074355631. The receipt proves presentation, destination, timing and the exact submitted-file integrity record; forwarding, admission, superior reference and outcome remain pending.' : 'REGAGE registró la presentación de 20 de agosto como REGAGE26e00074355631. El justificante acredita presentación, destino, hora e integridad exacta del archivo aportado; remisión, admisión, referencia superior y resultado siguen pendientes.'}</p><p>${isEn ? 'The same institutional chain also contains a finite CGPJ→TSJ reconciliation question: the Promotor ordered communication to the High Court, while the High Court Government Secretariat stated on 20 August that receipt was not recorded there as of that date. No dispatch failure or loss is inferred.' : 'La misma cadena institucional contiene una cuestión finita de conciliación CGPJ→TSJ: el Promotor ordenó comunicación al TSJ, mientras que la Secretaría de Gobierno manifestó el 20 de agosto que no constaba allí su recepción a esa fecha. No se infiere fallo de envío ni pérdida.'}</p><div class="update-links"><a href="${isEn ? '../tsj-canarias-exp-gub-38-2026-appeal-filed/' : '../tsj-canarias-exp-gub-38-2026-alzada-presentada/'}">${isEn ? 'Verified filing record →' : 'Registro verificado de presentación →'}</a><a href="${isEn ? '../open-message-cgpj/' : '../mensaje-abierto-cgpj/'}">CGPJ →</a></div></article><article class="material-update institutional"><div class="update-meta"><span>${isEn ? 'Professional custodians' : 'Custodios profesionales'}</span><span>PwC · Grant Thornton · RSM</span></div><h3>${isEn ? 'Preservation and reconciliation notices now form part of the public source map' : 'Los avisos de preservación y reconciliación ya forman parte del mapa público de fuentes'}</h3><p>${isEn ? 'PwC, Grant Thornton and RSM have received separate source-controlled updates. Their relevance is custodial and evidential: they may hold conflict, engagement, access, referral, time, billing and file-separation records capable of confirming, limiting or rebutting parts of the reconstruction. No firm is treated as liable merely because of a professional relationship, and no current response period is treated as expired.' : 'PwC, Grant Thornton y RSM han recibido actualizaciones separadas y controladas por fuentes. Su relevancia es custodial y probatoria: pueden conservar registros de conflicto, encargo, acceso, referral, tiempos, facturación y separación de expedientes capaces de confirmar, limitar o refutar partes de la reconstrucción. Ninguna firma se trata como responsable por la mera relación profesional, ni se considera vencido ningún plazo de respuesta actual.'}</p></article></div></section></div></section>`);
    }
  }

  const professional = [
    { re: /\/pwc-canarias-carlos-saavedra-sun-park\//, type: 'pwc' },
    { re: /\/grant-thornton\/2024-04\//, type: 'gt' },
    { re: /\/rsm\/nnr4-1025c2f66\//, type: 'rsm' }
  ].find(x => x.re.test(path));
  if (professional) {
    const hero = document.querySelector('.hero .shell') || document.querySelector('.hero');
    if (hero && !hero.querySelector('[data-professional-20aug-status]')) {
      const copy = professional.type === 'pwc'
        ? (isEn ? '<strong>19–20 August 2026 status.</strong> The institutional escalation and preservation request is now source-controlled, including six finite former-client/confidentiality/conflict/information-governance questions. No later substantive PwC merits response has been located; that absence is not treated as an admission.' : '<strong>Estado 19–20 agosto 2026.</strong> La escalación institucional y la petición de preservación quedan controladas por fuentes, incluidas seis preguntas finitas sobre antiguo cliente, confidencialidad, conflicto y gobierno de información. No se ha localizado una respuesta sustantiva posterior de PwC; esa ausencia no se trata como admisión.')
        : professional.type === 'gt'
        ? (isEn ? '<strong>18–20 August 2026 status.</strong> A supplemental reconciliation notice has been sent concerning the 2020 conflict/confidentiality memory, the later Canary professional/commercial relationship and the San Telmo source as an institutional-memory question. No adverse inference is drawn from the absence of a new substantive response at this stage.' : '<strong>Estado 18–20 agosto 2026.</strong> Se ha remitido una actualización de reconciliación sobre la memoria de conflicto/confidencialidad de 2020, la posterior relación profesional/comercial canaria y la fuente San Telmo como cuestión de memoria institucional. No se extrae inferencia adversa de la ausencia de nueva respuesta sustantiva a esta fecha.')
        : (isEn ? '<strong>19–20 August 2026 status.</strong> The San Telmo source has been formally added to ethics review NNR4-1025C2F66. RSM’s communicated September 2026 conclusion window remains operative; RSM is not treated as overdue and no current silence is treated as substantive refusal.' : '<strong>Estado 19–20 agosto 2026.</strong> La fuente San Telmo ha sido incorporada formalmente a la revisión ética NNR4-1025C2F66. La ventana comunicada por RSM para conclusiones en septiembre de 2026 sigue vigente; RSM no se trata como fuera de plazo ni el silencio actual como negativa sustantiva.');
      hero.insertAdjacentHTML('beforeend', `<div class="pd-parity-note" data-professional-20aug-status="true">${copy}</div>`);
    }
  }
})();
