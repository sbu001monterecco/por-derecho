(() => {
  const path = window.location.pathname.replace(/\/+$/, '') + '/';
  const es = path.endsWith('/es/calificacion-concurso-36-2012-vidas-paralelas/');
  const en = path.endsWith('/en/insolvency-classification-parallel-lives/');
  if (!es && !en) return;
  if (document.querySelector('[data-cal-judicial-adoption-20260816]')) return;

  const d = es ? {
    kicker: 'DE ALEGACIÓN A HECHO JUDICIAL · EFECTO FUERA DE LA CALIFICACIÓN',
    title: 'El punto crítico: el juez convirtió determinadas acusaciones de la AC en afirmaciones judiciales propias.',
    lead: '<strong>Mi acusación no es simplemente que la Administración Concursal mintiera y que el juez no la corrigiera.</strong> En el fundamento cuarto de la Sentencia 163/2023, Alberto López Villarrubia adoptó determinadas premisas como hechos judiciales y las utilizó contra nosotros.',
    cards: [
      ['HALLAZGO JUDICIAL', '<strong>“Connivencia” + “sin pagar renta alguna”.</strong> La sentencia considera acreditado que Pink explotó Sun Park en connivencia con LPB y sin pagar renta alguna. Atribuye a Gil al menos culpa grave —si no dolo— y declara probado el nexo causal con la agravación de la insolvencia.'],
      ['TENSIÓN INTERNA', '<strong>La misma palabra no recibe el mismo tratamiento en toda la sentencia.</strong> En el fundamento sexto, al rechazar la rama de alzamiento ligada a la ejecución frustrada contra Pink, la referencia a connivencia se califica como mera alegación sin corroboración probatoria. Son módulos distintos y pueden referirse a conductas o periodos distintos; precisamente por eso debe identificarse qué prueba sostuvo cada conclusión.'],
      ['CONTRA-REGISTRO EN APELACIÓN', '<strong>La apelación niega el “nunca pagó”.</strong> Sostiene que hubo pagos iniciales, pagos parciales posteriores y asunción de gastos de mantenimiento, y dice que los pagos constan en la contabilidad de LPB. Es una alegación de parte, no prueba definitiva. La comprobación finita es recuperar los asientos, bancos y anexos que estuvieron realmente ante el juez.'],
      ['PUENTE 1901 / ACTORES PRIVADOS', '<strong>DP 1901/2026 es una vía de verificación, no una condena.</strong> La providencia localizada de 12 julio 2026 trasladó la denuncia al Ministerio Fiscal por cinco días para informar sobre admisibilidad. La comunicación posterior a Fiscalía de la Audiencia Nacional pide coordinar sólo la prueba pertinente sobre identidad, conocimiento, control y beneficio sin diluir su objeto autónomo.']
    ],
    accusationTitle: 'Mi acusación sobre el efecto privado',
    accusation: '<strong>Alego que la judicialización de este relato materialmente falso operó criminalmente en favor de actores privados y, en particular, del perímetro Acosta Matos.</strong> El efecto que denuncio es una asignación asimétrica: culpa, pasivo y perjuicio concentrados en Pink/Gil, mientras las cuestiones de control, título, explotación, financiación y beneficio del otro lado siguieron una vida materialmente distinta. No afirmo que DP 1901/2026 haya probado ya esa tesis ni que exista ya una sentencia penal contra los actores privados. Exijo que se reconstruya actor por actor quién conocía qué, quién utilizó qué documento, quién obtuvo o esperaba obtener qué ventaja y mediante qué acto o flujo.',
    chainTitle: 'La cadena que debe auditarse',
    chain: 'AC ALEGA → FISCAL RESPALDA → JUEZ ADOPTA HECHOS → SENTENCIA IMPONE CONSECUENCIAS → EL DOCUMENTO ADQUIERE AUTORIDAD PORTÁTIL → SE INVESTIGA SU UTILIZACIÓN / BENEFICIO PRIVADO',
    dp: 'Abrir DP 1901/2026 →',
    note: 'Control probatorio: la adopción judicial de las premisas del fundamento cuarto es documental. El favorecimiento criminal, la intención, la eventual procuración del resultado y el beneficio privado son acusaciones de Gil Marer que requieren prueba independiente.'
  } : {
    kicker: 'FROM ALLEGATION TO JUDICIAL FACT · EFFECT BEYOND THE CLASSIFICATION',
    title: 'The critical point: the Judge converted selected AC accusations into the Court’s own findings.',
    lead: '<strong>My allegation is not simply that the insolvency administration lied and the Judge failed to correct it.</strong> In Ground Four of Judgment 163/2023, Alberto López Villarrubia adopted selected premises as judicial findings and used them against us.',
    cards: [
      ['JUDICIAL FINDING', '<strong>“Connivencia” + “no rent at all”.</strong> The judgment treats it as established that Pink operated Sun Park in connivance with LPB and paid no rent. It attributes at least gross negligence —if not intent— to Gil and declares a causal nexus with aggravation of insolvency.'],
      ['INTERNAL TENSION', '<strong>The same loaded concept is not treated the same way throughout the judgment.</strong> In Ground Six, while rejecting the concealment branch tied to the frustrated execution against Pink, the connivance reference is called a mere allegation without evidential corroboration. These are different legal modules and may concern different conduct or periods; that makes the evidence supporting each conclusion the question to expose.'],
      ['APPELLATE COUNTER-RECORD', '<strong>The appeal denies “never paid”.</strong> It says there were initial payments, later partial payments and maintenance expenditure, and says payment appears in LPB accounting. That is a party allegation, not final proof. The finite test is the actual ledger, bank records and exhibits that were before the Judge.'],
      ['DP 1901 / PRIVATE-ACTOR BRIDGE', '<strong>DP 1901/2026 is an evidence-verification route, not a conviction.</strong> The located 12 July 2026 providencia sent the complaint to the Public Prosecutor for five days on admissibility. The later Audiencia Nacional communication seeks only relevant evidence on identity, knowledge, control and benefit without diluting its autonomous object.']
    ],
    accusationTitle: 'My allegation about the private-actor effect',
    accusation: '<strong>I allege that judicialising this materially false narrative operated criminally in favour of private actors and, in particular, the Acosta Matos perimeter.</strong> The asymmetry I allege is blame, liabilities and prejudice concentrated on Pink/Gil while control, title, operation, finance and benefit questions on the other side followed a materially different track. I do not claim DP 1901/2026 has already proved that thesis or that a criminal court has already convicted the private actors. I demand an actor-by-actor reconstruction of who knew what, who used which document, who obtained or expected which advantage and through what act or flow.',
    chainTitle: 'The chain that must be audited',
    chain: 'AC ALLEGES → FISCAL ENDORSES → JUDGE ADOPTS FACTS → JUDGMENT IMPOSES CONSEQUENCES → DOCUMENT GAINS PORTABLE AUTHORITY → PRIVATE USE / BENEFIT IS INVESTIGATED',
    dp: 'Open DP 1901/2026 →',
    note: 'Evidential control: judicial adoption of the Ground Four premises is documented. Criminal favouring, intent, procurement of the outcome and private benefit are Gil Marer’s allegations and require independent proof.'
  };

  const style = document.createElement('style');
  style.textContent = `
    .cja{padding:0 0 2.2rem}.cja-wrap{max-width:1080px;margin:0 auto}.cja-box{background:#fff;border:2px solid #263b45;border-radius:20px;padding:1.4rem;box-shadow:0 12px 32px rgba(19,37,45,.07)}
    .cja-kicker{font-size:.75rem;letter-spacing:.09em;text-transform:uppercase;font-weight:900;color:#7b2e2e}.cja-box h2{font-size:clamp(1.7rem,3.7vw,2.45rem);line-height:1.08;margin:.4rem 0 .8rem}.cja-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.8rem;margin:1rem 0}.cja-card{background:#f5f3ee;border-radius:14px;padding:1rem;border-top:4px solid #8c6b2f}.cja-card b{font-size:.73rem;letter-spacing:.06em;text-transform:uppercase;color:#6b5841;display:block;margin-bottom:.4rem}.cja-acc{background:#f5e7e4;border-left:6px solid #7b2e2e;border-radius:14px;padding:1rem 1.1rem}.cja-chain{background:#10252e;color:#fff;border-radius:14px;padding:1rem 1.1rem;margin-top:.85rem;font-weight:800;letter-spacing:.015em}.cja-actions{margin-top:.9rem}.cja-note{font-size:.88rem;color:#555;margin:.8rem 0 0}@media(max-width:760px){.cja-grid{grid-template-columns:1fr}.cja-box{border-radius:0}}
  `;
  document.head.appendChild(style);

  const cards = d.cards.map(([h,b]) => `<article class="cja-card"><b>${h}</b><div>${b}</div></article>`).join('');
  const section = document.createElement('section');
  section.className = 'section cja';
  section.dataset.calJudicialAdoption20260816 = '1';
  section.innerHTML = `<div class="shell cja-wrap"><div class="cja-box"><div class="cja-kicker">${d.kicker}</div><h2>${d.title}</h2><p>${d.lead}</p><div class="cja-grid">${cards}</div><div class="cja-acc"><h3>${d.accusationTitle}</h3><p>${d.accusation}</p></div><div class="cja-chain"><div class="cja-kicker" style="color:#d6b16b">${d.chainTitle}</div>${d.chain}</div><div class="cja-actions"><a class="button secondary" href="${es ? '../dp-1901-2026/' : '../dp-1901-2026/'}">${d.dp}</a></div><p class="cja-note">${d.note}</p></div></div>`;

  const amount = document.querySelector('[data-calificacion-3032010-20260816]');
  const opening = document.querySelector('[data-calificacion-opening-20260816]');
  if (amount) amount.insertAdjacentElement('afterend', section);
  else if (opening) opening.insertAdjacentElement('afterend', section);
})();
