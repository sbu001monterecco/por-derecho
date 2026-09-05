(() => {
  'use strict';
  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  const es = path.endsWith('/es/reclamacion-caixabank-valencia/');
  const en = path.endsWith('/en/caixabank-valencia-claim/');
  if (!es && !en) return;
  if (document.getElementById('caixabank-lawyer-dataroom-unitary')) return;

  const injectStyles = () => {
    if (document.getElementById('caixabank-lawyer-dataroom-style')) return;
    const style = document.createElement('style');
    style.id = 'caixabank-lawyer-dataroom-style';
    style.textContent = `
      #caixabank-lawyer-dataroom-unitary .pd-room-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem}
      #caixabank-lawyer-dataroom-unitary .pd-room-card{background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:14px;padding:1rem}
      #caixabank-lawyer-dataroom-unitary .pd-room-card h3{margin-top:.15rem}
      #caixabank-lawyer-dataroom-unitary .pd-flow{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.8rem;align-items:stretch}
      #caixabank-lawyer-dataroom-unitary .pd-flow article{background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:12px;padding:.9rem}
      #caixabank-lawyer-dataroom-unitary .pd-source{width:100%;border-collapse:collapse}
      #caixabank-lawyer-dataroom-unitary .pd-source th,#caixabank-lawyer-dataroom-unitary .pd-source td{padding:.7rem;border-bottom:1px solid rgba(19,37,45,.14);text-align:left;vertical-align:top}
      #caixabank-lawyer-dataroom-unitary .pd-criminal{border-left:6px solid #8c2f2c;background:#fff4f3;padding:1rem 1.2rem;border-radius:0 12px 12px 0}
      #caixabank-lawyer-dataroom-unitary .pd-readfirst{background:#13252d;color:#fff;padding:1.15rem 1.25rem;border-radius:14px}
      #caixabank-lawyer-dataroom-unitary .pd-readfirst a{color:#fff;text-decoration:underline}
      @media(max-width:760px){#caixabank-lawyer-dataroom-unitary .pd-room-grid,#caixabank-lawyer-dataroom-unitary .pd-flow{grid-template-columns:1fr}}
    `;
    document.head.appendChild(style);
  };

  const mount = () => {
    if (document.getElementById('caixabank-lawyer-dataroom-unitary')) return;
    const main = document.querySelector('main');
    if (!main) return;
    injectStyles();

    const section = document.createElement('section');
    section.className = 'section';
    section.id = 'caixabank-lawyer-dataroom-unitary';

    if (es) {
      section.innerHTML = `
        <div class="shell record">
          <div class="section-head"><div><p class="kicker">ANTES DE CONTACTAR · SALA DOCUMENTAL PARA ABOGADOS</p><h2>Lee la demanda, la defensa y el contexto que convierte Valencia en algo mucho más amplio que un producto financiero.</h2></div><p>El objetivo es que una primera llamada empiece en estrategia y prueba, no reconstruyendo doce años de expediente.</p></div>
          <div class="pd-readfirst"><strong>Acceso abierto para profesionales.</strong> Hemos localizado la demanda de octubre de 2023, la contestación de CaixaBank de enero de 2024, el bundle de defensa, la pericial PKF de octubre de 2024, el escrito del AC de enero de 2021, su negativa de septiembre de 2023 y el expediente OB REM 2018–2019. Los lectores públicos distinguen escrito de parte, documento, alegación, hipótesis y prueba pendiente.</div>
          <div class="pd-room-grid" style="margin-top:1rem">
            <article class="pd-room-card"><p class="kicker">1 · FUENTES</p><h3>Demanda + contestación + pericial + AC</h3><p>Qué reclama Aweswell, qué opone CaixaBank y qué material del Administrador Concursal utiliza la defensa.</p><p><a class="button" href="documentos/">Abrir sala documental →</a></p></article>
            <article class="pd-room-card"><p class="kicker">2 · FAQ</p><h3>¿Por qué 2023? ¿Por qué importa tanto?</h3><p>Legitimación subsidiaria, retraso 2021–2023, cuantía, split-credit, testifical de Borja y qué tendría que probar una hipótesis de coordinación.</p><p><a class="button" href="faq-contexto-unitario/">Abrir FAQ unitario →</a></p></article>
            <article class="pd-room-card"><p class="kicker">3 · OB REM</p><h3>AC + CAM · 28-Nov-2018</h3><p>Una vinculación que describía el préstamo como uno solo fue extinguida en una operación de venta directa al mismo perímetro acreedor.</p><p><a class="button" href="ob-rem-ac-cam-28nov2018/">Abrir reconstrucción visual →</a></p></article>
          </div>

          <h3 style="margin-top:1.4rem">Visual unitario: paquete integrado → rutas separadas → reencuentro procesal</h3>
          <div class="pd-flow">
            <article><strong>2008–2010 · paquete</strong><p>Hipoteca 8,6 M€ + suelo + swap 5 M€ + refinanciación + 850.000 € + prenda 405.000 € + cuentas.</p></article>
            <article><strong>2011–2012 · ruptura</strong><p>Liquidaciones, imputaciones, supuesta mora, ejecución Bankia y Concurso 36/2012.</p></article>
            <article><strong>Después · split</strong><p><strong>Responsabilidad:</strong> Bankia→CaixaBank.<br><strong>Activo/crédito:</strong> Bankia→SAREB→PH122→CAM.</p></article>
          </div>
          <div class="pd-flow" style="margin-top:.8rem">
            <article><strong>Compuertas AC</strong><p>Representación, acción Bankia, disclosure, valoración, OB REM, liquidación, cuentas.</p></article>
            <article><strong>CAM / Acosta Matos</strong><p>Crédito → posición acreedora → compra/control → dación/título → HNT/MYND.</p></article>
            <article><strong>Valencia 2023–2027</strong><p>CaixaBank defiende la rama bancaria utilizando material del concurso/AC y pide al AC como testigo.</p></article>
          </div>

          <h3 style="margin-top:1.4rem">No es sólo similitud de lenguaje: es procedencia de la defensa</h3>
          <div class="table-wrap"><table class="pd-source"><thead><tr><th>Defensa CaixaBank</th><th>Fuente del concurso / AC</th><th>Qué debe aclararse bajo prueba</th></tr></thead><tbody>
            <tr><td>Legitimación de Aweswell.</td><td>Informe AC 2013 / tratamiento de crédito.</td><td>Qué documentación existía, qué cambió y qué material utilizó CaixaBank.</td></tr>
            <tr><td>Firmeza/preclusión del swap.</td><td>Textos concursales / reconocimiento del crédito.</td><td>Cómo se concilia con que el AC aceptara una acción contra Bankia en 2021.</td></tr>
            <tr><td>Exceso de la demanda 2023.</td><td>Escrito AC 25-Ene-2021 (~596.123,75 €).</td><td>Quién definió alcance, por qué no se presentó y qué cambió hasta 2023.</td></tr>
            <tr><td>Borja como testigo material.</td><td>CaixaBank pidió su testifical; Aweswell se adhirió.</td><td>Qué espera acreditar CaixaBank y cuál es la procedencia de ese conocimiento.</td></tr>
          </tbody></table></div>

          <div class="pd-criminal" style="margin-top:1rem"><p class="kicker">ALEGACIÓN DE POR DERECHO · CRIMINAL-FIRST · NO HALLAZGO JUDICIAL</p><strong>Hipótesis de agente funcional / compuerta habilitante.</strong> Por Derecho alega que el Administrador Concursal instrumentalizó deslealmente su cargo y actuó funcionalmente en beneficio del perímetro CAM/Acosta Matos y en detrimento de LPB y su perímetro. La publicación no convierte esa hipótesis en hecho: exige probar deber/poder, conocimiento, acto u omisión, dolo cuando corresponda, causalidad, daño, beneficio y cualquier instrucción o concertación necesaria. <a href="faq-contexto-unitario/">Ver test penal y prueba P0 →</a></div>

          <p class="linkrow" style="margin-top:1rem"><a class="button secondary" href="../administrador-concursal-puerta-credito-titulo/">AC · crédito→título</a><a class="button secondary" href="../acreedor-de-registro/responsabilidad/">Cadena acreedora</a><a class="button secondary" href="../acosta-matos-perimetro/">Acosta Matos</a><a class="button secondary" href="../ingenieria-inversa-criminal-unitaria/">Criminal unitario</a><a class="button secondary" href="../adjudicacion-2022-reconstruccion-documental/">Adjudicación 2022</a></p>
        </div>`;
    } else {
      section.innerHTML = `
        <div class="shell record">
          <div class="section-head"><div><p class="kicker">READ BEFORE CONTACTING · LAWYER DATA ROOM</p><h2>Read the claim, CaixaBank's defence and the wider context before deciding whether to speak with us.</h2></div><p>The aim is for a first call to start with evidence and strategy, not twelve years of reconstruction.</p></div>
          <div class="pd-readfirst"><strong>Open professional reading.</strong> We have located the October 2023 claim, January 2024 CaixaBank defence and defence exhibits, October 2024 PKF report, the Administrator's January 2021 court filing, his September 2023 refusal and the 2018–2019 OB REM record. English pages provide translated legal summaries; Spanish originals/control materials remain authoritative.</div>
          <div class="pd-room-grid" style="margin-top:1rem">
            <article class="pd-room-card"><p class="kicker">1 · SOURCES</p><h3>Claim + defence + expert + Administrator</h3><p>What Aweswell claims, what CaixaBank says and which insolvency/Administrator sources the defence relies on.</p><p><a class="button" href="documents/">Open document room →</a></p></article>
            <article class="pd-room-card"><p class="kicker">2 · FAQ</p><h3>Why 2023? Why does this matter?</h3><p>Delay, subsidiary standing, quantum, split-credit theory, Borja's testimony and the evidence required for any coordination theory.</p><p><a class="button" href="faq-unitary-context/">Open unitary FAQ →</a></p></article>
            <article class="pd-room-card"><p class="kicker">3 · OB REM</p><h3>Administrator + CAM · 28-Nov-2018</h3><p>An integrated mortgage/property link was extinguished in a direct transaction with the creditor perimeter.</p><p><a class="button" href="ob-rem-ac-cam-28nov2018/">Open visual reconstruction →</a></p></article>
          </div>

          <h3 style="margin-top:1.4rem">Unitary visual: integrated package → split paths → procedural reconvergence</h3>
          <div class="pd-flow"><article><strong>2008–2010 package</strong><p>€8.6m mortgage + floor + €5m swap + refinancing + €850k facility + €405k pledge + accounts.</p></article><article><strong>2011–2012 break</strong><p>Settlements, allocations, alleged arrears, Bankia enforcement and LPB insolvency.</p></article><article><strong>Later split</strong><p><strong>Responsibility:</strong> Bankia→CaixaBank.<br><strong>Asset/credit:</strong> Bankia→SAREB→PH122→CAM.</p></article></div>
          <div class="pd-flow" style="margin-top:.8rem"><article><strong>Administrator gateways</strong><p>Representation, Bankia action, disclosure, valuation, OB REM, liquidation, accounts.</p></article><article><strong>CAM / Acosta Matos</strong><p>Credit → creditor position → acquisition/control → credit-to-title → HNT/MYND.</p></article><article><strong>Valencia 2023–2027</strong><p>CaixaBank defends the upstream banking route using insolvency/Administrator material and requested the Administrator as witness.</p></article></div>

          <div class="pd-criminal" style="margin-top:1rem"><p class="kicker">POR DERECHO ALLEGATION · CRIMINAL-FIRST · NOT A JUDICIAL FINDING</p><strong>Functional-agent / enabling-gatekeeper hypothesis.</strong> Por Derecho alleges that the Insolvency Administrator disloyally instrumentalised his office in a way that functionally benefited the CAM/Acosta Matos perimeter and harmed LPB and its perimeter. This is an investigative allegation, not a finding; it requires actor-specific proof of power/duty, knowledge, act/omission, intent where required, causation, loss, benefit and any necessary instruction/concert. <a href="faq-unitary-context/">Read the evidential test →</a></div>

          <p class="linkrow" style="margin-top:1rem"><a class="button secondary" href="../../es/reclamacion-caixabank-valencia/documentos/" lang="es">Spanish source room</a><a class="button secondary" href="../lender-of-record/">Lender chain</a><a class="button secondary" href="../lpb-insolvency/">LPB insolvency</a></p>
        </div>`;
    }

    const outreach = document.getElementById('caixabank-adr-settlement-outreach');
    const hero = main.querySelector('.hero');
    if (outreach) outreach.insertAdjacentElement('afterend', section);
    else if (hero) hero.insertAdjacentElement('afterend', section);
    else main.prepend(section);
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount, {once:true});
  else mount();
})();
