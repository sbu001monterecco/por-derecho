(() => {
  const path = window.location.pathname.replace(/\/+$/, '') + '/';
  const es = path.endsWith('/es/calificacion-concurso-36-2012-vidas-paralelas/');
  const en = path.endsWith('/en/insolvency-classification-parallel-lives/');
  if (!es && !en) return;
  if (document.querySelector('[data-calificacion-3032010-20260816]')) return;

  const copy = es ? {
    kicker: '3.032.010,34 € · MI ACUSACIÓN SOBRE LA CIFRA',
    title: 'Acuso al AC y al juez de fabricar conscientemente esta cuantía y de hacerlo para un beneficio personal directo o indirecto, mantenido clandestinamente.',
    allegation: '<strong>Acuso al Administrador Concursal Francisco de Borja Rodríguez-Batllori y al juez Alberto López Villarrubia de fabricar y/o falsificar conscientemente la cifra de 3.032.010,34 €</strong> que terminó convertida en una condena patrimonial contra mí, más el interés legal incrementado en dos puntos. No sostengo que sea un simple error aritmético ni una discrepancia jurídica inocente. <strong>Alego que la cifra fue construida y mantenida deliberadamente y que la finalidad fue obtener o facilitar un beneficio personal directo o indirecto, mantenido de forma clandestina.</strong>',
    evidenceTitle: 'Lo que ya puede comprobarse en los documentos',
    evidence: [
      ['24.575 €/mes', 'La Sentencia 163/2023 recoge esa renta contractual mensual.'],
      ['1.130.450 €', 'Una apelación identifica 46 meses y calcula 24.575 € × 46, antes de descontar las rentas que sostiene que sí se pagaron.'],
      ['2.733.923,64 €', 'La misma apelación cuestiona esta cifra atribuida a la reclamación de la Administración Concursal.'],
      ['3.032.010,34 €', 'La AC pidió esta cuantía contra mí y la sentencia la convirtió en indemnización usando como medida el principal despachado en la ejecución contra Pink.']
    ],
    bridgeTitle: 'La pregunta que no voy a dejar diluir',
    bridge: '¿Cuál es la trazabilidad euro por euro que lleva desde una renta de 24.575 €/mes —y desde los pagos, créditos, compensaciones y costes reales— hasta 2.733.923,64 € y después hasta exactamente 3.032.010,34 €? En el apartado indemnizatorio, la sentencia no hace una reconstrucción mensual completa: declara que el daño está “correctamente cuantificado” por el principal ejecutado contra Pink una vez no se localizaron bienes embargables, y adopta ese principal como daño contra mí.',
    gainTitle: 'Beneficio personal: ésta es mi acusación; la ruta concreta debe ser investigada',
    gain: '<strong>Alego beneficio personal directo o indirecto y clandestino.</strong> No presento como ya probado quién cobró qué, por qué vehículo o mediante qué contraprestación. Exijo precisamente que se investigue y publique esa ruta: flujos financieros, honorarios, ventajas patrimoniales, relaciones, contraprestaciones, consecuencias sobre activos y cualquier beneficio esperado u obtenido por los intervinientes o personas relacionadas. La ausencia actual de una ruta financiera completa no convierte mi acusación en un hecho adjudicado; la convierte en una acusación concreta y falsable que debe contrastarse con los libros y documentos.',
    status: 'ESTADO PROBATORIO',
    statusBody: '<strong>Documentado:</strong> las cifras, la petición de la AC, la renta mensual, el razonamiento de la Sentencia 163/2023 y la condena. <strong>Mi acusación:</strong> fabricación/falsificación consciente por la AC y el juez para beneficio personal directo o indirecto mantenido clandestinamente. <strong>Abierto:</strong> la reconstrucción matemática completa y la ruta concreta de ese beneficio. Invito a cualquiera de los afectados a aportar la liquidación completa y documentación que corrija o refute esta acusación.',
    note: 'Esta formulación expresa la acusación de Gil Marer. No afirma que exista ya una condena penal por fabricación de la cifra, corrupción o enriquecimiento personal.'
  } : {
    kicker: '€3,032,010.34 · MY ACCUSATION ABOUT THE FIGURE',
    title: 'I accuse the AC and the Judge of knowingly fabricating this amount for direct or indirect personal gain kept clandestine.',
    allegation: '<strong>I accuse insolvency administrator Francisco de Borja Rodríguez-Batllori and Magistrate-Judge Alberto López Villarrubia of knowingly fabricating and/or falsifying the €3,032,010.34 figure</strong> that ultimately became a personal damages award against me, plus legal interest increased by two points. I do not allege a mere arithmetic mistake or an innocent legal disagreement. <strong>I allege that the figure was deliberately constructed and maintained, and that the purpose was to obtain or facilitate direct or indirect personal gain kept clandestine.</strong>',
    evidenceTitle: 'What can already be tested against the documents',
    evidence: [
      ['€24,575/month', 'Judgment 163/2023 records this contractual monthly rent.'],
      ['€1,130,450', 'One appeal identifies 46 months and calculates €24,575 × 46, before deducting rents it says were in fact paid.'],
      ['€2,733,923.64', 'The same appeal challenges this different figure attributed to the insolvency administration’s claim.'],
      ['€3,032,010.34', 'The AC sought this amount against me and the judgment converted it into damages by using the principal dispatched in the Pink enforcement as the measure.']
    ],
    bridgeTitle: 'The question I will not allow to be blurred',
    bridge: 'What is the euro-by-euro bridge from €24,575 per month —including actual payments, credits, set-offs and real operating costs— to €2,733,923.64 and then to exactly €3,032,010.34? In its damages section, the judgment does not set out a complete month-by-month reconstruction. It says the damage is “correctly quantified” by the principal under enforcement against Pink once no attachable assets were located, and adopts that principal as damage against me.',
    gainTitle: 'Personal gain: this is my allegation; the precise route must be investigated',
    gain: '<strong>I allege direct or indirect clandestine personal gain.</strong> I do not present as already proved who received what, through which vehicle or consideration. I demand that the route itself be investigated and published: financial flows, fees, patrimonial advantages, relationships, consideration, asset consequences and any benefit expected or obtained by the participants or related persons. The present absence of a complete financial route does not turn my accusation into an adjudicated fact; it makes it a concrete, falsifiable accusation that must be tested against the books and records.',
    status: 'EVIDENTIAL STATUS',
    statusBody: '<strong>Documented:</strong> the figures, the AC request, the monthly rent, the reasoning in Judgment 163/2023 and the award. <strong>My accusation:</strong> knowing fabrication/falsification by the AC and Judge for direct or indirect personal gain kept clandestine. <strong>Open:</strong> the complete arithmetic reconstruction and the precise benefit route. I invite any affected person to produce the complete calculation and records that correct or disprove this accusation.',
    note: 'This wording states Gil Marer’s accusation. It does not report an existing criminal conviction for fabrication of the amount, corruption or personal enrichment.'
  };

  const style = document.createElement('style');
  style.textContent = `
    .cal-3032{padding:0 0 2rem}.cal-3032-wrap{max-width:1080px;margin:0 auto}.cal-3032-box{border:2px solid #702c2c;border-radius:20px;background:#fff;padding:1.4rem;box-shadow:0 12px 36px rgba(20,30,35,.08)}
    .cal-3032-kicker{font-size:.76rem;letter-spacing:.09em;text-transform:uppercase;font-weight:900;color:#702c2c}.cal-3032-box h2{font-size:clamp(1.65rem,3.5vw,2.4rem);line-height:1.1;margin:.4rem 0 .8rem}.cal-3032-box h3{margin:1.15rem 0 .55rem}.cal-3032-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.75rem;margin:.85rem 0 1rem}.cal-3032-num{border-radius:14px;background:#f7f4ef;padding:1rem;border-top:4px solid #8c6b2f}.cal-3032-num strong{display:block;font-size:1.15rem;margin-bottom:.35rem}.cal-3032-bridge{background:#101f26;color:#fff;border-radius:14px;padding:1rem 1.1rem}.cal-3032-gain{background:#f4e9e6;border-left:6px solid #702c2c;border-radius:14px;padding:1rem 1.1rem}.cal-3032-status{background:#edf1ed;border-radius:14px;padding:1rem 1.1rem;margin-top:.8rem}.cal-3032-note{font-size:.88rem;color:#5b5b5b;margin:.75rem 0 0}
    @media(max-width:850px){.cal-3032-grid{grid-template-columns:1fr 1fr}.cal-3032-box{border-radius:0}}
    @media(max-width:520px){.cal-3032-grid{grid-template-columns:1fr}}
  `;
  document.head.appendChild(style);

  const cards = copy.evidence.map(([n, t]) => `<article class="cal-3032-num"><strong>${n}</strong><span>${t}</span></article>`).join('');
  const section = document.createElement('section');
  section.className = 'section cal-3032';
  section.dataset.calificacion303201020260816 = '1';
  section.innerHTML = `<div class="shell cal-3032-wrap"><div class="cal-3032-box">
    <div class="cal-3032-kicker">${copy.kicker}</div>
    <h2>${copy.title}</h2>
    <p>${copy.allegation}</p>
    <h3>${copy.evidenceTitle}</h3>
    <div class="cal-3032-grid">${cards}</div>
    <div class="cal-3032-bridge"><h3>${copy.bridgeTitle}</h3><p>${copy.bridge}</p></div>
    <div class="cal-3032-gain"><h3>${copy.gainTitle}</h3><p>${copy.gain}</p></div>
    <div class="cal-3032-status"><div class="cal-3032-kicker">${copy.status}</div><p>${copy.statusBody}</p></div>
    <p class="cal-3032-note">${copy.note}</p>
  </div></div>`;

  const opening = document.querySelector('[data-calificacion-opening-20260816]');
  if (opening) opening.insertAdjacentElement('afterend', section);
  else {
    const hero = document.querySelector('.hero.cal-hero') || document.querySelector('main .hero');
    if (hero) hero.insertAdjacentElement('afterend', section);
  }
})();