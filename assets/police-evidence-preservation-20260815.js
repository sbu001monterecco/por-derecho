(() => {
  const run = () => {
    const lang = document.documentElement.lang === 'en' ? 'en' : 'es';
    if (document.getElementById('police-evidence-preservation-20260815')) return;

    const groups = Array.from(document.querySelectorAll('.authority-directory-group'));
    if (!groups.length) return;

    const policeGroup = groups.find((group) => {
      const text = group.textContent || '';
      return /Guardia Civil\s*[—-]\s*Puesto Principal de Yaiza/i.test(text) ||
        /Fiscal[ií]a, polic[ií]a y preservaci[oó]n de prueba/i.test(text) ||
        /prosecution, police and evidence preservation/i.test(text);
    });

    // Make the national police body explicit for ordinary readers and search engines.
    document.querySelectorAll('.authority-directory li').forEach((li) => {
      const text = (li.textContent || '').trim();
      if (/Comisar[ií]a Provincial de Las Palmas/i.test(text)) {
        const name = li.querySelector('span:not(.mini-tile)');
        if (name && !/Polic[ií]a Nacional/i.test(name.textContent)) {
          name.textContent = lang === 'es'
            ? 'Policía Nacional — Comisaría Provincial de Las Palmas'
            : 'Policía Nacional (National Police) — Comisaría Provincial de Las Palmas';
        }
        li.dataset.search = `${li.dataset.search || ''} policía nacional national police comisaría provincial de las palmas`;
      }
    });

    // Correct the taxonomy: the Guardia Civil command belongs with police/evidence preservation,
    // not with registries/professional supervision.
    const commandLi = Array.from(document.querySelectorAll('.authority-directory li')).find((li) =>
      /Comandancia de Las Palmas/i.test(li.textContent || '')
    );
    if (policeGroup && commandLi && !policeGroup.contains(commandLi)) {
      const list = policeGroup.querySelector('ul');
      if (list) list.appendChild(commandLi);
    }

    const map = document.querySelector('#mapa-institucional') || document.querySelector('#institutional-map');
    const scope = map || document.querySelector('.authority-directory')?.closest('section') || document.querySelector('.authority-directory')?.parentElement;
    if (!scope) return;

    const anchor = scope.querySelector('.institutional-demand') || scope.querySelector('.directory-head') || scope.querySelector('.authority-directory');
    if (!anchor) return;

    const block = document.createElement('section');
    block.id = 'police-evidence-preservation-20260815';
    block.style.margin = '2rem 0';

    const es = `
      <div class="section-head">
        <div><p class="kicker">Fuerzas y Cuerpos de Seguridad del Estado · enero 2026</p><h3>Denuncias y preservación probatoria: qué consta y qué sigue sin constar</h3></div>
        <p>Los registros acreditan presentaciones y su estado registral. «Recibido» no acredita aceptación de las alegaciones, apertura de investigación, asignación a una unidad, adopción de medidas probatorias ni atribución de responsabilidad penal.</p>
      </div>
      <div class="authority-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1rem">
        <article class="authority-card" data-effect="pending" data-search="guardia civil comandancia las palmas denuncia penal preservación probatoria delitos económicos sun park">
          <header><span class="authority-tile" aria-hidden="true">GC</span><div><h4>Guardia Civil — Comandancia de Las Palmas</h4><p>Denuncias penales y solicitudes de preservación probatoria</p></div></header>
          <dl>
            <div><dt>Lo que consta</dt><dd>Entre el 4 y el 17 de enero de 2026 constan 10 presentaciones dirigidas a la Comandancia de Las Palmas y las 10 figuran como <strong>recibidas</strong>. Los asuntos incluyen denuncia penal, posible falsedad documental y estafa, explotación económica, delitos económicos complejos, Concurso 36/2012, comercialización Sun Park/Club Sei, Sun Park/RIC y solicitudes urgentes de preservación o aseguramiento probatorio.</dd></div>
            <div><dt>No acredita</dt><dd>La recepción registral no demuestra que la Guardia Civil aceptara los hechos denunciados, abriera diligencias, preservara prueba, asignara una unidad investigadora o atribuyera responsabilidad penal.</dd></div>
            <div><dt>Acción pendiente</dt><dd>Identificar qué unidad recibió o tramitó el material, si existe número de diligencias o referencia policial, qué valoración se hizo, qué preservación se acordó —si alguna— y si hubo remisión a Fiscalía o al órgano judicial competente.</dd></div>
          </dl>
          <footer><span>10 registros · 10 recibidos · 4–17 ene 2026</span><strong>Recepción documentada; actuación posterior por verificar</strong></footer>
        </article>
        <article class="authority-card" data-effect="pending" data-search="policía nacional comisaría provincial las palmas denuncia penal preservación probatoria delitos económicos sun park">
          <header><span class="authority-tile" aria-hidden="true">PN</span><div><h4>Policía Nacional — Comisaría Provincial de Las Palmas</h4><p>Denuncias penales y solicitudes de preservación probatoria</p></div></header>
          <dl>
            <div><dt>Lo que consta</dt><dd>Entre el 4 y el 16 de enero de 2026 constan 8 presentaciones dirigidas a la Comisaría Provincial de Las Palmas: <strong>4 figuran como recibidas y 4 como rechazadas</strong>. Las recibidas incluyen una puesta en conocimiento por posibles falsedad documental y fraude económico, una denuncia penal sobre explotación económica continuada, una denuncia penal y preservación probatoria por delitos económicos complejos y una solicitud urgente de actuaciones policiales y preservación probatoria.</dd></div>
            <div><dt>No acredita</dt><dd>La recepción registral no demuestra aceptación de las alegaciones, apertura de investigación, asignación a una unidad especializada, preservación efectiva de prueba ni atribución de responsabilidad penal. Los rechazos se publican como parte del rastro completo.</dd></div>
            <div><dt>Acción pendiente</dt><dd>Determinar qué ocurrió tras las cuatro recepciones: asignación, evaluación, referencia policial, preservación, traslado a Fiscalía o juzgado, archivo u otra actuación documentable.</dd></div>
          </dl>
          <footer><span>8 registros · 4 recibidos / 4 rechazados · 4–16 ene 2026</span><strong>Recepción parcial documentada; actuación posterior por verificar</strong></footer>
        </article>
      </div>
      <aside class="institutional-demand" style="margin-top:1rem"><strong>La pregunta verificable</strong><p>Tras una secuencia concentrada de denuncias y solicitudes expresas de preservación probatoria, ¿qué órgano o unidad recibió materialmente cada expediente, qué evaluación realizó y qué actuación posterior —si alguna— quedó documentada?</p></aside>
    `;

    const en = `
      <div class="section-head">
        <div><p class="kicker">State Security Forces · January 2026</p><h3>Criminal complaints and evidence preservation: what the record proves, and what it does not</h3></div>
        <p>The registration records prove submissions and their recorded status. “Received” does not prove acceptance of the allegations, the opening of an investigation, assignment to a police unit, preservation measures or attribution of criminal responsibility.</p>
      </div>
      <div class="authority-grid" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1rem">
        <article class="authority-card" data-effect="pending" data-search="guardia civil comandancia las palmas criminal complaint evidence preservation economic offences sun park">
          <header><span class="authority-tile" aria-hidden="true">GC</span><div><h4>Guardia Civil — Las Palmas Command</h4><p>Criminal complaints and evidence-preservation requests</p></div></header>
          <dl>
            <div><dt>What is documented</dt><dd>From 4 to 17 January 2026, 10 submissions were addressed to the Comandancia de Las Palmas and all 10 are recorded as <strong>received</strong>. Subjects include criminal complaints, possible documentary falsification and fraud, economic exploitation, complex economic offences, Concurso 36/2012, Sun Park/Club Sei marketing, Sun Park/RIC, and urgent evidence-preservation or securing requests.</dd></div>
            <div><dt>What this does not prove</dt><dd>Recorded receipt does not show that Guardia Civil accepted the allegations, opened proceedings, preserved evidence, assigned an investigating unit or attributed criminal responsibility.</dd></div>
            <div><dt>Outstanding action</dt><dd>Identify the unit that received or processed the material, any police reference or proceedings number, the assessment made, any preservation step actually ordered, and any referral to prosecutors or the competent court.</dd></div>
          </dl>
          <footer><span>10 records · 10 received · 4–17 Jan 2026</span><strong>Receipt documented; subsequent action to be verified</strong></footer>
        </article>
        <article class="authority-card" data-effect="pending" data-search="policía nacional national police comisaría provincial las palmas criminal complaint evidence preservation economic offences sun park">
          <header><span class="authority-tile" aria-hidden="true">PN</span><div><h4>Policía Nacional — Las Palmas Provincial Police Station</h4><p>Criminal complaints and evidence-preservation requests</p></div></header>
          <dl>
            <div><dt>What is documented</dt><dd>From 4 to 16 January 2026, 8 submissions were addressed to the Comisaría Provincial de Las Palmas: <strong>4 are recorded as received and 4 as rejected</strong>. The received items include a notification concerning possible documentary falsification and economic fraud, a criminal complaint concerning continued economic exploitation, a criminal complaint and evidence-preservation request concerning complex economic offences, and an urgent request for police action and evidence preservation.</dd></div>
            <div><dt>What this does not prove</dt><dd>Recorded receipt does not show acceptance of the allegations, the opening of an investigation, assignment to a specialist unit, actual preservation of evidence or attribution of criminal responsibility. The rejected submissions remain disclosed as part of the complete trail.</dd></div>
            <div><dt>Outstanding action</dt><dd>Determine what followed the four recorded receipts: allocation, assessment, police reference, preservation, referral to prosecutors or court, closure, or another documented step.</dd></div>
          </dl>
          <footer><span>8 records · 4 received / 4 rejected · 4–16 Jan 2026</span><strong>Partial receipt documented; subsequent action to be verified</strong></footer>
        </article>
      </div>
      <aside class="institutional-demand" style="margin-top:1rem"><strong>The verifiable question</strong><p>After this concentrated sequence of criminal complaints and express evidence-preservation requests, which body or unit actually received each file, what assessment was made, and what subsequent action — if any — was documented?</p></aside>
    `;

    block.innerHTML = lang === 'es' ? es : en;
    anchor.insertAdjacentElement('beforebegin', block);
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run, { once: true });
  else run();
})();
