
(()=> {
  const p=location.pathname;
  if(!/(dp-1901|gc-cri-008|control-24|gc-hc-010|fiscalia-dip-2|cgpj-permanent-commission-reader-room|cgpj-comision-permanente-sala-lectura|fiscalia-inspeccion-exp-gub-745|referencia-21|daily-reference-21|gc-ref-030)/.test(p)) return;
  const es=p.includes('/es/');
  const root='/por-derecho/';
  const T=es?{
    title:'TRAZABILIDAD DP 1901/2026',
    sub:'Dos presentaciones autónomas; su intersección posterior está documentada, pero el acto puente oficial sigue sin producirse.',
    proven:'DOCUMENTADO',
    provenText:'Ref. 24 (18 junio) y Ref. 21 (25 junio) son presentaciones autónomas. El 9 julio se presentó material privado bajo DP 1901. La providencia de 12 julio enlazó ese DP con DIP 2/2026. El Auto de 14 septiembre lo trató como prevaricación.',
    reported:'RELATO CONTEMPORÁNEO DOCUMENTADO',
    reportedText:'Correos de 9 y 12 julio a profesionales identificaron 1901 como la denuncia CAM/Comunidad y describieron el seguimiento en Plaza 6 antes de conocer el Auto de septiembre. Son evidencia de comprensión contemporánea, no certificado de reparto.',
    open:'SÓLO LA AUTORIDAD PUEDE CERRAR',
    openText:'Documento iniciador, reparto refs. 21/24, campos de objeto/denunciados, historial de asociación, acto de unión/reasignación/segregación, corpus remitido a Fiscalía e informe firmado de 29 julio.',
    boundary:'Ilustraciones de trazabilidad. No atribuyen autoría, intencionalidad ni alteración ilícita. Las transiciones deben acreditarse mediante fuentes oficiales.',
    labels:['REF. 24','REF. 21','DP 1901','DIP 2','FISCAL 29 JUL','AUTO 14 SEP','CGPJ'],
    small:['18 junio · juez / TSJC vía Decanato','25 junio · cinco actores privados','9 julio · material privado presentado','12 julio · vínculo oficial de admisión','corpus y objeto por certificar','sobreseimiento libre','Alzada 286 / trazabilidad'],
    figs:[
      ['01-double-file-metaphor.svg','Dos denuncias autónomas terminan asociadas al mismo DP; el puente oficial sigue abierto.'],
      ['02-decanato-routing.svg','Punto de entrada, registro, reparto y remisión: qué ocurrió con Ref. 21 y Ref. 24.'],
      ['03-fiscal-corpus.svg','Qué corpus y qué objeto procesal recibió Fiscalía antes del informe de 29 julio.'],
      ['04-atlante-traceability.svg','Cronología de estado: el evento de asociación/reclasificación debe salir del registro electrónico.']
    ]
  }:{
    title:'DP 1901/2026 TRACEABILITY',
    sub:'Two autonomous filings are documented; their later intersection is documented, but the official bridge act remains unproduced.',
    proven:'DOCUMENTED',
    provenText:'Ref. 24 (18 June) and Ref. 21 (25 June) were autonomous. On 9 July private-actor material was tendered under DP 1901. The 12 July direction linked that DP to DIP 2/2026. The 14 September order treated it as prevarication.',
    reported:'CONTEMPORANEOUS DOCUMENTED ACCOUNT',
    reportedText:'Emails of 9 and 12 July to professionals identified 1901 as the CAM/Community complaint and recorded follow-up at Plaza 6 before the September order was known. This evidences contemporaneous understanding, not certified allocation.',
    open:'AUTHORITY-ONLY GAP',
    openText:'Initiating document, allocation of refs. 21/24, object/defendant fields, association history, joinder/reassignment/segregation act, corpus sent to Prosecution and signed 29 July report.',
    boundary:'Traceability illustrations. They do not attribute authorship, intent or unlawful alteration. Every transition must be established from official sources.',
    labels:['REF. 24','REF. 21','DP 1901','DIP 2','29 JUL REPORT','14 SEP ORDER','CGPJ'],
    small:['18 June · judge / TSJC via Dean\'s Office','25 June · five private actors','9 July · private material tendered','12 July · official admission link','corpus and object to certify','final dismissal','Appeal 286 / traceability'],
    figs:[
      ['01-double-file-metaphor.svg','Two autonomous filings later appear inside one DP; the official bridge remains open.'],
      ['02-decanato-routing.svg','Entry, registration, allocation and remittal: what happened to Ref. 21 and Ref. 24.'],
      ['03-fiscal-corpus.svg','Which corpus and procedural object reached Prosecution before the 29 July report.'],
      ['04-atlante-traceability.svg','State chronology: the association/reclassification event must come from the electronic audit trail.']
    ]
  };
  const hrefs=es?[
    root+'es/control-24-denuncia-juez-concurso-36-2012/',
    root+'es/referencia-21-denuncia-actores-privados-25-junio-2026/',
    root+'es/dp-1901-2026/',
    root+'es/fiscalia-dip-2-2026/',
    root+'es/dp-1901-2026-auto-14-septiembre-2026/#informe-fiscal',
    root+'es/dp-1901-2026-auto-14-septiembre-2026/',
    root+'es/cgpj-comision-permanente-sala-lectura/'
  ]:[
    root+'en/control-24-insolvency-judge-complaint-36-2012/',
    root+'en/daily-reference-21-private-actor-complaint-25-june-2026/',
    root+'en/dp-1901-2026/',
    root+'en/fiscalia-dip-2-2026/',
    root+'en/dp-1901-2026-order-14-september-2026/#prosecution-report',
    root+'en/dp-1901-2026-order-14-september-2026/',
    root+'en/cgpj-permanent-commission-reader-room/'
  ];
  const classes=['ref24','ref21','dp1901','dip2','fiscal','auto','cgpj'];
  const sec=document.createElement('section'); sec.className='pd1901-router';
  sec.innerHTML='<p class="eyebrow">'+T.title+'</p><p>'+T.sub+'</p>'+
    '<div class="pd1901-ribbon">'+T.labels.map((x,i)=>'<a class="pd1901-step '+classes[i]+'" href="'+hrefs[i]+'"><span>'+x+'</span><small>'+T.small[i]+'</small></a>').join('')+'</div>'+
    '<div class="pd1901-evidence-grid"><article class="pd1901-evidence proven"><h3>'+T.proven+'</h3><p>'+T.provenText+'</p></article><article class="pd1901-evidence reported"><h3>'+T.reported+'</h3><p>'+T.reportedText+'</p></article><article class="pd1901-evidence open"><h3>'+T.open+'</h3><p>'+T.openText+'</p></article></div>'+
    '<div class="pd1901-visuals">'+T.figs.map((f,i)=>'<figure class="pd1901-visual"><img loading="lazy" src="'+root+'assets/dp1901-routing/'+f[0]+'" alt=""><figcaption><strong>G-'+(i+1)+'</strong> · '+f[1]+'</figcaption></figure>').join('')+'</div>'+
    '<div class="pd1901-boundary">'+T.boundary+'</div>';
  const main=document.querySelector('main');
  if(main) main.insertBefore(sec, main.firstChild);
})();
