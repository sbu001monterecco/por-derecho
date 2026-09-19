(() => {
  const path=location.pathname;
  if(!/\/dp-1901-2026-(?:auto-14-septiembre-2026|order-14-september-2026)\//.test(path)) return;
  if(document.getElementById('dp1901-cgpj-response-package')) return;
  const main=document.querySelector('main'); if(!main) return;
  const es=/\/es\//.test(path);
  const base=(()=>{const m=path.match(/^(.*?)(?:\/en\/|\/es\/)/);return m?m[1]:'';})();
  const href=p=>base+p;
  const md='/drafts/cgpj/2026-09-19_DP1901_CGPJ_RESPONSE_PROPOSED.md';
  const pdf='/drafts/cgpj/2026-09-19_DP1901_CGPJ_RESPONSE_PROPOSED.pdf';
  const docx='/drafts/cgpj/2026-09-19_DP1901_CGPJ_RESPONSE_PROPOSED.docx';
  const copy=es?{
    kicker:'RESPUESTA PROPUESTA · 19 SEPTIEMBRE 2026',
    title:'Alzada 286/2026: propuesta completa de aportación por hecho sobrevenido',
    status:'BORRADOR PROPUESTO · NO PRESENTADO · NO REMITIDO',
    statusText:'Esta publicación no equivale a presentar el escrito ante el CGPJ, a interponer un recurso judicial contra el Auto ni a presentar la respuesta de E.G. 745/2026. Las tres vías permanecen separadas.',
    pdfTitle:'PDF propuesto, visible en la propia página',
    fullTitle:'Texto completo legible',
    fullIntro:'Se muestra íntegramente el texto español del borrador propuesto. La versión publicada conserva expresamente la afirmación presencial de que Ref. 24 seguía intacta, sin escanear y sin asignar el 25 de junio, y separa esa afirmación de la certificación electrónica todavía pendiente.',
    galleryTitle:'Galería explicativa recuperada · con correcciones visibles',
    galleryIntro:'Estas seis imágenes se conservan como conceptos editoriales anteriores. No son anexos probatorios formales aprobados. El esquema SVG neutral que encabeza la galería es la referencia visual precisa actual.',
    readFail:'No se pudo cargar aquí el texto completo. Ábralo directamente en Markdown.',
    neutral:'Esquema neutral actual · trazabilidad sin atribuir intención, manipulación o delito.',
    lanes:['CGPJ: borrador de aportación por hecho sobrevenido, no presentado.','Auto 14/09: eventual impugnación judicial separada; esta publicación no la interpone.','E.G. 745/2026: respuesta separada ante Fiscalía; no se presenta desde esta página.'],
    related:'Rutas relacionadas'
  }:{
    kicker:'PROPOSED RESPONSE · 19 SEPTEMBER 2026',
    title:'Appeal 286/2026: complete proposed supervening-event submission',
    status:'PROPOSED DRAFT · NOT FILED · NOT SENT',
    statusText:'Publication is not filing with the CGPJ, does not lodge a judicial challenge to the 14 September order, and does not file the E.G. 745/2026 response. Those three lanes remain distinct.',
    pdfTitle:'Proposed PDF, viewable on this page',
    fullTitle:'Complete readable text',
    fullIntro:'The complete Spanish original of the proposed draft is displayed below. It expressly preserves the firsthand statement that Ref. 24 remained untouched, unscanned and unallocated at Decanato on 25 June, while separating that testimony from the still-outstanding independent electronic-history certification.',
    galleryTitle:'Recovered explanatory gallery · corrections shown',
    galleryIntro:'These six images are preserved as earlier editorial concepts. They are not approved formal evidentiary annexes. The neutral SVG leading the gallery is the current precise visual reference.',
    readFail:'The complete text could not be loaded here. Open the Markdown directly.',
    neutral:'Current neutral scheme · traceability without attributing intent, manipulation or crime.',
    lanes:['CGPJ: proposed supervening-event draft, not filed.','14/09 order: any judicial challenge is a separate lane; this publication does not lodge it.','E.G. 745/2026: separate Public Prosecution response; it is not filed from this page.'],
    related:'Related routes'
  };
  const corrections=es?[
    ['01 · “Una sola fosa”','Metáfora editorial sobre archivos/expedientes. No acredita destrucción, intención ni extinción de denuncia alguna. Los emblemas o escenarios no implican autoría institucional.'],
    ['02 · Decanato','Ilustración conceptual. El fondo representa Catalunya, no Canarias: es geográficamente incorrecto. Ref. 24 = 18/06/2026; su ampliación fue presentada el 25/06. No es imagen oficial.'],
    ['03 · Corpus Fiscalía','El rótulo “Diligencias de Investigación Previas” es incorrecto; el Auto usa “Diligencias de Investigación Preprocesales”. Las flechas no acreditan qué corpus recibió realmente Fiscalía. No es imagen oficial.'],
    ['04 · ATLANTE','La franja 8–17 julio no acredita fecha ni causa de una asociación. Sigue pendiente el historial certificado del sistema. No es captura oficial de ATLANTE.'],
    ['05 · Anexo compuesto','El panel 2 contiene un rótulo erróneo: la carpeta judicial es Ref. 24 / 18 junio, con ampliación de 25 junio, no Ref. 21 / 25 junio. No se usa como anexo probatorio formal.'],
    ['06 · Trazabilidad general','Concepto explicativo anterior. Sus flechas y fechas no sustituyen asientos, índices o metadatos certificados; los escudos no indican autoría institucional.']
  ]:[
    ['01 · “Single grave”','Editorial metaphor concerning files/case folders. It does not prove destruction, intent or extinction of any complaint. Crests or institutional settings do not imply official authorship.'],
    ['02 · Decanato','Conceptual illustration. The background depicts Catalonia rather than the Canary Islands and is geographically wrong. Ref. 24 = 18/06/2026; its supplement was filed on 25/06. Not an official image.'],
    ['03 · Prosecution corpus','“Diligencias de Investigación Previas” is an incorrect expansion; the order says “Diligencias de Investigación Preprocesales”. Arrows do not establish the corpus actually received by prosecutors. Not official.'],
    ['04 · ATLANTE','The 8–17 July band does not prove the date or cause of an association. The certified system history remains outstanding. This is not an official ATLANTE capture.'],
    ['05 · Composite annex','Panel 2 is mislabeled: the judicial folder is Ref. 24 / 18 June with the 25 June supplement, not Ref. 21 / 25 June. It is not used as a formal evidentiary annex.'],
    ['06 · Traceability overview','Earlier explanatory concept. Its arrows and dates do not replace certified entries, indexes or metadata; crests do not indicate institutional authorship.']
  ];
  const imgs=['01-single-grave.png','02-decanato.png','03-fiscal-corpus.png','04-atlante.png','05-composite-annex.png','06-traceability-overview.png'];
  const routes=es?[
    ['DP 1901','/es/dp-1901-2026/'],['Ref. 21','/es/control-21-denuncia-actores-privados-25-junio-2026/'],['Ref. 24','/es/control-24-denuncia-juez-concurso-36-2012/'],['CGPJ','/es/cgpj-comision-permanente-sala-lectura/'],['TSJC','/es/tsj-canarias-exp-gub-38-2026/'],['DIP 2','/es/fiscalia-dip-2-2026/'],['E.G. 745','/es/fiscalia-inspeccion-exp-gub-745-2026/']
  ]:[
    ['DP 1901','/en/dp-1901-2026/'],['Ref. 21','/en/control-21-private-actors-complaint-25-june-2026/'],['Ref. 24','/en/control-24-insolvency-judge-complaint-36-2012/'],['CGPJ','/en/cgpj-permanent-commission-reader-room/'],['TSJC','/en/tsj-canarias-exp-gub-38-2026/'],['DIP 2','/en/fiscalia-dip-2-2026/'],['E.G. 745','/en/public-prosecution-inspection-exp-gub-745-2026/']
  ];
  const wrap=document.createElement('div');
  wrap.id='dp1901-cgpj-response-package';
  wrap.innerHTML=`
  <style>
  #dp1901-cgpj-response-package{--ink:#13252d;--line:rgba(19,37,45,.16);--paper:#fbfaf6;--warn:#8f2d27;color:var(--ink)}
  #dp1901-cgpj-response-package .pd-shell{max-width:1120px;margin:auto;padding:0 1rem}
  #dp1901-cgpj-response-package section{padding:2rem 0}
  #dp1901-cgpj-response-package .pd-card{background:#fff;border:1px solid var(--line);border-radius:16px;padding:1.15rem}
  #dp1901-cgpj-response-package .pd-status{border-left:7px solid var(--warn);background:#fff5f2}
  #dp1901-cgpj-response-package .pd-k{font-size:.78rem;letter-spacing:.1em;font-weight:900;text-transform:uppercase}
  #dp1901-cgpj-response-package .pd-actions,#dp1901-cgpj-response-package .pd-routes{display:flex;gap:.55rem;flex-wrap:wrap;margin:.9rem 0}
  #dp1901-cgpj-response-package .pd-actions a,#dp1901-cgpj-response-package .pd-routes a{display:inline-block;padding:.55rem .75rem;border-radius:999px;border:1px solid var(--line);background:#fff;text-decoration:none;font-weight:800}
  #dp1901-cgpj-response-package .pd-pdf{background:#10252e;border-radius:18px;padding:.8rem}
  #dp1901-cgpj-response-package .pd-pdf object{width:100%;height:min(82vh,900px);min-height:620px;background:#fff;border:0;border-radius:12px}
  #dp1901-cgpj-response-package pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#fff;border:1px solid var(--line);border-radius:16px;padding:1.2rem;font:15px/1.58 ui-monospace,SFMono-Regular,Consolas,monospace;max-height:none}
  #dp1901-cgpj-response-package .pd-neutral img{width:100%;height:auto;border:1px solid var(--line);border-radius:14px;background:#fff}
  #dp1901-cgpj-response-package .pd-gallery{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}
  #dp1901-cgpj-response-package figure{margin:0;background:#fff;border:1px solid var(--line);border-radius:16px;overflow:hidden}
  #dp1901-cgpj-response-package figure img{width:100%;height:auto;display:block;background:#eee}
  #dp1901-cgpj-response-package figcaption{padding:.9rem 1rem}
  #dp1901-cgpj-response-package figcaption strong{display:block;margin-bottom:.35rem}
  #dp1901-cgpj-response-package .pd-lanes{display:grid;gap:.5rem;margin:.9rem 0;padding-left:1.2rem}
  @media(max-width:760px){#dp1901-cgpj-response-package .pd-gallery{grid-template-columns:1fr}#dp1901-cgpj-response-package .pd-pdf object{min-height:520px;height:72vh}}
  </style>
  <section id="response-pdf"><div class="pd-shell">
    <p class="pd-k">${copy.kicker}</p><h2>${copy.title}</h2>
    <div class="pd-card pd-status"><strong>${copy.status}</strong><p>${copy.statusText}</p><ul class="pd-lanes">${copy.lanes.map(x=>'<li>'+x+'</li>').join('')}</ul></div>
    <div class="pd-actions"><a href="${href(pdf)}" target="_blank" rel="noopener">PDF</a><a href="${href(docx)}" download>Word / DOCX</a><a href="${href(md)}" target="_blank" rel="noopener">Markdown</a></div>
    <h3>${copy.pdfTitle}</h3><div class="pd-pdf"><object data="${href(pdf)}#view=FitH" type="application/pdf"><p style="background:#fff;padding:1rem"><a href="${href(pdf)}">Open PDF</a></p></object></div>
  </div></section>
  <section id="response-full"><div class="pd-shell"><h2>${copy.fullTitle}</h2><p>${copy.fullIntro}</p><pre id="dp1901-cgpj-full-text" lang="es">…</pre><p id="dp1901-cgpj-read-fallback" hidden><a href="${href(md)}">${copy.readFail}</a></p></div></section>
  <section id="visual-gallery"><div class="pd-shell"><h2>${copy.galleryTitle}</h2><p>${copy.galleryIntro}</p>
    <div class="pd-card pd-neutral"><strong>${copy.neutral}</strong><img src="${href('/assets/visuals/dp1901-routing-collision-20260919.svg')}" alt="${copy.neutral}"></div>
    <div class="pd-gallery" style="margin-top:1rem">${imgs.map((src,i)=>`<figure><img loading="lazy" src="${href('/assets/visuals/dp1901-20260919/'+src)}" alt="${corrections[i][0]}"><figcaption><strong>${corrections[i][0]}</strong>${corrections[i][1]}</figcaption></figure>`).join('')}</div>
    <h3 style="margin-top:1.5rem">${copy.related}</h3><nav class="pd-routes">${routes.map(([t,u])=>`<a href="${href(u)}">${t}</a>`).join('')}</nav>
  </div></section>`;
  main.appendChild(wrap);
  if(location.hash && ['#response-pdf','#response-full','#visual-gallery'].includes(location.hash)){requestAnimationFrame(()=>document.querySelector(location.hash)?.scrollIntoView({block:'start'}));}
  fetch(href(md),{cache:'no-store'}).then(r=>{if(!r.ok) throw new Error('HTTP '+r.status); return r.text();}).then(t=>{document.getElementById('dp1901-cgpj-full-text').textContent=t;}).catch(()=>{document.getElementById('dp1901-cgpj-full-text').textContent='';document.getElementById('dp1901-cgpj-read-fallback').hidden=false;});
})();