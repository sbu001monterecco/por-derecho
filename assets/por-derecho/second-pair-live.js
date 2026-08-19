(()=>{
  const root=document.querySelector('[data-second-pair-app]');
  if(!root)return;
  const lang=document.documentElement.lang==='en'?'en':'es';
  const caseId=root.dataset.caseId;
  const dataUrl=root.dataset.data||'/por-derecho/assets/data/icalpa-second-pair-activation.json';
  const tx={
    es:{checks:['Fuente','Autoridad','Perímetro','Contradicción','Consecuencia','Reversibilidad'],status:{'not-checked':'Sin segunda comprobación','open':'Segunda comprobación abierta','survives':'Discrepancia material sobrevive al contraste','resolved':'Preocupación resuelta por segunda comprobación','human':'Juicio humano requerido'},missing:'Desconocido / fuente decisiva pendiente',gate:'Puerta humana',summary:'Estado de activación',open:'Comprobaciones abiertas',resolved:'Preocupaciones resueltas',human:'Decisiones humanas',rule:'Una segunda comprobación puede reforzar, debilitar o resolver una preocupación. No puntúa culpabilidad.'},
    en:{checks:['Source','Authority','Perimeter','Contradiction','Consequence','Reversibility'],status:{'not-checked':'Not second-checked','open':'Second check open','survives':'Material discrepancy survives check','resolved':'Concern resolved by second check','human':'Human judgment required'},missing:'Unknown / decisive source pending',gate:'Human gate',summary:'Activation state',open:'Open checks',resolved:'Concerns resolved',human:'Human decisions',rule:'A second check may strengthen, weaken or resolve a concern. It does not score guilt.'}
  }[lang];
  const el=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n};
  fetch(dataUrl).then(r=>{if(!r.ok)throw new Error(r.status);return r.json()}).then(data=>{
    const c=data.cases.find(x=>x.caseId===caseId);if(!c)throw new Error('case');
    const summary=el('div','sp-summary');
    const stats=[
      [c.checkpoints.length,tx.summary],
      [c.checkpoints.filter(x=>x.status==='open').length,tx.open],
      [c.checkpoints.filter(x=>x.status==='resolved').length,tx.resolved],
      [c.checkpoints.length,tx.human]
    ];
    stats.forEach(([v,l])=>{const a=el('article','sp-stat');a.append(el('strong','',String(v)),el('span','',l));summary.append(a)});
    root.append(summary);
    const note=el('div','sp-boundary');note.append(el('strong','',tx.rule));root.append(note);
    const wrap=el('div','sp-checkpoints');
    c.checkpoints.forEach((cp,i)=>{
      const d=el('details','sp-check');if(i===0)d.open=true;
      const s=el('summary');s.append(el('span','sp-num',String(i+1).padStart(2,'0')),el('span','sp-title',cp.module),el('span','sp-state',tx.status[cp.status]||cp.status));
      const body=el('div','sp-body'),grid=el('div','sp-grid');
      const vals=[cp.source,cp.authority,cp.perimeter,cp.contradiction,cp.consequence,cp.reversibility];
      tx.checks.forEach((label,j)=>{const b=el('div','sp-box');b.append(el('h3','',label),el('p','',vals[j]));grid.append(b)});
      const miss=el('div','sp-missing');miss.append(el('strong','',tx.missing+': '),document.createTextNode(cp.missing));
      const gate=el('div','sp-human');gate.append(el('strong','',tx.gate+': '),document.createTextNode(cp.humanGate));
      body.append(grid,miss,gate);d.append(s,body);wrap.append(d);
    });
    root.append(wrap);
  }).catch(err=>{root.textContent='Second Pair data could not be loaded: '+err.message});
})();
