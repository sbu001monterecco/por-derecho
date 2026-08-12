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

const esc = (value) => String(value)
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;');

const data = isSpanish ? {
  actorKicker: 'Personas, funciones y autoridad',
  actorTitle: 'No una galería de culpabilidad: quién podía hacer qué, sobre qué documento y con qué consecuencia.',
  actorIntro: 'La web distingue actores privados, Administración Concursal y supervisión judicial. La fotografía identifica una función pública o una intervención documentada; no convierte proximidad visual en prueba de coordinación.',
  operatorTitle: 'Punto de partida jurídico: la Explotadora no era la Comunidad de Propietarios.',
  operatorText: 'La posición sostenida y documentada por Aweswell es que la Comunidad de Explotación del Complejo Sun Park (CESP / Explotadora) recibió en 2008 la explotación turística del complejo y continuó la actividad hotelera. La Comunidad de Propietarios era un órgano de propietarios y gobierno: no era, por ese solo carácter, la explotadora hotelera. No se presenta CAM, HNT, Canarian Hospitality, MYND ni otra entidad como sucesora jurídica de CESP sin el título concreto de extinción, cesión o sustitución que lo demuestre.',
  operatorQuestion: 'Documento decisivo: ¿qué acto extinguió o desplazó válidamente el título de explotación de CESP y en qué fecha?',
  actors: [
    {
      name: 'José Daniel Acosta Matos',
      group: 'Actor privado · CAM / RIC',
      image: '../../assets/evidence/ric-webinar-sun-park.webp',
      imageAlt: 'Fotograma documental del webinar RIC de 11 noviembre 2020 sobre Sun Park',
      role: 'Consejero de RIC y principal voz pública de CAM en el proyecto Sun Park.',
      fact: 'El webinar de 11 NOV 2020 contiene las manifestaciones públicas sobre compra, fondos propios, cargas, cartera y calendario de Sun Park.',
      question: '¿Qué título, due diligence y aprobación sustentaban cada afirmación en su fecha?'
    },
    {
      name: 'Francisco Mario Matos Matas',
      group: 'Actor privado · perímetro comunitario',
      role: 'Administrador/secretaría y certificación en el perímetro Pamalexsha–Comunidad según la documentación investigada.',
      fact: 'El acta y certificaciones de 2022 hacen de la procedencia, cálculo de deuda, morosidad, votos, cargos y facultades un punto central de verificación.',
      question: '¿Quién produjo cada cifra, acta y certificado y qué autoridad válida permitía que produjera efectos?'
    },
    {
      name: 'Antonio Cogolludo Rojas',
      group: 'Actor privado · Comunidad / seguridad',
      role: 'Figura del perímetro de presidencia, representación, seguridad y acceso durante la secuencia crítica de 2018.',
      fact: 'Su intervención se reconstruye mediante actas, declaraciones, seguridad, llaves, accesos y comunicaciones contemporáneas.',
      question: '¿Qué título exacto autorizaba cada actuación material sobre el hotel y sobre bienes de otros titulares?'
    },
    {
      name: 'Shaila María Cogolludo Ramos',
      group: 'Actor privado · Comunidad / documentación',
      role: 'Figura documentada en el perímetro de administración, cuentas, representación y declaraciones de 2018.',
      fact: 'La investigación separa su papel personal de la antigüedad de Pamalexsha: no se atribuye una fecha de incorporación que no esté probada.',
      question: '¿Qué documentos preparó, recibió, custodió, firmó o transmitió y con qué efecto?'
    },
    {
      name: 'Francisco de Borja Rodríguez-Batllori Laffitte',
      group: 'Administrador Concursal · Concurso 36/2012',
      image: '../../assets/actors/francisco-de-borja-rodriguez-batllori.jpg',
      imageAlt: 'Retrato profesional archivado de Francisco de Borja Rodríguez-Batllori Laffitte',
      role: 'Administrador Concursal de Luchy Playa Blanca, S.L.U. La cuestión es qué verificó antes de permitir que actos privados controvertidos produjeran efectos concursales.',
      fact: 'Las acciones mercantiles, civiles, disciplinarias y penales promovidas cuestionan diligencia, independencia, protección de la masa, validación de deuda/actas, posesión, liquidación y rendición de cuentas. No existe condena penal aquí declarada.',
      question: 'Antes de aceptar cada acta, certificado, deuda, morosidad u officeholder: ¿comprobó independientemente su autoridad y soporte?'
    },
    {
      name: 'San Telmo Abogados y Economistas',
      group: 'Perímetro profesional posterior',
      role: 'El perfil archivado de Rodríguez-Batllori sitúa su incorporación a San Telmo en enero de 2014; la designación concursal es anterior.',
      fact: 'La cronología profesional justifica reconstrucción de relaciones, conflictos, disclosure y custodia documental; no prueba por sí sola coordinación ilícita.',
      question: '¿Qué relaciones existían en cada fecha, qué fue revelado y qué archivos del concurso quedaron bajo qué custodia?'
    },
    {
      name: 'Alberto López Villarrubia',
      group: 'Supervisión judicial',
      role: 'Magistrado-Juez del concurso durante el período relevante.',
      fact: 'Determinadas actuaciones y resoluciones han sido formalmente puestas en conocimiento de órganos competentes por posible relevancia penal, sin afirmar una responsabilidad criminal ya adjudicada.',
      question: 'Para cada alerta material: ¿qué conoció el Juzgado, qué medida podía adoptar, qué decidió, qué se ejecutó y qué efecto patrimonial permaneció?'
    }
  ],
  noticeTitle: '17 MAR 2021 · reacción contemporánea que exige trazabilidad',
  noticeText: 'Nueve días después de circular documentación confidencial sobre Sun Park, RIC y alertas regulatorias a un profesional con conocimiento previo del rescate/financiación del hotel, un mensaje de voz conservado comunicó una reacción procedente de un contacto empresarial previamente vinculado a ese perímetro y habló del malestar de «empresarios y sus contactos». La relevancia es de conocimiento y circulación de la alerta, no de amenaza o coordinación ilícita probada.',
  noticeLimits: 'Qué no acredita: filtración de información confidencial, identidad de los empresarios, mandato de RIC/CAM, coacción, conspiración o participación criminal. Pregunta: quién conoció qué entre el 8 y el 17 de marzo de 2021, por qué vía y con qué comunicaciones posteriores.',
  febTitle: '4 FEB 2022 · coste, voto, autoridad y fruto en una misma fecha crítica',
  febText: 'El acta localizada registra aproximadamente 20,993% presente o representado, mientras su propia tabla atribuye a LPB 72,976% y a Matkator 0,770%. También recoge deuda, voto, proyecto de CAM y actuaciones sobre permisos, obras e incorporación de todas las unidades y plazas a una explotación unitaria. La cuestión no es la aritmética aislada: es cómo deuda y morosidad construyeron el universo de voto y la disponibilidad que se proyectó fuera de la Comunidad.',
  burdenText: 'El material presentado atribuye a LPB aproximadamente €1,199m de deuda y, separadamente, alrededor de €3,26m de una derrama total de €4,467m para obras, además de una cantidad a Matkator. Al mismo tiempo los activos de LPB estaban en la secuencia de adjudicación a CAM. Pregunta: ¿por qué debía soportar LPB la mayor parte del coste de una mejora cuyos frutos esperados recaerían, de mantenerse la adjudicación, en otro perímetro?',
  matkatorText: 'Matkator no estaba en Concurso 36/2012. Ninguna adjudicación de bienes de LPB podía por sí sola transferir su propiedad ni autorizar obras, integración hotelera, renumeración o explotación de sus unidades. El escrito de 6 AGO 2026 pide a Yaiza una conciliación finca por finca y año por año de IBI, basura, sujeto pasivo, pagador, cambios y pagos por CAM/HNT/terceros. Es una solicitud de comprobación, no un hallazgo municipal ya emitido.',
  criminalLimit: 'Control de lenguaje: la web sostiene y atribuye las alegaciones formuladas en vías civil, mercantil/concursal, disciplinaria y penal, pero no presenta como hechos judicialmente declarados ni la existencia de una conspiración, ni la falsedad penal de una deuda, ni la prevaricación, ni la participación criminal de persona alguna.'
} : {
  actorKicker: 'People, functions and authority',
  actorTitle: 'Not a gallery of guilt: who could do what, on which document, and with what consequence.',
  actorIntro: 'The site separates private actors, the Insolvency Administration and judicial supervision. A photograph identifies a public function or documented intervention; visual proximity is not evidence of coordination.',
  operatorTitle: 'Legal starting point: the Operating Community was not the Owners’ Community.',
  operatorText: 'Aweswell’s documented position is that the Comunidad de Explotación del Complejo Sun Park (CESP / Explotadora) received the tourist operation of the complex in 2008 and continued the hotel activity. The Owners’ Community was an owners/governance body: that status did not itself make it the lawful hotel operator. CAM, HNT, Canarian Hospitality, MYND or any other entity is not described as CESP’s lawful successor without the specific instrument extinguishing, assigning or replacing CESP’s operating title.',
  operatorQuestion: 'Decisive document: what instrument validly extinguished or displaced CESP’s operating title, and on what date?',
  actors: [
    {name:'José Daniel Acosta Matos',group:'Private actor · CAM / RIC',image:'../../assets/evidence/ric-webinar-sun-park.webp',imageAlt:'Documentary frame from the 11 November 2020 RIC webinar concerning Sun Park',role:'RIC director and principal public CAM voice for the Sun Park project.',fact:'The 11 NOV 2020 webinar contains public statements about purchase, own funds, charges, portfolio status and the Sun Park timetable.',question:'What title, due diligence and approval supported each statement on the date it was made?'},
    {name:'Francisco Mario Matos Matas',group:'Private actor · Community perimeter',role:'Administration/secretarial and certification perimeter associated with Pamalexsha–Community in the investigated record.',fact:'The 2022 minutes and certificates make debt provenance, arrears, voting, offices and authority central verification issues.',question:'Who produced each figure, minute and certificate, and what valid authority allowed it to have effect?'},
    {name:'Antonio Cogolludo Rojas',group:'Private actor · Community / security',role:'Figure in the presidency, representation, security and access perimeter during the critical 2018 sequence.',fact:'His role is reconstructed through minutes, statements, security, keys, access and contemporaneous communications.',question:'What exact legal capacity authorised each material act over the hotel and other owners’ property?'},
    {name:'Shaila María Cogolludo Ramos',group:'Private actor · Community / documentation',role:'Documented figure in the administration, accounts, representation and 2018 statement perimeter.',fact:'The investigation separates her personal role from Pamalexsha’s history and does not attribute an unproved start date.',question:'Which documents did she prepare, receive, hold, sign or transmit, and with what effect?'},
    {name:'Francisco de Borja Rodríguez-Batllori Laffitte',group:'Insolvency Administrator · Proceeding 36/2012',image:'../../assets/actors/francisco-de-borja-rodriguez-batllori.jpg',imageAlt:'Archived professional portrait of Francisco de Borja Rodríguez-Batllori Laffitte',role:'Insolvency Administrator of Luchy Playa Blanca, S.L.U. The issue is what he verified before disputed private acts were allowed to have insolvency effects.',fact:'Commercial/civil, professional and criminal filings challenge diligence, independence, estate protection, validation of debt/minutes, possession, liquidation and accounting. No criminal conviction is asserted here.',question:'Before accepting each minute, certificate, debt, arrears position or officeholder: did he independently verify authority and support?'},
    {name:'San Telmo Abogados y Economistas',group:'Later professional perimeter',role:'Rodríguez-Batllori’s archived profile places his joining San Telmo in January 2014; the insolvency appointment predates it.',fact:'The chronology warrants reconstruction of relationships, conflicts, disclosure and document custody; it does not by itself prove unlawful coordination.',question:'What relationships existed on each date, what was disclosed, and who held the insolvency records?'},
    {name:'Alberto López Villarrubia',group:'Judicial supervision',role:'Insolvency judge during the relevant period.',fact:'Specific acts and decisions have been formally placed before competent authorities as potentially criminally relevant, without asserting criminal responsibility has been adjudicated.',question:'For each material alert: what did the Court know, what power existed, what was decided, what was executed, and what patrimonial effect remained?'}
  ],
  noticeTitle: '17 MAR 2021 · contemporaneous reaction requiring traceability',
  noticeText: 'Nine days after confidential Sun Park/RIC/regulatory-alert material circulated to a professional with prior knowledge of the hotel rescue/finance perimeter, a preserved voice message reported a reaction from a business contact previously connected with that perimeter and referred to concern among “entrepreneurs and their contacts”. Its relevance is notice and information flow, not a proved threat or unlawful coordination.',
  noticeLimits: 'What it does not prove: leakage of confidential information, identity of the entrepreneurs, a RIC/CAM mandate, coercion, conspiracy or criminal participation. Question: who knew what between 8 and 17 March 2021, through which route, and what communications followed?',
  febTitle: '4 FEB 2022 · cost, vote, authority and fruit at one critical date',
  febText: 'The located minutes record approximately 20.993% present or represented, while their own table attributes 72.976% to LPB and 0.770% to Matkator. They also address debt, voting, the CAM project and steps concerning permits, works and incorporation of all units and parking spaces into a unitary operation. The issue is not arithmetic alone: it is how debt and arrears constructed the voting universe and apparent availability projected outside the Community.',
  burdenText: 'Filed material attributes approximately €1.199m of debt to LPB and, separately, around €3.26m of a €4.467m works assessment, plus an amount to Matkator. At the same time LPB’s assets were in the CAM adjudication sequence. Question: why was LPB to bear most of the cost of an improvement whose expected fruits would, if adjudication stood, accrue elsewhere?',
  matkatorText: 'Matkator was outside Insolvency Proceeding 36/2012. No adjudication of LPB property could by itself transfer Matkator title or authorise works, hotel integration, renumbering or operation of its units. The signed 6 AUG 2026 Yaiza filing requests a property-by-property and year-by-year reconciliation of IBI, waste charges, taxpayer, payer, changes and payments by CAM/HNT/third parties. It is a verification request, not a municipal finding already made.',
  criminalLimit: 'Language control: the site stands behind and accurately attributes allegations advanced in civil, commercial/insolvency, professional and criminal proceedings, but does not present conspiracy, criminal falsification of debt, judicial misconduct or criminal participation by any person as already adjudicated facts.'
};

