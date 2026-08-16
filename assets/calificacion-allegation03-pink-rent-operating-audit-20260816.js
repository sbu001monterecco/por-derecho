(() => {
  const path = window.location.pathname.replace(/\/+$/, '') + '/';
  const es = path.endsWith('/es/calificacion-concurso-36-2012-vidas-paralelas/');
  const en = path.endsWith('/en/insolvency-classification-parallel-lives/');
  if (!es && !en) return;
  if (document.querySelector('[data-cal-allegation03-20260816]')) return;

  const d = es ? {
    eyebrow: 'AUDITORÍA PROFUNDA · ALEGACIÓN 03 · PINK / MONTERECCO · RENTA Y EXPLOTACIÓN',
    title: 'La propia sentencia partió la acusación en dos: celebrar el contrato no fue culpable; el impago sí fue declarado adverso',
    lead: 'La lectura rigurosa exige conservar las dos cosas a la vez. Sentencia 163/2023 rechazó la idea de que el contrato de 6 de febrero de 2012 fuera ya reprochable porque la renta no cubría la hipoteca. Pero después declaró adversamente que Pink no pagó rentas, que Gil no las reclamó con la diligencia exigible, y apreció culpa grave, causalidad y complicidad de Pink. Esa segunda rama está recurrida.',
    splitTitle: 'Dos proposiciones que no pueden volver a mezclarse',
    split: [
      ['03-A · ENTRAR EN EL CONTRATO', 'RECHAZADA', 'La comparación renta versus cuota hipotecaria no bastaba para convertir la celebración del contrato en acto antijurídico de calificación.'],
      ['03-B · IMPAGO / RECLAMACIÓN', 'ADVERSA · RECURRIDA', 'La sentencia sí reprocha el impago posterior y la falta de reclamación, y declara culpa grave, causalidad y complicidad.']
    ],
    contractTitle: 'Lo que la AC sabía del contrato completo',
    contractLead: 'El contrato original está dentro de la propia demanda de resolución de la AC. La economía pactada no era únicamente una renta de 24.575 €.',
    contract: [
      ['24.575 €/mes', 'Renta neta', 'Pago mensual a LPB.'],
      ['33.915,29 €/mes', 'Cuotas de Comunidad', 'La explotadora asumía las cuotas correspondientes a LPB.'],
      ['58.490,29 €/mes', 'Carga fija conjunta', 'Renta + Comunidad, antes de IGIC.'],
      ['701.883,48 €/año', 'Carga fija anualizada', 'Sin contar el amplio bloque de costes operativos asumidos por la explotadora.']
    ],
    frame: 'Por eso, usar sólo 24.575 € y compararlo con la cuota hipotecaria era una descripción económica incompleta del acuerdo. Eso no perdona una renta impagada: obliga a separar el valor del contrato de la conducta posterior de pago y cobro.',
    expertTitle: 'Pericial de Fiscalía recuperada: importante, pero no dice lo que a veces se le atribuye',
    expertLead: 'Hemos recuperado la pericial de Tomás Ramírez Gómez-Ojero, informe de 5 de abril de 2019 presentado el 25 de abril en DP 332/2014. Su objeto era estimar una renta media de mercado. Como no recibió documentación operativa completa, trabajó con un modelo y comparables.',
    expertRows: [
      ['Sí sostiene', 'El precio contractual estaba dentro de rangos razonables de rentabilidad/arrendamiento hotelero usados en la pericial.'],
      ['Sí modeliza', '124.851,74 € de ingreso mensual potencial, 87.950,13 € de gastos y un resultado operativo modelizado de 36.901,61 €.'],
      ['No demuestra', 'Los ingresos reales, ocupación, ADR, beneficio, caja o capacidad efectiva de pago de Pink durante 2012–2015.'],
      ['Corrección a la defensa', 'No permite afirmar como hecho probado que Pink no obtuvo beneficio o que todos sus ingresos reales se consumieron en mantenimiento.']
    ],
    adverseTitle: 'La rama adversa que no escondemos',
    adverse: [
      'La AC sí ejercitó una acción de resolución y reclamación; no es correcto decir que nunca actuó sobre la renta.',
      'La sentencia de 24 de noviembre de 2015 aparece en Sentencia 163/2023 con una condena de 2.733.923,64 €.',
      'La ejecución posterior no localizó bienes embargables, según el Auto de 6 de septiembre de 2016 citado por la sentencia.',
      'Sentencia 163/2023 considera que Gil debió reclamar y resolver antes, aprecia culpa grave y causalidad y declara a Pink cómplice.',
      'Todo este bloque está sometido a apelación; no se presenta como firme.'
    ],
    profitTitle: 'Capacidad de pago: una presunción no es una contabilidad',
    profit: 'La sentencia observa que la prueba de gastos no incorporaba los ingresos reales de explotación y razona que podía presumirse que éstos superaban a los gastos porque, de otro modo, no sería razonable mantener la explotación durante años. A la vez, reconoce la falta de prueba suficiente de ocupación y precio turístico diario. La pericial de Fiscalía ahora recuperada tampoco resuelve esto: es un modelo de mercado, no una auditoría de las cuentas reales de Pink.',
    moneyTitle: 'La escalera de cifras que necesita un puente euro por euro',
    money: [
      ['24.575 €/mes', 'renta contractual'],
      ['33.915,29 €/mes', 'cuota Comunidad asumida'],
      ['1.130.450 €', 'apelación Pink: 46 × 24.575; comparación sólo-renta'],
      ['1.375.775,01 €', 'importe monetario reclamado en la demanda inicial AC según el expediente recuperado'],
      ['1.670.675 €', 'cuantía procesal indicada en aquella demanda'],
      ['2.733.923,64 €', 'importe atribuido por Sentencia 163/2023 a la sentencia de 24-11-2015'],
      ['3.032.010,34 €', 'principal de ejecución convertido después en daños contra Gil']
    ],
    moneyNote: 'Estas cifras no son automáticamente equivalentes. La demanda original incluía renta, cuotas de Comunidad, devengos futuros y otros conceptos procesales. La pregunta correcta es qué componente produjo cada euro y cómo se pasó de la sentencia de 2015 al principal de ejecución de 3,032 millones.',
    conflictTitle: 'Una contradicción fáctica que sólo deben resolver los bancos y la contabilidad',
    conflict: 'La sentencia dice que Pink no pagó nunca renta. La apelación de Pink afirma que sí hubo pagos iniciales y parciales y remite a la contabilidad de LPB. Hoy esa afirmación defensiva sigue siendo una alegación. No la convertimos en hecho: exigimos el mayor, extractos bancarios, facturas y conciliación mes a mes.',
    gradeTitle: 'Graduación probatoria actual',
    grades: [
      ['Contrato culpable por renta inferior a hipoteca', 'RECHAZADO', 'La propia Sentencia 163/2023 separa y rechaza ese reproche.'],
      ['AC conocía renta + Comunidad + cargas operativas', 'VERIFICADO', 'El contrato está incorporado a su propia demanda.'],
      ['Precio contractual razonable en términos de mercado', 'APOYADO POR PERICIAL', 'Modelo de Fiscalía; no prueba la caja real de Pink.'],
      ['Pink obtuvo cero beneficio real', 'NO PROBADO', 'La pericial recuperada no reconstruyó las cuentas reales.'],
      ['Pink no pagó rentas', 'ADVERSO / RECURRIDO', 'Hallazgo de primera instancia; la apelación lo discute.'],
      ['Culpa grave, causalidad y complicidad Pink', 'ADVERSO / RECURRIDO', 'Conclusiones expresas de Sentencia 163/2023.'],
      ['Capacidad real de Pink para pagar en cada fecha', 'ABIERTO', 'Faltan cuentas, bancos, PMS, ocupación y cobros reales.'],
      ['Origen completo de 3.032.010,34 €', 'ABIERTO', 'Falta reconciliación sentencia → ejecución → daños.']
    ],
    quote: '“No tenemos que elegir entre borrar la sentencia o aceptar toda la acusación. El expediente obliga a algo más exigente: separar el contrato —cuyo reproche económico fue rechazado— del impago posterior —que fue declarado adverso— y producir la economía real y el cálculo completo.”',
    note: 'Control interno: CALIFICACION_ALLEGATION_03_PINK_OPERATING_RENT_CAUSATION_LEDGER_16AUG2026.md. Pericial Fiscalía recuperada: Tomás Ramírez Gómez-Ojero, informe 05-04-2019 / entrada 25-04-2019, DP 332/2014. La apelación continúa siendo una posición de parte. La recuperación de la pericial no prueba por sí sola qué material estaba incorporado o valorado en la pieza de calificación.'
  } : {
    eyebrow: 'DEEP AUDIT · ALLEGATION 03 · PINK / MONTERECCO · RENT AND OPERATION',
    title: 'The judgment itself split the accusation in two: entering the contract was not culpable; non-payment was found adversely',
    lead: 'A rigorous reading has to preserve both points at once. Judgment 163/2023 rejected the proposition that the 6-Feb-2012 agreement was itself blameworthy because rent did not cover the mortgage. It later found, however, that Pink failed to pay rent, that Gil failed to pursue it with the required diligence, and it found gross fault, causation and Pink complicity. That second branch is under appeal.',
    splitTitle: 'Two propositions that must not be merged again',
    split: [
      ['03-A · ENTERING THE AGREEMENT', 'REJECTED', 'Rent versus mortgage instalment was not enough to make entry into the contract an unlawful classification act.'],
      ['03-B · NON-PAYMENT / COLLECTION', 'ADVERSE · APPEALED', 'The judgment does criticise later non-payment and non-enforcement, finding gross fault, causation and complicity.']
    ],
    contractTitle: 'What the AC knew about the complete contract',
    contractLead: 'The original agreement sits inside the AC’s own resolution claim. The agreed economics were not merely a €24,575 rent.',
    contract: [
      ['€24,575/month', 'Net rent', 'Monthly payment to LPB.'],
      ['€33,915.29/month', 'Community charges', 'The operator assumed LPB’s corresponding Community quota.'],
      ['€58,490.29/month', 'Combined fixed burden', 'Rent + Community before IGIC.'],
      ['€701,883.48/year', 'Annualised fixed burden', 'Before the broad operating-cost block assumed by the operator.']
    ],
    frame: 'Using only €24,575 and comparing it with the mortgage therefore gave an incomplete economic description of the agreement. That does not excuse unpaid rent; it requires contract value to be separated from later payment and collection conduct.',
    expertTitle: 'Fiscalía expert recovered: important, but narrower than sometimes claimed',
    expertLead: 'We recovered the expert report by Tomás Ramírez Gómez-Ojero, dated 5 April 2019 and filed on 25 April in DP 332/2014. Its purpose was to estimate average market rent. Because complete operating material was not supplied, it used modelling and comparables.',
    expertRows: [
      ['It does support', 'The contractual price sat within the reasonable hotel-rent/return ranges used by the expert.'],
      ['It models', '€124,851.74 potential monthly income, €87,950.13 expenses and a €36,901.61 modelled operating result.'],
      ['It does not prove', 'Pink’s actual revenue, occupancy, ADR, profit, cash or practical ability to pay during 2012–2015.'],
      ['Defence correction', 'It cannot establish as fact that Pink made no profit or that all actual income was consumed by maintenance.']
    ],
    adverseTitle: 'The adverse branch we do not hide',
    adverse: [
      'The AC did bring a resolution/recovery action; it is inaccurate to say it never acted on rent.',
      'Judgment 163/2023 records the 24-Nov-2015 judgment at €2,733,923.64.',
      'Later enforcement found no attachable assets, according to the 6-Sep-2016 order cited by the judgment.',
      'Judgment 163/2023 finds Gil should have demanded payment/resolution earlier, and finds gross fault, causation and Pink complicity.',
      'That whole branch is on appeal; it is not described here as final.'
    ],
    profitTitle: 'Ability to pay: a presumption is not a set of accounts',
    profit: 'The judgment notes that the expense evidence did not include actual operating income and reasons that income could be presumed to exceed expenses because otherwise continued operation for years would be hard to understand. It also notes the lack of sufficient occupancy and daily-tourist-price proof. The recovered Fiscalía expert does not close that gap either: it is a market model, not an audit of Pink’s actual accounts.',
    moneyTitle: 'The amount ladder that needs a euro-by-euro bridge',
    money: [
      ['€24,575/month', 'contractual rent'],
      ['€33,915.29/month', 'Community charge assumed'],
      ['€1,130,450', 'Pink appeal: 46 × €24,575; rent-only comparator'],
      ['€1,375,775.01', 'monetary amount sought in the recovered early AC claim'],
      ['€1,670,675', 'procedural amount stated in that claim'],
      ['€2,733,923.64', 'amount Judgment 163/2023 attributes to the 24-Nov-2015 judgment'],
      ['€3,032,010.34', 'execution principal later converted into damages against Gil']
    ],
    moneyNote: 'These figures are not automatically equivalent. The original claim included rent, Community charges, future accrual and procedural components. The correct question is which component produced each euro and how the 2015 judgment became the €3.032m execution principal.',
    conflictTitle: 'A factual conflict that should be resolved by banks and ledgers, not assertion',
    conflict: 'The judgment says Pink never paid rent. Pink’s appeal says initial and partial payments did occur and points to LPB accounting. That defence statement remains a party allegation today. We do not upgrade it: the general ledger, bank statements, invoices and month-by-month reconciliation must decide it.',
    gradeTitle: 'Current evidential grading',
    grades: [
      ['Contract culpable because rent < mortgage', 'REJECTED', 'Judgment 163/2023 itself separates and rejects that reproach.'],
      ['AC knew rent + Community + operating burden', 'VERIFIED', 'The agreement is incorporated into the AC’s own claim.'],
      ['Contract price reasonable by market metrics', 'EXPERT-SUPPORTED', 'Fiscalía model; not proof of Pink’s actual cash.'],
      ['Pink made zero actual profit', 'NOT PROVED', 'Recovered expert did not reconstruct actual accounts.'],
      ['Pink paid no rent', 'ADVERSE / APPEALED', 'First-instance finding; the appeal disputes it.'],
      ['Gross fault, causation and Pink complicity', 'ADVERSE / APPEALED', 'Express Judgment 163/2023 conclusions.'],
      ['Pink’s actual ability to pay at each date', 'OPEN', 'Accounts, banks, PMS, occupancy and real receipts remain missing.'],
      ['Complete provenance of €3,032,010.34', 'OPEN', 'Judgment → enforcement → damages bridge remains unreconciled.']
    ],
    quote: '“We do not have to choose between erasing the judgment and accepting the whole accusation. The record requires something more demanding: separate the contract — whose economic reproach was rejected — from later non-payment — which was found adversely — and produce the actual economics and complete calculation.”',
    note: 'Internal control: CALIFICACION_ALLEGATION_03_PINK_OPERATING_RENT_CAUSATION_LEDGER_16AUG2026.md. Recovered Fiscalía expert: Tomás Ramírez Gómez-Ojero, report 05-Apr-2019 / filing 25-Apr-2019, DP 332/2014. The appeal remains party material. Recovery of the expert does not by itself prove what material was formally incorporated or assessed in the calificación proceeding.'
  };

  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
  const style = document.createElement('style');
  style.textContent = `
    [data-cal-allegation03-20260816]{background:#f9faf9;border-bottom:1px solid rgba(19,37,45,.12)}
    .a03-wrap{max-width:1080px;margin:0 auto;padding:4rem 1.25rem}.a03-eyebrow{font-size:.76rem;letter-spacing:.09em;text-transform:uppercase;font-weight:850;color:#76592c}.a03-wrap h2{font-size:clamp(2rem,4vw,3.15rem);line-height:1.06;max-width:950px;margin:.4rem 0 1rem}.a03-lead{font-size:1.12rem;line-height:1.65;max-width:950px}.a03-split{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin:1rem 0 2.4rem}.a03-card{border:1px solid rgba(19,37,45,.16);border-radius:16px;padding:1.1rem;background:#fff}.a03-card .status{font-size:.72rem;font-weight:900;letter-spacing:.05em;color:#76592c}.a03-card strong{display:block;margin:.35rem 0}.a03-card p{margin:.3rem 0 0;line-height:1.5}.a03-contract{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.8rem;margin:1rem 0 1.4rem}.a03-num{font-size:1.3rem;font-weight:850}.a03-frame{border-left:5px solid #8c6b2f;background:#f3efe4;padding:1rem 1.15rem;border-radius:10px;line-height:1.6;margin-bottom:2.5rem}.a03-expert{background:#13252d;color:#fff;border-radius:18px;padding:1.3rem;margin:1rem 0 2.4rem}.a03-expert p{line-height:1.6}.a03-expert table{width:100%;border-collapse:collapse;background:#fff;color:#13252d}.a03-expert td{padding:.78rem;border:1px solid #d8dddd;vertical-align:top}.a03-adverse{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.8rem;margin:1rem 0 2.3rem}.a03-adverse div{background:#fff;border:1px solid #d8dddd;border-radius:14px;padding:1rem;line-height:1.5}.a03-profit{border:2px solid #13252d;border-radius:16px;padding:1.15rem;line-height:1.65;margin:1rem 0 2.4rem}.a03-money{overflow-x:auto;margin:1rem 0}.a03-money table,.a03-grade table{width:100%;border-collapse:collapse;background:#fff}.a03-money th,.a03-money td,.a03-grade th,.a03-grade td{padding:.75rem;border:1px solid #dce0df;text-align:left;vertical-align:top}.a03-money th{background:#13252d;color:#fff}.a03-noteBox{background:#f3efe4;border-radius:12px;padding:1rem;line-height:1.55;margin-bottom:2.4rem}.a03-conflict{border-left:5px solid #13252d;padding:.9rem 1.1rem;line-height:1.6;margin:1rem 0 2.4rem}.a03-grade{overflow-x:auto}.a03-grade th{font-size:.78rem;text-transform:uppercase;letter-spacing:.04em}.a03-grade .status{font-size:.72rem;font-weight:900;white-space:nowrap}.a03-quote{margin:2.2rem 0 1.4rem;padding:1.4rem 0;border-top:1px solid rgba(19,37,45,.2);border-bottom:1px solid rgba(19,37,45,.2);font-size:1.18rem;line-height:1.55;font-weight:700}.a03-source{font-size:.82rem;color:#5d6262;line-height:1.5}
    @media(max-width:820px){.a03-split,.a03-contract,.a03-adverse{grid-template-columns:1fr}.a03-wrap{padding:3rem 1rem}}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.setAttribute('data-cal-allegation03-20260816','');
  section.innerHTML = `<div class="a03-wrap">
    <div class="a03-eyebrow">${esc(d.eyebrow)}</div><h2>${esc(d.title)}</h2><p class="a03-lead">${esc(d.lead)}</p>
    <h3>${esc(d.splitTitle)}</h3><div class="a03-split">${d.split.map(x=>`<article class="a03-card"><div class="status">${esc(x[1])}</div><strong>${esc(x[0])}</strong><p>${esc(x[2])}</p></article>`).join('')}</div>
    <h3>${esc(d.contractTitle)}</h3><p>${esc(d.contractLead)}</p><div class="a03-contract">${d.contract.map(x=>`<article class="a03-card"><div class="a03-num">${esc(x[0])}</div><strong>${esc(x[1])}</strong><p>${esc(x[2])}</p></article>`).join('')}</div><div class="a03-frame">${esc(d.frame)}</div>
    <div class="a03-expert"><h3>${esc(d.expertTitle)}</h3><p>${esc(d.expertLead)}</p><table><tbody>${d.expertRows.map(x=>`<tr><td><strong>${esc(x[0])}</strong></td><td>${esc(x[1])}</td></tr>`).join('')}</tbody></table></div>
    <h3>${esc(d.adverseTitle)}</h3><div class="a03-adverse">${d.adverse.map(x=>`<div>${esc(x)}</div>`).join('')}</div>
    <h3>${esc(d.profitTitle)}</h3><div class="a03-profit">${esc(d.profit)}</div>
    <h3>${esc(d.moneyTitle)}</h3><div class="a03-money"><table><thead><tr><th>${es?'Cifra':'Figure'}</th><th>${es?'Qué representa':'What it represents'}</th></tr></thead><tbody>${d.money.map(x=>`<tr><td><strong>${esc(x[0])}</strong></td><td>${esc(x[1])}</td></tr>`).join('')}</tbody></table></div><div class="a03-noteBox">${esc(d.moneyNote)}</div>
    <h3>${esc(d.conflictTitle)}</h3><div class="a03-conflict">${esc(d.conflict)}</div>
    <h3>${esc(d.gradeTitle)}</h3><div class="a03-grade"><table><thead><tr><th>${es?'Proposición':'Proposition'}</th><th>${es?'Estado':'Status'}</th><th>${es?'Base':'Basis'}</th></tr></thead><tbody>${d.grades.map(x=>`<tr><td>${esc(x[0])}</td><td><span class="status">${esc(x[1])}</span></td><td>${esc(x[2])}</td></tr>`).join('')}</tbody></table></div>
    <div class="a03-quote">${esc(d.quote)}</div><p class="a03-source">${esc(d.note)}</p>
  </div>`;

  const anchor = document.querySelector('[data-cal-allegation02-20260816]') || document.querySelector('[data-cal-allegation01-20260816]') || document.querySelector('[data-calificacion-radical-20260816]');
  if (anchor) anchor.insertAdjacentElement('afterend', section);
  else (document.querySelector('.hero.cal-hero') || document.querySelector('main .hero'))?.insertAdjacentElement('afterend', section);
})();