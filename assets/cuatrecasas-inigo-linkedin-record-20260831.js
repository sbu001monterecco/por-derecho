(() => {
  const path = window.location.pathname.replace(/\/+$/, '');
  const match = path.match(/\/(en|es)\/cuatrecasas-sun-park$/);
  if (!match || document.querySelector('[data-cuatrecasas-inigo-linkedin-record="20260306"]')) return;

  const lang = match[1];
  const isEs = lang === 'es';
  const message = 'Just received notice from the Madrid bar that you requested disciplinary action against me which has been adequately dismissed. This is an unloyal and unlawful move against a Friend Who help you tireless with all efforts. You are not a Friend and deserve the worst. Do not ever contact me and be sure I would Advise Everyone about the kind of person you are.';

  const copy = isEs ? {
    eyebrow: 'DOCUMENTO PRESERVADO · 6 MARZO 2026',
    title: 'Mensaje de LinkedIn preservado: Íñigo de Luisa Maíz',
    intro: 'Una captura conservada en el expediente muestra, a las 12:13 PM del 6 de marzo de 2026, una cuenta de LinkedIn que exhibía el nombre “Inigo de Luisa Maiz” y el siguiente mensaje. Se reproduce literalmente, incluidos mayúsculas, gramática y ortografía del original:',
    provenanceTitle: 'Trazabilidad y límite probatorio',
    provenance: 'Un correo de preservación enviado el mismo día a Cuatrecasas dejó constancia de que, poco después de transmitirse, el Sr. de Luisa “appears to have deleted it” y de que la captura se había tomado antes. Una segunda captura conserva el cambio posterior del estado de la conversación. Esa segunda captura no se trata, por sí sola, como prueba concluyente del borrado.',
    boundary: 'Publicación documental: el mensaje se muestra como comunicación preservada. Su contenido no se presenta por sí solo como prueba de responsabilidad civil, penal o deontológica. La referencia al borrado se mantiene expresamente en la forma cualificada del registro contemporáneo.',
    record: 'Ver registro controlado del repositorio →'
  } : {
    eyebrow: 'PRESERVED DOCUMENT · 6 MARCH 2026',
    title: 'Preserved LinkedIn message: Íñigo de Luisa Maíz',
    intro: 'A retained evidential capture shows, at 12:13 PM on 6 March 2026, a LinkedIn account displaying the name “Inigo de Luisa Maiz” and the following message. It is reproduced verbatim, including the original capitalization, grammar and spelling:',
    provenanceTitle: 'Provenance and evidential boundary',
    provenance: 'A same-day preservation email sent to Cuatrecasas recorded that, shortly after transmission, Mr de Luisa “appears to have deleted it” and that the screenshot had been taken beforehand. A second retained capture records the subsequent change in the LinkedIn conversation status. That second capture is not treated, by itself, as conclusive proof of deletion.',
    boundary: 'Documentary publication: the message is shown as a preserved communication. Its content is not presented, by itself, as proof of civil, criminal or disciplinary liability. The deletion point is deliberately retained only in the qualified form used in the contemporaneous record.',
    record: 'Open controlled repository record →'
  };

  const section = document.createElement('section');
  section.className = 'section cuatre-linkedin-record';
  section.setAttribute('data-cuatrecasas-inigo-linkedin-record', '20260306');
  section.innerHTML = `
    <div class="shell record">
      <div class="cuatre-linkedin-panel">
        <p class="eyeline">${copy.eyebrow}</p>
        <h2>${copy.title}</h2>
        <p class="cuatre-linkedin-intro">${copy.intro}</p>
        <blockquote class="cuatre-linkedin-message"></blockquote>
        <div class="cuatre-linkedin-provenance">
          <strong>${copy.provenanceTitle}</strong>
          <p>${copy.provenance}</p>
          <p class="cuatre-linkedin-boundary">${copy.boundary}</p>
          <p><a href="../../evidence/cuatrecasas/2026-03-06-inigo-de-luisa-linkedin-message.json">${copy.record}</a></p>
        </div>
      </div>
    </div>`;
  section.querySelector('.cuatre-linkedin-message').textContent = message;

  const style = document.createElement('style');
  style.setAttribute('data-cuatrecasas-inigo-linkedin-record-style', '20260306');
  style.textContent = `
    .cuatre-linkedin-record{background:#f4f1ea}
    .cuatre-linkedin-panel{background:#fff;border:1px solid #d9dede;border-top:7px solid #13252d;border-radius:22px;padding:clamp(1.2rem,3vw,2rem);box-shadow:0 16px 40px rgba(16,38,45,.10)}
    .cuatre-linkedin-panel h2{max-width:900px;margin:.35rem 0 .8rem}
    .cuatre-linkedin-intro{max-width:960px;font-size:1.02rem;line-height:1.65}
    .cuatre-linkedin-message{margin:1.25rem 0;padding:1.15rem 1.25rem;background:#13252d;color:#fff;border-left:7px solid #d0a12d;border-radius:12px;font-size:clamp(1.05rem,2vw,1.25rem);line-height:1.65;font-style:normal}
    .cuatre-linkedin-provenance{background:#f7faf9;border-left:5px solid #1d5c4a;border-radius:12px;padding:1rem 1.15rem}
    .cuatre-linkedin-provenance p{margin:.45rem 0;line-height:1.6}
    .cuatre-linkedin-boundary{font-size:.92rem;color:#4d5558}
  `;
  document.head.appendChild(style);

  const hero = document.querySelector('main > .hero, main .hero');
  if (hero) hero.insertAdjacentElement('afterend', section);
  else document.querySelector('main')?.prepend(section);
})();
