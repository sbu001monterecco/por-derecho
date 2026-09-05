(()=>{
  'use strict';
  const script=document.currentScript;
  if(!script)return;
  const assetBase=new URL('.',script.src);
  const projectBase=new URL('../',assetBase);
  const relative=decodeURI(location.pathname).replace(projectBase.pathname,'').replace(/index\.html$/,'');
  const eligible=new Set(['es/ric-private-equity-sun-park/','en/ric-private-equity-sun-park/','es/ricpe-responsabilidad-documental/','en/ricpe-documentary-accountability/','es/ricpe-perimetro-accionistas-medios/','en/ricpe-perimeter-shareholders-media/','es/cnmv-ricpe-verificacion/','en/cnmv-ricpe-verification/','es/ricpe-hnt-gc836-trazabilidad/','en/ricpe-hnt-gc836-traceability/','es/ricpe-idoneidad-series-f-g/','en/ricpe-idoneidad-series-f-g/','es/ricpe-idoneidad-aeat-preguntas/','en/ricpe-idoneidad-aeat-public-questions/','es/reconstruccion-unitaria-autoridades-publicas/','en/public-authority-unitary-case-reconstruction/','evidence/ricpe-cnmv/2026-08-27/']);
  if(!eligible.has(relative)||document.getElementById('ricpe-original-accountability'))return;
  const es=relative.startsWith('es/')||!relative.startsWith('en/');
  const lang=es?'es':'en';
  const esc=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const url=p=>new URL(p,projectBase).href;
  const mount=async()=>{
    const host=document.querySelector('main');
    if(!host||document.getElementById('ricpe-original-accountability'))return;
    const response=await fetch(new URL('data/ricpe-original-accountability-20260905.json',assetBase));
    if(!response.ok)throw new Error(`RICPE source index HTTP ${response.status}`);
    const data=await response.json();
    const context=data.routes.find(r=>r[lang]===relative);
    const panel=document.createElement('section');panel.id='ricpe-original-accountability';panel.className='ricpe-original-panel';
    panel.setAttribute('aria-labelledby','ricpe-original-accountability-title');
    const original=url(data.source.path),analysis=url(data.analysis[lang]);
    const redacted=url('evidence/ricpe-cnmv/2026-08-27/RICPE_Canal_Etico_Certificado_Resolucion_27AGO2026_PUBLICO_REDACTADO.pdf');
    panel.innerHTML=`<p>${es?'ACTUALIZACIÓN DOCUMENTAL · 5 SEPTIEMBRE 2026':'DOCUMENTARY UPDATE · 5 SEPTEMBER 2026'}</p><h2 id="ricpe-original-accountability-title">${es?'RICPE: PDF original, archivo y alegación de incumplimiento':'RICPE: original PDF, closure and non-compliance allegation'}</h2><p><strong>${es?'El 27 de agosto se inadmitió y archivó la alerta sin abrir investigación interna.':'The alert was rejected and closed on 27 August without opening an internal investigation.'}</strong> ${es?'Sí consta un examen preliminar declarado y la reserva de valorar nuevas pruebas.':'A stated preliminary examination and provision for assessing new evidence are also recorded.'}</p><p>${esc(context?context['context_'+lang]:(es?'Lector de evidencia: el original íntegro se incorpora como una edición distinta. El PDF redactado y sus seis imágenes anteriores no se sustituyen.':'Evidence reader: the complete original is added as a separate edition. The earlier redacted PDF and six page images are not replaced.'))}</p><p>${es?'Gil Marer, como alertador/informante y perjudicado, alega incumplimiento material y ocultación frente a órganos no conflictuados, inversores y autoridades. El certificado no prueba por sí solo intención, ausencia de traslado o culpabilidad. La explicación completa conserva los límites del art. 35.2.a y la posición contraria de RICPE.':'As an alertador/informante and injured party, Gil Marer alleges substantive non-compliance and concealment from non-conflicted oversight, investors and authorities. The certificate alone does not prove intent, absent circulation or guilt. The complete analysis preserves the article 35.2.a qualification and RICPE’s opposing position.'}</p><p class="links"><a href="${esc(original)}" target="_blank" rel="noopener">${es?'Abrir original PDF · 6 páginas':'Open original PDF · 6 pages'}</a><a href="${esc(analysis)}">${es?'Análisis crítico completo y fuentes':'Full critical analysis and sources'}</a><a href="${esc(redacted)}">${es?'Edición redactada anterior':'Earlier redacted edition'}</a></p><details><summary>${es?'Ver el PDF original aquí':'View the original PDF here'}</summary><p>${es?'Archivo sin modificar, publicado por autorización expresa; contiene los datos de contacto del informante y el identificador de comunicación. No incluye una contraseña secreta.':'Unchanged file published on express authority; it contains the reporting person’s contact details and communication identifier. It includes no secret password.'}</p><iframe title="${es?'Certificado original RICPE, seis páginas':'Original RICPE certificate, six pages'}" src="${esc(original)}#view=FitH" loading="lazy"></iframe><p>SHA-256: <code>${esc(data.source.sha256)}</code></p></details>`;
    if(!document.querySelector('[data-ricpe-original-style]')){const css=document.createElement('link');css.rel='stylesheet';css.href=new URL('ricpe-original-accountability-20260905.css',assetBase).href;css.dataset.ricpeOriginalStyle='true';document.head.append(css);}
    host.prepend(panel);
    if(relative===`${lang}/ric-private-equity-sun-park/`){
      const old=es?'Admisión · investigación · conflictos · preservación · Consejo · fondo no establecidos':'Admission · investigation · conflict review · preservation · Board treatment · merits not established';
      for(const el of host.querySelectorAll('strong'))if(el.textContent.trim()===old){el.dataset.ricpeHistoricalStatus=old;el.textContent=es?'Inadmisión y archivo sin investigación (27/08/2026); controles y circulación pendientes de prueba':'Inadmission and closure without investigation (27 August 2026); controls and circulation require evidence';el.setAttribute('title',es?'Actualiza el estado histórico anterior al cierre; véase el certificado original.':'Updates the historical pre-closure status; see the original certificate.');const container=el.parentElement;for(const label of container.querySelectorAll('span'))if(label.textContent.trim()===(es?'Estado abierto':'Open status'))label.textContent=es?'Estado actualizado':'Updated status';}
    }
    if(location.hash==='#ricpe-original-accountability')panel.scrollIntoView({block:'start'});
  };
  const run=()=>mount().catch(error=>{console.error(error);const host=document.querySelector('main');if(host&&!document.getElementById('ricpe-original-accountability')){const p=document.createElement('p');p.id='ricpe-original-accountability';const a=document.createElement('a');a.href=url(es?'es/ric-private-equity-sun-park/analisis-canal.html':'en/ric-private-equity-sun-park/channel-analysis.html');a.textContent=es?'RICPE: lector estático del PDF original y análisis':'RICPE: static original-PDF reader and analysis';p.append(a);host.prepend(p);}});
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run,{once:true});else run();
})();
