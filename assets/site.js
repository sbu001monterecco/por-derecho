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

/* Public RIC/Sun Park coherence layer. The language is deliberately evidence-led:
   it identifies finite documentary questions and does not infer guilt from silence. */
const isSpanish = document.documentElement.lang === 'es';
const dossierRoot = document.querySelector('.dossier-page');

const pressureCopy = isSpanish ? {
  sectionId: 'tres-preguntas',
  kicker: 'Tres preguntas · documentos, no negaciones generales',
  title: 'El núcleo del expediente puede resolverse con documentos contemporáneos.',
  intro: 'La presión pública sostenible no depende de multiplicar acusaciones. Depende de identificar qué se dijo, qué debía comprobarse, qué documento lo soportaba y quién lo aprobó.',
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
  timelineKicker: '2018 · la investigación no puede empezar en enero de 2022',
  timelineTitle: 'Control, preparación y alternativa financiada precedieron a las representaciones inversoras.',
  timelineText: 'La secuencia sometida a contraste incluye planificación y seguridad en febrero, acceso y mediciones en marzo, acuerdo comunitario en mayo, control material controvertido el 7 de junio, oferta de financiación el 12 y presentación de una vía financiada al juez y a la Administración Concursal el 13 de junio. La proximidad temporal no prueba comunicación o intención; convierte en finitas las preguntas de conocimiento, autorización y efecto.',
  timelineQuestion: 'Pregunta de control: ¿recibió RIC el resultado concursal como un hecho externo ya consumado, o su proyecto, calendario, compromisos y narrativa de propiedad contribuyeron a definir las condiciones económicas que CAM necesitaba?',
  statusKicker: 'Registro de documentos decisivos',
  statusTitle: 'Lo que está publicado y lo que sigue bajo control de sus custodios.',
  statusIntro: '«No localizado públicamente» no significa «no existe». Identifica el documento que puede cerrar cada cuestión y quién está en posición de producirlo.',
  statusRows: [
    ['Título CAM · junio/noviembre 2020', 'Informe de título + schedule de fincas', 'No localizado públicamente'],
    ['Cuatro informes Sun Park', 'Versiones nativas + anexos + circulación', 'No localizados públicamente'],
    ['Conflicto consejero-promotor', 'Declaración de interés + abstención + acta', 'No localizado públicamente'],
    ['Corrección a inversores', 'Comunicación + destinatarios + fecha', 'No localizada públicamente'],
    ['Custodia A&G / Orión', 'Transferencia, liquidación, servidores, buzones y backups', 'Cadena no establecida públicamente']
  ],
  roleKicker: 'Responsabilidad por función',
  roleTitle: 'Cada eslabón debe explicar su propio acto, conocimiento y dependencia.',
  roleText: 'Ni el Consejo puede refugiarse en el equipo sin identificar los informes, ni el equipo en el Consejo sin identificar qué recomendó, ni puede invocarse a un asesor sin contrato, alcance y entregable. Esta diferenciación protege a quien actuó correctamente y localiza el punto exacto donde falte un control.'
} : {
  sectionId: 'three-questions',
  kicker: 'Three questions · documents, not general denials',
  title: 'The core of the record can be resolved through contemporaneous documents.',
  intro: 'Sustainable public pressure does not depend on multiplying accusations. It depends on identifying what was said, what had to be checked, which document supported it and who approved it.',
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
  timelineKicker: '2018 · the investigation cannot begin in January 2022',
  timelineTitle: 'Control, preparation and a funded alternative pre-dated the investor representations.',
  timelineText: 'The sequence submitted for testing includes planning and security in February, access and measurements in March, a Community resolution in May, disputed material control on 7 June, a financing offer on 12 June and presentation of a funded route to the judge and Insolvency Administration on 13 June. Temporal proximity does not prove communication or intent; it makes the questions of knowledge, authority and effect finite.',
  timelineQuestion: 'Control question: did RIC receive the insolvency outcome as an external fact already produced, or did its project, timetable, commitments and ownership narrative contribute to defining the economic conditions CAM required?',
  statusKicker: 'Decisive-document register',
  statusTitle: 'What is public and what remains under custodial control.',
  statusIntro: '“Not publicly located” does not mean “does not exist”. It identifies the document capable of closing each question and the custodian able to produce it.',
  statusRows: [
    ['CAM title · June/November 2020', 'Title report + property schedule', 'Not publicly located'],
    ['Four Sun Park reports', 'Native versions + annexes + circulation', 'Not publicly located'],
    ['Promoter-director conflict', 'Interest declaration + recusal + minutes', 'Not publicly located'],
    ['Investor correction', 'Communication + recipients + date', 'Not publicly located'],
    ['A&G / Orión custody', 'Transfer, liquidation, servers, mailboxes and backups', 'Chain not publicly established']
  ],
  roleKicker: 'Responsibility by role',
  roleTitle: 'Each link must explain its own act, knowledge and reliance.',
  roleText: 'The Board cannot shelter behind the team without identifying the reports; the team cannot shelter behind the Board without identifying what it recommended; and an adviser cannot be invoked without engagement, scope and deliverable. Differentiation protects those who acted properly and locates the precise point at which a control may be missing.'
};

