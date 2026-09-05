(() => {
  'use strict';
  const script = document.currentScript;
  if (!script) return;
  const root = new URL('../', script.src);
  const path = location.pathname.replace(/index\.html$/, '');
  const es = path.includes('/es/reclamacion-caixabank-valencia/');
  const en = path.includes('/en/caixabank-valencia-claim/');
  if (!es && !en) return;
  const landing = path.endsWith('/es/reclamacion-caixabank-valencia/') || path.endsWith('/en/caixabank-valencia-claim/');
  const srcdir = 'assets/evidence/caixabank-valencia-publica-20260905/';
  const names = {
    'IQA_jgn9nZ7HS5RT7byXZwJ4AXG2kA1SGMZOfENKOQAc_80': 'caixabank-demanda-oct2023-publica-20260905.pdf',
    'IQDp2mBSGL5GQ5cNBhcEiVKrAcn8t1WXaYOaZCDghdJjo8Q': 'caixabank-contestacion-ene2024-publica-20260905.pdf',
    'IQBAYqfoXeLLSYqnpI5fm2CDAa1iTqAOPpKsimc7sp94dZc': 'caixabank-ac-25ene2021-publica-20260905.pdf'
  };
  const apply = () => {
    // A stale cached landing-only module must not build duplicate outreach on a source subpage.
    const outreach = document.getElementById('caixabank-adr-settlement-outreach');
    if (!landing && outreach) outreach.remove();
    document.querySelectorAll('a[href]').forEach(a => {
      let desired = null;
      for (const [token, name] of Object.entries(names)) if (a.href.includes(token)) desired = new URL(srcdir + name, root).href;
      if (a.href.includes('/en/insolvency-lpb/')) desired = new URL('en/lpb-insolvency/', root).href;
      if (/\/(?:documentos|faq-contexto-unitario|ob-rem-ac-cam-28nov2018)\/senalamiento-28-enero-2027\//.test(a.href)) desired = new URL('es/reclamacion-caixabank-valencia/senalamiento-28-enero-2027/', root).href;
      if (desired && a.href !== desired) a.href = desired;
    });
    document.querySelectorAll('img').forEach(img => {
      const m = img.src.match(/caixabank-valencia-1859-2023-diligencia-06nov2025-p([12])-publica\.jpg/);
      if (!m) return;
      const desired = new URL(`assets/evidence/caixabank-valencia-1859-2023-diligencia-06nov2025-p${m[1]}-publica.jpg?v=20260905repair`, root).href;
      if (img.src !== desired) img.src = desired;
      img.style.maxWidth = '100%'; img.style.height = 'auto';
    });
    document.querySelectorAll('main table').forEach(table => {
      if (table.closest('.table-wrap,.control-table-wrap,.pd-caixa-table')) return;
      const wrap = document.createElement('div');
      wrap.className = 'pd-caixa-table'; wrap.tabIndex = 0;
      wrap.setAttribute('role', 'region');
      wrap.setAttribute('aria-label', es ? 'Tabla desplazable horizontalmente' : 'Horizontally scrollable table');
      table.before(wrap); wrap.append(table);
    });
  };
  const start = () => {
    apply(); let pending = false;
    new MutationObserver(() => {
      if (pending) return;
      pending = true;
      setTimeout(() => {pending = false; apply();}, 40);
    }).observe(document.querySelector('main') || document.body, {childList:true, subtree:true});
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, {once:true});
  else start();
})();
