/* ISOLATED BRANCH EXPERIMENT · no main/publication claim · 2026-09-26 */
(() => {
  'use strict';

  const VERSION = '20260926a';
  const ALLOWED = [
    /\/en\/estate-payment-counsel-independence\/?(?:index\.html)?$/,
    /\/es\/pago-masa-independencia-defensa\/?(?:index\.html)?$/,
    /\/en\/insolvency-36-2012-ac-opposition-lpb-appeal-september-2026\/?(?:index\.html)?$/,
    /\/es\/concurso-36-2012-oposicion-ac-apelacion-lpb-septiembre-2026\/?(?:index\.html)?$/
  ];
  if (!ALLOWED.some((re) => re.test(location.pathname))) return;
  if (document.querySelector('[data-pd-puzzle-promo]')) return;

  const source = document.currentScript;
  if (!source) return;

  const root = new URL('../', source.src);
  const es = /\/es\//.test(location.pathname);
  const puzzleUrl = new URL(es ? 'es/puzzle/#p2' : 'en/puzzle/#p2', root).href;
  const params = new URLSearchParams(location.search);
  const force = params.get('puzzlePromo') === '1';
  if (params.get('puzzlePromo') === '0') return;

  const STORAGE_KEY = 'pd:puzzle-promo:20260926';
  const TTL = 7 * 24 * 60 * 60 * 1000;
  const now = Date.now();

  const isSuppressed = () => {
    if (force) return false;
    try {
      const stamp = Number(localStorage.getItem(STORAGE_KEY) || 0);
      return Number.isFinite(stamp) && stamp > 0 && now - stamp < TTL;
    } catch (_) {
      return false;
    }
  };
  if (isSuppressed()) return;

  const copy = es ? {
    eyebrow: 'PUZZLE · 32 PÁGINAS',
    title: 'Sigue las conexiones',
    body: 'Un activo. Vías paralelas. Lee el mapa probatorio.',
    cta: 'Explorar →',
    open: 'Abrir el PUZZLE de 32 páginas',
    close: 'Cerrar promoción del PUZZLE'
  } : {
    eyebrow: 'PUZZLE · 32 PAGES',
    title: 'Follow the connections',
    body: 'One asset. Parallel tracks. Read the evidence map.',
    cta: 'Explore →',
    open: 'Open the 32-page PUZZLE',
    close: 'Close PUZZLE promotion'
  };

  const style = document.createElement('style');
  style.setAttribute('data-pd-puzzle-promo-style', VERSION);
  style.textContent = `
    .pd-puzzle-promo{
      --pp-ink:#102a35;
      --pp-gold:#f0c54a;
      --pp-paper:#fffdf5;
      position:fixed;
      left:calc(12px + env(safe-area-inset-left,0px));
      bottom:calc(12px + env(safe-area-inset-bottom,0px));
      z-index:74;
      width:min(196px,calc(100vw - 24px));
      opacity:0;
      transform:translate3d(0,18px,0) scale(.97);
      pointer-events:none;
      transition:opacity .24s ease,transform .24s ease;
      font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
      filter:drop-shadow(0 14px 24px rgba(5,24,34,.24));
    }
    .pd-puzzle-promo[data-visible="true"]{
      opacity:1;
      transform:none;
      pointer-events:auto;
    }
    .pd-puzzle-promo[data-paused="true"]{
      opacity:0;
      transform:translate3d(0,14px,0) scale(.97);
      pointer-events:none;
    }
    .pd-puzzle-promo__link{
      display:block;
      position:relative;
      overflow:hidden;
      color:var(--pp-ink);
      background:
        radial-gradient(circle at 82% 12%,rgba(255,255,255,.72) 0 5%,transparent 6%),
        linear-gradient(145deg,#f6d55e 0%,var(--pp-gold) 56%,#e9b52b 100%);
      border:1px solid rgba(16,42,53,.18);
      border-radius:31px 38px 25px 42px / 35px 28px 40px 31px;
      padding:16px 15px 13px;
      text-decoration:none;
      min-height:164px;
      isolation:isolate;
    }
    .pd-puzzle-promo__link:focus-visible,
    .pd-puzzle-promo__close:focus-visible{
      outline:3px solid #0b5e72;
      outline-offset:3px;
    }
    .pd-puzzle-promo__network{
      display:block;
      width:100%;
      height:54px;
      margin:-2px 0 8px;
    }
    .pd-puzzle-promo__network path{stroke:rgba(16,42,53,.52);stroke-width:2;fill:none}
    .pd-puzzle-promo__network circle{fill:var(--pp-ink)}
    .pd-puzzle-promo__network circle:nth-of-type(2n){fill:#fff8dc;stroke:var(--pp-ink);stroke-width:2}
    .pd-puzzle-promo__eyebrow{
      display:block;
      font-size:.66rem;
      line-height:1.2;
      letter-spacing:.13em;
      font-weight:900;
      text-transform:uppercase;
    }
    .pd-puzzle-promo__title{
      display:block;
      margin:.22rem 0 .25rem;
      font:700 1.1rem/1.04 Georgia,"Times New Roman",serif;
      letter-spacing:-.02em;
    }
    .pd-puzzle-promo__body{
      display:block;
      max-width:18ch;
      font-size:.73rem;
      line-height:1.34;
      font-weight:650;
    }
    .pd-puzzle-promo__cta{
      display:inline-block;
      margin-top:.72rem;
      padding:.38rem .56rem;
      border-radius:999px;
      background:var(--pp-ink);
      color:#fff;
      font-size:.7rem;
      line-height:1;
      font-weight:900;
      letter-spacing:.045em;
      text-transform:uppercase;
    }
    .pd-puzzle-promo__close{
      position:absolute;
      top:-9px;
      right:-9px;
      z-index:2;
      width:44px;
      height:44px;
      display:grid;
      place-items:center;
      border:1px solid rgba(16,42,53,.28);
      border-radius:50%;
      background:var(--pp-paper);
      color:var(--pp-ink);
      box-shadow:0 5px 14px rgba(5,24,34,.2);
      font:800 1rem/1 system-ui,sans-serif;
      cursor:pointer;
    }
    @media (hover:hover){
      .pd-puzzle-promo__link:hover{transform:translateY(-1px)}
    }
    @media (max-width:1024px){
      .pd-puzzle-promo{width:min(174px,28vw)}
      .pd-puzzle-promo__link{min-height:148px;padding:14px 13px 12px}
      .pd-puzzle-promo__network{height:47px;margin:-1px 0 6px}
      .pd-puzzle-promo__title{font-size:1rem}
      .pd-puzzle-promo__body{font-size:.68rem}
    }
    @media (max-width:700px){
      .pd-puzzle-promo{
        width:min(124px,34vw);
        left:calc(9px + env(safe-area-inset-left,0px));
        bottom:calc(9px + env(safe-area-inset-bottom,0px));
      }
      .pd-puzzle-promo__link{
        min-height:110px;
        padding:10px 9px 9px;
        border-radius:24px 29px 20px 31px / 27px 22px 30px 24px;
      }
      .pd-puzzle-promo__network{height:33px;margin:0 0 4px}
      .pd-puzzle-promo__eyebrow{font-size:.55rem;letter-spacing:.08em}
      .pd-puzzle-promo__title{font-size:.88rem;margin:.14rem 0 .2rem}
      .pd-puzzle-promo__body{display:none}
      .pd-puzzle-promo__cta{margin-top:.3rem;font-size:.53rem;padding:.3rem .4rem}
      .pd-puzzle-promo__close{top:-8px;right:-8px}
    }
    @media (max-width:380px){
      .pd-puzzle-promo{width:min(112px,32vw)}
      .pd-puzzle-promo__link{min-height:100px;padding:9px 8px 8px}
      .pd-puzzle-promo__network{height:29px;margin:0 0 3px}
      .pd-puzzle-promo__title{font-size:.82rem}
      .pd-puzzle-promo__cta{font-size:.54rem}
    }
    @media (max-height:500px){
      .pd-puzzle-promo{width:112px}
      .pd-puzzle-promo__link{min-height:84px;padding:8px 8px 7px}
      .pd-puzzle-promo__network{height:25px;margin:0 0 3px}
      .pd-puzzle-promo__eyebrow{font-size:.5rem;white-space:nowrap}
      .pd-puzzle-promo__title,.pd-puzzle-promo__body{display:none}
      .pd-puzzle-promo__cta{margin-top:.28rem;font-size:.52rem;padding:.28rem .38rem}
    }
    @media (prefers-reduced-motion:reduce){
      .pd-puzzle-promo{transition:none;transform:none}
      .pd-puzzle-promo__link{transform:none!important}
    }
    @media print{
      .pd-puzzle-promo{display:none!important}
    }
  `;
  document.head.appendChild(style);

  const promo = document.createElement('aside');
  promo.className = 'pd-puzzle-promo';
  promo.dataset.pdPuzzlePromo = VERSION;
  promo.dataset.visible = 'false';
  promo.setAttribute('aria-label', es ? 'Promoción del PUZZLE' : 'PUZZLE promotion');
  promo.innerHTML = `
    <button class="pd-puzzle-promo__close" type="button" aria-label="${copy.close}" title="${copy.close}">×</button>
    <a class="pd-puzzle-promo__link" href="${puzzleUrl}" aria-label="${copy.open}">
      <svg class="pd-puzzle-promo__network" viewBox="0 0 180 66" role="img" aria-label="">
        <path d="M13 48 L46 20 L77 43 L112 17 L164 39 M46 20 L112 17 M77 43 L164 39 M13 48 L112 17"/>
        <circle cx="13" cy="48" r="6"/><circle cx="46" cy="20" r="7"/><circle cx="77" cy="43" r="6"/>
        <circle cx="112" cy="17" r="7"/><circle cx="164" cy="39" r="6"/>
      </svg>
      <span class="pd-puzzle-promo__eyebrow">${copy.eyebrow}</span>
      <strong class="pd-puzzle-promo__title">${copy.title}</strong>
      <span class="pd-puzzle-promo__body">${copy.body}</span>
      <span class="pd-puzzle-promo__cta">${copy.cta}</span>
    </a>
  `;
  document.body.appendChild(promo);

  // R33's sticky source viewer is evidence-first. Do not cover the PDF while it is
  // in the viewport; the promo returns automatically above/below that workbench.
  // A geometry check is used instead of relying only on IntersectionObserver so
  // WebKit, Chromium and Firefox behave identically during scripted/manual scroll.
  const evidenceViewer = document.querySelector('[data-rpl3304-forensic-reader]');
  if (evidenceViewer) {
    let pauseFrame = 0;
    const syncPause = () => {
      pauseFrame = 0;
      const rect = evidenceViewer.getBoundingClientRect();
      const intersectsViewport = rect.bottom > 0 && rect.top < window.innerHeight;
      promo.dataset.paused = String(intersectsViewport);
    };
    const queuePause = () => {
      if (pauseFrame) return;
      pauseFrame = requestAnimationFrame(syncPause);
    };
    window.addEventListener('scroll', queuePause, {passive:true});
    window.addEventListener('resize', queuePause, {passive:true});
    requestAnimationFrame(syncPause);
  }

  const emit = (action) => {
    try {
      window.dispatchEvent(new CustomEvent('pd:puzzle-promo', {
        detail: {action, version: VERSION, path: location.pathname}
      }));
    } catch (_) {}
  };

  let shown = false;
  const show = () => {
    if (shown || !promo.isConnected) return;
    shown = true;
    promo.dataset.visible = 'true';
    emit('impression');
    window.removeEventListener('scroll', onScroll);
  };
  const onScroll = () => {
    const h = Math.max(document.documentElement.scrollHeight, document.body.scrollHeight);
    const progress = h > innerHeight ? (scrollY + innerHeight) / h : 1;
    if (progress >= .22) show();
  };

  promo.querySelector('.pd-puzzle-promo__close').addEventListener('click', () => {
    try { localStorage.setItem(STORAGE_KEY, String(Date.now())); } catch (_) {}
    emit('dismiss');
    promo.remove();
  });
  promo.querySelector('.pd-puzzle-promo__link').addEventListener('click', () => emit('open'));

  if (force) {
    requestAnimationFrame(show);
  } else {
    window.addEventListener('scroll', onScroll, {passive:true});
    window.setTimeout(show, 8000);
  }
})();