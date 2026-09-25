(() => {
  const d = document;
  const en = (d.documentElement.lang || '').toLowerCase().startsWith('en');
  const path = location.pathname.replace(/\/index\.html$/, '/');
  const prefix = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const target = en
    ? `${prefix}en/evidence-pwc-sun-park-meeting-21-april-2016/#sequence`
    : `${prefix}es/evidencia-pwc-junta-sun-park-21-abril-2016/#secuencia`;
  const label = en
    ? 'Open the complete 15–26 April 2016 email-chain analysis. The graphic records the client’s penal-route decision and PwC’s acknowledgement; it is not an independent PwC finding of an offence.'
    : 'Abrir el análisis completo de la cadena de correos de 15–26 abril 2016. El gráfico documenta la decisión de vía penal del cliente y el acuse de PwC; no es una conclusión independiente de PwC sobre delito.';

  const linkImage = image => {
    if (!(image instanceof HTMLImageElement) || !image.src.includes('pwc-five-actors-plus-ac-2016-knowledge-checkpoint')) return;
    let link = image.closest('a');
    if (!link) {
      link = d.createElement('a');
      image.parentNode.insertBefore(link, image);
      link.append(image);
    }
    link.href = target;
    link.dataset.pwcAprilChainLink = '20260822';
    if (!link.querySelector('span, figcaption')) link.setAttribute('aria-label', label);
  };

  const scan = root => {
    if (root instanceof HTMLImageElement) linkImage(root);
    if (root.querySelectorAll) root.querySelectorAll('img[src*="pwc-five-actors-plus-ac-2016-knowledge-checkpoint"]').forEach(linkImage);
  };

  const start = () => {
    scan(d);
    if (d.readyState === 'complete') return;
    const observer = new MutationObserver(records => {
      records.forEach(record => record.addedNodes.forEach(node => {
        if (node.nodeType === Node.ELEMENT_NODE) scan(node);
      }));
    });
    observer.observe(d.body, { childList: true, subtree: true });
    window.addEventListener('load', () => {
      scan(d);
      observer.disconnect();
    }, { once: true });
  };

  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', start, { once: true });
  else start();
})();
