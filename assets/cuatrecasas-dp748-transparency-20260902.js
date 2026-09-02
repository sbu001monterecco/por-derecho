(() => {
  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  const targets = [
    '/es/cuatrecasas-sun-park/',
    '/en/cuatrecasas-sun-park/',
    '/es/cuatrecasas-dp748-accion-civil/',
    '/en/cuatrecasas-dp748-civil-action/'
  ];
  if (!targets.some(t => path.includes(t))) return;
  if (document.querySelector('[data-dp748-transparency-overlay="20260902"]')) return;

  const es = path.includes('/es/');
  const isMain = path.includes('/cuatrecasas-sun-park/');
  const hub = es
    ? '/por-derecho/es/cuatrecasas-dp748-transparencia-2026/'
    : '/por-derecho/en/cuatrecasas-dp748-transparency-2026/';
  const draft = '/por-derecho/docs/cuatrecasas/DP748/2026-09-02_borrador_apelacion_propuesta.md';
  const agenda = '/por-derecho/docs/cuatrecasas/DP748/2026-09-03_lawyer_call_agenda.md';

  const style = document.createElement('style');
  style.textContent = `
    .dp748t{background:linear-gradient(135deg,#f6faf8,#fff8e6);border-top:1px solid #dce6e1;border-bottom:1px solid #ded8c9}.dp748t .dp748t-shell{max-width:1160px;margin:0 auto;padding:clamp(1.3rem,4vw,2.4rem) 1.1rem}.dp748t-head{display:flex;gap:1rem;justify-content:space-between;align-items:flex-start;flex-wrap:wrap}.dp748t-kicker{font-size:.76rem;font-weight:800;letter-spacing:.05em;text-transform:uppercase;color:#80621d;margin:0 0 .35rem}.dp748t h2{margin:.1rem 0 .55rem;max-width:880px}.dp748t-lead{font-size:1.05rem;line-height:1.65;max-width:980px}.dp748t-badge{display:inline-block;background:#13252d;color:#fff;border-radius:999px;padding:.4rem .65rem;font-size:.72rem;font-weight:800;letter-spacing:.04em;text-transform:uppercase}.dp748t-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.75rem;margin:1rem 0}.dp748t-card{background:#fff;border:1px solid #dfe3e3;border-radius:14px;padding:.9rem}.dp748t-card strong{display:block;margin-bottom:.25rem}.dp748t-warn{background:#fff;border-left:5px solid #8c2f2c;border-radius:12px;padding:.9rem 1rem;margin:.9rem 0}.dp748t-good{background:#f3faf7;border-left:5px solid #1d5c4a;border-radius:12px;padding:.9rem 1rem;margin:.9rem 0}.dp748t-links{display:flex;gap:.6rem;flex-wrap:wrap;margin-top:1rem}.dp748t-links a{display:inline-block;text-decoration:none;border-radius:999px;padding:.58rem .85rem;font-weight:800;background:#13252d;color:#fff}.dp748t-links a:nth-child(n+2){background:#fff;color:#13252d;border:1px solid #bdc9c6}.dp748t-spine{display:grid;grid-template-columns:repeat(4,1fr);gap:.55rem;margin:.9rem 0}.dp748t-step{position:relative;background:#13252d;color:#fff;border-radius:12px;padding:.8rem}.dp748t-step time{display:block;color:#f2d47e;font-weight:800;font-size:.78rem}.dp748t-step small{color:#dbe7e4}.dp748t-note{font-size:.86rem;color:#4d5558}.dp748t-supersede{font-size:.9rem;background:#fff7df;border-left:5px solid #c48d14;border-radius:10px;padding:.8rem .9rem}@media(max-width:760px){.dp748t-spine{grid-template-columns:1fr 1fr}}@media(max-width:480px){.dp748t-spine{grid-template-columns:1fr}}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.className = 'dp748t';
  section.setAttribute('data-dp748-transparency-overlay','20260902');

  if (es) {
    section.innerHTML = isMain ? `
      <div class="dp748t-shell">
        <div class="dp748t-head"><div><p class="dp748t-kicker">ACTUALIZACIÓN DE TRANSPARENCIA · 2 SEPTIEMBRE 2026</p><h2>DP 748/2026: Auto de 16 julio ya controlado, notificación de 1 septiembre y borrador público de apelación.</h2></div><span class="dp748t-badge">BORRADOR NO PRESENTADO</span></div>
        <p class="dp748t-lead">La revisión posterior a la notificación reduce la hipótesis a una finca, una secuencia corta de escritos y preguntas documentales capaces tanto de confirmar como de descartar engaño. Para apoyar la revisión letrada de 3 septiembre y la vía abierta de solución global con Cuatrecasas, se publica también la contraprueba y cada corrección material.</p>
        <div class="dp748t-spine"><div class="dp748t-step"><time>20 SEP 2024</time><strong>Matkator</strong><small>plantea controversia material</small></div><div class="dp748t-step"><time>17 OCT 2024</time><strong>Adjudicación</strong><small>Cuatrecasas solicita 70 %</small></div><div class="dp748t-step"><time>21 FEB 2025</time><strong>77.840 EUR</strong><small>+ saldo residual alegado</small></div><div class="dp748t-step"><time>25 APR 2025</time><strong>Conocimiento</strong><small>y revelación al juzgado</small></div></div>
        <div class="dp748t-grid"><div class="dp748t-card"><strong>Un solo lote</strong>Finca 8.584 · apartamento histórico 758 · 111.200 EUR.</div><div class="dp748t-card"><strong>No se presume fraude</strong>Conocimiento + continuación de ejecución no basta: falta identificar engaño, manipulación u omisión concreta.</div><div class="dp748t-card"><strong>Corrección adversa preservada</strong>Sí hubo conversaciones directas de deuda con Gil/Aweswell en 2020 y 2022.</div><div class="dp748t-card"><strong>Diligencias escalonadas</strong>Testimonio judicial → identidad 8.584 → personas sólo si queda contradicción.</div></div>
        <p class="dp748t-supersede"><strong>Control de versión:</strong> este aviso supera la línea de 24 agosto que decía que la resolución firmada de 16 julio faltaba del corpus público. La actualización trabaja con esa resolución y registra notificación de 1 septiembre.</p>
        <div class="dp748t-links"><a href="${hub}">Abrir hub transparente DP 748 →</a><a href="${draft}">Borrador completo de apelación →</a><a href="${agenda}">Agenda llamada abogados →</a></div>
      </div>` : `
      <div class="dp748t-shell">
        <div class="dp748t-head"><div><p class="dp748t-kicker">CONTROL POST-NOTIFICACIÓN · 2 SEPTIEMBRE 2026</p><h2>Esta página queda complementada por el hub transparente de apelación.</h2></div><span class="dp748t-badge">AUTO NOTIFICADO 01 SEP</span></div>
        <p class="dp748t-lead">La nueva capa publica el Auto de 16 julio como resolución controlada, corrige el perímetro a un solo lote de subasta, preserva expresamente la contraprueba del escrito de 25 abril y publica el borrador de apelación con notas de revisión para los abogados.</p>
        <div class="dp748t-good"><strong>Regla de prioridad:</strong> cuando una formulación anterior sea incompatible con las siete correcciones de 2 septiembre, rige la versión nueva hasta que un documento primario exija otra corrección.</div>
        <div class="dp748t-links"><a href="${hub}">Ver actualización completa →</a><a href="${draft}">Abrir borrador →</a><a href="${agenda}">Agenda 3 septiembre →</a></div>
      </div>`;
  } else {
    section.innerHTML = isMain ? `
      <div class="dp748t-shell">
        <div class="dp748t-head"><div><p class="dp748t-kicker">TRANSPARENCY UPDATE · 2 SEPTEMBER 2026</p><h2>DP 748/2026: the 16 July order is now controlled, notice was received on 1 September, and the proposed appeal is public for counsel review.</h2></div><span class="dp748t-badge">NOT FILED</span></div>
        <p class="dp748t-lead">The post-notification review narrows the issue to one auction lot, a short sequence of execution filings and documentary questions capable of confirming or excluding deception. The same transparent record is intended to support the 3 September lawyer call and a responsible global-resolution dialogue with Cuatrecasas.</p>
        <div class="dp748t-grid"><div class="dp748t-card"><strong>One auction lot</strong>Registry property 8,584 · historic apartment 758 · EUR 111,200.</div><div class="dp748t-card"><strong>No shortcut to fraud</strong>Knowledge plus continued enforcement is not enough; a concrete deception, manipulation or material omission must be identified.</div><div class="dp748t-card"><strong>Adverse evidence preserved</strong>Debt-resolution discussions with Gil/Aweswell did occur in 2020 and 2022.</div><div class="dp748t-card"><strong>Three-stage test</strong>Certified court record → identity of 8,584 → witness evidence only if a material contradiction remains.</div></div>
        <div class="dp748t-links"><a href="${hub}">Open DP 748 transparency hub →</a><a href="${draft}">Spanish proposed appeal →</a><a href="${agenda}">Lawyer-call agenda →</a></div>
      </div>` : `
      <div class="dp748t-shell"><div class="dp748t-head"><div><p class="dp748t-kicker">POST-NOTIFICATION CONTROL · 2 SEPTEMBER 2026</p><h2>This page is supplemented by the new DP 748 transparency and appeal hub.</h2></div><span class="dp748t-badge">1 SEP NOTICE</span></div><p class="dp748t-lead">The new record incorporates the signed 16 July order, the one-lot correction, the strongest defence and adverse evidence, a finite investigation plan and the proposed Spanish appeal for counsel review.</p><div class="dp748t-links"><a href="${hub}">Open full update →</a><a href="${draft}">Spanish appeal draft →</a></div></div>`;
  }

  const hero = document.querySelector('main .hero');
  if (hero) hero.insertAdjacentElement('afterend', section);
  else document.querySelector('main')?.prepend(section);
})();
