/* RICPE-CNMV-VISUAL-EVIDENCE-20260827 */
(() => {
  const normalise = value => {
    let route = value.replace(/\/index\.html$/, '/');
    if (!route.endsWith('/')) route += '/';
    return route;
  };
  const path = normalise(location.pathname);
  const supported = [
    '/es/ric-private-equity-sun-park/',
    '/en/ric-private-equity-sun-park/',
    '/es/cnmv-ricpe-verificacion/',
    '/en/cnmv-ricpe-verification/'
  ].some(route => path.endsWith(route));
  if (!supported) return;

  const render = attempt => {
    if (document.querySelector('[data-ricpe-cnmv-visual-evidence-20260827]')) return;
    const anchor = document.querySelector('[data-ricpe-cnmv-closure-20260827]');
    if (!anchor) {
      if (attempt < 12) setTimeout(() => render(attempt + 1), 50);
      return;
    }

    const isEnglish = document.documentElement.lang === 'en';
    const basePrefix = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
    const source = `${basePrefix}evidence/ricpe-cnmv/2026-08-27/`;
    const copy = isEnglish ? {
      kicker: 'Original PNG evidence visuals · Spanish-language sources',
      title: 'San Telmo, the insolvency administrator and the PwC knowledge checkpoint',
      intro: 'These are the two exact PNG files used in the institutional communications. Open either image at full size. They document attributed statements, named actors and questions for verification; they do not by themselves establish culpability, liability or intent.',
      sanTitle: 'San Telmo / RICPE / Sun Park',
      sanCaption: 'The composite visual brings together the statement attributed to Eduardo Sánchez, an image of the hotel and Francisco de Borja Rodríguez-Batllori Laffitte identified as insolvency administrator. It documents the visual source and traceability questions; it does not itself attribute responsibility.',
      pwcTitle: 'PwC Canary Islands 2016: five actors + insolvency administrator',
      pwcCaption: 'The visual presents a professional knowledge-transfer checkpoint, identifies five actors and the insolvency administrator, and poses documentary questions. It is not, by itself, a finding of culpability.',
      boundary: '<strong>Reading boundary:</strong> both files are composite, argumentative visuals supplied by the reporting person. They must be tested against primary documents, responses from the identified persons and entities, and potentially exculpatory evidence.'
    } : {
      kicker: 'Visuales probatorios PNG originales',
      title: 'San Telmo, el administrador concursal y el punto de conocimiento PwC',
      intro: 'Estos son los dos archivos PNG exactos utilizados en las comunicaciones institucionales. Abra cada imagen a tamaño completo. Documentan manifestaciones atribuidas, actores identificados y preguntas de verificación; no establecen por sí solos culpabilidad, responsabilidad ni intención.',
      sanTitle: 'San Telmo / RICPE / Sun Park',
      sanCaption: 'El gráfico reúne la manifestación atribuida a Eduardo Sánchez, una imagen del hotel y la identificación de Francisco de Borja Rodríguez-Batllori Laffitte como administrador concursal. Documenta la fuente visual y las preguntas de trazabilidad; no atribuye por sí solo responsabilidad.',
      pwcTitle: 'PwC Canarias 2016: cinco actores + administrador concursal',
      pwcCaption: 'El gráfico plantea un punto de conocimiento y transferencia profesional, identifica cinco actores y al administrador concursal, y formula preguntas documentales. No constituye por sí mismo una determinación de culpabilidad.',
      boundary: '<strong>Límite de lectura:</strong> ambos archivos son visuales compuestos y argumentativos aportados por el informante. Deben contrastarse con los documentos primarios, las respuestas de las personas y entidades identificadas y la evidencia potencialmente exculpatoria.'
    };

    const style = document.createElement('style');
    style.dataset.ricpeCnmvVisualEvidenceStyle = '20260827';
    style.textContent = `
      [data-ricpe-cnmv-visual-evidence-20260827]{padding:2rem 0;background:#edf3ee;border-bottom:1px solid rgba(19,37,45,.14)}
      [data-ricpe-cnmv-visual-evidence-20260827] .visual-wrap{max-width:1180px;margin:0 auto;padding:0 1.1rem}
      [data-ricpe-cnmv-visual-evidence-20260827] .visual-kicker{margin:0 0 .4rem;font-size:.72rem;font-weight:900;letter-spacing:.08em;text-transform:uppercase;color:#526b59}
      [data-ricpe-cnmv-visual-evidence-20260827] h2{margin:.15rem 0 .7rem;max-width:34ch;font-size:clamp(1.55rem,3vw,2.45rem);line-height:1.1;color:#13252d}
      [data-ricpe-cnmv-visual-evidence-20260827] .visual-intro{max-width:88ch;line-height:1.65;color:#26383f}
      [data-ricpe-cnmv-visual-evidence-20260827] .visual-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;margin:1.15rem 0}
      [data-ricpe-cnmv-visual-evidence-20260827] figure{margin:0;overflow:hidden;border:1px solid rgba(19,37,45,.18);border-radius:15px;background:#fff;box-shadow:0 8px 26px rgba(19,37,45,.08)}
      [data-ricpe-cnmv-visual-evidence-20260827] figure a{display:block;background:#e9eff1}
      [data-ricpe-cnmv-visual-evidence-20260827] img{display:block;width:100%;height:auto;aspect-ratio:3/2;object-fit:contain}
      [data-ricpe-cnmv-visual-evidence-20260827] figcaption{padding:.9rem;line-height:1.5;color:#26383f}
      [data-ricpe-cnmv-visual-evidence-20260827] figcaption strong{display:block;margin-bottom:.3rem;color:#13252d}
      [data-ricpe-cnmv-visual-evidence-20260827] .visual-boundary{max-width:94ch;margin:.7rem 0 0;padding:.8rem .95rem;border-left:5px solid #526b59;background:#fff;line-height:1.55}
      @media(max-width:760px){[data-ricpe-cnmv-visual-evidence-20260827] .visual-grid{grid-template-columns:1fr}}
    `;
    document.head.append(style);

    const section = document.createElement('section');
    section.dataset.ricpeCnmvVisualEvidence20260827 = 'true';
    section.id = 'ricpe-cnmv-visuales-27ago2026';
    section.innerHTML = `<div class="visual-wrap">
      <p class="visual-kicker">${copy.kicker}</p>
      <h2>${copy.title}</h2>
      <p class="visual-intro">${copy.intro}</p>
      <div class="visual-grid">
        <figure><a href="${source}san-telmo-ricpe-sun-park-stamp-v1-ES.png"><img src="${source}san-telmo-ricpe-sun-park-stamp-v1-ES.png" width="1536" height="1024" loading="lazy" decoding="async" alt="${isEnglish ? 'Spanish-language composite visual with Eduardo Sánchez, Hotel Sun Park MYND Yaiza and Francisco de Borja Rodríguez-Batllori Laffitte identified as insolvency administrator' : 'Visual en español con Eduardo Sánchez, el Hotel Sun Park MYND Yaiza y Francisco de Borja Rodríguez-Batllori Laffitte identificado como administrador concursal'}"></a><figcaption><strong>${copy.sanTitle}</strong>${copy.sanCaption}</figcaption></figure>
        <figure><a href="${source}pwc-five-actors-plus-ac-2016-knowledge-checkpoint-ES.png"><img src="${source}pwc-five-actors-plus-ac-2016-knowledge-checkpoint-ES.png" width="1536" height="1024" loading="lazy" decoding="async" alt="${isEnglish ? 'Spanish-language PwC Canary Islands 2016 visual concerning five actors and the insolvency administrator' : 'Visual en español sobre PwC Canarias 2016, cinco actores y el administrador concursal'}"></a><figcaption><strong>${copy.pwcTitle}</strong>${copy.pwcCaption}</figcaption></figure>
      </div>
      <p class="visual-boundary">${copy.boundary}</p>
    </div>`;
    anchor.insertAdjacentElement('afterend', section);
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => render(0), { once: true });
  else render(0);
})();
