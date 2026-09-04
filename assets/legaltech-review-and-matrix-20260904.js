(() => {
  'use strict';

  const current = document.currentScript;
  if (!current || !document.body) return;
  const siteRoot = new URL('../', current.src);
  const rootPath = siteRoot.pathname.replace(/\/+$/, '/');
  const pathname = window.location.pathname.replace(/\/index\.html$/, '/').replace(/\/+$/, '/');
  const relative = pathname.startsWith(rootPath) ? pathname.slice(rootPath.length) : pathname.replace(/^\/+/, '');
  const lang = relative.startsWith('en/') ? 'en' : 'es';
  const reviewRoutes = new Set(['en/canonical-review/', 'es/revision-canonica/']);
  const matrixRoutes = new Set(['en/notice-continued-conduct-matrix/', 'es/matriz-aviso-conducta-continuada/']);
  const selectionRoutes = new Set(['en/evidence-intake-selection/', 'es/seleccion-ingesta-evidencia/']);
  if (![...reviewRoutes, ...matrixRoutes, ...selectionRoutes].some((route) => route === relative)) return;

  const href = (path) => new URL(String(path || '').replace(/^\//, ''), siteRoot).href;
  const esc = (value) => String(value ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  const storageKey = 'por-derecho-canonical-review-decisions-v1';
  const main = document.querySelector('main');
  if (!main) return;

  const copy = lang === 'es' ? {
    loading: 'Cargando el registro LegalTech…', error: 'No se pudo cargar el registro.',
    yes: 'Sí — admitir ahora', notNow: 'Ahora no', verify: 'Necesita verificación', clear: 'Borrar decisión',
    saved: 'Decisión guardada en este navegador', localOnly: 'La decisión del navegador no modifica por sí sola GitHub. Exporta el paquete para revisión y commit autenticado.',
    export: 'Exportar decisiones JSON', copy: 'Copiar decisiones', copied: 'Decisiones copiadas.',
    source: 'Fuentes registradas', why: 'Por qué apareció', boundary: 'Por qué no es canónico todavía', next: 'Siguiente acción', routes: 'Rutas propuestas',
    matrixActor: 'Actor / capacidad', notice: 'Primer aviso documentado', information: 'Información disponible', conduct: 'Acto u omisión posterior', claimant: 'Posición atribuida a Gil Marer', outcome: 'Resultado / beneficio', innocent: 'Explicación inocente o lícita', missing: 'Prueba faltante', issues: 'Posibles cuestiones si se prueba', status: 'Estado',
    selectionClass: 'Clase de publicación', selectionStatus: 'Estado actual', reason: 'Razón', outputs: 'Salidas exigidas', interlinks: 'Interconexiones',
    full: 'Registro completo', partial: 'La enumeración recursiva de Google Drive no está soportada por el conector; esta es una selección priorizada y no una afirmación de lectura byte a byte de todo Drive.'
  } : {
    loading: 'Loading the LegalTech register…', error: 'The register could not be loaded.',
    yes: 'Yes — admit now', notNow: 'Not now', verify: 'Needs verification', clear: 'Clear decision',
    saved: 'Decision saved in this browser', localOnly: 'A browser decision does not itself modify GitHub. Export the package for authenticated review and commit.',
    export: 'Export decisions JSON', copy: 'Copy decisions', copied: 'Decisions copied.',
    source: 'Registered sources', why: 'Why it appeared', boundary: 'Why it is not canonical yet', next: 'Next action', routes: 'Suggested routes',
    matrixActor: 'Actor / capacity', notice: 'First documented notice', information: 'Information available', conduct: 'Later act or omission', claimant: 'Position attributed to Gil Marer', outcome: 'Outcome / benefit', innocent: 'Innocent or lawful explanation', missing: 'Missing evidence', issues: 'Possible issues if proved', status: 'Status',
    selectionClass: 'Publication class', selectionStatus: 'Current status', reason: 'Reason', outputs: 'Required outputs', interlinks: 'Interlinks',
    full: 'Complete register', partial: 'Recursive Google Drive enumeration is not supported by the connector; this is a prioritised selection, not a claim that every Drive byte was read.'
  };

  const addStyle = () => {
    const style = document.createElement('style');
    style.setAttribute('data-legaltech-review-style', '20260904');
    style.textContent = `
      .lt-app{max-width:1240px;margin:0 auto;padding:2rem 1rem 4rem}.lt-app-status{padding:1rem;border:1px solid #cad8d4;border-radius:12px;background:#f6faf8}.lt-toolbar{display:flex;flex-wrap:wrap;gap:.6rem;margin:1rem 0}.lt-toolbar button,.lt-toolbar a{border:0;border-radius:999px;padding:.65rem .9rem;font:inherit;font-weight:800;cursor:pointer;text-decoration:none;background:#173f36;color:#fff}.lt-toolbar button:nth-child(2){background:#6b3f72}.lt-toolbar a{background:#6a4b13}
      .lt-review-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));gap:1rem}.lt-review-card{border:1px solid rgba(19,37,45,.2);border-top:6px solid #a56c00;border-radius:16px;background:#fff;padding:1rem;box-shadow:0 9px 26px rgba(19,37,45,.07)}.lt-review-card[data-decision="ADMIT_NOW"]{border-top-color:#176b54}.lt-review-card[data-decision="NOT_NOW"]{border-top-color:#63737a}.lt-review-card[data-decision="NEEDS_VERIFICATION"]{border-top-color:#7b4d9e}.lt-review-card h2{font-size:1.25rem;margin:.25rem 0}.lt-review-id{font:800 .78rem ui-monospace,monospace;color:#6a4b13}.lt-review-meta{display:grid;gap:.6rem;margin:.8rem 0}.lt-review-meta div{background:#f5f7f6;border-radius:10px;padding:.7rem}.lt-review-meta strong{display:block;font-size:.75rem;text-transform:uppercase;letter-spacing:.04em;color:#47635b;margin-bottom:.25rem}.lt-review-actions{display:flex;flex-wrap:wrap;gap:.45rem}.lt-review-actions button{border:1px solid #173f36;background:#fff;color:#173f36;border-radius:999px;padding:.5rem .7rem;font:inherit;font-weight:800;cursor:pointer}.lt-review-actions button[data-action="ADMIT_NOW"]{background:#176b54;color:#fff;border-color:#176b54}.lt-review-actions button[data-action="NEEDS_VERIFICATION"]{background:#6b3f72;color:#fff;border-color:#6b3f72}.lt-review-decision{font-weight:850;margin:.65rem 0 0}
      .lt-matrix-wrap{overflow-x:auto;border:1px solid rgba(19,37,45,.18);border-radius:14px}.lt-matrix{border-collapse:collapse;min-width:2200px;background:#fff}.lt-matrix th,.lt-matrix td{vertical-align:top;text-align:left;padding:.75rem;border-bottom:1px solid rgba(19,37,45,.14);border-right:1px solid rgba(19,37,45,.1);line-height:1.45}.lt-matrix th{position:sticky;top:0;background:#173f36;color:#fff;z-index:1;min-width:170px}.lt-matrix td:first-child{position:sticky;left:0;background:#f8faf9;min-width:240px;font-weight:800;z-index:0}.lt-matrix ul{margin:.2rem 0;padding-left:1.1rem}.lt-matrix-status{display:inline-block;border-radius:999px;padding:.25rem .55rem;border:1px solid #8a6728;background:#fff8e8;font-size:.75rem;font-weight:850}
      .lt-selection{display:grid;gap:1rem}.lt-selection-card{border:1px solid rgba(19,37,45,.18);border-left:7px solid #176b54;border-radius:14px;background:#fff;padding:1rem}.lt-selection-card[data-class*="WITHHOLD"]{border-left-color:#8d3d36}.lt-selection-card[data-class*="PARTIAL"],.lt-selection-card[data-class*="EXCERPT"]{border-left-color:#a56c00}.lt-selection-card h2{margin:.1rem 0 .45rem;font-size:1.2rem}.lt-pill{display:inline-block;border-radius:999px;padding:.25rem .55rem;background:#edf3ee;color:#173f36;font-size:.75rem;font-weight:850;margin:.15rem .25rem .15rem 0}.lt-selection-card dl{display:grid;grid-template-columns:minmax(140px,.28fr) 1fr;gap:.4rem .8rem}.lt-selection-card dt{font-weight:850;color:#47635b}.lt-selection-card dd{margin:0}.lt-note{border-left:6px solid #a56c00;background:#fff8e8;padding:1rem 1.1rem;border-radius:0 12px 12px 0;line-height:1.55}
      @media(max-width:760px){.lt-review-grid{grid-template-columns:1fr}.lt-selection-card dl{grid-template-columns:1fr}.lt-selection-card dt{margin-top:.4rem}}
    `;
    document.head.appendChild(style);
  };

  const getDecisions = () => {
    try { return JSON.parse(localStorage.getItem(storageKey) || '{}'); } catch (_) { return {}; }
  };
  const setDecisions = (value) => localStorage.setItem(storageKey, JSON.stringify(value));
  const decisionLabel = (value) => ({ ADMIT_NOW: copy.yes, NOT_NOW: copy.notNow, NEEDS_VERIFICATION: copy.verify }[value] || '');

  const renderReview = async (mount) => {
    const queue = await fetch(href('/data/canonical-discovery/review-candidates-20260904.json'), { cache: 'no-store' }).then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); });
    const decisions = getDecisions();
    mount.innerHTML = `
      <p class="lt-note">${esc(copy.localOnly)}</p>
      <div class="lt-toolbar"><button type="button" data-export>${esc(copy.export)}</button><button type="button" data-copy>${esc(copy.copy)}</button><a href="${esc(href(lang === 'es' ? '/es/seleccion-ingesta-evidencia/' : '/en/evidence-intake-selection/'))}">${esc(lang === 'es' ? 'Selección de evidencia' : 'Evidence selection')}</a></div>
      <div class="lt-review-grid">${(queue.candidates || []).map((candidate) => {
        const decision = decisions[candidate.candidate_id]?.decision || '';
        return `<article class="lt-review-card" id="${esc(candidate.candidate_id)}" data-candidate="${esc(candidate.candidate_id)}" data-decision="${esc(decision)}">
          <span class="lt-review-id">${esc(candidate.candidate_id)} · ${esc(candidate.candidate_type)} · ${esc(candidate.confidence)}</span>
          <h2>${esc(candidate.name)}</h2>
          <div class="lt-review-meta">
            <div><strong>${esc(copy.why)}</strong>${esc(candidate.why_found)}</div>
            <div><strong>${esc(copy.boundary)}</strong>${esc(candidate.why_not_canonical_yet)}</div>
            <div><strong>${esc(copy.next)}</strong>${esc(candidate.suggested_action)}</div>
            <div><strong>${esc(copy.source)}</strong>${(candidate.source_refs || []).map((item) => `<span class="lt-pill">${esc(item)}</span>`).join('')}</div>
            <div><strong>${esc(copy.routes)}</strong>${(candidate.suggested_routes || []).map((item) => `<a class="lt-pill" href="${esc(href(item))}">${esc(item)}</a>`).join('')}</div>
          </div>
          <div class="lt-review-actions">
            <button type="button" data-action="ADMIT_NOW">${esc(copy.yes)}</button>
            <button type="button" data-action="NOT_NOW">${esc(copy.notNow)}</button>
            <button type="button" data-action="NEEDS_VERIFICATION">${esc(copy.verify)}</button>
            <button type="button" data-action="CLEAR">${esc(copy.clear)}</button>
          </div><p class="lt-review-decision">${decision ? `${esc(copy.saved)}: ${esc(decisionLabel(decision))}` : ''}</p>
        </article>`;
      }).join('')}</div>`;

    const save = (card, action) => {
      const id = card.dataset.candidate;
      const state = getDecisions();
      if (action === 'CLEAR') delete state[id];
      else state[id] = { decision: action, decided_at: new Date().toISOString(), candidate_name: card.querySelector('h2')?.textContent || id };
      setDecisions(state);
      card.dataset.decision = action === 'CLEAR' ? '' : action;
      card.querySelector('.lt-review-decision').textContent = action === 'CLEAR' ? '' : `${copy.saved}: ${decisionLabel(action)}`;
    };
    mount.querySelectorAll('[data-action]').forEach((button) => button.addEventListener('click', () => save(button.closest('.lt-review-card'), button.dataset.action)));

    const packageData = () => ({ schema: 'por-derecho.canonical-discovery.user-decisions.v1', queue_id: queue.queue_id, exported_at: new Date().toISOString(), decisions: getDecisions() });
    mount.querySelector('[data-export]')?.addEventListener('click', () => {
      const blob = new Blob([JSON.stringify(packageData(), null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob); const link = document.createElement('a');
      link.href = url; link.download = `por-derecho-canonical-decisions-${new Date().toISOString().slice(0,10)}.json`; link.click(); URL.revokeObjectURL(url);
    });
    mount.querySelector('[data-copy]')?.addEventListener('click', async (event) => {
      await navigator.clipboard.writeText(JSON.stringify(packageData(), null, 2)); event.currentTarget.textContent = copy.copied;
    });
    const hash = window.location.hash.slice(1); if (hash) document.getElementById(hash)?.scrollIntoView({ block: 'start' });
  };

  const list = (items) => (items || []).length ? `<ul>${items.map((item) => `<li>${esc(item)}</li>`).join('')}</ul>` : '—';
  const renderMatrix = async (mount) => {
    const matrix = await fetch(href('/data/legaltech/notice-continued-conduct-matrix-20260904.json'), { cache: 'no-store' }).then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); });
    mount.innerHTML = `<p class="lt-note">${esc(matrix.purpose)}</p><div class="lt-toolbar"><a href="${esc(href(lang === 'es' ? '/es/uria-menendez-sun-park/#cronologia-integral' : '/en/uria-menendez-sun-park/#complete-chronology'))}">${esc(lang === 'es' ? 'Cronología Uría' : 'Uría chronology')}</a><a href="${esc(href(lang === 'es' ? '/es/revision-canonica/' : '/en/canonical-review/'))}">${esc(lang === 'es' ? 'Revisión canónica' : 'Canonical review')}</a></div><div class="lt-matrix-wrap"><table class="lt-matrix"><thead><tr>${[copy.matrixActor,copy.notice,copy.information,copy.conduct,copy.claimant,copy.outcome,copy.innocent,copy.missing,copy.issues,copy.status].map((item) => `<th>${esc(item)}</th>`).join('')}</tr></thead><tbody>${(matrix.rows || []).map((row) => `<tr><td>${esc(row.actor)}<br><small>${esc(row.capacity)}</small>${row.canonical_id ? `<br><code>${esc(row.canonical_id)}</code>` : ''}</td><td>${esc(row.first_documented_notice)}</td><td>${esc(row.information_available)}</td><td>${esc(row.subsequent_conduct)}</td><td>${esc(row.claimant_position)}</td><td>${esc(row.outcome_or_benefit)}</td><td>${esc(row.innocent_or_lawful_explanation)}</td><td>${list(row.missing_evidence)}</td><td>${list(row.possible_issues_if_proved)}</td><td><span class="lt-matrix-status">${esc(row.status)}</span></td></tr>`).join('')}</tbody></table></div>`;
  };

  const renderSelection = async (mount) => {
    const register = await fetch(href('/data/canonical-discovery/library-evidence-selection-20260904.json'), { cache: 'no-store' }).then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); });
    mount.innerHTML = `<p class="lt-note">${esc(copy.partial)}</p><div class="lt-toolbar"><a href="${esc(href(lang === 'es' ? '/es/revision-canonica/' : '/en/canonical-review/'))}">${esc(lang === 'es' ? 'Cola “sí / ahora no”' : '“Yes / not now” queue')}</a><a href="${esc(href(lang === 'es' ? '/es/visibilidad-evidencia/' : '/en/evidence-visibility/'))}">${esc(lang === 'es' ? 'Estándar de visibilidad' : 'Visibility standard')}</a></div><div class="lt-selection">${(register.priority_records || []).map((record) => `<article class="lt-selection-card" id="${esc(record.record_id)}" data-class="${esc(record.class)}"><span class="lt-review-id">${esc(record.record_id)}</span><h2>${esc(record.name)}</h2><span class="lt-pill">${esc(record.class)}</span><span class="lt-pill">${esc(record.status)}</span><dl><dt>${esc(copy.reason)}</dt><dd>${esc(record.reason)}</dd>${record.required_outputs ? `<dt>${esc(copy.outputs)}</dt><dd>${list(record.required_outputs)}</dd>` : ''}${record.public_derivative ? `<dt>${esc(lang === 'es' ? 'Derivado público' : 'Public derivative')}</dt><dd>${esc(record.public_derivative)}</dd>` : ''}${record.public_route ? `<dt>${esc(copy.source)}</dt><dd><a href="${esc(href(record.public_route))}">${esc(record.public_route)}</a></dd>` : ''}${record.interlinks ? `<dt>${esc(copy.interlinks)}</dt><dd>${record.interlinks.map((item) => `<span class="lt-pill">${esc(item)}</span>`).join('')}</dd>` : ''}</dl></article>`).join('')}</div>`;
  };

  const init = async () => {
    addStyle();
    const mount = document.querySelector('[data-legaltech-app]') || (() => { const div = document.createElement('div'); div.className = 'lt-app'; div.dataset.legaltechApp = '20260904'; main.appendChild(div); return div; })();
    mount.innerHTML = `<p class="lt-app-status">${esc(copy.loading)}</p>`;
    if (reviewRoutes.has(relative)) await renderReview(mount);
    else if (matrixRoutes.has(relative)) await renderMatrix(mount);
    else if (selectionRoutes.has(relative)) await renderSelection(mount);
  };

  init().catch((error) => {
    console.error('LegalTech review/matrix interface failed', error);
    const mount = document.querySelector('[data-legaltech-app]'); if (mount) mount.innerHTML = `<p class="lt-app-status">${esc(copy.error)}</p>`;
  });
})();
