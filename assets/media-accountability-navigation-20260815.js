(() => {
  const path = location.pathname;
  const isEs = path.includes('/es/');
  const c7Href = isEs ? '../canarias7-articulo-30mayo2022/' : '../canarias7-article-30may2022/';
  const ecoHref = isEs ? '../eleconomista-javier-romera-enero2025/' : '../eleconomista-javier-romera-january2025/';

  if (path.includes('quien-debe-responder-que') || path.includes('who-should-answer-what')) {
    const grid = document.querySelector('.card-grid');
    if (grid && !grid.querySelector('[data-canarias7-card]')) {
      const card = document.createElement('article'); card.className='card'; card.dataset.canarias7Card='true';
      card.innerHTML = isEs
        ? '<h3>Canarias7 / Francisco José Fajardo / INFORCASA</h3><p><strong>Pregunta:</strong> ¿qué documento sustentó el artículo de 30/05/2022, qué ocurrió después y qué registro editorial explica su retirada o despublicación?</p><p><a href="../canarias7-articulo-30mayo2022/">Ver trazabilidad editorial →</a></p>'
        : '<h3>Canarias7 / Francisco José Fajardo / INFORCASA</h3><p><strong>Question:</strong> what document supported the 30 May 2022 article, what happened afterwards, and what editorial record explains its removal or unpublishing?</p><p><a href="../canarias7-article-30may2022/">Open editorial traceability →</a></p>';
      grid.appendChild(card);
    }
    if (grid && !grid.querySelector('[data-eleconomista-card]')) {
      const card = document.createElement('article'); card.className='card'; card.dataset.eleconomistaCard='true';
      card.innerHTML = isEs
        ? '<h3>elEconomista / Javier Romera / Editorial Ecoprensa</h3><p><strong>Pregunta:</strong> una investigación de interés público sobre comercialización, Meeting Point/FTI, RIC, financiación pública y fondos europeos seguía abierta el 17/01/2025; tras recibirse un auto, el 20/01 se comunicó que no podía publicarse. ¿Qué ocurrió entre ambos momentos?</p><p><a href="../eleconomista-javier-romera-enero2025/">Ver trazabilidad editorial →</a></p>'
        : '<h3>elEconomista / Javier Romera / Editorial Ecoprensa</h3><p><strong>Question:</strong> a public-interest investigation concerning commercialisation, Meeting Point/FTI, RIC, public finance and European funds remained open on 17 Jan 2025; after a court order was received, non-publication was communicated on 20 Jan. What happened between those points?</p><p><a href="../eleconomista-javier-romera-january2025/">Open editorial traceability →</a></p>';
      grid.appendChild(card);
    }
  }

  if (path.includes('canarias7-articulo-30mayo2022') || path.includes('canarias7-article-30may2022')) {
    const firstSection = document.querySelector('section.section');
    if (firstSection && !document.querySelector('[data-fiscal-verification]')) {
      const note = document.createElement('div'); note.className='shell'; note.dataset.fiscalVerification='true';
      note.innerHTML = isEs
        ? '<p class="safe"><strong>Fiscal firmante: nivel de verificación.</strong> La copia preservada permite afirmar que el artículo identificaba al <strong>fiscal Luis Estévez</strong> como quien suscribía el escrito de acusación. Aún no hemos localizado en el corpus una copia certificada del escrito fiscal o del expediente que permita verificar de forma independiente su identidad completa, adscripción y si fue el fiscal responsable durante toda la causa. Por ello no usamos todavía la expresión «fiscal que lideró toda la acusación» como hecho cerrado.</p>'
        : '<p class="safe"><strong>Signing prosecutor: verification level.</strong> The preserved copy supports saying that the article identified <strong>prosecutor Luis Estévez</strong> as the person who signed the prosecution filing. We have not yet located a certified copy of that filing or the case record independently establishing his full identity, assignment, or whether he remained the responsible prosecutor throughout the proceedings. We therefore do not yet state that he “led the entire prosecution” as an established fact.</p>';
      firstSection.appendChild(note);
    }
  }

  if (path.includes('acosta-matos-perimetro') || path.includes('acosta-matos-perimeter') || path.includes('carta-abierta-ministerio-fiscal') || path.includes('open-letter-public-prosecution-service')) {
    const main = document.querySelector('main');
    if (main && !document.querySelector('[data-media-related]')) {
      const section = document.createElement('section'); section.className='section alt'; section.dataset.mediaRelated='true';
      section.innerHTML = isEs
        ? `<div class="shell"><h2>Registros periodísticos relacionados</h2><p><strong>Canarias7 (30/05/2022):</strong> acusación fiscal publicada y posterior despublicación, tratada como cuestión de autenticación y custodia editorial, no como prueba de Sun Park. <a href="${c7Href}">Ver →</a></p><p><strong>elEconomista / Javier Romera (enero 2025):</strong> investigación de interés público sobre comercialización, Meeting Point/FTI, RIC, financiación pública y fondos europeos; el 17 de enero seguía en contraste y el 20 se comunicó la no publicación después de recibirse un auto. La transmisión y su caracterización siguen abiertas. <a href="${ecoHref}">Ver →</a></p></div>`
        : `<div class="shell"><h2>Related press records</h2><p><strong>Canarias7 (30 May 2022):</strong> a reported prosecution accusation followed by unpublishing, treated as an authentication and editorial-custody question, not proof of Sun Park allegations. <a href="${c7Href}">Open →</a></p><p><strong>elEconomista / Javier Romera (January 2025):</strong> a public-interest investigation concerning commercialisation, Meeting Point/FTI, RIC, public finance and European funds; verification remained open on 17 January and non-publication was communicated on 20 January after a court order was received. The transmission and its characterisation remain open. <a href="${ecoHref}">Open →</a></p></div>`;
      main.appendChild(section);
    }
  }
})();