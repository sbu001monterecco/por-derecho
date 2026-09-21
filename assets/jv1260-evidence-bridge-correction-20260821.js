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
      const hinge = cards.find(card => /bisagra de apelación|appellate hinge|28-may-2012: la capacidad|28-May-2012: capacity|28-may-2012: gil marer|28-May-2012: Gil Marer/i.test(card.textContent));
      if (hinge) {
        hinge.innerHTML = isEs ? `
          <span class="jvre-status open">DECLARACIÓN DIRECTA · CORROBORACIÓN PRIMARIA P1</span>
          <h3>28-may-2012: Gil Marer afirma que entregó personalmente las copias como Presidente de CEXP</h3>
          <p><strong>Declaración de testigo directo:</strong> Gil Marer afirma que, poco después de incorporarse al hotel y asumir la Presidencia de CEXP, acudieron al complejo personas del o por cuenta del juzgado local acompañadas de un notario. Le mostraron documentación indicando que tenían derecho a recibir las llaves de las habitaciones afectadas. Gil afirma que obtuvo las copias y las entregó personalmente, como Presidente de CEXP, en simple cumplimiento de la orden/situación judicial. No atribuye al acto ningún significado adicional de entrega de posesión por Monterecco ni de reconocimiento de explotación turística por Monterecco.</p>
          <p><strong>Naturaleza de las llaves:</strong> la evidencia contemporánea controlada las describe como copias de mantenimiento de CEXP. En un complejo hotelero con apartamentos verticalmente interdependientes, una fuga de agua en una unidad superior puede afectar a la inferior o al bloque. Por ello, incluso una unidad cerrada y no utilizada por el hotel podía requerir acceso de mantenimiento para evitar daños a otras fincas e instalaciones. La tenencia de una copia para mantenimiento no equivale por sí sola a explotación turística o posesión jurídica de la unidad.</p>
          <p><strong>Cumplimiento pese al desacuerdo:</strong> Gil afirma que desde el principio consideró equivocada la resolución y que, con el conocimiento adquirido después, llegó a sospechar que el juzgado de Arrecife había recibido una caracterización materialmente distorsionada de los derechos y obligaciones de las unidades —tratándolas como si fueran simples apartamentos vacacionales en vez de unidades insertas en una estructura de participación/explotación hotelera—. Esa es <strong>su alegación actual y una hipótesis a probar</strong>, no un hecho penal adjudicado. Su conducta contemporánea fue, según declara, respetar la orden y combatirla por vías legales, no mediante autotutela.</p>
          <p><strong>No reutilización hotelera:</strong> Gil afirma categóricamente que, después de que las partes adversas cambiaran las cerraduras y hasta el 7-jun-2018, <strong>ninguna de esas unidades se utilizó una sola noche a través de la plataforma del hotel</strong>. No afirma que se produjeran entradas de mantenimiento en todas o alguna de ellas; su punto es que, si una emergencia de agua u otra incidencia exigía acceso, éste habría sido exclusivamente para mantenimiento y no para huéspedes o explotación comercial.</p>
          <p><strong>Contraste conservado:</strong> una comunicación privada contemporánea bajo custodia refiere que un vigilante realizaría la entrega. Esa fuente contraria debe reconciliarse; no elimina ni sustituye la declaración personal de Gil sobre un acto que afirma haber realizado él mismo.</p>
          <p><strong>Control primario:</strong> acta notarial completa + recibí firmado + relación llave/unidad + asistentes/capacidades + cualquier registro de entrega material. Para la no reutilización hotelera: PMS + reservas/folios + housekeeping + ingresos por unidad + inventario de canales + logs de mantenimiento.</p>` : `
          <span class="jvre-status open">DIRECT WITNESS STATEMENT · P1 PRIMARY CORROBORATION</span>
          <h3>28-May-2012: Gil Marer states that he personally handed over the copies as CEXP President</h3>
          <p><strong>Direct witness statement:</strong> Gil Marer states that, shortly after becoming involved at the hotel and assuming the CEXP Presidency, persons from or on behalf of the local court attended the complex with a notary. They showed papers indicating entitlement to receive the keys for the affected rooms. Gil states that he obtained the copies and personally handed them over, as President of CEXP, in straightforward compliance with the court-imposed position. He does not attribute to that act any additional meaning of Monterecco delivering possession or admitting tourist operation by Monterecco.</p>
          <p><strong>Nature of the keys:</strong> controlled contemporaneous evidence describes them as CEXP maintenance copies. In a hotel complex with vertically interdependent units, a water leak in an upper unit can damage the unit below or the wider block. Even a locked unit not being used by the hotel could therefore require maintenance access to prevent damage to other properties and infrastructure. Holding a maintenance copy does not by itself establish tourist operation or legal possession of that unit.</p>
          <p><strong>Compliance despite disagreement:</strong> Gil states that he regarded the ruling as wrong from the outset and, with later knowledge of the underlying history, came to suspect that the Arrecife court had been given a materially distorted account of the rights and obligations attaching to the units — treating them as ordinary holiday apartments rather than units embedded in a hotel participation/operation structure. That is <strong>his present allegation and an investigative hypothesis</strong>, not an adjudicated criminal finding. His contemporaneous conduct, he states, was to respect the order and challenge it through legal means rather than self-help.</p>
          <p><strong>No hotel re-use:</strong> Gil states categorically that, after the adverse parties changed the locks and through 7 June 2018, <strong>none of those affected units was used for a single night through the hotel platform</strong>. He does not assert that maintenance entered every or any unit; his point is that, if a water leak or other emergency required access, it would have been maintenance-only, not guest use or commercial hotel operation.</p>
          <p><strong>Contrary source preserved:</strong> a contemporaneous private communication under custody refers to a security guard making the delivery. That contrary source must be reconciled; it does not erase or replace Gil's first-hand statement about an act he says he personally performed.</p>
          <p><strong>Primary control:</strong> full notarial act + signed receipt + key/unit schedule + attendees/capacities + any physical-delivery record. For the non-use statement: PMS + bookings/folios + housekeeping + unit revenue + channel inventory + maintenance logs.</p>`;
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
        ? '<strong>Grado penal/procesal actual:</strong> la declaración directa de Gil sobre su propia entrega y la no utilización hotelera posterior se conserva como evidencia testimonial/operativa de primera mano; la comunicación contemporánea discordante se conserva como contraevidencia. Su alegación de que el juzgado pudo recibir una representación materialmente falsa de la naturaleza hotelera de los derechos sigue siendo una hipótesis a probar, no una conclusión penal. La pregunta jurídica más fuerte continúa siendo una posible <strong>sobrelectura de un acto de cumplimiento de CEXP y de copias de mantenimiento como prueba de posesión de Monterecco</strong>.'
        : '<strong>Current criminal/procedural grade:</strong> Gil’s direct statement about his own delivery and the subsequent absence of hotel use is preserved as first-hand witness/operational evidence; the inconsistent contemporaneous communication is preserved as counterevidence. His allegation that the court may have received a materially false characterisation of the hotel nature of the rights remains a hypothesis to prove, not a criminal finding. The strongest legal question continues to be a possible <strong>over-reading of a CEXP compliance event and maintenance copies as proof of Monterecco possession</strong>.';
    } else {
      const prior = reverse.querySelector('[data-jv1260-21aug-correction]');
      if (prior) prior.remove();
      const oldDirect = reverse.querySelector('[data-jv1260-direct-witness-21aug]');
      if (oldDirect) oldDirect.remove();
      if (!reverse.querySelector('[data-jv1260-direct-witness-expanded-21aug]')) {
        const head = reverse.querySelector('.jvre-head');
        if (head) {
          const note = document.createElement('div');
          note.className = 'jvre-warning';
          note.dataset.jv1260DirectWitnessExpanded21aug = 'true';
          note.innerHTML = isEs
            ? '<strong>Declaración directa · 21 ago 2026:</strong> Gil Marer afirma que entregó personalmente las copias de llaves como Presidente de CEXP cuando acudieron al hotel personas del o por cuenta del juzgado con un notario y documentación que exigía la entrega. Dice que cumplió deliberadamente aunque consideraba equivocada la resolución y decidió combatirla por vías legales. Las llaves se caracterizan como copias de mantenimiento necesarias para incidencias entre unidades interdependientes. Afirma además que, tras el cambio de cerraduras y hasta el 7-jun-2018, ninguna unidad afectada fue utilizada una sola noche a través de la plataforma del hotel; cualquier acceso de emergencia, si ocurrió, habría sido sólo de mantenimiento. Su sospecha posterior de falsa representación de la naturaleza hotelera de los derechos es una alegación a investigar, no un hecho adjudicado. Una comunicación contemporánea discordante sobre quién haría la entrega se conserva como contraevidencia.'
            : '<strong>Direct witness statement · 21 Aug 2026:</strong> Gil Marer states that he personally handed over the key copies as CEXP President when persons from or on behalf of the court attended the hotel with a notary and papers requiring delivery. He says he deliberately complied although he regarded the ruling as wrong and chose to challenge it through legal means. The keys are characterised as maintenance copies needed for incidents between interdependent units. He further states that, after the locks were changed and through 7 June 2018, no affected unit was used for a single night through the hotel platform; any emergency access, if it occurred, would have been maintenance-only. His later suspicion of a false characterisation of the hotel nature of the rights is an allegation to investigate, not an adjudicated fact. An inconsistent contemporaneous communication about who would deliver the keys is preserved as counterevidence.';
          head.appendChild(note);
        }
      }
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', apply, { once: true });
  else apply();
})();

