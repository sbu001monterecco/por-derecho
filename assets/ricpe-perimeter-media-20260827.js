/* RICPE-PERIMETER-MEDIA-20260827 */
(() => {
  const norm = p => { let x=p.replace(/\/index\.html$/,'/'); if(!x.endsWith('/')) x+='/'; return x; };
  const path=norm(location.pathname);
  const supported=['/es/ric-private-equity-sun-park/','/en/ric-private-equity-sun-park/','/es/cnmv-ricpe-verificacion/','/en/cnmv-ricpe-verification/'].some(r=>path.endsWith(r));
  if(!supported) return;
  const run=(n=0)=>{
    if(document.querySelector('[data-ricpe-perimeter-media-20260827]')) return;
    const anchor=document.querySelector('[data-ricpe-cnmv-visual-evidence-20260827]')||document.querySelector('[data-ricpe-cnmv-closure-20260827]');
    if(!anchor){if(n<20)setTimeout(()=>run(n+1),50);return;}
    const en=document.documentElement.lang==='en';
    const base=path.includes('/por-derecho/')?'/por-derecho/':'/';
    const href=base+(en?'en/ricpe-perimeter-shareholders-media/':'es/ricpe-perimetro-accionistas-medios/');
    const s=document.createElement('style');s.textContent='[data-ricpe-perimeter-media-20260827]{padding:2rem 0;background:linear-gradient(120deg,#12242c,#253f47);color:#fff}[data-ricpe-perimeter-media-20260827] .rpw{max-width:1180px;margin:auto;padding:0 1.1rem}[data-ricpe-perimeter-media-20260827] h2{color:#fff;max-width:28ch;font-size:clamp(1.7rem,3vw,2.7rem);line-height:1.08}[data-ricpe-perimeter-media-20260827] p{max-width:88ch;color:#dbe6e9;line-height:1.6}[data-ricpe-perimeter-media-20260827] a{display:inline-block;margin-top:.5rem;padding:.75rem 1rem;border-radius:999px;background:#fff;color:#13252d;text-decoration:none;font-weight:900}';document.head.appendChild(s);
    const sec=document.createElement('section');sec.dataset.ricpePerimeterMedia20260827='true';sec.innerHTML=`<div class="rpw"><p>${en?'UNITARY PERIMETER · FOUNDERS · BOARD · INVESTORS · MEDIA':'PERÍMETRO UNITARIO · FUNDADORES · CONSEJO · INVERSORES · MEDIOS'}</p><h2>${en?'Who surrounded RICPE, what was publicly represented, and when did Sun Park enter the capital story?':'¿Quién estaba alrededor de RICPE, qué se representó públicamente y cuándo entró Sun Park en la historia del capital?'}</h2><p>${en?'A new control page separates publicly identified founders/shareholders, the CNMV-registered board, series/investor questions, project vehicles, Sun Park/MYND Yaiza events and Canary/Spanish media coverage. It also marks the current shareholder denominator as an open evidential gap rather than guessing it.':'Una nueva página de control separa fundadores/accionistas públicamente identificados, Consejo inscrito en CNMV, preguntas sobre series e inversores, vehículos de proyecto, eventos Sun Park/MYND Yaiza y cobertura mediática canaria/española. El denominador accionarial actual queda expresamente marcado como gap abierto, sin inferencias.'}</p><a href="${href}">${en?'Open full perimeter and media reconstruction →':'Abrir reconstrucción completa de perímetro y medios →'}</a></div>`;anchor.insertAdjacentElement('afterend',sec);
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',()=>run(),{once:true});else run();
})();