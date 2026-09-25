(() => {
  const isEs = /\/es\/?$/.test(location.pathname);
  const routes = isEs ? {
    "#historia-reconstruida":"centro-mando-recuperacion/",
    "#plataforma-construida-2011-2018":"centro-mando-recuperacion/",
    "#recuperacion":"centro-mando-recuperacion/",
    "#tesis":"centro-mando-recuperacion/",
    "#registro":"evidencia/",
    "#mapa-institucional":"centro-mando-recuperacion/",
    "#institutional-accountability-12aug":"centro-mando-recuperacion/",
    "#futuro":"futuro/",
    "#por-derecho":"por-derecho/",
    "#metodo":"evidencia/"
  } : {
    "#reverse-engineered-story":"recovery-command-center/",
    "#platform-built-2011-2018":"recovery-command-center/",
    "#recovery":"recovery-command-center/",
    "#thesis":"recovery-command-center/",
    "#record":"evidence/",
    "#institutional-map":"recovery-command-center/",
    "#institutional-accountability-12aug-en":"recovery-command-center/",
    "#future":"future/",
    "#por-derecho":"por-derecho/",
    "#method":"evidence/"
  };
  const target = routes[location.hash];
  if (target) location.replace(target);
})();
