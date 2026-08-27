/* RICPE-RESOLVER-ACCESS-CONTROL-20260827 */
(() => {
  const path = location.pathname.replace(/\/index\.html$/, '/');
  const eligible = [
    '/es/ric-private-equity-sun-park/', '/en/ric-private-equity-sun-park/',
    '/es/cnmv-ricpe-verificacion/', '/en/cnmv-ricpe-verification/',
    '/evidence/ricpe-cnmv/2026-08-27/'
  ].some(s => path.endsWith(s));
  if (!eligible) return;

  const render = () => {
    if (document.querySelector('[data-ricpe-resolver-access-20260827]')) return;
    const es = !path.includes('/en/');
    const base = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
    const evidence = `${base}evidence/ricpe-cnmv/2026-08-27/`;
    const section = document.createElement('section');
    section.dataset.ricpeResolverAccess20260827 = 'true';
    section.id = 'identidad-responsable-acceso-27ago2026';
    section.style.cssText = 'padding:2.4rem 0;background:linear-gradient(135deg,#fff4cc,#ffe7e7 48%,#e5f0ff);border-top:1px solid #d8c58d;border-bottom:1px solid #d8c58d';
    const title = es ? '¿Quién tomó realmente la decisión y quién tuvo acceso al expediente?' : 'Who actually made the decision, and who had access to the file?';
    const intro = es
      ? 'El certificado comunicado el 27 de agosto no identifica por nombre a la persona de RICPE que resolvió. La resolución atribuye la decisión sólo al “Responsable del Sistema Interno de Información”; el PDF no contiene autor nominal y su firma criptográfica pertenece al certificado de comunicaciones de DIGITAL PRODUCTS DEVELOPMENT SL / Ithikios, no a una persona física de RICPE. Esto no prueba acceso indebido: convierte la identidad, autorización y conflicto del gestor real en una cuestión de producción verificable.'
      : 'The 27 August certificate does not identify by name the RICPE person who decided the case. The decision is attributed only to the “Internal Information System Responsible Officer”; the PDF has no named author and its cryptographic signature belongs to DIGITAL PRODUCTS DEVELOPMENT SL / Ithikios’ communications certificate, not a RICPE natural person. This does not prove improper access: it makes the actual handler’s identity, authority and conflict status a verifiable production question.';
    const questions = es ? [
      '¿Quién era el Responsable formal del Sistema, quién era su delegado si existía órgano colegiado y quién ejecutó cada acción en Ithikios?',
      '¿Qué usuario abrió, asignó, visualizó, descargó, solicitó información, cambió estados, redactó/aprobó la resolución y cerró la comunicación?',
      '¿Tuvo alguna persona nombrada en la alerta —o alguien que actuara para ella— acceso directo o indirecto, capacidad de influencia, reasignación, restricción o cierre?',
      '¿Quién generó o aplicó el estado “No mostrado al denunciante” a la petición de la certificación RICPE de 20 julio 2021, y fue esa petición técnicamente visible en algún momento?',
      '¿Se realizó una recusación/control de conflictos antes de la asignación y el cierre? ¿Qué personas fueron excluidas del acceso?',
      '¿Cuándo recibió la comunicación íntegra el Consejo, su Presidente, los consejeros no conflictuados y la Unidad de Cumplimiento, y quién puede certificar esa circulación?',
      '¿Conservan RICPE e Ithikios el export nativo, IDs de usuario, roles, permisos, timestamps, historial de asignación, logs de acceso, versiones y hashes?'
    ] : [
      'Who was the formally appointed System Responsible Officer, who was the delegate if a collegiate body existed, and who executed each Ithikios action?',
      'Which user opened, assigned, viewed, downloaded, requested information, changed status, drafted/approved the decision and closed the communication?',
      'Did any person named in the alert —or anyone acting for them— have direct or indirect access, influence, reassignment, restriction or closure capability?',
      'Who created or applied the “Not shown to the reporting person” state to the request for RICPE’s 20 July 2021 certificate, and was that request ever technically visible?',
      'Was a conflict/recusal check performed before assignment and closure? Who was excluded from access?',
      'When did the full communication reach the Board, its Chair, non-conflicted directors and the Compliance Unit, and who can certify that circulation?',
      'Do RICPE and Ithikios preserve the native export, user IDs, roles, permissions, timestamps, assignment history, access logs, versions and hashes?'
    ];
    const boundary = es
      ? '<strong>Límite:</strong> la hipótesis de que una persona nombrada en la denuncia —incluido el director vinculado al perímetro Acosta Matos/CAM— pudiera haber accedido o influido se formula únicamente para ser comprobada con logs. No existe actualmente prueba pública de que Acosta Matos, CAM u otra persona accediera sin autorización, suplantara al Responsable, manipulara el expediente o impidiera su llegada al Consejo.'
      : '<strong>Boundary:</strong> the possibility that a person named in the report —including the director linked to the Acosta Matos/CAM perimeter— accessed or influenced the file is raised only for testing against logs. There is currently no public proof that Acosta Matos, CAM or anyone else gained unauthorised access, impersonated the Responsible Officer, manipulated the file or prevented Board escalation.';

    section.innerHTML = `<div class="shell" style="max-width:1180px"><p style="font-size:.74rem;font-weight:900;letter-spacing:.08em;text-transform:uppercase;color:#7c4c12;margin:0 0 .45rem">27 AUG 2026 · ACCESS CONTROL · CONFLICT SEGREGATION</p><h2 style="font-size:clamp(1.7rem,3vw,2.8rem);line-height:1.05;max-width:27ch;margin:.1rem 0 .8rem;color:#13252d">${title}</h2><p style="max-width:92ch;line-height:1.65;color:#26383f">${intro}</p><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:.7rem;margin:1.1rem 0">${questions.map((q,i)=>`<article style="background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:15px;padding:1rem"><strong style="display:block;color:#805f22;margin-bottom:.35rem">Q${i+1}</strong><span style="line-height:1.5;color:#1f343c">${q}</span></article>`).join('')}</div><p style="background:#fff;border-left:5px solid #b44d36;padding:.9rem 1rem;max-width:96ch;line-height:1.55">${boundary}</p><p><a href="${evidence}" style="display:inline-flex;padding:.7rem .95rem;border-radius:999px;background:#13252d;color:#fff;text-decoration:none;font-weight:850">${es?'Abrir resolución completa y registro certificado':'Open full resolution and certified record'}</a></p></div>`;

    const main = document.querySelector('main');
    if (!main) return;
    const anchor = document.querySelector('[data-ricpe-full-resolution-20260827], [data-ricpe-cnmv-closure-20260827]');
    if (anchor) anchor.insertAdjacentElement('afterend', section);
    else main.prepend(section);
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render, {once:true}); else render();
})();
