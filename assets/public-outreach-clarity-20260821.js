/* PUBLIC-OUTREACH-CLARITY-20260821
 * Selective public-facing clarity layer for worker/informant invitations and collaboration routes.
 * Scope is deliberately narrow: it does not modify substantive dossier allegations or evidential conclusions.
 */
(() => {
  const normalise = value => {
    let path = value.replace(/\/index\.html$/, '/');
    if (!path.endsWith('/')) path += '/';
    return path.toLowerCase();
  };

  const path = normalise(location.pathname);
  const isEn = document.documentElement.lang === 'en' || path.includes('/en/');
  const workerRoutes = [
    '/es/carta-abierta-trabajadores-acosta-matos/',
    '/en/open-letter-workers-acosta-matos/',
    '/es/carta-abierta-trabajadores-mynd-yaiza/',
    '/en/open-letter-workers-mynd-yaiza/'
  ];
  const collabRoutes = ['/es/colaborar/', '/en/collaborate/'];
  const isWorker = workerRoutes.some(route => path.endsWith(route));
  const isCollab = collabRoutes.some(route => path.endsWith(route));
  if (!isWorker && !isCollab) return;

  const css = `
    .outreach-clarity-box{border:1px solid rgba(19,37,45,.22);border-left:6px solid #8c6b2f;background:#fffdf8;padding:1.2rem 1.35rem;border-radius:14px;margin:1.5rem 0;box-shadow:0 8px 24px rgba(19,37,45,.05)}
    .outreach-clarity-box h2,.outreach-clarity-box h3{margin:.1rem 0 .65rem;color:#13252d}
    .outreach-clarity-box p:last-child{margin-bottom:0}
    .outreach-clarity-box .outreach-kicker{display:block;font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;font-weight:800;color:#6d5527;margin-bottom:.45rem}
    .outreach-clarity-box.outreach-reporting-boundary{border-left-color:#13252d;background:#f7f9f8}
    .outreach-clarity-actions{display:flex;gap:.65rem;flex-wrap:wrap;margin-top:.9rem}
    .outreach-clarity-actions a{font-weight:700}
    .outreach-correction-box{border-top:1px solid rgba(19,37,45,.2);border-bottom:1px solid rgba(19,37,45,.2);padding:1.15rem 0;margin:1.75rem 0}
    .outreach-correction-box h2{margin-top:0}
  `;
  if (!document.querySelector('style[data-public-outreach-clarity-style]')) {
    const style = document.createElement('style');
    style.dataset.publicOutreachClarityStyle = '20260821';
    style.textContent = css;
    document.head.appendChild(style);
  }

  const html = {
    es: {
      relationship: `
        <span class="outreach-kicker">Regla de lectura · personas y entidades relacionadas</span>
        <h2>RELACIÓN NO ES RESPONSABILIDAD</h2>
        <p><strong>Trabajar, haber trabajado, invertir, financiar, asesorar, suministrar servicios, franquiciar una marca o colaborar con una entidad mencionada en esta web no implica participación, conocimiento ni responsabilidad.</strong> Cualquier posible responsabilidad debe acreditarse persona por persona, acto por acto, fecha por fecha y documento por documento.</p>
        <p>Esta invitación tiene cuatro finalidades igualmente válidas: <strong>aclarar, corregir, confirmar o informar</strong>. No exige compartir nuestra interpretación del expediente ni contactar con Por Derecho.</p>
        <p>Si la información pudiera referirse a una infracción conocida en un contexto laboral o profesional, puede utilizar directamente una vía oficial o protegida. No obtenga información ilícitamente y no envíe originales sensibles por correo ordinario sin comprender antes los riesgos de confidencialidad y custodia.</p>`,
      correction: `
        <h2>Corregir el registro también es contribuir</h2>
        <p>Si una afirmación factual de esta web es incorrecta, incompleta o carece de contexto material, identifique la proposición concreta, la fuente que considera insuficiente y, cuando sea posible, la evidencia que permitiría corregirla. <strong>Una explicación legítima que reduzca, limite o descarte una inferencia tiene el mismo valor metodológico que una confirmación.</strong></p>
        <p>No tratamos una corrección documentada como hostilidad ni como admisión. Las correcciones deben incorporarse con fecha, fuente y alcance.</p>`,
      collab: `
        <span class="outreach-kicker">Separación de finalidades</span>
        <h2>COLABORACIÓN ≠ CANAL DE INFORMANTES</h2>
        <p>Esta página sirve para colaboración profesional, editorial, institucional y, cuando proceda, conversaciones comerciales selectivas. <strong>No es un canal protegido de denuncias.</strong></p>
        <p>El correo ordinario publicado aquí no debe utilizarse para remitir pruebas sensibles, secretos empresariales, bases de datos, documentos obtenidos sin autorización ni material cuya custodia o confidencialidad requiera protección especial. Quien desee comunicar una posible infracción puede acudir directamente a una vía oficial o protegida y <strong>no necesita colaborar con Project Sun Rock ni aceptar nuestra interpretación</strong>.</p>
        <p>Las conversaciones sobre futuros hoteles, activos, inversiones o socios quedan separadas de cualquier comunicación de hechos, corrección del registro o información protegida.</p>
        <div class="outreach-clarity-actions"><a href="https://www.proteccioninformante.gob.es/canales-de-presentacion-de-informaciones" rel="external noopener">Consultar el canal externo AIPI ↗</a></div>`
    },
    en: {
      relationship: `
        <span class="outreach-kicker">Reading rule · related people and organisations</span>
        <h2>RELATIONSHIP IS NOT RESPONSIBILITY</h2>
        <p><strong>Working or having worked for, investing in, financing, advising, supplying services to, franchising a brand to, or otherwise collaborating with an organisation mentioned on this site does not imply participation, knowledge or responsibility.</strong> Any possible responsibility must be established person by person, act by act, date by date and document by document.</p>
        <p>This invitation has four equally legitimate purposes: <strong>clarify, correct, confirm or report</strong>. You do not have to accept our interpretation of the record or contact Por Derecho.</p>
        <p>If information may concern an infringement learned in a work or professional context, you may use an official or protected route directly. Do not obtain information unlawfully and do not send sensitive originals by ordinary email without first understanding confidentiality and custody risks.</p>`,
      correction: `
        <h2>Correcting the record is also a contribution</h2>
        <p>If a factual proposition on this site is wrong, incomplete or missing material context, identify the specific proposition, the source you consider insufficient and, where possible, the evidence that would correct it. <strong>A legitimate explanation that narrows, limits or defeats an inference has the same methodological value as confirmation.</strong></p>
        <p>We do not treat a documented correction as hostility or as an admission. Corrections should be recorded with date, source and scope.</p>`,
      collab: `
        <span class="outreach-kicker">Separation of purposes</span>
        <h2>COLLABORATION ≠ INFORMANT CHANNEL</h2>
        <p>This page is for professional, editorial and institutional collaboration and, where appropriate, selective commercial conversations. <strong>It is not a protected reporting channel.</strong></p>
        <p>Ordinary email published here should not be used to send sensitive evidence, trade secrets, databases, material obtained without authorisation, or documents requiring protected custody or confidentiality. Anyone wishing to report a possible infringement may use an official or protected route directly and <strong>does not need to collaborate with Project Sun Rock or accept our interpretation</strong>.</p>
        <p>Conversations about future hotels, assets, investments or partners are kept separate from factual reports, corrections to the record or protected information.</p>
        <div class="outreach-clarity-actions"><a href="https://www.proteccioninformante.gob.es/canales-de-presentacion-de-informaciones" rel="external noopener">Open the AIPI external reporting route ↗</a></div>`
    }
  };

  const copy = isEn ? html.en : html.es;

  const replaceAcostaLead = () => {
    const acosta = path.endsWith('/es/carta-abierta-trabajadores-acosta-matos/') || path.endsWith('/en/open-letter-workers-acosta-matos/');
    if (!acosta) return;
    const lead = document.querySelector('.hero .lead');
    if (!lead) return;
    lead.textContent = isEn
      ? 'If you know a fact, instruction, account, file, meeting, decision or explanation that may help establish what happened, I am not asking you to choose a side. If you lawfully hold relevant information, preserve it without alteration and consider using an appropriate lawful route. Explanations that correct, narrow or contradict what we have published are equally important.'
      : 'Si conoces un hecho, una instrucción, una cuenta, un archivo, una reunión, una decisión o una explicación que pueda ayudar a esclarecer lo ocurrido, no te pedimos que elijas un bando. Si conservas legítimamente información relevante, presérvala sin alterarla y valora utilizar una vía legal adecuada. Las explicaciones que corrijan, limiten o contradigan lo publicado son igualmente importantes.';
  };

  const neutraliseBornInSin = () => {
    if (!path.includes('trabajadores-mynd-yaiza') && !path.includes('open-letter-workers-mynd-yaiza')) return;
    const paragraphs = [...document.querySelectorAll('main p')];
    const target = paragraphs.find(p => /nacido en pecado|born in sin/i.test(p.textContent));
    if (!target) return;
    target.innerHTML = isEn
      ? '<strong>Collective attribution is not the method used here.</strong> Metaphors or moral characterisations used elsewhere on the site must not be read as assigning guilt, knowledge or responsibility to every company, worker, investor, adviser, supplier or commercial partner. The controlling rule for this invitation is actor-specific evidence.'
      : '<strong>La atribución colectiva no es el método de esta web.</strong> Las metáforas o valoraciones morales utilizadas en otros lugares no deben interpretarse como atribución de culpabilidad, conocimiento o responsabilidad a toda empresa, trabajador, inversor, asesor, proveedor o socio comercial. La regla que gobierna esta invitación es la prueba individualizada por actor.';
  };

  const applyWorker = () => {
    replaceAcostaLead();
    neutraliseBornInSin();

    if (!document.querySelector('[data-relationship-not-responsibility-20260821]')) {
      const box = document.createElement('div');
      box.className = 'outreach-clarity-box outreach-reporting-boundary';
      box.dataset.relationshipNotResponsibility20260821 = 'true';
      box.innerHTML = copy.relationship;
      const heroShell = document.querySelector('.hero .shell');
      if (heroShell) heroShell.appendChild(box);
    }

    if (!document.querySelector('[data-correction-first-20260821]')) {
      const correction = document.createElement('div');
      correction.className = 'outreach-correction-box';
      correction.dataset.correctionFirst20260821 = 'true';
      correction.innerHTML = copy.correction;
      const signature = document.querySelector('.signature');
      const parent = signature && signature.parentElement;
      if (parent && signature) parent.insertBefore(correction, signature);
      else document.querySelector('main .shell')?.appendChild(correction);
    }
  };

  const applyCollab = () => {
    if (document.querySelector('[data-collaboration-reporting-separation-20260821]')) return;
    const box = document.createElement('div');
    box.className = 'outreach-clarity-box outreach-reporting-boundary';
    box.dataset.collaborationReportingSeparation20260821 = 'true';
    box.innerHTML = copy.collab;
    const routes = document.querySelector('#vias .shell');
    const head = routes?.querySelector('.section-head');
    if (routes && head) head.insertAdjacentElement('afterend', box);
    else if (routes) routes.prepend(box);
  };

  const apply = () => {
    if (isWorker) applyWorker();
    if (isCollab) applyCollab();
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', apply, { once: true });
  else apply();
})();
