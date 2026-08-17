(() => {
  const path = location.pathname;
  const isEs = path.includes('/es/');
  const current = document.currentScript;
  const selfRoutes = [
    '/es/caso-insignia-jv1260-2011-ap89-2014/',
    '/en/flagship-case-jv1260-2011-ap89-2014/'
  ];

  const reverseTargets = [
    ...selfRoutes,
    '/es/comunidad-instrumentalizacion/',
    '/en/community-instrumentalisation/',
    '/es/toma-control-sun-park-7-junio-2018/',
    '/en/sun-park-takeover-7-june-2018/',
    '/es/reconstruccion-unitaria-autoridades-publicas/',
    '/en/public-authority-unitary-case-reconstruction/'
  ];
  if (current && reverseTargets.some(route => path.includes(route)) && !document.querySelector('script[data-jv1260-reverse-engineering]')) {
    const script = document.createElement('script');
    script.src = new URL('jv1260-unitary-reverse-engineering-20260817.js?v=20260817a', current.src).href;
    script.defer = true;
    script.dataset.jv1260ReverseEngineering = 'true';
    document.head.appendChild(script);
  }

  if (selfRoutes.some(route => path.includes(route))) return;

  const targets = [
    /\/por-derecho\/(es|en)\/?$/,
    /comunidad-instrumentalizacion|community-instrumentalisation/,
    /reconstruccion-unitaria-autoridades-publicas|public-authority-unitary-case-reconstruction/,
    /cuaderno-juridico|legal-notebook/,
    /proyecto-conocimiento|knowledge-project/,
    /sobre-nosotros|\/about\//,
    /insolvencia-lpb|lpb-insolvency/,
    /concurso-36-2012-responsabilidad-institucional|insolvency-36-2012-institutional-accountability/,
    /calificacion-concurso-36-2012-vidas-paralelas|insolvency-classification-parallel-lives/,
    /dp-1901-2026|fiscalia-dip-2-2026/,
    /toma-control-sun-park-7-junio-2018|sun-park-takeover-7-june-2018/,
    /libros\/justicia-en-fragmentos|books\/justice-in-pieces/,
    /libros\/law-mower-man|books\/law-mower-man/
  ];
  if (!targets.some(re => re.test(path))) return;
  if (document.getElementById('flagship-case-1260-spotlight')) return;

  if (current && !document.querySelector('link[data-flagship-case-styles]')) {
    const css = document.createElement('link');
    css.rel = 'stylesheet';
    css.href = new URL('flagship-case-1260-2011-20260817.css?v=20260817a', current.src).href;
    css.dataset.flagshipCaseStyles = 'true';
    document.head.appendChild(css);
  }

  const main = document.querySelector('main');
  if (!main) return;

  const section = document.createElement('section');
  section.id = 'flagship-case-1260-spotlight';
  section.className = 'flagship-spotlight-strip';
  section.setAttribute('aria-label', isEs ? 'Caso insignia JV 1260/2011' : 'Flagship case JV 1260/2011');
  section.innerHTML = isEs ? `
    <div class="shell spotlight-inner">
      <div class="spotlight-mark">SPOTLIGHT · CASO INSIGNIA</div>
      <div><h2>JV 1260/2011 → AP Las Palmas 89/2014</h2><p>El caso testigo para seguir 18 unidades, explotación hotelera, el filtro deuda→voto, la ampliación actora contra Monterecco, dos niveles judiciales y la convergencia documentada con el nodo CAM de mayo–junio de 2018. Las hipótesis de fraude procesal se investigan; no se presentan como hechos adjudicados.</p></div>
      <a href="/por-derecho/es/caso-insignia-jv1260-2011-ap89-2014/">Abrir caso insignia →</a>
    </div>` : `
    <div class="shell spotlight-inner">
      <div class="spotlight-mark">SPOTLIGHT · FLAGSHIP CASE</div>
      <div><h2>JV 1260/2011 → AP Las Palmas 89/2014</h2><p>The test case for tracing 18 units, hotel operation, the debt→vote filter, the claimant-driven extension against Monterecco, two judicial levels and the documented May/June-2018 CAM convergence. Procedural-fraud theories are investigated, not presented as adjudicated fact.</p></div>
      <a href="/por-derecho/en/flagship-case-jv1260-2011-ap89-2014/">Open flagship case →</a>
    </div>`;

  const hero = main.querySelector(':scope > .hero, :scope > section.hero, :scope > .dossier-hero, :scope > section.dossier-hero');
  if (hero) hero.insertAdjacentElement('afterend', section);
  else {
    const priority = main.querySelector(':scope > .priority-band');
    if (priority) priority.insertAdjacentElement('afterend', section);
    else main.insertAdjacentElement('afterbegin', section);
  }
})();
