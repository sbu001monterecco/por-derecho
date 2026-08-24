(() => {
  const normalize = value => {
    let path = value.replace(/\/index\.html$/, '/');
    if (!path.endsWith('/')) path += '/';
    return path;
  };
  const path = normalize(location.pathname);
  const central = ['/es/ricpe-acciones-pendientes-ahora/','/en/ricpe-outstanding-actions-now/'];
  if (central.some(route => path.endsWith(route))) return;

  const generalRoutes = [
    '/es/','/en/','/es/actualizaciones/','/en/updates/','/es/registros-institucionales/','/en/institutional-records/',
    '/es/ric-private-equity-sun-park/','/en/ric-private-equity-sun-park/',
    '/es/ricpe-idoneidad-aeat-preguntas/','/en/ricpe-idoneidad-aeat-public-questions/',
    '/es/ricpe-idoneidad-series-f-g/','/en/ricpe-idoneidad-series-f-g/',
    '/es/incentivos-regionales-gc836-p06/','/en/regional-incentives-gc836-p06/',
    '/es/cadena-instrumentalizacion-ric-fondos-incentivos/','/en/institutionalisation-chain-ric-eu-incentives/',
    '/es/mismo-hotel-multiples-vidas-financieras/','/en/same-hotel-multiple-financial-lives/',
    '/es/cnmv-ricpe-verificacion/','/en/cnmv-ricpe-verification/',
    '/es/snca-fondos-europeos-trazabilidad/','/en/snca-european-funds-traceability/'
  ];
  const professionalRoutes = [
    '/es/pwc-canarias-carlos-saavedra-sun-park/','/en/pwc-canarias-carlos-saavedra-sun-park/',
    '/es/grant-thornton/cuyas-canarias/','/en/grant-thornton/cuyas-canarias/',
    '/es/grant-thornton/2024-04/','/en/grant-thornton/2024-04/',
    '/es/rsm/nnr4-1025c2f66/','/en/rsm/nnr4-1025c2f66/',
    '/es/san-telmo-ricpe-sun-park/','/en/san-telmo-ricpe-sun-park/'
  ];
  const isGeneral = generalRoutes.some(route => path.endsWith(route));
  const isProfessional = professionalRoutes.some(route => path.endsWith(route));
  if (!isGeneral && !isProfessional) return;

  const isEnglish = document.documentElement.lang === 'en' || path.includes('/en/');
  const prefix = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const target = isEnglish ? `${prefix}en/ricpe-outstanding-actions-now/` : `${prefix}es/ricpe-acciones-pendientes-ahora/`;

  const style = document.createElement('style');
  style.dataset.ricpeSaipBatchStyle = '20260824';
  style.textContent = `
    [data-ricpe-saip-batch]{--b-green:#176343;--b-amber:#9a6418;--b-red:#8c1d18;--b-blue:#254d68}
    .ricpe-saip-batch{background:#eef7f2;border-top:6px solid var(--b-green);border-bottom:1px solid rgba(19,37,45,.14);padding:1.35rem 0}
    .ricpe-saip-batch__grid{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(250px,.5fr);gap:1rem;align-items:center}
    .ricpe-saip-batch h2{margin:.2rem 0 .55rem;font-size:clamp(1.55rem,3vw,2.35rem);line-height:1.05}
    .ricpe-saip-batch p{margin:.35rem 0;line-height:1.5}
    .ricpe-saip-batch__kicker{font-size:.72rem;text-transform:uppercase;letter-spacing:.08em;font-weight:950;color:var(--b-green)}
    .ricpe-saip-batch__stats{display:grid;grid-template-columns:repeat(2,1fr);gap:.45rem}
    .ricpe-saip-batch__stats span{display:block;background:#fff;border:1px solid rgba(19,37,45,.14);border-radius:10px;padding:.6rem;font-weight:850}
    .ricpe-saip-batch__stats b{display:block;font-size:1.4rem;color:var(--b-green)}
    .ricpe-saip-batch__status{display:flex;flex-wrap:wrap;gap:.4rem;margin:.65rem 0}
    .ricpe-saip-batch__status i{font-style:normal;border-radius:999px;padding:.25rem .55rem;font-size:.67rem;font-weight:900}
    .ricpe-saip-batch__status .g{background:#dcefe6;color:var(--b-green)}.ricpe-saip-batch__status .a{background:#f5e8cb;color:#754707}.ricpe-saip-batch__status .r{background:#f4ddda;color:var(--b-red)}
    .ricpe-saip-batch__link{display:inline-block;background:#13252d;color:#fff;text-decoration:none;border-radius:999px;padding:.65rem .85rem;font-weight:900}
    .ricpe-saip-professional-note{border-left:6px solid var(--b-blue);background:#eef5f8;padding:1rem 1.1rem;border-radius:12px}
    @media(max-width:780px){.ricpe-saip-batch__grid{grid-template-columns:1fr}}
  `;
  document.head.append(style);

  const section = document.createElement('section');
  section.className = 'ricpe-saip-batch';
  section.dataset.ricpeSaipBatch = '20260824';
  section.setAttribute('aria-label', isEnglish ? 'Eight public-information access routes filed' : 'Ocho vías de acceso a información pública registradas');

  const title = isEnglish ? 'Eight access routes are now formally filed.' : 'Ocho vías de acceso ya están formalmente registradas.';
  const lead = isEnglish
    ? 'Five new access requests and three supplements were filed on 24 August 2026. Applicant action is complete; internal routing, file allocation, document production and reasoned responses remain pending.'
    : 'Cinco nuevas SAIP y tres aportaciones fueron registradas el 24 de agosto de 2026. La actuación del solicitante está completa; quedan pendientes la ruta interna, asignación de expediente, producción documental y respuesta motivada.';
  const boundary = isEnglish
    ? 'Registration proves presentation and attachment integrity; it does not prove admission, allocation, a supervisory investigation or a merits decision.'
    : 'El registro acredita presentación e integridad del anexo; no acredita admisión, asignación, investigación supervisora ni decisión de fondo.';
  const professional = isEnglish
    ? 'Fairness boundary: PwC, Grant Thornton/Cuyás and RSM/San Telmo names, the visual exhibits and webinar were supplied solely as search and document-location aids—not as official findings the authorities were asked to adopt.'
    : 'Frontera de equidad: los nombres PwC, Grant Thornton/Cuyás y RSM/San Telmo, los anexos visuales y el webinar se aportaron únicamente como ayudas de búsqueda y localización documental, no como conclusiones oficiales que se pidiera adoptar a las autoridades.';

  section.innerHTML = `<div class="shell ricpe-saip-batch__grid"><div><p class="ricpe-saip-batch__kicker">${isEnglish ? '24 AUGUST 2026 · 8/8 REGISTERED' : '24 AGOSTO 2026 · 8/8 REGISTRADAS'}</p><h2>${title}</h2><p>${lead}</p><div class="ricpe-saip-batch__status"><i class="g">${isEnglish ? 'FILED' : 'PRESENTADO'}</i><i class="a">${isEnglish ? 'ROUTING / FILE PENDING' : 'RUTA / EXPEDIENTE PENDIENTE'}</i><i class="r">${isEnglish ? 'DOCUMENTARY RESPONSE PENDING' : 'RESPUESTA DOCUMENTAL PENDIENTE'}</i></div><p><strong>${isEnglish ? 'Evidence boundary:' : 'Límite probatorio:'}</strong> ${boundary}</p>${isProfessional ? `<p class="ricpe-saip-professional-note">${professional}</p>` : ''}<a class="ricpe-saip-batch__link" href="${target}">${isEnglish ? 'Open the coordinated register →' : 'Abrir el registro coordinado →'}</a></div><div class="ricpe-saip-batch__stats"><span><b>8</b>${isEnglish ? 'filings' : 'presentaciones'}</span><span><b>5</b>${isEnglish ? 'new requests' : 'nuevas SAIP'}</span><span><b>3</b>${isEnglish ? 'supplements' : 'aportaciones'}</span><span><b>8</b>${isEnglish ? 'REGAGE receipts' : 'justificantes REGAGE'}</span></div></div>`;

  const main = document.querySelector('main');
  if (!main || document.querySelector('[data-ricpe-saip-batch]')) return;
  const first = main.querySelector(':scope > section:first-of-type');
  if (first) first.insertAdjacentElement('afterend', section);
  else main.prepend(section);
})();
