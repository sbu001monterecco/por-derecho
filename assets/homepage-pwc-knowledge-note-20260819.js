(()=>{
  const d=document;
  const path=location.pathname.replace(/\/+$/,'/');
  const en=path.endsWith('/en/');
  const es=path.endsWith('/es/');
  if(!en&&!es)return;

  const render=()=>{
    if(d.querySelector('[data-home-pwc-knowledge-note]'))return;
    const actorGrid=d.querySelector('#private-actors + .actor-grid, #private-actors ~ .actor-grid');
    if(!actorGrid)return;

    const style=d.createElement('style');
    style.textContent=`
      .home-pwc-note{margin:.8rem 0 1.15rem;border:2px solid #8c2f2c;border-radius:16px;background:#fff8f5;box-shadow:0 6px 20px rgba(19,37,45,.09);overflow:hidden;position:relative}
      .home-pwc-note:before{content:"";display:block;width:56%;max-width:680px;height:3px;background:#8c2f2c;margin:0 0 0 0}
      .home-pwc-note__inner{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(260px,.75fr);gap:1rem;padding:1rem 1.1rem}
      .home-pwc-note__k{font-size:.74rem;font-weight:950;letter-spacing:.08em;text-transform:uppercase;color:#8c2f2c;margin:0 0 .3rem}
      .home-pwc-note__quote{font-size:clamp(1.6rem,3.7vw,2.8rem);line-height:1;font-weight:1000;letter-spacing:-.025em;color:#8c2f2c;margin:.15rem 0 .55rem}
      .home-pwc-note p{margin:.35rem 0;line-height:1.48}
      .home-pwc-note__why{border-left:5px solid #9a6a20;background:#fffdf4;border-radius:10px;padding:.75rem .85rem}
      .home-pwc-note__why strong{display:block;margin-bottom:.25rem}
      .home-pwc-note__boundary{font-size:.88rem;color:#53656d;margin-top:.55rem!important}
      .home-pwc-note__link{display:inline-block;margin-top:.65rem;font-weight:900;text-decoration:none;background:#13252d;color:#fff;padding:.58rem .78rem;border-radius:999px}
      @media(max-width:760px){.home-pwc-note__inner{grid-template-columns:1fr}.home-pwc-note:before{width:100%}.home-pwc-note__quote{font-size:clamp(1.7rem,9vw,2.5rem)}}
    `;
    d.head.appendChild(style);

    const note=d.createElement('aside');
    note.className='home-pwc-note';
    note.dataset.homePwcKnowledgeNote='20260819';
    note.setAttribute('aria-label',es?'Nota de conocimiento profesional PwC 2016':'PwC 2016 professional-knowledge note');
    note.innerHTML=es?`
      <div class="home-pwc-note__inner">
        <div>
          <p class="home-pwc-note__k">PWC · PUNTO DE CONOCIMIENTO PROFESIONAL · 2016 · JUNTO A FMMM / ANTONIO / SHAILA COGOLLUDO</p>
          <div class="home-pwc-note__quote">“LA VÍA PENAL CONTRA ESTA GENTE”</div>
          <p>Mientras PwC/Carlos Saavedra asesoraban sobre Sun Park y la controversia de la Comunidad, el cliente trasladó alegaciones graves sobre el perímetro entonces adverso e instruyó expresamente acudir a <strong>“la vía penal contra esta gente”</strong>. PwC respondió <strong>“Tomamos nota de vuestra decisión”</strong> —Carlos en copia— y posteriormente confirmó contacto directo con el Administrador Concursal.</p>
          <a class="home-pwc-note__link" href="pwc-canarias-carlos-saavedra-sun-park/">Ver expediente PwC / Carlos 2016 →</a>
        </div>
        <div class="home-pwc-note__why">
          <strong>Por qué aparece aquí</strong>
          <p>Fija que las preocupaciones sobre la estructura de Comunidad/control asociada en el expediente a FMMM, Antonio Cogolludo y Shaila Cogolludo estaban siendo elevadas contemporáneamente a asesores profesionales externos en 2016.</p>
          <p class="home-pwc-note__boundary"><strong>Límite:</strong> esto no significa que PwC determinara de forma independiente que FMMM, Antonio Cogolludo o Shaila Cogolludo hubieran cometido delito alguno. Acredita aviso contemporáneo, instrucción penal del cliente y conocimiento profesional.</p>
        </div>
      </div>`:`
      <div class="home-pwc-note__inner">
        <div>
          <p class="home-pwc-note__k">PWC · PROFESSIONAL-KNOWLEDGE CHECKPOINT · 2016 · BESIDE FMMM / ANTONIO / SHAILA COGOLLUDO</p>
          <div class="home-pwc-note__quote">“LA VÍA PENAL CONTRA ESTA GENTE”</div>
          <p>While PwC/Carlos Saavedra were advising on Sun Park and the Community dispute, the client communicated serious allegations concerning the then-adverse perimeter and expressly instructed a move to <strong>“la vía penal contra esta gente”</strong>. PwC replied <strong>“Tomamos nota de vuestra decisión”</strong> —Carlos copied— and later confirmed direct contact with the Insolvency Administrator.</p>
          <a class="home-pwc-note__link" href="pwc-canarias-carlos-saavedra-sun-park/">See the 2016 PwC / Carlos record →</a>
        </div>
        <div class="home-pwc-note__why">
          <strong>Why this note sits here</strong>
          <p>It fixes a contemporaneous professional-knowledge checkpoint: concerns about the Community/control structure associated in the record with FMMM, Antonio Cogolludo and Shaila Cogolludo were being raised with external professional advisers in 2016.</p>
          <p class="home-pwc-note__boundary"><strong>Boundary:</strong> this does not mean PwC independently determined that FMMM, Antonio Cogolludo or Shaila Cogolludo committed a crime. It establishes contemporaneous notice, the client's penal-route instruction and professional knowledge.</p>
        </div>
      </div>`;

    actorGrid.insertAdjacentElement('afterend',note);
  };
  if(d.readyState==='loading')d.addEventListener('DOMContentLoaded',render,{once:true});else render();
})();