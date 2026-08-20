(() => {
  const currentScript = document.currentScript;
  const path = location.pathname.replace(/\/+$/, '/') || '/';
  const isEn = /\/en\//.test(path);
  const lang = isEn ? 'en' : 'es';
  const root = `/por-derecho/${lang}/`;
  const p = (slug = '') => `${root}${slug}`;
  const t = (es, en) => isEn ? en : es;
  const RELEASE = '2026-08-18-optimum-reader-journey-v1';
  const RELEASE_DATE = t('20 agosto 2026', '20 August 2026');

  const communityUrl = p(isEn ? 'community-instrumentalisation/' : 'comunidad-instrumentalizacion/');
  const actasUrl = p(isEn ? 'community-instrumentalisation/minutes-2011-2022/' : 'comunidad-instrumentalizacion/actas-2011-2022/');
  const controlUrl = p(isEn ? 'sun-park-takeover-7-june-2018/' : 'toma-control-sun-park-7-junio-2018/');
  const insolvencyUrl = p(isEn ? 'lpb-insolvency/' : 'insolvencia-lpb/');
  const ricpeUrl = p('ric-private-equity-sun-park/');
  const ricpeControlsUrl = p(isEn ? 'ricpe-documentary-accountability/' : 'ricpe-responsabilidad-documental/');
  const fundingUrl = p(isEn ? 'same-hotel-multiple-financial-lives/' : 'mismo-hotel-multiples-vidas-financieras/');
  const fundingChainUrl = p(isEn ? 'institutionalisation-chain-ric-eu-incentives/' : 'cadena-instrumentalizacion-ric-fondos-incentivos/');
  const myndUrl = p('hosteltur-sun-park-mynd-yaiza/');
  const recoveryUrl = p(isEn ? 'recovery-restitution-objectives/' : 'objetivos-recuperacion-restitucion/');
  const cleanRoomUrl = p(isEn ? 'public-authority-unitary-case-reconstruction/' : 'reconstruccion-unitaria-autoridades-publicas/');
  const cnmvUrl = p(isEn ? 'cnmv-ricpe-verification/' : 'cnmv-ricpe-verificacion/');
  const incentivesUrl = p(isEn ? 'regional-incentives-gc836-p06/' : 'incentivos-regionales-gc836-p06/');
  const sncaUrl = p(isEn ? 'snca-eu-funds-traceability/' : 'snca-fondos-europeos-trazabilidad/');
  const updatesUrl = p(isEn ? 'updates/' : 'actualizaciones/');
  const collaborateUrl = p(isEn ? 'collaborate/' : 'colaborar/');
  const homeUrl = p('');

  const make = (html) => {
    const template = document.createElement('template');
    template.innerHTML = html.trim();
    return template.content.firstElementChild;
  };

  const ensureCss = () => {
    if (!currentScript || document.querySelector('link[data-optimum-reader-journey]')) return;
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = new URL('optimum-reader-journey-20260818.css?v=20260818a', currentScript.src).href;
    link.dataset.optimumReaderJourney = '20260818';
    document.head.appendChild(link);
  };

  const isHome = new RegExp(`/por-derecho/${lang}/?$`).test(path);
  const isUpdates = /\/(actualizaciones|updates)\/$/.test(path);
  const main = () => document.querySelector('main');
  const hero = () => main()?.querySelector(':scope > .dossier-hero, :scope > .cnmv-hero, :scope > .eu-hero, :scope > .ir-hero, :scope > .hero, :scope > section.hero');

  const firstSubstantiveSection = () => {
    const h = hero();
    return [...(main()?.children || [])].find((node) => node.tagName === 'SECTION' && node !== h && !node.hidden && getComputedStyle(node).display !== 'none');
  };

  const findBySelectors = (selectors = []) => {
    for (const selector of selectors) {
      const node = document.querySelector(selector);
      if (node) return node;
    }
    return null;
  };

  const findSectionByHeading = (patterns = []) => {
    for (const section of main()?.querySelectorAll(':scope > section') || []) {
      const text = section.querySelector('h1,h2,h3')?.textContent?.trim() || '';
      if (patterns.some((pattern) => pattern.test(text))) return section;
    }
    return null;
  };

  const anchorFor = (node, fallbackId) => {
    if (!node) return null;
    if (!node.id) node.id = fallbackId;
    node.classList.add('psr-reader-mode-target');
    return `#${node.id}`;
  };

  const routeConfig = () => {
    if (/\/ric-private-equity-sun-park\/$/.test(path)) return {
      stage: 'RICPE',
      quick: ['#psr-ricpe-cockpit'], guided: ['#psr-ricpe-five-docs'], full: '#pregunta-unitaria',
      previous: { href: controlUrl, title: t('Control material de 2018', '2018 material control'), desc: t('Volver al punto donde acceso y autoridad adquirieron consecuencias físicas.', 'Return to the point where access and authority acquired physical consequences.') },
      next: { href: fundingUrl, title: t('Financiación y apoyo', 'Funding and support'), desc: t('Seguir activo, coste, empleo y euro por cada instrumento.', 'Follow asset, cost, employment and euro across each instrument.') },
      verify: { href: ricpeControlsUrl, title: t('Auditar los controles RICPE', 'Audit RICPE controls'), desc: t('Origen, conflictos, DD, valoración, dispensas, HNT y desembolsos.', 'Origin, conflicts, DD, valuation, waivers, HNT and drawdowns.') },
      actionInstitutional: true
    };
    if (/\/ricpe-(responsabilidad-documental|documentary-accountability)\/$/.test(path)) return {
      stage: t('Controles RICPE', 'RICPE controls'),
      quickHeading: [/2019–2021/i, /governance.*knowledge/i], guidedHeading: [/20–21.*jul/i, /20–21.*july/i], full: ricpeUrl,
      previous: { href: ricpeUrl, title: t('Lectura RICPE de 7 minutos', 'RICPE 7-minute read'), desc: t('Volver a la pregunta ejecutiva y al estado de respuesta.', 'Return to the executive question and response status.') },
      next: { href: fundingUrl, title: t('Conciliar las vidas financieras', 'Reconcile financial lives'), desc: t('Comprobar costes, activos, empleos y valor.', 'Check costs, assets, jobs and value.') },
      verify: { href: cleanRoomUrl, title: t('Abrir sala limpia', 'Open clean room'), desc: t('Contrastar el expediente sin asumir la teoría global.', 'Test the file without adopting the global theory.') },
      actionInstitutional: true
    };
    if (/\/(cnmv-ricpe-verificacion|cnmv-ricpe-verification)\/$/.test(path)) return {
      stage: 'CNMV',
      quick: [isEn ? '#seven-minute-review' : '#revision-7-minutos'], guided: [isEn ? '#what-changed' : '#que-cambio'], full: ricpeUrl,
      previous: { href: ricpeUrl, title: t('Expediente RICPE', 'RICPE file'), desc: t('Ver la cadena interna y la comunicación formal.', 'See the internal chain and formal communication.') },
      next: { href: incentivesUrl, title: t('Incentivos Regionales', 'Regional Incentives'), desc: t('Seguir beneficiario, inversión, empleo, pago y cumplimiento.', 'Follow beneficiary, investment, employment, payment and compliance.') },
      verify: { href: cleanRoomUrl, title: t('Revisión independiente', 'Independent review'), desc: t('Una base factual, competencias separadas.', 'One factual base, separate competences.') },
      actionInstitutional: true
    };
    if (/\/(incentivos-regionales-gc836-p06|regional-incentives-gc836-p06)\/$/.test(path)) return {
      stage: t('Incentivos Regionales', 'Regional Incentives'),
      quickHeading: [/caso en 7 minutos/i, /case in 7 minutes/i], guided: [isEn ? '#open-practice' : '#practica-abierta'], full: fundingChainUrl,
      previous: { href: cnmvUrl, title: 'CNMV / RICPE', desc: t('Volver al origen, gobierno, DD y reentrada del proyecto.', 'Return to project origin, governance, DD and re-entry.') },
      next: { href: sncaUrl, title: t('SNCA / FEDER', 'SNCA / ERDF'), desc: t('Seguir gasto, certificación, verificación y corrección.', 'Follow expenditure, certification, verification and correction.') },
      verify: { href: fundingUrl, title: t('Conciliación económica', 'Economic reconciliation'), desc: t('Comparar activo, factura, empleo y euro.', 'Compare asset, invoice, job and euro.') },
      actionInstitutional: true
    };
    if (/\/(snca-fondos-europeos-trazabilidad|snca-eu-funds-traceability)\/$/.test(path)) return {
      stage: t('SNCA / fondos UE', 'SNCA / EU funds'),
      quickHeading: [/caso en 7 minutos/i, /case in 7 minutes/i], guided: [isEn ? '#open-practice' : '#practica-abierta'], full: fundingUrl,
      previous: { href: incentivesUrl, title: t('Expediente GC/836/P06', 'GC/836/P06 file'), desc: t('Volver a concesión, elegibilidad, empleo y pago.', 'Return to award, eligibility, jobs and payment.') },
      next: { href: cleanRoomUrl, title: t('Matriz interinstitucional', 'Cross-authority matrix'), desc: t('Identificar qué órgano puede comprobar cada premisa.', 'Identify which body can verify each proposition.') },
      verify: { href: fundingChainUrl, title: t('Cadena RIC / fondos / incentivos', 'RIC / funds / incentives chain'), desc: t('Comparar capas jurídicas y económicas sin sumarlas automáticamente.', 'Compare legal and economic layers without automatically adding them.') },
      actionInstitutional: true
    };
    if (/\/(reconstruccion-unitaria-autoridades-publicas|public-authority-unitary-case-reconstruction)\/$/.test(path)) return {
      stage: t('Sala limpia', 'Clean room'),
      quick: ['#un-minuto'], guided: ['#por-institucion'], full: '#sala-limpia',
      previous: { href: sncaUrl, title: t('Fondos UE / SNCA', 'EU funds / SNCA'), desc: t('Volver al flujo de alerta, gasto, verificación y corrección.', 'Return to alert, expenditure, verification and correction.') },
      next: { href: recoveryUrl, title: t('Recuperación y restitución', 'Recovery and restitution'), desc: t('Ver los objetivos patrimoniales, de ingresos, daños y plataforma.', 'See asset, income, damages and platform objectives.') },
      verify: { href: fundingUrl, title: t('Auditoría económica unitaria', 'Unitary economic audit'), desc: t('Probar o descartar solapamientos con una sola conciliación.', 'Prove or rule out overlap through one reconciliation.') },
      actionInstitutional: true
    };
    if (/\/(comunidad-instrumentalizacion|community-instrumentalisation)\/$/.test(path)) return {
      stage: t('Origen / Comunidad', 'Origin / Community'),
      quick: ['#resumen'], guided: ['#psr-community-to-ricpe'], full: actasUrl,
      previous: { href: homeUrl, title: t('Mapa general', 'Case map'), desc: t('Volver a la explicación en 60 segundos.', 'Return to the 60-second explanation.') },
      next: { href: controlUrl, title: t('Control material · 7 junio 2018', 'Material control · 7 June 2018'), desc: t('Ver cuándo la autoridad discutida produjo acceso, seguridad y exclusión.', 'See when disputed authority produced access, security and exclusion.') },
      verify: { href: actasUrl, title: t('Auditar actas y autoridad', 'Audit minutes and authority'), desc: t('Convocatoria, asistencia, poderes, deuda, voto, custodia y mandato.', 'Notice, attendance, proxies, debt, vote, custody and mandate.') }
    };
    if (/\/(toma-control-sun-park-7-junio-2018|sun-park-takeover-7-june-2018)\/$/.test(path)) return {
      stage: t('Control 2018', '2018 control'),
      quick: ['#perimetros-juridicos'], guided: ['#hechos-7-junio'], full: '#prueba-pendiente',
      previous: { href: communityUrl, title: t('Origen / Comunidad', 'Origin / Community'), desc: t('Volver a deuda, voto, autoridad y custodia.', 'Return to debt, vote, authority and custody.') },
      next: { href: ricpeUrl, title: 'RICPE', desc: t('Seguir cómo el activo llegó al proyecto, DD y financiación.', 'Follow how the asset reached project, DD and funding.') },
      verify: { href: cleanRoomUrl, title: t('Contrastar autoridad y consecuencia', 'Test authority and consequence'), desc: t('Separar título, control material, conocimiento y resultado oficial.', 'Separate title, material control, knowledge and official outcome.') }
    };
    if (/\/(insolvencia-lpb|lpb-insolvency)\/$/.test(path)) return {
      stage: t('Concurso', 'Insolvency'),
      quickHeading: [/punto de partida/i, /starting point/i], guidedHeading: [/caus/i, /masa/i, /estate/i], full: p(isEn ? 'insolvency-classification-parallel-lives/' : 'calificacion-concurso-36-2012-vidas-paralelas/'),
      previous: { href: controlUrl, title: t('Control material 2018', '2018 material control'), desc: t('Volver al perímetro físico y extraconcursal.', 'Return to the physical and extra-insolvency perimeter.') },
      next: { href: ricpeUrl, title: 'RICPE', desc: t('Seguir el proyecto y el capital fuera y dentro del concurso.', 'Follow the project and capital outside and within the insolvency.') },
      verify: { href: cleanRoomUrl, title: t('Reconstrucción institucional', 'Institutional reconstruction'), desc: t('Separar actos, funciones, fechas y dependencias.', 'Separate acts, functions, dates and dependencies.') }
    };
    if (/\/(calificacion-concurso-36-2012-vidas-paralelas|insolvency-classification-parallel-lives)\/$/.test(path)) return {
      stage: t('Calificación', 'Classification'),
      quickHeading: [/punto de partida/i, /starting point/i], guided: ['#di248'], full: fundingUrl,
      previous: { href: insolvencyUrl, title: t('Concurso LPB', 'LPB insolvency'), desc: t('Volver al perímetro y causalidad de la insolvencia.', 'Return to insolvency perimeter and causation.') },
      next: { href: ricpeUrl, title: 'RICPE', desc: t('Contrastar la atribución de culpa con las vidas posteriores del activo.', 'Compare attributed fault with the asset’s later lives.') },
      verify: { href: cleanRoomUrl, title: t('Auditoría de actores y fuentes', 'Actor and source audit'), desc: t('Qué alegó o decidió cada persona y con qué material contrario.', 'What each person alleged or decided and with which contrary material.') }
    };
    if (/\/(mismo-hotel-multiples-vidas-financieras|same-hotel-multiple-financial-lives)\/$/.test(path)) return {
      stage: t('Financiación', 'Funding'),
      quick: ['#psr-conversion-matrix'], guidedHeading: [/vidas financieras/i, /financial lives/i], full: fundingChainUrl,
      previous: { href: ricpeUrl, title: 'RICPE', desc: t('Volver a origen, DD, aprobación y desembolso.', 'Return to origin, DD, approval and drawdown.') },
      next: { href: incentivesUrl, title: t('Incentivos Regionales', 'Regional Incentives'), desc: t('Seguir inversión elegible, empleo, pago y cumplimiento.', 'Follow eligible investment, employment, payment and compliance.') },
      verify: { href: sncaUrl, title: t('Auditar fondos UE', 'Audit EU funds'), desc: t('Operación, factura, pago, certificación, auditoría y corrección.', 'Operation, invoice, payment, certification, audit and correction.') }
    };
    if (/\/(cadena-instrumentalizacion-ric-fondos-incentivos|institutionalisation-chain-ric-eu-incentives)\/$/.test(path)) return {
      stage: t('Cadena institucional', 'Institutional chain'),
      quick: ['#psr-authority-before-funds'], guidedHeading: [/matriz/i, /matrix/i], full: fundingUrl,
      previous: { href: ricpeUrl, title: 'RICPE', desc: t('Volver al origen del capital y los controles.', 'Return to capital origin and controls.') },
      next: { href: incentivesUrl, title: t('Incentivos Regionales', 'Regional Incentives'), desc: t('Abrir el expediente especializado GC/836/P06.', 'Open the specialist GC/836/P06 file.') },
      verify: { href: sncaUrl, title: t('SNCA / FEDER', 'SNCA / ERDF'), desc: t('Seguir gestión, certificación, control y recovery.', 'Follow management, certification, control and recovery.') },
      actionInstitutional: true
    };
    if (/\/hosteltur-sun-park-mynd-yaiza\/$/.test(path)) return {
      stage: 'MYND', quickHeading: [/resultado/i, /result/i], guidedHeading: [/document/i, /evidence/i], full: fundingUrl,
      previous: { href: fundingUrl, title: t('Financiación y apoyo', 'Funding and support'), desc: t('Volver a las vidas financieras que sostienen el resultado.', 'Return to the financial lives supporting the outcome.') },
      next: { href: recoveryUrl, title: t('Recuperación', 'Recovery'), desc: t('Ver restitución, ingresos, daños y reconstrucción de la plataforma.', 'See restitution, income, damages and platform rebuilding.') },
      verify: { href: cleanRoomUrl, title: t('Auditar el resultado visible', 'Audit the visible outcome'), desc: t('El resultado no demuestra por sí solo la legitimidad de cada transición.', 'The outcome does not by itself prove the legitimacy of every transition.') }
    };
    if (/\/(objetivos-recuperacion-restitucion|recovery-restitution-objectives)\/$/.test(path)) return {
      stage: t('Recuperación', 'Recovery'), quickHeading: [/objetiv/i, /objective/i], guidedHeading: [/restitu/i, /recover/i], full: collaborateUrl,
      previous: { href: fundingUrl, title: t('Evidencia económica', 'Economic evidence'), desc: t('Volver a activos, costes, ingresos y valor.', 'Return to assets, costs, income and value.') },
      next: { href: collaborateUrl, title: t('Colaborar o aportar prueba', 'Collaborate or provide evidence'), desc: t('Correcciones y documentos verificables reciben trazabilidad.', 'Verifiable corrections and documents receive traceability.') },
      verify: { href: cleanRoomUrl, title: t('Base probatoria', 'Evidence base'), desc: t('Comprobar qué objetivo depende de qué hecho.', 'Check which objective depends on which fact.') }
    };
    return null;
  };

  const visitState = () => {
    let seen = null;
    try { seen = localStorage.getItem('psr:last-reader-release'); } catch (_) { /* local-only optional state */ }
    const state = seen && seen !== RELEASE ? 'new' : seen === RELEASE ? 'current' : 'first';
    try { localStorage.setItem('psr:last-reader-release', RELEASE); } catch (_) { /* no storage required */ }
    return state;
  };

  const updateStatusHtml = () => {
    const state = visitState();
    const label = state === 'new'
      ? t('Nuevo desde su última visita', 'New since your last visit')
      : state === 'current'
        ? t('Registro actual', 'Current record')
        : t('Última actualización verificada', 'Latest verified update');
    return `<strong>${label}:</strong> ${RELEASE_DATE} · <a href="${updatesUrl}">${t('ver cambios materiales', 'see material changes')}</a>`;
  };

  const addProgress = () => {
    if (document.getElementById('psr-reading-progress') || !main()) return;
    const bar = document.createElement('div');
    bar.id = 'psr-reading-progress';
    bar.setAttribute('aria-hidden', 'true');
    document.body.prepend(bar);
    const update = () => {
      const max = document.documentElement.scrollHeight - innerHeight;
      const ratio = max > 0 ? Math.min(1, Math.max(0, scrollY / max)) : 0;
      bar.style.width = `${ratio * 100}%`;
    };
    addEventListener('scroll', update, { passive: true });
    addEventListener('resize', update, { passive: true });
    update();
  };

  const repairRail = () => {
    const rail = document.getElementById('psr-unitary-journey');
    if (!rail) return;
    const anchors = [...rail.querySelectorAll('a')];
    const first = anchors[0];
    if (first && /^(Propiedad|Ownership)$/i.test(first.textContent.trim())) first.remove();
    const remaining = [...rail.querySelectorAll('a')];
    const community = remaining.find((a) => /^(Comunidad|Community)$/i.test(a.textContent.trim()));
    if (community) community.textContent = t('Origen / Comunidad', 'Origin / Community');
    remaining.forEach((a) => a.removeAttribute('aria-current'));

    let current = null;
    if (/actas-2011-2022|minutes-2011-2022|comunidad-instrumentalizacion|community-instrumentalisation/.test(path)) current = community;
    else current = remaining.find((a) => {
      const href = a.getAttribute('href') || '';
      const slug = href.replace(/^.*\/por-derecho\/(es|en)\//, '/');
      return slug !== '/' && path.includes(slug);
    });
    if (current) {
      current.setAttribute('aria-current', 'step');
      requestAnimationFrame(() => current.scrollIntoView({ block: 'nearest', inline: 'center', behavior: 'auto' }));
    }
  };

  const addHomeIntent = () => {
    if (!isHome || document.getElementById('psr-reader-intent')) return;
    document.getElementById('supervisory-practice-home-18aug')?.remove();
    document.querySelectorAll('.psr-home-path').forEach((node) => node.remove());
    const section = make(`
      <section class="psr-intent" id="psr-reader-intent" aria-labelledby="psr-reader-intent-title">
        <div class="shell">
          <div class="psr-intent-head"><div><p class="psr-intent-kicker">${t('EMPIECE POR SU OBJETIVO', 'START WITH YOUR PURPOSE')}</p><h2 id="psr-reader-intent-title">${t('Una historia; cuatro formas de entrar.', 'One story; four ways in.')}</h2><p>${t('Elija profundidad y función. Todas las rutas vuelven a la misma base documental y conservan hechos, alegaciones, inferencias, límites y correcciones.', 'Choose depth and function. Every route returns to the same documentary base and preserves facts, allegations, inferences, limits and corrections.')}</p></div><aside class="psr-intent-status">${updateStatusHtml()}</aside></div>
          <div class="psr-intent-grid">
            <a class="psr-intent-card" href="${isEn ? '#sixty-second-summary' : '#resumen-60-segundos'}"><span class="num">01 · ${t('Primera visita', 'First visit')}</span><strong>${t('Entender en 60 segundos', 'Understand in 60 seconds')}</strong><span>${t('Dominio fragmentado, promoción antes del título, aviso, respuesta y resultado.', 'Fragmented ownership, promotion before title, notice, response and outcome.')}</span><em>${t('Tiempo: 1–2 minutos →', 'Time: 1–2 minutes →')}</em></a>
            <a class="psr-intent-card" href="${cleanRoomUrl}"><span class="num">02 · ${t('Institución / profesional', 'Institution / professional')}</span><strong>${t('Revisar por competencia', 'Review by competence')}</strong><span>${t('CNMV, Incentivos Regionales, fondos UE, Fiscalía, Juzgado, Turismo y otras oficinas.', 'CNMV, Regional Incentives, EU funds, prosecutors, courts, tourism and other offices.')}</span><em>${t('Pregunta finita + producción →', 'Finite question + production →')}</em></a>
            <a class="psr-intent-card" href="#registro"><span class="num">03 · ${t('Lector escéptico', 'Sceptical reader')}</span><strong>${t('Auditar la evidencia', 'Audit the evidence')}</strong><span>${t('Abrir fuentes, estados de prueba, contradicciones, actores y cuestiones pendientes.', 'Open sources, evidence states, contradictions, actors and unresolved questions.')}</span><em>${t('Expediente completo →', 'Full record →')}</em></a>
            <a class="psr-intent-card" href="${recoveryUrl}"><span class="num">04 · ${t('Resultado / participación', 'Outcome / participation')}</span><strong>${t('Recuperación, corrección y contribución', 'Recovery, correction and contribution')}</strong><span>${t('Restitución de activos e ingresos, daños, plataforma futura y aportación documental responsable.', 'Restitution of assets and income, damages, future platform and responsible documentary contribution.')}</span><em>${t('Objetivos y próximos pasos →', 'Objectives and next steps →')}</em></a>
          </div>
          <div class="psr-next-footer"><a href="${cnmvUrl}">CNMV</a><a href="${incentivesUrl}">${t('Incentivos Regionales', 'Regional Incentives')}</a><a href="${sncaUrl}">${t('Fondos UE / SNCA', 'EU funds / SNCA')}</a><a href="${collaborateUrl}">${t('Aportar corrección o evidencia', 'Submit correction or evidence')}</a></div>
        </div>
      </section>`);
    const priority = document.querySelector('.priority-band');
    const h = hero();
    if (priority) priority.insertAdjacentElement('afterend', section);
    else if (h) h.insertAdjacentElement('afterend', section);
    else main()?.insertAdjacentElement('afterbegin', section);
  };

  const targetHref = (config, mode) => {
    if (!config) return null;
    if (mode === 'quick') {
      const node = findBySelectors(config.quick || []) || findSectionByHeading(config.quickHeading || []) || firstSubstantiveSection();
      return anchorFor(node, 'psr-quick-orientation');
    }
    if (mode === 'guided') {
      const node = findBySelectors(config.guided || []) || findSectionByHeading(config.guidedHeading || []) || [...(main()?.querySelectorAll(':scope > section') || [])][2] || firstSubstantiveSection();
      return anchorFor(node, 'psr-guided-read');
    }
    if (typeof config.full === 'string') return config.full;
    return null;
  };

  const addDepth = () => {
    if (isHome || isUpdates || document.getElementById('psr-depth-switcher')) return;
    const config = routeConfig();
    if (!config || !main()) return;
    const quick = targetHref(config, 'quick');
    const guided = targetHref(config, 'guided');
    const full = targetHref(config, 'full') || config.verify?.href || cleanRoomUrl;
    const nav = make(`
      <nav class="psr-depth" id="psr-depth-switcher" aria-label="${t('Profundidad de lectura', 'Reading depth')}"><div class="shell"><span class="psr-depth-label">${config.stage} · ${t('elija profundidad', 'choose depth')}</span>${quick ? `<a class="primary" href="${quick}">1 · ${t('Orientación', 'Orientation')}</a>` : ''}${guided ? `<a href="${guided}">7 · ${t('Lectura guiada', 'Guided read')}</a>` : ''}<a href="${full}">${t('Expediente completo', 'Full record')}</a><a class="status" href="${updatesUrl}">${t('Estado y cambios', 'Status and changes')}</a></div></nav>`);
    const h = hero();
    if (h) h.insertAdjacentElement('afterend', nav);
    else main()?.insertAdjacentElement('afterbegin', nav);
  };

  const addNext = () => {
    if (isHome || isUpdates || document.getElementById('psr-next-step')) return;
    const config = routeConfig();
    if (!config || !main()) return;
    const action = config.actionInstitutional
      ? { href: collaborateUrl, title: t('Corrección o respuesta documentada', 'Documented correction or response'), desc: t('Las correcciones verificables reciben trazabilidad y visibilidad equivalente; use cauces lícitos.', 'Verifiable corrections receive traceability and equivalent visibility; use lawful channels.') }
      : { href: recoveryUrl, title: t('Recuperación y restitución', 'Recovery and restitution'), desc: t('Conectar la prueba con activos, ingresos, daños, remedios y reconstrucción de la plataforma.', 'Connect the evidence to assets, income, damages, remedies and platform rebuilding.') };
    const section = make(`
      <section class="psr-next" id="psr-next-step" aria-labelledby="psr-next-title"><div class="shell"><p class="psr-next-kicker">${t('SIGUIENTE PASO', 'NEXT STEP')}</p><h2 id="psr-next-title">${t('Ya conoce este nodo. Continúe sin perder el hilo.', 'You know this node. Continue without losing the thread.')}</h2><p class="psr-next-intro">${t('Elija la siguiente acción según su función: seguir la historia, verificar el expediente o aportar una respuesta/corrección vinculada a la recuperación.', 'Choose the next action for your role: continue the story, verify the record or provide a response/correction linked to recovery.')}</p><div class="psr-next-grid"><a class="psr-next-card" href="${config.next.href}"><span class="label">${t('Continuar la secuencia', 'Continue the sequence')}</span><strong>${config.next.title}</strong><span>${config.next.desc}</span><em>${t('Siguiente nodo →', 'Next node →')}</em></a><a class="psr-next-card" href="${config.verify.href}"><span class="label">${t('Verificar', 'Verify')}</span><strong>${config.verify.title}</strong><span>${config.verify.desc}</span><em>${t('Abrir control →', 'Open control →')}</em></a><a class="psr-next-card" href="${action.href}"><span class="label">${t('Actuar / responder', 'Act / respond')}</span><strong>${action.title}</strong><span>${action.desc}</span><em>${t('Abrir vía →', 'Open route →')}</em></a></div><div class="psr-next-footer"><a href="${config.previous.href}">← ${config.previous.title}</a><a href="${homeUrl}">${t('Mapa general', 'Case map')}</a><a href="${updatesUrl}">${t('Cambios materiales', 'Material changes')}</a><a href="${collaborateUrl}">${t('Aportar evidencia', 'Provide evidence')}</a></div></div></section>`);
    main()?.insertAdjacentElement('beforeend', section);
  };

  const apply = () => {
    ensureCss();
    addProgress();
    repairRail();
    addHomeIntent();
    addDepth();
    addNext();
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => setTimeout(apply, 1700), { once: true });
  else setTimeout(apply, 1700);
  setTimeout(apply, 3200);
  setTimeout(apply, 5200);
})();
