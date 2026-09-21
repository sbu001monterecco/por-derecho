(() => {
  const path = window.location.pathname.replace(/\/+$/, '') + '/';
  const en = path.endsWith('/en/insolvency-classification-parallel-lives/');
  const es = path.endsWith('/es/calificacion-concurso-36-2012-vidas-paralelas/');
  if (!en && !es) return;
  if (document.querySelector('[data-cal-allegation01-20260816]')) return;

  const data = es ? {
    eyebrow: 'AUDITORÍA PROFUNDA · ALEGACIÓN 01 · COLABORACIÓN',
    title: '“No colaboró”: cuando el propio expediente de la AC contiene los hechos que contradicen la versión global',
    intro: 'La cuestión no es si LPB entregó perfectamente y a tiempo cada documento solicitado. No lo hizo: la propia fuente de 2013 habla de retrasos y documentación pendiente. La cuestión es distinta y más grave: si era veraz presentar esos incumplimientos parciales como una ausencia de colaboración que habría impedido a la Administración Concursal conocer las causas económicas de la insolvencia.',
    thesis: '<strong>Conclusión controlada:</strong> la formulación global de la AC queda materialmente contradicha por sus propias fuentes y fue después estrechada por la Sentencia 163/2023. Gil Marer alega que fue una exageración consciente y autoservicial porque la propia AC poseía y reprodujo el material contrario. No se presenta como falsedad penal ya declarada.',
    cards: [
      ['15 ENE 2013 · INFORME AC', 'Adverso, pero específico', 'La AC calificó la colaboración de “no aceptable” por retrasos y documentos faltantes, pero reconoció que el representante de LPB había asistido a todas las reuniones a las que fue convocado. El mismo informe pudo reconstruir historia jurídica y económica, actividad, causas, viabilidad, ratios, contabilidad, activos y pasivos.'],
      ['30 ENE 2018 · RESPUESTA REPRODUCIDA POR LA AC', 'Cooperación expresa', 'El informe adverso de 2019 reproduce a Gil diciendo que busca la mejor forma de colaborar, que no pretende obstaculizar y que responde los requerimientos punto por punto, distinguiendo lo ya aportado, lo pendiente y lo que dependía de terceros.'],
      ['11 FEB 2019 · INFORME DE CALIFICACIÓN', 'El salto acusatorio', 'Pese a ese historial, la AC presenta una tesis global: que la falta de colaboración le impidió conocer adecuadamente las causas económicas y obligó a acudir a presunciones de culpabilidad.'],
      ['28 SEP 2023 · SENTENCIA 163/2023', 'La versión global no sobrevive intacta', 'La sentencia reconoce que LPB entregó la documentación contable que poseía y no aprecia falta de colaboración respecto de esa contabilidad. Mantiene sólo una cuestión más estrecha sobre soportes de determinados créditos CEXP/terceros; ese extremo sigue recurrido.']
    ],
    chainTitle: 'La diferencia que no puede borrarse',
    chain: [
      ['1', 'Retrasos o documentos pendientes', 'Puede ser cierto y está documentado.'],
      ['2', 'Asistencia, respuestas y entregas sustanciales', 'También está documentado por la propia AC.'],
      ['3', 'Información económica, contable, operativa y de rescate en poder de la AC', 'También aparece en sus fuentes.'],
      ['4', '“La falta de colaboración impidió conocer las causas económicas”', 'Ésta es la proposición global que queda contradicha y judicialmente estrechada.']
    ],
    knowledgeTitle: 'Por qué la cuestión de conocimiento es aquí especialmente fuerte',
    knowledgeBody: 'No dependemos sólo de demostrar que un juez rechazó después parte de la acusación. El material contrario estaba <strong>dentro del informe que la propia AC redactó</strong>: respuestas expresas de cooperación, contabilidad ya recibida, datos de explotación, negociaciones con Haya, recapitalización, convenio/viabilidad, carta bancaria, posibles operadores y demanda comercial. Además, el informe AC de 2013 confirma asistencia a todas las reuniones convocadas. Por eso la acusación pública de Gil no es simplemente “se equivocó”: es que <strong>la AC sabía que su propio expediente no describía una ausencia simple de colaboración</strong>.',
    displacementTitle: '¿Qué desplazó del foco esa narrativa?',
    displacementIntro: 'El efecto práctico del marco “no coopera” fue cambiar la pregunta. El expediente contenía rutas de investigación que exigían mirar fuera de Gil y dentro de la economía real del hotel y de la propia administración concursal.',
    displacement: [
      ['Comunidad / CEXP', 'Gobernanza, obligaciones, cobros, gastos, servicios y créditos frente a terceros.'],
      ['Negocio hotelero', 'Quién explotaba, qué ingresos/costes existían, qué valor se preservaba y qué ocurría con la unidad de explotación.'],
      ['Rescate y salida', 'Haya, recapitalización, convenio, carta bancaria, operadores y clientes esperando reservar.'],
      ['Recuperación de valor', 'Qué acciones de cobro, preservación o recuperación siguió realmente la AC y cuáles no.'],
      ['DI 248/2018', 'En enero de 2019 Gil/Aweswell pedían a Fiscalía investigar al AC/CAM y afirmaban una vía financiada de conclusión del concurso.'],
      ['Administración de la masa', 'Qué decisiones de liquidación, disposición, control y protección patrimonial debían ser examinadas por sus propios resultados.']
    ],
    effect: '<strong>Efecto documentable:</strong> “¿qué ocurrió con el negocio, el valor, el control y las rutas de recuperación?” quedó desplazado por “¿por qué Gil no colabora con la AC?”. <strong>Intención de distraer</strong> sigue siendo una hipótesis de motivo que debe probarse actor por actor; no se convierte aquí en hecho establecido.',
    gradeTitle: 'Graduación probatoria actual',
    grades: [
      ['Proposición global de “no colaboración”', 'CONTRADICHA / ESTRECHADA', 'Las propias fuentes AC y la sentencia impiden presentarla como una ausencia global de cooperación.'],
      ['Incumplimientos documentales concretos', 'PARCIALMENTE DOCUMENTADOS', 'Hubo retrasos y materiales faltantes; no se borran para defender a Gil.'],
      ['Exageración consciente', 'ALEGACIÓN FUERTEMENTE FUNDADA', 'La AC poseía y reproducía los hechos contrarios a la caracterización global.'],
      ['Efecto autoservicial', 'FUERTE COMO EFECTO', 'El marco trasladó escrutinio desde la gestión, recuperación y economía del hotel hacia la conducta del denunciante/deudor.'],
      ['Motivo deliberado de distracción', 'HIPÓTESIS ABIERTA', 'Requiere demostrar finalidad subjetiva y beneficio/defensa de la trayectoria administrativa.'],
      ['Falsedad penal', 'NO ADJUDICADA', 'La calificación penal corresponde a los órganos competentes. Aquí se documenta la acusación y su base.']
    ],
    quote: '“La pregunta no es si Gil cumplió perfectamente cada requerimiento. La pregunta es si la Administración Concursal describió con verdad el historial de colaboración cuando lo utilizó para pedir una de las consecuencias personales y patrimoniales más severas del procedimiento.”',
    source: 'Control interno: CALIFICACION_ALLEGATION_01_COLLABORATION_FALSEHOOD_LEDGER_16AUG2026.md. Fuente adicional reconsultada: Informe AC art. 75 de 15-01-2013 (referencia pública MF-CAL-SRC-A01-ART75; localizador privado omitido). La frase “cordiales y fluidas” citada en apelación sigue pendiente de recuperación en su fuente AC original y no se usa aquí como hecho verificado.'
  } : {
    eyebrow: 'DEEP AUDIT · ALLEGATION 01 · COLLABORATION',
    title: '“He did not cooperate”: when the AC’s own record contains the facts that contradict the global portrayal',
    intro: 'The issue is not whether LPB perfectly and promptly delivered every requested document. It did not: the 2013 source itself records delays and outstanding material. The different and more serious question is whether those partial shortcomings could truthfully be presented as an absence of collaboration that prevented the insolvency administrator from understanding the economic causes of insolvency.',
    thesis: '<strong>Controlled conclusion:</strong> the AC’s global formulation is materially contradicted by his own sources and was later narrowed by Judgment 163/2023. Gil Marer alleges that it was a knowing and self-serving exaggeration because the AC himself held and reproduced the contrary material. It is not presented as an already adjudicated criminal falsehood.',
    cards: [
      ['15 JAN 2013 · AC REPORT', 'Adverse, but specific', 'The AC described cooperation as “not acceptable” because of delays and missing documents, but acknowledged that LPB’s representative had attended every meeting to which he was summoned. The same report was able to reconstruct legal and economic history, activity, causes, viability, ratios, accounting, assets and liabilities.'],
      ['30 JAN 2018 · RESPONSE REPRODUCED BY THE AC', 'Express cooperation', 'The adverse 2019 report reproduces Gil saying that he is seeking the best way to cooperate, has no intention of obstructing the AC and is answering requests item by item, distinguishing what had been supplied, what remained pending and what depended on third parties.'],
      ['11 FEB 2019 · CLASSIFICATION REPORT', 'The accusatory leap', 'Despite that record, the AC advances the broad proposition that lack of collaboration prevented him from properly knowing the economic causes and required reliance on statutory presumptions of culpability.'],
      ['28 SEP 2023 · JUDGMENT 163/2023', 'The global version does not survive intact', 'The judgment records that LPB delivered the accounting documentation it possessed and does not find non-collaboration as to that accounting. It preserves only a narrower issue concerning support for specified CEXP/third-party credits; that branch remains under appeal.']
    ],
    chainTitle: 'The distinction that cannot be erased',
    chain: [
      ['1', 'Delays or outstanding documents', 'Can be true and is documented.'],
      ['2', 'Attendance, responses and substantial deliveries', 'Also documented by the AC himself.'],
      ['3', 'Economic, accounting, operating and rescue information held by the AC', 'Also appears in his sources.'],
      ['4', '“Lack of collaboration prevented knowledge of the economic causes”', 'This is the broad proposition contradicted by the record and narrowed judicially.']
    ],
    knowledgeTitle: 'Why the knowledge issue is unusually strong here',
    knowledgeBody: 'This does not rest only on showing that a court later rejected part of the accusation. The contrary material was <strong>inside the report authored by the AC himself</strong>: express cooperation responses, accounting already received, operating information, Haya negotiations, recapitalisation, arrangement/viability work, a bank letter, possible operators and customer demand. The 2013 AC report also confirms attendance at every meeting convened by the AC. Gil’s public allegation is therefore not simply “he was mistaken”; it is that <strong>the AC knew his own file did not describe simple non-cooperation</strong>.',
    displacementTitle: 'What did that narrative push out of focus?',
    displacementIntro: 'The practical effect of the “non-cooperation” frame was to change the question. The record contained investigative routes that required looking beyond Gil and into the actual hotel economy and the conduct of the insolvency administration itself.',
    displacement: [
      ['Community / CEXP', 'Governance, obligations, collections, expenditure, services and third-party receivables.'],
      ['Hotel business', 'Who operated, what income/costs existed, what value was being preserved and what happened to the unity of exploitation.'],
      ['Rescue and exit', 'Haya, recapitalisation, arrangement, bank letter, operators and customers waiting to book.'],
      ['Value recovery', 'Which collection, preservation or recovery actions the AC actually pursued and which he did not.'],
      ['DI 248/2018', 'By January 2019 Gil/Aweswell were asking Fiscalía to investigate the AC/CAM perimeter and asserting a financed route to conclude the insolvency.'],
      ['Estate administration', 'Which liquidation, disposition, control and asset-protection decisions needed examination on their own results.']
    ],
    effect: '<strong>Documentable effect:</strong> “what happened to the business, value, control and recovery routes?” was displaced by “why is Gil not cooperating with the AC?”. <strong>An intention to distract</strong> remains a motive hypothesis requiring actor-specific proof; it is not converted here into an established fact.',
    gradeTitle: 'Current evidential grading',
    grades: [
      ['Global “non-collaboration” proposition', 'CONTRADICTED / NARROWED', 'The AC’s own sources and the judgment prevent a fair portrayal of total non-cooperation.'],
      ['Specific documentary shortcomings', 'PARTLY DOCUMENTED', 'There were delays and missing materials; they are not erased in order to defend Gil.'],
      ['Knowing exaggeration', 'STRONGLY GROUNDED ALLEGATION', 'The AC held and reproduced facts inconsistent with the global characterization.'],
      ['Self-serving effect', 'STRONG AS EFFECT', 'The frame redirected scrutiny away from administration, recovery and the hotel economy toward the conduct of the debtor/complainant.'],
      ['Deliberate distraction motive', 'OPEN HYPOTHESIS', 'Requires proof of subjective purpose and benefit/defence of the administrative trajectory.'],
      ['Criminal falsehood', 'NOT ADJUDICATED', 'Criminal characterization belongs to the competent authorities. This page documents the allegation and its basis.']
    ],
    quote: '“The question is not whether Gil perfectly complied with every request. The question is whether the insolvency administrator truthfully described the cooperation record when using it to seek some of the most severe personal and patrimonial consequences available in the proceeding.”',
    source: 'Internal control: CALIFICACION_ALLEGATION_01_COLLABORATION_FALSEHOOD_LEDGER_16AUG2026.md. Additional primary source re-queried: AC Article-75 report dated 15-Jan-2013 (public reference MF-CAL-SRC-A01-ART75; private locator withheld). The phrase “cordiales y fluidas” quoted in the appeal remains pending recovery in its original AC source and is not used here as a verified fact.'
  };

  const esc = (s) => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));

  const style = document.createElement('style');
  style.textContent = `
    [data-cal-allegation01-20260816]{background:#f7f4ec;border-top:1px solid rgba(19,37,45,.12);border-bottom:1px solid rgba(19,37,45,.12)}
    .a01-wrap{max-width:1080px;margin:0 auto;padding:4rem 1.25rem}.a01-eyebrow{font-size:.76rem;letter-spacing:.09em;text-transform:uppercase;font-weight:800;color:#755d31;margin-bottom:.55rem}
    .a01-wrap h2{font-size:clamp(2rem,4vw,3.25rem);line-height:1.05;max-width:900px;margin:.25rem 0 1rem}.a01-lead{font-size:1.13rem;line-height:1.65;max-width:920px}.a01-thesis{background:#13252d;color:#fff;border-radius:18px;padding:1.2rem 1.35rem;margin:1.4rem 0 2rem;line-height:1.55}
    .a01-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;margin:1.2rem 0 2.2rem}.a01-card{background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:16px;padding:1.15rem;border-top:5px solid #8c6b2f}.a01-card .k{font-size:.72rem;font-weight:800;letter-spacing:.06em;color:#755d31}.a01-card h3{font-size:1.08rem;margin:.35rem 0 .6rem}.a01-card p{margin:0;line-height:1.55}
    .a01-chain{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.75rem;margin:1rem 0 2.2rem}.a01-step{background:#fff;border:1px solid rgba(19,37,45,.15);border-radius:14px;padding:1rem}.a01-n{display:inline-grid;place-items:center;width:28px;height:28px;border-radius:50%;background:#13252d;color:#fff;font-weight:800;margin-bottom:.55rem}.a01-step strong{display:block;margin-bottom:.35rem}.a01-step p{margin:0;font-size:.92rem}
    .a01-knowledge{background:#fff;border:2px solid #13252d;border-radius:18px;padding:1.3rem 1.4rem;margin:1.3rem 0 2rem}.a01-knowledge h3{margin-top:0}
    .a01-displace{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.8rem;margin:1rem 0}.a01-d{background:#fff;border-radius:14px;padding:1rem;border:1px solid rgba(19,37,45,.13)}.a01-d strong{display:block;margin-bottom:.35rem}.a01-d p{margin:0;font-size:.93rem}.a01-effect{border-left:5px solid #8c6b2f;padding:1rem 1.2rem;background:#fff;border-radius:12px;margin:1rem 0 2.2rem}
    .a01-table{overflow-x:auto;margin-top:1rem}.a01-table table{width:100%;border-collapse:separate;border-spacing:0;font-size:.94rem}.a01-table th,.a01-table td{padding:.8rem;text-align:left;vertical-align:top;border-right:1px solid #dde1e1;border-bottom:1px solid #dde1e1}.a01-table th{background:#13252d;color:#fff}.a01-table td:first-child{border-left:1px solid #dde1e1;font-weight:700}.a01-status{font-size:.72rem;font-weight:900;letter-spacing:.04em}.a01-quote{font-size:1.2rem;line-height:1.55;font-weight:650;border-top:1px solid rgba(19,37,45,.18);border-bottom:1px solid rgba(19,37,45,.18);padding:1.4rem 0;margin:2rem 0}.a01-source{font-size:.84rem;color:#5e6262;line-height:1.5}
    @media(max-width:820px){.a01-grid,.a01-chain,.a01-displace{grid-template-columns:1fr}.a01-wrap{padding:3rem 1rem}}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.setAttribute('data-cal-allegation01-20260816', '');
  section.innerHTML = `<div class="a01-wrap">
    <div class="a01-eyebrow">${esc(data.eyebrow)}</div>
    <h2>${esc(data.title)}</h2>
    <p class="a01-lead">${esc(data.intro)}</p>
    <div class="a01-thesis">${data.thesis}</div>
    <div class="a01-grid">${data.cards.map(c => `<article class="a01-card"><div class="k">${esc(c[0])}</div><h3>${esc(c[1])}</h3><p>${esc(c[2])}</p></article>`).join('')}</div>
    <h3>${esc(data.chainTitle)}</h3>
    <div class="a01-chain">${data.chain.map(c => `<div class="a01-step"><span class="a01-n">${esc(c[0])}</span><strong>${esc(c[1])}</strong><p>${esc(c[2])}</p></div>`).join('')}</div>
    <div class="a01-knowledge"><h3>${esc(data.knowledgeTitle)}</h3><p>${data.knowledgeBody}</p></div>
    <h3>${esc(data.displacementTitle)}</h3><p>${esc(data.displacementIntro)}</p>
    <div class="a01-displace">${data.displacement.map(c => `<div class="a01-d"><strong>${esc(c[0])}</strong><p>${esc(c[1])}</p></div>`).join('')}</div>
    <div class="a01-effect">${data.effect}</div>
    <h3>${esc(data.gradeTitle)}</h3>
    <div class="a01-table"><table><thead><tr><th>${es?'Proposición':'Proposition'}</th><th>${es?'Estado':'Status'}</th><th>${es?'Por qué':'Why'}</th></tr></thead><tbody>${data.grades.map(r => `<tr><td>${esc(r[0])}</td><td><span class="a01-status">${esc(r[1])}</span></td><td>${esc(r[2])}</td></tr>`).join('')}</tbody></table></div>
    <div class="a01-quote">${esc(data.quote)}</div>
    <p class="a01-source">${esc(data.source)}</p>
  </div>`;

  const anchor = document.querySelector('[data-calificacion-radical-20260816]');
  if (anchor) anchor.insertAdjacentElement('afterend', section);
  else {
    const hero = document.querySelector('.hero.cal-hero') || document.querySelector('main .hero');
    if (hero) hero.insertAdjacentElement('afterend', section);
  }
})();
