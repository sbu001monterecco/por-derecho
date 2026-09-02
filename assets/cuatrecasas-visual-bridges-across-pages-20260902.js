(() => {
  'use strict';
  const current = document.currentScript;
  if (!current) return;
  const path = window.location.pathname.replace(/\/+$/, '');
  if (document.querySelector('[data-cuatrecasas-visual-bridge-page="20260902"]')) return;

  const configs = [
    {
      matches: ['/en/cuatrecasas-dp748-civil-action','/es/cuatrecasas-dp748-accion-civil'],
      panel: 'left bottom',
      titleEn: 'From former-client mandate to execution against Matkator',
      titleEs: 'Del mandato del antiguo cliente a la ejecución frente a Matkator',
      bodyEn: 'Visual bridge: documented client relationship → integrated hotel/insolvency/finance work → invoices and pagarés → Matkator as executed debtor → remate / cession questions.',
      bodyEs: 'Puente visual: relación documentada con el cliente → trabajo integrado hotel/concurso/financiación → facturas y pagarés → Matkator como ejecutada → preguntas sobre remate / cesión.',
      hrefEn: '../cuatrecasas-mandate-ric-continuity/#mandate-inversion',
      hrefEs: '../cuatrecasas-mandato-continuidad-ric/#inversion-mandato',
      linkEn: 'Continue to mandate-inversion bridge →',
      linkEs: 'Continuar al puente de inversión del mandato →'
    },
    {
      matches: ['/en/matkator-asset-rights-register','/es/registro-activos-derechos-matkator'],
      panel: 'right top',
      titleEn: 'What Step 4 can — and cannot — reach',
      titleEs: 'Qué puede — y qué no puede — alcanzar el Paso 4',
      bodyEn: 'Visual bridge: finca 8,584 as the current controlled remate object → finca 8,588 as historical Matkator property → other Matkator assets only if proved and attachable → Aweswell corporate firewall.',
      bodyEs: 'Puente visual: finca 8.584 como objeto actual de remate controlado → finca 8.588 como propiedad histórica de Matkator → otros activos Matkator sólo si se prueban y son embargables → cortafuegos corporativo de Aweswell.',
      hrefEn: '../cuatrecasas-mandate-ric-continuity/#aweswell-gateway',
      hrefEs: '../cuatrecasas-mandato-continuidad-ric/#aweswell-gateway',
      linkEn: 'Continue to the Aweswell gateway analysis →',
      linkEs: 'Continuar al análisis del gateway Aweswell →'
    },
    {
      matches: ['/en/cuatrecasas-mandate-ric-continuity','/es/cuatrecasas-mandato-continuidad-ric'],
      panel: 'right bottom',
      titleEn: 'Mandate continuity into RIC / CNMV warnings',
      titleEs: 'Continuidad del mandato hacia los avisos RIC / CNMV',
      bodyEn: 'Visual bridge: pre-existing Sun Park mandate → 2021 affected-party warning and direct notice → voice-note/message context → RIC/CNMV chronology → later funding questions, without backdating later evidence.',
      bodyEs: 'Puente visual: mandato Sun Park preexistente → aviso directo de 2021 → contexto de nota de voz/mensaje → cronología RIC/CNMV → cuestiones de financiación posterior, sin retrotraer evidencia posterior.',
      hrefEn: '../ric-private-equity-sun-park/',
      hrefEs: '../ric-private-equity-sun-park/',
      linkEn: 'Continue to RIC / CNMV record →',
      linkEs: 'Continuar al registro RIC / CNMV →'
    },
    {
      matches: ['/en/cuatrecasas-sun-park'],
      panel: 'left top',
      titleEn: 'How the Cuatrecasas pages connect',
      titleEs: 'Cómo se conectan las páginas de Cuatrecasas',
      bodyEn: 'Visual map of the unitary record: Aweswell mandate → Sun Park/hotel-mobbing record → LPB Concurso 36/2012 → fee instruments / Matkator → ETJ 163/2020 → RIC/CNMV and later funding.',
      bodyEs: 'Mapa visual del registro unitario: mandato Aweswell → Sun Park/hostigamiento hotelero → Concurso LPB 36/2012 → instrumentos de honorarios / Matkator → ETJ 163/2020 → RIC/CNMV y financiación posterior.',
      hrefEn: '../cuatrecasas-mandate-ric-continuity/',
      hrefEs: '../cuatrecasas-mandato-continuidad-ric/',
      linkEn: 'Open the unitary bridge →',
      linkEs: 'Abrir el puente unitario →'
    }
  ];

  const config = configs.find(c => c.matches.some(m => path.includes(m)));
  if (!config) return;
  const isEs = /\/es(?:\/|$)/.test(path);

  const inject = () => {
    const atlas = window.__CUAT_VIS_BRIDGE_ATLAS_20260902__;
    if (!atlas || document.querySelector('[data-cuatrecasas-visual-bridge-page="20260902"]')) return;
    const section = document.createElement('section');
    section.className = 'section';
    section.setAttribute('data-cuatrecasas-visual-bridge-page', '20260902');
    const title = isEs ? config.titleEs : config.titleEn;
    const body = isEs ? config.bodyEs : config.bodyEn;
    const href = isEs ? config.hrefEs : config.hrefEn;
    const link = isEs ? config.linkEs : config.linkEn;
    section.innerHTML = `
      <div class="shell" style="max-width:1180px">
        <style>
          [data-cuatrecasas-visual-bridge-page="20260902"] .cvbp{background:#fff;border:1px solid #d8dddd;border-radius:20px;overflow:hidden;box-shadow:0 16px 38px rgba(16,39,47,.1)}
          [data-cuatrecasas-visual-bridge-page="20260902"] .cvbp-img{width:100%;aspect-ratio:520/290;background-image:var(--cvbp-atlas);background-repeat:no-repeat;background-size:200% 200%;background-position:var(--cvbp-pos);border-bottom:1px solid #dfe3e3}
          [data-cuatrecasas-visual-bridge-page="20260902"] .cvbp-copy{padding:1rem 1.15rem 1.1rem}
          [data-cuatrecasas-visual-bridge-page="20260902"] .cvbp-kicker{margin:0 0 .3rem;color:#80621d;font-size:.75rem;font-weight:900;letter-spacing:.055em;text-transform:uppercase}
          [data-cuatrecasas-visual-bridge-page="20260902"] .cvbp-copy h2{margin:.18rem 0 .5rem;color:#13252d}
          [data-cuatrecasas-visual-bridge-page="20260902"] .cvbp-copy p{margin:.35rem 0;line-height:1.55;color:#556164}
          [data-cuatrecasas-visual-bridge-page="20260902"] .cvbp-link{display:inline-block;margin-top:.65rem;background:#13252d;color:#fff;text-decoration:none;font-weight:850;border-radius:999px;padding:.56rem .85rem}
          [data-cuatrecasas-visual-bridge-page="20260902"] .cvbp-boundary{margin-top:.65rem;font-size:.82rem;color:#667174}
        </style>
        <div class="cvbp">
          <div class="cvbp-img" role="img" aria-label="${title.replace(/"/g,'&quot;')}"></div>
          <div class="cvbp-copy">
            <p class="cvbp-kicker">${isEs ? 'PUENTE VISUAL · LECTURA ENTRE PÁGINAS' : 'VISUAL BRIDGE · PAGE-TO-PAGE READING'}</p>
            <h2>${title}</h2>
            <p>${body}</p>
            <a class="cvbp-link" href="${href}">${link}</a>
            <p class="cvbp-boundary"><strong>${isEs ? 'Límite visual:' : 'Visual boundary:'}</strong> ${isEs ? 'la ilustración resume la arquitectura documental; no sustituye las fuentes ni convierte inferencias o alegaciones en hechos adjudicados.' : 'the illustration summarizes the documentary architecture; it does not replace sources or convert inferences or allegations into adjudicated facts.'}</p>
          </div>
        </div>
      </div>`;
    const image = section.querySelector('.cvbp-img');
    image.style.setProperty('--cvbp-atlas', `url("${atlas}")`);
    image.style.setProperty('--cvbp-pos', config.panel);

    const main = document.querySelector('main');
    if (!main) return;
    const preferred = main.querySelector('#mandate-inversion,#inversion-mandato,#aweswell-gateway,[data-matkator-asset-rights-inbound="20260902"],[data-cuatrecasas-why-step4="20260902"]');
    const anchor = preferred || main.querySelector('section');
    if (anchor && anchor.nextSibling) main.insertBefore(section, anchor.nextSibling);
    else main.appendChild(section);
  };

  const ensureAtlas = () => {
    if (window.__CUAT_VIS_BRIDGE_ATLAS_20260902__) { inject(); return; }
    if (document.querySelector('script[data-cuatrecasas-visual-bridge-atlas-data-loader]')) {
      window.setTimeout(inject, 120);
      return;
    }
    const data = document.createElement('script');
    data.src = new URL('cuatrecasas-visual-bridge-atlas-data-20260902.js?v=20260902b', current.src).href;
    data.async = false;
    data.setAttribute('data-cuatrecasas-visual-bridge-atlas-data-loader', '20260902b');
    data.addEventListener('load', inject, { once: true });
    document.head.appendChild(data);
  };
  ensureAtlas();
})();
