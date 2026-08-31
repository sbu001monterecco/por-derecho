(() => {
  const normalise = value => {
    let path = value.replace(/\/index\.html$/, '/');
    if (!path.endsWith('/')) path += '/';
    return path;
  };
  const path = normalise(location.pathname);
  const isEn = document.documentElement.lang === 'en';
  const base = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const target = isEn
    ? `${base}en/ricpe-hnt-gc836-traceability/`
    : `${base}es/ricpe-hnt-gc836-trazabilidad/`;

  const relevant = [
    '/es/', '/en/',
    '/es/ric-private-equity-sun-park/', '/en/ric-private-equity-sun-park/',
    '/es/acosta-matos-perimetro/', '/en/acosta-matos-perimeter/',
    '/es/arquitectura-nodo-documental-jdam/', '/en/architecture-documentary-node-jdam/',
    '/es/recuperacion-activos-intervencion-decomiso/', '/en/asset-recovery-intervention-confiscation/',
    '/es/cadena-instrumentalizacion-ric-fondos-incentivos/', '/en/institutionalisation-chain-ric-eu-incentives/',
    '/es/mismo-hotel-multiples-vidas-financieras/', '/en/same-hotel-multiple-financial-lives/'
  ];
  if (!relevant.some(route => path.endsWith(route)) || document.querySelector('[data-traceability-crosslink-20260821]')) return;

  const main = document.querySelector('main');
  if (!main) return;
  const section = document.createElement('section');
  section.className = 'section alt';
  section.dataset.traceabilityCrosslink20260821 = 'true';
  section.innerHTML = `<div class="shell"><div class="section-head"><div><p class="kicker">${isEn ? 'Funding · restructuring · public-support traceability' : 'Financiación · reestructuración · trazabilidad de apoyo público'}</p><h2>${isEn ? 'Follow the structure and the money in one chronology.' : 'Siga la estructura y los fondos en una sola cronología.'}</h2></div><p>${isEn ? 'A source-controlled route links the RICPE investor/materialisation phase, the 2022 Hotel New Trend segregation, MYND Yaiza and the finite evidence questions around GC/836/P06. It does not presume double funding, EU funding, fraud or illegality.' : 'Una ruta source-controlled conecta la fase inversora/materialización RICPE, la segregación de Hotel New Trend de 2022, MYND Yaiza y las preguntas probatorias finitas de GC/836/P06. No presume doble financiación, financiación UE, fraude ni ilicitud.'}</p></div><div class="actions"><a class="button" href="${target}">${isEn ? 'Open the traceability chronology' : 'Abrir la cronología de trazabilidad'}</a></div></div>`;

  const priority = document.querySelector('.priority-band');
  if (priority && (path.endsWith('/es/') || path.endsWith('/en/'))) priority.insertAdjacentElement('afterend', section);
  else main.append(section);
})();

/* CGPJ-RECURSOS-RECEIPT-CORRECTION-20260821 */
(() => {
  const path = location.pathname.toLowerCase();
  if (!path.includes('cgpj') || document.querySelector('[data-cgpj-recursos-receipt-20260821]')) return;
  const main = document.querySelector('main');
  if (!main) return;
  const isEn = document.documentElement.lang === 'en';
  const note = document.createElement('section');
  note.className = 'section';
  note.dataset.cgpjRecursosReceipt20260821 = 'true';
  note.innerHTML = `<div class="shell"><div class="status" style="border-left:5px solid #245c49;background:#f0f7f3;padding:1rem 1.15rem;border-radius:13px"><strong>${isEn ? 'Source-status correction · 21 August 2026.' : 'Corrección de estado de fuente · 21 de agosto de 2026.'}</strong> ${isEn ? 'The CGPJ Appeals service has now confirmed by email that the documentation sent on 28 July, entered in the electronic registry on 29 July with five attachments, was received and incorporated for the relevant handling. This confirmation is limited to that identified submission; it does not by itself establish examination of every later communication or any merits outcome.' : 'El servicio de Recursos del CGPJ ha confirmado ya por correo electrónico que la documentación remitida el 28 de julio, con entrada en el registro electrónico el 29 de julio y cinco archivos adjuntos, fue recibida e incorporada para la gestión correspondiente. La confirmación se limita a esa presentación identificada; no acredita por sí sola el examen de todas las comunicaciones posteriores ni ningún resultado sobre el fondo.'}</div></div>`;
  const first = main.querySelector('section');
  if (first) first.insertAdjacentElement('afterend', note); else main.prepend(note);
})();

