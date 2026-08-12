const toggle = document.querySelector('.nav-toggle');
const nav = document.querySelector('.main-nav');

if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
  });

  nav.addEventListener('click', (event) => {
    if (event.target.closest('a')) {
      nav.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    }
  });
}

document.querySelectorAll('[data-current-year]').forEach((node) => {
  node.textContent = new Date().getFullYear();
});

const isSpanish = document.documentElement.lang === 'es';
const dossierRoot = document.querySelector('.dossier-page');

const copy = isSpanish ? {
  questionsId: 'tres-preguntas',
  questionsKicker: 'Tres preguntas · documentos, no negaciones generales',
  questionsTitle: 'El núcleo del expediente puede resolverse con documentos contemporáneos.',
  questionsIntro: 'La presión pública sostenible no depende de multiplicar acusaciones. Depende de identificar qué se dijo, qué debía comprobarse, qué documento lo soportaba y quién lo aprobó.',
  questions: [
    ['¿Qué poseía exactamente CAM en 2020?', 'Finca por finca, derecho por derecho y fecha por fecha: crédito, posesión, expectativa, unidades concretas y propiedad del conjunto no son equivalentes.'],
    ['¿Existieron los cuatro informes favorables?', 'RIC describió cuatro filtros previos al Consejo. Para Sun Park, la cuestión es binaria: identificar los informes, autores, fechas, reservas y destinatarios, o explicar qué proceso alternativo se aplicó.'],
    ['¿Qué conoció RIC de la secuencia de 2018?', 'Qué recibió sobre acceso, mediciones, control material y la alternativa financiada; quién lo analizó; y qué efecto tuvo en aceptación, retirada o reentrada del proyecto.']
  ],
  maxim: 'Cada expresión exige una fecha, un activo, un documento, un autor y un aprobador.',
  maximText: 'Una respuesta corporativa general no sustituye la trazabilidad de cada representación, informe, voto, reserva, abstención y corrección.',
  contradictionKicker: '2020 → 2022 · contradicción documental central',
  contradictionTitle: '¿Qué significaban «sociedad titular», «hemos comprado», «propiedad», «libres de cargas» y «en cartera» cuando se pronunciaron?',
  contradictionIntro: 'El folleto y webinar de 2020 deben leerse con su propia cautela —el folleto decía que los proyectos estaban «en estudio»— y, al mismo tiempo, reconciliarse con la adjudicación principal de enero de 2022. El hecho posterior no responde por sí solo qué soporte existía en 2020.',
  rows: [
    ['4 JUN 2020 · folleto', 'CAM como «sociedad titular» de Sun Park', 'Título por fincas; LPB/Matkator/terceros; concurso y cargas', 'Ficha de origen, informe de título, DD legal, reservas y aprobación'],
    ['11 NOV 2020 · webinar', 'Tres complejos comprados con fondos propios, libres de cargas y propiedad de CAM', 'Crédito ≠ posesión ≠ expectativa ≠ unidades concretas ≠ propiedad del conjunto', 'Guion, revisión legal, fuentes de la afirmación y aprobación'],
    ['11 NOV 2020 · webinar', 'Sun Park «en cartera»; obras Q1 2021; financiación fin 2021', 'Disponibilidad, acceso, licencias, litigios y calendario real', 'Memorando de inversión, cronograma, compromisos y condiciones'],
    ['ENE 2022 y después', 'Adjudicación, HNT y financiación posterior', 'Qué cambió jurídicamente y qué se corrigió', 'Puente de reentrada, documentación del Consejo y comunicaciones']
  ],
  fourTitle: 'Los cuatro informes: existen o no existen.',
  fourText: 'Si existieron para Sun Park, deben poder identificarse por versión, fecha, autor, alcance, reservas, anexos y destinatarios. Si no existieron, debe explicarse qué proceso permitió presentar el proyecto y qué controles sustituyeron a los públicamente descritos.',
  filters: [['01','Inversiones'],['02','Riesgo / Intermoney'],['03','Fiscal / expedientes administrativos'],['04','Informe favorable del Director General']],
  knowledgeKicker: '2018 · la investigación no puede empezar en enero de 2022',
  knowledgeTitle: 'Control, preparación y alternativa financiada precedieron a las representaciones inversoras.',
  knowledgeText: 'La secuencia sometida a contraste incluye planificación y seguridad en febrero, acceso y mediciones en marzo, acuerdo comunitario en mayo, control material controvertido el 7 de junio, oferta de financiación el 12 y presentación de una vía financiada al juez y a la Administración Concursal el 13 de junio. La proximidad temporal no prueba comunicación o intención; convierte en finitas las preguntas de conocimiento, autorización y efecto.',
  knowledgeQuestion: 'Pregunta de control: ¿recibió RIC el resultado concursal como un hecho externo ya consumado, o su proyecto, calendario, compromisos y narrativa de propiedad contribuyeron a definir las condiciones económicas que CAM necesitaba?',
  conversionKicker: 'ENE–FEB 2022 · secuencia de conversión',
  conversionTitle: 'La reunión de 4 de febrero no debe analizarse de forma aislada.',
  conversionIntro: 'El expediente actualmente localizado sitúa la reunión dentro de una secuencia más amplia: encargos de reforma anteriores, adjudicación, acta comunitaria, pasos de RIC, certificación, licencia, visado y posterior explotación. La cuestión no es presumir ilicitud de cada documento, sino conciliar autoridad, coste, propiedad y beneficio en cada fecha.',
  conversionRows: [
    ['5 ENE 2022', 'La Comunidad aparece como promotora de un encargo de reforma', 'Contrato original, firmante, alcance, autoridad y unidades afectadas'],
    ['15 ENE 2022', 'Encargo referido a 54 unidades y presupuesto aproximado de €1,27m', 'Listado de unidades, propietarios, consentimiento y archivo nativo'],
    ['26 ENE 2022', 'Auto de adjudicación alegado a favor de CAM', 'Firmeza, alcance exacto, inventario y efecto jurídico a 4 de febrero'],
    ['4 FEB 2022', 'Acta con 20,993% presente/representado; LPB ausente; deuda, voto, proyecto y permisos', 'Convocatoria, propietarios, poderes, libro de actas, audio, ledger de deuda y base de voto'],
    ['11 FEB 2022', 'Paso corporativo RIC vinculado al proyecto Sun Park', 'Acta, condiciones, proyecto considerado y documentación de reentrada'],
    ['18 FEB 2022', 'Certificación atribuida a FMMM sobre obras comunes y solicitud de licencias', 'Nombramiento, facultad certificante, acuerdo exacto y documento transmitido'],
    ['21–25 FEB 2022', 'Formalización/licencia/visado en la secuencia administrativa', 'Solicitud completa, título o disponibilidad, perímetro y controles municipales']
  ],
  burdenTitle: 'Coste sin frutos: la contradicción debe reconciliarse documentalmente.',
  burdenText: 'La documentación presentada en el expediente atribuye a LPB aproximadamente €1,199m de deuda y, separadamente, aproximadamente €3,26m de una derrama total de €4,467m para obras, además de una cantidad a Matkator. Si CAM avanzaba hacia la recepción y explotación del activo, la pregunta verificable es quién debía soportar el coste, quién sería propietario de la mejora y quién recibiría sus frutos. Estas cifras son posiciones documentales sometidas a verificación, no una declaración judicial de fraude.',
  matkatorTitle: 'Matkator exige un título independiente.',
  matkatorText: 'Matkator no era deudora en Concurso 36/2012. La afectación de sus fincas por ocupación, obras, integración hotelera, renumeración, renta o pérdida de valor no puede derivarse automáticamente de la masa concursal: debe identificarse el título, consentimiento y tratamiento finca por finca.',
  privacyTitle: 'Testigos y personas de apoyo: identidad reservada por defecto.',
  privacyText: 'La web no debe identificar a testigos privados ni a personas que asisten al informante salvo necesidad probatoria concreta, consentimiento informado y una razón proporcionada para hacer pública su identidad. El contenido público se apoya preferentemente en documentos, actos oficiales y atribuciones institucionales verificables.'
} : {
  questionsId: 'three-questions',
  questionsKicker: 'Three questions · documents, not general denials',
  questionsTitle: 'The core record can be resolved through contemporaneous documents.',
  questionsIntro: 'Sustainable public pressure does not depend on multiplying accusations. It depends on identifying what was said, what had to be checked, which document supported it and who approved it.',
  questions: [
    ['What exactly did CAM own in 2020?', 'Property by property, right by right and date by date: credit, possession, expectation, specific units and ownership of the whole are not equivalent.'],
    ['Did the four favourable reports exist?', 'RIC described four filters before a project could reach the Board. For Sun Park the question is binary: identify the reports, authors, dates, reservations and recipients, or explain what alternative process applied.'],
    ['What did RIC know about the 2018 sequence?', 'What it received about access, measurements, material control and the funded alternative; who analysed it; and what effect it had on acceptance, withdrawal or re-entry.']
  ],
  maxim: 'Every expression requires a date, an asset, a document, an author and an approver.',
  maximText: 'A general corporate response does not replace traceability for each representation, report, vote, reservation, recusal and correction.',
  contradictionKicker: '2020 → 2022 · central documentary contradiction',
  contradictionTitle: 'What did “titleholder company”, “we bought”, “property”, “unencumbered” and “in portfolio” mean when they were said?',
  contradictionIntro: 'The 2020 brochure and webinar must be read with their own qualification —the brochure said projects were “under study”— while also being reconciled with the principal January 2022 adjudication. The later event does not by itself answer what support existed in 2020.',
  rows: [
    ['4 JUN 2020 · brochure', 'CAM as Sun Park “titleholder company”', 'Title by property; LPB/Matkator/third parties; insolvency and charges', 'Origination file, title report, legal DD, reservations and approval'],
    ['11 NOV 2020 · webinar', 'Three complexes bought with own funds, unencumbered and CAM property', 'Credit ≠ possession ≠ expectation ≠ specific units ≠ ownership of the whole', 'Script, legal review, sources for the statement and approval'],
    ['11 NOV 2020 · webinar', 'Sun Park “in portfolio”; works Q1 2021; finance end-2021', 'Availability, access, licences, disputes and actual timetable', 'Investment memo, timetable, commitments and conditions'],
    ['JAN 2022 onward', 'Adjudication, HNT and later financing', 'What changed legally and what was corrected', 'Re-entry bridge, Board materials and communications']
  ],
  fourTitle: 'The four reports: they exist or they do not.',
  fourText: 'If they existed for Sun Park, they should be identifiable by version, date, author, scope, reservations, annexes and recipients. If they did not, the record should explain what process allowed the project to be presented and what controls replaced those publicly described.',
  filters: [['01','Investments'],['02','Risk / Intermoney'],['03','Tax / administrative files'],['04','Favourable Director General report']],
  knowledgeKicker: '2018 · the investigation cannot begin in January 2022',
  knowledgeTitle: 'Control, preparation and a funded alternative pre-dated the investor representations.',
  knowledgeText: 'The sequence submitted for testing includes planning and security in February, access and measurements in March, a Community resolution in May, disputed material control on 7 June, a financing offer on 12 June and presentation of a funded route to the judge and Insolvency Administration on 13 June. Temporal proximity does not prove communication or intent; it makes the questions of knowledge, authority and effect finite.',
  knowledgeQuestion: 'Control question: did RIC receive the insolvency outcome as an external fact already produced, or did its project, timetable, commitments and ownership narrative contribute to defining the economic conditions CAM required?',
  conversionKicker: 'JAN–FEB 2022 · conversion sequence',
  conversionTitle: 'The 4 February meeting should not be analysed in isolation.',
  conversionIntro: 'The currently located record places the meeting inside a wider sequence: earlier refurbishment commissions, adjudication, Community minutes, RIC steps, certification, licence, professional approval and later operation. The issue is not to presume each document unlawful, but to reconcile authority, cost, ownership and benefit at each date.',
  conversionRows: [
    ['5 JAN 2022', 'The Community appears as promoter of a refurbishment commission', 'Original contract, signatory, scope, authority and affected units'],
    ['15 JAN 2022', 'Commission referring to 54 units and c. €1.27m budget', 'Unit list, owners, consent and native file'],
    ['26 JAN 2022', 'Alleged adjudication order in CAM’s favour', 'Finality, exact scope, inventory and legal effect by 4 February'],
    ['4 FEB 2022', 'Minutes recording 20.993% present/represented; LPB absent; debt, voting, project and permissions', 'Notice, owners, proxies, minute book, audio, debt ledger and voting basis'],
    ['11 FEB 2022', 'RIC corporate step linked to the Sun Park project', 'Minutes, conditions, project considered and re-entry documentation'],
    ['18 FEB 2022', 'Certificate attributed to FMMM concerning common works and licence applications', 'Appointment, certification power, exact resolution and transmitted document'],
    ['21–25 FEB 2022', 'Formalisation/licence/professional approval in the administrative sequence', 'Complete application, title or availability, perimeter and municipal checks']
  ],
  burdenTitle: 'Cost without fruits: the contradiction requires documentary reconciliation.',
  burdenText: 'Material filed in the record attributes approximately €1.199m of debt to LPB and, separately, about €3.26m of a €4.467m works assessment, plus an amount to Matkator. If CAM was moving toward receipt and operation of the asset, the verifiable question is who was to bear the cost, who would own the improvement and who would receive its fruits. These are documentary positions requiring verification, not a judicial finding of fraud.',
  matkatorTitle: 'Matkator requires an independent title.',
  matkatorText: 'Matkator was not a debtor in Insolvency Proceeding 36/2012. Any occupation, works, hotel integration, renumbering, rent or loss of value affecting its properties cannot automatically derive from the insolvency estate: title, consent and treatment must be identified property by property.',
  privacyTitle: 'Witnesses and support persons: identity withheld by default.',
  privacyText: 'The site should not identify private witnesses or persons assisting the reporting person absent concrete evidential necessity, informed consent and a proportionate reason for public identification. Public content should rely preferentially on documents, official acts and verifiable institutional attribution.'
};

