(() => {
  const path = window.location.pathname.replace(/\/+$/, '') + '/';
  const calEs = path.endsWith('/es/calificacion-concurso-36-2012-vidas-paralelas/');
  const calEn = path.endsWith('/en/insolvency-classification-parallel-lives/');
  const comEs = path.endsWith('/es/comunidad-instrumentalizacion/');
  const comEn = path.endsWith('/en/community-instrumentalisation/');
  if (!calEs && !calEn && !comEs && !comEn) return;
  if (document.querySelector('[data-a03-unitary-causation-20260816]')) return;

  const es = calEs || comEs;
  const d = es ? {
    eyebrow: 'ALEGACIÓN 03 · ANÁLISIS UNITARIO · COMUNIDAD + OPERACIÓN + AC + ACTORES PRIVADOS',
    title: 'Una sola economía hotelera: la renta no puede aislarse del sistema que producía —o impedía producir— esa renta',
    lead: 'La alegación contra Gil/Pink tiene que contrastarse con el hotel como sistema completo. La defensa sostiene que la unidad de explotación ya estaba dañada por conflictos con propietarios minoritarios y por la maquinaria de deuda, voto y gestión de la Comunidad. Esa tesis no está judicialmente probada como causa única. Pero la propia AC conocía el conflicto y, tras la liquidación, utilizó o autorizó mecanismos de Comunidad para acceso, mantenimiento y seguridad. Eso convierte la causalidad en una pregunta unitaria, no en cinco expedientes desconectados.',
    status: 'CONTROL PROBATORIO: “secuestro de la Comunidad” es una caracterización de parte. Lo verificable hoy es el conflicto, el aviso a la AC y el uso posterior de la Comunidad como mecanismo operativo de acceso; cualquier coordinación ilícita con actores privados exige prueba específica.',
    chainTitle: 'La cadena que debe reconstruirse antes de atribuir agravación de insolvencia',
    chain: [
      ['1 · HOTEL UNITARIO', 'Sun Park dependía económicamente de una explotación turística coordinada aunque la propiedad estuviera dividida finca por finca.'],
      ['2 · CONFLICTO COMUNIDAD/MINORÍAS', 'La defensa alega unidades fuera de explotación, costes desplazados, deuda comunitaria discutida y pérdida práctica de capacidad de voto/gobierno. La sentencia reproduce parte de esa defensa; no la declara causa única.'],
      ['3 · PINK COMO RESPUESTA OPERATIVA', 'El contrato combinaba renta, cuotas de Comunidad y costes de explotación/conservación. Un memorando contable contemporáneo de noviembre de 2013 propuso compensaciones entre renta y obligaciones soportadas por Monterecco; no es prueba bancaria de que cada compensación fuera válida.'],
      ['4 · AVISO DIRECTO A LA AC', 'El propio informe de la AC reproduce la queja de Gil sobre deuda/voto comunitarios y su petición de que se exigieran cuentas y actas a quienes gestionaban la Comunidad. Eso prueba conocimiento de la alegación, no que la deuda fuera falsa.'],
      ['5 · AC → COMUNIDAD / ACCESO', 'Tras liquidación, la AC trató llaves/posesión y mantenimiento mediante la Comunidad. Una copia de su declaración judicial de 2018 le atribuye autorizaciones de acceso, incluso a Laura Acosta Matos; la certificación completa sigue pendiente.'],
      ['6 · CALIFICACIÓN', 'La acusación posterior puso el foco en renta, falta de reclamación, ingresos extranjeros y “connivencia”. La sentencia rechazó parte de ese marco, pero mantuvo adversamente la falta posterior de reclamación de rentas, culpa grave, causalidad y complicidad de Pink; está recurrido.']
    ],
    asymTitle: 'La pregunta que faltaba: ¿qué parte del problema estaba aguas arriba?',
    asym: 'Si unidades dejaron de estar disponibles para explotación, si había costes comunitarios/operativos soportados por el operador, si una deuda discutida afectaba al gobierno del propietario mayoritario y si después la propia AC utilizó la Comunidad como canal de acceso y mantenimiento, no basta con medir el resultado final como “renta no cobrada”. Hay que calcular qué inventario era realmente explotable, qué ocupación e ingresos existían, qué costes y pagos se soportaron, qué compensaciones eran jurídicamente válidas, qué hizo cada actor y qué renta era realmente recuperable en cada fecha.',
    roleTitle: 'El cambio de papeles de la AC dentro del mismo sistema',
    roles: [
      ['Demandante frente a Pink', 'La AC sí litigó la resolución y reclamación de rentas. No se publica que permaneciera inactiva.'],
      ['Receptor de la alarma comunitaria', 'Su propio informe conserva la alegación sobre deuda, voto, cuentas y actas de la Comunidad.'],
      ['Administrador post-liquidación', 'Interpreta entrega de llaves/posesión y canaliza mantenimiento/seguridad mediante la Comunidad.'],
      ['Testigo material de 2018', 'La copia controlada de DP 1132/2018 atribuye a la AC autorizaciones de acceso; el original certificado sigue siendo objetivo probatorio.'],
      ['Acusador en calificación', 'En febrero de 2019 formula el relato adverso contra Gil/Pink. La coherencia entre lo que sabía, autorizó, investigó y luego imputó es una cuestión legítima de rendición de cuentas.']
    ],
    judicialTitle: 'Lo que los tribunales ya corrigieron — y lo que sigue adverso',
    judicial: [
      ['RECHAZADO', 'Celebrar el contrato por una renta inferior a la cuota hipotecaria no fue, por sí solo, un acto culpable.'],
      ['CORREGIDO', 'La teoría de que el crédito CEXP de 737.338,85 € equivalía a LPB debiéndose a sí misma no prevaleció frente a la pericial aceptada.'],
      ['RECHAZADO', 'La “connivencia” usada en la rama de alzamiento no quedó corroborada de forma suficiente para esa imputación.'],
      ['RECHAZADO', 'La extensión de complicidad personal a Patricia no prosperó por falta de argumentación individual suficiente.'],
      ['ADVERSO · RECURRIDO', 'La falta posterior de reclamación/cobro de rentas sí sustentó culpa grave, causalidad y complicidad de Pink en Sentencia 163/2023.']
    ],
    adverse: 'También existe un contexto judicial adverso en el episodio de accesos de 2018: la Audiencia Provincial confirmó el archivo provisional de aquella vía penal y aceptó como explicación posible la autoridad de mantenimiento/acceso de la Comunidad apoyada en la declaración de la AC. Eso no es un auto de posesión de todo el hotel a favor de CAM ni una resolución de todas las consecuencias civiles/concursales posteriores.',
    close: 'La prueba decisiva no es una etiqueta. Es una conciliación: INVENTARIO EXPLOTABLE → OCUPACIÓN → COBROS → COSTES → COMUNIDAD → COMPENSACIONES → BANCOS → DECISIONES DE LA AC → ACCESO/CONTROL → EFECTO SOBRE EXPLOTACIÓN → RENTA RECUPERABLE → AGRAVACIÓN CONCRETA. Hasta que exista esa reconstrucción, Allegación 03 sigue abierta como análisis unitario.',
    link: calEs ? '../comunidad-instrumentalizacion/' : (comEs ? '../calificacion-concurso-36-2012-vidas-paralelas/' : null),
    linkText: calEs ? 'Abrir el dossier de Comunidad e instrumentalización →' : (comEs ? 'Volver a la Calificación — Alegación 03 →' : '')
  } : {
    eyebrow: 'ALLEGATION 03 · UNITARY ANALYSIS · COMMUNITY + OPERATION + AC + PRIVATE ACTORS',
    title: 'One hotel economy: rent cannot be isolated from the system that produced — or prevented production of — that rent',
    lead: 'The accusation against Gil/Pink must be tested against the hotel as a whole operating system. The defence says unity of operation was already impaired by minority-owner conflict and by Community debt, voting and governance machinery. That thesis has not been judicially established as the sole cause. But the AC himself knew of the dispute and, after liquidation, used or authorised Community mechanisms for access, maintenance and security. Causation therefore has to be unitary rather than split across disconnected case files.',
    status: 'EVIDENTIAL CONTROL: “Community hijacking” is a party characterisation. What is presently verifiable is the conflict, notice to the AC and later use of the Community as an operational access mechanism; any unlawful coordination with private actors requires specific proof.',
    chainTitle: 'The chain that must be reconstructed before attributing insolvency aggravation',
    chain: [
      ['1 · UNITARY HOTEL', 'Sun Park economically depended on coordinated tourist operation even though title was divided unit by unit.'],
      ['2 · COMMUNITY/MINORITY CONFLICT', 'The defence alleges units withheld from common operation, shifted costs, disputed Community debt and practical loss of majority voting/governance capacity. The judgment records part of that defence; it does not establish sole causation.'],
      ['3 · PINK AS OPERATING RESPONSE', 'The agreement combined rent, Community charges and operation/conservation costs. A contemporaneous November-2013 accountant memorandum proposed offsets between rent and obligations borne by Monterecco; it is not bank proof that every offset was legally valid.'],
      ['4 · DIRECT NOTICE TO THE AC', 'The AC’s own report reproduces Gil’s complaint about Community debt/voting and the request to require supporting accounts and minutes from Community managers. That proves notice of the allegation, not that the debt was false.'],
      ['5 · AC → COMMUNITY / ACCESS', 'After liquidation the AC dealt with keys/possession and maintenance through the Community. A controlled copy of his 2018 judicial testimony attributes access authorisations to him, including access for Laura Acosta Matos; certified production remains outstanding.'],
      ['6 · CLASSIFICATION', 'The later accusation focused on rent, non-enforcement, foreign receipts and “connivencia”. The judgment rejected parts of that frame but adversely retained later rent non-collection, gross fault, causation and Pink complicity; those findings are appealed.']
    ],
    asymTitle: 'The missing question: how much of the problem was upstream?',
    asym: 'If units were unavailable for operation, operating/Community costs were borne by the operator, disputed debt affected majority governance and the AC later used the Community as an access/maintenance channel, the result cannot be measured only as “uncollected rent”. The record must show actually exploitable inventory, occupancy and income, costs and payments borne, legally valid offsets, each actor’s conduct and the rent realistically recoverable at each date.',
    roleTitle: 'The AC’s changing roles inside the same operating system',
    roles: [
      ['Claimant against Pink', 'The AC did litigate contract resolution and rent recovery. The site does not say he was inactive.'],
      ['Recipient of the Community warning', 'His own report preserves the debt/voting/accounts/minutes allegation.'],
      ['Post-liquidation administrator', 'He interprets keys/possession and channels maintenance/security through the Community.'],
      ['Material 2018 witness', 'The controlled DP 1132/2018 copy attributes access authorisations to the AC; certified production remains an evidence target.'],
      ['Classification accuser', 'In February 2019 he advances the adverse Gil/Pink case. Consistency between what he knew, authorised, investigated and later alleged is a legitimate accountability question.']
    ],
    judicialTitle: 'What the courts already corrected — and what remains adverse',
    judicial: [
      ['REJECTED', 'Entering the agreement at rent below the mortgage instalment was not, by itself, a culpable act.'],
      ['CORRECTED', 'The €737,338.85 CEXP “LPB owes itself” theory did not prevail against the accepted expert explanation.'],
      ['REJECTED', 'The “connivencia” assertion did not receive sufficient corroboration for the alzamiento branch.'],
      ['REJECTED', 'Personal complicity was not extended to Patricia where individual attribution was insufficiently argued.'],
      ['ADVERSE · APPEALED', 'Later failure to pursue/collect rent did support gross fault, causation and Pink complicity in Judgment 163/2023.']
    ],
    adverse: 'There is also adverse judicial context in the 2018 access episode: the Provincial Court upheld provisional criminal archive and accepted Community maintenance/access authority, supported by the AC’s account, as a possible lawful explanation. That was not a whole-hotel possession order in CAM’s favour and did not decide every later civil, insolvency or patrimonial consequence.',
    close: 'The decisive evidence is not a label. It is a reconciliation: EXPLOITABLE INVENTORY → OCCUPANCY → RECEIPTS → COSTS → COMMUNITY → OFFSETS → BANKS → AC DECISIONS → ACCESS/CONTROL → EFFECT ON OPERATION → RECOVERABLE RENT → SPECIFIC INSOLVENCY AGGRAVATION. Until that exists, Allegation 03 remains open as a unitary causation analysis.',
    link: calEn ? '../community-instrumentalisation/' : (comEn ? '../insolvency-classification-parallel-lives/' : null),
    linkText: calEn ? 'Open the Community / instrumentalisation dossier →' : (comEn ? 'Return to Classification — Allegation 03 →' : '')
  };

  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
  const style = document.createElement('style');
  style.textContent = `
    [data-a03-unitary-causation-20260816]{background:#13252d;color:#fff;border-top:1px solid rgba(255,255,255,.12);border-bottom:1px solid rgba(255,255,255,.12)}
    .u03-wrap{max-width:1100px;margin:0 auto;padding:4rem 1.25rem}.u03-eye{font-size:.76rem;font-weight:900;letter-spacing:.09em;text-transform:uppercase;color:#e3c782}.u03-wrap h2{font-size:clamp(2rem,4vw,3.25rem);line-height:1.06;margin:.45rem 0 1rem;max-width:980px}.u03-lead{font-size:1.12rem;line-height:1.7;max-width:980px}.u03-status{margin:1.3rem 0 2.4rem;padding:1rem 1.15rem;border:1px solid #e3c782;border-radius:12px;color:#f5e9c7;line-height:1.55}.u03-chain{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.8rem;margin:1rem 0 2.5rem}.u03-step{background:#fff;color:#13252d;border-radius:14px;padding:1rem}.u03-step strong{display:block;color:#76592c;margin-bottom:.4rem}.u03-step span{line-height:1.5}.u03-block{background:rgba(255,255,255,.07);border-left:5px solid #e3c782;padding:1rem 1.15rem;border-radius:10px;line-height:1.65;margin:1rem 0 2.5rem}.u03-roles,.u03-judicial{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.8rem;margin:1rem 0 2.5rem}.u03-mini{border:1px solid rgba(255,255,255,.22);border-radius:13px;padding:1rem;line-height:1.5}.u03-mini strong{display:block;color:#e3c782;margin-bottom:.35rem}.u03-adverse{background:#fff;color:#13252d;border-radius:14px;padding:1.1rem;line-height:1.65;margin:1rem 0 2.2rem}.u03-close{font-size:1.08rem;font-weight:750;line-height:1.65;border-top:1px solid rgba(255,255,255,.2);padding-top:1.4rem}.u03-link{display:inline-block;margin-top:1.2rem;color:#13252d;background:#e3c782;padding:.75rem 1rem;border-radius:9px;text-decoration:none;font-weight:800}
    @media(max-width:820px){.u03-chain,.u03-roles,.u03-judicial{grid-template-columns:1fr}.u03-wrap{padding:3rem 1rem}}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.setAttribute('data-a03-unitary-causation-20260816','');
  section.innerHTML = `<div class="u03-wrap">
    <div class="u03-eye">${esc(d.eyebrow)}</div><h2>${esc(d.title)}</h2><p class="u03-lead">${esc(d.lead)}</p><div class="u03-status">${esc(d.status)}</div>
    <h3>${esc(d.chainTitle)}</h3><div class="u03-chain">${d.chain.map(x=>`<article class="u03-step"><strong>${esc(x[0])}</strong><span>${esc(x[1])}</span></article>`).join('')}</div>
    <h3>${esc(d.asymTitle)}</h3><div class="u03-block">${esc(d.asym)}</div>
    <h3>${esc(d.roleTitle)}</h3><div class="u03-roles">${d.roles.map(x=>`<article class="u03-mini"><strong>${esc(x[0])}</strong><span>${esc(x[1])}</span></article>`).join('')}</div>
    <h3>${esc(d.judicialTitle)}</h3><div class="u03-judicial">${d.judicial.map(x=>`<article class="u03-mini"><strong>${esc(x[0])}</strong><span>${esc(x[1])}</span></article>`).join('')}</div>
    <div class="u03-adverse">${esc(d.adverse)}</div><div class="u03-close">${esc(d.close)}</div>${d.link ? `<a class="u03-link" href="${esc(d.link)}">${esc(d.linkText)}</a>` : ''}
  </div>`;

  if (calEs || calEn) {
    const anchor = document.querySelector('[data-cal-allegation03-20260816]');
    if (anchor) anchor.insertAdjacentElement('afterend', section);
    else document.querySelector('main')?.prepend(section);
  } else {
    const anchor = document.querySelector('#control-2018-sin-auto-posesion') || document.querySelector('.dossier-hero');
    if (anchor) anchor.insertAdjacentElement('afterend', section);
    else document.querySelector('main')?.prepend(section);
  }
})();