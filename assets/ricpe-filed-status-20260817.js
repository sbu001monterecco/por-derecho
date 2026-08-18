(() => {
  const currentScript = document.currentScript;
  const isEn = /\/en\//.test(location.pathname);

  const apply = () => {
    const status = document.querySelector('[data-ricpe-prefiling-status]');
    if (status) {
      status.innerHTML = isEn
        ? '<div class="shell"><p class="eyebrow">FORMAL COMMUNICATION STATUS · 17 AUGUST 2026</p><h2>RICPE Ethical Channel submission corroborated by native platform email.</h2><p>Gil Marer, writing from San Cristóbal de La Laguna, submitted a formal communication through the RICPE Ethical Channel on 17 August 2026. The final platform screen and a native platform email timestamped 22:51:17 UTC corroborate submission and assignment of a private follow-up code.</p><p class="warn"><strong>Current controlled status:</strong> filed/submitted and platform acknowledgment are established. Admission, investigation, conflict-screening outcome, preservation measures, Board treatment and merits are not yet established. A contemporaneous Gmail record preserves a digitally signed 22-page PDF, SHA-256 <code>b455075ceda7841471ef5f4ebfbb784ccd00357439aa8bf282e736fe4757832c</code>, whose cryptographic signature validates; exact byte identity with the channel attachment remains pending platform metadata.</p><p><strong>Status grammar:</strong> prepared ≠ signed ≠ filed ≠ received ≠ admitted ≠ examined ≠ decided. Access credentials remain private. Any later CNMV or other-authority transmission will be recorded separately.</p></div>'
        : '<div class="shell"><p class="eyebrow">ESTADO DE LA COMUNICACIÓN FORMAL · 17 AGOSTO 2026</p><h2>Presentación por el Canal Ético de RICPE corroborada por correo nativo de plataforma.</h2><p>Gil Marer, desde San Cristóbal de La Laguna, presentó una comunicación formal por el Canal Ético de RICPE el 17 de agosto de 2026. La pantalla final y un correo nativo de la plataforma de las 22:51:17 UTC corroboran la presentación y la asignación de un código privado de seguimiento.</p><p class="warn"><strong>Estado controlado actual:</strong> constan presentación y acuse de plataforma. No constan todavía admisión, investigación, resultado del control de conflictos, medidas de preservación, tratamiento por el Consejo ni fondo. Un registro Gmail contemporáneo conserva un PDF firmado de 22 páginas, SHA-256 <code>b455075ceda7841471ef5f4ebfbb784ccd00357439aa8bf282e736fe4757832c</code>, cuya firma criptográfica resulta válida; la identidad byte a byte con el adjunto del Canal permanece pendiente de metadatos de plataforma.</p><p><strong>Gramática de estado:</strong> preparado ≠ firmado ≠ presentado ≠ recibido ≠ admitido ≠ examinado ≠ decidido. Las credenciales permanecen privadas. Toda remisión posterior a CNMV u otra autoridad se registrará por separado.</p></div>';
    }

    const update = document.querySelector('#ricpe-formal-prefiling-17aug');
    if (update) {
      update.innerHTML = isEn
        ? '<div class="update-meta"><span class="new">Filed</span><span>Ethical Channel</span><span>Native email corroboration</span></div><h3>RICPE Ethical Channel filing corroborated by platform email</h3><p>Submission on 17 August 2026 is corroborated by the final platform screen and a native platform email at 22:51:17 UTC. A contemporaneous sender-controlled Gmail record also preserves a digitally signed 22-page PDF with valid cryptographic signature and SHA-256 <code>b455075ceda7841471ef5f4ebfbb784ccd00357439aa8bf282e736fe4757832c</code>.</p><p><strong>Evidence boundary:</strong> exact byte identity between that recovered signed PDF and the channel attachment remains open. Admission, investigation, conflict review, preservation measures, Board treatment and merits are not established.</p><div class="update-actions"><a class="button" href="../ricpe-documentary-accountability/#formal-communication-17aug">Current RICPE status →</a></div>'
        : '<div class="update-meta"><span class="new">Presentada</span><span>Canal Ético</span><span>Corroboración por correo nativo</span></div><h3>Presentación por Canal Ético corroborada por correo de plataforma</h3><p>La presentación de 17 de agosto de 2026 queda corroborada por la pantalla final y por un correo nativo de plataforma de las 22:51:17 UTC. Un registro Gmail contemporáneo del remitente conserva además un PDF firmado de 22 páginas, con firma criptográfica válida y SHA-256 <code>b455075ceda7841471ef5f4ebfbb784ccd00357439aa8bf282e736fe4757832c</code>.</p><p><strong>Límite probatorio:</strong> la identidad byte a byte entre ese PDF firmado recuperado y el adjunto exacto del Canal permanece abierta. No constan todavía admisión, investigación, control de conflictos, preservación, tratamiento del Consejo ni fondo.</p><div class="update-actions"><a class="button" href="../ricpe-responsabilidad-documental/#comunicacion-formal-17ago">Estado actual RICPE →</a></div>';
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => setTimeout(apply, 0), { once: true });
  else setTimeout(apply, 0);
  setTimeout(apply, 250);

  if (currentScript && !document.querySelector('link[data-open-kimono-css]')) {
    const css = document.createElement('link');
    css.rel = 'stylesheet';
    css.href = new URL('practitioner-open-kimono-20260818.css?v=20260818b', currentScript.src).href;
    css.dataset.openKimonoCss = '20260818';
    document.head.appendChild(css);
  }

  const load = (filename, marker, version) => {
    if (!currentScript || document.querySelector(`script[${marker}]`)) return;
    const script = document.createElement('script');
    script.src = new URL(`${filename}?v=${version}`, currentScript.src).href;
    script.async = false;
    script.setAttribute(marker, version);
    document.head.appendChild(script);
  };

  load('reader-journey-20260818.js', 'data-psr-reader-journey', '20260818b');
  load('reader-journey-hero-20260818.js', 'data-psr-reader-journey-hero', '20260818b');
  load('practitioner-open-kimono-20260818.js', 'data-open-kimono-practitioner', '20260818b');
  load('supervisory-practice-entrypoints-20260818.js', 'data-supervisory-practice-entrypoints', '20260818a');
  load('optimum-reader-journey-20260818.js', 'data-optimum-reader-journey', '20260818b');
  load('optimum-reader-journey-finish-20260818.js', 'data-optimum-reader-journey-finish', '20260818a');
})();