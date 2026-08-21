(() => {
  const path = location.pathname.replace(/\/index\.html$/, '/');
  const isEs = path.includes('/es/');
  const relevant = /caso-insignia-jv1260-2011-ap89-2014|flagship-case-jv1260-2011-ap89-2014|comunidad-instrumentalizacion|community-instrumentalisation|toma-control-sun-park-7-junio-2018|sun-park-takeover-7-june-2018|reconstruccion-unitaria-autoridades-publicas|public-authority-unitary-case-reconstruction/.test(path);
  if (!relevant) return;

  let tries = 0;
  const apply = () => {
    const reverse = document.getElementById('jv1260-reverse-engineering-17aug2026');
    if (!reverse) {
      if (tries++ < 50) setTimeout(apply, 75);
      return;
    }

    const cards = [...reverse.querySelectorAll('.jvre-card')];
    const hinge = cards.find(card => /28-may-2012|28-may-2012|28 mayo 2012|28-may/i.test(card.textContent) && /gil marer|capacidad|capacity|llaves|keys/i.test(card.textContent));
    if (hinge) {
      hinge.innerHTML = isEs ? `
        <span class="jvre-status open">RECUERDO DISCUTIDO · CONFLICTO CON FUENTE CONTEMPORÁNEA · MANDA EL ACTA PRIMARIA</span>
        <h3>28-may-2012: CEXP y las copias de mantenimiento están sólidamente apoyados; el entregante material sigue sin resolver</h3>
        <p><strong>Corrección de fuente:</strong> el recuerdo posterior de Gil de haber realizado personalmente la entrega no puede publicarse como hecho establecido. Un correo contemporáneo de 28-may-2012, escrito antes de la hora prevista, afirma que Gil ya había salido de Lanzarote y que un vigilante realizaría la entrega. Existe por tanto un conflicto material de fuente.</p>
        <p><strong>Lo que sí queda reforzado:</strong> correspondencia contemporánea privada de mayo de 2012 identifica a <strong>CEXP —no Monterecco—</strong> como la entidad obligada a devolver las copias y caracteriza esas llaves como <strong>copias de mantenimiento</strong>. También se contempló que la procuradora CEXP hiciera la entrega material si Gil/Patricia no la realizaban.</p>
        <p><strong>Regla probatoria:</strong> ni el recuerdo posterior ni el correo de planificación prueban por sí solos quién ejecutó finalmente la entrega. La identidad del entregante, asistentes y capacidades debe fijarse por el <strong>recibí firmado, acta notarial íntegra, relación llave/unidad y registro judicial</strong>.</p>
        <p><strong>Frontera de entidad:</strong> la incertidumbre sobre la persona que entregó físicamente las llaves no convierte el acto de CEXP en un acto de Monterecco ni prueba posesión de Monterecco. Ese puente requiere prueba separada.</p>
        <p><strong>Privacidad/privilegio:</strong> la correspondencia letrada privada se utiliza como mapa de evidencia y control de contradicción; la publicación debe apoyarse preferentemente en los originales notariales y judiciales no privilegiados.</p>` : `
        <span class="jvre-status open">DISPUTED RECOLLECTION · CONTEMPORANEOUS SOURCE CONFLICT · PRIMARY ACT CONTROLS</span>
        <h3>28-May-2012: CEXP and maintenance copies are strongly supported; the physical deliverer remains unresolved</h3>
        <p><strong>Source-status correction:</strong> Gil's later recollection that he personally performed the delivery cannot be published as established fact. A contemporaneous 28-May-2012 email written before the scheduled delivery states that Gil had already left Lanzarote and that a security guard would make the delivery. There is therefore a material source conflict.</p>
        <p><strong>What is strengthened:</strong> contemporaneous private May-2012 correspondence identifies <strong>CEXP —not Monterecco—</strong> as the entity obliged to return the copies and characterises the keys as <strong>maintenance copies</strong>. It also contemplated the CEXP procuradora performing material delivery if Gil/Patricia did not.</p>
        <p><strong>Evidential rule:</strong> neither the later recollection nor a planning email by itself proves who ultimately performed the handover. The deliverer's identity, attendees and capacities must be fixed by the <strong>signed receipt, complete notarial act, key/unit schedule and court record</strong>.</p>
        <p><strong>Entity boundary:</strong> uncertainty over the natural person who physically handed over the keys does not turn the CEXP event into a Monterecco act or prove Monterecco possession. That bridge requires separate evidence.</p>
        <p><strong>Privilege/privacy:</strong> private legal correspondence is used as an evidence map and contradiction control; public proof should preferably rest on non-privileged notarial and court originals.</p>`;
    }

    const oldExpanded = reverse.querySelector('[data-jv1260-direct-witness-expanded-21aug]');
    if (oldExpanded) {
      oldExpanded.innerHTML = isEs
        ? '<strong>Corrección de fuente · 21 ago 2026:</strong> el recuerdo posterior de entrega personal está materialmente contradicho por un correo contemporáneo del 28-may-2012 que dice que Gil ya había salido de Lanzarote y que un vigilante haría la entrega. La persona que finalmente entregó las llaves queda abierta hasta obtener recibí y acta notarial. Se mantiene, con apoyo contemporáneo fuerte, que la obligación correspondía a CEXP —no Monterecco— y que se trataba de copias de mantenimiento.'
        : '<strong>Source-status correction · 21 Aug 2026:</strong> the later recollection of personal delivery is materially inconsistent with a contemporaneous 28-May-2012 email stating that Gil had already left Lanzarote and that a security guard would make the delivery. The actual physical deliverer remains open pending the signed receipt and notarial act. The contemporaneous record strongly supports that the obligation belonged to CEXP —not Monterecco— and concerned maintenance copies.';
    }

    const warning = reverse.querySelector('.jvre-warning:not([data-jv1260-direct-witness-expanded-21aug])');
    if (warning && /Gil|entrega|delivery|handover|llaves|keys/i.test(warning.textContent)) {
      warning.innerHTML = isEs
        ? '<strong>Grado actual:</strong> CEXP/copias de mantenimiento está fuertemente apoyado por fuentes contemporáneas. La identidad del entregante material está discutida y debe resolverse con el recibí y el acta notarial. No utilizar la entrega como hecho personal de Gil ni como acto de Monterecco sin prueba primaria adicional.'
        : '<strong>Current grade:</strong> the CEXP/maintenance-copy proposition is strongly supported by contemporaneous sources. The identity of the physical deliverer is disputed and must be resolved by the receipt and notarial act. Do not use the handover as an established personal act by Gil or as a Monterecco act without additional primary evidence.';
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', apply, { once: true });
  else apply();
})();