(() => {
  const path = location.pathname.replace(/\/index\.html$/, '/');
  const isEs = path.includes('/es/');
  const flagship = /caso-insignia-jv1260-2011-ap89-2014|flagship-case-jv1260-2011-ap89-2014/.test(path);
  const community = /comunidad-instrumentalizacion|community-instrumentalisation/.test(path);
  const relevant = flagship || community || /toma-control-sun-park-7-junio-2018|sun-park-takeover-7-june-2018|reconstruccion-unitaria-autoridades-publicas|public-authority-unitary-case-reconstruction/.test(path);
  if (!relevant) return;

  const correctCommunityPossessionLabel = main => {
    if (!community) return;
    const oldValues = new Set([
      'NO POSSESSION OR EVICTION ORDER IN CAM’S FAVOUR',
      "NO POSSESSION OR EVICTION ORDER IN CAM'S FAVOUR",
      'NINGÚN AUTO DE POSESIÓN O DESALOJO A FAVOR DE CAM'
    ]);
    const replacement = isEs
      ? 'NO SE HA LOCALIZADO AUTO QUE ENTREGARA A CAM LA POSESIÓN DEL CONJUNTO SUN PARK EL 7 DE JUNIO DE 2018'
      : 'NO ORDER HAS BEEN LOCATED DELIVERING CAM POSSESSION OF THE SUN PARK COMPLEX ON 7 JUNE 2018';
    for (const el of main.querySelectorAll('strong, b, h2, h3, h4, p, span, div')) {
      if (el.children.length) continue;
      if (oldValues.has(el.textContent.trim())) el.textContent = replacement;
    }
  };

  let attempts = 0;
  const apply = () => {
    const main = document.querySelector('main');
    if (!main) return;
    correctCommunityPossessionLabel(main);

    const reverse = document.getElementById('jv1260-reverse-engineering-17aug2026');
    if (!reverse) {
      if (attempts++ < 40) setTimeout(apply, 75);
      return;
    }

    if (flagship) {
      const cards = [...reverse.querySelectorAll('.jvre-card')];
      const hinge = cards.find(card => /bisagra de apelación|appellate hinge|28-may-2012: la capacidad|28-May-2012: capacity/i.test(card.textContent));
      if (hinge) {
        hinge.innerHTML = isEs ? `
          <span class="jvre-status open">DECLARACIÓN DIRECTA · CORROBORACIÓN PRIMARIA P1</span>
          <h3>28-may-2012: Gil Marer afirma que entregó personalmente las copias como Presidente de CEXP</h3>
          <p><strong>Declaración de testigo directo:</strong> Gil Marer afirma que, poco después de incorporarse al hotel y asumir la Presidencia de CEXP, acudieron al complejo personas del o por cuenta del juzgado local acompañadas de un notario. Le mostraron documentación indicando que tenían derecho a recibir las llaves de las habitaciones afectadas. Gil afirma que obtuvo las copias y las entregó personalmente, como Presidente de CEXP, en simple cumplimiento de la orden/situación judicial. No atribuye al acto ningún significado adicional de entrega de posesión por Monterecco ni de reconocimiento de explotación turística por Monterecco.</p>
          <p><strong>Naturaleza de las llaves:</strong> la evidencia contemporánea controlada las describe como copias de mantenimiento de CEXP. En un complejo hotelero con apartamentos verticalmente interdependientes, una fuga de agua en una unidad superior puede afectar a la inferior o al bloque. Por ello, incluso una unidad cerrada y no utilizada por el hotel podía requerir acceso de mantenimiento para evitar daños a otras fincas e instalaciones. La tenencia de una copia para mantenimiento no equivale por sí sola a explotación turística o posesión jurídica de la unidad.</p>
          <p><strong>Contraste conservado:</strong> una comunicación privada contemporánea bajo custodia refiere que un vigilante realizaría la entrega. Esa fuente contraria debe reconciliarse; no elimina ni sustituye la declaración personal de Gil sobre un acto que afirma haber realizado él mismo.</p>
          <p><strong>Control primario:</strong> acta notarial completa + recibí firmado + relación llave/unidad + asistentes/capacidades + cualquier registro de entrega material.</p>` : `
          <span class="jvre-status open">DIRECT WITNESS STATEMENT · P1 PRIMARY CORROBORATION</span>
          <h3>28-May-2012: Gil Marer states that he personally handed over the copies as CEXP President</h3>
          <p><strong>Direct witness statement:</strong> Gil Marer states that, shortly after becoming involved at the hotel and assuming the CEXP Presidency, persons from or on behalf of the local court attended the complex with a notary. They showed papers indicating entitlement to receive the keys for the affected rooms. Gil states that he obtained the copies and personally handed them over, as President of CEXP, in straightforward compliance with the court-imposed position. He does not attribute to that act any additional meaning of Monterecco delivering possession or admitting tourist operation by Monterecco.</p>
          <p><strong>Nature of the keys:</strong> controlled contemporaneous evidence describes them as CEXP maintenance copies. In a hotel complex with vertically interdependent units, a water leak in an upper unit can damage the unit below or the wider block. Even a locked unit not being used by the hotel could therefore require maintenance access to prevent damage to other properties and infrastructure. Holding a maintenance copy does not by itself establish tourist operation or legal possession of that unit.</p>
          <p><strong>Contrary source preserved:</strong> a contemporaneous private communication under custody refers to a security guard making the delivery. That contrary source must be reconciled; it does not erase or replace Gil's first-hand statement about an act he says he personally performed.</p>
          <p><strong>Primary control:</strong> full notarial act + signed receipt + key/unit schedule + attendees/capacities + any physical-delivery record.</p>`;
      }

      if (!document.getElementById('jv1260-show-documentary-bridge')) {
        const bridge = document.createElement('article');
        bridge.id = 'jv1260-show-documentary-bridge';
        bridge.className = 'jvre-card jvre-cam';
        bridge.innerHTML = isEs ? `
          <span class="jvre-status open">PRUEBA DECISIVA · PRODUZCA EL PUENTE</span>
          <h3>CEXP → Monterecco: ¿qué documento primario convierte una devolución de mantenimiento en posesión de Monterecco?</h3>
          <p>La secuencia controlada contiene tres puntos que no deben comprimirse: <strong>primera instancia no encontró prueba suficiente de posesión/explotación por Monterecco</strong>; el registro contemporáneo identifica <strong>copias de mantenimiento de CEXP</strong>; y la Audiencia atribuyó relevancia al hecho posterior de 28-may-2012. La cuestión de máxima carga probatoria es el puente entre esos puntos.</p>
          <ul><li>Acta notarial íntegra y asistentes con su capacidad.</li><li>Recibí firmado y tabla exacta de llaves, apartamentos y fincas.</li><li>Escrito de aportación de nueva prueba, admisión y oposición.</li><li>Cualquier registro separado que acredite posesión, aceptación, control o entrega por Monterecco en capacidad propia.</li><li>Proposición exacta que la AP extrajo del hecho de 28-may-2012.</li></ul>
          <p><strong>Regla:</strong> si ese puente existe, debe incorporarse. Si no existe, la inferencia debe explicarse sin convertir CEXP y Monterecco en una sola entidad retrospectivamente.</p>` : `
          <span class="jvre-status open">DECISIVE EVIDENCE · SHOW THE BRIDGE</span>
          <h3>CEXP → Monterecco: which primary document converts a maintenance-key return into Monterecco possession?</h3>
          <p>The controlled sequence contains three points that must not be compressed: <strong>first instance found insufficient proof of possession/operation by Monterecco</strong>; the contemporaneous record identifies <strong>CEXP maintenance copies</strong>; and the Provincial Court gave significance to the later 28-May-2012 event. The highest-burden question is the documentary bridge between those points.</p>
          <ul><li>Full notarial act and attendees with their capacities.</li><li>Signed receipt and exact key/apartment/property schedule.</li><li>New-evidence filing, admission decision and opposition.</li><li>Any separate record proving possession, acceptance, control or delivery by Monterecco in its own capacity.</li><li>The exact proposition the Provincial Court drew from the 28-May-2012 event.</li></ul>
          <p><strong>Rule:</strong> if that bridge exists, it belongs in the record. If it does not, the inference must be explained without retrospectively collapsing CEXP and Monterecco into one entity.</p>`;
        if (hinge) hinge.insertAdjacentElement('afterend', bridge);
        else reverse.querySelector('.jvre-grid')?.appendChild(bridge);
      }

      const warning = reverse.querySelector('.jvre-warning');
      if (warning) warning.innerHTML = isEs
        ? '<strong>Grado penal/procesal actual:</strong> la declaración directa de Gil sobre su propia entrega se conserva como evidencia testimonial de primera mano; la comunicación contemporánea discordante se conserva como contraevidencia. La pregunta jurídica más fuerte sigue siendo una posible <strong>sobrelectura de un acto de cumplimiento de CEXP y de copias de mantenimiento como prueba de posesión de Monterecco</strong>. No es una conclusión de fraude. La fuente notarial y el recibí deben resolver el contraste factual y delimitar exactamente el acto.'
        : '<strong>Current criminal/procedural grade:</strong> Gil’s direct statement about his own delivery is preserved as first-hand witness evidence; the inconsistent contemporaneous communication is preserved as counterevidence. The strongest legal question remains a possible <strong>over-reading of a CEXP compliance event and maintenance copies as proof of Monterecco possession</strong>. This is not a fraud finding. The notarial source and receipt should resolve the factual contrast and define the act precisely.';
    } else {
      const prior = reverse.querySelector('[data-jv1260-21aug-correction]');
      if (prior) prior.remove();
      if (!reverse.querySelector('[data-jv1260-direct-witness-21aug]')) {
        const head = reverse.querySelector('.jvre-head');
        if (head) {
          const note = document.createElement('div');
          note.className = 'jvre-warning';
          note.dataset.jv1260DirectWitness21aug = 'true';
          note.innerHTML = isEs
            ? '<strong>Declaración directa · 21 ago 2026:</strong> Gil Marer afirma que él mismo entregó personalmente las copias de llaves, como Presidente de CEXP, cuando acudieron al hotel personas del o por cuenta del juzgado acompañadas de un notario y mostraron la documentación correspondiente. Describe el acto como simple cumplimiento. Las llaves se mantienen caracterizadas como copias de mantenimiento necesarias, entre otros motivos, para intervenir ante fugas o incidencias entre unidades interdependientes. Una comunicación contemporánea discordante se conserva como contraevidencia y debe reconciliarse con el acta notarial y el recibí; no sustituye la declaración de testigo directo.'
            : '<strong>Direct witness statement · 21 Aug 2026:</strong> Gil Marer states that he personally handed over the key copies, as CEXP President, when persons from or on behalf of the court attended the hotel with a notary and showed the relevant papers. He describes the act as straightforward compliance. The keys remain characterised as maintenance copies needed, among other things, to deal with leaks or incidents between interdependent units. An inconsistent contemporaneous communication is preserved as counterevidence and must be reconciled with the notarial act and receipt; it does not replace the direct witness statement.';
          head.appendChild(note);
        }
      }
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', apply, { once: true });
  else apply();
})();
