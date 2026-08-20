(() => {
  const current = document.currentScript;
  if (!current) return;

  const path = window.location.pathname.replace(/index\.html$/, '');
  const isEnglishHome = /\/en\/?$/.test(path);
  const isSpanishHome = /\/es\/?$/.test(path);
  if (!isEnglishHome && !isSpanishHome) return;

  const ensureCss = (marker, href) => {
    if (document.querySelector(`link[${marker}]`)) return;
    const css = document.createElement('link');
    css.rel = 'stylesheet';
    css.href = new URL(href, current.src).href;
    css.setAttribute(marker, 'true');
    document.head.appendChild(css);
  };

  ensureCss('data-playa-blanca-concept-css', 'playa-blanca-concept.css?v=20260820a');
  ensureCss('data-project-horizon-css', 'project-horizon-20260820.css?v=20260820a');

  const playaImage = new URL('playa-blanca-return-poster.svg', current.src).href;
  const horizonImage = new URL('project-horizon-hero.svg', current.src).href;

  const playa = isEnglishHome
    ? {
        sectionId: 'future', route: 'playa-blanca-hotel-services-concept/', tag: 'Playa Blanca · Yaiza',
        title: 'A new hotel and local-services concept',
        body: 'A separate 100% hotel opportunity in southern Lanzarote, close to Playa Blanca’s town and ferry harbour, designed around a green inward resort and a useful outward commercial edge.',
        confidence: 'Recovery and reinvestment can proceed in parallel. Our confidence in Playa Blanca remains intact.',
        status: 'Private opportunity review · no approval or endorsement implied', link: 'Explore the concept →',
        alt: 'Art Deco-inspired illustrative concept poster for a hotel and local-services development in Playa Blanca',
        caption: 'Illustrative concept · exact private site not identified.'
      }
    : {
        sectionId: 'futuro', route: 'playa-blanca-concepto-hotel-servicios/', tag: 'Playa Blanca · Yaiza',
        title: 'Un nuevo concepto hotelero y de servicios locales',
        body: 'Una oportunidad independiente, 100% hotelera, en el sur de Lanzarote, próxima al pueblo y al puerto de ferris de Playa Blanca, concebida alrededor de un resort interior verde y un borde comercial útil hacia fuera.',
        confidence: 'Recuperación y reinversión pueden avanzar en paralelo. Nuestra confianza en Playa Blanca sigue intacta.',
        status: 'Oportunidad en revisión privada · no se implica aprobación o respaldo', link: 'Explorar el concepto →',
        alt: 'Cartel conceptual inspirado en el Art Déco para un desarrollo hotelero y de servicios locales en Playa Blanca',
        caption: 'Concepto ilustrativo · no se identifica el solar privado exacto.'
      };

  const horizon = isEnglishHome
    ? {
        sectionId: 'future', route: 'tenerife-south-active-holiday-community/', tag: 'Project Horizon · Tenerife South',
        title: 'Stay longer. Live better.',
        body: 'A live redevelopment workstream for a hospitality-led active holiday community in the municipality of Adeje: flexible stays, community, sport and wellness designed primarily around independent adults 50+.',
        status: 'Live redevelopment · private site · hospitality, not residential · no approval implied',
        link: 'Explore Project Horizon →',
        alt: 'Illustrative mid-century-inspired poster for Project Horizon, a Tenerife South active holiday community',
        caption: 'Illustrative redevelopment concept · exact private site not identified.'
      }
    : {
        sectionId: 'futuro', route: 'tenerife-sur-comunidad-vacacional-activa/', tag: 'Project Horizon · Tenerife Sur',
        title: 'Quédate más. Vive mejor.',
        body: 'Una línea activa de reposicionamiento para una comunidad vacacional hotelera en el municipio de Adeje: estancias flexibles, comunidad, deporte y bienestar, concebidos principalmente para adultos independientes de 50+.',
        status: 'Reposicionamiento activo · ubicación privada · hotelero, no residencial · sin aprobación implícita',
        link: 'Explorar Project Horizon →',
        alt: 'Cartel ilustrativo de inspiración mid-century para Project Horizon, comunidad vacacional activa en Tenerife Sur',
        caption: 'Concepto ilustrativo de reposicionamiento · no se identifica la ubicación privada exacta.'
      };

  const inject = () => {
    const future = document.getElementById(playa.sectionId);
    if (!future) return;
    const heading = future.querySelector('.section-head');
    if (!heading) return;

    let playaCard = future.querySelector('[data-playa-blanca-home-feature]');
    if (!playaCard) {
      playaCard = document.createElement('article');
      playaCard.className = 'pb-home-feature';
      playaCard.setAttribute('data-playa-blanca-home-feature', 'true');
      playaCard.setAttribute('aria-label', playa.title);
      playaCard.innerHTML = `
        <div class="pb-home-feature-copy">
          <span class="pb-home-tag">${playa.tag}</span>
          <h3>${playa.title}</h3>
          <p>${playa.body}</p>
          <p><strong>${playa.confidence}</strong></p>
          <p class="pb-home-status">${playa.status}</p>
          <a href="${playa.route}">${playa.link}</a>
        </div>
        <figure>
          <img src="${playaImage}" width="1600" height="1000" loading="lazy" alt="${playa.alt}">
          <figcaption>${playa.caption}</figcaption>
        </figure>`;
      heading.insertAdjacentElement('afterend', playaCard);
    }

    if (!future.querySelector('[data-project-horizon-home-feature]')) {
      const horizonCard = document.createElement('article');
      horizonCard.className = 'hz-home-feature';
      horizonCard.setAttribute('data-project-horizon-home-feature', 'true');
      horizonCard.setAttribute('aria-label', horizon.title);
      horizonCard.innerHTML = `
        <div class="hz-home-feature-copy">
          <span class="hz-home-tag">${horizon.tag}</span>
          <h3>${horizon.title}</h3>
          <p>${horizon.body}</p>
          <p class="hz-home-status">${horizon.status}</p>
          <a href="${horizon.route}">${horizon.link}</a>
        </div>
        <figure>
          <img src="${horizonImage}" width="1600" height="1000" loading="lazy" alt="${horizon.alt}">
          <figcaption>${horizon.caption}</figcaption>
        </figure>`;
      playaCard.insertAdjacentElement('afterend', horizonCard);
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', inject, { once: true });
  else inject();
})();
