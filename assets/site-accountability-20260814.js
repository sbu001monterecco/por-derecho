(() => {
  const current = document.currentScript;

  // Preserve the established site behaviour, but do not make the new accountability
  // material depend on the legacy bundle loading successfully.
  if (current) {
    const legacy = document.createElement('script');
    legacy.src = new URL('site-base-1728fcf.js?v=20260812b', current.src).href;
    legacy.defer = true;
    document.head.appendChild(legacy);
  }

  const asset = (path) => current ? new URL(path, current.src).href : `../assets/${path}`;

  function portrait(url, alt) {
    return `<img src="${url}" alt="${alt}" loading="lazy" style="width:132px;height:158px;object-fit:cover;border-radius:14px;display:block;margin:0 0 1rem;border:1px solid rgba(19,37,45,.18)">`;
  }

  function render() {
    const isSpanish = document.documentElement.lang === 'es';
    const pageText = (document.body && document.body.textContent) || '';
    const relevantPage = /LPB|Luchy Playa Blanca|Sun Park|MYND|HNT|CEXP|concurso|concursal|insolvenc|insolvency|administrator|administrador/i.test(pageText);
    const commonShell = document.querySelector(isSpanish ? '#recuperacion .shell' : '#recovery .shell') || document.querySelector('main .section .shell');

    if (relevantPage && !document.getElementById('limited-concurso') && commonShell && !document.getElementById('lpb-concurso-overreach-note')) {
      const note = document.createElement('article');
      note.id = 'lpb-concurso-overreach-note';
      note.className = 'thesis-block';
      note.style.marginTop = '2rem';
      note.innerHTML = isSpanish ? `
        <h2>Concurso LPB*: procedimiento limitado, desbordamiento alegado</h2>
        <p>Un concurso limitado de LPB fue utilizado repetidamente, o se permitió que fuera utilizado, como si diera autoridad sobre todo el hotel, todo el perímetro de propiedad, la capa CEXP/explotación, las unidades de Matkator y terceros, las obras, la financiación y la explotación hotelera posterior.</p>
        <p>En este sitio, "concurso LPB" significa Luchy Playa Blanca, S.L.U. y la masa del Concurso 36/2012. La causa bancaria alegada explica por qué se presentó la solicitud defensiva; no absuelve a actores posteriores que usaron, ampliaron, financiaron, certificaron, explotaron o se beneficiaron de una lectura desbordada de ese procedimiento.</p>
        <p><a class="text-link" href="/por-derecho/es/acreedor-de-registro/">Ver la página Acreedor de Registro</a></p>
      ` : `
        <h2>LPB concurso*: limited proceeding, alleged overreach</h2>
        <p>A limited LPB concurso was repeatedly used, or allowed to be used, as if it were authority over the whole hotel, the whole ownership perimeter, the CEXP/exploitation layer, Matkator/third-party units, works, finance and later hotel operation.</p>
        <p>On this site, "LPB concurso" means Luchy Playa Blanca, S.L.U. and the estate in Concurso 36/2012. The alleged banking trigger explains why the defensive filing was made; it does not absolve later actors who used, expanded, financed, certified, operated or benefited from an overextended reading of that proceeding.</p>
        <p><a class="text-link" href="/por-derecho/en/lender-of-record/">Open the Lender of Record page</a></p>
      `;

      const anchor = commonShell.querySelector(isSpanish ? '#tesis' : '#thesis') || commonShell.querySelector('.section-head') || commonShell.firstElementChild;
      if (anchor && anchor.insertAdjacentElement) anchor.insertAdjacentElement('afterend', note);
      else commonShell.insertBefore(note, commonShell.firstChild);
    }

    if (!isSpanish) return;
    const recovery = document.querySelector('#recuperacion .shell');
    if (!recovery) return;

    // 1) Put the FMMM portrait into the existing private-actor card.
    document.querySelectorAll('.actor-grid article').forEach((card) => {
      const strong = card.querySelector('strong');
      if (strong && strong.textContent.includes('Francisco Mario Matos Matas') && !card.querySelector('img[data-portrait="fmmm"]')) {
        const img = document.createElement('img');
        img.src = asset('actors/francisco-mario-matos-matas.jpg');
        img.alt = 'Retrato utilizado para Francisco Mario Matos Matas, identificación confirmada por el titular del expediente';
        img.loading = 'lazy';
        img.dataset.portrait = 'fmmm';
        img.style.cssText = 'width:104px;height:128px;object-fit:cover;border-radius:12px;margin:0 0 .9rem;border:1px solid rgba(19,37,45,.18)';
        card.prepend(img);
      }
    });

    // 2) Re-open the origin of the insolvency without naming the current bank defendant fully.
    if (!document.getElementById('preconcurso-origin-12aug')) {
      const origin = document.createElement('article');
      origin.id = 'preconcurso-origin-12aug';
      origin.className = 'thesis-block';
      origin.style.marginTop = '2rem';
      origin.innerHTML = `
        <div>
          <span class="evidence-badge allegation-badge">Origen del concurso · cuestión reabierta</span>
          <h3>¿Y si el concurso voluntario nació sobre una premisa bancaria incompleta o errónea?</h3>
          <p>La historia no empieza con el concurso ni con Acosta Matos. La documentación contractual, contable y procesal hoy utilizada en un procedimiento civil en Valencia contra la sucesora de la entidad bancaria de 2011–2012 obliga a revisar el supuesto punto de partida. Gil Marer y Aweswell sostienen que la relación financiera de LPB fue tratada como morosa antes de que existiera una base correcta y completa para hacerlo, y que la posterior ejecución y amenaza de subasta descansaron sobre esa misma premisa controvertida.</p>
          <p>Entre los datos que deben reconciliarse figuran una carencia contractual que alcanzaba el final de 2011, el cierre de la cuenta en diciembre de 2011, el inicio de amortización previsto para enero de 2012 y la promoción de ejecución hipotecaria en enero de 2012. El litigio civil actualmente en curso ante el Juzgado de Primera Instancia nº 27 de Valencia, Procedimiento Ordinario 1859/2023-9, examina parte de ese paquete financiero y sus consecuencias. Esta web no anticipa el resultado.</p>
          <p>Aweswell adquirió la posición societaria de LPB a finales de 2011. Ante la ejecución y el riesgo de subasta, LPB solicitó concurso voluntario en junio de 2012. Gil Marer sostiene hoy que el consejo de utilizar el concurso como escudo frente a aquella ejecución fue, visto el expediente completo, equivocado, negligente o basado en información insuficiente. <b>Si el supuesto impago que precipitó la maquinaria concursal estaba mal caracterizado, el origen causal del Concurso 36/2012 también debe ser revisado.</b></p>
        </div>
        <div class="proof-split"><div><strong>Documentado</strong><span>Adquisición societaria a finales de 2011; ejecución bancaria en enero de 2012; concurso voluntario en junio de 2012; litigio posterior en Valencia.</span></div><div><strong>Controvertido</strong><span>Morosidad exigible, cálculo financiero correcto, causalidad con el concurso y responsabilidad bancaria o profesional.</span></div></div>`;
      const thesis = recovery.querySelector('#tesis');
      (thesis || recovery.firstElementChild).insertAdjacentElement('afterend', origin);
    }

    // 3) Make the AC and judge visually unavoidable and legally differentiated.
    if (!document.getElementById('institutional-accountability-12aug')) {
      const section = document.createElement('section');
      section.id = 'institutional-accountability-12aug';
      section.style.marginTop = '2.25rem';
      section.innerHTML = `
        <div class="section-head"><div><p class="kicker">Dos niveles institucionales · una cadena causal</p><h2>Administrador Concursal y tutela judicial efectiva</h2></div><p>La alegación distingue las funciones. El Administrador Concursal era gatekeeper de LPB; el Juzgado ejercía la tutela y supervisión del concurso. Ninguna de esas funciones convertía por sí sola en masa concursal los derechos propios o residuales de CEXP, Matkator o terceros.</p></div>
        <div class="grid-2">
          <article class="path-card primary">
            ${portrait(asset('actors/francisco-de-borja-rodriguez-batllori.jpg'),'Retrato profesional del Administrador Concursal Francisco de Borja Rodríguez-Batllori Laffitte')}
            <span class="number">Administrador Concursal · gatekeeper</span>
            <h3>Francisco de Borja Rodríguez-Batllori Laffitte</h3>
            <p>Su relevancia no depende de haber ejecutado personalmente cada acto privado. Depende de qué verificó, autorizó, transmitió, toleró, informó, preservó o intentó revertir mientras administraba la masa de LPB.</p>
            <p>En 2018 consta una secuencia documental sobre claves, acceso, mantenimiento y vigilancia. Gil Marer sostuvo contemporáneamente que esas funciones y la explotación correspondían a CEXP y pidió verificar estatutos, libros, cuentas, contratos y deuda. Esa era su posición de parte: el Auto 804/2018 no reconoció a CEXP el derecho posesorio actual invocado. La declaración judicial de 31 de julio de 2018 añade cuestiones sobre autorizaciones de acceso, puerta forzada y cerraduras.</p>
            <p><b>Pregunta de rendición de cuentas:</b> una vez advertida la separación entre LPB, CEXP, Comunidad de Propietarios y terceros, ¿qué medida concreta protegió cada perímetro y qué restitución, inspección, reclamación de frutos o cuantificación de daños se produjo?</p>
            <p class="source-policy">Gil Marer ha formulado alegaciones civiles, concursales y penales sobre esta conducta. No existe condena ni declaración firme de responsabilidad criminal.</p>
          </article>
          <article class="path-card">
            ${portrait(asset('actors/alberto-lopez-villarrubia.jpg'),'Retrato utilizado para el Magistrado D. Alberto López Villarrubia, identificación confirmada por el titular del expediente')}
            <span class="number">Tutela judicial efectiva · acción y omisión</span>
            <h3>Alberto López Villarrubia</h3>
            <p>Gil Marer sostiene que el problema no se reduce a resoluciones desfavorables: consiste en si la tutela concursal protegió realmente el activo, la unidad productiva y los límites del procedimiento cuando hechos externos estaban alterando control, posesión, acceso, obras, valor y competencia.</p>
            <p>El test público es: <b>conocimiento → competencia → remedio disponible → decisión u omisión → efecto</b>. Deben reconciliarse el funded exit de 2018, la pérdida de control material, OB REM y su no convalidación, las demoliciones y restricciones de acceso denunciadas, la inspección/pericial solicitada, la competencia por el activo y la adjudicación de 2022.</p>
            <p><b>Sobre el alcance:</b> una resolución sobre LPB no podía por mera irradiación práctica crear título sobre Matkator, decidir por sí sola qué autoridad residual conservaba CEXP ni convertir posesión de facto en propiedad. Si produjo efectos sobre esos planos, debe identificarse el puente jurídico individualizado.</p>
            <p class="source-policy">Gil Marer sostiene que determinados hechos y resoluciones superan el umbral de indicios que justifica investigación penal. Es una alegación formalmente planteada, no una declaración de culpabilidad.</p>
          </article>
        </div>
        <div class="pressure-maxim" style="margin-top:1.25rem"><strong>Acción y omisión pueden ser jurídicamente distintas y causalmente convergentes.</strong><span>La cuestión es si una actuación positiva o la negativa a ejercer una medida protectora disponible permitió que el mismo estado de cosas se consolidara, afectara a la masa y se proyectara sobre derechos situados fuera del concurso.</span></div>`;
      const actorPolicy = recovery.querySelector('.actor-policy');
      const actorGrid = recovery.querySelector('.actor-grid');
      (actorPolicy || actorGrid || recovery.lastElementChild).insertAdjacentElement('afterend', section);
    }

    // 4) Make the 2018 -> RIC -> 2022 -> MYND continuity and the harm easy to read.
    if (!document.getElementById('continuity-harm-12aug')) {
      const block = document.createElement('article');
      block.id = 'continuity-harm-12aug';
      block.className = 'forensic-chain';
      block.style.marginTop = '2rem';
      block.innerHTML = `
        <header class="chain-head"><div><p class="kicker">Continuidad material y económica alegada</p><h3>2018 control → destrucción/alteración → proyecto RIC → 2022 título → MYND</h3></div><p>La adjudicación de 2022 no explica por sí sola lo que ya había ocurrido antes. Gil Marer sostiene que las demoliciones y alteraciones anteriores formaron materialmente parte de la trayectoria mediante la cual el antiguo Sun Park fue convertido en el activo después financiado, reformado y explotado.</p></header>
        <ol class="chain-track">
          <li><span>7 jun 2018</span><strong>Control material</strong><small>La toma de posesión/control aparece como punto de partida de denuncias posteriores y de la secuencia de acceso y seguridad.</small></li>
          <li><span>2018–2021</span><strong>Obras y deterioro</strong><small>Demoliciones, alteración física, restricciones de acceso, inspección y pérdida de valor/competencia fueron llevadas al expediente judicial.</small></li>
          <li><span>2020</span><strong>Narrativa RIC</strong><small>Sun Park aparece presentado dentro del perímetro CAM/RIC como proyecto adquirido/propio, libre de cargas y sujeto a una transformación hotelera relevante antes del título formal de 2022.</small></li>
          <li><span>2022</span><strong>Formalización</strong><small>Adjudicación, proyecto comunitario, licencias, transmisión estructural CAM → HNT y posterior explotación.</small></li>
          <li><span>MYND</span><strong>Monetización</strong><small>El activo transformado entra en explotación hotelera y continúa generando valor, ingresos y relaciones comerciales.</small></li>
        </ol>
        <div class="proof-split"><div><strong>Inferencia publicada</strong><span>Se presenta como inferencia causal documentada, no como sentencia firme sobre cada partida de obra. Quien sostenga que las demoliciones pertenecían a otra secuencia puede identificar proyecto, orden, licencia, contratista, certificación, factura o restitución que rompa la continuidad.</span></div><div><strong>Daño continuado alegado</strong><span>LPB: masa, unidad productiva, salida financiada y valor. CEXP: derechos operativos y económicos residuales que deben concretarse por periodo. Matkator: posesión, transformación física y frutos. Aweswell/Sun Rock: inversión, plataforma comercial y costes de recuperación, evitando doble cómputo.</span></div></div>`;
      document.getElementById('institutional-accountability-12aug').insertAdjacentElement('afterend', block);
    }

    // 5) A visible final line on criminal indicia and institutional accountability.
    if (!document.getElementById('criminal-indicia-12aug')) {
      const p = document.createElement('div');
      p.id = 'criminal-indicia-12aug';
      p.className = 'pressure-maxim';
      p.style.marginTop = '1.5rem';
      p.innerHTML = `<strong>Indicio no es condena. Pero la acumulación de indicios exige una investigación que no fragmente la cadena.</strong><span>Control antes del título, alteración física, autoridad comunitaria controvertida, intervención o no-protección fiduciaria, conocimiento judicial, narrativa inversora previa a la adjudicación y beneficio económico posterior deben examinarse como una secuencia. La misma exigencia de trazabilidad se dirige a todos los órganos de Fiscalía que han intervenido: qué recibieron, qué investigaron, qué remitieron, qué corrigieron y qué dejaron fuera.</span>`;
      document.getElementById('continuity-harm-12aug').insertAdjacentElement('afterend', p);
    }

    // 6) 12 Aug 2026: formal routing into the Canary Islands internal whistleblower system under Ley 2/2023.
    if (!document.getElementById('ley2-routing-12aug')) {
      const whistle = document.createElement('article');
      whistle.id = 'ley2-routing-12aug';
      whistle.className = 'thesis-block';
      whistle.style.marginTop = '1.5rem';
      whistle.innerHTML = `
        <div>
          <span class="evidence-badge">12 AGO 2026 · HITO INSTITUCIONAL</span>
          <h3>Ley 2/2023: traslado formal al Sistema interno de información del Gobierno de Canarias.</h3>
          <p>La Secretaría General Técnica de la Consejería de Hacienda y Relaciones con la Unión Europea comunica que la documentación presentada el 15 de julio de 2026 ante la Dirección General del Tesoro y Política Financiera —REGAGE26e00065752755— ha sido trasladada a la <b>Dirección General de Modernización y Calidad de los Servicios</b>, de la Consejería de Presidencia, Administraciones Públicas, Justicia y Seguridad, <b>a los efectos previstos en la Ley 2/2023</b> y conforme al Decreto 91/2024 que regula el Sistema interno de información de infracciones normativas de la Administración Pública de la Comunidad Autónoma de Canarias.</p>
          <p>El traslado responde expresamente a la solicitud de determinar el tratamiento de la comunicación bajo la Ley 2/2023, incluyendo <b>canal, responsable, confidencialidad, acceso restringido y protección del informante</b>. La comunicación fue firmada electrónicamente por la Secretaria General Técnica, María Belén Díaz Elías, el 12 de agosto de 2026.</p>
          <p><b>Qué significa:</b> no es una resolución sobre el fondo ni una declaración de infracción. Sí es un hito procedimental objetivo: la documentación deja de estar únicamente en el perímetro sectorial de Tesoro/Hacienda y queda formalmente encaminada hacia el sistema autonómico previsto para comunicaciones de infracciones y protección del informante.</p>
        </div>
        <div class="proof-split"><div><strong>Lo ya trazable</strong><span>Origen: DG Tesoro y Política Financiera. Registro de la comunicación: 15/07/2026. Traslado Ley 2/2023: 12/08/2026. Destino: Dirección General de Modernización y Calidad de los Servicios.</span></div><div><strong>Lo que ahora debe ser verificable</strong><span>Quién asume la gestión; qué acceso se restringe; qué preservación se ordena; cómo se protege al informante; qué órgano analiza el fondo; qué coordinaciones o remisiones se practican; y qué respuesta motivada queda registrada.</span></div></div>`;
      document.getElementById('criminal-indicia-12aug').insertAdjacentElement('afterend', whistle);
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render, { once: true });
  else render();

  // A second pass protects against older scripts rebuilding sections after this script.
  window.addEventListener('load', () => setTimeout(render, 150), { once: true });
})();
