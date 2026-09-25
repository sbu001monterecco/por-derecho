(() => {
  const path = location.pathname;
  const isEs = path.includes('/es/');
  const eligible = [
    'mensaje-abierto-cgpj','open-message-cgpj','carta-abierta-ministerio-fiscal','open-letter-public-prosecution-service',
    'cnmv-ricpe-verificacion','cnmv-ricpe-verification','concurso-36-2012-laj','insolvency-36-2012-laj',
    'concurso-36-2012-magistrado-juez','insolvency-36-2012-judge','concurso-36-2012-administrador-concursal',
    'insolvency-36-2012-insolvency-administrator','concurso-36-2012-ap-seccion-4','insolvency-36-2012-ap-section-4',
    'ricpe-responsabilidad-documental','ricpe-documentary-accountability','yaiza-trazabilidad-institucional','yaiza-institutional-traceability',
    'cabildo-lanzarote-turismo-trazabilidad','cabildo-lanzarote-tourism-traceability','intervencion-general-siinf-trazabilidad',
    'intervencion-general-siinf-traceability','snca-fondos-europeos-trazabilidad','snca-eu-funds-traceability','acosta-matos-perimetro'
  ].some(s => path.includes('/' + s + '/'));
  if (!eligible || document.querySelector('[data-accountability-grammar]')) return;
  const main = document.querySelector('main');
  if (!main) return;
  const anchor = main.querySelector('section');
  if (!anchor) return;

  const style = document.createElement('style');
  style.textContent = `.aeg{background:#111f27;color:#fff;padding:1rem 0;border-top:1px solid rgba(255,255,255,.12);border-bottom:1px solid rgba(255,255,255,.12)}.aeg .aeg-title{font-size:.78rem;letter-spacing:.09em;text-transform:uppercase;font-weight:900;opacity:.78;margin:0 0 .7rem}.aeg-flow{display:grid;grid-template-columns:repeat(5,1fr);gap:.45rem;align-items:stretch}.aeg-step{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.14);border-radius:11px;padding:.7rem .75rem;font-size:.82rem;line-height:1.3}.aeg-step strong{display:block;font-size:.88rem;margin-bottom:.2rem}.aeg-note{font-size:.78rem;opacity:.82;margin:.65rem 0 0}.aeg-badges{display:flex;gap:.4rem;flex-wrap:wrap;margin-top:.65rem}.aeg-badge{font-size:.7rem;font-weight:900;letter-spacing:.04em;padding:.27rem .5rem;border-radius:999px;background:#fff;color:#13252d}@media(max-width:760px){.aeg-flow{grid-template-columns:1fr}.aeg-step{padding:.6rem .7rem}}`;
  document.head.appendChild(style);

  const box = document.createElement('section');
  box.className = 'aeg';
  box.dataset.accountabilityGrammar = 'true';
  box.innerHTML = isEs ? `<div class="shell"><p class="aeg-title">Cómo leer cualquier expediente de responsabilidad institucional</p><div class="aeg-flow"><div class="aeg-step"><strong>1 · RECIBIDO</strong>¿Existe constancia de entrada o conocimiento institucional?</div><div class="aeg-step"><strong>2 · EXAMINADO</strong>¿Qué material fue realmente leído o valorado?</div><div class="aeg-step"><strong>3 · VERIFICADO</strong>¿Qué hecho se contrastó con una fuente independiente u oficial?</div><div class="aeg-step"><strong>4 · DECIDIDO</strong>¿Qué resolvió el órgano competente y qué dejó fuera?</div><div class="aeg-step"><strong>5 · ACTUACIÓN</strong>¿Hubo corrección, remisión, preservación, investigación u otra consecuencia?</div></div><p class="aeg-note"><strong>No son sinónimos.</strong> Recibido ≠ examinado ≠ verificado ≠ decidido ≠ corregido.</p><div class="aeg-badges"><span class="aeg-badge">DOCUMENTADO</span><span class="aeg-badge">ALEGADO</span><span class="aeg-badge">INFERENCIA</span><span class="aeg-badge">ABIERTO</span><span class="aeg-badge">CORREGIDO</span></div></div>` : `<div class="shell"><p class="aeg-title">How to read any institutional-accountability record</p><div class="aeg-flow"><div class="aeg-step"><strong>1 · RECEIVED</strong>Is there evidence of institutional receipt or notice?</div><div class="aeg-step"><strong>2 · EXAMINED</strong>What material was actually read or assessed?</div><div class="aeg-step"><strong>3 · VERIFIED</strong>What fact was checked against an independent or official source?</div><div class="aeg-step"><strong>4 · DECIDED</strong>What did the competent body decide, and what did it leave outside?</div><div class="aeg-step"><strong>5 · ACTION</strong>Was there correction, referral, preservation, investigation or another consequence?</div></div><p class="aeg-note"><strong>These are not synonyms.</strong> Received ≠ examined ≠ verified ≠ decided ≠ corrected.</p><div class="aeg-badges"><span class="aeg-badge">DOCUMENTED</span><span class="aeg-badge">ALLEGED</span><span class="aeg-badge">INFERENCE</span><span class="aeg-badge">OPEN</span><span class="aeg-badge">CORRECTED</span></div></div>`;
  anchor.insertAdjacentElement('afterend', box);
})();