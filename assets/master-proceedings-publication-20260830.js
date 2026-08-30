(() => {
  const current = document.currentScript;
  if (!current) return;

  const assetBase = new URL('.', current.src);
  const repoBase = new URL('../', assetBase);
  const lang = (document.documentElement.lang || 'en').toLowerCase().startsWith('es') ? 'es' : 'en';
  const routes = {
    en: new URL('en/master-proceedings-register/', repoBase).href,
    es: new URL('es/registro-maestro-procedimientos/', repoBase).href
  };
  const detailRoutes = {
    'LZ-JUD-042': {
      en: new URL('en/dp-3205-2014-arrecife/', repoBase).href,
      es: new URL('es/dp-3205-2014-arrecife/', repoBase).href
    }
  };
  const csvUrl = new URL('archive/PROCEEDINGS_MASTER_REGISTER.csv', repoBase).href;

  const addCss = () => {
    if (document.querySelector('link[data-master-proceedings-css]')) return;
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = new URL('master-proceedings-publication-20260830.css?v=20260830a', assetBase).href;
    link.setAttribute('data-master-proceedings-css', '20260830a');
    document.head.appendChild(link);
  };

  const addSiteLinks = () => {
    const nav = document.querySelector('.main-nav');
    if (nav && !nav.querySelector('[data-master-proceedings-nav]')) {
      const a = document.createElement('a');
      a.href = routes[lang];
      a.className = 'pd-proceedings-nav-link';
      a.setAttribute('data-master-proceedings-nav', '20260830');
      a.textContent = lang === 'es' ? 'Procedimientos' : 'Proceedings';
      const record = Array.from(nav.querySelectorAll('a')).find((item) => /registro|record/i.test(item.textContent || ''));
      if (record && record.nextSibling) nav.insertBefore(a, record.nextSibling);
      else nav.appendChild(a);
    }

    const timeline = document.querySelector('.recovery-timeline');
    if (timeline && !document.querySelector('[data-master-proceedings-timeline-link]')) {
      const box = document.createElement('aside');
      box.className = 'pd-proceedings-timeline-link';
      box.setAttribute('data-master-proceedings-timeline-link', '20260830');
      if (lang === 'es') {
        box.innerHTML = '<strong>La cronología tiene una columna procesal.</strong><p>El Registro Maestro de Procedimientos enlaza las distintas vías judiciales, fiscales, administrativas, regulatorias, tributarias, profesionales y de fondos públicos sin confundirlas entre sí.</p><a href="' + routes.es + '">Abrir el mapa multivía de procedimientos →</a>';
      } else {
        box.innerHTML = '<strong>The chronology has a procedural spine.</strong><p>The Master Proceedings Register links the judicial, prosecutorial, administrative, regulatory, tax, professional and public-funds tracks without collapsing legally distinct files into one case.</p><a href="' + routes.en + '">Open the multitrack proceedings map →</a>';
      }
      timeline.parentNode.insertBefore(box, timeline.nextSibling);
    }
  };

  const parseCsv = (text) => {
    const rows = [];
    let row = [];
    let field = '';
    let quoted = false;
    for (let i = 0; i < text.length; i += 1) {
      const ch = text[i];
      if (quoted) {
        if (ch === '"' && text[i + 1] === '"') {
          field += '"';
          i += 1;
        } else if (ch === '"') {
          quoted = false;
        } else {
          field += ch;
        }
      } else if (ch === '"') {
        quoted = true;
      } else if (ch === ',') {
        row.push(field);
        field = '';
      } else if (ch === '\n') {
        row.push(field.replace(/\r$/, ''));
        rows.push(row);
        row = [];
        field = '';
      } else {
        field += ch;
      }
    }
    if (field.length || row.length) {
      row.push(field.replace(/\r$/, ''));
      rows.push(row);
    }
    if (!rows.length) return [];
    const headers = rows.shift();
    return rows.filter((r) => r.some((v) => v.trim() !== '')).map((r) => {
      const obj = {};
      headers.forEach((h, idx) => { obj[h] = r[idx] || ''; });
      return obj;
    });
  };

  const isPublicRow = (row) => {
    const treatment = (row.Public_Treatment || '').toUpperCase();
    if (treatment.includes('INTERNAL_ONLY')) return false;
    if (treatment.includes('PRIVATE')) return false;
    if (treatment.includes('NOT_SITE_AGGREGATED')) return false;
    return true;
  };

  const esc = (value) => String(value || '').replace(/[&<>"']/g, (ch) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[ch]));

  const norm = (value) => String(value || '').trim();

  const initRegister = async () => {
    const root = document.querySelector('[data-master-proceedings-page]');
    if (!root) return;

    const copy = lang === 'es' ? {
      loading: 'Cargando el registro canónico…', error: 'No se pudo cargar el registro maestro.',
      visible: 'registros visibles', export: 'Exportar vista filtrada CSV', all: 'Todos',
      search: 'Buscar referencia, órgano, objeto, estado…', stream: 'Vía', state: 'Tipo de registro', source: 'Estado de fuente',
      id: 'ID', type: 'Clase / vía', organ: 'Órgano / custodio', ref: 'Referencia', period: 'Periodo', connection: 'Conexión / objeto', status: 'Estado / último evento', links: 'Relaciones', proof: 'Fuente / brecha',
      noRows: 'No hay filas que coincidan con los filtros actuales.'
    } : {
      loading: 'Loading the canonical register…', error: 'The master register could not be loaded.',
      visible: 'visible records', export: 'Export filtered view CSV', all: 'All',
      search: 'Search reference, organ, object, status…', stream: 'Track', state: 'Record state', source: 'Source status',
      id: 'ID', type: 'Class / track', organ: 'Organ / custodian', ref: 'Reference', period: 'Period', connection: 'Connection / object', status: 'Status / latest event', links: 'Relationships', proof: 'Source / gap',
      noRows: 'No rows match the current filters.'
    };

    const loading = root.querySelector('[data-register-loading]');
    try {
      const response = await fetch(csvUrl, { cache: 'no-store' });
      if (!response.ok) throw new Error('HTTP ' + response.status);
      const text = await response.text();
      const allRows = parseCsv(text);
      const rows = allRows.filter(isPublicRow);
      const excluded = allRows.length - rows.length;

      const getSet = (key) => Array.from(new Set(rows.map((r) => norm(r[key])).filter(Boolean))).sort((a, b) => a.localeCompare(b));
      const streamValues = getSet('Stream');
      const sourceValues = getSet('Source_Status');
      const stateValues = ['TRUE', 'FALSE', 'UNVERIFIED'].filter((v) => rows.some((r) => norm(r.Is_Proceeding).toUpperCase() === v));

      root.innerHTML = `
        <div class="pd-stats" data-register-stats></div>
        <div class="pd-filters" aria-label="${lang === 'es' ? 'Filtros del registro' : 'Register filters'}">
          <label>${lang === 'es' ? 'Buscar' : 'Search'}<input type="search" data-filter-search placeholder="${copy.search}"></label>
          <label>${copy.stream}<select data-filter-stream><option value="">${copy.all}</option>${streamValues.map((v) => `<option>${esc(v)}</option>`).join('')}</select></label>
          <label>${copy.state}<select data-filter-state><option value="">${copy.all}</option>${stateValues.map((v) => `<option>${esc(v)}</option>`).join('')}</select></label>
          <label>${copy.source}<select data-filter-source><option value="">${copy.all}</option>${sourceValues.map((v) => `<option>${esc(v)}</option>`).join('')}</select></label>
        </div>
        <div class="pd-register-tools"><strong data-visible-count></strong><button type="button" data-export-visible>${copy.export}</button></div>
        <div class="pd-register-table-wrap"><table>
          <thead><tr><th>${copy.id}</th><th>${copy.type}</th><th>${copy.organ}</th><th>${copy.ref}</th><th>${copy.period}</th><th>${copy.connection}</th><th>${copy.status}</th><th>${copy.links}</th><th>${copy.proof}</th></tr></thead>
          <tbody data-register-body></tbody>
        </table></div>
        <p class="pd-source-note">${lang === 'es' ? `Proyección pública del registro canónico. ${excluded} fila(s) con tratamiento interno/privado quedan fuera de esta vista. Las notas internas, anclajes privados y campos de estrategia no se representan.` : `Public projection of the canonical register. ${excluded} row(s) marked internal/private are excluded from this view. Internal notes, private anchors and strategy fields are not rendered.`}</p>
      `;

      const body = root.querySelector('[data-register-body]');
      const search = root.querySelector('[data-filter-search]');
      const stream = root.querySelector('[data-filter-stream]');
      const state = root.querySelector('[data-filter-state]');
      const source = root.querySelector('[data-filter-source]');
      const count = root.querySelector('[data-visible-count]');
      const stats = root.querySelector('[data-register-stats]');
      let visible = [];

      const renderStats = () => {
        const distinctProceedings = rows.filter((r) => norm(r.Is_Proceeding).toUpperCase() === 'TRUE').length;
        const unverified = rows.filter((r) => norm(r.Is_Proceeding).toUpperCase() === 'UNVERIFIED').length;
        const references = rows.filter((r) => norm(r.Is_Proceeding).toUpperCase() === 'FALSE').length;
        const tracks = new Set(rows.map((r) => norm(r.Stream)).filter(Boolean)).size;
        const labels = lang === 'es' ? ['Procedimientos / expedientes', 'Candidatos no verificados', 'Referencias de apoyo', 'Vías distintas'] : ['Proceedings / files', 'Unverified candidates', 'Supporting references', 'Distinct tracks'];
        stats.innerHTML = [distinctProceedings, unverified, references, tracks].map((n, i) => `<div class="pd-stat"><strong>${n}</strong><span>${labels[i]}</span></div>`).join('');
      };

      const render = () => {
        const q = search.value.trim().toLowerCase();
        const s = stream.value;
        const st = state.value;
        const so = source.value;
        visible = rows.filter((r) => {
          if (s && norm(r.Stream) !== s) return false;
          if (st && norm(r.Is_Proceeding).toUpperCase() !== st) return false;
          if (so && norm(r.Source_Status) !== so) return false;
          if (!q) return true;
          const hay = [r.Master_ID, r.Legacy_ID, r.Stream, r.Geography, r.Origin_Organ, r.Current_Custodian, r.Reference, r.Secondary_Reference, r.NIG, r.Connection, r.Object_or_Purpose, r.Status, r.Latest_Known_Event, r.Appeal_or_Review, r.Linked_Proceedings, r.Source_Status, r.Open_Reference_Gap].join(' ').toLowerCase();
          return hay.includes(q);
        });
        count.textContent = `${visible.length} ${copy.visible}`;
        if (!visible.length) {
          body.innerHTML = `<tr><td colspan="9" class="pd-empty">${copy.noRows}</td></tr>`;
          return;
        }
        body.innerHTML = visible.map((r) => {
          const stateValue = norm(r.Is_Proceeding).toUpperCase() || 'UNVERIFIED';
          const relation = [r.Parent_Master_ID ? `${lang === 'es' ? 'Padre' : 'Parent'}: ${r.Parent_Master_ID}` : '', r.Linked_Proceedings, r.Appeal_or_Review].filter(Boolean).join(' · ');
          const statusText = [r.Status, r.Latest_Known_Event].filter(Boolean).join(' — ');
          const proofText = [r.Source_Status, r.Open_Reference_Gap].filter(Boolean).join(' — ');
          const organText = [r.Origin_Organ, r.Current_Custodian && r.Current_Custodian !== r.Origin_Organ ? `${lang === 'es' ? 'Ahora' : 'Now'}: ${r.Current_Custodian}` : ''].filter(Boolean).join(' · ');
          const refText = [r.Reference, r.Secondary_Reference, r.NIG ? `NIG ${r.NIG}` : ''].filter(Boolean).join(' · ');
          const typeText = [r.Record_Type, r.Proceeding_Class, r.Stream].filter(Boolean).join(' · ');
          const connectionText = [r.Connection, r.Object_or_Purpose].filter(Boolean).join(' — ');
          const detailUrl = detailRoutes[r.Master_ID] && detailRoutes[r.Master_ID][lang];
          const idHtml = detailUrl
            ? `<a class="pd-ref" href="${esc(detailUrl)}" aria-label="${esc(`${r.Master_ID} · ${refText || r.Reference || ''}`)}">${esc(r.Master_ID)} ↗</a>`
            : `<span class="pd-ref">${esc(r.Master_ID)}</span>`;
          return `<tr>
            <td>${idHtml}<br><span class="pd-chip" data-state="${esc(stateValue)}">${esc(stateValue)}</span></td>
            <td>${esc(typeText)}</td><td>${esc(organText)}</td><td>${esc(refText)}</td><td>${esc(r.Date_or_Period)}</td><td>${esc(connectionText)}</td><td>${esc(statusText)}</td><td>${esc(relation)}</td><td><span class="pd-muted">${esc(r.Source_Status)}</span>${r.Open_Reference_Gap ? `<br><span class="pd-gap">${esc(r.Open_Reference_Gap)}</span>` : ''}</td>
          </tr>`;
        }).join('');
      };

      [search, stream, state, source].forEach((control) => control.addEventListener('input', render));
      root.querySelector('[data-export-visible]').addEventListener('click', () => {
        const headers = ['Master_ID','Is_Proceeding','Record_Type','Proceeding_Class','Stream','Geography','Origin_Organ','Current_Custodian','Reference','Secondary_Reference','NIG','Date_or_Period','Connection','Object_or_Purpose','Status','Latest_Known_Event','Appeal_or_Review','Parent_Master_ID','Linked_Proceedings','Source_Status','Open_Reference_Gap'];
        const quote = (v) => `"${String(v || '').replace(/"/g, '""')}"`;
        const output = [headers.join(','), ...visible.map((r) => headers.map((h) => quote(r[h])).join(','))].join('\n');
        const blob = new Blob([output], { type: 'text/csv;charset=utf-8' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = lang === 'es' ? 'registro-maestro-procedimientos-vista-publica.csv' : 'master-proceedings-register-public-view.csv';
        document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
      });
      renderStats();
      render();
    } catch (err) {
      if (loading) loading.remove();
      root.innerHTML = `<div class="pd-error"><strong>${copy.error}</strong><br>${esc(err.message || err)}</div>`;
    }
  };

  addCss();
  const start = () => { addSiteLinks(); initRegister(); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, { once: true });
  else start();
})();
