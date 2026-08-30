(() => {
  'use strict';
  const path = window.location.pathname.replace(/\/+$/, '/') || '/';
  const lang = document.documentElement.lang === 'en' ? 'en' : 'es';
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
  const missing = lang === 'en' ? 'NOT LOCATED / NOT RESOLVED IN THIS CONTROLLED RECORD' : 'NO LOCALIZADO / NO RESUELTO EN ESTE REGISTRO CONTROLADO';
  const labels = lang === 'en' ? {
    actors:'^ ALL ACTORS/PARTIES', source:'^ SOURCE', authority:'^ CLAIMED AUTHORITY', status:'^ PROCEDURAL STATUS', happened:'^ WHAT HAPPENED', proves:'^ WHAT THE RECORD PROVES', alleged:'^ WHAT IS ALLEGED', criminal:'^ CRIMINAL / FORENSIC SIGNIFICANCE', contrary:'^ CONTRARY EVIDENCE', gap:'^ MISSING EVIDENCE', links:'^ CROSS-LINKS'
  } : {
    actors:'^ ALL PARTIES / TODAS LAS PARTES', source:'^ SOURCE / FUENTE', authority:'^ CLAIMED AUTHORITY / AUTORIDAD ALEGADA', status:'^ PROCEDURAL STATUS / ESTADO PROCESAL', happened:'^ WHAT HAPPENED / QUÉ OCURRIÓ', proves:'^ WHAT THE RECORD PROVES / QUÉ PRUEBA EL REGISTRO', alleged:'^ WHAT IS ALLEGED / QUÉ SE ALEGA', criminal:'^ CRIMINAL / FORENSIC SIGNIFICANCE / SIGNIFICADO PENAL-FORENSE', contrary:'^ CONTRARY EVIDENCE / PRUEBA CONTRARIA', gap:'^ MISSING EVIDENCE / PRUEBA FALTANTE', links:'^ CROSS-LINKS / ENLACES'
  };
  const t = (en, es) => lang === 'en' ? en : es;
  const authorityHref = lang === 'en' ? '../insolvency-36-2012-community-authority/' : '../concurso-36-2012-autoridad-comunidad/';
  const bridgeHref = lang === 'en' ? '../insolvency-36-2012-arrecife-mercantile-bridge/' : '../concurso-36-2012-puente-arrecife-mercantil/';

  const makeBox = meta => {
    const box = document.createElement('details');
    box.setAttribute('data-c36-caret','20260830');
    box.style.marginTop = '.8rem';
    box.innerHTML = `<summary style="cursor:pointer;font-weight:900">^ ${lang === 'en' ? 'INCIDENT CONTROL' : 'INCIDENT / CONTROL DE INCIDENTE'}</summary><div style="margin-top:.65rem;border-left:5px solid #b7832f;padding-left:.85rem;font-size:.9rem;line-height:1.45"><p><strong>^ DATE / FECHA</strong> — ${esc(meta.date || missing)}</p><p><strong>^ INCIDENT</strong> — ${esc(meta.incident || missing)}</p><p><strong>${esc(labels.actors)}</strong> — ${esc(meta.actors || missing)}</p><p><strong>${esc(labels.source)}</strong> — ${esc(meta.source || missing)}</p><p><strong>${esc(labels.authority)}</strong> — ${esc(meta.authority || missing)}</p><p><strong>${esc(labels.status)}</strong> — ${esc(meta.status || missing)}</p><p><strong>${esc(labels.happened)}</strong> — ${esc(meta.happened || missing)}</p><p><strong>${esc(labels.proves)}</strong> — ${esc(meta.proves || missing)}</p><p><strong>${esc(labels.alleged)}</strong> — ${esc(meta.alleged || missing)}</p><p><strong>${esc(labels.criminal)}</strong> — ${esc(meta.criminal || missing)}</p><p><strong>${esc(labels.contrary)}</strong> — ${esc(meta.contrary || missing)}</p><p><strong>${esc(labels.gap)}</strong> — ${esc(meta.gap || missing)}</p><p><strong>${esc(labels.links)}</strong> — <a href="${authorityHref}">${lang === 'en' ? 'Authority matrix' : 'Matriz autoridad'}</a> · <a href="${bridgeHref}">Arrecife ↔ Concurso</a></p></div>`;
    return box;
  };

  const actorText = r => {
    const values = [r.party, r.claimant, r.defendant, r.issuer, r.signed_by, ...(r.parties || []), ...(r.actor_refs || [])].filter(Boolean);
    return [...new Set(values.map(String))].join(' · ') || missing;
  };
  const sourceText = r => [r.verification, r.lexnet_id && `LexNET ${r.lexnet_id}`, r.lexnet_sent_id && `LexNET ${r.lexnet_sent_id}`, r.electronic_document_id && `Doc ${r.electronic_document_id}`, r.registry_csv && `CSV ${r.registry_csv}`].filter(Boolean).join(' · ') || missing;
  const authorityText = r => {
    if (r.record_class === 'party_filing') return t('Party/counsel procedural capacity reflected by the filing; underlying representation/power remains governed by the primary instrument.','Capacidad procesal de parte/letrado reflejada por el escrito; la representación/poder subyacente queda gobernada por el instrumento primario.');
    if ((r.record_class || '').startsWith('court_')) return t('Judicial capacity reflected by the signed court instrument; scope is limited to that act.','Capacidad judicial reflejada por el instrumento firmado; su alcance queda limitado a ese acto.');
    if ((r.record_class || '').startsWith('laj_')) return t('LAJ procedural-office capacity reflected by the signed act; scope is limited to that act.','Capacidad procesal de LAJ reflejada por el acto firmado; alcance limitado a ese acto.');
    if (r.record_class === 'administrator_report') return t('Insolvency Administrator capacity; exact authority/effect remains act-specific.','Capacidad de Administrador Concursal; autoridad/efecto exactos son específicos del acto.');
    return missing;
  };

  const collectCourtRecords = async () => {
    const urls = ['concurso36-court-record-reconstruction-v1.json','concurso36-court-record-reconstruction-2022-appellate-supplement.json','concurso36-court-record-reconstruction-gapclose2-20260829.json'];
    const [d,s,g] = await Promise.all(urls.map(u => fetch(`../../assets/data/${u}`, {cache:'no-store'}).then(r => r.ok ? r.json() : null).catch(() => null)));
    const out = [];
    (d?.verified_families || []).forEach(f => out.push(...(f.records || [])));
    if (s?.records) out.push(...s.records);
    if (g?.append_records) out.push(...g.append_records);
    (g?.additional_families || []).forEach(f => out.push(...(f.records || [])));
    return out;
  };

  const renderCourtRecord = async () => {
    const root = document.querySelector('[data-c36-court-record]');
    if (!root || root.dataset.caretOverlayDone === '1') return;
    const cards = [...root.querySelectorAll('.c36-record')];
    if (!cards.length) return;
    const records = await collectCourtRecords();
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
      const proves = r.verification || t('The located record proves this procedural act/representation occurred to the extent stated; it does not prove every allegation within it.','El registro localizado prueba que este acto/representación procesal ocurrió en el alcance indicado; no prueba todas las alegaciones contenidas.');
      const alleged = r.record_class === 'party_filing' ? t('The filing contains party allegations/requests; they are not converted into findings by filing or receipt.','El escrito contiene alegaciones/peticiones de parte; la presentación o recepción no las convierte en hallazgos.') : t('No additional criminal allegation is inferred from this record alone.','No se infiere una alegación penal adicional de este registro por sí solo.');
      const criminal = t('Any criminal/prosecutorial theory requires actor-specific elements, knowledge/intent where required, reliance/effect, prejudice and contrary evidence. This record alone is not a finding of criminal misconduct.','Toda teoría penal/fiscal exige elementos actor por actor, conocimiento/intención cuando proceda, confianza/efecto, perjuicio y prueba contraria. Este registro por sí solo no declara conducta penal.');
      const contrary = r.proof_limit || r.reasoning_summary || t('Must be reconciled with the opposing filings, decision challenged, review/appeal, finality and implementation chain.','Debe conciliarse con escritos contrarios, resolución impugnada, recurso/revisión, firmeza e implementación.');
      const gap = r.open_point || r.open_link || t('Any unlocated power, receipt, service, response, finality or implementation step remains an evidence gap rather than proof of nonexistence.','Todo poder, recibo, traslado, respuesta, firmeza o implementación no localizado sigue siendo vacío probatorio, no prueba de inexistencia.');
      card.appendChild(makeBox({date:r.date || date, incident:r.title || r.summary || r.id || title, actors:actorText(r), source:sourceText(r), authority:authorityText(r), status:r.response_taxonomy || r.status || r.record_class, happened:what, proves, alleged, criminal, contrary, gap}));
    });
    root.dataset.caretOverlayDone = '1';
  };

  const bridgeMetaEn = [
    {actors:'Arrecife criminal court / Judge Jerónimo Alonso Herrero; Mercantile Court nº1 as addressee',source:'2-May-2018 judicial-assistance record; later Arrecife receipt/Auto controls response existence',authority:'Judicial-assistance / exhorto capacity; exact initiating act governs scope',status:'PRE-TAKEOVER JUDICIAL-ASSISTANCE EVENT',proves:'The exhorto predated 7 June and a Mercantile response was later received.',alleged:'The underlying criminal track included allegations concerning Mercantile conduct; the exhorto is not itself a criminal finding.',contrary:'Mercantile did respond; the record therefore does not support a no-response/ignored inference.',gap:'Actual Mercantile response, annexes, preparation date and full scope.'},
    {actors:'Affected parties; alleged private actors; Insolvency Administrator and legal advisers as recipients where source proves receipt',source:'7-June contemporaneous criminal/protection communications and takeover dossier; actor attribution remains source-specific',authority:'Any private authority for security, access or control must be proved incident-by-incident',status:'ALLEGED MATERIAL-CONTROL / TAKEOVER EVENT',proves:'The controlled record proves allegations were made and urgent protection was sought; it does not by itself adjudicate a seizure.',alleged:'Takeover/seizure by force; alleged interference with LPB/estate and wider hotel rights.',contrary:'Security/common-area/individual-owner explanations and any lawful authority must be tested against the physical perimeter and instructions.',gap:'Exact instructions, Community resolution/power, payer/security contract, key/access chain, inventory and complete actor list.'},
    {actors:'Juan Tomás Parrilla Suárez; Francisco de Borja Rodríguez-Batllori Laffitte (Insolvency Administrator)',source:'8-June contemporaneous report beginning “He llamado a Borja…” and underlying communication chain',authority:'IA office for estate protection/administration; any Community/security premise requires its own source',status:'ACTUAL IA CONTACT / KNOWLEDGE CHECKPOINT',proves:'A direct IA contact and reported IA account existed by 8 June.',alleged:'The evidence is relied upon in support of allegations of later validation/enablement or failure to protect; those propositions require further proof.',contrary:'The IA account and any claimed Community/owner security rationale must be weighed on its own documents.',gap:'IA-authored report, verification, filing, protective request, accounting and all pre/post-event communications.'},
    {actors:'Gil Marer as declarant; advisers/insolvency actors only where the underlying correspondence identifies them',source:'10-June declaration/correspondence concerning the historical Article 176 conclusion route',authority:'Historical Ley Concursal route; exact procedural standing and filing vehicle remain source-governed',status:'DECLARED INTENTION / PROCEDURAL ROUTE',proves:'The record supports a declared conclusion-route intention, not a completed court filing or granted conclusion.',alleged:'Gil alleges the later route was frustrated in the wider 7-June/funded-exit sequence.',contrary:'Any lawful reason the route was unavailable, changed, abandoned or superseded must be tested.',gap:'Exact intended filing, instructions, final draft, filing receipt and court treatment.'},
    {actors:'Mercantile Court nº1; Arrecife criminal court as recipient',source:'Arrecife record of receipt on 11 June; 13-June Auto joining the response',authority:'Judicial response to prior exhorto',status:'RESPONSE EXISTENCE PROVED / CONTENT MISSING',proves:'A Mercantile response existed and reached Arrecife by 11 June.',alleged:'No proposition about the response content or its treatment of 7 June is established.',contrary:'The response predates or may have been prepared before full post-7-June information; content cannot be inferred.',gap:'The actual response, annexes, preparation/signature date and service/transmission metadata.'},
    {actors:'Arrecife criminal court / Judge Jerónimo Alonso Herrero; DP 1132/2018 procedural actors as identified by the primary Auto',source:'13-June-2018 Arrecife Auto',authority:'Judicial authority in DP 1132/2018',status:'AUTO JOINS MERCANTILE RESPONSE',proves:'The response was joined to DP 1132/2018, correcting any earlier no-response inference.',alleged:'The joinder does not establish the truth of any allegation contained in the underlying materials.',contrary:'The primary Auto and response content control; neither should be enlarged by repository inference.',gap:'Complete response/annexes and downstream criminal-proceeding treatment.'},
    {actors:'Daniel Irigoyen; Mercantile judge; Insolvency Administrator',source:'13-June funded-exit correspondence/meeting evidence; exact institutional minute remains source-governed',authority:'Prospective funded-exit / restructuring engagement; judicial and IA roles must remain distinct',status:'FUNDED-EXIT MEETING',proves:'The controlled record supports that the meeting occurred in the funded-exit chronology.',alleged:'The affected party relies on the sequence in alleging frustration of a funded exit after 7 June.',contrary:'A meeting does not prove agreement, approval, causation, obstruction or criminal intent.',gap:'Agenda, attendees, contemporaneous notes, documents presented, response and decision/effect.'},
    {actors:'Client/Aweswell-LPB side; Cuatrecasas; Rosa Gual and other counsel only as the underlying communications identify them',source:'13-June client/counsel communications recording that Mercantile should be informed and an escrito had been drafted',authority:'Counsel mandate/procedural representation; exact filing authority and client identity remain instrument-specific',status:'INSTRUCTION → DRAFT → FORMALISATION GAP',proves:'Counsel agreed Mercantile should be informed and a protective pleading was reported drafted.',alleged:'Any allegation of non-filing, professional failure or intentional frustration remains unresolved without the formalisation chain.',contrary:'The pleading may have been filed or a documented tactical decision may explain timing; absence of the receipt is not proof of non-filing.',gap:'Final pleading, LexNET receipt/court stamp, DIOR, service, judicial treatment or documented decision not to file.'}
  ];
  const bridgeMetaEs = [
    {actors:'Juzgado penal de Arrecife / juez Jerónimo Alonso Herrero; Juzgado Mercantil nº1 como destinatario',source:'Registro de auxilio judicial de 2-mayo-2018; recepción/Auto de Arrecife controla la existencia de respuesta',authority:'Capacidad de auxilio judicial / exhorto; el acto iniciador exacto gobierna su alcance',status:'EVENTO DE AUXILIO JUDICIAL PREVIO AL 7-JUNIO',proves:'El exhorto fue anterior al 7 junio y posteriormente se recibió respuesta del Mercantil.',alleged:'La vía penal contenía alegaciones relativas a la actuación mercantil; el exhorto no es por sí mismo hallazgo penal.',contrary:'Mercantil sí respondió; no procede inferir ausencia de respuesta/ignorancia.',gap:'Respuesta Mercantil real, anexos, fecha de preparación y alcance íntegro.'},
    {actors:'Partes afectadas; actores privados alegados; AC y asesores como receptores solo donde la fuente acredita recepción',source:'Comunicaciones penales/protectoras contemporáneas de 7 junio y dossier de toma; atribución actor por actor',authority:'Toda autoridad privada para seguridad, acceso o control debe probarse incidente por incidente',status:'EVENTO ALEGADO DE CONTROL MATERIAL / TOMA',proves:'El registro prueba que se formularon alegaciones y se pidió protección urgente; no adjudica por sí solo una toma.',alleged:'Toma/apoderamiento por fuerza; interferencia alegada con LPB/masa y derechos del hotel.',contrary:'Deben probarse y contrastarse explicaciones de seguridad, zonas comunes o derechos de propietarios individuales.',gap:'Instrucciones exactas, acuerdo/poder Comunidad, pagador/contrato de seguridad, llaves/acceso, inventario y lista completa de actores.'},
    {actors:'Juan Tomás Parrilla Suárez; Francisco de Borja Rodríguez-Batllori Laffitte (Administrador Concursal)',source:'Relato contemporáneo de 8 junio “He llamado a Borja…” y cadena subyacente',authority:'Oficio AC para protección/administración de masa; cualquier premisa Comunidad/seguridad requiere fuente propia',status:'CONTACTO / CONOCIMIENTO REAL AC',proves:'Existía contacto directo con el AC y relato de su posición el 8 junio.',alleged:'La prueba se invoca para alegar validación/habilitación posterior o falta de protección; requiere prueba adicional.',contrary:'La explicación del AC y toda justificación de seguridad/propiedad deben ponderarse documentalmente.',gap:'Informe AC, verificación, escrito, petición protectora, contabilidad y comunicaciones pre/post evento.'},
    {actors:'Gil Marer como declarante; asesores/actores concursales solo cuando la correspondencia los identifica',source:'Declaración/correspondencia de 10 junio sobre la vía histórica del artículo 176',authority:'Vía histórica de Ley Concursal; legitimación y vehículo procesal exactos quedan gobernados por fuente',status:'INTENCIÓN DECLARADA / VÍA PROCESAL',proves:'Se sostiene una intención declarada de conclusión, no un escrito presentado ni una conclusión acordada.',alleged:'Gil alega frustración posterior de esa vía dentro de la secuencia 7-junio/salida financiada.',contrary:'Debe examinarse toda razón lícita de indisponibilidad, cambio, abandono o sustitución de la vía.',gap:'Escrito previsto, instrucciones, borrador final, recibo y tratamiento judicial.'},
    {actors:'Juzgado Mercantil nº1; Juzgado de Arrecife como receptor',source:'Registro de recepción 11 junio; Auto 13 junio incorporando la respuesta',authority:'Respuesta judicial al exhorto previo',status:'EXISTENCIA DE RESPUESTA PROBADA / CONTENIDO FALTANTE',proves:'Existió respuesta Mercantil y llegó a Arrecife el 11 junio.',alleged:'No queda establecida ninguna proposición sobre su contenido o tratamiento del 7 junio.',contrary:'No puede inferirse contenido; pudo prepararse antes de disponer de información completa posterior al 7 junio.',gap:'Respuesta, anexos, fecha de preparación/firma y metadatos de transmisión.'},
    {actors:'Juzgado penal de Arrecife / juez Jerónimo Alonso Herrero; actores procesales de DP 1132/2018 según el Auto primario',source:'Auto Arrecife de 13-junio-2018',authority:'Autoridad judicial en DP 1132/2018',status:'AUTO INCORPORA RESPUESTA MERCANTIL',proves:'La respuesta fue incorporada a DP 1132/2018 y corrige cualquier inferencia previa de no respuesta.',alleged:'La incorporación no prueba la veracidad de las alegaciones contenidas en los materiales.',contrary:'El Auto y la respuesta primaria gobiernan; no deben ampliarse por inferencia del repositorio.',gap:'Respuesta/anexos completos y tratamiento posterior en la causa penal.'},
    {actors:'Daniel Irigoyen; juez mercantil; Administrador Concursal',source:'Correspondencia/evidencia de reunión de salida financiada de 13 junio; acta institucional exacta pendiente',authority:'Interlocución sobre salida financiada/reestructuración; roles del juez y AC deben mantenerse separados',status:'REUNIÓN DE SALIDA FINANCIADA',proves:'El registro controlado sostiene que la reunión ocurrió en la cronología de salida financiada.',alleged:'La parte afectada invoca la secuencia para alegar frustración de una salida financiada posterior al 7 junio.',contrary:'Una reunión no prueba acuerdo, aprobación, causalidad, obstrucción ni intención penal.',gap:'Agenda, asistentes, notas, documentos presentados, respuesta y decisión/efecto.'},
    {actors:'Cliente/perímetro Aweswell-LPB; Cuatrecasas; Rosa Gual y otros letrados solo según comunicaciones subyacentes',source:'Comunicaciones cliente/letrados de 13 junio: debía informarse al Mercantil y se dijo que el escrito estaba preparado',authority:'Mandato/representación letrada; autoridad exacta de presentación e identidad del cliente son específicas del instrumento',status:'INSTRUCCIÓN → BORRADOR → GAP DE FORMALIZACIÓN',proves:'Los letrados aceptaron que debía informarse al Mercantil y se reportó un escrito protector redactado.',alleged:'Toda alegación de no presentación, fallo profesional o frustración intencional sigue abierta sin la cadena de formalización.',contrary:'El escrito pudo presentarse o existir decisión táctica documentada; no localizar recibo no prueba no presentación.',gap:'Escrito final, recibo LexNET/sello, DIOR, traslado, tratamiento judicial o decisión documentada de no presentar.'}
  ];

  const renderBridge = () => {
    const isBridge = path.endsWith('/en/insolvency-36-2012-arrecife-mercantile-bridge/') || path.endsWith('/es/concurso-36-2012-puente-arrecife-mercantil/');
    if (!isBridge) return;
    const metas = lang === 'en' ? bridgeMetaEn : bridgeMetaEs;
    [...document.querySelectorAll('.timeline .incident')].forEach((card, i) => {
      if (card.querySelector('[data-c36-caret]')) return;
      const meta = metas[i] || {};
      const date = card.querySelector('.date')?.textContent?.trim() || '';
      const incident = card.querySelector('h3')?.textContent?.trim() || '';
      const happened = [...card.querySelectorAll('p')].map(p => p.textContent.trim()).filter(Boolean).join(' ');
      card.appendChild(makeBox({...meta,date,incident,happened}));
    });
  };

  const renderContinuityTracks = () => {
    const isContinuity = path.endsWith('/en/insolvency-36-2012-continuity-governance-7-june/') || path.endsWith('/es/concurso-36-2012-continuidad-gobernanza-7-junio/');
    if (!isContinuity) return;
    const selectors = ['#notice-grid .track','#convenio-grid .track','#creditor-grid .track','#counsel-grid .track'];
    document.querySelectorAll(selectors.join(',')).forEach(card => {
      if (card.querySelector('[data-c36-caret]')) return;
      const top = [...card.querySelectorAll('.track-top span,.track-top time')].map(x => x.textContent.trim()).filter(Boolean);
      const date = card.querySelector('time')?.textContent?.trim() || top.find(x => /\d{4}|\d{1,2}[ -][A-ZÁÉÍÓÚ]/i.test(x)) || missing;
      const incident = card.querySelector('h3')?.textContent?.trim() || card.querySelector('p')?.textContent?.trim() || missing;
      const actors = card.querySelector('h3')?.textContent?.trim() || missing;
      const happened = [...card.querySelectorAll('p,li')].map(x => x.textContent.trim()).filter(Boolean).join(' ');
      const status = card.querySelector('.evidence-pill')?.textContent?.trim() || top.join(' · ') || missing;
      const treatment = card.querySelector('.treatment')?.textContent?.trim() || missing;
      card.appendChild(makeBox({date,incident,actors,source:'assets/data/concurso36-continuity-governance-20260829.json and linked primary/controlled records',authority:t('Exact authority/capacity remains source- and actor-specific; no Community, creditor, owner, counsel or institutional capacity is inferred from a label alone.','La autoridad/capacidad exacta es específica de fuente y actor; no se infiere capacidad de Comunidad, acreedor, propietario, letrado o institución por la etiqueta sola.'),status,happened,proves:t('This card preserves the controlled event/checkpoint to the stated evidential level; it does not prove every allegation or legal conclusion associated with it.','Esta tarjeta conserva el evento/hito controlado al nivel probatorio indicado; no prueba toda alegación o conclusión jurídica asociada.'),alleged:t('Any allegation remains attributed to the party/source that advanced it and must be tested independently.','Toda alegación permanece atribuida a la parte/fuente que la formuló y debe probarse independientemente.'),criminal:t('Criminal/prosecutorial relevance requires act, actor, deception/authority issue where alleged, knowledge or intent where required, reliance/effect, prejudice, contrary evidence and statutory-element testing.','La relevancia penal/fiscal exige acto, actor, engaño/problema de autoridad cuando se alegue, conocimiento o intención cuando proceda, confianza/efecto, perjuicio, prueba contraria y contraste con elementos típicos.'),contrary:t('Read the primary record, opposing explanation, court/IA treatment and later implementation before drawing an inference.','Debe leerse el registro primario, explicación contraria, tratamiento judicial/AC e implementación posterior antes de inferir.'),gap:treatment !== missing ? treatment : t('Any unlocated filing, power, receipt, response, finality or implementation step remains an evidence gap, not proof of nonexistence.','Todo escrito, poder, recibo, respuesta, firmeza o implementación no localizado sigue siendo vacío probatorio, no prueba de inexistencia.')}));
    });
  };

  const renderAll = () => {
    renderCourtRecord();
    renderBridge();
    renderContinuityTracks();
  };
  const observer = new MutationObserver(() => renderAll());
  observer.observe(document.documentElement,{childList:true,subtree:true});
  renderAll();
  window.setTimeout(renderAll, 500);
  window.setTimeout(renderAll, 1500);
})();