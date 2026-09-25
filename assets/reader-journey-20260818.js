(() => {
  const current = document.currentScript;
  if (current && !document.querySelector('link[data-psr-reader-journey]')) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = new URL('reader-journey-20260818.css?v=20260818a', current.src).href;
    link.dataset.psrReaderJourney = '20260818';
    document.head.appendChild(link);
  }

  const path = location.pathname.replace(/\/+$/, '/') || '/';
  const isEn = /\/en\//.test(path);
  const root = '/por-derecho/';
  const lang = isEn ? 'en' : 'es';
  const p = (slug = '') => `${root}${lang}/${slug}`;
  const t = (es, en) => isEn ? en : es;

  const relevant = [
    '/comunidad-instrumentalizacion/',
    '/community-instrumentalisation/',
    '/toma-control-sun-park-7-junio-2018/',
    '/sun-park-takeover-7-june-2018/',
    '/insolvencia-lpb/', '/lpb-insolvency/',
    '/calificacion-concurso-36-2012-vidas-paralelas/', '/insolvency-classification-parallel-lives/',
    '/ric-private-equity-sun-park/',
    '/ricpe-responsabilidad-documental/', '/ricpe-documentary-accountability/',
    '/mismo-hotel-multiples-vidas-financieras/', '/same-hotel-multiple-financial-lives/',
    '/cadena-instrumentalizacion-ric-fondos-incentivos/', '/institutionalisation-chain-ric-eu-incentives/',
    '/objetivos-recuperacion-restitucion/', '/recovery-restitution-objectives/'
  ].some(s => path.includes(s));

  const ownershipUrl = isEn ? p('community-instrumentalisation/minutes-2011-2022/') : p('comunidad-instrumentalizacion/actas-2011-2022/');
  const communityUrl = isEn ? p('community-instrumentalisation/') : p('comunidad-instrumentalizacion/');
  const controlUrl = isEn ? p('sun-park-takeover-7-june-2018/') : p('toma-control-sun-park-7-junio-2018/');
  const insolvencyUrl = isEn ? p('lpb-insolvency/') : p('insolvencia-lpb/');
  const ricpeUrl = p('ric-private-equity-sun-park/');
  const fundingUrl = isEn ? p('same-hotel-multiple-financial-lives/') : p('mismo-hotel-multiples-vidas-financieras/');
  const myndUrl = isEn ? p('hosteltur-sun-park-mynd-yaiza/') : p('hosteltur-sun-park-mynd-yaiza/');
  const recoveryUrl = isEn ? p('recovery-restitution-objectives/') : p('objetivos-recuperacion-restitucion/');

  const railSteps = [
    [t('Propiedad', 'Ownership'), ownershipUrl, /actas-2011-2022|minutes-2011-2022/],
    [t('Comunidad', 'Community'), communityUrl, /comunidad-instrumentalizacion|community-instrumentalisation/],
    [t('Control 2018', '2018 control'), controlUrl, /toma-control-sun-park-7-junio-2018|sun-park-takeover-7-june-2018/],
    [t('Concurso', 'Insolvency'), insolvencyUrl, /insolvencia-lpb|lpb-insolvency|calificacion-concurso|insolvency-classification/],
    ['RICPE', ricpeUrl, /ric-private-equity-sun-park|ricpe-responsabilidad-documental|ricpe-documentary-accountability/],
    [t('Financiación', 'Funding'), fundingUrl, /mismo-hotel-multiples-vidas-financieras|same-hotel-multiple-financial-lives|cadena-instrumentalizacion-ric|institutionalisation-chain-ric/],
    ['MYND', myndUrl, /hosteltur-sun-park-mynd-yaiza/],
    [t('Recuperación', 'Recovery'), recoveryUrl, /objetivos-recuperacion-restitucion|recovery-restitution-objectives/]
  ];

  function addRail() {
    if (!relevant || document.getElementById('psr-unitary-journey')) return;
    const header = document.querySelector('.site-header');
    if (!header) return;
    const rail = document.createElement('nav');
    rail.id = 'psr-unitary-journey';
    rail.className = 'psr-journey-rail';
    rail.setAttribute('aria-label', t('Ruta unitaria Sun Park', 'Sun Park unitary journey'));
    rail.innerHTML = `<div class="shell"><span class="psr-rail-label">${t('Un hotel · una ruta', 'One hotel · one journey')}</span>${railSteps.map(([label,url,re]) => `<a href="${url}"${re.test(path) ? ' aria-current="step"' : ''}>${label}</a>`).join('')}</div>`;
    header.insertAdjacentElement('afterend', rail);
  }

  function insertAfterHero(node) {
    const main = document.querySelector('main');
    if (!main) return false;
    const hero = main.querySelector('.dossier-hero, .hero');
    if (hero) hero.insertAdjacentElement('afterend', node);
    else main.insertAdjacentElement('afterbegin', node);
    return true;
  }

  function addRicpeCockpit() {
    const isMainRicpe = /\/ric-private-equity-sun-park\/$/.test(path);
    if (!isMainRicpe || document.getElementById('psr-ricpe-cockpit')) return;

    document.title = t('RICPE / Sun Park — comunicación formal, controles y trazabilidad | Project Sun Rock', 'RICPE / Sun Park — formal communication, controls and traceability | Project Sun Rock');
    const meta = document.querySelector('meta[name="description"]');
    if (meta) meta.setAttribute('content', t('Comunicación formal presentada a RICPE el 17 de agosto de 2026. Ruta de 7 minutos por título, conflicto, due diligence, julio de 2021, reactivación, financiación, Comunidad y respuesta institucional.', 'Formal communication submitted to RICPE on 17 August 2026. A seven-minute route through title, conflicts, due diligence, July 2021, reactivation, funding, Community authority and institutional response.'));

    const section = document.createElement('section');
    section.id = 'psr-ricpe-cockpit';
    section.className = 'section psr-cockpit';
    section.innerHTML = `
      <div class="shell">
        <div class="psr-cockpit-head">
          <div>
            <p class="psr-kicker">${t('Consejo / Compliance · lectura guiada de 7 minutos', 'Board / Compliance · guided 7-minute read')}</p>
            <h2>${t('Una cuestión finita: ¿qué convirtió un proyecto fragmentado y condicionado en un proyecto nuevamente aprobable y financiable?', 'A finite question: what converted a fragmented, conditional project into one that could again be approved and financed?')}</h2>
            <p class="psr-lead">${t('La ruta no exige aceptar una teoría global. Empieza por documentos controlados y pregunta, paso a paso, qué verificó RICPE de forma independiente, qué condición cambió y qué premisa pudo heredarse de terceros.', 'The route does not require accepting a global theory. It starts with controlled documents and asks, step by step, what RICPE independently verified, what condition changed, and which premise may have been inherited from third parties.')}</p>
            <div class="psr-actions">
              <a href="#psr-ricpe-five-docs">${t('Ver 5 documentos decisivos', 'See 5 decisive documents')}</a>
              <a class="secondary" href="#psr-ricpe-production">${t('Qué sólo RICPE puede responder', 'What only RICPE can answer')}</a>
              <a class="tertiary" href="#respuesta">${t('Estado y respuesta', 'Status and response')}</a>
            </div>
          </div>
          <aside class="psr-status-card" aria-label="${t('Estado de la comunicación formal', 'Formal communication status')}">
            <strong>${t('17 AGO 2026 · COMUNICACIÓN FORMAL', '17 AUG 2026 · FORMAL COMMUNICATION')}</strong>
            <div class="psr-status-flow">
              <span class="done">${t('Firmada', 'Signed')}</span><span class="done">${t('Presentada', 'Submitted')}</span><span class="done">${t('Acuse plataforma', 'Platform ack.')}</span><span class="open">${t('Admisión', 'Admission')}</span><span class="open">${t('Examen', 'Review')}</span><span class="open">${t('Consejo', 'Board')}</span><span class="open">${t('Decisión', 'Decision')}</span>
            </div>
            <p>${t('Constan presentación por Canal Ético y acuse técnico de plataforma. No constan todavía admisión, investigación, control de conflictos, preservación, tratamiento por el Consejo ni decisión de fondo.', 'Ethical Channel submission and technical platform acknowledgment are established. Admission, investigation, conflict screening, preservation, Board treatment and a merits decision are not yet established.')}</p>
            <p>${t('PDF firmado controlado: 22 páginas · firma criptográfica válida. La identidad byte a byte con el adjunto exacto del Canal sigue pendiente de metadatos de plataforma.', 'Controlled signed PDF: 22 pages · cryptographic signature valid. Byte-for-byte identity with the exact Channel attachment remains pending platform metadata.')}</p>
          </aside>
        </div>

        <div class="psr-decision-strip" id="psr-ricpe-five-docs">
          <header><strong>${t('Cinco documentos/eventos que cambian la lectura', 'Five documents/events that change the read')}</strong><span>${t('Primero el núcleo; después el expediente completo', 'Core first; full dossier second')}</span></header>
          <div class="psr-timeline">
            <article><time>2020</time><h3>${t('Representación del proyecto', 'Project representation')}</h3><p>${t('Qué se dijo sobre titularidad, cargas, adquisición, inversión y calendario.', 'What was represented about title, encumbrances, acquisition, investment and timing.')}</p></article>
            <article><time>20 JUL 2021</time><h3>${t('Certificación interna RICPE', 'RICPE internal certification')}</h3><p>${t('54 CAM · 190 LPB · 18 terceros; titularidad CAM futura/condicionada; LOI sin firma; DD completa no iniciada.', '54 CAM · 190 LPB · 18 third parties; CAM title future/conditional; unsigned LOI; full DD not started.')}</p></article>
            <article><time>21 JUL 2021</time><h3>${t('Uso ante el Concurso', 'Use in the insolvency')}</h3><p>${t('La certificación entra en Concurso 36/2012. Debe reconstruirse finalidad, autorización, recepción y tratamiento.', 'The certification enters Insolvency 36/2012. Purpose, authorisation, receipt and treatment must be reconstructed.')}</p></article>
            <article><time>2021–2022</time><h3>${t('Reentrada / título', 'Re-entry / title')}</h3><p>${t('La pregunta crítica es qué hecho, documento, condición o dispensa permitió superar la posición restrictiva anterior.', 'The critical question is what fact, document, condition or waiver overcame the earlier restrictive position.')}</p></article>
            <article><time>2022–2023</time><h3>${t('Financiación y apoyo', 'Funding and support')}</h3><p>${t('Series F/G, HNT, incentivo regional, FEDER y explotación MYND deben reconciliarse con activos, costes, obras y empleo.', 'Series F/G, HNT, regional incentive, ERDF and MYND operation must be reconciled against assets, costs, works and employment.')}</p></article>
          </div>
        </div>

        <div class="psr-what-changed" aria-label="${t('Qué cambió después de julio de 2021', 'What changed after July 2021')}">
          <div class="side"><strong>${t('20 JUL 2021 · posición documentada', '20 JUL 2021 · documented position')}</strong><p>${t('Propiedad fragmentada; adquisición CAM todavía futura/condicionada; LOI no firmada; due diligence completa no iniciada; retirada previa del proyecto.', 'Fragmented ownership; CAM acquisition still future/conditional; LOI unsigned; full due diligence not started; prior project withdrawal.')}</p></div>
          <div class="question">${t('¿QUÉ CAMBIÓ?', 'WHAT CHANGED?')}</div>
          <div class="side"><strong>${t('Después · resultado observable', 'Afterwards · observable outcome')}</strong><p>${t('Reactivación, título posterior, HNT, financiación, apoyo público y apertura de MYND. Cada salto requiere su documento y su órgano decisor.', 'Reactivation, later title, HNT, funding, public support and MYND opening. Each step requires its document and decision-maker.')}</p></div>
        </div>

        <details class="psr-disclosure" id="psr-ricpe-production">
          <summary>${t('RICPE puede resolver estas preguntas con sus propios archivos', 'RICPE can resolve these questions from its own files')}</summary>
          <div class="body">
            <div class="psr-question-grid">
              <div class="psr-question"><strong>${t('Origen / patrocinio', 'Origin / sponsorship')}</strong><span>${t('Quién introdujo Sun Park, en qué fecha, con qué promotor, prestatario, titularidad y conflicto declarado.', 'Who introduced Sun Park, when, with which sponsor, borrower, title position and declared conflict.')}</span></div>
              <div class="psr-question"><strong>${t('Conflictos / abstenciones', 'Conflicts / recusals')}</strong><span>${t('Declaraciones, recusaciones, acceso a información y participación en comité/Consejo.', 'Declarations, recusals, access to information and committee/Board participation.')}</span></div>
              <div class="psr-question"><strong>${t('2020 → julio 2021', '2020 → July 2021')}</strong><span>${t('Qué verificaciones llevaron de la promoción inicial a la retirada/condicionalidad documentada.', 'Which checks led from initial promotion to the documented withdrawal/conditionality.')}</span></div>
              <div class="psr-question"><strong>${t('Reentrada', 'Re-entry')}</strong><span>${t('Qué nueva prueba, condición cumplida, dispensa o decisión permitió reactivar el proyecto.', 'What new evidence, satisfied condition, waiver or decision allowed the project to be reactivated.')}</span></div>
              <div class="psr-question"><strong>${t('Título / disponibilidad', 'Title / availability')}</strong><span>${t('Qué finca, derecho, zona común o autoridad se consideró disponible en cada fecha, y mediante qué fuente primaria.', 'Which unit, right, common area or authority was considered available at each date, and through which primary source.')}</span></div>
              <div class="psr-question"><strong>${t('Valoración / DD', 'Valuation / DD')}</strong><span>${t('Informes, reservas, alcance, autores, circulación y downside usado por cada órgano.', 'Reports, reservations, scope, authors, circulation and downside used by each decision-maker.')}</span></div>
              <div class="psr-question"><strong>${t('HNT / Series F–G', 'HNT / Series F–G')}</strong><span>${t('Admisión, garantías, desembolsos, source-and-use, facturas, obras y empleo.', 'Admission, guarantees, drawdowns, source-and-use, invoices, works and employment.')}</span></div>
              <div class="psr-question"><strong>${t('Comunidad ≈€4,5m', 'Community ≈€4.5m')}</strong><span>${t('Qué conoció RICPE de la autoridad, voto, obras, financiación y posible coincidencia de costes; la cifra sigue como alegación pendiente del expediente primario.', 'What RICPE knew about authority, voting, works, funding and possible cost overlap; the figure remains an allegation pending the primary file.')}</span></div>
            </div>
          </div>
        </details>

        <details class="psr-disclosure">
          <summary>${t('Qué evidencia podría debilitar o cambiar esta reconstrucción', 'What evidence could weaken or change this reconstruction')}</summary>
          <div class="body"><p>${t('Título contemporáneo suficiente; due diligence independiente que resolviera las reservas; conflictos declarados y abstenciones documentadas; una explicación soportada del cambio julio-2021→reentrada; costes de Comunidad, RICPE/RIC, incentivo y FEDER demostrablemente distintos; empleo definido por poblaciones y periodos distintos; o advertencias contemporáneas de actores sobre límites de autoridad. Toda evidencia exculpatoria o correctora debe recibir el mismo tratamiento documental.', 'Sufficient contemporaneous title; independent due diligence resolving the reservations; documented conflict declarations and recusals; a supported explanation of the July-2021→re-entry change; Community, RICPE/RIC, incentive and ERDF costs demonstrably distinct; employment figures defined by different populations and periods; or contemporaneous warnings about limits of authority. Exculpatory or corrective evidence should receive the same documentary treatment.')}</p></div>
        </details>

        <div class="psr-response-ledger" aria-label="${t('Registro de respuesta RICPE', 'RICPE response ledger')}">
          <div class="confirmed"><strong>${t('Presentación', 'Submission')}</strong><span>${t('Confirmada · 17 ago 2026', 'Confirmed · 17 Aug 2026')}</span></div>
          <div class="confirmed"><strong>${t('Acuse plataforma', 'Platform acknowledgment')}</strong><span>${t('Confirmado', 'Confirmed')}</span></div>
          <div class="pending"><strong>${t('Admisión / examen', 'Admission / review')}</strong><span>${t('No establecido', 'Not established')}</span></div>
          <div class="pending"><strong>${t('Conflictos / preservación', 'Conflicts / preservation')}</strong><span>${t('No establecido', 'Not established')}</span></div>
          <div class="pending"><strong>${t('Tratamiento Consejo', 'Board treatment')}</strong><span>${t('No establecido', 'Not established')}</span></div>
          <div class="pending"><strong>${t('Respuesta de fondo', 'Merits response')}</strong><span>${t('No establecida', 'Not established')}</span></div>
          <div class="pending"><strong>${t('Corrección / remedio', 'Correction / remedy')}</strong><span>${t('No establecido', 'Not established')}</span></div>
          <div class="pending"><strong>${t('Silencio', 'Silence')}</strong><span>${t('No equivale a culpabilidad', 'Does not equal wrongdoing')}</span></div>
        </div>
      </div>`;
    insertAfterHero(section);
  }

  function addCommunityBridge() {
    const communityMain = /\/(comunidad-instrumentalizacion|community-instrumentalisation)\/$/.test(path);
    if (!communityMain || document.getElementById('psr-community-to-ricpe')) return;
    const section = document.createElement('section');
    section.id = 'psr-community-to-ricpe';
    section.className = 'psr-module alt';
    section.innerHTML = `<div class="shell"><p class="psr-kicker">${t('Por qué importa fuera de la Comunidad', 'Why this matters beyond the Community')}</p><h2>${t('De autoridad comunitaria a disponibilidad del proyecto: el puente que debe probarse, no presumirse.', 'From Community authority to project availability: the bridge that must be proved, not assumed.')}</h2><p class="psr-intro">${t('La cuestión no es si la Comunidad “era dueña del hotel”. No lo era por el mero hecho de administrar elementos comunes. La cuestión investigable es si determinadas actas, deudas, exclusiones de voto, certificaciones, instrucciones de acceso o decisiones de mantenimiento produjeron una apariencia de autoridad que después fue utilizada por otros actores. Cada conversión exige una fuente y una atribución separadas.', 'The question is not whether the Community “owned the hotel”. It did not merely by administering common elements. The investigable question is whether particular minutes, debts, voting exclusions, certifications, access instructions or maintenance decisions produced an appearance of authority later used by other actors. Each conversion requires its own source and attribution.')}</p>
      <div class="psr-conversion-chain">
        <a href="${ownershipUrl}"><strong>${t('Título / fincas', 'Title / units')}</strong><span>${t('Quién era propietario y podía participar.', 'Who owned and could participate.')}</span></a>
        <a href="${communityUrl}"><strong>${t('Deuda / voto', 'Debt / vote')}</strong><span>${t('Quién calculó, certificó y quedó habilitado.', 'Who calculated, certified and remained entitled.')}</span></a>
        <a href="${communityUrl}"><strong>${t('Autoridad', 'Authority')}</strong><span>${t('Qué acta/mandato legitimaba a cada actor.', 'Which minute/mandate authorised each actor.')}</span></a>
        <a href="${controlUrl}"><strong>${t('Acceso / seguridad', 'Access / security')}</strong><span>${t('Qué poder permitió la actuación material.', 'What power allowed material action.')}</span></a>
        <a href="${controlUrl}"><strong>${t('Control práctico', 'Practical control')}</strong><span>${t('No equivale automáticamente a título.', 'Does not automatically equal title.')}</span></a>
        <a href="${ricpeUrl}"><strong>${t('Proyecto CAM', 'CAM project')}</strong><span>${t('Qué disponibilidad se presentó a terceros.', 'What availability was represented externally.')}</span></a>
        <a href="${ricpeUrl}"><strong>RICPE</strong><span>${t('Qué recibió y verificó de forma independiente.', 'What it received and independently verified.')}</span></a>
        <a href="${fundingUrl}"><strong>${t('Financiación', 'Funding')}</strong><span>${t('Capital, obras, costes y empleo.', 'Capital, works, costs and employment.')}</span></a>
        <a href="${myndUrl}"><strong>MYND</strong><span>${t('Resultado operativo actual.', 'Current operating outcome.')}</span></a>
      </div>
      <p class="psr-safety-note"><strong>${t('Límite probatorio:', 'Evidence boundary:')}</strong> ${t('esta secuencia es un mapa de dependencias a comprobar. No demuestra que RICPE recibiera información falsa, que conociera una irregularidad ni que todo acto comunitario fuera inválido. La pregunta es qué premisa verificó cada receptor contra fuentes originales y cuál heredó.', 'this sequence is a dependency map to be tested. It does not establish that RICPE received false information, knew of an irregularity, or that every Community act was invalid. The question is which premise each recipient verified against original sources and which it inherited.')}</p>
      <div class="psr-actions"><a href="${ricpeUrl}">${t('Seguir la ruta hacia RICPE', 'Continue the route to RICPE')}</a><a class="secondary" href="${controlUrl}">${t('Ver el nodo 7 junio 2018', 'See the 7 June 2018 node')}</a></div></div>`;
    const anchor = document.querySelector('#resumen') || document.querySelector('main .section');
    if (anchor) anchor.insertAdjacentElement('afterend', section); else insertAfterHero(section);
  }

  function addMultipleLivesConversions() {
    const multi = /\/(mismo-hotel-multiples-vidas-financieras|same-hotel-multiple-financial-lives)\/$/.test(path);
    if (!multi || document.getElementById('psr-conversion-matrix')) return;
    const section = document.createElement('section');
    section.id = 'psr-conversion-matrix';
    section.className = 'psr-module';
    section.innerHTML = `<div class="shell"><p class="psr-kicker">${t('Auditar conversiones antes de clasificar irregularidades', 'Audit conversions before classifying irregularities')}</p><h2>${t('Probar el solapamiento primero; clasificarlo después.', 'Prove overlap first; classify it second.')}</h2><p class="psr-intro">${t('La coexistencia de varias fuentes de financiación no prueba doble financiación. La auditoría debe demostrar o descartar, tramo a tramo, cómo una premisa se convirtió en la siguiente y si la verificación fue independiente.', 'The coexistence of several funding sources does not prove double funding. The audit must show or rule out, step by step, how one premise became the next and whether verification was independent.')}</p><div class="psr-matrix-wrap"><table class="psr-matrix"><thead><tr><th>${t('Conversión', 'Conversion')}</th><th>${t('Pregunta raíz', 'Root question')}</th><th>${t('Prueba que resolvería', 'Evidence that resolves it')}</th></tr></thead><tbody>
      <tr><td>${t('Propiedad → voto', 'Ownership → vote')}</td><td>${t('¿Qué fincas/coefs daban derecho a participar?', 'Which units/coefficients conferred voting rights?')}</td><td>${t('Título, coeficientes, asistencia, poderes.', 'Title, coefficients, attendance, proxies.')}</td></tr>
      <tr><td>${t('Voto → autoridad', 'Vote → authority')}</td><td>${t('¿Qué acuerdo nombró válidamente a quien actuó después?', 'Which resolution validly appointed the later actor?')}</td><td>${t('Convocatoria, acta, mandato y cadena de nombramiento.', 'Notice, minutes, mandate and appointment chain.')}</td></tr>
      <tr><td>${t('Autoridad → deuda', 'Authority → debt')}</td><td>${t('¿Quién creó, calculó y certificó la obligación?', 'Who created, calculated and certified the liability?')}</td><td>${t('Presupuesto, reparto, libros, facturas y certificado.', 'Budget, allocation, ledgers, invoices and certificate.')}</td></tr>
      <tr><td>${t('Autoridad → acceso', 'Authority → access')}</td><td>${t('¿Qué poder permitía seguridad, mantenimiento o entrada?', 'What power allowed security, maintenance or entry?')}</td><td>${t('Acta, contrato, autorización AC, finca/perímetro.', 'Minutes, contract, AC authorisation, unit/perimeter.')}</td></tr>
      <tr><td>${t('Acceso → proyecto', 'Access → project')}</td><td>${t('¿Cómo se convirtió control material en disponibilidad del activo?', 'How did material control become asset availability?')}</td><td>${t('Comunicaciones, DD, planos, contratos, título.', 'Communications, DD, plans, contracts, title.')}</td></tr>
      <tr><td>${t('Proyecto → RICPE', 'Project → RICPE')}</td><td>${t('¿Qué recibió RICPE y qué comprobó por sí mismo?', 'What did RICPE receive and independently verify?')}</td><td>${t('Data room, informes, conflictos, comité, Consejo.', 'Data room, reports, conflicts, committee, Board.')}</td></tr>
      <tr><td>${t('RICPE → dinero', 'RICPE → money')}</td><td>${t('¿Qué condiciones/dispensas permitieron desembolsar?', 'Which conditions/waivers allowed drawdown?')}</td><td>${t('Acuerdos, condiciones, dispensas, drawdowns.', 'Approvals, conditions, waivers, drawdowns.')}</td></tr>
      <tr><td>${t('Obras → ayudas', 'Works → public support')}</td><td>${t('¿Eran los mismos costes o bases distintas?', 'Were they the same costs or distinct bases?')}</td><td>${t('Factura por factura, source-and-use, empleo por periodo.', 'Invoice-by-invoice, source-and-use, employment by period.')}</td></tr>
      <tr><td>${t('Financiación → valor MYND', 'Funding → MYND value')}</td><td>${t('¿Qué activos, obras y empleos generan hoy el valor?', 'Which assets, works and jobs generate today’s value?')}</td><td>${t('Activo fijo, PMS, nómina, ingresos, finca por finca.', 'Fixed assets, PMS, payroll, revenue, unit-by-unit map.')}</td></tr>
      </tbody></table></div></div>`;
    insertAfterHero(section);
  }

  function addFundingAuthorityPrefix() {
    const institutional = /\/(cadena-instrumentalizacion-ric-fondos-incentivos|institutionalisation-chain-ric-eu-incentives)\/$/.test(path);
    if (!institutional || document.getElementById('psr-authority-before-funds')) return;
    const section = document.createElement('section');
    section.id = 'psr-authority-before-funds';
    section.className = 'psr-module alt';
    section.innerHTML = `<div class="shell"><p class="psr-kicker">${t('La cadena empieza antes del dinero', 'The chain starts before the money')}</p><h2>${t('Título → voto → autoridad → disponibilidad → control financiero.', 'Title → vote → authority → availability → financial control.')}</h2><p class="psr-intro">${t('Antes de comparar RIC, subvención, FEDER o financiación privada, debe fijarse quién podía obligar a qué finca, quién podía autorizar obras y qué derecho sobre el activo se presentó a cada financiador o administración.', 'Before comparing RIC, subsidy, ERDF or private funding, the analysis must establish who could bind which unit, who could authorise works, and what right over the asset was represented to each funder or authority.')}</p><div class="psr-actions"><a href="${communityUrl}">${t('Auditar autoridad de la Comunidad', 'Audit Community authority')}</a><a class="secondary" href="${ricpeUrl}">${t('Auditar controles RICPE', 'Audit RICPE controls')}</a></div></div>`;
    insertAfterHero(section);
  }

  function addHomeJourney() {
    const isHome = path === `${root}${lang}/`;
    if (!isHome || document.getElementById('psr-home-unitary-path')) return;
    const main = document.querySelector('main');
    if (!main) return;
    const box = document.createElement('section');
    box.id = 'psr-home-unitary-path';
    box.className = 'psr-home-path';
    box.innerHTML = `<div class="inner"><p class="psr-kicker">${t('Ruta recomendada para una primera visita', 'Recommended route for a first visit')}</p><h2>${t('Siga un solo activo a través de todo el sistema.', 'Follow one asset through the whole system.')}</h2><p>${t('Empiece por la autoridad y termine en el resultado operativo. Cada etapa separa hechos, alegaciones, inferencias y cuestiones abiertas.', 'Start with authority and end with the operating outcome. Each stage separates facts, allegations, inferences and open questions.')}</p><div class="steps"><a href="${communityUrl}">1 · ${t('Comunidad', 'Community')}</a><a href="${controlUrl}">2 · ${t('Control 2018', '2018 control')}</a><a href="${insolvencyUrl}">3 · ${t('Concurso', 'Insolvency')}</a><a href="${ricpeUrl}">4 · RICPE</a><a href="${fundingUrl}">5 · ${t('Financiación', 'Funding')}</a><a href="${myndUrl}">6 · MYND</a><a href="${recoveryUrl}">7 · ${t('Recuperación', 'Recovery')}</a></div></div>`;
    const hero = main.querySelector('.hero, .dossier-hero');
    if (hero) hero.insertAdjacentElement('afterend', box); else main.insertAdjacentElement('afterbegin', box);
  }

  function addUpdatesCard() {
    const updates = /\/(actualizaciones|updates)\/$/.test(path);
    if (!updates || document.getElementById('psr-update-ricpe-17aug')) return;
    const main = document.querySelector('main');
    if (!main) return;
    const card = document.createElement('article');
    card.id = 'psr-update-ricpe-17aug';
    card.className = 'psr-update-card';
    card.innerHTML = `<div class="meta"><span>17 ${t('ago', 'Aug')} 2026</span><span>RICPE</span><span>${t('Canal Ético', 'Ethical Channel')}</span></div><h3>${t('Comunicación formal presentada a RICPE', 'Formal communication submitted to RICPE')}</h3><p>${t('La presentación por el Canal Ético y el acuse técnico de plataforma están corroborados. La comunicación solicita preservación, explicación independiente de gobierno/título/DD/conflictos/financiación y una decisión institucional trazable.', 'Ethical Channel submission and technical platform acknowledgment are corroborated. The communication requests preservation, independent explanation of governance/title/DD/conflicts/funding, and a traceable institutional decision.')}</p><p><strong>${t('Límite:', 'Boundary:')}</strong> ${t('no constan todavía admisión, investigación, control de conflictos, preservación, tratamiento del Consejo ni decisión de fondo.', 'admission, investigation, conflict screening, preservation, Board treatment and a merits decision are not yet established.')}</p><div class="psr-actions"><a href="${ricpeUrl}">${t('Abrir la lectura RICPE de 7 minutos', 'Open the 7-minute RICPE read')}</a></div>`;
    const target = main.querySelector('.updates-list, .update-list, .section .shell, .shell');
    if (target) target.insertAdjacentElement('afterbegin', card); else main.insertAdjacentElement('afterbegin', card);
  }

  function addDeepContext() {
    const deep = /actas-2011-2022|minutes-2011-2022|toma-control-sun-park-7-junio-2018|sun-park-takeover-7-june-2018/.test(path);
    if (!deep || document.getElementById('psr-deep-context')) return;
    const main = document.querySelector('main');
    if (!main) return;
    const note = document.createElement('aside');
    note.id = 'psr-deep-context';
    note.className = 'psr-module';
    note.innerHTML = `<div class="shell"><p class="psr-kicker">${t('Está leyendo un nodo de prueba', 'You are reading one evidence node')}</p><p class="psr-intro">${t('Este documento forma parte de una reconstrucción unitaria. No trate este nodo como si validara por sí solo título, autoridad, posesión, financiación o responsabilidad posteriores.', 'This document is part of a unitary reconstruction. Do not treat this node as independently validating later title, authority, possession, funding or responsibility.')}</p><div class="psr-actions"><a href="${communityUrl}">${t('Contexto anterior: Comunidad', 'Previous context: Community')}</a><a class="secondary" href="${ricpeUrl}">${t('Siguiente: RICPE / proyecto', 'Next: RICPE / project')}</a></div></div>`;
    const hero = main.querySelector('.dossier-hero, .hero');
    if (hero) hero.insertAdjacentElement('afterend', note);
  }

  function addCriminalLensNote() {
    const targetRoute = /\/(comunidad-instrumentalizacion|community-instrumentalisation|ric-private-equity-sun-park)\/$/.test(path);
    if (!targetRoute || document.getElementById('psr-criminal-lens-boundary')) return;
    const main = document.querySelector('main');
    if (!main) return;
    const note = document.createElement('section');
    note.id = 'psr-criminal-lens-boundary';
    note.className = 'psr-module';
    note.innerHTML = `<div class="shell"><p class="psr-kicker">${t('Lente penal/investigativa separada', 'Separate criminal/investigative lens')}</p><p class="psr-intro">${t('La validez o invalidez civil, concursal o administrativa no decide por sí sola la relevancia penal. Para cada actor se separan acto, conocimiento, aviso contrario, representación u omisión, uso, confianza/reliance, beneficio, perjuicio, causalidad y explicación lícita alternativa. Una inconsistencia no se convierte automáticamente en dolo ni una resolución institucional adversa en participación criminal.', 'Civil, insolvency or administrative validity or invalidity does not by itself determine criminal relevance. For each actor the analysis separates act, knowledge, contrary notice, representation or omission, use, reliance, benefit, harm, causation and the strongest lawful alternative explanation. An inconsistency does not automatically become intent, nor does an adverse institutional decision become criminal participation.')}</p></div>`;
    main.appendChild(note);
  }

  function apply() {
    addRail();
    addHomeJourney();
    addRicpeCockpit();
    addCommunityBridge();
    addMultipleLivesConversions();
    addFundingAuthorityPrefix();
    addUpdatesCard();
    addDeepContext();
    addCriminalLensNote();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => setTimeout(apply, 350), { once: true });
  else setTimeout(apply, 350);
  setTimeout(apply, 1200);
})();
