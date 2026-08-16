(() => {
  const path = window.location.pathname.replace(/\/+$/, '/');
  const isEs = document.documentElement.lang.toLowerCase().startsWith('es') || path.includes('/es/');
  const relevant = [
    '/es/calificacion-concurso-36-2012-vidas-paralelas/',
    '/en/insolvency-classification-parallel-lives/',
    '/es/mensaje-abierto-cgpj/',
    '/en/open-message-cgpj/',
    '/es/concurso-36-2012-magistrado-juez/',
    '/en/insolvency-36-2012-mercantile-court-1/',
    '/es/concurso-36-2012-juzgado-mercantil-1/',
    '/es/concurso-36-2012-responsabilidad-institucional/',
    '/en/insolvency-36-2012-institutional-accountability/'
  ];
  if (!relevant.some(route => path.endsWith(route))) return;
  if (document.getElementById('lpam-magistrado-source-control')) return;

  const section = document.createElement('section');
  section.id = 'lpam-magistrado-source-control';
  section.className = 'section alt';
  section.dataset.lpamMagistradoSourceControl = 'true';
  section.innerHTML = isEs ? `
    <div class="shell record">
      <p class="eyebrow">CONTROL DE FUENTES · LPAM–MAGISTRADO · 16 AGO 2026</p>
      <h2>Qué está documentado, qué se ha corregido y qué todavía exige verificación oficial</h2>
      <p>La revisión conjunta de Gmail, Library/Files, Drive y los documentos judiciales permite separar por fin las capas de este módulo. <strong>No publicamos como hecho que existiera una amistad, acceso impropio, influencia o coordinación.</strong> Publicamos qué fuentes existen y qué registro oficial puede confirmarlas, rechazarlas o limitar su alcance.</p>
      <ul>
        <li><strong>24 enero 2018 · registro contemporáneo:</strong> un correo conserva una partida de <em>“Intermediación/Comisiones (3%) - 350.000,00”</em>. Acredita que esa partida fue consignada en aquel contexto comercial. <strong>No acredita por sí sola pago, destinatario, ilicitud ni vínculo alguno con el Magistrado.</strong></li>
        <li><strong>5 junio 2020 · memorialización contemporánea:</strong> Patricia Domínguez dejó por escrito afirmaciones que atribuye a Laura Patricia Acosta Matos sobre amistad/acceso/contacto con el Magistrado y señaló a Cristo como presente. Esto acredita la existencia del relato a esa fecha; <strong>no acredita la verdad de la relación afirmada</strong> ni sustituye metadatos telefónicos, comunicaciones directas o una comprobación oficial.</li>
        <li><strong>12 y 18 mayo 2021 · documentos judiciales:</strong> el expediente acredita la condición procesal de Construcciones Acosta Matos, S.A. y que su <em>representación</em> acudió a la comparecencia de 18 de mayo. Los documentos examinados <strong>no identifican personalmente a LPAM como representante</strong>; esa identificación personal procede hoy del material testimonial y requiere lista de asistentes/poderes para su comprobación independiente.</li>
        <li><strong>Contraprueba obligatoria:</strong> el Auto 164/2021 de 18 de mayo recoge que Aweswell formuló la oferta superior y que el resultado inmediato de aquella comparecencia fue favorable a Aweswell. Ese dato debe permanecer visible frente a cualquier teoría simplista de una decisión predeterminada en favor de CAM.</li>
        <li><strong>Corrección testimonial:</strong> las declaraciones firmadas de 28 de julio de 2026 limitan lo observado a la salida del Magistrado, saludo y breve intercambio/cortesías. Patricia dice expresamente que no oyó el contenido de una conversación privada, no vio a LPAM a solas con el Magistrado y no la vio entrar en su despacho. La expresión anterior de Gil equivalente a <em>“conversación privada”</em> queda controlada como inferencia, no como percepción auditiva directa.</li>
        <li><strong>Anomalía técnica del Auto de 18 mayo:</strong> la copia judicial preservada muestra una marca de descarga a las <strong>11:50:54</strong> y una firma electrónica del Magistrado a las <strong>12:47:38</strong> del mismo día. La secuencia merece certificación técnica sobre generación, firma, puesta a disposición, descarga y notificación; <strong>no constituye por sí sola prueba de alteración, retrodatación, predeterminación o conducta irregular.</strong></li>
        <li><strong>CGPJ · 28–30 julio 2026:</strong> el paquete de cinco PDF fue presentado bajo <code>REGAGE26e00069061338</code>. Una notificación REC de 30 de julio añade que la presentación <em>“ha pasado a ser tramitada por”</em> el <strong>Registro General del CGPJ</strong> a las 08:36:02. Esto prueba presentación y enrutamiento registral posterior; <strong>todavía no prueba unión a Alzada 286/2026, examen sustantivo, aceptación ni veracidad.</strong></li>
      </ul>
      <p><strong>Relevancia para la calificación:</strong> este módulo sólo puede utilizarse, en el estado actual de la prueba, como una cuestión separada de apariencia de imparcialidad y verificación finita alrededor de un Magistrado que posteriormente adoptó determinadas proposiciones como hallazgos judiciales en la Sentencia 163/2023. No permite saltar de un relato histórico a “sesgo probado” ni a “sentencia procurada por un actor privado”. Ese puente temporal y causal tendría que probarse por separado.</p>
      <p><strong>Comprobaciones finitas pendientes:</strong> lista certificada de asistentes/poderes y audiovisual o acta de 18/05/2021; certificado técnico del sistema judicial sobre las horas del Auto; fuentes lícitas independientes capaces de confirmar o refutar el contacto alegado; trazabilidad de la partida de €350.000; informe fiscal y decisión posterior en DP 1901/2026; índice íntegro de Alzada 286/2026 que muestre la incorporación y tratamiento de cada archivo; y cualquier prueba de continuidad temporal relevante hasta la calificación de 2023.</p>
    </div>` : `
    <div class="shell record">
      <p class="eyebrow">SOURCE CONTROL · LPAM–JUDGE · 16 AUG 2026</p>
      <h2>What is documented, what has been corrected, and what still requires official verification</h2>
      <p>The combined Gmail, Library/Files, Drive and court-record review now separates the evidential layers of this module. <strong>We do not publish as fact that there was a friendship, improper access, influence or coordination.</strong> We publish the sources that exist and the official records capable of confirming, rejecting or narrowing them.</p>
      <ul>
        <li><strong>24 January 2018 · contemporaneous record:</strong> an email preserves a line for <em>“Intermediación/Comisiones (3%) - 350.000,00”</em>. It proves that the line was recorded in that commercial context. <strong>It does not by itself prove payment, recipient, illegality or any link to the Judge.</strong></li>
        <li><strong>5 June 2020 · contemporaneous memorialisation:</strong> Patricia Domínguez put in writing statements she attributes to Laura Patricia Acosta Matos concerning friendship/access/contact with the Judge and identified Cristo as present. This proves the account existed by that date; <strong>it does not prove the asserted relationship was true</strong> and is not a substitute for telephone metadata, direct communications or official verification.</li>
        <li><strong>12 and 18 May 2021 · court records:</strong> the file establishes Construcciones Acosta Matos, S.A.'s procedural role and records that its <em>representation</em> attended the 18 May event. The records reviewed <strong>do not personally identify LPAM as that representative</strong>; her personal identification currently rests on witness material and requires the certified attendance/powers record for independent confirmation.</li>
        <li><strong>Mandatory counterevidence:</strong> the 18 May Auto 164/2021 records that Aweswell made the higher offer and that the immediate result of the event favoured Aweswell. That fact must remain visible against any simplistic theory that the event itself was predetermined in CAM's favour.</li>
        <li><strong>Witness correction:</strong> the signed 28 July 2026 declarations limit the observed episode to the Judge's exit, a greeting and brief words/courtesies. Patricia expressly says she did not hear the content of a private conversation, did not see LPAM alone with the Judge and did not see her enter his chambers. Gil's earlier wording equivalent to a <em>“private conversation”</em> is controlled as inference, not direct auditory observation.</li>
        <li><strong>18 May Auto technical anomaly:</strong> the preserved court copy displays a download marker at <strong>11:50:54</strong> and the Judge's electronic signature at <strong>12:47:38</strong> on the same date. The sequence warrants technical certification of generation, signing, availability, download and notification; <strong>it is not by itself evidence of alteration, backdating, predetermination or misconduct.</strong></li>
        <li><strong>CGPJ · 28–30 July 2026:</strong> the five-PDF package was presented under <code>REGAGE26e00069061338</code>. A 30 July REC notice further states that the presentation <em>“ha pasado a ser tramitada por”</em> the <strong>CGPJ General Registry</strong> at 08:36:02. This proves presentation and subsequent registry routing; <strong>it still does not prove joinder to Appeal 286/2026, substantive examination, acceptance or truth.</strong></li>
      </ul>
      <p><strong>Relevance to the insolvency classification:</strong> on the current evidence this module can only be used as a separate appearance-of-impartiality and finite-verification question concerning a Judge who later adopted selected propositions as judicial findings in Judgment 163/2023. It does not permit a leap from a historical account to “proven bias” or a “judgment procured by a private actor”. Any temporal and causal bridge must be proved separately.</p>
      <p><strong>Finite outstanding checks:</strong> certified attendance/powers and audiovisual record or substitute minute for 18 May 2021; court-system technical certification of the Auto timestamps; lawful independent sources capable of confirming or refuting the alleged contact; traceability of the €350,000 line; the Fiscalía report and later decision in DP 1901/2026; the complete Appeal 286/2026 index showing incorporation and treatment of each file; and any evidence of relevant temporal continuity into the 2023 classification adjudication.</p>
    </div>`;

  const main = document.querySelector('main');
  if (!main) return;
  const calTarget = document.getElementById('eleconomista');
  if (calTarget && calTarget.parentNode) {
    calTarget.parentNode.insertBefore(section, calTarget);
    return;
  }
  const sections = main.querySelectorAll(':scope > section');
  const last = sections[sections.length - 1];
  if (last && last.parentNode) last.parentNode.insertBefore(section, last);
  else main.appendChild(section);
})();
