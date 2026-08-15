(() => {
  const path = window.location.pathname;
  const isEs = path.includes('/es/');
  const isWhoEs = path.includes('/es/quien-debe-responder-que/');
  const isWhoEn = path.includes('/en/who-should-answer-what/');
  const isC7Es = path.includes('/es/canarias7-articulo-30mayo2022/');
  const isC7En = path.includes('/en/canarias7-article-30may2022/');
  const isEcoEs = path.includes('/es/eleconomista-javier-romera-enero2025/');
  const isEcoEn = path.includes('/en/eleconomista-javier-romera-january2025/');
  if (!(isWhoEs || isWhoEn || isC7Es || isC7En || isEcoEs || isEcoEn)) return;

  const css = document.createElement('style');
  css.textContent = `
    .media-marks-wrap{margin:1.4rem 0 0}
    .media-marks-kicker{font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;font-weight:800;opacity:.72;margin:0 0 .65rem}
    .media-marks{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.8rem;max-width:760px}
    .media-mark{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:.95rem 1.1rem;border:1px solid rgba(19,37,45,.18);border-radius:14px;background:#fff;text-decoration:none;color:inherit;box-shadow:0 7px 22px rgba(19,37,45,.06)}
    .media-mark:hover{transform:translateY(-1px);box-shadow:0 10px 26px rgba(19,37,45,.1)}
    .media-mark-name{font-size:1.08rem;font-weight:900;line-height:1}
    .media-mark-name.eco{font-family:Georgia,'Times New Roman',serif;font-style:italic;font-weight:700}
    .media-mark small{display:block;margin-top:.28rem;font-size:.75rem;opacity:.68;font-weight:600}
    .media-mark-arrow{font-size:1.15rem;opacity:.65}
    .media-marks-note{font-size:.82rem;line-height:1.45;opacity:.72;max-width:760px;margin:.65rem 0 0}
    .media-switcher{padding:1rem 0;background:#f4f1ea;border-top:1px solid rgba(19,37,45,.08);border-bottom:1px solid rgba(19,37,45,.08)}
    .media-switcher .media-marks-wrap{margin:0}
    @media(max-width:640px){.media-marks{grid-template-columns:1fr}}
  `;
  document.head.appendChild(css);

  const routes = isEs ? {
    c7:'../canarias7-articulo-30mayo2022/', eco:'../eleconomista-javier-romera-enero2025/',
    title:'Medios · trazabilidad editorial', c7sub:'Artículo 30/05/2022 · publicación/despublicación', ecosub:'Enero 2025 · verificación/no publicación',
    note:'Identificación editorial. Estos medios no se presentan como autoridades públicas ni se atribuye aval, afiliación o responsabilidad por el mero uso de su nombre.'
  } : {
    c7:'../canarias7-article-30may2022/', eco:'../eleconomista-javier-romera-january2025/',
    title:'Media · editorial traceability', c7sub:'30 May 2022 · publication/unpublishing', ecosub:'January 2025 · verification/non-publication',
    note:'Editorial identification only. These publications are not presented as public authorities and no endorsement, affiliation or responsibility is implied by use of their names.'
  };

  const build = () => {
    const wrap = document.createElement('div');
    wrap.className = 'media-marks-wrap';
    wrap.innerHTML = `<p class="media-marks-kicker">${routes.title}</p><div class="media-marks"><a class="media-mark" href="${routes.c7}" aria-label="Canarias7"><span><span class="media-mark-name">CANARIAS7</span><small>${routes.c7sub}</small></span><span class="media-mark-arrow">→</span></a><a class="media-mark" href="${routes.eco}" aria-label="elEconomista"><span><span class="media-mark-name eco">elEconomista</span><small>${routes.ecosub}</small></span><span class="media-mark-arrow">→</span></a></div><p class="media-marks-note">${routes.note}</p>`;
    return wrap;
  };

  if (isWhoEs || isWhoEn) {
    const hero = document.querySelector('main .hero');
    if (hero && !document.querySelector('[data-media-marks-index]')) {
      const section = document.createElement('section');
      section.className = 'section alt';
      section.dataset.mediaMarksIndex = 'true';
      const shell = document.createElement('div');
      shell.className = 'shell';
      shell.appendChild(build());
      section.appendChild(shell);
      hero.insertAdjacentElement('afterend', section);
    }
  } else {
    const hero = document.querySelector('main .hero, main .mhero');
    if (hero && !document.querySelector('[data-media-switcher]')) {
      const section = document.createElement('section');
      section.className = 'media-switcher';
      section.dataset.mediaSwitcher = 'true';
      const shell = document.createElement('div');
      shell.className = 'shell';
      shell.appendChild(build());
      section.appendChild(shell);
      hero.insertAdjacentElement('afterend', section);
    }
  }
})();
