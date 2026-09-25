(() => {
  if (window.__pdTransparencyFederRoutingCrosslinks20260826) return;
  window.__pdTransparencyFederRoutingCrosslinks20260826 = true;

  const current = document.currentScript;
  const assetsBase = current && current.src
    ? new URL('.', current.src)
    : new URL('/por-derecho/assets/', window.location.origin);
  const siteBase = new URL('../', assetsBase);

  const normalise = value => {
    let path = value.replace(/\/index\.html$/, '/');
    if (!path.endsWith('/')) path += '/';
    return path;
  };

  const path = normalise(window.location.pathname);
  const isEnglish = (document.documentElement.lang || '').toLowerCase().startsWith('en');

  const canonicalEnglish = new URL(
    'en/government-canary-islands-transparency-feder-routing-16-2026-0825121919/',
    siteBase
  );
  const canonicalSpanish = new URL(
    'es/gobierno-canarias-transparencia-feder-remision-16-2026-0825121919/',
    siteBase
  );
  const viewer = new URL(
    'evidence/2026-08-26-gobierno-canarias-transparency-feder-sun-park-mynd/document.html',
    siteBase
  );

  const canonicalRoutes = new Set([
    '/en/government-canary-islands-transparency-feder-routing-16-2026-0825121919/',
    '/es/gobierno-canarias-transparencia-feder-remision-16-2026-0825121919/'
  ]);

  const contextRoutes = new Set([
    '/en/public-authority-unitary-case-reconstruction/',
    '/es/reconstruccion-unitaria-autoridades-publicas/',
    '/en/institutionalisation-chain-ric-eu-incentives/',
    '/es/cadena-instrumentalizacion-ric-fondos-incentivos/',
    '/en/regional-incentives-gc836-p06/',
    '/es/incentivos-regionales-gc836-p06/',
    '/en/snca-eu-funds-traceability/',
    '/es/snca-fondos-europeos-trazabilidad/',
    '/en/sun-park-material-control-chronology/',
    '/es/cronologia-control-material-sun-park/',
    '/en/reverse-engineering-360-sun-park-chain/',
    '/es/ingenieria-inversa-360-cadena-sun-park/',
    '/en/hosteltur-sun-park-mynd-yaiza/',
    '/es/hosteltur-sun-park-mynd-yaiza/',
    '/en/la-voz-lanzarote-sun-park-mynd-yaiza/',
    '/es/la-voz-lanzarote-sun-park-mynd-yaiza/'
  ]);

  const matches = routes => [...routes].some(route => path.endsWith(route));

  const correctCanonicalMetadata = () => {
    if (!matches(canonicalRoutes)) return;
    const canonical = document.querySelector('link[rel="canonical"]');
    if (canonical) canonical.href = isEnglish ? canonicalEnglish.href : canonicalSpanish.href;
    document.querySelectorAll('link[rel="alternate"][hreflang]').forEach(link => {
      const language = (link.getAttribute('hreflang') || '').toLowerCase();
      if (language === 'en') link.href = canonicalEnglish.href;
      else if (language === 'es' || language === 'x-default') link.href = canonicalSpanish.href;
    });
  };

  const inject = () => {
    correctCanonicalMetadata();
    if (!matches(contextRoutes) || document.querySelector('[data-pd-transparency-feder-routing]')) return;

    const style = document.createElement('style');
    style.textContent = `
      .pd-feder-routing-development{padding:1.2rem 0;background:linear-gradient(135deg,#edf3ee 0%,#f7f4ed 100%);border-top:1px solid rgba(19,37,45,.13);border-bottom:1px solid rgba(19,37,45,.13)}
      .pd-feder-routing-development__card{max-width:1080px;margin:0 auto;background:#fff;border:1px solid rgba(19,37,45,.17);border-left:6px solid #526b59;border-radius:18px;padding:1.15rem 1.25rem;box-shadow:0 12px 30px rgba(19,37,45,.08)}
      .pd-feder-routing-development__eyebrow{margin:0 0 .45rem;font-size:.76rem;line-height:1.35;letter-spacing:.075em;text-transform:uppercase;font-weight:900;color:#526b59}
      .pd-feder-routing-development h2{margin:.1rem 0 .65rem;font-size:clamp(1.25rem,2.2vw,1.8rem)}
      .pd-feder-routing-development p{line-height:1.62}
      .pd-feder-routing-development__limit{margin:.8rem 0 0;padding:.72rem .85rem;border-radius:12px;background:#f3efe4;border-left:4px solid #8c6b2f;font-size:.94rem}
      .pd-feder-routing-development__actions{display:flex;gap:.55rem;flex-wrap:wrap;margin-top:.9rem}
      .pd-feder-routing-development__actions a{display:inline-block;padding:.58rem .82rem;border-radius:999px;background:#13252d;color:#fff;text-decoration:none;font-weight:850}
      .pd-feder-routing-development__actions a.secondary{background:#fff;color:#13252d;border:1px solid #13252d}
      @media(max-width:720px){.pd-feder-routing-development__card{border-radius:0;border-left-width:5px}.pd-feder-routing-development{padding:.8rem 0}}
    `;
    document.head.appendChild(style);

    const section = document.createElement('section');
    section.className = 'pd-feder-routing-development';
    section.dataset.pdTransparencyFederRouting = '20260826';
    section.setAttribute('aria-labelledby', 'pd-feder-routing-development-title');

    const title = isEnglish
      ? 'Administrative routing is now documented for the Sun Park / MYND Yaiza FEDER inquiry.'
      : 'Ya está documentada la remisión administrativa de la consulta FEDER sobre Sun Park / MYND Yaiza.';
    const body = isEnglish
      ? 'On 26 August 2026, the Government of the Canary Islands described transparency file 16/2026-0825121919 as concerning the FEDER operation publicised at Hotel Sun Park, subsequently marketed as MYND Yaiza, and routed the request to the Directorate-General for Economic Promotion and Diversification. This links the official notice to the ownership, control, financing, Regional Incentives, public-support and later-operation chronology examined on this page.'
      : 'El 26 de agosto de 2026, el Gobierno de Canarias describió el expediente de transparencia 16/2026-0825121919 como relativo a la operación FEDER publicitada en Hotel Sun Park, posteriormente comercializado como MYND Yaiza, y remitió la solicitud a la Dirección General de Promoción y Diversificación Económica. La notificación queda así enlazada con la cronología de propiedad, control, financiación, Incentivos Regionales, apoyo público y explotación posterior examinada en esta página.';
    const limit = isEnglish
      ? 'Evidential limit: the notice records the Administration’s description and routing of the request. It does not, by itself, establish an award, beneficiary, eligible expenditure, amount, payment, compliance or irregularity.'
      : 'Límite probatorio: la notificación acredita la descripción y la remisión administrativa de la solicitud. Por sí sola no acredita concesión, beneficiario, gasto elegible, importe, pago, cumplimiento ni irregularidad.';

    section.innerHTML = `
      <div class="shell">
        <article class="pd-feder-routing-development__card">
          <p class="pd-feder-routing-development__eyebrow">${isEnglish ? 'Official development · 26 August 2026' : 'Novedad oficial · 26 de agosto de 2026'}</p>
          <h2 id="pd-feder-routing-development-title">${title}</h2>
          <p>${body}</p>
          <p class="pd-feder-routing-development__limit"><strong>${isEnglish ? 'Source boundary.' : 'Frontera de la fuente.'}</strong> ${limit}</p>
          <div class="pd-feder-routing-development__actions">
            <a href="${isEnglish ? canonicalEnglish.href : canonicalSpanish.href}">${isEnglish ? 'Read the official-notice digest' : 'Leer la digestión de la notificación oficial'} →</a>
            <a class="secondary" href="${viewer.href}">${isEnglish ? 'Open the redacted source viewer' : 'Abrir el visor de la fuente redactada'} →</a>
          </div>
        </article>
      </div>`;

    const main = document.querySelector('main');
    if (!main) return;
    const firstSection = main.querySelector(':scope > section:first-of-type');
    if (firstSection) firstSection.insertAdjacentElement('afterend', section);
    else main.prepend(section);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inject, {once:true});
  } else {
    inject();
  }
})();
