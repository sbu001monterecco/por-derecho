(() => {
  'use strict';
  const path = window.location.pathname.replace(/\/+$/, '');
  if (document.querySelector('[data-cuatrecasas-step4-publication="20260902"]')) return;

  const isEs = /\/es(?:\/|$)/.test(path);
  const isHome = /\/(?:por-derecho\/)?(?:es|en)?$/.test(path) || path.endsWith('/por-derecho');
  const eligible = isHome || [
    'cuatrecasas-sun-park',
    'cuatrecasas-mandate-ric-continuity',
    'cuatrecasas-mandato-continuidad-ric',
    'cuatrecasas-dp748-civil-action',
    'cuatrecasas-dp748-accion-civil',
    'reverse-engineering-360-sun-park-chain',
    'ingenieria-inversa-360-cadena-sun-park',
    'unitary-record',
    'registro-unitario'
  ].some(slug => path.includes('/' + slug));
  if (!eligible) return;

  const page = isEs
    ? '/por-derecho/es/cuatrecasas-mandato-continuidad-ric/#inversion-mandato'
    : '/por-derecho/en/cuatrecasas-sun-park/#why-step4';
  const bridge = isEs
    ? '/por-derecho/es/cuatrecasas-mandato-continuidad-ric/'
    : '/por-derecho/en/cuatrecasas-mandate-ric-continuity/';
  const record = '/por-derecho/evidence/cuatrecasas/2026-09-02-linkedin-why-step4-publication.json';

  const copy = isEs ? {
    eyebrow: 'PUBLICACIÓN · LINKEDIN · 2 SEP 2026',
    title: '“Why go straight to Step 4?” ya es un nodo público del expediente',
    body: 'La síntesis pública conecta mandato, instrumentos de honorarios, ejecución frente a Matkator y el efecto económico indirecto sobre Aweswell. El post no añade peso probatorio a los hechos subyacentes: registra una comunicación pública basada en el expediente controlado.',
    status: 'Publicación comunicada como realizada; la URL canónica de LinkedIn aún no ha sido capturada en el repositorio.',
    open: 'Abrir análisis Step 4 →',
    bridge: 'Abrir puente unitario →',
    record: 'Registro de publicación →'
  } : {
    eyebrow: 'PUBLICATION · LINKEDIN · 2 SEP 2026',
    title: '“Why go straight to Step 4?” is now a public-event node',
    body: 'The public synthesis connects the mandate, fee instruments, enforcement against Matkator and the indirect economic effect on Aweswell. The post does not add evidential weight to the underlying facts: it records a public communication derived from the controlled record.',
    status: 'Publication reported as posted; the canonical LinkedIn URL has not yet been captured in the repository.',
    open: 'Open Step 4 analysis →',
    bridge: 'Open unitary bridge →',
    record: 'Publication record →'
  };

  const section = document.createElement('section');
  section.className = 'section';
  section.setAttribute('data-cuatrecasas-step4-publication', '20260902');
  section.innerHTML = `<div class="shell" style="max-width:1160px"><div style="border:1px solid #d7dddd;border-left:7px solid #80621d;background:#fff;border-radius:18px;padding:1rem 1.15rem;box-shadow:0 12px 28px rgba(16,39,47,.08)"><p style="margin:0 0 .3rem;color:#80621d;font-size:.75rem;font-weight:900;letter-spacing:.055em;text-transform:uppercase">${copy.eyebrow}</p><h2 style="margin:.2rem 0 .55rem;color:#13252d">${copy.title}</h2><p style="margin:.35rem 0;line-height:1.55">${copy.body}</p><p style="margin:.55rem 0;font-size:.86rem;color:#5e686a"><strong>${copy.status}</strong></p><p style="margin:.8rem 0 0"><a href="${page}" style="display:inline-block;background:#13252d;color:#fff;text-decoration:none;font-weight:800;border-radius:999px;padding:.55rem .8rem">${copy.open}</a> <a href="${bridge}" style="display:inline-block;margin-left:.55rem;font-weight:800">${copy.bridge}</a> <a href="${record}" style="display:inline-block;margin-left:.55rem;font-weight:800">${copy.record}</a></p></div></div>`;

  const main = document.querySelector('main');
  if (!main) return;
  const insert = () => {
    const step4 = main.querySelector('[data-cuatrecasas-why-step4="20260902"]');
    if (step4 && !step4.id) step4.id = 'why-step4';
    const mandate = main.querySelector('#mandate-inversion, #inversion-mandato, [data-cuatrecasas-mandate-ric-inbound="20260902"]');
    const anchor = step4 || mandate || main.querySelector('section');
    if (anchor && anchor.nextSibling) main.insertBefore(section, anchor.nextSibling);
    else main.appendChild(section);
  };
  if (path.includes('/cuatrecasas-sun-park')) window.setTimeout(insert, 120);
  else insert();
})();
