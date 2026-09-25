(() => {
  'use strict';
  const root = location.pathname.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const lang = document.documentElement.lang === 'en' ? 'en' : 'es';
  const tr = (es,en) => lang === 'es' ? es : en;
  const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const arr = v => Array.isArray(v) ? v : [];
  const badge = s => `<span class="up-badge">${esc(s)}</span>`;
  const list = items => `<ul>${arr(items).map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`;
  const setText = (sel,val) => { const e=document.querySelector(sel); if(e)e.textContent=val; };

  fetch(root+'assets/data/concurso36-unitary-prosecutorial-theory-20260829.json',{cache:'no-store'})
    .then(r=>r.ok?r.json():Promise.reject(r.status))
    .then(d=>{
      setText('[data-baseline]',d.baseline_main_sha);
      setText('[data-denominator]',d.repository_audit?.located_discovery_denominator || '—');
      setText('[data-p0]',d.repository_audit?.p0_open_families ?? '—');
      setText('[data-p1]',d.repository_audit?.p1_open_families ?? '—');
      setText('[data-perimeter]',`${d.fixed_perimeter?.ricpe_20jul2021_262_fincas?.cam_owned||54} CAM · ${d.fixed_perimeter?.ricpe_20jul2021_262_fincas?.lpb_components||190} LPB · ${d.fixed_perimeter?.ricpe_20jul2021_262_fincas?.third_party_fincas||18} ${tr('terceros','third party')}`);

      const thesis=document.querySelector('#unitary-thesis');
      if(thesis) thesis.innerHTML=`<p>${esc(lang==='es'?d.unitary_thesis.es:d.unitary_thesis.en)}</p>`;

      const stages=document.querySelector('#prosecutorial-stages');
      if(stages) stages.innerHTML=arr(d.prosecutorial_stages).map(x=>`<article class="up-stage" id="${esc(x.id)}">
        <div class="up-stage-head"><span>${esc(x.id)} · ${esc(x.period)}</span>${badge(x.status)}</div>
        <h3>${esc(lang==='es'?x.title_es:x.title_en)}</h3>
        <p><strong>${tr('Documentado','Documented')}:</strong> ${esc(x.documented)}</p>
        <p class="up-question"><strong>${tr('Pregunta fiscal/prosecutorial','Prosecutorial question')}:</strong> ${esc(x.prosecutorial_question)}</p>
        <p class="up-counter"><strong>${tr('Contrapeso / explicación lícita','Counterweight / lawful explanation')}:</strong> ${esc(x.counterweight)}</p>
      </article>`).join('');

      const hyps=document.querySelector('#criminal-hypotheses');
      if(hyps) hyps.innerHTML=arr(d.criminal_hypothesis_tests).map(x=>`<article class="up-hyp">
        <div class="up-stage-head"><span>${esc(x.id)}</span>${badge(x.candidate_articles)}</div>
        <h3>${esc(lang==='es'?x.label_es:x.label_en)}</h3>
        <p><strong>${tr('Disparador investigativo','Investigative trigger')}:</strong> ${esc(x.trigger)}</p>
        <p><strong>${tr('Debe probarse','Must prove')}:</strong> ${esc(x.must_prove)}</p>
        <p class="up-counter"><strong>${tr('No basta','Not enough')}:</strong> ${esc(x.not_enough)}</p>
      </article>`).join('');

      const lives=document.querySelector('#parallel-lives');
      if(lives) lives.innerHTML=arr(d.parallel_lives).map((x,i)=>`<article class="up-life">
        <span>${tr('OBJETO','OBJECT')} ${i+1}</span><h3>${esc(x.object)}</h3>
        <ol>${arr(x.lives).map(v=>`<li>${esc(v)}</li>`).join('')}</ol>
      </article>`).join('');

      const judicial=document.querySelector('#judicial-balance');
      if(judicial) judicial.innerHTML=`<div class="up-two"><article><h3>${tr('Actos adversos/contrarios','Adverse/contrary acts')}</h3>${list(d.judicial_balance?.adverse_or_contrary_nodes)}</article><article><h3>${tr('Contrapesos favorables/protectores','Favourable/protective counterweights')}</h3>${list(d.judicial_balance?.favourable_or_protective_counterweights)}</article></div><div class="up-rule"><strong>${tr('Regla de integridad','Integrity rule')}.</strong> ${esc(d.judicial_balance?.rule||'')}</div>`;

      const reliance=document.querySelector('#downstream-reliance');
      if(reliance) reliance.innerHTML=`<p><strong>${tr('Documentado','Documented')}:</strong> ${esc(d.downstream_reliance_boundary?.documented||'')}</p><p><strong>${tr('No se infiere','Not inferred')}:</strong> ${esc(d.downstream_reliance_boundary?.not_inferred||'')}</p><p><strong>${tr('Test','Test')}:</strong> ${esc(d.downstream_reliance_boundary?.investigative_test||'')}</p>`;

      const gaps=document.querySelector('#unitary-gaps');
      if(gaps) gaps.innerHTML=arr(d.highest_leverage_gaps).map((x,i)=>`<li><strong>${i+1}.</strong> ${esc(x)}</li>`).join('');
      const prod=document.querySelector('#production-requests');
      if(prod) prod.innerHTML=arr(d.prosecutorial_production_requests).map((x,i)=>`<li><strong>${i+1}.</strong> ${esc(x)}</li>`).join('');

      const audit=document.querySelector('#repo-audit');
      if(audit) audit.innerHTML=`<p>${esc(lang==='es'?d.repository_audit.material_finding_es:d.repository_audit.material_finding_en)}</p><div class="up-mini-grid"><article><strong>${tr('Descubrimiento','Discovery')}</strong><span>${esc(d.repository_audit.located_discovery_denominator)}</span></article><article><strong>${tr('Índice judicial certificado','Certified court index')}</strong><span>${d.repository_audit.certified_docket?tr('Sí','Yes'):tr('No localizado','Not located')}</span></article><article><strong>P0</strong><span>${esc(d.repository_audit.p0_open_families)}</span></article><article><strong>P1</strong><span>${esc(d.repository_audit.p1_open_families)}</span></article></div>`;

      const sourceLinks=document.querySelector('#source-links');
      if(sourceLinks){
        const map=lang==='es' ? [
          ['/es/control-acreedor-cam-administracion-hecho-omision-judicial/','Control acreedor / 7 junio / AC / juez'],
          ['/es/concurso-36-2012-escritos-tratamiento-sobreextension/','Escritos / respuesta / sobreextensión'],
          ['/es/ric-private-equity-sun-park/','RICPE / capital / ayuda / título'],
          ['/es/comunidad-instrumentalizacion/actas-2011-2022/','Actas / deuda / voto / autoridad'],
          ['/es/reclamacion-caixabank-valencia/','Cadena bancaria / NPL / crédito'],
          ['/es/calificacion-concurso-36-2012-vidas-paralelas/','Calificación / vidas paralelas']
        ] : [
          ['/en/cam-creditor-control-shadow-administration-judicial-omission/','Creditor control / 7 June / IA / judge'],
          ['/en/insolvency-36-2012-filings-court-treatment-overreach/','Filings / response / overreach'],
          ['/en/ric-private-equity-sun-park/','RICPE / capital / aid / title'],
          ['/en/caixabank-valencia-claim/','Banking / NPL / claim chain'],
          ['/en/','English evidence hub']
        ];
        sourceLinks.innerHTML=map.map(([p,l])=>`<a href="${root.replace(/\/$/,'')}${p}">${esc(l)} →</a>`).join('');
      }
      document.querySelectorAll('[data-loading]').forEach(e=>e.remove());
    })
    .catch(err=>{
      console.error(err);
      document.querySelectorAll('[data-loading]').forEach(e=>e.textContent=tr('No se pudo cargar la matriz. Abra el JSON fuente.','Could not load the matrix. Open the source JSON.'));
    });
})();
