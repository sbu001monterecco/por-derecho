(() => {
  const path = window.location.pathname.replace(/\/+$/, '/');
  const isEn = path.endsWith('/en/cuatrecasas-sun-park/');
  const isEs = path.endsWith('/es/cuatrecasas-sun-park/');
  if (!isEn && !isEs) return;
  if (document.querySelector('[data-four-green-houses-cover-link]')) return;

  const base = path.includes('/es/') ? '../' : '../';
  const bookHref = isEn
    ? '../books/four-green-houses-one-red-hotel/'
    : '../libros/four-green-houses-one-red-hotel/';
  const imageHref = '../../assets/book-covers/locked/four-green-houses-one-red-hotel.jpg';

  const section = document.createElement('section');
  section.className = 'section alt';
  section.setAttribute('data-four-green-houses-cover-link', '20260831');
  section.innerHTML = `
    <div class="shell record">
      <div style="display:grid;grid-template-columns:minmax(230px,.72fr) minmax(0,1.28fr);gap:clamp(1.2rem,4vw,2.4rem);align-items:center;background:#0f252c;color:#fff;border-radius:22px;padding:clamp(1rem,3vw,1.7rem);box-shadow:0 20px 48px rgba(15,37,44,.2)">
        <a href="${bookHref}" aria-label="${isEn ? 'Open 4 Green Houses, One Red Hotel' : 'Abrir 4 Green Houses, One Red Hotel'}" style="display:block">
          <img src="${imageHref}" alt="4 Green Houses, One Red Hotel" width="500" height="625" loading="lazy" style="display:block;width:100%;height:auto;border-radius:14px;box-shadow:0 14px 34px rgba(0,0,0,.35)">
        </a>
        <div>
          <p class="eyeline" style="color:#f3d17a">${isEn ? 'BOOK · VISUAL METAPHOR · DOCUMENTARY RECORD' : 'LIBRO · METÁFORA VISUAL · REGISTRO DOCUMENTAL'}</p>
          <h2 style="color:#fff;margin:.25rem 0 .7rem">4 Green Houses, One Red Hotel</h2>
          <p style="font-size:1.08rem;line-height:1.65;color:#e7eeee">${isEn
            ? 'Four green houses surround one red hotel: an original visual metaphor for professional readiness, fragmented legal structures and one real hotel under legal and economic pressure. The artwork is a narrative device, not a finding of liability and not an assertion that any actor joined a common plan.'
            : 'Cuatro casas verdes rodean un hotel rojo: una metáfora visual original sobre preparación profesional, fragmentación jurídica y un hotel real sometido a presión jurídica y económica. La imagen es un recurso narrativo, no una declaración de responsabilidad ni una afirmación de que ningún actor se integró en un plan común.'}</p>
          <p style="line-height:1.55;color:#cfdcdb">${isEn
            ? 'The book landing page connects the metaphor to the controlled record: mandate → knowledge → act or omission → communication → fee-enforcement inversion → causation, defence and remedy.'
            : 'La página del libro conecta la metáfora con el registro controlado: mandato → conocimiento → acción u omisión → comunicación → inversión por ejecución de honorarios → causalidad, defensa y remedio.'}</p>
          <p><a class="button" href="${bookHref}" style="background:#f3d17a;color:#10262d">${isEn ? 'Open the book landing page →' : 'Abrir la página del libro →'}</a></p>
          <p class="small" style="color:#cfdcdb;margin-bottom:0">${isEn
            ? 'Independent editorial artwork. No Monopoly® logo, board, mascot, cards, typography or branded game pieces are used.'
            : 'Obra editorial independiente. No se utilizan el logotipo Monopoly®, el tablero, la mascota, las tarjetas, la tipografía ni las piezas de juego de marca.'}</p>
        </div>
      </div>
    </div>`;

  const hero = document.querySelector('main > .hero, main .hero');
  if (hero && hero.parentNode) hero.insertAdjacentElement('afterend', section);
  else document.querySelector('main')?.prepend(section);

  const style = document.createElement('style');
  style.textContent = '@media(max-width:760px){[data-four-green-houses-cover-link]>div>div{grid-template-columns:1fr!important}[data-four-green-houses-cover-link] img{max-width:420px;margin:0 auto}}';
  document.head.appendChild(style);
})();