function questionsHTML() {
  return copy.questions.map((q, i) => `<article class="pressure-card" data-number="0${i + 1}"><span class="evidence-badge question-badge">${isSpanish ? 'Cuestión verificable' : 'Verifiable question'}</span><h3>${q[0]}</h3><p>${q[1]}</p></article>`).join('');
}

function rowsHTML(rows) {
  return rows.map(r => `<tr><td><strong>${r[0]}</strong></td><td>${r[1]}</td><td>${r[2]}</td><td>${r[3] || ''}</td></tr>`).join('');
}

if (dossierRoot) {
  const unitary = document.querySelector(isSpanish ? '#pregunta-unitaria' : '#unitary-question');
  const genealogy = document.querySelector(isSpanish ? '#genealogia' : '#genealogy');
  if (unitary && genealogy && !document.getElementById(copy.questionsId)) {
    const block = document.createElement('div');
    block.innerHTML = `
      <section class="section alt" id="${copy.questionsId}">
        <div class="shell">
          <div class="section-head"><div><p class="kicker">${copy.questionsKicker}</p><h2>${copy.questionsTitle}</h2></div><p>${copy.questionsIntro}</p></div>
          <div class="pressure-questions">${questionsHTML()}</div>
          <div class="pressure-maxim"><strong>${copy.maxim}</strong><span>${copy.maximText}</span></div>
        </div>
      </section>
      <section class="section" id="${isSpanish ? 'contradiccion-2020' : '2020-contradiction'}">
        <div class="shell">
          <div class="section-head"><div><p class="kicker">${copy.contradictionKicker}</p><h2>${copy.contradictionTitle}</h2></div><p>${copy.contradictionIntro}</p></div>
          <div class="control-table-wrap" role="region" tabindex="0"><table class="control-table"><thead><tr><th>${isSpanish ? 'Fecha / fuente' : 'Date / source'}</th><th>${isSpanish ? 'Proposición pública' : 'Public proposition'}</th><th>${isSpanish ? 'Realidad a verificar' : 'Reality to verify'}</th><th>${isSpanish ? 'Documento decisivo' : 'Decisive document'}</th></tr></thead><tbody>${rowsHTML(copy.rows)}</tbody></table></div>
          <div class="binary-test"><h3>${copy.fourTitle}</h3><p>${copy.fourText}</p><div class="filter-grid">${copy.filters.map(f => `<article><span>${f[0]}</span><strong>${f[1]}</strong></article>`).join('')}</div></div>
        </div>
      </section>
      <section class="section alt" id="${isSpanish ? 'conocimiento-2018' : '2018-knowledge'}">
        <div class="shell">
          <div class="section-head"><div><p class="kicker">${copy.knowledgeKicker}</p><h2>${copy.knowledgeTitle}</h2></div><p>${copy.knowledgeText}</p></div>
          <div class="pressure-maxim"><strong>${isSpanish ? 'Pregunta de control' : 'Control question'}</strong><span>${copy.knowledgeQuestion}</span></div>
        </div>
      </section>
      <section class="section" id="${isSpanish ? 'secuencia-2022' : '2022-sequence'}">
        <div class="shell">
          <div class="section-head"><div><p class="kicker">${copy.conversionKicker}</p><h2>${copy.conversionTitle}</h2></div><p>${copy.conversionIntro}</p></div>
          <div class="control-table-wrap" role="region" tabindex="0"><table class="control-table"><thead><tr><th>${isSpanish ? 'Fecha' : 'Date'}</th><th>${isSpanish ? 'Hito documentado' : 'Documented step'}</th><th>${isSpanish ? 'Documento que lo cierra' : 'Decisive closing document'}</th><th></th></tr></thead><tbody>${rowsHTML(copy.conversionRows)}</tbody></table></div>
          <div class="pressure-questions">
            <article class="pressure-card"><span class="evidence-badge question-badge">${isSpanish ? 'Contradicción económica' : 'Economic contradiction'}</span><h3>${copy.burdenTitle}</h3><p>${copy.burdenText}</p></article>
            <article class="pressure-card"><span class="evidence-badge question-badge">${isSpanish ? 'Perímetro extraconcursal' : 'Outside-insolvency perimeter'}</span><h3>${copy.matkatorTitle}</h3><p>${copy.matkatorText}</p></article>
          </div>
          <div class="pressure-maxim"><strong>${copy.privacyTitle}</strong><span>${copy.privacyText}</span></div>
        </div>
      </section>`;
    unitary.insertAdjacentElement('afterend', block);
  }
}

