(() => {
  'use strict';
  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  const relevant = path.endsWith('/en/caixabank-valencia-claim/documents/')
    || path.endsWith('/en/caixabank-valencia-claim/faq-unitary-context/')
    || path.endsWith('/en/caixabank-valencia-claim/ob-rem-ac-cam-28nov2018/');
  if (!relevant) return;

  const fix = () => {
    document.querySelectorAll('a[href="../lender-of-record/"]').forEach(a => a.setAttribute('href','../../lender-of-record/'));
    document.querySelectorAll('a[href="../insolvency-lpb/"]').forEach(a => a.setAttribute('href','../../insolvency-lpb/'));
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fix, {once:true});
  else fix();
})();
