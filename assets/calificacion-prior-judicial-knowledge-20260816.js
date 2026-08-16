(() => {
  const path = window.location.pathname.replace(/\/+$/, '/');
  const routes = {
    esMain: '/por-derecho/es/calificacion-concurso-36-2012-vidas-paralelas/',
    enMain: '/por-derecho/en/insolvency-classification-parallel-lives/',
    esDetail: '/por-derecho/es/calificacion-concurso-36-2012-vidas-paralelas/conocimiento-previo-rescate/',
    enDetail: '/por-derecho/en/insolvency-classification-parallel-lives/prior-judicial-knowledge-rescue/'
  };
  const isEsMain = path === routes.esMain;
  const isEnMain = path === routes.enMain;
  const isEsDetail = path === routes.esDetail;
  const isEnDetail = path === routes.enDetail;
  if (!isEsMain && !isEnMain && !isEsDetail && !isEnDetail) return;

  const replaceText = (root, replacements) => {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach((node) => {
      let next = node.nodeValue;
      replacements.forEach(([from, to]) => {
        next = next.split(from).join(to);
      });
      if (next !== node.nodeValue) node.nodeValue = next;
    });
  };

  if (isEsDetail || isEnDetail) {
    const main = document.querySelector('main');
    const hero = document.querySelector('main .hero');
    if (!main || !hero) return;

    if (isEsDetail) {
      replaceText(main, [
        ['salida financiada', 'salida estructurada y financiable'],
        ['vía financiada', 'vía estructurada y financiable'],
        ['estrategia financiada', 'estrategia estructurada y financiable']
      ]);
      const lead = hero.querySelector('.lead');
      if (lead) {
        lead.innerHTML = 'Qué estaba formalmente ante el órgano judicial, qué fue comunicado personalmente según dos registros profesionales contemporáneos y qué sigue sin probarse sobre la presentación formal, la certificación de deuda y la respuesta procesal.';
      }
    } else {
      replaceText(main, [
        ['financed exit', 'structured, financeable exit'],
        ['financed route', 'structured, financeable route'],
        ['funded rescue/conclusion strategy', 'structured, financeable rescue/conclusion strategy']
      ]);
      const lead = hero.querySelector('.lead');
      if (lead) {
        lead.innerHTML = 'What was formally before the court institution, what two contemporaneous professional records say was put personally to the judge, and what remains unproved about formal filing, debt certification and procedural treatment.';
      }
    }

    if (document.getElementById('june2018-source-refresh')) return;
    const section = document.createElement('section');
    section.id = 'june2018-source-refresh';
    section.className = 'section alt';

    if (isEsDetail) {
      section.innerHTML = `
        <div class="shell record">
          <p class="eyebrow">ACTUALIZACIÓN PROBATORIA · 12–26 JUNIO 2018</p>
          <h2>El plan y el aviso contemporáneo están documentados; la presentación formal todavía no</h2>
          <div class="evidence-note dark">
            <strong>Corrección de vocabulario.</strong>
            <p>La estructura debe describirse como <strong>concreta, condicionada y financiable</strong>, no como préstamo ejecutado o fondos incondicionalmente disponibles. El term sheet revisado contemplaba hasta €15,5 millones —€13,84 millones para deuda concursal y posterior—, pero conservaba condiciones materiales y casillas de firma en blanco.</p>
          </div>
          <div class="bridge-flow" aria-label="Secuencia probatoria junio 2018">
            <div class="bridge-step"><time>13 JUN</time><strong>Relato directo de Irigoyen</strong><p>Su correo profesional de esa misma noche describe la reunión, la coordinación de fondo, socio/sociedad y operador, la conclusión pagando y una respuesta judicial sustantiva. Es un relato contemporáneo, no un acta.</p></div>
            <div class="bridge-step"><time>13 JUN</time><strong>Corroboración de Carlos Sanz</strong><p>Tras hablar con Irigoyen, comunicó separadamente la visita al Juzgado, la oportunidad de concluir, la urgencia y el siguiente escrito. Corrobora la reunión y su núcleo, no las palabras exactas del juez.</p></div>
            <div class="bridge-step"><time>14–15 JUN</time><strong>Ruta en curso, todavía informal</strong><p>Juan Tomás informó que la consignación del pasivo seguía su curso y, al día siguiente, que la conclusión pagando se estaba trasladando informalmente al Juzgado.</p></div>
            <div class="bridge-step"><time>26 JUN</time><strong>Freno judicial protector</strong><p>El Juzgado suspendió la realización de determinadas fincas por el posible efecto del recurso. Es contraprueba obligatoria frente a una lectura de dirección única.</p></div>
          </div>
          <div class="evidence-note">
            <strong>El adjunto no era un escrito presentado.</strong>
            <p><em>Esquema Escrito para proceder a la conclusión del concurso.docx</em> era una hoja con campos en blanco que proponía cartas de confort, contratos, garantías y que la AC certificara exactamente la deuda. No lleva firma, sello ni acuse LexNET en la copia revisada.</p>
          </div>
          <div class="evidence-note">
            <strong>Extremo expresamente excluido por ahora.</strong>
            <p>Un correo posterior de parte afirmó que el juez pidió un informe pericial y concedió hasta 25 días. Ese detalle no aparece como exigencia en el relato completo de Irigoyen ni se ha localizado en una resolución firmada. No se publica como hecho judicial probado.</p>
          </div>
          <div class="status-strip">
            <div><strong>Probado</strong><span>Plan estructurado, term sheet condicional, dos comunicaciones contemporáneas y continuidad 14–15 junio.</span></div>
            <div><strong>Abierto</strong><span>Acuse LexNET, asiento, proveído, certificado actualizado de deuda, depósito/garantía y decisión sobre conclusión.</span></div>
            <div><strong>Apelación</strong><span>AP Las Palmas · Sección 4ª · RPL 2523/2025. Sin sentencia terminativa localizada en Gmail controlado hasta 16-08-2026.</span></div>
          </div>
          <p class="small"><strong>Regla:</strong> comunicación informal no equivale a incorporación formal; un borrador no equivale a escrito presentado; y la existencia de documentación comercial no prueba que el magistrado leyera cada anexo.</p>
        </div>`;
    } else {
      section.innerHTML = `
        <div class="shell record">
          <p class="eyebrow">EVIDENCE UPDATE · 12–26 JUNE 2018</p>
          <h2>The plan and contemporaneous notice are evidenced; formal filing is not yet proved</h2>
          <div class="evidence-note dark">
            <strong>Vocabulary correction.</strong>
            <p>The structure should be described as <strong>concrete, conditional and financeable</strong>, not as an executed loan or unconditionally available funds. The reviewed term sheet contemplated up to €15.5 million —€13.84 million for insolvency and post-petition debt— but retained material conditions and blank signature boxes.</p>
          </div>
          <div class="bridge-flow" aria-label="June 2018 evidence sequence">
            <div class="bridge-step"><time>13 JUN</time><strong>Irigoyen's direct account</strong><p>His same-night professional email describes the meeting, coordination of fund, shareholder/company and operator, conclusion by payment and a substantive reported judicial response. It is a contemporaneous account, not a court minute.</p></div>
            <div class="bridge-step"><time>13 JUN</time><strong>Carlos Sanz corroboration</strong><p>After speaking with Irigoyen, he separately reported the court visit, the opportunity to conclude, urgency and the next proposed application. It corroborates the meeting and core strategy, not the judge's exact words.</p></div>
            <div class="bridge-step"><time>14–15 JUN</time><strong>Route continuing, still informal</strong><p>Juan Tomás reported that consignation of the liabilities remained in progress and, the next day, that conclusion by payment was being communicated to the court informally.</p></div>
            <div class="bridge-step"><time>26 JUN</time><strong>Protective judicial brake</strong><p>The court suspended realization of specified properties because of the appeal's potential effect. This is mandatory counterevidence against a one-direction account.</p></div>
          </div>
          <div class="evidence-note">
            <strong>The attachment was not a filed pleading.</strong>
            <p><em>Esquema Escrito para proceder a la conclusión del concurso.docx</em> was a one-page outline with blanks, proposing comfort letters, contracts, security and an exact AC debt certificate. The reviewed copy has no signature, stamp or LexNET acknowledgement.</p>
          </div>
          <div class="evidence-note">
            <strong>Expressly excluded for now.</strong>
            <p>A later party email said the judge requested an expert report and allowed up to 25 days. That detail is not recorded as a requirement in Irigoyen's full account and no signed judicial act has been located. It is not published as proved judicial fact.</p>
          </div>
          <div class="status-strip">
            <div><strong>Evidenced</strong><span>Structured plan, conditional term sheet, two contemporaneous communications and 14–15 June continuation.</span></div>
            <div><strong>Open</strong><span>LexNET receipt, docket entry, order, updated debt certificate, deposit/security and conclusion disposition.</span></div>
            <div><strong>Appeal</strong><span>Las Palmas Provincial Court · Section 4 · RPL 2523/2025. No terminating appellate ruling located in controlled Gmail through 16 Aug 2026.</span></div>
          </div>
          <p class="small"><strong>Rule:</strong> informal notice is not formal incorporation; a draft is not a filed pleading; and commercial documents do not prove the judge personally read every annex.</p>
        </div>`;
    }

    hero.insertAdjacentElement('afterend', section);
    return;
  }

  if (document.getElementById('prior-judicial-knowledge-rescue-link')) return;
  const hero = document.querySelector('main .hero');
  if (!hero) return;

  const section = document.createElement('section');
  section.id = 'prior-judicial-knowledge-rescue-link';
  section.className = 'section alt';

  if (isEsMain) {
    section.innerHTML = `
      <div class="shell record">
        <p class="eyebrow">CAPA PROBATORIA ACTUALIZADA · QUÉ SABÍA EL JUZGADO</p>
        <h2>Antes de la Sentencia 163/2023 existía un historial documentado de viabilidad, pago, operación y defensa de LPB</h2>
        <p>Un acuse LexNET prueba que el 27 de abril de 2017 entraron en el Concurso 36/2012 una propuesta de convenio, un plan de viabilidad y un plan de pagos. Dos comunicaciones profesionales independientes del 13 de junio de 2018 documentan contemporáneamente la reunión judicial y el núcleo de una vía estructurada y financiable para pagar el pasivo, coordinar un fondo y un operador, preservar la explotación y devolver autonomía a LPB.</p>
        <p>La precisión importa: el term sheet era condicional y la copia revisada no estaba firmada; el adjunto del 13 de junio era un esquema con campos en blanco; y el 15 de junio otro abogado describía la conclusión pagando como comunicación informal al Juzgado. El acuse formal, el certificado actualizado de deuda, el depósito o garantía y la respuesta procesal siguen abiertos.</p>
        <p>El Auto de 26 de junio de 2018 suspendió la realización de determinadas fincas y permanece como contraprueba frente a cualquier relato de dirección judicial única.</p>
        <p><strong>Esta capa no declara probado ningún delito.</strong> Obliga a contrastar cada fundamento adverso con el conocimiento formal, el aviso personal reportado, la prueba contraria y una explicación judicial razonable.</p>
        <p class="linkrow"><a class="button" href="./conocimiento-previo-rescate/">Ver la cronología, las dos comunicaciones y la matriz de límites →</a></p>
      </div>`;
  } else {
    section.innerHTML = `
      <div class="shell record">
        <p class="eyebrow">UPDATED EVIDENCE LAYER · WHAT THE COURT KNEW</p>
        <h2>Before Judgment 163/2023 there was a documented LPB viability, payment, operation and defence history</h2>
        <p>A LexNET acknowledgement proves that on 27 April 2017 a composition proposal, viability plan and payment plan entered Insolvency 36/2012. Two independent professional communications dated 13 June 2018 contemporaneously document the judicial meeting and the core of a structured, financeable route to pay the liabilities, coordinate a fund and operator, preserve hotel operation and restore LPB's autonomy.</p>
        <p>The qualification matters: the term sheet was conditional and the reviewed copy was unsigned; the 13 June attachment was an outline with blank fields; and on 15 June another lawyer described conclusion by payment as being communicated to the court informally. The formal receipt, updated debt certificate, deposit/security and procedural response remain open.</p>
        <p>The 26 June 2018 order suspended realization of specified properties and remains counterevidence against any one-direction judicial account.</p>
        <p><strong>This evidence layer does not declare any offence proved.</strong> It requires each adverse ground to be tested against formal knowledge, reported personal notice, contrary evidence and a reasonable judicial explanation.</p>
        <p class="linkrow"><a class="button" href="./prior-judicial-knowledge-rescue/">See the chronology, both communications and the limitations matrix →</a></p>
      </div>`;
  }

  hero.insertAdjacentElement('afterend', section);
})();