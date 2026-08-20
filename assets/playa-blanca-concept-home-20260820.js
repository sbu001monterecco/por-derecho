(() => {
  const current = document.currentScript;
  if (!current) return;

  const path = window.location.pathname.replace(/index\.html$/, '');
  const isEnglishHome = /\/en\/?$/.test(path);
  const isSpanishHome = /\/es\/?$/.test(path);
  if (!isEnglishHome && !isSpanishHome) return;

  if (!document.querySelector('link[data-playa-blanca-concept-css]')) {
    const css = document.createElement('link');
    css.rel = 'stylesheet';
    css.href = new URL('playa-blanca-concept.css?v=20260820a', current.src).href;
    css.setAttribute('data-playa-blanca-concept-css', 'true');
    document.head.appendChild(css);
  }

  const imageHref = new URL('playa-blanca-return-poster.svg', current.src).href;

  const copy = isEnglishHome
    ? {
        sectionId: 'future',
        route: 'playa-blanca-hotel-services-concept/',
        tag: 'Playa Blanca · Yaiza',
        title: 'A new hotel and local-services concept',
        body: 'A separate 100% hotel opportunity in southern Lanzarote, close to Playa Blanca’s town and ferry harbour, designed around a green inward resort and a useful outward commercial edge.',
        confidence: 'Recovery and reinvestment can proceed in parallel. Our confidence in Playa Blanca remains intact.',
        status: 'Private opportunity review · no approval or endorsement implied',
        link: 'Explore the concept →',
        alt: 'Art Deco-inspired illustrative concept poster for a hotel and local-services development in Playa Blanca',
        caption: 'Illustrative concept · exact private site not identified.'
      }
    : {
        sectionId: 'futuro',
        route: 'playa-blanca-concepto-hotel-servicios/',
        tag: 'Playa Blanca · Yaiza',
        title: 'Un nuevo concepto hotelero y de servicios locales',
        body: 'Una oportunidad independiente, 100% hotelera, en el sur de Lanzarote, próxima al pueblo y al puerto de ferris de Playa Blanca, concebida alrededor de un resort interior verde y un borde comercial útil hacia fuera.',
        confidence: 'Recuperación y reinversión pueden avanzar en paralelo. Nuestra confianza en Playa Blanca sigue intacta.',
        status: 'Oportunidad en revisión privada · no se implica aprobación o respaldo',
        link: 'Explorar el concepto →',
        alt: 'Cartel conceptual inspirado en el Art Déco para un desarrollo hotelero y de servicios locales en Playa Blanca',
        caption: 'Concepto ilustrativo · no se identifica el solar privado exacto.'
      };

  const inject = () => {
    const future = document.getElementById(copy.sectionId);
    if (!future || future.querySelector('[data-playa-blanca-home-feature]')) return;
    const heading = future.querySelector('.section-head');
    if (!heading) return;

    const card = document.createElement('article');
    card.className = 'pb-home-feature';
    card.setAttribute('data-playa-blanca-home-feature', 'true');
    card.setAttribute('aria-label', copy.title);
    card.innerHTML = `
      <div class="pb-home-feature-copy">
        <span class="pb-home-tag">${copy.tag}</span>
        <h3>${copy.title}</h3>
        <p>${copy.body}</p>
        <p><strong>${copy.confidence}</strong></p>
        <p class="pb-home-status">${copy.status}</p>
        <a href="${copy.route}">${copy.link}</a>
      </div>
      <figure>
        <img src="${imageHref}" width="1600" height="1000" loading="lazy" alt="${copy.alt}">
        <figcaption>${copy.caption}</figcaption>
      </figure>`;
    heading.insertAdjacentElement('afterend', card);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inject, { once: true });
  } else {
    inject();
  }
})();