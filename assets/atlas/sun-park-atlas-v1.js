(() => {
  'use strict';
  const scriptNode = document.currentScript;
  if (!scriptNode || !document.querySelector('main')) return;
  const base = new URL('.', scriptNode.src);
  const path = location.pathname.replace(/index\.html$/i, '').replace(/\/+$/, '/');
  const lang = path.startsWith('/por-derecho/es/') ? 'es' : 'en';
  const routes = {
    '/en/case-control-room/': 'overview',
    '/es/sala-control-caso/': 'overview',
    '/en/actua-gesvalt-2018-valuation-comparison/': 'valuation',
    '/es/comparativa-tasaciones-actua-gesvalt-2018/': 'valuation',
    '/en/sun-park-forensic-map-262-properties/': 'perimeter',
    '/es/mapa-forense-sun-park-262-fincas/': 'perimeter',
    '/en/ric-private-equity-sun-park/': 'positions',
    '/es/ric-private-equity-sun-park/': 'positions',
    '/en/pwc-canarias-carlos-saavedra-sun-park/': 'band',
    '/es/pwc-canarias-carlos-saavedra-sun-park/': 'band',
    '/en/same-hotel-multiple-financial-lives/': 'finance',
    '/es/mismo-hotel-multiples-vidas-financieras/': 'finance',
    '/en/ricpe-hnt-gc836-traceability/': 'finance',
    '/es/ricpe-hnt-gc836-trazabilidad/': 'finance',
    '/en/sun-park-atlas/': 'full',
    '/es/atlas-probatorio-sun-park/': 'full'
  };
  const tail = path.startsWith('/por-derecho/') ? path.slice('/por-derecho'.length) : '';
  const mode = routes[tail];
  if (!mode || document.querySelector('[data-sp-atlas-v1]')) return;
  const atlasUrl = lang === 'es' ? '/por-derecho/es/atlas-probatorio-sun-park/' : '/por-derecho/en/sun-park-atlas/';
  const cssHref = new URL('sun-park-atlas-v1.css', base).href;
  if (!document.querySelector('link[href*="sun-park-atlas-v1.css"]')) {
    const css = document.createElement('link');
    css.rel = 'stylesheet'; css.href = cssHref;
    document.head.appendChild(css);
  }
  const el = (tag, css, content, parent) => {
    const n = document.createElement(tag);
    if (css) n.className = css;
    if (content !== undefined && content !== null) n.textContent = String(content);
    if (parent) parent.appendChild(n);
    return n;
  };
  const safeLink = (href, label, parent, css = '') => {
    const target = new URL(href, location.origin);
    if (target.origin !== location.origin || !target.pathname.startsWith('/por-derecho/')) return null;
    const a = el('a', css, label, parent);
    a.href = target.pathname + target.search + target.hash;
    return a;
  };
  const source = (item, data, parent) => safeLink(item.href, data.labels.source + ' ↗', parent, 'spa-source');
  const banner = (section, data, subtitle) => {
    const h = el('div', 'spa-heading', null, section);
    el('span', 'spa-eyebrow', data.publicControl + ' · ' + data.version, h);
    el('h2', '', subtitle || data.title, h);
    el('p', 'spa-intro', data.intro, h);
  };
  const note = (parent, text) => el('p', 'spa-warning', text, parent);
  const more = (parent, data) => safeLink(atlasUrl, data.labels.openAtlas + ' →', parent, 'spa-cta');
  const renderTracks = (mount, data) => {
    const grid = el('div', 'spa-tracks', null, mount);
    data.tracks.forEach((t, i) => {
      const card = el('article', 'spa-track', null, grid);
      el('span', 'spa-track-index', String(i + 1).padStart(2, '0'), card);
      el('h3', '', t.name, card);
      el('p', '', t.summary, card);
      source(t, data, card);
    });
  };
  const renderFilters = (mount, data, filterCallback) => {
    const filters = el('div', 'spa-filters', null, mount);
    filters.setAttribute('role', 'group');
    filters.setAttribute('aria-label', data.labels.tracks);
    const choices = [{id:'all', name:data.labels.viewAll}].concat(data.tracks);
    const buttons = choices.map(track => {
      const button = el('button', 'spa-filter', track.name, filters);
      button.type = 'button';
      button.dataset.track = track.id;
      button.setAttribute('aria-pressed', String(track.id === 'all'));
      button.addEventListener('click', () => {
        buttons.forEach(other => other.setAttribute('aria-pressed', String(other === button)));
        filterCallback(track.id);
      });
      return button;
    });
  };
  const renderStages = (mount, data) => {
    el('h3', 'spa-section-title', data.labels.stages, mount);
    const status = el('p', 'spa-screen-reader', '', mount);
    status.setAttribute('aria-live', 'polite');
    const cards = el('div', 'spa-stage-grid', null, mount);
    const nodes = data.stages.map((s, i) => {
      const card = el('article', 'spa-stage', null, cards);
      card.dataset.tracks = s.tracks.join(' ');
      const cap = el('div', 'spa-stage-top', null, card);
      el('span', 'spa-stage-num', String(i + 1).padStart(2, '0'), cap);
      el('span', 'spa-year', s.year, cap);
      el('h4', '', s.title, card);
      el('p', 'spa-kind', s.kind, card);
      el('p', '', s.assertion, card);
      const d = el('details', 'spa-detail', null, card);
      el('summary', '', data.labels.expand, d);
      note(d, data.labels.qualifier + ': ' + s.limit);
      el('p', 'spa-gap', data.labels.open + ': ' + s.missing, d);
      source(s, data, d);
      return {s,card};
    });
    return track => {
      const count = nodes.reduce((n,x) => {
        x.card.hidden = track !== 'all' && !x.s.tracks.includes(track);
        return n + (x.card.hidden ? 0 : 1);
      },0);
      status.textContent = String(count) + ' / ' + String(nodes.length);
    };
  };
  const renderValuations = (mount, data) => {
    el('h3', 'spa-section-title', data.labels.valuations, mount);
    const cards = el('div', 'spa-value-grid', null, mount);
    data.valuations.forEach(v => {
      const card = el('article', 'spa-value', null, cards);
      el('p', 'spa-year', v.when, card);
      el('h4', '', v.title, card);
      el('p', 'spa-value-amount', v.amount, card);
      el('p', '', v.basis, card);
      note(card, v.limit);
      source(v, data, card);
    });
    note(mount, data.labels.comparison + ': ' + (lang === 'es' ?
      'Estas cifras describen finalidades y bienes diferentes. La distancia aritmética NO acredita un perjuicio.' :
      'These numbers concern different rights and purposes. The arithmetic difference does NOT establish loss.'));
  };
  const renderPositions = (mount, data) => {
    el('h3', 'spa-section-title', data.labels.positions, mount);
    const grid = el('div', 'spa-position-grid', null, mount);
    data.positions.forEach(p => {
      const card = el('article', 'spa-position', null, grid);
      el('span', 'spa-year', p.year, card);
      el('h4', '', p.speaker, card);
      el('p', '', p.point, card);
      note(card, p.limit);
      source(p, data, card);
    });
    note(mount, data.labels.noCausation);
  };
  const renderPerimeter = (mount, data) => {
    el('h3', 'spa-section-title', data.labels.perimeter, mount);
    const summary = el('div', 'spa-split', null, mount);
    data.perimeter.forEach(p => {
      const card = el('div', 'spa-split-card', null, summary);
      el('strong', 'spa-big', p.count, card);
      el('span', '', p.name, card);
    });
    const bar = el('div', 'spa-split-bar', null, mount);
    bar.setAttribute('role', 'img');
    bar.setAttribute('aria-label', data.perimeter.map(p => p.name + ': ' + p.count).join('; '));
    data.perimeter.forEach((p,i) => {
      const part = el('span', 'spa-split-part spa-split-' + String(i+1), null, bar);
      part.style.flexGrow = String(p.count);
    });
    note(mount, data.labels.notTitle);
    safeLink(lang==='es' ? '/por-derecho/es/mapa-forense-sun-park-262-fincas/' : '/por-derecho/en/sun-park-forensic-map-262-properties/', data.labels.source+' ↗', mount, 'spa-source');
  };
  const renderFinance = (mount, data) => {
    el('h3', 'spa-section-title', data.labels.finance, mount);
    const steps = el('div', 'spa-finance-grid', null, mount);
    data.finance.forEach((f,i) => {
      const c = el('article', 'spa-finance-step', null, steps);
      el('span', 'spa-stage-num', String(i+1).padStart(2,'0'), c);
      el('h4', '', f.name, c);
      el('p', 'spa-kind', f.status, c);
      note(c, f.limit);
    });
    note(mount, data.labels.noCausation);
  };
  const build = data => {
    if (data.schema !== 'por-derecho.sun-park-atlas.public.v1' || data.locale !== lang ||
        data.tracks.length !== 8 || data.stages.length !== 9) throw Error('Atlas source contract');
    const mount = mode === 'full' ? document.getElementById('sun-park-atlas-root') : document.querySelector('main');
    if (!mount) return;
    const wrapper = el('section', 'spa-atlas spa-mode-' + mode);
    wrapper.dataset.spAtlasV1 = mode;
    wrapper.setAttribute('aria-label', data.title);
    banner(wrapper, data, mode==='full' ? data.title : (mode==='band' ? data.labels.stages :
      mode==='valuation' ? data.labels.valuations : mode==='positions' ? data.labels.positions :
      mode==='perimeter' ? data.labels.perimeter : mode==='finance' ? data.labels.finance : data.title));
    const body = el('div', 'spa-body', null, wrapper);
    if (mode === 'full') {
      renderTracks(body,data);
      const display = el('div', 'spa-stage-area', null, body);
      const setFilter = renderStages(display, data);
      setFilter('all');
      const controls = el('div', 'spa-full-track-controls', null, body);
      renderFilters(controls, data, setFilter);
      renderPositions(body,data);
      renderValuations(body,data);
      renderPerimeter(body,data);
      renderFinance(body,data);
      note(body,data.boundary);
      mount.appendChild(wrapper);
      const fallback = document.querySelector('.spa-atlas-static');
      if (fallback) fallback.hidden = true;
      return;
    }
    if (mode === 'overview') {
      renderTracks(body,data);
      note(body,data.boundary);
    } else if (mode === 'valuation') {
      renderValuations(body,data);
    } else if (mode === 'positions') {
      renderPositions(body,data);
    } else if (mode === 'band') {
      const filter = renderStages(body,data); filter('all');
      note(body,data.boundary);
    } else if (mode === 'perimeter') {
      renderPerimeter(body,data);
    } else if (mode === 'finance') {
      renderFinance(body,data);
    }
    more(wrapper,data);
    const anchors = {
      overview: lang==='es' ? '#entender' : '#understand',
      valuation: '.metrics',
      positions: lang==='es' ? '#tres-realidades-ricpe' : '#three-ricpe-realities',
      band: '#pwc-eccta-economic-fruits-20261018 figure.evidence-figure.wide',
      perimeter: '#resetMap',
      finance: 'main section:first-of-type'
    };
    const node = document.querySelector(anchors[mode]);
    if (node) {
      const anchor = mode==='band' ? node : (node.closest('section') || node);
      anchor.insertAdjacentElement('afterend', wrapper);
    } else mount.appendChild(wrapper);
  };
  fetch(new URL('atlas-public-v1.' + lang + '.json',base),{credentials:'same-origin'})
    .then(r => {if (!r.ok) throw Error('Atlas data ' + r.status); return r.json();})
    .then(build)
    .catch(() => {
      if (mode === 'full') return;
      const m = document.querySelector('main');
      if (!m) return;
      const fallback = el('aside','spa-atlas spa-fallback',null,m);
      el('p','',lang==='es'?'Vista Atlas temporalmente no disponible.':'Atlas view temporarily unavailable.',fallback);
      safeLink(atlasUrl,lang==='es'?'Abrir Atlas':'Open Atlas',fallback,'spa-cta');
    });
})();
