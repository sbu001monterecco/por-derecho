(() => {
  const path = window.location.pathname.replace(/\/+$/, '/');
  const id = 'prescription-caducity-recovery-26aug2026';
  if (document.getElementById(id)) return;

  const isEs = path.includes('/es/');
  const isEn = path.includes('/en/');
  if (!isEs && !isEn) return;

  if (path.includes('/prescripcion-caducidad-danos-medidas-cautelares/') ||
      path.includes('/limitation-prescription-damages-interim-relief/')) return;

  const relevant = [
    'retracto', 'article-1535', 'articulo-1535', 'acreedor-de-registro', 'lender-of-record',
    'administrador-concursal', 'insolvency-administrator', 'acosta-matos',
    'recuperacion-restitucion', 'recovery-restitution', 'toma-control', 'takeover',
    'insolvencia-lpb', 'lpb-insolvency', 'comunidad', 'community', 'cexp', 'explotacion', 'exploitation',
    'penal', 'criminal', 'fiscalia', 'prosecution', 'dp1901', 'dp-1901',
    'magistrado', 'judge', 'responsabilidad-institucional', 'institutional-accountability',
    'lender-liability', 'responsabilidad-prestamista', 'ricpe', 'mismo-hotel', 'same-hotel',
    'adjudicacion', 'adjudication', 'calificacion', 'calificación'
  ];
  if (!relevant.some(fragment => path.includes(fragment))) return;

  const style = document.createElement('style');
  style.textContent = `
    #${id}{background:#edf2f3}
    #${id} .pcr-wrap{max-width:1120px;margin:0 auto}
    #${id} .pcr-shell{background:#13252d;color:#fff;border-radius:18px;padding:1.1rem 1.3rem;box-shadow:0 10px 28px rgba(19,37,45,.10)}
    #${id} .pcr-label{display:inline-block;color:#13252d;background:#f0dfc4;border-radius:999px;padding:.28rem .58rem;font-size:.72rem;font-weight:850;letter-spacing:.06em;text-transform:uppercase}
    #${id} h2{color:#fff;margin:.65rem 0 .55rem;font-size:1.35rem}
    #${id} p{line-height:1.55;margin:.45rem 0}
    #${id} .pcr-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.65rem;margin:.9rem 0}
    #${id} .pcr-card{background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.18);border-radius:12px;padding:.75rem .8rem;font-size:.9rem;overflow-wrap:anywhere}
    #${id} .pcr-card strong{display:block;color:#f0dfc4;margin-bottom:.25rem}
    #${id} .pcr-boundary{background:#fff8e8;color:#13252d;border-left:5px solid #c58a39;border-radius:0 12px 12px 0;padding:.8rem .9rem;margin:.8rem 0}
    #${id} .pcr-actions{display:flex;flex-wrap:wrap;gap:.6rem;margin-top:.8rem}
    #${id} .pcr-actions a{display:inline-block;background:#fff;color:#13252d;text-decoration:none;font-weight:800;border-radius:999px;padding:.56rem .84rem}
    @media(max-width:900px){#${id} .pcr-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
    @media(max-width:600px){#${id} .pcr-grid{grid-template-columns:1fr}}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.id = id;
  section.className = 'section';

  section.innerHTML = isEs ? `
    <div class="shell pcr-wrap"><div class="pcr-shell">
      <span class="pcr-label">PRESERVACIÓN DE DERECHOS · NO HAY UN SOLO RELOJ</span>
      <h2>Penal, civil, caducidad, AC y daños siguen reglas temporales distintas.</h2>
      <p>Por Derecho no sostiene que una denuncia penal “congele todo”. Cada acción exige identificar titular, demandado, Día Cero, plazo, acto de interrupción o suspensión y remedio.</p>
      <div class="pcr-grid">
        <div class="pcr-card"><strong>Penal · arts. 131–132 CP</strong>La interrupción depende de la judicialización y de los requisitos legales. Una denuncia ordinaria a Fiscalía o Policía no se presenta como interrupción automática.</div>
        <div class="pcr-card"><strong>Civil · art. 1973 CC</strong>Demanda, reclamación extrajudicial o reconocimiento pueden interrumpir. La causa penal puede afectar la prescripción civil cuando existe el puente jurídico de mismos hechos.</div>
        <div class="pcr-card"><strong>Caducidad</strong>Art. 1535, art. 1524 y otros plazos breves se analizan por separado. La causa penal no los suspende automáticamente ni revive un derecho extinguido.</div>
        <div class="pcr-card"><strong>Recuperación</strong>Restitución, daños y cautelares deben ser proporcionales, trazables y sin doble conteo, con legitimación separada para LPB, Aweswell, Matkator, CEXP y terceros.</div>
      </div>
      <div class="pcr-boundary"><strong>Pregunta operativa:</strong> ¿qué activo, título, ingreso, prueba o valor será más difícil de recuperar si no se adopta ahora una actuación legalmente eficaz para preservar el derecho o asegurar la reparación final?</div>
      <div class="pcr-actions"><a href="/por-derecho/es/prescripcion-caducidad-danos-medidas-cautelares/">Abrir análisis completo →</a></div>
    </div></div>` : `
    <div class="shell pcr-wrap"><div class="pcr-shell">
      <span class="pcr-label">RIGHTS PRESERVATION · THERE IS NO SINGLE CLOCK</span>
      <h2>Criminal, civil, caducity, IA liability and damages follow different temporal rules.</h2>
      <p>Por Derecho does not say that a criminal complaint “freezes everything”. Each claim requires the claimant, defendant, Day Zero, statutory period, legally effective interruption/suspension event and remedy.</p>
      <div class="pcr-grid">
        <div class="pcr-card"><strong>Criminal · arts. 131–132</strong>Interruption depends on judicialisation and the statutory requirements. An ordinary report to the prosecutor or police is not presented as automatic interruption.</div>
        <div class="pcr-card"><strong>Civil · art. 1973</strong>Court action, extrajudicial demand or acknowledgment can interrupt. Criminal proceedings can affect civil prescription where the same-facts legal bridge exists.</div>
        <div class="pcr-card"><strong>Caducity</strong>Article 1535, article 1524 and other short periods are separate. Criminal proceedings do not automatically suspend them or revive an expired right.</div>
        <div class="pcr-card"><strong>Recovery</strong>Restitution, damages and interim relief must be proportionate, traceable and free from double counting, with standing separated among LPB, Aweswell, Matkator, CEXP and third parties.</div>
      </div>
      <div class="pcr-boundary"><strong>Operational question:</strong> what asset, title, income stream, evidence or value will be harder to recover if no legally effective preservation or security step is taken now?</div>
      <div class="pcr-actions"><a href="/por-derecho/en/limitation-prescription-damages-interim-relief/">Open full analysis →</a></div>
    </div></div>`;

  const main = document.querySelector('main');
  if (!main) return;
  const anchors = [
    main.querySelector(':scope > .hero'),
    main.querySelector(':scope > section.hero'),
    main.querySelector(':scope > .dossier-hero'),
    main.querySelector(':scope > section.dossier-hero')
  ].filter(Boolean);
  if (anchors.length) anchors[0].insertAdjacentElement('afterend', section);
  else main.appendChild(section);
})();
