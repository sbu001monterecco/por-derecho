(() => {
  const path = window.location.pathname;
  const isEs = path.includes('/es/canarias7-articulo-30mayo2022/');
  const isEn = path.includes('/en/canarias7-article-30may2022/');
  if (!isEs && !isEn) return;

  const section = document.querySelector(isEs ? '#articulo .shell' : '#article .shell');
  if (!section || section.querySelector('[data-c7-preview]')) return;

  const figure = document.createElement('figure');
  figure.dataset.c7Preview = 'true';
  figure.style.margin = '1.5rem 0 2rem';
  figure.style.padding = '0';

  const link = document.createElement('a');
  link.href = '../../assets/canarias7-article-30may2022-preview.jpg';
  link.target = '_blank';
  link.rel = 'noopener';
  link.setAttribute('aria-label', isEs ? 'Abrir la reproducción preservada del artículo de Canarias7' : 'Open the preserved reproduction of the Canarias7 article');

  const img = document.createElement('img');
  img.src = '../../assets/canarias7-article-30may2022-preview.jpg';
  img.alt = isEs
    ? 'Reproducción preservada del artículo de Canarias7 de 30 de mayo de 2022 firmado por Francisco José Fajardo'
    : 'Preserved reproduction of the 30 May 2022 Canarias7 article by Francisco José Fajardo';
  img.loading = 'eager';
  img.decoding = 'async';
  img.style.display = 'block';
  img.style.width = '100%';
  img.style.maxWidth = '980px';
  img.style.height = 'auto';
  img.style.margin = '0 auto';
  img.style.border = '1px solid rgba(20,35,45,.18)';
  img.style.borderRadius = '14px';
  img.style.boxShadow = '0 12px 34px rgba(20,35,45,.12)';
  img.style.background = '#fff';

  const caption = document.createElement('figcaption');
  caption.style.maxWidth = '980px';
  caption.style.margin = '.65rem auto 0';
  caption.style.fontSize = '.92rem';
  caption.style.lineHeight = '1.45';
  caption.style.color = '#52616b';
  caption.innerHTML = isEs
    ? '<strong>Reproducción preservada.</strong> Vista previa del artículo de Canarias7 de 30/05/2022. Pulse la imagen para abrirla a tamaño completo. Se publica como evidencia de la existencia y contenido de la publicación, no como prueba de culpabilidad ni de los hechos Sun Park.'
    : '<strong>Preserved reproduction.</strong> Preview of the 30 May 2022 Canarias7 article. Click the image to open it full size. It is shown as evidence of the publication\'s existence and content, not as proof of guilt or of the Sun Park allegations.';

  link.appendChild(img);
  figure.appendChild(link);
  figure.appendChild(caption);

  const heading = section.querySelector('h2');
  if (heading && heading.nextSibling) {
    heading.parentNode.insertBefore(figure, heading.nextSibling);
  } else {
    section.prepend(figure);
  }
})();
