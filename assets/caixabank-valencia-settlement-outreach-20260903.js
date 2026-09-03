(() => {
  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  if (!path.includes('/es/reclamacion-caixabank-valencia/')) return;
  if (path.includes('/senalamiento-28-enero-2027/')) return;
  if (document.getElementById('caixabank-adr-settlement-outreach')) return;

  const hero = document.querySelector('main .hero');
  if (!hero) return;

  const section = document.createElement('section');
  section.className = 'section alt';
  section.id = 'caixabank-adr-settlement-outreach';
  section.innerHTML = `
    <div class="shell record">
      <div class="section-head">
        <div>
          <p class="kicker">INVITACIÓN ABIERTA · ADR · RESOLUCIÓN PREVIA AL JUICIO</p>
          <h2>Una oportunidad para resolver el procedimiento antes del 28 de enero de 2027</h2>
        </div>
        <p>Aweswell mantiene abierta una vía seria, confidencial y comercial para explorar una solución extrajudicial con CaixaBank.</p>
      </div>

      <div class="grid">
        <article class="card">
          <h3>Invitación abierta a CaixaBank</h3>
          <p><strong>Aweswell Limited invita a CaixaBank, a sus representantes y al equipo interno con competencia para resolver este tipo de controversias a ponerse en contacto con nosotros</strong> con el fin de explorar, de buena fe y antes del juicio, una solución extrajudicial.</p>
          <p>La intención es abrir una conversación <strong>confidencial, constructiva y comercialmente racional</strong> que permita comprobar si existe una salida beneficiosa para ambas partes y evite, si es posible, el coste, el tiempo y la incertidumbre de continuar hasta juicio.</p>
          <p>Esta invitación se formula <strong>sin perjuicio de las posiciones procesales de las partes y sin admisión alguna de responsabilidad</strong>. Su finalidad es exclusivamente facilitar una posible resolución negociada.</p>
        </article>
        <article class="card">
          <h3>Buscamos abogado/a con experiencia real en ADR con CaixaBank</h3>
          <p>También queremos hablar con abogados que tengan <strong>experiencia práctica y demostrable negociando acuerdos con CaixaBank</strong>, especialmente en litigación bancaria compleja, productos financieros, derivados/swaps o controversias comerciales y financieras.</p>
          <p>Buscamos a alguien que conozca no sólo cómo litigar frente a una gran entidad financiera, sino cómo <strong>identificar a los responsables internos adecuados, llegar al nivel de decisión correcto, estructurar una propuesta creíble y facilitar una negociación pre-juicio capaz de conducir a una solución real</strong>.</p>
          <p>Si has llevado personalmente este tipo de negociación con CaixaBank, o puedes presentarnos a alguien que tenga esa experiencia, agradecemos el contacto privado.</p>
        </article>
      </div>

      <article class="card" style="margin-top:1rem">
        <p class="kicker">DOCUMENTO PROCESAL · COPIA PÚBLICA DISOCIADA</p>
        <h3>Señalamiento vigente: 28 de enero de 2027 a las 10:00</h3>
        <p>La diligencia de 6 de noviembre de 2025 del <strong>Juzgado de Primera Instancia nº 27 de Valencia</strong>, en el Procedimiento Ordinario <strong>1859/2023-9</strong>, volvió a señalar la vista para el <strong>28 de enero de 2027 a las 10:00</strong>. La imagen publicada a continuación es una copia pública con datos personales y de verificación de terceros innecesarios disociados.</p>
        <figure style="margin:1rem 0 0">
          <a href="senalamiento-28-enero-2027/" aria-label="Abrir el registro del señalamiento de 28 de enero de 2027">
            <img src="../../assets/evidence/caixabank-valencia-1859-2023-diligencia-06nov2025-p1-publica.jpg" alt="Copia pública parcialmente disociada de la diligencia del JPI nº 27 de Valencia que señala la vista para el 28 de enero de 2027 a las 10:00" loading="lazy" style="display:block;width:100%;height:auto;border:1px solid rgba(19,37,45,.16);border-radius:12px;background:#fff">
          </a>
          <figcaption class="small" style="margin-top:.65rem">Copia pública parcialmente disociada. <a href="senalamiento-28-enero-2027/">Abrir el registro documental y la segunda página →</a></figcaption>
        </figure>
      </article>

      <article class="card" style="margin-top:1rem">
        <p class="kicker">LLAMAMIENTO PÚBLICO · LINKEDIN · SEPTIEMBRE 2026</p>
        <h3>Busco abogados con experiencia real en la negociación de acuerdos con CaixaBank</h3>
        <p>Tenemos actualmente un procedimiento bancario en curso frente a <strong>CaixaBank</strong> ante el <strong>Juzgado de Primera Instancia nº 27 de Valencia</strong>, con el juicio señalado para <strong>enero de 2027</strong>.</p>
        <p>Nuestro objetivo inmediato no es trasladar públicamente el litigio, sino determinar si, antes de llegar a juicio, existe una vía seria y constructiva para alcanzar una <strong>solución negociada y confidencial</strong>.</p>
        <p>Por ello, me gustaría contactar con abogados que tengan <strong>experiencia práctica y demostrable negociando acuerdos con CaixaBank</strong>, especialmente en asuntos bancarios complejos, productos financieros, derivados/swaps o controversias comerciales.</p>
        <p>Me interesan particularmente profesionales que conozcan no sólo cómo litigar frente a una gran entidad financiera, sino también cómo:</p>
        <ul>
          <li>identificar a los responsables internos adecuados;</li>
          <li>llegar al nivel de decisión correcto dentro del banco;</li>
          <li>estructurar un planteamiento de negociación creíble; y</li>
          <li>facilitar una conversación preprocesal o pre-juicio que pueda conducir a una solución real.</li>
        </ul>
        <p>Si has llevado personalmente este tipo de negociación con CaixaBank, o puedes presentarme a alguien que tenga esa experiencia, agradecería mucho que me contactaras por privado.</p>
        <p>La notificación judicial publicada en esta página proporciona el contexto procesal. El procedimiento está activo y nuestra intención es sencilla: <strong>aprovechar el periodo hasta el juicio de enero de 2027 para explorar si existe una solución comercialmente racional y beneficiosa para ambas partes</strong>.</p>
        <p>Agradezco también que compartáis este llamamiento con la persona adecuada.</p>
        <p class="small">#CaixaBank #DerechoBancario #LitigaciónBancaria #ResoluciónDeConflictos #Negociación #Mediación #ADR #LitigaciónFinanciera #España</p>
      </article>

      <div class="warn" style="margin-top:1rem">
        <strong>Canal abierto.</strong> Esta publicación es una invitación a dialogar, no una renuncia, concesión ni exposición pública de la estrategia procesal. Aweswell está disponible durante septiembre de 2026 para identificar el canal adecuado dentro de CaixaBank y, si existe voluntad recíproca, explorar una solución antes del juicio.
      </div>
    </div>`;

  hero.insertAdjacentElement('afterend', section);
})();