(() => {
  'use strict';
  const path = window.location.pathname.replace(/\/+$/, '');
  if (!path.includes('/en/cuatrecasas-sun-park')) return;
  if (document.querySelector('[data-cuatrecasas-visual-bridge-atlas="20260902"]')) return;
  const atlas = window.__CUAT_VIS_BRIDGE_ATLAS_20260902__;
  if (!atlas) return;

  const panels = [
    {
      key: 'overview',
      title: 'How the Cuatrecasas pages connect',
      note: 'The whole chain in one view: Aweswell mandate → Sun Park/hotel record → LPB insolvency → fees/Matkator → ETJ → RIC/CNMV/later funding.',
      href: '../cuatrecasas-mandate-ric-continuity/',
      pos: 'left top'
    },
    {
      key: 'step4',
      title: 'What Step 4 can — and cannot — reach',
      note: 'The bridge from the current finca 8,584 remate to Matkator’s wider patrimonial perimeter, while preserving the Aweswell corporate firewall.',
      href: '../matkator-asset-rights-register/',
      pos: 'right top'
    },
    {
      key: 'etj',
      title: 'From former-client mandate to execution against Matkator',
      note: 'The page-to-page bridge between the documented client mandate, fee instruments and ETJ 163/2020 / civil-action analysis.',
      href: '../cuatrecasas-dp748-civil-action/',
      pos: 'left bottom'
    },
    {
      key: 'ric',
      title: 'Mandate continuity into RIC / CNMV warnings',
      note: 'The chronology bridge from the pre-existing Sun Park mandate to the 2021 warning/notice record and the later funding questions.',
      href: '../cuatrecasas-mandate-ric-continuity/#ric-cnmv-knowledge-bridge',
      pos: 'right bottom'
    }
  ];

  const section = document.createElement('section');
  section.className = 'section';
  section.setAttribute('data-cuatrecasas-visual-bridge-atlas', '20260902');
  section.innerHTML = `
    <div class="shell" style="max-width:1240px">
      <style>
        [data-cuatrecasas-visual-bridge-atlas="20260902"] .cvba-head{max-width:920px;margin-bottom:1rem}
        [data-cuatrecasas-visual-bridge-atlas="20260902"] .cvba-kicker{margin:0 0 .35rem;color:#80621d;font-size:.77rem;font-weight:900;letter-spacing:.06em;text-transform:uppercase}
        [data-cuatrecasas-visual-bridge-atlas="20260902"] .cvba-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}
        [data-cuatrecasas-visual-bridge-atlas="20260902"] .cvba-card{display:block;text-decoration:none;color:inherit;background:#fff;border:1px solid #d8dddd;border-radius:18px;overflow:hidden;box-shadow:0 12px 30px rgba(16,39,47,.09);transition:transform .16s ease,box-shadow .16s ease}
        [data-cuatrecasas-visual-bridge-atlas="20260902"] .cvba-card:hover{transform:translateY(-2px);box-shadow:0 17px 38px rgba(16,39,47,.14)}
        [data-cuatrecasas-visual-bridge-atlas="20260902"] .cvba-image{width:100%;aspect-ratio:520/290;background-image:var(--cvba-atlas);background-repeat:no-repeat;background-size:200% 200%;background-position:var(--cvba-pos);border-bottom:1px solid #dfe3e3}
        [data-cuatrecasas-visual-bridge-atlas="20260902"] .cvba-copy{padding:.9rem 1rem 1rem}
        [data-cuatrecasas-visual-bridge-atlas="20260902"] .cvba-copy h3{margin:.05rem 0 .4rem;color:#13252d;font-size:1.08rem}
        [data-cuatrecasas-visual-bridge-atlas="20260902"] .cvba-copy p{margin:0;color:#556164;line-height:1.5;font-size:.9rem}
        [data-cuatrecasas-visual-bridge-atlas="20260902"] .cvba-link{display:inline-block;margin-top:.55rem;color:#1d5c4a;font-weight:850;font-size:.87rem}
        [data-cuatrecasas-visual-bridge-atlas="20260902"] .cvba-boundary{margin-top:1rem;border-left:6px solid #80621d;background:#fff8e8;border-radius:14px;padding:.85rem 1rem;font-size:.86rem;color:#4f5b5e}
        @media(max-width:820px){[data-cuatrecasas-visual-bridge-atlas="20260902"] .cvba-grid{grid-template-columns:1fr}}
      </style>
      <div class="cvba-head">
        <p class="cvba-kicker">VISUAL BRIDGE ATLAS · 2 SEPTEMBER 2026</p>
        <h2>Read the Cuatrecasas record as connected pages, not isolated files.</h2>
        <p>Each visual below sits at a transition where the documentary record changes layer: mandate, hotel/insolvency, fee enforcement, Matkator’s asset perimeter, and RIC/CNMV notice continuity. Select a panel to continue into the underlying page.</p>
      </div>
      <div class="cvba-grid"></div>
      <div class="cvba-boundary"><strong>Visual-method boundary.</strong> These are navigational illustrations of the controlled reconstruction. They do not replace the source record and do not convert inference, allegation or later chronology into adjudicated fact.</div>
    </div>`;

  const grid = section.querySelector('.cvba-grid');
  panels.forEach(panel => {
    const card = document.createElement('a');
    card.className = 'cvba-card';
    card.href = panel.href;
    card.setAttribute('data-cuatrecasas-visual-panel', panel.key);
    card.innerHTML = `<div class="cvba-image" role="img" aria-label="${panel.title.replace(/"/g,'&quot;')}"></div><div class="cvba-copy"><h3>${panel.title}</h3><p>${panel.note}</p><span class="cvba-link">Open connected page →</span></div>`;
    const image = card.querySelector('.cvba-image');
    image.style.setProperty('--cvba-atlas', `url("${atlas}")`);
    image.style.setProperty('--cvba-pos', panel.pos);
    grid.appendChild(card);
  });

  const main = document.querySelector('main');
  if (!main) return;
  const insert = () => {
    const step4 = main.querySelector('[data-cuatrecasas-why-step4="20260902"]');
    const publication = main.querySelector('[data-cuatrecasas-step4-publication="20260902"]');
    const assetRegister = main.querySelector('[data-matkator-asset-rights-inbound="20260902"]');
    const anchor = step4 || publication || assetRegister || main.querySelector('section');
    if (anchor && anchor.nextSibling) main.insertBefore(section, anchor.nextSibling);
    else main.appendChild(section);
  };
  window.setTimeout(insert, 220);
})();
