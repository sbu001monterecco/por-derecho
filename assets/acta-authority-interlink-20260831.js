(() => {
  'use strict';
  const script = document.currentScript;
  if (!script || document.querySelector('[data-ca-reciprocal-interlink]')) return;
  const path = location.pathname;
  const isActa = /\/(community-instrumentalisation\/acta-document-room|comunidad-instrumentalizacion\/sala-documental-actas)\//.test(path);
  const isAdjudication = /\/(2022-adjudication-documentary-reconstruction|adjudicacion-2022-reconstruccion-documental)\//.test(path);
  if (!isActa && !isAdjudication) return;
  const lang = document.documentElement.lang.toLowerCase().startsWith('es') ? 'es' : 'en';
  const repo = new URL('../', new URL('.', script.src));
  const route = new URL(lang === 'es' ? 'es/actas-comunidad-autoridades-publicas/' : 'en/community-actas-public-authorities/', repo);
  if (isAdjudication) route.hash = 'parallel-2022';
  else if (/\/2022-02-04\//.test(path)) route.hash = 'acta=SP-ACTA-2022-02-04';
  else route.hash = 'actas';
  const copy = lang === 'es' ? {
    title: isAdjudication ? 'Ver la vía paralela de 2022' : 'Conectar esta ACTA con procedimientos y autoridades',
    body: isAdjudication ? 'Compara los Autos, aclaraciones y escritura 457 con el ACTA de 4 de febrero sin inferir causalidad.' : 'Abre el registro recíproco de 20 ACTAs, siete ejes probatorios y 49 expedientes públicos.',
    link: 'Abrir interconexión controlada'
  } : {
    title: isAdjudication ? 'View the 2022 parallel track' : 'Connect this ACTA to proceedings and authorities',
    body: isAdjudication ? 'Compare the orders, clarifications and deed 457 with the 4 February ACTA without inferring causation.' : 'Open the reciprocal register of 20 ACTAs, seven evidence axes and 49 public-authority files.',
    link: 'Open controlled interconnectivity'
  };
  const aside = document.createElement('aside');
  aside.setAttribute('data-ca-reciprocal-interlink', '20260831');
  aside.innerHTML = `<strong>${copy.title}</strong><p>${copy.body}</p><a href="${route.href}">${copy.link} →</a>`;
  const style = document.createElement('style');
  style.textContent = '[data-ca-reciprocal-interlink]{width:min(1080px,calc(100% - 2rem));margin:1rem auto;padding:1rem 1.2rem;border:1px solid #91aaa7;border-left:6px solid #1c665e;border-radius:14px;background:#f3faf7;color:#17363a}[data-ca-reciprocal-interlink] p{margin:.35rem 0}[data-ca-reciprocal-interlink] a{font-weight:800;color:#14584f}';
  document.head.appendChild(style);
  const main = document.querySelector('main');
  if (main) main.insertBefore(aside, main.firstChild);
})();
