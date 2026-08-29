(() => {
  'use strict';
  const root = document.querySelector('[data-c36-court-record]');
  if (!root) return;
  const lang = root.dataset.lang === 'en' ? 'en' : 'es';
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
  const missing = lang === 'en' ? 'NOT LOCATED / NOT RESOLVED IN THIS CONTROLLED RECORD' : 'NO LOCALIZADO / NO RESUELTO EN ESTE REGISTRO CONTROLADO';
  const labels = lang === 'en' ? {
    actors:'^ ALL ACTORS/PARTIES', source:'^ SOURCE', authority:'^ CLAIMED AUTHORITY', status:'^ PROCEDURAL STATUS', happened:'^ WHAT HAPPENED', proves:'^ WHAT THE RECORD PROVES', alleged:'^ WHAT IS ALLEGED', criminal:'^ CRIMINAL / FORENSIC SIGNIFICANCE', contrary:'^ CONTRARY EVIDENCE', gap:'^ MISSING EVIDENCE', links:'^ CROSS-LINKS'
  } : {
    actors:'^ ALL PARTIES / TODAS LAS PARTES', source:'^ SOURCE / FUENTE', authority:'^ CLAIMED AUTHORITY / AUTORIDAD ALEGADA', status:'^ PROCEDURAL STATUS / ESTADO PROCESAL', happened:'^ WHAT HAPPENED / QUÉ OCURRIÓ', proves:'^ WHAT THE RECORD PROVES / QUÉ PRUEBA EL REGISTRO', alleged:'^ WHAT IS ALLEGED / QUÉ SE ALEGA', criminal:'^ CRIMINAL / FORENSIC SIGNIFICANCE / SIGNIFICADO PENAL-FORENSE', contrary:'^ CONTRARY EVIDENCE / PRUEBA CONTRARIA', gap:'^ MISSING EVIDENCE / PRUEBA FALTANTE', links:'^ CROSS-LINKS / ENLACES'
  };
  const actorText = r => {
    const values = [r.party, r.claimant, r.defendant, r.issuer, r.signed_by, ...(r.parties || []), ...(r.actor_refs || [])].filter(Boolean);
    return [...new Set(values.map(String))].join(' · ') || missing;
  };
  const sourceText = r => [r.verification, r.lexnet_id && `LexNET ${r.lexnet_id}`, r.lexnet_sent_id && `LexNET ${r.lexnet_sent_id}`, r.electronic_document_id && `Doc ${r.electronic_document_id}`, r.registry_csv && `CSV ${r.registry_csv}`].filter(Boolean).join(' · ') || missing;
  const authorityText = r => {
    if (r.record_class === 'party_filing') return lang === 'en' ? 'Party/counsel procedural capacity reflected by the filing; underlying representation/power remains governed by the primary instrument.' : 'Capacidad procesal de parte/letrado reflejada por el escrito; la representación/poder subyacente queda gobernada por el instrumento primario.';
    if ((r.record_class || '').startsWith('court_')) return lang === 'en' ? 'Judicial capacity reflected by the signed court instrument; scope is limited to that act.' : 'Capacidad judicial reflejada por el instrumento firmado; su alcance queda limitado a ese acto.';
    if ((r.record_class || '').startsWith('laj_')) return lang === 'en' ? 'LAJ procedural-office capacity reflected by the signed act; scope is limited to that act.' : 'Capacidad procesal de LAJ reflejada por el acto firmado; alcance limitado a ese acto.';
    if (r.record_class === 'administrator_report') return lang === 'en' ? 'Insolvency Administrator capacity; exact authority/effect remains act-specific.' : 'Capacidad de Administrador Concursal; autoridad/efecto exactos son específicos del acto.';
    return missing;
  };
  const collect = async () => {
    const urls = ['concurso36-court-record-reconstruction-v1.json','concurso36-court-record-reconstruction-2022-appellate-supplement.json','concurso36-court-record-reconstruction-gapclose2-20260829.json'];
    const [d,s,g] = await Promise.all(urls.map(u => fetch(`../../assets/data/${u}`, {cache:'no-store'}).then(r => r.ok ? r.json() : null).catch(() => null)));
    const out = [];
    (d?.verified_families || []).forEach(f => out.push(...(f.records || [])));
    if (s?.records) out.push(...s.records);
    if (g?.append_records) out.push(...g.append_records);
    (g?.additional_families || []).forEach(f => out.push(...(f.records || [])));
    return out;
  };
  const render = async () => {
    if (root.dataset.caretOverlayDone === '1') return;
    const cards = [...root.querySelectorAll('.c36-record')];
    if (!cards.length) return;
    const records = await collect();
    const used = new Set();
    cards.forEach(card => {
      if (card.querySelector('[data-c36-caret]')) return;
      const title = card.querySelector('h3')?.textContent?.trim() || '';
      const kicker = card.querySelector('.c36-kicker')?.textContent || '';
      const date = (kicker.match(/\d{4}-\d{2}-\d{2}/) || [])[0] || '';
      let r = records.find(x => !used.has(x) && String(x.title || x.summary || x.id || '').trim() === title && (!date || x.date === date));
      if (!r) r = records.find(x => !used.has(x) && String(x.title || x.summary || x.id || '').trim() === title);
      if (!r) r = {date, title, summary:title}; else used.add(r);
      const what = r.operative_effect || r.summary || r.request_summary || r.reasoning_summary || r.title || missing;
      const proves = r.verification || (lang === 'en' ? 'The located record proves this procedural act/representation occurred to the extent stated; it does not prove every allegation within it.' : 'El registro localizado prueba que este acto/representación procesal ocurrió en el alcance indicado; no prueba todas las alegaciones contenidas.');
      const alleged = r.record_class === 'party_filing' ? (lang === 'en' ? 'The filing contains party allegations/requests; they are not converted into findings by filing or receipt.' : 'El escrito contiene alegaciones/peticiones de parte; la presentación o recepción no las convierte en hallazgos.') : (lang === 'en' ? 'No additional criminal allegation is inferred from this record alone.' : 'No se infiere una alegación penal adicional de este registro por sí solo.');
      const criminal = lang === 'en' ? 'Any criminal/prosecutorial theory requires actor-specific elements, knowledge/intent where required, reliance/effect, prejudice and contrary evidence. This record alone is not a finding of criminal misconduct.' : 'Toda teoría penal/fiscal exige elementos actor por actor, conocimiento/intención cuando proceda, confianza/efecto, perjuicio y prueba contraria. Este registro por sí solo no declara conducta penal.';
      const contrary = r.proof_limit || r.reasoning_summary || (lang === 'en' ? 'Must be reconciled with the opposing filings, decision challenged, review/appeal, finality and implementation chain.' : 'Debe conciliarse con escritos contrarios, resolución impugnada, recurso/revisión, firmeza e implementación.');
      const gap = r.open_point || r.open_link || (lang === 'en' ? 'Any unlocated power, receipt, service, response, finality or implementation step remains an evidence gap rather than proof of nonexistence.' : 'Todo poder, recibo, traslado, respuesta, firmeza o implementación no localizado sigue siendo vacío probatorio, no prueba de inexistencia.');
      const box = document.createElement('details');
      box.setAttribute('data-c36-caret','20260829');
      box.style.marginTop = '.8rem';
      box.innerHTML = `<summary style="cursor:pointer;font-weight:900">^ ${lang === 'en' ? 'INCIDENT CONTROL' : 'INCIDENT / CONTROL DE INCIDENTE'}</summary><div style="margin-top:.65rem;border-left:5px solid #b7832f;padding-left:.85rem;font-size:.9rem;line-height:1.45"><p><strong>^ DATE / FECHA</strong> — ${esc(r.date || date || missing)}</p><p><strong>^ INCIDENT</strong> — ${esc(r.title || r.summary || r.id || title || missing)}</p><p><strong>${esc(labels.actors)}</strong> — ${esc(actorText(r))}</p><p><strong>${esc(labels.source)}</strong> — ${esc(sourceText(r))}</p><p><strong>${esc(labels.authority)}</strong> — ${esc(authorityText(r))}</p><p><strong>${esc(labels.status)}</strong> — ${esc(r.response_taxonomy || r.status || r.record_class || missing)}</p><p><strong>${esc(labels.happened)}</strong> — ${esc(what)}</p><p><strong>${esc(labels.proves)}</strong> — ${esc(proves)}</p><p><strong>${esc(labels.alleged)}</strong> — ${esc(alleged)}</p><p><strong>${esc(labels.criminal)}</strong> — ${esc(criminal)}</p><p><strong>${esc(labels.contrary)}</strong> — ${esc(contrary)}</p><p><strong>${esc(labels.gap)}</strong> — ${esc(gap)}</p><p><strong>${esc(labels.links)}</strong> — <a href="${lang === 'en' ? '../insolvency-36-2012-community-authority/' : '../concurso-36-2012-autoridad-comunidad/'}">${lang === 'en' ? 'Authority matrix' : 'Matriz autoridad'}</a> · <a href="${lang === 'en' ? '../insolvency-36-2012-arrecife-mercantile-bridge/' : '../concurso-36-2012-puente-arrecife-mercantil/'}">Arrecife ↔ Concurso</a></p></div>`;
      card.appendChild(box);
    });
    root.dataset.caretOverlayDone = '1';
  };
  const observer = new MutationObserver(() => { if (root.querySelector('.c36-record')) { render(); observer.disconnect(); } });
  observer.observe(root,{childList:true,subtree:true});
  render();
})();
