(() => {
  'use strict';

  const path = window.location.pathname.replace(/\/+$/, '/');
  const isEs = document.documentElement.lang.toLowerCase().startsWith('es') || path.includes('/es/');

  const fullRoutes = [
    '/es/calificacion-concurso-36-2012-vidas-paralelas/',
    '/en/insolvency-classification-parallel-lives/',
    '/es/calificacion-concurso-36-2012-vidas-paralelas/conocimiento-previo-rescate/',
    '/en/insolvency-classification-parallel-lives/prior-judicial-knowledge-rescue/',
    '/es/concurso-36-2012-magistrado-juez/',
    '/en/insolvency-36-2012-mercantile-court-1/',
    '/es/mensaje-abierto-cgpj/',
    '/en/open-message-cgpj/'
  ];

  const compactRoutes = [
    '/es/mismo-hotel-multiples-vidas-financieras/',
    '/en/same-hotel-multiple-financial-lives/',
    '/es/ric-private-equity-sun-park/',
    '/en/ric-private-equity-sun-park/',
    '/es/registros-institucionales/',
    '/en/institutional-records/',
    '/es/concurso-36-2012-responsabilidad-institucional/',
    '/en/insolvency-36-2012-institutional-accountability/'
  ];

  const isFull = fullRoutes.some(route => path.endsWith(route));
  const isCompact = compactRoutes.some(route => path.endsWith(route));
  if (!isFull && !isCompact) return;
  if (document.getElementById('lpam-cgpj169-calificacion-unitary')) return;

  const section = document.createElement('section');
  section.id = 'lpam-cgpj169-calificacion-unitary';
  section.className = 'section alt';
  section.dataset.lpamCgpj169Unitary = '20260817b';

  const esFull = `
    <div class="shell record">
      <p class="eyebrow">CADENA DE CONOCIMIENTO · 2018 → 2021 → 2023 → CGPJ 2026</p>
      <h2>El mismo hotel ya tenía varias vidas documentadas antes de la Sentencia 163/2023</h2>
      <p>El punto probatorio ya no es si Sun Park podía analizarse únicamente como una concursada y una deuda de renta. El expediente documenta capas simultáneas: <strong>masa de LPB, propiedad mixta, acceso/control material, explotación hotelera, proyecto CAM, promoción/inversión RICPE y venta concursal</strong>. La pregunta de Calificación es qué efecto tuvo ese contexto conocido sobre <strong>poder real, capacidad, agencia y causalidad</strong>.</p>

      <div class="callout">
        <p><strong>13 ENE 2021 · CNMV + AEAT.</strong> La comunicación a CNMV quedó registrada con nº <code>2021002141</code>. Un registro telemático AEAT del mismo día documenta <code>ZZ061 / ZZ06</code>, asunto <em>“Posible fraude de inversores mediante la materialización de la RIC”</em>, con la denuncia RICPE anexa. <strong>El registro prueba recepción/tramitación de entrada; no prueba fraude ni una conclusión de fondo del regulador.</strong></p>
      </div>

      <div class="callout">
        <p><strong>4 FEB / 17 FEB 2021 · LEXNET + REGISTRO 918/2021.</strong> Aweswell presentó formalmente en el Concurso 36/2012 recurso de reposición contra el Auto de 25-ene-2021. El escrito alegó expresamente que CAM se presentaba públicamente como propietaria/proyecto de Sun Park y captaba inversores mediante RIC Private Equity, invocando o anexando material del webinar/web y lo remitido a CNMV. La Diligencia de 17-feb registra y tramita ese recurso como <strong>918/2021</strong>.</p>
        <p><strong>Consecuencia:</strong> la vida externa CAM/RICPE del hotel no es sólo una reconstrucción posterior. La alegación entró formalmente en el mismo procedimiento mercantil antes de la sentencia de 2023. Eso prueba <em>conocimiento institucional del expediente sobre la cuestión</em>; no demuestra por sí solo que el Magistrado leyera cada anexo ni que cada alegación fuera verdadera.</p>
      </div>

      <p><strong>2023 · CALIFICACIÓN.</strong> Permanecen hallazgos adversos de primera instancia sobre renta/Pink, Libro Diario y una cuestión más estrecha de colaboración documental, todos dentro del estado de recurso publicado. La cuestión finita ahora es si el contexto ya incorporado de control, comercialización, inversión y adquisición se reconstruyó al atribuir a Gil/Pink capacidad de cobro, causalidad y la consecuencia de <strong>€3.032.010,34</strong>.</p>

      <div class="callout">
        <p><strong>CUESTIÓN ADICIONAL DE IMPARCIALIDAD APARENTE.</strong> Existe un relato documentado que atribuye a <strong>un actor privado de un perímetro materialmente interesado</strong> un grado inusualmente próximo de proximidad personal o acceso directo al decisor judicial. El relato se considera suficientemente serio para exigir comprobación independiente, pero <strong>no se publica como hecho probado</strong>.</p>
        <p>La pregunta es cerrada y verificable: <strong>palabras exactas → fecha/lugar/testigos → llamadas/mensajes → reuniones/accesos → eventual canal declarado o no declarado → corroboración o refutación</strong>. La existencia de esa alegación no prueba por sí sola amistad, influencia, parcialidad, concertación, corrupción ni prevaricación.</p>
      </div>

      <p><strong>DI 169/2026 · ALZADA 286/2026.</strong> El archivo disciplinario es de <strong>14-may-2026</strong>. El recurso se presentó formalmente el <strong>15-jun-2026</strong> bajo <code>REGAGE26e00056359487</code>; el <strong>18-jun</strong> es la fecha de entrada en CGPJ comunicada después por la Sección de Recursos. El escrito de 15-jul quedó expresamente unido al expediente. El <strong>módulo específico sobre posible proximidad o acceso no declarado</strong> aparece por primera vez formalmente acreditado en la vía de Alzada en el suplemento de <strong>28-jul-2026</strong>, <code>REGAGE26e00069061338</code>. A la fecha de control no se ha localizado resolución sustantiva posterior ni prueba de examen de fondo de ese suplemento.</p>

      <p><strong>Gramática de prueba:</strong><br><code>VIDAS PARALELAS YA PUESTAS EN EL EXPEDIENTE → CONTROL/CAPACIDAD REAL → DEBER DE COBRO → CAPACIDAD REAL DE COBRAR/OPERAR → CAUSAS COMPETIDORAS → CAUSALIDAD ATRIBUIDA → CULPABILIDAD</code></p>

      <p><strong>Pregunta central:</strong> si antes de la titulación formal posterior el propio expediente contenía una impugnación que decía que CAM/RICPE presentaban el mismo hotel como proyecto propio de inversión, ¿qué efecto tuvo ese contexto sobre la capacidad real de Gil/Pink y sobre el puente causal hasta €3.032.010,34?</p>

      <p class="note"><strong>Límite:</strong> esta cadena refuerza cuestiones de conocimiento, causalidad, apariencia de imparcialidad e investigación. <strong>No prueba por sí sola amistad, influencia, concertación, corrupción ni prevaricación.</strong></p>
    </div>`;

  const enFull = `
    <div class="shell record">
      <p class="eyebrow">KNOWLEDGE CHAIN · 2018 → 2021 → 2023 → CGPJ 2026</p>
      <h2>The same hotel already had multiple documented lives before Judgment 163/2023</h2>
      <p>The evidential issue is no longer whether Sun Park could be analysed only as an insolvent company plus a rent debt. The record documents simultaneous layers: <strong>LPB estate, mixed ownership, material access/control, hotel operation, CAM project, RICPE investment/publicity and insolvency sale</strong>. The classification question is what effect that known context had on <strong>real power, capacity, agency and causation</strong>.</p>

      <div class="callout">
        <p><strong>13 JAN 2021 · CNMV + AEAT.</strong> The CNMV communication was formally registered as <code>2021002141</code>. An AEAT telematic registry record from the same date documents <code>ZZ061 / ZZ06</code>, subject <em>“Posible fraude de inversores mediante la materialización de la RIC”</em>, with the RICPE complaint attached. <strong>Registration proves intake/receipt; it does not prove fraud or a regulator merits finding.</strong></p>
      </div>

      <div class="callout">
        <p><strong>4 FEB / 17 FEB 2021 · LEXNET + REGISTRY 918/2021.</strong> Aweswell formally filed in Insolvency 36/2012 a reposición against the 25-Jan-2021 order. The pleading expressly alleged that CAM publicly presented itself as owner/project holder of Sun Park and attracted investors through RIC Private Equity, invoking or annexing webinar/web material and information sent to CNMV. The 17-Feb court Diligencia records and processes that challenge as <strong>918/2021</strong>.</p>
        <p><strong>Consequence:</strong> the hotel's external CAM/RICPE life is not merely a later reconstruction. The allegation entered the same Mercantile proceeding before the 2023 judgment. That proves <em>institutional court-record notice of the issue</em>; it does not by itself prove that the Judge read every annex or that every allegation was true.</p>
      </div>

      <p><strong>2023 · CLASSIFICATION.</strong> Materially adverse first-instance findings remain on the Pink/rent branch, Daily Journal issue and a narrower document-cooperation issue, all within the published appeal status. The finite question is now whether the already-filed context of control, commercialisation, investment and acquisition was reconstructed before assigning Gil/Pink collection capacity, causation and the <strong>€3,032,010.34</strong> consequence.</p>

      <div class="callout">
        <p><strong>ADDITIONAL APPEARANCE-OF-IMPARTIALITY QUESTION.</strong> A documented account attributes to <strong>a private actor within a materially interested perimeter</strong> an unusually close degree of personal proximity or direct access to the judicial decision-maker. The account is considered sufficiently serious to require independent verification, but <strong>is not published as established fact</strong>.</p>
        <p>The question is finite and testable: <strong>exact words → date/place/witnesses → calls/messages → meetings/access → any disclosed or undisclosed channel → corroboration or disproof</strong>. The existence of the allegation does not by itself prove friendship, influence, bias, coordination, corruption or judicial prevarication.</p>
      </div>

      <p><strong>DI 169/2026 · APPEAL 286/2026.</strong> The disciplinary archive is dated <strong>14-May-2026</strong>. The appeal was formally presented on <strong>15-Jun-2026</strong> under <code>REGAGE26e00056359487</code>; <strong>18-Jun</strong> is the later CGPJ-reported Council entry date. The 15-Jul traceability filing was expressly confirmed as joined. The <strong>specific module concerning possible undisclosed proximity or direct access</strong> is first presently verified as formally presented in the appeal route in the <strong>28-Jul-2026</strong> supplement, <code>REGAGE26e00069061338</code>. No later substantive decision or proof of merits examination of that supplement has been located at the controlled cut-off.</p>

      <p><strong>Evidence grammar:</strong><br><code>PARALLEL LIVES ALREADY PUT IN THE RECORD → REAL CONTROL/CAPACITY → COLLECTION DUTY → REAL ABILITY TO COLLECT/OPERATE → COMPETING CAUSES → ATTRIBUTED CAUSATION → CULPABILITY</code></p>

      <p><strong>Central question:</strong> if, before later formal title, the court file already contained a challenge saying CAM/RICPE presented the same hotel as their investment project, what effect did that context have on Gil/Pink's real capacity and on the causal bridge to €3,032,010.34?</p>

      <p class="note"><strong>Boundary:</strong> this chain strengthens questions of knowledge, causation, appearance of impartiality and investigation. <strong>It does not by itself prove friendship, influence, coordination, corruption or judicial prevarication.</strong></p>
    </div>`;

  const esCompact = `
    <div class="shell record">
      <p class="eyebrow">ACTUALIZACIÓN PROBATORIA · 17 AGO 2026</p>
      <h2>La vida RICPE/CAM de Sun Park entró formalmente en Concurso 36/2012 antes de la sentencia de 2023</h2>
      <p>El 4-feb-2021 Aweswell presentó por LexNET una reposición que alegaba que CAM presentaba públicamente Sun Park como proyecto/propiedad y captaba inversores mediante RIC Private Equity; la Diligencia de 17-feb la registra como <strong>918/2021</strong>. CNMV y AEAT habían recibido el 13-ene comunicaciones formales sobre el mismo perímetro. <strong>Esto prueba la ruta de conocimiento institucional, no la verdad automática de cada alegación.</strong></p>
      <p>Permanece una cuestión no resuelta: si <strong>un actor privado de un perímetro materialmente interesado</strong> disfrutó de una proximidad personal o acceso directo no declarado al decisor judicial. <strong>Es una alegación que exige corroboración objetiva, no un hecho establecido.</strong> El módulo correspondiente fue presentado formalmente en Alzada 286/2026 el 28-jul-2026, <code>REGAGE26e00069061338</code>.</p>
      <p class="note"><strong>Límite:</strong> conocimiento institucional + alegación documentada justifican verificación; no prueban por sí solos influencia, concertación, corrupción o prevaricación.</p>
    </div>`;

  const enCompact = `
    <div class="shell record">
      <p class="eyebrow">EVIDENCE UPDATE · 17 AUG 2026</p>
      <h2>Sun Park's RICPE/CAM external life formally entered Insolvency 36/2012 before the 2023 judgment</h2>
      <p>On 4-Feb-2021 Aweswell filed by LexNET a reposición alleging that CAM publicly presented Sun Park as its property/project and attracted investors through RIC Private Equity; the 17-Feb Diligencia records it as <strong>918/2021</strong>. CNMV and AEAT had received formal 13-Jan communications concerning the same perimeter. <strong>This proves the institutional notice route, not the automatic truth of every allegation.</strong></p>
      <p>An unresolved question remains whether <strong>a private actor within a materially interested perimeter</strong> enjoyed undisclosed personal proximity or direct access to the judicial decision-maker. <strong>It is an allegation requiring objective corroboration, not an established fact.</strong> The corresponding module was formally presented in Appeal 286/2026 on 28-Jul-2026, <code>REGAGE26e00069061338</code>.</p>
      <p class="note"><strong>Boundary:</strong> institutional knowledge plus a documented allegation warrants verification; it does not by itself prove influence, coordination, corruption or judicial prevarication.</p>
    </div>`;

  section.innerHTML = isFull ? (isEs ? esFull : enFull) : (isEs ? esCompact : enCompact);

  const main = document.querySelector('main');
  if (!main) return;

  const existingLpam = document.getElementById('lpam-magistrado-source-control');
  if (existingLpam && existingLpam.parentNode) {
    existingLpam.insertAdjacentElement('afterend', section);
    return;
  }

  const priorKnowledge = document.querySelector('[data-calificacion-prior-judicial-knowledge], #calificacion-prior-judicial-knowledge');
  if (priorKnowledge && priorKnowledge.parentNode) {
    priorKnowledge.insertAdjacentElement('afterend', section);
    return;
  }

  const firstSection = main.querySelector(':scope > section');
  if (firstSection && firstSection.parentNode) firstSection.insertAdjacentElement('afterend', section);
  else main.appendChild(section);
})();