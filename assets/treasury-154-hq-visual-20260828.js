(() => {
  const current = document.currentScript;
  if (!current) return;

  const base = new URL('.', current.src);
  const normalise = value => {
    let path = value.replace(/\/index\.html$/, '/');
    if (!path.endsWith('/')) path += '/';
    return path;
  };
  const path = normalise(location.pathname);
  const routes = {
    accountability: '/es/ricpe-responsabilidad-documental/',
    ricpe: '/es/ric-private-equity-sun-park/',
    cnmv: '/es/cnmv-ricpe-verificacion/'
  };
  const matched = Object.entries(routes).find(([, suffix]) => path.endsWith(suffix));
  if (!matched) return;

  const imageUrl = new URL('tesoro-resolucion-154-2026-contexto-publicacion-hq-20260828.svg?v=20260828hq4', base).href;
  const siteRoot = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const fullRecordUrl = `${siteRoot}es/ricpe-responsabilidad-documental/#tesoro-acceso-154-2026`;
  const ricpeUrl = `${siteRoot}es/ric-private-equity-sun-park/`;
  const cnmvUrl = `${siteRoot}es/cnmv-ricpe-verificacion/`;
  const imageAlt = 'Tesoro de Canarias: resumen visual de la notificación de 28 de agosto de 2026 que materializa el acceso parcial reconocido por la Resolución 154/2026, con contratación y expedientes de endeudamiento 2022 a 2025 en entrega y producción posterior sucesiva.';

  const ensureStyles = () => {
    if (document.querySelector('#treasury-154-hq-styles')) return;
    const style = document.createElement('style');
    style.id = 'treasury-154-hq-styles';
    style.textContent = `
      .treasury154-hq-section{background:#f4f1ea}
      .treasury154-hq-shell{max-width:1180px}
      .treasury154-hq-head{max-width:78ch}
      .treasury154-hq-kicker{font-size:.74rem;font-weight:900;letter-spacing:.09em;text-transform:uppercase;color:#805f22;margin:0 0 .55rem}
      .treasury154-hq-head h2{font-size:clamp(2rem,4vw,3.25rem);line-height:1.05;margin:.25rem 0 .85rem}
      .treasury154-hq-lead{font-size:1.08rem;line-height:1.62;color:#344b55}
      .treasury154-hq-figure{max-width:1122px;margin:1.4rem auto;background:#fff;border:1px solid rgba(19,37,45,.18);border-radius:18px;padding:.85rem;box-shadow:0 14px 38px rgba(19,37,45,.09)}
      .treasury154-hq-figure>a{display:block;border-radius:11px;overflow:hidden;background:#fff}
      .treasury154-hq-figure img{display:block;width:100%;height:auto;image-rendering:auto}
      .treasury154-hq-figure figcaption{font-size:.92rem;line-height:1.5;color:#52646c;margin-top:.72rem}
      .treasury154-hq-open{display:inline-flex;margin-top:.55rem;font-weight:850;text-decoration:none}
      .treasury154-hq-boundaries{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;margin-top:1rem}
      .treasury154-hq-boundary{background:#fff;border:1px solid rgba(19,37,45,.14);border-radius:14px;padding:1rem}
      .treasury154-hq-boundary strong{display:block;margin-bottom:.35rem}
      .treasury154-hq-boundary p{margin:0;font-size:.94rem;line-height:1.55}
      .treasury154-hq-actions{display:flex;gap:.65rem;flex-wrap:wrap;margin-top:1rem}
      .treasury154-hq-actions a{font-weight:850}
      @media(max-width:760px){.treasury154-hq-boundaries{grid-template-columns:1fr}.treasury154-hq-figure{padding:.45rem;border-radius:12px}.treasury154-hq-figure figcaption{padding:0 .25rem .2rem}}
    `;
    document.head.appendChild(style);
  };

  const makeFigure = captionHtml => {
    const figure = document.createElement('figure');
    figure.className = 'treasury154-hq-figure';
    figure.dataset.treasury154HqVisual = '20260828';

    const link = document.createElement('a');
    link.href = imageUrl;
    link.target = '_blank';
    link.rel = 'noopener';
    link.setAttribute('aria-label', 'Abrir la imagen del Tesoro de Canarias a resolución completa');

    const image = document.createElement('img');
    image.src = imageUrl;
    image.alt = imageAlt;
    image.width = 1122;
    image.height = 1402;
    image.loading = 'eager';
    image.fetchPriority = 'high';
    image.decoding = 'async';
    link.appendChild(image);

    const caption = document.createElement('figcaption');
    caption.innerHTML = captionHtml;
    const open = document.createElement('a');
    open.className = 'treasury154-hq-open';
    open.href = imageUrl;
    open.target = '_blank';
    open.rel = 'noopener';
    open.textContent = 'Abrir imagen a resolución completa →';
    caption.append(document.createElement('br'), open);

    figure.append(link, caption);
    return figure;
  };

  const upgradeAccountabilityFigure = () => {
    const section = document.querySelector('#tesoro-acceso-154-2026');
    if (!section) return;
    const existingImage = section.querySelector('img[src*="tesoro-resolucion-154-2026-contexto-publicacion-20260828"]');
    if (!existingImage) return;
    const figure = existingImage.closest('figure');
    if (!figure || figure.dataset.treasury154HqVisual === '20260828') return;

    ensureStyles();
    figure.className = 'treasury154-hq-figure';
    figure.dataset.treasury154HqVisual = '20260828';
    existingImage.src = imageUrl;
    existingImage.alt = imageAlt;
    existingImage.width = 1122;
    existingImage.height = 1402;
    existingImage.loading = 'eager';
    existingImage.fetchPriority = 'high';
    existingImage.decoding = 'async';
    existingImage.removeAttribute('style');

    if (existingImage.parentElement?.tagName !== 'A') {
      const link = document.createElement('a');
      link.href = imageUrl;
      link.target = '_blank';
      link.rel = 'noopener';
      link.setAttribute('aria-label', 'Abrir la imagen del Tesoro de Canarias a resolución completa');
      existingImage.replaceWith(link);
      link.appendChild(existingImage);
    } else {
      existingImage.parentElement.href = imageUrl;
      existingImage.parentElement.target = '_blank';
      existingImage.parentElement.rel = 'noopener';
    }

    let caption = figure.querySelector('figcaption');
    if (!caption) {
      caption = document.createElement('figcaption');
      figure.appendChild(caption);
    }
    caption.innerHTML = '<strong>Resumen visual de alta resolución.</strong> La composición facilita la lectura de los cuatro hitos. Los extractos oficiales situados inmediatamente debajo siguen siendo la capa probatoria primaria. Los datos personales y cualquier acceso sensible permanecen protegidos.';
    const open = document.createElement('a');
    open.className = 'treasury154-hq-open';
    open.href = imageUrl;
    open.target = '_blank';
    open.rel = 'noopener';
    open.textContent = 'Abrir imagen a resolución completa →';
    caption.append(document.createElement('br'), open);
  };

  const createCrossPageSection = kind => {
    ensureStyles();
    const section = document.createElement('section');
    section.className = 'section treasury154-hq-section';
    section.dataset.treasury154HqSection = kind;
    section.id = kind === 'ricpe' ? 'tesoro-acceso-154-2026' : 'tesoro-acceso-154-2026-cnmv';

    const shell = document.createElement('div');
    shell.className = 'shell treasury154-hq-shell';
    const head = document.createElement('header');
    head.className = 'treasury154-hq-head';
    const kicker = document.createElement('p');
    kicker.className = 'treasury154-hq-kicker';
    const title = document.createElement('h2');
    const lead = document.createElement('p');
    lead.className = 'treasury154-hq-lead';

    if (kind === 'ricpe') {
      kicker.textContent = 'TRANSPARENCIA Y PRODUCCIÓN DOCUMENTAL · 28 AGOSTO 2026';
      title.textContent = 'Tesoro materializa el acceso reconocido por la Resolución 154/2026.';
      lead.textContent = 'La notificación comunica la puesta a disposición de documentación de contratación y de expedientes de endeudamiento de 2022 a 2025, y mantiene la entrega sucesiva de documentación posterior. Este hito abre una vía de comprobación primaria para las preguntas RIC, financiación y trazabilidad ya formuladas en este registro.';
    } else {
      kicker.textContent = 'PUENTE DOCUMENTAL · TESORO / RIC / REVISIÓN SUPERVISORA';
      title.textContent = 'Una nueva vía de documentación primaria, no una decisión de fondo de CNMV.';
      lead.textContent = 'La materialización del acceso reconocido permite contrastar contratación, endeudamiento, deuda pública apta para RIC y trazabilidad financiera con las preguntas supervisoras delimitadas en esta página. La notificación del Tesoro no modifica la competencia de CNMV ni sustituye una decisión supervisora motivada.';
    }
    head.append(kicker, title, lead);

    const caption = kind === 'ricpe'
      ? '<strong>Imagen de lectura y navegación.</strong> Resume el estado del acceso reconocido y la secuencia de producción. Selecciónela para verla a tamaño completo; el expediente RICPE de responsabilidad documental conserva los extractos oficiales y la explicación probatoria completa.'
      : '<strong>Puente de contraste documental.</strong> La imagen resume la producción comunicada por Tesoro. Su inclusión aquí no atribuye a CNMV conocimiento, aprobación, omisión o conclusión sobre el fondo.';
    const figure = makeFigure(caption);

    const boundaries = document.createElement('div');
    boundaries.className = 'treasury154-hq-boundaries';
    const relevance = document.createElement('article');
    relevance.className = 'treasury154-hq-boundary';
    const limit = document.createElement('article');
    limit.className = 'treasury154-hq-boundary';
    if (kind === 'ricpe') {
      relevance.innerHTML = '<strong>Relevancia documental</strong><p>El derecho de acceso ya fue reconocido y la producción material ha comenzado. Contratación y endeudamiento 2022–2025 forman parte de la entrega actual; la documentación posterior permanece anunciada para entrega sucesiva.</p>';
      limit.innerHTML = '<strong>Límite probatorio</strong><p>La notificación no prueba por sí sola irregularidad RIC/RICPE, uso indebido de fondos, conflicto o responsabilidad. Permite comprobar esas cuestiones mediante archivos primarios.</p>';
    } else {
      relevance.innerHTML = '<strong>Relevancia para la revisión</strong><p>Los archivos producidos pueden ayudar a conciliar fuentes, instrumentos, fechas, aprobaciones, contratación y flujos financieros con el perímetro RICPE sometido a revisión.</p>';
      limit.innerHTML = '<strong>Límite institucional</strong><p>No es una resolución CNMV, no acredita inacción supervisora y no convierte el acceso documental en un hallazgo de infracción. Es una fuente paralela de contraste y preservación.</p>';
    }
    boundaries.append(relevance, limit);

    const actions = document.createElement('div');
    actions.className = 'treasury154-hq-actions';
    const full = document.createElement('a');
    full.className = 'button';
    full.href = fullRecordUrl;
    full.textContent = 'Abrir contexto y extractos oficiales →';
    actions.appendChild(full);
    if (kind === 'cnmv') {
      const ricpe = document.createElement('a');
      ricpe.className = 'button secondary';
      ricpe.href = ricpeUrl;
      ricpe.textContent = 'Registro unitario RICPE';
      actions.appendChild(ricpe);
    } else {
      const cnmv = document.createElement('a');
      cnmv.className = 'button secondary';
      cnmv.href = cnmvUrl;
      cnmv.textContent = 'Puerta de revisión CNMV';
      actions.appendChild(cnmv);
    }

    shell.append(head, figure, boundaries, actions);
    section.appendChild(shell);
    return section;
  };

  const place = () => {
    const [kind] = matched;
    if (kind === 'accountability') {
      upgradeAccountabilityFigure();
      return;
    }
    if (document.querySelector(`[data-treasury154-hq-section="${kind}"]`)) return;
    const main = document.querySelector('main');
    if (!main) return;
    const section = createCrossPageSection(kind);
    const anchor = kind === 'ricpe'
      ? document.querySelector('#pregunta-unitaria')
      : document.querySelector('#revision-7-minutos');
    if (anchor) anchor.insertAdjacentElement('beforebegin', section);
    else main.appendChild(section);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', place, { once: true });
  } else {
    place();
  }
  window.addEventListener('pageshow', place);
})();
