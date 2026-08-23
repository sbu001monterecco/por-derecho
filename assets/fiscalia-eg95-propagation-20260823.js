/* FISCALIA-TENERIFE-EG95-PROPAGATION-20260823 */
(() => {
  const normalise = value => {
    let path = value.replace(/\/index\.html$/, '/');
    if (!path.endsWith('/')) path += '/';
    return path;
  };
  const path = normalise(location.pathname);
  const isEnglish = document.documentElement.lang === 'en';
  const root = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const route = `${root}${isEnglish ? 'en' : 'es'}/fiscalia-tenerife-eg95-2026/`;
  const spanishRoute = `${root}es/fiscalia-tenerife-eg95-2026/`;
  const englishRoute = `${root}en/fiscalia-tenerife-eg95-2026/`;

  const addStyles = () => {
    if (document.querySelector('style[data-fiscalia-eg95-styles]')) return;
    const style = document.createElement('style');
    style.dataset.fiscaliaEg95Styles = '20260823';
    style.textContent = `
      .eg95-procedural-update{border-top:5px solid #8c2f2c;background:linear-gradient(135deg,#fffaf0,#fff);box-shadow:0 14px 34px rgba(19,37,45,.08)}
      .eg95-procedural-update .eg95-grid{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(240px,.65fr);gap:1.4rem;align-items:start}
      .eg95-procedural-update .eg95-label{font-size:.76rem;font-weight:900;letter-spacing:.07em;text-transform:uppercase;color:#8c2f2c}
      .eg95-procedural-update h2{margin:.35rem 0 .75rem;line-height:1.08}
      .eg95-procedural-update .eg95-boundary{background:#13252d;color:#fff;border-radius:14px;padding:1rem}
      .eg95-procedural-update .eg95-actions{display:flex;gap:.7rem;flex-wrap:wrap;margin-top:1rem}
      .eg95-procedural-update .eg95-actions a{font-weight:800}
      .ir-subrecord.eg95-subrecord{border-top-color:#8c2f2c}
      .material-update.eg95-update{border-left-color:#8c2f2c}
      @media(max-width:760px){.eg95-procedural-update .eg95-grid{grid-template-columns:1fr}}
    `;
    document.head.append(style);
  };

  const placeDp748Notice = () => {
    if (!path.endsWith('/es/fiscalia-tenerife-dp748/') || document.querySelector('[data-eg95-dp748-update]')) return;
    const main = document.querySelector('main');
    const hero = main && main.querySelector(':scope > section:first-of-type');
    if (!main || !hero) return;
    const section = document.createElement('section');
    section.className = 'section eg95-procedural-update';
    section.dataset.eg95Dp748Update = '20260823';
    section.innerHTML = `
      <div class="shell"><div class="eg95-grid"><div>
        <p class="eg95-label">Actualización procedimental · 21 de agosto de 2026</p>
        <h2>Fiscalía abrió y archivó el Expediente Gubernativo 95/2026.</h2>
        <p>El Decreto trató la aportación como una solicitud de revisión vinculada a DP 748/2026 y consideró que no podían abrirse nuevas DIP ni acordarse diligencias fuera de aquel procedimiento judicial, aunque estuviera archivado.</p>
        <p><strong>Alcance documentado:</strong> el correo también pedía preservación, asociación con antecedentes fiscales, separación de expedientes y comprobaciones finitas en ETJ 163/2020 / Cambiario 1048/2019. El Decreto no contiene una decisión individual sobre cada una.</p>
        <div class="eg95-actions"><a class="button" href="${spanishRoute}">Abrir EG 95/2026 →</a><a href="${englishRoute}" lang="en">English record</a></div>
      </div><aside class="eg95-boundary"><strong>No es una conclusión de fondo.</strong><p>El Decreto no declara falsos, irrelevantes o insuficientes los documentos aportados. Tampoco confirma que el correo y sus anexos fueran incorporados a DP 748/2026.</p></aside></div></div>`;
    hero.insertAdjacentElement('afterend', section);
  };

  const placeInstitutionalRecord = () => {
    const isInstitutional = path.endsWith('/es/registros-institucionales/') || path.endsWith('/en/institutional-records/');
    if (!isInstitutional || document.querySelector('[data-eg95-institutional-record]')) return;
    const article = document.querySelector('#ministerio-fiscal');
    if (!article) return;
    const container = article.querySelector('.ir-subrecords') || article;
    const card = document.createElement('section');
    card.className = 'ir-subrecord eg95-subrecord';
    card.id = 'fiscalia-tenerife-eg95';
    card.dataset.eg95InstitutionalRecord = '20260823';
    if (isEnglish) {
      card.innerHTML = `<h3>Santa Cruz de Tenerife · File 95/2026</h3>
        <p>On 21 August 2026 the Chief Prosecutor opened and closed Administrative File 95/2026, reasoning that the matter was judicialised in DP 748/2026 and could not be investigated through parallel prosecutorial proceedings.</p>
        <p class="sub-status">Procedural closure; no express merits rejection of the newly supplied documents.</p>
        <p><a href="${englishRoute}">Controlled record, full translation and open questions →</a></p>`;
    } else {
      card.innerHTML = `<h3>Santa Cruz de Tenerife · EG 95/2026</h3>
        <p>El 21 de agosto de 2026 el Fiscal Jefe abrió y archivó EG 95/2026, al considerar que la materia estaba judicializada en DP 748/2026 y no podía investigarse mediante diligencias fiscales paralelas.</p>
        <p class="sub-status">Archivo procedimental; sin rechazo expreso de fondo de los nuevos documentos.</p>
        <p><a href="${spanishRoute}">Registro controlado, traducción completa y preguntas abiertas →</a></p>`;
    }
    container.prepend(card);
    const lastVerified = article.querySelector('.ir-meta div:first-child strong');
    if (lastVerified) lastVerified.textContent = isEnglish ? '23 August 2026' : '23 de agosto de 2026';
  };

  const makeUpdateArticle = () => {
    const article = document.createElement('article');
    article.className = 'material-update institutional eg95-update';
    article.id = 'fiscalia-tenerife-eg95-21aug';
    article.dataset.eg95Update = '20260823';
    if (isEnglish) {
      article.innerHTML = `<div class="update-meta"><span class="new">New</span><span>Public Prosecutor</span><span>File 95/2026</span><span>DP 748/2026</span></div>
        <h3>Tenerife Prosecutor opens and closes File 95/2026 on procedural-routing grounds</h3>
        <p>The 21 August Decree treats the submission principally as a request to revisit the prosecution position in DP 748/2026 and says no parallel prosecutorial investigation can be opened. The complete email also requested preservation, cross-file association and finite ETJ/Cambiario checks.</p>
        <p><strong>Boundary:</strong> the Decree does not expressly reject the supplied documents on their merits, and judicial incorporation of the email and annexes remains unverified.</p>
        <div class="update-links"><a href="${englishRoute}">Open the bilingual controlled record →</a><a href="${spanishRoute}" lang="es">Registro en español</a></div>`;
    } else {
      article.innerHTML = `<div class="update-meta"><span class="new">Nuevo</span><span>Ministerio Fiscal</span><span>EG 95/2026</span><span>DP 748/2026</span></div>
        <h3>Fiscalía Tenerife abre y archiva EG 95/2026 por una razón de cauce procedimental</h3>
        <p>El Decreto de 21 de agosto trata la aportación principalmente como una petición de revisión vinculada a DP 748/2026 y afirma que no pueden abrirse diligencias fiscales paralelas. El correo completo también pedía preservación, asociación interexpedientes y comprobaciones finitas en ETJ/Cambiario.</p>
        <p><strong>Límite:</strong> el Decreto no rechaza expresamente los documentos en cuanto al fondo y sigue sin verificarse su incorporación judicial.</p>
        <div class="update-links"><a href="${spanishRoute}">Abrir registro bilingüe controlado →</a><a href="${englishRoute}" lang="en">English record</a></div>`;
    }
    return article;
  };

  const placeUpdates = () => {
    const isUpdates = path.endsWith('/es/actualizaciones/') || path.endsWith('/en/updates/');
    if (!isUpdates || document.querySelector('[data-eg95-update]')) return;
    const groups = [...document.querySelectorAll('.date-group')];
    const dateNeedle = isEnglish ? '21 August 2026' : '21 de agosto de 2026';
    const group = groups.find(item => (item.querySelector('h2')?.textContent || '').includes(dateNeedle));
    const article = makeUpdateArticle();
    if (group) {
      const stream = group.querySelector('.update-stream') || group;
      stream.prepend(article);
      return;
    }
    const shell = document.querySelector('.updates-section .shell');
    if (!shell) return;
    const section = document.createElement('section');
    section.className = 'date-group';
    const headingId = isEnglish ? 'fiscalia-eg95-date' : 'fiscalia-eg95-fecha';
    section.setAttribute('aria-labelledby', headingId);
    section.innerHTML = `<h2 id="${headingId}">${dateNeedle} · ${isEnglish ? 'prosecutorial routing' : 'cauce fiscal'}</h2><div class="update-stream"></div>`;
    section.querySelector('.update-stream').append(article);
    const first = shell.querySelector('.date-group');
    if (first) first.insertAdjacentElement('afterend', section);
    else shell.append(section);
  };

  const run = () => {
    addStyles();
    placeDp748Notice();
    placeInstitutionalRecord();
    placeUpdates();
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, { once: true });
  else run();
})();
