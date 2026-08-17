(() => {
  'use strict';

  const path = window.location.pathname.replace(/\/+$/, '/');
  const isEs = document.documentElement.lang.toLowerCase().startsWith('es') || path.includes('/es/');

  const allowedRoutes = [
    '/es/calificacion-concurso-36-2012-vidas-paralelas/',
    '/en/insolvency-classification-parallel-lives/',
    '/es/calificacion-concurso-36-2012-vidas-paralelas/conocimiento-previo-rescate/',
    '/en/insolvency-classification-parallel-lives/prior-judicial-knowledge-rescue/',
    '/es/concurso-36-2012-magistrado-juez/',
    '/en/insolvency-36-2012-mercantile-court-1/',
    '/es/mensaje-abierto-cgpj/',
    '/en/open-message-cgpj/',
    '/es/mismo-hotel-multiples-vidas-financieras/',
    '/en/same-hotel-multiple-financial-lives/',
    '/es/ric-private-equity-sun-park/',
    '/en/ric-private-equity-sun-park/',
    '/es/registros-institucionales/',
    '/en/institutional-records/',
    '/es/concurso-36-2012-responsabilidad-institucional/',
    '/en/insolvency-36-2012-institutional-accountability/'
  ];

  if (!allowedRoutes.some(route => path.endsWith(route))) return;

  const fullEs = `
    <p><strong>CUESTIÓN ADICIONAL DE IMPARCIALIDAD APARENTE.</strong> Existe un relato documentado que atribuye a <strong>un actor privado de un perímetro materialmente interesado</strong> un grado inusualmente próximo de proximidad personal o acceso directo al decisor judicial. El relato se considera suficientemente serio para exigir comprobación independiente, pero <strong>no se publica como hecho probado</strong>.</p>
    <p>La pregunta es cerrada y verificable: <strong>palabras exactas → fecha/lugar/testigos → llamadas/mensajes → reuniones/accesos → eventual canal declarado o no declarado → corroboración o refutación</strong>. La existencia de esa alegación no prueba por sí sola amistad, influencia, parcialidad, concertación, corrupción ni prevaricación.</p>`;

  const fullEn = `
    <p><strong>ADDITIONAL APPEARANCE-OF-IMPARTIALITY QUESTION.</strong> A documented account attributes to <strong>a private actor within a materially interested perimeter</strong> an unusually close degree of personal proximity or direct access to the judicial decision-maker. The account is considered sufficiently serious to require independent verification, but <strong>is not published as established fact</strong>.</p>
    <p>The question is finite and testable: <strong>exact words → date/place/witnesses → calls/messages → meetings/access → any disclosed or undisclosed channel → corroboration or disproof</strong>. The existence of the allegation does not by itself prove friendship, influence, bias, coordination, corruption or judicial prevarication.</p>`;

  const compactEs = `<p>Permanece una cuestión no resuelta: si <strong>un actor privado de un perímetro materialmente interesado</strong> disfrutó de una proximidad personal o acceso directo no declarado al decisor judicial. <strong>Es una alegación que exige corroboración objetiva, no un hecho establecido.</strong> La vía de comprobación son comunicaciones, reuniones, accesos y cualquier deber de revelación aplicable.</p>`;
  const compactEn = `<p>An unresolved question remains whether <strong>a private actor within a materially interested perimeter</strong> enjoyed undisclosed personal proximity or direct access to the judicial decision-maker. <strong>It is an allegation requiring objective corroboration, not an established fact.</strong> The verification route is communications, meetings, access records and any applicable disclosure duty.</p>`;

  const rewrite = () => {
    const unitary = document.getElementById('lpam-cgpj169-calificacion-unitary');
    if (unitary) {
      const candidates = [...unitary.querySelectorAll('.callout, p')];
      const target = candidates.find(el => /Patricia Domínguez|LPAM–MAGISTRADO|LPAM–JUDGE|friendship\/personal-access|amistad\/acceso personal/i.test(el.textContent || ''));
      if (target) {
        if (target.classList && target.classList.contains('callout')) {
          target.innerHTML = isEs ? fullEs : fullEn;
        } else {
          target.outerHTML = isEs ? compactEs : compactEn;
        }
      }
    }

    const narrow = document.getElementById('lpam-magistrado-source-control');
    if (narrow) {
      [...narrow.querySelectorAll('p, li')].forEach(el => {
        if (/Patricia Domínguez|Patricia memorialised|Patricia dejó constancia|Gil Marer states|Gil Marer manifiesta/i.test(el.textContent || '')) {
          el.innerHTML = isEs
            ? '<strong>Fuente testimonial controlada.</strong> El expediente conserva un relato documentado sobre posible proximidad personal o acceso directo de un actor privado materialmente interesado al decisor judicial. Se mantiene como alegación susceptible de corroboración objetiva, no como hecho establecido.'
            : '<strong>Controlled testimonial source.</strong> The record preserves a documented account concerning possible personal proximity or direct access by a materially interested private actor to the judicial decision-maker. It remains an allegation for objective corroboration, not an established fact.';
        }
      });
    }
  };

  rewrite();
  requestAnimationFrame(rewrite);
})();
