/* Public-safe 262-finca journey explorer.  No global site loader is used. */
(() => {
  'use strict';

  const root = document.querySelector('[data-finca-journey]');
  if (!root) return;

  const lang = root.dataset.lang === 'es' ? 'es' : 'en';
  const copy = {
    en: {
      loading: 'Loading the public-safe journey…', error: 'The journey data could not be loaded. No property conclusion should be drawn from this error.',
      all: 'All', search: 'Search finca, unit, historical label…', finca: 'Registry finca', type: 'Type', block: 'Block / zone', coverage: 'Coverage state',
      showing: 'properties shown', total: 'fincas in the canonical register', propertyEvents: 'properties with source-bound events', separateContext: 'Whole-complex context — not a property event',
      physical: 'Physical baseline', historic: 'Historical source label', overlay: 'Acquisition-sheet source pointer', journey: 'Property-specific journey', conflict: 'Identifier conflict',
      questions: 'Open questions and next evidence', sources: 'Sources and status', date: 'Date', layer: 'Track', status: 'Evidence status', limitation: 'Limit', alternative: 'Alternative / counterpoint', next: 'Next document needed',
      noEvents: 'No source-bound property event has yet been entered for this finca.', noEventsExplanation: 'This is an explicit evidence gap, not a statement that nothing happened or that no right exists.',
      typeLabels: { APARTMENT: 'Apartment', COMMERCIAL: 'Commercial / service', SOLARIUM: 'Solarium' },
      zoneLabels: { FRONT: 'Commercial / services', CENTRAL: 'Central solaria', UNKNOWN: 'Unmapped physical zone' },
      stateLabels: { NOT_YET_RECONSTRUCTED: 'Not yet reconstructed', SOURCE_POINTER_ONLY: 'Source pointer only', PARTIALLY_RECONSTRUCTED: 'Partially reconstructed', IDENTIFIER_CONFLICT_OPEN: 'Identifier conflict open' },
      evidenceLabels: { VERIFIED_OFFICIAL: 'Verified official record', DOCUMENTED_REPRESENTATION: 'Documented representation', DOCUMENTED_CONTEXT: 'Documented context', PARTY_ALLEGATION: 'Party allegation', WORKING_LEAD: 'Working lead', PUBLIC_REPORT: 'Public report' },
      layerLabels: { title: 'Title', physical: 'Physical', possession: 'Possession / control', operation: 'Operation / revenue', community: 'Community / CEXP', concurso: 'Insolvency', registry: 'Registry', works: 'Works', valuation: 'Valuation', funding: 'Funding' },
      unit: 'Unit', aptLocal: 'Apartment / local', area: 'Area', historicCaution: 'Historic source label only; not current registered title.', overlayCaution: 'Working-sheet category only; it does not prove a completed acquisition, payment, authority, possession or registered title.', contextIntro: 'These dated records provide the background from 2008 onward. They are deliberately separate from the selected finca’s own source-bound events.',
      sourceAccess: { PUBLIC_SOURCE: 'public source', PUBLIC_SAFE_DERIVATIVE: 'public-safe derivative', CONTROLLED_SOURCE_NOT_PUBLISHED: 'controlled source, not published' },
      fieldFallback: 'Not recorded', selected: 'Selected finca'
    },
    es: {
      loading: 'Cargando el recorrido apto para publicación…', error: 'No se han podido cargar los datos del recorrido. No debe extraerse ninguna conclusión sobre una finca de este error.',
      all: 'Todas', search: 'Buscar finca, unidad, etiqueta histórica…', finca: 'Finca registral', type: 'Tipo', block: 'Bloque / zona', coverage: 'Estado de cobertura',
      showing: 'fincas mostradas', total: 'fincas del registro canónico', propertyEvents: 'fincas con eventos vinculados a fuente', separateContext: 'Contexto del conjunto — no es un evento de finca',
      physical: 'Base física', historic: 'Etiqueta histórica de fuente', overlay: 'Puntero de fuente de hoja de adquisición', journey: 'Recorrido específico de finca', conflict: 'Conflicto identificador',
      questions: 'Preguntas abiertas y siguiente prueba', sources: 'Fuentes y estado', date: 'Fecha', layer: 'Vía', status: 'Estado probatorio', limitation: 'Límite', alternative: 'Alternativa / contrapunto', next: 'Siguiente documento necesario',
      noEvents: 'Aún no se ha incorporado ningún evento de finca vinculado a fuente.', noEventsExplanation: 'Es una laguna probatoria expresa, no una afirmación de que no ocurrió nada ni de que no exista un derecho.',
      typeLabels: { APARTMENT: 'Apartamento', COMMERCIAL: 'Local / servicio', SOLARIUM: 'Solárium' },
      zoneLabels: { FRONT: 'Locales / servicios', CENTRAL: 'Soláriums centrales', UNKNOWN: 'Zona física sin mapear' },
      stateLabels: { NOT_YET_RECONSTRUCTED: 'Aún no reconstruida', SOURCE_POINTER_ONLY: 'Sólo puntero de fuente', PARTIALLY_RECONSTRUCTED: 'Parcialmente reconstruida', IDENTIFIER_CONFLICT_OPEN: 'Conflicto identificador abierto' },
      evidenceLabels: { VERIFIED_OFFICIAL: 'Registro oficial verificado', DOCUMENTED_REPRESENTATION: 'Representación documentada', DOCUMENTED_CONTEXT: 'Contexto documentado', PARTY_ALLEGATION: 'Alegación de parte', WORKING_LEAD: 'Pista de trabajo', PUBLIC_REPORT: 'Información pública' },
      layerLabels: { title: 'Título', physical: 'Física', possession: 'Posesión / control', operation: 'Explotación / ingresos', community: 'Comunidad / CEXP', concurso: 'Concurso', registry: 'Registro', works: 'Obras', valuation: 'Valoración', funding: 'Financiación' },
      unit: 'Unidad', aptLocal: 'Apartamento / local', area: 'Superficie', historicCaution: 'Sólo etiqueta histórica de fuente; no es titularidad registral actual.', overlayCaution: 'Sólo categoría de hoja de trabajo; no acredita adquisición consumada, pago, facultad, posesión ni titularidad inscrita.', contextIntro: 'Estos registros fechados proporcionan el contexto desde 2008. Se mantienen deliberadamente separados de los eventos de fuente vinculada de la finca seleccionada.',
      sourceAccess: { PUBLIC_SOURCE: 'fuente pública', PUBLIC_SAFE_DERIVATIVE: 'derivado apto para publicación', CONTROLLED_SOURCE_NOT_PUBLISHED: 'fuente controlada, no publicada' },
      fieldFallback: 'No consta', selected: 'Finca seleccionada'
    }
  }[lang];

  const els = {
    search: root.querySelector('[data-fj-search]'), finca: root.querySelector('[data-fj-finca]'), type: root.querySelector('[data-fj-type]'), block: root.querySelector('[data-fj-block]'), coverage: root.querySelector('[data-fj-coverage]'),
    count: root.querySelector('[data-fj-count]'), list: root.querySelector('[data-fj-property-list]'), detail: root.querySelector('[data-fj-detail]'), total: document.querySelector('[data-fj-total]'), eventCount: document.querySelector('[data-fj-event-count]'), sourceCount: document.querySelector('[data-fj-source-count]')
  };
  let data = null;
  const state = { search: '', finca: root.dataset.selectedFinca || '8588', type: '', block: '', coverage: '' };

  const textFor = value => value && typeof value === 'object' ? value[lang] : value;
  const label = (dictionary, key) => dictionary[key] || key || copy.fieldFallback;
  const element = (tag, className, content) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (content !== undefined && content !== null) node.textContent = String(content);
    return node;
  };
  const appendParagraph = (parent, text, className = '') => { if (text) parent.append(element('p', className, text)); };
  const renderListOfText = (parent, values, className = 'fj-question-list') => {
    const items = Array.isArray(values) ? values : [];
    if (!items.length) return;
    const list = element('ul', className);
    items.forEach(value => list.append(element('li', '', value)));
    parent.append(list);
  };
  const sourceById = id => (data.source_ledger || []).find(source => source.id === id);
  const addSources = (parent, ids) => {
    const unique = [...new Set(ids || [])];
    if (!unique.length) return;
    const heading = element('h4', '', copy.sources);
    parent.append(heading);
    const list = element('ul', 'fj-source-list');
    unique.forEach(id => {
      const source = sourceById(id);
      const item = element('li');
      item.append(element('span', 'fj-key', id));
      item.append(document.createTextNode(' — '));
      const sourceLabel = source ? textFor(source.label) : id;
      if (source && source.reference_url) {
        const link = element('a', '', sourceLabel);
        link.href = source.reference_url;
        link.target = '_blank';
        link.rel = 'noopener';
        item.append(link);
      } else {
        item.append(document.createTextNode(sourceLabel));
      }
      if (source && source.access) item.append(element('span', 'fj-source-access', `(${label(copy.sourceAccess, source.access)})`));
      list.append(item);
    });
    parent.append(list);
  };
  const addFact = (parent, labelText, value) => {
    const box = element('div', 'fj-fact');
    box.append(element('small', '', labelText));
    box.append(element('strong', '', value === null || value === '' ? copy.fieldFallback : value));
    parent.append(box);
  };
  const addPill = (parent, stateName) => parent.append(element('span', 'fj-pill', label(copy.stateLabels, stateName)));
  const formValue = element => element ? element.value : '';

  function renderEvent(event, isContext = false) {
    const article = element('article', 'fj-event');
    const head = element('div', 'fj-event-head');
    const heading = element('div');
    heading.append(element('small', 'fj-key', event.id));
    heading.append(element('h4', '', textFor(event.proposition)));
    head.append(heading);
    const meta = element('div', 'fj-meta');
    meta.append(element('span', 'fj-pill', event.date));
    meta.append(element('span', 'fj-pill', label(copy.layerLabels, event.layer)));
    meta.append(element('span', 'fj-pill', label(copy.evidenceLabels, event.evidence_status)));
    head.append(meta);
    article.append(head);
    const description = element('dl');
    const addDefinition = (term, value) => {
      if (!value) return;
      description.append(element('dt', '', term));
      description.append(element('dd', '', textFor(value)));
    };
    addDefinition(copy.limitation, event.limitation);
    addDefinition(copy.alternative, event.alternative_explanation);
    addDefinition(copy.next, event.next_document_needed);
    if (description.childElementCount) article.append(description);
    addSources(article, event.source_ids);
    if (isContext) article.dataset.context = 'true';
    return article;
  }

  function filteredProperties() {
    const query = state.search.trim().toLowerCase();
    return data.properties.filter(property => {
      const pieces = [property.registry_finca, property.unit, property.physical.apartment_or_local, property.historic_source_label.owner_as_listed_gesvalt, property.physical.type, property.physical.block_or_zone].filter(Boolean).join(' ').toLowerCase();
      return (!query || pieces.includes(query)) && (!state.type || property.physical.type === state.type) && (!state.block || property.physical.block_or_zone === state.block) && (!state.coverage || property.coverage_state === state.coverage);
    });
  }

  function renderPropertyList() {
    const filtered = filteredProperties();
    els.list.replaceChildren();
    if (!filtered.length) {
      els.list.append(element('p', 'fj-loading', lang === 'es' ? 'No hay fincas que coincidan con los filtros.' : 'No properties match the filters.'));
    }
    filtered.forEach(property => {
      const button = element('button', 'fj-property-button');
      button.type = 'button';
      button.dataset.finca = property.registry_finca;
      button.setAttribute('aria-current', String(property.registry_finca === state.finca));
      const pill = element('span', 'fj-pill', label(copy.stateLabels, property.coverage_state));
      pill.dataset.state = property.coverage_state;
      button.append(pill);
      const info = element('span');
      info.append(element('strong', '', `${copy.finca} ${property.registry_finca}`));
      info.append(element('small', '', `${copy.unit} ${property.unit} · ${label(copy.typeLabels, property.physical.type)} · ${property.physical.apartment_or_local || property.physical.horizontal_number || copy.fieldFallback}`));
      button.append(info);
      button.addEventListener('click', () => { state.finca = property.registry_finca; els.finca.value = state.finca; render(); });
      els.list.append(button);
    });
    els.count.textContent = `${filtered.length} / ${data.properties.length} ${copy.showing}`;
    if (!filtered.some(property => property.registry_finca === state.finca) && filtered[0]) {
      state.finca = filtered[0].registry_finca;
      els.finca.value = state.finca;
    }
  }

  function renderDetail() {
    const property = data.properties.find(item => item.registry_finca === state.finca) || data.properties[0];
    els.detail.replaceChildren();
    if (!property) return;
    const heading = element('div', 'fj-property-heading');
    const headingCopy = element('div');
    headingCopy.append(element('small', 'fj-key', `${copy.selected} · ${property.finca_id}`));
    headingCopy.append(element('h2', '', `${copy.finca} ${property.registry_finca}`));
    heading.append(headingCopy);
    const headingPill = element('span', 'fj-pill', label(copy.stateLabels, property.coverage_state));
    headingPill.dataset.state = property.coverage_state;
    heading.append(headingPill);
    els.detail.append(heading);

    els.detail.append(element('h3', '', copy.physical));
    const facts = element('div', 'fj-facts');
    addFact(facts, copy.unit, property.unit);
    addFact(facts, copy.type, label(copy.typeLabels, property.physical.type));
    addFact(facts, copy.aptLocal, property.physical.apartment_or_local || property.physical.horizontal_number);
    addFact(facts, copy.block, property.physical.block_or_zone.match(/^\d+$/) ? property.physical.block_or_zone : label(copy.zoneLabels, property.physical.block_or_zone));
    addFact(facts, copy.area, `${property.physical.area_m2} m²`);
    els.detail.append(facts);

    const historic = element('div', 'fj-notice');
    historic.append(element('strong', '', copy.historic));
    appendParagraph(historic, property.historic_source_label);
    appendParagraph(historic, textFor(data.defaults.historic_source_caution));
    addSources(historic, ['SP-BASE-262-GESVALT']);
    els.detail.append(historic);

    if (property.acquisition_overlay) {
      const overlay = element('div', 'fj-notice');
      overlay.append(element('strong', '', copy.overlay));
      appendParagraph(overlay, property.acquisition_overlay);
      appendParagraph(overlay, copy.overlayCaution);
      addSources(overlay, ['SP-OVERLAY-MATKATOR']);
      els.detail.append(overlay);
    }

    els.detail.append(element('h3', '', copy.journey));
    if (property.events.length) {
      const events = element('div', 'fj-event-list');
      property.events.forEach(event => events.append(renderEvent(event)));
      els.detail.append(events);
    } else {
      const gap = element('div', 'fj-notice alert');
      gap.append(element('strong', '', copy.noEvents));
      appendParagraph(gap, copy.noEventsExplanation);
      els.detail.append(gap);
    }

    (property.identifier_conflicts || []).forEach(conflict => {
      const box = element('div', 'fj-notice alert');
      box.append(element('strong', '', copy.conflict));
      appendParagraph(box, textFor(conflict.proposition));
      appendParagraph(box, `${copy.next}: ${textFor(conflict.next_document_needed)}`);
      addSources(box, conflict.source_ids);
      els.detail.append(box);
    });

    const questions = element('div', 'fj-notice ok');
    questions.append(element('strong', '', copy.questions));
    renderListOfText(questions, textFor(property.open_questions || data.defaults.open_questions));
    appendParagraph(questions, `${copy.next}: ${textFor(property.next_document_needed || data.defaults.next_document_needed)}`);
    els.detail.append(questions);

    const context = element('section', 'fj-context');
    context.append(element('h3', '', copy.separateContext));
    appendParagraph(context, copy.contextIntro);
    const timeline = element('div', 'fj-event-list');
    data.complex_context_events.forEach(event => timeline.append(renderEvent(event, true)));
    context.append(timeline);
    els.detail.append(context);
  }

  function render() {
    renderPropertyList();
    renderDetail();
  }

  function populateControls() {
    const appendOption = (select, value, text) => {
      const option = element('option', '', text);
      option.value = value;
      select.append(option);
    };
    els.finca.replaceChildren();
    data.properties.forEach(property => appendOption(els.finca, property.registry_finca, `${property.registry_finca} · ${property.physical.apartment_or_local || property.physical.horizontal_number || copy.fieldFallback}`));
    const types = [...new Set(data.properties.map(property => property.physical.type))].sort();
    const blocks = [...new Set(data.properties.map(property => property.physical.block_or_zone))].sort((a, b) => String(a).localeCompare(String(b), undefined, { numeric: true }));
    const states = Object.keys(copy.stateLabels);
    [els.type, els.block, els.coverage].forEach(select => { while (select.options.length > 1) select.remove(1); });
    types.forEach(value => appendOption(els.type, value, label(copy.typeLabels, value)));
    blocks.forEach(value => appendOption(els.block, value, /^\d+$/.test(value) ? value : label(copy.zoneLabels, value)));
    states.forEach(value => appendOption(els.coverage, value, label(copy.stateLabels, value)));
    els.finca.value = state.finca;
    els.total.textContent = data.coverage.total_properties;
    els.eventCount.textContent = data.coverage.properties_with_property_specific_events;
    els.sourceCount.textContent = data.source_ledger.length;
  }

  function bindControls() {
    els.search.addEventListener('input', event => { state.search = event.target.value; render(); });
    els.finca.addEventListener('change', event => { state.finca = event.target.value; render(); });
    els.type.addEventListener('change', event => { state.type = event.target.value; render(); });
    els.block.addEventListener('change', event => { state.block = event.target.value; render(); });
    els.coverage.addEventListener('change', event => { state.coverage = event.target.value; render(); });
  }

  async function initialise() {
    els.detail.replaceChildren(element('p', 'fj-loading', copy.loading));
    try {
      const response = await fetch('../../assets/data/sun-park-262-finca-journey-v1.json', { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      data = await response.json();
      if (!Array.isArray(data.properties) || data.properties.length !== 262) throw new Error('invalid 262-property projection');
      if (!data.properties.some(property => property.registry_finca === state.finca)) state.finca = data.properties[0].registry_finca;
      populateControls();
      bindControls();
      render();
    } catch (error) {
      els.detail.replaceChildren(element('p', 'fj-error', copy.error));
      els.list.replaceChildren(element('p', 'fj-error', copy.error));
      els.count.textContent = copy.fieldFallback;
      root.dataset.loadError = 'true';
      console.error('262-finca journey data failed to load', error);
    }
  }

  initialise();
})();
