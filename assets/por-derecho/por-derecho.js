(() => {
  const navToggle = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-nav]');
  if (navToggle && nav) {
    navToggle.addEventListener('click', () => {
      const open = nav.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', String(open));
    });
  }

  const lang = document.documentElement.lang === 'en' ? 'en' : 'es';
  const base = `/por-derecho/${lang}/por-derecho/`;

  // Keep the application register and institutional programme discoverable
  // across Por Derecho without changing any live-matter page.
  if (nav && !nav.querySelector('a[href*="aplicaciones-y-colaboracion"],a[href*="applications-and-collaboration"]')) {
    const link = document.createElement('a');
    link.dataset.pdApplicationsLink = 'true';
    link.href = lang === 'en'
      ? `${base}applications-and-collaboration/`
      : `${base}aplicaciones-y-colaboracion/`;
    link.textContent = lang === 'en' ? 'Applications' : 'Aplicaciones';
    const anchor = nav.querySelector('.pd-language,.pd-back');
    nav.insertBefore(link, anchor || null);
  }
  if (nav && !nav.querySelector('a[href*="governance-and-independence"],a[href*="gobernanza-e-independencia"]')) {
    const link = document.createElement('a');
    link.dataset.pdInstitutionLink = 'true';
    link.href = lang === 'en'
      ? `${base}governance-and-independence/`
      : `${base}gobernanza-e-independencia/`;
    link.textContent = lang === 'en' ? 'Institution' : 'Institución';
    const anchor = nav.querySelector('.pd-language,.pd-back');
    nav.insertBefore(link, anchor || null);
  }
  if (nav && !nav.querySelector('a[href*="institutional-execution"],a[href*="ejecucion-institucional"]')) {
    const link = document.createElement('a');
    link.dataset.pdExecutionLink = 'true';
    link.href = lang === 'en'
      ? `${base}institutional-execution/`
      : `${base}ejecucion-institucional/`;
    link.textContent = lang === 'en' ? 'Execution' : 'Ejecución';
    const anchor = nav.querySelector('.pd-language,.pd-back');
    nav.insertBefore(link, anchor || null);
  }
  if (nav && !nav.querySelector('a[href*="transparency"],a[href*="transparencia"]')) {
    const link = document.createElement('a');
    link.dataset.pdTransparencyLink = 'true';
    link.href = lang === 'en'
      ? `${base}transparency/`
      : `${base}transparencia/`;
    link.textContent = lang === 'en' ? 'Transparency' : 'Transparencia';
    const anchor = nav.querySelector('.pd-language,.pd-back');
    nav.insertBefore(link, anchor || null);
  }

  function ensureStageTwoCss() {
    if (document.querySelector('link[href*="foundation-stage-2.css"]')) return;
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = '/por-derecho/assets/por-derecho/foundation-stage-2.css';
    document.head.appendChild(link);
  }

  function ensureStageThreeCss() {
    if (document.querySelector('link[href*="foundation-stage-3.css"]')) return;
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = '/por-derecho/assets/por-derecho/foundation-stage-3.css';
    document.head.appendChild(link);
  }

  function addTransparencyHome() {
    const path = window.location.pathname.replace(/index\.html$/, '');
    const isHome = path === '/por-derecho/es/por-derecho/' || path === '/por-derecho/en/por-derecho/';
    if (!isHome || document.querySelector('[data-pd-transparency-phase1]')) return;
    ensureStageTwoCss();
    const main = document.querySelector('main');
    if (!main) return;
    const originBand = main.querySelector('.pd-origin-band');
    const section = document.createElement('section');
    section.className = 'pd-section';
    section.setAttribute('data-pd-transparency-phase1', '20260825');
    if (lang === 'en') {
      section.innerHTML = `<div class="pd-shell">
        <div class="pd-section-head"><div><p class="pd-kicker">Phase 1 transparency</p><h2>Who speaks, whose interests are involved, what is implemented and what remains unverified.</h2></div><p>Por Derecho now publishes one present-tense transparency gateway without claiming a registered Foundation, independent governance, external funding, institutional adoption or a complete historical actor census.</p></div>
        <div class="pds2-docs">
          <article class="pds2-doc"><span class="pds2-state">Current</span><h3>Founder-led</h3><p>Gil Marer is the founder and current public voice. No independent governing body has yet been constituted.</p></article>
          <article class="pds2-doc"><span class="pds2-state">Disclosed interest</span><h3>Born from Sun Park</h3><p>The founding experience involves direct legal and economic interests. It may generate questions; it cannot validate the answer.</p></article>
          <article class="pds2-doc"><span class="pds2-state">Controlled names</span><h3>P0–P3 only</h3><p>No new historical profile is created. Public names remain limited to the reviewed immutable identity register.</p></article>
          <article class="pds2-doc"><span class="pds2-state">Under verification</span><h3>Funding statement</h3><p>Current costs and in-kind support are being reconciled. No external grant, donation, sponsorship or institutional funding is claimed here.</p></article>
        </div>
        <div class="pd-actions"><a class="pd-button" href="${base}transparency/">Open the Transparency Hub →</a><a class="pd-button secondary" href="/por-derecho/en/matter-identity-registry/">Review the identity workbench</a></div>
      </div>`;
    } else {
      section.innerHTML = `<div class="pd-shell">
        <div class="pd-section-head"><div><p class="pd-kicker">Fase 1 de transparencia</p><h2>Quién habla, qué intereses existen, qué está implementado y qué sigue sin verificar.</h2></div><p>Por Derecho publica ahora una puerta de transparencia en tiempo presente sin afirmar Fundación registrada, gobierno independiente, financiación externa, adopción institucional o censo histórico completo.</p></div>
        <div class="pds2-docs">
          <article class="pds2-doc"><span class="pds2-state">Actual</span><h3>Dirigido por el fundador</h3><p>Gil Marer es el fundador y la voz pública actual. Todavía no se ha constituido un órgano independiente.</p></article>
          <article class="pds2-doc"><span class="pds2-state">Interés declarado</span><h3>Nacido de Sun Park</h3><p>La experiencia de origen incluye intereses jurídicos y económicos directos. Puede generar preguntas; no puede validar la respuesta.</p></article>
          <article class="pds2-doc"><span class="pds2-state">Nombres controlados</span><h3>Solo P0–P3</h3><p>No se crea ninguna ficha histórica nueva. Los nombres públicos siguen limitados al registro inmutable revisado.</p></article>
          <article class="pds2-doc"><span class="pds2-state">En verificación</span><h3>Declaración de financiación</h3><p>Se están conciliando costes actuales y apoyo en especie. Aquí no se afirma subvención, donación, patrocinio o financiación institucional externa.</p></article>
        </div>
        <div class="pd-actions"><a class="pd-button" href="${base}transparencia/">Abrir el Portal de Transparencia →</a><a class="pd-button secondary" href="/por-derecho/es/registro-identidad-materia/">Revisar el banco de identidades</a></div>
      </div>`;
    }
    if (originBand && originBand.nextSibling) main.insertBefore(section, originBand.nextSibling);
    else if (main.firstElementChild && main.firstElementChild.nextSibling) main.insertBefore(section, main.firstElementChild.nextSibling);
    else main.appendChild(section);
  }

  function addTransparencyStrip() {
    const path = window.location.pathname.replace(/index\.html$/, '');
    const isHome = path === '/por-derecho/es/por-derecho/' || path === '/por-derecho/en/por-derecho/';
    const isHub = path.includes('/por-derecho/transparency/') || path.includes('/por-derecho/transparencia/');
    if (isHome || isHub || document.querySelector('[data-pd-transparency-strip]')) return;
    ensureStageTwoCss();
    const main = document.querySelector('main');
    if (!main) return;
    const section = document.createElement('section');
    section.className = 'pd-section alt';
    section.setAttribute('data-pd-transparency-strip', '20260825');
    if (lang === 'en') {
      section.innerHTML = `<div class="pd-shell"><div class="pds2-boundary"><h3>Transparency status</h3><p>Por Derecho remains a founder-led initiative in formation. The founder-related origin, absence of constituted independent governance, P0–P3 public-name gate, human-reviewed AI boundary, funding uncertainty and correction route are disclosed in one place.</p><p><a href="${base}transparency/">Read the current Transparency Hub →</a></p></div></div>`;
    } else {
      section.innerHTML = `<div class="pd-shell"><div class="pds2-boundary"><h3>Estado de transparencia</h3><p>Por Derecho sigue siendo una iniciativa en formación dirigida por el fundador. El origen vinculado al fundador, la ausencia de gobierno independiente constituido, la puerta P0–P3 para nombres públicos, el límite de IA bajo revisión humana, la financiación pendiente y la vía de corrección se declaran en un único lugar.</p><p><a href="${base}transparencia/">Leer el Portal de Transparencia actual →</a></p></div></div>`;
    }
    main.appendChild(section);
  }

  function addFoundationStageTwoHome() {
    const path = window.location.pathname.replace(/index\.html$/, '');
    const isHome = path === '/por-derecho/es/por-derecho/' || path === '/por-derecho/en/por-derecho/';
    if (!isHome || document.querySelector('[data-pd-foundation-stage2]')) return;
    ensureStageTwoCss();
    const main = document.querySelector('main');
    if (!main) return;
    const target = main.querySelector('#formacion') || main.lastElementChild;
    const section = document.createElement('section');
    section.className = 'pd-section alt';
    section.dataset.pdFoundationStage2 = '20260820';
    if (lang === 'en') {
      section.innerHTML = `<div class="pd-shell">
        <div class="pd-section-head"><div><p class="pd-kicker">Institutional stage two</p><h2>Draft the institution. Try to break the method. Preserve the house carefully.</h2></div><p>Three working instruments move Por Derecho beyond a demonstrator without overstating its status. The Foundation is not registered, independent review has not yet occurred, and the San Bernardo acquisition is not complete.</p></div>
        <div class="pds2-docs">
          <article class="pds2-doc"><span class="pds2-state">Working draft</span><h3>Formation and governance</h3><p>Proposed purposes, Board, conflicts committee, scientific council, funding controls, founder-related quarantine and the rule that no asset or donor controls conclusions.</p><footer><a href="${base}governance-and-independence/">Open the governance draft →</a></footer></article>
          <article class="pds2-doc"><span class="pds2-state">Review not yet performed</span><h3>Independent red-team protocol</h3><p>Pre-registered synthetic tests, false-positive clearance, stop conditions, dissent, redesign and a real “do not deploy” outcome.</p><footer><a href="${base}research-and-training/">Open the review protocol →</a></footer></article>
          <article class="pds2-doc"><span class="pds2-state">Acquisition not completed</span><h3>San Bernardo preservation brief</h3><p>Preservation, archive, room programme and quiet technology, strictly separate from title, condition, finance, diligence and authority to inspect or alter.</p><footer><a href="${base}palacete/">Open the preservation brief →</a></footer></article>
        </div>
        <div class="pd-actions"><a class="pd-button secondary" href="${base}origin/">Why the founder’s case may originate questions but cannot control conclusions →</a></div>
      </div>`;
    } else {
      section.innerHTML = `<div class="pd-shell">
        <div class="pd-section-head"><div><p class="pd-kicker">Segunda etapa institucional</p><h2>Redactar la institución. Intentar romper el método. Preservar la casa con cuidado.</h2></div><p>Tres instrumentos de trabajo llevan Por Derecho más allá del demostrador sin inflar su estado. La Fundación no está registrada, la revisión independiente no se ha realizado y la adquisición de San Bernardo no está completada.</p></div>
        <div class="pds2-docs">
          <article class="pds2-doc"><span class="pds2-state">Borrador de trabajo</span><h3>Formación y gobernanza</h3><p>Fines, Patronato, comité de conflictos, consejo científico, financiación, cuarentena de asuntos vinculados y regla de que ningún activo o donante controla conclusiones.</p><footer><a href="${base}gobernanza-e-independencia/">Abrir el borrador de gobernanza →</a></footer></article>
          <article class="pds2-doc"><span class="pds2-state">Revisión no realizada</span><h3>Protocolo de red-team independiente</h3><p>Pruebas sintéticas pre-registradas, cierre de falsos positivos, condiciones de parada, disenso, rediseño y un resultado real de “no desplegar”.</p><footer><a href="${base}investigacion-y-formacion/">Abrir el protocolo de revisión →</a></footer></article>
          <article class="pds2-doc"><span class="pds2-state">Adquisición no completada</span><h3>Brief de preservación de San Bernardo</h3><p>Conservación, archivo, programa de estancias y tecnología discreta, separados de titularidad, estado, financiación, diligencia y autoridad para inspeccionar o alterar.</p><footer><a href="${base}palacete/">Abrir el brief de preservación →</a></footer></article>
        </div>
        <div class="pd-actions"><a class="pd-button secondary" href="${base}origen/">Por qué el caso del fundador puede originar preguntas pero no controlar conclusiones →</a></div>
      </div>`;
    }
    main.insertBefore(section, target || null);
  }

  function addFoundationStageThreeHome() {
    const path = window.location.pathname.replace(/index\.html$/, '');
    const isHome = path === '/por-derecho/es/por-derecho/' || path === '/por-derecho/en/por-derecho/';
    if (!isHome || document.querySelector('[data-pd-foundation-stage3]')) return;
    ensureStageThreeCss();
    const main = document.querySelector('main');
    if (!main) return;
    const target = main.querySelector('#formacion') || main.lastElementChild;
    const section = document.createElement('section');
    section.className = 'pd-section';
    section.dataset.pdFoundationStage3 = '20260820';
    if (lang === 'en') {
      section.innerHTML = `<div class="pd-shell">
        <div class="pd-section-head"><div><p class="pd-kicker">Institutional execution</p><h2>Four commission-ready packs. No external responsibility is presumed.</h2></div><p>Legal formation, independent Board recruitment, synthetic red-team review and San Bernardo conservation now have defined scopes and stop gates. They remain prepared—not appointed, commissioned, validated or legally completed.</p></div>
        <div class="pds3-actions">
          <article class="pds3-action"><strong>Legal/notarial formation</strong><span>Prepared for a lawyer to accept, redirect or recommend a pause.</span></article>
          <article class="pds3-action"><strong>Independent governance</strong><span>Role and conflict architecture prepared; no trustees appointed.</span></article>
          <article class="pds3-action"><strong>Synthetic red team</strong><span>Commission protocol prepared; independent review not performed.</span></article>
          <article class="pds3-action"><strong>San Bernardo conservation</strong><span>RFP prepared; no architect, access or survey authorised.</span></article>
        </div>
        <div class="pd-actions"><a class="pd-button" href="${base}institutional-execution/">Open the 90-day execution control →</a></div>
      </div>`;
    } else {
      section.innerHTML = `<div class="pd-shell">
        <div class="pd-section-head"><div><p class="pd-kicker">Ejecución institucional</p><h2>Cuatro paquetes preparados para encargo. No se presume responsabilidad externa.</h2></div><p>Constitución jurídica, selección de Patronato independiente, red-team sintético y conservación de San Bernardo tienen ya alcance y puertas de parada. Siguen preparados: no nombrados, encargados, validados ni legalmente completados.</p></div>
        <div class="pds3-actions">
          <article class="pds3-action"><strong>Constitución jurídica/notarial</strong><span>Preparado para que un abogado acepte, redirija o recomiende pausar.</span></article>
          <article class="pds3-action"><strong>Gobierno independiente</strong><span>Arquitectura de funciones y conflictos preparada; sin patronos nombrados.</span></article>
          <article class="pds3-action"><strong>Red-team sintético</strong><span>Protocolo de encargo preparado; revisión independiente no realizada.</span></article>
          <article class="pds3-action"><strong>Conservación de San Bernardo</strong><span>RFP preparado; sin arquitecto, acceso o levantamiento autorizado.</span></article>
        </div>
        <div class="pd-actions"><a class="pd-button" href="${base}ejecucion-institucional/">Abrir el control de ejecución a 90 días →</a></div>
      </div>`;
    }
    main.insertBefore(section, target || null);
  }

  function addCorrectedMaturityLadder() {
    const path = window.location.pathname;
    const isApplications = path.includes('/aplicaciones-y-colaboracion/') || path.includes('/applications-and-collaboration/');
    if (!isApplications || document.querySelector('[data-pd-maturity-20260820]')) return;
    ensureStageTwoCss();
    const main = document.querySelector('main');
    if (!main) return;
    const hero = main.firstElementChild;
    const section = document.createElement('section');
    section.className = 'pd-section';
    section.dataset.pdMaturity20260820 = 'true';
    if (lang === 'en') {
      section.innerHTML = `<div class="pd-shell">
        <div class="pd-section-head"><div><p class="pd-kicker">Correct maturity sequence · 20 August 2026</p><h2>Simulation, independent criticism, controlled use, then institutional decision.</h2></div><p>Readiness, receipt and experimental use are not validation or adoption. Each stage requires distinct evidence.</p></div>
        <div class="pds2-flow">
          <article><div><h3>Brief synthetic demonstrator</h3><p>The public File Alpha explains the six checks and human decision gate.</p></div><aside>Available as a teaching demonstrator.</aside></article>
          <article><div><h3>Expanded synthetic simulation</h3><p>Case Prism tests time, competence, mixed perimeters, alternatives and difficult-to-reverse effects.</p></div><aside><strong>Under internal validation; not deployed.</strong></aside></article>
          <article><div><h3>Independent red-team review</h3><p>Pre-registered synthetic cases must test false positives, bias, privacy, security, human control and stop conditions.</p></div><aside>Protocol prepared; review not yet performed.</aside></article>
          <article><div><h3>Controlled real-matter application</h3><p>DIP 79/2026 and DIP 80/2026 are experimental founder-related research applications under visible conflict controls.</p></div><aside>Not independent validation, ICALPA endorsement, adoption or a disciplinary conclusion.</aside></article>
          <article><div><h3>Institutional pilot</h3><p>A competent institution may authorise a bounded synthetic or controlled pilot under its own governance.</p></div><aside>No institutional pilot is presently claimed.</aside></article>
          <article><div><h3>Adoption</h3><p>Use, partnership, accreditation or adoption is recorded only after the institution expressly confirms it.</p></div><aside>No adoption is presently claimed.</aside></article>
        </div>
        <div class="pds2-boundary" style="margin-top:20px"><h3>Case separation remains mandatory</h3><p>Sharing a method never transfers evidence between matters. Each use requires a human decision on relevance, provenance, lawful access, competence and the exact purpose for which a source is sufficient.</p></div>
        <div class="pd-actions"><a class="pd-button secondary" href="${base}institutional-execution/">See the prepared commissions and unresolved external gates →</a></div>
      </div>`;
    } else {
      section.innerHTML = `<div class="pd-shell">
        <div class="pd-section-head"><div><p class="pd-kicker">Secuencia de madurez corregida · 20 agosto 2026</p><h2>Simulación, crítica independiente, uso controlado y después decisión institucional.</h2></div><p>Preparación, recepción y uso experimental no son validación ni adopción. Cada etapa exige una evidencia distinta.</p></div>
        <div class="pds2-flow">
          <article><div><h3>Demostrador sintético breve</h3><p>El Expediente Alfa público explica las seis comprobaciones y la puerta de decisión humana.</p></div><aside>Disponible como demostrador pedagógico.</aside></article>
          <article><div><h3>Simulación sintética ampliada</h3><p>Caso Prisma prueba tiempo, competencia, perímetros mixtos, alternativas y efectos difíciles de revertir.</p></div><aside><strong>Bajo validación interna; no desplegado.</strong></aside></article>
          <article><div><h3>Red-team independiente</h3><p>Casos sintéticos pre-registrados deben probar falsos positivos, sesgo, privacidad, seguridad, control humano y parada.</p></div><aside>Protocolo preparado; revisión no realizada.</aside></article>
          <article><div><h3>Aplicación controlada a asunto real</h3><p>DIP 79/2026 y DIP 80/2026 son aplicaciones experimentales de investigación relacionadas con el fundador y con conflicto visible.</p></div><aside>No son validación independiente, respaldo de ICALPA, adopción ni conclusión disciplinaria.</aside></article>
          <article><div><h3>Piloto institucional</h3><p>Una institución competente puede autorizar un piloto sintético o controlado bajo su propia gobernanza.</p></div><aside>No se afirma actualmente ningún piloto institucional.</aside></article>
          <article><div><h3>Adopción</h3><p>Uso, colaboración, acreditación o adopción solo se registra tras confirmación expresa de la institución.</p></div><aside>No se afirma actualmente adopción.</aside></article>
        </div>
        <div class="pds2-boundary" style="margin-top:20px"><h3>La separación entre asuntos sigue siendo obligatoria</h3><p>Compartir método nunca transfiere prueba. Cada uso exige decisión humana sobre relevancia, procedencia, acceso lícito, competencia y el propósito exacto para el que una fuente resulta suficiente.</p></div>
        <div class="pd-actions"><a class="pd-button secondary" href="${base}ejecucion-institucional/">Ver los encargos preparados y las puertas externas pendientes →</a></div>
      </div>`;
    }
    if (hero && hero.nextSibling) main.insertBefore(section, hero.nextSibling);
    else main.appendChild(section);
  }

  addTransparencyHome();
  addFoundationStageTwoHome();
  addFoundationStageThreeHome();
  addCorrectedMaturityLadder();
  addTransparencyStrip();

  const decisions = document.querySelectorAll('[data-decision]');
  const output = document.querySelector('[data-decision-output]');
  const audit = document.querySelector('[data-audit]');
  decisions.forEach((button) => {
    button.addEventListener('click', () => {
      decisions.forEach((item) => item.setAttribute('aria-pressed', 'false'));
      button.setAttribute('aria-pressed', 'true');
      if (output) output.innerHTML = `<strong>${button.dataset.title}</strong><br>${button.dataset.output}`;
      if (audit) {
        const li = document.createElement('li');
        li.textContent = `${button.dataset.audit}: ${lang === 'en' ? 'the warning and human reasons are preserved.' : 'se conserva la advertencia y la motivación humana.'}`;
        audit.prepend(li);
      }
    });
  });

  const resolvedToggle = document.querySelector('[data-resolved-toggle]');
  const resolvedPanel = document.querySelector('[data-resolved-panel]');
  if (resolvedToggle && resolvedPanel) {
    resolvedToggle.addEventListener('click', () => {
      const willOpen = resolvedPanel.hasAttribute('hidden');
      resolvedPanel.toggleAttribute('hidden');
      resolvedToggle.setAttribute('aria-expanded', String(willOpen));
      resolvedToggle.textContent = willOpen ? resolvedToggle.dataset.close : resolvedToggle.dataset.open;
    });
  }
})();
