(() => {
  const path = window.location.pathname.replace(/\/+$/, '') + '/';
  const es = path.endsWith('/es/calificacion-concurso-36-2012-vidas-paralelas/');
  const en = path.endsWith('/en/insolvency-classification-parallel-lives/');
  if (!es && !en) return;
  if (document.querySelector('[data-cal-allegation02-20260816]')) return;

  const d = es ? {
    eyebrow: 'AUDITORÍA PROFUNDA · ALEGACIÓN 02 · CRÉDITOS FRENTE A TERCEROS',
    title: 'La inversión de la acusación: dinero que otros debían a LPB terminó convertido en culpabilidad contra Gil',
    lead: 'Ésta no es una historia limpia de “acusación falsa” frente a “defensa verdadera”. Existía una cuestión real de diligencia en el cobro y la sentencia conserva una controversia más estrecha sobre documentación soporte. Pero la AC fue mucho más lejos: transformó saldos de terceros, de cobro incierto según su propio informe, en una teoría de culpa grave y en el contrafactual de que LPB podría haber salido de la insolvencia.',
    headline: 'La fuerza de esta auditoría está en separar lo que sí sobrevivió del salto acusatorio que no sobrevivió.',
    amountsTitle: 'Los activos que la AC convirtió en acusación',
    amounts: [
      ['€101.724,93', 'Sun Energy Spaces', 'Crédito a largo plazo. La propia AC advertía que su recuperación dependía de liquidez y solvencia.'],
      ['€518.908,69', 'Clientes', 'Incluía Fermín Pérez Rojas (€4.891,93), Monterecco Sun Park (€41.516,76) y Comunidad de Explotación (€472.500).'],
      ['€737.338,85', 'CEXP', 'Dividendo/derecho de cobro. La AC llegó a sugerir que LPB se debía a sí misma gran parte del importe; la sentencia rechazó esa construcción.']
    ],
    inversionTitle: 'El cambio de dirección que hay que ver',
    inversion: [
      ['ORIGEN', 'La contabilidad registraba dinero adeudado a LPB por terceros / CEXP.'],
      ['GIRO', 'La AC convirtió la falta de cobro en una omisión imputable a Gil.'],
      ['AMPLIFICACIÓN', 'Afirmó que recuperar esas cantidades podría haber permitido superar la insolvencia.'],
      ['CONTROL JUDICIAL', 'La sentencia no aceptó que esa omisión, en estas circunstancias, probara culpa grave bajo el art. 164.1.']
    ],
    breaksTitle: 'Cinco fracturas documentales de la teoría de la AC',
    breaks: [
      ['1 · Cobro incierto', 'El propio inventario de la AC decía que la recuperación dependía de la liquidez y solvencia de los deudores. Un saldo contable no era efectivo disponible.'],
      ['2 · Contrafactual sin puente', 'La frase “podría haber salido de la insolvencia” no venía acompañada de una reconstrucción de probabilidad de cobro, tiempo, costes, solvencia, ejecución ni caja neta disponible.'],
      ['3 · €737k: tesis corregida', 'La pericial aceptada por Sentencia 163/2023 acreditó un derecho de cobro válido de LPB y enervó la afirmación de la AC de que LPB se debía a sí misma una fracción sustancial.'],
      ['4 · Falta el elemento de culpa grave', 'La propia sentencia critica que el informe AC no justificara ni argumentara suficientemente dolo/culpa grave y dice que los créditos principales no eran de fácil reclamación.'],
      ['5 · Un error admitido', 'La sentencia registra que, dentro de esta rama, la AC reconoció en la vista que una partida presentada como reclamable era un error porque no podía reclamarse.']
    ],
    courtTitle: 'Qué decidió realmente Sentencia 163/2023',
    courtLead: 'La sentencia no absolvió toda esta materia ni confirmó toda la acusación. Hizo algo más importante para una lectura seria: la dividió.',
    courtRows: [
      ['Omisión/diligencia al reclamar', 'ADVERSO', 'La sentencia considera acreditada una omisión antijurídica respecto de determinados créditos.'],
      ['Culpa grave del art. 164.1', 'RECHAZADA', 'Los créditos principales eran conflictivos/difíciles y la AC no hizo el esfuerzo argumentativo exigible.'],
      ['“LPB se debe a sí misma” €737k', 'CORREGIDA', 'La pericial aceptada demuestra un crédito válido y enerva la afirmación AC.'],
      ['“Cobrar habría sacado a LPB de insolvencia”', 'NO PROBADO', 'No existe en la acusación un puente económico reproducible que demuestre ese contrafactual.'],
      ['Documentación soporte tras liquidación', 'ADVERSO / RECURRIDO', 'El tribunal mantiene una causa más estrecha de no colaboración; el recurso cuestiona su lógica causal.']
    ],
    tensionTitle: 'La tensión que sigue viva en apelación',
    tension: 'El propio fallo dice primero que los grandes créditos eran de cobro incierto y que esa falta de reclamación no acredita culpa grave. Después, al analizar colaboración, afirma que se desconoce si las acciones habrían prosperado pero presume que al menos alguna cantidad podría haber entrado en la masa. El recurso ataca precisamente esa tensión: <strong>incertidumbre usada para rechazar causalidad fuerte en un fundamento y, después, posibilidad hipotética usada para sostener agravación en otro.</strong>',
    distractTitle: 'Lo que no debe desaparecer detrás de “Gil no cobró”',
    distract: [
      ['Quién debía el dinero', 'Deudor, base jurídica, fecha, obligaciones, defensas y solvencia, crédito por crédito.'],
      ['Por qué quedó impagado', 'El impago de terceros también puede ser causalmente relevante para la situación económica de LPB.'],
      ['Cómo funcionaba CEXP', 'El crédito de €737k obliga a reconstruir contribuciones, gastos, compensaciones y propietarios, no a reducirlo a una frase de “deuda consigo misma”.'],
      ['Qué acciones ya existían', 'La oposición de 2019 afirmó que había procedimientos y esfuerzos de recuperación. Eso debe verificarse uno a uno en sus expedientes primarios.'],
      ['Qué hizo la AC', 'Una vez abierta la liquidación, la propia AC dice que quería ejercitar acciones. Hay que reconstruir qué recibió, qué pudo obtener, qué reclamó, qué dejó vencer y por qué.'],
      ['Cuál era el contrafactual real', '€1,358m en asientos nominales no equivale automáticamente a €1,358m cobrables, líquidos y disponibles en una fecha determinada.']
    ],
    gradeTitle: 'Graduación probatoria actual',
    grades: [
      ['“Nunca se reclamó nada”', 'DISPUTADO', 'Falta la reconstrucción completa de acciones/procedimientos; la oposición afirma que existían.'],
      ['Falta de diligencia en parte del cobro', 'ADVERSO', 'La sentencia lo aprecia; no se borra.'],
      ['Culpa grave por esa omisión', 'RECHAZADA', 'No superó el test del art. 164.1 en primera instancia.'],
      ['Tesis de auto-deuda €737k', 'RECHAZADA', 'La sentencia acepta la pericial contraria.'],
      ['Contrafactual de salida de insolvencia', 'NO PROBADO', 'Falta cálculo causal y de recuperabilidad.'],
      ['Exageración causal consciente', 'ALEGACIÓN SERIA', 'La propia AC había documentado incertidumbre de cobro; falta cerrar conocimiento subjetivo y documentación disponible.'],
      ['Efecto autoservicial/inversor', 'FUERTE COMO EFECTO', 'La atención pasa de los terceros deudores y de la recuperación de la masa a la culpabilidad de Gil.'],
      ['Propósito deliberado de proteger a terceros / distraer', 'HIPÓTESIS ABIERTA', 'Debe probarse mediante decisiones de recuperación, conocimiento, beneficios y comunicaciones.']
    ],
    quote: '“La pregunta completa no es sólo por qué Gil no cobró. Es quién debía a LPB, por qué no pagó, qué acciones existían y qué hizo la propia Administración Concursal para convertir esos activos en dinero una vez que dirigía la liquidación.”',
    note: 'Control interno: CALIFICACION_ALLEGATION_02_THIRDPARTY_CEXP_CREDITS_LEDGER_16AUG2026.md. Fuentes primarias reconsultadas el 16-08-2026: informe AC 11-02-2019, oposición Gil 06-06-2019, Sentencia 163/2023 y recurso de apelación. Las afirmaciones de la oposición sobre actuaciones de la AC/CPSP se mantienen como alegaciones hasta completar los expedientes y comunicaciones originales.'
  } : {
    eyebrow: 'DEEP AUDIT · ALLEGATION 02 · THIRD-PARTY RECEIVABLES',
    title: 'The inversion of the accusation: money others allegedly owed LPB became culpability against Gil',
    lead: 'This is not a clean story of “false accusation” versus “true defence”. There was a genuine collection-diligence issue and the judgment preserves a narrower dispute over supporting documents. But the AC went much further: it transformed third-party balances that its own report described as uncertain to recover into a gross-fault theory and a counterfactual claim that LPB could have emerged from insolvency.',
    headline: 'The strength of this audit is in separating what survived from the accusatory leap that did not.',
    amountsTitle: 'The assets the AC turned into an accusation',
    amounts: [
      ['€101,724.93', 'Sun Energy Spaces', 'Long-term receivable. The AC itself warned that recovery depended on liquidity and solvency.'],
      ['€518,908.69', 'Customers', 'Included Fermín Pérez Rojas (€4,891.93), Monterecco Sun Park (€41,516.76) and the Exploitation Community (€472,500).'],
      ['€737,338.85', 'CEXP', 'Dividend/receivable. The AC suggested LPB substantially owed this to itself; the judgment rejected that construction.']
    ],
    inversionTitle: 'The change of direction that matters',
    inversion: [
      ['ORIGIN', 'LPB accounting recorded money owed to LPB by third parties / CEXP.'],
      ['TURN', 'The AC converted non-collection into an omission attributed to Gil.'],
      ['AMPLIFICATION', 'It asserted that recovery could have enabled LPB to overcome insolvency.'],
      ['JUDICIAL TEST', 'The judgment did not accept that the omission, in these circumstances, proved gross fault under Art. 164.1.']
    ],
    breaksTitle: 'Five documentary breaks in the AC theory',
    breaks: [
      ['1 · Uncertain recovery', 'The AC’s own inventory said recovery depended on debtor liquidity and solvency. An accounting balance was not cash in hand.'],
      ['2 · Counterfactual without a bridge', '“Could have exited insolvency” was not accompanied by a reconstruction of recovery probability, timing, costs, solvency, enforcement or net cash actually available.'],
      ['3 · €737k theory corrected', 'The expert evidence accepted by Judgment 163/2023 established a valid LPB receivable and defeated the AC assertion that LPB substantially owed itself the amount.'],
      ['4 · Gross fault not established', 'The judgment itself criticises the AC report for not sufficiently justifying dolo/gross fault and says the principal receivables were not easy to recover.'],
      ['5 · An admitted error', 'The judgment records that, within this branch, the AC acknowledged at the hearing that one item presented as claimable was an error because it could not be claimed.']
    ],
    courtTitle: 'What Judgment 163/2023 actually decided',
    courtLead: 'The judgment neither rejected all of this material nor validated the whole accusation. It did something more useful for a serious reader: it split the propositions apart.',
    courtRows: [
      ['Omission / collection diligence', 'ADVERSE', 'The judgment finds an unlawful omission concerning pursuit of certain receivables.'],
      ['Gross fault under Art. 164.1', 'REJECTED', 'The principal credits were difficult/conflicted and the AC had not done the required argumentative work.'],
      ['€737k “LPB owes itself” theory', 'CORRECTED', 'Accepted expert evidence establishes a valid receivable and defeats the AC assertion.'],
      ['“Collection would have taken LPB out of insolvency”', 'NOT PROVED', 'The accusation contains no reproducible economic bridge establishing that counterfactual.'],
      ['Supporting documents after liquidation', 'ADVERSE / APPEALED', 'The court preserves a narrower non-collaboration cause; the appeal challenges its causal logic.']
    ],
    tensionTitle: 'The tension still live on appeal',
    tension: 'The judgment first says the major claims were uncertain/difficult to recover and that non-pursuit did not establish gross fault. Later, under collaboration, it says it is unknown whether the actions would have succeeded but reasons that at least some money might have entered the estate. The appeal attacks that precise tension: <strong>uncertainty used to reject strong causation in one section, then hypothetical possibility used to support aggravation in another.</strong>',
    distractTitle: 'What must not disappear behind “Gil did not collect”',
    distract: [
      ['Who owed the money', 'Debtor, legal basis, due date, obligations, defences and solvency, receivable by receivable.'],
      ['Why it remained unpaid', 'Third-party non-payment may itself be economically relevant to LPB’s distress.'],
      ['How CEXP worked', 'The €737k correction requires reconstruction of contributions, costs, compensations and owners, not a “self-debt” slogan.'],
      ['Which actions already existed', 'The 2019 opposition says proceedings/recovery efforts existed. Each must be verified in its primary file.'],
      ['What the AC did', 'After liquidation opened, the AC itself said it intended to pursue actions. Reconstruct what it received, could obtain, sued on, allowed to lapse and why.'],
      ['The real counterfactual', '€1.358m of nominal accounting entries does not automatically equal €1.358m collectible, liquid and available at a given date.']
    ],
    gradeTitle: 'Current evidential grading',
    grades: [
      ['“Nothing was ever pursued”', 'DISPUTED', 'Full action/proceeding reconstruction is still missing; the opposition says proceedings existed.'],
      ['Some collection-diligence failure', 'ADVERSE', 'The judgment finds it; it is not erased.'],
      ['Gross fault because of that omission', 'REJECTED', 'It did not pass the first-instance Art. 164.1 test.'],
      ['€737k self-debt theory', 'REJECTED', 'The judgment accepts the contrary expert evidence.'],
      ['Insolvency-exit counterfactual', 'NOT PROVED', 'No controlled causation/recoverability calculation.'],
      ['Knowing causal exaggeration', 'SERIOUS ALLEGATION', 'The AC itself had documented recovery uncertainty; subjective-knowledge proof remains incomplete.'],
      ['Self-serving / inverting effect', 'STRONG AS EFFECT', 'Attention moves from third-party debtors and estate recovery to Gil’s culpability.'],
      ['Deliberate purpose to shield third parties / distract', 'OPEN HYPOTHESIS', 'Must be proved through recovery decisions, knowledge, benefit and communications.']
    ],
    quote: '“The complete question is not only why Gil did not collect. It is who owed LPB, why they did not pay, what actions already existed, and what the insolvency administration itself did to turn those assets into money once it was directing the liquidation.”',
    note: 'Internal control: CALIFICACION_ALLEGATION_02_THIRDPARTY_CEXP_CREDITS_LEDGER_16AUG2026.md. Primary sources re-queried 16-Aug-2026: AC report 11-Feb-2019, Gil opposition 6-Jun-2019, Judgment 163/2023 and appeal. Opposition allegations concerning AC/CPSP conduct remain allegations until the underlying proceedings and communications are completed.'
  };

  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
  const style = document.createElement('style');
  style.textContent = `
    [data-cal-allegation02-20260816]{background:#fff;border-bottom:1px solid rgba(19,37,45,.12)}
    .a02-wrap{max-width:1080px;margin:0 auto;padding:4rem 1.25rem}.a02-eyebrow{font-size:.76rem;letter-spacing:.09em;text-transform:uppercase;font-weight:850;color:#76592c}.a02-wrap h2{font-size:clamp(2rem,4vw,3.2rem);line-height:1.06;max-width:940px;margin:.4rem 0 1rem}.a02-lead{font-size:1.12rem;line-height:1.65;max-width:940px}.a02-headline{font-size:1.22rem;font-weight:750;border-left:5px solid #8c6b2f;padding:.9rem 1rem;margin:1.5rem 0 2.3rem;background:#f7f4ec;border-radius:10px}
    .a02-amounts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem;margin:1rem 0 2.4rem}.a02-amount{border:1px solid rgba(19,37,45,.15);border-radius:16px;padding:1.15rem;background:#f9f8f4}.a02-num{font-size:1.45rem;font-weight:850;color:#13252d}.a02-amount strong{display:block;margin:.2rem 0 .55rem}.a02-amount p{margin:0;line-height:1.5;font-size:.94rem}
    .a02-flow{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.7rem;margin:1rem 0 2.4rem}.a02-f{background:#13252d;color:#fff;border-radius:14px;padding:1rem}.a02-f .tag{font-size:.7rem;letter-spacing:.07em;font-weight:850;color:#d9c18a}.a02-f p{margin:.45rem 0 0;line-height:1.45}
    .a02-breaks{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.8rem;margin:1rem 0 2.4rem}.a02-break{border:1px solid rgba(19,37,45,.15);border-radius:14px;padding:1rem}.a02-break strong{display:block;margin-bottom:.4rem;color:#76592c}.a02-break p{margin:0;line-height:1.5}
    .a02-court{background:#f7f4ec;border-radius:18px;padding:1.25rem;margin:1.2rem 0 2.2rem}.a02-table{overflow-x:auto}.a02-table table{width:100%;border-collapse:collapse;background:#fff}.a02-table th,.a02-table td{padding:.78rem;border:1px solid #dce0df;text-align:left;vertical-align:top}.a02-table th{background:#13252d;color:#fff}.a02-status{font-size:.73rem;font-weight:900;letter-spacing:.04em;white-space:nowrap}
    .a02-tension{border:2px solid #13252d;border-radius:16px;padding:1.2rem;margin:1rem 0 2.3rem;line-height:1.6}.a02-distract{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.8rem;margin:1rem 0 2.4rem}.a02-d{background:#f7f4ec;border-radius:14px;padding:1rem}.a02-d strong{display:block;margin-bottom:.35rem}.a02-d p{margin:0;font-size:.93rem;line-height:1.45}
    .a02-grade{overflow-x:auto}.a02-grade table{width:100%;border-collapse:collapse}.a02-grade td,.a02-grade th{border-bottom:1px solid #d8dddd;padding:.75rem;text-align:left;vertical-align:top}.a02-grade th{font-size:.78rem;text-transform:uppercase;letter-spacing:.05em}.a02-quote{margin:2.2rem 0 1.4rem;padding:1.4rem 0;border-top:1px solid rgba(19,37,45,.2);border-bottom:1px solid rgba(19,37,45,.2);font-size:1.2rem;line-height:1.55;font-weight:700}.a02-note{font-size:.82rem;color:#5d6262;line-height:1.5}
    @media(max-width:820px){.a02-amounts,.a02-flow,.a02-breaks,.a02-distract{grid-template-columns:1fr}.a02-wrap{padding:3rem 1rem}}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.setAttribute('data-cal-allegation02-20260816','');
  section.innerHTML = `<div class="a02-wrap">
    <div class="a02-eyebrow">${esc(d.eyebrow)}</div><h2>${esc(d.title)}</h2><p class="a02-lead">${esc(d.lead)}</p><div class="a02-headline">${esc(d.headline)}</div>
    <h3>${esc(d.amountsTitle)}</h3><div class="a02-amounts">${d.amounts.map(x=>`<article class="a02-amount"><div class="a02-num">${esc(x[0])}</div><strong>${esc(x[1])}</strong><p>${esc(x[2])}</p></article>`).join('')}</div>
    <h3>${esc(d.inversionTitle)}</h3><div class="a02-flow">${d.inversion.map(x=>`<div class="a02-f"><div class="tag">${esc(x[0])}</div><p>${esc(x[1])}</p></div>`).join('')}</div>
    <h3>${esc(d.breaksTitle)}</h3><div class="a02-breaks">${d.breaks.map(x=>`<div class="a02-break"><strong>${esc(x[0])}</strong><p>${esc(x[1])}</p></div>`).join('')}</div>
    <div class="a02-court"><h3>${esc(d.courtTitle)}</h3><p>${esc(d.courtLead)}</p><div class="a02-table"><table><thead><tr><th>${es?'Proposición':'Proposition'}</th><th>${es?'Resultado':'Outcome'}</th><th>${es?'Lectura controlada':'Controlled reading'}</th></tr></thead><tbody>${d.courtRows.map(r=>`<tr><td>${esc(r[0])}</td><td><span class="a02-status">${esc(r[1])}</span></td><td>${esc(r[2])}</td></tr>`).join('')}</tbody></table></div></div>
    <h3>${esc(d.tensionTitle)}</h3><div class="a02-tension">${d.tension}</div>
    <h3>${esc(d.distractTitle)}</h3><div class="a02-distract">${d.distract.map(x=>`<div class="a02-d"><strong>${esc(x[0])}</strong><p>${esc(x[1])}</p></div>`).join('')}</div>
    <h3>${esc(d.gradeTitle)}</h3><div class="a02-grade"><table><thead><tr><th>${es?'Proposición':'Proposition'}</th><th>${es?'Estado':'Status'}</th><th>${es?'Base':'Basis'}</th></tr></thead><tbody>${d.grades.map(r=>`<tr><td>${esc(r[0])}</td><td><span class="a02-status">${esc(r[1])}</span></td><td>${esc(r[2])}</td></tr>`).join('')}</tbody></table></div>
    <div class="a02-quote">${esc(d.quote)}</div><p class="a02-note">${esc(d.note)}</p>
  </div>`;

  const anchor = document.querySelector('[data-cal-allegation01-20260816]') || document.querySelector('[data-calificacion-radical-20260816]');
  if (anchor) anchor.insertAdjacentElement('afterend', section);
  else (document.querySelector('.hero.cal-hero') || document.querySelector('main .hero'))?.insertAdjacentElement('afterend', section);
})();
