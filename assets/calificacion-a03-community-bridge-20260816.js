(() => {
  const path = window.location.pathname.replace(/\/+$/, '') + '/';
  const es = path.endsWith('/es/comunidad-instrumentalizacion/');
  const en = path.endsWith('/en/community-instrumentalisation/');
  if (!es && !en) return;
  if (document.querySelector('[data-a03-community-bridge-20260816]')) return;
  const box = document.createElement('section');
  box.setAttribute('data-a03-community-bridge-20260816','');
  box.className = 'section';
  box.innerHTML = es ? `<div class="shell"><aside class="pressure-maxim"><strong>Puente a Calificación · Alegación 03</strong><span>Este conflicto no debe quedar aislado como un dossier de Comunidad. La propia AC conocía la alegación sobre deuda, voto, cuentas y actas; después utilizó o autorizó mecanismos de Comunidad para acceso, mantenimiento y seguridad; y más tarde imputó a Gil/Pink el efecto económico de rentas no cobradas. La página de Calificación integra ahora toda la cadena como una sola cuestión causal, preservando que el “secuestro de la Comunidad” es una alegación y que la condena por falta posterior de cobro de rentas sigue siendo adversa y recurrida.</span><a class="button" href="../calificacion-concurso-36-2012-vidas-paralelas/">Abrir el análisis unitario de Alegación 03 →</a></aside></div>` : `<div class="shell"><aside class="pressure-maxim"><strong>Bridge to Classification · Allegation 03</strong><span>This conflict must not remain isolated as a Community dossier. The AC himself knew of the debt, voting, accounts and minutes allegation; later used or authorised Community mechanisms for access, maintenance and security; and later attributed the economic effect of uncollected rent to Gil/Pink. The Classification page now integrates that chain as one causation question, while preserving that “Community hijacking” is a party allegation and that the later adverse rent-recovery finding remains appealed.</span><a class="button" href="../insolvency-classification-parallel-lives/">Open the unitary Allegation 03 analysis →</a></aside></div>`;
  const anchor = document.querySelector('#control-2018-sin-auto-posesion') || document.querySelector('.dossier-hero');
  if (anchor) anchor.insertAdjacentElement('afterend', box);
  else document.querySelector('main')?.prepend(box);
})();