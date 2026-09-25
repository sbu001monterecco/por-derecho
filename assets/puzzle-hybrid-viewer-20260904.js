(() => {
  'use strict';
  const path = location.pathname.replace(/\/+$/, '/');
  const isPuzzle = path.endsWith('/en/puzzle/') || path.endsWith('/es/puzzle/');
  if (!isPuzzle || document.querySelector('[data-pd-puzzle-viewer="20260904a"]')) return;

  const script = document.currentScript;
  if (!script) return;
  const rootUrl = new URL('../', script.src);
  const dataUrl = new URL('../data/puzzle/puzzle-reading-guide-2026.json', script.src);
  const cssUrl = new URL('puzzle-hybrid-viewer-20260904.css?v=20260904a', script.src);
  const css = document.createElement('link');
  css.rel = 'stylesheet';
  css.href = cssUrl.href;
  document.head.appendChild(css);

  const lang = path.includes('/es/') ? 'es' : 'en';
  const t = lang === 'es' ? {
    title:'PUZZLE — mapa visual histórico y guía de lectura 2026',
    eyebrow:'EXPOSICIÓN HISTÓRICA · LECTURA CONTROLADA',
    historical:'El PUZZLE original se conserva como exposición histórica; la guía sustitutiva de 2026 controla cómo debe leerse hoy.',
    filed:'Guía presentada', track1956:'DP 1956', track1901:'DP 1901', current:'Registro actual', sources:'Fuentes',
    previous:'Anterior', next:'Siguiente', fit:'Ajustar', zoomOut:'−', zoomIn:'+', present:'Presentación', fullscreen:'Pantalla completa', pdf:'PDF original', slides:'Presentación original',
    page:'Página', of:'de', use:'Uso', limit:'Límite', content:'Contenido', rules:'Reglas de lectura', source:'Estado de fuente',
    missingTitle:'El visor está diseñado y listo; falta materializar el PDF original aprobado en el repositorio público.',
    missingText:'La interfaz no sustituye el original por capturas ni reconstrucciones. El despliegue debe añadir el binario original verificado en la ruta controlada indicada en el manifiesto.',
    later:'Ir al grafo de evidencia actual', noSlides:'Presentación original pendiente de verificación pública',
    keyboard:'← / → páginas', sourceBoundary:'La guía de 2026 y el registro posterior se muestran como capas separadas. El registro posterior no reescribe el contenido de la presentación judicial de 2026.'
  } : {
    title:'PUZZLE — historical visual map & 2026 reading guide',
    eyebrow:'HISTORICAL EXHIBIT · CONTROLLED READING',
    historical:'The original PUZZLE is preserved as a historical exhibit; the 2026 substitute guide controls how it should be read today.',
    filed:'Filed guide', track1956:'DP 1956', track1901:'DP 1901', current:'Current record', sources:'Sources',
    previous:'Previous', next:'Next', fit:'Fit', zoomOut:'−', zoomIn:'+', present:'Presentation', fullscreen:'Full screen', pdf:'Original PDF', slides:'Original presentation',
    page:'Page', of:'of', use:'Use', limit:'Limit', content:'Content', rules:'Reading rules', source:'Source status',
    missingTitle:'The viewer is designed and ready; the approved original PDF still needs to be materialised in the public repository.',
    missingText:'The interface does not replace the original with screenshots or reconstructions. Deployment should add the verified original binary at the controlled path stated in the manifest.',
    later:'Go to the current evidence graph', noSlides:'Original presentation pending public-access verification',
    keyboard:'← / → pages', sourceBoundary:'The 2026 filed guide and the later record are shown as separate layers. Later evidence does not rewrite what the 2026 judicial companion said when filed.'
  };

  const esc = (s='') => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const chapterFor = (data, page) => data.chapters.find(c => page >= c.pages[0] && page <= c.pages[1]) || data.chapters[0];
  const pageFromLocation = max => {
    const hash = location.hash.match(/^#p(\d{1,2})$/i);
    const q = new URLSearchParams(location.search).get('page');
    const n = Number(hash?.[1] || q || 1);
    return Math.min(max, Math.max(1, Number.isFinite(n) ? n : 1));
  };

  fetch(dataUrl.href, {cache:'no-store'}).then(r => {
    if (!r.ok) throw new Error(`guide ${r.status}`);
    return r.json();
  }).then(data => {
    const main = document.querySelector('main');
    if (!main) return;
    const pdfUrl = new URL(data.document.assetPath, rootUrl).href;
    let page = pageFromLocation(data.document.pageCount);
    let zoom = 100;
    let fit = true;
    let activeTab = 'filed';

    const section = document.createElement('section');
    section.className = 'pd-puzzle-viewer';
    section.dataset.pdPuzzleViewer = '20260904a';
    section.dataset.pdfState = 'checking';
    section.tabIndex = -1;
    section.innerHTML = `
      <div class="pd-puzzle-viewer__intro">
        <div><p class="pd-puzzle-viewer__eyebrow">${esc(t.eyebrow)}</p><h2>${esc(t.title)}</h2><p>${esc(t.historical)}</p></div>
        <div class="pd-puzzle-viewer__status"><strong>${esc(data.filedGuide.proceedings.join(' · '))}</strong><br>${esc(data.filedGuide.formalDate)} · 32 pages · SHA-256 ${esc(data.document.sha256.slice(0,12))}…</div>
      </div>
      <div class="pd-puzzle-viewer__toolbar" role="toolbar" aria-label="PUZZLE viewer">
        <button type="button" data-action="prev" aria-label="${esc(t.previous)}">←</button>
        <button type="button" data-action="next" aria-label="${esc(t.next)}">→</button>
        <label class="pd-puzzle-viewer__counter">${esc(t.page)} <input type="number" min="1" max="${data.document.pageCount}" value="${page}" data-page-input> ${esc(t.of)} ${data.document.pageCount}</label>
        <button type="button" data-action="zoom-out" aria-label="${esc(t.zoomOut)}">−</button>
        <button type="button" data-action="fit">${esc(t.fit)}</button>
        <button type="button" data-action="zoom-in" aria-label="${esc(t.zoomIn)}">+</button>
        <span class="pd-puzzle-viewer__kbd">${esc(t.keyboard)}</span>
        <span class="pd-puzzle-viewer__spacer"></span>
        <button type="button" data-action="presentation">${esc(t.present)}</button>
        <button type="button" data-action="fullscreen">⛶ ${esc(t.fullscreen)}</button>
        <a class="pd-puzzle-viewer__button" data-original-pdf href="${esc(pdfUrl)}" target="_blank" rel="noopener">${esc(t.pdf)}</a>
        <a class="pd-puzzle-viewer__button" data-original-slides ${data.document.presentationUrl ? `href="${esc(data.document.presentationUrl)}" target="_blank" rel="noopener"` : 'aria-disabled="true" title="'+esc(t.noSlides)+'"'}>${esc(t.slides)}</a>
      </div>
      <div class="pd-puzzle-viewer__stage">
        <div class="pd-puzzle-viewer__document">
          <iframe class="pd-puzzle-viewer__frame" title="PUZZLE 2024" loading="eager"></iframe>
          <div class="pd-puzzle-viewer__missing"><div><strong>${esc(t.missingTitle)}</strong><p>${esc(t.missingText)}</p><p><code>assets/docs/puzzle/PUZZLE-2024-original.pdf</code><br><small>SHA-256: ${esc(data.document.sha256)} · ${Math.round(data.document.sizeBytes/1024/1024)} MB · ${data.document.pageCount} pages</small></p></div></div>
        </div>
        <aside class="pd-puzzle-viewer__notes" aria-label="2026 reading guide">
          <div class="pd-puzzle-viewer__tabs" role="tablist">
            <button class="pd-puzzle-viewer__tab" role="tab" data-tab="filed">${esc(t.filed)}</button>
            <button class="pd-puzzle-viewer__tab" role="tab" data-tab="1956">${esc(t.track1956)}</button>
            <button class="pd-puzzle-viewer__tab" role="tab" data-tab="1901">${esc(t.track1901)}</button>
            <button class="pd-puzzle-viewer__tab" role="tab" data-tab="current">${esc(t.current)}</button>
            <button class="pd-puzzle-viewer__tab" role="tab" data-tab="sources">${esc(t.sources)}</button>
          </div>
          <div class="pd-puzzle-viewer__note-body" data-note-body></div>
        </aside>
      </div>
      <nav class="pd-puzzle-viewer__chapter-nav" aria-label="PUZZLE chapters"></nav>
      <div class="pd-puzzle-viewer__source-boundary">${esc(t.sourceBoundary)}</div>`;
    main.prepend(section);

    const frame = section.querySelector('.pd-puzzle-viewer__frame');
    const input = section.querySelector('[data-page-input]');
    const note = section.querySelector('[data-note-body]');
    const chapterNav = section.querySelector('.pd-puzzle-viewer__chapter-nav');

    const frameSrc = () => `${pdfUrl}#page=${page}&${fit ? 'view=FitH' : `zoom=${zoom}`}&pagemode=none`;
    const updateFrame = () => { if (section.dataset.pdfState === 'ready') frame.src = frameSrc(); };
    const updateHash = () => { try { history.replaceState(null, '', `${location.pathname}${location.search}#p${page}`); } catch (_) {} };
    const setPage = n => {
      page = Math.min(data.document.pageCount, Math.max(1, Number(n) || 1));
      input.value = page;
      updateFrame();
      updateHash();
      renderNotes();
      renderChapters();
    };

    const renderChapters = () => {
      chapterNav.innerHTML = data.chapters.map(ch => {
        const c = ch[lang] || ch.en;
        const current = page >= ch.pages[0] && page <= ch.pages[1];
        return `<button type="button" class="pd-puzzle-viewer__chapter" data-page="${ch.pages[0]}" aria-current="${current}"><strong>${esc(c.label)}</strong><small>${ch.pages[0]}–${ch.pages[1]}</small></button>`;
      }).join('');
    };

    const list = items => `<ul>${items.map(x => `<li>${esc(x)}</li>`).join('')}</ul>`;
    const renderNotes = () => {
      const ch = chapterFor(data, page);
      const c = ch[lang] || ch.en;
      section.querySelectorAll('[data-tab]').forEach(b => b.setAttribute('aria-selected', String(b.dataset.tab === activeTab)));
      if (activeTab === 'filed') {
        const g = data.filedGuide[lang] || data.filedGuide.en;
        note.innerHTML = `<h3>${esc(g.title)} · ${esc(t.page)} ${page}</h3><p><strong>${esc(c.label)} · ${ch.pages[0]}–${ch.pages[1]}</strong></p><h4>${esc(t.content)}</h4><p>${esc(c.content)}</p><h4>${esc(t.use)}</h4><p>${esc(c.use)}</p><div class="pd-puzzle-viewer__limit"><strong>${esc(t.limit)}</strong><p>${esc(c.limit)}</p></div><h4>${esc(t.rules)}</h4>${list(data.globalRules[lang] || data.globalRules.en)}`;
      } else if (activeTab === '1956' || activeTab === '1901') {
        const tr = data.tracks[activeTab][lang] || data.tracks[activeTab].en;
        note.innerHTML = `<h3>${esc(tr.label)}</h3><p>${esc(tr.summary)}</p>${tr.directNotice ? `<div class="pd-puzzle-viewer__limit"><p>${esc(tr.directNotice)}</p></div>` : ''}${tr.focus ? `<div class="pd-puzzle-viewer__limit"><p>${esc(tr.focus)}</p></div>` : ''}<h4>${esc(c.label)} · ${ch.pages[0]}–${ch.pages[1]}</h4><p>${esc(c.use)}</p><p><strong>${esc(t.limit)}:</strong> ${esc(c.limit)}</p>`;
      } else if (activeTab === 'current') {
        const p = data.postFiling[lang] || data.postFiling.en;
        note.innerHTML = `<h3>${esc(p.title)}</h3><p>${esc(p.text)}</p><a class="pd-puzzle-viewer__later-link" href="${lang === 'es' ? '#mapa' : '#map'}">${esc(t.later)} ↓</a>`;
      } else {
        note.innerHTML = `<h3>${esc(t.sources)}</h3><p><strong>PUZZLE 2024</strong><br>32 pages · ${Math.round(data.document.sizeBytes/1024/1024)} MB<br>SHA-256: <code>${esc(data.document.sha256)}</code></p><p><strong>${esc(data.filedGuide.proceedings.join(' · '))}</strong><br>${esc(data.filedGuide.formalDate)}</p><p><a class="pd-puzzle-viewer__later-link" href="../../data/puzzle/uria-haya-puzzle-registry.json">Current structured Puzzle evidence register</a></p><p><a class="pd-puzzle-viewer__later-link" href="${lang === 'es' ? '#documentos' : '#documents'}">${esc(t.later)} ↓</a></p>`;
      }
    };

    section.addEventListener('click', e => {
      const action = e.target.closest('[data-action]')?.dataset.action;
      if (action === 'prev') setPage(page - 1);
      if (action === 'next') setPage(page + 1);
      if (action === 'zoom-out') { fit = false; zoom = Math.max(50, zoom - 25); updateFrame(); }
      if (action === 'zoom-in') { fit = false; zoom = Math.min(250, zoom + 25); updateFrame(); }
      if (action === 'fit') { fit = true; updateFrame(); }
      if (action === 'presentation') section.classList.toggle('presentation-mode');
      if (action === 'fullscreen') {
        if (document.fullscreenElement) document.exitFullscreen?.(); else section.requestFullscreen?.();
      }
      const tab = e.target.closest('[data-tab]')?.dataset.tab;
      if (tab) { activeTab = tab; renderNotes(); }
      const chapterPage = e.target.closest('[data-page]')?.dataset.page;
      if (chapterPage) setPage(Number(chapterPage));
    });
    input.addEventListener('change', () => setPage(input.value));
    section.addEventListener('keydown', e => {
      if (['INPUT','TEXTAREA'].includes(e.target.tagName)) return;
      if (e.key === 'ArrowLeft') { e.preventDefault(); setPage(page - 1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); setPage(page + 1); }
    });

    renderNotes();
    renderChapters();

    fetch(pdfUrl, {method:'HEAD', cache:'no-store'}).then(r => {
      if (!r.ok) throw new Error(`pdf ${r.status}`);
      section.dataset.pdfState = 'ready';
      frame.src = frameSrc();
    }).catch(() => {
      section.dataset.pdfState = 'missing';
      section.querySelector('[data-original-pdf]')?.setAttribute('aria-disabled','true');
    });
  }).catch(err => console.warn('Puzzle hybrid viewer unavailable:', err));
})();
