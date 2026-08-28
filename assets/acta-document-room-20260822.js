(() => {
  'use strict';

  const room = document.querySelector('[data-acta-room]');
  if (!room) return;

  const locale = document.documentElement.lang === 'es' ? 'es' : 'en';
  const manifestUrl = room.dataset.manifest;
  const repoRoot = room.dataset.repoRoot || '../../../';
  const list = room.querySelector('[data-acta-list]');
  const search = room.querySelector('[data-acta-search]');
  const filter = room.querySelector('[data-acta-filter]');
  const resultCount = room.querySelector('[data-acta-count]');
  const stats = {
    total: room.querySelector('[data-stat-total]'),
    complete: room.querySelector('[data-stat-complete]'),
    partial: room.querySelector('[data-stat-partial]'),
    open: room.querySelector('[data-stat-open]')
  };

  const perimeterMeta = {
    pre_sale_montelanza: { code: 'A', primaryLane: 'A' },
    project_lpb_aweswell_gil: { code: 'B', primaryLane: 'B' },
    adverse_montelanza_molina: { code: 'C1', primaryLane: 'C' },
    adverse_acosta_matos: { code: 'C2', primaryLane: 'C' },
    mixed_or_contested: { code: 'D-MIXED', primaryLane: 'D' },
    unresolved: { code: 'D-OPEN', primaryLane: 'D' }
  };

  const copy = {
    en: {
      status: {
        'located-package-complete-public': 'Complete public-safe package',
        'located-package-digitised-public': 'Located copy digitised and posted',
        'located-package-partial': 'Located · public package partial',
        'referenced-original-not-located': 'Referenced · original not located',
        'no-acta-located': 'No ACTA located',
        'non-acta-event': 'Separate event · not an ACTA'
      },
      body: { owners: 'Owners’ Community', cexp: 'CEXP', corporate: 'Corporate shareholders', event: 'Working event', reference: 'Later recital' },
      availability: { transcript: 'Public-safe text', pdf: 'Text-edition PDF', images: 'Rendered edition pages', facsimile: 'Redacted source facsimile', sourceImages: 'Redacted source-page images', integrity: 'Integrity record', sourcePages: 'Received source', publicPages: 'Public text edition' },
      available: 'Available', pending: 'Pending', pages: n => `${n} page${n === 1 ? '' : 's'}`,
      verificationPending: 'Available · line verification pending',
      actions: { detail: 'Open complete event page', source: 'Source-language transcript', translation: 'English reading', pdf: 'Public text-edition PDF', facsimile: 'Redacted source facsimile', manifest: 'Integrity manifest', provenance: 'Source provenance', redactions: 'Redaction log', previews: 'Show rendered edition pages', sourcePreviews: 'Show redacted source pages', hide: 'Hide pages' },
      perimeter: {
        pre_sale_montelanza: 'Montelanza · pre-sale',
        project_lpb_aweswell_gil: 'Project · Multimatrix/LPB → Aweswell/LPB–Gil',
        adverse_montelanza_molina: 'Attributed adverse · AAS → FMMM / Cogolludo / Pamanil',
        adverse_acosta_matos: 'Alleged adverse · Acosta Matos/CAM',
        mixed_or_contested: 'Mixed or contested',
        unresolved: 'Unresolved'
      },
      attributionBoundary: 'Documentary/editorial lane—not a finding of validity, joint conduct, fraud or guilt.',
      shown: (shown, total) => `${shown} of ${total} records shown`,
      empty: 'No record matches this search and filter.',
      indexUnavailable: 'The public ACTA index could not be loaded. No evidential records are displayed.',
      indexUnavailableCount: 'Public ACTA index unavailable · no records displayed',
      image: (title, page) => `${title}, rendered page ${page} of the public-safe text edition`,
      page: page => `Page ${page}`,
      integrityNote: 'A repository hash identifies a received digital copy; it is not proof of an official certified original or an uninterrupted forensic chain of custody.',
      translationPending: 'A complete source-language text may be available while an English reading remains pending.'
    },
    es: {
      status: {
        'located-package-complete-public': 'Paquete público seguro completo',
        'located-package-digitised-public': 'Copia localizada digitalizada y publicada',
        'located-package-partial': 'Localizada · paquete público parcial',
        'referenced-original-not-located': 'Referenciada · original no localizado',
        'no-acta-located': 'No se localizó ACTA',
        'non-acta-event': 'Evento separado · no es ACTA'
      },
      body: { owners: 'Comunidad de Propietarios', cexp: 'CEXP', corporate: 'Accionistas societarios', event: 'Reunión de trabajo', reference: 'Mención posterior' },
      availability: { transcript: 'Texto público seguro', pdf: 'PDF de edición textual', images: 'Páginas de la edición textual', facsimile: 'Facsímil fuente expurgado', sourceImages: 'Imágenes fuente expurgadas', integrity: 'Registro de integridad', sourcePages: 'Fuente recibida', publicPages: 'Edición textual pública' },
      available: 'Disponible', pending: 'Pendiente', pages: n => `${n} página${n === 1 ? '' : 's'}`,
      verificationPending: 'Disponible · cotejo línea por línea pendiente',
      actions: { detail: 'Abrir página completa del evento', source: 'Transcripción en lengua fuente', translation: 'Lectura en inglés', pdf: 'PDF de edición textual pública', facsimile: 'Facsímil fuente expurgado', manifest: 'Manifiesto de integridad', provenance: 'Procedencia de fuente', redactions: 'Registro de expurgación', previews: 'Mostrar páginas de la edición textual', sourcePreviews: 'Mostrar páginas fuente expurgadas', hide: 'Ocultar páginas' },
      perimeter: {
        pre_sale_montelanza: 'Montelanza · pre-venta',
        project_lpb_aweswell_gil: 'Proyecto · Multimatrix/LPB → Aweswell/LPB–Gil',
        adverse_montelanza_molina: 'Adverso atribuido · AAS → FMMM / Cogolludo / Pamanil',
        adverse_acosta_matos: 'Adverso alegado · Acosta Matos/CAM',
        mixed_or_contested: 'Mixto o controvertido',
        unresolved: 'No resuelto'
      },
      attributionBoundary: 'Carril documental/editorial; no es hallazgo de validez, actuación conjunta, fraude o culpabilidad.',
      shown: (shown, total) => `${shown} de ${total} registros visibles`,
      empty: 'Ningún registro coincide con la búsqueda y el filtro.',
      indexUnavailable: 'No se pudo cargar el índice público de ACTA. No se muestra ningún registro probatorio.',
      indexUnavailableCount: 'Índice público de ACTA no disponible · no se muestran registros',
      image: (title, page) => `${title}, página ${page} de la edición textual pública segura`,
      page: page => `Página ${page}`,
      integrityNote: 'Un hash del repositorio identifica una copia digital recibida; no acredita un original oficial certificado ni una cadena de custodia forense ininterrumpida.',
      translationPending: 'Puede estar disponible el texto íntegro en lengua fuente mientras queda pendiente la lectura en inglés.'
    }
  }[locale];

  const allowedStates = new Set([
    'located-package-complete-public', 'located-package-digitised-public', 'located-package-partial',
    'referenced-original-not-located', 'no-acta-located', 'non-acta-event'
  ]);

  function normaliseBody(value, defaultBody = 'owners') {
    if (['owners', 'cexp', 'corporate', 'event', 'reference'].includes(value)) return value;
    const source = String(value || '').toLowerCase();
    if (source.includes('corporate') || source.includes('shareholder') || source.includes('accionista')) return 'corporate';
    if (source.includes('working') || source.includes('trabajo')) return 'event';
    if (source.includes('recital') || source.includes('mención') || source.includes('refer')) return 'reference';
    if (source.includes('cexp') && !source.includes('propietarios')) return 'cexp';
    return defaultBody;
  }

  function normaliseIndexEvent(incoming, base = {}) {
    const limitations = incoming.limitations || {};
    const publicArtifacts = incoming.public_artifacts || {};
    const previewCount = Number(incoming.preview_count || incoming.pdf_pages || publicArtifacts.preview_count || publicArtifacts.pdf_pages);
    let previews = incoming.preview_pages || publicArtifacts.preview_pages || [];
    if ((!Array.isArray(previews) || !previews.length) && incoming.preview_dir && Number.isInteger(previewCount) && previewCount > 0) {
      previews = Array.from({ length: previewCount }, (_, index) => `${String(incoming.preview_dir).replace(/\/$/, '')}/page-${String(index + 1).padStart(3, '0')}.webp`);
    }
    const perimeter = incoming.perimeter || base.perimeter || 'unresolved';
    const meta = perimeterMeta[perimeter] || perimeterMeta.unresolved;
    return {
      ...base,
      ...incoming,
      body: normaliseBody(incoming.body, base.body),
      title_en: incoming.title_en || base.title_en,
      title_es: incoming.title_es || base.title_es,
      notes_en: incoming.notes_en || limitations.en || incoming.source_variant_note_en || incoming.source_variant_note || base.notes_en,
      notes_es: incoming.notes_es || limitations.es || incoming.source_variant_note_es || incoming.source_variant_note || base.notes_es,
      transcript_source: incoming.transcript_source || incoming.transcript_path || publicArtifacts.transcript_es || base.transcript_source,
      transcript_es: incoming.transcript_es || incoming.transcript_path || publicArtifacts.transcript_es || base.transcript_es,
      transcript_en: incoming.transcript_en || base.transcript_en,
      public_pdf: incoming.public_pdf || incoming.public_pdf_path || publicArtifacts.pdf || base.public_pdf,
      redacted_source_facsimile: incoming.redacted_source_facsimile || publicArtifacts.redacted_source_facsimile || base.redacted_source_facsimile,
      manifest: incoming.manifest || incoming.manifest_path || base.manifest,
      provenance: incoming.provenance || incoming.provenance_path || publicArtifacts.provenance || base.provenance,
      redaction_log: incoming.redaction_log || incoming.redaction_log_path || publicArtifacts.redaction_log || base.redaction_log,
      source_page_count: incoming.source_variant_page_count || incoming.source_pages || incoming.source_page_count || incoming.page_count || base.source_page_count,
      page_count: previewCount || incoming.page_count || base.page_count,
      preview_pages: Array.isArray(previews) ? previews : [],
      source_preview_pages: Array.isArray(incoming.source_preview_pages || publicArtifacts.source_preview_pages) ? (incoming.source_preview_pages || publicArtifacts.source_preview_pages) : [],
      source_sha256: incoming.source_sha256 || incoming.source_hash_sha256 || (incoming.source && incoming.source.sha256) || base.source_sha256,
      detail_page_es: incoming.detail_page_es || base.detail_page_es,
      detail_page_en: incoming.detail_page_en || base.detail_page_en,
      perimeter,
      perimeter_code: incoming.perimeter_code || base.perimeter_code || meta.code,
      primary_lane: incoming.primary_lane || base.primary_lane || meta.primaryLane,
      attribution_status: incoming.attribution_status || base.attribution_status,
      phase_es: incoming.phase_es || base.phase_es,
      phase_en: incoming.phase_en || base.phase_en,
      complete_public_text: incoming.complete_public_text === true,
      status: allowedStates.has(incoming.status) ? incoming.status : (base.status || 'located-package-partial')
    };
  }

  const safeUrl = value => {
    if (typeof value !== 'string' || !value.trim()) return null;
    const url = value.trim();
    if (/^(https:\/\/|mailto:)/i.test(url)) return url;
    if (/^[a-z][a-z0-9+.-]*:/i.test(url)) return null;
    return repoRoot + url.replace(/^(\.\/|\/)+/, '');
  };

  const textFor = (event, key) => event[`${key}_${locale}`] || event[key] || event[`${key}_es`] || event[`${key}_en`] || '';
  const previewList = event => Array.isArray(event.preview_pages) ? event.preview_pages.filter(page => typeof page === 'string' || (page && typeof page.url === 'string')) : [];
  const sourcePreviewList = event => Array.isArray(event.source_preview_pages) ? event.source_preview_pages.filter(page => typeof page === 'string' || (page && typeof page.url === 'string')) : [];

  function gatedState(event) {
    const requested = allowedStates.has(event.status) ? event.status : 'located-package-partial';
    if (requested === 'located-package-digitised-public') {
      const sourcePreviews = sourcePreviewList(event);
      const sourcePageCount = Number(event.source_page_count || event.source_variant_page_count);
      const coherentSourcePages = Number.isInteger(sourcePageCount) && sourcePageCount > 0 && sourcePreviews.length === sourcePageCount;
      const digitised = event.digitisation_complete_for_located_copy === true && Boolean(event.transcript_source || event.transcript_es || event.transcript);
      const facsimile = event.redacted_facsimile_available === true && Boolean(safeUrl(event.redacted_source_facsimile));
      return digitised && facsimile && event.source_page_images_available === true && coherentSourcePages ? requested : 'located-package-partial';
    }
    if (requested !== 'located-package-complete-public') return requested;
    const previews = previewList(event);
    const pageCount = Number(event.page_count);
    const coherentPreviews = Number.isInteger(pageCount) && pageCount > 0 && previews.length === pageCount;
    const hasText = event.complete_public_text === true && event.manual_source_line_verification === true && Boolean(event.transcript_source || event.transcript_es || event.transcript);
    const hasPdf = Boolean(safeUrl(event.public_pdf));
    const hasSourceFacsimile = event.redacted_facsimile_available === true && event.source_page_images_available === true;
    return hasText && hasPdf && coherentPreviews && hasSourceFacsimile ? requested : 'located-package-partial';
  }

  function statusClass(state) {
    if (state === 'located-package-complete-public') return 'complete';
    if (state === 'located-package-digitised-public') return 'complete';
    if (state === 'located-package-partial') return 'partial';
    if (state === 'non-acta-event') return 'event';
    return 'missing';
  }

  function element(tag, className, value) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (value !== undefined) node.textContent = value;
    return node;
  }

  function actionLink(label, href, secondary = false) {
    const link = element('a', secondary ? 'secondary' : '', label);
    link.href = href;
    if (/^https:\/\//.test(href)) link.rel = 'noopener';
    return link;
  }

  function availabilityRow(label, value) {
    const row = element('div');
    row.append(element('span', '', label), element('strong', '', value));
    return row;
  }

  function renderRecord(event) {
    const state = gatedState(event);
    const perimeterKey = perimeterMeta[event.perimeter] ? event.perimeter : 'unresolved';
    const metaForPerimeter = perimeterMeta[perimeterKey];
    const perimeterCode = event.perimeter_code || metaForPerimeter.code;
    const primaryLane = event.primary_lane || metaForPerimeter.primaryLane;
    const article = element('article', 'acta-record');
    article.dataset.state = state;
    article.dataset.body = event.body || 'owners';
    article.dataset.perimeter = perimeterKey;
    article.dataset.perimeterCode = perimeterCode;
    article.dataset.primaryLane = primaryLane;
    article.dataset.search = [event.id, event.date, perimeterCode, primaryLane, textFor(event, 'title'), textFor(event, 'notes'), textFor(event, 'phase'), copy.body[event.body], copy.perimeter[perimeterKey]].join(' ').toLowerCase();

    const head = element('header', 'acta-record-head');
    const heading = element('div');
    const meta = element('div', 'acta-record-meta');
    meta.append(element('span', 'acta-record-id', event.id || '—'));
    meta.append(element('span', '', copy.body[event.body] || copy.body.owners));
    if (event.date) meta.append(element('time', '', event.date));
    heading.append(meta, element('h2', '', textFor(event, 'title') || event.id));
    head.append(heading, element('span', `acta-status ${statusClass(state)}`, copy.status[state]));

    const body = element('div', 'acta-record-body');
    const narrative = element('div');
    const perimeter = element('div', 'acta-perimeter-ribbon');
    perimeter.dataset.perimeter = perimeterKey;
    perimeter.dataset.perimeterCode = perimeterCode;
    perimeter.dataset.primaryLane = primaryLane;
    const perimeterHeading = element('strong');
    perimeterHeading.append(
      element('span', 'acta-perimeter-code', perimeterCode),
      document.createTextNode(copy.perimeter[perimeterKey] || copy.perimeter.unresolved)
    );
    perimeter.append(
      perimeterHeading,
      element('span', '', textFor(event, 'phase') || copy.attributionBoundary)
    );
    narrative.append(perimeter);
    narrative.append(element('p', 'acta-record-summary', textFor(event, 'notes')));

    const detailPage = safeUrl(locale === 'es' ? event.detail_page_es : event.detail_page_en);
    const sourceTranscript = safeUrl(event.transcript_source || event.transcript_es || event.transcript);
    const translation = safeUrl(event.transcript_en);
    const publicPdf = safeUrl(event.public_pdf);
    const sourceFacsimile = safeUrl(event.redacted_source_facsimile);
    const manifest = safeUrl(event.manifest);
    const provenance = safeUrl(event.provenance);
    const redactionLog = safeUrl(event.redaction_log);
    const previews = previewList(event);
    const sourcePreviews = sourcePreviewList(event);
    const pageCount = Number(event.page_count);
    const actions = element('div', 'acta-room-actions');
    if (detailPage) actions.append(actionLink(copy.actions.detail, detailPage));
    if (sourceTranscript) actions.append(actionLink(copy.actions.source, sourceTranscript));
    if (locale === 'en' && translation && translation !== sourceTranscript) actions.append(actionLink(copy.actions.translation, translation, true));
    if (publicPdf) actions.append(actionLink(copy.actions.pdf, publicPdf, true));
    if (sourceFacsimile) actions.append(actionLink(copy.actions.facsimile, sourceFacsimile, true));
    if (manifest) actions.append(actionLink(copy.actions.manifest, manifest, true));
    if (provenance) actions.append(actionLink(copy.actions.provenance, provenance, true));
    if (redactionLog) actions.append(actionLink(copy.actions.redactions, redactionLog, true));
    if (actions.childElementCount) narrative.append(actions);
    if (event.complete_public_text === true && locale === 'en' && !translation) narrative.append(element('p', 'acta-record-note', copy.translationPending));

    const availability = element('aside', 'acta-record-availability');
    const transcriptStatus = sourceTranscript ? (event.manual_source_line_verification === false ? copy.verificationPending : copy.available) : copy.pending;
    availability.append(
      availabilityRow(copy.availability.transcript, transcriptStatus),
      availabilityRow(copy.availability.pdf, publicPdf ? copy.available : copy.pending),
      availabilityRow(copy.availability.images, previews.length ? copy.pages(previews.length) : copy.pending),
      availabilityRow(copy.availability.facsimile, sourceFacsimile ? copy.available : copy.pending),
      availabilityRow(copy.availability.sourceImages, sourcePreviews.length ? copy.pages(sourcePreviews.length) : copy.pending),
      availabilityRow(copy.availability.integrity, manifest || event.source_sha256 ? copy.available : copy.pending)
    );
    const sourcePageCount = Number(event.source_page_count);
    if (Number.isInteger(sourcePageCount) && sourcePageCount > 0) availability.append(availabilityRow(copy.availability.sourcePages, copy.pages(sourcePageCount)));
    if (Number.isInteger(pageCount) && pageCount > 0) availability.append(availabilityRow(copy.availability.publicPages, copy.pages(pageCount)));
    if (Number.isInteger(pageCount) && pageCount > 0 && previews.length && previews.length !== pageCount) {
      availability.append(availabilityRow(locale === 'es' ? 'Control de páginas' : 'Page control', `${previews.length}/${pageCount}`));
    }
    body.append(narrative, availability);
    article.append(head, body);

    if (previews.length) {
      const previewWrap = element('div', 'acta-preview-wrap');
      const toggle = element('button', 'acta-room-toggle', copy.actions.previews);
      toggle.type = 'button';
      toggle.setAttribute('aria-expanded', 'false');
      const grid = element('div', 'acta-preview-grid');
      grid.hidden = true;
      const gridId = `previews-${String(event.id).toLowerCase().replace(/[^a-z0-9-]/g, '-')}`;
      grid.id = gridId;
      toggle.setAttribute('aria-controls', gridId);
      previews.forEach((item, index) => {
        const rawUrl = typeof item === 'string' ? item : item.url;
        const href = safeUrl(rawUrl);
        if (!href) return;
        const page = typeof item === 'object' && item.page ? item.page : index + 1;
        const link = element('a', 'acta-preview');
        link.href = href;
        const image = document.createElement('img');
        image.loading = 'lazy';
        image.decoding = 'async';
        image.alt = copy.image(textFor(event, 'title') || event.id, page);
        image.src = href;
        link.append(image, element('span', '', copy.page(page)));
        grid.append(link);
      });
      toggle.addEventListener('click', () => {
        const expanded = toggle.getAttribute('aria-expanded') === 'true';
        toggle.setAttribute('aria-expanded', String(!expanded));
        toggle.textContent = expanded ? copy.actions.previews : copy.actions.hide;
        grid.hidden = expanded;
      });
      previewWrap.append(toggle, grid);
      article.append(previewWrap);
    }
    if (sourcePreviews.length) {
      const previewWrap = element('div', 'acta-preview-wrap');
      const toggle = element('button', 'acta-room-toggle', copy.actions.sourcePreviews);
      toggle.type = 'button';
      toggle.setAttribute('aria-expanded', 'false');
      const grid = element('div', 'acta-preview-grid');
      grid.hidden = true;
      const gridId = `source-previews-${String(event.id).toLowerCase().replace(/[^a-z0-9-]/g, '-')}`;
      grid.id = gridId;
      toggle.setAttribute('aria-controls', gridId);
      sourcePreviews.forEach((item, index) => {
        const rawUrl = typeof item === 'string' ? item : item.url;
        const href = safeUrl(rawUrl);
        if (!href) return;
        const page = typeof item === 'object' && item.page ? item.page : index + 1;
        const link = element('a', 'acta-preview');
        link.href = href;
        const image = document.createElement('img');
        image.loading = 'lazy';
        image.decoding = 'async';
        image.alt = `${textFor(event, 'title') || event.id}, ${copy.availability.sourceImages}, ${copy.page(page)}`;
        image.src = href;
        link.append(image, element('span', '', copy.page(page)));
        grid.append(link);
      });
      toggle.addEventListener('click', () => {
        const expanded = toggle.getAttribute('aria-expanded') === 'true';
        toggle.setAttribute('aria-expanded', String(!expanded));
        toggle.textContent = expanded ? copy.actions.sourcePreviews : copy.actions.hide;
        grid.hidden = expanded;
      });
      previewWrap.append(toggle, grid);
      article.append(previewWrap);
    }
    return article;
  }

  let events = [];
  let indexState = 'loading';

  function renderIndexUnavailable() {
    events = [];
    indexState = 'unavailable';
    room.dataset.manifestState = 'unavailable';
    list.replaceChildren();
    const message = element('p', 'acta-room-empty', copy.indexUnavailable);
    message.setAttribute('role', 'alert');
    list.append(message);
    resultCount.textContent = copy.indexUnavailableCount;
    Object.values(stats).forEach(stat => { stat.textContent = '—'; });
    search.disabled = true;
    filter.disabled = true;
  }

  function render() {
    if (indexState === 'unavailable') {
      renderIndexUnavailable();
      return;
    }
    if (indexState !== 'ready') return;
    const needle = search.value.trim().toLowerCase();
    const selected = filter.value;
    const visible = events.filter(event => {
      const state = gatedState(event);
      const meta = perimeterMeta[event.perimeter] || perimeterMeta.unresolved;
      const haystack = [event.id, event.date, event.perimeter_code || meta.code, event.primary_lane || meta.primaryLane, textFor(event, 'title'), textFor(event, 'notes'), textFor(event, 'phase'), copy.body[event.body], copy.perimeter[event.perimeter]].join(' ').toLowerCase();
      const matchesText = !needle || haystack.includes(needle);
      let matchesFilter = selected === 'all';
      if (selected === 'owners' || selected === 'cexp' || selected === 'corporate' || selected === 'event' || selected === 'reference') matchesFilter = event.body === selected;
      if (selected.startsWith('perimeter:')) matchesFilter = event.perimeter === selected.slice('perimeter:'.length);
      if (selected === 'complete') matchesFilter = state === 'located-package-complete-public' || state === 'located-package-digitised-public';
      if (selected === 'open') matchesFilter = state !== 'located-package-complete-public' && state !== 'located-package-digitised-public';
      return matchesText && matchesFilter;
    });

    list.replaceChildren();
    if (!visible.length) list.append(element('p', 'acta-room-empty', copy.empty));
    else visible.forEach(event => list.append(renderRecord(event)));
    resultCount.textContent = copy.shown(visible.length, events.length);

    const states = events.map(gatedState);
    stats.total.textContent = String(events.length);
    stats.complete.textContent = String(states.filter(state => state === 'located-package-complete-public' || state === 'located-package-digitised-public').length);
    stats.partial.textContent = String(states.filter(state => state === 'located-package-partial').length);
    stats.open.textContent = String(states.filter(state => state !== 'located-package-complete-public' && state !== 'located-package-digitised-public').length);
  }

  search.addEventListener('input', render);
  filter.addEventListener('change', render);
  const initialQuery = new URLSearchParams(window.location.search).get('q');
  if (initialQuery) search.value = initialQuery;
  const c1Option = filter.querySelector('option[value="perimeter:adverse_montelanza_molina"]');
  if (c1Option) c1Option.textContent = copy.perimeter.adverse_montelanza_molina;
  room.dataset.manifestState = 'loading';

  if (manifestUrl) {
    fetch(manifestUrl, { cache: 'no-store' })
      .then(response => {
        if (!response.ok) throw new Error(`manifest ${response.status}`);
        return response.json();
      })
      .then(data => {
        const supplied = Array.isArray(data) ? data : data.events;
        if (!Array.isArray(supplied) || !supplied.length) throw new Error('empty public index');
        if (supplied.some(event => !event || typeof event !== 'object' || Array.isArray(event) || typeof event.id !== 'string' || !event.id.trim())) {
          throw new Error('invalid public index event');
        }
        const suppliedIds = new Set(supplied.map(event => event.id));
        if (suppliedIds.size !== supplied.length) throw new Error('duplicate public index event');
        events = supplied.map(incoming => normaliseIndexEvent(incoming));
        indexState = 'ready';
        room.dataset.manifestState = 'ready';
        search.disabled = false;
        filter.disabled = false;
        render();
      })
      .catch(renderIndexUnavailable);
  } else renderIndexUnavailable();
})();
