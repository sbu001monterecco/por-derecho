(() => {
  'use strict';

  const script = document.currentScript;
  const root = document.querySelector('[data-unitary-gap-closure]');
  if (!script || !root || root.dataset.rendered === 'true') return;

  const repo = new URL('../', new URL('.', script.src));
  const lang = document.documentElement.lang.toLowerCase().startsWith('es') ? 'es' : 'en';
  const dataUrl = new URL('assets/data/unitary-multitrack-criminal-first-gap-closure-v1.json', repo);
  const authorityDataUrl = new URL('assets/data/community-acta-authority-interconnectivity-v1.json', repo);
  const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[char]));
  const loc = (item, key) => item?.[`${key}_${lang}`] ?? item?.[lang] ?? item?.[`${key}_en`] ?? item?.[`${key}_es`] ?? '';
  const internal = (path, fragment = '') => `${new URL(path, repo).href}${fragment}`;

  const copy = lang === 'es' ? {
    skip: 'Saltar al registro de brechas',
    summaryKicker: 'Lectura fiscal · 90 segundos',
    summaryTitle: 'Una teoría falsable, una prueba unitaria, salidas separadas.',
    directPositionLabel: 'Posición penal directa atribuida · sin dilución',
    denominatorKicker: 'Denominadores reconciliados',
    denominatorTitle: 'Qué cuenta cada número y por qué no deben fusionarse.',
    legendKicker: 'Código visual y textual',
    legendTitle: 'Siete clases probatorias; el color nunca actúa solo.',
    chainKicker: 'Ingeniería inversa',
    chainTitle: 'Resultado actual → origen → prueba causal hacia delante.',
    chainBoundary: 'Las flechas muestran preguntas de dependencia y producción. No prueban sucesión jurídica, mando común, concierto, conocimiento, dolo, causalidad, delito ni culpabilidad. C1/C2 son fases atribuidas; D-MIXED/D-OPEN son estados de prueba.',
    authorityKicker: 'Autoridad → legitimidad aparente → uso',
    authorityTitle: 'Diez etapas documentales; ninguna flecha transmite responsabilidad penal.',
    carried: 'Premisa alegadamente transportada',
    test: 'Prueba penal/fiscal de la etapa',
    openGaps: 'Brechas de cierre',
    specialist: 'Abrir control especialista',
    noticeKicker: 'Checkpoint institucional',
    noticeTitle: 'Primera respuesta de Intervención General: aviso y remisión, no fondo.',
    verified: 'Contenido primario verificado',
    caretState: 'Auditoría ^ / identidad',
    communicationsKicker: 'Comunicación pública → tratamiento → decisión',
    communicationsTitle: 'Diecinueve eventos canónicos en cinco niveles institucionales.',
    communicationsBoundary: 'El nivel institucional y la materia de fondos son ejes distintos. SNCA y la Dirección General de Fondos Europeos son órganos estatales españoles; solo Fiscalía Europea se muestra en el nivel UE. Ningún acuse prueba incorporación, examen, adopción, utilización, dolo o culpabilidad.',
    communicationSearch: 'Buscar evento, órgano, referencia o expediente',
    authorityTier: 'Nivel institucional',
    communicationsShown: 'comunicaciones mostradas',
    proves: 'Acredita',
    doesNotProve: 'No acredita',
    handling: 'Escalera de tratamiento',
    identity: 'Identidad CAEPR',
    source: 'Abrir fuente pública',
    masterFiles: 'Expedientes maestros',
    noMaster: 'enlace maestro abierto',
    canonicalEvent: 'Ancla canónica',
    tierLabels: {ES_LOCAL_MUNICIPAL:'LOCAL', ES_ISLAND_CABILDO:'CABILDO', ES_CANARY_AUTONOMOUS:'AUT', ES_STATE:'EST', EU_SUPRANATIONAL:'UE'},
    handlingLabels: {transmission:'transmisión', registration:'registro', delivery:'entrega', routing:'remisión', incorporation:'incorporación', examination:'examen', verification_or_rejection:'verificación/rechazo', adoption:'adopción', decision_or_use:'decisión/uso', effect:'efecto', causation:'causalidad', benefit_or_loss:'beneficio/pérdida'},
    tracksKicker: '18 pistas unificadas',
    tracksTitle: 'Un grafo común; ninguna pista sustituye a otra.',
    trackSearch: 'Buscar pista o pregunta',
    evidenceFilter: 'Clase probatoria',
    all: 'Todas',
    tracksShown: 'pistas mostradas',
    thresholdKicker: 'Matriz penal/fiscal',
    thresholdTitle: 'Cinco hipótesis; diecisiete campos de prueba actor-específica.',
    actorCapacity: 'Actor y capacidad',
    act: 'Acto o problema alegado',
    knowledge: 'Conocimiento e intención',
    useEffect: 'Uso, efecto y beneficio',
    contrary: 'Explicación contraria/lícita',
    openProof: 'Prueba abierta',
    relevance: 'Relevancia potencial, solo si encajan los elementos',
    sources: 'Referencias controladas',
    gapsKicker: 'Registro canónico de brechas',
    gapsTitle: 'Dieciséis obligaciones de producción, cada una con ID y ancla propia.',
    gapSearch: 'Buscar ID, título, custodio o cierre',
    priority: 'Prioridad',
    status: 'Estado',
    shown: 'brechas mostradas',
    gap: 'Brecha',
    tracks: 'Pistas',
    custodian: 'Custodio / universo',
    closure: 'Prueba de cierre',
    canonical: 'Referencia canónica',
    contraryKicker: 'Contradicción y falsación',
    contraryTitle: 'La hipótesis debe sobrevivir a la mejor explicación lícita.',
    acquisitionKicker: 'Adquisición y custodia',
    acquisitionTitle: 'Qué se revisó y qué no se adquirió en esta ejecución.',
    scope: 'Ámbito',
    universe: 'Universo',
    result: 'Resultado',
    boundary: 'Límite',
    outputKicker: 'Orden de trabajo',
    outputTitle: 'Penal/fiscal primero; remedios paralelos, no mezclados.',
    loading: 'Cargando el control unitario…',
    error: 'No se pudo cargar el control unitario.',
    actions: {
      lph: 'Control LPH · 122 referencias', authority: 'ACTAS ↔ 49 expedientes', room: 'Sala documental ACTAS', deFacto: 'Administración de hecho', insolvency: 'Concurso · penal unitario', ricpe: 'RIC/RICPE', intervention: 'Intervención General', gaps: 'Cerrar brechas'
    },
    outputLabels: {
      criminal_prosecutorial: 'penal / Fiscalía', civil_horizontal_property: 'civil / LPH', insolvency: 'concursal', administrative: 'administrativo', regulatory_public_funds: 'regulatorio / fondos', professional_discipline: 'profesional / disciplina', recovery_restitution: 'recuperación / restitución'
    }
  } : {
    skip: 'Skip to the gap register',
    summaryKicker: 'Prosecutorial read · 90 seconds',
    summaryTitle: 'One falsifiable theory, one unitary proof record, separate outputs.',
    directPositionLabel: 'Direct attributed criminal position · without dilution',
    denominatorKicker: 'Reconciled denominators',
    denominatorTitle: 'What each number counts and why they must not be collapsed.',
    legendKicker: 'Visual and textual code',
    legendTitle: 'Seven evidence classes; colour never acts alone.',
    chainKicker: 'Reverse engineering',
    chainTitle: 'Current outcome → origin → forward causal test.',
    chainBoundary: 'Arrows show reliance and production questions. They do not prove legal succession, common command, agreement, knowledge, intent, causation, offence or guilt. C1/C2 are attributed phases; D-MIXED/D-OPEN are evidence statuses.',
    authorityKicker: 'Authority → apparent legitimacy → use',
    authorityTitle: 'Ten documentary stages; no arrow transfers criminal responsibility.',
    carried: 'Premise allegedly carried forward',
    test: 'Criminal/prosecutorial test at this stage',
    openGaps: 'Closure gaps',
    specialist: 'Open specialist control',
    noticeKicker: 'Institutional checkpoint',
    noticeTitle: 'First Intervención General response: notice and routing, not merits.',
    verified: 'Verified primary content',
    caretState: '^ audit / identity',
    communicationsKicker: 'Public communication → handling → decision',
    communicationsTitle: 'Nineteen canonical events across five institutional tiers.',
    communicationsBoundary: 'Institutional tier and funding subject are separate axes. SNCA and the Directorate-General for European Funds are Spanish State bodies; only the European Public Prosecutor route is shown at EU tier. No receipt proves incorporation, examination, adoption, reliance, intent or guilt.',
    communicationSearch: 'Search event, office, reference or file',
    authorityTier: 'Institutional tier',
    communicationsShown: 'communications shown',
    proves: 'Proves',
    doesNotProve: 'Does not prove',
    handling: 'Handling ladder',
    identity: 'CAEPR identity',
    source: 'Open public source',
    masterFiles: 'Master files',
    noMaster: 'master link open',
    canonicalEvent: 'Canonical anchor',
    tierLabels: {ES_LOCAL_MUNICIPAL:'LOCAL', ES_ISLAND_CABILDO:'CABILDO', ES_CANARY_AUTONOMOUS:'AUT', ES_STATE:'STATE', EU_SUPRANATIONAL:'EU'},
    handlingLabels: {transmission:'transmission', registration:'registration', delivery:'delivery', routing:'routing', incorporation:'incorporation', examination:'examination', verification_or_rejection:'verification/rejection', adoption:'adoption', decision_or_use:'decision/use', effect:'effect', causation:'causation', benefit_or_loss:'benefit/loss'},
    tracksKicker: '18 unified tracks',
    tracksTitle: 'One common graph; no track substitutes for another.',
    trackSearch: 'Search track or question',
    evidenceFilter: 'Evidence class',
    all: 'All',
    tracksShown: 'tracks shown',
    thresholdKicker: 'Criminal/prosecutorial matrix',
    thresholdTitle: 'Five hypotheses; seventeen actor-specific proof fields.',
    actorCapacity: 'Actor and capacity',
    act: 'Alleged act or issue',
    knowledge: 'Knowledge and intent',
    useEffect: 'Use, effect and benefit',
    contrary: 'Contrary/lawful explanation',
    openProof: 'Open proof',
    relevance: 'Potential relevance, only if the elements fit',
    sources: 'Controlled references',
    gapsKicker: 'Canonical gap register',
    gapsTitle: 'Sixteen production obligations, each with its own ID and anchor.',
    gapSearch: 'Search ID, title, custodian or closure',
    priority: 'Priority',
    status: 'Status',
    shown: 'gaps shown',
    gap: 'Gap',
    tracks: 'Tracks',
    custodian: 'Custodian / universe',
    closure: 'Closure test',
    canonical: 'Canonical reference',
    contraryKicker: 'Contradiction and falsification',
    contraryTitle: 'The hypothesis must survive the strongest lawful explanation.',
    acquisitionKicker: 'Acquisition and custody',
    acquisitionTitle: 'What was reviewed and what this run did not acquire.',
    scope: 'Scope',
    universe: 'Universe',
    result: 'Result',
    boundary: 'Boundary',
    outputKicker: 'Work order',
    outputTitle: 'Criminal/prosecutorial first; parallel remedies kept distinct.',
    loading: 'Loading the unitary control…',
    error: 'The unitary control could not be loaded.',
    actions: {
      lph: 'LPH control · 122 references', authority: 'ACTAs ↔ 49 files', room: 'ACTA document room', deFacto: 'De facto administration', insolvency: 'Insolvency · unitary criminal', ricpe: 'RIC/RICPE', intervention: 'Intervención General', gaps: 'Close gaps'
    },
    outputLabels: {
      criminal_prosecutorial: 'criminal / prosecution', civil_horizontal_property: 'civil / LPH', insolvency: 'insolvency', administrative: 'administrative', regulatory_public_funds: 'regulatory / funds', professional_discipline: 'professional / discipline', recovery_restitution: 'recovery / restitution'
    }
  };

  let data;
  let authorityData;
  let classById;

  function evidenceBadge(id) {
    const item = classById.get(id);
    if (!item) return '';
    return `<span class="pd-ucf-badge" data-evidence-class="${esc(id)}" data-symbol="${esc(item.symbol)}">${esc(id)}</span>`;
  }

  function refList(refs) {
    return `<span class="pd-ucf-ref-list">${(refs || []).map((ref) => `<code>${esc(ref)}</code>`).join('')}</span>`;
  }

  function renderTracks() {
    const query = root.querySelector('[data-ucf-track-search]').value.trim().toLowerCase();
    const evidence = root.querySelector('[data-ucf-track-class]').value;
    const rows = data.tracks.filter((track) => {
      const haystack = [track.id, loc(track, 'label'), loc(track, 'criminal_question'), ...track.primary_classes].join(' ').toLowerCase();
      return (!query || haystack.includes(query)) && (!evidence || track.primary_classes.includes(evidence));
    });
    root.querySelector('[data-ucf-track-grid]').innerHTML = rows.map((track) => `
      <article class="pd-ucf-track" data-ucf-track="${esc(track.id)}">
        <header><code>${esc(track.id)}</code><span class="pd-ucf-badges">${track.primary_classes.map(evidenceBadge).join('')}</span></header>
        <h3>${esc(loc(track, 'label'))}</h3>
        <p>${esc(loc(track, 'criminal_question'))}</p>
      </article>`).join('');
    root.querySelector('[data-ucf-track-count]').textContent = `${rows.length} / ${data.tracks.length} ${copy.tracksShown}`;
  }

  function renderGaps() {
    const query = root.querySelector('[data-ucf-gap-search]').value.trim().toLowerCase();
    const priority = root.querySelector('[data-ucf-gap-priority]').value;
    const status = root.querySelector('[data-ucf-gap-status]').value;
    const rows = data.gaps.filter((gap) => {
      const haystack = [gap.id, gap.priority, gap.status, loc(gap, 'title'), loc(gap, 'custodian'), loc(gap, 'closure'), ...gap.tracks, ...gap.source_refs].join(' ').toLowerCase();
      return (!query || haystack.includes(query)) && (!priority || gap.priority === priority) && (!status || gap.status === status);
    });
    root.querySelector('[data-ucf-gap-body]').innerHTML = rows.map((gap) => `
      <tr class="pd-ucf-gap-row" id="gap-${esc(gap.id)}" data-ucf-gap="${esc(gap.id)}">
        <th scope="row"><code>${esc(gap.id)}</code><br><span class="pd-ucf-priority">${esc(gap.priority)}</span></th>
        <td><strong>${esc(loc(gap, 'title'))}</strong><br>${refList(gap.source_refs)}</td>
        <td><span class="pd-ucf-status">${esc(gap.status)}</span></td>
        <td>${gap.tracks.map((id) => `<code>${esc(id)}</code>`).join(' ')}</td>
        <td>${esc(loc(gap, 'custodian'))}</td>
        <td>${esc(loc(gap, 'closure'))}</td>
        <td><a href="#gap-${encodeURIComponent(gap.id)}">#gap-${esc(gap.id)}</a></td>
      </tr>`).join('');
    root.querySelector('[data-ucf-gap-count]').textContent = `${rows.length} / ${data.gaps.length} ${copy.shown}`;
  }

  function handlingClass(value) {
    const state = String(value || 'OPEN');
    if (state === 'NOT_PROVEN') return 'not-proven';
    if (state.includes('PROVEN') && !state.startsWith('NOT_')) return 'proven';
    if (state === 'OPEN') return 'open';
    return 'limited';
  }

  function renderCommunications() {
    const query = root.querySelector('[data-ucf-communication-search]').value.trim().toLowerCase();
    const tier = root.querySelector('[data-ucf-communication-tier]').value;
    const rows = authorityData.public_communications.filter((event) => {
      const haystack = [event.event_id, event.institution_label, event.official_reference, event.primary_authority_tier_id,
        loc(event, 'summary'), ...(event.master_ids || []), ...(event.context_master_ids || []), ...(event.gap_ids || [])].join(' ').toLowerCase();
      return (!query || haystack.includes(query)) && (!tier || event.primary_authority_tier_id === tier);
    });
    const authorityRoute = data.specialist_links[`authority_${lang}`];
    root.querySelector('[data-ucf-communication-grid]').innerHTML = rows.map((event) => {
      const identity = event.institution_identity_state === 'CARET_CONFIRMED'
        ? `${esc(event.institution_label)}<sup aria-label="CAEPR identity confirmed">^</sup> · <code>${esc(event.institution_id)}</code>`
        : `${esc(event.institution_label)} · <code>${esc(event.institution_identity_state)}</code>`;
      const masters = (event.master_ids || []).map((id) => `<a href="${esc(internal(authorityRoute, `#authority=${encodeURIComponent(id)}`))}"><code>${esc(id)}</code></a>`).join(' ')
        || `<span class="pd-ucf-open-text">${esc(copy.noMaster)}</span>`;
      const sourceHref = internal(event.source_anchor);
      const handling = Object.entries(event.handling_state).map(([key, value]) => `
        <li data-handling-state="${esc(handlingClass(value))}"><span>${esc(copy.handlingLabels[key] || key)}</span><strong>${esc(value)}</strong></li>`).join('');
      return `<article class="pd-ucf-communication" id="communication-${esc(event.event_id)}" data-authority-tier="${esc(event.primary_authority_tier_id)}">
        <header><div><span class="pd-ucf-tier">${esc(copy.tierLabels[event.primary_authority_tier_id] || event.primary_authority_tier_id)}</span><code>${esc(event.event_id)}</code></div><time>${esc(event.date)}</time></header>
        <h3>${esc(event.official_reference)}</h3>
        <p class="pd-ucf-identity"><strong>${esc(copy.identity)}:</strong> ${identity}</p>
        <p>${esc(loc(event, 'summary'))}</p>
        <div class="pd-ucf-badges">${event.evidence_classes.map(evidenceBadge).join('')}</div>
        <dl><div><dt>${esc(copy.proves)}</dt><dd>${esc(loc(event, 'proves'))}</dd></div><div><dt>${esc(copy.doesNotProve)}</dt><dd>${esc(loc(event, 'does_not_prove'))}</dd></div></dl>
        <h4>${esc(copy.handling)}</h4><ol class="pd-ucf-handling">${handling}</ol>
        <p><strong>${esc(copy.masterFiles)}:</strong> ${masters}</p>
        <p><strong>${esc(copy.openGaps)}:</strong> ${event.gap_ids.map((id) => `<a href="#gap-${encodeURIComponent(id)}"><code>${esc(id)}</code></a>`).join(' ')}</p>
        <footer><a href="${esc(sourceHref)}">${esc(copy.source)} →</a><a href="#communication-${encodeURIComponent(event.event_id)}">${esc(copy.canonicalEvent)} #</a></footer>
      </article>`;
    }).join('');
    root.querySelector('[data-ucf-communication-count]').textContent = `${rows.length} / ${authorityData.public_communications.length} ${copy.communicationsShown}`;
  }

  function applyHash() {
    if (!location.hash) return;
    const id = decodeURIComponent(location.hash.slice(1));
    const target = document.getElementById(id);
    if (target) requestAnimationFrame(() => target.scrollIntoView({block: 'center'}));
  }

  function render() {
    classById = new Map(data.evidence_classes.map((item) => [item.id, item]));
    const links = data.specialist_links;
    const lph = internal(links[`lph_${lang}`]);
    const authority = internal(links[`authority_${lang}`]);
    const room = internal(links[`acta_room_${lang}`]);
    const deFacto = internal(links[`de_facto_${lang}`]);
    const insolvency = internal(links[`insolvency_criminal_${lang}`]);
    const ricpe = internal(links[`ricpe_${lang}`]);
    const intervention = internal(links[`intervencion_${lang}`]);
    const edgeByFrom = new Map(data.reverse_chain.edges.map((edge) => [edge.from, edge]));
    const priorities = [...new Set(data.gaps.map((gap) => gap.priority))].sort();
    const statuses = [...new Set(data.gaps.map((gap) => gap.status))].sort();
    const authorityTiers = authorityData.authority_tiers.filter((tier) => tier.event_count > 0);

    root.innerHTML = `<a class="skip-link" href="#unitary-gap-register">${esc(copy.skip)}</a>
      <div class="pd-ucf">
        <section class="pd-ucf-header" aria-labelledby="pd-ucf-title">
          <p class="eyebrow">${esc(data.control_id)} · ${esc(data.control_date)} · ${esc(data.status)}</p>
          <h1 id="pd-ucf-title">${esc(loc(data, 'title'))}</h1>
          <p class="lead">${esc(loc(data, 'subtitle'))}</p>
          <div class="pd-ucf-direct-position"><strong>HIP · ${esc(copy.directPositionLabel)}</strong><p>${esc(loc(data, 'direct_criminal_position'))}</p><p>${esc(loc(data, 'non_dilution_rule'))}</p></div>
          <div class="pd-ucf-boundary"><strong>${esc(copy.boundary)}.</strong> ${esc(loc(data, 'publication_boundary'))}</div>
          <div class="pd-ucf-caret-rule"><strong>^</strong> ${esc(loc(data, 'identity_reference_rule'))}</div>
          <nav class="pd-ucf-actions" aria-label="Specialist controls">
            <a href="${esc(lph)}">${esc(copy.actions.lph)}</a>
            <a href="${esc(authority)}">${esc(copy.actions.authority)}</a>
            <a href="${esc(room)}">${esc(copy.actions.room)}</a>
            <a href="${esc(deFacto)}">${esc(copy.actions.deFacto)}</a>
            <a href="${esc(insolvency)}">${esc(copy.actions.insolvency)}</a>
            <a href="${esc(ricpe)}">${esc(copy.actions.ricpe)}</a>
            <a href="${esc(intervention)}">${esc(copy.actions.intervention)}</a>
            <a href="#unitary-gap-register">${esc(copy.actions.gaps)}</a>
          </nav>
        </section>

        <section class="pd-ucf-section" id="unitary-90-second-summary">
          <header><div><p class="eyebrow">${esc(copy.summaryKicker)}</p><h2>${esc(copy.summaryTitle)}</h2></div></header>
          <ol class="pd-ucf-summary">${data.executive_summary.map((item) => `<li>${esc(loc(item, ''))}</li>`).join('')}</ol>
        </section>

        <section class="pd-ucf-section" id="unitary-denominator-crosswalk">
          <header><div><p class="eyebrow">${esc(copy.denominatorKicker)}</p><h2>${esc(copy.denominatorTitle)}</h2></div></header>
          <div class="pd-ucf-metrics">${data.denominator_crosswalk.map((item) => `<article class="pd-ucf-metric"><strong>${esc(item.value)}</strong><span>${esc(loc(item, 'label'))}</span><small><code>${esc(item.id)}</code></small></article>`).join('')}</div>
        </section>

        <section class="pd-ucf-section" id="unitary-evidence-legend">
          <header><div><p class="eyebrow">${esc(copy.legendKicker)}</p><h2>${esc(copy.legendTitle)}</h2></div></header>
          <div class="pd-ucf-legend">${data.evidence_classes.map((item) => `<article class="pd-ucf-class" data-evidence-class="${esc(item.id)}"><div><b>${esc(item.symbol)}</b><strong>${esc(item.id)} · ${esc(loc(item, 'label'))}</strong></div><p>${esc(loc(item, 'meaning'))}</p></article>`).join('')}</div>
        </section>

        <section class="pd-ucf-section" id="unitary-reverse-chain">
          <header><div><p class="eyebrow">${esc(copy.chainKicker)}</p><h2>${esc(copy.chainTitle)}</h2></div></header>
          <div class="pd-ucf-chain">${data.reverse_chain.nodes.map((node) => {
            const outgoing = edgeByFrom.get(node.id);
            const primary = node.classes.includes('HIP') ? 'HIP' : node.classes[0];
            return `<article class="pd-ucf-node" data-primary-class="${esc(primary)}" data-ucf-node="${esc(node.id)}"><header><code>${esc(node.id)}</code><time>${esc(node.date)}</time></header><h3>${esc(loc(node, 'label'))}</h3><p>${esc(loc(node, 'detail'))}</p><div class="pd-ucf-badges">${node.classes.map(evidenceBadge).join('')}</div>${outgoing ? `<p><a href="#gap-${encodeURIComponent(outgoing.closure_gap)}">${esc(outgoing.status)} → ${esc(outgoing.closure_gap)}</a></p>` : ''}</article>`;
          }).join('')}</div>
          <p class="pd-ucf-chain-boundary"><strong>${esc(copy.boundary)}.</strong> ${esc(copy.chainBoundary)}</p>
        </section>

        <section class="pd-ucf-section" id="unitary-authority-propagation">
          <header><div><p class="eyebrow">${esc(copy.authorityKicker)}</p><h2>${esc(copy.authorityTitle)}</h2></div></header>
          <p class="pd-ucf-authority-thesis">${esc(loc(data.authority_legitimacy_propagation, 'thesis'))}</p>
          <div class="pd-ucf-authority-flow">${data.authority_legitimacy_propagation.stages.map((stage) => {
            const primary = stage.classes.includes('HIP') ? 'HIP' : stage.classes[0];
            const route = internal(loc(stage, 'route'));
            return `<article class="pd-ucf-authority-stage" id="authority-${esc(stage.id)}" data-primary-class="${esc(primary)}" data-ucf-authority-stage="${esc(stage.id)}"><header><code>${esc(stage.id)}</code><time>${esc(stage.period)}</time></header><h3>${esc(loc(stage, 'label'))}</h3><dl><div><dt>${esc(copy.carried)}</dt><dd>${esc(loc(stage, 'proposition'))}</dd></div><div><dt>${esc(copy.test)}</dt><dd>${esc(loc(stage, 'test'))}</dd></div></dl><div class="pd-ucf-badges">${stage.classes.map(evidenceBadge).join('')}</div><p><strong>${esc(copy.openGaps)}:</strong> ${stage.gap_ids.map((id) => `<a href="#gap-${encodeURIComponent(id)}"><code>${esc(id)}</code></a>`).join(' ')}</p><p><strong>${esc(copy.sources)}:</strong> ${refList(stage.source_refs)}</p><p><a class="pd-ucf-specialist-link" href="${esc(route)}">${esc(copy.specialist)} →</a></p></article>`;
          }).join('')}</div>
          <p class="pd-ucf-chain-boundary"><strong>${esc(copy.boundary)}.</strong> ${esc(loc(data.authority_legitimacy_propagation, 'responsibility_boundary'))}</p>
          <article class="pd-ucf-notice-checkpoint" id="evidence-${esc(data.authority_legitimacy_propagation.notice_checkpoint.id)}">
            <header><div><p class="eyebrow">${esc(copy.noticeKicker)}</p><h3>${esc(copy.noticeTitle)}</h3></div><code>${esc(data.authority_legitimacy_propagation.notice_checkpoint.id)}</code></header>
            <p><strong>${esc(loc(data.authority_legitimacy_propagation.notice_checkpoint, 'label'))}</strong> · <code>${esc(data.authority_legitimacy_propagation.notice_checkpoint.master_file_id)}</code></p>
            <p><strong>${esc(copy.verified)}:</strong> ${esc(loc(data.authority_legitimacy_propagation.notice_checkpoint, 'verified_content'))}</p>
            <p class="pd-ucf-notice-boundary"><strong>${esc(copy.boundary)}:</strong> ${esc(loc(data.authority_legitimacy_propagation.notice_checkpoint, 'evidential_boundary'))}</p>
            <p><strong>${esc(copy.caretState)}:</strong> <code>${esc(data.authority_legitimacy_propagation.notice_checkpoint.caret_command_audit_label)}</code> · <code>${esc(data.authority_legitimacy_propagation.notice_checkpoint.presentation_caret_state)}</code> · <code>${esc(data.authority_legitimacy_propagation.notice_checkpoint.issuing_institution_identity_state)}</code></p>
            <p><a class="pd-ucf-specialist-link" href="${esc(intervention)}">${esc(copy.actions.intervention)} →</a> <a href="#gap-PD-GAP-UCF-016"><code>PD-GAP-UCF-016</code></a></p>
          </article>
        </section>

        <section class="pd-ucf-section" id="unitary-public-authority-communications">
          <header><div><p class="eyebrow">${esc(copy.communicationsKicker)}</p><h2>${esc(copy.communicationsTitle)}</h2></div><span class="pd-ucf-count" data-ucf-communication-count></span></header>
          <p class="pd-ucf-chain-boundary"><strong>${esc(copy.boundary)}.</strong> ${esc(copy.communicationsBoundary)}</p>
          <div class="pd-ucf-tier-summary">${authorityTiers.map((tier) => `<article data-authority-tier="${esc(tier.id)}"><strong>${esc(tier.event_count)}</strong><span>${esc(loc(tier, 'label'))}</span><small>${esc(copy.tierLabels[tier.id] || tier.id)}</small></article>`).join('')}</div>
          <div class="pd-ucf-controls">
            <label>${esc(copy.communicationSearch)}<input type="search" data-ucf-communication-search></label>
            <label>${esc(copy.authorityTier)}<select data-ucf-communication-tier><option value="">${esc(copy.all)}</option>${authorityTiers.map((tier) => `<option value="${esc(tier.id)}">${esc(copy.tierLabels[tier.id] || tier.id)} · ${esc(loc(tier, 'label'))} (${esc(tier.event_count)})</option>`).join('')}</select></label>
          </div>
          <div class="pd-ucf-communication-grid" data-ucf-communication-grid></div>
          <p class="pd-ucf-chain-boundary"><strong>${esc(copy.boundary)}.</strong> ${esc(loc(authorityData.communication_scan_control, 'responsibility_boundary'))}</p>
        </section>

        <section class="pd-ucf-section" id="unitary-track-matrix">
          <header><div><p class="eyebrow">${esc(copy.tracksKicker)}</p><h2>${esc(copy.tracksTitle)}</h2></div><span class="pd-ucf-count" data-ucf-track-count></span></header>
          <div class="pd-ucf-controls">
            <label>${esc(copy.trackSearch)}<input type="search" data-ucf-track-search></label>
            <label>${esc(copy.evidenceFilter)}<select data-ucf-track-class><option value="">${esc(copy.all)}</option>${data.evidence_classes.map((item) => `<option value="${esc(item.id)}">${esc(item.id)} · ${esc(loc(item, 'label'))}</option>`).join('')}</select></label>
          </div>
          <div class="pd-ucf-track-grid" data-ucf-track-grid></div>
        </section>

        <section class="pd-ucf-section" id="unitary-criminal-threshold-matrix">
          <header><div><p class="eyebrow">${esc(copy.thresholdKicker)}</p><h2>${esc(copy.thresholdTitle)}</h2></div></header>
          <div class="pd-ucf-thresholds">${data.criminal_threshold_hypotheses.map((item) => `<article class="pd-ucf-threshold" id="hypothesis-${esc(item.id)}"><header><div><code>${esc(item.id)}</code><h3>${esc(loc(item, 'label'))}</h3></div><strong>${esc(item.status)}</strong></header><dl><div><dt>${esc(copy.actorCapacity)}</dt><dd>${esc(loc(item, 'actor_capacity'))}</dd></div><div><dt>${esc(copy.act)}</dt><dd>${esc(loc(item, 'act'))}</dd></div><div><dt>${esc(copy.knowledge)}</dt><dd>${esc(loc(item, 'knowledge_intent'))}</dd></div><div><dt>${esc(copy.useEffect)}</dt><dd>${esc(loc(item, 'use_effect_benefit'))}</dd></div><div><dt>${esc(copy.contrary)}</dt><dd>${esc(loc(item, 'contrary'))}</dd></div><div><dt>${esc(copy.openProof)}</dt><dd>${esc(loc(item, 'open_proof'))}</dd></div></dl><p><strong>${esc(copy.relevance)}:</strong> ${item.potential_relevance.map((value) => `<code>${esc(value)}</code>`).join(' · ')}</p><p><strong>${esc(copy.sources)}:</strong> ${refList(item.source_refs)}</p></article>`).join('')}</div>
        </section>

        <section class="pd-ucf-section" id="unitary-gap-register">
          <header><div><p class="eyebrow">${esc(copy.gapsKicker)}</p><h2>${esc(copy.gapsTitle)}</h2></div><span class="pd-ucf-count" data-ucf-gap-count></span></header>
          <div class="pd-ucf-controls">
            <label>${esc(copy.gapSearch)}<input type="search" data-ucf-gap-search></label>
            <label>${esc(copy.priority)}<select data-ucf-gap-priority><option value="">${esc(copy.all)}</option>${priorities.map((value) => `<option>${esc(value)}</option>`).join('')}</select></label>
            <label>${esc(copy.status)}<select data-ucf-gap-status><option value="">${esc(copy.all)}</option>${statuses.map((value) => `<option>${esc(value)}</option>`).join('')}</select></label>
          </div>
          <div class="pd-ucf-table-wrap"><table class="pd-ucf-table"><thead><tr><th>${esc(copy.canonical)}</th><th>${esc(copy.gap)}</th><th>${esc(copy.status)}</th><th>${esc(copy.tracks)}</th><th>${esc(copy.custodian)}</th><th>${esc(copy.closure)}</th><th>URL</th></tr></thead><tbody data-ucf-gap-body></tbody></table></div>
        </section>

        <section class="pd-ucf-section" id="unitary-contrary-acquisition">
          <div class="pd-ucf-two"><div><header><p class="eyebrow">${esc(copy.contraryKicker)}</p><h2>${esc(copy.contraryTitle)}</h2></header><ol class="pd-ucf-list">${data.contrary_evidence.map((item) => `<li><code>${esc(item.id)}</code> ${esc(loc(item, ''))}</li>`).join('')}</ol></div><div><header><p class="eyebrow">${esc(copy.acquisitionKicker)}</p><h2>${esc(copy.acquisitionTitle)}</h2></header><div class="pd-ucf-acquisition">${data.acquisition_log.map((item) => `<article><header><code>${esc(item.id)}</code><time>${esc(item.date)}</time></header><p><strong>${esc(copy.scope)}:</strong> ${esc(loc(item, 'scope'))}</p><p><strong>${esc(copy.universe)}:</strong> ${esc(loc(item, 'universe'))}</p><p><strong>${esc(copy.result)}:</strong> ${esc(item.result)}</p><p><strong>${esc(copy.boundary)}:</strong> ${esc(loc(item, 'boundary'))}</p></article>`).join('')}</div></div></div>
        </section>

        <section class="pd-ucf-section" id="unitary-output-order">
          <header><div><p class="eyebrow">${esc(copy.outputKicker)}</p><h2>${esc(copy.outputTitle)}</h2></div></header>
          <ol class="pd-ucf-output-order">${data.method.output_order.map((item) => `<li>${esc(copy.outputLabels[item] || item)}</li>`).join('')}</ol>
        </section>
      </div>`;

    root.dataset.rendered = 'true';
    root.querySelector('[data-ucf-track-search]').addEventListener('input', renderTracks);
    root.querySelector('[data-ucf-track-class]').addEventListener('change', renderTracks);
    root.querySelector('[data-ucf-gap-search]').addEventListener('input', renderGaps);
    root.querySelector('[data-ucf-gap-priority]').addEventListener('change', renderGaps);
    root.querySelector('[data-ucf-gap-status]').addEventListener('change', renderGaps);
    root.querySelector('[data-ucf-communication-search]').addEventListener('input', renderCommunications);
    root.querySelector('[data-ucf-communication-tier]').addEventListener('change', renderCommunications);
    renderTracks();
    renderGaps();
    renderCommunications();
    applyHash();
    addEventListener('hashchange', applyHash);
  }

  root.innerHTML = `<div class="pd-ucf"><p>${esc(copy.loading)}</p></div>`;
  Promise.all([dataUrl, authorityDataUrl].map((url) => fetch(url, {cache: 'no-store'}).then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })))
    .then(([unitaryPayload, authorityPayload]) => { data = unitaryPayload; authorityData = authorityPayload; render(); })
    .catch((error) => {
      root.innerHTML = `<div class="pd-ucf"><p class="pd-ucf-error" role="alert">${esc(copy.error)} ${esc(error.message)}</p></div>`;
    });
})();
