(() => {
  const normalise = value => {
    const path = value.replace(/\/index\.html$/, '/');
    return path.endsWith('/') ? path : `${path}/`;
  };
  const path = normalise(location.pathname);
  const targets = new Set([
    '/es/ingenieria-forense-criminal-sun-park/',
    '/en/sun-park-criminal-engineering-investigation/',
    '/es/ingenieria-inversa-criminal-unitaria/',
    '/en/unitary-criminal-reverse-engineering/',
    '/es/recuperacion-activos-intervencion-decomiso/',
    '/en/asset-recovery-intervention-confiscation/'
  ]);
  const route = [...targets].find(target => path.endsWith(target));
  const main = document.querySelector('main');
  if (!route || !main || document.querySelector('[data-criminal-public-boundaries]')) return;

  const english = document.documentElement.lang === 'en';
  const prefix = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const charter = english
    ? `${prefix}en/criminal-law-reading-rules/`
    : `${prefix}es/reglas-lectura-derecho-penal/`;
  const copy = english
    ? {
        eyebrow: 'PUBLIC CRIMINAL-LAW SAFEGUARD',
        title: 'Evidence first. Individual attribution. No collective guilt.',
        text: 'A sequence is not a plan; a relationship is not responsibility; receipt is not endorsement; an adverse decision or legal error is not criminal intent. Each hypothesis requires an act, authority, authorship, knowledge, intent where required, prejudice, benefit, causation and contrary evidence.',
        link: 'Read the criminal-law reading rules →',
        engineTitle: 'Forensic reconstruction of contested acts · criminal-law questions actor by actor | Por Derecho',
        engineDescription: 'Evidence-led reconstruction of contested credit, authority, control, title, finance and operation. It tests criminal-law hypotheses actor by actor without collective attribution.',
        engineEyebrow: 'LIVE INVESTIGATION · SOURCES · AUTHORITY · CAUSATION · CONTRADICTION',
        engineHeading: 'A documentary sequence requires separate questions, not a collective conclusion.',
        engineLead: 'Por Derecho tests whether identified acts had a lawful authority, documented source, individual author, relevant knowledge, causal effect and traceable benefit. A chronology does not prove a common plan or criminal responsibility.',
        engineAllegation: '<strong>POR DERECHO INVESTIGATIVE HYPOTHESES · NOT JUDICIAL FINDINGS</strong><p>No person or entity is publicly categorised as an “enabler”. Any criminal-law hypothesis must be proved or disproved actor by actor, act by act and element by element, including the strongest contrary evidence and innocent explanation.</p>',
        ladderTitle: 'No public “enabler” scale',
        ladderText: 'Public material does not assign ranks of facilitation, knowledge or culpability. A role can be examined only through a specific act, source, authority, knowledge, intent, causal contribution, contrary evidence and competent outcome.',
        scoreText: 'Any numerical marker is an evidence-collection priority only. It is not proof, a probability of conviction, a finding about a person or entity, or a forecast of an official outcome.'
      }
    : {
        eyebrow: 'GARANTÍA PÚBLICA DE DERECHO PENAL',
        title: 'Prueba primero. Atribución individual. Sin culpabilidad colectiva.',
        text: 'Una secuencia no es un plan; una relación no es responsabilidad; una recepción no es respaldo; una decisión adversa o un error jurídico no son dolo penal. Cada hipótesis exige acto, autoridad, autoría, conocimiento, dolo cuando proceda, perjuicio, beneficio, causalidad y prueba contraria.',
        link: 'Leer las reglas de lectura penal →',
        engineTitle: 'Reconstrucción forense de actos controvertidos · preguntas penales actor por actor | Por Derecho',
        engineDescription: 'Reconstrucción probatoria de crédito, autoridad, control, título, financiación y explotación controvertidos. Comprueba hipótesis penales actor por actor, sin atribución colectiva.',
        engineEyebrow: 'INVESTIGACIÓN VIVA · FUENTES · AUTORIDAD · CAUSALIDAD · CONTRADICCIÓN',
        engineHeading: 'Una secuencia documental exige preguntas separadas, no una conclusión colectiva.',
        engineLead: 'Por Derecho comprueba si cada acto identificado tuvo autoridad lícita, fuente documentada, autor individual, conocimiento relevante, efecto causal y beneficio trazable. Una cronología no prueba un plan común ni responsabilidad penal.',
        engineAllegation: '<strong>HIPÓTESIS INVESTIGATIVAS DE POR DERECHO · NO HALLAZGOS JUDICIALES</strong><p>Ninguna persona o entidad se clasifica públicamente como «facilitadora». Toda hipótesis penal debe probarse o descartarse actor por actor, acto por acto y elemento por elemento, incluida la prueba contraria y la explicación inocente más fuertes.</p>',
        ladderTitle: 'No existe una escala pública de «facilitación»',
        ladderText: 'El material público no asigna rangos de facilitación, conocimiento o culpabilidad. Un papel sólo puede examinarse mediante acto concreto, fuente, autoridad, conocimiento, dolo, contribución causal, prueba contraria y resultado competente.',
        scoreText: 'Cualquier marcador numérico es sólo una prioridad de obtención de prueba. No es prueba, probabilidad de condena, hallazgo sobre una persona o entidad, ni previsión de un resultado oficial.'
      };

  const safeguard = document.createElement('section');
  safeguard.className = 'section alt';
  safeguard.dataset.criminalPublicBoundaries = '20260822';
  safeguard.innerHTML = `<div class="shell"><div class="decision"><p class="kicker">${copy.eyebrow}</p><h2>${copy.title}</h2><p>${copy.text}</p><p><a class="button secondary" href="${charter}">${copy.link}</a></p></div></div>`;
  main.insertAdjacentElement('afterbegin', safeguard);

  const engineering = route.includes('criminal-engineering') || route.includes('ingenieria-forense-criminal');
  if (engineering) {
    document.title = copy.engineTitle;
    const description = document.querySelector('meta[name="description"]');
    if (description) description.content = copy.engineDescription;
    const hero = document.querySelector('.hero .record');
    if (hero) {
      const eyebrow = hero.querySelector('.eyebrow');
      const heading = hero.querySelector('h1');
      const lead = hero.querySelector('.lead');
      const allegation = hero.querySelector('.allegation');
      if (eyebrow) eyebrow.textContent = copy.engineEyebrow;
      if (heading) heading.textContent = copy.engineHeading;
      if (lead) lead.textContent = copy.engineLead;
      if (allegation) allegation.innerHTML = copy.engineAllegation;
    }
    const ladder = document.querySelector('.ladder');
    const ladderSection = ladder && ladder.closest('section');
    if (ladderSection) ladderSection.innerHTML = `<div class="shell record"><h2>${copy.ladderTitle}</h2><p>${copy.ladderText}</p><p><a class="button secondary" href="${charter}">${copy.link}</a></p></div>`;
  }

  document.querySelectorAll('p small').forEach(node => {
    if (/Percentages are investigative strength|Porcentajes.*prioridad|investigative strength/i.test(node.textContent)) node.textContent = copy.scoreText;
  });
})();
