(() => {
  'use strict';

  const current = document.currentScript;
  if (!current) return;

  const pathname = window.location.pathname.replace(/\/index\.html$/, '/');
  const isHome = /\/(?:por-derecho\/)?(?:es\/|en\/)?$/.test(pathname);
  if (!isHome) return;
  if (document.querySelector('[data-canonical-home-search]')) return;

  const lang = (document.documentElement.lang || 'es').toLowerCase().startsWith('en') ? 'en' : 'es';
  const copy = lang === 'es' ? {
    eyebrow: 'BUSCADOR CANÓNICO ^ · IDENTIDADES · ENTIDADES · ÓRGANOS · PROCEDIMIENTOS',
    title: 'Buscar por nombre, alias, NIF, referencia o número ^',
    intro: 'Búsqueda tolerante a tildes y errores menores, con control de colisiones. Los vínculos son asunto-por-asunto: una coincidencia de nombre o documento no transfiere mandato, conocimiento, control ni responsabilidad.',
    label: 'Buscar en el registro canónico',
    placeholder: 'Ej.: Uria Menendez · Juan Francisco Falcon · DP 748/2026 · ^P-0147 · ^I-0044',
    button: 'Buscar', loading: 'Cargando el registro canónico…',
    ready: 'Registro listo. Escribe al menos dos caracteres.',
    none: 'Sin coincidencias seguras. Prueba el nombre completo, un alias, NIF/NIG, referencia o identificador PD-SP-*.',
    result: 'resultado', results: 'resultados',
    types: {PERSON:'Persona',ORGANISATION:'Entidad',STRUCTURE:'Estructura',INSTITUTION:'Órgano / institución',PROCEEDING:'Procedimiento',MASTER_PROCEEDING:'Registro Maestro'}
  } : {
    eyebrow: 'CANONICAL ^ SEARCH · IDENTITIES · ENTITIES · COURTS · PROCEEDINGS',
    title: 'Search by name, alias, identifier, reference or ^ number',
    intro: 'Accent-insensitive search with bounded typo tolerance and collision controls. Links remain matter-specific: a shared name or document does not transfer mandate, knowledge, control or liability.',
    label: 'Search the canonical register',
    placeholder: 'E.g. Uria Menendez · Juan Francisco Falcon · DP 748/2026 · ^P-0147 · ^I-0044',
    button: 'Search', loading: 'Loading the canonical register…',
    ready: 'Register ready. Enter at least two characters.',
    none: 'No safe match. Try the full name, an alias, NIF/NIG, proceeding reference or PD-SP-* ID.',
    result: 'result', results: 'results',
    types: {PERSON:'Person',ORGANISATION:'Entity',STRUCTURE:'Structure',INSTITUTION:'Court / institution',PROCEEDING:'Proceeding',MASTER_PROCEEDING:'Master Register'}
  };

  const assetBase = new URL('.', current.src);
  const dataUrl = (name) => new URL(`data/${name}`, assetBase).href;
  const siteRoot = new URL('../', assetBase);
  const queue = window.PorDerechoCanonicalSearchQueue = window.PorDerechoCanonicalSearchQueue || [];

  const normalise = (value) => String(value || '')
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[–—]/g, '-')
    .replace(/&/g, ' and ')
    .replace(/[^a-z0-9^]+/g, ' ')
    .trim()
    .replace(/\s+/g, ' ');

  const collapse = (value) => normalise(value).replace(/[^a-z0-9^]/g, '');
  const STOP = new Set(['de','del','la','las','los','el','y','e','the','of','and','sl','slu','sa','slp']);
  const tokens = (value) => normalise(value).split(' ').filter((term) => term && !STOP.has(term));

  const escapeHtml = (value) => String(value || '')
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#039;');

  const idVariants = (id) => {
    const value = String(id || '').toUpperCase();
    const match = /^PD-SP-([POSIR])-(\d{4})$/.exec(value);
    if (!match) return value ? [value] : [];
    const [, kind, number] = match;
    const compact = String(Number(number));
    return [value, `${kind}-${number}`, `${kind}${number}`, `^${kind}-${number}`, `^${kind}${number}`, `^${number}`, `^${compact}`];
  };

  // Positive-field allowlist. Evidential boundaries, collision warnings,
  // allegations, forbidden aliases and “do not infer” text are deliberately
  // excluded so a negative warning cannot itself create a false search hit.
  const positiveValues = (record) => {
    const output = [];
    const add = (value) => {
      if (value == null) return;
      if (Array.isArray(value)) { value.forEach(add); return; }
      if (typeof value === 'string' || typeof value === 'number') output.push(String(value));
    };
    add(record.search_meta);
    add(record.master_register_id);
    add(record.master_register_ids);
    add(record.nig);
    add(record.procedural_state);
    add(record.identity_resolution);
    add(record.registered_denominational_form);
    add(record.former_name);
    add(record.former_names);
    add(record.source_literal_variants);
    add(record.retrieval_aliases_not_legal_names);
    add(record.search_aliases_not_legal_names);
    add(record.identifier && record.identifier.type);
    add(record.identifier && record.identifier.value);
    (record.matter_roles || []).forEach((role) => {
      if (!role || typeof role !== 'object') return;
      add(role.matter); add(role.role); add(role.date); add(role.period);
      add(role.evidence_id); add(role.evidence_ids); add(role.reference);
    });
    return output;
  };

  const oneEditApart = (a, b) => {
    if (a === b) return true;
    if (Math.abs(a.length - b.length) > 1) return false;
    let i = 0, j = 0, edits = 0;
    while (i < a.length && j < b.length) {
      if (a[i] === b[j]) { i += 1; j += 1; continue; }
      edits += 1;
      if (edits > 1) return false;
      if (a.length > b.length) i += 1;
      else if (b.length > a.length) j += 1;
      else if (i + 1 < a.length && j + 1 < b.length && a[i] === b[j + 1] && a[i + 1] === b[j]) { i += 2; j += 2; }
      else { i += 1; j += 1; }
    }
    if (i < a.length || j < b.length) edits += 1;
    return edits <= 1;
  };

  const routeFor = (record) => {
    const routes = record && record.routes;
    if (routes && routes[lang]) return new URL(String(routes[lang]).replace(/^\//, ''), siteRoot).href;
    const fallback = lang === 'es' ? 'es/registro-identidad-materia/' : 'en/matter-identity-registry/';
    return new URL(`${fallback}#${encodeURIComponent(record.id || '')}`, siteRoot).href;
  };

  let proceedingRoutes = {};
  const masterRoute = () => new URL(lang === 'es' ? 'es/registro-maestro-procedimientos/' : 'en/master-proceedings-register/', siteRoot).href;

  const makeEntry = (record) => {
    const aliases = [
      ...(Array.isArray(record.aliases) ? record.aliases : []),
      ...(Array.isArray(record.search_aliases) ? record.search_aliases : []),
      ...(Array.isArray(record.legacy_ambiguous_aliases) ? record.legacy_ambiguous_aliases : []),
      ...(Array.isArray(record.master_register_ids) ? record.master_register_ids : []),
      record.master_register_id, record.nig, record.identifier && record.identifier.value,
      ...idVariants(record.id)
    ].filter(Boolean);
    const exclusions = new Set((record.search_exclusions || []).map(normalise).filter(Boolean));
    const name = record.name || record.id;
    const values = [record.id, name, ...aliases, ...positiveValues(record)];
    const norms = [...new Set(values.map(normalise).filter(Boolean))];
    const exact = new Set([record.id, name, ...aliases].map(normalise).filter(Boolean));
    return {
      key: `caepr:${record.id}`, id: record.id, type: record.type || 'STRUCTURE', name,
      aliases, meta: record.search_meta || record.identity_resolution || record.procedural_state || '',
      route: routeFor(record), norms, exact, exclusions,
      collapsed: new Set(norms.map(collapse).filter(Boolean)),
      tokenSet: new Set(norms.flatMap(tokens)), sourceTier: record.source_tier || record.source_status || ''
    };
  };

  const makeMasterEntry = (record) => {
    const aliases = [record.Legacy_ID,record.Secondary_Reference,record.NIG,record.Origin_Organ,record.Current_Custodian,record.Stream,record.Geography,record.Parent_Master_ID,record.Linked_Proceedings,record.Appeal_or_Review].filter(Boolean);
    const name = record.Reference || record.Object_or_Purpose || record.Master_ID;
    const values = [record.Master_ID, name, ...aliases, record.Object_or_Purpose, record.Connection].filter(Boolean);
    const norms = values.map(normalise).filter(Boolean);
    return {
      key:`master:${record.Master_ID}`, id:record.Master_ID, type:'MASTER_PROCEEDING', name, aliases,
      meta:[record.Origin_Organ,record.Status].filter(Boolean).join(' · '),
      route: proceedingRoutes[record.Master_ID]?.[lang] ? new URL(proceedingRoutes[record.Master_ID][lang], siteRoot).href : `${masterRoute()}?q=${encodeURIComponent(record.Reference || record.Master_ID)}`,
      norms, exact:new Set([record.Master_ID,name,...aliases].map(normalise).filter(Boolean)), exclusions:new Set(),
      collapsed:new Set(norms.map(collapse).filter(Boolean)), tokenSet:new Set(norms.flatMap(tokens)), sourceTier:'MASTER'
    };
  };

  const scoreEntry = (entry, rawQuery) => {
    const query = normalise(rawQuery);
    if (!query || entry.exclusions.has(query)) return 0;
    const queryCollapsed = collapse(query);
    const queryTokens = tokens(query);
    if (entry.exact.has(query)) return 1400;
    if (normalise(entry.id) === query) return 1380;
    if (queryCollapsed && entry.collapsed.has(queryCollapsed)) return 1320;

    const nameNorm = normalise(entry.name);
    if (nameNorm.startsWith(query)) return 1160 + Math.max(0, 100 - entry.name.length);
    if (entry.aliases.some((alias) => normalise(alias).startsWith(query))) return 1100;
    if (entry.norms.some((value) => value.includes(query))) return 980;

    if (!queryTokens.length) return 0;
    let exactTokenHits = 0, prefixHits = 0, fuzzyHits = 0;
    for (const term of queryTokens) {
      if (entry.tokenSet.has(term)) { exactTokenHits += 1; continue; }
      if (term.length >= 3 && [...entry.tokenSet].some((candidate) => candidate.startsWith(term))) { prefixHits += 1; continue; }
      if (term.length >= 5 && [...entry.tokenSet].some((candidate) => candidate.length >= 4 && oneEditApart(term, candidate))) { fuzzyHits += 1; continue; }
      return 0;
    }
    let score = 650 + exactTokenHits * 90 + prefixHits * 55 + fuzzyHits * 25;
    if (queryTokens.every((term) => tokens(entry.name).some((candidate) => candidate === term || candidate.startsWith(term)))) score += 180;
    if (entry.sourceTier) score += 15;
    return score + Math.max(0, 80 - entry.name.length);
  };

  const section = document.createElement('section');
  section.className = 'canonical-home-search section';
  section.setAttribute('data-canonical-home-search', '20260904');
  section.innerHTML = `<div class="shell canonical-search-shell"><p class="eyebrow">${escapeHtml(copy.eyebrow)}</p><div class="canonical-search-heading"><div><h2>${escapeHtml(copy.title)}</h2><p>${escapeHtml(copy.intro)}</p></div><a class="canonical-search-register-link" href="${escapeHtml(masterRoute())}">${lang === 'es' ? 'Registro Maestro' : 'Master Register'}</a></div><form class="canonical-search-form" role="search"><label for="canonical-home-search-input">${escapeHtml(copy.label)}</label><div class="canonical-search-controls"><input id="canonical-home-search-input" name="q" type="search" autocomplete="off" spellcheck="false" placeholder="${escapeHtml(copy.placeholder)}" aria-describedby="canonical-home-search-status"><button type="submit">${escapeHtml(copy.button)}</button></div></form><p id="canonical-home-search-status" class="canonical-search-status" aria-live="polite">${escapeHtml(copy.loading)}</p><div class="canonical-search-results" hidden></div></div>`;

  const style = document.createElement('style');
  style.setAttribute('data-canonical-home-search-style', '20260904');
  style.textContent = `.canonical-home-search{background:#eef4f2;border-top:1px solid #d4e1dd;border-bottom:1px solid #d4e1dd}.canonical-search-shell{max-width:1180px}.canonical-search-heading{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:1.5rem;align-items:end}.canonical-search-heading h2{max-width:20ch;margin:.25rem 0 .65rem;font-size:clamp(2rem,4vw,3.5rem);line-height:1.02}.canonical-search-heading p{max-width:84ch;margin:0}.canonical-search-register-link{display:inline-flex;align-items:center;justify-content:center;border:1px solid #173f36;border-radius:999px;padding:.65rem 1rem;font-weight:750;text-decoration:none;white-space:nowrap}.canonical-search-form{margin-top:1.3rem}.canonical-search-form label{display:block;font-weight:800;margin-bottom:.45rem}.canonical-search-controls{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:.65rem}.canonical-search-controls input{width:100%;min-height:3.25rem;border:2px solid #476b62;border-radius:12px;padding:.8rem 1rem;font:inherit;background:#fff;color:#13252d}.canonical-search-controls input:focus{outline:3px solid rgba(36,92,73,.22);outline-offset:2px}.canonical-search-controls button{border:0;border-radius:12px;padding:.75rem 1.25rem;background:#173f36;color:#fff;font:inherit;font-weight:800;cursor:pointer}.canonical-search-status{margin:.7rem 0 0;color:#3d514c;font-size:.95rem}.canonical-search-results{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.75rem;margin-top:1rem}.canonical-search-result{display:block;background:#fff;border:1px solid #cad8d4;border-radius:14px;padding:1rem;text-decoration:none;color:inherit;box-shadow:0 5px 18px rgba(22,44,38,.06)}.canonical-search-result:hover,.canonical-search-result:focus{border-color:#245c49;transform:translateY(-1px)}.canonical-search-result-top{display:flex;align-items:center;justify-content:space-between;gap:.75rem;margin-bottom:.45rem}.canonical-search-badge{font-size:.75rem;font-weight:850;letter-spacing:.04em;text-transform:uppercase;color:#245c49}.canonical-search-id{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.82rem;font-weight:800;color:#6a4b13}.canonical-search-result strong{display:block;font-size:1.08rem;line-height:1.25}.canonical-search-result small{display:block;margin-top:.45rem;color:#536660;line-height:1.35}@media(max-width:760px){.canonical-search-heading{grid-template-columns:1fr}.canonical-search-register-link{justify-self:start}.canonical-search-results{grid-template-columns:1fr}}@media(max-width:520px){.canonical-search-controls{grid-template-columns:1fr}.canonical-search-controls button{width:100%}}`;
  document.head.appendChild(style);

  const siteHeader = document.querySelector('.site-header');
  if (!siteHeader) return;
  const mountTopLevel = () => {
    if (section.parentElement !== document.body || section.previousElementSibling !== siteHeader || section.closest('details')) siteHeader.insertAdjacentElement('afterend', section);
  };
  mountTopLevel(); requestAnimationFrame(mountTopLevel); window.setTimeout(mountTopLevel, 250);

  const form = section.querySelector('form');
  const input = section.querySelector('input');
  const status = section.querySelector('.canonical-search-status');
  const results = section.querySelector('.canonical-search-results');
  const entryMap = new Map();
  let masterEntries = [];
  let entries = [];

  const rebuild = () => { entries = [...entryMap.values(), ...masterEntries]; };
  const rank = (query) => entries.map((entry) => ({entry,score:scoreEntry(entry,query)})).filter((row) => row.score > 0).sort((a,b) => b.score-a.score || a.entry.name.localeCompare(b.entry.name,lang));

  const render = (rawQuery) => {
    const query = String(rawQuery || '').trim();
    if (query.length < 2) { results.hidden = true; results.innerHTML = ''; status.textContent = `${copy.ready} (${entries.length})`; return []; }
    const matches = rank(query).slice(0, 12).map((row) => row.entry);
    if (!matches.length) { results.hidden = true; results.innerHTML = ''; status.textContent = copy.none; return []; }
    status.textContent = `${matches.length} ${matches.length === 1 ? copy.result : copy.results}`;
    results.innerHTML = matches.map((entry) => `<a class="canonical-search-result" href="${escapeHtml(entry.route)}" data-search-result-id="${escapeHtml(entry.id)}"><span class="canonical-search-result-top"><span class="canonical-search-badge">${escapeHtml(copy.types[entry.type] || entry.type)}</span><span class="canonical-search-id">${escapeHtml(entry.id)}</span></span><strong>${escapeHtml(entry.name)}</strong>${entry.meta ? `<small>${escapeHtml(entry.meta)}</small>` : ''}</a>`).join('');
    results.hidden = false; return matches;
  };

  const register = (records) => {
    const list = Array.isArray(records) ? records : [records];
    list.filter((record) => record && record.id).forEach((record) => entryMap.set(`caepr:${record.id}`, makeEntry(record)));
    rebuild();
    if (input.value.trim().length >= 2) render(input.value);
    return list.length;
  };

  const load = async () => {
    const [registryIndex, master, routeMap] = await Promise.all([
      fetch(dataUrl('matter-identity-registry-v1.json'), {cache:'no-store'}).then((r) => {if(!r.ok) throw new Error(`registry ${r.status}`); return r.json();}),
      fetch(dataUrl('proceedings-master-public-v1.json'), {cache:'no-store'}).then((r) => {if(!r.ok) throw new Error(`proceedings ${r.status}`); return r.json();}),
      fetch(dataUrl('proceeding-page-routes-20260902.json'), {cache:'no-store'}).then((r) => {if(!r.ok) throw new Error(`routes ${r.status}`); return r.json();})
    ]);
    proceedingRoutes = routeMap.routes || {};
    const shards = await Promise.all((registryIndex.parts || []).map((part) => fetch(dataUrl(part.path), {cache:'no-store'}).then((r) => {if(!r.ok) throw new Error(`${part.path} ${r.status}`); return r.json();})));
    shards.forEach((shard) => register(shard.records || []));
    masterEntries = (master.records || []).map(makeMasterEntry); rebuild();

    const api = {version:'20260904',normalise,search:(query) => rank(query).map((row) => row.entry),register};
    Object.defineProperty(api, 'count', {enumerable:true,get:() => entries.length});
    window.PorDerechoCanonicalSearch = Object.freeze(api);
    while (queue.length) register(queue.shift());
    window.dispatchEvent(new CustomEvent('pd:canonical-search-ready', {detail:{version:'20260904',count:entries.length}}));

    const params = new URLSearchParams(window.location.search);
    const initial = params.get('q') || params.get('search') || '';
    if (initial) { input.value = initial; render(initial); section.scrollIntoView({block:'start'}); }
    else status.textContent = `${copy.ready} (${entries.length})`;
  };

  form.addEventListener('submit', (event) => { event.preventDefault(); render(input.value); });
  input.addEventListener('input', () => render(input.value));
  load().catch((error) => {
    console.error('Canonical home search failed', error);
    status.textContent = lang === 'es' ? 'El buscador no pudo cargar el registro. Abre el Registro Maestro.' : 'The search could not load the register. Open the Master Register.';
  });
})();
