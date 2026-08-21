/* Project Sun Rock privacy-first public-record assistant. No chat history is persisted by this client. */
(() => {
  if (document.querySelector('[data-psr-ai-launcher]')) return;
  const path = location.pathname.toLowerCase();
  if (path.includes('/admin/')) return;
  const isEn = (document.documentElement.lang || '').toLowerCase().startsWith('en') || path.includes('/en/');
  const copy = isEn ? {
    launch:'Ask the record', title:'Public-record AI assistant', subtitle:'AI-generated answers · source constrained',
    intro:'Ask about the public Project Sun Rock / Por Derecho record by text or voice. This is an AI system, not a person, lawyer or protected reporting channel.',
    privacy:'Your question is processed to generate the answer. Project Sun Rock does not save the question, transcript, answer or raw audio in its analytics store. Do not submit confidential, privileged, special-category or unnecessary personal data.',
    analytics:'Optional: allow privacy-minimised usage analytics. Only daily aggregates are kept — never the question, transcript, answer, IP address or a persistent visitor ID.',
    interest:'Your broad interest (optional)', general:'General visitor', hospitality:'Hospitality / property', legal:'Legal / finance / professional', media:'Media / research', public:'Public / institutional', connected:'Directly connected to the documented matters', prefer:'Prefer not to say',
    placeholder:'Ask a question about the public record…', send:'Send', mic:'Voice', stop:'Stop', ready:'Ready', thinking:'Reading the public record…', recording:'Recording', unavailable:'The AI backend is not active on this host yet.', error:'I could not answer that safely. Please try again or use the site search.', transcript:'I heard:', sources:'Sources used', listen:'Listen to answer', privacyLink:'AI privacy notice', fullPrivacy:'Full privacy notice', analyticsLabel:'Help improve the assistant with aggregate analytics',
    scope:'This assistant answers only from public pages on this site. If the sources do not support an answer, it should say so.'
  } : {
    launch:'Preguntar al expediente', title:'Asistente IA del registro público', subtitle:'Respuestas generadas por IA · limitadas a fuentes',
    intro:'Pregunte por texto o voz sobre el registro público de Project Sun Rock / Por Derecho. Es un sistema de IA, no una persona, abogado ni canal protegido de denuncias.',
    privacy:'Su pregunta se trata para generar la respuesta. Project Sun Rock no guarda la pregunta, transcripción, respuesta ni audio original en su almacén de analítica. No envíe información confidencial, privilegiada, categorías especiales ni datos personales innecesarios.',
    analytics:'Opcional: permita analítica de uso minimizada. Solo se conservan agregados diarios; nunca la pregunta, transcripción, respuesta, dirección IP ni un identificador persistente del visitante.',
    interest:'Su interés general (opcional)', general:'Visitante general', hospitality:'Hotelería / inmobiliario', legal:'Legal / finanzas / profesional', media:'Medios / investigación', public:'Público / institucional', connected:'Conexión directa con los asuntos documentados', prefer:'Prefiero no decirlo',
    placeholder:'Pregunte sobre el registro público…', send:'Enviar', mic:'Voz', stop:'Parar', ready:'Preparado', thinking:'Leyendo el registro público…', recording:'Grabando', unavailable:'El backend de IA todavía no está activo en este host.', error:'No he podido responder con seguridad. Inténtelo de nuevo o utilice la búsqueda del sitio.', transcript:'He entendido:', sources:'Fuentes utilizadas', listen:'Escuchar respuesta', privacyLink:'Privacidad del asistente IA', fullPrivacy:'Aviso completo de privacidad', analyticsLabel:'Ayudar a mejorar el asistente con analítica agregada',
    scope:'Este asistente responde únicamente desde páginas públicas de este sitio. Si las fuentes no bastan, debe indicarlo.'
  };

  const prefix = location.pathname.includes('/por-derecho/') ? '/por-derecho' : '';
  const privacyHref = isEn ? `${prefix}/en/ai-assistant-privacy/` : `${prefix}/es/asistente-ia-privacidad/`;
  const fullPrivacyHref = isEn ? `${prefix}/en/legal-privacy/` : `${prefix}/es/aviso-legal-privacidad/`;
  const cfg = window.PSR_CHAT_CONFIG || {};
  const apiBase = String(cfg.apiBase || '').replace(/\/$/, '');
  const endpoint = `${apiBase}/api/psr-chat`;
  const analyticsEndpoint = `${apiBase}/api/psr-chat-analytics`;

  const launcher = document.createElement('button');
  launcher.type = 'button'; launcher.className = 'psr-ai-launcher'; launcher.dataset.psrAiLauncher = '20260821';
  launcher.setAttribute('aria-expanded','false'); launcher.innerHTML = `<span aria-hidden="true">AI</span><span>${copy.launch}</span>`;
  document.body.appendChild(launcher);

  const panel = document.createElement('section');
  panel.className = 'psr-ai-panel'; panel.dataset.open = 'false'; panel.setAttribute('aria-label', copy.title);
  panel.innerHTML = `
    <div class="psr-ai-head"><div><strong>${copy.title}</strong><small>${copy.subtitle}</small></div><button type="button" aria-label="Close">×</button></div>
    <div class="psr-ai-notice">
      <p><strong>${copy.intro}</strong></p><p>${copy.privacy}</p><p>${copy.scope}</p>
      <p><a href="${privacyHref}">${copy.privacyLink} →</a> · <a href="${fullPrivacyHref}">${copy.fullPrivacy} →</a></p>
      <label><input type="checkbox" data-analytics> <span>${copy.analyticsLabel}</span></label>
      <div data-analytics-details class="psr-ai-hidden"><p>${copy.analytics}</p><select class="psr-ai-interest" data-interest aria-label="${copy.interest}"><option value="prefer-not-to-say">${copy.interest}: ${copy.prefer}</option><option value="general">${copy.general}</option><option value="hospitality">${copy.hospitality}</option><option value="legal-finance">${copy.legal}</option><option value="media-research">${copy.media}</option><option value="public-institutional">${copy.public}</option><option value="directly-connected">${copy.connected}</option></select></div>
    </div>
    <div class="psr-ai-log" data-log aria-live="polite"></div>
    <form class="psr-ai-compose"><textarea maxlength="2400" data-input placeholder="${copy.placeholder}" aria-label="${copy.placeholder}"></textarea><div class="psr-ai-controls"><button type="button" class="psr-ai-mic" data-mic>🎙 ${copy.mic}</button><button type="submit" class="send" data-send>${copy.send}</button></div><p class="psr-ai-status" data-status>${copy.ready}</p></form>`;
  document.body.appendChild(panel);

  const closeBtn = panel.querySelector('.psr-ai-head button');
  const log = panel.querySelector('[data-log]');
  const form = panel.querySelector('form');
  const input = panel.querySelector('[data-input]');
  const mic = panel.querySelector('[data-mic]');
  const send = panel.querySelector('[data-send]');
  const status = panel.querySelector('[data-status]');
  const analytics = panel.querySelector('[data-analytics]');
  const analyticsDetails = panel.querySelector('[data-analytics-details]');
  const interest = panel.querySelector('[data-interest]');
  let recorder = null, chunks = [], stream = null, recordTimer = null, remaining = 60, lastAnswer = '';

  const setOpen = open => { panel.dataset.open = open ? 'true' : 'false'; launcher.setAttribute('aria-expanded', String(open)); if (open) setTimeout(() => input.focus(), 50); };
  launcher.addEventListener('click', () => setOpen(panel.dataset.open !== 'true'));
  closeBtn.addEventListener('click', () => setOpen(false));
  analytics.addEventListener('change', () => analyticsDetails.classList.toggle('psr-ai-hidden', !analytics.checked));

  const msg = (text, role='assistant') => { const div=document.createElement('div'); div.className=`psr-ai-msg ${role}`; div.textContent=text; log.appendChild(div); log.scrollTop=log.scrollHeight; return div; };
  const setBusy = busy => { input.disabled=busy; send.disabled=busy; mic.disabled=busy && !recorder; };
  const arrayBufferToBase64 = buffer => { let binary=''; const bytes=new Uint8Array(buffer); const step=0x8000; for(let i=0;i<bytes.length;i+=step) binary += String.fromCharCode(...bytes.subarray(i,i+step)); return btoa(binary); };
  const readAnswer = () => { if (!lastAnswer || !('speechSynthesis' in window)) return; speechSynthesis.cancel(); const u=new SpeechSynthesisUtterance(lastAnswer); u.lang=isEn?'en-GB':'es-ES'; speechSynthesis.speak(u); };

  async function health() {
    try { const r=await fetch(endpoint,{headers:{accept:'application/json'}}); return r.ok; } catch { return false; }
  }

  async function submitAnalytics(result, inputType) {
    if (!analytics.checked) return;
    try {
      await fetch(analyticsEndpoint,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({analyticsConsent:true,consentVersion:'20260821a',inputType,lang:isEn?'en':'es',topic:result.topic,pagePath:location.pathname,interest:interest.value,status:result.status||'error',sourceCount:Array.isArray(result.sources)?result.sources.length:0}),keepalive:true});
    } catch {}
  }

  const containsObviousPrivateIdentifier = (value) => {
    const v = String(value || '');
    return /\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b/i.test(v) || /\+\d[\d\s().-]{7,}\d/.test(v) || /\b(?:[XYZ]\d{7,8}|\d{8})[A-Z]\b/i.test(v) || /\b[A-Z]{2}\d{2}(?:[ ]?\d){11,30}\b/i.test(v);
  };

  async function ask({ text='', audioBlob=null } = {}) {
    const cleaned = String(text || '').trim();
    if (!cleaned && !audioBlob) return;
    if (cleaned && containsObviousPrivateIdentifier(cleaned)) {
      msg(isEn ? 'Please remove email addresses, telephone numbers, identity numbers or bank-account details before sending the question.' : 'Elimine direcciones de correo, teléfonos, números de identidad o datos bancarios antes de enviar la pregunta.', 'system');
      return;
    }
    if (cleaned) msg(cleaned,'user'); else msg(isEn?'[Voice question]':'[Pregunta por voz]','user');
    setBusy(true); status.textContent=copy.thinking;
    try {
      if (!(await health())) throw new Error('backend_unavailable');
      let audioBase64='', audioMime='';
      if (audioBlob) { if (audioBlob.size > 3_500_000) throw new Error('audio_too_large'); audioBase64=arrayBufferToBase64(await audioBlob.arrayBuffer()); audioMime=audioBlob.type || 'audio/webm'; }
      const response=await fetch(endpoint,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({text:cleaned,audioBase64,audioMime,lang:isEn?'en':'es',pagePath:location.pathname})});
      const result=await response.json().catch(()=>({}));
      if (!response.ok) throw new Error(result.error || 'request_failed');
      if (result.transcript) { const t=document.createElement('div'); t.className='psr-ai-transcript'; t.textContent=`${copy.transcript} ${result.transcript}`; log.appendChild(t); }
      lastAnswer=String(result.answer || copy.error); msg(lastAnswer,'assistant');
      if ('speechSynthesis' in window && lastAnswer) { const b=document.createElement('button'); b.type='button'; b.className='psr-ai-listen'; b.textContent=`🔊 ${copy.listen}`; b.addEventListener('click',readAnswer); log.appendChild(b); }
      if (Array.isArray(result.sources) && result.sources.length) { const wrap=document.createElement('div'); wrap.className='psr-ai-sources'; result.sources.forEach((s,i)=>{ const a=document.createElement('a'); a.href=s.url; a.target='_blank'; a.rel='noopener'; a.textContent=`[${i+1}] ${s.title}`; wrap.appendChild(a); }); log.appendChild(wrap); }
      await submitAnalytics(result, audioBlob?'audio':'text');
      status.textContent=copy.ready; log.scrollTop=log.scrollHeight;
    } catch (e) {
      msg(e?.message==='backend_unavailable'?copy.unavailable:copy.error,'system'); status.textContent=copy.ready;
    } finally { setBusy(false); input.value=''; input.focus(); }
  }

  form.addEventListener('submit', e => { e.preventDefault(); ask({text:input.value}); });
  input.addEventListener('keydown', e => { if (e.key==='Enter' && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); } });

  async function stopRecording(sendIt=true) {
    if (!recorder) return;
    clearInterval(recordTimer); recordTimer=null;
    const active=recorder; recorder=null;
    active.addEventListener('stop', async () => { const blob=new Blob(chunks,{type:active.mimeType || 'audio/webm'}); chunks=[]; if(sendIt && blob.size) await ask({audioBlob:blob}); }, {once:true});
    if (active.state!=='inactive') active.stop();
    mic.dataset.recording='false'; mic.textContent=`🎙 ${copy.mic}`; status.textContent=copy.ready;
    if (stream) { stream.getTracks().forEach(t=>t.stop()); stream=null; }
  }

  mic.addEventListener('click', async () => {
    if (recorder) { await stopRecording(true); return; }
    if (!navigator.mediaDevices?.getUserMedia || !window.MediaRecorder) { msg(isEn?'Voice input is not supported by this browser.':'Este navegador no admite entrada de voz.','system'); return; }
    try {
      stream=await navigator.mediaDevices.getUserMedia({audio:true,video:false});
      const preferred=['audio/webm;codecs=opus','audio/webm','audio/ogg;codecs=opus'].find(t=>MediaRecorder.isTypeSupported?.(t));
      recorder=new MediaRecorder(stream, preferred?{mimeType:preferred}:undefined); chunks=[]; remaining=60;
      recorder.ondataavailable=e=>{if(e.data?.size) chunks.push(e.data)}; recorder.start(500);
      mic.dataset.recording='true'; mic.textContent=`■ ${copy.stop}`; status.textContent=`${copy.recording} · ${remaining}s`;
      recordTimer=setInterval(()=>{ remaining-=1; status.textContent=`${copy.recording} · ${remaining}s`; if(remaining<=0) stopRecording(true); },1000);
    } catch { msg(isEn?'Microphone permission was not granted. You can still type your question.':'No se concedió permiso al micrófono. Puede escribir la pregunta.','system'); if(stream){stream.getTracks().forEach(t=>t.stop());stream=null;} }
  });
})();
