(() => {
  'use strict';
  const path = window.location.pathname.replace(/\/+$/, '');
  if (document.querySelector('[data-matkator-asset-rights-inbound="20260902"]')) return;

  const isEs = /\/es(?:\/|$)/.test(path);
  const segments = path.split('/').filter(Boolean);
  const isHome = segments.length === 0
    || (segments.length === 1 && ['por-derecho','es','en'].includes(segments[0]))
    || (segments.length === 2 && segments[0] === 'por-derecho' && ['es','en'].includes(segments[1]));
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

  const href = isEs
    ? '/por-derecho/es/registro-activos-derechos-matkator/'
    : '/por-derecho/en/matkator-asset-rights-register/';
  const json = '/por-derecho/evidence/matkator/2026-09-02-asset-rights-register.json';

  const copy = isEs ? {
    eyebrow: isHome ? 'NUEVO REGISTRO CANÓNICO · MATKATOR' : 'PERÍMETRO PATRIMONIAL · MATKATOR',
    title: isHome ? 'Paso 4 ya tiene un mapa finito de activos y derechos' : 'El “Paso 4” ya no es una abstracción: 8.584, 8.588 y los límites del perímetro Matkator',
    body: 'El registro separa la finca 8.584 —único objeto actual de remate bloqueado en ETJ— de la finca 8.588, históricamente 100% Matkator pero no identificada como subastada actualmente. También clasifica cuentas, créditos, ingresos y derechos procesales como probados, potenciales, desconocidos o excluidos, sin trasladar a Matkator activos de LPB o Aweswell.',
    boundary: 'Cortafuegos: una ejecución frente a Matkator puede reducir indirectamente el valor de la filial para Aweswell; no convierte automáticamente a Aweswell en deudor ejecutado.',
    open: 'Abrir registro de activos y derechos →',
    machine: 'Registro JSON →'
  } : {
    eyebrow: isHome ? 'NEW CANONICAL REGISTER · MATKATOR' : 'PATRIMONIAL PERIMETER · MATKATOR',
    title: isHome ? 'Step 4 now has a finite asset-and-rights map' : '“Step 4” is no longer abstract: 8,584, 8,588 and the limits of Matkator’s perimeter',
    body: 'The register separates finca 8,584 — the only current ETJ remate object source-locked here — from finca 8,588, historically 100% Matkator but not identified as currently auctioned. It also classifies accounts, receivables, income and procedural rights as proved, potential, unknown or excluded, without moving LPB or Aweswell assets into Matkator.',
    boundary: 'Firewall: enforcement against Matkator may indirectly reduce subsidiary value for Aweswell; it does not automatically make Aweswell an executed debtor.',
    open: 'Open asset & rights register →',
    machine: 'Canonical JSON →'
  };

  const section = document.createElement('section');
  section.className = 'section';
  section.setAttribute('data-matkator-asset-rights-inbound','20260902');
  section.innerHTML = `<div class="shell" style="max-width:1160px"><div style="border:1px solid #d8dddd;border-left:7px solid #1d5c4a;background:#fff;border-radius:18px;padding:1rem 1.15rem;box-shadow:0 12px 28px rgba(16,39,47,.08)"><p style="margin:0 0 .3rem;color:#1d5c4a;font-size:.75rem;font-weight:900;letter-spacing:.055em;text-transform:uppercase">${copy.eyebrow}</p><h2 style="margin:.2rem 0 .55rem;color:#13252d">${copy.title}</h2><p style="margin:.35rem 0;line-height:1.55">${copy.body}</p><p style="margin:.55rem 0;font-size:.88rem;color:#5b6467"><strong>${copy.boundary}</strong></p><p style="margin:.8rem 0 0"><a href="${href}" style="display:inline-block;background:#13252d;color:#fff;text-decoration:none;font-weight:800;border-radius:999px;padding:.58rem .85rem">${copy.open}</a> <a href="${json}" style="display:inline-block;margin-left:.55rem;font-weight:800">${copy.machine}</a></p></div></div>`;

  const main = document.querySelector('main');
  if (!main) return;
  const insert = () => {
    const step4 = main.querySelector('[data-cuatrecasas-why-step4="20260902"]');
    const mandate = main.querySelector('#mandate-inversion,#inversion-mandato,#aweswell-gateway,[data-cuatrecasas-step4-publication="20260902"]');
    const anchor = step4 || mandate || main.querySelector('section');
    if (anchor && anchor.nextSibling) main.insertBefore(section, anchor.nextSibling);
    else main.appendChild(section);
  };
  if (path.includes('/cuatrecasas-sun-park')) window.setTimeout(insert, 170);
  else insert();
})();