/* ELECONOMISTA-JUDGMENT-SCOPE-CLARIFICATION-20260821 */
(() => {
  const path = location.pathname.replace(/\/index\.html$/, '/').toLowerCase();
  const isEs = path.endsWith('/es/eleconomista-javier-romera-enero2025/');
  const isEn = path.endsWith('/en/eleconomista-javier-romera-january2025/');
  if ((!isEs && !isEn) || document.querySelector('#eleconomista-source-status-clarification-20260821')) return;

  const hero = document.querySelector('.mhero .shell');
  if (!hero) return;

  const box = document.createElement('aside');
  box.id = 'eleconomista-source-status-clarification-20260821';
  box.setAttribute('aria-label', isEn ? 'Documentary clarification on Judgment 163/2023' : 'Clarificación documental sobre la Sentencia 163/2023');
  box.style.cssText = 'margin:1.25rem 0 0;padding:1.05rem 1.15rem;border:1px solid rgba(255,255,255,.28);border-left:6px solid #f0c666;border-radius:14px;background:rgba(255,255,255,.96);color:#172632;box-shadow:0 12px 34px rgba(0,0,0,.16);';

  if (isEn) {
    box.innerHTML = `
      <p style="margin:0 0 .55rem;font-size:.76rem;font-weight:900;letter-spacing:.08em;text-transform:uppercase;color:#7b171d">Documentary clarification · what the judgment did — and did not — decide</p>
      <div style="display:flex;flex-wrap:wrap;gap:.4rem;margin:0 0 .75rem">
        <span class="tag">FIRST INSTANCE</span><span class="tag">APPEALED</span><span class="tag">NOT FINAL</span><span class="tag">LPB ≠ SUN PARK</span><span class="tag">MEETING POINT UNDECIDED</span>
      </div>
      <p style="margin:.35rem 0"><strong>Judgment 163/2023 was a materially adverse first-instance insolvency-classification judgment concerning Luchy Playa Blanca, S.L. (Concurso 36/2012), not a judgment about “Sun Park” as a whole.</strong> By 20 January 2025 it had already been appealed and was not final; the judgment itself makes the stated disqualification run from finality.</p>
      <p style="margin:.65rem 0"><strong>It did not decide the question elEconomista was verifying:</strong> whether Meeting Point/FTI had presented or commercialised Club Sei/Sun Park, under what authority, over which units, or with what economic flows.</p>
      <p style="margin:.65rem 0;padding:.7rem .8rem;border-left:4px solid #315c7b;background:#f5f8fa"><strong>The document that stopped publication did not answer the factual question the newsroom had been investigating.</strong></p>
      <p style="margin:.65rem 0 0;font-size:.94rem">The preserved independent commercial evidence — Meeting Point Hotels’ corporate brochure and the sonnenklar.TV offer dated 27/01/2020 — places Club Sei Lanzarote at Calle Janubio 3, the Sun Park address, within the FTI/Meeting Point commercial ecosystem. <strong>This establishes public presentation/distribution;</strong> it does not yet establish the contract, exact inventory, consummated bookings, receipts, or the lawfulness of the commercialisation.</p>`;
  } else {
    box.innerHTML = `
      <p style="margin:0 0 .55rem;font-size:.76rem;font-weight:900;letter-spacing:.08em;text-transform:uppercase;color:#7b171d">Clarificación documental · qué decidía — y qué no decidía — la sentencia</p>
      <div style="display:flex;flex-wrap:wrap;gap:.4rem;margin:0 0 .75rem">
        <span class="tag">PRIMERA INSTANCIA</span><span class="tag">RECURRIDA</span><span class="tag">NO FIRME</span><span class="tag">LPB ≠ SUN PARK</span><span class="tag">MEETING POINT NO RESUELTO</span>
      </div>
      <p style="margin:.35rem 0"><strong>La Sentencia 163/2023 era una resolución de primera instancia materialmente adversa sobre la calificación del concurso de Luchy Playa Blanca, S.L. (Concurso 36/2012), no una resolución sobre «Sun Park» en su conjunto.</strong> El 20 de enero de 2025 ya estaba recurrida y no era firme; la propia sentencia hace operar la inhabilitación desde su firmeza.</p>
      <p style="margin:.65rem 0"><strong>No resolvió la cuestión que elEconomista estaba contrastando:</strong> si Meeting Point/FTI había presentado o comercializado Club Sei/Sun Park, con qué autoridad, sobre qué unidades o con qué flujos económicos.</p>
      <p style="margin:.65rem 0;padding:.7rem .8rem;border-left:4px solid #315c7b;background:#f5f8fa"><strong>El documento que detuvo la publicación no contestó la pregunta factual que la redacción venía investigando.</strong></p>
      <p style="margin:.65rem 0 0;font-size:.94rem">La evidencia comercial independiente preservada —el folleto corporativo de Meeting Point Hotels y la oferta de sonnenklar.TV del 27/01/2020— sitúa Club Sei Lanzarote en Calle Janubio 3, la dirección de Sun Park, dentro del ecosistema comercial FTI/Meeting Point. <strong>Esto acredita presentación/distribución pública;</strong> no acredita todavía el contrato, el inventario exacto, reservas consumadas, cobros ni la licitud de la comercialización.</p>`;
  }

  const lead = hero.querySelector('.lead');
  if (lead) lead.insertAdjacentElement('afterend', box);
  else hero.append(box);
})();

