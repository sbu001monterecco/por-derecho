(() => {
  'use strict';
  const root = location.pathname.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const lang = document.documentElement.lang === 'en' ? 'en' : 'es';
  const tr = (es,en) => lang === 'es' ? es : en;
  const t = lang === 'es' ? {
    loading:'Cargando el registro canónico…', error:'No se pudo cargar el registro canónico. Use los enlaces de datos directos.',
    noDate:'Fecha no cerrada', source:'Fuente pública controlada',
    supplement:'Escritos primarios recuperados fuera del denominador',
    parallel:'Seis vidas paralelas del mismo activo / derecho',
    ric:'RIC / RICPE — comparación temporal del perímetro',
    judicial:'Cadena judicial 2021–2022: conocimiento → decisión → título',
    failures:'Fallos/omisiones alegados: qué puede decirse hoy con seguridad',
    proved:'Documentado', gap:'Aún no cerrado', next:'Cierre requerido', status:'Estado público seguro'
  } : {
    loading:'Loading canonical record…', error:'The canonical record could not be loaded. Use the direct data links.',
    noDate:'Date not closed', source:'Controlled public source',
    supplement:'Recovered primary filings outside the denominator',
    parallel:'Six parallel lives of the same asset / right',
    ric:'RIC / RICPE — time-specific perimeter comparison',
    judicial:'2021–2022 judicial chain: notice → decision → title',
    failures:'Alleged failures/omissions: what can safely be said today',
    proved:'Documented', gap:'Not yet closed', next:'Closure required', status:'Safe public status'
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

  const insertJump = () => {
    const nav = document.querySelector('.jump .shell');
    if (!nav) return;
    const links = lang === 'es'
      ? [['#recuperados','Recuperados'],['#vidas-paralelas','Vidas paralelas'],['#ricpe','RIC/RICPE'],['#cadena-judicial','Cadena judicial'],['#fallos-matriz','Fallos/omisiones']]
      : [['#recovered','Recovered'],['#parallel-lives','Parallel lives'],['#ricpe','RIC/RICPE'],['#judicial-chain','Judicial chain'],['#failure-matrix','Failures/omissions']];
    links.forEach(([href,label]) => {
      if (nav.querySelector(`a[href="${href}"]`)) return;
      const a = document.createElement('a'); a.href=href; a.textContent=label; nav.appendChild(a);
    });
  };

  const renderSupplement = multi => {
    const anchor = document.querySelector(lang==='es'?'#escritos':'#filings');
    if (!anchor || document.querySelector('#recovered-primary-section')) return;
    const rows = (multi.recovered_primary_supplement||[]).map(r=>`<tr>
      <td><strong>${date(r.date)}</strong><small>${esc(r.id)}</small></td>
      <td><strong>${esc(r.document)}</strong></td>
      <td>${esc(r.actor)}</td>
      <td>${esc(lang==='es'?r.relevance_es:r.relevance_en)}<small>${esc(r.verification)}</small></td>
      <td><span class="evidence-pill">${esc(r.canonical_status)}</span></td>
    </tr>`).join('');
    const id = lang==='es'?'recuperados':'recovered';
    const sec = document.createElement('section');
    sec.className='section alt'; sec.id='recovered-primary-section';
    sec.innerHTML=`<div class="shell"><span id="${id}"></span><p class="eyebrow">${esc(t.supplement)}</p>
      <h2>${esc(tr('El denominador de 34 escritos ya no es suficiente','The former 34-filing denominator is no longer sufficient'))}</h2>
      <p class="lede">${esc(multi.display?.recovered_intro?.[lang]||'')}</p>
      <div class="warning"><strong>${esc(tr('Corrección de continuidad.','Continuity correction.'))}</strong>
      ${esc(tr('Estos escritos se muestran como suplemento primario recuperado hasta que se dedupliquen e incorporen formalmente al catálogo canónico. No se presentan como el denominador judicial certificado.','These filings are shown as a recovered-primary supplement until they are deduplicated and formally incorporated into the canonical catalogue. They are not presented as the certified court denominator.'))}</div>
      <div class="table-wrap"><table><thead><tr><th>${esc(tr('Fecha / ID','Date / ID'))}</th><th>${esc(tr('Escrito','Filing'))}</th><th>${esc(tr('Actor','Actor'))}</th><th>${esc(tr('Relevancia / verificación','Relevance / verification'))}</th><th>${esc(tr('Estado','Status'))}</th></tr></thead><tbody>${rows}</tbody></table></div></div>`;
    anchor.insertAdjacentElement('afterend',sec);
  };

  const renderParallel = multi => {
    const anchor = document.querySelector(lang==='es'?'#danos':'#harm');
    if (!anchor || document.querySelector('#parallel-lives-section')) return;
    const cards=(multi.parallel_asset_lives||[]).map((r,i)=>{
      const asset=lang==='es'?r.asset_es:r.asset_en;
      const lives=lang==='es'?r.lives_es:r.lives_en;
      return `<article class="track"><div class="track-top"><span>ASSET-LIFE ${i+1}</span><span>${esc(tr('6 vidas','6 lives'))}</span></div>
      <h3>${esc(asset)}</h3><ol>${(lives||[]).map((x,j)=>`<li><strong>${j+1}.</strong> ${esc(x)}</li>`).join('')}</ol></article>`;
    }).join('');
    const id=lang==='es'?'vidas-paralelas':'parallel-lives';
    const sec=document.createElement('section'); sec.className='section'; sec.id='parallel-lives-section';
    sec.innerHTML=`<div class="shell"><span id="${id}"></span><p class="eyebrow">${esc(t.parallel)}</p>
      <h2>${esc(tr('El activo no tuvo una sola vida jurídica o económica','The asset did not have a single legal or economic life'))}</h2>
      <p class="lede">${esc(multi.display?.parallel_intro?.[lang]||'')}</p>
      <div class="track-grid">${cards}</div></div>`;
    anchor.insertAdjacentElement('afterend',sec);
  };

  const renderRic = multi => {
    const anchor=document.querySelector('#parallel-lives-section');
    if(!anchor || document.querySelector('#ricpe-section')) return;
    const cps=(multi.representation_checkpoints||[]).map(cp=>`<article class="track">
      <div class="track-top"><time>${esc(cp.date)}</time><span>${esc(cp.status)}</span></div>
      <h3>${esc(cp.source)}</h3><p>${esc(lang==='es'?cp.summary_es:cp.summary_en)}</p></article>`).join('');
    const sec=document.createElement('section'); sec.className='section alt'; sec.id='ricpe-section';
    sec.innerHTML=`<div class="shell"><span id="ricpe"></span><p class="eyebrow">${esc(t.ric)}</p>
      <h2>${esc(tr('2020: proyecto de 12 M€ · 2021: perímetro certificado y condicionado','2020: €12m project · 2021: certified, conditional perimeter'))}</h2>
      <p class="lede">${esc(multi.display?.ric_intro?.[lang]||'')}</p>
      <div class="warning"><strong>${esc(tr('Punto crítico de reconciliación.','Critical reconciliation point.'))}</strong> ${esc(tr('El webinar de 11 noviembre 2020 presenta Sun Park como proyecto de 220 apartamentos y 12 M€; la certificación RICPE de 20 julio 2021 fija 262 fincas y desglosa 54 CAM + 190 activos/componentes LPB + 18 terceros, indicando que el proyecto seguía preliminar y condicionado a adquirir los activos LPB.','The 11 November 2020 webinar presents Sun Park as a 220-apartment, €12m project; the 20 July 2021 RICPE certification fixes a 262-finca perimeter split into 54 CAM + 190 LPB assets/components + 18 third-party fincas, and says the project remained preliminary and conditional on acquisition of the LPB assets.'))}</div>
      <div class="track-grid">${cps}</div>
      <p class="lede"><strong>${esc(tr('Lectura controlada:','Controlled reading:'))}</strong> ${esc(tr('la divergencia entre una presentación inversora y el perímetro posteriormente certificado es una cuestión objetiva que debe reconciliarse con Registro, hipotecas, firmeza de adjudicación, posesión y financiación. No es, por sí sola, una conclusión de falsedad o fraude.','the divergence between an investor presentation and the later certified perimeter is an objective question to reconcile with Registry title, mortgages, adjudication finality, possession and financing. It is not, by itself, a finding of falsity or fraud.'))}</p></div>`;
    anchor.insertAdjacentElement('afterend',sec);
  };

  const renderJudicialChain = judicial => {
    const anchor=document.querySelector('#ricpe-section');
    if(!anchor || document.querySelector('#judicial-chain-section')) return;
    const id=lang==='es'?'cadena-judicial':'judicial-chain';
    const correction=judicial.primary_correction||{};
    const cards=(judicial.chain||[]).map(x=>`<article class="track">
      <div class="track-top"><span>${esc(x.step)}</span><time>${esc(x.date)}</time></div>
      <h3>${esc(x.actor)}</h3>
      <p class="treatment"><strong>${esc(tr('Acto / respuesta','Act / response'))}:</strong> ${esc(lang==='es'?x.event_es:x.event_en)}</p>
      <p><strong>${esc(tr('Efecto','Effect'))}:</strong> ${esc(lang==='es'?x.effect_es:x.effect_en)}</p>
      <p><strong>${esc(tr('Límite','Limit'))}:</strong> ${esc(lang==='es'?x.limit_es:x.limit_en)}</p>
      <footer><span class="evidence-pill">${esc(x.status)}</span></footer>
    </article>`).join('');
    const tests=(judicial.failure_tests||[]).map(x=>`<article class="track">
      <div class="track-top"><span>${esc(x.id)}</span><span>${esc(tr('prueba de fallo/omisión','failure/omission test'))}</span></div>
      <h3>${esc(lang==='es'?x.title_es:x.title_en)}</h3>
      <p><strong>${esc(t.proved)}:</strong> ${esc(lang==='es'?x.proved_es:x.proved_en)}</p>
      <p><strong>${esc(tr('Pregunta de cierre','Closure question'))}:</strong> ${esc(lang==='es'?x.question_es:x.question_en)}</p>
    </article>`).join('');
    const sec=document.createElement('section'); sec.className='section'; sec.id='judicial-chain-section';
    sec.innerHTML=`<div class="shell"><span id="${id}"></span><p class="eyebrow">${esc(t.judicial)}</p>
      <h2>${esc(tr('Del aviso formal a la escritura: ya no es una acusación genérica','From formal notice to deed: no longer a generic accusation'))}</h2>
      <p class="lede">${esc(lang==='es'?judicial.reading_rule_es:judicial.reading_rule_en)}</p>
      <div class="warning"><strong>${esc(lang==='es'?correction.status_es:correction.status_en)}</strong> ${esc(lang==='es'?correction.safe_conclusion_es:correction.safe_conclusion_en)}</div>
      <div class="track-grid">${cards}</div>
      <h3>${esc(tr('Cinco pruebas de respuesta, protección y coherencia','Five response, protection and coherence tests'))}</h3>
      <div class="track-grid">${tests}</div></div>`;
    anchor.insertAdjacentElement('afterend',sec);
  };

  const renderFailures = multi => {
    const anchor=document.querySelector('#judicial-chain-section') || document.querySelector('#ricpe-section');
    if(!anchor || document.querySelector('#failure-matrix-section')) return;
    const cards=(multi.judicial_failure_matrix||[]).map(r=>`<article class="track">
      <h3>${esc(lang==='es'?r.issue_es:r.issue_en)}</h3>
      <p class="treatment"><strong>${esc(t.status)}:</strong> ${esc(lang==='es'?r.status_es:r.status_en)}</p>
      <p><strong>${esc(t.proved)}:</strong> ${esc(lang==='es'?r.proved_es:r.proved_en)}</p>
      <p><strong>${esc(t.gap)}:</strong> ${esc(lang==='es'?r.gap_es:r.gap_en)}</p>
      <p><strong>${esc(t.next)}:</strong> ${esc(lang==='es'?r.next_es:r.next_en)}</p></article>`).join('');
    const id=lang==='es'?'fallos-matriz':'failure-matrix';
    const sec=document.createElement('section'); sec.className='section alt'; sec.id='failure-matrix-section';
    sec.innerHTML=`<div class="shell"><span id="${id}"></span><p class="eyebrow">${esc(t.failures)}</p>
      <h2>${esc(tr('No una acusación genérica al juez: pruebas de respuesta y protección','Not a generic accusation against the judge: response-and-protection tests'))}</h2>
      <p class="lede">${esc(tr('La formulación más fuerte que resiste auditoría separa resolución judicial adversa, cuestión expresamente puesta ante el Juzgado, contradicción verificable, respuesta parcial, autoridad no localizada y seguimiento protector/contable no localizado. La responsabilidad personal exige un análisis jurídico y probatorio separado.','The strongest audit-resistant formulation separates adverse judicial ruling, matters expressly put before the court, verifiable contradiction, partial response, authority not located and protective/accounting follow-up not located. Personal responsibility requires separate legal and evidential analysis.'))}</p><div class="track-grid">${cards}</div></div>`;
    anchor.insertAdjacentElement('afterend',sec);
  };

  Promise.all([
    fetch(root+'assets/data/concurso36-complete-record-v1.json',{cache:'no-store'}).then(r=>r.ok?r.json():Promise.reject(r.status)),
    fetch(root+'assets/data/concurso36-court-treatment-overreach-matrix-20260829.json',{cache:'no-store'}).then(r=>r.ok?r.json():Promise.reject(r.status)),
    fetch(root+'assets/data/concurso36-multitrack-asset-lives-20260829.json',{cache:'no-store'}).then(r=>r.ok?r.json():Promise.reject(r.status)),
    fetch(root+'assets/data/concurso36-judicial-chain-202110-202204.json',{cache:'no-store'}).then(r=>r.ok?r.json():Promise.reject(r.status))
  ]).then(([record,matrix,multi,judicial]) => {
    const records = Array.isArray(record.records) ? record.records : [];
    const filings = records.filter(r => r.record_class === 'party_filing').sort((a,b)=>(a.date||'9999').localeCompare(b.date||'9999'));
    const judicialRecords = records.filter(r => ['judicial_act','laj_or_court_office_act','judicial_or_laj_type_unresolved'].includes(r.record_class));
    document.querySelectorAll('[data-filing-count]').forEach(el=>el.textContent=filings.length);
    document.querySelectorAll('[data-judicial-count]').forEach(el=>el.textContent=judicialRecords.length);
    document.querySelectorAll('[data-cutoff]').forEach(el=>el.textContent=record.cutoff || matrix.cutoff || '2026-08-29');

    const body = document.querySelector('#filing-body');
    const input = document.querySelector('#filing-filter');
    const renderFilings = q => {
      const needle = (q||'').trim().toLowerCase();
      const shown = needle ? filings.filter(r=>searchable(r).includes(needle)) : filings;
      if (body) body.innerHTML = shown.map(r=>`<tr>
        <td><strong>${date(r.date)}</strong><small>${esc(r.canonical_id)}</small></td>
        <td><strong>${esc(r.title_or_function || r.document_type || '')}</strong><small>${esc(r.document_type || '')}</small></td>
        <td>${esc(r.issuer_or_actor || '—')}</td>
        <td>${esc(r.direct_effect_or_proposition || '—')}<small>${esc(r.conditions_or_limits || '')}</small>${linkFor(r)}</td>
        <td><span class="evidence-pill">${esc(r.evidence_label || r.complete_copy_status || '—')}</span></td>
      </tr>`).join('') || `<tr><td colspan="5">0</td></tr>`;
      const visible = document.querySelector('[data-visible-count]'); if (visible) visible.textContent=shown.length;
    };
    renderFilings('');
    if (input) input.addEventListener('input',()=>renderFilings(input.value));

    const tracks = document.querySelector('#treatment-tracks');
    if (tracks) tracks.innerHTML = (matrix.tracks||[]).map(x=>`<article class="track" id="${esc(x.id)}">
      <div class="track-top"><span>${esc(x.id)}</span><time>${esc(x.date_or_period)}</time></div>
      <h3>${esc(x.issue)}</h3>
      ${x.documented_court_effect?`<p><strong>${tr('Efecto judicial documentado','Documented court effect')}:</strong> ${esc(x.documented_court_effect)}</p>`:''}
      ${x.documented_or_reported_event?`<p><strong>${tr('Hecho documentado o registrado','Documented or recorded event')}:</strong> ${esc(x.documented_or_reported_event)}</p>`:''}
      ${x.court_treatment_status?`<p class="treatment"><strong>${tr('Tratamiento / estado','Treatment / status')}:</strong> ${esc(x.court_treatment_status)}</p>`:''}
      <p><strong>${tr('Límite','Limit')}:</strong> ${esc(x.limit || '—')}</p>
      <p><strong>${tr('Relevancia','Relevance')}:</strong> ${esc(x.position_or_consequence || '—')}</p>
      <footer><span class="evidence-pill">${esc(x.evidence_status || '')}</span>${(x.source_records||[]).length?` <code>${esc(x.source_records.join(' · '))}</code>`:''}</footer>
    </article>`).join('');

    const gaps = document.querySelector('#gap-list');
    if (gaps) {
      const merged=[...(matrix.gap_closure||[]),...(multi.gap_closure||[]),...(judicial.closure_requests||[])];
      gaps.innerHTML = [...new Set(merged)].map(x=>`<li>${esc(x)}</li>`).join('');
    }
    insertJump();
    renderSupplement(multi);
    renderParallel(multi);
    renderRic(multi);
    renderJudicialChain(judicial);
    renderFailures(multi);
    document.querySelectorAll('[data-loading]').forEach(el=>el.remove());
  }).catch(err => {
    console.error(err);
    document.querySelectorAll('[data-loading]').forEach(el=>el.textContent=t.error);
  });
})();
