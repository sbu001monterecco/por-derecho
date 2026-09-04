(() => {
  'use strict';
  const path = location.pathname.replace(/\/+$/, '/');

  const add = (target, html) => {
    if (!target || document.querySelector('[data-uria-haya-puzzle-supplement="20260904a"]')) return;
    const wrap = document.createElement('section');
    wrap.className = 'section alt';
    wrap.setAttribute('data-uria-haya-puzzle-supplement', '20260904a');
    wrap.innerHTML = html;
    target.appendChild(wrap);
  };

  const es = path.includes('/es/');
  const puzzle = path.endsWith('/puzzle/');
  const uria = path.endsWith('/uria-menendez-sun-park/');
  if (!puzzle && !uria) return;

  const main = document.querySelector('main');
  if (!main) return;

  if (es) {
    add(main, `<div class="shell"><p class="kicker">INTEGRACIÓN UNITARIA · 4 SEPTIEMBRE 2026</p><h2>HAYA / Cerberus + huellas Uría 2017 y 2024</h2><div class="pressure-maxim"><strong>URÍA MENÉNDEZ NO ENTRA POR PRIMERA VEZ EN ESTA HISTORIA CON LA DEFENSA DE CAIXABANK DE 2024.</strong><span> El expediente conserva un contacto AC–Uría reportado en 2015; una representación primaria de PH122 por Uría dentro del Concurso 36/2012 en 2017; asesoramiento público a RICPE en 2019–2021; la defensa de CaixaBank en 2024; y una solicitud judicial de producción en 2026.</span></div><p><strong>Entidad canónica:</strong> URÍA MENÉNDEZ ABOGADOS, S.L.P. · NIF B28563963.</p><p><strong>Estado:</strong> DOCUMENTED MULTI-ROLE OVERLAP — CONFLICT / CONFIDENTIALITY REVIEW REQUIRED. La coincidencia temporal o institucional no prueba conflicto, coordinación ni conducta ilícita; cliente, mandato, información recibida, barreras y conflictos deben reconstruirse asunto por asunto.</p><p><strong>HAYA / Cerberus:</strong> el módulo separado mantiene la regla <em>servicing/interlocución ≠ titularidad ≠ mandato específico ≠ control de Cerberus sobre el activo concreto</em>.</p><div class="actions"><a class="button" href="../haya-cerberus/">HAYA / Cerberus</a><a class="button secondary" href="../uria-menendez/">Uría · panorama 2017/2019–20/2024/2026</a><a class="button secondary" href="../../data/puzzle/uria-haya-puzzle-registry.json">Registro estructurado</a></div></div>`);
  } else {
    add(main, `<div class="shell"><p class="kicker">UNITARY INTEGRATION · 4 SEPTEMBER 2026</p><h2>HAYA / Cerberus + the 2017 and 2024 Uría footprints</h2><div class="pressure-maxim"><strong>URÍA MENÉNDEZ DID NOT ENTER THIS HISTORY FOR THE FIRST TIME WITH CAIXABANK'S 2024 DEFENCE.</strong><span> The record preserves a reported AC–Uría contact in 2015; primary Uría representation of PH122 inside Concurso 36/2012 in 2017; publicly documented RICPE advice in 2019–2021; CaixaBank's defence in 2024; and a judicial production request in 2026.</span></div><p><strong>Canonical entity:</strong> URÍA MENÉNDEZ ABOGADOS, S.L.P. · NIF B28563963.</p><p><strong>Status:</strong> DOCUMENTED MULTI-ROLE OVERLAP — CONFLICT / CONFIDENTIALITY REVIEW REQUIRED. Repeated involvement does not itself prove conflict, coordination or wrongdoing; client, mandate, information received, barriers and conflict process must be reconstructed matter by matter.</p><p><strong>HAYA / Cerberus:</strong> the separate Spanish deep-dive preserves the rule <em>servicing/contact ≠ title ≠ asset-specific mandate ≠ Cerberus control of the specific asset</em>.</p><div class="actions"><a class="button" href="../../es/haya-cerberus/">HAYA / Cerberus (ES)</a><a class="button secondary" href="../../es/uria-menendez/">Uría overview (ES)</a><a class="button secondary" href="../../data/puzzle/uria-haya-puzzle-registry.json">Structured registry</a></div></div>`);
  }
})();
