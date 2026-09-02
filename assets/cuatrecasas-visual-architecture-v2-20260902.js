(() => {
  'use strict';
  const current = document.currentScript;
  if (!current) return;

  const path = window.location.pathname.replace(/\/+$/, '');
  const isEs = /\/es(?:\/|$)/.test(path);
  const lang = isEs ? 'es' : 'en';

  const legacy = [
    '[data-cuatrecasas-visual-bridge-atlas="20260902"]',
    '[data-cuatrecasas-visual-bridge-page="20260902"]'
  ];
  legacy.forEach(sel => document.querySelectorAll(sel).forEach(el => el.remove()));
  if (document.querySelector('[data-cuatrecasas-visual-architecture-v2="20260902"]')) return;

  const ends = slug => path.endsWith('/' + lang + '/' + slug);
  const contains = slug => path.includes('/' + lang + '/' + slug);

  let kind = null;
  let panels = [];

  if (ends('cuatrecasas-sun-park')) {
    kind = 'main'; panels = ['A','C','D'];
  } else if ((lang === 'en' && ends('cuatrecasas-mandate-ric-continuity')) || (lang === 'es' && ends('cuatrecasas-mandato-continuidad-ric'))) {
    kind = 'bridge'; panels = ['A','B','C','D'];
  } else if ((lang === 'en' && ends('cuatrecasas-dp748-civil-action')) || (lang === 'es' && ends('cuatrecasas-dp748-accion-civil'))) {
    kind = 'etj'; panels = ['C','B'];
  } else if ((lang === 'en' && ends('matkator-asset-rights-register')) || (lang === 'es' && ends('registro-activos-derechos-matkator'))) {
    kind = 'matkator'; panels = ['B'];
  } else if ((lang === 'en' && ends('reverse-engineering-360-sun-park-chain')) || (lang === 'es' && ends('ingenieria-inversa-360-cadena-sun-park'))) {
    kind = '360'; panels = ['A','B'];
  } else if ((lang === 'en' && ends('unitary-record')) || (lang === 'es' && ends('registro-unitario'))) {
    kind = 'unitary'; panels = ['A'];
  } else if (
    contains('ric-private-equity-sun-park') ||
    contains('ricpe-cnmv-dossier-2021') ||
    contains('cnmv-ricpe-verification') ||
    (lang === 'en' && contains('same-hotel-multiple-financial-lives')) ||
    (lang === 'es' && contains('mismo-hotel-multiples-vidas-financieras'))
  ) {
    kind = 'ric'; panels = ['D'];
  }

  if (!kind) return;

  const atlas = new URL(
    isEs ? 'cuatrecasas-visual-bridge-atlas-es-20260902.svg?v=20260902c' : 'cuatrecasas-visual-bridge-atlas-en-20260902.svg?v=20260902c',
    current.src
  ).href;

  const view = {
    A: '0 0 600 600',
    B: '600 0 600 600',
    C: '0 600 600 600',
    D: '600 600 600 600'
  };

  const target = key => {
    if (key === 'A') return isEs ? '../cuatrecasas-mandato-continuidad-ric/' : '../cuatrecasas-mandate-ric-continuity/';
    if (key === 'B') return isEs ? '../registro-activos-derechos-matkator/' : '../matkator-asset-rights-register/';
    if (key === 'C') return isEs ? '../cuatrecasas-dp748-accion-civil/' : '../cuatrecasas-dp748-civil-action/';
    return '../ric-private-equity-sun-park/';
  };

  const copy = {
    en: {
      A: {
        title: 'How the Cuatrecasas pages connect',
        alt: 'Visual A: Aweswell mandate to Sun Park, LPB insolvency workstream, fee instruments and Matkator, ETJ 163/2020, then RIC/CNMV and later funding.',
        body: 'Use this as the top-level navigation map. It keeps the Aweswell mandate above the LPB insolvency workstream and shows where the fee/Matkator and RIC/CNMV branches reconnect.',
        link: 'Continue to the unitary mandate/RIC bridge →'
      },
      B: {
        title: 'What Step 4 can — and cannot — reach',
        alt: 'Visual B: finca 8,584 is the current controlled remate object; finca 8,588 is historical Matkator property; other Matkator assets require proof; Aweswell remains behind a corporate firewall.',
        body: 'This panel separates the single controlled remate object from the wider Matkator debtor perimeter and from Aweswell’s indirect economic/equity-value gateway.',
        link: 'Open the Matkator asset-and-rights register →'
      },
      C: {
        title: 'From former-client mandate to execution against Matkator',
        alt: 'Visual C: documented Aweswell client relationship, integrated mandate, invoices and pagarés, Matkator as executed debtor, 17 October 2024 adjudication request and open mandate-coherence question.',
        body: 'This is the professional-mandate-to-ETJ bridge: fee entitlement is kept separate from the open question whether the later enforcement mechanism cohered with the protective mandate.',
        link: 'Open the ETJ / civil-action reconstruction →'
      },
      D: {
        title: 'Mandate continuity into RIC / CNMV warnings',
        alt: 'Visual D: pre-existing Sun Park mandate, 8 March 2021 direct notice, 17 March communications, 2021 RIC/CNMV record, 2025 to March 2026 escalations and later funding under a temporal firewall.',
        body: 'This panel preserves continuity without backdating later evidence: the 2021 notice record is connected to the earlier mandate, but later incentives/FEDER/funding records remain later.',
        link: 'Open the RIC / CNMV record →'
      }
    },
    es: {
      A: {
        title: 'Cómo se conectan las páginas de Cuatrecasas',
        alt: 'Visual A: mandato Aweswell, Sun Park, workstream del Concurso LPB, instrumentos de honorarios y Matkator, ETJ 163/2020, y después RIC/CNMV y financiación posterior.',
        body: 'Mapa de navegación de nivel superior. Mantiene el mandato Aweswell por encima del workstream concursal de LPB y muestra dónde vuelven a conectarse las ramas de honorarios/Matkator y RIC/CNMV.',
        link: 'Continuar al puente unitario mandato/RIC →'
      },
      B: {
        title: 'Qué puede — y qué no puede — alcanzar el Paso 4',
        alt: 'Visual B: finca 8.584 como objeto actual controlado de remate; finca 8.588 como propiedad histórica de Matkator; otros activos requieren prueba; Aweswell queda tras el cortafuegos corporativo.',
        body: 'Separa el único objeto de remate actualmente controlado del perímetro patrimonial más amplio de Matkator y del gateway económico/de valor de equity indirecto de Aweswell.',
        link: 'Abrir el registro de activos y derechos de Matkator →'
      },
      C: {
        title: 'Del mandato del antiguo cliente a la ejecución frente a Matkator',
        alt: 'Visual C: relación documentada con Aweswell, mandato integrado, facturas y pagarés, Matkator como ejecutada, solicitud de adjudicación de 17 octubre 2024 y pregunta abierta de coherencia del mandato.',
        body: 'Puente del mandato profesional a la ETJ: el eventual derecho al cobro queda separado de la pregunta abierta sobre la coherencia del mecanismo ejecutivo posterior con el mandato protector.',
        link: 'Abrir la reconstrucción ETJ / acción civil →'
      },
      D: {
        title: 'Continuidad del mandato hacia los avisos RIC / CNMV',
        alt: 'Visual D: mandato Sun Park preexistente, aviso directo de 8 marzo 2021, comunicaciones de 17 marzo, registro RIC/CNMV 2021, escaladas 2025 a marzo 2026 y financiación posterior bajo cortafuegos temporal.',
        body: 'Preserva continuidad sin retrotraer evidencia: el aviso de 2021 se conecta con el mandato anterior, pero los registros posteriores de incentivos/FEDER/fondos siguen siendo posteriores.',
        link: 'Abrir el registro RIC / CNMV →'
      }
    }
  }[lang];

  const headings = {
    en: {
      main: ['VISUAL ROUTE · UNITARY MANDATE HISTORY', 'Follow the Cuatrecasas record by bridges, not isolated files.'],
      bridge: ['VISUAL EXPLAINER · ALL FOUR BRIDGES', 'Mandate → Matkator → ETJ → RIC/CNMV: the whole architecture on one page.'],
      etj: ['VISUAL BRIDGE · ETJ / MANDATE INVERSION', 'Separate the professional-mandate question from the execution perimeter.'],
      matkator: ['VISUAL BRIDGE · ASSET / RIGHTS PERIMETER', 'One current remate object does not equal the whole debtor perimeter.'],
      ric: ['VISUAL BRIDGE · RIC / CNMV CONTINUITY', 'Connect the 2021 notice to the pre-existing mandate without backdating later evidence.'],
      '360': ['VISUAL BRIDGE · 360° RECONSTRUCTION', 'Place the Cuatrecasas mandate and Matkator perimeter inside the wider Sun Park chain.'],
      unitary: ['VISUAL BRIDGE · UNITARY RECORD', 'Use the mandate architecture as a navigation layer into the Cuatrecasas record.']
    },
    es: {
      main: ['RUTA VISUAL · HISTORIA UNITARIA DEL MANDATO', 'Seguir el registro Cuatrecasas mediante puentes, no como archivos aislados.'],
      bridge: ['EXPLICADOR VISUAL · LOS CUATRO PUENTES', 'Mandato → Matkator → ETJ → RIC/CNMV: toda la arquitectura en una sola página.'],
      etj: ['PUENTE VISUAL · ETJ / INVERSIÓN DEL MANDATO', 'Separar la cuestión del mandato profesional del perímetro de ejecución.'],
      matkator: ['PUENTE VISUAL · PERÍMETRO DE ACTIVOS / DERECHOS', 'Un objeto actual de remate no equivale a todo el perímetro del deudor.'],
      ric: ['PUENTE VISUAL · CONTINUIDAD RIC / CNMV', 'Conectar el aviso de 2021 con el mandato preexistente sin retrotraer evidencia posterior.'],
      '360': ['PUENTE VISUAL · RECONSTRUCCIÓN 360°', 'Situar el mandato Cuatrecasas y el perímetro Matkator dentro de la cadena Sun Park más amplia.'],
      unitary: ['PUENTE VISUAL · REGISTRO UNITARIO', 'Usar la arquitectura del mandato como capa de navegación hacia el registro Cuatrecasas.']
    }
  }[lang][kind];

  const section = document.createElement('section');
  section.className = 'section';
  section.setAttribute('data-cuatrecasas-visual-architecture-v2', '20260902');
  section.setAttribute('data-cuatrecasas-visual-bridge-atlas', '20260902');
  section.setAttribute('data-cuatrecasas-visual-bridge-page', '20260902');

  section.innerHTML = `
    <div class="shell cv2-shell">
      <style>
        [data-cuatrecasas-visual-architecture-v2="20260902"] .cv2-shell{max-width:1240px}
        [data-cuatrecasas-visual-architecture-v2="20260902"] .cv2-head{max-width:980px;margin-bottom:1rem}
        [data-cuatrecasas-visual-architecture-v2="20260902"] .cv2-kicker{margin:0 0 .35rem;color:#80621d;font-size:.76rem;font-weight:900;letter-spacing:.06em;text-transform:uppercase}
        [data-cuatrecasas-visual-architecture-v2="20260902"] .cv2-head h2{margin:.15rem 0 .45rem;color:#13252d}
        [data-cuatrecasas-visual-architecture-v2="20260902"] .cv2-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}
        [data-cuatrecasas-visual-architecture-v2="20260902"] .cv2-card{display:block;text-decoration:none;color:inherit;background:#fff;border:1px solid #d8dddd;border-radius:20px;overflow:hidden;box-shadow:0 14px 34px rgba(16,39,47,.1);transition:transform .16s ease,box-shadow .16s ease}
        [data-cuatrecasas-visual-architecture-v2="20260902"] .cv2-card:hover{transform:translateY(-2px);box-shadow:0 18px 42px rgba(16,39,47,.15)}
        [data-cuatrecasas-visual-architecture-v2="20260902"] .cv2-figure{margin:0;background:#eef2f0;border-bottom:1px solid #dfe3e3}
        [data-cuatrecasas-visual-architecture-v2="20260902"] .cv2-figure svg{display:block;width:100%;height:auto;aspect-ratio:1/1}
        [data-cuatrecasas-visual-architecture-v2="20260902"] .cv2-copy{padding:.9rem 1rem 1.05rem}
        [data-cuatrecasas-visual-architecture-v2="20260902"] .cv2-copy h3{margin:.05rem 0 .4rem;color:#13252d;font-size:1.08rem}
        [data-cuatrecasas-visual-architecture-v2="20260902"] .cv2-copy p{margin:.25rem 0;color:#556164;line-height:1.5;font-size:.9rem}
        [data-cuatrecasas-visual-architecture-v2="20260902"] .cv2-next{display:inline-block;margin-top:.55rem;color:#1d5c4a;font-weight:850;font-size:.88rem}
        [data-cuatrecasas-visual-architecture-v2="20260902"] .cv2-boundary{margin-top:1rem;border-left:6px solid #80621d;background:#fff8e8;border-radius:14px;padding:.9rem 1rem;color:#4f5b5e;font-size:.86rem}
        @media(max-width:820px){[data-cuatrecasas-visual-architecture-v2="20260902"] .cv2-grid{grid-template-columns:1fr}}
      </style>
      <div class="cv2-head"><p class="cv2-kicker">${headings[0]}</p><h2>${headings[1]}</h2></div>
      <div class="cv2-grid"></div>
      <div class="cv2-boundary"><strong>${isEs ? 'Límite visual.' : 'Visual boundary.'}</strong> ${isEs ? 'Estos diagramas son ayudas de navegación/reconstrucción. No sustituyen las fuentes, no convierten inferencias o alegaciones en hechos adjudicados y no eliminan los cortafuegos de identidad, titularidad, temporalidad o procedimiento.' : 'These diagrams are navigation/reconstruction aids. They do not replace sources, convert inferences or allegations into adjudicated facts, or remove identity, title, temporal or procedural firewalls.'}</div>
    </div>`;

  const grid = section.querySelector('.cv2-grid');
  panels.forEach(key => {
    const c = copy[key];
    const card = document.createElement('a');
    card.className = 'cv2-card';
    card.href = target(key);
    card.setAttribute('data-cuatrecasas-visual-panel-v2', key);
    card.innerHTML = `
      <figure class="cv2-figure">
        <svg viewBox="${view[key]}" role="img" aria-label="${c.alt.replace(/"/g,'&quot;')}" preserveAspectRatio="xMidYMid meet">
          <title>${c.alt}</title>
          <image href="${atlas}" x="0" y="0" width="1200" height="1200" preserveAspectRatio="xMidYMid meet"></image>
        </svg>
      </figure>
      <div class="cv2-copy"><h3>${c.title}</h3><p>${c.body}</p><span class="cv2-next">${c.link}</span></div>`;
    grid.appendChild(card);
  });

  const insert = () => {
    const main = document.querySelector('main');
    if (!main || section.isConnected) return;
    document.querySelectorAll(legacy.join(',')).forEach(el => {
      if (el !== section) el.remove();
    });

    let anchor = null;
    if (kind === 'main') anchor = main.querySelector('[data-cuatrecasas-why-step4="20260902"]');
    if (kind === 'matkator') anchor = main.querySelector('[data-matkator-asset-rights-inbound="20260902"]');
    if (!anchor) anchor = main.querySelector('section');
    if (anchor && anchor.nextSibling) main.insertBefore(section, anchor.nextSibling);
    else main.appendChild(section);
  };

  window.setTimeout(insert, 320);
})();