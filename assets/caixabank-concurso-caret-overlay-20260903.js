(() => {
  'use strict';

  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  const localPath = path.startsWith('/por-derecho/') ? path : `/por-derecho${path.startsWith('/') ? '' : '/'}${path}`;
  const routes = new Set([
    '/por-derecho/es/reclamacion-caixabank-valencia/',
    '/por-derecho/en/caixabank-valencia-claim/',
    '/por-derecho/es/reclamacion-caixabank-valencia/senalamiento-28-enero-2027/',
    '/por-derecho/es/caixabank-concurso-efecto-domino/',
    '/por-derecho/en/caixabank-insolvency-ripple/',
    '/por-derecho/es/insolvencia-lpb/',
    '/por-derecho/en/lpb-insolvency/',
    '/por-derecho/es/acreedor-de-registro/',
    '/por-derecho/en/lender-of-record/',
    '/por-derecho/es/convergencia-venta-acreedor/',
    '/por-derecho/en/sale-lender-convergence/',
    '/por-derecho/es/objetivos-recuperacion-restitucion/',
    '/por-derecho/en/recovery-restitution-objectives/',
    '/por-derecho/es/concurso-36-2012-separacion-administrador-concursal-rpl-3304-2025/',
    '/por-derecho/en/insolvency-36-2012-administrator-removal-rpl-3304-2025/',
    '/por-derecho/es/concurso-36-2012-administrador-concursal/',
    '/por-derecho/en/insolvency-36-2012-insolvency-administrator/',
    '/por-derecho/es/concurso-36-2012-separacion-ac-honorarios/',
    '/por-derecho/en/insolvency-36-2012-administrator-removal-fees/'
  ]);
  if (!routes.has(localPath)) return;
  if (document.documentElement.dataset.caixaConcursoCaret === '20260903a') return;
  document.documentElement.dataset.caixaConcursoCaret = '20260903a';

  const base = '/por-derecho';
  const isEs = localPath.includes('/es/');
  const registryHref = isEs ? `${base}/es/registro-identidad-materia/` : `${base}/en/matter-identity-registry/`;

  const identities = [
    { id: 'PD-SP-P-0010', labels: ['Francisco de Borja Rodríguez-Batllori Laffitte'] },
    { id: 'PD-SP-O-0001', labels: ['Aweswell Limited', 'Aweswell'] },
    { id: 'PD-SP-O-0002', labels: ['Luchy Playa Blanca, S.L.U.', 'Luchy Playa Blanca, S.L.', 'LPB'] },
    { id: 'PD-SP-O-0007', labels: ['Construcciones Acosta Matos, S.A.', 'CAM'] },
    { id: 'PD-SP-O-0021', labels: ['Promontoria Holding 122 B.V.', 'PH122'] },
    { id: 'PD-SP-O-0029', labels: ['Bankia, S.A.', 'Bankia'] },
    { id: 'PD-SP-O-0030', labels: ['Sociedad de Gestión de Activos Procedentes de la Reestructuración Bancaria, S.A.', 'SAREB'] },
    { id: 'PD-SP-O-0032', labels: ['CAIXABANK, S.A.', 'CaixaBank, S.A.', 'CaixaBank'] },
    { id: 'PD-SP-R-0001', labels: ['Concurso 36/2012', 'Insolvency 36/2012'] },
    { id: 'PD-SP-R-0008', labels: ['ORD 1859/2023-9', '1859/2023-9'] },
    { id: 'PD-SP-R-0011', labels: ['RPL 3304/2025'] },
    { id: 'PD-SP-R-0012', labels: ['RPL 3319/2025'] },
    { id: 'PD-SP-I-0049', labels: ['Juzgado de Primera Instancia nº 27 de Valencia', 'JPI no.27 Valencia', 'JPI nº 27 Valencia'] }
  ];

  const candidates = identities
    .flatMap(item => item.labels.map(label => ({ id: item.id, label })))
    .sort((a, b) => b.label.length - a.label.length);

  const skipTags = new Set(['SCRIPT', 'STYLE', 'SUP', 'CODE', 'PRE', 'TEXTAREA', 'NOSCRIPT']);

  const makeToken = (text, id) => {
    const span = document.createElement('span');
    span.className = 'pd-caret-identity';
    span.dataset.caeprId = id;
    span.dataset.caretState = 'CARET_CONFIRMED';
    span.title = `${id} · CARET_CONFIRMED`;
    span.append(document.createTextNode(text));
    const sup = document.createElement('sup');
    sup.textContent = '^';
    sup.setAttribute('aria-label', ` identidad ${id} confirmada`);
    span.append(sup);
    return span;
  };

  const specialCombinedAppeals = (text) => {
    if (text !== 'RPL 3304/3319') return null;
    const frag = document.createDocumentFragment();
    frag.append(makeToken('RPL 3304/2025', 'PD-SP-R-0011'));
    frag.append(document.createTextNode(' + '));
    frag.append(makeToken('RPL 3319/2025', 'PD-SP-R-0012'));
    return frag;
  };

  const findNext = (text, from) => {
    let best = null;
    for (const candidate of candidates) {
      const index = text.indexOf(candidate.label, from);
      if (index < 0) continue;
      if (!best || index < best.index || (index === best.index && candidate.label.length > best.label.length)) {
        best = { ...candidate, index };
      }
    }
    const combinedIndex = text.indexOf('RPL 3304/3319', from);
    if (combinedIndex >= 0 && (!best || combinedIndex < best.index)) {
      best = { label: 'RPL 3304/3319', id: null, index: combinedIndex, special: true };
    }
    return best;
  };

  const processTextNode = (node) => {
    const parent = node.parentElement;
    if (!parent || skipTags.has(parent.tagName) || parent.closest('[data-caepr-id]')) return;
    const text = node.nodeValue || '';
    if (!text.trim()) return;

    let cursor = 0;
    let match = findNext(text, cursor);
    if (!match) return;

    const frag = document.createDocumentFragment();
    while (match) {
      if (match.index > cursor) frag.append(document.createTextNode(text.slice(cursor, match.index)));
      if (match.special) {
        frag.append(specialCombinedAppeals(match.label));
      } else {
        frag.append(makeToken(match.label, match.id));
      }
      cursor = match.index + match.label.length;
      match = findNext(text, cursor);
    }
    if (cursor < text.length) frag.append(document.createTextNode(text.slice(cursor)));
    node.replaceWith(frag);
  };

  const processRoot = (root) => {
    if (!root) return;
    if (root.nodeType === Node.TEXT_NODE) {
      processTextNode(root);
      return;
    }
    if (!(root instanceof Element) && root !== document.body) return;
    if (root instanceof Element && (skipTags.has(root.tagName) || root.matches('[data-caepr-id]'))) return;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(processTextNode);
  };

  const style = document.createElement('style');
  style.setAttribute('data-caixabank-concurso-caret-style', '20260903a');
  style.textContent = `
    .pd-caret-identity{white-space:normal}.pd-caret-identity>sup{font-weight:900;color:#8c2f2c;margin-left:.06em;font-size:.72em;line-height:0}.pd-caret-control{max-width:1180px;margin:.75rem auto;padding:0 1rem}.pd-caret-control>div{border-left:5px solid #245c49;background:#eef4f2;padding:.75rem 1rem;border-radius:10px;font-size:.9rem}.pd-caret-control a{font-weight:800}
  `;
  document.head.appendChild(style);

  const addControl = () => {
    const main = document.querySelector('main');
    if (!main || main.querySelector('[data-caixabank-caret-control="20260903a"]')) return;
    const control = document.createElement('div');
    control.className = 'pd-caret-control';
    control.setAttribute('data-caixabank-caret-control', '20260903a');
    control.innerHTML = isEs
      ? `<div><strong>^ Control de identidad activo.</strong> Las identidades exactas y fuente-cerradas de este carril se muestran con su caret e ID inmutable PD-SP. Las etiquetas de perímetro cuya persona jurídica exacta siga abierta no se elevan artificialmente a ^. <a href="${registryHref}">Abrir registro canónico →</a></div>`
      : `<div><strong>^ Identity control active.</strong> Exact, source-locked identities on this track are shown with their caret and immutable PD-SP ID. Perimeter labels whose exact legal entity remains open are not artificially promoted to ^. <a href="${registryHref}">Open canonical registry →</a></div>`;
    const first = main.firstElementChild;
    if (first) first.insertAdjacentElement('afterend', control);
    else main.appendChild(control);
  };

  processRoot(document.body);
  addControl();
  processRoot(document.body);

  const observer = new MutationObserver(mutations => {
    for (const mutation of mutations) {
      mutation.addedNodes.forEach(processRoot);
    }
  });
  observer.observe(document.body, { childList: true, subtree: true });
  window.setTimeout(() => observer.disconnect(), 5000);
})();
