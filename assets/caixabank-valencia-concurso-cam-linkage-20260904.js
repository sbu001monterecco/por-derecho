(() => {
  'use strict';

  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  if (!path.includes('/es/reclamacion-caixabank-valencia/')) return;
  if (path.includes('/senalamiento-28-enero-2027/')) return;

  const mount = () => {
    if (document.getElementById('caixabank-concurso-cam-linkage')) return;

    const anchor = document.getElementById('caixabank-borja-witness-control');
    if (!anchor) return;

    const section = document.createElement('section');
    section.className = 'section alt';
    section.id = 'caixabank-concurso-cam-linkage';
    section.innerHTML = `
      <div class="shell record">
        <div class="section-head">
          <div>
            <p class="kicker">VALENCIA ↔ CONCURSO 36/2012 ↔ CAM · NEXO PROBATORIO CONTROLADO</p>
            <h2>La reclamación, la defensa y el puente hacia el Administrador Concursal y el perímetro Acosta Matos</h2>
          </div>
          <p>Una misma historia económica puede atravesar procedimientos y sociedades distintas. La prueba debe unirlas sin convertir esa continuidad en una acusación automática.</p>
        </div>

        <div class="grid">
          <article class="card">
            <h3>La reclamación de Aweswell</h3>
            <p><strong>Aweswell Limited</strong> mantiene frente a <strong>CAIXABANK, S.A.</strong> el Procedimiento Ordinario 1859/2023-9. La demanda articula pretensiones de nulidad/restitución y, subsidiariamente, daños derivados del paquete financiero originado en 2008–2010 y de su posterior administración y ejecución.</p>
            <p>La tesis económica publicada exige analizar conjuntamente préstamo, suelo, swap, refinanciación, prenda, cuentas, imputaciones, supuesta mora, vencimiento y ejecución, y después asignar responsabilidad jurídica actor por actor.</p>
          </article>
          <article class="card">
            <h3>La defensa de CaixaBank</h3>
            <p><strong>CaixaBank controvierte responsabilidad, prescripción, causalidad, pagos y cuantía.</strong> Su pericial sostiene, entre otros extremos, que la documentación contractual advertía de posibles liquidaciones negativas del swap y ofrece su propia lectura económica del producto y del perjuicio reclamado.</p>
            <p>No existe sentencia sobre el fondo. La posición de Aweswell y la defensa de CaixaBank deben conservarse separadas de cualquier conclusión judicial todavía inexistente.</p>
          </article>
        </div>

        <div class="warn" style="margin-top:1rem">
          <strong>El puente económico que no puede fragmentarse.</strong> Aweswell y Por Derecho alegan que el drenaje financiero, la administración de cuentas y la ejecución de Bankia contribuyeron a la necesidad de acudir al Concurso 36/2012 como respuesta defensiva. Después, el activo hipotecario siguió una cadena distinta: <strong>Bankia → SAREB → Promontoria Holding 122 B.V. → Construcciones Acosta Matos, S.A. (CAM)</strong>. La cesión del crédito no convierte a todos los actores en una sola persona, pero tampoco borra saldo, pagos, garantías, excepciones, conocimiento o decisiones anteriores.
        </div>

        <article class="card" style="margin-top:1rem">
          <p class="kicker">HECHO PROCESAL DOCUMENTADO · NO INFERENCIA</p>
          <h3>CaixaBank eligió como testigo al mismo Administrador Concursal cuya actuación es discutida en la ruta PH122→CAM</h3>
          <p>El expediente ya registra que <strong>CaixaBank solicitó la testifical de Francisco de Borja Rodríguez-Batllori Laffitte, Administrador Concursal del Concurso 36/2012, y Aweswell se adhirió después a esa petición</strong>.</p>
          <p>Ese hecho <strong>no demuestra por sí solo</strong> parcialidad, coordinación impropia, colusión o testimonio falso. Sí crea un nexo probatorio concreto: CaixaBank considera material para su defensa al mismo cargo institucional que administró el concurso surgido de la historia bancaria objeto de la reclamación y cuya actuación posterior se discute respecto de CAM.</p>
        </article>

        <div class="grid" style="margin-top:1rem">
          <article class="card">
            <h3>1 · Bankia / CaixaBank</h3>
            <p>La vía aguas arriba examina administración de cuentas, productos financieros, regularización/mora, vencimiento, certificación, ejecución y las obligaciones o responsabilidades que pudieran haber permanecido o transmitido por sucesión.</p>
          </article>
          <article class="card">
            <h3>2 · PH122 / CAM / Acosta Matos</h3>
            <p>La vía aguas abajo examina qué crédito adquirió realmente CAM, a qué saldo, precio y condiciones, qué conocía, qué control material obtuvo, qué valoración se utilizó y cómo el crédito terminó convertido en posición patrimonial y título.</p>
          </article>
          <article class="card">
            <h3>3 · Administrador Concursal</h3>
            <p>La actuación del AC debe examinarse como compuerta institucional: representación de LPB, disclosure de la cesión, verificación del acreedor, valoración, alternativas, conservación de la masa, implementación y cuentas.</p>
          </article>
          <article class="card">
            <h3>4 · El resultado común que debe explicarse</h3>
            <p>La secuencia publicada muestra actos distintos que, según la alegación de Por Derecho, convergieron objetivamente en debilitar las rutas de refinanciación, recuperación y control de LPB/Aweswell mientras se consolidaba la vía acreedora que terminó en CAM. <strong>Convergencia de efectos no equivale todavía a concierto.</strong></p>
          </article>
        </div>

        <article class="card" style="margin-top:1rem">
          <p class="kicker">PP 1041/2017 · SEGUNDO LADO DEL TRIÁNGULO</p>
          <h3>La controversia sobre disclosure y representación de LPB</h3>
          <p>Por Derecho alega que, en la vía dirigida a conocer escritura, precio, pago y costes de la adquisición <strong>PH122→CAM</strong>, el Administrador Concursal puso fin al mandato formal del abogado de LPB que perseguía esa información; posteriormente se presentó un desistimiento en nombre de LPB; <strong>CAM no se opuso</strong>; y aquella vía terminó.</p>
          <p>La autoridad, instrucción, redacción, firma, finalidad, conocimiento y beneficio para la masa de esos actos siguen requiriendo el <strong>expediente certificado completo PP 1041/2017</strong>. La alegación no sustituye esa prueba primaria.</p>
        </article>

        <div class="warn" style="margin-top:1rem">
          <strong>Tesis de trabajo atribuida a Aweswell / Por Derecho.</strong> El expediente permite ya sostener una <strong>alineación adversa objetiva y un nexo suficientemente concreto para investigar conducta concertada</strong>. La hipótesis es que actos de Bankia/CaixaBank, del perímetro acreedor que desemboca en CAM y de las compuertas controladas por el Administrador Concursal pudieron operar de forma conscientemente complementaria contra los objetivos de refinanciación, recuperación y preservación patrimonial de LPB/Aweswell. <strong>“Colusión” no se publica como hecho probado.</strong> Debe demostrarse mediante conocimiento, comunicaciones, instrucciones, intercambio documental, decisiones complementarias, ocultación o supresión deliberada de alternativas, beneficio conocido y causalidad.
        </div>

        <div class="grid" style="margin-top:1rem">
          <article class="card">
            <h3>Implicaciones civiles y concursales</h3>
            <ul>
              <li>nulidad, restitución, daños, causalidad y cuantificación en Valencia;</li>
              <li>conciliación del saldo real que entró y salió del concurso;</li>
              <li>eventual daño a la masa por actos u omisiones del Administrador Concursal;</li>
              <li>eventual beneficio o recuperación sin base suficiente, si la contabilidad completa lo demuestra;</li>
              <li>reparto actor por actor del daño incremental y de las obligaciones retenidas o transmitidas.</li>
            </ul>
          </article>
          <article class="card">
            <h3>Dimensión penal · sólo si se prueban los elementos</h3>
            <p>La coincidencia de intereses o la hostilidad procesal no son delito. La dimensión penal sólo aparece si los originales demuestran, según el acto y la fecha, elementos adicionales como <strong>engaño intencional, manipulación o uso consciente de documentación materialmente falsa, ocultación deliberada de información determinante, extralimitación consciente en patrimonio ajeno, fraude procesal o participación consciente en un resultado patrimonial ilícito</strong>.</p>
            <p>Cada posible figura penal requiere prueba de autor, capacidad, acto, dolo, uso, causalidad y perjuicio. No se infiere responsabilidad penal por pertenencia a una cadena empresarial o por una resolución judicial adversa.</p>
          </article>
        </div>

        <article class="card" style="margin-top:1rem">
          <p class="kicker">PRUEBA QUE PUEDE CAMBIAR “ALINEACIÓN” POR “COORDINACIÓN”</p>
          <h3>Producción prioritaria P0</h3>
          <ol>
            <li><strong>PP 1041/2017 completo y certificado:</strong> escrito original de desistimiento, instrucción, redactor, firma, poder, metadatos, comunicaciones, ratificación y análisis de interés de la masa.</li>
            <li><strong>Designación y preparación de la testifical de Borja en Valencia:</strong> solicitud de CaixaBank, objeto concreto de la prueba, comunicaciones procesales, documentación remitida o utilizada y preparación de la declaración dentro de los límites legales.</li>
            <li><strong>Cadena Bankia→SAREB→PH122→CAM:</strong> instrumentos, anexos, saldo, pagos, garantías, precio, due diligence, servicing, instrucciones y obligaciones retenidas.</li>
            <li><strong>AC↔CAM y AC↔perímetro acreedor:</strong> comunicaciones, informes, verificaciones, valoración, tratamiento de alternativas, instrucciones de control, implementación y cuentas.</li>
            <li><strong>Mayor económico único:</strong> principal → intereses → swap → prenda → pagos → mora → ejecución → concurso → cesiones → dación/adjudicación → recuperación, sin doble cómputo.</li>
          </ol>
        </article>

        <article class="card" style="margin-top:1rem">
          <p class="kicker">DEFENSA / EXPLICACIÓN INOCENTE QUE DEBE SER CONTRASTADA</p>
          <h3>La hipótesis adversa no elimina explicaciones independientes</h3>
          <p>CaixaBank puede sostener que propuso al Administrador únicamente por su conocimiento institucional del concurso; el AC puede sostener que actuó dentro de sus poderes, bajo supervisión judicial y en interés de la masa; y CAM puede sostener que adquirió y ejercitó regularmente un crédito y que toda posterior adquisición o dación fue jurídicamente autorizada. También pueden existir razones legítimas para rechazar alternativas, cambiar representación, valorar activos o defender posiciones coincidentes.</p>
          <p><strong>La función del expediente no es presumir que esas explicaciones son falsas.</strong> Es contrastarlas con los documentos contemporáneos y comprobar si explican de forma coherente la secuencia completa o si, por el contrario, aparecen comunicaciones, decisiones o beneficios incompatibles con una actuación verdaderamente independiente.</p>
        </article>

        <div class="warn" style="margin-top:1rem">
          <strong>Pregunta central.</strong> ¿Estamos ante actores independientes cuyas posiciones jurídicas coincidieron, o ante una secuencia en la que conocimiento, decisiones y actuaciones se complementaron conscientemente para producir un resultado patrimonial común? La respuesta no puede obtenerse fragmentando Valencia, Concurso 36/2012 y CAM en expedientes estancos.
        </div>

        <p class="linkrow" style="margin-top:1rem">
          <a class="button" href="../administrador-concursal-puerta-credito-titulo/">Administrador · compuerta crédito→título →</a>
          <a class="button secondary" href="../acreedor-de-registro/responsabilidad/">Cadena acreedora y responsabilidad →</a>
          <a class="button secondary" href="../acosta-matos-perimetro/">Perímetro Acosta Matos →</a>
          <a class="button secondary" href="../ingenieria-inversa-criminal-unitaria/">Análisis penal unitario →</a>
        </p>

        <p class="small"><strong>Control de lenguaje.</strong> Publicado como alegación y marco de investigación. No se declara colusión, concierto, fraude, falsedad, administración desleal ni responsabilidad penal firme de CaixaBank, CAM, el perímetro Acosta Matos, el Administrador Concursal o cualquier otra persona. Cada conclusión depende de prueba primaria y del régimen jurídico aplicable a la fecha de cada acto.</p>
      </div>`;

    anchor.insertAdjacentElement('afterend', section);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount, { once: true });
  } else {
    mount();
  }
})();
