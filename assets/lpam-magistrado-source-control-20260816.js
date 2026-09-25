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
    '/en/insolvency-36-2012-institutional-accountability/',
    '/es/acosta-matos-perimetro/',
    '/en/acosta-matos-perimeter/'
  ];
  if (!relevant.some(route => path.endsWith(route))) return;
  if (document.getElementById('lpam-magistrado-source-control')) return;

  const section = document.createElement('section');
  section.id = 'lpam-magistrado-source-control';
  section.className = 'section alt';
  section.dataset.lpamMagistradoSourceControl = '20260817-source-complete';

  section.innerHTML = isEs ? `
    <div class="shell record">
      <p class="eyebrow">CONTROL DE FUENTES · LPAM–MAGISTRADO · REESCANEO 17 AGO 2026</p>
      <h2>La cronología documental es ahora más fuerte; la relación alegada sigue pendiente de prueba objetiva</h2>
      <p>El reescaneo de Gmail y del paquete institucional permite reforzar la <strong>procedencia y contemporaneidad</strong> del módulo sin convertirlo en una conclusión de parcialidad. <strong>No publicamos como hecho que existiera amistad íntima, acceso impropio, influencia, coordinación o una decisión judicial afectada por esa relación.</strong></p>
      <p><strong>Control de identidad:</strong> la declarante pertenece al perímetro personal y empresarial de Gil Marer y su identidad se reserva públicamente. Es una persona distinta de <strong>Laura Patricia Acosta Matos (LPAM)</strong>. El otro testigo se describe como <strong>un asesor jurídico de Gil Marer en aquel momento</strong>.</p>
      <ul>
        <li><strong>24 enero 2018 · reacción contemporánea:</strong> el paquete conserva un correo que consigna <em>“Intermediación/Comisiones (3%) - 350.000,00”</em> y solicita confirmar o corregir las cifras. La copia presentada documenta la reacción contemporánea; el mensaje nativo/RFC822 todavía debe recuperarse de forma independiente. <strong>No prueba pago, destinatario, ilicitud ni vínculo con el Magistrado.</strong></li>
        <li><strong>5 junio 2020 · fuente contemporánea recuperada:</strong> se ha releído una cadena preservada de correo dirigida a <strong>asesoría jurídica externa</strong>, en una conversación activa sobre Laura/CAM y una posible solución acordada. En ella la declarante deja por escrito las manifestaciones que atribuye a LPAM sobre móvil personal, comunicaciones diarias y numerosas llamadas, e identifica a un asesor jurídico como persona presente. <strong>Esto prueba que el relato estaba documentado en junio de 2020, años antes de DI 169/2026; no prueba que las llamadas o la relación afirmada fueran reales.</strong></li>
        <li><strong>18 mayo 2021 · dos relatos firmados, alcance limitado:</strong> Gil Marer y la declarante describen separadamente que, tras la comparecencia de licitación, observaron a LPAM y a una acompañante permanecer cerca de la Sala, vieron salir al Magistrado y observaron saludo, apretón de manos, palabras y sonrisas. <strong>Ninguno afirma haber oído una conversación privada, haber visto a LPAM entrar en el despacho, quedar a solas con el Magistrado ni conocer lo sucedido después.</strong></li>
        <li><strong>Contraprueba y corrección obligatorias:</strong> existió una vía formal de licitación y una propuesta de tercero de 14,8 millones de euros. Pero el Auto 164/2021 recoge que ese postor no compareció, no estaba personado y no depositó la fianza exigida; acto seguido aprobó definitivamente la propuesta de CAM sobre las fincas LPB enumeradas. Aweswell no ganó aquella comparecencia.</li>
        <li><strong>Capacidad procesal todavía por certificar:</strong> los documentos examinados acreditan la participación procesal de CAM y de su representación, pero la identificación personal de LPAM, sus poderes concretos y la identidad/capacidad de su acompañante necesitan lista certificada de asistentes, poderes y acta/audiovisual. El cargo societario de LPAM <strong>no equivale automáticamente</strong> a la condición jurídica de “parte” a efectos de la hipótesis planteada.</li>
        <li><strong>Auto de 18 mayo · cuestión técnica, no conclusión:</strong> la copia preservada presenta una marca de descarga a las <strong>11:50:54</strong> y firma electrónica a las <strong>12:47:38</strong>. Deben certificarse fin de la comparecencia, generación, firma, puesta a disposición, descarga y notificación. <strong>La secuencia aparente no prueba alteración, retrodatación, predeterminación ni irregularidad.</strong></li>
        <li><strong>Fiscalía · 16 enero 2026:</strong> <code>REGAGE26e00003908732</code> acredita presentación formal del núcleo LPAM–Magistrado; los avisos oficiales de estado acreditan presentación y posterior tramitación registral. Sigue abierta la trazabilidad anexo por anexo hacia DIP 2/2026.</li>
        <li><strong>CGPJ · 28–30 julio 2026:</strong> el paquete de cinco PDF se presentó bajo <code>REGAGE26e00069061338</code> y una notificación 060 de 30 de julio acredita su encaminamiento posterior al Registro General del CGPJ. <strong>Presentación/enrutamiento ≠ unión a Alzada 286/2026 ≠ examen de fondo ≠ aceptación ≠ veracidad.</strong> El reescaneo de 17 de agosto no localizó una resolución sustantiva posterior ni confirmación directa del examen del paquete; es un resultado de búsqueda acotado, no prueba de inexistencia.</li>
      </ul>
      <p><strong>Relevancia para Calificación, el Magistrado y el perímetro Acosta Matos:</strong> el módulo constituye, en el estado actual, una <strong>cuestión documentada de apariencia de imparcialidad susceptible de verificación finita</strong>. Cualquier conexión con Sentencia 163/2023 u otra actuación debe probarse acto por acto mediante <code>FUENTE → CAPACIDAD PROCESAL → EVIDENCIA ANTE EL ACTOR → POSIBLE RELEVANCIA → CONTRAPRUEBA → RECURSO/REMEDIO</code>. No autoriza a publicar “sesgo probado”, “amistad probada” ni que una sentencia fuera procurada por un actor privado.</p>
      <p><strong>Comprobaciones pendientes:</strong> mensaje nativo de 24-ene-2018; RFC822/metadatos de la cadena de 5-jun-2020; testimonio independiente y limitado del asesor jurídico si fuera necesario y compatible con el secreto profesional; acta/audiovisual, asistentes, poderes y cobertura final de 18-may-2021; certificación técnica del Auto; manifiesto de transmisión de DIP 2/2026; informe fiscal y actuación posterior en DP 1901/2026; índice/movimientos y decisión motivada de Alzada 286/2026; y cualquier informe real del Promotor, Inspección o Comisión Permanente.</p>
    </div>` : `
    <div class="shell record">
      <p class="eyebrow">SOURCE CONTROL · LPAM–JUDGE · 17 AUG 2026 RESCAN</p>
      <h2>The documentary chronology is stronger; the alleged relationship still requires objective proof</h2>
      <p>The Gmail and institutional-package rescan strengthens the module's <strong>provenance and contemporaneity</strong> without converting it into a finding of bias. <strong>We do not publish as fact that there was intimate friendship, improper access, influence, coordination or a judicial decision affected by such a relationship.</strong></p>
      <p><strong>Identity control:</strong> the declarant is within Gil Marer’s personal and business perimeter and their identity is withheld publicly. That person is distinct from <strong>Laura Patricia Acosta Matos (LPAM)</strong>. The other witness is described as <strong>one of Gil Marer’s legal advisers at the relevant time</strong>.</p>
      <ul>
        <li><strong>24 January 2018 · contemporaneous reaction:</strong> the package preserves an email recording <em>“Intermediación/Comisiones (3%) - 350.000,00”</em> and asking for the figures to be confirmed or corrected. The filed copy documents the contemporaneous reaction; the standalone native/RFC822 message remains to be independently recovered. <strong>It does not prove payment, recipient, illegality or any link to the Judge.</strong></li>
        <li><strong>5 June 2020 · contemporaneous source recovered:</strong> a preserved email chain to <strong>external legal counsel</strong> has been re-read in an active exchange concerning Laura/CAM and a possible agreed solution. In it the declarant records statements attributed to LPAM concerning a personal mobile number, daily communications and numerous calls, and identifies a legal adviser as present. <strong>This proves the account was documented by June 2020, years before DI 169/2026; it does not prove the calls or asserted relationship were real.</strong></li>
        <li><strong>18 May 2021 · two signed accounts, limited scope:</strong> Gil Marer and the declarant separately describe that after the tender hearing they observed LPAM and an accompanying woman remain near the courtroom, saw the Judge emerge, and observed a greeting, handshake, words and smiles. <strong>Neither claims to have heard a private conversation, seen LPAM enter chambers, seen her alone with the Judge or known what happened afterwards.</strong></li>
        <li><strong>Mandatory counterevidence and correction:</strong> a formal tender route and a reported EUR 14.8 million third-party proposal existed. But Auto 164/2021 records that the bidder did not appear, was not personated and did not lodge the required bond; it then definitively approved CAM's proposal for the enumerated LPB properties. Aweswell did not win that hearing.</li>
        <li><strong>Procedural capacity still requires certification:</strong> reviewed documents establish CAM's procedural participation and representation, but personal identification of LPAM, her exact powers and the identity/capacity of the accompanying woman require the certified attendance list, powers and audiovisual/minute. LPAM's corporate office does <strong>not automatically equal</strong> legal “party” status for the theory raised.</li>
        <li><strong>18 May Auto · technical question, not conclusion:</strong> the preserved copy shows a download marker at <strong>11:50:54</strong> and electronic signature at <strong>12:47:38</strong>. Hearing end, generation, signing, availability, download and notification require technical certification. <strong>The apparent sequence does not prove alteration, backdating, predetermination or misconduct.</strong></li>
        <li><strong>Fiscalía · 16 January 2026:</strong> <code>REGAGE26e00003908732</code> verifies formal presentation of the LPAM–Judge nucleus; official state notices verify presentation and later registry processing. Annex-by-annex traceability into DIP 2/2026 remains open.</li>
        <li><strong>CGPJ · 28–30 July 2026:</strong> the five-PDF package was presented under <code>REGAGE26e00069061338</code>, and a 30 July 060 notice verifies later routing to the CGPJ General Registry. <strong>Presentation/routing ≠ joinder to Appeal 286/2026 ≠ merits examination ≠ acceptance ≠ truth.</strong> The 17-August rescan located no later substantive decision or direct confirmation of examination of the package; that is a bounded search result, not proof of non-existence.</li>
      </ul>
      <p><strong>Relevance to the insolvency classification, Judge and Acosta Matos perimeter pages:</strong> on current evidence this is a <strong>documented appearance-of-impartiality question capable of finite verification</strong>. Any connection to Judgment 163/2023 or another act must be shown act by act through <code>SOURCE → PROCEDURAL CAPACITY → EVIDENCE BEFORE ACTOR → POSSIBLE RELEVANCE → COUNTEREVIDENCE → REVIEW/REMEDY</code>. It does not justify publishing “proven bias”, “proven friendship” or a judgment procured by a private actor.</p>
      <p><strong>Outstanding checks:</strong> native 24-Jan-2018 message; RFC822/metadata for the 5-Jun-2020 chain; independent and limited legal-adviser evidence if necessary and compatible with professional secrecy; 18-May-2021 audiovisual/minute, attendance, powers and final recording coverage; technical certification of the Auto; DIP 2/2026 transmission manifest; Fiscalía report and later act in DP 1901/2026; Appeal 286/2026 index/movements and reasoned decision; and any genuine Promotor, Inspection or Permanent Commission report.</p>
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