/* MEETING-POINT-DIRECT-COMMERCIAL-EVIDENCE-PROPAGATION-20260821 */
(() => {
  const normalise = value => {
    let path = value.replace(/\/index\.html$/, '/').toLowerCase();
    if (!path.endsWith('/')) path += '/';
    return path;
  };
  const path = normalise(location.pathname);
  const isEn = document.documentElement.lang === 'en';
  const base = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const lavaEs = path.endsWith('/es/lava-verde-club-sei-meeting-point/');
  const lavaEn = path.endsWith('/en/lava-verde-club-sei-meeting-point/');
  const mp357Es = path.endsWith('/es/cuaderno-juridico/meeting-point-357-2024-trazabilidad-judicial/');
  const mp357En = path.endsWith('/en/legal-notebook/meeting-point-357-2024-judicial-traceability/');
  const takeoverEs = path.endsWith('/es/toma-control-sun-park-7-junio-2018/');
  const takeoverEn = path.endsWith('/en/sun-park-takeover-7-june-2018/');

  if ((lavaEs || lavaEn || mp357Es || mp357En) && !document.querySelector('[data-mp-direct-commercial-source-20260821], [data-mp-direct-commercial-source20260821]')) {
    const panel = document.createElement('aside');
    panel.setAttribute('data-mp-direct-commercial-source-20260821', 'true');
    panel.style.cssText = 'margin:1rem 0 1.4rem;padding:1rem 1.15rem;border-left:5px solid #315c7b;background:#f5f8fa;border-radius:12px;color:#172632;';
    panel.innerHTML = isEn
      ? `<strong>Direct-source upgrade · same location, independent commercial layer.</strong> A preserved Meeting Point Hotels corporate brochure describes <strong>Club Sei Lanzarote</strong> as a 315-room Playa Blanca hotel, while an archived <strong>sonnenklar.TV offer dated 27 January 2020 places Club Sei Lanzarote at Calle Janubio 3</strong>. Historical Sun Park material gives the same Calle Janubio 3 address. Together, these sources establish public presentation/distribution of the Sun Park location within the FTI/Meeting Point commercial ecosystem. They do <strong>not</strong> yet establish the exact contracting legal person, room-by-room authority, completed bookings, receipts, commissions or legality.`
      : `<strong>Refuerzo de fuente directa · misma localización, capa comercial independiente.</strong> Un folleto corporativo preservado de Meeting Point Hotels describe <strong>Club Sei Lanzarote</strong> como hotel de 315 habitaciones en Playa Blanca, mientras una oferta archivada de <strong>sonnenklar.TV de 27 de enero de 2020 sitúa Club Sei Lanzarote en Calle Janubio 3</strong>. El material histórico de Sun Park da la misma dirección, Calle Janubio 3. En conjunto, estas fuentes acreditan presentación/distribución pública de la localización Sun Park dentro del ecosistema comercial FTI/Meeting Point. <strong>No</strong> acreditan todavía la persona jurídica contractual exacta, la autoridad habitación por habitación, reservas consumadas, cobros, comisiones ni la licitud.`;

    let anchor = null;
    if (lavaEs || lavaEn) anchor = document.querySelector('.notebook-hero');
    if (mp357Es || mp357En) anchor = document.querySelector('#sun-park .notebook-intro') || document.querySelector('.notebook-hero');
    if (anchor) {
      if (mp357Es || mp357En) anchor.insertAdjacentElement('afterend', panel);
      else anchor.insertAdjacentElement('afterend', panel);
    }
  }

  if ((mp357Es || mp357En) && !document.querySelector('[data-mp357-custody-boundary-20260821], [data-mp357-custody-boundary20260821]')) {
    const boundary = document.createElement('div');
    boundary.setAttribute('data-mp357-custody-boundary-20260821', 'true');
    boundary.className = 'editorial-rule';
    boundary.innerHTML = isEn
      ? `<strong>357/2024 boundary:</strong> signed Auto 97/2025 fixes the joint three-debtor chronology and Auren appointment. The same-address commercial evidence makes the proceeding a possible records-custody/disclosure node; it does not prove that Sun Park records entered any debtor schedule or Auren workfile, that either judge personally saw them, or that the earlier register attribution reflects anything improper.`
      : `<strong>Límite 357/2024:</strong> el Auto 97/2025 firmado fija la cronología conjunta de tres deudores y el nombramiento de Auren. La evidencia comercial de misma dirección hace del procedimiento un posible nodo de custodia/revelación; no prueba que registros Sun Park entraran en anexos de ningún deudor o en el archivo Auren, que los magistrados los vieran personalmente ni que la atribución registral anterior refleje impropiedad.`;
    const sunPark = document.querySelector('#sun-park .shell');
    if (sunPark) sunPark.append(boundary);
  }

  if ((takeoverEs || takeoverEn) && !document.querySelector('[data-takeover-meeting-point-gateway-20260821], [data-takeover-meeting-point-gateway20260821]')) {
    const gateway = document.createElement('div');
    gateway.setAttribute('data-takeover-meeting-point-gateway-20260821', 'true');
    gateway.style.cssText = 'margin:1.35rem 0;padding:1rem 1.15rem;border:1px solid rgba(20,35,45,.16);border-left:5px solid #315c7b;border-radius:12px;background:#fff;';
    const target = isEn
      ? `${base}en/lava-verde-club-sei-meeting-point/`
      : `${base}es/lava-verde-club-sei-meeting-point/`;
    gateway.innerHTML = isEn
      ? `<p class="kicker" style="margin-top:0">From material control to commercial product</p><h3 style="margin:.2rem 0 .55rem">Follow the downstream chain: Lava Verde → Club Sei → Meeting Point/FTI.</h3><p>Independent preserved commercial sources later place Club Sei Lanzarote at the same Calle Janubio 3 address as Sun Park before the 2022 LPB title threshold. That strengthens the chronology from access/control to project and distribution, while leaving contract, exact inventory, authority, completed bookings and legality open.</p><p><a class="button secondary" href="${target}">Open the commercialisation dossier →</a></p>`
      : `<p class="kicker" style="margin-top:0">Del control material al producto comercial</p><h3 style="margin:.2rem 0 .55rem">Seguir la cadena posterior: Lava Verde → Club Sei → Meeting Point/FTI.</h3><p>Fuentes comerciales independientes preservadas sitúan después Club Sei Lanzarote en la misma dirección Calle Janubio 3 de Sun Park antes del umbral de título LPB de 2022. Esto refuerza la cronología desde acceso/control hacia proyecto y distribución, manteniendo abiertos contrato, inventario exacto, autoridad, reservas consumadas y licitud.</p><p><a class="button secondary" href="${target}">Abrir el dossier de comercialización →</a></p>`;
    const project = document.querySelector('#proyecto-antes-del-titulo .shell, #project-before-title .shell');
    if (project) project.append(gateway);
  }
})();
