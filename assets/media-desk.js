/* Only the existing media-desk fragment: preserve all shared content and user scroll intent. */
(() => {
  'use strict';
  if (!document.body.classList.contains('media-desk-page')) return;
  const title = document.getElementById('media-desk-title');
  const main = document.querySelector('main');
  if (!title || !main) return;
  let armed = false, deadline = 0, scheduled = 0, expiry = 0;
  const observer = new MutationObserver(() => schedule());
  const stop = () => { armed = false; observer.disconnect(); clearTimeout(scheduled); clearTimeout(expiry); };
  const align = () => {
    scheduled = 0;
    if (!armed || location.hash !== '#media-desk' || performance.now() > deadline) return;
    const header = document.querySelector('.site-header');
    const clearance = Math.max(20, header ? header.getBoundingClientRect().bottom + 20 : 20);
    const top = Math.max(0, window.scrollY + title.getBoundingClientRect().top - clearance);
    if (Math.abs(window.scrollY - top) > 2) window.scrollTo({top, behavior:'instant'});
  };
  function schedule() { if (armed) { clearTimeout(scheduled); scheduled = setTimeout(align, 100); } }
  const arm = (duration = 10000) => {
    stop();
    if (location.hash !== '#media-desk') return;
    armed = true; deadline = performance.now() + duration;
    observer.observe(main, {childList:true, subtree:true});
    expiry = setTimeout(stop, duration);
    schedule();
  };
  // Stop following layout changes as soon as the reader takes scroll/focus control.
  ['wheel','touchstart','pointerdown','keydown'].forEach(type => window.addEventListener(type, stop, {passive:true}));
  window.addEventListener('hashchange', () => arm());
  document.addEventListener('click', event => {
    const link = event.target.closest && event.target.closest('a[href]');
    if (!link) return;
    const target = new URL(link.href, location.href);
    if (target.origin === location.origin && target.pathname === location.pathname && target.hash === '#media-desk') {
      setTimeout(() => arm(2000), 0);
    }
  });
  arm();
})();
