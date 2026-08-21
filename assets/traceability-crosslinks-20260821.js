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