function actorCard(actor) {
  const image = actor.image ? `<img src="${actor.image}" alt="${esc(actor.imageAlt || actor.name)}" loading="lazy" style="width:100%;max-height:230px;object-fit:cover;border-radius:.65rem;margin-bottom:1rem">` : '';
  return `<article class="path-card" style="height:100%">${image}<span class="number">${esc(actor.group)}</span><h3>${esc(actor.name)}</h3><p><strong>${isSpanish ? 'Función:' : 'Role:'}</strong> ${actor.role}</p><p><strong>${isSpanish ? 'Registro:' : 'Record:'}</strong> ${actor.fact}</p><p><strong>${isSpanish ? 'Pregunta pendiente:' : 'Open question:'}</strong> ${actor.question}</p></article>`;
}

if (dossierRoot && !document.getElementById('actor-accountability-12aug')) {
  const anchor = document.getElementById('pregunta-unitaria');
  if (anchor) {
    const section = document.createElement('section');
    section.className = 'section alt';
    section.id = 'actor-accountability-12aug';
    section.innerHTML = `
      <div class="shell">
        <div class="section-head">
          <div><p class="kicker">${data.actorKicker}</p><h2>${data.actorTitle}</h2></div>
          <p>${data.actorIntro}</p>
        </div>
        <div class="pressure-maxim"><strong>${data.operatorTitle}</strong><span>${data.operatorText}<br><br><b>${data.operatorQuestion}</b></span></div>
        <div class="responsibility-grid" style="margin-top:1.5rem">${data.actors.map(actorCard).join('')}</div>
        <div class="pressure-maxim" style="margin-top:1.5rem"><strong>${data.noticeTitle}</strong><span>${data.noticeText}<br><br>${data.noticeLimits}</span></div>
        <div class="pressure-maxim" style="margin-top:1.5rem"><strong>${data.febTitle}</strong><span>${data.febText}<br><br>${data.burdenText}<br><br>${data.matkatorText}</span></div>
        <p class="source-policy" style="margin-top:1.25rem"><strong>${isSpanish ? 'Límite probatorio:' : 'Evidence limit:'}</strong> ${data.criminalLimit}</p>
      </div>`;
    anchor.insertAdjacentElement('afterend', section);
  }
}

