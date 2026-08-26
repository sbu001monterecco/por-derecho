(() => {
  'use strict';

  const path = window.location.pathname.replace(/\/+$/, '/');
  const isEs = path.includes('/por-derecho/es/');
  const isEn = path.includes('/por-derecho/en/');
  if (!isEs && !isEn) return;

  const lang = isEs ? 'es' : 'en';
  const base = '/por-derecho';
  const routes = {
    control: isEs ? `${base}/es/sala-control-caso/` : `${base}/en/case-control-room/`,
    investigation: isEs ? `${base}/es/ingenieria-forense-criminal-sun-park/` : `${base}/en/sun-park-criminal-engineering-investigation/`,
    method: isEs ? `${base}/es/ingenieria-inversa-360-cadena-sun-park/` : `${base}/en/reverse-engineering-360-sun-park-chain/`,
    corrections: isEs ? `${base}/es/correcciones-control-versiones/` : `${base}/en/corrections-version-control/`,
    notary: isEs ? `${base}/es/implementacion-notarial-protocolo-457/` : `${base}/en/notarial-implementation-protocol-457/`,
    registry: isEs ? `${base}/es/implementacion-registral-finca-por-finca/` : `${base}/en/land-registry-implementation-property-by-property/`,
    updates: isEs ? `${base}/es/actualizaciones/` : `${base}/en/updates/`,
  };

  const copy = isEs ? {
    hubLabel: 'EXPEDIENTE SUN PARK',
    control: 'Sala de Control',
    investigation: 'Investigación forense',
    method: 'Método 360°',
    corrections: 'Correcciones',
    homeEyebrow: 'ESTADO DEL CASO · PRUEBA, ALEGACIÓN Y PREGUNTAS ABIERTAS',
    homeTitle: 'Una sola entrada para entender qué está documentado, qué se alega y qué falta por probar.',
    homeBody: 'La Sala de Control enlaza cada cuestión CE-001–CE-010 con su fuente, la defensa más fuerte, el documento decisivo pendiente y la página que mantiene el estado vigente. LIVE_VERIFIED describe publicación técnica y lectura pública, no una validación independiente del fondo.',
    openControl: 'Abrir Sala de Control',
    openInvestigation: 'Abrir investigación',
    openCorrections: 'Ver correcciones',
    canonicalTitle: 'Sun Park / MYND Yaiza · investigación forense de la cadena de control, adjudicación y financiación',
    canonicalDescription: 'Investigación forense activa y actor por actor sobre la cadena Sun Park→CAM→HNT→RICPE/MYND, con hechos documentados, alegaciones, defensas, preguntas abiertas y correcciones visibles.',
    canonicalH1: 'Hay que reconstruir si —y, en su caso, cómo— actos privados e institucionales separados convirtieron premisas disputadas en control, título, financiación y un resultado progresivamente difícil de revertir.',
    proofTitle: 'Estado de prueba: lo documentado no debe mezclarse con lo alegado.',
    documented: 'DOCUMENTADO ACTUALMENTE',
    alleged: 'POR DERECHO ALEGA',
    notProved: 'NO PROBADO',
    missing: 'PRUEBA DECISIVA PENDIENTE',
    documentedBody: 'En el protocolo 457, los seis componentes impresos suman 13.065.186,68 €; el diferencial de 102.895,34 € hasta 13.168.082,02 € coincide con el paso de la demora de primer rango al tope hipotecario. El instrumento se refiere a 159 fincas hipotecadas; la rama de 400.000 € para 29 locales y 2 piscinas/solárium es separada; y la certificación RICPE de julio de 2021 distinguió 54 fincas CAM, 190 LPB y 18 de terceros.',
    allegedBody: 'Premisas disputadas pudieron atravesar controles privados, concursales, judiciales, notariales, registrales, financieros y supervisores, con niveles distintos de conocimiento, deber, acción u omisión y beneficio.',
    notProvedBody: 'Fondos incondicionales en una fecha concreta, obstrucción deliberada, sesgo judicial, connivencia, prevaricación, coordinación criminal, duplicidad material de financiación o causalidad exclusiva del control de junio de 2018.',
    missingBody: 'Textos definitivos completos; soporte jurídico de cada componente de deuda; comunicación de la escritura en cinco días; cuentas finales; cadena bancaria/contable/registral de 400.000 €; certificados finca por finca; y archivos RICPE de gobierno, DD y desembolso.',
    issueTitle: 'Registro vivo CE-001–CE-010',
    issueIntro: 'Cada tarjeta muestra el estado público controlado, no una conclusión penal. La fuente primaria y la validación jurídica prevalecen sobre resúmenes, borradores o páginas anteriores.',
    lastReviewed: 'Última revisión',
    documentedLabel: 'Documentado',
    notProvedLabel: 'No probado',
    defenceLabel: 'Defensa más fuerte',
    nextSourceLabel: 'Prueba decisiva siguiente',
    counsel: 'Validación letrada requerida',
    openIssue: 'Abrir expediente',
    contextEyebrow: 'ESTA PÁGINA DENTRO DEL CASO',
    requiredProof: 'Prueba exigida',
    requiredProofBody: 'autoridad + conocimiento + deber + acto/omisión + beneficio + daño + causalidad',
    contextBoundary: 'La ventaja repetida justifica examen reforzado; no prueba automáticamente coordinación, delito ni responsabilidad colectiva.',
    updateHeading: '19 agosto 2026 · arquitectura del caso',
    updateTitle: 'Sala de Control, registro CE-001–CE-010 y correcciones visibles',
    updateBody: 'La navegación pública se reorganiza alrededor de una Sala de Control, una investigación forense condicionada, un método 360° y un registro de correcciones. Los dos bloques dinámicos anteriores se sustituyen por un único módulo compacto que identifica fase, actor, cuestiones y límites probatorios.',
    updateTag: 'Arquitectura y correcciones',
    updateNew: 'Nuevo',
    liveBoundary: 'LIVE_VERIFIED = publicación técnica y lectura pública; no equivale a verificación independiente del fondo.',
  } : {
    hubLabel: 'SUN PARK RECORD',
    control: 'Case Control Room',
    investigation: 'Forensic investigation',
    method: '360° method',
    corrections: 'Corrections',
    homeEyebrow: 'CASE STATUS · EVIDENCE, ALLEGATION AND OPEN QUESTIONS',
    homeTitle: 'One entry point for what is documented, what is alleged and what remains to be proved.',
    homeBody: 'The Case Control Room links every CE-001–CE-010 issue to its source, strongest defence, decisive missing document and authoritative status page. LIVE_VERIFIED describes technical publication and public read-back, not independent verification of the merits.',
    openControl: 'Open Case Control Room',
    openInvestigation: 'Open investigation',
    openCorrections: 'View corrections',
    canonicalTitle: 'Sun Park / MYND Yaiza · forensic investigation of the control, adjudication and financing chain',
    canonicalDescription: 'Active actor-by-actor forensic investigation of the Sun Park→CAM→HNT→RICPE/MYND chain, separating documented facts, allegations, defences, open questions and visible corrections.',
    canonicalH1: 'The investigation must determine whether—and, if so, how—separate private and institutional acts converted disputed premises into control, title, financing and a progressively harder-to-reverse outcome.',
    proofTitle: 'State of proof: documented material must not be conflated with allegation.',
    documented: 'CURRENTLY DOCUMENTED',
    alleged: 'POR DERECHO ALLEGES',
    notProved: 'NOT PROVED',
    missing: 'DECISIVE EVIDENCE OUTSTANDING',
    documentedBody: 'In Protocol 457, the six printed components total EUR 13,065,186.68; the EUR 102,895.34 difference to EUR 13,168,082.02 matches the first-rank default-interest cap step. The instrument concerns 159 mortgaged properties; the EUR 400,000 branch for 29 premises and 2 pools/solarium is separate; and the July 2021 RICPE certification distinguished 54 CAM, 190 LPB and 18 third-party properties.',
    allegedBody: 'Disputed premises may have crossed private, insolvency, judicial, notarial, Registry, financing and supervisory gates, with different levels of knowledge, duty, action or omission and benefit.',
    notProvedBody: 'Unconditional funds on a specific date, deliberate obstruction, judicial bias, collusion, prevarication, criminal coordination, material funding duplication or exclusive causation by the June 2018 control event.',
    missingBody: 'Complete definitive creditor texts; legal basis for every debt component; five-day deed notification; final accounts; the EUR 400,000 bank/accounting/Registry chain; property-by-property certificates; and RICPE governance, DD and drawdown files.',
    issueTitle: 'Live CE-001–CE-010 register',
    issueIntro: 'Each card shows the controlled public status, not a criminal finding. Primary evidence and date-specific legal validation prevail over summaries, drafts and earlier pages.',
    lastReviewed: 'Last reviewed',
    documentedLabel: 'Documented',
    notProvedLabel: 'Not proved',
    defenceLabel: 'Strongest defence',
    nextSourceLabel: 'Next decisive evidence',
    counsel: 'Counsel validation required',
    openIssue: 'Open dossier',
    contextEyebrow: 'THIS PAGE WITHIN THE CASE',
    requiredProof: 'Required proof',
    requiredProofBody: 'authority + knowledge + duty + act/omission + benefit + harm + causation',
    contextBoundary: 'Repeated advantage warrants heightened examination; it does not automatically prove coordination, crime or collective responsibility.',
    updateHeading: '19 August 2026 · case architecture',
    updateTitle: 'Case Control Room, CE-001–CE-010 register and visible corrections',
    updateBody: 'Public navigation is reorganised around a Case Control Room, a conditional forensic investigation, a 360° method and a corrections register. The former two large dynamic gateways are replaced by one compact module identifying phase, actor, issues and evidential limits.',
    updateTag: 'Architecture and corrections',
    updateNew: 'New',
    liveBoundary: 'LIVE_VERIFIED = technical publication and public read-back; it is not independent verification of the merits.',
  };

  const categoryRules = [
    { id:'cam', fragments:['acosta-matos-perimetro','acosta-matos-perimeter','patron-efectos-favorables-acosta-matos','acosta-matos-favourable-effect-pattern','toma-control-sun-park','sun-park-takeover'], phase:'1–8', issues:'CE-003 · CE-005 · CE-009 · CE-010', es:['Perímetro CAM/HNT','¿Qué persona jurídica hizo qué, en qué capacidad, sobre qué finca o derecho y con qué autoridad documental?'], en:['CAM/HNT perimeter','Which legal person did what, in what capacity, over which property or right, and with what documentary authority?'] },
    { id:'ricpe', fragments:['ricpe','ric-private-equity','orion-ricpe','fondos-incentivos','eu-incentives'], phase:'6–8', issues:'CE-005 · CE-010', es:['RICPE, controles y financiación','¿Quién introdujo, patrocinó, retiró, reactivó, autorizó y financió el proyecto; qué conflicto, DD, condición, dispensa y desembolso consta?'], en:['RICPE, controls and financing','Who introduced, sponsored, withdrew, reactivated, authorised and financed the project; what conflict, DD, condition, waiver and drawdown is recorded?'] },
    { id:'ac', fragments:['administrador-concursal','insolvency-administrator','insolvencia-lpb','lpb-insolvency'], phase:'3–5', issues:'CE-001 · CE-002 · CE-006', es:['Administración Concursal','¿Qué protegió, verificó, decidió u omitió la AC; qué efecto produjo; y dónde se sitúa, si procede, entre juicio razonable, error, negligencia, deslealtad o facilitación consciente?'], en:['Insolvency Administration','What did the Administrator protect, verify, decide or omit; what effect followed; and where, if at all, does it fall between reasonable judgment, error, negligence, disloyalty or knowing facilitation?'] },
    { id:'judge', fragments:['magistrado-juez','mercantile-court-1','cgpj-supervision','judicial-supervision'], phase:'4', issues:'CE-002 · CE-007', es:['Juez: decisiones jurisdiccionales','¿Qué decidió realmente cada resolución, con qué prueba y contradicción, qué dejó sin decidir y qué operación exacta autorizó?'], en:['Judge: jurisdictional decisions','What did each decision actually determine, on what evidence and adversarial process, what remained undecided and what exact transaction was authorised?'] },
    { id:'laj', fragments:['concurso-36-2012-laj','insolvency-36-2012-laj','oficina-judicial','judicial-office'], phase:'4–5', issues:'CE-002 · CE-007', es:['LAJ / oficina judicial','¿Cómo se tramitaron escritos, anexos, notificaciones, recursos, firmeza, testimonios, ejecución y comunicación de la escritura?'], en:['LAJ / judicial office','How were filings, schedules, service, appeals, finality, testimonies, execution and deed notification handled?'] },
    { id:'adjudication', fragments:['adjudicacion-2022','2022-adjudication'], phase:'3–5', issues:'CE-001 · CE-002 · CE-004', es:['Adjudicación, deuda y cuentas','Reconstruya texto definitivo, seis componentes, oferta, auto, escritura, 400.000 €, comunicación, cuentas y Registro antes de atribuir estabilidad al resultado.'], en:['Adjudication, debt and accounts','Reconstruct definitive texts, six components, offer, order, deed, EUR 400,000, notification, accounts and Registry before treating the outcome as stable.'] },
    { id:'credit', fragments:['acreedor-de-registro','lender-of-record','articulo-1535','article-1535','retracto','litigious-credit','banking-recovery'], phase:'1–5', issues:'CE-001 · CE-009', es:['Crédito, clasificación y palanca','Separe crédito reconocido, privilegio, cobertura hipotecaria, deuda pagadera, débito-contraprestación y beneficio obtenido.'], en:['Credit, classification and leverage','Separate recognised credit, privilege, mortgage coverage, payable debt, debt-consideration and benefit obtained.'] },
    { id:'funding', fragments:['mismo-hotel','same-hotel','financiacion','funding','feder','subsid','incentivos'], phase:'6–8', issues:'CE-005 · CE-010', es:['Financiación y apoyo público','Siga activo, obra, factura, empleo y valor por cada capa; coexistencia no equivale a duplicidad o ilicitud.'], en:['Financing and public support','Trace asset, works, invoice, employment and value through each layer; coexistence is not proof of duplication or wrongdoing.'] },
    { id:'notary', fragments:['implementacion-notarial','notarial-implementation'], phase:'5', issues:'CE-001 · CE-002', es:['Implementación notarial','¿Qué título y autoridad se presentaron, quién suministró el cálculo y qué advertencias, cancelación y comunicación constan?'], en:['Notarial implementation','What title and authority were presented, who supplied the calculation, and what warnings, cancellation request and notification are recorded?'] },
    { id:'registry', fragments:['implementacion-registral','land-registry-implementation','mapa-forense-sun-park-262','262-property-forensic'], phase:'5–8', issues:'CE-003 · CE-004 · CE-009', es:['Registro y tracto finca por finca','¿Qué se presentó, calificó, inscribió o canceló y qué derechos posteriores sobreviven con título independiente?'], en:['Registry and property-by-property chain','What was presented, qualified, registered or cancelled, and which later rights survive on an independent title?'] },
    { id:'institutional', fragments:['responsabilidad-institucional','institutional-accountability','fiscalia','prosecution','audiencia-cuentas','external-audit','cnmv','public-authority'], phase:'4–8', issues:'CE-007 · CE-008 · CE-010', es:['Autoridad o supervisor después del aviso','¿Qué aviso concreto recibió, qué competencia tenía, qué podía preservar, verificar, remitir o detener y qué efecto siguió?'], en:['Authority or supervisor after notice','What specific warning was received, what power existed, what could be preserved, verified, referred or stopped, and what effect followed?'] },
  ];

  const esc = value => String(value ?? '').replace(/[&<>'"]/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));
  const absRoute = route => route?.startsWith('/por-derecho/') ? route : `${base}${route || ''}`;

  function addStyles() {
    if (document.getElementById('case-information-architecture-styles-20260819')) return;
    const style = document.createElement('style');
    style.id = 'case-information-architecture-styles-20260819';
    style.textContent = `
      .case-hub-strip{background:#0f222a;color:#fff;border-top:1px solid rgba(255,255,255,.12);border-bottom:1px solid rgba(255,255,255,.12)}
      .case-hub-strip .shell{display:flex;gap:.7rem;align-items:center;flex-wrap:wrap;padding:.62rem 0}.case-hub-strip strong{font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:#e5cfa5;margin-right:.35rem}.case-hub-strip a{color:#fff;text-decoration:none;font-weight:780;font-size:.9rem;border:1px solid rgba(255,255,255,.28);border-radius:999px;padding:.33rem .62rem}.case-hub-strip a:hover{background:#fff;color:#0f222a}
      .case-status-band{background:#f4f1ea;border-bottom:1px solid rgba(19,37,45,.14)}.case-status-card{max-width:1160px;margin:0 auto;padding:1.35rem 0}.case-status-card .eyebrow{color:#7b4c22}.case-status-card h2{max-width:900px;margin:.25rem 0 .65rem}.case-status-card p{max-width:920px}.case-status-actions{display:flex;gap:.65rem;flex-wrap:wrap;margin-top:.9rem}.case-status-actions a{display:inline-block;border-radius:999px;padding:.6rem .88rem;background:#13252d;color:#fff;text-decoration:none;font-weight:800}.case-status-actions a.secondary{background:#fff;color:#13252d;border:1px solid #13252d}
      .case-proof-panel{margin:1rem auto 0;max-width:1160px}.case-proof-panel>h2{margin:.1rem 0 .8rem}.case-proof-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.75rem}.case-proof-card{background:#fff;border:1px solid rgba(19,37,45,.16);border-top:5px solid #536d79;border-radius:14px;padding:1rem}.case-proof-card.alleged{border-top-color:#8c2f2c}.case-proof-card.not-proved{border-top-color:#8c6b2f}.case-proof-card.missing{border-top-color:#245c49}.case-proof-card strong{display:block;font-size:.72rem;letter-spacing:.06em;text-transform:uppercase;margin-bottom:.42rem}.case-proof-card p{margin:0;line-height:1.55}
      .case-evidence-legend{display:flex;gap:.45rem;flex-wrap:wrap;margin:1rem 0}.case-evidence-legend span{border-radius:999px;padding:.28rem .58rem;background:#eef2f1;font-size:.72rem;font-weight:820;letter-spacing:.035em}
      .case-issue-register{background:#eef3f4}.case-issue-register .shell{max-width:1180px}.case-issue-intro{max-width:880px}.case-issue-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;margin-top:1rem}.case-issue-card{background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:16px;padding:1rem;box-shadow:0 10px 24px rgba(19,37,45,.05)}.case-issue-head{display:flex;justify-content:space-between;gap:.8rem;align-items:flex-start}.case-issue-id{font-weight:900;color:#8c2f2c}.case-issue-priority{border-radius:999px;background:#13252d;color:#fff;padding:.22rem .5rem;font-size:.72rem;font-weight:850}.case-issue-status{font-weight:760;color:#536d79;margin:.25rem 0 .7rem}.case-issue-card details{border-top:1px solid rgba(19,37,45,.12);padding:.55rem 0}.case-issue-card summary{cursor:pointer;font-weight:820}.case-issue-card details p{margin:.45rem 0 0}.case-issue-meta{font-size:.82rem;color:#5f6a6e}.case-issue-card a{display:inline-block;margin-top:.55rem;font-weight:850}.case-counsel{display:inline-block;margin:.45rem 0;border-radius:999px;background:#fff0c6;padding:.25rem .55rem;font-size:.72rem;font-weight:850}
      .case-context-section{background:#f4f1ea}.case-context-card{max-width:1120px;margin:0 auto;background:#fff;border:1px solid rgba(19,37,45,.16);border-left:6px solid #8c6b2f;border-radius:0 16px 16px 0;padding:1rem 1.15rem}.case-context-top{display:flex;justify-content:space-between;gap:.75rem;flex-wrap:wrap}.case-context-eyebrow{font-size:.72rem;font-weight:900;letter-spacing:.07em;text-transform:uppercase;color:#7b4c22}.case-context-phase{font-size:.78rem;font-weight:850;background:#eef2f1;border-radius:999px;padding:.25rem .55rem}.case-context-card h2{margin:.35rem 0}.case-context-question{font-weight:750}.case-context-rule{background:#f7fafb;border-radius:12px;padding:.7rem .85rem}.case-context-actions{display:flex;gap:.65rem;flex-wrap:wrap}.case-context-actions a{font-weight:850}.case-context-boundary{font-size:.88rem;color:#5f6a6e}
      .case-update-entry{margin-top:1.25rem}.case-update-entry .material-update{border-left-color:#245c49}
      .case-live-boundary{border-left:5px solid #536d79;background:#f4f8fa;padding:.8rem 1rem;border-radius:0 12px 12px 0;margin:1rem 0;font-weight:720}
      @media(max-width:980px){.case-proof-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.case-issue-grid{grid-template-columns:1fr}}
      @media(max-width:620px){.case-proof-grid{grid-template-columns:1fr}.case-hub-strip .shell{padding-left:1rem;padding-right:1rem}.case-status-card{padding-left:1rem;padding-right:1rem}}
    `;
    document.head.appendChild(style);
  }

  function installHubStrip() {
    if (document.querySelector('[data-case-hub-strip]')) return;
    const header = document.querySelector('header.site-header');
    if (!header) return;
    const strip = document.createElement('div');
    strip.className = 'case-hub-strip';
    strip.dataset.caseHubStrip = 'true';
    strip.innerHTML = `<div class="shell"><strong>${esc(copy.hubLabel)}</strong><a href="${routes.control}">${esc(copy.control)}</a><a href="${routes.investigation}">${esc(copy.investigation)}</a><a href="${routes.method}">${esc(copy.method)}</a><a href="${routes.corrections}">${esc(copy.corrections)}</a></div>`;
    header.insertAdjacentElement('afterend', strip);
  }

  function installHomepageStatus() {
    const homeEs = path === '/por-derecho/es/';
    const homeEn = path === '/por-derecho/en/';
    if (!homeEs && !homeEn) return;
    if (document.querySelector('[data-case-status-band]')) return;
    const target = document.querySelector('.priority-band') || document.querySelector('main > .hero');
    if (!target) return;
    const section = document.createElement('section');
    section.className = 'case-status-band';
    section.dataset.caseStatusBand = 'true';
    section.innerHTML = `<div class="shell"><div class="case-status-card"><p class="eyebrow">${esc(copy.homeEyebrow)}</p><h2>${esc(copy.homeTitle)}</h2><p>${esc(copy.homeBody)}</p><div class="case-status-actions"><a href="${routes.control}">${esc(copy.openControl)} →</a><a class="secondary" href="${routes.investigation}">${esc(copy.openInvestigation)} →</a><a class="secondary" href="${routes.corrections}">${esc(copy.openCorrections)} →</a></div></div></div>`;
    target.insertAdjacentElement('afterend', section);
  }

  function installCanonicalOpening() {
    const canonical = path === `${routes.investigation}/`.replace(/\/\/$/, '/') || path === routes.investigation;
    if (!canonical) return;
    document.title = copy.canonicalTitle;
    const description = document.querySelector('meta[name="description"]');
    if (description) description.setAttribute('content', copy.canonicalDescription);
    const h1 = document.querySelector('main .hero h1');
    if (h1) h1.textContent = copy.canonicalH1;
    const allegation = document.querySelector('main .hero .allegation');
    if (!allegation || document.querySelector('[data-case-proof-panel]')) return;
    const panel = document.createElement('div');
    panel.className = 'case-proof-panel';
    panel.dataset.caseProofPanel = 'true';
    panel.innerHTML = `<h2>${esc(copy.proofTitle)}</h2><div class="case-proof-grid"><article class="case-proof-card"><strong>${esc(copy.documented)}</strong><p>${esc(copy.documentedBody)}</p></article><article class="case-proof-card alleged"><strong>${esc(copy.alleged)}</strong><p>${esc(copy.allegedBody)}</p></article><article class="case-proof-card not-proved"><strong>${esc(copy.notProved)}</strong><p>${esc(copy.notProvedBody)}</p></article><article class="case-proof-card missing"><strong>${esc(copy.missing)}</strong><p>${esc(copy.missingBody)}</p></article></div><div class="case-status-actions"><a href="${routes.control}">${esc(copy.openControl)} →</a><a class="secondary" href="${routes.corrections}">${esc(copy.openCorrections)} →</a></div><p class="case-live-boundary">${esc(copy.liveBoundary)}</p>`;
    allegation.insertAdjacentElement('afterend', panel);
  }

  function installEvidenceLegend() {
    const eligible = [routes.control, routes.investigation, routes.corrections, routes.notary, routes.registry].includes(path);
    if (!eligible || document.querySelector('[data-case-evidence-legend]')) return;
    const main = document.querySelector('main');
    const hero = main?.querySelector(':scope > .hero, :scope > .psr-control-hero');
    if (!main || !hero) return;
    const legend = document.createElement('div');
    legend.className = 'shell case-evidence-legend';
    legend.dataset.caseEvidenceLegend = 'true';
    const labels = isEs ? ['HECHO DOCUMENTADO','DECLARACIÓN DE FUENTE','ALEGACIÓN POR DERECHO','INFERENCIA','DISPUTADO/CORREGIDO','PREGUNTA ABIERTA','RESULTADO OFICIAL','VALIDACIÓN LETRADA','RESPUESTA INVITADA'] : ['DOCUMENTED FACT','SOURCE STATEMENT','POR DERECHO ALLEGATION','INFERENCE','DISPUTED/CORRECTED','OPEN QUESTION','OFFICIAL OUTCOME','COUNSEL VALIDATION','RESPONSE INVITED'];
    legend.innerHTML = labels.map(label => `<span>${esc(label)}</span>`).join('');
    hero.insertAdjacentElement('afterend', legend);
  }

  async function fetchRegister() {
    const response = await fetch(`${base}/assets/data/criminal-engineering-investigation-v1.json?v=20260819b`, { cache: 'no-store' });
    if (!response.ok) throw new Error(`Issue register HTTP ${response.status}`);
    return response.json();
  }

  function issueCard(issue) {
    const title = issue[`title_${lang}`] || issue.title_en || issue.id;
    const status = issue[`status_${lang}`] || issue.status;
    const documented = issue[`documented_${lang}`] || '';
    const notProved = issue[`not_proved_${lang}`] || '';
    const defence = issue[`strongest_defence_${lang}`] || '';
    const next = issue[`decisive_next_source_${lang}`] || '';
    const route = absRoute(issue[`route_${lang}`]);
    return `<article class="case-issue-card" data-ce-issue="${esc(issue.id)}"><div class="case-issue-head"><div><span class="case-issue-id">${esc(issue.id)}</span><h3>${esc(title)}</h3></div><span class="case-issue-priority">${esc(issue.priority)}</span></div><p class="case-issue-status">${esc(status)}</p>${issue.counsel_gate ? `<span class="case-counsel">${esc(copy.counsel)}</span>` : ''}<details><summary>${esc(copy.documentedLabel)}</summary><p>${esc(documented)}</p></details><details><summary>${esc(copy.notProvedLabel)}</summary><p>${esc(notProved)}</p></details><details><summary>${esc(copy.defenceLabel)}</summary><p>${esc(defence)}</p></details><details><summary>${esc(copy.nextSourceLabel)}</summary><p>${esc(next)}</p></details><p class="case-issue-meta">${esc(copy.lastReviewed)}: ${esc(issue.last_reviewed || '')}</p><a href="${route}">${esc(copy.openIssue)} →</a></article>`;
  }

  async function installIssueRegister() {
    const isControl = path === routes.control;
    const isInvestigation = path === routes.investigation;
    if (!isControl && !isInvestigation) return;
    if (document.querySelector('[data-case-issue-register]')) return;
    try {
      const data = await fetchRegister();
      const issues = isInvestigation ? data.priority_issues.filter(issue => issue.priority === 'P0') : data.priority_issues;
      const section = document.createElement('section');
      section.className = 'section case-issue-register';
      section.dataset.caseIssueRegister = 'true';
      section.innerHTML = `<div class="shell"><h2>${esc(copy.issueTitle)}</h2><p class="case-issue-intro">${esc(copy.issueIntro)}</p><div class="case-issue-grid">${issues.map(issueCard).join('')}</div>${isInvestigation ? `<div class="case-status-actions"><a href="${routes.control}">${esc(copy.openControl)} →</a></div>` : ''}</div>`;
      if (isControl) {
        const audit = document.querySelector('#auditar');
        if (audit) audit.insertAdjacentElement('beforebegin', section);
        else document.querySelector('main')?.append(section);
      } else {
        const phases = [...document.querySelectorAll('main > section')].find(sectionNode => /ocho fases|eight phases/i.test(sectionNode.innerText));
        if (phases) phases.insertAdjacentElement('afterend', section);
        else document.querySelector('main')?.append(section);
      }
    } catch (error) {
      console.warn('Case issue register unavailable', error);
    }
  }

  function contextMatch() {
    return categoryRules.find(rule => rule.fragments.some(fragment => path.includes(fragment)));
  }

  function removeLegacyGateways() {
    document.getElementById('reverse-engineering-360-gateway-20260819')?.remove();
    document.querySelectorAll('[data-criminal-engineering-gateway]').forEach(node => node.remove());
  }

  function installCompactContext() {
    const excluded = [routes.control, routes.investigation, routes.corrections, routes.notary, routes.registry, `${base}/es/`, `${base}/en/`];
    if (excluded.includes(path) || document.querySelector('[data-case-context-gateway]')) return;
    const match = contextMatch();
    if (!match) return;
    const data = isEs ? match.es : match.en;
    const main = document.querySelector('main');
    const hero = main?.querySelector(':scope > .hero, :scope > section.hero, :scope > .dossier-hero, :scope > .cnmv-hero, :scope > .mhero, :scope > .psr-control-hero');
    if (!main || !hero) return;
    const section = document.createElement('section');
    section.className = 'section case-context-section';
    section.dataset.caseContextGateway = 'true';
    section.dataset.caseContextCategory = match.id;
    section.innerHTML = `<div class="shell"><div class="case-context-card"><div class="case-context-top"><span class="case-context-eyebrow">${esc(copy.contextEyebrow)}</span><span class="case-context-phase">${esc(isEs ? 'Fase' : 'Phase')} ${esc(match.phase)} · ${esc(match.issues)}</span></div><h2>${esc(data[0])}</h2><p class="case-context-question">${esc(data[1])}</p><p class="case-context-rule"><strong>${esc(copy.requiredProof)}:</strong> ${esc(copy.requiredProofBody)}.</p><p class="case-context-boundary">${esc(copy.contextBoundary)}</p><div class="case-context-actions"><a href="${routes.control}">${esc(copy.openControl)} →</a><a href="${routes.investigation}">${esc(copy.openInvestigation)} →</a><a href="${routes.method}">${esc(copy.method)} →</a></div></div></div>`;
    hero.insertAdjacentElement('afterend', section);
  }

  function keepOneContextModule() {
    removeLegacyGateways();
    installCompactContext();
    const observer = new MutationObserver(() => {
      const legacy = document.getElementById('reverse-engineering-360-gateway-20260819') || document.querySelector('[data-criminal-engineering-gateway]');
      if (legacy) {
        removeLegacyGateways();
        installCompactContext();
      }
    });
    observer.observe(document.documentElement, { childList: true, subtree: true });
    window.setTimeout(() => observer.disconnect(), 7000);
  }

  function installUpdateEntry() {
    const isUpdates = path === routes.updates;
    if (!isUpdates || document.querySelector('[data-case-update-entry]')) return;
    const status = document.querySelector('.update-status strong');
    if (status) status.textContent = isEs ? '19 agosto 2026' : '19 August 2026';
    const firstSection = document.querySelector('main .updates-section');
    if (!firstSection) return;
    const wrapper = document.createElement('section');
    wrapper.className = 'updates-section case-update-entry';
    wrapper.dataset.caseUpdateEntry = 'true';
    wrapper.innerHTML = `<div class="shell"><section class="date-group"><h2>${esc(copy.updateHeading)}</h2><div class="update-stream"><article class="material-update institutional"><div class="update-meta"><span class="new">${esc(copy.updateNew)}</span><span>${esc(copy.updateTag)}</span></div><h3>${esc(copy.updateTitle)}</h3><p>${esc(copy.updateBody)}</p><p>${esc(copy.liveBoundary)}</p><div class="update-actions"><a class="button" href="${routes.control}">${esc(copy.openControl)} →</a><a class="button secondary" href="${routes.corrections}">${esc(copy.openCorrections)} →</a></div></article></div></section></div>`;
    firstSection.insertAdjacentElement('beforebegin', wrapper);
  }

  function markTechnicalLiveBoundary() {
    const eligible = [routes.control, routes.investigation].includes(path);
    if (!eligible || document.querySelector('[data-live-boundary-note]')) return;
    const main = document.querySelector('main');
    const target = main?.querySelector(':scope > .hero, :scope > .psr-control-hero');
    if (!target) return;
    const note = document.createElement('div');
    note.className = 'shell case-live-boundary';
    note.dataset.liveBoundaryNote = 'true';
    note.textContent = copy.liveBoundary;
    target.insertAdjacentElement('afterend', note);
  }

  function init() {
    addStyles();
    installHubStrip();
    installHomepageStatus();
    installCanonicalOpening();
    installEvidenceLegend();
    installIssueRegister();
    keepOneContextModule();
    installUpdateEntry();
    markTechnicalLiveBoundary();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
