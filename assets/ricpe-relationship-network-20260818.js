(() => {
  const PATH_RE = /\/(es|en)\/ric-private-equity-sun-park\/?$/;

  function renderRelationshipNetwork() {
    if (!PATH_RE.test(window.location.pathname)) return;

    const es = document.documentElement.lang === 'es';
    const sectionId = es ? 'red-relacional-ricpe-2019-2024' : 'ricpe-relationship-network-2019-2024';
    const webinarId = es ? 'tres-realidades-ricpe' : 'three-ricpe-realities';

    const nav = document.querySelector('.main-nav');
    if (nav) {
      const legacyWebinarLink = nav.querySelector(`a[href="#${webinarId}"]`);
      if (legacyWebinarLink) {
        legacyWebinarLink.href = `#${sectionId}`;
        legacyWebinarLink.textContent = es ? 'Relación RICPE 2019–24' : 'RICPE relationship 2019–24';
      } else if (!nav.querySelector(`a[href="#${sectionId}"]`)) {
        const link = document.createElement('a');
        link.href = `#${sectionId}`;
        link.textContent = es ? 'Relación RICPE 2019–24' : 'RICPE relationship 2019–24';
        const updateLink = nav.querySelector('.nav-update');
        nav.insertBefore(link, updateLink || null);
      }
    }

    const heroActions = document.querySelector('.dossier-hero .actions');
    if (heroActions) {
      const legacyButton = heroActions.querySelector(`a[href="#${webinarId}"]`);
      if (legacyButton) {
        legacyButton.href = `#${sectionId}`;
        legacyButton.textContent = es ? 'Ver relación, reuniones y controles' : 'See relationship, meetings and controls';
      } else if (!heroActions.querySelector(`a[href="#${sectionId}"]`)) {
        const button = document.createElement('a');
        button.className = 'button secondary';
        button.href = `#${sectionId}`;
        button.textContent = es ? 'Ver relación, reuniones y controles' : 'See relationship, meetings and controls';
        heroActions.appendChild(button);
      }
    }

    if (document.getElementById(sectionId)) return;

    const hero = document.querySelector('.dossier-hero');
    if (!hero) return;

    const section = document.createElement('section');
    section.className = 'section alt';
    section.id = sectionId;
    section.setAttribute('aria-labelledby', `${sectionId}-title`);

    section.innerHTML = es ? `
      <div class="shell">
        <div class="section-head">
          <div>
            <p class="kicker">2019–2024 · reconstrucción de relación, no de un solo evento</p>
            <h2 id="${sectionId}-title">No fue un único webinar: fue una cadena de reuniones, análisis, asesores, inversores y formalización.</h2>
          </div>
          <p>El 11 de noviembre de 2020 es una fotografía pública especialmente útil, pero no es la unidad de análisis correcta. El propio material preservado describe una relación operativa más amplia: origen y selección de proyectos, análisis iniciado meses antes, asesoramiento fiscal y jurídico, due diligence, control externo de riesgo, compromisos de inversión, negociación y formalización, validación técnica de desembolsos, seguimiento y contactos institucionales.</p>
        </div>

        <aside class="pressure-maxim" role="note" aria-label="Regla de lectura de la relación RICPE Acosta Matos">
          <strong>Regla de lectura:</strong>
          <span>La pregunta no es sólo «¿qué se dijo en un webinar?». Es <b>quién introdujo a quién, quién convocó cada reunión, qué asesor preparó cada paso, qué documentación circuló, qué inversores participaron, qué autoridad o fedatario intervino en la formalización y qué conocimiento llegó a cada decisor, desde 2019 y con seguimiento reforzado en 2022–2024</b>.</span>
        </aside>

        <div class="control-table-wrap" role="region" aria-label="Mapa de interacciones RICPE y Acosta Matos" tabindex="0">
          <table class="control-table">
            <thead><tr><th>Carril</th><th>Lo que el material de 11 noviembre 2020 documenta o describe</th><th>Qué debe producirse para Sun Park</th></tr></thead>
            <tbody>
              <tr><td><strong>RICPE ↔ Acosta Matos</strong></td><td>José Acosta aparece como director general de Construcciones Acosta Matos y consejero de RICPE; afirma que tres proyectos turísticos del grupo fueron puestos en la cartera de RICPE.</td><td>Introducción inicial, agendas, llamadas, reuniones, presentaciones, data room, comité, Consejo, decisiones y seguimientos, con fecha y asistentes.</td></tr>
              <tr><td><strong>Fiscal / RIC</strong></td><td>Murli Kessomal interviene como asesor fiscal y vicesecretario; se describen expedientes e informes de Gobierno de Canarias/Administración tributaria y un filtro fiscal previo al Consejo.</td><td>Expedientes concretos, consultas, informes, correos, reuniones, reservas, autoría y fecha aplicables al proyecto Sun Park.</td></tr>
              <tr><td><strong>Legal y formalización</strong></td><td>Enrique Guerra afirma que los abogados que tramitan el proceso son Uría Menéndez de Madrid y sitúa dentro del proceso el estudio, análisis, negociación y formalización.</td><td>Hoja de encargo, equipo, reuniones, instrucciones, versiones, closing checklist, escrituras/contratos y cualquier reserva sobre título, concurso o terceros.</td></tr>
              <tr><td><strong>Due diligence legal/fiscal</strong></td><td>Se atribuye a Pricewaterhouse la due diligence legal y fiscal de la compañía y, en especial, del proyecto.</td><td>Informe Sun Park completo, alcance, reliance, anexos, fuentes registrales, preguntas, respuestas, reservas y circulación interna.</td></tr>
              <tr><td><strong>Financiero y seguimiento</strong></td><td>RICPE describe due diligence financiera interna y seguimiento trimestral; Guerra vincula los desembolsos al grado de ejecución.</td><td>Modelo financiero, solvencia, minutas de seguimiento, covenant review, desembolsos, facturas y decisiones 2020–2024.</td></tr>
              <tr><td><strong>Riesgo externo</strong></td><td>Guerra identifica a Intermoney como área de control de riesgo externalizada y dice que el Consejo no puede valorar un proyecto sin informe favorable y vinculante.</td><td>Informe específico Sun Park, fecha, hipótesis de título/propiedad, garantías, reservas, actualizaciones y destinatarios.</td></tr>
              <tr><td><strong>Técnico / obra</strong></td><td>Se describe un arquitecto asesor técnico que controla la obra, valida facturas y determina cuándo procede desembolsar.</td><td>Identidad, mandato, visitas, certificados, fotografías, facturas validadas, hitos de obra y comunicaciones con CAM/RICPE.</td></tr>
              <tr><td><strong>Seguro</strong></td><td>AON se menciona expresamente como ejemplo de asesor de seguros.</td><td>No se atribuye a AON el encargo Sun Park sin prueba. Debe identificarse el broker/asegurador real, pólizas, inspecciones y comunicaciones del proyecto.</td></tr>
              <tr><td><strong>Otros inversores</strong></td><td>El webinar habla de compromisos de inversión, terceros inversores que acompañan al promotor y de la experiencia de José Acosta como inversor en RICPE.</td><td>Quién invirtió en qué vehículo/proyecto, cuándo fue solicitado el capital, qué información recibió y qué decisiones o reuniones precedieron cada compromiso.</td></tr>
              <tr><td><strong>Eventos institucionales</strong></td><td>Guerra menciona un acto institucional distinto del webinar con presencia del Presidente del Gobierno de Canarias y de una representante de la AEAT. El material preservado incorpora además un programa separado de «Reinicio del Turismo en Canarias» de 9 noviembre 2020.</td><td>Conciliar fechas, invitaciones, lista de asistentes, agenda, reuniones laterales, documentación entregada y cualquier petición o respuesta institucional sobre los proyectos.</td></tr>
              <tr><td><strong>Notaría / fedatarios / cierre</strong></td><td>El webinar sí habla de negociación y formalización, pero no identifica por sí solo a un notario concreto de Sun Park.</td><td>Reconstruir escrituras, poderes, números de protocolo, notarios, borradores, citas, correos de cierre, asistentes y documentos entregados. No atribuir un fedatario hasta localizar la fuente primaria.</td></tr>
            </tbody>
          </table>
        </div>

        <div class="evidence-pair">
          <article class="privacy-callout"><strong>Febrero de 2020: análisis previo.</strong><span>En el turno de preguntas, Enrique Guerra dice que el análisis de los proyectos había empezado en febrero. Esto sitúa la relación de trabajo antes del webinar y obliga a buscar reuniones, encargos y documentación anteriores.</span></article>
          <article class="privacy-callout"><strong>Noviembre de 2020: más de un evento.</strong><span>El webinar de 11 noviembre convivió con otro acto institucional referido por RICPE y con materiales de un evento separado de 9 noviembre. La fecha exacta de cada contacto debe conciliarse documentalmente, no presumirse.</span></article>
        </div>

        <div class="proof-split" role="group" aria-label="Alcance de reconstrucción 2022 a 2024">
          <div><strong>2022–2024 no es un epílogo</strong><span>La reconstrucción debe seguir las reuniones y comunicaciones posteriores a adjudicación, dación, reorganización CAM→HNT, apertura MYND Yaiza, prospectos posteriores, seguimiento, garantías, refinanciación, reembolso o salida.</span></div>
          <div><strong>Regla de evidencia</strong><span>Una firma mencionada en el webinar prueba la manifestación sobre su función general; no prueba automáticamente que esa firma asumiera un encargo Sun Park concreto ni cuál fue su conclusión. Cada relación se vincula a encargo, fecha, equipo, documento y custodio.</span></div>
        </div>

        <div class="actions">
          <a class="button" href="#${webinarId}">Abrir el nodo público de 11 noviembre 2020</a>
          <a class="button secondary" href="../cnmv-ricpe-verificacion/">Ver verificación CNMV / RICPE</a>
          <a class="button secondary" href="../ricpe-responsabilidad-documental/">Ver responsabilidad documental</a>
        </div>
      </div>
    ` : `
      <div class="shell">
        <div class="section-head">
          <div>
            <p class="kicker">2019–2024 · relationship reconstruction, not a single event</p>
            <h2 id="${sectionId}-title">It was not one webinar: it was a chain of meetings, analysis, advisers, investors and formalisation.</h2>
          </div>
          <p>The 11 November 2020 webinar is an unusually useful public snapshot, but it is not the correct unit of analysis. The preserved material itself describes a broader operating relationship: project origination and selection, analysis begun months earlier, tax and legal advice, due diligence, external risk control, investor commitments, negotiation and formalisation, technical validation of drawdowns, monitoring and institutional contacts.</p>
        </div>

        <aside class="pressure-maxim" role="note" aria-label="RICPE Acosta Matos relationship reading rule">
          <strong>Reading rule:</strong>
          <span>The question is not only “what was said in one webinar?”. It is <b>who introduced whom, who arranged each meeting, which adviser prepared each step, what documents circulated, which investors participated, which authority or notarial officer took part in formalisation, and what knowledge reached each decision-maker from 2019 onward, with an enhanced 2022–2024 pass</b>.</span>
        </aside>

        <div class="control-table-wrap" role="region" aria-label="RICPE and Acosta Matos interaction map" tabindex="0">
          <table class="control-table">
            <thead><tr><th>Lane</th><th>What the 11 November 2020 material documents or describes</th><th>What must be produced for Sun Park</th></tr></thead>
            <tbody>
              <tr><td><strong>RICPE ↔ Acosta Matos</strong></td><td>José Acosta appears as managing director of Construcciones Acosta Matos and a RICPE director; he says three group tourism projects had been put into RICPE's portfolio.</td><td>Initial introduction, diaries, calls, meetings, presentations, data room, committee, Board decisions and monitoring, with dates and attendees.</td></tr>
              <tr><td><strong>Tax / RIC</strong></td><td>Murli Kessomal speaks as tax adviser and deputy secretary; the process describes Government of the Canary Islands/tax-administration files and reports plus a fiscal filter before Board review.</td><td>Project-specific files, queries, reports, emails, meetings, qualifications, authorship and dates applicable to Sun Park.</td></tr>
              <tr><td><strong>Legal and formalisation</strong></td><td>Enrique Guerra says the lawyers handling the process are Uría Menéndez in Madrid and places study, analysis, negotiation and formalisation within the process.</td><td>Engagement letter, team, meetings, instructions, versions, closing checklist, deeds/contracts and any qualification concerning title, insolvency or third parties.</td></tr>
              <tr><td><strong>Legal/tax due diligence</strong></td><td>Pricewaterhouse is described as carrying out legal and tax due diligence of the company and, especially, the project.</td><td>Complete Sun Park report, scope, reliance, annexes, registry sources, questions, answers, qualifications and internal circulation.</td></tr>
              <tr><td><strong>Financial / monitoring</strong></td><td>RICPE describes internal financial due diligence and quarterly monitoring; Guerra links drawdowns to progress of the project.</td><td>Financial model, solvency work, monitoring minutes, covenant review, drawdowns, invoices and decisions across 2020–2024.</td></tr>
              <tr><td><strong>External risk</strong></td><td>Guerra identifies Intermoney as outsourced risk-control function and says the Board cannot consider a project without its favourable binding report.</td><td>Sun Park-specific report, date, title/ownership assumptions, security assumptions, qualifications, updates and recipients.</td></tr>
              <tr><td><strong>Technical / works</strong></td><td>A technical architect is described as monitoring works, validating invoices and determining when loan drawdowns may be made.</td><td>Identity, mandate, visits, certificates, photographs, validated invoices, milestones and communications with CAM/RICPE.</td></tr>
              <tr><td><strong>Insurance</strong></td><td>AON is expressly given as an example of an insurance adviser.</td><td>Do not attribute a Sun Park engagement to AON without evidence. Identify the actual broker/insurer, policies, inspections and project communications.</td></tr>
              <tr><td><strong>Other investors</strong></td><td>The webinar refers to investment commitments, third-party investors accompanying the promoter and José Acosta's experience as a RICPE investor.</td><td>Who invested through which vehicle/project, when capital was called, what information was supplied and which decisions or meetings preceded each commitment.</td></tr>
              <tr><td><strong>Institutional events</strong></td><td>Guerra refers to an institutional RICPE event distinct from the webinar, attended by the President of the Canary Islands Government and an AEAT representative. The preserved material also contains a separate 9 November 2020 “Reinicio del Turismo en Canarias” programme.</td><td>Reconcile dates, invitations, attendance lists, agenda, side meetings, documents delivered and any institutional request or response concerning the projects.</td></tr>
              <tr><td><strong>Notary / closing officers</strong></td><td>The webinar does refer to negotiation and formalisation, but does not by itself identify a particular Sun Park notary.</td><td>Reconstruct deeds, powers, protocol numbers, notaries, drafts, appointments, closing emails, attendees and documents delivered. Do not attribute a notary until the primary record is located.</td></tr>
            </tbody>
          </table>
        </div>

        <div class="evidence-pair">
          <article class="privacy-callout"><strong>February 2020: prior analysis.</strong><span>During Q&A, Enrique Guerra says analysis of the projects began in February. That places the working relationship before the webinar and requires a search for earlier meetings, mandates and documents.</span></article>
          <article class="privacy-callout"><strong>November 2020: more than one event.</strong><span>The 11 November webinar sat alongside another institutional event referred to by RICPE and preserved material for a separate 9 November event. Exact dates and contacts must be reconciled from records, not assumed.</span></article>
        </div>

        <div class="proof-split" role="group" aria-label="2022 to 2024 reconstruction scope">
          <div><strong>2022–2024 is not an epilogue</strong><span>The reconstruction must continue through meetings and communications after adjudication, dación, the CAM→HNT reorganisation, MYND Yaiza opening, later investor documents, monitoring, security, refinancing, repayment or exit.</span></div>
          <div><strong>Evidence rule</strong><span>A firm named in the webinar proves the representation about its general function; it does not automatically prove that the firm accepted a Sun Park-specific mandate or what it concluded. Each relationship must be tied to engagement, date, team, document and custodian.</span></div>
        </div>

        <div class="actions">
          <a class="button" href="#${webinarId}">Open the 11 November 2020 public node</a>
          <a class="button secondary" href="../cnmv-ricpe-verification/">See CNMV / RICPE verification</a>
          <a class="button secondary" href="../ricpe-documentary-accountability/">See documentary accountability</a>
        </div>
      </div>
    `;

    hero.insertAdjacentElement('afterend', section);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderRelationshipNetwork, { once: true });
  } else {
    renderRelationshipNetwork();
  }

  window.addEventListener('load', () => setTimeout(renderRelationshipNetwork, 250), { once: true });
})();