const updates = document.querySelector('#actualizaciones');
if (updates && !dossierRoot && !document.getElementById('actor-update-12aug2026')) {
  const section = document.createElement('section');
  section.className = 'section alt';
  section.id = 'actor-update-12aug2026';
  section.innerHTML = isSpanish ? `
    <div class="shell">
      <div class="section-head"><div><p class="kicker">12 agosto 2026 · actualización de coherencia</p><h2>De actores aislados a una cadena de autoridad verificable.</h2></div><p>La lectura pública se reorganiza alrededor de una pregunta: quién tenía título para actuar, quién verificó ese título y qué consecuencia produjo cada documento.</p></div>
      <div class="grid-3">
        <article class="path-card primary"><span class="number">01 · EXPLOTACIÓN</span><h3>CESP / Explotadora</h3><p>La Comunidad de Explotación del Complejo Sun Park se presenta como la explotadora hotelera cuya sustitución jurídica exige un título concreto; la Comunidad de Propietarios no se confunde con la operadora.</p></article>
        <article class="path-card"><span class="number">02 · 4 FEB 2022</span><h3>Coste, voto y fruto</h3><p>20,993% presente/representado; LPB 72,976%; Matkator 0,770%; deuda, reforma y autoridad hotel-wide sometidas a conciliación documental. El punto es quién debía pagar y quién recibiría los frutos.</p></article>
        <article class="path-card"><span class="number">03 · CONTROL</span><h3>Privado → AC → Juzgado</h3><p>Los actores privados, el Administrador Concursal y la supervisión judicial se muestran por funciones separadas. Las alegaciones penales se atribuyen como tales; no se publican como condenas inexistentes.</p></article>
      </div>
    </div>` : `
    <div class="shell">
      <div class="section-head"><div><p class="kicker">12 August 2026 · coherence update</p><h2>From isolated actors to a verifiable authority chain.</h2></div><p>The public record is reorganised around one question: who had authority to act, who verified that authority, and what consequence followed from each document.</p></div>
      <div class="grid-3">
        <article class="path-card primary"><span class="number">01 · OPERATION</span><h3>CESP / Explotadora</h3><p>The Comunidad de Explotación del Complejo Sun Park is presented as the hotel operating vehicle whose lawful replacement requires a specific instrument; the Owners’ Community is not conflated with the operator.</p></article>
        <article class="path-card"><span class="number">02 · 4 FEB 2022</span><h3>Cost, vote and fruit</h3><p>20.993% present/represented; LPB 72.976%; Matkator 0.770%; debt, refurbishment and hotel-wide authority submitted to documentary reconciliation. The issue is who was to pay and who would receive the fruits.</p></article>
        <article class="path-card"><span class="number">03 · CONTROL</span><h3>Private → administrator → court</h3><p>Private actors, the Insolvency Administrator and judicial supervision are shown as distinct functions. Criminal allegations are attributed as allegations; they are not published as convictions that do not exist.</p></article>
      </div>
    </div>`;
  updates.parentNode.insertBefore(section, updates);
}
