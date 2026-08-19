(() => {
  'use strict';

  const path = window.location.pathname.replace(/\/+$/, '/');
  const isEs = path.includes('/por-derecho/es/');
  const isEn = path.includes('/por-derecho/en/');
  if (!isEs && !isEn) return;

  const canonicalEs = '/por-derecho/es/ingenieria-forense-criminal-sun-park/';
  const canonicalEn = '/por-derecho/en/sun-park-criminal-engineering-investigation/';
  if (path === canonicalEs || path === canonicalEn) return;

  const categories = [
    {
      id: 'cam',
      fragments: ['acosta-matos-perimetro','acosta-matos-perimeter','patron-efectos-favorables-acosta-matos','acosta-matos-favourable-effect-pattern','toma-control-sun-park','sun-park-takeover'],
      es: ['Perímetro privado central','¿Qué iniciaron, calcularon, representaron, omitieron, adquirieron y trasladaron CAM/HNT y las personas con capacidad de decisión?'],
      en: ['Core private perimeter','What did CAM/HNT and the relevant decision-makers initiate, calculate, represent, omit, acquire and transfer?']
    },
    {
      id: 'ricpe',
      fragments: ['ricpe','ric-private-equity','fondos-incentivos','eu-incentives','orion-ricpe'],
      es: ['Conversión inversora y gatekeepers','¿Quién introdujo, patrocinó, retiró, reactivó y financió el proyecto; qué conflicto, abstención, condición, dispensa y control existieron?'],
      en: ['Investment conversion and gatekeepers','Who introduced, sponsored, withdrew, reactivated and financed the project; what conflicts, abstentions, conditions, waivers and controls existed?']
    },
    {
      id: 'ac',
      fragments: ['administrador-concursal','insolvency-administrator','insolvencia-lpb','lpb-insolvency'],
      es: ['Administración Concursal','¿Protegió la masa o facilitó un resultado favorable a CAM; qué verificó independientemente y qué contradicción dejó sin resolver?'],
      en: ['Insolvency Administration','Did it protect the estate or facilitate a CAM-favourable result; what was independently verified and what contradiction remained unresolved?']
    },
    {
      id: 'judge',
      fragments: ['magistrado-juez','mercantile-court-1','cgpj','judicial-supervision'],
      es: ['Juez: decisión jurisdiccional','¿Qué decidió realmente, sobre qué material, con qué contradicción y motivación; qué cuestión quedó sin decidir?'],
      en: ['Judge: jurisdictional decision','What was actually decided, on what material, with what adversarial process and reasons; what remained undecided?']
    },
    {
      id: 'institutional',
      fragments: ['responsabilidad-institucional','institutional-accountability','fiscalia','prosecution','audiencia-cuentas','external-audit','cnmv','public-authority'],
      es: ['Autoridad o supervisor después del aviso','¿Qué aviso concreto recibió, qué competencia tenía, qué podía preservar o detener y qué efecto produjo la respuesta o inacción?'],
      en: ['Authority or supervisor after notice','What specific warning was received, what power existed, what could be preserved or stopped, and what effect followed from action or inaction?']
    },
    {
      id: 'adjudication',
      fragments: ['adjudicacion-2022','2022-adjudication','ingenieria-inversa-360','reverse-engineering-360'],
      es: ['Conversión judicial, notarial y registral','Reconstruya oferta, deuda, auto, escritura, comunicación, cuentas y Registro antes de atribuir estabilidad al resultado.'],
      en: ['Judicial, notarial and registry conversion','Reconstruct offer, debt, order, deed, notification, accounts and Registry before treating the end-state as stable.']
    },
    {
      id: 'credit',
      fragments: ['acreedor-de-registro','lender-of-record','articulo-1535','article-1535','retracto','litigious-credit','banking-recovery'],
      es: ['Crédito, deuda y palanca','Separe crédito reconocido, privilegio, cobertura hipotecaria, deuda pagadera, débito-contraprestación y beneficio obtenido.'],
      en: ['Credit, debt and leverage','Separate recognised credit, privilege, mortgage coverage, payable debt, debt-consideration and benefit obtained.']
    },
    {
      id: 'funding',
      fragments: ['mismo-hotel','same-hotel','financiacion','funding','feder','incentivos','subsid'],
      es: ['Beneficio, financiación e irreversibilidad','Siga el mismo activo, obra, coste, empleo y valor por cada capa de financiación y apoyo.'],
      en: ['Benefit, funding and irreversibility','Trace the same asset, works, costs, employment and value through every funding and support layer.']
    }
  ];

  const match = categories.find(category => category.fragments.some(fragment => path.includes(fragment)));
  if (!match) return;
  if (document.querySelector('[data-criminal-engineering-gateway]')) return;

  const copy = isEs ? {
    eyebrow: 'INVESTIGACIÓN FORENSE ACTIVA · ALEGACIÓN, NO HALLAZGO',
    title: match.es[0],
    question: match.es[1],
    body: 'Este expediente forma parte de una investigación unitaria sobre una presunta secuencia de entrada estratégica, control de facto, construcción económica, conversión judicial/notarial/registral, financiación, normalización operativa y preservación del beneficio. La existencia de actos formales no sustituye la comprobación de la premisa aguas arriba.',
    rule: '<strong>Prueba exigida:</strong> autoridad + conocimiento + deber + acto/omisión + beneficio + daño + causalidad. La ventaja repetida es una razón para investigar, no prueba automática de coordinación o delito.',
    cta: 'Abrir investigación de presunta ingeniería criminal',
    href: canonicalEs,
    boundary: 'Se preservan la presunción de inocencia, la mejor explicación alternativa y el derecho de respuesta.'
  } : {
    eyebrow: 'ACTIVE FORENSIC INVESTIGATION · ALLEGATION, NOT FINDING',
    title: match.en[0],
    question: match.en[1],
    body: 'This dossier sits within a unitary investigation into an alleged sequence of strategic entry, de facto control, economic construction, judicial/notarial/registry conversion, financing, operational normalisation and benefit preservation. Formal acts do not replace verification of the upstream premise.',
    rule: '<strong>Required proof:</strong> authority + knowledge + duty + act/omission + benefit + harm + causation. Repeated advantage is a reason to investigate, not automatic proof of coordination or crime.',
    cta: 'Open the alleged criminal-engineering investigation',
    href: canonicalEn,
    boundary: 'Presumption of innocence, the strongest alternative explanation and the right of response are preserved.'
  };

  const id = `criminal-engineering-gateway-${match.id}-20260819`;
  const style = document.createElement('style');
  style.textContent = `
    #${id}{background:#f4f1ea}
    #${id} .ce-gateway{max-width:1120px;margin:0 auto;background:#3c1715;color:#fff;border-radius:20px;padding:1.2rem 1.35rem;box-shadow:0 12px 30px rgba(19,37,45,.12)}
    #${id} .ce-eyebrow{color:#f1c6be;font-size:.75rem;font-weight:900;letter-spacing:.08em;text-transform:uppercase;margin:0 0 .35rem}
    #${id} h2{color:#fff;margin:.2rem 0 .55rem}
    #${id} .ce-question{background:#fff;color:#17242b;border-radius:13px;padding:.85rem 1rem;border-left:5px solid #8c6b2f;font-weight:750}
    #${id} .ce-rule{background:rgba(255,255,255,.1);border-radius:12px;padding:.8rem .95rem}
    #${id} .ce-boundary{font-size:.9rem;color:#f6dfda}
    #${id} a{display:inline-block;background:#fff;color:#17242b;text-decoration:none;font-weight:850;border-radius:999px;padding:.62rem .92rem;margin-top:.35rem}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.id = id;
  section.className = 'section';
  section.dataset.criminalEngineeringGateway = 'true';
  section.dataset.criminalEngineeringCategory = match.id;
  section.innerHTML = `<div class="shell"><div class="ce-gateway"><p class="ce-eyebrow">${copy.eyebrow}</p><h2>${copy.title}</h2><p class="ce-question">${copy.question}</p><p>${copy.body}</p><p class="ce-rule">${copy.rule}</p><p class="ce-boundary">${copy.boundary}</p><a href="${copy.href}">${copy.cta} →</a></div></div>`;

  const main = document.querySelector('main');
  if (!main) return;
  const hero = main.querySelector(':scope > .hero, :scope > section.hero, :scope > .dossier-hero, :scope > .cnmv-hero, :scope > .mhero');
  if (hero) hero.insertAdjacentElement('afterend', section);
  else main.insertAdjacentElement('afterbegin', section);
})();
