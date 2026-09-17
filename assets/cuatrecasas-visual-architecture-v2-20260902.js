(() => {
  'use strict';
  const p=location.pathname.replace(/\/+$/,'');
  const es=/\/es(?:\/|$)/.test(p);
  if(!/(cuatrecasas|edgeworth|matkator|dp748|sra-cuatrecasas|whole-claim|invoices-payments|facturas-pagos|primary-record|registro-primario)/i.test(p))return;
  if(document.querySelector('[data-cuathub="20260917"]'))return;
  const R='/por-derecho/';
  const items=es?[
    ['DOSSIER','Cuatrecasas / Sun Park',R+'es/cuatrecasas-sun-park/'],
    ['COMPARADOR','Edgeworth / Aweswell',R+'es/comparador-cuatrecasas-edgeworth/'],
    ['PRUEBA','Registro primario',R+'es/cuatrecasas-registro-primario/'],
    ['CIVIL','DP 748 / acción civil',R+'es/cuatrecasas-dp748-accion-civil/'],
    ['CUENTA','Facturas y pagos',R+'es/cuatrecasas-facturas-pagos/'],
    ['EJECUCIÓN','Matkator / ETJ 163/2020',R+'es/registro-activos-derechos-matkator/'],
    ['DEONTOLOGÍA','ICAM / CCACM',R+'es/cuatrecasas-icam-ccacm-2026/'],
    ['BRECHAS','Brechas críticas',R+'es/cuatrecasas-brechas-criticas/']
  ]:[
    ['DOSSIER','Cuatrecasas / Sun Park',R+'en/cuatrecasas-sun-park/'],
    ['COMPARATOR','Edgeworth / Aweswell',R+'en/cuatrecasas-edgeworth-comparator/'],
    ['EVIDENCE','Primary record',R+'en/cuatrecasas-primary-record/'],
    ['CIVIL','DP 748 / civil action',R+'en/cuatrecasas-dp748-civil-action/'],
    ['ACCOUNT','Invoices & payments',R+'en/cuatrecasas-invoices-payments/'],
    ['EXECUTION','Matkator / ETJ 163/2020',R+'en/matkator-8584-hotel-title-remate-restitution/'],
    ['CONDUCT','ICAM / CCACM',R+'en/cuatrecasas-icam-ccacm-2026/'],
    ['LONDON','SRA / London perimeter',R+'en/sra-cuatrecasas-london-professional-conduct/'],
    ['GAPS','Critical gaps',R+'en/cuatrecasas-critical-gaps/']
  ];
  const st=document.createElement('style');st.textContent=`[data-cuathub]{max-width:1180px;margin:1.25rem auto;padding:0 1rem}.ch{background:linear-gradient(145deg,#0d2230,#173847 68%,#6b5120);border-radius:24px;padding:1.2rem;color:#fff}.ch h2{color:#fff;margin:.15rem 0 .55rem}.chk{color:#f3d17a;font-weight:900;font-size:.72rem;letter-spacing:.08em}.chg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.7rem}.chc{display:block;text-decoration:none;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.23);border-radius:14px;padding:.8rem;color:#fff}.chc:hover{background:rgba(255,255,255,.16)}.chc small{display:block;color:#f3d17a;font-weight:900}.chc b{display:block;color:#fff}.chb{margin-top:.8rem;border-left:5px solid #f3d17a;padding:.65rem .8rem;background:rgba(0,0,0,.16);border-radius:10px;font-size:.8rem}.cv{display:grid;grid-template-columns:1fr .9fr 1fr;gap:.75rem;background:#0d2230;border-radius:17px;padding:.8rem;color:#fff}.cvh,.cvf{grid-column:1/-1;text-align:center}.cvh b{font-size:clamp(1.1rem,2.5vw,1.65rem)}.cvp{background:#102b3a;border-radius:13px;overflow:hidden}.cvp img{display:block;width:100%;aspect-ratio:1;object-fit:cover}.cvp div{padding:.55rem}.cvp small{color:#f3d17a}.cvl{display:grid;place-items:center;text-align:center;background:#f3f0e8;color:#152735;border-radius:13px;padding:.7rem}.cvl b{color:#6c172b;font-size:1.4rem}@media(max-width:760px){.chg{grid-template-columns:1fr 1fr}.cv{grid-template-columns:1fr 1fr}.cvl{grid-column:1/-1}}@media(max-width:520px){.chg,.cv{grid-template-columns:1fr}.cvh,.cvf,.cvl{grid-column:auto}}`;document.head.appendChild(st);
  const s=document.createElement('section');s.dataset.cuathub='20260917';s.innerHTML=`<div class="ch"><div class="chk">${es?'DOSSIER CUATRECASAS · NAVEGACIÓN':'CUATRECASAS DOSSIER · NAVIGATION'}</div><h2>${es?'Un expediente conectado. Cada cuestión conserva su propia prueba.':'One connected dossier. Each question keeps its own evidence.'}</h2><div class="chg">${items.map(x=>`<a class="chc" href="${x[2]}"><small>${x[0]}</small><b>${x[1]}</b></a>`).join('')}</div><div class="chb">${es?'Los enlaces son ayudas de reconstrucción. No transfieren responsabilidad, hechos ni conclusiones entre asuntos.':'Links are reconstruction aids. They do not transfer liability, facts or conclusions between matters.'}</div></div>`;
  const a=document.querySelector('.hero .notice,.hero .lead,main .notice,main .lead');if(a&&a.parentElement)a.parentElement.insertAdjacentElement('afterend',s);else(document.querySelector('main')||document.body).prepend(s);
  if(p.includes('cuatrecasas-edgeworth-comparator')){const f=document.querySelector('figure.hero-visual');if(f)f.innerHTML=`<div class="cv"><div class="cvh"><b>SAME JURISPRUDENCE. DIFFERENT ALLEGED FAILURES.</b></div><div class="cvp"><img src="${R}assets/images/robert-tchenguiz/robert-tchenguiz-source-controlled-20260917.webp" alt="Robert Tchenguiz"><div><b>Robert Tchenguiz</b><small>Edgeworth Capital</small></div></div><div class="cvl"><div>TRIBUNAL SUPREMO<br><b>STS 112/2019</b><br>20 February 2019<br><small>ECLI:ES:TS:2019:521</small></div></div><div class="cvp"><img src="${R}assets/images/gil-marer/gil-marer-source-controlled-20260917.webp" alt="Gil Marer"><div><b>Gil Marer</b><small>Aweswell / Sun Rock</small></div></div><div class="cvf">Separate matters · separate evidence · merits unresolved.</div></div><figcaption>Source-controlled explanatory visual using previously supplied portraits. It is not primary evidence and does not imply endorsement by any person depicted.</figcaption>`;}
})();