const updates = document.querySelector('#actualizaciones');
if (updates && !dossierRoot && !document.getElementById('actualizacion-evidencia-12ago2026')) {
  const section = document.createElement('section');
  section.className = 'section alt';
  section.id = 'actualizacion-evidencia-12ago2026';
  section.innerHTML = isSpanish ? `
    <div class="shell">
      <div class="section-head"><div><p class="kicker">12 agosto 2026 · actualización probatoria</p><h2>De una reunión aislada a una secuencia verificable de enero–febrero de 2022.</h2></div><p>El reescaneo de escritos presentados, expedientes administrativos, documentación comunitaria y comunicaciones con abogados actuales refuerza una formulación más precisa: la cuestión central es cómo se conectaron adjudicación, deuda, reforma, licencias, financiación y explotación.</p></div>
      <div class="grid-3">
        <article class="path-card primary"><span class="number">01 · 4 FEB 2022</span><h3>20,993% y carga económica</h3><p>El acta localizada registra aproximadamente 20,993% presente/representado, LPB ausente y acuerdos sobre deuda, voto, reforma y permisos. El expediente atribuye a LPB aproximadamente €1,199m de deuda y, separadamente, cerca de €3,26m de una derrama de €4,467m. La validez, soporte e intención siguen sometidos a prueba.</p></article>
        <article class="path-card"><span class="number">02 · MATKATOR</span><h3>Fuera del concurso</h3><p>Matkator no era deudora en Concurso 36/2012. Cualquier ocupación, obra, integración hotelera, renumeración o renta de sus fincas requiere un título y una conciliación propios, finca por finca.</p></article>
        <article class="path-card"><span class="number">03 · VERIFICACIÓN</span><h3>Abogados, juzgados y custodios</h3><p>La revisión con abogados actuales y anteriores se utiliza como ruta de localización y contraste, no como sustituto de la prueba. La prioridad sigue siendo obtener resoluciones, escritos, notificaciones, libros de actas, poderes, ledgers y archivos nativos que permitan fijar qué conocía cada órgano y cuándo.</p></article>
      </div>
      <p class="source-policy"><strong>Control de privacidad:</strong> los testigos privados y las personas que asisten al informante permanecen sin identificar en la web salvo necesidad concreta, consentimiento informado y justificación proporcionada.</p>
    </div>` : `
    <div class="shell">
      <div class="section-head"><div><p class="kicker">12 August 2026 · evidence update</p><h2>From an isolated meeting to a verifiable January–February 2022 sequence.</h2></div><p>The rescan of filed pleadings, administrative records, Community documents and communications with current lawyers supports a more precise formulation: the central question is how adjudication, debt, refurbishment, licences, finance and operation were connected.</p></div>
      <div class="grid-3">
        <article class="path-card primary"><span class="number">01 · 4 FEB 2022</span><h3>20.993% and economic burden</h3><p>The located minutes record approximately 20.993% present/represented, LPB absent, and resolutions concerning debt, voting, refurbishment and permissions. Filed material attributes about €1.199m of debt to LPB and, separately, about €3.26m of a €4.467m works assessment. Validity, support and intent remain matters for proof.</p></article>
        <article class="path-card"><span class="number">02 · MATKATOR</span><h3>Outside the insolvency estate</h3><p>Matkator was not a debtor in Insolvency Proceeding 36/2012. Any occupation, works, hotel integration, renumbering or rent affecting its properties requires its own title and property-by-property reconciliation.</p></article>
        <article class="path-card"><span class="number">03 · VERIFICATION</span><h3>Lawyers, courts and custodians</h3><p>Review with current and former lawyers is used as a route to locate and test evidence, not as a substitute for it. Priority remains primary orders, pleadings, notices, minute books, powers, ledgers and native files showing what each body knew and when.</p></article>
      </div>
      <p class="source-policy"><strong>Privacy control:</strong> private witnesses and persons assisting the reporting person remain unidentified on the public site absent concrete necessity, informed consent and proportionate justification.</p>
    </div>`;
  updates.parentNode.insertBefore(section, updates);
}
