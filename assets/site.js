(() => {
  const current = document.currentScript;
  const legacy = document.createElement('script');
  legacy.src = new URL('site-base-1728fcf.js', current.src).href;
  legacy.onload = () => {
    const isSpanish = document.documentElement.lang === 'es';

    const title = isSpanish
      ? 'Límite del concurso: LPB sí; Matkator y la Explotadora, no por arrastre.'
      : 'Insolvency boundary: LPB was in the proceeding; Matkator and the Operating Community were not pulled in automatically.';

    const text = isSpanish
      ? 'El Concurso 36/2012 era de Luchy Playa Blanca, S.L.U. El propio expediente trata a la Comunidad de Explotación del Complejo Sun Park (CESP / Explotadora) como una estructura separada —incluso como deudora de un dividendo frente a LPB— y a Matkator como titular extraconcursal. Por ello, la condición de Administrador Concursal de LPB y la supervisión del Juzgado del concurso no conferían, por sí solas, poder directo para sustituir la autoridad de la Explotadora ni disponer de bienes de Matkator: cualquier efecto sobre esos planos exigía un título jurídico independiente y contemporáneo.<br><br>El puente de 2018 es verificable documentalmente. El Administrador Concursal escribió que entendía recibida la posesión al recibir las claves de acceso y anunció que daría instrucciones al administrador de la Comunidad para que accediera al complejo para mantenimiento y vigilancia; Gil respondió contemporáneamente que mantenimiento, vigilancia y explotación correspondían a la Explotadora. Esta web no presenta ese intercambio como una sentencia de extralimitación. Lo presenta como la pregunta jurídica que debe cerrarse: <b>¿qué poder concreto permitió que facultades concursales sobre LPB produjeran efectos materiales sobre la Explotadora, Matkator, terceros y el negocio hotelero?</b><br><br>Gil Marer alega que éste fue un mecanismo recurrente: actores privados generaban o ejecutaban el acto operativo; la Administración Concursal lo habilitaba, transmitía o no lo impedía; y las actuaciones u omisiones judiciales permitían que la posición resultante persistiera. Si existió coordinación ilícita o responsabilidad individual es una cuestión para prueba y decisión por los órganos competentes, no una conclusión judicial que esta página dé por establecida.'
      : 'Insolvency Proceeding 36/2012 concerned Luchy Playa Blanca, S.L.U. The record itself treats the Comunidad de Explotación del Complejo Sun Park (CESP / Operating Community) as a separate structure —including as owing a dividend to LPB— and Matkator as an owner outside the insolvency estate. Accordingly, the Insolvency Administrator’s office over LPB and the insolvency court’s supervision did not, by themselves, confer direct power to replace the Operating Community’s authority or dispose of Matkator property: any effect on those separate planes required an independent, contemporaneous legal basis.<br><br>The 2018 bridge is document-verifiable. The Insolvency Administrator wrote that he understood possession to have been given to him when he received the access codes and said he would instruct the Owners’ Community administrator to enter the complex for maintenance and security; Gil replied contemporaneously that maintenance, security and operation belonged to the Operating Community. This site does not present that exchange as a judicial finding of excess of power. It presents the legal question that must be closed: <b>what specific authority allowed insolvency powers over LPB to produce material effects on the Operating Community, Matkator, third parties and the hotel business?</b><br><br>Gil Marer alleges that this became a recurring mechanism: private actors generated or executed the operative act; the Insolvency Administration enabled, transmitted or failed to stop it; and judicial acts or omissions allowed the resulting position to persist. Whether unlawful coordination or individual liability existed is a matter for evidence and determination by competent authorities, not a judicial conclusion asserted by this page.';

    const dossierSection = document.querySelector('#actor-accountability-12aug .shell');
    if (dossierSection && !document.getElementById('insolvency-boundary-12aug')) {
      const box = document.createElement('div');
      box.className = 'pressure-maxim';
      box.id = 'insolvency-boundary-12aug';
      box.style.marginTop = '1.5rem';
      box.innerHTML = `<strong>${title}</strong><span>${text}</span>`;
      const responsibility = dossierSection.querySelector('.responsibility-grid');
      if (responsibility) dossierSection.insertBefore(box, responsibility);
      else dossierSection.appendChild(box);
    }

    const mainUpdate = document.querySelector('#actor-update-12aug2026 .shell');
    if (mainUpdate && !document.getElementById('insolvency-boundary-main-12aug')) {
      const box = document.createElement('div');
      box.className = 'pressure-maxim';
      box.id = 'insolvency-boundary-main-12aug';
      box.style.marginTop = '1.5rem';
      box.innerHTML = `<strong>${title}</strong><span>${text}</span>`;
      mainUpdate.appendChild(box);
    }

    if (isSpanish) {
      const recovery = document.querySelector('#recuperacion .shell');
      if (recovery && !document.getElementById('preconcurso-origin-12aug')) {
        const origin = document.createElement('article');
        origin.id = 'preconcurso-origin-12aug';
        origin.className = 'thesis-block';
        origin.style.marginTop = '2rem';
        origin.innerHTML = `
          <div>
            <span class="evidence-badge allegation-badge">Origen del concurso · cuestión reabierta</span>
            <h3>¿Y si el concurso voluntario nació sobre una premisa bancaria incompleta o errónea?</h3>
            <p>La historia no empieza con el concurso ni con Acosta Matos. La documentación contractual, contable y procesal que hoy sustenta un procedimiento civil en Valencia contra la sucesora de la entidad bancaria de 2011–2012 obliga a revisar el supuesto punto de partida. Gil Marer y Aweswell sostienen que la relación financiera de LPB fue tratada como morosa antes de que existiera una base correcta y completa para hacerlo, y que la posterior ejecución y amenaza de subasta descansaron sobre esa misma premisa controvertida.</p>
            <p>Entre los datos que hoy exigen reconciliación figuran una carencia contractual que alcanzaba el final de 2011, el cierre de la cuenta en diciembre de 2011, el inicio de amortización previsto para enero de 2012 y la promoción de ejecución hipotecaria en enero de 2012. El litigio civil actualmente en curso ante el Juzgado de Primera Instancia nº 27 de Valencia, Procedimiento Ordinario 1859/2023-9, examina parte de este paquete financiero y de sus consecuencias. Esta web no anticipa su resultado.</p>
            <p>Aweswell adquirió la posición societaria de LPB a finales de 2011. Ante la ejecución y el riesgo de subasta, LPB acabó solicitando concurso voluntario el 4 de junio de 2012. Gil Marer sostiene hoy que el consejo de utilizar el concurso como escudo frente a aquella ejecución fue, visto el expediente completo, equivocado, negligente o basado en información insuficiente. La cuestión causal es de enorme alcance: <b>si el supuesto impago que precipitó la maquinaria concursal estaba mal caracterizado, ¿qué parte de los doce años posteriores debe ser revisada desde su origen?</b></p>
          </div>
          <div class="proof-split" role="group" aria-label="Estado del punto de origen">
            <div><strong>Lo documentado</strong><span>Adquisición societaria a finales de 2011; ejecución bancaria en enero de 2012; solicitud de concurso voluntario en junio de 2012; litigio posterior y actualmente existente en Valencia.</span></div>
            <div><strong>Lo que sigue controvertido</strong><span>Si existía morosidad jurídicamente exigible en los términos invocados, el cálculo correcto del paquete financiero, la causalidad con el concurso y las responsabilidades profesionales o bancarias derivadas.</span></div>
          </div>`;
        const thesis = recovery.querySelector('#tesis');
        if (thesis) thesis.insertAdjacentElement('afterend', origin);
        else recovery.prepend(origin);
      }

      if (recovery && !document.getElementById('cesp-direct-market-12aug')) {
        const market = document.createElement('article');
        market.id = 'cesp-direct-market-12aug';
        market.className = 'forensic-chain';
        market.style.marginTop = '2rem';
        market.innerHTML = `
          <header class="chain-head">
            <div><p class="kicker">La empresa hotelera también estaba fuera del concurso</p><h3>CESP no era LPB. Y el negocio no era una simple colección de apartamentos.</h3></div>
            <p>La Comunidad de Explotación del Complejo Sun Park era la estructura operativa separada de explotación unitaria. Como Matkator, no quedó absorbida automáticamente por el Concurso 36/2012 de LPB.</p>
          </header>
          <ol class="chain-track">
            <li><span>2008</span><strong>Explotación unitaria</strong><small>La documentación histórica sitúa en la Explotadora el mantenimiento, vigilancia, personal, suministros, relaciones comerciales y explotación turística.</small></li>
            <li><span>2008–2011</span><strong>Minoría disidente</strong><small>Gil Marer alega que el perímetro Monte Lanza/Molina se apartó de la explotación unitaria, utilizó unidades de forma independiente y contribuyó a fragmentar operación, costes y autoridad.</small></li>
            <li><span>2012</span><strong>Choque comercial</strong><small>La inestabilidad interna dificultó la relación con turoperadores y el hotel cerró temporalmente antes de reabrir.</small></li>
            <li><span>2012–2014</span><strong>Directo al mercado</strong><small>Gil Marer y Patricia Domínguez desarrollaron una distribución directa al consumidor, independiente de los turoperadores que evitaban un hotel afectado por conflictos internos.</small></li>
            <li><span>2014</span><strong>Plataforma real</strong><small>Correos contemporáneos muestran una operativa propia de reservas, atención telefónica, publicidad, clientes repetidores, medios digitales y desarrollo de Summers Villages/Sun Park Living.</small></li>
            <li><span>2018 →</span><strong>Desplazamiento</strong><small>La alegación es que control físico, Comunidad, Administración Concursal y decisiones u omisiones judiciales terminaron afectando también esta empresa y sus derechos, aunque no fueran por sí mismos masa concursal.</small></li>
          </ol>
          <div class="chain-conclusion"><strong>La pregunta no es sólo quién era dueño de cada finca.</strong><span>Es quién tenía derecho a explotar el hotel, quién construyó la clientela y la distribución, qué título permitió desplazar esos derechos y quién capturó después el valor comercial resultante.</span></div>`;
        const chain = recovery.querySelector('.forensic-chain');
        if (chain) chain.insertAdjacentElement('afterend', market);
        else recovery.appendChild(market);
      }

      const accountability = document.querySelector('#actor-accountability-12aug .shell') || recovery;
      if (accountability && !document.getElementById('ac-judge-causation-12aug')) {
        const inst = document.createElement('section');
        inst.id = 'ac-judge-causation-12aug';
        inst.style.marginTop = '2rem';
        inst.innerHTML = `
          <div class="section-head">
            <div><p class="kicker">Dos niveles de poder institucional · una misma pregunta causal</p><h2>Administrador Concursal y tutela judicial: acción, omisión y efectos fuera del perímetro.</h2></div>
            <p>Gil Marer no limita su alegación a decisiones adversas. Sostiene que la combinación de actuaciones positivas y pasividad institucional permitió que actos privados adquirieran efectos estables sobre patrimonio, explotación y negocio que no estaban automáticamente bajo el concurso.</p>
          </div>
          <div class="grid-2">
            <article class="path-card primary">
              <img src="${new URL('actors/francisco-de-borja-rodriguez-batllori.jpg', current.src).href}" alt="Retrato profesional de Francisco de Borja Rodríguez-Batllori Laffitte" style="width:108px;height:108px;object-fit:cover;border-radius:12px;margin-bottom:1rem">
              <span class="number">Administrador Concursal</span>
              <h3>Francisco de Borja Rodríguez-Batllori Laffitte</h3>
              <p>Su relevancia no deriva de haber ejecutado personalmente cada acto privado, sino de su posición de gatekeeper de LPB. En enero de 2018 escribió que entendía recibida la posesión al recibir las claves y que daría instrucciones al administrador de la Comunidad para acceder al complejo. Gil le respondió expresamente que la explotación, mantenimiento y vigilancia correspondían a la Explotadora y le pidió verificar libros, estatutos, cuentas, contratos y deuda comunitaria.</p>
              <p>La cuestión acumulativa es qué verificó, qué autorizó, qué dejó producir efectos, qué comunicó al Juzgado, qué intentó revertir y qué protección dio a la masa frente a una estructura comunitaria cuya legitimidad y deuda se estaban impugnando. Los escritos penales de 2026 formulan ya esa cuestión como posible relevancia criminal; no existe condena ni declaración firme de responsabilidad.</p>
            </article>
            <article class="path-card">
              <span class="number">Tutela judicial efectiva</span>
              <h3>Alberto López Villarrubia · acción y omisión judicial</h3>
              <p>El concurso confería jurisdicción sobre LPB y su masa, no una competencia general para absorber CESP, Matkator, todos los propietarios, el negocio hotelero o sus ingresos. Gil Marer sostiene que, sin embargo, la forma en que se ejerció —o dejó de ejercer— la tutela permitió que hechos nacidos fuera del título concursal se consolidaran materialmente y regresaran al procedimiento como una realidad aparentemente dada.</p>
              <p>El test público es concreto: <b>conocimiento + competencia + remedio disponible + decisión u omisión + efecto</b>. Deben reconciliarse la pérdida de control, el acceso de terceros, la destrucción y alteración física denunciadas, la negativa a determinadas medidas de inspección/pericial, el problema OB REM, la competencia por el activo, la salida financiada y el impacto sobre derechos extraconcursales. Gil Marer sostiene que la secuencia supera el umbral de indicios que justifica investigación penal; esa alegación no equivale a culpabilidad establecida.</p>
            </article>
          </div>
          <div class="pressure-maxim" style="margin-top:1.25rem"><strong>El límite de jurisdicción también se mide por sus efectos.</strong><span>Si una decisión formalmente referida a LPB terminó alterando de hecho posesión, explotación, valor, ingresos o derechos de terceros, debe identificarse el puente jurídico que autorizó cada efecto. Si no existe, la ausencia no puede quedar oculta detrás de la palabra «concurso».</span></div>`;
        accountability.appendChild(inst);
      }

      if (accountability && !document.getElementById('unitary-harm-12aug')) {
        const harm = document.createElement('div');
        harm.id = 'unitary-harm-12aug';
        harm.className = 'pressure-maxim';
        harm.style.marginTop = '1.5rem';
        harm.innerHTML = `<strong>Una sola secuencia; daños en varios patrimonios.</strong><span>El daño alegado no se agota en el precio de las fincas de LPB. Incluye, según el derecho que corresponda a cada perjudicado y sin doble contabilización: pérdida de valor de la masa y de la unidad productiva; frustración de alternativas de salida financiada; pérdida de explotación y clientela de CESP; intervención y explotación de bienes extraconcursales de Matkator; pérdida de valor y oportunidad para Aweswell; costes de reconstrucción, financiación, litigación y recuperación; y los frutos e ingresos que continúan generándose sobre el hotel transformado. La pregunta económica final es sencilla: <b>¿qué valor existía antes, quién lo perdió, qué valor se creó después con el mismo activo y quién lo está cobrando?</b></span>`;
        accountability.appendChild(harm);
      }
    }
  };
  legacy.onerror = () => console.error('Project Sun Rock base script failed to load.');
  document.head.appendChild(legacy);
})();