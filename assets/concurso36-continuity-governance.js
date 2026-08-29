(() => {
  'use strict';
  const root = location.pathname.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const lang = document.documentElement.lang === 'en' ? 'en' : 'es';
  const tr = (es,en) => lang === 'es' ? es : en;
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const text = (o, esKey='es', enKey='en') => esc(lang === 'es' ? o?.[esKey] : o?.[enKey]);
  const card = (head, body, status='') => `<article class="track">${head}${body}${status?`<footer><span class="evidence-pill">${esc(status)}</span></footer>`:''}</article>`;

  fetch(root + 'assets/data/concurso36-continuity-governance-20260829.json', {cache:'no-store'})
    .then(r => r.ok ? r.json() : Promise.reject(r.status))
    .then(d => {
      const hf = d.headline_findings || [];
      const set = (id, html) => { const el=document.getElementById(id); if(el) el.innerHTML=html; };
      set('headline-finding', text(hf[0]));
      set('definitive-correction', `<strong>${esc(tr('Corrección:','Correction:'))}</strong> ${text(hf[1])}`);
      set('amount-reconciliation', text(hf[2]));
      set('convenio-summary', text(hf[3]));

      set('notice-grid', (d.notice_protection_chain||[]).map(x => card(
        `<div class="track-top"><span>${esc(x.id)}</span><time>${esc(x.date)}</time></div><h3>${esc(x.actor)}</h3>`,
        `<p>${text(x)}</p><p class="treatment"><strong>${esc(tr('Cierre requerido','Closure required'))}:</strong> ${esc(x.closure)}</p>`,
        x.status
      )).join(''));

      const ac=d.administrator_concursal_lane||{};
      set('ac-position', text(ac,'safe_position_es','safe_position_en'));
      set('ac-law', (ac.legal_baseline_2018||[]).map(x=>`<li>${esc(x)}</li>`).join(''));
      const acQs = lang==='es' ? [
        '¿Qué verificó el AC después de tener conocimiento real el 8 de junio de 2018?',
        '¿Qué escrito, informe o comunicación remitió al Juzgado Mercantil sobre el episodio del 7 de junio y cuándo?',
        '¿Pidió instrucciones, auxilio judicial, inspección, acceso, conservación, contabilidad o medidas cautelares/protectoras?',
        '¿Qué reflejaron sus informes de liquidación sobre ocupación/uso, cerraduras/seguridad, explotación, ingresos, obras, deterioro y salidas financiadas?',
        'Si pidió o apoyó medidas de seguridad, ¿qué título y qué perímetro cubrían?',
        '¿Cómo separó activos LPB de Comunidad, Matkator y terceros y cómo cuantificó el efecto sobre masa/unidad productiva?'
      ] : [
        'What did the IA verify after having actual knowledge on 8 June 2018?',
        'What filing, report or communication did he send the Mercantile Court about the 7 June episode, and when?',
        'Did he seek directions, judicial assistance, inspection, access, preservation, accounting or protective measures?',
        'What did liquidation reports record about occupation/use, locks/security, operations, income, works, deterioration and funded exits?',
        'If he requested or supported security measures, what title and perimeter did they cover?',
        'How did he separate LPB assets from Community, Matkator and third parties and quantify the estate/productive-unit effect?'
      ];
      set('ac-questions', acQs.map(x=>`<li>${esc(x)}</li>`).join(''));

      set('definitive-body', (d.definitive_texts_lane||[]).map(x=>`<tr><td><strong>${esc(x.date)}</strong></td><td>${esc(x.event)}</td><td><span class="evidence-pill">${esc(x.status)}</span></td></tr>`).join(''));

      set('convenio-grid', (d.convenio_liquidation_lane||[]).map(x=>card(
        `<div class="track-top"><time>${esc(x.date)}</time><span>${esc(x.status)}</span></div>`,
        `<p>${text(x)}</p>`
      )).join(''));

      set('creditor-grid', (d.creditor_workout_continuity||[]).map(x=>card(
        `<div class="track-top"><span>${esc(x.period)}</span><span>${esc(x.status)}</span></div><h3>${esc(x.counterparty)}</h3>`,
        `<ul>${(x.anchors||[]).map(a=>`<li>${esc(a)}</li>`).join('')}</ul><p class="treatment"><strong>${esc(tr('Control','Control'))}:</strong> ${esc(x.audit)}</p>`
      )).join(''));

      set('plan-grid', (d.cam_plan_compliance_questions||[]).map((x,i)=>card(
        `<div class="track-top"><span>PLAN-${String(i+1).padStart(2,'0')}</span><span>${esc(tr('prueba de cumplimiento','compliance test'))}</span></div>`,
        `<p>${esc(x)}</p>`
      )).join(''));

      set('counsel-grid', (d.counsel_instruction_filing_audit||[]).map(x=>card(
        `<div class="track-top"><span>${esc(x.period)}</span><span>${esc(tr('trazabilidad','traceability'))}</span></div><h3>${esc(x.actor)}</h3>`,
        `<p><strong>${esc(tr('Conservar','Preserve'))}:</strong></p><ul>${(x.preserve||[]).map(a=>`<li>${esc(a)}</li>`).join('')}</ul><p class="treatment"><strong>${esc(tr('Tensión instrucción→acción','Instruction→action tension'))}:</strong> ${text(x,'tension_es','tension_en')}</p>`
      )).join(''));

      const governance = lang==='es' ? [
        '¿Dónde está el índice cronológico electrónico certificado y la relación oficial por pieza/sección?',
        '¿Recibió el Mercantil el exhorto ordenado el 2 mayo 2018, cuándo respondió y qué se incorporó al concurso?',
        '¿Dónde está el escrito/informe del AC sobre el 7 junio y qué protección generó?',
        '¿Dónde está el escrito que Cuatrecasas dijo haber preparado, su versión final y su recibo —o la decisión documentada de no presentarlo?',
        '¿Dónde está el acta oficial del 28 junio 2017 con quórum, constitución, asistencia, voto y resultado del convenio?',
        '¿Qué resolución, si alguna, cambió después del 8 febrero 2018 la cuantía fija y cómo se llega de 9.052.251,69 € a 13.168.082,02 €?',
        '¿Qué activos LPB estaban jurídicamente incluidos en oferta CAM, plan, mejora, suspensión, adjudicación y escritura, y qué quedó fuera?',
        '¿Cómo se reconcilian ONA, Stoneweg/Varia, Elaia/Lagune y otras salidas 2018 con el cambio de control del 7 junio y la respuesta judicial/AC?',
        'Para cada abogado: ¿qué instrucción recibió, qué redactó, qué presentó, qué no se ha localizado y qué remedio/plazo se preservó o perdió?',
        '¿Cómo se reconcilia Bankia→SAREB→Promontoria/Cerberus/Haya→CAM con cuantía, garantías, autoridad negociadora, sucesión procesal y salidas?'
      ] : [
        'Where is the certified electronic chronological index and official per-piece/section act list?',
        'Did the Mercantile Court receive the 2 May 2018 judicial-assistance request, when did it respond and what entered the insolvency record?',
        'Where is the IA filing/report about 7 June and what protection did it generate?',
        'Where is the pleading Cuatrecasas said it had prepared, its final version and receipt — or the documented decision not to file?',
        'Where is the official 28 June 2017 minute recording quorum, constitution, attendance, vote and composition outcome?',
        'What order, if any, changed the fixed amount after 8 February 2018 and how is €9,052,251.69 reconciled to €13,168,082.02?',
        'Which LPB assets were legally included in the CAM offer, plan, improvement process, suspension, adjudication and deed, and what remained outside?',
        'How are ONA, Stoneweg/Varia, Elaia/Lagune and other 2018 exits reconciled with the 7 June control change and court/IA response?',
        'For each lawyer: what instruction was received, what was drafted, what was filed, what remains unlocated and what remedy/deadline was preserved or lost?',
        'How is Bankia→SAREB→Promontoria/Cerberus/Haya→CAM reconciled with amount, security, negotiation authority, procedural succession and exits?'
      ];
      set('governance-questions', governance.map((x,i)=>`<li><strong>Q-${String(i+1).padStart(2,'0')}</strong> ${esc(x)}</li>`).join(''));
      set('master-gaps', (d.master_open_gaps||[]).map(x=>`<li>${esc(x)}</li>`).join(''));
      document.querySelectorAll('[data-loading]').forEach(el=>el.remove());
    })
    .catch(err => {
      console.error(err);
      document.querySelectorAll('[data-loading]').forEach(el=>el.textContent=tr('No se pudo cargar el registro de continuidad.','The continuity record could not be loaded.'));
    });

  fetch(root + 'assets/data/concurso36-procedural-taxonomy-judicial-ac-dual-lens-20260829.json', {cache:'no-store'})
    .then(r => r.ok ? r.json() : Promise.reject(r.status))
    .then(d => {
      const anchor = document.getElementById('textos');
      if (!anchor || document.getElementById('dual-lens-governance')) return;
      const pos = lang === 'es' ? d.declared_position.es : d.declared_position.en;
      const june = d.critical_4_june_2018_comparator || {};
      const incidents = d.verified_incidentes_concursales_located || [];
      const why = d.why_material_acts_are_not_automatically_incidents || [];
      const gate = d.definitive_text_change_gate || {};
      const dualHref = root + 'CHATGPT_START_HERE_CONCURSO36_DUAL_LENS_GOVERNANCE.md';
      const dataHref = root + 'assets/data/concurso36-procedural-taxonomy-judicial-ac-dual-lens-20260829.json';
      const html = `<section class="section alt" id="dual-lens-governance"><div class="shell">
        <p class="eyebrow">${esc(tr('DERECHO ESTRICTO + LENTE ADVERSARIAL AC/JUEZ','BLACK-LETTER LAW + ADVERSARIAL JUDGE/IA LENS'))}</p>
        <h2>${esc(tr('La alegación es acumulativa: no un solo Auto, no una sola omisión','The allegation is cumulative: not one order, not one omission'))}</h2>
        <div class="warning"><strong>${esc(tr('Posición declarada / límite probatorio.','Declared position / evidentiary boundary.'))}</strong> ${esc(pos)}</div>
        <div class="track-grid">
          ${card(`<div class="track-top"><span>DRY LAW</span><span>${esc(tr('clasificación','classification'))}</span></div><h3>${esc(tr('Primero: qué vía procesal era','First: what procedural route applied'))}</h3>`,`<p>${text(d.mandatory_dual_lens.dry_law)}</p><p class="treatment">${esc(tr('Importancia material ≠ incidente concursal.','Material importance ≠ insolvency incident.'))}</p>`)}
          ${card(`<div class="track-top"><span>ADVERSARIAL</span><span>${esc(tr('patrón','pattern'))}</span></div><h3>${esc(tr('Después: juez, AC y actores privados','Then: judge, IA and private actors'))}</h3>`,`<p>${text(d.mandatory_dual_lens.adversarial_misconduct)}</p>`)}
        </div>
        <h3>${esc(tr('4 junio 2018: comparador primario que no puede borrarse','4 June 2018: primary comparator that must remain visible'))}</h3>
        <div class="track-grid">
          ${card(`<div class="track-top"><span>08-02-2018</span><span>${esc(june['8_february_2018']?.status || '')}</span></div><h3>€9.052.251,69</h3>`,`<p>${esc(june['8_february_2018']?.operative_rule || '')}</p><p>${esc(june['8_february_2018']?.recorded_special_privilege || '')}</p>`)}
          ${card(`<div class="track-top"><span>04-06-2018</span><span>${esc(june['4_june_2018']?.status || '')}</span></div><h3>€13.165.832,36 + ${esc(tr('interés limitado por garantía','interest limited by security'))}</h3>`,`<p>${esc(june['4_june_2018']?.source_mechanics || '')}</p><p class="treatment"><strong>${esc(tr('Posición Gil/Aweswell','Gil/Aweswell position'))}:</strong> ${esc(june['4_june_2018']?.user_position || '')}</p>`)}
        </div>
        <h3>${esc(tr('Por qué no metemos todo en “incidente concursal”','Why we do not put every material act into “insolvency incident”'))}</h3>
        <div class="table-wrap"><table><thead><tr><th>${esc(tr('Acto','Act'))}</th><th>${esc(tr('Clase correcta','Correct class'))}</th><th>${esc(tr('Razón','Reason'))}</th></tr></thead><tbody>${why.map(x=>`<tr><td><strong>${esc(x.act)}</strong></td><td>${esc(x.classification)}</td><td>${esc(x.reason)}</td></tr>`).join('')}</tbody></table></div>
        <h3>${esc(tr('Incidentes concursales primarios localizados','Primary verified insolvency incidents located'))}</h3>
        <div class="track-grid">${incidents.map(x=>card(`<div class="track-top"><span>${esc(x.piece)}</span><time>${esc(x.date_decision)}</time></div><h3>${esc(x.claimant)} → ${esc(x.defendant || x.defendants)}</h3>`,`<p><strong>${esc(x.caption)}</strong></p><p>${esc(x.object)}</p><p class="treatment">${esc(x.result)}</p>`,x.status)).join('')}</div>
        <div class="callout"><strong class="big">${esc(tr('Gate obligatorio del texto definitivo','Mandatory definitive-text gate'))}</strong><p>${esc(lang==='es' ? gate.rule_es : gate.rule_en)}</p><ol class="gaps">${(gate.required_fields||[]).map(x=>`<li>${esc(x)}</li>`).join('')}</ol></div>
        <div class="boundary"><h2>${esc(tr('Gobernanza permanente para la investigación','Permanent investigation governance'))}</h2><p>${esc(tr('Las quejas CGPJ y demás denuncias se enlazan como historia de alegaciones, no como prueba de culpabilidad. Cada nuevo documento debe compararse con el patrón alegado y con la explicación jurídica contraria.','CGPJ complaints and other complaints are linked as allegation history, not proof of guilt. Every new document must be tested against the alleged pattern and the competing lawful explanation.'))}</p><div class="links"><a href="${dualHref}">${esc(tr('Protocolo agente / prompt','Agent protocol / prompt'))}</a><a href="${dataHref}">${esc(tr('Datos máquina','Machine data'))}</a></div></div>
      </div></section>`;
      anchor.insertAdjacentHTML('afterend', html);
    })
    .catch(err => console.error('dual-lens governance', err));
})();