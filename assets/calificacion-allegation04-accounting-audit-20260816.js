(() => {
  const path = window.location.pathname.replace(/\/+$/, '') + '/';
  const es = path.endsWith('/es/calificacion-concurso-36-2012-vidas-paralelas/');
  const en = path.endsWith('/en/insolvency-classification-parallel-lives/');
  if (!es && !en) return;
  if (document.querySelector('[data-cal-allegation04-20260816]')) return;

  const d = es ? {
    eyebrow: 'AUDITORÍA PROFUNDA · ALEGACIÓN 04 · CONTABILIDAD · ART. 164.2.1 LC',
    title: 'No es “no había contabilidad”: el pronunciamiento adverso se concentra en el Libro Diario durante el concurso',
    lead: 'La propia AC reconoció que LPB siguió contabilizando en 2012 y que recibió diarios contables y balances de sumas y saldos de 2008–2012. La Sentencia 163/2023 descarta además que la mera falta de legalización anterior al concurso baste por sí sola. Pero mantiene un pronunciamiento adverso distinto: considera no aportado el Libro Diario estatutario durante el concurso. Ese pronunciamiento está recurrido.',
    splitTitle: 'Tres cuestiones distintas que no deben volver a fusionarse',
    split: [
      ['Material contable existente', 'VERIFICADO', 'La AC reconoce diarios y balances 2008–2012; la sentencia reconoce además balances de comprobación, estados y cuentas anuales posteriores.'],
      ['Libro Diario durante el concurso', 'ADVERSO · RECURRIDO', 'La sentencia considera que no quedó aportado el Libro Diario y trata esa ausencia como incumplimiento sustancial.'],
      ['Cuentas anuales / doble contabilidad', 'NO CONFUNDIR', 'La presunción separada por falta de formulación de cuentas anuales fue desestimada; no hay una conclusión probada de doble contabilidad o falsificación contable.']
    ],
    acTitle: 'Lo que la propia AC dejó escrito',
    ac: 'Su informe reproduce que “la sociedad ha seguido contabilizando” y que recibió en PDF diarios contables y balances de sumas y saldos de 2008, 2009, 2010, 2011 y parte de 2012. Por tanto, cualquier resumen que diga simplemente “LPB no llevaba contabilidad” borra una admisión documental central de la propia acusación.',
    courtTitle: 'Lo que realmente decidió Sentencia 163/2023',
    court: [
      'La mera falta de legalización de los libros anteriores al concurso no integra por sí sola la causa, salvo que impida comprender la situación patrimonial o financiera.',
      'El tribunal centra el análisis en el período del concurso.',
      'Reconoce balances de comprobación de 2013–2016, estados contables 2012–2016 y correos remitiendo cuentas anuales.',
      'Distingue esos materiales del Libro Diario exigido por el Código de Comercio y concluye que éste no quedó facilitado a la AC.',
      'Sobre esa falta concreta mantiene el incumplimiento sustancial; el pronunciamiento está recurrido.'
    ],
    tensionTitle: 'La contradicción que exige una auditoría documental, no un eslogan',
    tension: 'El mismo expediente permitió a la AC calcular patrimonio neto, ratios de liquidez y solvencia, créditos frente a terceros, inversiones y evolución financiera. Eso hace insostenible una narrativa de vacío contable absoluto. Pero tampoco demuestra por sí solo que el Diario obligatorio se llevara correctamente. La pregunta verificable es año por año: Diario existente → formato → legalización → envío → recepción AC → uso posterior → información que faltaba realmente.',
    collaborationTitle: 'La sentencia también separó contabilidad de colaboración',
    collaboration: 'Al estudiar la colaboración, el tribunal afirma que LPB entregó la documentación contable de la que disponía y no aprecia falta de colaboración por la mera entrega de contabilidad. Esa conclusión no elimina el fallo adverso del art. 164.2.1; confirma que “no llevar/probar el libro estatutario” y “negarse a entregar toda la contabilidad disponible” son proposiciones distintas.',
    gradeTitle: 'Graduación probatoria actual',
    grades: [
      ['“LPB no tenía contabilidad”', 'CONTRADICHO', 'La AC reconoce contabilidad continuada y entrega de diarios/balances.'],
      ['No legalización 2008–2011 = culpabilidad automática', 'NARROWED', 'La propia sentencia dice que la mera falta de legalización no basta.'],
      ['Material contable sustancial entregado', 'VERIFICADO', 'Informe AC + correos/adjuntos reproducidos en la oposición.'],
      ['Libro Diario completo durante el concurso', 'DISPUTADO', 'La sentencia dice que no se aportó; la apelación sostiene lo contrario.'],
      ['Incumplimiento sustancial art. 164.2.1', 'ADVERSO · RECURRIDO', 'Fundamento Quinto de Sentencia 163/2023.'],
      ['Presunción separada por cuentas anuales', 'DESESTIMADA', 'Fundamento Décimo.'],
      ['Doble contabilidad / falsificación', 'NO PROBADO', 'No es el hallazgo judicial que sostiene esta causa.'],
      ['AC inventó toda la causa contable', 'NO ESTABLECIDO', 'Existe un fallo adverso más estrecho; sí hay base fuerte para cuestionar la amplitud de su narrativa.']
    ],
    askTitle: 'Lo que resolvería la controversia',
    ask: 'Libro Diario 2012–2017; Libro de Inventarios y Cuentas Anuales; originales de los correos de Jonathan Simó y sus adjuntos; acuses de la AC; certificados del Registro Mercantil; auditorías posteriores; y audiovisual/transcripción íntegra de la vista de 25 de julio de 2023, especialmente la prueba de los profesionales contables.',
    quote: '“La cuestión ya no puede presentarse como ‘había o no había contabilidad’. La cuestión es qué libro estatutario existía, qué recibió la AC y qué información material no podía reconstruir con todo lo que sí tenía.”',
    source: 'Control interno: CALIFICACION_ALLEGATION_04_ACCOUNTING_BOOKS_SUBSTANTIAL_BREACH_LEDGER_16AUG2026.md. Sentencia 163/2023 sigue siendo materialmente adversa y está recurrida.'
  } : {
    eyebrow: 'DEEP AUDIT · ALLEGATION 04 · ACCOUNTING · ART. 164.2.1 LC',
    title: 'This is not “there were no accounts”: the adverse finding centres on the statutory Daily Journal during the insolvency',
    lead: 'The AC itself acknowledged that LPB continued accounting in 2012 and that it received accounting journals and trial balances for 2008–2012. Judgment 163/2023 also rejects mere pre-insolvency non-legalisation as sufficient by itself. It nevertheless makes a different adverse finding: the statutory Daily Journal was not established as supplied during the insolvency. That finding is on appeal.',
    splitTitle: 'Three different questions that must not be merged again',
    split: [
      ['Accounting material existed', 'VERIFIED', 'The AC acknowledges journals and balances for 2008–2012; the judgment also records later checking balances, statements and annual accounts.'],
      ['Daily Journal during insolvency', 'ADVERSE · APPEALED', 'The judgment holds that the statutory Daily Journal was not supplied and treats that absence as a substantial breach.'],
      ['Annual accounts / double accounting', 'KEEP SEPARATE', 'The separate annual-accounts presumption was dismissed; there is no proved double-accounting or falsified-accounting finding.']
    ],
    acTitle: 'What the AC itself recorded',
    ac: 'Its report reproduces that “the company continued accounting” and that PDF accounting journals and trial balances for 2008, 2009, 2010, 2011 and part of 2012 were received. Any summary saying simply “LPB kept no accounts” therefore erases a central documentary admission within the accusation itself.',
    courtTitle: 'What Judgment 163/2023 actually decided',
    court: [
      'Mere failure to legalise the pre-insolvency books does not by itself make out the ground unless it obstructs understanding of the patrimonial or financial position.',
      'The court focuses on the insolvency-period accounting.',
      'It records 2013–2016 checking balances, 2012–2016 accounting statements and emails sending annual accounts.',
      'It distinguishes those materials from the statutory Daily Journal required by the Commercial Code and holds that the Journal was not supplied to the AC.',
      'On that narrower basis it upholds the substantial-breach ground; the finding is appealed.'
    ],
    tensionTitle: 'The tension that requires a documentary audit, not a slogan',
    tension: 'The same record allowed the AC to calculate net equity, liquidity and solvency ratios, third-party receivables, investments and financial evolution. That makes an absolute “accounting vacuum” narrative untenable. But it does not itself prove that the mandatory Journal was properly kept. The reproducible question is year by year: Journal existed → format → legalisation → transmission → AC receipt → later use → what information was actually missing.',
    collaborationTitle: 'The judgment also separates accounting from cooperation',
    collaboration: 'When deciding cooperation, the court says LPB delivered the accounting documentation it possessed and does not find non-cooperation merely from delivery of accounting. That does not cancel the Art. 164.2.1 finding; it confirms that “failure to keep/prove a statutory book” and “refusal to deliver all accounting in one’s possession” are different propositions.',
    gradeTitle: 'Current evidential grading',
    grades: [
      ['“LPB had no accounting”', 'CONTRADICTED', 'The AC acknowledges continued accounting and delivery of journals/balances.'],
      ['Non-legalisation 2008–2011 = automatic culpability', 'NARROWED', 'The judgment itself says mere non-legalisation is insufficient.'],
      ['Substantial accounting material delivered', 'VERIFIED', 'AC report + emails/attachments reproduced in the opposition.'],
      ['Complete Daily Journal during insolvency', 'DISPUTED', 'Judgment says it was not supplied; appeal says otherwise.'],
      ['Art. 164.2.1 substantial breach', 'ADVERSE · APPEALED', 'Ground Five of Judgment 163/2023.'],
      ['Separate annual-accounts presumption', 'DISMISSED', 'Ground Ten.'],
      ['Double accounting / falsification', 'NOT PROVED', 'That is not the judicial finding sustaining this ground.'],
      ['AC invented the entire accounting case', 'NOT ESTABLISHED', 'A narrower adverse finding exists; there is strong basis to challenge the breadth of the narrative.']
    ],
    askTitle: 'What would resolve the dispute',
    ask: 'Daily Journals for 2012–2017; Inventory/Annual-Accounts books; original Jonathan Simó emails and attachments; AC acknowledgements; Mercantile Registry certificates; later audit files; and the complete audiovisual/transcript of the 25 July 2023 hearing, especially the accounting professionals’ evidence.',
    quote: '“The issue can no longer honestly be framed as ‘accounts or no accounts’. It is which statutory book existed, what the AC received, and what material information it could not reconstruct from everything it did have.”',
    source: 'Internal control: CALIFICACION_ALLEGATION_04_ACCOUNTING_BOOKS_SUBSTANTIAL_BREACH_LEDGER_16AUG2026.md. Judgment 163/2023 remains materially adverse and is on appeal.'
  };

  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
  const section = document.createElement('section');
  section.setAttribute('data-cal-allegation04-20260816','');
  section.className = 'section';
  section.innerHTML = `<div class="shell">
    <div class="section-head"><div><p class="kicker">${esc(d.eyebrow)}</p><h2>${esc(d.title)}</h2></div><p>${esc(d.lead)}</p></div>
    <h3>${esc(d.splitTitle)}</h3><div class="grid-3">${d.split.map(x=>`<article class="path-card"><span class="evidence-badge">${esc(x[1])}</span><h3>${esc(x[0])}</h3><p>${esc(x[2])}</p></article>`).join('')}</div>
    <article class="chain-conclusion"><h2>${esc(d.acTitle)}</h2><p>${esc(d.ac)}</p></article>
    <div class="grid-2"><article class="path-card primary"><h3>${esc(d.courtTitle)}</h3><ul>${d.court.map(x=>`<li>${esc(x)}</li>`).join('')}</ul></article><article class="path-card"><h3>${esc(d.tensionTitle)}</h3><p>${esc(d.tension)}</p></article></div>
    <article class="chain-conclusion"><h2>${esc(d.collaborationTitle)}</h2><p>${esc(d.collaboration)}</p></article>
    <h3>${esc(d.gradeTitle)}</h3><div class="control-table-wrap"><table class="control-table"><thead><tr><th>${es?'Proposición':'Proposition'}</th><th>${es?'Estado':'Status'}</th><th>${es?'Base':'Basis'}</th></tr></thead><tbody>${d.grades.map(x=>`<tr><td>${esc(x[0])}</td><td><strong>${esc(x[1])}</strong></td><td>${esc(x[2])}</td></tr>`).join('')}</tbody></table></div>
    <aside class="pressure-maxim"><strong>${esc(d.askTitle)}</strong><span>${esc(d.ask)}</span></aside>
    <blockquote>${esc(d.quote)}</blockquote><p class="source-policy">${esc(d.source)}</p>
  </div>`;

  const anchor = document.querySelector('[data-cal-allegation03-20260816]') || document.querySelector('[data-cal-allegation02-20260816]');
  if (anchor) anchor.insertAdjacentElement('afterend', section);
  else (document.querySelector('main .hero') || document.querySelector('main'))?.insertAdjacentElement('afterend', section);
})();