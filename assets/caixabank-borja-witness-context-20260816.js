(() => {
  const path = window.location.pathname.replace(/\/+$/, '/');
  const enRoutes = [
    '/en/caixabank-valencia-claim/',
    '/en/lender-of-record/',
    '/en/sale-lender-convergence/',
    '/en/insolvency-36-2012-insolvency-administrator/',
    '/en/insolvency-classification-parallel-lives/',
    '/en/insolvency-36-2012-ap-section-4/'
  ];
  const esRoutes = [
    '/es/reclamacion-caixabank-valencia/',
    '/es/acreedor-de-registro/',
    '/es/convergencia-venta-acreedor/',
    '/es/concurso-36-2012-administrador-concursal/',
    '/es/calificacion-concurso-36-2012-vidas-paralelas/',
    '/es/concurso-36-2012-ap-seccion-4/'
  ];
  const isEn = enRoutes.some((r) => path.endsWith(r));
  const isEs = esRoutes.some((r) => path.endsWith(r));
  if (!isEn && !isEs) return;
  if (document.getElementById('caixabank-borja-witness-control')) return;

  const main = document.querySelector('main');
  const hero = main && main.querySelector('.hero, .dossier-hero');
  if (!main || !hero) return;

  const isClaim = path.endsWith('/en/caixabank-valencia-claim/') || path.endsWith('/es/reclamacion-caixabank-valencia/');
  const isAP = path.endsWith('/en/insolvency-36-2012-ap-section-4/') || path.endsWith('/es/concurso-36-2012-ap-seccion-4/');
  const claimHref = isEn ? '../caixabank-valencia-claim/' : '../reclamacion-caixabank-valencia/';

  const section = document.createElement('section');
  section.id = 'caixabank-borja-witness-control';
  section.className = 'section';
  section.innerHTML = isEn
    ? `<div class="shell"><div class="section-head"><div><p class="kicker">SOURCE-CONTROLLED CORRECTION · VALENCIA</p><h2>CaixaBank requested Borja's witness evidence; Aweswell adhered.</h2></div><p>The later court phrase “proposed by claimant and defendant” records the resulting procedural posture after adhesion. It must not be flattened into equal or independent sponsorship.</p></div><article class="thesis-block"><p><strong>Contemporaneous counsel record, 30 October 2024:</strong></p><blockquote><p>“Se admitió la testifical de Borja, a petición de Caixabank, a la cual nos adherimos.”</p></blockquote><p><strong>VERIFIED:</strong> CaixaBank requested/proposed Francisco de Borja Rodríguez-Batllori Laffitte. <strong>VERIFIED:</strong> Aweswell's lawyers subsequently adhered. <strong>VERIFIED:</strong> later court citations use <em>testigo propuesto por la parte actora y demandada</em>.</p><p><strong>Do not paraphrase this as:</strong> “both parties asked for the AC”, “both sides independently wanted Borja”, or “Aweswell chose Borja as its own witness”.</p><p><strong>CLIENT-REPORTED PROCEDURAL CONTEXT:</strong> counsel regarded adherence as defensive/risk-avoidant and did not want to expose Aweswell to procedural prejudice. No contemporaneous lawyer source has yet been located expressly saying “no choice”, “coerced” or equivalent. That express rationale remains an open evidential target.</p><p><strong>Separation/removal sequence:</strong> Rollo 3304/2025 (LPB) and Rollo 3319/2025 (Aweswell) are recorded as accumulated by Auto 223/2026 of 15 July 2026. The strategic objective is a favourable determination before Borja gives his Valencia evidence; no outcome or automatic evidential consequence is assumed.</p><p><strong>Current hearing control:</strong> the 6 November 2025 at 10:00 hearing was suspended at short notice after the opposing expert reported a cancelled flight. The signed court diligence relisted it for 28 January 2027 at 10:00. That procedural incident does not prove tactical delay or affect the merits.</p>${isClaim ? '' : `<p><a class="button" href="${claimHref}">Open the dedicated CaixaBank Valencia claim →</a></p>`}</article><p class="source-policy"><strong>Boundary:</strong> who initiated the witness request is proved. The sequence does not by itself prove that Borja's eventual testimony will favour CaixaBank, nor bias, collusion, conflict, improper coordination or false evidence.</p></div>`
    : `<div class="shell"><div class="section-head"><div><p class="kicker">CORRECCIÓN CONTROLADA POR FUENTE · VALENCIA</p><h2>CaixaBank pidió la testifical de Borja; Aweswell se adhirió.</h2></div><p>La fórmula judicial posterior «propuesto por la parte actora y demandada» describe la posición procesal resultante tras la adhesión. No debe convertirse en patrocinio igual o independiente.</p></div><article class="thesis-block"><p><strong>Registro contemporáneo del abogado, 30 de octubre de 2024:</strong></p><blockquote><p>“Se admitió la testifical de Borja, a petición de Caixabank, a la cual nos adherimos.”</p></blockquote><p><strong>VERIFICADO:</strong> CaixaBank pidió/propuso a Francisco de Borja Rodríguez-Batllori Laffitte. <strong>VERIFICADO:</strong> los abogados de Aweswell se adhirieron después. <strong>VERIFICADO:</strong> las citaciones posteriores utilizan <em>testigo propuesto por la parte actora y demandada</em>.</p><p><strong>No debe parafrasearse como:</strong> «ambas partes pidieron al AC», «ambas partes querían independientemente a Borja» o «Aweswell eligió a Borja como su propio testigo».</p><p><strong>CONTEXTO PROCESAL COMUNICADO POR EL CLIENTE:</strong> los abogados entendían la adhesión como defensiva y orientada a evitar riesgo o perjuicio procesal. Todavía no se ha localizado una fuente contemporánea del abogado que diga expresamente «no teníamos elección», «fuimos coaccionados» o equivalente. Esa explicación expresa sigue siendo un objetivo probatorio abierto.</p><p><strong>Secuencia de separación/remoción:</strong> Rollo 3304/2025 (LPB) y Rollo 3319/2025 (Aweswell) constan acumulados por Auto 223/2026 de 15 de julio de 2026. El objetivo estratégico es obtener una decisión favorable antes de que Borja preste su prueba en Valencia; no se presume resultado ni consecuencia probatoria automática.</p><p><strong>Control actual de la vista:</strong> la vista de 6 de noviembre de 2025 a las 10:00 fue suspendida con escasa antelación después de que el perito de la parte contraria comunicara la cancelación de su vuelo. La diligencia judicial firmada volvió a señalarla para el 28 de enero de 2027 a las 10:00. La incidencia procesal no prueba una dilación táctica ni afecta al fondo.</p>${isClaim ? '' : `<p><a class="button" href="${claimHref}">Abrir la reclamación CaixaBank en Valencia →</a></p>`}</article><p class="source-policy"><strong>Límite:</strong> está probado quién inició la petición de testifical. La secuencia no demuestra por sí sola que la futura declaración de Borja vaya a favorecer a CaixaBank, ni parcialidad, colusión, conflicto, coordinación impropia o testimonio falso.</p></div>`;

  if (isAP) {
    section.classList.add('alt');
  }
  hero.insertAdjacentElement('afterend', section);
})();
