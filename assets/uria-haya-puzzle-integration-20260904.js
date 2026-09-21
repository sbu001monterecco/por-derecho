(() => {
  'use strict';
  const path = location.pathname.replace(/\/+$/, '/');

  const add = (target, html) => {
    if (!target || document.querySelector('[data-uria-haya-puzzle-supplement="20260904b"]')) return;
    const wrap = document.createElement('section');
    wrap.className = 'section alt';
    wrap.setAttribute('data-uria-haya-puzzle-supplement', '20260904b');
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
    add(main, `<div class="shell"><p class="kicker">INTEGRACIÓN UNITARIA · 4 SEPTIEMBRE 2026</p><h2>HAYA / Cerberus + huellas Uría 2015, 2017 y 2024</h2><div class="pressure-maxim"><strong>URÍA MENÉNDEZ NO ENTRA POR PRIMERA VEZ EN ESTA HISTORIA CON LA DEFENSA DE CAIXABANK DE 2024.</strong><span> El expediente conserva comunicaciones reportadas dentro del perímetro acreedor/AC en 2015; una representación primaria de PH122 por Uría dentro del Concurso 36/2012 en 2017; asesoramiento documentado a RICPE en 2019–2021; la defensa de CaixaBank en 2024; y una solicitud judicial de producción en 2026.</span></div><p><strong>Contraprueba 2015 que debe leerse junto a la conexión:</strong> el hilo contemporáneo informa de una vía HAYA → documentación del procedimiento → Uría Madrid y de intervención reportada de Javier González; pero el 30/04/2015 Cuatrecasas informó, tras hablar con Uría, que Uría <em>todavía no tenía encargo para realizar actuación alguna en nombre de HAYA</em>. Por tanto, el cliente y mandato de Uría en abril de 2015 no pueden presumirse.</p><p><strong>Entidad canónica:</strong> URÍA MENÉNDEZ ABOGADOS, S.L.P. · NIF B28563963.</p><p><strong>Estado:</strong> DOCUMENTED MULTI-ROLE OVERLAP — CONFLICT / CONFIDENTIALITY REVIEW REQUIRED. La coincidencia temporal o institucional no prueba conflicto, coordinación ni conducta ilícita; cliente, mandato, información recibida, barreras y conflictos deben reconstruirse asunto por asunto.</p><p><strong>HAYA / Cerberus:</strong> el módulo separado mantiene la regla <em>servicing/interlocución ≠ titularidad ≠ mandato específico ≠ control de Cerberus sobre el activo concreto</em>.</p><div class="actions"><a class="button" href="../haya-cerberus/">HAYA / Cerberus</a><a class="button secondary" href="../uria-menendez/">Uría · panorama</a><a class="button secondary" href="../../evidence/uria-ricpe-sun-park/2015-creditor-haya-uria-source-note.md">Fuente y contraprueba 2015</a><a class="button secondary" href="../../evidence/uria-ricpe-sun-park/caixabank-defence-20240129-source-note.md">Defensa CaixaBank 2024</a><a class="button secondary" href="../../evidence/uria-ricpe-sun-park/control21-09jul2026-xii-bis-translation.md">Control 21 + traducción</a><a class="button secondary" href="../../data/puzzle/uria-haya-puzzle-registry.json">Registro estructurado</a></div></div>`);
  } else {
    add(main, `<div class="shell"><p class="kicker">UNITARY INTEGRATION · 4 SEPTEMBER 2026</p><h2>HAYA / Cerberus + the 2015, 2017 and 2024 Uría footprints</h2><div class="pressure-maxim"><strong>URÍA MENÉNDEZ DID NOT ENTER THIS HISTORY FOR THE FIRST TIME WITH CAIXABANK'S 2024 DEFENCE.</strong><span> The record preserves reported communications within the creditor/AC perimeter in 2015; primary Uría representation of PH122 inside Concurso 36/2012 in 2017; documented RICPE advice in 2019–2021; CaixaBank's defence in 2024; and a judicial production request in 2026.</span></div><p><strong>2015 counter-evidence that must be read with the connection:</strong> the contemporaneous thread reports a HAYA → case-material → Uría Madrid path and reported Javier González involvement; however, on 30 April 2015 Cuatrecasas reported after speaking with Uría that Uría <em>did not yet have instructions to take any action on HAYA's behalf</em>. Uría's April 2015 client and mandate therefore cannot be presumed.</p><p><strong>Canonical entity:</strong> URÍA MENÉNDEZ ABOGADOS, S.L.P. · NIF B28563963.</p><p><strong>Status:</strong> DOCUMENTED MULTI-ROLE OVERLAP — CONFLICT / CONFIDENTIALITY REVIEW REQUIRED. Repeated involvement does not itself prove conflict, coordination or wrongdoing; client, mandate, information received, barriers and conflict process must be reconstructed matter by matter.</p><p><strong>HAYA / Cerberus:</strong> the separate Spanish deep-dive preserves the rule <em>servicing/contact ≠ title ≠ asset-specific mandate ≠ Cerberus control of the specific asset</em>.</p><div class="actions"><a class="button" href="../../es/haya-cerberus/">HAYA / Cerberus (ES)</a><a class="button secondary" href="../../es/uria-menendez/">Uría overview (ES)</a><a class="button secondary" href="../../evidence/uria-ricpe-sun-park/2015-creditor-haya-uria-source-note.md">2015 source + counter-evidence</a><a class="button secondary" href="../../evidence/uria-ricpe-sun-park/caixabank-defence-20240129-source-note.md">2024 CaixaBank defence</a><a class="button secondary" href="../../evidence/uria-ricpe-sun-park/control21-09jul2026-xii-bis-translation.md">Control 21 + translation</a><a class="button secondary" href="../../data/puzzle/uria-haya-puzzle-registry.json">Structured registry</a></div></div>`);
  }
})();
