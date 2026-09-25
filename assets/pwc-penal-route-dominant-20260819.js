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

(()=>{
  const d=document;
  const path=location.pathname.replace(/\/+$/,'/');
  const routes={
    enPwC:'/en/pwc-canarias-carlos-saavedra-sun-park/',
    esPwC:'/es/pwc-canarias-carlos-saavedra-sun-park/',
    enAC:'/en/insolvency-36-2012-insolvency-administrator/',
    esAC:'/es/concurso-36-2012-administrador-concursal/',
    enCal:'/en/insolvency-classification-parallel-lives/',
    esCal:'/es/calificacion-concurso-36-2012-vidas-paralelas/'
  };
  const key=Object.keys(routes).find(k=>path.endsWith(routes[k]));
  if(!key) return;
  const es=key.startsWith('es');
  const isAC=key.endsWith('AC');
  const isCal=key.endsWith('Cal');

  const render=()=>{
    if(d.querySelector('[data-pd-pwc-ac-knowledge-transfer]')) return;
    const main=d.querySelector('main');
    if(!main) return;
    const style=d.createElement('style');
    style.textContent=`
      .pd-kt{max-width:1140px;margin:1.6rem auto;padding:1.35rem;border:2px solid #315c7b;border-radius:20px;background:#f7f9fa;color:#13252d;box-shadow:0 7px 24px rgba(19,37,45,.1)}
      .pd-kt__k{font-size:.76rem;font-weight:950;letter-spacing:.08em;text-transform:uppercase;color:#7e2929}
      .pd-kt h2{font-size:clamp(1.65rem,3.6vw,2.65rem);line-height:1.05;margin:.35rem 0 .7rem}.pd-kt__flow{font-size:clamp(1.2rem,3vw,2rem);font-weight:1000;text-align:center;padding:1rem;background:#13252d;color:#fff;border-radius:14px;margin:1rem 0}.pd-kt__flow b{color:#f0dfc4}
      .pd-kt__chron{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.75rem;margin:1rem 0}.pd-kt__chron article{background:#fff;border-top:5px solid #8c2f2c;border-radius:13px;padding:.9rem}.pd-kt__chron strong{display:block;margin-bottom:.35rem}
      .pd-kt__table{width:100%;border-collapse:collapse;background:#fff;margin:1rem 0}.pd-kt__table th,.pd-kt__table td{border:1px solid #d6dddd;padding:.7rem;vertical-align:top;text-align:left}.pd-kt__table th{background:#e9eeee}.pd-kt__q{border-left:6px solid #9a6a20;background:#fff8dc;border-radius:12px;padding:1rem;font-weight:800}.pd-kt__down{border-left:6px solid #7e2929;background:#fff5f2;border-radius:12px;padding:1rem;margin-top:.8rem}.pd-kt__precision{font-size:.9rem;color:#53656d;margin-top:.8rem}.pd-kt a{font-weight:850}
      @media(max-width:800px){.pd-kt__chron{grid-template-columns:1fr}.pd-kt__table{font-size:.88rem;display:block;overflow-x:auto}}
    `;
    d.head.appendChild(style);
    const sec=d.createElement('section');
    sec.className='pd-kt';
    sec.dataset.pdPwcAcKnowledgeTransfer='true';
    const pwcHref=es?'../pwc-canarias-carlos-saavedra-sun-park/':'../pwc-canarias-carlos-saavedra-sun-park/';
    const acHref=es?'../concurso-36-2012-administrador-concursal/':'../insolvency-36-2012-insolvency-administrator/';
    const calHref=es?'../calificacion-concurso-36-2012-vidas-paralelas/':'../insolvency-classification-parallel-lives/';
    sec.innerHTML=es?`
      <div class="pd-kt__k">CONOCIMIENTO · TRANSMISIÓN · ADMINISTRADOR CONCURSAL · RECONSTRUCCIÓN DOCUMENTAL</div>
      <h2>¿Quién sabía qué — y qué se transmitió al Administrador Concursal?</h2>
      <p>La secuencia documentada crea una cuestión de transferencia de conocimiento, no una presunción automática: <strong>antes del contacto directo confirmado PwC–AC, PwC/Carlos ya habían recibido alegaciones que el cliente consideraba potencialmente penales y una instrucción expresa de acudir a “la vía penal contra esta gente”.</strong></p>
      <div class="pd-kt__flow">CLIENTE → <b>PWC / CARLOS SAAVEDRA</b> → ADMINISTRADOR CONCURSAL</div>
      <div class="pd-kt__chron"><article><strong>12 JUN 2016 · AVISO DIRECTO</strong>Patricia escribe a Carlos y Miguel, atribuyendo parte del contexto a lo explicado por Carlos, Jonathan y Cristo, y expone alegaciones graves sobre deuda, control, liquidación y posible fraude/conducta penal.</article><article><strong>19–20 JUL 2016 · VÍA PENAL</strong>Mientras PwC ultimaba la impugnación de acuerdos de Comunidad, el cliente reitera “la vía penal contra esta gente”. Miguel/PwC responde “Tomamos nota de vuestra decisión”; Carlos está en copia.</article><article><strong>SEP 2016 · CONTACTO PWC–AC</strong>PwC confirma que habló directamente con el AC sobre la propuesta de touroperador/nuevo contrato de explotación. PwC limita el alcance: conversación telefónica general, sin detalle contractual, informe ni emails; Patricia pide inmediatamente que se documente qué se dijo y qué respondió el AC.</article></div>
      <table class="pd-kt__table"><thead><tr><th>Qué sabía PwC/Carlos</th><th>Qué sabía el AC independientemente</th><th>Qué transmisión está probada</th><th>Qué falta</th></tr></thead><tbody><tr><td>Alegaciones del cliente sobre deuda discutida, control/liquidación, actuación de terceros y posible dimensión penal; respuesta jurídica en curso; instrucción penal expresa.</td><td><strong>Debe reconstruirse fuente por fuente.</strong> No se atribuye al AC conocimiento por mera inferencia. Deben separarse comunicaciones directas, escritos, reuniones, expediente concursal y otras fuentes.</td><td>Existió conversación directa PwC–AC sobre la ruta de touroperador/nuevo contrato de explotación. La existencia del contacto está confirmada por PwC.</td><td>Contenido exacto de la llamada; participantes; notas/calendario; borradores o “informe para el AC”; qué alegaciones se trasladaron; qué contestó el AC; qué hizo después con la información.</td></tr></tbody></table>
      <p class="pd-kt__q"><strong>Pregunta central:</strong> cuando PwC habló directamente con el Administrador Concursal ya poseía conocimiento documentado de alegaciones que su cliente consideraba potencialmente penales. ¿Qué comunicó exactamente PwC al AC, qué sabía éste ya por otras vías, qué entendió y dónde está el registro de lo que hizo con ese conocimiento?</p>
      ${(isAC||isCal)?`<p class="pd-kt__down"><strong>Consecuencia para el concurso y la calificación:</strong> si el AC tenía conocimiento independiente o transmitido de hechos materiales atribuidos a terceros, ¿cómo influyó —o por qué no aparece que influyera— en el tratamiento de la deuda de Comunidad discutida, control/liquidación, responsabilidad de terceros, causalidad alternativa y posterior calificación? La pregunta exige reconstrucción documental; no presume respuesta ni intención.</p>`:''}
      <p class="pd-kt__down"><strong>Puente posterior a comprobar:</strong> 2016 conocimiento PwC + contacto AC → decisiones posteriores dentro del concurso → perímetro posteriormente documentado <strong>Grupo Acosta Matos / RIC Private Equity (#RICPE) / Sun Park–MYND</strong>. Esta secuencia justifica preguntar por continuidad, conocimiento y conflictos; no prueba por sí sola concertación, transmisión de todas las alegaciones ni conducta criminal.</p>
      <p class="pd-kt__precision"><strong>Control probatorio:</strong> no se afirma que PwC “imputara conocimiento penal” al AC como hecho consumado. Lo probado es el conocimiento previo de PwC y el contacto directo posterior con el AC. El contenido transferido es precisamente la cuestión abierta. <a href="${pwcHref}">PwC/Carlos</a> · <a href="${acHref}">Administrador Concursal</a> · <a href="${calHref}">Calificación</a>.</p>
    `:`
      <div class="pd-kt__k">KNOWLEDGE · TRANSFER · INSOLVENCY ADMINISTRATOR · DOCUMENTARY RECONSTRUCTION</div>
      <h2>Who knew what — and what passed to the Insolvency Administrator?</h2>
      <p>The documented sequence creates a knowledge-transfer question, not an automatic presumption: <strong>before the confirmed direct PwC–Administrator contact, PwC/Carlos had already received allegations the client regarded as potentially criminal and an express instruction to pursue “la vía penal contra esta gente”.</strong></p>
      <div class="pd-kt__flow">CLIENT → <b>PWC / CARLOS SAAVEDRA</b> → INSOLVENCY ADMINISTRATOR</div>
      <div class="pd-kt__chron"><article><strong>12 JUN 2016 · DIRECT NOTICE</strong>Patricia writes to Carlos and Miguel, attributes part of the context to what Carlos, Jonathan and Cristo had explained, and sets out serious client allegations concerning debt, control, liquidation and possible fraud/criminal implications.</article><article><strong>19–20 JUL 2016 · PENAL ROUTE</strong>While PwC was finalising the Community challenge, the client reiterates “la vía penal contra esta gente”. Miguel/PwC replies “Tomamos nota de vuestra decisión”; Carlos is copied.</article><article><strong>SEP 2016 · PWC–AC CONTACT</strong>PwC confirms it spoke directly with the Administrator about the tour-operator/new exploitation-contract route. PwC limits the scope: a general telephone conversation, no contract detail, report or email exchange; Patricia immediately asks for a written account of what was said and what the AC answered.</article></div>
      <table class="pd-kt__table"><thead><tr><th>What PwC/Carlos knew</th><th>What the AC knew independently</th><th>What transfer is proved</th><th>What remains missing</th></tr></thead><tbody><tr><td>Client allegations concerning disputed debt, control/liquidation, third-party conduct and possible criminal significance; an active legal response; an express penal-route instruction.</td><td><strong>Must be reconstructed source by source.</strong> Knowledge is not attributed to the AC by mere inference. Direct communications, filings, meetings, the insolvency file and other sources must be separated.</td><td>A direct PwC–AC conversation existed concerning the tour-operator/new exploitation-contract route. PwC itself confirmed the contact.</td><td>Exact call content; participants; notes/calendar; drafts or contemplated “report for the AC”; which allegations were conveyed; what the AC answered; what he later did with the information.</td></tr></tbody></table>
      <p class="pd-kt__q"><strong>Central question:</strong> when PwC spoke directly with the Insolvency Administrator it already possessed documented knowledge of allegations its client regarded as potentially criminal. What exactly did PwC communicate to the AC, what did he already know independently, what did he understand, and where is the record of what he did with that knowledge?</p>
      ${(isAC||isCal)?`<p class="pd-kt__down"><strong>Consequence for the insolvency and classification:</strong> if the AC possessed independent or transmitted knowledge of material allegations involving third parties, how did that knowledge affect — or why does the record not show it affecting — disputed Community debt, control/liquidation, third-party responsibility, alternative causation and the later classification? The question requires documentary reconstruction; it presumes neither answer nor motive.</p>`:''}
      <p class="pd-kt__down"><strong>Later bridge to test:</strong> 2016 PwC knowledge + AC contact → later insolvency decisions → subsequently documented <strong>Grupo Acosta Matos / RIC Private Equity (#RICPE) / Sun Park–MYND perimeter</strong>. The sequence warrants questions about continuity, knowledge and conflicts; it does not by itself prove coordination, transmission of every allegation or criminal conduct.</p>
      <p class="pd-kt__precision"><strong>Evidential control:</strong> this does not state that PwC “imputed criminal knowledge” to the AC as an established fact. What is proved is PwC's prior knowledge and later direct AC contact. What was transferred is the open question. <a href="${pwcHref}">PwC/Carlos</a> · <a href="${acHref}">Insolvency Administrator</a> · <a href="${calHref}">Classification</a>.</p>
    `;

    const hero=main.querySelector('.hero,.ca-hero,.cal-open,[class*="hero"]');
    if(key.endsWith('PwC')){
      const dominant=d.querySelector('[data-pd-pwc-penal-dominant]');
      if(dominant) dominant.insertAdjacentElement('afterend',sec); else if(hero) hero.insertAdjacentElement('afterend',sec); else main.prepend(sec);
    }else if(hero){
      hero.insertAdjacentElement('afterend',sec);
    }else{
      main.prepend(sec);
    }
  };

  if(d.readyState==='loading') d.addEventListener('DOMContentLoaded',render,{once:true}); else render();
})();
