(() => {
  const path = window.location.pathname.replace(/\/+$/, '') + '/';
  const es = path.endsWith('/es/calificacion-concurso-36-2012-vidas-paralelas/');
  const en = path.endsWith('/en/insolvency-classification-parallel-lives/');
  if (!es && !en) return;
  if (document.querySelector('[data-a03-unitary-causation-20260816]')) return;

  const d = es ? {
    eyebrow: 'ALEGACIÓN 03 · ANÁLISIS UNITARIO · COMUNIDAD + OPERACIÓN + AC + ACTORES PRIVADOS',
    title: 'Una sola economía hotelera: la renta no puede aislarse del sistema que producía —o impedía producir— esa renta',
    lead: 'La imputación contra Gil/Pink debe contrastarse con Sun Park como sistema completo. La defensa sostiene que la unidad de explotación ya estaba dañada por propietarios minoritarios y por mecanismos de deuda, voto y gestión de la Comunidad. Eso no está judicialmente probado como causa única. Pero la propia AC conocía ese conflicto y, tras la liquidación, pasó a utilizar o autorizar a la Comunidad como canal de seguridad, acceso y mantenimiento. Las declaraciones judiciales de julio de 2018 permiten reconstruir ahora esa cadena actor por actor.',
    status: 'CONTROL PROBATORIO: “secuestro de la Comunidad” es una caracterización de parte. Lo verificado es más preciso: una deuda comunitaria utilizada para excluir el voto de LPB; un administrador de la Comunidad que declaró no conocer el origen de esa deuda; una reducción retroactiva muy sustancial de las cuotas; seguridad solicitada por la AC; reglas de acceso transmitidas por la Comunidad; acceso CAM como propietario; y autorizaciones directas de la AC sobre locales LPB. La ilicitud, coordinación criminal y causalidad final siguen abiertas.',
    chainTitle: 'La cadena no fragmentada que debe auditarse',
    chain: [
      ['1 · HOTEL UNITARIO', 'El valor dependía de una explotación turística coordinada aunque el título estuviera dividido finca por finca.'],
      ['2 · DEUDA → VOTO → GOBIERNO', 'La Comunidad trató a LPB como gran morosa y le negó voto. Su administrador declaró que la deuda había bajado de unos 3 M€ a alrededor de 1 M€ tras reducir retroactivamente las cuotas, y dijo no conocer el origen de la deuda. Esto exige verificar libros, facturas, certificados y legalidad del voto; no prueba falsedad por sí solo.'],
      ['3 · PINK DENTRO DEL SISTEMA', 'El contrato combinaba renta, cuotas de Comunidad y costes de explotación/conservación. Un memorando contable contemporáneo de 2013 propuso compensaciones entre renta y obligaciones soportadas por Monterecco; no prueba bancariamente que cada compensación fuera válida.'],
      ['4 · AVISO DIRECTO A LA AC', 'El informe de calificación de la propia AC reproduce la queja de Gil sobre deuda, voto, cuentas y actas de la Comunidad y su petición de intervención. Eso prueba conocimiento de la explicación competidora, no que la deuda fuera falsa.'],
      ['5 · AC → COMUNIDAD → SEGURIDAD/ACCESO', 'La declaración judicial de la AC de 31-07-2018 dice que impulsó seguridad, autorizó accesos a locales LPB y autorizó a Laura Acosta Matos a entrar en locales LPB para supervisión/mantenimiento, distinguiéndolo expresamente de usar u ocupar.'],
      ['6 · IMPLEMENTACIÓN Y CAM', 'Shaila declaró que decisiones y cambios de cerraduras se comunicaban y tenían visto bueno de la AC, que transmitió a los vigilantes reglas de acceso de la AC y que CAM/JDAM accedían como propietarios. Laura declaró que conocía desde la junta del 18 de mayo la instalación de seguridad y acudió el 7 de junio para entrar.'],
      ['7 · CALIFICACIÓN', 'En 2019 la AC centra la agravación en renta, falta de reclamación, recibos extranjeros y una teoría de “connivencia”. La sentencia corrigió varias ramas, pero mantuvo adversamente la falta posterior de cobro de rentas, culpa grave, causalidad y complicidad de Pink; está recurrido.']
    ],
    earlyTitle: 'La cuestión de planificación previa: febrero de 2018',
    early: 'Los escritos NEXUS 36 aportan una transcripción Logalty/Burovoz de una conversación de 26-02-2018 cuyos interlocutores están formalmente numerados y cuya voz 1 se atribuye por la parte a José Daniel Acosta Matos. Allí se atribuyen frases sobre que “dentro de dos meses” entrarían ellos, que habría “seguritas”, que existía “un acuerdo con la comunidad”, que se permitiría pasar “haciéndose el loco” y que él entraría en obra. El propio protocolo de prueba de Por Derecho ordena no tratarlo como confesión: la atribución y el audio nativo necesitan autenticación. Sí constituye una pista temporal de alto valor porque precede a la junta de seguridad de mayo y al 7 de junio.',
    rolesTitle: 'Qué reconoce cada actor en las declaraciones de julio',
    roles: [
      ['AC · Borja', 'Conocía el conflicto Comunidad/LPB; dijo no saber si existía unidad de explotación ni cuánto costaba mantener el complejo; impulsó seguridad; autorizó a la Comunidad a acceder a locales LPB y a Laura a entrar en locales LPB para supervisión/mantenimiento; negó autorizar ocupación.'],
      ['F. Mario Matos · administración Comunidad', 'LPB no votaba por morosidad; deuda antes cercana a 3 M€ y luego ~1 M€ tras reducción retroactiva de cuotas; declaró desconocer su origen; seguridad del 18 de mayo a solicitud de la AC; CAM aportó liquidez/pagos contra deuda para gastos urgentes, entre ellos seguridad/seguro.'],
      ['Shaila · vicepresidencia/administración', 'Seguridad solicitada por la AC; Comunidad entra desde 18 de mayo; decisiones comunicadas y con visto bueno de la AC; cerraduras cambiadas por acuerdo y aprobación; transmitió a los vigilantes el documento/regla de acceso de la AC; CAM/JDAM entraban como propietarios.'],
      ['Laura Acosta Matos · CAM', 'Asistió a juntas de mayo/junio; sabía que se instalaría vigilancia; acudió el 7 de junio para acceder; negó ordenar cerraduras o daños; dijo que CAM pagaba cuotas/deudas y aportaba liquidez. Su relación de acceso debe leerse junto a la autorización que la AC declaró haberle dado.'],
      ['José Daniel Acosta Matos · CAM', 'Reconoció visitas previas para inspeccionar unidades adquiridas o por adquirir y estudiar reformas con asesores; dijo que entraba con Miguel, negó forzar accesos u ocultar visitas y negó proclamarse dueño de todo el complejo. Es contrapeso obligatorio frente a las alegaciones de acceso clandestino.'],
      ['Antonio Cogolludo · presidencia Comunidad', 'Dijo que la junta del 18 de mayo acordó control de seguridad y que sustituyó el código de acceso por vigilante; negó otras actuaciones de cerraduras por su parte.']
    ],
    asymTitle: 'La asimetría causal que ahora debe responderse',
    asym: 'La calificación mide aguas abajo: renta no cobrada y supuesta capacidad económica del operador. El expediente ampliado obliga a medir también aguas arriba: inventario realmente explotable, gobierno y voto, costes de Comunidad, mantenimiento y personal, compensaciones, ocupación, ingresos, decisiones de la AC y efecto posterior del régimen de acceso. La misma persona que acusó por el resultado económico reconoce límites de conocimiento sobre la unidad de explotación y el coste de mantenimiento y, después, una intervención directa en el sistema de seguridad/acceso. Eso no prueba parcialidad: exige una auditoría recíproca de conocimiento, poder, decisión y causalidad.',
    judicialTitle: 'Lo que ya está corregido y lo que sigue adverso',
    judicial: [
      ['RECHAZADO', 'Celebrar el contrato porque la renta era inferior a la hipoteca no fue, por sí solo, acto culpable.'],
      ['CORREGIDO', 'La construcción de 737.338,85 € como si LPB se debiera a sí misma no prevaleció frente a la explicación pericial aceptada.'],
      ['RECHAZADO EN ESA RAMA', 'La “connivencia” no quedó corroborada para convertir la falta de bienes de Pink en un alzamiento atribuible a LPB; no debe decirse que toda referencia a connivencia fue judicialmente borrada.'],
      ['RECHAZADO', 'La complicidad personal de Patricia no se extendió por falta de argumentación individual suficiente.'],
      ['ADVERSO · RECURRIDO', 'La posterior falta de reclamación/cobro de rentas sí sustentó culpa grave, causalidad y complicidad de Pink en Sentencia 163/2023.']
    ],
    adverse: 'También existe un contexto judicial adverso sobre los accesos de 2018: la Audiencia Provincial confirmó el archivo provisional de aquella vía penal y aceptó la autoridad de mantenimiento/acceso de la Comunidad y la declaración de la AC como parte de una explicación civil/lícita posible. Eso no fue un auto otorgando posesión de todo el hotel a CAM ni decidió todas las consecuencias civiles, concursales, turísticas o patrimoniales.',
    close: 'La prueba decisiva es una conciliación única: INVENTARIO EXPLOTABLE → OCUPACIÓN → COBROS → COSTES → COMUNIDAD/DEUDA/VOTO → COMPENSACIONES → BANCOS → DECISIONES AC → SEGURIDAD/ACCESO → IMPLEMENTACIÓN POR COMUNIDAD/PROPIETARIOS → EFECTO OPERATIVO → RENTA REALMENTE RECUPERABLE → AGRAVACIÓN CONCRETA. Por decisión expresa de esta auditoría, no avanzamos todavía a Alegación 04.',
    source: 'Control interno: CALIFICACION_ALLEGATION_03_UNITARY_COMMUNITY_PRIVATE_ACTORS_AC_CAUSATION_16AUG2026.md + CALIFICACION_ALLEGATION_03_DP1132_PRIVATE_ACTOR_SOURCE_COMPLETION_16AUG2026.md. Declaraciones judiciales preservadas: DP 1132/2018, 20 y 31 julio 2018. La transcripción de 26 febrero es prueba atribuida de parte pendiente de autenticación nativa.'
  } : {
    eyebrow: 'ALLEGATION 03 · UNITARY ANALYSIS · COMMUNITY + OPERATION + AC + PRIVATE ACTORS',
    title: 'One hotel economy: rent cannot be isolated from the system that produced — or prevented production of — that rent',
    lead: 'The accusation against Gil/Pink must be tested against Sun Park as a complete operating system. The defence says unity of operation was already impaired by minority owners and Community debt, voting and governance mechanisms. That is not judicially established as the sole cause. But the AC knew of that conflict and, after liquidation, used or authorised the Community as a security, access and maintenance channel. The July-2018 court declarations now let that chain be reconstructed actor by actor.',
    status: 'EVIDENTIAL CONTROL: “Community hijacking” is a party characterisation. What is verified is more specific: Community debt used to exclude LPB voting; a Community administrator who said he did not know the origin of that debt; a major retroactive reduction in charges; security requested by the AC; Community transmission of access rules; CAM owner-access; and direct AC authorisations concerning LPB premises. Illegality, criminal coordination and final causation remain open.',
    chainTitle: 'The non-fragmented chain that must be audited',
    chain: [
      ['1 · UNITARY HOTEL', 'Value depended on coordinated tourist operation even though title was divided unit by unit.'],
      ['2 · DEBT → VOTE → GOVERNANCE', 'The Community treated LPB as a major debtor and denied its vote. Its administrator said the debt fell from about €3m to around €1m after retroactive charge reductions and said he did not know its origin. Books, invoices, certificates and voting law must decide the issue; this alone does not prove fabrication.'],
      ['3 · PINK INSIDE THAT SYSTEM', 'The agreement combined rent, Community charges and operation/conservation costs. A contemporaneous 2013 accountant memorandum proposed offsets between rent and obligations borne by Monterecco; it is not bank proof that each offset was legally valid.'],
      ['4 · DIRECT NOTICE TO THE AC', 'The AC’s own classification report reproduces Gil’s complaint about Community debt, voting, accounts and minutes and the request for intervention. That proves knowledge of the competing explanation, not that the debt was false.'],
      ['5 · AC → COMMUNITY → SECURITY/ACCESS', 'The AC’s 31-Jul-2018 court declaration says he drove the security route, authorised access to LPB premises and authorised Laura Acosta Matos to enter LPB premises for supervision/maintenance, expressly distinguishing that from use or occupation.'],
      ['6 · IMPLEMENTATION AND CAM', 'Shaila said decisions and lock changes were communicated to and approved by the AC, that she passed AC access rules to guards and that CAM/JDAM entered as owners. Laura said she knew from the 18-May meeting that security would be installed and went on 7 June to gain access.'],
      ['7 · CLASSIFICATION', 'In 2019 the AC focused aggravation on rent, non-enforcement, foreign receipts and “connivencia”. The judgment corrected several branches but adversely retained later rent non-collection, gross fault, causation and Pink complicity; appeal pending.']
    ],
    earlyTitle: 'The prior-planning question: February 2018',
    early: 'NEXUS 36 filings use a Logalty/Burovoz transcript of a 26-Feb-2018 conversation whose speakers are formally numbered and whose Speaker 1 is attributed by the party to José Daniel Acosta Matos. The attributed phrases concern their entering “in two months”, security guards, an “agreement with the community”, being let through while someone “plays dumb”, and his entering to carry out works. Por Derecho’s own evidence protocol says this is not to be treated as a confession: speaker attribution and native audio require authentication. It is nevertheless a high-value temporal lead because it predates the May security meeting and 7 June.',
    rolesTitle: 'What each actor acknowledged in the July declarations',
    roles: [
      ['AC · Borja', 'Knew the Community/LPB conflict; said he did not know whether unity of operation existed or what the complex cost to maintain; drove security; authorised Community access to LPB premises and Laura access to LPB premises for supervision/maintenance; denied authorising occupation.'],
      ['F. Mario Matos · Community administration', 'LPB could not vote because of arrears; debt once about €3m then ~€1m after retroactive charge reduction; said he did not know its origin; 18-May security at AC request; CAM supplied liquidity/payments against arrears for urgent costs including security/insurance.'],
      ['Shaila · vice-president/administration', 'Security requested by AC; Community could enter from 18 May; decisions communicated to and approved by AC; lock changes by agreement/approval; she transmitted AC access rules to guards; CAM/JDAM entered as owners.'],
      ['Laura Acosta Matos · CAM', 'Attended May/June meetings; knew security would be installed; went on 7 June to access; denied ordering lock changes/damage; said CAM was paying Community arrears/charges and supplying liquidity. Read together with the AC’s separate access authorisation.'],
      ['José Daniel Acosta Matos · CAM', 'Acknowledged prior inspection/project visits to acquired or prospective units, sometimes with tourism advisers; said he entered with Miguel, denied forced or concealed access and denied claiming ownership of the whole complex. Mandatory counterevidence to a blanket clandestine-access narrative.'],
      ['Antonio Cogolludo · Community presidency', 'Said the 18-May meeting adopted security access control and that he replaced code access with a guard; denied broader lock changes by him.']
    ],
    asymTitle: 'The causal asymmetry that now has to be answered',
    asym: 'The classification measures downstream: uncollected rent and supposed operator economic capacity. The expanded record requires upstream measurement too: actually exploitable inventory, governance and voting, Community costs, maintenance and payroll, offsets, occupancy, revenue, AC decisions and the later access regime. The same actor who advanced the economic accusation acknowledged limits in his knowledge of unity of operation and maintenance cost and later a direct role in the security/access system. That does not prove bias; it requires a reciprocal knowledge, power, decision and causation audit.',
    judicialTitle: 'What is already corrected — and what remains adverse',
    judicial: [
      ['REJECTED', 'Entering the agreement because rent was below the mortgage was not, by itself, a culpable act.'],
      ['CORRECTED', 'The €737,338.85 “LPB owes itself” construction did not prevail against the accepted expert explanation.'],
      ['REJECTED IN THAT BRANCH', '“Connivencia” was not sufficiently corroborated to convert Pink’s lack of attachable assets into an LPB alzamiento; do not say every reference to connivencia was erased.'],
      ['REJECTED', 'Personal complicity was not extended to Patricia where individual attribution was insufficiently argued.'],
      ['ADVERSE · APPEALED', 'Later failure to pursue/collect rent did support gross fault, causation and Pink complicity in Judgment 163/2023.']
    ],
    adverse: 'There is also adverse judicial context on the 2018 access episode: the Provincial Court upheld provisional criminal archive and accepted Community maintenance/access authority and the AC’s account as part of a possible civil/lawful explanation. That was not a whole-hotel possession order for CAM and did not decide every later civil, insolvency, tourism or patrimonial consequence.',
    close: 'The decisive evidence is one reconciliation: EXPLOITABLE INVENTORY → OCCUPANCY → RECEIPTS → COSTS → COMMUNITY/DEBT/VOTE → OFFSETS → BANKS → AC DECISIONS → SECURITY/ACCESS → COMMUNITY/OWNER IMPLEMENTATION → OPERATING EFFECT → REALISTICALLY RECOVERABLE RENT → SPECIFIC INSOLVENCY AGGRAVATION. By express control of this audit, we are not advancing to Allegation 04 yet.',
    source: 'Internal control: CALIFICACION_ALLEGATION_03_UNITARY_COMMUNITY_PRIVATE_ACTORS_AC_CAUSATION_16AUG2026.md + CALIFICACION_ALLEGATION_03_DP1132_PRIVATE_ACTOR_SOURCE_COMPLETION_16AUG2026.md. Preserved court declarations: DP 1132/2018, 20 and 31 July 2018. The 26-February transcript remains party-attributed evidence pending native authentication.'
  };

  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
  const style = document.createElement('style');
  style.textContent = `
    [data-a03-unitary-causation-20260816]{background:#13252d;color:#fff;border-top:1px solid rgba(255,255,255,.12);border-bottom:1px solid rgba(255,255,255,.12)}
    .u03-wrap{max-width:1100px;margin:0 auto;padding:4rem 1.25rem}.u03-eye{font-size:.76rem;font-weight:900;letter-spacing:.09em;text-transform:uppercase;color:#e3c782}.u03-wrap h2{font-size:clamp(2rem,4vw,3.25rem);line-height:1.06;margin:.45rem 0 1rem;max-width:980px}.u03-lead{font-size:1.12rem;line-height:1.7;max-width:980px}.u03-status{margin:1.3rem 0 2.4rem;padding:1rem 1.15rem;border:1px solid #e3c782;border-radius:12px;color:#f5e9c7;line-height:1.55}.u03-chain{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.8rem;margin:1rem 0 2.5rem}.u03-step{background:#fff;color:#13252d;border-radius:14px;padding:1rem}.u03-step strong{display:block;color:#76592c;margin-bottom:.4rem}.u03-step span{line-height:1.5}.u03-block{background:rgba(255,255,255,.07);border-left:5px solid #e3c782;padding:1rem 1.15rem;border-radius:10px;line-height:1.65;margin:1rem 0 2.5rem}.u03-roles,.u03-judicial{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.8rem;margin:1rem 0 2.5rem}.u03-mini{border:1px solid rgba(255,255,255,.22);border-radius:13px;padding:1rem;line-height:1.5}.u03-mini strong{display:block;color:#e3c782;margin-bottom:.35rem}.u03-adverse{background:#fff;color:#13252d;border-radius:14px;padding:1.1rem;line-height:1.65;margin:1rem 0 2.2rem}.u03-close{font-size:1.08rem;font-weight:750;line-height:1.65;border-top:1px solid rgba(255,255,255,.2);padding-top:1.4rem}.u03-source{font-size:.8rem;line-height:1.55;color:#c9d1d4;margin-top:1.25rem}
    @media(max-width:820px){.u03-chain,.u03-roles,.u03-judicial{grid-template-columns:1fr}.u03-wrap{padding:3rem 1rem}}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.setAttribute('data-a03-unitary-causation-20260816','');
  section.innerHTML = `<div class="u03-wrap">
    <div class="u03-eye">${esc(d.eyebrow)}</div><h2>${esc(d.title)}</h2><p class="u03-lead">${esc(d.lead)}</p><div class="u03-status">${esc(d.status)}</div>
    <h3>${esc(d.chainTitle)}</h3><div class="u03-chain">${d.chain.map(x=>`<article class="u03-step"><strong>${esc(x[0])}</strong><span>${esc(x[1])}</span></article>`).join('')}</div>
    <h3>${esc(d.earlyTitle)}</h3><div class="u03-block">${esc(d.early)}</div>
    <h3>${esc(d.rolesTitle)}</h3><div class="u03-roles">${d.roles.map(x=>`<article class="u03-mini"><strong>${esc(x[0])}</strong><span>${esc(x[1])}</span></article>`).join('')}</div>
    <h3>${esc(d.asymTitle)}</h3><div class="u03-block">${esc(d.asym)}</div>
    <h3>${esc(d.judicialTitle)}</h3><div class="u03-judicial">${d.judicial.map(x=>`<article class="u03-mini"><strong>${esc(x[0])}</strong><span>${esc(x[1])}</span></article>`).join('')}</div>
    <div class="u03-adverse">${esc(d.adverse)}</div><div class="u03-close">${esc(d.close)}</div><p class="u03-source">${esc(d.source)}</p>
  </div>`;

  const anchor = document.querySelector('[data-cal-allegation03-20260816]');
  if (anchor) anchor.insertAdjacentElement('afterend', section);
  else document.querySelector('main')?.prepend(section);
})();
