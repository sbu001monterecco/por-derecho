(()=>{
  const d=document,path=location.pathname.replace(/\/+$/,'/');
  const es=/\/es\//.test(path);
  if(!/\/(en|es)\/rsm\/nnr4-1025c2f66\/$/.test(path))return;
  const run=()=>{
    const board=d.querySelector('.board');
    if(board){const items=[...board.children];const last=items[items.length-1];if(last)last.innerHTML=`<strong>${es?'Actualizado':'Updated'}</strong>${es?'19 agosto 2026':'19 August 2026'}`;}
    const tl=d.querySelector('.timeline');
    if(tl&&!tl.querySelector('[data-rsm-19aug-san-telmo]')){
      const a=d.createElement('article');a.dataset.rsm19augSanTelmo='true';
      a.innerHTML=es?`<time datetime="2026-08-19">19 ago 2026</time><div><strong>Nuevo elemento documental · San Telmo ↔ RICPE ↔ Sun Park.</strong><p>La revisión íntegra del registro contemporáneo de 30 noviembre 2021 identifica una conexión que no debe fragmentarse: Eduardo Sánchez, socio de San Telmo, manifiesta que “el despacho” introdujo varios clientes en la inversión RICPE conectada con el proyecto hotelero Acosta Matos / Sun Park, mientras el Administrador Concursal del concurso que afectaba al mismo activo operaba dentro del perímetro profesional San Telmo. La transmisión de información entre ambos profesionales, coordinación o ilicitud no se presumen: deben determinarse mediante los registros heredados.</p></div>`:`<time datetime="2026-08-19">19 Aug 2026</time><div><strong>New documentary development · San Telmo ↔ RICPE ↔ Sun Park.</strong><p>The full contemporaneous 30 November 2021 record identifies a connection that should not be fragmented: San Telmo partner Eduardo Sánchez states that “the firm” put several clients into the RICPE investment connected to the Acosta Matos / Sun Park hotel project, while the Insolvency Administrator in the insolvency affecting the same asset operated within the San Telmo professional perimeter. Information transfer between the two professionals, coordination or unlawfulness are not presumed; they must be determined from the legacy records.</p></div>`;
      tl.appendChild(a);
    }
  };
  if(d.readyState==='loading')d.addEventListener('DOMContentLoaded',run,{once:true});else run();
})();