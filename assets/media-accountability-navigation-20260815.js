(() => {
  const path = location.pathname;
  const isEs = path.includes('/es/');
  const href = isEs ? '../canarias7-articulo-30mayo2022/' : '../canarias7-article-30may2022/';

  if (path.includes('quien-debe-responder-que') || path.includes('who-should-answer-what')) {
    const grid = document.querySelector('.card-grid');
    if (grid && !grid.querySelector('[data-canarias7-card]')) {
      const card = document.createElement('article');
      card.className = 'card';
      card.dataset.canarias7Card = 'true';
      card.innerHTML = isEs
        ? '<h3>Canarias7 / Francisco José Fajardo / INFORCASA</h3><p><strong>Pregunta:</strong> ¿qué documento sustentó el artículo de 30/05/2022, qué ocurrió después y qué registro editorial explica su retirada o despublicación?</p><p><a href="../canarias7-articulo-30mayo2022/">Ver trazabilidad editorial →</a></p>'
        : '<h3>Canarias7 / Francisco José Fajardo / INFORCASA</h3><p><strong>Question:</strong> what document supported the 30 May 2022 article, what happened afterwards, and what editorial record explains its removal or unpublishing?</p><p><a href="../canarias7-article-30may2022/">Open editorial traceability →</a></p>';
      grid.appendChild(card);
    }
  }

  if (path.includes('acosta-matos-perimetro') || path.includes('acosta-matos-perimeter') || path.includes('carta-abierta-ministerio-fiscal') || path.includes('open-letter-public-prosecution-service')) {
    const main = document.querySelector('main');
    if (main && !document.querySelector('[data-canarias7-related]')) {
      const section = document.createElement('section');
      section.className = 'section alt';
      section.dataset.canarias7Related = 'true';
      section.innerHTML = isEs
        ? `<div class="shell"><h2>Registro periodístico relacionado: Canarias7, 30 mayo 2022</h2><p>Una noticia separada sobre una acusación atribuida a Fiscalía en el entorno Acosta Matos fue preservada y posteriormente dejó de estar accesible. No la tratamos como prueba de Sun Park; la tratamos como cuestión de autenticación y trazabilidad editorial.</p><p><a href="${href}"><strong>Ver artículo, contexto y mensaje abierto a Canarias7 →</strong></a></p></div>`
        : `<div class="shell"><h2>Related press record: Canarias7, 30 May 2022</h2><p>A separate report concerning a prosecution accusation in the Acosta Matos business environment was preserved and later ceased to be accessible. We do not treat it as proof of Sun Park allegations; we treat it as an authentication and editorial-traceability question.</p><p><a href="${href}"><strong>Open article context and message to Canarias7 →</strong></a></p></div>`;
      main.appendChild(section);
    }
  }
})();