/* CEXP-COMPETENCE-TO-HNT-GOVERNANCE-BRIDGE-20260821 */
(() => {
  const path = location.pathname.replace(/\/index\.html$/, '/').toLowerCase();
  const isEs = path.includes('/es/');
  const community = /comunidad-instrumentalizacion|community-instrumentalisation/.test(path);
  if (!community || document.querySelector('[data-cexp-hnt-governance-bridge-20260821]')) return;

  let tries = 0;
  const mount = () => {
    const main = document.querySelector('main');
    if (!main) return;
    const reverse = document.getElementById('jv1260-reverse-engineering-17aug2026');
    if (!reverse) {
      if (tries++ < 40) setTimeout(mount, 75);
      return;
    }
    const shell = reverse.querySelector('.shell');
    if (!shell || shell.querySelector('[data-cexp-hnt-governance-bridge-20260821]')) return;

    const wrap = document.createElement('div');
    wrap.className = 'jvre-grid';
    wrap.dataset.cexpHntGovernanceBridge20260821 = 'true';
    const target = isEs
      ? '/por-derecho/es/ricpe-hnt-gc836-trazabilidad/'
      : '/por-derecho/en/ricpe-hnt-gc836-traceability/';
    const minutes = isEs
      ? '/por-derecho/es/comunidad-instrumentalizacion/actas-2011-2022/'
      : '/por-derecho/en/community-instrumentalisation/minutes-2011-2022/';

    wrap.innerHTML = isEs ? `
      <article class="jvre-card jvre-cam">
        <span class="jvre-status open">CONTRADICCIÓN DE GOBERNANZA · PRODUZCA EL PUENTE DE SUCESIÓN</span>
        <h3>En 2011 la explotación estaba «fuera de la Comunidad». ¿Qué instrumento permitió después a la Comunidad autorizar la explotación unitaria y qué ocurrió jurídicamente con CEXP?</h3>
        <p><strong>2011 · límite de competencia:</strong> el propio registro de la Comunidad de Propietarios de 2-feb-2011 trata el cierre/continuidad de la explotación hotelera y la licencia turística como materias fuera de su competencia ordinaria. El 22-jun-2011, dentro del controvertido circuito deuda→voto, la mayoría LPB estaba presente pero quedó sin voto por deuda atribuida y la línea habilitada acordó, entre otras cosas, terminar el mantenimiento CEXP y desplazar funciones hacia Pamanil.</p>
        <p><strong>CEXP siguió teniendo un registro propio:</strong> existe un acta separada de gobernanza CEXP de 7-abr-2017. En el conjunto revisado no se ha localizado una resolución CEXP debidamente convocada, notificada, constituida y votada que la disuelva, la retire o sustituya válidamente su órgano. La ausencia documental no prueba inexistencia; convierte el instrumento en prueba prioritaria.</p>
        <p><strong>2022 · la función reaparece desde otra entidad:</strong> la copia escaneada localizada de 4-feb-2022 es de la <em>Comunidad de Propietarios</em>, no de CEXP. Declara un 20,993% de asistencia/representación, identifica a José Daniel Acosta Matos como presidente de esa Comunidad y pretende aprobar el proyecto CAM, licencias y la incorporación a explotación turística unitaria, además de autoridad bancaria comunitaria. Después, la cadena societaria BORME sitúa la unidad económica hotelera en Hotel New Trend para transformación y posterior explotación MYND.</p>
        <p><strong>Corrección esencial:</strong> ninguna fuente primaria revisada acredita actualmente que José Daniel Acosta Matos fuera Presidente de CEXP. Presidencia de la Comunidad de Propietarios ≠ Presidencia de CEXP. Tampoco se ha localizado el acto CEXP que transfiera su mandato derivado de los propietarios a HNT o al operador posterior.</p>
        <p><strong>Alegación de Gil Marer:</strong> Gil sostiene que la línea comunitaria minoritaria/discutida capturó el órgano en 2011 mediante el circuito deuda→voto, rechazó o desplazó CEXP y que, tras el control material de 2018, la estructura posterior se apropió de la función de gobernanza de la explotación para reemplazar de hecho CEXP en favor de HNT/operación posterior sin autoridad CEXP válida. Esa es una <strong>alegación a probar</strong>, no una conclusión adjudicada. El episodio físico de 7-jun-2018 tampoco constituye por sí solo sucesión corporativa de CEXP.</p>
        <p><strong>Produzca cinco documentos:</strong></p>
        <ul>
          <li>la resolución CEXP que nombró, removió o sustituyó sus órganos después del último registro controlado, con convocatoria, miembros, poderes, quórum y voto;</li>
          <li>el instrumento que disolvió, retiró o sustituyó CEXP, o transfirió su mandato, derechos y obligaciones de explotación;</li>
          <li>la base jurídica que permitió a la Comunidad de Propietarios autorizar en 2022 licencias y explotación unitaria pese a su propio límite competencial de 2011;</li>
          <li>el instrumento por el que HNT y/o el operador posterior adquirieron derechos de explotación sobre cada perímetro relevante, separado de una segregación societaria o del título sobre fincas concretas; y</li>
          <li>qué documentos de autoridad CEXP/Comunidad/HNT fueron entregados a Yaiza, Cabildo, inversores, financiadores, autoridades turísticas y operador actual, y qué verificó cada receptor.</li>
        </ul>
        <p><strong>Regla:</strong> control material ≠ sucesión de gobernanza; Comunidad de Propietarios ≠ CEXP; segregación de una unidad económica ≠ transferencia automática del mandato colectivo de los propietarios.</p>
        <div class="jvre-actions"><a href="${minutes}">Ver actas y autoridad →</a><a class="secondary" href="${target}">Seguir CEXP → HNT → MYND →</a></div>
      </article>` : `
      <article class="jvre-card jvre-cam">
        <span class="jvre-status open">GOVERNANCE CONTRADICTION · PRODUCE THE SUCCESSION BRIDGE</span>
        <h3>Operation was “outside the Community” in 2011. What instrument later empowered the Community to authorise unified operation—and what legally happened to CEXP?</h3>
        <p><strong>2011 · competence boundary:</strong> the Owners’ Community’s own 2-Feb-2011 record treats closure/continuation of hotel operation and the tourism licence as outside ordinary Community competence. On 22-Jun-2011, within the disputed debt→vote chain, the LPB majority was present but treated as unable to vote because of attributed debt; the enabled line then resolved, among other things, to terminate CEXP maintenance and move functions toward Pamanil.</p>
        <p><strong>CEXP still had its own governance record:</strong> a separate CEXP minute exists dated 7-Apr-2017. In the reviewed source set, no duly convened, notified, constituted and voted CEXP resolution has been located dissolving it, retiring it or validly replacing its governing organ. Absence from the reviewed record does not prove non-existence; it makes the instrument priority evidence.</p>
        <p><strong>2022 · the function reappears through a different body:</strong> the located 4-Feb-2022 scanned copy is an <em>Owners’ Community</em> record, not a CEXP act. On its face it records 20.993% attendance/representation, identifies José Daniel Acosta Matos as president of that Community and purports to approve the CAM project, licences and incorporation into unified tourist operation, as well as Community banking authority. Later BORME/corporate records place the hotel economic unit into Hotel New Trend for transformation and later MYND operation.</p>
        <p><strong>Essential correction:</strong> no reviewed primary source currently establishes that José Daniel Acosta Matos was President of CEXP. Owners’ Community presidency ≠ CEXP presidency. Nor has a CEXP act been located transferring its owners-derived collective mandate to HNT or the later operator.</p>
        <p><strong>Gil Marer’s allegation:</strong> Gil alleges that the minority-led/disputed Community line captured the Community organ in 2011 through the debt→vote mechanism, rejected or displaced CEXP and that, after the 2018 material-control change, the later structure appropriated the exploitation-governance function so as to replace CEXP in practice in favour of HNT/later operation without valid CEXP authority. That is an <strong>allegation to prove</strong>, not an adjudicated finding. The physical 7-Jun-2018 event does not itself constitute CEXP corporate succession.</p>
        <p><strong>Produce five records:</strong></p>
        <ul>
          <li>the CEXP resolution appointing, removing or replacing its governing officers after the last controlled record, with notice, members, proxies, quorum and vote;</li>
          <li>the instrument dissolving, retiring or replacing CEXP, or transferring its exploitation mandate, rights and obligations;</li>
          <li>the legal basis on which the Owners’ Community purported in 2022 to authorise licences and unified operation despite its own 2011 competence boundary;</li>
          <li>the instrument by which HNT and/or the later operator acquired exploitation rights over each relevant perimeter, separately from corporate segregation or title to particular properties; and</li>
          <li>which CEXP/Community/HNT authority records were supplied to Yaiza, Cabildo, investors, financiers, tourism authorities and the current operator, and what each recipient verified.</li>
        </ul>
        <p><strong>Rule:</strong> material control ≠ governance succession; Owners’ Community ≠ CEXP; segregation of an economic unit ≠ automatic transfer of an owners-derived collective mandate.</p>
        <div class="jvre-actions"><a href="${minutes}">Open minutes and authority →</a><a class="secondary" href="${target}">Follow CEXP → HNT → MYND →</a></div>
      </article>`;

    shell.appendChild(wrap);
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount, { once: true });
  else mount();
})();
