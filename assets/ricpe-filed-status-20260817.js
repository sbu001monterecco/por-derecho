(() => {
  const currentScript = document.currentScript;
  const isEn = /\/en\//.test(location.pathname);
  const isRicpeMain = /\/(en|es)\/ric-private-equity-sun-park\/?$/.test(location.pathname);

  const statusCopy = isEn
    ? {
        eyebrow: 'FORMAL COMMUNICATION STATUS · UPDATED 19 AUGUST 2026',
        title: 'RICPE Ethical Channel: filing acknowledged; a further same-case notification has now been received.',
        body: 'The 17 August 2026 formal communication concerning Sun Park / MYND Yaiza and the CAM–HNT / RICPE perimeter was submitted through RICPE’s Ethical Channel and acknowledged by the platform. On 19 August 2026 at 12:38:57 UTC, the same platform sent a further email stating that additional information had been provided in that communication.',
        boundary: '<strong>Current controlled status:</strong> filed → platform acknowledged → further same-case notification received. This does <strong>not</strong>, by itself, establish admission on the merits, opening of a formal investigation, conflict-screening outcome, preservation measures, Board treatment, acceptance of any allegation or any merits decision.',
        grammar: '<strong>Status grammar:</strong> filed ≠ acknowledged ≠ further communication ≠ admitted ≠ investigated ≠ accepted ≠ decided. The exact channel access/case code remains private; the public repository uses only a one-way SHA-256 correlation fingerprint.',
        fingerprint: 'Case-code correlation fingerprint (SHA-256): <code>e53bda34973e530520bde39648768a1e32a358d8984294b21258789faebe6a24</code>.'
      }
    : {
        eyebrow: 'ESTADO DE LA COMUNICACIÓN FORMAL · ACTUALIZADO 19 AGOSTO 2026',
        title: 'Canal Ético de RICPE: presentación acusada; ya existe una nueva notificación del mismo expediente.',
        body: 'La comunicación formal de 17 de agosto de 2026 relativa a Sun Park / MYND Yaiza y al perímetro CAM–HNT / RICPE fue presentada a través del Canal Ético de RICPE y acusada por la plataforma. El 19 de agosto de 2026, a las 12:38:57 UTC, la misma plataforma remitió un nuevo correo indicando que se había aportado información adicional en esa comunicación.',
        boundary: '<strong>Estado controlado actual:</strong> presentada → acuse de plataforma → nueva notificación del mismo expediente recibida. Esto <strong>no</strong> acredita por sí solo admisión a trámite sobre el fondo, apertura de investigación formal, resultado del control de conflictos, medidas de preservación, tratamiento por el Consejo, aceptación de ninguna alegación ni decisión de fondo.',
        grammar: '<strong>Gramática de estado:</strong> presentada ≠ acusada ≠ nueva comunicación ≠ admitida ≠ investigada ≠ aceptada ≠ decidida. El código exacto de acceso/expediente del Canal permanece privado; el repositorio público utiliza únicamente una huella SHA-256 unidireccional de correlación.',
        fingerprint: 'Huella de correlación del código del expediente (SHA-256): <code>e53bda34973e530520bde39648768a1e32a358d8984294b21258789faebe6a24</code>.'
      };

  const statusMarkup = () => `<div class="shell"><p class="eyebrow">${statusCopy.eyebrow}</p><h2>${statusCopy.title}</h2><p>${statusCopy.body}</p><p class="warn">${statusCopy.boundary}</p><p>${statusCopy.grammar}</p><p class="micro">${statusCopy.fingerprint}</p></div>`;

  const injectMainRicpeStatus = () => {
    if (!isRicpeMain || document.querySelector('[data-ricpe-19aug-status]')) return;
    const hero = document.querySelector('.dossier-hero');
    if (!hero) return;
    const section = document.createElement('section');
    section.className = 'section';
    section.dataset.ricpe19augStatus = '20260819';
    section.setAttribute('aria-label', isEn ? 'Latest RICPE procedural status' : 'Último estado procesal RICPE');
    section.innerHTML = statusMarkup();
    hero.insertAdjacentElement('afterend', section);
  };

  const apply = () => {
    const status = document.querySelector('[data-ricpe-prefiling-status]');
    if (status) status.innerHTML = statusMarkup();

    const update = document.querySelector('#ricpe-formal-prefiling-17aug');
    if (update) {
      update.innerHTML = isEn
        ? '<div class="update-meta"><span class="new">Live</span><span>Ethical Channel</span><span>Updated 19 Aug 2026</span></div><h3>RICPE channel: filing acknowledged and further same-case notification received</h3><p>The 17 August filing is corroborated by the platform acknowledgment. On 19 August 2026 at 12:38:57 UTC, the platform sent a further email saying additional information had been provided in the same communication.</p><p><strong>Evidence boundary:</strong> this is a procedural-status event only. It does not establish admission, investigation, conflict review, preservation measures, Board treatment, acceptance of allegations or merits.</p><div class="update-actions"><a class="button" href="../ricpe-documentary-accountability/#formal-communication-17aug">Current RICPE status →</a></div>'
        : '<div class="update-meta"><span class="new">En vivo</span><span>Canal Ético</span><span>Actualizado 19 ago 2026</span></div><h3>Canal RICPE: presentación acusada y nueva notificación del mismo expediente recibida</h3><p>La presentación de 17 de agosto está corroborada por el acuse de plataforma. El 19 de agosto de 2026, a las 12:38:57 UTC, la plataforma remitió un nuevo correo indicando que se había aportado información adicional en la misma comunicación.</p><p><strong>Límite probatorio:</strong> se trata únicamente de un hito de estado procesal. No acredita admisión, investigación, control de conflictos, preservación, tratamiento del Consejo, aceptación de alegaciones ni fondo.</p><div class="update-actions"><a class="button" href="../ricpe-responsabilidad-documental/#comunicacion-formal-17ago">Estado actual RICPE →</a></div>';
    }

    injectMainRicpeStatus();
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => setTimeout(apply, 0), { once: true });
  else setTimeout(apply, 0);
  setTimeout(apply, 250);
  setTimeout(apply, 900);

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
  load('ricpe-idoneidad-public-questions-20260818.js', 'data-ricpe-idoneidad-public-questions', '20260818a');
  load('ricpe-pwc-control-node-20260819.js', 'data-ricpe-pwc-control-node', '20260819a');
})();