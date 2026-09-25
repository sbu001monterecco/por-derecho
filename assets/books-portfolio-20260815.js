(() => {
  const isEs = document.documentElement.lang === 'es';
  const path = location.pathname;
  const isHome = /\/por-derecho\/(en|es)\/?$/.test(path);
  if (!isHome) return;

  const href = isEs ? 'libros/' : 'books/';
  const main = document.querySelector('main');
  const porDerecho = document.getElementById('por-derecho');

  if (porDerecho && !porDerecho.querySelector('[data-books-portfolio]')) {
    const shell = porDerecho.querySelector('.shell');
    if (shell) {
      const block = document.createElement('article');
      block.className = 'entity-note';
      block.setAttribute('data-books-portfolio','');
      block.innerHTML = isEs
        ? `<p class="kicker">Gil Marer · libros en publicación</p><h3>Seis libros · seis formas de leer la experiencia</h3><p><strong>Razón para creer</strong> · <strong>Law-mower Man</strong> · <strong>The SunRockers</strong> · <strong>Justicia en fragmentos</strong> · <strong>Situaciones Especiales</strong> · <strong>4 Green Houses, One Red Hotel</strong>.</p><p>Estado de derecho y memoria del caso, IA y memoria jurídica, comunidad 50+, fragmentación institucional, mercados distressed/NPL y responsabilidad profesional.</p><div class="actions"><a class="button" href="${href}">Ver todos los libros</a></div>`
        : `<p class="kicker">Gil Marer · books in publication</p><h3>Six books · six ways into the experience</h3><p><strong>Reason to Believe</strong> · <strong>Law-mower Man</strong> · <strong>The SunRockers</strong> · <strong>Justice in Pieces</strong> · <strong>Special Situations</strong> · <strong>4 Green Houses, One Red Hotel</strong>.</p><p>Rule of law and single-case memory, AI and legal memory, the 50+ community, institutional fragmentation, distressed/NPL markets and professional accountability.</p><div class="actions"><a class="button" href="${href}">Explore all books</a></div>`;
      shell.appendChild(block);
    }
  }

  if (main && !document.querySelector('[data-books-footer-link]')) {
    const section = document.createElement('section');
    section.className = 'section alt';
    section.setAttribute('data-books-footer-link','');
    section.innerHTML = isEs
      ? `<div class="shell"><p class="kicker">Publicaciones</p><h2>Libros en publicación · de próxima aparición</h2><p>El programa editorial de Gil Marer desarrolla seis libros distintos. Las descripciones y portadas son públicas; los manuscritos completos permanecen en el repositorio privado de trabajo.</p><div class="actions"><a class="button" href="${href}">Abrir la página de libros</a></div></div>`
      : `<div class="shell"><p class="kicker">Publishing</p><h2>Books in publication · coming shortly</h2><p>Gil Marer's publishing programme is developing six distinct books. Descriptions and covers are public; the full manuscripts remain in the private working repository.</p><div class="actions"><a class="button" href="${href}">Open the books page</a></div></div>`;
    main.appendChild(section);
  }

  const footer = document.querySelector('.site-footer');
  if (footer && !footer.querySelector('[data-books-footer-nav]')) {
    const footerLinks = footer.querySelector('.footer-links');
    if (footerLinks) {
      const link = document.createElement('a');
      link.href = href;
      link.setAttribute('data-books-footer-nav','');
      link.setAttribute('aria-label', isEs ? 'Abrir libros de Gil Marer' : 'Open Gil Marer books');
      link.innerHTML = isEs ? '▣ <strong>Libros</strong>' : '▣ <strong>Books</strong>';
      footerLinks.insertBefore(link, footerLinks.firstChild);
    }

    const footerIntro = footer.querySelector('.footer-grid > div:first-child');
    if (footerIntro) {
      const badge = document.createElement('p');
      badge.setAttribute('data-books-footer-nav','');
      badge.innerHTML = isEs
        ? `<a href="${href}" style="font-weight:700">▣ Gil Marer · Libros en publicación →</a>`
        : `<a href="${href}" style="font-weight:700">▣ Gil Marer · Books in publication →</a>`;
      footerIntro.appendChild(badge);
    }
  }
})();
