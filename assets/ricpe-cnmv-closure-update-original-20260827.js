/* RICPE-CNMV-CLOSURE-UPDATE-20260827 */
(() => {
  const normalise = value => {
    let path = value.replace(/\/index\.html$/, '/');
    if (!path.endsWith('/')) path += '/';
    return path;
  };
  const path = normalise(location.pathname);
  const routes = {
    ricpeEs: '/es/ric-private-equity-sun-park/',
    ricpeEn: '/en/ric-private-equity-sun-park/',
    cnmvEs: '/es/cnmv-ricpe-verificacion/',
    cnmvEn: '/en/cnmv-ricpe-verification/'
  };
  const kind = Object.entries(routes).find(([, suffix]) => path.endsWith(suffix));
  if (!kind) return;

  const render = () => {
    if (document.querySelector('[data-ricpe-cnmv-closure-20260827]')) return;
    const isEnglish = document.documentElement.lang === 'en';
    const isCnmv = kind[0].startsWith('cnmv');
    const basePrefix = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
    const evidence = `${basePrefix}evidence/ricpe-cnmv/2026-08-27/`;
    const ricpePage = `${basePrefix}${isEnglish ? 'en/ric-private-equity-sun-park/' : 'es/ric-private-equity-sun-park/'}`;
    const cnmvPage = `${basePrefix}${isEnglish ? 'en/cnmv-ricpe-verification/' : 'es/cnmv-ricpe-verificacion/'}`;

    const style = document.createElement('style');
    style.dataset.ricpeCnmvClosureStyle = '20260827';
    style.textContent = `
      [data-ricpe-cnmv-closure-20260827]{background:#fff7e8;border-top:1px solid #e5d3aa;border-bottom:1px solid #e5d3aa;padding:2rem 0}
      [data-ricpe-cnmv-closure-20260827] .closure-wrap{max-width:1180px;margin:0 auto;padding:0 1.1rem}
      [data-ricpe-cnmv-closure-20260827] .closure-kicker{margin:0 0 .45rem;font-size:.72rem;font-weight:900;letter-spacing:.08em;text-transform:uppercase;color:#805f22}
      [data-ricpe-cnmv-closure-20260827] h2{margin:.15rem 0 .75rem;max-width:30ch;font-size:clamp(1.65rem,3vw,2.6rem);line-height:1.08;color:#13252d}
      [data-ricpe-cnmv-closure-20260827] .closure-lead{max-width:86ch;line-height:1.65;color:#26383f}
      [data-ricpe-cnmv-closure-20260827] .closure-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.7rem;margin:1rem 0}
      [data-ricpe-cnmv-closure-20260827] .closure-card{background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:14px;padding:.9rem}
      [data-ricpe-cnmv-closure-20260827] .closure-card time{display:block;font-size:.68rem;font-weight:900;letter-spacing:.06em;text-transform:uppercase;color:#805f22}
      [data-ricpe-cnmv-closure-20260827] .closure-card strong{display:block;margin:.25rem 0;color:#13252d}
      [data-ricpe-cnmv-closure-20260827] .closure-card p{margin:.25rem 0 0;font-size:.88rem;line-height:1.5}
      [data-ricpe-cnmv-closure-20260827] .closure-boundary{max-width:92ch;margin:.9rem 0;padding:.8rem .95rem;border-left:5px solid #805f22;background:#fff;line-height:1.55}
      [data-ricpe-cnmv-closure-20260827] .closure-actions{display:flex;flex-wrap:wrap;gap:.55rem;margin-top:1rem}
      [data-ricpe-cnmv-closure-20260827] .closure-actions a{display:inline-flex;align-items:center;text-decoration:none;border-radius:999px;padding:.68rem .9rem;background:#13252d;color:#fff;font-weight:850}
      [data-ricpe-cnmv-closure-20260827] .closure-actions a.secondary{background:#fff;color:#13252d;border:1px solid rgba(19,37,45,.25)}
      [data-ricpe-cnmv-closure-20260827] .closure-state{font-weight:850;color:#6d4b12}
      @media(max-width:760px){[data-ricpe-cnmv-closure-20260827] .closure-grid{grid-template-columns:1fr}}
    `;
    document.head.append(style);

    const section = document.createElement('section');
    section.dataset.ricpeCnmvClosure20260827 = 'true';
    section.id = isCnmv ? 'ampliacion-ricpe-27ago2026' : 'ricpe-cierre-27ago2026';

    const copy = isEnglish ? {
      kicker: '27 August 2026 · certified Ethics Channel closure',
      title: 'RICPE rejected and closed the communication without opening an internal investigation.',
      lead: 'The Ithikios certificate records the full resolution communicated through the channel and its visible workflow. It does not establish that this is RICPE’s complete internal decision record, identify every document reviewed, or evidence the conflict check and preservation steps requested.',
      card1Title: 'Filed and acknowledged',
      card1Body: 'The signed 22-page communication was filed through the RICPE Ethics Channel and assigned a private tracking reference.',
      card2Title: 'Accepted, assigned and preliminarily examined',
      card2Body: 'The history records a request for RICPE’s own 20 July 2021 certificate and marks that request “Not shown to the reporting person”. The cause remains to be established.',
      card3Title: 'Rejected and archived',
      card3Body: 'The Responsible Officer recorded rejection and closure without opening an internal investigation, while leaving open reconsideration if new concrete evidence is supplied.',
      boundary: '<strong>Evidence boundary:</strong> “Not shown to the reporting person” is a certified workflow fact, not proof of intent. The relevant questions are who set that state, whether the requested document was already held and reviewed, what “immediately available documentation” meant, and what was preserved before closure.',
      state: 'CNMV extension state: the complete five-attachment documentary package was sent on 27 August 2026 in the existing supervisory thread to the five-address CNMV distribution previously used on 20 August. It followed an initial linked notice to the two core infringement-reporting channels. Receipt, incorporation and substantive examination remain pending primary confirmation.',
      evidenceLink: 'Open certified public record',
      otherLink: isCnmv ? 'Open the RICPE dossier' : 'Open the CNMV gateway',
      sourceLink: 'Read the controlled resolution transcript',
      manifestLink: 'Hashes and publication limits'
    } : {
      kicker: '27 agosto 2026 · cierre certificado del Canal Ético',
      title: 'RICPE inadmitió y archivó la comunicación sin abrir investigación interna.',
      lead: 'El certificado de Ithikios registra la resolución íntegra comunicada a través del canal y el historial visible de tramitación. No acredita que sea el expediente decisorio interno completo de RICPE, qué documentación concreta se examinó, ni el control de conflictos y las medidas de preservación solicitadas.',
      card1Title: 'Presentación y acuse',
      card1Body: 'La comunicación firmada de 22 páginas fue presentada por el Canal Ético de RICPE y recibió una referencia privada de seguimiento.',
      card2Title: 'Aceptación, asignación y examen preliminar',
      card2Body: 'El historial registra una petición de la certificación propia de RICPE de 20 de julio de 2021 y marca esa petición “No mostrado al denunciante”. La causa debe determinarse.',
      card3Title: 'Inadmisión y archivo',
      card3Body: 'El Responsable del Sistema acordó inadmisión y archivo sin abrir investigación interna, dejando abierta una eventual valoración ante nueva evidencia concreta.',
      boundary: '<strong>Límite probatorio:</strong> “No mostrado al denunciante” es un hecho certificado del flujo, no prueba de intención. Las preguntas son quién configuró ese estado, si el documento pedido ya obraba y fue examinado, qué significó “documentación inmediatamente disponible” y qué se preservó antes del cierre.',
      state: 'Estado ampliación CNMV: el 27 de agosto de 2026 se remitió, dentro del hilo supervisor existente, el paquete documental completo de cinco anexos a la distribución CNMV de cinco direcciones ya utilizada el 20 de agosto. Le precedió un aviso enlazado a los dos canales centrales de comunicación de infracciones. La recepción, incorporación y revisión de fondo quedan pendientes de confirmación primaria.',
      evidenceLink: 'Abrir registro público certificado',
      otherLink: isCnmv ? 'Abrir dossier RICPE' : 'Abrir puerta CNMV',
      sourceLink: 'Leer transcripción controlada de la resolución',
      manifestLink: 'Huellas y límites de publicación'
    };

    section.innerHTML = `<div class="closure-wrap">
      <p class="closure-kicker">${copy.kicker}</p>
      <h2>${copy.title}</h2>
      <p class="closure-lead">${copy.lead}</p>
      <div class="closure-grid">
        <article class="closure-card"><time>17 AGO 2026</time><strong>${copy.card1Title}</strong><p>${copy.card1Body}</p></article>
        <article class="closure-card"><time>19 AGO 2026</time><strong>${copy.card2Title}</strong><p>${copy.card2Body}</p></article>
        <article class="closure-card"><time>27 AGO 2026</time><strong>${copy.card3Title}</strong><p>${copy.card3Body}</p></article>
      </div>
      <p class="closure-boundary">${copy.boundary}</p>
      <p class="closure-state" data-cnmv-extension-state>${copy.state}</p>
      <div class="closure-actions">
        <a href="${evidence}">${copy.evidenceLink}</a>
        <a class="secondary" href="${evidence}resolution.txt">${copy.sourceLink}</a>
        <a class="secondary" href="${evidence}manifest.txt">${copy.manifestLink}</a>
        <a class="secondary" href="${isCnmv ? ricpePage : cnmvPage}">${copy.otherLink}</a>
      </div>
    </div>`;

    const main = document.querySelector('main');
    if (!main) return;
    const hero = main.querySelector(':scope > section:first-of-type');
    if (hero) hero.insertAdjacentElement('afterend', section);
    else main.prepend(section);

    if (!isCnmv) {
      const eyebrow = document.querySelector('.dossier-hero .eyebrow');
      if (eyebrow) eyebrow.textContent = isEnglish
        ? 'Formal communication filed 17 August 2026 · certified closure 27 August 2026'
        : 'Comunicación formal presentada 17 agosto 2026 · cierre certificado 27 agosto 2026';
      const status = document.querySelectorAll('.dossier-status div strong');
      if (status[1]) status[1].textContent = isEnglish
        ? 'Filed 17 Aug · accepted/assigned 19 Aug · closed 27 Aug'
        : 'Presentada 17 ago · aceptada/asignada 19 ago · cerrada 27 ago';
      if (status[2]) status[2].textContent = isEnglish
        ? 'Rejected and archived without internal investigation; complete internal file not evidenced'
        : 'Inadmitida y archivada sin investigación interna; expediente interno completo no acreditado';
    } else {
      const strip = document.querySelector('.status-strip');
      if (strip) {
        const last = strip.lastElementChild;
        if (last) last.innerHTML = `<span>27 ${isEnglish ? 'Aug' : 'ago'} 2026</span><strong>${isEnglish ? 'RICPE closure · full CNMV package sent' : 'Cierre RICPE · paquete CNMV completo remitido'}</strong>`;
      }
      const grid = document.querySelector('#revision-7-minutos .cnmv-grid');
      if (grid && !grid.querySelector('[data-closure-card-20260827]')) {
        const card = document.createElement('article');
        card.className = 'cnmv-card';
        card.dataset.closureCard20260827 = 'true';
        card.innerHTML = isEnglish
          ? '<span class="ok-status official">7 · 27 Aug 2026</span><h3>Certified closure</h3><p>RICPE rejected and archived the communication without opening an internal investigation. The Ithikios record exposes a request for the 20 July 2021 certificate marked “Not shown to the reporting person”. A linked notice and then the complete five-attachment package were sent to the five-address CNMV distribution on 27 August.</p>'
          : '<span class="ok-status official">7 · 27 ago 2026</span><h3>Cierre certificado</h3><p>RICPE inadmitió y archivó la comunicación sin abrir investigación interna. El registro Ithikios muestra una petición de la certificación de 20 julio 2021 marcada “No mostrado al denunciante”. El 27 de agosto se remitieron un aviso enlazado y después el paquete completo de cinco anexos a la distribución CNMV de cinco direcciones.</p>';
        grid.append(card);
      }
    }

    const meta = document.createElement('meta');
    meta.name = 'pd-last-material-update';
    meta.content = '2026-08-27';
    document.head.append(meta);
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render, { once: true });
  else render();
})();
