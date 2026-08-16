(() => {
  const path = window.location.pathname.replace(/\/+$/, '') + '/';
  const es = path.endsWith('/es/calificacion-concurso-36-2012-vidas-paralelas/');
  const en = path.endsWith('/en/insolvency-classification-parallel-lives/');
  if (!es && !en) return;

  const old = document.querySelector('[data-cal-allegation04-20260816]');
  if (old) old.remove();
  if (document.querySelector('[data-cal-allegation04-corrected-20260816]')) return;

  const d = es ? {
    eyebrow: 'AUDITORÍA PROFUNDA · ALEGACIÓN 04 · CORRECCIÓN CLS / BDO',
    title: 'La sentencia dice que no se entregó el Libro Diario; el archivo contemporáneo contiene prueba concreta en sentido contrario',
    lead: 'No adoptamos como hecho objetivo la afirmación de Sentencia 163/2023 de que el Libro Diario no fue facilitado a la AC. Es un pronunciamiento adverso de primera instancia, recurrido, y debe confrontarse con la documentación contemporánea de Jonathan Simó/CLS y BDO.',
    points: [
      ['Entrega inicial', 'La propia AC reconoce que recibió diarios contables y balances 2008–2012. El expediente conserva además un documento de calificación titulado “documentación y cuentas 2008-12 entregados”.'],
      ['Diario 2015', 'Una transmisión de Jonathan Simó/CLS de junio de 2015 enumera expresamente un archivo “DIARIO Luchy 2015.xlsx”.'],
      ['BDO', 'La misma transmisión dice que los impuestos se preparaban sobre Cuentas Anuales elaboradas por BDO para 2011, 2012 y 2013, con resumen de 2014.'],
      ['CLS ↔ BDO', 'Existe correspondencia profesional directa de junio de 2015 entre Jonathan Simó/CLS y BDO sobre la revisión de las cuentas anuales de LPB.'],
      ['Cuentas 2012–2014', 'Drive conserva un expediente específico “Cuentas Anuales LPB 2012-2014” y documentación BDO de mayo de 2015.']
    ],
    courtTitle: 'Qué queda adverso',
    court: 'La sentencia sí afirma que el Libro Diario no fue facilitado y sobre esa premisa declara incumplimiento sustancial del art. 164.2.1 LC. Esa conclusión está recurrida. Por Derecho no la transforma en un hecho histórico neutral: la trata como una conclusión judicial controvertida que debe verificarse contra los archivos y envíos contemporáneos.',
    testTitle: 'La prueba que decide el punto',
    test: 'Año → archivo/libro Diario exacto → profesional custodio → fecha → formato → legalización si procedía → envío a la AC → destinatario → acuse/recepción → uso posterior por la AC → incorporación a la pieza de calificación. Si esa cadena confirma entrega, la premisa fáctica de primera instancia quedaría contradicha por documentación primaria.',
    quote: '“No es una discusión abstracta sobre si había contabilidad. Hay archivos, profesionales, correos y revisiones concretas. La pregunta es si el tribunal afirmó una no-entrega que el expediente documental puede demostrar que sí ocurrió.”',
    source: 'Control interno: CALIFICACION_ALLEGATION_04_JONATHAN_CLS_BDO_SOURCE_CORRECTION_16AUG2026.md. Fuentes reabiertas: Jonathan Simó/CLS, correspondencia BDO y expediente de cuentas LPB 2012–2014.'
  } : {
    eyebrow: 'DEEP AUDIT · ALLEGATION 04 · CLS / BDO CORRECTION',
    title: 'The judgment says the Daily Journal was not supplied; the contemporaneous record contains concrete evidence pointing the other way',
    lead: 'We do not adopt Judgment 163/2023’s statement that the Daily Journal was not supplied to the AC as objective historical fact. It is an adverse first-instance finding under appeal and must be tested against the contemporaneous Jonathan Simó/CLS and BDO record.',
    points: [
      ['Initial delivery', 'The AC itself acknowledges receiving accounting journals and trial balances for 2008–2012. The classification evidence file also preserves a document titled “documentation and accounts 2008-12 delivered”.'],
      ['2015 Journal', 'A June-2015 Jonathan Simó/CLS transmission expressly lists a “DIARIO Luchy 2015.xlsx” file.'],
      ['BDO', 'The same transmission says corporate-tax work was prepared from annual accounts produced by BDO for 2011, 2012 and 2013, with a 2014 summary available.'],
      ['CLS ↔ BDO', 'Direct June-2015 professional correspondence exists between Jonathan Simó/CLS and BDO concerning review of LPB annual accounts.'],
      ['2012–2014 accounts', 'Drive preserves a dedicated “LPB Annual Accounts 2012-2014” correspondence file and BDO material from May 2015.']
    ],
    courtTitle: 'What remains adverse',
    court: 'The judgment does state that the Daily Journal was not supplied and relies on that premise to uphold the Art. 164.2.1 substantial-breach ground. That finding is appealed. Por Derecho does not convert it into a neutral historical fact; it is a disputed judicial conclusion to be checked against the contemporaneous files and transmissions.',
    testTitle: 'The evidence that decides the point',
    test: 'Year → exact Daily Journal file/book → professional custodian → date → format → legalisation if applicable → transmission to AC → recipient → acknowledgement/receipt → later AC use → incorporation into the classification record. If that chain confirms delivery, the first-instance factual premise would be contradicted by primary documentary evidence.',
    quote: '“This is not an abstract debate about whether accounting existed. There are concrete files, professionals, emails and reviews. The question is whether the court found non-delivery where the documentary record can prove delivery actually occurred.”',
    source: 'Internal control: CALIFICACION_ALLEGATION_04_JONATHAN_CLS_BDO_SOURCE_CORRECTION_16AUG2026.md. Re-opened sources: Jonathan Simó/CLS, BDO correspondence and LPB 2012–2014 accounts file.'
  };

  const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
  const section = document.createElement('section');
  section.setAttribute('data-cal-allegation04-corrected-20260816','');
  section.className = 'section';
  section.innerHTML = `<div class="shell"><div class="section-head"><div><p class="kicker">${esc(d.eyebrow)}</p><h2>${esc(d.title)}</h2></div><p>${esc(d.lead)}</p></div><div class="grid-2">${d.points.map(x=>`<article class="path-card"><h3>${esc(x[0])}</h3><p>${esc(x[1])}</p></article>`).join('')}</div><article class="chain-conclusion"><h2>${esc(d.courtTitle)}</h2><p>${esc(d.court)}</p></article><aside class="pressure-maxim"><strong>${esc(d.testTitle)}</strong><span>${esc(d.test)}</span></aside><blockquote>${esc(d.quote)}</blockquote><p class="source-policy">${esc(d.source)}</p></div>`;
  const anchor = document.querySelector('[data-cal-allegation03-unitary-community-ac-causation-20260816]') || document.querySelector('[data-cal-allegation03-20260816]') || document.querySelector('[data-cal-allegation02-20260816]');
  if (anchor) anchor.insertAdjacentElement('afterend', section);
  else (document.querySelector('main .hero') || document.querySelector('main'))?.insertAdjacentElement('afterend', section);
})();