(() => {
  'use strict';

  const current = document.currentScript;
  if (!current) return;
  const pathname = window.location.pathname.replace(/\/index\.html$/, '/');
  const isHome = /\/(?:por-derecho\/)?(?:es\/|en\/)?$/.test(pathname);
  if (!isHome) return;

  const lang = (document.documentElement.lang || 'es').toLowerCase().startsWith('en') ? 'en' : 'es';
  const assetBase = new URL('.', current.src);
  const siteRoot = new URL('../', assetBase);
  const dataUrl = (path) => new URL(path.replace(/^\//, ''), siteRoot).href;
  const escapeHtml = (value) => String(value ?? '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#039;');

  const legalSuffixes = /\b(s\.?l\.?u?|s\.?a\.?u?|s\.?a|s\.?l\.?p|scr|s\.c\.r|bv|b\.v|llp|lp|l\.p|limited|sociedad limitada|sociedad anonima)\b/g;
  const normalise = (value) => String(value ?? '')
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .toLowerCase().replace(/[–—]/g, '-')
    .replace(/&/g, ' and ').replace(/[^a-z0-9^]+/g, ' ')
    .replace(legalSuffixes, ' ').trim().replace(/\s+/g, ' ');

  const flatten = (value, out = []) => {
    if (value == null) return out;
    if (typeof value === 'string' || typeof value === 'number') out.push(String(value));
    else if (Array.isArray(value)) value.forEach((item) => flatten(item, out));
    else if (typeof value === 'object') Object.values(value).forEach((item) => flatten(item, out));
    return out;
  };

  const editDistance = (a, b) => {
    if (a === b) return 0;
    if (!a.length) return b.length;
    if (!b.length) return a.length;
    const row = Array.from({ length: b.length + 1 }, (_, i) => i);
    for (let i = 1; i <= a.length; i += 1) {
      let prev = row[0];
      row[0] = i;
      for (let j = 1; j <= b.length; j += 1) {
        const old = row[j];
        row[j] = Math.min(row[j] + 1, row[j - 1] + 1, prev + (a[i - 1] === b[j - 1] ? 0 : 1));
        prev = old;
      }
    }
    return row[b.length];
  };

  const trigrams = (value) => {
    const text = `  ${normalise(value)}  `;
    const set = new Set();
    for (let i = 0; i < text.length - 2; i += 1) set.add(text.slice(i, i + 3));
    return set;
  };

  const dice = (a, b) => {
    const left = trigrams(a); const right = trigrams(b);
    if (!left.size || !right.size) return 0;
    let overlap = 0;
    left.forEach((gram) => { if (right.has(gram)) overlap += 1; });
    return (2 * overlap) / (left.size + right.size);
  };

  const synonymGroups = [
    ['uria', 'uria menendez', 'professional conflict', 'conflicto profesional', 'confidentiality', 'confidencialidad'],
    ['haya', 'servicer', 'servicing', 'gestor', 'plataforma de gestion'],
    ['ph122', 'promontoria 122', 'promontoria holding 122'],
    ['ricpe', 'ric private equity', 'canal etico', 'ethics channel', 'inadmission', 'inadmision', 'reassessment', 'revaloracion'],
    ['administrador concursal', 'insolvency administrator', 'borja rodriguez batllori'],
    ['caixabank', 'caixa bank', 'valencia 1859 2023', 'hearing 2027', 'vista 2027'],
    ['bankia', 'bfa', 'sareb', 'lender chain', 'cadena acreedora'],
    ['conflict check', 'conflict screening', 'control de conflictos', 'pantalla etica'],
    ['notice', 'knowledge', 'aviso', 'conocimiento', 'continued conduct', 'conducta continuada']
  ].map((group) => group.map(normalise));

  const expandQuery = (raw) => {
    const query = normalise(raw);
    const expanded = new Set([query]);
    synonymGroups.forEach((group) => {
      if (group.some((term) => query.includes(term) || term.includes(query))) group.forEach((term) => expanded.add(term));
    });
    return [...expanded].filter(Boolean);
  };

  const routeFor = (record) => {
    const routes = record.routes || {};
    const chosen = routes[lang] || routes.es || routes.en;
    if (chosen) return new URL(String(chosen).replace(/^\//, ''), siteRoot).href;
    return new URL(lang === 'es' ? 'es/registro-identidad-materia/' : 'en/matter-identity-registry/', siteRoot).href + `#${encodeURIComponent(record.id || '')}`;
  };

  const scoreRecord = (record, rawQuery) => {
    const variants = expandQuery(rawQuery);
    const name = normalise(record.name || record.label || record.title || '');
    const aliases = (record.aliases || []).map(normalise);
    const allText = normalise(flatten(record).join(' | '));
    const words = new Set(allText.split(' ').filter(Boolean));
    let best = 0; let reason = '';

    variants.forEach((query) => {
      if (!query) return;
      if (name === query || aliases.includes(query) || normalise(record.id) === query || normalise(record.canonical_id) === query) {
        if (1000 > best) { best = 1000; reason = 'exact'; }
        return;
      }
      if (name.startsWith(query) || aliases.some((alias) => alias.startsWith(query))) {
        if (900 > best) { best = 900; reason = 'name prefix'; }
      }
      const terms = query.split(' ').filter(Boolean);
      if (terms.length && terms.every((term) => allText.includes(term))) {
        const candidate = 720 + Math.min(120, terms.length * 20);
        if (candidate > best) { best = candidate; reason = 'all terms'; }
      }
      if (query.length >= 4) {
        const queryWords = query.split(' ').filter((word) => word.length >= 3);
        const fuzzyAll = queryWords.length && queryWords.every((word) => {
          const limit = word.length >= 8 ? 2 : 1;
          return [...words].some((candidate) => candidate.length >= 3 && editDistance(word, candidate) <= limit);
        });
        if (fuzzyAll && 610 > best) { best = 610; reason = 'spelling tolerant'; }
        const similarity = Math.max(dice(query, name), ...aliases.map((alias) => dice(query, alias)), 0);
        if (similarity >= 0.48) {
          const candidate = Math.round(430 + similarity * 150);
          if (candidate > best) { best = candidate; reason = 'pattern similarity'; }
        }
      }
    });
    return { score: best, reason };
  };

  const typeLabel = (type) => {
    const labels = lang === 'es'
      ? { PERSON: 'Persona', ORGANISATION: 'Entidad', EVENT: 'Evento', EVIDENCE: 'Evidencia', REVIEW: 'Candidato · revisar', PROCEEDING: 'Procedimiento', MASTER_PROCEEDING: 'Registro Maestro' }
      : { PERSON: 'Person', ORGANISATION: 'Entity', EVENT: 'Event', EVIDENCE: 'Evidence', REVIEW: 'Candidate · review', PROCEEDING: 'Proceeding', MASTER_PROCEEDING: 'Master Register' };
    return labels[type] || type || (lang === 'es' ? 'Registro' : 'Record');
  };

  const waitForSearch = () => new Promise((resolve, reject) => {
    let attempts = 0;
    const poll = () => {
      const input = document.getElementById('canonical-home-search-input');
      const section = document.querySelector('[data-canonical-home-search]');
      if (input && section && window.PorDerechoCanonicalSearch) return resolve({ input, section });
      attempts += 1;
      if (attempts > 160) return reject(new Error('canonical search did not initialise'));
      window.setTimeout(poll, 50);
    };
    poll();
  });

  const init = async () => {
    const { input, section } = await waitForSearch();
    if (section.dataset.knowledgeSearch === '20260904') return;
    section.dataset.knowledgeSearch = '20260904';

    const status = section.querySelector('.canonical-search-status');
    const results = section.querySelector('.canonical-search-results');
    const form = section.querySelector('form');
    const [registryIndex, graph, reviewQueue] = await Promise.all([
      fetch(dataUrl('assets/data/matter-identity-registry-v1.json'), { cache: 'no-store' }).then((r) => r.json()),
      fetch(dataUrl('data/legaltech/uria-bankia-caixabank-unitary-graph-20260904.json'), { cache: 'no-store' }).then((r) => r.json()),
      fetch(dataUrl('data/canonical-discovery/review-candidates-20260904.json'), { cache: 'no-store' }).then((r) => r.json())
    ]);
    const shards = await Promise.all((registryIndex.parts || []).map((part) =>
      fetch(dataUrl(`assets/data/${part.path}`), { cache: 'no-store' }).then((r) => r.json())
    ));

    const canonical = [];
    shards.forEach((shard) => (shard.records || []).forEach((record) => canonical.push({
      key: `canonical:${record.id}`,
      id: record.id,
      type: record.type,
      name: record.name,
      meta: record.domain || record.identity_resolution || record.procedural_state || '',
      route: routeFor(record),
      raw: record
    })));
    const graphRecords = [
      ...(graph.events || []).map((event) => ({ key: `event:${event.id}`, id: event.id, type: 'EVENT', name: `${event.date} · ${event.label}`, meta: event.status, route: new URL(lang === 'es' ? 'es/uria-menendez-sun-park/#cronologia-integral' : 'en/uria-menendez-sun-park/#complete-chronology', siteRoot).href, raw: event })),
      ...(graph.public_evidence || []).map((evidence) => ({ key: `evidence:${evidence.id}`, id: evidence.id, type: 'EVIDENCE', name: evidence.title, meta: lang === 'es' ? 'Fuente visual / texto' : 'Visual / text source', route: new URL(evidence.route.replace(/^\//, ''), siteRoot).href, raw: evidence }))
    ];
    const candidates = (reviewQueue.candidates || []).map((candidate) => ({
      key: `review:${candidate.candidate_id}`,
      id: candidate.candidate_id,
      type: 'REVIEW',
      name: candidate.name,
      meta: candidate.why_not_canonical_yet,
      route: new URL(lang === 'es' ? `es/revision-canonica/#${candidate.candidate_id}` : `en/canonical-review/#${candidate.candidate_id}`, siteRoot).href,
      raw: candidate
    }));

    const renderEnhanced = (rawQuery) => {
      const query = String(rawQuery || '').trim();
      if (query.length < 2) return;
      const rows = [...canonical, ...graphRecords, ...candidates]
        .map((entry) => ({ entry, ...scoreRecord(entry.raw, query) }))
        .filter((row) => row.score > 0)
        .sort((a, b) => b.score - a.score || a.entry.name.localeCompare(b.entry.name, lang));

      const existing = window.PorDerechoCanonicalSearch.search(query).slice(0, 20).map((entry) => ({
        entry: { key: entry.key || `legacy:${entry.id}`, id: entry.id, type: entry.type, name: entry.name, meta: entry.meta, route: entry.route },
        score: 650,
        reason: 'canonical register'
      }));
      const merged = new Map();
      [...rows, ...existing].forEach((row) => {
        const key = row.entry.id || row.entry.key;
        const prior = merged.get(key);
        if (!prior || row.score > prior.score) merged.set(key, row);
      });
      const matches = [...merged.values()]
        .sort((a, b) => b.score - a.score || a.entry.name.localeCompare(b.entry.name, lang))
        .slice(0, 18);
      if (!matches.length) return;

      results.innerHTML = matches.map(({ entry, reason }) => `
        <a class="canonical-search-result" href="${escapeHtml(entry.route)}" data-search-result-id="${escapeHtml(entry.id)}" data-search-match="${escapeHtml(reason)}">
          <span class="canonical-search-result-top">
            <span class="canonical-search-badge">${escapeHtml(typeLabel(entry.type))}</span>
            <span class="canonical-search-id">${escapeHtml(entry.id)}</span>
          </span>
          <strong>${escapeHtml(entry.name)}</strong>
          ${entry.meta ? `<small>${escapeHtml(entry.meta)}</small>` : ''}
          <small class="canonical-search-match-reason">${escapeHtml(lang === 'es' ? `Coincidencia: ${reason}` : `Matched: ${reason}`)}</small>
        </a>`).join('');
      results.hidden = false;
      const candidateCount = matches.filter(({ entry }) => entry.type === 'REVIEW').length;
      status.textContent = lang === 'es'
        ? `${matches.length} resultados · búsqueda por alias, relaciones, eventos y tolerancia ortográfica${candidateCount ? ` · ${candidateCount} candidato(s) pendiente(s)` : ''}`
        : `${matches.length} results · aliases, relationships, events and spelling tolerance${candidateCount ? ` · ${candidateCount} pending candidate(s)` : ''}`;
    };

    const run = () => window.setTimeout(() => renderEnhanced(input.value), 0);
    input.addEventListener('input', run);
    form?.addEventListener('submit', run);

    const note = document.createElement('p');
    note.className = 'canonical-search-status';
    note.setAttribute('data-knowledge-search-note', '20260904');
    note.innerHTML = lang === 'es'
      ? `Índice LegalTech activo: nombres sin tildes, variantes, errores leves, eventos, relaciones y evidencia. Los <a href="${new URL('es/revision-canonica/', siteRoot).href}">candidatos “sí / ahora no”</a> se muestran separados de identidades canónicas.`
      : `LegalTech index active: accent-free names, variants, minor misspellings, events, relationships and evidence. <a href="${new URL('en/canonical-review/', siteRoot).href}">“yes / not now” candidates</a> remain separate from canonical identities.`;
    status.insertAdjacentElement('afterend', note);

    const style = document.createElement('style');
    style.textContent = `.canonical-search-match-reason{font-size:.75rem!important;color:#6b4c1c!important}.canonical-search-result[data-search-result-id^="PD-MAYBE-"]{border-style:dashed;background:#fff9ea}`;
    document.head.appendChild(style);
  };

  init().catch((error) => console.error('LegalTech canonical search enhancement failed', error));
})();
