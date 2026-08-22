(() => {
  'use strict';

  const normalise = value => {
    let path = value.replace(/\/index\.html$/, '/');
    if (!path.endsWith('/')) path += '/';
    return path;
  };

  const run = () => {
    const path = normalise(window.location.pathname);
    const isEs = document.documentElement.lang === 'es' || path.includes('/es/');
    const isEn = document.documentElement.lang === 'en' || path.includes('/en/');
    if (!isEs && !isEn) return;

    const isIdoneidad = path.endsWith('/es/ricpe-idoneidad-series-f-g/') || path.endsWith('/en/ricpe-idoneidad-series-f-g/');
    const isReverse = path.endsWith('/es/ingenieria-inversa-360-cadena-sun-park/') || path.endsWith('/en/reverse-engineering-360-sun-park-chain/');
    if (!isIdoneidad && !isReverse) return;
    if (document.querySelector('[data-declaration004-source-provenance="20260821"]')) return;

    const copy = isEs ? {
      eyebrow: 'FUENTE PERSONAL · ESTADO PROBATORIO',
      title: 'Una declaración personal preserva la pregunta; no sustituye el expediente.',
      idoneidad: 'La Declaración 004, derivada de una fuente personal de voz de 18 de agosto de 2026 y registrada con identidad reservada en la capa pública, deja constancia de que esta misma tensión temporal/documental fue identificada y de que se pidieron la idoneidad, el informe AEAT, los documentos de financiación y la trazabilidad de obras y pagos. Esto acredita la procedencia de la pregunta en el registro personal; no prueba qué cubrió el Decreto 224/2022, qué decía íntegramente el informe AEAT, cómo se aplicaron las Series F/G, que faltara una segunda autorización ni que existiera irregularidad.',
      reverse: 'Regla 360° de fuente: una declaración derivada de una fuente personal entra en el grafo como nodo de conocimiento, recuerdo, aviso o procedencia de una pregunta. No debe convertirse en el puente jurídico o económico que pretende describir. En el nodo RICPE/idoneidad, la Declaración 004 preserva la pregunta formulada el 18 de agosto de 2026; los puentes siguen siendo la solicitud, el informe AEAT, el Decreto/acto final, los contratos, los desembolsos, las facturas, los certificados y la contabilidad fuente–uso.',
      boundary: 'Regla de control: fuente personal ≠ documento primario. La coincidencia entre recuerdo y documento no crea corroboración independiente si ambos proceden del mismo material subyacente.',
      action: isIdoneidad ? 'Abrir método 360° →' : 'Abrir pregunta Series F/G →',
      href: isIdoneidad ? '/por-derecho/es/ingenieria-inversa-360-cadena-sun-park/' : '/por-derecho/es/ricpe-idoneidad-series-f-g/'
    } : {
      eyebrow: 'PERSONAL SOURCE · EVIDENTIAL STATUS',
      title: 'A personal statement preserves the question; it does not replace the file.',
      idoneidad: 'Declaration 004, derived from a personal voice source of 18 August 2026 and registered with identity reserved in the public layer, records that this same timing/documentary tension was identified and that the idoneidad file, AEAT report, financing records and works/payment trace were requested. This establishes provenance of the question in the personal record; it does not prove what Decree 224/2022 covered, what the full AEAT report said, how Series F/G were applied, that a second authorisation was absent, or that any wrongdoing occurred.',
      reverse: '360° source rule: a declaration derived from a personal source enters the graph as a knowledge, recollection, notice or question-provenance node. It must not be converted into the legal or economic bridge it describes. At the RICPE/idoneidad node, Declaration 004 preserves the question raised on 18 August 2026; the bridges remain the application, AEAT report, final Decree/act, contracts, drawdowns, invoices, certificates and source-and-use accounting.',
      boundary: 'Control rule: personal source ≠ primary document. Agreement between recollection and a document is not independent corroboration when both derive from the same underlying material.',
      action: isIdoneidad ? 'Open 360° method →' : 'Open Series F/G question →',
      href: isIdoneidad ? '/por-derecho/en/reverse-engineering-360-sun-park-chain/' : '/por-derecho/en/ricpe-idoneidad-series-f-g/'
    };

    if (!document.getElementById('declaration004-source-provenance-style')) {
      const style = document.createElement('style');
      style.id = 'declaration004-source-provenance-style';
      style.textContent = '.decl004-prov{max-width:1120px;margin:0 auto;border-left:6px solid #8c6b2f;background:#fff8e8;border-radius:0 16px 16px 0;padding:1.1rem 1.25rem}.decl004-prov h2{margin:.25rem 0 .6rem}.decl004-prov-eyebrow{margin:0;font-size:.72rem;font-weight:900;letter-spacing:.07em;text-transform:uppercase;color:#77591d}.decl004-prov-boundary{border-top:1px solid rgba(19,37,45,.18);padding-top:.7rem;margin-top:.8rem;font-size:.9rem;color:#4f5c61}.decl004-prov a{font-weight:850}';
      document.head.appendChild(style);
    }

    const section = document.createElement('section');
    section.className = 'section';
    section.setAttribute('data-declaration004-source-provenance', '20260821');
    section.innerHTML = `<div class="shell"><aside class="decl004-prov"><p class="decl004-prov-eyebrow">${copy.eyebrow}</p><h2>${copy.title}</h2><p>${isIdoneidad ? copy.idoneidad : copy.reverse}</p><p class="decl004-prov-boundary"><strong>${copy.boundary}</strong></p><p><a href="${copy.href}">${copy.action}</a></p></aside></div>`;

    const main = document.querySelector('main');
    if (!main) return;
    const hero = main.querySelector(':scope > .hero, :scope > .hero-q, :scope > section.hero, :scope > section.hero-q');
    if (hero) hero.insertAdjacentElement('afterend', section);
    else main.insertAdjacentElement('afterbegin', section);
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, {once: true});
  else run();
})();
