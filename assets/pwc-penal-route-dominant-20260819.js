(()=>{
  const d=document;
  const path=location.pathname.replace(/\/+$/,'/');
  const en=/\/en\/pwc-canarias-carlos-saavedra-sun-park\/$/.test(path);
  const es=/\/es\/pwc-canarias-carlos-saavedra-sun-park\/$/.test(path);
  if(!en&&!es) return;

  const render=()=>{
    if(d.querySelector('[data-pd-pwc-penal-dominant]')) return;
    const hero=d.querySelector('main .hero .record');
    if(!hero) return;

    const style=d.createElement('style');
    style.textContent=`
      .pd-pwc-penal-dominant{margin:1.35rem 0 1.1rem;padding:1.4rem 1.5rem;border:4px solid #8c2f2c;border-radius:20px;background:#fff5f2;color:#13252d;box-shadow:0 8px 28px rgba(19,37,45,.14)}
      .pd-pwc-penal-dominant__label{margin:0 0 .5rem;font-size:.78rem;font-weight:950;letter-spacing:.08em;text-transform:uppercase;color:#8c2f2c}
      .pd-pwc-penal-dominant__quote{margin:.2rem 0 .8rem;font-size:clamp(2rem,5.2vw,4.25rem);line-height:.96;font-weight:1000;letter-spacing:-.035em;color:#8c2f2c}
      .pd-pwc-penal-dominant__date{font-size:.82rem;font-weight:900;text-transform:uppercase;letter-spacing:.06em}
      .pd-pwc-penal-dominant__bridge{margin:.95rem 0 0;padding:.9rem 1rem;border-left:6px solid #9a6a20;background:#fffaf0;border-radius:10px;font-weight:800}
      .pd-pwc-penal-dominant__chain{display:grid;gap:.35rem;margin:1rem 0 0;font-weight:850}
      .pd-pwc-penal-dominant__chain span{display:block}
      .pd-pwc-penal-dominant__arrow{color:#8c2f2c;font-size:1.25rem}
      .pd-pwc-penal-dominant__precision{margin:.9rem 0 0;font-size:.9rem;color:#53656d}
      @media(max-width:700px){.pd-pwc-penal-dominant{padding:1.05rem}.pd-pwc-penal-dominant__quote{font-size:clamp(2rem,12vw,3.3rem)}}
    `;
    d.head.appendChild(style);

    const box=d.createElement('section');
    box.className='pd-pwc-penal-dominant';
    box.dataset.pdPwcPenalDominant='true';
    box.setAttribute('aria-label',es?'Instrucción expresa de vía penal comunicada a PwC':'Express penal-route instruction communicated to PwC');
    box.innerHTML=es?`
      <p class="pd-pwc-penal-dominant__label">19 JULIO 2016 · INSTRUCCIÓN EXPRESA DEL CLIENTE A PWC · CARLOS SAAVEDRA EN COPIA</p>
      <p class="pd-pwc-penal-dominant__quote">“LA VÍA PENAL CONTRA ESTA GENTE”</p>
      <p class="pd-pwc-penal-dominant__date">PwC estaba ultimando la impugnación judicial de los acuerdos de la Comunidad cuando recibió esta instrucción.</p>
      <div class="pd-pwc-penal-dominant__bridge">La frase se refería a los actores y al perímetro adverso identificados en la controversia Sun Park de 2016. <strong>No se reescribe retrospectivamente como si el correo de 2016 hubiera nombrado a RIC Private Equity o Grupo Acosta Matos.</strong> La cuestión probatoria posterior es cómo ese conflicto histórico y sus actores, predecesores o asociados se relacionan —si se relacionan— con el perímetro posteriormente documentado <strong>Grupo Acosta Matos / RIC Private Equity (#RICPE) / Sun Park–MYND</strong> y con la posterior convergencia profesional de PwC/Carlos.</div>
      <div class="pd-pwc-penal-dominant__chain"><span>2016 · PwC asesorando dentro de la respuesta frente al perímetro adverso entonces identificado</span><span class="pd-pwc-penal-dominant__arrow">↓</span><span>“LA VÍA PENAL CONTRA ESTA GENTE”</span><span class="pd-pwc-penal-dominant__arrow">↓</span><span>PwC: “Tomamos nota de vuestra decisión” · Carlos en copia</span><span class="pd-pwc-penal-dominant__arrow">↓</span><span>2019/2020 en adelante · relación documentada de una entidad PwC con RICPE y posterior convergencia profesional Carlos/PwC–Acosta Matos</span><span class="pd-pwc-penal-dominant__arrow">↓</span><span>PREGUNTA ABIERTA · ¿qué cambió, qué conflictos se detectaron y qué salvaguardias se aplicaron?</span></div>
      <p class="pd-pwc-penal-dominant__precision"><strong>Control de precisión:</strong> esta secuencia documenta conocimiento previo, una instrucción penal expresa y convergencias profesionales posteriores. No convierte por sí sola la convergencia posterior en prueba de deslealtad, utilización de información confidencial o ilícito.</p>
    `:`
      <p class="pd-pwc-penal-dominant__label">19 JULY 2016 · EXPRESS CLIENT INSTRUCTION TO PWC · CARLOS SAAVEDRA COPIED</p>
      <p class="pd-pwc-penal-dominant__quote">“LA VÍA PENAL CONTRA ESTA GENTE”</p>
      <p class="pd-pwc-penal-dominant__date">PwC was finalising the court challenge to the Community resolutions when it received this instruction.</p>
      <div class="pd-pwc-penal-dominant__bridge">The phrase referred to the adverse actors and perimeter identified in the 2016 Sun Park dispute. <strong>It is not retrospectively rewritten as though the 2016 email itself named RIC Private Equity or Grupo Acosta Matos.</strong> The later evidential question is how that historical conflict and its actors, predecessors or associates relate — if they relate — to the subsequently documented <strong>Grupo Acosta Matos / RIC Private Equity (#RICPE) / Sun Park–MYND perimeter</strong> and to the later PwC/Carlos professional convergence.</div>
      <div class="pd-pwc-penal-dominant__chain"><span>2016 · PwC advising within the response to the then-identified adverse perimeter</span><span class="pd-pwc-penal-dominant__arrow">↓</span><span>“LA VÍA PENAL CONTRA ESTA GENTE”</span><span class="pd-pwc-penal-dominant__arrow">↓</span><span>PwC: “Tomamos nota de vuestra decisión” · Carlos copied</span><span class="pd-pwc-penal-dominant__arrow">↓</span><span>2019/2020 onward · documented PwC-entity relationship with RICPE and later Carlos/PwC–Acosta Matos professional convergence</span><span class="pd-pwc-penal-dominant__arrow">↓</span><span>OPEN QUESTION · what changed, what conflicts were identified, and what safeguards were applied?</span></div>
      <p class="pd-pwc-penal-dominant__precision"><strong>Precision control:</strong> this sequence documents prior knowledge, an express penal-route instruction and later professional convergence. It does not by itself turn that later convergence into proof of disloyalty, confidential-information misuse or wrongdoing.</p>
    `;

    const lead=hero.querySelector('.lead');
    if(lead) lead.insertAdjacentElement('afterend',box); else hero.prepend(box);
  };

  if(d.readyState==='loading') d.addEventListener('DOMContentLoaded',render,{once:true}); else render();
})();
