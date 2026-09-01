(() => {
  const path = window.location.pathname.replace(/\/+$/, '');
  const match = path.match(/\/(en|es)\/cuatrecasas-sun-park$/);
  if (!match || document.querySelector('[data-cuatrecasas-inigo-linkedin-record="20260306"]')) return;

  const lang = match[1];
  const isEs = lang === 'es';
  const message = 'Just received notice from the Madrid bar that you requested disciplinary action against me which has been adequately dismissed. This is an unloyal and unlawful move against a Friend Who help you tireless with all efforts. You are not a Friend and deserve the worst. Do not ever contact me and be sure I would Advise Everyone about the kind of person you are.';
  const escapeHTML = (value) => String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');

  const copy = isEs ? {
    eyebrow: 'AUDITORÍA UNITARIA · MENSAJE, CORREOS Y EXPEDIENTES OFICIALES',
    title: 'Un archivo procesal no responde al expediente profesional',
    intro: 'Dos capturas preservadas muestran, a las 12:13 PM del 6 de marzo de 2026, una cuenta de LinkedIn con el nombre visible “Inigo de Luisa Maiz”, el mensaje y un estado posterior de la interfaz. Se publican las copias exactas suministradas y, debajo, el texto literal con sus mayúsculas, gramática y ortografía:',
    capturesTitle: 'Las capturas, no sólo la transcripción',
    capturesIntro: 'Copias exactas de los dos archivos JPEG suministrados, publicadas sin alteración de imagen por autorización expresa de 1 de septiembre de 2026. Son las mejores copias de captura disponibles aportadas por el usuario, no exportaciones certificadas por LinkedIn. Pulse cada imagen para abrirla a resolución completa.',
    capture1Title: 'Captura 1 · identidad visible y mensaje completo.',
    capture1: 'Muestra el nombre de cuenta “Inigo de Luisa Maiz”, el mensaje de las 12:13 PM y el estado “LinkedIn member unable to receive messages”. No acredita por sí sola la fecha de calendario, la autoría certificada por el proveedor, la decisión del Colegio de Madrid ni la causa del estado posterior.',
    capture2Title: 'Captura 2 · estado posterior de la interfaz.',
    capture2: 'Muestra “LinkedIn Member”, el aviso de contenido no deseado o dañino y el estado de imposibilidad de recibir mensajes. No demuestra por sí sola borrado, bloqueo, desactivación, moderación ni otro motivo técnico.',
    openCapture: 'Abrir captura a resolución completa ↗',
    correctionTitle: 'Corrección necesaria a “adequately dismissed”',
    correction: 'ICAM 434/26 archivó la queja el 6 de marzo por prescripción disciplinaria. Sus consideraciones se declararon de alcance meramente dialéctico y quedaron a salvo acciones de otro orden. Ese mismo día se interpuso alzada; CCACM abrió 193/2026 y el 27 de agosto informó de que seguía en estudio. No se ha localizado resolución final sobre el fondo.',
    adverseTitle: 'Resultado institucional adverso que también debe leerse',
    adverse: 'En resolución separada de 1 de julio, ICAM 1487/26 trató el texto de LinkedIn como privado y personal tras el fin de la relación profesional, no apreció prueba de trascendencia fuera de la esfera privada ni de daño y consideró esa cuestión fuera de su competencia disciplinaria objetiva. Los actos procesales territorialmente distintos se remitieron a Tenerife. Ese resultado es contrario a la queja y se publica sin ocultarlo; no acredita autorización del despacho ni convierte la frase “adequately dismissed” en una decisión material sobre la queja profesional anterior.',
    auditTitle: 'Cada afirmación, en su contexto',
    auditIntro: 'La columna central expone la lectura más fuerte que permite el registro. La última columna marca lo que ese mismo registro no permite afirmar.',
    exact: 'Texto exacto',
    reading: 'Lectura documental',
    limit: 'Límite probatorio',
    clauses: [
      ['“Just received notice from the Madrid bar”', 'La cuenta visible afirmó haber recibido noticia del Colegio de Madrid.', 'La captura no es la notificación colegial ni autentica por proveedor la autoría, la hora de recepción o el contenido comunicado.'],
      ['“you requested disciplinary action against me”', 'Existió una queja que pidió examen profesional de la conducta atribuida.', 'Pedir examen no equivale a pedir una sanción predeterminada ni acredita infracción.'],
      ['“which has been adequately dismissed”', '“Adequately” es la valoración del remitente. El archivo localizado se apoyó en prescripción.', 'No es absolución de fondo ni prueba de finalización: hubo alzada y 193/2026 seguía en estudio el 27 de agosto.'],
      ['“an unloyal … move”', 'Es un juicio personal de deslealtad.', 'No es un hallazgo institucional y no responde a encargo, facturación, conflicto, retirada o ejecución.'],
      ['“an … unlawful move”', 'La cuenta calificó la queja de ilícita.', 'No se ha localizado decisión colegial o judicial que declare ilícita, abusiva o maliciosa la presentación.'],
      ['“against a Friend”', 'El registro permite que amistad y relación profesional facturada coexistieran.', 'La amistad no elimina el derecho a solicitar control profesional ni transforma el encargo en ayuda informal.'],
      ['“Who help you tireless with all efforts”', 'Los correos, facturas y actuaciones acreditan trabajo profesional sustancial.', '“Tireless” y “all efforts” son caracterizaciones personales. La cuestión sostenible es integración, implementación y handover, no trabajo cero.'],
      ['“You are not a Friend”', 'Es un juicio sobre una relación personal.', 'No resuelve ninguna cuestión profesional o probatoria.'],
      ['“deserve the worst”', 'El lenguaje es hostil y retributivo.', 'No identifica un acto concreto ni se presenta aquí como amenaza violenta, delito o infracción ya probada.'],
      ['“Do not ever contact me”', 'Es un límite inequívoco al contacto personal directo y se respeta.', 'No extingue vías de abogado, institucionales o procesales legalmente disponibles. Esta publicación no invita a contactar al remitente.'],
      ['“I would Advise Everyone”', 'Anuncia la intención de influir en la opinión de una audiencia indefinida.', 'No se ha probado difusión efectiva a terceros ni una campaña.'],
      ['“about the kind of person you are”', 'El cierre ataca el carácter del destinatario en lugar de responder al expediente documental.', 'No se presenta como difamación adjudicada ni como hecho imputable al despacho sin prueba separada.']
    ],
    emailTitle: 'Qué añade el registro de correos',
    emailIntro: 'La revisión dirigida del buzón conectado confirma una relación profesional sustancial, una tensión real por honorarios y una transición posterior al recobro. Son resúmenes públicos minimizados: no se publican correos completos, asuntos, direcciones ni identificadores privados. La búsqueda no certifica la integridad de todos los sistemas o archivos del despacho.',
    date: 'Fecha',
    emailRecord: 'Registro documentado',
    emailBoundary: 'Efecto y límite',
    emails: [
      ['2014–18', 'El registro muestra que el encargo de Cuatrecasas precedía a la intervención directa de Íñigo. Desde 2018, su trabajo se insertó en una arquitectura ya existente y se amplió materialmente más allá de la propuesta de entrada.', 'Impide atribuir a Íñigo todo el expediente histórico o tratar a LPB, Aweswell y Matkator como cliente/deudor universal. Cada workstream exige mapa propio.'],
      ['29 ene 2019', 'Íñigo escribió que el despacho estaba “fully committed to defending your interests”; a la vez cuantificó honorarios pendientes y advirtió del riesgo de “pencils down”.', 'Acredita encargo y defensa material, además de presión legítima por cobro; no prueba por sí solo negligencia ni obligación de trabajar gratis.'],
      ['26–28 jul 2019', 'Indicó que las reglas internas impedían nueva asistencia sin pago, ofreció ayuda puntual “as a friend, not as a lawyer” y después circuló una arquitectura detallada de préstamo puente y rescate.', 'Acredita coexistencia de roles personal y profesional y conocimiento integrado; no convierte toda ayuda personal en asesoramiento del despacho.'],
      ['7–30 oct 2019', 'Comunicó que el trabajo del despacho estaba suspendido por honorarios; después celebró resultados recientes y escribió que el trabajo, en particular el de Rosa, estaba dando fruto, antes de anunciar retirada formal.', 'Acredita trabajo y resultados, y sustenta la defensa de impago. Deja abierta la pregunta limitada sobre protección de urgencias y handover.'],
      ['26 may–3 jun 2020', 'Rosa concedió expresamente la venia y ofreció coordinación inmediata. Íñigo describió “2yrs of work in your interest” y señaló que cobros asumía el asunto.', 'Impide afirmar obstrucción de la venia. La integridad del traspaso sigue sin probarse; tampoco prueba que Íñigo dirigiera actuaciones ejecutivas posteriores.'],
      ['8 mar 2021', 'Se remitió a Íñigo un paquete confidencial sobre CNMV/RICPE/Sun Park.', 'Prueba transmisión, no lectura, aceptación de encargo, reenvío ni actuación.'],
      ['18 feb 2022', 'Íñigo comunicó una demanda total de 441.463 EUR, con dos bloques de principal, intereses y costes.', 'Es la cuantificación del remitente, no una liquidación independiente ni prueba de doble cobro. Exige conciliación única factura–pagaré–cobro.'],
      ['6 mar 2026', 'Ese mismo día se envió una comunicación de preservación a un canal de protección de datos del despacho. No se localizó respuesta ordinaria en el hilo revisado; existen avisos automáticos de portal de cumplimiento sin contenido visible en Gmail.', 'El envío no acredita recepción, lectura, investigación, silencio institucional ni admisión.'],
      ['24–27 ago 2026', 'La invitación posterior de conciliación y derecho de respuesta no se entregó a los destinatarios ensayados: hubo rebotes y expiración.', 'No puede presentarse como invitación recibida ni como silencio de Cuatrecasas.']
    ],
    attributionTitle: 'De expresión individual a expresión del despacho: cuatro niveles',
    attributionIntro: 'La respuesta tiene relevancia institucional porque nació de una queja sobre un encargo profesional sustancial. Esa conexión permite preguntas de capacidad, conocimiento y gobernanza; no autoriza a saltar directamente a una admisión corporativa.',
    attributionLevel: 'Nivel',
    attributionSupport: 'Lo que sostiene el registro',
    attributionLimit: 'Límite',
    attributionRows: [
      ['1 · Personal', 'Manifestación en primera persona atribuida a Íñigo de Luisa Maíz en las dos capturas preservadas.', 'No acredita por sí sola autoría certificada por proveedor, infracción, difusión, represalia o responsabilidad.'],
      ['2 · Socio / contexto profesional', 'La queja deriva de relación profesional facturada; correos anteriores emplearon la voz del despacho, invocaron reglas internas y trataron defensa y cobro.', 'No convierte toda frase personal en consejo del despacho ni prueba que Íñigo instruyera las actuaciones ETJ.'],
      ['3 · Conocimiento / gobernanza de firma', 'Ese día se envió preservación a un canal de la firma; recepción, conservación, escalado, conflicto, acceso y riesgo son preguntas documentales finitas.', 'Enviar no prueba recepción, investigación, ratificación, silencio institucional ni admisión.'],
      ['4 · Adopción / responsabilidad de firma', 'La expresión sería imputable al despacho si se prueban instrucción, autorización, adopción, ratificación, uso o fallo directamente imputable de gobernanza.', 'Condición de socio y contexto profesional no bastan para una declaración corporativa ni responsabilidad colectiva.']
    ],
    lagunaBridge: 'Puente La Laguna: el mensaje no prueba estafa procesal, delito concursal ni identidad del cesionario del remate. Sí documenta una reacción a control profesional y abre preguntas sobre si los archivos de la firma conectan conocimiento histórico, decisiones ETJ 2024–2026, reserva de cesión, destinatario/UBO, satisfacción única y el uso o comercialización de la finca 8584 dentro del hotel. La hipótesis de destinatario conectado con Acosta Matos es la valoración principal atribuida de Gil; sigue sin probarse.',
    questionsTitle: 'Preguntas que Cuatrecasas puede cerrar con documentos',
    questions: [
      '¿Qué mapa de cliente, deudor e instrumento conectó las facturas de Aweswell/LPB con los pagarés de Matkator?',
      '¿Qué registro contemporáneo integró riesgos de posesión, titularidad, financiación, concurso e implementación, y quién fue dueño de cada condición?',
      '¿Qué urgencias y plazos se protegieron o entregaron al cesar el encargo, más allá de la venia concedida?',
      '¿Qué revisión de conflicto, secreto, autoridad y crédito único precedió a cada decisión ejecutiva de 2024–2026?',
      '¿Recibió, preservó y evaluó el despacho el mensaje de 6 de marzo bajo sus controles, y puede documentar esa cadena sin atribuir responsabilidad colectiva por asociación?'
    ],
    provenanceTitle: 'Trazabilidad, contacto y derecho de corrección',
    provenance: 'Las capturas originales permanecen en custodia privada. La segunda conserva un cambio posterior de interfaz; no prueba por sí sola borrado, bloqueo, desactivación o moderación. La comunicación contemporánea sólo dijo que el mensaje “appears to have deleted it”, y la publicación mantiene esa reserva.',
    boundary: 'No se solicita contacto directo con Íñigo de Luisa. Cualquier corrección o respuesta verificable recibida por abogado, canal institucional o canal profesional autorizado se publicará con igual prominencia. La ausencia de respuesta no se tratará como admisión.',
    record: 'Abrir registro público controlado →',
    institutional: 'Abrir expediente ICAM / CCACM →',
    laguna: 'Abrir análisis La Laguna / remate →',
    dossier: 'Volver al expediente unitario Cuatrecasas ↑'
  } : {
    eyebrow: 'UNITARY AUDIT · MESSAGE, EMAILS AND OFFICIAL RECORDS',
    title: 'A procedural archive does not answer the professional record',
    intro: 'Two preserved captures show, at 12:13 PM on 6 March 2026, a LinkedIn account displaying the name “Inigo de Luisa Maiz”, the message and a later interface state. The exact supplied copies are published below, followed by the verbatim text, including its capitalization, grammar and spelling:',
    capturesTitle: 'The captures, not only the transcript',
    capturesIntro: 'Exact copies of the two supplied JPEG files, published without image alteration under express authorization dated 1 September 2026. They are the best available user-supplied screenshot copies, not provider-certified LinkedIn exports. Select either image to open it at full resolution.',
    capture1Title: 'Capture 1 · displayed identity and complete message.',
    capture1: 'Shows the account name “Inigo de Luisa Maiz”, the 12:13 PM message and the “LinkedIn member unable to receive messages” state. It does not by itself establish the calendar date, provider-certified authorship, the Madrid Bar outcome or the cause of the later state.',
    capture2Title: 'Capture 2 · later interface state.',
    capture2: 'Shows “LinkedIn Member”, the unwanted-or-harmful-content warning and the unable-to-receive-messages state. It does not by itself prove deletion, blocking, deactivation, moderation or another technical cause.',
    openCapture: 'Open full-resolution capture ↗',
    correctionTitle: 'The necessary correction to “adequately dismissed”',
    correction: 'ICAM 434/26 archived the complaint on 6 March because the disciplinary limitation period had elapsed. Its factual remarks were expressly only dialectical, and other avenues were reserved. An appeal was filed that day; CCACM opened 193/2026 and said on 27 August that it remained under study. No final merits resolution has been located.',
    adverseTitle: 'The adverse institutional outcome must also be read',
    adverse: 'In a separate 1 July decision, ICAM 1487/26 treated the LinkedIn text as private and personal after the professional relationship, found no evidence that it had passed beyond the private sphere or caused harm, and treated that issue as outside its objective disciplinary competence. Territorially distinct court conduct was referred to Tenerife. That outcome is adverse to the complaint and is reported without concealment; it does not establish firm authorization or turn “adequately dismissed” into a merits decision on the earlier professional-work complaint.',
    auditTitle: 'Every statement, in context',
    auditIntro: 'The middle column gives the strongest reading the record permits. The final column marks what the same record does not permit anyone to claim.',
    exact: 'Exact text',
    reading: 'Documentary reading',
    limit: 'Evidential limit',
    clauses: [
      ['“Just received notice from the Madrid bar”', 'The displayed account stated that it had received Madrid Bar notice.', 'The capture is not the Bar notice and does not provider-authenticate authorship, receipt time or the content communicated.'],
      ['“you requested disciplinary action against me”', 'A complaint existed and requested professional examination of attributed conduct.', 'Requesting examination is not demanding a predetermined sanction and does not establish misconduct.'],
      ['“which has been adequately dismissed”', '“Adequately” is the sender’s assessment. The located archive rested on limitation.', 'It is not a merits exoneration or proof of finality: an appeal followed and 193/2026 remained under study on 27 August.'],
      ['“an unloyal … move”', 'This is a personal judgment of disloyalty.', 'It is not an institutional finding and does not answer mandate, billing, conflict, withdrawal or enforcement.'],
      ['“an … unlawful move”', 'The account labelled the complaint unlawful.', 'No located Bar or court decision declares the submission unlawful, abusive or malicious.'],
      ['“against a Friend”', 'The record permits friendship and a billed professional relationship to have coexisted.', 'Friendship does not remove the right to request professional scrutiny or turn the mandate into informal help.'],
      ['“Who help you tireless with all efforts”', 'The emails, invoices and acts document substantial professional work.', '“Tireless” and “all efforts” are personal characterizations. The sustainable question is integration, implementation and handover—not zero work.'],
      ['“You are not a Friend”', 'This is a judgment about a personal relationship.', 'It resolves no professional or evidential issue.'],
      ['“deserve the worst”', 'The wording is hostile and retributive.', 'It identifies no specific act and is not presented here as a violent threat, crime or already-proved professional breach.'],
      ['“Do not ever contact me”', 'This is an unequivocal direct personal-contact boundary, and it is respected.', 'It does not extinguish legally available counsel, institutional or procedural routes. This publication does not invite anyone to contact the sender.'],
      ['“I would Advise Everyone”', 'It announces an intention to influence an undefined audience’s view.', 'No actual third-party dissemination or campaign has been proved.'],
      ['“about the kind of person you are”', 'The closing attacks the recipient’s character instead of answering the documentary record.', 'It is not presented as adjudicated defamation or as a firm act without separate proof.']
    ],
    emailTitle: 'What the email record adds',
    emailIntro: 'The targeted review of the connected mailbox confirms a substantial professional relationship, genuine fee pressure and a later transition to collection. These are minimized public summaries: no full emails, subjects, addresses or private identifiers are published. The search is not a completeness certificate for every firm system or archive.',
    date: 'Date',
    emailRecord: 'Documented record',
    emailBoundary: 'Effect and limit',
    emails: [
      ['2014–18', 'The record shows that the Cuatrecasas mandate predated Íñigo’s direct involvement. From 2018, his work entered an existing architecture and broadened materially beyond the entry proposal.', 'This prevents attributing the entire historic file to Íñigo or treating LPB, Aweswell and Matkator as one universal client/debtor. Each workstream needs its own map.'],
      ['29 Jan 2019', 'Íñigo wrote that the firm was “fully committed to defending your interests”; at the same time, he quantified outstanding fees and warned of “pencils down”.', 'This documents a mandate and material advocacy, together with legitimate collection pressure; it does not by itself prove negligence or a duty to work without payment.'],
      ['26–28 Jul 2019', 'He said internal rules barred new assistance without repayment, offered punctual help “as a friend, not as a lawyer”, and then circulated a detailed bridge-loan and rescue architecture.', 'This documents coexisting personal and professional roles and integrated knowledge; it does not turn all personal help into firm advice.'],
      ['7–30 Oct 2019', 'He said firm work was suspended for fees; later he welcomed recent successful outcomes and wrote that the work, particularly Rosa’s, was paying back, before announcing formal withdrawal.', 'This documents work and results and supports the non-payment defence. It leaves the narrow protection-and-handover question open.'],
      ['26 May–3 Jun 2020', 'Rosa expressly granted venia and offered immediate coordination. Íñigo described “2yrs of work in your interest” and said collection had taken over.', 'This prevents an obstruction-of-venia claim. Handover completeness remains unproved; it also does not show that Íñigo directed later enforcement acts.'],
      ['8 Mar 2021', 'A confidential CNMV/RICPE/Sun Park package was sent to Íñigo.', 'This proves transmission—not reading, acceptance of a mandate, onward transmission or action.'],
      ['18 Feb 2022', 'Íñigo communicated a total EUR 441,463 demand comprising two principal blocks, interest and costs.', 'This is the sender’s quantification, not an independent adjudication or proof of double recovery. It calls for one invoice–promissory-note–receipt reconciliation.'],
      ['6 Mar 2026', 'A preservation communication was sent that day to a firm data-protection channel. No ordinary reply was located in the reviewed thread; automated compliance-portal notices exist without visible case content in Gmail.', 'Sending does not establish receipt, readership, investigation, institutional silence or admission.'],
      ['24–27 Aug 2026', 'A later reconciliation and right-of-reply invitation was not delivered to the attempted recipients: delivery bounced or expired.', 'It cannot be presented as a received invitation or as Cuatrecasas silence.']
    ],
    attributionTitle: 'From individual expression to firm expression: four levels',
    attributionIntro: 'The response has institutional relevance because it arose from a complaint concerning a substantial professional engagement. That connection permits questions about capacity, knowledge and governance; it does not permit a direct leap to corporate admission.',
    attributionLevel: 'Level',
    attributionSupport: 'What the record supports',
    attributionLimit: 'Boundary',
    attributionRows: [
      ['1 · Personal', 'First-person statement attributed to Iñigo de Luisa Maíz in the two preserved captures.', 'It does not by itself establish provider-certified authorship, misconduct, dissemination, retaliation or liability.'],
      ['2 · Partner / professional context', 'The complaint arose from a billed professional relationship; earlier emails used the firm’s voice, invoked internal rules and addressed advocacy and collection.', 'It does not make every personal sentence firm advice or prove that Iñigo instructed the ETJ acts.'],
      ['3 · Firm knowledge / governance', 'Preservation was sent to a firm channel that day; receipt, retention, escalation, conflict, access and risk handling are finite document questions.', 'Sending does not prove receipt, investigation, ratification, institutional silence or admission.'],
      ['4 · Firm adoption / responsibility', 'The expression would become imputable to the firm upon proof of instruction, authorisation, adoption, ratification, use or directly imputable governance failure.', 'Partner status and professional context alone do not establish a corporate statement or collective responsibility.']
    ],
    lagunaBridge: 'La Laguna bridge: the message does not prove procedural fraud, an insolvency offence or the remate assignee’s identity. It does document a reaction to professional scrutiny and opens questions whether firm files connect historic knowledge, 2024–2026 ETJ choices, the assignment reservation, recipient/UBO, single satisfaction and use or commercialisation of finca 8584 within the hotel. A recipient connected to Acosta Matos is Gil’s leading attributed assessment; it remains unproved.',
    questionsTitle: 'Questions Cuatrecasas can close with documents',
    questions: [
      'What client, debtor and instrument map connected the Aweswell/LPB invoices to the Matkator promissory notes?',
      'What contemporaneous record integrated possession, title, finance, insolvency and implementation risks, and who owned each condition?',
      'Which urgent consequences and deadlines were protected or handed over when the mandate ended, beyond the venia that was granted?',
      'What conflict, secrecy, authority and single-credit review preceded each 2024–2026 enforcement choice?',
      'Did the firm receive, preserve and assess the 6 March message under its controls, and can it document that chain without attributing collective responsibility by association?'
    ],
    provenanceTitle: 'Provenance, contact and correction right',
    provenance: 'The original captures remain in private custody. The second preserves a later interface change; it does not by itself prove deletion, blocking, deactivation or moderation. The contemporaneous communication said only that the message “appears to have deleted it”, and this publication preserves that qualification.',
    boundary: 'No direct contact with Íñigo de Luisa is sought. Any verifiable correction or response received through counsel, an institutional route or an authorized professional channel will be published with equal prominence. No absence of response will be treated as an admission.',
    record: 'Open controlled public record →',
    institutional: 'Open ICAM / CCACM record →',
    laguna: 'Open La Laguna / remate analysis →',
    dossier: 'Return to unitary Cuatrecasas dossier ↑'
  };

  const clauseRows = copy.clauses.map(([exact, reading, limit]) => `
    <tr><th scope="row">${escapeHTML(exact)}</th><td>${escapeHTML(reading)}</td><td>${escapeHTML(limit)}</td></tr>`).join('');
  const emailRows = copy.emails.map(([date, record, boundary]) => `
    <tr><th scope="row">${escapeHTML(date)}</th><td>${escapeHTML(record)}</td><td>${escapeHTML(boundary)}</td></tr>`).join('');
  const attributionRows = copy.attributionRows.map(([level, support, limit]) => `
    <tr><th scope="row">${escapeHTML(level)}</th><td>${escapeHTML(support)}</td><td>${escapeHTML(limit)}</td></tr>`).join('');
  const questionItems = copy.questions.map((question) => `<li>${escapeHTML(question)}</li>`).join('');

  const section = document.createElement('section');
  section.className = 'section cuatre-linkedin-record';
  section.id = 'inigo-linkedin-20260306';
  section.setAttribute('aria-labelledby', 'inigo-linkedin-20260306-title');
  section.setAttribute('data-cuatrecasas-inigo-linkedin-record', '20260306');
  section.setAttribute('data-publication-marker', 'cuatrecasas-linkedin-interlink-20260831');
  section.setAttribute('data-image-publication-marker', 'cuatrecasas-linkedin-images-20260901');
  section.setAttribute('data-governance-revision', '20260901b');
  section.innerHTML = `
    <div class="shell record">
      <div class="cuatre-linkedin-panel">
        <p class="eyeline">${escapeHTML(copy.eyebrow)}</p>
        <h2 id="inigo-linkedin-20260306-title">${escapeHTML(copy.title)}</h2>
        <p class="cuatre-linkedin-intro">${escapeHTML(copy.intro)}</p>
        <h3 class="cuatre-linkedin-section-title">${escapeHTML(copy.capturesTitle)}</h3>
        <p>${escapeHTML(copy.capturesIntro)}</p>
        <div class="cuatre-linkedin-captures" data-public-capture-count="2">
          <figure data-evidence-id="CUATRECASAS-LINKEDIN-20260306-INIGO-DE-LUISA.CAPTURE-01">
            <a href="../../assets/evidence/cuatrecasas/inigo-de-luisa-linkedin-message-20260306-capture-01.jpg" target="_blank" rel="noopener"><img src="../../assets/evidence/cuatrecasas/inigo-de-luisa-linkedin-message-20260306-capture-01.jpg" width="921" height="2048" loading="eager" fetchpriority="high" decoding="async" alt="${escapeHTML(isEs ? 'Captura de LinkedIn suministrada que muestra la cuenta Inigo de Luisa Maiz y el mensaje completo de las 12:13 PM' : 'Supplied LinkedIn capture displaying the Inigo de Luisa Maiz account and the complete 12:13 PM message')}"></a>
            <figcaption><strong>${escapeHTML(copy.capture1Title)}</strong> ${escapeHTML(copy.capture1)} <a href="../../assets/evidence/cuatrecasas/inigo-de-luisa-linkedin-message-20260306-capture-01.jpg" target="_blank" rel="noopener">${escapeHTML(copy.openCapture)}</a></figcaption>
          </figure>
          <figure data-evidence-id="CUATRECASAS-LINKEDIN-20260306-INIGO-DE-LUISA.CAPTURE-02">
            <a href="../../assets/evidence/cuatrecasas/inigo-de-luisa-linkedin-message-20260306-capture-02.jpg" target="_blank" rel="noopener"><img src="../../assets/evidence/cuatrecasas/inigo-de-luisa-linkedin-message-20260306-capture-02.jpg" width="921" height="2048" loading="lazy" decoding="async" alt="${escapeHTML(isEs ? 'Captura de LinkedIn suministrada que muestra LinkedIn Member, el aviso de contenido y el estado de imposibilidad de recibir mensajes' : 'Supplied LinkedIn capture displaying LinkedIn Member, the content warning and the unable-to-receive-messages state')}"></a>
            <figcaption><strong>${escapeHTML(copy.capture2Title)}</strong> ${escapeHTML(copy.capture2)} <a href="../../assets/evidence/cuatrecasas/inigo-de-luisa-linkedin-message-20260306-capture-02.jpg" target="_blank" rel="noopener">${escapeHTML(copy.openCapture)}</a></figcaption>
          </figure>
        </div>
        <blockquote class="cuatre-linkedin-message"></blockquote>
        <div class="cuatre-linkedin-rulings">
          <article><h3>${escapeHTML(copy.correctionTitle)}</h3><p>${escapeHTML(copy.correction)}</p></article>
          <article><h3>${escapeHTML(copy.adverseTitle)}</h3><p>${escapeHTML(copy.adverse)}</p></article>
        </div>
        <h3 class="cuatre-linkedin-section-title">${escapeHTML(copy.auditTitle)}</h3>
        <p>${escapeHTML(copy.auditIntro)}</p>
        <div class="cuatre-linkedin-tablewrap"><table class="cuatre-linkedin-table"><thead><tr><th>${escapeHTML(copy.exact)}</th><th>${escapeHTML(copy.reading)}</th><th>${escapeHTML(copy.limit)}</th></tr></thead><tbody>${clauseRows}</tbody></table></div>
        <h3 class="cuatre-linkedin-section-title">${escapeHTML(copy.emailTitle)}</h3>
        <p>${escapeHTML(copy.emailIntro)}</p>
        <div class="cuatre-linkedin-tablewrap"><table class="cuatre-linkedin-table cuatre-linkedin-email-table"><thead><tr><th>${escapeHTML(copy.date)}</th><th>${escapeHTML(copy.emailRecord)}</th><th>${escapeHTML(copy.emailBoundary)}</th></tr></thead><tbody>${emailRows}</tbody></table></div>
        <h3 class="cuatre-linkedin-section-title">${escapeHTML(copy.attributionTitle)}</h3>
        <p>${escapeHTML(copy.attributionIntro)}</p>
        <div class="cuatre-linkedin-tablewrap"><table class="cuatre-linkedin-table"><thead><tr><th>${escapeHTML(copy.attributionLevel)}</th><th>${escapeHTML(copy.attributionSupport)}</th><th>${escapeHTML(copy.attributionLimit)}</th></tr></thead><tbody>${attributionRows}</tbody></table></div>
        <p class="cuatre-linkedin-attribution-boundary">${escapeHTML(copy.lagunaBridge)}</p>
        <div class="cuatre-linkedin-questions"><h3>${escapeHTML(copy.questionsTitle)}</h3><ol>${questionItems}</ol></div>
        <div class="cuatre-linkedin-provenance">
          <strong>${escapeHTML(copy.provenanceTitle)}</strong>
          <p>${escapeHTML(copy.provenance)}</p>
          <p class="cuatre-linkedin-boundary">${escapeHTML(copy.boundary)}</p>
          <p class="cuatre-linkedin-links"><a href="../../evidence/cuatrecasas/2026-03-06-inigo-de-luisa-linkedin-message.json">${escapeHTML(copy.record)}</a><span aria-hidden="true"> · </span><a href="../cuatrecasas-icam-ccacm-2026/#linkedin-firm-attribution-20260901">${escapeHTML(copy.institutional)}</a><span aria-hidden="true"> · </span><a href="${isEs ? '../cuatrecasas-dp748-accion-civil/' : '../cuatrecasas-dp748-civil-action/'}#laguna-remate-ccacm-firm-expression-20260901">${escapeHTML(copy.laguna)}</a><span aria-hidden="true"> · </span><a href="#top">${escapeHTML(copy.dossier)}</a></p>
        </div>
      </div>
    </div>`;
  section.querySelector('.cuatre-linkedin-message').textContent = message;

  const style = document.createElement('style');
  style.setAttribute('data-cuatrecasas-inigo-linkedin-record-style', '20260901b');
  style.textContent = `
    .cuatre-linkedin-record{background:#f4f1ea;scroll-margin-top:1.5rem}
    .cuatre-linkedin-panel{background:#fff;border:1px solid #d9dede;border-top:7px solid #13252d;border-radius:22px;padding:clamp(1.2rem,3vw,2rem);box-shadow:0 16px 40px rgba(16,38,45,.10)}
    .cuatre-linkedin-panel h2{max-width:930px;margin:.35rem 0 .8rem}
    .cuatre-linkedin-intro{max-width:980px;font-size:1.02rem;line-height:1.65}
    .cuatre-linkedin-captures{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;margin:1rem 0 1.4rem}
    .cuatre-linkedin-captures figure{margin:0;background:#eef2f1;border:1px solid #d5dddb;border-radius:15px;overflow:hidden;box-shadow:0 10px 26px rgba(16,38,45,.08)}
    .cuatre-linkedin-captures figure>a{display:block;background:#fff}
    .cuatre-linkedin-captures img{display:block;width:100%;height:auto;background:#fff}
    .cuatre-linkedin-captures figcaption{padding:.9rem 1rem;font-size:.92rem;line-height:1.55;color:#374247}
    .cuatre-linkedin-captures figcaption strong{display:block;margin-bottom:.3rem;color:#13252d}
    .cuatre-linkedin-captures figcaption a{display:inline-block;margin-top:.45rem;font-weight:750}
    .cuatre-linkedin-message{margin:1.25rem 0;padding:1.15rem 1.25rem;background:#13252d;color:#fff;border-left:7px solid #d0a12d;border-radius:12px;font-size:clamp(1.05rem,2vw,1.25rem);line-height:1.65;font-style:normal}
    .cuatre-linkedin-rulings{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;margin:1.25rem 0}
    .cuatre-linkedin-rulings article{background:#f8f6f0;border:1px solid #ded8c9;border-radius:14px;padding:1rem}
    .cuatre-linkedin-rulings article:first-child{border-top:5px solid #a76c00}
    .cuatre-linkedin-rulings article:last-child{border-top:5px solid #1d5c4a}
    .cuatre-linkedin-rulings h3,.cuatre-linkedin-rulings p{margin:.2rem 0 .55rem;line-height:1.55}
    .cuatre-linkedin-section-title{margin:1.75rem 0 .45rem}
    .cuatre-linkedin-tablewrap{overflow-x:auto;margin:1rem 0 1.4rem;border:1px solid #d9dede;border-radius:14px}
    .cuatre-linkedin-table{width:100%;min-width:780px;border-collapse:collapse;font-size:.94rem;line-height:1.52}
    .cuatre-linkedin-table th,.cuatre-linkedin-table td{padding:.82rem;vertical-align:top;border-bottom:1px solid #e4e8e7;text-align:left}
    .cuatre-linkedin-table thead th{background:#13252d;color:#fff;font-size:.84rem;letter-spacing:.03em;text-transform:uppercase}
    .cuatre-linkedin-table tbody th{width:23%;background:#f8faf9;color:#13252d}
    .cuatre-linkedin-table tbody tr:last-child th,.cuatre-linkedin-table tbody tr:last-child td{border-bottom:0}
    .cuatre-linkedin-email-table tbody th{width:13%;white-space:nowrap}
    .cuatre-linkedin-attribution-boundary{background:#fffaf0;border-left:5px solid #a76c00;border-radius:12px;padding:1rem 1.15rem;line-height:1.6}
    .cuatre-linkedin-questions{margin:1.25rem 0;background:#13252d;color:#fff;border-radius:14px;padding:1.1rem 1.25rem}
    .cuatre-linkedin-questions h3{margin:.1rem 0 .65rem;color:#fff}
    .cuatre-linkedin-questions ol{margin:.4rem 0 .2rem;padding-left:1.35rem}
    .cuatre-linkedin-questions li{margin:.55rem 0;line-height:1.55}
    .cuatre-linkedin-provenance{background:#f7faf9;border-left:5px solid #1d5c4a;border-radius:12px;padding:1rem 1.15rem}
    .cuatre-linkedin-provenance p{margin:.45rem 0;line-height:1.6}
    .cuatre-linkedin-boundary{font-size:.92rem;color:#4d5558}
    .cuatre-linkedin-links{font-weight:650}
    @media (max-width:760px){.cuatre-linkedin-captures,.cuatre-linkedin-rulings{grid-template-columns:1fr}.cuatre-linkedin-panel{border-radius:15px}.cuatre-linkedin-table{font-size:.9rem}}
  `;
  document.head.appendChild(style);

  const hero = document.querySelector('main > .hero, main .hero');
  if (hero) hero.insertAdjacentElement('afterend', section);
  else document.querySelector('main')?.prepend(section);

  if (window.location.hash === '#inigo-linkedin-20260306') {
    window.requestAnimationFrame(() => section.scrollIntoView({ block: 'start' }));
  }
})();
