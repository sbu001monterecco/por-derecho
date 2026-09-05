(() => {
  'use strict';

  const path = window.location.pathname.replace(/\/+$/, '/');
  const isPuzzle = path.endsWith('/en/puzzle/') || path.endsWith('/es/puzzle/');
  if (!isPuzzle || window.__pdPuzzleViewer20260905Loaded) return;
  window.__pdPuzzleViewer20260905Loaded = true;

  const script = document.currentScript;
  if (!script) return;
  const ROOT = new URL('../', script.src);
  const lang = path.includes('/es/') ? 'es' : 'en';
  const PAGE_COUNT = 32;
  const ORIGINAL_HASH = 'e441bdb368c0092d5b15ca5ee911eeac266540bde54817e424f3075f4c5fdd47';
  const ORIGINAL_BYTES = 50046618;
  const urls = {
    guide: new URL('data/puzzle/puzzle-reading-guide-2026.json', ROOT),
    provenance: new URL('data/puzzle/puzzle-provenance-public-interest-20260905.json', ROOT),
    manifest: new URL('assets/docs/puzzle/manifest.json', ROOT),
    pdf: new URL('assets/docs/puzzle/PUZZLE-2024-original.pdf', ROOT)
  };

  const t = lang === 'es' ? {
    eyebrow: 'ORIGINAL EXACTO · BASE PRESENTADA · CAPAS SEPARADAS',
    title: 'PUZZLE — visor universal de la fuente original',
    intro: 'El visor principal usa imágenes de página derivadas del PDF original exacto, no un iframe PDF. Así el PUZZLE sigue siendo visible en escritorio, tablet y móvil aunque el navegador no incorpore un visor PDF.',
    exact: 'Original exacto verificado', openPdf: 'Abrir PDF original', downloadPdf: 'Descargar PDF original', pageImage: 'Abrir imagen de página', manifest: 'Manifiesto de imágenes',
    previous: 'Anterior', next: 'Siguiente', page: 'Página', of: 'de', fit: 'Ajustar', presentation: 'Presentación', fullscreen: 'Pantalla completa', zoom: 'Zoom',
    baseline: 'Base junio 2026', dp1956: 'DP 1956', dp1901: 'DP 1901', current: 'Registro actual', sources: 'Fuentes',
    content: 'Contenido', use: 'Uso', limit: 'Límite', readingRules: 'Reglas de lectura', sourceStatus: 'Estado de fuente',
    imageLoading: 'Cargando página fuente…', imageError: 'La imagen de página no pudo cargarse. El PDF original sigue disponible directamente.',
    connected: 'Conexiones unitarias', publicInterest: 'Posición de interés público y de informante', publicFunds: 'Daño/fondos públicos — prueba antes de afirmar', predatory: '“Inclusión predatoria” — tesis atribuida de Gil Marer',
    publicInterestText: 'Gil Marer manifiesta que actúa tanto como parte directamente interesada y presuntamente perjudicada, con interés económico, como alertador/informante ante autoridades. Invoca Ley 2/2023, el marco UE y, cuando proceda por materia y alcance personal, los marcos alemán y británico. El sitio no presenta esa condición protegida como una determinación judicial o administrativa si no existe tal resolución.',
    publicFundsText: 'La presencia de RIC, subvenciones, financiación pública, fondos UE/regionales o una autoridad no equivale por sí sola a daño al erario. La ruta debe identificar beneficiario, base legal, importe, desembolso/efecto fiscal, representación utilizada, gasto/proyecto elegible, corrección o recuperación y pérdida pública contrafactual.',
    predatoryText: '“Inclusión predatoria” es la formulación analítica atribuida a Gil Marer. Para elevarla respecto de cualquier actor posterior exige: exposición previa → hecho material y razón/deber de revelar → conocimiento individualizable → omisión/presentación engañosa → entrada del nuevo actor/recurso → confianza/efecto habilitante → beneficio/causalidad, conservando siempre la explicación lícita. La falta de conocimiento de un nuevo actor puede ser exculpatoria de su intención.',
    juneNotJuly: 'Control de procedencia: la base narrativa/metodológica presentada en junio es el escrito Control 21 de 25 de junio de 2026. Los acompañantes DP 1956/DP 1901 son posteriores, de 21 de julio de 2026, y se muestran como lentes distintas.',
    originalLayer: 'PUZZLE 2024 original', currentLayer: 'Registro posterior', notFinding: 'Una flecha, fotografía, coincidencia, relación profesional/corporativa o cronología no constituye por sí sola hallazgo de conocimiento, intención, coordinación, conflicto, control, beneficio o responsabilidad.'
  } : {
    eyebrow: 'EXACT ORIGINAL · FILED BASELINE · SEPARATE LAYERS',
    title: 'PUZZLE — universal source-original viewer',
    intro: 'The primary viewer uses page images derived from the exact original PDF rather than a PDF iframe. The PUZZLE therefore remains visible on desktop, tablet and mobile even where the browser has no embedded PDF viewer.',
    exact: 'Verified exact original', openPdf: 'Open original PDF', downloadPdf: 'Download original PDF', pageImage: 'Open page image', manifest: 'Image manifest',
    previous: 'Previous', next: 'Next', page: 'Page', of: 'of', fit: 'Fit', presentation: 'Presentation', fullscreen: 'Full screen', zoom: 'Zoom',
    baseline: 'June 2026 baseline', dp1956: 'DP 1956', dp1901: 'DP 1901', current: 'Current record', sources: 'Sources',
    content: 'Content', use: 'Use', limit: 'Limit', readingRules: 'Reading rules', sourceStatus: 'Source status',
    imageLoading: 'Loading source page…', imageError: 'The page image could not be loaded. The exact original PDF remains directly available.',
    connected: 'Unitary connections', publicInterest: 'Public-interest and informant position', publicFunds: 'Public funds/harm — prove before asserting', predatory: '“Predatory inclusion” — Gil Marer’s attributed thesis',
    publicInterestText: 'Gil Marer states that he acts both as a directly interested and allegedly injured party with an economic interest, and as an alertador/informant reporting to authorities. He invokes Spain’s Law 2/2023, the EU framework and, where their personal/material scope applies, German and UK frameworks. The site does not present protected status as a judicial or administrative determination unless such a determination exists.',
    publicFundsText: 'The presence of RIC, a subsidy, public finance, EU/regional funds or a public authority is not itself proof of harm to public funds. The route should identify beneficiary, legal basis, amount, disbursement/tax effect, representation relied upon, eligible project/spend, correction/recovery and any source-supported counterfactual public loss.',
    predatoryText: '“Predatory inclusion” is Gil Marer’s attributed analytical expression. Elevating it as to any later actor requires: legacy exposure → material fact and disclosure reason/duty → actor-specific knowledge → omission/misleading presentation → entry of the new actor/resource → reliance/enabling effect → benefit/causation, while preserving the lawful alternative. A later actor’s lack of knowledge may be exculpatory of that actor’s intent.',
    juneNotJuly: 'Provenance control: the June narrative/methodological baseline is the Control 21 filing presented on 25 June 2026. The DP 1956/DP 1901 companions are later, dated 21 July 2026, and are shown as separate lenses.',
    originalLayer: 'Original PUZZLE 2024', currentLayer: 'Later record', notFinding: 'An arrow, photograph, coincidence, professional/corporate relationship or chronology does not by itself establish knowledge, intent, coordination, conflict, control, benefit or liability.'
  };

  const escapeHTML = (value) => String(value ?? '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  const pad = (n) => String(n).padStart(2, '0');
  const pageImageUrl = (n) => new URL(`assets/docs/puzzle/page-${pad(n)}.webp`, ROOT).href;
  const cleanPage = (value) => Math.min(PAGE_COUNT, Math.max(1, Number.parseInt(value, 10) || 1));
  const hashPage = () => {
    const match = window.location.hash.match(/^#p(\d{1,2})$/i);
    return match ? cleanPage(match[1]) : 1;
  };
  const routeUrl = (route) => new URL(String(route).replace(/^\/+/, ''), ROOT).href;

  const loadJSON = async (url) => {
    const response = await fetch(url.href, {credentials: 'same-origin', cache: 'no-store'});
    if (!response.ok) throw new Error(`${response.status} ${url.pathname}`);
    return response.json();
  };

  const chapterForPage = (guide, page) => guide.chapters.find((chapter) => page >= chapter.pages[0] && page <= chapter.pages[1]) || guide.chapters[0];
  const chapterMarkup = (chapter) => {
    const item = chapter?.[lang] || {};
    return `<div class="puz25__meta">
      <div><span>${escapeHTML(t.content)}</span><strong>${escapeHTML(item.content || '')}</strong></div>
      <div><span>${escapeHTML(t.use)}</span><strong>${escapeHTML(item.use || '')}</strong></div>
      <div><span>${escapeHTML(t.limit)}</span><strong>${escapeHTML(item.limit || '')}</strong></div>
    </div>`;
  };

  const makeList = (items) => Array.isArray(items) && items.length ? `<ul>${items.map((item) => `<li>${escapeHTML(item)}</li>`).join('')}</ul>` : '';

  const noteMarkup = (tab, guide, provenance, page) => {
    const chapter = chapterForPage(guide, page);
    let body = '';
    if (tab === 'baseline') {
      const source = guide.juneFiledBaseline?.[lang] || {};
      body = `<h3>${escapeHTML(source.title || t.baseline)}</h3><p><strong>${escapeHTML(source.status || '')}</strong></p><p>${escapeHTML(source.text || '')}</p><p class="puz25__limit">${escapeHTML(source.boundary || '')}</p><p><strong>${escapeHTML(t.juneNotJuly)}</strong></p>`;
    } else if (tab === '1956') {
      const track = guide.tracks?.['1956']?.[lang] || {};
      body = `<h3>${escapeHTML(track.label || t.dp1956)}</h3><p>${escapeHTML(track.summary || '')}</p><p class="puz25__limit">${escapeHTML(track.directNotice || '')}</p>`;
    } else if (tab === '1901') {
      const track = guide.tracks?.['1901']?.[lang] || {};
      body = `<h3>${escapeHTML(track.label || t.dp1901)}</h3><p>${escapeHTML(track.summary || '')}</p><p class="puz25__limit">${escapeHTML(track.focus || '')}</p>`;
    } else if (tab === 'current') {
      const current = guide.postFiling?.[lang] || {};
      body = `<h3>${escapeHTML(current.title || t.current)}</h3><p>${escapeHTML(current.text || '')}</p><p class="puz25__limit">${escapeHTML(t.notFinding)}</p>`;
    } else {
      const original = provenance.original || {};
      const layers = provenance.layers || [];
      body = `<h3>${escapeHTML(t.sources)}</h3>
        <p><strong>${escapeHTML(t.exact)}:</strong> ${escapeHTML(original.pageCount)} pages · ${Number(original.sizeBytes || ORIGINAL_BYTES).toLocaleString()} bytes</p>
        <p><code>SHA-256 ${escapeHTML(original.sha256 || ORIGINAL_HASH)}</code></p>
        ${makeList(layers.map((layer) => `${layer.date} · ${lang === 'es' ? layer.labelEs : layer.labelEn} · ${layer.status || layer.interpretiveStatus || ''}`))}
        <p class="puz25__limit">${escapeHTML(original.limit || t.notFinding)}</p>`;
    }
    return `${body}${chapterMarkup(chapter)}`;
  };

  const routeLabels = lang === 'es' ? {
    'es/uria-menendez-sun-park/': 'Uría / Sun Park',
    'es/ric-private-equity-sun-park/': 'RICPE',
    'es/orion-rental-socimi/': 'Orion Rental SOCIMI',
    'es/comunidad-instrumentalizacion/': 'Comunidad / instrumentalización',
    'es/comunidad-instrumentalizacion/actas-2011-2022/': 'Actas 2011–2022',
    'es/acosta-matos-perimetro/': 'Perímetro Acosta Matos',
    'es/toma-control-sun-park-7-junio-2018/': 'Toma de control 7 jun 2018'
  } : {
    'en/uria-menendez-sun-park/': 'Uría / Sun Park',
    'en/ric-private-equity-sun-park/': 'RICPE',
    'en/orion-rental-socimi/': 'Orion Rental SOCIMI',
    'en/community-instrumentalisation/': 'Community / instrumentalisation',
    'en/community-instrumentalisation/minutes-2011-2022/': 'Minutes 2011–2022',
    'en/acosta-matos-perimeter/': 'Acosta Matos perimeter',
    'en/sun-park-takeover-7-june-2018/': '7 June 2018 takeover'
  };

  const build = (guide, provenance, manifest) => {
    document.querySelectorAll('[data-pd-puzzle-viewer="20260904a"]').forEach((node) => node.remove());
    const original = provenance.original || {};
    const viewer = document.createElement('section');
    viewer.className = 'puz25';
    viewer.setAttribute('data-pd-puzzle-viewer', '20260904a');
    viewer.setAttribute('data-pd-puzzle-viewer-v2', '20260905a');
    viewer.id = 'puzzle-original-viewer';
    viewer.style.setProperty('--puz-image-width', '100%');
    viewer.innerHTML = `
      <header class="puz25__head">
        <div>
          <div class="puz25__eyebrow">${escapeHTML(t.eyebrow)}</div>
          <h2>${escapeHTML(t.title)}</h2>
          <p>${escapeHTML(t.intro)}</p>
          <div class="puz25__integrity"><strong>${escapeHTML(t.exact)}:</strong> 32 pages · ${ORIGINAL_BYTES.toLocaleString()} bytes · SHA-256 <code>${ORIGINAL_HASH}</code></div>
        </div>
        <div class="puz25__actions">
          <a href="${urls.pdf.href}" target="_blank" rel="noopener">${escapeHTML(t.openPdf)}</a>
          <a href="${urls.pdf.href}" download="PUZZLE-2024-original.pdf">${escapeHTML(t.downloadPdf)}</a>
          <a data-puz-page-image href="${pageImageUrl(1)}" target="_blank" rel="noopener">${escapeHTML(t.pageImage)}</a>
          <a href="${urls.manifest.href}" target="_blank" rel="noopener">${escapeHTML(t.manifest)}</a>
        </div>
      </header>
      <nav class="puz25__chapters" aria-label="PUZZLE chapters">${guide.chapters.map((chapter) => {
        const item = chapter[lang] || {};
        return `<button type="button" data-puz-chapter="${chapter.pages[0]}">${escapeHTML(item.label || chapter.id)} · ${chapter.pages[0]}–${chapter.pages[1]}</button>`;
      }).join('')}</nav>
      <div class="puz25__toolbar">
        <button class="puz25__button" type="button" data-puz-prev>← ${escapeHTML(t.previous)}</button>
        <label>${escapeHTML(t.page)} <input type="number" min="1" max="32" step="1" value="1" data-puz-page></label>
        <span class="puz25__page-state" data-puz-state>1 ${escapeHTML(t.of)} 32</span>
        <button class="puz25__button" type="button" data-puz-next>${escapeHTML(t.next)} →</button>
        <label>${escapeHTML(t.zoom)} <input type="range" min="60" max="220" step="10" value="100" data-puz-zoom></label>
        <button class="puz25__button" type="button" data-puz-fit>${escapeHTML(t.fit)}</button>
        <button class="puz25__button" type="button" data-puz-present>${escapeHTML(t.presentation)}</button>
        <button class="puz25__button" type="button" data-puz-fullscreen>${escapeHTML(t.fullscreen)}</button>
      </div>
      <div class="puz25__grid">
        <div class="puz25__stage" data-puz-stage>
          <div class="puz25__loading" data-puz-loading>${escapeHTML(t.imageLoading)}</div>
          <div class="puz25__image-wrap"><img class="puz25__image" data-puz-image src="${pageImageUrl(1)}" alt="PUZZLE 2024 · page 1 of 32"></div>
        </div>
        <aside class="puz25__notes">
          <div class="puz25__tabs" role="tablist">
            <button type="button" role="tab" aria-selected="true" data-puz-tab="baseline">${escapeHTML(t.baseline)}</button>
            <button type="button" role="tab" aria-selected="false" data-puz-tab="1956">${escapeHTML(t.dp1956)}</button>
            <button type="button" role="tab" aria-selected="false" data-puz-tab="1901">${escapeHTML(t.dp1901)}</button>
            <button type="button" role="tab" aria-selected="false" data-puz-tab="current">${escapeHTML(t.current)}</button>
            <button type="button" role="tab" aria-selected="false" data-puz-tab="sources">${escapeHTML(t.sources)}</button>
          </div>
          <div class="puz25__note" data-puz-note>${noteMarkup('baseline', guide, provenance, 1)}</div>
        </aside>
      </div>
      <section class="puz25__connections"><h3>${escapeHTML(t.connected)}</h3><div class="puz25__links">${Object.entries(routeLabels).map(([route, label]) => `<a href="${routeUrl(route)}">${escapeHTML(label)}</a>`).join('')}</div></section>
      <section class="puz25__public">
        <article><h3>${escapeHTML(t.publicInterest)}</h3><p>${escapeHTML(t.publicInterestText)}</p></article>
        <article><h3>${escapeHTML(t.publicFunds)}</h3><p>${escapeHTML(t.publicFundsText)}</p></article>
        <article><h3>${escapeHTML(t.predatory)}</h3><p>${escapeHTML(t.predatoryText)}</p></article>
      </section>`;

    const hero = document.querySelector('.dossier-hero');
    const main = document.querySelector('main') || document.body;
    if (hero?.parentNode) hero.parentNode.insertBefore(viewer, hero.nextSibling);
    else main.insertBefore(viewer, main.firstChild);

    const image = viewer.querySelector('[data-puz-image]');
    const loading = viewer.querySelector('[data-puz-loading]');
    const note = viewer.querySelector('[data-puz-note]');
    const pageInput = viewer.querySelector('[data-puz-page]');
    const state = viewer.querySelector('[data-puz-state]');
    const pageLink = viewer.querySelector('[data-puz-page-image]');
    const zoom = viewer.querySelector('[data-puz-zoom]');
    let page = hashPage();
    let activeTab = 'baseline';

    const setChapterState = () => {
      const chapter = chapterForPage(guide, page);
      viewer.querySelectorAll('[data-puz-chapter]').forEach((button) => {
        const start = Number(button.dataset.puzChapter);
        const match = guide.chapters.find((item) => item.pages[0] === start);
        button.setAttribute('aria-current', String(Boolean(match && page >= match.pages[0] && page <= match.pages[1])));
      });
    };

    const renderPage = (nextPage, updateHash = true) => {
      page = cleanPage(nextPage);
      loading.hidden = false;
      loading.textContent = t.imageLoading;
      image.hidden = false;
      image.src = pageImageUrl(page);
      image.alt = `PUZZLE 2024 · ${t.page.toLowerCase()} ${page} ${t.of} ${PAGE_COUNT}`;
      pageInput.value = String(page);
      state.textContent = `${page} ${t.of} ${PAGE_COUNT}`;
      pageLink.href = pageImageUrl(page);
      note.innerHTML = noteMarkup(activeTab, guide, provenance, page);
      setChapterState();
      viewer.querySelector('[data-puz-prev]').disabled = page === 1;
      viewer.querySelector('[data-puz-next]').disabled = page === PAGE_COUNT;
      if (updateHash) history.replaceState(null, '', `${location.pathname}${location.search}#p${page}`);
      const preload = page < PAGE_COUNT ? new Image() : null;
      if (preload) preload.src = pageImageUrl(page + 1);
    };

    image.addEventListener('load', () => { loading.hidden = true; });
    image.addEventListener('error', () => {
      image.hidden = true;
      loading.hidden = false;
      loading.innerHTML = `<div class="puz25__error"><strong>${escapeHTML(t.imageError)}</strong><br><br><a href="${urls.pdf.href}" target="_blank" rel="noopener">${escapeHTML(t.openPdf)}</a></div>`;
    });
    viewer.querySelector('[data-puz-prev]').addEventListener('click', () => renderPage(page - 1));
    viewer.querySelector('[data-puz-next]').addEventListener('click', () => renderPage(page + 1));
    pageInput.addEventListener('change', () => renderPage(pageInput.value));
    viewer.querySelectorAll('[data-puz-chapter]').forEach((button) => button.addEventListener('click', () => renderPage(button.dataset.puzChapter)));
    viewer.querySelectorAll('[data-puz-tab]').forEach((button) => button.addEventListener('click', () => {
      activeTab = button.dataset.puzTab;
      viewer.querySelectorAll('[data-puz-tab]').forEach((item) => item.setAttribute('aria-selected', String(item === button)));
      note.innerHTML = noteMarkup(activeTab, guide, provenance, page);
    }));
    const applyZoom = () => viewer.style.setProperty('--puz-image-width', `${Number(zoom.value)}%`);
    zoom.addEventListener('input', applyZoom);
    viewer.querySelector('[data-puz-fit]').addEventListener('click', () => { zoom.value = '100'; applyZoom(); viewer.querySelector('[data-puz-stage]').scrollTo({top: 0, left: 0}); });
    viewer.querySelector('[data-puz-present]').addEventListener('click', () => viewer.classList.toggle('puz25--presentation'));
    viewer.querySelector('[data-puz-fullscreen]').addEventListener('click', async () => {
      try {
        if (document.fullscreenElement) await document.exitFullscreen();
        else if (viewer.requestFullscreen) await viewer.requestFullscreen();
      } catch (error) { console.warn('PUZZLE fullscreen unavailable', error); }
    });
    window.addEventListener('hashchange', () => renderPage(hashPage(), false));
    document.addEventListener('keydown', (event) => {
      const tag = document.activeElement?.tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;
      if (event.key === 'ArrowLeft') renderPage(page - 1);
      if (event.key === 'ArrowRight') renderPage(page + 1);
      if (event.key === 'Escape') viewer.classList.remove('puz25--presentation');
    });
    renderPage(page, false);

    viewer.dataset.pdfState = guide.document?.assetState || original.publicState || 'UNKNOWN';
    viewer.dataset.manifestPages = String(manifest.pages?.length || 0);
  };

  const init = async () => {
    try {
      const [guide, provenance, manifest] = await Promise.all([loadJSON(urls.guide), loadJSON(urls.provenance), loadJSON(urls.manifest)]);
      if (guide.document?.sha256 !== ORIGINAL_HASH || provenance.original?.sha256 !== ORIGINAL_HASH || manifest.original?.sha256 !== ORIGINAL_HASH) throw new Error('PUZZLE parent hash mismatch');
      if (guide.document?.pageCount !== PAGE_COUNT || provenance.original?.pageCount !== PAGE_COUNT || manifest.original?.pageCount !== PAGE_COUNT || manifest.pages?.length !== PAGE_COUNT) throw new Error('PUZZLE 32-page contract mismatch');
      build(guide, provenance, manifest);
    } catch (error) {
      console.error('PUZZLE viewer 20260905 failed', error);
      const fallback = document.createElement('section');
      fallback.className = 'puz25 puz25__fallback';
      fallback.setAttribute('data-pd-puzzle-viewer', '20260904a');
      fallback.setAttribute('data-pd-puzzle-viewer-v2', '20260905a');
      fallback.innerHTML = `<h2>${escapeHTML(t.title)}</h2><p>${escapeHTML(t.imageError)}</p><p><a class="puz25__button" href="${urls.pdf.href}" target="_blank" rel="noopener">${escapeHTML(t.openPdf)}</a> <a class="puz25__button" href="${urls.pdf.href}" download="PUZZLE-2024-original.pdf">${escapeHTML(t.downloadPdf)}</a></p>`;
      const hero = document.querySelector('.dossier-hero');
      if (hero?.parentNode) hero.parentNode.insertBefore(fallback, hero.nextSibling);
      else (document.querySelector('main') || document.body).prepend(fallback);
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once: true});
  else init();
})();
