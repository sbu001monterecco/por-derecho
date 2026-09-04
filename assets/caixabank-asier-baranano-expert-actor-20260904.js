(() => {
  'use strict';

  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  if (!path.includes('/es/reclamacion-caixabank-valencia/')) return;
  if (path.includes('/senalamiento-28-enero-2027/')) return;

  const mount = () => {
    if (document.getElementById('caixabank-asier-baranano-expert-actor')) return;

    const anchor = document.getElementById('caixabank-concurso-cam-linkage') ||
      document.getElementById('caixabank-borja-witness-control');
    if (!anchor) return;

    const section = document.createElement('section');
    section.className = 'section';
    section.id = 'caixabank-asier-baranano-expert-actor';
    section.innerHTML = `
      <div class="shell record">
        <div class="section-head">
          <div>
            <p class="kicker">ACTOR CONFIRMADO · PERICIAL DE CAIXABANK · PO 1859/2023</p>
            <h2>Asier Barañano Revuelta · PKF Attest · ROAC 18046</h2>
          </div>
          <p>La conexión con CaixaBank es directa y documental: aceptación del encargo pericial y firma del informe aportado por la defensa.</p>
        </div>

        <div class="grid">
          <article class="card">
            <h3>Identidad profesional verificada</h3>
            <ul>
              <li><strong>Nombre canónico:</strong> Asier Barañano Revuelta.</li>
              <li><strong>ROAC:</strong> 18046.</li>
              <li><strong>Firma:</strong> PKF Attest.</li>
              <li><strong>Perfil público:</strong> socio de Auditoría de cuentas.</li>
              <li><strong>Alias de búsqueda:</strong> “Asier Baraño Revuelta” y “Asier Baranano Revuelta”.</li>
            </ul>
          </article>

          <article class="card">
            <h3>24 enero 2024 · aceptación</h3>
            <p>El expediente de <strong>Aweswell Limited v CAIXABANK, S.A., PO 1859/2023-9</strong> contiene la carta de aceptación del encargo pericial de PKF Attest para la parte CaixaBank, firmada por <strong>Asier Barañano Revuelta</strong>.</p>
            <p><strong>Clasificación:</strong> vínculo procesal directo, confirmado por documento del expediente.</p>
          </article>

          <article class="card">
            <h3>17 octubre 2024 · informe pericial</h3>
            <p><strong>Asier Barañano Revuelta y Zigor Bilbao</strong> figuran como firmantes/responsables profesionales del informe pericial de PKF Attest utilizado por la defensa de CaixaBank.</p>
            <p>La pericial y sus cálculos deben analizarse por mandato, fuentes, supuestos, integridad documental, reproducibilidad, causalidad y quantum.</p>
          </article>

          <article class="card">
            <h3>Control de independencia</h3>
            <p>La LEC exige al perito actuar con la mayor objetividad posible y considerar lo favorable y perjudicial para cualquiera de las partes. El expediente DD mantiene abierta una revisión documental de aceptación, independencia y conflictos.</p>
            <p><strong>No se publica como hecho</strong> ninguna falta de objetividad, conflicto o irregularidad sin prueba primaria específica.</p>
          </article>
        </div>

        <div class="warn" style="margin-top:1rem">
          <strong>Mapa de relaciones confirmado.</strong><br>
          <strong>Asier Barañano Revuelta → PKF Attest</strong> · afiliación profesional.<br>
          <strong>PKF Attest → CaixaBank / PO 1859/2023</strong> · encargo pericial de parte.<br>
          <strong>Asier Barañano Revuelta → CaixaBank / PO 1859/2023</strong> · aceptación firmada + informe pericial cofirmado.<br>
          <strong>Asier Barañano Revuelta ↔ Zigor Bilbao</strong> · cofirmantes / profesionales responsables del informe.
        </div>

        <article class="card" style="margin-top:1rem">
          <p class="kicker">LÍMITE PROBATORIO</p>
          <h3>Lo que esta conexión no demuestra</h3>
          <p>No se infiere que Barañano fuera empleado o decisor interno de CaixaBank/Bankia, que interviniera en la originación de 2008–2010, la ejecución, el Concurso 36/2012, la cadena Bankia→SAREB→PH122→CAM, ni que tuviera relación con CAM, RICPE, Cerberus/Promontoria o el Administrador Concursal. Cualquier relación adicional exige prueba primaria propia.</p>
        </article>

        <article class="card" style="margin-top:1rem">
          <p class="kicker">PRODUCCIÓN P0 · PERICIAL</p>
          <h3>Qué debe poder reproducirse y contrastarse</h3>
          <ol>
            <li>aceptación original/certificada de 24 enero 2024 y alcance exacto del encargo;</li>
            <li>instrucciones y preguntas remitidas por CaixaBank a PKF Attest;</li>
            <li>corpus completo de documentos y datos entregados al equipo pericial;</li>
            <li>informe de 17 octubre 2024, anexos, hojas de cálculo y fuentes primarias;</li>
            <li>autoría y reparto del trabajo entre Barañano, Zigor Bilbao y demás equipo;</li>
            <li>declaraciones y controles de independencia/conflictos que sean legalmente obtenibles;</li>
            <li>reproducción independiente de cálculos y prueba de sensibilidad a los hechos controvertidos.</li>
          </ol>
        </article>

        <p class="linkrow" style="margin-top:1rem">
          <a class="button" href="#caixabank-concurso-cam-linkage">CaixaBank ↔ Concurso ↔ CAM →</a>
          <a class="button secondary" href="../acreedor-de-registro/responsabilidad/">Cadena acreedora →</a>
          <a class="button secondary" href="../ingenieria-inversa-criminal-unitaria/">Análisis unitario →</a>
        </p>

        <p class="small"><strong>Control de lenguaje.</strong> Asier Barañano Revuelta se registra como actor material por su función pericial documentada para la defensa de CaixaBank. No se atribuye conducta impropia, falta de independencia, conflicto, fraude o responsabilidad alguna sin prueba específica.</p>
      </div>`;

    anchor.insertAdjacentElement('afterend', section);
  };

  const attempt = () => {
    mount();
    if (!document.getElementById('caixabank-asier-baranano-expert-actor')) {
      window.setTimeout(mount, 250);
      window.setTimeout(mount, 750);
    }
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', attempt, { once: true });
  } else {
    attempt();
  }
})();
