(() => {
  'use strict';
  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  const targets = {
    '/es/administrador-concursal-puerta-credito-titulo/': {
      kicker:'NUEVO PUENTE · VALENCIA ↔ AC ↔ CAM',
      title:'La defensa de CaixaBank convierte las palabras y decisiones del AC en prueba material fuera del concurso.',
      body:'CaixaBank ha llevado al procedimiento de Valencia el informe del Administrador Concursal y su posición de 2021 para sostener legitimación, firmeza/preclusión y alcance. Además pidió la testifical del propio AC. El nuevo nodo documenta esa procedencia y la conecta con PP 1041, OB REM y la ruta crédito→título sin declarar coordinación como hecho probado.'
    },
    '/es/acreedor-de-registro/responsabilidad/': {
      kicker:'PUENTE DE RESPONSABILIDAD · SPLIT CREDIT',
      title:'La reclamación de Valencia es la rama aguas arriba de la misma historia económica que aguas abajo terminó en CAM.',
      body:'El paquete financiero originario y el activo hipotecario no siguieron necesariamente la misma ruta jurídica. La nueva sala de Valencia separa responsabilidad Caja/BFA/Bankia→CaixaBank de activo Bankia→SAREB→PH122→CAM y obliga a reconciliar ambas ramas con un único mayor económico.'
    },
    '/es/acosta-matos-perimetro/': {
      kicker:'CAIXABANK VALENCIA · PERÍMETRO ACOSTA MATOS',
      title:'La reclamación bancaria no es externa al perímetro: examina la rama de responsabilidad del crédito que después convergió en CAM.',
      body:'El nuevo análisis conecta el paquete 2008–2010, la ejecución Bankia, Concurso 36/2012, la cesión a CAM, las compuertas del AC y el episodio OB REM. Por Derecho atribuye al AC una hipótesis de agente funcional/habilitante del perímetro CAM; la página identifica qué prueba necesitaría esa alegación para pasar de patrón a coordinación demostrable.'
    },
    '/es/ingenieria-inversa-criminal-unitaria/': {
      kicker:'CLÚSTER P0 · CAIXABANK / AC / CAM / OB REM',
      title:'Nueva vía criminal-first: procedencia de la defensa, testifical del AC y desagregación del crédito/activo.',
      body:'La evidencia nueva no es sólo paralelismo narrativo. CaixaBank utiliza material del AC como fundamento defensivo y lo propone como testigo; el episodio OB REM muestra además una desvinculación AC↔CAM de una estructura registral que trataba préstamo y fincas como conjunto. Se publica como clúster de investigación con explicación inocente y elementos penales condicionados.'
    },
    '/es/adjudicacion-2022-reconstruccion-documental/': {
      kicker:'ANTECEDENTE 2018 · OB REM → DACIÓN 2022',
      title:'La dación de 2022 debe leerse con el antecedente de desvinculación y venta directa AC↔CAM de 2018.',
      body:'La cláusula OB REM reproducida en la oposición de Aweswell trataba el préstamo distribuido como uno solo para imputación de pagos. En 2018 LPB/AC y CAM declararon extinguida esa vinculación para una venta directa; el Registro suspendió inicialmente y la AC pidió convalidación. El nuevo nodo pregunta cómo esa separación afectó saldo, valor, competencia y resultado crédito→título.'
    }
  };
  const cfg = targets[path];
  if (!cfg) return;

  const mount = () => {
    if (document.getElementById('caixabank-valencia-unitary-inbound')) return;
    const hero = document.querySelector('main .hero');
    const main = document.querySelector('main');
    if (!main) return;
    const section = document.createElement('section');
    section.id = 'caixabank-valencia-unitary-inbound';
    section.className = 'section alt';
    section.innerHTML = `<div class="shell record"><div style="border-left:6px solid #8c6b2f;background:#fffaf0;padding:1rem 1.2rem;border-radius:0 14px 14px 0"><p class="kicker">${cfg.kicker}</p><h2>${cfg.title}</h2><p>${cfg.body}</p><p class="linkrow"><a class="button" href="../reclamacion-caixabank-valencia/faq-contexto-unitario/">FAQ unitario Valencia →</a><a class="button secondary" href="../reclamacion-caixabank-valencia/documentos/">Demanda / defensa / AC →</a><a class="button secondary" href="../reclamacion-caixabank-valencia/ob-rem-ac-cam-28nov2018/">OB REM · AC · CAM →</a></p><p class="small"><strong>Límite:</strong> conexión documental y patrón de investigación no equivalen a colusión, concierto o responsabilidad penal probada.</p></div></div>`;
    if (hero) hero.insertAdjacentElement('afterend', section); else main.prepend(section);
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount, {once:true});
  else mount();
})();
