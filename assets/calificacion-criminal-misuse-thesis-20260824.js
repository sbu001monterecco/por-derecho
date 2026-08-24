(() => {
  const current = document.currentScript;
  if (!current) return;

  const normalise = value => {
    let path = value.replace(/\/index\.html$/, '/');
    if (!path.endsWith('/')) path += '/';
    return path;
  };
  const path = normalise(location.pathname);
  const featured = new Set([
    '/es/',
    '/en/',
    '/es/concurso-36-2012-responsabilidad-institucional/',
    '/en/insolvency-36-2012-institutional-accountability/'
  ]);
  const canonical = new Set([
    '/es/tesis-uso-criminal-procedimiento-calificacion/',
    '/en/insolvency-classification-criminal-misuse-thesis/'
  ]);
  const priorityStatic = new Set([
    '/es/concurso-36-2012-ap-seccion-4/',
    '/en/insolvency-36-2012-ap-section-4/',
    '/es/nota-independencia-judicial-estado-procesal-reserva-acciones/'
  ]);
  const compact = new Set([
    '/es/concurso-36-2012-administrador-concursal/',
    '/en/insolvency-36-2012-insolvency-administrator/',
    '/es/concurso-36-2012-magistrado-juez/',
    '/en/insolvency-36-2012-mercantile-court-1/',
    '/es/carta-abierta-ministerio-fiscal/',
    '/es/acosta-matos-perimetro/',
    '/en/acosta-matos-perimeter/',
    '/es/control-acreedor-cam-administracion-hecho-omision-judicial/',
    '/en/cam-creditor-control-shadow-administration-judicial-omission/',
    '/es/dp-1901-2026/',
    '/en/dp-1901-2026/',
    '/es/dp-1956-2026/',
    '/en/dp-1956-2026/'
  ]);
  const match = suffixes => [...suffixes].some(suffix => path.endsWith(suffix));

  const pinFirstRead = (section, main) => {
    const persistent = match(featured);
    const pin = () => {
      const hero = main.querySelector(':scope > section:first-of-type');
      const sourceFunds = main.querySelector(':scope > .source-funds-notice-section--featured');
      const anchor = sourceFunds || hero;
      if (anchor && anchor.nextElementSibling !== section) anchor.insertAdjacentElement('afterend', section);
    };
    const observer = new MutationObserver(pin);
    observer.observe(main, { childList: true });
    if (persistent) {
      main.dataset.calificacionMisusePin = 'persistent-20260824c';
      window.setInterval(pin, 1000);
    }
    [0, 100, 350, 1000, 3000, 7000, 11000, 15000, 22000, 30000].forEach(delay => window.setTimeout(pin, delay));
    window.addEventListener('load', () => {
      pin();
      window.setTimeout(pin, 7000);
      window.setTimeout(pin, 15000);
      window.setTimeout(pin, 25000);
    }, { once: true });
    pin();
  };

  const place = () => {
    const existing = document.querySelector('[data-calificacion-misuse-thesis]');
    if (existing) {
      if (!match(canonical) && !match(featured) && !match(priorityStatic)) return;
      const existingMain = document.querySelector('main');
      if (existingMain) pinFirstRead(existing, existingMain);
      return;
    }
    const isFeatured = match(featured);
    if (!isFeatured && !match(compact)) return;
    const main = document.querySelector('main');
    const hero = main && main.querySelector(':scope > section:first-of-type');
    if (!main || !hero) return;

    const isEnglish = document.documentElement.lang === 'en';
    const href = new URL(isEnglish
      ? '../en/insolvency-classification-criminal-misuse-thesis/'
      : '../es/tesis-uso-criminal-procedimiento-calificacion/', current.src).href;
    const section = document.createElement('section');
    section.dataset.calificacionMisuseThesis = isFeatured ? 'featured' : 'compact';
    section.className = isFeatured ? 'cm-thesis-section' : 'cm-thesis-compact';

    if (isFeatured) {
      const shell = document.createElement('div');
      shell.className = 'shell';
      const head = document.createElement('div');
      head.className = 'cm-thesis-head';
      const copy = document.createElement('div');
      const kicker = document.createElement('p');
      kicker.className = 'cm-thesis-kicker';
      kicker.textContent = isEnglish ? 'CRIMINAL-MISUSE THESIS · DOCUMENT-BASED · NOT A FINDING' : 'TESIS DE USO CRIMINAL · DOCUMENTAL · NO ES UNA CONDENA';
      const title = document.createElement('h2');
      title.textContent = isEnglish ? 'The culpability record requires a separate investigation.' : 'La calificación exige una investigación separada.';
      const lead = document.createElement('p');
      lead.className = 'cm-thesis-lead';
      lead.textContent = isEnglish
        ? 'The present record supports a serious, document-based investigative thesis: materially excessive Administrator allegations, a severe defective two-page Fiscal opinion, DI 248 circularity, judicial adoption of selected adverse propositions, and possible benefit to the Acosta Matos perimeter.'
        : 'El registro actual sustenta una tesis investigativa seria y documental: alegaciones materialmente excesivas del AC, un dictamen fiscal severo y defectuoso de dos páginas, circularidad en DI 248, adopción judicial de proposiciones adversas seleccionadas y posible beneficio para el perímetro Acosta Matos.';
      copy.append(kicker, title, lead);
      const boundary = document.createElement('aside');
      boundary.className = 'cm-thesis-boundary';
      const boundaryStrong = document.createElement('strong');
      boundaryStrong.textContent = isEnglish ? 'Proof boundary' : 'Límite probatorio';
      const boundaryText = document.createElement('span');
      boundaryText.textContent = isEnglish
        ? 'This is not an adjudicated criminal fact and does not prove common design, coordination, knowing falsity or purposeful benefit.'
        : 'No es un hecho penal declarado y no prueba diseño común, coordinación, falsedad consciente ni beneficio deliberado.';
      boundary.append(boundaryStrong, boundaryText);
      head.append(copy, boundary);
      const actions = document.createElement('div');
      actions.className = 'cm-thesis-actions';
      const link = document.createElement('a');
      link.href = href;
      link.textContent = isEnglish ? 'Examine the five-part thesis →' : 'Examinar la tesis en cinco partes →';
      actions.append(link);
      shell.append(head, actions);
      section.append(shell);
    } else {
      const shell = document.createElement('div');
      shell.className = 'shell cm-thesis-compact-inner';
      const copy = document.createElement('div');
      const kicker = document.createElement('p');
      kicker.className = 'cm-thesis-kicker';
      kicker.textContent = isEnglish ? 'CRIMINAL-MISUSE THESIS · INVESTIGATIVE, NOT ADJUDICATED' : 'TESIS DE USO CRIMINAL · INVESTIGATIVA, NO DECLARADA';
      const title = document.createElement('h2');
      title.textContent = isEnglish ? 'Five documentary signals require one disciplined investigation.' : 'Cinco señales documentales exigen una investigación disciplinada.';
      const body = document.createElement('p');
      body.textContent = isEnglish
        ? 'Administrator overreach · defective two-page Fiscal opinion · DI 248 circularity · selected judicial adoption · possible benefit to the Acosta Matos perimeter.'
        : 'Exceso del AC · dictamen fiscal defectuoso de dos páginas · circularidad DI 248 · adopción judicial selectiva · posible beneficio del perímetro Acosta Matos.';
      copy.append(kicker, title, body);
      const link = document.createElement('a');
      link.href = href;
      link.textContent = isEnglish ? 'Open the evidence test →' : 'Abrir el test probatorio →';
      shell.append(copy, link);
      section.append(shell);
    }
    hero.insertAdjacentElement('afterend', section);
    pinFirstRead(section, main);
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', place, { once: true });
  else place();
})();
