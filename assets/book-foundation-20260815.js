(() => {
  const isEs = document.documentElement.lang === 'es';

  const porDerecho = document.getElementById('por-derecho');
  if (porDerecho && !porDerecho.querySelector('[data-por-derecho-book]')) {
    const shell = porDerecho.querySelector('.shell');
    if (shell) {
      const card = document.createElement('article');
      card.className = 'entity-note';
      card.setAttribute('data-por-derecho-book', '');
      card.setAttribute('aria-labelledby', isEs ? 'por-derecho-book-title-es' : 'por-derecho-book-title-en');

      if (isEs) {
        card.innerHTML = `
          <p class="kicker">Próximo libro · Playa Blanca · SunRockers</p>
          <h3 id="por-derecho-book-title-es">Razón para creer <span lang="en">· Reason to Believe</span></h3>
          <p><strong>UN ACTIVO. UNA HISTORIA.</strong> Antes de convertirse en un expediente, Sun Park fue un lugar al que la gente venía a quedarse, volver, hacer amigos y formar parte de una comunidad. El libro une esa experiencia SunRockers con la historia del mismo lugar hoy conocido como MYND Yaiza y con la reconstrucción documental de lo ocurrido entre ambas etapas.</p>
          <p><strong>La evidencia explica qué ocurrió. El libro recuerda qué importaba.</strong></p>
          <p class="qualification">Proyecto editorial y educativo asociado a Fundación Por Derecho. La asociación no implica por sí misma cesión de derechos de autor, regalías u otros derechos comerciales; una compra y una eventual donación son operaciones distintas.</p>
          <div class="actions"><a class="button" href="libro/">Descubrir Sun Park y los SunRockers</a><a class="button secondary" href="proyecto-conocimiento/">Examinar la evidencia y el método</a></div>`;
      } else {
        card.innerHTML = `
          <p class="kicker">Upcoming book · Playa Blanca · SunRockers</p>
          <h3 id="por-derecho-book-title-en">Reason to Believe <span lang="es">· Razón para creer</span></h3>
          <p><strong>ONE ASSET. ONE HISTORY.</strong> Before it became a case file, Sun Park was a place people came to stay, return, make friends and belong. The book connects that SunRockers experience with the story of the same place now known as MYND Yaiza and the documentary reconstruction of what happened in between.</p>
          <p><strong>The evidence explains what happened. The book remembers what mattered.</strong></p>
          <p class="qualification">A publishing and educational project associated with Fundación Por Derecho. Association does not by itself assign copyright, royalties or other commercial rights; a purchase and any future donation are distinct transactions.</p>
          <div class="actions"><a class="button" href="book/">Discover Sun Park and the SunRockers</a><a class="button secondary" href="knowledge-project/">Examine the evidence and method</a></div>`;
      }
      shell.appendChild(card);
    }
  }

  const knowledgeMain = document.querySelector('main');
  const isKnowledgePage = document.getElementById(isEs ? 'metodo' : 'method') && document.getElementById(isEs ? 'reto' : 'challenge');
  if (knowledgeMain && isKnowledgePage && !document.querySelector('[data-research-continuity]')) {
    const section = document.createElement('section');
    section.className = 'section';
    section.setAttribute('data-research-continuity', '');
    const href = isEs ? 'continuidad/' : 'continuity/';
    section.innerHTML = isEs
      ? `<div class="shell"><p class="kicker">Continuidad de investigación</p><h2>Este trabajo no debe depender de un único hilo de ChatGPT.</h2><p>El repositorio conserva una capa pública de continuidad con la arquitectura evidencial, decisiones de diseño, auditoría de corpus/tokens, plan de ejecución y límites entre libro, Fundación Por Derecho y Havidia. Las fuentes privadas siguen en sus sistemas de origen y deben consultarse cuando sean necesarias.</p><div class="actions"><a class="button" href="${href}">Abrir la guía de continuidad</a></div></div>`
      : `<div class="shell"><p class="kicker">Research continuity</p><h2>This work should not depend on one ChatGPT thread.</h2><p>The repository preserves a public continuity layer covering the evidence architecture, design decisions, corpus/token audit, execution plan, and boundaries between the book, Fundación Por Derecho and Havidia. Private sources remain in their source systems and must be searched when needed.</p><div class="actions"><a class="button" href="${href}">Open the continuity guide</a></div></div>`;
    knowledgeMain.appendChild(section);
  }
})();
