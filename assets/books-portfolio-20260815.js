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
        ? `<p class="kicker">Gil Marer · libros en publicación</p><h3>Cinco libros · cinco formas de leer la misma experiencia</h3><p><strong>Razón para creer</strong> · <strong>Law-mower Man</strong> · <strong>The SunRockers</strong> · <strong>Justicia en fragmentos</strong> · <strong>Situaciones Especiales</strong>.</p><p>Historia humana, IA y memoria jurídica, comunidad, instituciones y el submundo financiero de NPL, claims trading, defaults y special situations como oportunidad de inversión.</p><div class="actions"><a class="button" href="${href}">Ver todos los libros</a></div>`
        : `<p class="kicker">Gil Marer · books in publication</p><h3>Five books · five ways into the same experience</h3><p><strong>Reason to Believe</strong> · <strong>Law-mower Man</strong> · <strong>The SunRockers</strong> · <strong>Justice in Pieces</strong> · <strong>Special Situations</strong>.</p><p>Human story, AI and legal memory, community, institutions, and the largely unseen financial world of NPLs, claims trading, defaults and special-situations investing.</p><div class="actions"><a class="button" href="${href}">Explore all books</a></div>`;
      shell.appendChild(block);
    }
  }

  if (main && !document.querySelector('[data-books-footer-link]')) {
    const section = document.createElement('section');
    section.className = 'section alt';
    section.setAttribute('data-books-footer-link','');
    section.innerHTML = isEs
      ? `<div class="shell"><p class="kicker">Publicaciones</p><h2>Libros en publicación · de próxima aparición</h2><p>El programa editorial de Gil Marer desarrolla cinco libros distintos a partir del trabajo de Sun Park, Por Derecho y el Proyecto de Conocimiento.</p><div class="actions"><a class="button" href="${href}">Abrir la página de libros</a></div></div>`
      : `<div class="shell"><p class="kicker">Publishing</p><h2>Books in publication · coming shortly</h2><p>Gil Marer's publishing programme is developing five distinct books from the Sun Park, Por Derecho and Knowledge Project work.</p><div class="actions"><a class="button" href="${href}">Open the books page</a></div></div>`;
    main.appendChild(section);
  }
})();
