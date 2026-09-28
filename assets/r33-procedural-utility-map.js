/* PD-AC-REMOVAL-PRECISION-20260928-01
 * Reader-layer clarification of existing dossiers. No original evidence is changed.
 * Shared data remains assets/data/r33-procedural-utility-map-v1.json.
 * The six-route allowlist does not alter home, capital or unrelated proceedings.
 */
(function () {
  'use strict';
  const ROUTES = Object.freeze({
    'es/concurso-36-2012-separacion-administrador-concursal-rpl-3304-2025/': 'removal',
    'en/insolvency-36-2012-administrator-removal-rpl-3304-2025/': 'removal',
    'es/concurso-36-2012-oposicion-ac-apelacion-lpb-septiembre-2026/': 'r33',
    'en/insolvency-36-2012-ac-opposition-lpb-appeal-september-2026/': 'r33',
    'es/cgpj-supervision-masa-activa/': 'cgpj',
    'en/cgpj-insolvency-estate-supervision/': 'cgpj'
  });
  const ISSUE_IDS = ['accounts', 'dation', 'hotel', 'counsel', 'fees', 'independence', 'banking'];
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[c]));
  const pick = (value, lang) => value && typeof value === 'object' && !Array.isArray(value) ? (value[lang] || value.en || '') : value;
  const normaliseRoute = path => path.replace(/^\//, '').replace(/index\.html$/, '').replace(/\/*$/, '/');
  function validateData(d) {
    if (!d || d.schema !== 'por-derecho.r33-procedural-utility-map.v1') throw new Error('Unexpected map schema');
    if (d.control !== 'PD-R33-PROCEDURAL-UTILITY-20260925-01') throw new Error('Unexpected canonical control');
    if (!Array.isArray(d.issues) || d.issues.map(i => i.id).join('|') !== ISSUE_IDS.join('|')) throw new Error('Existing issue identities changed');
    if (!d.sources || !d.clarifications || !Array.isArray(d.evidence_states)) throw new Error('Missing precision data');
    if (d.document.pages !== 22 || d.document.statement_propositions !== 276) throw new Error('Source coverage changed');
    const bilingual = value => value && typeof value.es === 'string' && value.es.length > 0 && typeof value.en === 'string' && value.en.length > 0;
    for (const item of d.issues) {
      for (const key of ['label', 'why', 'next', 'comparison', 'contrary', 'requested_outcome']) {
        if (!bilingual(item[key])) throw new Error('Missing bilingual issue field: ' + item.id + '/' + key);
      }
      if (!item.claim_family_ids.length || item.claim_family_ids.some(id => !/^AC-CLM-00[1-9]$|^AC-CLM-01[0-4]$/.test(id))) throw new Error('Unknown claim family');
      if (item.source_refs.some(id => !d.sources[id])) throw new Error('Unknown source reference');
    }
    for (const item of Object.values(d.clarifications)) {
      if (!bilingual(item.title) || !bilingual(item.body) || item.source_refs.some(id => !d.sources[id])) throw new Error('Invalid clarification');
    }
    if (d.transaction_rows.some(r => r.es.length !== 4 || r.en.length !== 4)) throw new Error('Incomplete bilingual comparison');
    return d;
  }
  // Export pure functions for dependency-free Node tests; do not execute browser code there.
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = {ROUTES, ISSUE_IDS, esc, pick, normaliseRoute, validateData};
    return;
  }
  if (window.__PD_AC_REMOVAL_PRECISION_STARTED) return;
  window.__PD_AC_REMOVAL_PRECISION_STARTED = true;
  const sourceScript = document.currentScript;
  if (!sourceScript) return;
  const rootURL = new URL('../', sourceScript.src);
  const route = location.pathname.startsWith(rootURL.pathname) ? normaliseRoute(location.pathname.slice(rootURL.pathname.length)) : '';
  const kind = ROUTES[route] || null;
  const lang = (document.documentElement.lang || 'en').toLowerCase().startsWith('es') ? 'es' : 'en';
  const t = value => pick(value, lang);
  const root = () => document.querySelector('main');
  const applied = [];
  const unresolved = [];

  function internalURL(path) {
    if (typeof path !== 'string' || !/^\/(en|es|assets|evidence)\//.test(path) || path.includes('..') || path.startsWith('//')) throw new Error('Unsafe internal source route');
    return new URL(path.slice(1), rootURL).href;
  }
  function sourceURL(s) {
    if (s.route || s.routes) return internalURL(s.route || s.routes[lang]);
    const url = new URL(s.url);
    if (url.protocol !== 'https:' || !['www.boe.es', 'github.com'].includes(url.hostname)) throw new Error('Unapproved external source');
    return url.href;
  }
  function refs(ids, d) {
    return '<p class="pd-r33-precision-sources">' + (lang === 'es' ? 'Fuentes y marco: ' : 'Sources and framework: ') + ids.map(id => {
      const s = d.sources[id];
      return '<a href="' + esc(sourceURL(s)) + '">' + esc(s.label) + '</a>';
    }).join(' · ') + '</p>';
  }
  function ensureStyles() {
    if (!document.querySelector('link[data-r33-precision-style]')) {
      const link = document.createElement('link');
      link.rel = 'stylesheet';
      link.href = new URL('assets/r33-procedural-utility-map.css?v=20260928a', rootURL).href;
      link.setAttribute('data-r33-precision-style', '20260928a');
      document.head.appendChild(link);
    }
    if (document.getElementById('pd-r33-precision-style')) return;
    const style = document.createElement('style');
    style.id = 'pd-r33-precision-style';
    style.textContent = '.pd-r33-precision{box-sizing:border-box;max-width:100%;margin:1.25rem 0;padding:1.2rem;border:1px solid #c7d2d5;border-left:5px solid #315c7b;border-radius:8px;background:#f7fafb;color:#142a33;overflow-wrap:anywhere}.pd-r33-precision h2,.pd-r33-precision h3{margin-top:.25rem;line-height:1.25}.pd-r33-precision p{line-height:1.65}.pd-r33-precision-sources{font-size:.88rem}.pd-r33-precision-sources a{font-weight:700}.pd-r33-precision-scroll{max-width:100%;overflow-x:auto}.pd-r33-precision table{width:100%;border-collapse:collapse}.pd-r33-precision th,.pd-r33-precision td{border:1px solid #ccd5d8;padding:.65rem;text-align:left;vertical-align:top;min-width:10rem}.pd-r33-precision th{background:#e9eff1}.pd-r33-precision details{margin:.75rem 0}.pd-r33-precision summary{cursor:pointer;font-weight:700}.pd-r33-precision .pd-r33-review-date{font-size:.78rem;letter-spacing:.04em;font-weight:700}.r33-issue .pd-r33-precision{margin:.7rem 0;padding:.8rem}.pd-r33-priority{padding:1rem;border-left:4px solid #315c7b;background:#f7fafb;color:#142a33}.pd-r33-methodology{margin:1rem 0;padding:.8rem;border:1px solid #ccd5d8}.pd-r33-methodology summary{cursor:pointer;font-weight:700}@media(max-width:600px){.pd-r33-precision{padding:.9rem}.pd-r33-precision th,.pd-r33-precision td{min-width:9rem}}';
    document.head.appendChild(style);
  }
  function panel(key, d, customId) {
    const c = d.clarifications[key];
    const box = document.createElement('aside');
    box.className = 'pd-r33-precision';
    box.id = customId || ('pd-r33-precision-' + key);
    box.setAttribute('data-pd-ac-precision', key);
    box.innerHTML = '<p class="pd-r33-review-date">' + (lang === 'es' ? 'PRECISIÓN DOCUMENTAL · 28 SEPTIEMBRE 2026' : 'DOCUMENTARY CLARIFICATION · 28 SEPTEMBER 2026') + '</p><h3>' + esc(t(c.title)) + '</h3><p>' + esc(t(c.body)) + '</p>' + refs(c.source_refs, d);
    return box;
  }
  function insertPanel(key, d, selector, after) {
    const id = 'pd-r33-precision-' + key;
    if (document.getElementById(id)) return;
    const box = panel(key, d);
    const target = selector && document.querySelector(selector);
    if (target) {
      if (after) target.insertAdjacentElement('afterend', box);
      else (target.querySelector('.shell') || target).appendChild(box);
    } else if (root()) {
      root().appendChild(box);
      if (selector) unresolved.push('Placement fallback: ' + key + ' / ' + selector);
    }
    applied.push(key);
  }
  function comparisonTable(d) {
    const heads = d.comparison_columns[lang].map(s => '<th scope="col">' + esc(s) + '</th>').join('');
    const rows = d.transaction_rows.map(r => '<tr><th scope="row">' + esc(r.date) + ' · ' + esc(r[lang][0]) + refs(r.source_refs, d) + '</th>' + r[lang].slice(1).map(s => '<td>' + esc(s) + '</td>').join('') + '</tr>').join('');
    return '<div class="pd-r33-precision-scroll" tabindex="0" role="region" aria-label="' + (lang === 'es' ? 'Comparación documental por operación' : 'Documentary comparison by transaction') + '"><table><thead><tr>' + heads + '</tr></thead><tbody>' + rows + '</tbody></table></div><p>' + (lang === 'es' ? 'Las celdas identifican comparaciones y documentos a verificar. No afirman que la documentación pendiente haya sido obtenida, admitida o resuelta favorablemente.' : 'Cells identify comparisons and records to verify. They do not claim that outstanding documents have been obtained, admitted or decided favourably.') + '</p>';
  }
  function addEvidenceStates(d, target) {
    if (document.getElementById('pd-r33-evidence-states')) return;
    const box = document.createElement('aside');
    box.id = 'pd-r33-evidence-states';
    box.className = 'pd-r33-precision';
    box.innerHTML = '<h3>' + (lang === 'es' ? 'Cuatro estados que no deben confundirse' : 'Four states that must not be conflated') + '</h3><dl>' + d.evidence_states.map(s => '<dt><strong>' + esc(t(s.label)) + '</strong></dt><dd>' + esc(t(s.rule)) + '</dd>').join('') + '</dl>' + refs(['LEC'], d);
    (target || root()).appendChild(box);
    applied.push('evidence-states');
  }
  function addHistoryBridge(d) {
    const id = lang === 'es' ? 'historia-separacion' : 'removal-history';
    if (document.getElementById(id)) return;
    const h = d.history_bridge;
    const section = document.createElement('section');
    section.id = id;
    section.className = 'section';
    section.setAttribute('data-pd-history-bridge', '20260928');
    section.innerHTML = '<div class="shell wrap"><div class="pd-r33-precision"><h2>' + esc(t(h.title)) + '</h2><p>' + esc(t(h.body)) + '</p><dl>' + h.events.map(e => '<dt><strong>' + esc(e.date) + '</strong></dt><dd>' + esc(e[lang]) + '</dd>').join('') + '</dl>' + refs(h.source_refs, d) + '</div></div>';
    const before = document.getElementById(lang === 'es' ? 'demanda-58-paginas' : 'application-58-pages');
    if (before) before.insertAdjacentElement('beforebegin', section); else root().appendChild(section);
    // Preserve both historically used incoming hash forms without duplicating an existing ID.
    const alias = lang === 'es' ? 'removal-history' : 'historia-separacion';
    if (!document.getElementById(alias)) {
      const a = document.createElement('span'); a.id = alias; section.prepend(a);
    }
    applied.push('history-bridge');
  }
  function correctDatedGapText(d) {
    const headings = Array.from(root().querySelectorAll('h2'));
    const h = headings.find(el => /^(Qué falta todavía|What is still missing|What remains missing|Remaining gaps)$/i.test(el.textContent.trim()));
    if (!h || h.dataset.pdPrecisionRevised) return;
    const p = h.nextElementSibling;
    if (!p || p.tagName !== 'P') return;
    const old = p.textContent;
    const history = document.createElement('details');
    history.className = 'pd-r33-methodology';
    history.innerHTML = '<summary>' + (lang === 'es' ? 'Redacción anterior preservada · no representa una comprobación actual de ausencia' : 'Previous wording preserved · not a current finding of absence') + '</summary><p>' + esc(old) + '</p>';
    h.textContent = lang === 'es' ? 'Control documental · revisión editorial de 28 septiembre 2026' : 'Document control · editorial review of 28 September 2026';
    h.dataset.pdPrecisionRevised = '20260928';
    p.textContent = t(d.clarifications.status.body);
    p.insertAdjacentElement('afterend', history);
    applied.push('dated-gap-correction');
  }
  function correctR33Terminology(d) {
    const headings = Array.from(root().querySelectorAll('h2,h3'));
    for (const h of headings) {
      if (/declaración probatoria|evidential declaration|evidentiary declaration/i.test(h.textContent)) {
        h.dataset.pdOriginalHeading = h.textContent;
        h.textContent = t(d.clarifications.r33_status.title);
        h.dataset.pdPrecisionRevised = '20260928';
        applied.push('r33-terminology');
      }
    }
  }
  function correctEquivalentAssumption() {
    const section = document.getElementById('nucleos') || document.getElementById('cores');
    if (section) {
      for (const p of section.querySelectorAll('p')) {
        if (/fuente neutral equivalente|equivalent neutral source/i.test(p.textContent)) {
          p.dataset.pdOriginalText = p.textContent;
          p.textContent = lang === 'es' ? 'Ante la denegación de pericial o reconocimiento, identificar las razones dadas y la prueba utilizada, en su caso, para resolver la cuestión fáctica controvertida. No presumir que toda denegación exigía legalmente una comprobación sustitutiva equivalente.' : 'Where an expert examination or inspection was refused, identify the reasons given and the evidence, if any, used to decide the disputed factual issue. Do not assume that every refusal legally required an equivalent substitute.';
          applied.push('expert-refusal-clarification');
        }
      }
    }
    const ledger = document.getElementById('ledger');
    if (ledger) {
      for (const td of ledger.querySelectorAll('td')) {
        if (/Pericial, inspección o fuente neutral equivalente|expert.*equivalent neutral/i.test(td.textContent)) {
          td.dataset.pdOriginalText = td.textContent;
          td.textContent = lang === 'es' ? 'Resolución y razones de admisión/denegación; prueba efectivamente utilizada para decidir' : 'Decision and reasons for admitting/refusing examination; evidence actually used to decide';
        }
      }
    }
  }
  function renderUtility(el, d) {
    if (el.dataset.pdPrecisionRendered === '20260928') return;
    const localLang = (el.dataset.lang || lang).startsWith('es') ? 'es' : 'en';
    const p = value => pick(value, localLang);
    const lanesById = Object.fromEntries(d.lanes.map(x => [x.id, x]));
    const lanes = d.lanes.map(l => '<article class="r33-lane ' + esc(l.tone) + '"><div class="role">' + esc(p(l.role)) + '</div><h3>' + esc(p(l.label)) + '</h3><p>' + esc(p(l.test)) + '</p><p><a href="' + esc(internalURL(l.routes[localLang])) + '">' + (localLang === 'es' ? 'Abrir vía' : 'Open lane') + ' →</a></p></article>').join('');
    const issues = d.issues.map(i => {
      const chips = i.lanes.map(id => '<a class="r33-chip" data-lane="' + esc(id) + '" href="' + esc(internalURL(lanesById[id].routes[localLang])) + '">' + esc(p(lanesById[id].label)) + '</a>').join('');
      const extra = ((i.extra_routes || {})[localLang] || []).map(r => '<a class="r33-chip" href="' + esc(internalURL(r)) + '">' + (localLang === 'es' ? 'Fuente relacionada' : 'Related source') + ' ↗</a>').join('');
      return '<article class="r33-issue" id="r33-utility-' + esc(i.id) + '"><div class="r33-issue-top"><h4>' + esc(p(i.label)) + '</h4><span class="r33-pages">' + (localLang === 'es' ? 'págs. ' : 'pp. ') + esc(i.pages) + '</span></div><p><strong>' + (localLang === 'es' ? 'Motivo y fuente: ' : 'Ground and source: ') + '</strong>' + esc(i.pleading_locator) + ' · ' + esc(i.claim_family_ids.join(' / ')) + '</p><p><strong>' + (localLang === 'es' ? 'Por qué importa. ' : 'Why it matters. ') + '</strong>' + esc(p(i.why)) + '</p><p><strong>' + (localLang === 'es' ? 'Comparación concreta. ' : 'Specific comparison. ') + '</strong>' + esc(p(i.comparison)) + '</p><p><strong>' + (localLang === 'es' ? 'Prueba contraria / alternativa lícita. ' : 'Contrary evidence / lawful alternative. ') + '</strong>' + esc(p(i.contrary)) + '</p><div class="r33-lane-tags">' + chips + extra + '</div><div class="r33-proof"><strong>' + (localLang === 'es' ? 'Prueba pendiente que cierra el salto' : 'Outstanding proof that closes the gap') + '</strong>' + esc(p(i.next)) + '</div><p><strong>' + (localLang === 'es' ? 'Resultado solicitado. ' : 'Requested outcome. ') + '</strong>' + esc(p(i.requested_outcome)) + '</p>' + refs(i.source_refs, d) + '</article>';
    }).join('');
    const gateways = d.gateways[localLang].map(g => '<a href="' + esc(internalURL(g.route)) + '">' + esc(g.label) + ' →</a>').join('');
    const priority = localLang === 'es' ? 'Primero: qué respuesta siguió al conocimiento de 2016; qué documento faltaba realmente para cada ejercicio contable; y si lo ejecutado coincidió con lo autorizado.' : 'Start with the response to 2016 notice, the records actually missing for each accounting year, and whether implementation matched authorisation.';
    const metrics = '<details class="pd-r33-methodology"><summary>' + (localLang === 'es' ? 'Metodología y cobertura · no puntuación de veracidad' : 'Methodology and coverage · not a truth score') + '</summary><p>' + esc(p(d.review_contract.metrics)) + '</p><p>R33 · ' + d.document.pages + ' ' + (localLang === 'es' ? 'páginas · ' : 'pages · ') + d.document.statement_propositions + ' ' + (localLang === 'es' ? 'proposiciones.' : 'propositions.') + '</p><p>' + d.issues.map(i => esc(p(i.label)) + ': ' + i.count).join(' · ') + '</p></details>';
    el.innerHTML = '<div class="r33-util-head"><div class="r33-util-spine"><div class="eyebrow">' + esc(d.document.id) + ' · ' + esc(d.control) + '</div><h2>' + (localLang === 'es' ? 'R33 como mapa de utilidad procesal' : 'R33 as a procedural-utility map') + '</h2><p>' + (localLang === 'es' ? 'Motivo → fuente → contraste → actor/capacidad → vía → resultado solicitado' : 'Ground → source → comparison → actor/capacity → lane → requested outcome') + '</p></div><div class="r33-util-boundary"><strong>' + esc(p(d.boundary)) + '</strong></div></div><p class="pd-r33-priority">' + priority + '</p><div class="r33-util-lanes">' + lanes + '</div><div class="r33-util-section-title"><h3>' + (localLang === 'es' ? 'Siete puertas probatorias' : 'Seven evidential gateways') + '</h3><p>' + (localLang === 'es' ? 'No son siete cargos ni siete conclusiones. Son siete rutas de prueba, vinculadas a las familias de pretensiones existentes.' : 'Not seven charges or conclusions. Seven routes for proof, linked to the existing claim families.') + '</p></div><div class="r33-issues">' + issues + '</div>' + metrics + '<h3>' + (localLang === 'es' ? 'Abrir expedientes conectados' : 'Open connected case files') + '</h3><div class="r33-util-gateways">' + gateways + '</div><p class="r33-util-note">' + esc(p(d.boundary)) + '</p>';
    el.dataset.pdPrecisionRendered = '20260928';
  }
  function applyPage(d) {
    if (!kind || !root()) return;
    const hero = root().querySelector('.hero,.ms-hero');
    insertPanel('thesis', d, hero ? ('main .' + (hero.classList.contains('ms-hero') ? 'ms-hero' : 'hero')) : null, true);
    if (kind === 'removal') {
      insertPanel('adverse', d, lang === 'es' ? '#primera-instancia' : '#first-instance');
      insertPanel('present_purpose', d, lang === 'es' ? '#petitum' : '#relief');
      insertPanel('authority', d, lang === 'es' ? '#siete-fundamentos' : '#seven-grounds', true);
      document.getElementById('pd-r33-precision-authority').insertAdjacentHTML('beforeend', comparisonTable(d));
      insertPanel('ownership', d, lang === 'es' ? '#fundamento-unidad' : '#ground-hotel-unit');
      const accounts = document.querySelector(lang === 'es' ? '#fundamento-cuentas' : '#ground-accounts');
      if (accounts && !accounts.querySelector('[data-pd-accounting-comparison]')) {
        const p = document.createElement('p'); p.setAttribute('data-pd-accounting-comparison', '20260928'); p.textContent = t(d.issues[0].comparison); accounts.appendChild(p);
      }
      addHistoryBridge(d);
      correctDatedGapText(d);
      insertPanel('status', d, lang === 'es' ? '#matriz-evidencia' : '#evidence-matrix');
      addEvidenceStates(d, document.getElementById('pd-r33-precision-status'));
    }
    if (kind === 'r33') {
      correctR33Terminology(d);
      insertPanel('r33_status', d, '#paso-forense-procesal, #forensic-procedural-step');
      insertPanel('notice2016', d, '#paso-forense-procesal, #forensic-procedural-step');
      insertPanel('authority', d, '#paso-forense-procesal, #forensic-procedural-step');
      document.getElementById('pd-r33-precision-authority').insertAdjacentHTML('beforeend', comparisonTable(d));
      if (!document.querySelector('[data-r33-procedural-utility]')) {
        const section = document.createElement('section'); section.className = 'section'; section.id = 'pd-r33-utility-continuity';
        section.innerHTML = '<div class="shell"><div data-r33-procedural-utility data-lang="' + lang + '"></div></div>';
        root().appendChild(section);
      }
      addEvidenceStates(d);
    }
    if (kind === 'cgpj') {
      insertPanel('institutional', d, '#ledger');
      insertPanel('authority', d, '#ledger');
      document.getElementById('pd-r33-precision-authority').insertAdjacentHTML('beforeend', comparisonTable(d));
      insertPanel('ownership', d, '#perimetro, #perimeter');
      correctEquivalentAssumption();
      addEvidenceStates(d);
    }
  }
  async function init() {
    if (!kind && !document.querySelector('[data-r33-procedural-utility]')) return;
    ensureStyles();
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 15000);
    try {
      const url = new URL('assets/data/r33-procedural-utility-map-v1.json', rootURL);
      const response = await fetch(url.href, {cache: 'no-store', signal: controller.signal, credentials: 'same-origin'});
      if (!response.ok) throw new Error('HTTP ' + response.status);
      const d = validateData(await response.json());
      applyPage(d);
      document.querySelectorAll('[data-r33-procedural-utility]').forEach(el => renderUtility(el, d));
      window.PD_AC_REMOVAL_PRECISION = {control: d.review_control, route, kind, applied, unresolved, dataLoaded: true};
      document.dispatchEvent(new CustomEvent('pd-ac-removal-precision-ready', {detail: window.PD_AC_REMOVAL_PRECISION}));
      // Repair incoming history deep links only after the additive anchor exists.
      if (kind === 'removal' && ['#historia-separacion', '#removal-history'].includes(location.hash)) {
        const target = document.getElementById(location.hash.slice(1)); if (target) target.scrollIntoView({block: 'start'});
      }
    } catch (error) {
      window.PD_AC_REMOVAL_PRECISION = {route, kind, dataLoaded: false, error: String(error.message || error)};
      const target = document.querySelector('[data-r33-procedural-utility]') || (kind && root());
      if (target && !document.getElementById('pd-r33-precision-error')) {
        const p = document.createElement('p'); p.id = 'pd-r33-precision-error'; p.className = 'pd-r33-precision';
        p.textContent = lang === 'es' ? 'La precisión documental actual no ha podido cargarse. El contenido y las fuentes anteriores permanecen disponibles; no se certifica una actualización de estado.' : 'The current documentary clarification could not be loaded. Earlier content and sources remain available; no status update is certified.';
        target.appendChild(p);
      }
    } finally { clearTimeout(timer); }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once: true}); else init();
})();
