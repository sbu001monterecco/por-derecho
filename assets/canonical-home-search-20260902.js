(() => {
  'use strict';

  const current = document.currentScript;
  if (!current) return;

  const pathname = window.location.pathname.replace(/\/index\.html$/, '/');
  const isHome = /\/(?:por-derecho\/)?(?:es\/|en\/)?$/.test(pathname);
  if (!isHome) return;
  if (document.querySelector('[data-canonical-home-search="20260902"]')) return;

  const lang = (document.documentElement.lang || 'es').toLowerCase().startsWith('en') ? 'en' : 'es';
  const copy = lang === 'es'
    ? {
        eyebrow: 'BUSCADOR CANÓNICO ^ · PERSONAS · ENTIDADES · ÓRGANOS · PROCEDIMIENTOS',
        title: 'Buscar por nombre, referencia procesal o número ^',
        intro: 'Consulta el registro CAEPR y el Registro Maestro de Procedimientos. Admite nombres, referencias, NIG, Master ID, PD-SP-* y formas abreviadas como ^P-0147 o ^I-0044.',
        label: 'Buscar en el registro canónico',
        placeholder: 'Ej.: Graciela Pérez-Valencia · DP 748/2026 · ^P-0147 · Audiencia Provincial · ^I-0044',
        button: 'Buscar',
        loading: 'Cargando el registro canónico…',
        ready: 'Registro listo. Escribe al menos dos caracteres.',
        none: 'Sin coincidencias. Prueba el nombre completo, la referencia, el NIG, el Master ID o el identificador PD-SP-*.',
        result: 'resultado',
        results: 'resultados',
        open: 'Abrir registro',
        types: {
          PERSON: 'Persona', ORGANISATION: 'Entidad', STRUCTURE: 'Estructura',
          INSTITUTION: 'Órgano / institución', PROCEEDING: 'Procedimiento', MASTER_PROCEEDING: 'Registro Maestro'
        }
      }
    : {
        eyebrow: 'CANONICAL ^ SEARCH · PEOPLE · ENTITIES · COURTS · PROCEEDINGS',
        title: 'Search by name, proceeding reference or ^ number',
        intro: 'Searches CAEPR and the Master Proceedings Register. It accepts names, references, NIGs, Master IDs, PD-SP-* IDs and short forms such as ^P-0147 or ^I-0044.',
        label: 'Search the canonical register',
        placeholder: 'E.g. Graciela Pérez-Valencia · DP 748/2026 · ^P-0147 · Provincial Court · ^I-0044',
        button: 'Search',
        loading: 'Loading the canonical register…',
        ready: 'Register ready. Enter at least two characters.',
        none: 'No matches. Try the full name, reference, NIG, Master ID or PD-SP-* identifier.',
        result: 'result',
        results: 'results',
        open: 'Open record',
        types: {
          PERSON: 'Person', ORGANISATION: 'Entity', STRUCTURE: 'Structure',
          INSTITUTION: 'Court / institution', PROCEEDING: 'Proceeding', MASTER_PROCEEDING: 'Master Register'
        }
      };

  const assetBase = new URL('.', current.src);
  const dataUrl = (name) => new URL(`data/${name}`, assetBase).href;
  const siteRoot = new URL('../', assetBase);

  const normalise = (value) => String(value || '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[–—]/g, '-')
    .replace(/[^a-z0-9^]+/g, ' ')
    .trim()
    .replace(/\s+/g, ' ');

  const escapeHtml = (value) => String(value || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');

  const idVariants = (id) => {
    const value = String(id || '').toUpperCase();
    const match = /^PD-SP-([POSIR])-(\d{4})$/.exec(value);
    if (!match) return value ? [value] : [];
    const [, kind, number] = match;
    const compactNumber = String(Number(number));
    return [
      value,
      `${kind}-${number}`,
      `${kind}${number}`,
      `^${kind}-${number}`,
      `^${kind}${number}`,
      `^${number}`,
      `^${compactNumber}`
    ];
  };

  const routeFor = (record) => {
    const routes = record && record.routes;
    if (routes && routes[lang]) return new URL(String(routes[lang]).replace(/^\//, ''), siteRoot).href;
    const fallback = lang === 'es' ? 'es/registro-identidad-materia/' : 'en/matter-identity-registry/';
    return new URL(`${fallback}#${encodeURIComponent(record.id || '')}`, siteRoot).href;
  };

  let proceedingRoutes = {};

  const masterRoute = () => new URL(
    lang === 'es' ? 'es/registro-maestro-procedimientos/' : 'en/master-proceedings-register/',
    siteRoot
  ).href;

  const makeEntry = (record) => {
    const aliases = [
      ...(Array.isArray(record.aliases) ? record.aliases : []),
      ...(Array.isArray(record.legacy_ambiguous_aliases) ? record.legacy_ambiguous_aliases : []),
      ...(Array.isArray(record.master_register_ids) ? record.master_register_ids : []),
      record.master_register_id,
      record.nig,
      record.procedural_state,
      record.identity_resolution,
      ...idVariants(record.id)
    ].filter(Boolean);
    const name = record.name || record.id;
    const haystack = normalise([record.id, name, ...aliases].join(' | '));
    return {
      key: `caepr:${record.id}`,
      id: record.id,
      type: record.type || 'STRUCTURE',
      name,
      aliases,
      meta: record.identity_resolution || record.procedural_state || '',
      route: routeFor(record),
      haystack,
      exact: new Set([record.id, name, ...aliases].map(normalise).filter(Boolean))
    };
  };

  const makeMasterEntry = (record) => {
    const aliases = [
      record.Legacy_ID, record.Secondary_Reference, record.NIG, record.Origin_Organ,
      record.Current_Custodian, record.Stream, record.Geography, record.Parent_Master_ID,
      record.Linked_Proceedings, record.Appeal_or_Review
    ].filter(Boolean);
    const name = record.Reference || record.Object_or_Purpose || record.Master_ID;
    return {
      key: `master:${record.Master_ID}`,
      id: record.Master_ID,
      type: 'MASTER_PROCEEDING',
      name,
      aliases,
      meta: [record.Origin_Organ, record.Status].filter(Boolean).join(' · '),
      route: proceedingRoutes[record.Master_ID]?.[lang] ? new URL(proceedingRoutes[record.Master_ID][lang], siteRoot).href : `${masterRoute()}?q=${encodeURIComponent(record.Reference || record.Master_ID)}`,
      haystack: normalise([record.Master_ID, name, ...aliases, record.Object_or_Purpose, record.Connection].join(' | ')),
      exact: new Set([record.Master_ID, name, ...aliases].map(normalise).filter(Boolean))
    };
  };

  const scoreEntry = (entry, rawQuery) => {
    const query = normalise(rawQuery);
    if (!query) return 0;
    if (entry.exact.has(query)) return 1000;
    if (normalise(entry.id) === query) return 990;
    if (entry.haystack.startsWith(query)) return 850;
    const terms = query.split(' ').filter(Boolean);
    if (!terms.every((term) => entry.haystack.includes(term))) return 0;
    let score = 500;
    if (normalise(entry.name).includes(query)) score += 220;
    if (normalise(entry.id).includes(query)) score += 180;
    score += Math.max(0, 80 - entry.name.length);
    return score;
  };

  const section = document.createElement('section');
  section.className = 'canonical-home-search section';
  section.setAttribute('data-canonical-home-search', '20260902');
  section.innerHTML = `
    <div class="shell canonical-search-shell">
      <p class="eyebrow">${escapeHtml(copy.eyebrow)}</p>
      <div class="canonical-search-heading">
        <div>
          <h2>${escapeHtml(copy.title)}</h2>
          <p>${escapeHtml(copy.intro)}</p>
        </div>
        <a class="canonical-search-register-link" href="${escapeHtml(masterRoute())}">${escapeHtml(lang === 'es' ? 'Registro Maestro' : 'Master Register')}</a>
      </div>
      <form class="canonical-search-form" role="search">
        <label for="canonical-home-search-input">${escapeHtml(copy.label)}</label>
        <div class="canonical-search-controls">
          <input id="canonical-home-search-input" name="q" type="search" autocomplete="off" spellcheck="false" placeholder="${escapeHtml(copy.placeholder)}" aria-describedby="canonical-home-search-status">
          <button type="submit">${escapeHtml(copy.button)}</button>
        </div>
      </form>
      <p id="canonical-home-search-status" class="canonical-search-status" aria-live="polite">${escapeHtml(copy.loading)}</p>
      <div class="canonical-search-results" hidden></div>
    </div>`;

  const style = document.createElement('style');
  style.setAttribute('data-canonical-home-search-style', '20260902');
  style.textContent = `
    .canonical-home-search{background:#eef4f2;border-top:1px solid #d4e1dd;border-bottom:1px solid #d4e1dd}
    .canonical-search-shell{max-width:1180px}
    .canonical-search-heading{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:1.5rem;align-items:end}
    .canonical-search-heading h2{max-width:18ch;margin:.25rem 0 .65rem;font-size:clamp(2rem,4vw,3.5rem);line-height:1.02}
    .canonical-search-heading p{max-width:78ch;margin:0}
    .canonical-search-register-link{display:inline-flex;align-items:center;justify-content:center;border:1px solid #173f36;border-radius:999px;padding:.65rem 1rem;font-weight:750;text-decoration:none;white-space:nowrap}
    .canonical-search-form{margin-top:1.3rem}
    .canonical-search-form label{display:block;font-weight:800;margin-bottom:.45rem}
    .canonical-search-controls{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:.65rem}
    .canonical-search-controls input{width:100%;min-height:3.25rem;border:2px solid #476b62;border-radius:12px;padding:.8rem 1rem;font:inherit;background:#fff;color:#13252d}
    .canonical-search-controls input:focus{outline:3px solid rgba(36,92,73,.22);outline-offset:2px}
    .canonical-search-controls button{border:0;border-radius:12px;padding:.75rem 1.25rem;background:#173f36;color:#fff;font:inherit;font-weight:800;cursor:pointer}
    .canonical-search-status{margin:.7rem 0 0;color:#3d514c;font-size:.95rem}
    .canonical-search-results{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.75rem;margin-top:1rem}
    .canonical-search-result{display:block;background:#fff;border:1px solid #cad8d4;border-radius:14px;padding:1rem;text-decoration:none;color:inherit;box-shadow:0 5px 18px rgba(22,44,38,.06)}
    .canonical-search-result:hover,.canonical-search-result:focus{border-color:#245c49;transform:translateY(-1px)}
    .canonical-search-result-top{display:flex;align-items:center;justify-content:space-between;gap:.75rem;margin-bottom:.45rem}
    .canonical-search-badge{font-size:.75rem;font-weight:850;letter-spacing:.04em;text-transform:uppercase;color:#245c49}
    .canonical-search-id{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.82rem;font-weight:800;color:#6a4b13}
    .canonical-search-result strong{display:block;font-size:1.08rem;line-height:1.25}
    .canonical-search-result small{display:block;margin-top:.45rem;color:#536660;line-height:1.35}
    @media(max-width:760px){.canonical-search-heading{grid-template-columns:1fr}.canonical-search-register-link{justify-self:start}.canonical-search-results{grid-template-columns:1fr}}
    @media(max-width:520px){.canonical-search-controls{grid-template-columns:1fr}.canonical-search-controls button{width:100%}}
  `;
  document.head.appendChild(style);

  const main = document.querySelector('main');
const siteHeader = document.querySelector('.site-header');
if (!main || !siteHeader) return;

// Mount as a top-level body section immediately after the site header.
// The homepage contains nested evidence <details> blocks and generic
// insertion points must never place this primary navigation control inside one.
const mountTopLevel = () => {
  if (section.parentElement !== document.body || section.previousElementSibling !== siteHeader || section.closest('details')) {
    siteHeader.insertAdjacentElement('afterend', section);
  }
};
mountTopLevel();
requestAnimationFrame(mountTopLevel);
window.setTimeout(mountTopLevel, 250);

  const form = section.querySelector('form');
  const input = section.querySelector('input');
  const status = section.querySelector('.canonical-search-status');
  const results = section.querySelector('.canonical-search-results');
  let entries = [];

  const render = (rawQuery) => {
    const query = String(rawQuery || '').trim();
    if (query.length < 2) {
      results.hidden = true;
      results.innerHTML = '';
      status.textContent = copy.ready;
      return [];
    }
    const matches = entries
      .map((entry) => ({ entry, score: scoreEntry(entry, query) }))
      .filter((row) => row.score > 0)
      .sort((a, b) => b.score - a.score || a.entry.name.localeCompare(b.entry.name, lang))
      .slice(0, 12)
      .map((row) => row.entry);

    if (!matches.length) {
      results.hidden = true;
      results.innerHTML = '';
      status.textContent = copy.none;
      return [];
    }

    status.textContent = `${matches.length} ${matches.length === 1 ? copy.result : copy.results}`;
    results.innerHTML = matches.map((entry) => `
      <a class="canonical-search-result" href="${escapeHtml(entry.route)}" data-search-result-id="${escapeHtml(entry.id)}">
        <span class="canonical-search-result-top">
          <span class="canonical-search-badge">${escapeHtml(copy.types[entry.type] || entry.type)}</span>
          <span class="canonical-search-id">${escapeHtml(entry.id)}</span>
        </span>
        <strong>${escapeHtml(entry.name)}</strong>
        ${entry.meta ? `<small>${escapeHtml(entry.meta)}</small>` : ''}
      </a>`).join('');
    results.hidden = false;
    return matches;
  };

  const load = async () => {
    const [registryIndex, master, proceedingRouteMap] = await Promise.all([
      fetch(dataUrl('matter-identity-registry-v1.json'), { cache: 'no-store' }).then((response) => {
        if (!response.ok) throw new Error(`registry ${response.status}`);
        return response.json();
      }),
      fetch(dataUrl('proceedings-master-public-v1.json'), { cache: 'no-store' }).then((response) => {
        if (!response.ok) throw new Error(`proceedings ${response.status}`);
        return response.json();
      }),
      fetch(dataUrl('proceeding-page-routes-20260902.json'), { cache: 'no-store' }).then((response) => {
        if (!response.ok) throw new Error(`proceeding routes ${response.status}`);
        return response.json();
      })
    ]);
    proceedingRoutes = proceedingRouteMap.routes || {};

    const shards = await Promise.all((registryIndex.parts || []).map((part) =>
      fetch(dataUrl(part.path), { cache: 'no-store' }).then((response) => {
        if (!response.ok) throw new Error(`${part.path} ${response.status}`);
        return response.json();
      })
    ));

    const byId = new Map();
    shards.forEach((shard) => (shard.records || []).forEach((record) => {
      if (record && record.id && !byId.has(record.id)) byId.set(record.id, makeEntry(record));
    }));
    const masterEntries = (master.records || []).map(makeMasterEntry);
    entries = [...byId.values(), ...masterEntries];

    window.PorDerechoCanonicalSearch = Object.freeze({
      version: '20260902',
      normalise,
      search: (query) => entries
        .map((entry) => ({ entry, score: scoreEntry(entry, query) }))
        .filter((row) => row.score > 0)
        .sort((a, b) => b.score - a.score)
        .map((row) => row.entry),
      count: entries.length
    });

    const params = new URLSearchParams(window.location.search);
    const initial = params.get('q') || params.get('search') || '';
    if (initial) {
      input.value = initial;
      render(initial);
      section.scrollIntoView({ block: 'start' });
    } else {
      status.textContent = `${copy.ready} (${entries.length})`;
    }
  };

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    render(input.value);
  });
  input.addEventListener('input', () => render(input.value));

  load().catch((error) => {
    console.error('Canonical home search failed', error);
    status.textContent = lang === 'es'
      ? 'El buscador no pudo cargar el registro. Abre el Registro Maestro desde el enlace superior.'
      : 'The search could not load the register. Open the Master Register using the link above.';
  });
})();
