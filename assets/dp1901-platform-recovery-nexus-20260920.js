/* PD-DP1901-PLATFORM-NEXUS-20260920-01: additive, route-scoped reader layer. */
(() => {
  'use strict';
  const script = document.currentScript;
  if (!script || window.__pd1901PlatformNexus) return;
  window.__pd1901PlatformNexus = true;
  const root = new URL('../', script.src);
  const relative = location.pathname.startsWith(root.pathname)
    ? location.pathname.slice(root.pathname.length).replace(/index\.html$/, '').replace(/\/?$/, '/') : '';
  const lang = relative.startsWith('es/') ? 'es' : 'en';
  const element = (tag, text, cls) => {
    const el = document.createElement(tag);
    if (text !== undefined) el.textContent = text;
    if (cls) el.className = cls;
    return el;
  };
  const link = (path, text) => {
    const a = element('a', text);
    a.href = new URL(path, root).href;
    return a;
  };
  const words = lang === 'es' ? {
    title: 'DP1901: el objeto investigado y la recuperación que está en juego',
    source: 'Fuentes y tesis actualizada', all: 'Mapa completo de conexiones',
    related: 'Conexiones de esta materia', boundary: 'Conexión probatoria no equivale a acumulación, culpabilidad ni prueba de incorporación judicial. Los estados de presentación siguen en su registro canónico.',
    index: 'Recorrido por las materias conectadas', receipt: 'Consultar estado de actuaciones'
  } : {
    title: 'DP1901: the investigative subject and the recovery at stake',
    source: 'Sources and updated thesis', all: 'Complete connection map',
    related: 'Connections for this subject', boundary: 'An evidential connection is not joinder, guilt or proof of court incorporation. Filing states remain in their canonical register.',
    index: 'Navigate the connected subjects', receipt: 'Check action status'
  };
  const render = (data) => {
    if (!data || data.control_id !== 'PD-DP1901-PLATFORM-NEXUS-20260920-01') return;
    const node = data.nodes.find((n) => n.routes[lang] === relative);
    const central = data.central_routes[lang] === relative;
    if (!node && !central) return;
    if (!document.querySelector('link[data-pd1901-platform-nexus-style]')) {
      const css = element('link');
      css.rel = 'stylesheet';
      css.href = new URL('assets/dp1901-platform-recovery-nexus-20260920.css', root).href;
      css.setAttribute('data-pd1901-platform-nexus-style', '20260920');
      document.head.appendChild(css);
    }
    const host = document.querySelector('main');
    if (!host) return;
    if (!central && !document.getElementById('pd1901-platform-nexus')) {
      const section = element('section', undefined, 'pd1901-platform-nexus');
      section.id = 'pd1901-platform-nexus';
      section.setAttribute('aria-labelledby', 'pd1901-platform-nexus-title');
      section.dataset.nexusNode = node.id;
      const h2 = element('h2', words.title); h2.id = 'pd1901-platform-nexus-title';
      section.append(h2, element('p', node.context[lang]), element('p', data.thesis[lang]));
      const nav = element('nav'); nav.setAttribute('aria-label', words.related);
      nav.append(link(data.central_routes[lang], words.all), link(data.archive, words.source));
      const ids = new Set();
      data.edges.forEach((edge) => {
        if (edge.from === node.id) ids.add(edge.to);
        if (edge.to === node.id) ids.add(edge.from);
      });
      ids.forEach((id) => {
        const other = data.nodes.find((n) => n.id === id);
        if (other) nav.append(link(other.routes[lang] + '#pd1901-platform-nexus', other.label[lang]));
      });
      section.append(nav, element('p', words.boundary, 'pd1901-nexus-boundary'));
      const firstSection = host.querySelector(':scope > section');
      if (firstSection) firstSection.before(section); else host.append(section);
    }
    const index = document.querySelector('[data-dp1901-nexus-index]');
    if (central && index && !index.dataset.ready) {
      const ul = element('ul', undefined, 'pd1901-nexus-index');
      data.nodes.forEach((n) => {
        const li = element('li');
        li.append(link(n.routes[lang] + '#pd1901-platform-nexus', n.label[lang]), element('p', n.context[lang]));
        ul.append(li);
      });
      index.replaceChildren(ul); index.dataset.ready = 'true';
    }
    document.documentElement.dataset.pd1901Nexus = 'ready';
  };
  const start = () => fetch(new URL('assets/data/dp1901-platform-recovery-nexus-20260920.json', root), {credentials: 'same-origin'})
    .then((response) => { if (!response.ok) throw new Error('Nexus data unavailable'); return response.json(); })
    .then(render).catch(() => { /* Preserve all original source content on failure. */ });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, {once: true});
  else start();
})();
