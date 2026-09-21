(() => {
  const path = window.location.pathname.replace(/index\.html$/, '');
  const es = path.includes('/es/');
  const target = es ? '/por-derecho/es/arquitectura-nodo-documental-jdam/' : '/por-derecho/en/architecture-documentary-node-jdam/';
  const label = es ? 'Arquitectura' : 'Architecture';
  const title = es ? 'Arquitectura como nodo documental' : 'Architecture as a documentary node';
  const text = es
    ? 'El visado de 25/02/2022 se integra en una cadena que conecta autoridad aparente, encargo, proyecto, Yaiza, turismo, inversión, financiación, RIC/REF, incentivos, operación y prueba judicial. El registro separa hechos, alegaciones, límites y preguntas finitas para COALZ y COAGC.'
    : 'The 25 February 2022 visado sits within a chain connecting apparent authority, commission, project, Yaiza, tourism, investment, finance, RIC/REF, public support, operation and judicial evidence. The record separates facts, allegations, limits and finite questions for COALZ and COAGC.';
  const relevant = [
    '/es/', '/en/',
    'acosta-matos-perimetro', 'acosta-matos-perimeter',
    'comunidad-instrumentalizacion', 'community-instrumentalisation',
    'toma-control-sun-park', 'sun-park-takeover',
    'mismo-hotel-multiples-vidas-financieras', 'same-hotel-multiple-financial-lives',
    'ingenieria-criminal', 'criminal-engineering', 'investigacion-penal', 'criminal-investigation',
    'autoridad-publica', 'public-authority', 'institucional', 'institutional',
    'ric-private-equity-sun-park', 'ricpe-responsabilidad-documental', 'ricpe-documentary-accountability',
    'ricpe-idoneidad', 'orion-ricpe', 'portfolio-orion',
    'san-telmo-ricpe-sun-park',
    'pwc-canarias-carlos-saavedra-sun-park', 'pwc-canary-islands-carlos-saavedra-sun-park',
    'grant-thornton/2024-04', 'rsm/nnr4-1025c2f66',
    'cabildo-lanzarote-turismo-trazabilidad', 'cabildo-lanzarote-tourism-traceability',
    'yaiza', 'turismo', 'tourism', 'feder', 'fondos', 'funds', 'incentivos', 'incentives',
    'intervencion-general', 'audiencia-cuentas', 'audit-office',
    'concurso-36-2012', 'insolvency-36-2012',
    'actualizaciones', 'updates'
  ].some(x => path === '/por-derecho' + x || path.includes(x));

  const style = document.createElement('style');
  style.textContent = `.jdam-architecture-gateway{max-width:1120px;margin:1.5rem auto;padding:1.15rem 1.25rem;border-radius:16px;background:#f6f1e5;border:1px solid rgba(19,37,45,.18);border-left:6px solid #9a6813;box-sizing:border-box}.jdam-architecture-gateway strong{display:block;font-size:1.2rem;margin-bottom:.35rem}.jdam-architecture-gateway p{margin:.35rem 0 .75rem;line-height:1.55}.jdam-architecture-gateway a{font-weight:850}.jdam-update{border-left-color:#9a6813!important}.jdam-ir-current{position:relative}.jdam-ir-current::before{content:'20·08·2026';position:absolute;right:0;top:1rem;background:#9a6813;color:#fff;border-radius:999px;padding:.25rem .55rem;font-size:.67rem;font-weight:900;letter-spacing:.06em}`;
  document.head.appendChild(style);

  const spanishCoagc = () => `
    <div class="ir-record-head"><div><span class="ir-number">10</span><h2>Colegio Oficial de Arquitectos de Gran Canaria — COAGC</h2><p><strong>Competencia:</strong> colegiación, habilitación, registros históricos, corrección profesional y deontología dentro de su propio ámbito. El artículo 44.3 del Real Decreto 129/2018 sitúa en COALZ la competencia disciplinaria principal sobre la actuación material desarrollada en Lanzarote, pero no permite dejar sin autenticar o explicar los registros que solo el COAGC custodia.</p></div><div class="ir-meta"><div><span>Última verificación</span><strong>20 agosto 2026</strong></div><div><span>Estado</span><strong>Respuesta territorial, discrepancia registral y distribución institucional completa; aclaración exacta pendiente</strong></div></div></div>
    <div class="ir-table-wrap"><table class="ir-table"><thead><tr><th scope="col">Fecha</th><th scope="col">Dirección</th><th scope="col">Referencia</th><th scope="col">Objeto / estado</th></tr></thead><tbody>
      <tr><td>13 jul 2026</td><td>COAGC → aportante</td><td>Art. 44.3 RD 129/2018</td><td>Indicó que la potestad disciplinaria principal correspondía al Colegio de Lanzarote por el lugar de la actuación profesional.</td></tr>
      <tr><td>22 jul 2026</td><td>COAGC → aportante</td><td>Respuesta de Pablo Cabrera</td><td>Manifestó que los datos aportados «no son coincidentes» con sus registros; no abrió referencia auxiliar; confirmó la custodia de los datos colegiales de D. José Daniel Acosta Matos; declaró que no constaba documentación Sun Park / MYND Yaiza y descartó coordinación sobre esa base.</td></tr>
      <tr><td>22 jul 2026</td><td>Aportante → COAGC</td><td>Solicitud de aclaración</td><td>Pidió identificar qué dato no coincidía —adscripción, 2315, 21428, situación o habilitación a 25/02/2022— y cuál era el dato profesional correcto. No se localizó respuesta posterior en el hilo revisado.</td></tr>
      <tr><td>20 ago 2026</td><td>Aportante → COAGC</td><td>Seguimiento y redistribución por cuatro canales funcionales</td><td>Comunicación separada posterior al envío a COALZ, seguida de redistribución íntegra a Colegio, Secretario, Secretaría y Supervisión/Visados. Solicitó reconciliación registral, preservación, alcance de la búsqueda, actos autónomos en Gran Canaria, coordinación, valoración del art. 262 LECrim si se alcanza el umbral y decisión motivada.</td></tr>
    </tbody></table></div>
    <div class="ir-controls"><div class="ir-control proves"><strong>Acredita</strong>El COAGC respondió sobre competencia territorial, afirmó custodiar datos colegiales propios, identificó una discrepancia concreta aunque no explicada, declaró el resultado de una búsqueda y recibió la comunicación de 20 agosto por la distribución funcional completa.</div><div class="ir-control limit"><strong>No acredita</strong>La discrepancia no prueba falsedad del visado, falta de colegiación o habilitación, actuación profesional autónoma, infracción deontológica, delito, coordinación ni decisión sobre el fondo.</div><div class="ir-control action"><strong>Acción finita pendiente</strong>Identificar el dato no coincidente; certificar la situación correcta a 25/02/2022; explicar 21428 y 2315; delimitar registros, periodo y custodio de la búsqueda; preservar su trazabilidad; comunicar la corrección a COALZ; y emitir decisión motivada con vía de revisión.</div></div>
    <div class="ir-links"><a href="../arquitectura-nodo-documental-jdam/">Registro completo JDAM / COALZ / COAGC →</a><a href="../#planos-sobre-la-mesa">Contexto técnico</a><a class="official" href="https://arquitectosgrancanaria.es/" rel="external noopener">Sitio oficial COAGC ↗</a></div>
    <p class="ir-source-note">La referencia al nexus de Gran Canaria identifica conexiones documentales, societarias, concursales, financieras, profesionales, institucionales y judiciales. No es una conclusión de que allí se cometiera una infracción. El silencio se registra como falta de respuesta, no como admisión.</p>`;

  const spanishCoalz = () => `
    <div class="ir-record-head"><div><span class="ir-number">11</span><h2>Colegio Oficial de Arquitectos de Lanzarote — COALZ</h2><p><strong>Competencia:</strong> vía territorial principal para verificar la actuación profesional y el expediente de visado vinculado al inmueble de Yaiza, sin decidir titularidad privada, concurso, urbanismo municipal, turismo, fiscalidad, ayudas públicas o responsabilidad penal.</p></div><div class="ir-meta"><div><span>Última verificación</span><strong>20 agosto 2026</strong></div><div><span>Estado</span><strong>Tres entradas registradas, traslado a la Junta y ampliación de 20 agosto; no localizada decisión de fondo</strong></div></div></div>
    <div class="ir-table-wrap"><table class="ir-table"><thead><tr><th scope="col">Fecha</th><th scope="col">Dirección</th><th scope="col">Referencia</th><th scope="col">Objeto / estado</th></tr></thead><tbody>
      <tr><td>13–14 jul 2026</td><td>Aportante → COALZ</td><td>RE 26/008230</td><td>Solicitud principal sobre D. José Daniel Acosta Matos, Sun Park / MYND Yaiza, visado 25/02/2022, ref. 22/000036/7800 y expediente Yaiza 1748/2022. Solicitó identificación, preservación, autoridad, archivos nativos, metadatos y posible verificación deontológica preliminar.</td></tr>
      <tr><td>15–16 jul 2026</td><td>Aportante → COALZ</td><td>RE 26/008474</td><td>Aportación adicional de identidad, representación societaria e interés patrimonial directo a requerimiento del propio Colegio.</td></tr>
      <tr><td>15–16 jul 2026</td><td>Aportante → COALZ</td><td>RE 26/008476</td><td>Hecho sobrevenido relativo a Yaiza y Cabildo. Isabel Arcas confirmó su traslado a la Junta del COALZ, «al igual que» las comunicaciones anteriores.</td></tr>
      <tr><td>20 ago 2026</td><td>Aportante → COALZ</td><td>Seguimiento dentro del hilo existente</td><td>Amplió el contexto con dos índices visuales españoles, fuente audiovisual directa, cronología PwC–Grant Thornton–San Telmo/RICPE–RSM y providencia de DP 1901/2026. Reiteró preservación, cliente/autoridad/perímetro, usos posteriores, reconciliación 21428/2315, actuación preliminar, art. 262 LECrim si procede y decisión expresa.</td></tr>
    </tbody></table></div>
    <div class="ir-controls"><div class="ir-control proves"><strong>Acredita</strong>COALZ recibió y registró tres aportaciones, pidió acreditación de relación, recibió esa documentación y trasladó el material a su Junta. La comunicación de 20 agosto quedó enviada en el mismo hilo con tres anexos.</div><div class="ir-control limit"><strong>No acredita</strong>Registro, recepción, traslado o envío no prueban preservación ejecutada, apertura de información reservada, expediente disciplinario, notificación a JDAM, infracción, delito ni decisión de fondo.</div><div class="ir-control action"><strong>Acción finita pendiente</strong>Confirmar gestor y referencia interna; preservar expediente, nativos y metadatos; decidir verificación preliminar o motivar su rechazo; reconstruir cliente, autoridad, perímetro y usos posteriores; conciliar 21428/2315; valorar art. 262 LECrim solo si se alcanza el umbral; e indicar vía de revisión.</div></div>
    <div class="ir-links"><a href="../arquitectura-nodo-documental-jdam/">Registro completo JDAM / COALZ / COAGC →</a><a href="../cabildo-lanzarote-turismo-trazabilidad/">Cabildo / Turismo</a><a class="official" href="https://coa-lz.com/arquitectos-lanzarote/" rel="external noopener">Sitio oficial COALZ ↗</a></div>
    <p class="ir-source-note">La providencia de DP 1901/2026 se utiliza solo como referencia judicial identificable y de preservación. No acredita admisión definitiva, delito o responsabilidad. Las dos imágenes son mapas de evidencia con límites expresos, no conclusiones periciales o colegiales.</p>`;

  const englishCoagc = () => `
    <div class="ir-record-head"><div><span class="ir-number">10</span><h2>Official College of Architects of Gran Canaria — COAGC</h2><p><strong>Competence:</strong> its own membership, habilitation, historical records, professional correction and professional-conduct functions. Article 44.3 of Royal Decree 129/2018 places primary disciplinary competence for the physical Lanzarote work with COALZ, but it does not leave COAGC's own historical records or identified discrepancy unauthenticated.</p></div><div class="ir-meta"><div><span>Last verified</span><strong>20 August 2026</strong></div><div><span>Status</span><strong>Territorial answer, record discrepancy and complete institutional distribution; exact clarification pending</strong></div></div></div>
    <div class="ir-table-wrap"><table class="ir-table"><thead><tr><th scope="col">Date</th><th scope="col">Direction</th><th scope="col">Reference</th><th scope="col">Object / status</th></tr></thead><tbody>
      <tr><td>13 Jul 2026</td><td>COAGC → contributor</td><td>Art. 44.3 RD 129/2018</td><td>Stated that primary disciplinary authority lay with the Lanzarote College because that was where the professional act occurred.</td></tr>
      <tr><td>22 Jul 2026</td><td>COAGC → contributor</td><td>Pablo Cabrera response</td><td>Said the supplied data did not coincide with its records; opened no auxiliary reference; confirmed custody of José Daniel Acosta Matos's membership data; reported no Sun Park / MYND Yaiza documentation and declined coordination on that basis.</td></tr>
      <tr><td>22 Jul 2026</td><td>Contributor → COAGC</td><td>Clarification request</td><td>Asked which datum differed — affiliation, 2315, 21428, status or habilitation on 25 February 2022 — and what the correct professional datum was. No later answer was located in the reviewed thread.</td></tr>
      <tr><td>20 Aug 2026</td><td>Contributor → COAGC</td><td>Follow-up and four-channel redistribution</td><td>Separate communication after the COALZ dispatch, followed by full redistribution to Colegio, Secretary, Secretariat and Supervision/Visados. It requested record reconciliation, preservation, search scope, autonomous Gran Canaria acts, coordination, Article 262 LECrim assessment if the threshold is met and a reasoned decision.</td></tr>
    </tbody></table></div>
    <div class="ir-controls"><div class="ir-control proves"><strong>Establishes</strong>COAGC answered on territorial competence, said it retains its own membership data, identified a specific but unexplained mismatch, reported a search result and received the 20 August communication through the complete functional distribution.</div><div class="ir-control limit"><strong>Does not establish</strong>The mismatch does not prove a false visado, lack of membership or habilitation, an autonomous professional act, a professional breach, an offence, coordination or a merits decision.</div><div class="ir-control action"><strong>Finite action pending</strong>Identify the non-matching datum; certify the correct 25 February 2022 position; explain 21428 and 2315; delimit the searched records, period and custodian; preserve the search trail; notify COALZ of any correction; and issue a reasoned, reviewable decision.</div></div>
    <div class="ir-links"><a href="../architecture-documentary-node-jdam/">Full JDAM / COALZ / COAGC record →</a><a href="../#plans-on-the-table">Technical context</a><a class="official" href="https://arquitectosgrancanaria.es/" rel="external noopener">Official COAGC site ↗</a></div>
    <p class="ir-source-note">Calling Gran Canaria a documentary nexus refers to corporate, insolvency, finance, professional, institutional and judicial connections. It is not a finding that a professional breach occurred there. Non-response is recorded as non-response, not admission.</p>`;

  const englishCoalz = () => `
    <div class="ir-record-head"><div><span class="ir-number">11</span><h2>Official College of Architects of Lanzarote — COALZ</h2><p><strong>Competence:</strong> primary territorial route for verification of the professional act and visado file linked to the Yaiza property, without deciding private title, insolvency, municipal planning, tourism, tax, public support or criminal liability.</p></div><div class="ir-meta"><div><span>Last verified</span><strong>20 August 2026</strong></div><div><span>Status</span><strong>Three registered entries, Board transfer and 20 August supplement; no merits decision located</strong></div></div></div>
    <div class="ir-table-wrap"><table class="ir-table"><thead><tr><th scope="col">Date</th><th scope="col">Direction</th><th scope="col">Reference</th><th scope="col">Object / status</th></tr></thead><tbody>
      <tr><td>13–14 Jul 2026</td><td>Contributor → COALZ</td><td>RE 26/008230</td><td>Principal request concerning José Daniel Acosta Matos, Sun Park / MYND Yaiza, the 25 February 2022 visado, ref. 22/000036/7800 and Yaiza file 1748/2022. It requested identification, preservation, authority records, native files, metadata and possible preliminary professional-conduct verification.</td></tr>
      <tr><td>15–16 Jul 2026</td><td>Contributor → COALZ</td><td>RE 26/008474</td><td>Additional identity, corporate-capacity and direct property-interest material provided after the College requested evidence of the contributor's relationship to the file.</td></tr>
      <tr><td>15–16 Jul 2026</td><td>Contributor → COALZ</td><td>RE 26/008476</td><td>Supervening-event update concerning Yaiza and Cabildo. Isabel Arcas confirmed transfer to the COALZ Board, as with the earlier communications.</td></tr>
      <tr><td>20 Aug 2026</td><td>Contributor → COALZ</td><td>Follow-up in the existing thread</td><td>Added two Spanish visual indexes, the direct audiovisual source, the PwC–Grant Thornton–San Telmo/RICPE–RSM chronology and the DP 1901/2026 order. It renewed requests concerning preservation, client/authority/perimeter, later uses, 21428/2315 reconciliation, preliminary action, Article 262 LECrim where applicable and an express decision.</td></tr>
    </tbody></table></div>
    <div class="ir-controls"><div class="ir-control proves"><strong>Establishes</strong>COALZ received and registered three submissions, requested relationship evidence, received that material and passed the record to its Board. The 20 August communication was sent in the same thread with three attachments.</div><div class="ir-control limit"><strong>Does not establish</strong>Registration, receipt, internal transfer or dispatch does not prove completed preservation, preliminary inquiry, disciplinary proceedings, notice to JDAM, breach, offence or merits determination.</div><div class="ir-control action"><strong>Finite action pending</strong>Confirm handler and internal reference; preserve the file, native data and metadata; decide preliminary verification or give reasons for refusal; reconstruct client, authority, perimeter and later use; reconcile 21428/2315; assess Article 262 LECrim only if the threshold is met; and identify the review route.</div></div>
    <div class="ir-links"><a href="../architecture-documentary-node-jdam/">Full JDAM / COALZ / COAGC record →</a><a href="../cabildo-lanzarote-tourism-traceability/">Cabildo / Tourism</a><a class="official" href="https://coa-lz.com/arquitectos-lanzarote/" rel="external noopener">Official COALZ site ↗</a></div>
    <p class="ir-source-note">The DP 1901/2026 order is used only as an identifiable judicial and preservation reference. It does not establish final admission, an offence or liability. The two images are evidence maps with express limits, not expert or College findings.</p>`;

  const synchroniseInstitutionalRecords = () => {
    if (!document.body.classList.contains('institutional-records-page')) return;
    const coagc = document.querySelector('#coagc');
    const coalz = document.querySelector('#coa-lanzarote');
    if (coagc) {
      coagc.classList.add('jdam-ir-current');
      coagc.dataset.jdamInstitutionalParity = '2026-08-20';
      coagc.innerHTML = es ? spanishCoagc() : englishCoagc();
    }
    if (coalz) {
      coalz.classList.add('jdam-ir-current');
      coalz.dataset.jdamInstitutionalParity = '2026-08-20';
      coalz.innerHTML = es ? spanishCoalz() : englishCoalz();
    }
  };

  const inject = () => {
    document.querySelectorAll('.main-nav').forEach(nav => {
      if (nav.querySelector('[data-jdam-architecture-nav]')) return;
      const a = document.createElement('a');
      a.href = target;
      a.textContent = label;
      a.dataset.jdamArchitectureNav = 'true';
      const lang = nav.querySelector('.language-link');
      if (lang) nav.insertBefore(a, lang); else nav.appendChild(a);
    });

    synchroniseInstitutionalRecords();

    if (relevant && !path.includes('arquitectura-nodo-documental-jdam') && !path.includes('architecture-documentary-node-jdam') && !document.querySelector('.jdam-architecture-gateway')) {
      const box = document.createElement('aside');
      box.className = 'jdam-architecture-gateway';
      box.setAttribute('data-jdam-architecture-gateway', '2026-08-20');
      box.innerHTML = `<strong>${title}</strong><p>${text}</p><a href="${target}">${es ? 'Abrir el registro JDAM / COALZ / COAGC →' : 'Open the JDAM / COALZ / COAGC record →'}</a>`;
      const hero = document.querySelector('main .hero, main section');
      if (hero) hero.insertAdjacentElement('afterend', box);
    }

    const updates = document.querySelector('.updates-page main');
    if (updates && !document.querySelector('#jdam-arquitectura-colegios-20ago')) {
      const section = document.createElement('section');
      section.className = 'updates-section';
      section.innerHTML = `<div class="shell"><section class="date-group"><h2>20 ${es ? 'agosto' : 'August'} 2026 · ${es ? 'arquitectura y deontología' : 'architecture and professional conduct'}</h2><div class="update-stream"><article class="material-update institutional jdam-update" id="jdam-arquitectura-colegios-20ago"><div class="update-meta"><span class="new">${es ? 'Nuevo' : 'New'}</span><span>JDAM</span><span>COALZ / COAGC</span></div><h3>${title}</h3><p>${text}</p><p>${es ? 'COALZ recibió tres entradas en julio y trasladó el material a su Junta. El 20 de agosto se remitió una ampliación en el hilo previo. COAGC recibió una comunicación separada y una redistribución por los cuatro canales funcionales utilizados en julio. Envío no equivale a investigación abierta ni decisión de fondo.' : 'COALZ received three July entries and passed the material to its Board. A supplemental communication was sent in the existing thread on 20 August. COAGC received a separate communication and redistribution through the four functional channels used in July. Sending does not mean an investigation or merits decision.'}</p><div class="update-actions"><a class="button" href="${target}">${es ? 'Abrir registro →' : 'Open record →'}</a></div></article></div></section></div>`;
      updates.insertBefore(section, updates.firstChild.nextSibling || updates.firstChild);
      const status = document.querySelector('.update-status strong');
      if (status) status.textContent = es ? '20 agosto 2026' : '20 August 2026';
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', inject, { once: true });
  else inject();
})();