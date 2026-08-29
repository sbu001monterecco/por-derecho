(() => {
  'use strict';
  const root = location.pathname.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const lang = document.documentElement.lang === 'en' ? 'en' : 'es';
  const t = lang === 'es' ? {
    loading:'Cargando el registro canónico…', error:'No se pudo cargar el registro canónico. Use los enlaces de datos directos.',
    filings:'escritos de parte localizados', judicial:'actos judiciales/LAJ localizados', noDate:'Fecha no cerrada',
    actor:'Actor / presentante', effect:'Objeto, efecto o proposición registrada', limit:'Condición / límite', status:'Estado probatorio',
    search:'Filtrar por fecha, actor, título, ID o texto…', all:'Todos los escritos de parte localizados',
    treatment:'Tratamiento judicial, omisiones verificables y límites', gaps:'Vacíos que deben cerrarse', source:'Fuente pública controlada'
  } : {
    loading:'Loading canonical record…', error:'The canonical record could not be loaded. Use the direct data links.',
    filings:'located party filings', judicial:'located judicial/LAJ acts', noDate:'Date not closed',
    actor:'Actor / filer', effect:'Recorded object, effect or proposition', limit:'Condition / limit', status:'Evidence status',
    search:'Filter by date, actor, title, ID or text…', all:'All located party filings',
    treatment:'Court treatment, verifiable omissions and limits', gaps:'Gaps still to close', source:'Controlled public source'
  };
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const date = s => s ? esc(s) : t.noDate;
  const linkFor = r => {
    const p = r.public_derivative || {};
    const target = p.public_pdf || p.index || null;
    if (!target) return '';
    const href = target.startsWith('http') ? target : root + target.replace(/^\//,'');
    return `<a class="mini-link" href="${esc(href)}">${t.source}</a>`;
  };
  const searchable = r => [r.canonical_id,r.date,r.document_type,r.title_or_function,r.issuer_or_actor,r.direct_effect_or_proposition,r.conditions_or_limits,r.evidence_label].join(' ').toLowerCase();
  Promise.all([
    fetch(root+'assets/data/concurso36-complete-record-v1.json',{cache:'no-store'}).then(r=>r.ok?r.json():Promise.reject(r.status)),
    fetch(root+'assets/data/concurso36-court-treatment-overreach-matrix-20260829.json',{cache:'no-store'}).then(r=>r.ok?r.json():Promise.reject(r.status))
  ]).then(([record,matrix]) => {
    const records = Array.isArray(record.records) ? record.records : [];
    const filings = records.filter(r => r.record_class === 'party_filing').sort((a,b)=>(a.date||'9999').localeCompare(b.date||'9999'));
    const judicial = records.filter(r => ['judicial_act','laj_or_court_office_act','judicial_or_laj_type_unresolved'].includes(r.record_class));
    document.querySelectorAll('[data-filing-count]').forEach(el=>el.textContent=filings.length);
    document.querySelectorAll('[data-judicial-count]').forEach(el=>el.textContent=judicial.length);
    document.querySelectorAll('[data-cutoff]').forEach(el=>el.textContent=record.cutoff || matrix.cutoff || '2026-08-29');

    const body = document.querySelector('#filing-body');
    const input = document.querySelector('#filing-filter');
    const renderFilings = q => {
      const needle = (q||'').trim().toLowerCase();
      const shown = needle ? filings.filter(r=>searchable(r).includes(needle)) : filings;
      body.innerHTML = shown.map(r=>`<tr>
        <td><strong>${date(r.date)}</strong><small>${esc(r.canonical_id)}</small></td>
        <td><strong>${esc(r.title_or_function || r.document_type || '')}</strong><small>${esc(r.document_type || '')}</small></td>
        <td>${esc(r.issuer_or_actor || '—')}</td>
        <td>${esc(r.direct_effect_or_proposition || '—')}<small>${esc(r.conditions_or_limits || '')}</small>${linkFor(r)}</td>
        <td><span class="evidence-pill">${esc(r.evidence_label || r.complete_copy_status || '—')}</span></td>
      </tr>`).join('') || `<tr><td colspan="5">0</td></tr>`;
      const visible = document.querySelector('[data-visible-count]'); if (visible) visible.textContent=shown.length;
    };
    renderFilings('');
    input.addEventListener('input',()=>renderFilings(input.value));

    const tracks = document.querySelector('#treatment-tracks');
    tracks.innerHTML = (matrix.tracks||[]).map(x=>`<article class="track" id="${esc(x.id)}">
      <div class="track-top"><span>${esc(x.id)}</span><time>${esc(x.date_or_period)}</time></div>
      <h3>${esc(x.issue)}</h3>
      ${x.documented_court_effect?`<p><strong>${lang==='es'?'Efecto judicial documentado':'Documented court effect'}:</strong> ${esc(x.documented_court_effect)}</p>`:''}
      ${x.documented_or_reported_event?`<p><strong>${lang==='es'?'Hecho documentado o registrado':'Documented or recorded event'}:</strong> ${esc(x.documented_or_reported_event)}</p>`:''}
      ${x.court_treatment_status?`<p class="treatment"><strong>${lang==='es'?'Tratamiento / estado':'Treatment / status'}:</strong> ${esc(x.court_treatment_status)}</p>`:''}
      <p><strong>${lang==='es'?'Límite':'Limit'}:</strong> ${esc(x.limit || '—')}</p>
      <p><strong>${lang==='es'?'Relevancia':'Relevance'}:</strong> ${esc(x.position_or_consequence || '—')}</p>
      <footer><span class="evidence-pill">${esc(x.evidence_status || '')}</span>${(x.source_records||[]).length?` <code>${esc(x.source_records.join(' · '))}</code>`:''}</footer>
    </article>`).join('');

    const gaps = document.querySelector('#gap-list');
    gaps.innerHTML = (matrix.gap_closure||[]).map(x=>`<li>${esc(x)}</li>`).join('');
    document.querySelectorAll('[data-loading]').forEach(el=>el.remove());
  }).catch(err => {
    console.error(err);
    document.querySelectorAll('[data-loading]').forEach(el=>el.textContent=t.error);
  });
})();
