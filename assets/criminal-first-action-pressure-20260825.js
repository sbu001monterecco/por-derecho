(() => {
  'use strict';
  if (window.__pdCriminalFirstActionPressure20260825) return;
  window.__pdCriminalFirstActionPressure20260825 = true;

  const normalise = value => {
    let path = String(value || '').replace(/\/index\.html$/, '/');
    if (!path.endsWith('/')) path += '/';
    return path;
  };
  const path = normalise(location.pathname);
  const isEnglish = document.documentElement.lang === 'en' || /\/en\//.test(path);
  const prefix = path.includes('/por-derecho/') ? '/por-derecho' : '';
  const route = relative => `${prefix}/${isEnglish ? 'en' : 'es'}/${relative}`;
  const routes = isEnglish ? {
    action: route('unitary-criminal-hypothesis-2011-present/institutional-action/'),
    graph: route('unitary-criminal-hypothesis-2011-present/acosta-matos-convergence/'),
    ids: route('matter-identity-registry/')
  } : {
    action: route('hipotesis-criminal-unitaria-2011-presente/accion-institucional/'),
    graph: route('hipotesis-criminal-unitaria-2011-presente/convergencia-acosta-matos/'),
    ids: route('registro-identidad-materia/')
  };

  const actionSuffixes = [
    '/es/hipotesis-criminal-unitaria-2011-presente/accion-institucional/',
    '/en/unitary-criminal-hypothesis-2011-present/institutional-action/',
    '/es/hipotesis-criminal-unitaria-2011-presente/convergencia-acosta-matos/',
    '/en/unitary-criminal-hypothesis-2011-present/acosta-matos-convergence/'
  ];
  if (actionSuffixes.some(suffix => path.endsWith(suffix))) return;

  const fullHome = /\/(es|en)\/$/.test(path);
  const compactSuffixes = [
    '/es/comunidad-instrumentalizacion/',
    '/en/community-instrumentalisation/',
    '/es/comunidad-instrumentalizacion/actas-2011-2022/',
    '/en/community-instrumentalisation/minutes-2011-2022/',
    '/es/acosta-matos-perimetro/',
    '/en/acosta-matos-perimeter/',
    '/es/francisco-de-borja-rodriguez-batllori-laffitte/',
    '/en/francisco-de-borja-rodriguez-batllori-laffitte/',
    '/es/toma-control-sun-park-7-junio-2018/',
    '/en/sun-park-takeover-7-june-2018/',
    '/es/actores-partes-abogados-representantes/',
    '/en/actors-parties-lawyers-representatives/',
    '/es/hipotesis-criminal-unitaria-2011-presente/',
    '/en/unitary-criminal-hypothesis-2011-present/',
    '/es/hipotesis-criminal-unitaria-2011-presente/atribucion-maxima/',
    '/en/unitary-criminal-hypothesis-2011-present/maximal-attribution/'
  ];
  const compact = compactSuffixes.some(suffix => path.endsWith(suffix));
  if (!fullHome && !compact) return;

  const copy = isEnglish ? {
    kicker: 'PD-SP-ACTION-2011-CONVERGENCE-001 · public action control',
    title: 'Preserve. Disclose. Explain. Investigate. Recover.',
    lead: 'The 2011-to-present convergence case is now translated into 15 immutable actions, including 12 P0 preservation and disclosure packages addressed by actor, entity, institution and proceeding ID.',
    boundary: 'Allegations are not findings. No relationship transfers knowledge or intent. The pressure is documentary: preserve the native record, identify authority, explain verification, test alternatives and quantify claimant-specific recovery.',
    action: 'Open immediate institutional action',
    graph: 'Explore the 37 graded bridges',
    ids: 'Resolve every actor by ID'
  } : {
    kicker: 'PD-SP-ACTION-2011-CONVERGENCE-001 · control público de acción',
    title: 'Preservar. Entregar. Explicar. Investigar. Recuperar.',
    lead: 'El caso de convergencia 2011–presente ya está traducido a 15 acciones inmutables, incluidos 12 paquetes P0 de preservación y entrega dirigidos por ID de actor, entidad, institución y procedimiento.',
    boundary: 'Las alegaciones no son conclusiones. Ninguna relación transmite conocimiento o dolo. La presión es documental: preservar el registro nativo, identificar autoridad, explicar la verificación, contrastar alternativas y cuantificar la recuperación por perjudicado.',
    action: 'Abrir acción institucional inmediata',
    graph: 'Explorar los 37 puentes graduados',
    ids: 'Resolver cada actor por ID'
  };

  const style = document.createElement('style');
  style.textContent = `
    .pd-action-pressure{background:radial-gradient(circle at 86% 20%,rgba(205,154,72,.26),transparent 28%),linear-gradient(135deg,#10262e,#18323b 58%,#50282c);color:#fff;padding:clamp(2.2rem,5vw,3.6rem) 0;border-top:1px solid rgba(255,255,255,.14);border-bottom:1px solid rgba(10,28,35,.28)}
    .pd-action-pressure__inner{max-width:1180px;margin:0 auto;padding:0 clamp(1rem,4vw,2rem)}
    .pd-action-pressure__kicker{margin:0 0 .55rem;font-size:.72rem;font-weight:900;letter-spacing:.075em;text-transform:uppercase;color:#efc777}
    .pd-action-pressure h2{margin:0;max-width:19ch;font-size:clamp(1.8rem,4vw,3.45rem);line-height:1.02;letter-spacing:-.03em;color:#fff}
    .pd-action-pressure__lead{max-width:77rem;margin:.9rem 0 0;font-size:clamp(1rem,1.8vw,1.16rem);line-height:1.58;color:#f4f7f6}
    .pd-action-pressure__boundary{max-width:78rem;margin:1rem 0 0;padding:.8rem .95rem;border:1px solid rgba(255,255,255,.28);border-radius:12px;background:rgba(255,255,255,.075);font-size:.88rem;line-height:1.5;color:#eef3f1}
    .pd-action-pressure__links{display:flex;flex-wrap:wrap;gap:.62rem;margin-top:1.1rem}
    .pd-action-pressure__links a{display:inline-flex;align-items:center;justify-content:center;border-radius:999px;padding:.68rem .9rem;text-decoration:none;font-weight:900;font-size:.82rem}
    .pd-action-pressure__links a:first-child{background:#fff;color:#13252d}
    .pd-action-pressure__links a:not(:first-child){border:1px solid rgba(255,255,255,.46);color:#fff;background:transparent}
    .pd-action-pressure--compact{padding:1.45rem 0}
    .pd-action-pressure--compact .pd-action-pressure__inner{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(280px,.6fr);gap:1rem;align-items:center}
    .pd-action-pressure--compact h2{font-size:clamp(1.45rem,2.8vw,2.25rem);max-width:none}
    .pd-action-pressure--compact .pd-action-pressure__lead{font-size:.94rem;margin:.55rem 0 0}
    .pd-action-pressure--compact .pd-action-pressure__boundary{display:none}
    .pd-action-pressure--compact .pd-action-pressure__links{justify-content:flex-end;margin:0}
    @media(max-width:760px){.pd-action-pressure--compact .pd-action-pressure__inner{grid-template-columns:1fr}.pd-action-pressure--compact .pd-action-pressure__links{justify-content:flex-start}}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.className = `pd-action-pressure${compact && !fullHome ? ' pd-action-pressure--compact' : ''}`;
  section.dataset.criminalFirstActionPressure = '20260825';
  section.setAttribute('aria-label', copy.title);
  const boundary = fullHome ? `<p class="pd-action-pressure__boundary"><strong>${isEnglish ? 'Evidence boundary.' : 'Límite probatorio.'}</strong> ${copy.boundary}</p>` : '';
  section.innerHTML = `<div class="pd-action-pressure__inner"><div><p class="pd-action-pressure__kicker">${copy.kicker}</p><h2>${copy.title}</h2><p class="pd-action-pressure__lead">${copy.lead}</p>${boundary}</div><nav class="pd-action-pressure__links" aria-label="${isEnglish ? 'Criminal-first action links' : 'Enlaces de acción criminal-first'}"><a href="${routes.action}">${copy.action}</a><a href="${routes.graph}">${copy.graph}</a><a href="${routes.ids}">${copy.ids}</a></nav></div>`;

  const mount = () => {
    if (document.querySelector('[data-criminal-first-action-pressure]')) return;
    const main = document.querySelector('main');
    if (!main) return;
    if (fullHome) {
      const lockedFirstRead = main.querySelector(':scope > section[data-pd-five-ac]');
      if (lockedFirstRead) {
        lockedFirstRead.insertAdjacentElement('afterend', section);
        return;
      }
    }
    const opening = main.querySelector(':scope > section:first-of-type');
    if (opening) opening.insertAdjacentElement('afterend', section);
    else main.prepend(section);
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount, {once:true});
  else mount();
})();