(() => {
  const root = document.querySelector('[data-c36-court-record]');
  if (!root) return;

  const lang = root.dataset.lang === 'en' ? 'en' : 'es';
  const t = lang === 'en' ? {
    status: 'Status', records: 'Controlled/corroborated nodes', closed: 'Closed points',
    open: 'Open points / next proof', queue: 'Autonomous P0 queue', filing: 'Party filing',
    decision: 'Court decision', laj: 'LAJ act', cross: 'Court decision (cross-reference)',
    admin: 'AC report', registry: 'Registry record', verified: 'Primary-controlled',
    boundary: 'This is a reconstructed located corpus, not the certified court docket. A filing proves an allegation/request was made; a ruling proves what the court/LAJ decided. Neither alone proves criminal misconduct.',
    supp: 'supplements loaded', families: 'Additional closed/narrowed families',
    corr: 'Gap corrections', orph: 'Orphans / non-promoted material', impl: 'Implementation checkpoints'
  } : {
    status: 'Estado', records: 'Nodos controlados/corroborados', closed: 'Puntos cerrados',
    open: 'Puntos abiertos / próxima prueba', queue: 'Cola autónoma P0', filing: 'Escrito de parte',
    decision: 'Resolución judicial', laj: 'Acto LAJ', cross: 'Resolución judicial (referencia cruzada)',
    admin: 'Informe AC', registry: 'Registro de la Propiedad', verified: 'Control primario',
    boundary: 'Este es un corpus localizado reconstruido, no el índice judicial certificado. Un escrito prueba que se formuló una alegación/petición; una resolución prueba lo que decidió el órgano/LAJ. Ninguno por sí solo prueba conducta penal.',
    supp: 'suplementos cargados', families: 'Familias adicionales cerradas/acotadas',
    corr: 'Correcciones de gaps', orph: 'Huérfanos / material no promovido', impl: 'Checkpoints de implementación'
  };

  const esc = value => String(value ?? '').replace(/[&<>"']/g, char => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
  }[char]));
  const klass = record => record.record_class === 'party_filing' ? t.filing
    : record.record_class === 'court_decision' ? t.decision
    : record.record_class === 'court_decision_cross_reference' ? t.cross
    : record.record_class === 'administrator_report' ? t.admin
    : record.record_class === 'registry_record' ? t.registry : t.laj;
  const card = record => `<article class="c36-record">
    <p class="c36-kicker">${esc(record.date)} · ${esc(klass(record))}</p>
    <h3>${esc(record.title || record.summary || record.id)}</h3>
    ${record.verification ? `<p><strong>${esc(t.verified)}:</strong> ${esc(record.verification)}</p>` : ''}
    ${record.procedure ? `<p><strong>Procedure:</strong> ${esc(record.procedure)}</p>` : ''}
    ${record.lexnet_id ? `<p><strong>LexNET:</strong> <code>${esc(record.lexnet_id)}</code></p>` : ''}
    ${record.notification_lexnet_id ? `<p><strong>Notification LexNET:</strong> <code>${esc(record.notification_lexnet_id)}</code></p>` : ''}
    ${record.lexnet_sent_id ? `<p><strong>LexNET sent:</strong> <code>${esc(record.lexnet_sent_id)}</code>${record.lexnet_ack_id ? ` · ack <code>${esc(record.lexnet_ack_id)}</code>` : ''}</p>` : ''}
    ${record.electronic_document_id ? `<p><strong>Doc ID:</strong> <code>${esc(record.electronic_document_id)}</code></p>` : ''}
    ${record.registry_csv ? `<p><strong>Registry CSV:</strong> <code>${esc(record.registry_csv)}</code></p>` : ''}
    ${record.operative_effect ? `<p>${esc(record.operative_effect)}</p>` : ''}
    ${record.summary ? `<p>${esc(record.summary)}</p>` : ''}
    ${record.proof_limit ? `<p><em>${esc(record.proof_limit)}</em></p>` : ''}
    ${record.open_point ? `<p><strong>Open:</strong> ${esc(record.open_point)}</p>` : ''}
    ${record.response_taxonomy ? `<p><span class="c36-tag">${esc(record.response_taxonomy)}</span></p>` : ''}
  </article>`;

  Promise.all([
    fetch('../../assets/data/concurso36-court-record-reconstruction-v1.json', { cache: 'no-store' }).then(response => response.json()),
    fetch('../../assets/data/concurso36-court-record-reconstruction-2022-appellate-supplement.json', { cache: 'no-store' }).then(response => response.ok ? response.json() : null).catch(() => null),
    fetch('../../assets/data/concurso36-court-record-reconstruction-gapclose2-20260829.json', { cache: 'no-store' }).then(response => response.ok ? response.json() : null).catch(() => null),
    fetch('../../assets/data/concurso36-court-record-reconstruction-registry-notice-20260831.json', { cache: 'no-store' }).then(response => response.ok ? response.json() : null).catch(() => null)
  ]).then(([data, appeal, gap, notice]) => {
    const family = data.verified_families?.[0] || {};
    const records = [
      ...(family.records || []),
      ...((appeal && appeal.family_id === family.family_id) ? appeal.records || [] : []),
      ...((gap && gap.append_to_family_id === family.family_id) ? gap.append_records || [] : [])
    ].sort((a, b) => (a.date || '').localeCompare(b.date || '') || (a.id || '').localeCompare(b.id || ''));
    const extras = [...(gap?.additional_families || []), ...(notice?.additional_families || [])];
    const total = records.length + extras.reduce((sum, item) => sum + (item.records || []).length, 0);
    const closed = [...(family.closed_points || []), ...((appeal && appeal.family_id === family.family_id) ? appeal.closed_points_add || [] : [])];
    const open = gap?.open_points_replace?.length ? gap.open_points_replace
      : (appeal && appeal.family_id === family.family_id && appeal.open_points_replace?.length ? appeal.open_points_replace : (family.open_points || []));
    const checkpoints = (gap?.implementation_checkpoints || []).filter(item => !notice || item.id !== 'C36-CHK-20181228-REGISTRY-FREE-FINCAS');

    root.innerHTML = `<div class="c36-boundary"><strong>${esc(t.status)}:</strong> ${esc(data.status)} · ${esc(t.supp)}: ${[appeal, gap, notice].filter(Boolean).length}<br>${esc(t.boundary)}</div>
      <h2>${esc(family.label || '2021–2022 appeal/testimonio family')}</h2>
      <p><strong>${esc(t.records)}:</strong> ${total}</p>
      <div class="c36-record-grid">${records.map(card).join('')}</div>
      ${extras.length ? `<section><h2>${esc(t.families)}</h2>${extras.map(item => `<section><h3>${esc(lang === 'en' ? (item.label_en || item.family_id) : (item.label_es || item.family_id))}</h3><div class="c36-record-grid">${(item.records || []).sort((a, b) => (a.date || '').localeCompare(b.date || '')).map(card).join('')}</div>${item.open_points?.length ? `<ul>${item.open_points.map(point => `<li>${esc(point)}</li>`).join('')}</ul>` : ''}</section>`).join('')}</section>` : ''}
      ${gap?.gap_corrections?.length ? `<section><h2>${esc(t.corr)}</h2><ul>${gap.gap_corrections.map(item => `<li>${esc(item)}</li>`).join('')}</ul></section>` : ''}
      ${checkpoints.length ? `<section><h2>${esc(t.impl)}</h2><div class="c36-queue">${checkpoints.map(item => `<article><strong>${esc(item.date)} · ${esc(item.id)}</strong><p>${esc(item.summary)}</p><p><em>${esc(item.proof_limit || '')}</em></p></article>`).join('')}</div></section>` : ''}
      ${gap?.orphan_records?.length ? `<section><h2>${esc(t.orph)}</h2><div class="c36-queue">${gap.orphan_records.map(item => `<article><strong>${esc(item.id)} · ${esc(item.status)}</strong><p>${esc(item.summary)}</p></article>`).join('')}</div></section>` : ''}
      <div class="c36-two"><section><h2>${esc(t.closed)}</h2><ul>${closed.map(item => `<li>${esc(item)}</li>`).join('')}</ul></section><section><h2>${esc(t.open)}</h2><ul>${open.map(item => `<li>${esc(item)}</li>`).join('')}</ul></section></div>
      <section><h2>${esc(t.queue)}</h2><div class="c36-queue">${open.map((item, index) => `<article><strong>P0-${index + 1}</strong><p>${esc(item)}</p></article>`).join('')}</div></section>`;
  }).catch(error => {
    root.innerHTML = `<p>Record registry unavailable: ${esc(error.message)}</p>`;
  });
})();
