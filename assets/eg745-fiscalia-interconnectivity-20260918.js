(()=> {
  const lang=(document.documentElement.lang||'es').toLowerCase().startsWith('en')?'en':'es';
  const path=location.pathname;
  const targets=[
    '/fiscalia-inspeccion-exp-gub-745-2026/',
    '/public-prosecution-inspection-exp-gub-745-2026/',
    '/carta-abierta-ministerio-fiscal/',
    '/open-letter-public-prosecution-service/',
    '/dp-1901-2026-auto-14-septiembre-2026/',
    '/dp-1901-2026-order-14-september-2026/',
    '/fiscalia-dip-2-2026/',
    '/calificacion-concurso-36-2012-vidas-paralelas/',
    '/insolvency-classification-parallel-lives/',
    '/ricardo-de-mosteyrin-sampalo/'
  ];
  if(!targets.some(x=>path.includes(x)) || document.getElementById('eg745-fiscalia-bridge')) return;
  const es=lang==='es';
  const links=es?[
    ['Respuesta EG 745','../eg-745-respuesta-inminente-matriz-fiscalia/'],
    ['PDF Fiscalía','../ministerio-fiscal-documentos-pdf/'],
    ['E.G. 745/2026','../fiscalia-inspeccion-exp-gub-745-2026/'],
    ['Ministerio Fiscal','../carta-abierta-ministerio-fiscal/'],
    ['DP 1901/2026','../dp-1901-2026-auto-14-septiembre-2026/'],
    ['Respuesta CGPJ propuesta · 19 sep','../dp-1901-2026-auto-14-septiembre-2026/#response-full'],
    ['Ref. 21','../control-21-denuncia-actores-privados-25-junio-2026/'],
    ['Ref. 24','../control-24-denuncia-juez-concurso-36-2012/'],
    ['CGPJ','../cgpj-comision-permanente-sala-lectura/'],
    ['TSJC','../tsj-canarias-exp-gub-38-2026/'],
    ['DIP 2/2026','../fiscalia-dip-2-2026/'],
    ['Calificación / DI 248','../calificacion-concurso-36-2012-vidas-paralelas/#di248'],
    ['Ricardo de Mosteyrín','../ricardo-de-mosteyrin-sampalo/'],
    ['Mapa de procedimientos','../mapa-procedimientos/#case-prism']
  ]:[
    ['E.G. 745 response','../eg-745-imminent-response-prosecution-matrix/'],
    ['Prosecution PDFs','../public-prosecution-pdf-document-room/'],
    ['E.G. 745/2026','../public-prosecution-inspection-exp-gub-745-2026/'],
    ['Public Prosecution','../open-letter-public-prosecution-service/'],
    ['DP 1901/2026','../dp-1901-2026-order-14-september-2026/'],
    ['Proposed CGPJ response · 19 Sep','../dp-1901-2026-order-14-september-2026/#response-full'],
    ['Ref. 21','../control-21-private-actors-complaint-25-june-2026/'],
    ['Ref. 24','../control-24-insolvency-judge-complaint-36-2012/'],
    ['CGPJ','../cgpj-permanent-commission-reader-room/'],
    ['TSJC','../tsj-canarias-exp-gub-38-2026/'],
    ['DIP 2/2026','../fiscalia-dip-2-2026/'],
    ['Classification / DI 248','../insolvency-classification-parallel-lives/#di248'],
    ['Ricardo de Mosteyrín','../ricardo-de-mosteyrin-sampalo/'],
    ['Proceedings map','../proceedings-map/#case-prism']
  ];
  const sec=document.createElement('section');
  sec.id='eg745-fiscalia-bridge';
  sec.setAttribute('data-eg745-interconnectivity','2026-09-18');
  sec.innerHTML=`
    <div class="shell record" style="max-width:1180px;padding:1.1rem 0 1.35rem">
      <div style="border:1px solid rgba(19,37,45,.16);border-left:6px solid #7b2d26;border-radius:16px;background:#fff7f4;padding:1rem 1.15rem">
        <p style="margin:.1rem 0 .35rem;font-size:.76rem;font-weight:900;letter-spacing:.06em;text-transform:uppercase">${es?'PUENTE E.G. 745 · INTERCONEXIÓN PARA PRESENTACIÓN':'E.G. 745 BRIDGE · FILING INTERCONNECTIVITY'}</p>
        <strong>${es?'Una sola matriz: acto → autor → corpus → tratamiento → efecto → prueba faltante.':'One matrix: act → author → corpus → treatment → effect → missing proof.'}</strong>
        <p style="margin:.55rem 0 .75rem">${es?'La reconstrucción documenta un patrón alegado de tratamiento fiscal asimétrico con efecto protector de facto para el perímetro privado. Ese efecto es una tesis probatoria atribuida, no una declaración de culpabilidad ni prueba automática de intención.':'The reconstruction documents an alleged pattern of asymmetric prosecutorial treatment with a de facto protective effect for the private-actor perimeter. That effect is an attributed evidential thesis, not a finding of guilt or automatic proof of intent.'}</p>
        <nav aria-label="${es?'Interconexión E.G. 745':'E.G. 745 interconnectivity'}" style="display:flex;flex-wrap:wrap;gap:.45rem">
          ${links.map(([t,h])=>`<a href="${h}" style="display:inline-block;padding:.42rem .62rem;border:1px solid rgba(19,37,45,.2);border-radius:999px;background:#fff;text-decoration:none"><strong>${t}</strong></a>`).join('')}
        </nav>
        <p style="margin:.72rem 0 0;font-size:.88rem"><strong>${es?'Control de presentación:':'Filing control:'}</strong> ${es?'la versión de 12 septiembre es predecesora; el parche sucesor de 18 septiembre incorpora DP 1901/D36–D39; no se eleva a PRESENTADO sin justificante REG-AGE/equivalente.':'the 12 September version is the predecessor; the 18 September successor patch incorporates DP 1901/D36–D39; status is not upgraded to FILED without a REG-AGE/equivalent receipt.'}</p>
      </div>
    </div>`;
  const main=document.querySelector('main');
  if(!main) return;
  const hero=main.querySelector(':scope > section.hero, :scope > .hero');
  if(hero && hero.nextSibling) main.insertBefore(sec,hero.nextSibling); else main.insertBefore(sec,main.firstChild);
})();