function pressureCards(copy) {
  return copy.questions.map((q, i) => `<article class="pressure-card" data-number="0${i + 1}"><span class="evidence-badge question-badge">${isSpanish ? 'Cuestión verificable' : 'Verifiable question'}</span><h3>${q[0]}</h3><p>${q[1]}</p></article>`).join('');
}

function contradictionRows(copy) {
  return copy.rows.map(r => `<tr><td><strong>${r[0]}</strong></td><td>${r[1]}</td><td>${r[2]}</td><td>${r[3]}</td></tr>`).join('');
}

function statusRows(copy) {
  return copy.statusRows.map(r => `<tr><td><strong>${r[0]}</strong></td><td>${r[1]}</td><td><span class="status-pill missing">${r[2]}</span></td></tr>`).join('');
}

if (dossierRoot) {
  const unitary = document.querySelector(isSpanish ? '#pregunta-unitaria' : '#unitary-question');
  const genealogy = document.querySelector(isSpanish ? '#genealogia' : '#genealogy');
  if (unitary && genealogy && !document.getElementById(pressureCopy.sectionId)) {
    const block = document.createElement('div');
    block.innerHTML = `
      <section class="section alt" id="${pressureCopy.sectionId}">
        <div class="shell">
          <div class="section-head"><div><p class="kicker">${pressureCopy.kicker}</p><h2>${pressureCopy.title}</h2></div><p>${pressureCopy.intro}</p></div>
          <div class="pressure-questions">${pressureCards(pressureCopy)}</div>
          <div class="pressure-maxim"><strong>${pressureCopy.maxim}</strong><span>${pressureCopy.maximText}</span></div>
        </div>
      </section>
      <section class="section" id="${isSpanish ? 'contradiccion-2020' : '2020-contradiction'}">
        <div class="shell">
          <div class="section-head"><div><p class="kicker">${pressureCopy.contradictionKicker}</p><h2>${pressureCopy.contradictionTitle}</h2></div><p>${pressureCopy.contradictionIntro}</p></div>
          <div class="control-table-wrap" role="region" tabindex="0"><table class="control-table"><thead><tr><th>${isSpanish ? 'Fecha / fuente' : 'Date / source'}</th><th>${isSpanish ? 'Proposición pública' : 'Public proposition'}</th><th>${isSpanish ? 'Realidad a verificar' : 'Reality to verify'}</th><th>${isSpanish ? 'Documento decisivo' : 'Decisive document'}</th></tr></thead><tbody>${contradictionRows(pressureCopy)}</tbody></table></div>
          <div class="binary-test"><h3>${pressureCopy.fourTitle}</h3><p>${pressureCopy.fourText}</p><div class="filter-grid">${pressureCopy.filters.map(f => `<article><span>${f[0]}</span><strong>${f[1]}</strong></article>`).join('')}</div></div>
        </div>
      </section>
      <section class="section alt" id="${isSpanish ? 'conocimiento-2018' : '2018-knowledge'}">
        <div class="shell">
          <div class="section-head