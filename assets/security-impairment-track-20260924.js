(() => {
  'use strict';
  const current=document.currentScript;
  if(!current) return;
  const normalise=p=>{ let x=p.replace(/\/index\.html$/,''); if(!x.endsWith('/')) x+='/'; return x; };
  const rawPath=location.pathname.replace(/\/index\\.html$/,'');\n  const langPath=rawPath.match(/\/(?:es|en)\/.+$/);\n  const path=normalise(langPath?langPath[0]:rawPath.replace(/^\/por-derecho(?=\/)/,''));
  const dataUrl=new URL('data/security-impairment-track-v1.json?v=20260924a',current.src);
  const root=new URL('../',current.src);
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const style=()=>{
    if(document.getElementById('pd-security-impairment-style')) return;
    const s=document.createElement('style'); s.id='pd-security-impairment-style';
    s.textContent=`
    .pd-si{margin:1.7rem auto;padding:1.15rem;border:1px solid #d9d3c8;border-radius:1.25rem;background:#fffdf8;color:#102028;box-shadow:0 1rem 2.6rem rgba(16,32,40,.08)}
    .pd-si *{box-sizing:border-box}.pd-si__head{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:1rem;align-items:start;margin-bottom:1rem}
    .pd-si__eyebrow{margin:0 0 .25rem;color:#5f6b6d;font-size:.68rem;font-weight:900;letter-spacing:.11em;text-transform:uppercase}
    .pd-si h2{margin:.05rem 0 .25rem;font:600 clamp(1.45rem,3vw,2.15rem)/1.12 Georgia,serif}.pd-si__sub{margin:0;color:#5f6b6d}
    .pd-si__rule{margin:.9rem 0 1.05rem;padding:.95rem 1rem;border-left:.34rem solid #c58a39;border-radius:.55rem;background:#13252d;color:#fffdf8;font-weight:720;line-height:1.5}
    .pd-si__steps{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:.55rem}.pd-si__step{min-height:9.2rem;padding:.8rem;border-radius:.75rem;border:1px solid rgba(16,32,40,.13);background:#f7f2e8}
    .pd-si__step strong{display:block;margin-bottom:.45rem;font-size:.8rem;letter-spacing:.01em}.pd-si__step p{margin:0;font-size:.77rem;line-height:1.45}
    .pd-si__step[data-tone=teal]{border-top:.35rem solid #146a70;background:#edf7f6}.pd-si__step[data-tone=gold]{border-top:.35rem solid #c58a39;background:#fff7e8}
    .pd-si__step[data-tone=amber]{border-top:.35rem solid #8d4f34;background:#f8ede6}.pd-si__step[data-tone=red]{border-top:.35rem solid #a52d28;background:#fff1ee}
    .pd-si__step[data-tone=darkred]{border:.12rem dashed #651819;border-top:.35rem solid #651819;background:#f5dfd9}
    .pd-si__step.is-focus{outline:.18rem solid #102028;outline-offset:.08rem;transform:translateY(-.08rem)}
    .pd-si__lanes{display:grid;grid-template-columns:1fr 1fr;gap:.75rem;margin-top:.9rem}.pd-si__lane{padding:.85rem;border:1px solid #d9d3c8;border-radius:.8rem;background:#f7f2e8}
    .pd-si__lane h3{margin:0 0 .45rem;font-size:.88rem}.pd-si__lane ul{display:flex;flex-wrap:wrap;gap:.35rem;margin:0;padding:0;list-style:none}.pd-si__lane li{padding:.26rem .48rem;border-radius:999px;background:#fffdf8;border:1px solid #d9d3c8;font-size:.7rem}
    .pd-si__bridge{text-align:center;margin:.55rem 0 0;font-size:.72rem;font-weight:850;color:#146a70}.pd-si__application{margin-top:.95rem;padding:.85rem 1rem;border-left:.3rem solid #146a70;background:#eef6f5;border-radius:.5rem}
    .pd-si__application h3{margin:0 0 .3rem;font-size:.95rem}.pd-si__application p{margin:0;font-size:.82rem;line-height:1.52}
    .pd-si__chain{display:flex;flex-wrap:wrap;align-items:center;gap:.35rem;margin:.8rem 0}.pd-si__chain span{font-size:.7rem;padding:.3rem .5rem;background:#13252d;color:#fff;border-radius:999px}.pd-si__chain b{color:#8d4f34}
    .pd-si__states{display:grid;grid-template-columns:repeat(3,1fr);gap:.5rem;margin:.8rem 0}.pd-si__state{padding:.65rem;border-radius:.65rem;border:1px solid #d9d3c8;background:#fff}
    .pd-si__state strong{display:block;font-size:.67rem;letter-spacing:.06em}.pd-si__state span{display:block;margin-top:.25rem;font-size:.72rem;line-height:1.4}
    .pd-si__limits{padding:.72rem .85rem;border:1px dashed #a52d28;border-radius:.65rem;background:#fff8f5;font-size:.75rem;line-height:1.5}
    .pd-si details{margin-top:.8rem;border-top:1px solid #d9d3c8;padding-top:.7rem}.pd-si summary{cursor:pointer;font-weight:800}.pd-si__law{display:grid;grid-template-columns:12rem 1fr;gap:.65rem;padding:.55rem 0;border-bottom:1px solid #ece6dc;font-size:.75rem}.pd-si__law:last-child{border-bottom:0}.pd-si__law a{font-weight:800;color:#146a70}.pd-si__foot{display:flex;justify-content:space-between;gap:.8rem;align-items:center;margin-top:.85rem;font-size:.72rem}.pd-si__foot a{font-weight:850;color:#146a70}
    @media(max-width:900px){.pd-si__steps{grid-template-columns:1fr 1fr}.pd-si__step{min-height:0}.pd-si__lanes{grid-template-columns:1fr}.pd-si__law{grid-template-columns:1fr}.pd-si__head{grid-template-columns:1fr}}
    @media(max-width:560px){.pd-si{padding:.8rem}.pd-si__steps,.pd-si__states{grid-template-columns:1fr}.pd-si__foot{display:block}.pd-si__foot a{display:inline-block;margin-top:.55rem}}
    `; document.head.appendChild(s);
  };
  fetch(dataUrl).then(r=>{if(!r.ok) throw new Error('track data '+r.status); return r.json();}).then(d=>{
    const route=d.routes.find(r=>normalise(r.path)===path); if(!route) return;
    const L=route.lang==='es'?'es':'en'; style();
    const labels=L==='es'?{
      app:'Qué aporta esta página',bridge:'Jurídicamente distintos · económicamente interdependientes',
      doc:'DOCUMENTADO',alg:'ALEGADO / ATRIBUCIÓN PENDIENTE',open:'EFECTO JURÍDICO ABIERTO',
      legal:'Base jurídica — abrir',fals:'Regla de falsificación',deep:'Abrir análisis canónico completo →',
      chain:['derecho formal','conducta atribuible alegada','deterioro','DD / valor / garantía sustitutiva','no-cierre / déficit posterior'],
      falsText:'Cada flecha exige su propio puente de fuente. Cronología ≠ causalidad; relación ≠ atribución; daño ≠ cuantificación; alegación penal ≠ hallazgo penal.'
    }:{
      app:'What this page contributes',bridge:'Legally distinct · economically interdependent',
      doc:'DOCUMENTED',alg:'ALLEGED / ATTRIBUTION REQUIRED',open:'LEGAL EFFECT OPEN',
      legal:'Legal basis — open',fals:'Falsification rule',deep:'Open the canonical full analysis →',
      chain:['formal right','alleged attributable conduct','impairment','DD / value / replacement security','later non-completion / deficiency'],
      falsText:'Every arrow requires its own source bridge. Chronology ≠ causation; relationship ≠ attribution; damage ≠ quantum; criminal allegation ≠ criminal finding.'
    };
    const hub=new URL(L==='es'?'es/garantia-deterioro-causacion-acreedor/':'en/security-impairment-creditor-causation/',root).href;
    const steps=d.stages.map(x=>`<article class="pd-si__step ${x.id===route.focus?'is-focus':''}" data-tone="${esc(x.tone)}"><strong>${esc(x.label[L])}</strong><p>${esc(x.body[L])}</p></article>`).join('');
    const lanes=d.lanes.map(x=>`<article class="pd-si__lane"><h3>${esc(x.label[L])}</h3><ul>${x.items[L].map(i=>`<li>${esc(i)}</li>`).join('')}</ul></article>`).join('');
    const laws=d.legal_basis.map(x=>`<div class="pd-si__law"><a href="${esc(x.url)}" target="_blank" rel="noopener">${esc(x.label)}</a><span>${esc(x.note[L])}</span></div>`).join('');
    const chain=labels.chain.map((x,i)=>`${i?'<b>→</b>':''}<span>${esc(x)}</span>`).join('');
    const section=document.createElement('section'); section.className='pd-si'; section.setAttribute('data-security-impairment-track',d.track_id);
    section.innerHTML=`<div class="pd-si__head"><div><p class="pd-si__eyebrow">${esc(d.track_id)} · ${esc(d.control_date)}</p><h2>${esc(d.title[L])}</h2><p class="pd-si__sub">${esc(d.subtitle[L])}</p></div></div>
      <div class="pd-si__rule">${esc(d.core_rule[L])}</div><div class="pd-si__steps">${steps}</div>
      <div class="pd-si__lanes">${lanes}</div><p class="pd-si__bridge">${esc(labels.bridge)}</p>
      <div class="pd-si__application"><h3>${esc(labels.app)}</h3><p>${esc(route.contribution)}</p></div>
      <div class="pd-si__chain">${chain}</div>
      <div class="pd-si__states"><div class="pd-si__state"><strong>${esc(labels.doc)}</strong><span>${esc(route.documented)}</span></div><div class="pd-si__state"><strong>${esc(labels.alg)}</strong><span>${esc(route.alleged)}</span></div><div class="pd-si__state"><strong>${esc(labels.open)}</strong><span>${esc(route.open)}</span></div></div>
      <div class="pd-si__limits"><strong>${esc(labels.fals)}:</strong> ${esc(labels.falsText)}<br><br>${esc(d.anti_overstatement[L])}</div>
      <details><summary>${esc(labels.legal)}</summary>${laws}</details>
      <div class="pd-si__foot"><span>${esc(d.subtitle[L])}</span><a href="${hub}">${esc(labels.deep)}</a></div>`;
    let anchor=route.selector?document.querySelector(route.selector):null;
    if(!anchor) anchor=document.querySelector('main .section, main section, main article, main');
    if(!anchor) return;
    if(route.position==='before') anchor.insertAdjacentElement('beforebegin',section);
    else if(route.position==='append') anchor.appendChild(section);
    else anchor.insertAdjacentElement('afterend',section);
  }).catch(()=>{});
})();
