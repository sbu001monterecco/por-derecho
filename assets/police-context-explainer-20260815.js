(() => {
  const run = () => {
    const lang = document.documentElement.lang === 'en' ? 'en' : 'es';
    const parent = document.getElementById('police-evidence-preservation-20260815');
    const drill = document.getElementById('police-regage-drilldown-20260815');
    if (!parent || !drill || document.getElementById('police-context-explainer-20260815')) return;
    const box = document.createElement('article');
    box.id = 'police-context-explainer-20260815';
    box.className = 'thesis-block';
    box.style.marginTop = '1.25rem';
    box.innerHTML = lang === 'es' ? `
      <h3>Qué se pidió · qué acredita el registro · qué no está todavía documentado</h3>
      <p><strong>Qué se pidió.</strong> Las comunicaciones de enero de 2026 no se limitaron a informar de un conflicto civil o concursal. Según sus asuntos registrales, se formularon denuncias o puestas en conocimiento de posibles hechos de relevancia penal y se solicitaron expresamente actuaciones de preservación o aseguramiento probatorio. Las materias comunicadas incluían, entre otras, posibles irregularidades documentales/falsedad, fraude económico, explotación económica continuada, delitos económicos complejos, contradicciones económicas vinculadas al Concurso 36/2012, material de marzo de 2018 y la posterior comercialización o financiación de Sun Park.</p>
      <p><strong>Qué acredita el registro.</strong> Acredita la presentación y el estado registral que se muestra: diez presentaciones dirigidas a la Comandancia de Las Palmas figuran como recibidas; de ocho dirigidas a la Comisaría Provincial de Las Palmas, cuatro figuran como recibidas y cuatro como rechazadas.</p>
      <p><strong>Qué no acredita.</strong> «Recibido» no significa que Guardia Civil o Policía Nacional hayan confirmado las alegaciones, apreciado delito, identificado responsables, abierto diligencias, asignado una unidad investigadora o ejecutado la preservación solicitada. «Rechazado» se trata aquí como estado registral/de tramitación y no como rechazo de fondo de los hechos denunciados, salvo que el documento de rechazo demuestre otra cosa.</p>
      <p><strong>Qué no está todavía evidenciado en el material publicado/revisado.</strong> No se ha identificado documentación suficiente para afirmar una unidad investigadora asignada, número de diligencias o referencia policial, atestado, requerimientos a terceros, declaraciones, preservación efectiva, remisión a Fiscalía/juzgado, archivo motivado u otra decisión policial de fondo.</p>
      <p><strong>Precisión esencial:</strong> la ausencia de documentación localizada sobre una actuación posterior no demuestra que esa actuación no ocurriera. La cuestión pendiente es documental y verificable: <em>¿qué ocurrió después de la recepción?</em></p>` : `
      <h3>What was requested · what the registry proves · what is not yet documented</h3>
      <p><strong>What was requested.</strong> The January 2026 communications were not merely notices of a civil or insolvency dispute. According to their registered subjects, criminal complaints or notifications of potentially criminal facts were submitted and police evidence-preservation or securing action was expressly requested. The communicated subjects included possible documentary irregularity/falsification, economic fraud, continued economic exploitation, complex economic offences, economic contradictions connected with Concurso 36/2012, March 2018 material, and later Sun Park commercialisation or financing.</p>
      <p><strong>What the registry proves.</strong> It proves submission and the displayed registration status: ten submissions addressed to the Guardia Civil Las Palmas Command are recorded as received; of eight addressed to the Policía Nacional Las Palmas Provincial Police Station, four are recorded as received and four as rejected.</p>
      <p><strong>What it does not prove.</strong> “Received” does not mean that Guardia Civil or Policía Nacional confirmed the allegations, found an offence, identified responsible persons, opened police proceedings, assigned an investigating unit or carried out the requested preservation. “Rejected” is treated here as a registration/processing status, not a merits rejection of the reported facts, unless the underlying rejection document establishes otherwise.</p>
      <p><strong>What is not yet evidenced in the published/reviewed material.</strong> No sufficient document has been identified to assert an assigned investigating unit, police proceedings/reference number, police report, third-party requests, interviews, actual preservation, referral to prosecutors/court, reasoned closure or another substantive police decision.</p>
      <p><strong>Essential qualification:</strong> absence of located documentation of subsequent action does not prove that no such action occurred. The outstanding question is documentary and verifiable: <em>what happened after receipt?</em></p>`;
    drill.insertAdjacentElement('beforebegin', box);
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, { once: true }); else run();
})();
