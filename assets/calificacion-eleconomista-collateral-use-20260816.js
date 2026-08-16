(() => {
  const path = location.pathname.replace(/\/+$/, '') + '/';
  const esCal = '/por-derecho/es/calificacion-concurso-36-2012-vidas-paralelas/';
  const enCal = '/por-derecho/en/insolvency-classification-parallel-lives/';
  const esMedia = '/por-derecho/es/eleconomista-javier-romera-enero2025/';
  const enMedia = '/por-derecho/en/eleconomista-javier-romera-january2025/';
  const isES = path === esCal || path === esMedia;
  const isEN = path === enCal || path === enMedia;
  if (!isES && !isEN) return;
  if (document.getElementById('calificacion-eleconomista-collateral-use')) return;

  const css = document.createElement('style');
  css.textContent = `
  #calificacion-eleconomista-collateral-use{border-top:1px solid rgba(19,37,45,.14)}
  .ce-chain{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.8rem;margin:1rem 0}
  .ce-step{position:relative;border:1px solid rgba(19,37,45,.16);border-radius:14px;padding:1rem;background:#fff}
  .ce-step:not(:last-child):after{content:'→';position:absolute;right:-.72rem;top:42%;font-weight:800}
  .ce-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem;margin:1rem 0}
  .ce-card{border:1px solid rgba(19,37,45,.16);border-radius:14px;padding:1rem;background:#fff}
  .ce-card h3{margin-top:0}.ce-status{font-size:.72rem;font-weight:800;letter-spacing:.04em;text-transform:uppercase}
  .ce-open{border-left:5px solid #8c6b2f;background:#f3efe4;border-radius:12px;padding:1rem 1.15rem}
  .ce-dark{background:#13252d;color:white;border-radius:16px;padding:1.2rem 1.3rem}.ce-dark a{color:white}
  .ce-table{width:100%;border-collapse:collapse;margin:1rem 0}.ce-table th,.ce-table td{border:1px solid #dfe3e3;padding:.7rem;vertical-align:top;text-align:left}.ce-table th{background:#13252d;color:#fff}
  @media(max-width:860px){.ce-chain,.ce-grid{grid-template-columns:1fr}.ce-step:not(:last-child):after{content:'↓';right:auto;left:50%;top:auto;bottom:-1rem}}
  `;
  document.head.appendChild(css);

  const sec = document.createElement('section');
  sec.id = 'calificacion-eleconomista-collateral-use';
  sec.className = 'section alt';

  if (isES) {
    sec.innerHTML = `<div class="shell record">
      <p class="eyebrow">CALIFICACIÓN · USO EXTRAPROCESAL · ELCONOMISTA · ENERO 2025</p>
      <h2>La Sentencia 163/2023 tuvo al menos dos vidas</h2>
      <p><strong>Dentro del Concurso 36/2012</strong>, fue una sentencia de primera instancia materialmente adversa y recurrida sobre la calificación culpable de <strong>Luchy Playa Blanca, S.L.U. (LPB)</strong>, que al mismo tiempo rechazó o redujo partes relevantes del paquete acusatorio de la administración concursal y del Ministerio Fiscal. <strong>Fuera del concurso</strong>, la secuencia del 16 al 20 de enero de 2025 muestra que fue utilizada como material judicial adverso mientras elEconomista contrastaba cuestiones mucho más amplias sobre Sun Park, CAM, Meeting Point/FTI, comercialización y financiación.</p>
      <div class="ce-dark"><strong>Conclusión de procedencia controlada.</strong><p>La identidad técnica del remitente físico sigue abierta; <strong>la procedencia contextual ya no es neutral</strong>. La secuencia fechada sustenta con fuerza que la Sentencia 163/2023 fue suministrada o procurada a través del <strong>canal de respuesta CAM/Acosta Matos activado tras la intervención de Laura Patricia Acosta Matos</strong>. No afirmamos todavía que LPAM pulsara personalmente «enviar», ni que Borja Rodríguez-Batllori, un abogado u otro intermediario fuera el transmisor físico: para eso hacen falta el mensaje entrante nativo y sus cabeceras.</p></div>
      <div class="ce-chain" aria-label="Cadena de uso colateral">
        <div class="ce-step"><strong>AC + Fiscalía</strong><p>Paquete de calificación adverso.</p></div>
        <div class="ce-step"><strong>Sentencia 163/2023 → apelación</strong><p>Decisión adversa de primera instancia; recursos ya interpuestos antes de enero de 2025.</p></div>
        <div class="ce-step"><strong>16–17 ENE 2025</strong><p>Canal de respuesta CAM/LPAM; Romera confirma que le piden esperar al lunes para recibir «autos judiciales».</p></div>
        <div class="ce-step"><strong>20 ENE 2025</strong><p>Llega <em>AUTO CONCURSO CULPOSO.pdf</em>; Romera comunica: «con esto no podemos publicarlo».</p></div>
      </div>
      <h3>Cuatro correcciones necesarias</h3>
      <div class="ce-grid">
        <article class="ce-card"><span class="ce-status">DOCUMENTO</span><h3>Sentencia, no auto</h3><p>El documento operativo era la <strong>Sentencia 163/2023</strong>. El nombre del archivo y la descripción contemporánea como «auto» no deben convertirse en una descripción jurídica correcta del documento.</p></article>
        <article class="ce-card"><span class="ce-status">SUJETO</span><h3>LPB, no Sun Park entero</h3><p>La concursada era LPB. El complejo de propiedad mixta, sus demás titulares y sus fincas extraconcursales no se convierten por esa sentencia en el deudor del concurso.</p></article>
        <article class="ce-card"><span class="ce-status">ESTADO</span><h3>Primera instancia y recurrida</h3><p>La resolución era adversa, pero estaba recurrida. Sigue abierta la pregunta de qué se dijo al medio sobre apelación, firmeza y alcance de la inhabilitación.</p></article>
        <article class="ce-card"><span class="ce-status">OBJETO</span><h3>No resolvía la historia más amplia</h3><p>No adjudicaba por sí sola la titularidad hotelera total, Matkator, el control material de 2018, la autoridad de Meeting Point/Club Sei, RIC/RICPE, incentivos o FEDER.</p></article>
        <article class="ce-card"><span class="ce-status">CAUSALIDAD</span><h3>No legitima retroactivamente 2018</h3><p>Una sentencia de 2023 contra Gil/LPB no crea retrospectivamente la autoridad que pudiera faltar para actos concretos de control, acceso, obras o comercialización en 2018.</p></article>
        <article class="ce-card"><span class="ce-status">EFECTO</span><h3>La consecuencia sí está documentada</h3><p>Tras recibir el documento, Romera comunicó que con ese material no podían publicar. Documentar esa consecuencia no equivale a declarar jurídicamente censura o interferencia ilícita.</p></article>
      </div>
      <h3>Por qué cambia la lectura de la calificación</h3>
      <p>El episodio refuerza la necesidad de separar <strong>lo que la sentencia realmente decidió</strong> de <strong>lo que pudo llegar a significar fuera del proceso</strong>. También obliga a mantener junto al fallo adverso las partes de la acusación AC/Fiscal que la propia Sentencia 163/2023 rechazó o estrechó, y a no convertirla en una exoneración judicial de CAM respecto de hechos que no fueron su objeto.</p>
      <p>La secuencia completa además el problema de circularidad ya documentado en esta página: denuncia DI 248 contra el perímetro AC/CAM → posición fiscal adversa en calificación → archivo DI 248 que invoca esa posición contra el denunciante → Sentencia 163/2023 → apelación → uso externo de esa sentencia durante el contraste periodístico del perímetro CAM/Meeting Point. Es una cuestión legítima de <strong>anclaje institucional, dependencia de trayectoria y asignación asimétrica de credibilidad</strong>; no es, por sí sola, prueba de coordinación personal entre los actores.</p>
      <h3>La pieza que falta</h3>
      <table class="ce-table"><thead><tr><th>Hipótesis</th><th>Estado actual</th></tr></thead><tbody>
        <tr><td>LPAM envió personalmente el archivo</td><td>ABIERTO · no hay cabecera nativa del mensaje entrante.</td></tr>
        <tr><td>El canal CAM/LPAM causó o procuró el suministro</td><td><strong>INFERENCIA FUERTE BASADA EN EVIDENCIA</strong> · llamada/hilo, espera hasta el lunes y recepción el lunes.</td></tr>
        <tr><td>Abogado/asesor/intermediario CAM fue el transmisor físico</td><td>ABIERTO · compatible con la cronología.</td></tr>
        <tr><td>El administrador concursal/Borja intervino en la transmisión o suministro</td><td>ABIERTO · actualmente sin puente documental directo.</td></tr>
        <tr><td>Fuente independiente no relacionada</td><td>POSIBLE · pero es una explicación principal más débil frente a la secuencia fechada disponible.</td></tr>
      </tbody></table>
      <p class="ce-open"><strong>Petición probatoria finita:</strong> mensaje entrante original a elEconomista con cabeceras completas; binario original de <em>AUTO CONCURSO CULPOSO.pdf</em>; hash y metadatos comparados con copias judiciales/AC/CAM/abogados; audios/WhatsApp/notas de Romera del 16–20 de enero; registros CAM/LPAM sobre la obtención y envío; cualquier comunicación que explique qué se dijo que la sentencia «probaba» y si se informó de los recursos.</p>
      <p><a href="../eleconomista-javier-romera-enero2025/">Ver la reconstrucción completa del episodio elEconomista →</a></p>
    </div>`;
  } else {
    sec.innerHTML = `<div class="shell record">
      <p class="eyebrow">CLASSIFICATION · EXTRA-PROCEDURAL USE · ELCONOMISTA · JANUARY 2025</p>
      <h2>Sentencia 163/2023 had at least two lives</h2>
      <p><strong>Inside Concurso 36/2012</strong>, it was a materially adverse, appealed first-instance judgment concerning the culpable classification of <strong>Luchy Playa Blanca, S.L.U. (LPB)</strong>, while rejecting or narrowing important parts of the insolvency administrator/Fiscal accusation package. <strong>Outside the insolvency</strong>, the 16–20 January 2025 sequence shows it operating as adverse judicial material while elEconomista was checking materially wider issues concerning Sun Park, CAM, Meeting Point/FTI, commercialisation and financing.</p>
      <div class="ce-dark"><strong>Controlled provenance conclusion.</strong><p>The technical identity of the physical sender remains open; <strong>the contextual provenance is no longer neutral</strong>. The dated sequence strongly supports that Sentencia 163/2023 was supplied or procured through the <strong>CAM/Acosta Matos response channel activated following Laura Patricia Acosta Matos's intervention</strong>. We do not yet state that LPAM personally pressed send, or that Borja Rodríguez-Batllori, a lawyer or another intermediary physically transmitted it: the native inbound message and headers are required for that.</p></div>
      <div class="ce-chain"><div class="ce-step"><strong>IA + Fiscal</strong><p>Adverse classification package.</p></div><div class="ce-step"><strong>Sentencia 163/2023 → appeal</strong><p>Adverse first-instance decision; appeals already filed before January 2025.</p></div><div class="ce-step"><strong>16–17 JAN 2025</strong><p>CAM/LPAM response channel; Romera confirms he was asked to wait until Monday for judicial orders.</p></div><div class="ce-step"><strong>20 JAN 2025</strong><p><em>AUTO CONCURSO CULPOSO.pdf</em> arrives; Romera says they cannot publish with this.</p></div></div>
      <div class="ce-grid">
        <article class="ce-card"><h3>Judgment, not order</h3><p>The operative document was Sentencia 163/2023. The filename/description as an “auto” must not replace its correct legal characterisation.</p></article>
        <article class="ce-card"><h3>LPB, not the whole Sun Park</h3><p>LPB was the debtor. The mixed-ownership hotel, other owners and extrainsolvency properties were not thereby classified as the debtor.</p></article>
        <article class="ce-card"><h3>First instance and appealed</h3><p>The judgment was adverse but appealed. What the source disclosed about appeal/finality remains an evidence question.</p></article>
        <article class="ce-card"><h3>Wider issues not adjudicated</h3><p>It did not itself decide whole-hotel title, Matkator rights, 2018 material control, Meeting Point/Club Sei authority, RIC/RICPE, incentives or FEDER.</p></article>
        <article class="ce-card"><h3>No retrospective authority</h3><p>A 2023 judgment against Gil/LPB cannot retrospectively create legal authority for specific disputed 2018 control/access/commercialisation acts.</p></article>
        <article class="ce-card"><h3>Documented consequence</h3><p>After receipt, Romera communicated that the newsroom could not publish with that material. That consequence can be documented without asserting unlawful censorship.</p></article>
      </div>
      <p>The episode reinforces the need to distinguish <strong>what the judgment decided</strong> from <strong>what it came to mean outside the proceeding</strong>. It also extends the documented path-dependence question: DI 248 complaint against the IA/CAM perimeter → adverse Fiscal classification position → DI 248 archive invokes that position → Sentencia 163/2023 → appeal → external use during CAM/Meeting Point verification. This supports an institutional anchoring/asymmetric-credibility inquiry, not a finding of personal coordination.</p>
      <p class="ce-open"><strong>Finite evidence request:</strong> original inbound message and full headers; native judicial PDF and hash comparison; 16–20 January WhatsApp/audio/newsroom notes; CAM/LPAM records concerning sourcing/transmission; any lawyer/IA intermediary chain; and any communication describing what the judgment was said to prove or disclosing its appeal status.</p>
      <p><a href="../eleconomista-javier-romera-january2025/">See the full elEconomista reconstruction →</a></p>
    </div>`;
  }

  const main = document.querySelector('main');
  if (!main) return;
  const footer = main.querySelector('footer');
  if (footer) main.insertBefore(sec, footer); else main.appendChild(sec);
})();
