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
      const hinge = cards.find(card => /bisagra de apelación|appellate hinge/i.test(card.textContent));
      if (hinge) {
        hinge.innerHTML = isEs ? `
          <span class="jvre-status open">P1 · CONTRASTE ABIERTO</span>
          <h3>28-may-2012: la capacidad está mucho más clara que la identidad del autor material</h3>
          <p>Los registros contemporáneos controlados describen la devolución como <strong>copias de llaves de mantenimiento de CEXP</strong>, en cumplimiento de una obligación atribuida a CEXP y no a Monterecco. Un registro privado contemporáneo bajo custodia entra en tensión con una memoria personal posterior sobre quién hizo físicamente la entrega. Por ello, Por Derecho no publica ahora como hecho cerrado que Gil Marer entregara personalmente las llaves.</p>
          <p><strong>Lo que permanece fuertemente apoyado:</strong> la separación de capacidad CEXP ≠ Monterecco. <strong>Lo que permanece abierto:</strong> quién realizó la entrega material, en qué capacidad y qué quedó exactamente documentado el 28-may-2012.</p>
          <p><strong>Control primario:</strong> acta notarial completa + recibí firmado + relación llave/unidad + asistentes/capacidades.</p>` : `
          <span class="jvre-status open">P1 · OPEN CONTRAST</span>
          <h3>28-May-2012: capacity is much clearer than the identity of the physical deliverer</h3>
          <p>Controlled contemporaneous records describe the return as <strong>CEXP maintenance-key copies</strong>, under an obligation attributed to CEXP rather than Monterecco. A contemporaneous private-source record under custody conflicts with a later personal recollection about who physically handed the keys over. Por Derecho therefore does not now publish as settled fact that Gil Marer personally delivered the keys.</p>
          <p><strong>What remains strongly supported:</strong> the CEXP ≠ Monterecco capacity separation. <strong>What remains open:</strong> who physically delivered the keys, in what capacity, and exactly what the 28-May-2012 record documented.</p>
          <p><strong>Primary control:</strong> full notarial act + signed receipt + key/unit schedule + attendees/capacities.</p>`;
      }

      if (!document.getElementById('jv1260-show-documentary-bridge')) {
        const bridge = document.createElement('article');
        bridge.id = 'jv1260-show-documentary-bridge';
        bridge.className = 'jvre-card jvre-cam';
        bridge.innerHTML = isEs ? `
          <span class="jvre-status open">PRUEBA DECISIVA · PRODUZCA EL PUENTE</span>
          <h3>CEXP → Monterecco: ¿qué documento primario convierte una devolución de mantenimiento en posesión de Monterecco?</h3>
          <p>La secuencia controlada contiene tres puntos que no deben comprimirse: <strong>primera instancia no encontró prueba suficiente de posesión/explotación por Monterecco</strong>; el registro contemporáneo identifica <strong>copias de mantenimiento de CEXP</strong>; y la Audiencia atribuyó relevancia al hecho posterior de 28-may-2012. La cuestión de máxima carga probatoria es el puente entre esos puntos.</p>
          <ul>
            <li>Acta notarial íntegra y asistentes con su capacidad.</li>
            <li>Recibí firmado y tabla exacta de llaves, apartamentos y fincas.</li>
            <li>Escrito de aportación de nueva prueba, admisión y oposición.</li>
            <li>Cualquier registro separado que acredite posesión, aceptación, control o entrega por Monterecco en capacidad propia.</li>
            <li>Proposición exacta que la AP extrajo del hecho de 28-may-2012.</li>
          </ul>
          <p><strong>Regla:</strong> si ese puente existe, debe incorporarse. Si no existe, la inferencia debe explicarse sin convertir CEXP y Monterecco en una sola entidad retrospectivamente.</p>` : `
          <span class="jvre-status open">DECISIVE EVIDENCE · SHOW THE BRIDGE</span>
          <h3>CEXP → Monterecco: which primary document converts a maintenance-key return into Monterecco possession?</h3>
          <p>The controlled sequence contains three points that must not be compressed: <strong>first instance found insufficient proof of possession/operation by Monterecco</strong>; the contemporaneous record identifies <strong>CEXP maintenance copies</strong>; and the Provincial Court gave significance to the later 28-May-2012 event. The highest-burden question is the documentary bridge between those points.</p>
          <ul>
            <li>Full notarial act and attendees with their capacities.</li>
            <li>Signed receipt and exact key/apartment/property schedule.</li>
            <li>New-evidence filing, admission decision and opposition.</li>
            <li>Any separate record proving possession, acceptance, control or delivery by Monterecco in its own capacity.</li>
            <li>The exact proposition the Provincial Court drew from the 28-May-2012 event.</li>
          </ul>
          <p><strong>Rule:</strong> if that bridge exists, it belongs in the record. If it does not, the inference must be explained without retrospectively collapsing CEXP and Monterecco into one entity.</p>`;
        if (hinge) hinge.insertAdjacentElement('afterend', bridge);
        else reverse.querySelector('.jvre-grid')?.appendChild(bridge);
      }

      const warning = reverse.querySelector('.jvre-warning');
      if (warning) {
        warning.innerHTML = isEs
          ? '<strong>Grado penal/procesal actual:</strong> la pregunta más fuerte es una posible <strong>sobrelectura de un acto de cumplimiento de CEXP como prueba de posesión de Monterecco</strong>. No es una conclusión de fraude. Maquinación fraudulenta, estafa procesal o falsedad exigen prueba actor-específica de representación, conocimiento, engaño u omisión material, error judicial causal, perjuicio e intención. La contradicción sobre quién hizo la entrega física se conserva como contradicción y debe resolverla la fuente primaria.'
          : '<strong>Current criminal/procedural grade:</strong> the strongest question is a possible <strong>over-reading of a CEXP compliance event as proof of Monterecco possession</strong>. It is not a fraud finding. Fraudulent contrivance, procedural fraud or document offences require actor-specific proof of representation, knowledge, material deception or omission, causative judicial error, prejudice and intent. The conflict over who physically delivered the keys is preserved as a conflict and must be resolved by the primary record.';
      }
    } else if (!reverse.querySelector('[data-jv1260-21aug-correction]')) {
      const head = reverse.querySelector('.jvre-head');
      if (head) {
        const note = document.createElement('div');
        note.className = 'jvre-warning';
        note.dataset.jv126021augCorrection = 'true';
        note.innerHTML = isEs
          ? '<strong>Corrección probatoria · 21 ago 2026:</strong> el registro contemporáneo apoya con fuerza que las llaves de 28-may-2012 eran copias de mantenimiento de CEXP y que la obligación correspondía a CEXP, no a Monterecco. La identidad de quien hizo la entrega material se mantiene abierta porque una fuente privada contemporánea entra en tensión con una memoria personal posterior. El acta notarial y el recibí firmado deben controlar.'
          : '<strong>Evidence correction · 21 Aug 2026:</strong> the contemporaneous record strongly supports that the 28-May-2012 keys were CEXP maintenance copies and that the obligation was CEXP’s, not Monterecco’s. The identity of the physical deliverer remains open because a contemporaneous private source conflicts with a later personal recollection. The notarial act and signed receipt must control.';
        head.appendChild(note);
      }
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', apply, { once: true });
  else apply();
})();
