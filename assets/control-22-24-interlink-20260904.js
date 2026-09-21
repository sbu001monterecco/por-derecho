(() => {
  'use strict';

  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  const lang = (document.documentElement.lang || (path.includes('/en/') ? 'en' : 'es'))
    .toLowerCase().startsWith('en') ? 'en' : 'es';

  const routes = {
    dp1901: lang === 'en' ? '/por-derecho/en/dp-1901-2026/' : '/por-derecho/es/dp-1901-2026/',
    c22: lang === 'en' ? '/por-derecho/en/control-22-insolvency-administrator-complaint/' : '/por-derecho/es/control-22-denuncia-administrador-concursal/',
    dp1956: lang === 'en' ? '/por-derecho/en/dp-1956-2026/' : '/por-derecho/es/dp-1956-2026/',
    c24: lang === 'en' ? '/por-derecho/en/control-24-insolvency-judge-complaint-36-2012/' : '/por-derecho/es/control-24-denuncia-juez-concurso-36-2012/',
    judge: lang === 'en' ? '/por-derecho/en/insolvency-36-2012-mercantile-court-1/' : '/por-derecho/es/concurso-36-2012-magistrado-juez/',
    ac: lang === 'en' ? '/por-derecho/en/insolvency-36-2012-insolvency-administrator/' : '/por-derecho/es/concurso-36-2012-administrador-concursal/',
    register: '/por-derecho/data/three-track-full-digitisation-20260904.json'
  };

  const relevantFragments = [
    'dp-1901-2026', 'dp-1956-2026', 'control-22-insolvency-administrator-complaint',
    'control-22-denuncia-administrador-concursal', 'control-24-insolvency-judge-complaint-36-2012',
    'control-24-denuncia-juez-concurso-36-2012', 'concurso-36-2012-administrador-concursal',
    'insolvency-36-2012-insolvency-administrator', 'concurso-36-2012-magistrado-juez',
    'insolvency-36-2012-mercantile-court-1', 'concurso-36-2012-separacion-ac-honorarios',
    'insolvency-36-2012-administrator-removal-fees', 'cgpj-supervision-masa-activa',
    'cgpj-insolvency-estate-supervision', 'fiscalia-dip-2-2026', 'unitary-criminal-digest-2026-09-03',
    'unitary-criminal-reverse-engineering', 'insolvency-36-2012-unitary-criminal-forensic-analysis'
  ];

  const isHome = /\/(?:por-derecho\/)?(?:es\/|en\/)?$/.test(path);
  if (!isHome && !relevantFragments.some(fragment => path.includes(fragment))) return;

  const pageKind = path.includes('dp-1901-2026') ? 'dp1901'
    : path.includes('dp-1956-2026') ? 'dp1956'
    : (path.includes('control-24-denuncia-juez-concurso-36-2012') || path.includes('control-24-insolvency-judge-complaint-36-2012')) ? 'c24'
    : (path.includes('control-22-denuncia-administrador-concursal') || path.includes('control-22-insolvency-administrator-complaint')) ? 'c22'
    : 'context';

  const sharedEvents = lang === 'en' ? [
    ['Community authority / debt / voting', 'Private actors: alleged creation and use of the documentary authority layer.', 'Insolvency administrator: what was known, verified, relied upon, reported or left uncorrected.', 'Judicial layer: what reached the court and what decision or supervisory response followed.'],
    ['7 June 2018 material control', 'Private-actor conduct, access, security and control are tested actor by actor.', 'The AC question is knowledge, authority, preservation, reporting and restoration — not attribution of the physical acts.', 'The judicial question is notice, protection requests and later decisions — not attribution of the takeover itself.'],
    ['2018 funded exit', 'Private layer: knowledge, motive, interference and beneficiary questions.', 'AC layer: estate preservation, payoff, facilitation and accounting duties.', 'Judicial layer: knowledge, quantified conditions, interim protection and decision sequence.'],
    ['28 Nov 2018 OB REM / €400k and 24 Oct 2019 non-validation', 'Private layer: participation, benefit and downstream use.', 'AC layer: authority, safeguarding, accounting, restoration and reporting.', 'Judicial layer: non-validation, implementation and consistency of later supervision.'],
    ['Credit / threshold / 2021 bidding / 2022 adjudication', 'Private layer: offer, access, information, control and beneficiary questions.', 'AC layer: calculation, reporting, equal-treatment and implementation questions.', 'Judicial layer: scope of orders, res judicata, competition and final decision bridge.'],
    ['HNT / MYND / RICPE / later operation', 'Private layer: downstream control, commercialisation and benefit allegations.', 'AC layer: later evidence only where it bears on knowledge, restoration, accounts or continuing consequence.', 'Judicial layer: later context does not prove historical judicial knowledge.']
  ] : [
    ['Autoridad comunitaria / deuda / voto', 'Actores privados: creación y uso alegados de la capa documental de autoridad.', 'Administrador Concursal: qué conoció, verificó, asumió, comunicó o dejó sin corregir.', 'Capa judicial: qué llegó al órgano y qué respuesta decisoria o supervisora siguió.'],
    ['7 junio 2018 · control material', 'Conducta privada, acceso, seguridad y control se examinan actor por actor.', 'La pregunta del AC es conocimiento, autoridad, preservación, comunicación y restitución; no se le atribuyen los actos físicos por asociación.', 'La pregunta judicial es aviso, peticiones de protección y decisiones posteriores; no autoría material del control.'],
    ['Salida financiada de 2018', 'Capa privada: conocimiento, motivo, interferencia y beneficiario alegados.', 'Capa AC: preservación de masa, payoff, facilitación y deberes contables.', 'Capa judicial: conocimiento, condiciones cuantificadas, protección temporal y secuencia decisoria.'],
    ['OB REM 28/11/2018 / €400k y no convalidación 24/10/2019', 'Capa privada: participación, beneficio y uso posterior.', 'Capa AC: autoridad, salvaguarda, contabilidad, restitución y reporte.', 'Capa judicial: no convalidación, ejecución de sus efectos y consistencia de la supervisión posterior.'],
    ['Crédito / umbral / licitación 2021 / adjudicación 2022', 'Capa privada: oferta, acceso, información, control y beneficio.', 'Capa AC: cálculo, reporte, igualdad material e implementación.', 'Capa judicial: alcance de autos, cosa juzgada, competencia efectiva y puente decisorio final.'],
    ['HNT / MYND / RICPE / operación posterior', 'Capa privada: control, comercialización y beneficio posteriores alegados.', 'Capa AC: solo cuando la prueba posterior incide en conocimiento, restitución, cuentas o consecuencia continuada.', 'Capa judicial: el contexto posterior no demuestra conocimiento histórico del magistrado.']
  ];

  const copy = lang === 'en' ? {
    eyebrow: 'FULL DIGITISATION · THREE SEPARATE TRACKS · ONE EVIDENTIAL CONTEXT',
    title: 'DP 1901/2026, DP 1956/2026 and Control 24 now read together without being merged.',
    lead: 'The public layer now exposes a source-complete, page-aware digest of the two operative complaints and the judge-related filing. The raw private pleadings are not published: personal data, signatures, private contact details, verification codes and protected material remain outside public Git.',
    boundary: 'Procedures separate · knowledge connected · evidence cross-referenced · custody coordinated · attribution actor-specific. Shared evidence never transfers guilt, intent or responsibility.',
    fullData: 'Open structured full-digitisation control',
    read1901: 'DP 1901 / private actors',
    read1956: 'DP 1956 / insolvency administrator',
    read24: 'Control 24 / judicial layer',
    contextTitle: 'One event, three legally different questions',
    sourceTitle: 'What “full digitisation” means here',
    sourceText: 'Every page of the controlling text-layer sources has been processed and indexed for the public digest. The public presentation is structured, redacted and traceable; it is not a publication of the raw private pleading.',
    dp1901Title: 'DP 1901/2026 · Control 21 / NEXUS 36',
    dp1901Text: '69-page base complaint reported filed on 25 June 2026, plus a 7-page expansion reported filed on 9 July. The base is organised through persons/entities, evidential discipline, territorial/autonomous scope, matrix questions, detailed facts, actor-specific attribution, damage/benefit/causation, provisional legal characterisation, limitation, asymmetric evidence, requested measures, protection/traceability and relief. The expansion adds the non-fragmentation rule, apparent-authority → decision → value model, JDAM/LPAM-specific modules, RICPE/HNT/MYND, digital/customer assets, commercialisation, custodians and prioritised measures.',
    dp1956Title: 'DP 1956/2026 · Control 22 / Insolvency Administrator',
    dp1956Text: '55-page operative complaint reported presented on 18 June 2026. Its text is organised around a limited criminal object; recovery routes; entity separation; removal proceedings; estate definition and enhanced duties; early notice; the disputed Community/debt structure; CAM/Promontoria; the 2018 funded exit; the 7 June material-control event; later validation/authority questions; and the September 2018 request for an operational payoff figure. The current controlled status remains provisional dismissal communicated on 21 July 2026.',
    c24Title: 'Control 24 · judge-related complaint/notitia',
    c24Text: '79-page signed package reported presented on 18 June 2026, containing the principal complaint and selected annexes, plus a dependent 10-page supplement presented on 25 June. Its five documentary modules are funded exit/judicial knowledge; recognised credit/threshold/res judicata; OB REM/non-validation; bidding/adjudication; and legal identity of creditor/enforcing party/bidder/adjudicatee/title holder. Daily locator 24 is not a case number; allocation and current judicial status remain unverified.',
    proof: 'Source boundary',
    proofText: 'A complaint proves the content of the allegation and request. It does not prove criminality. Later operation, registration, financing, public support or institutional receipt do not validate earlier title, authority, causation or guilt.'
  } : {
    eyebrow: 'DIGITALIZACIÓN ÍNTEGRA · TRES VÍAS SEPARADAS · UN CONTEXTO PROBATORIO',
    title: 'DP 1901/2026, DP 1956/2026 y Control 24 se leen ya conjuntamente sin fundirse.',
    lead: 'La capa pública expone ahora un digesto completo, por páginas y por módulos, de las dos denuncias operativas y de la actuación relativa al juez. No se publican los escritos privados en bruto: datos personales, firmas, contactos privados, códigos de verificación y material protegido permanecen fuera del Git público.',
    boundary: 'Procedimientos separados · conocimiento conectado · prueba cruzada · custodia coordinada · atribución actor-específica. La prueba compartida nunca transfiere culpabilidad, dolo o responsabilidad.',
    fullData: 'Abrir control estructurado de digitalización íntegra',
    read1901: 'DP 1901 / actores privados',
    read1956: 'DP 1956 / Administrador Concursal',
    read24: 'Control 24 / capa judicial',
    contextTitle: 'Un mismo evento, tres preguntas jurídicas distintas',
    sourceTitle: 'Qué significa “digitalización íntegra” aquí',
    sourceText: 'Se ha procesado e indexado la capa textual de todas las páginas de las fuentes controladoras para construir el digesto público. La presentación pública es estructurada, redactada y trazable; no es la publicación del escrito privado en bruto.',
    dp1901Title: 'DP 1901/2026 · Control 21 / NEXUS 36',
    dp1901Text: 'Denuncia base de 69 páginas reportada como presentada el 25 de junio de 2026, más una ampliación de 7 páginas reportada como presentada el 9 de julio. La base se ordena por personas/entidades, disciplina probatoria, autonomía y competencia, preguntas matrices, relación circunstanciada de hechos, atribución actor-específica, daños/beneficios/nexo causal, calificación provisional, prescripción, asimetría de prueba, diligencias, protección/trazabilidad y suplico. La ampliación añade la lectura no fragmentada, el modelo autoridad aparente → decisión → valor, módulos específicos JDAM/LPAM, RICPE/HNT/MYND, activos digitales/clientela, comercialización, custodios y diligencias priorizadas.',
    dp1956Title: 'DP 1956/2026 · Control 22 / Administrador Concursal',
    dp1956Text: 'Denuncia operativa de 55 páginas reportada como presentada el 18 de junio de 2026. Se estructura alrededor de un objeto penal limitado; vías de recuperación; separación societaria; separación del AC; identificación de la masa y deber reforzado; aviso temprano; estructura Comunidad/deuda controvertida; CAM/Promontoria; salida financiada; evento de control material de 7 de junio; cuestiones posteriores de autoridad/validación; y solicitud de septiembre de 2018 de una cifra operativa para concluir el concurso. El estado controlado sigue siendo sobreseimiento provisional comunicado el 21 de julio de 2026.',
    c24Title: 'Control 24 · denuncia/notitia relativa al juez',
    c24Text: 'Paquete firmado de 79 páginas reportado como presentado el 18 de junio de 2026, con denuncia principal y anexos seleccionados, más una aportación dependiente de 10 páginas presentada el 25 de junio. Sus cinco módulos son salida financiada/conocimiento judicial; crédito/umbral/cosa juzgada; OB REM/no convalidación; licitación/adjudicación; e identidad jurídica de acreedor, ejecutante, oferente, adjudicatario y titular. El localizador diario 24 no es número de causa; reparto y estado judicial actual siguen sin verificarse.',
    proof: 'Límite de fuente',
    proofText: 'Una denuncia acredita qué se alegó y qué se pidió; no acredita la comisión de delito. Operación posterior, inscripción, financiación, ayudas o recepción institucional tampoco validan por sí solas título, autoridad, causalidad o culpabilidad anteriores.'
  };

  const addStyle = () => {
    if (document.getElementById('pd-three-track-style')) return;
    const style = document.createElement('style');
    style.id = 'pd-three-track-style';
    style.textContent = `
      .pd-3t{background:linear-gradient(135deg,#13262e,#3b2c37 58%,#72571d);color:#fff;padding:2.4rem 0;position:relative;z-index:2}
      .pd-3t.pd-3t-home{max-width:1180px;margin:1.25rem auto;border-radius:24px;overflow:hidden;box-shadow:0 18px 44px rgba(15,34,42,.22)}
      .pd-3t h2,.pd-3t h3{color:#fff}.pd-3t h2{max-width:1000px;margin:.25rem 0 .7rem;font-size:clamp(1.8rem,4vw,3rem)}.pd-3t p{color:#f1f4f4;line-height:1.62}
      .pd-3t-ey{font-size:.73rem;font-weight:900;letter-spacing:.08em;text-transform:uppercase;color:#f2d57b}.pd-3t-boundary{border-left:4px solid #f2d57b;padding-left:.9rem;max-width:1100px}
      .pd-3t-links{display:flex;gap:.52rem;flex-wrap:wrap;margin-top:1rem}.pd-3t-links a{display:inline-block;background:#f2d57b;color:#17272e;text-decoration:none;border-radius:999px;padding:.55rem .8rem;font-weight:850}
      .pd-3t-source{margin-top:1.2rem;background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.2);border-radius:16px;padding:1rem 1.1rem}.pd-3t-source strong{color:#fff}
      .pd-3t-detail{background:#f5f2ea;color:#17272e;padding:2.6rem 0}.pd-3t-detail h2,.pd-3t-detail h3{color:#17272e}.pd-3t-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem}.pd-3t-card{background:#fff;border:1px solid rgba(19,38,46,.14);border-radius:18px;padding:1.2rem;border-top:5px solid #8a6a22}.pd-3t-card p{color:#263a42}.pd-3t-card a{font-weight:850}
      .pd-3t-context{background:#fff;padding:2.5rem 0}.pd-3t-event{display:grid;grid-template-columns:minmax(180px,.65fr) repeat(3,minmax(0,1fr));gap:.65rem;margin:.7rem 0}.pd-3t-event>div{border:1px solid rgba(19,38,46,.14);border-radius:12px;padding:.85rem;background:#fafafa}.pd-3t-event .pd-3t-label{background:#17272e;color:#fff;font-weight:850}.pd-3t-event strong{display:block;font-size:.72rem;text-transform:uppercase;letter-spacing:.05em;margin-bottom:.25rem}
      .pd-3t-proof{margin-top:1rem;border-left:5px solid #315c7b;background:#eef5f7;padding:1rem 1.1rem;border-radius:10px}
      @media(max-width:900px){.pd-3t-grid{grid-template-columns:1fr}.pd-3t-event{grid-template-columns:1fr}.pd-3t.pd-3t-home{margin:1rem .7rem}}
    `;
    document.head.appendChild(style);
  };

  const render = () => {
    if (document.querySelector('[data-three-track-digitisation]')) return;
    addStyle();
    const main = document.querySelector('main') || document.body;

    const intro = document.createElement('section');
    intro.className = 'pd-3t' + (isHome ? ' pd-3t-home' : '');
    intro.setAttribute('data-three-track-digitisation', '20260904');
    intro.innerHTML = `<div class="shell"><p class="pd-3t-ey">${copy.eyebrow}</p><h2>${copy.title}</h2><p>${copy.lead}</p><p class="pd-3t-boundary">${copy.boundary}</p><div class="pd-3t-links"><a href="${routes.dp1901}">${copy.read1901}</a><a href="${routes.dp1956}">${copy.read1956}</a><a href="${routes.c24}">${copy.read24}</a><a href="${routes.register}">${copy.fullData}</a></div><div class="pd-3t-source"><strong>${copy.sourceTitle}.</strong> ${copy.sourceText}</div></div>`;

    if (isHome) {
      const sections = main.querySelectorAll(':scope > section');
      if (sections.length > 1) main.insertBefore(intro, sections[1]); else main.appendChild(intro);
      return;
    }

    const firstSection = main.querySelector(':scope > section');
    if (firstSection && firstSection.nextSibling) main.insertBefore(intro, firstSection.nextSibling); else main.appendChild(intro);

    if (['dp1901','dp1956','c24','c22'].includes(pageKind)) {
      const detail = document.createElement('section');
      detail.className = 'pd-3t-detail';
      detail.innerHTML = `<div class="shell"><div class="pd-3t-grid">
        <article class="pd-3t-card"><h3>${copy.dp1901Title}</h3><p>${copy.dp1901Text}</p><p><a href="${routes.dp1901}">${copy.read1901} →</a></p></article>
        <article class="pd-3t-card"><h3>${copy.dp1956Title}</h3><p>${copy.dp1956Text}</p><p><a href="${routes.dp1956}">${copy.read1956} →</a></p></article>
        <article class="pd-3t-card"><h3>${copy.c24Title}</h3><p>${copy.c24Text}</p><p><a href="${routes.c24}">${copy.read24} →</a></p></article>
      </div><div class="pd-3t-proof"><strong>${copy.proof}.</strong> ${copy.proofText}</div></div>`;
      main.appendChild(detail);

      const context = document.createElement('section');
      context.className = 'pd-3t-context';
      const labels = lang === 'en' ? ['Event / document','DP 1901','DP 1956','Control 24'] : ['Evento / documento','DP 1901','DP 1956','Control 24'];
      context.innerHTML = `<div class="shell"><h2>${copy.contextTitle}</h2>${sharedEvents.map(ev => `<div class="pd-3t-event"><div class="pd-3t-label">${ev[0]}</div><div><strong>${labels[1]}</strong>${ev[1]}</div><div><strong>${labels[2]}</strong>${ev[2]}</div><div><strong>${labels[3]}</strong>${ev[3]}</div></div>`).join('')}<p class="pd-3t-proof"><strong>${copy.proof}.</strong> ${copy.boundary}</p></div>`;
      main.appendChild(context);
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render, { once: true });
  else render();
})();
