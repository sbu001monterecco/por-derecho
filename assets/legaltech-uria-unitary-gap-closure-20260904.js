(() => {
  'use strict';

  const current = document.currentScript;
  if (!current || !document.body) return;
  const siteRoot = new URL('../', current.src);
  const rootPath = siteRoot.pathname.replace(/\/+$/, '/');
  const pathname = window.location.pathname.replace(/\/index\.html$/, '/').replace(/\/+$/, '/');
  const relative = pathname.startsWith(rootPath) ? pathname.slice(rootPath.length) : pathname.replace(/^\/+/, '');
  const targets = new Set([
    'en/uria-menendez-sun-park/', 'es/uria-menendez-sun-park/',
    'en/puzzle/', 'es/puzzle/', 'es/uria-menendez/', 'es/haya-cerberus/',
    'en/ric-private-equity-sun-park/', 'es/ric-private-equity-sun-park/',
    'es/reclamacion-caixabank-valencia/'
  ]);
  if (!targets.has(relative) || document.querySelector('[data-legaltech-unitary="20260904"]')) return;

  const lang = relative.startsWith('en/') ? 'en' : 'es';
  const href = (path) => new URL(String(path || '').replace(/^\//, ''), siteRoot).href;
  const esc = (value) => String(value ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  const main = document.querySelector('main');
  if (!main) return;

  const copy = lang === 'es' ? {
    eyebrow: 'LEGALTECH · CRONOLOGÍA UNITARIA · FUENTE Y LÍMITE EN CADA NODO',
    chronology: 'Cronología integral Uría · HAYA · PH122 · RICPE · CaixaBank',
    chronologyIntro: 'La página anterior mostraba sólo cuatro momentos. Esta capa incorpora todos los nodos ya registrados en el manifiesto y los conecta sin convertir proximidad temporal o profesional en conocimiento, conflicto, coordinación o responsabilidad.',
    currentBranch: 'Rama actual CaixaBank / Uría — 2024 → 2027',
    currentBranchText: 'La defensa de CaixaBank de 29 de enero de 2024 identifica a Raimon Tagliavini Sansa y David García Martín y utiliza expresamente el registro del Concurso 36/2012 y de la Administración Concursal. El procedimiento sigue pendiente y controvertido; la vista está señalada para el 28 de enero de 2027. Esto convierte a la firma y a esos abogados en actores profesionales y posibles custodios documentales actuales, no en responsables históricos por asociación.',
    falcon: 'Puente Falcón → formación de RICPE',
    falconText: 'Fuentes públicas de RICPE/Uría atribuyen asesoramiento de formación a Juan Francisco Falcón y sitúan a Acosta Matos en el perímetro fundador/consejo. Falta probar si ese mandato alcanzó Sun Park, qué información recibió y qué controles de conflicto se aplicaron.',
    ph122: 'Huella primaria PH122 / Uría — 15 mayo 2017',
    ph122Text: 'Un escrito de Promontoria Holding 122 B.V. dentro del Concurso 36/2012 aparece firmado por abogados de Uría, incluidos Javier Rubio Sanz, Juan Miguel Hernández Herrera y Ángel Alonso Hernández. Es una huella primaria distinta del contacto reportado de 2015 y de la rama CaixaBank de 2024.',
    borja: 'Corrección de origen del testigo Borja',
    borjaText: 'CaixaBank solicitó el testimonio del Administrador Concursal. Aweswell se adhirió después, de forma renuente y procesal según Gil Marer; la posterior formulación judicial lo registró como propuesto por ambas partes. No debe leerse como selección, patrocinio o confianza positiva independiente de Aweswell.',
    ethics: 'Pruebas jurídicas/deontológicas que deben aplicarse',
    closure: 'Estado RICPE corregido — 27 agosto 2026',
    closureText: 'El Sistema Interno de Información de RICPE inadmitió y archivó la comunicación sin abrir investigación interna. La propia resolución dejó abierta una valoración futura si se aportan hechos o evidencias nuevas, concretas, objetivamente verificables, relevantes y directamente conectadas con conducta propia de RICPE.',
    controls: 'Control documentado vs. alegación de insuficiencia vs. prueba decisiva',
    graph: 'Puzzle actualizado: ya no hay nodos colgantes',
    graphIntro: 'El mapa incorpora CaixaBank, Bankia, BFA, SAREB, HAYA, Cerberus, PH122, RICPE, CAM, Uría y las personas profesionales fechadas. Cada relación conserva su propio estado probatorio.',
    evidence: 'Evidencia visual ya preservada',
    evidenceIntro: 'El cierre RICPE ya dispone de PDF público redactado, texto searchable y seis imágenes de página. Se reutilizan esos activos canónicos; no se crean duplicados ni imágenes sintéticas.',
    matrix: 'Abrir matriz aviso → conducta continuada',
    register: 'Abrir revisión “sí / ahora no”',
    status: 'Estado',
    limits: 'Límites',
    source: 'Fuente / ruta',
    notFinding: 'No es una conclusión de conflicto, infracción, coordinación o culpabilidad.'
  } : {
    eyebrow: 'LEGALTECH · UNITARY CHRONOLOGY · SOURCE AND LIMIT AT EVERY NODE',
    chronology: 'Complete Uría · HAYA · PH122 · RICPE · CaixaBank chronology',
    chronologyIntro: 'The prior page showed only four moments. This layer renders every node already present in the evidence record and connects them without converting professional or temporal proximity into knowledge, conflict, coordination or liability.',
    currentBranch: 'Current CaixaBank / Uría branch — 2024 → 2027',
    currentBranchText: 'CaixaBank’s defence dated 29 January 2024 identifies Raimon Tagliavini Sansa and David García Martín and expressly uses the Concurso 36/2012 / Insolvency Administration record. The proceeding remains pending and contested, with a hearing listed for 28 January 2027. That makes the firm and lawyers current professional actors and possible document custodians—not historical wrongdoers by association.',
    falcon: 'Falcón → RICPE formation bridge',
    falconText: 'RICPE/Uría public material attributes formation advice to Juan Francisco Falcón and places Acosta Matos in the founding/board perimeter. It remains open whether that engagement reached Sun Park, what information was received, and what conflict controls applied.',
    ph122: 'Primary PH122 / Uría footprint — 15 May 2017',
    ph122Text: 'A Promontoria Holding 122 B.V. filing in Concurso 36/2012 is signed by Uría lawyers including Javier Rubio Sanz, Juan Miguel Hernández Herrera and Ángel Alonso Hernández. This is separate from the reported 2015 contact and the 2024 CaixaBank branch.',
    borja: 'Borja witness-origin correction',
    borjaText: 'CaixaBank sought the Insolvency Administrator’s testimony. Aweswell later adhered reluctantly and procedurally according to Gil Marer; the later court formulation records both parties. It must not be read as Aweswell’s independent positive selection, sponsorship or reliance.',
    ethics: 'Legal/professional tests that must be applied',
    closure: 'Corrected RICPE status — 27 August 2026',
    closureText: 'RICPE’s Internal Information System inadmitted and archived the communication without opening an internal investigation. The resolution expressly reserved future assessment if new, concrete, objectively verifiable and relevant evidence directly connected to RICPE conduct is supplied.',
    controls: 'Documented control vs. insufficiency allegation vs. decisive proof',
    graph: 'Updated Puzzle: no dangling nodes',
    graphIntro: 'The map now includes CaixaBank, Bankia, BFA, SAREB, HAYA, Cerberus, PH122, RICPE, CAM, Uría and the dated professional people. Every relationship retains its own evidential status.',
    evidence: 'Visual evidence already preserved',
    evidenceIntro: 'The RICPE closure already has a public redacted PDF, searchable text and six page images. Those canonical assets are reused; no duplicate or synthetic evidence is created.',
    matrix: 'Open notice → continued conduct matrix',
    register: 'Open “yes / not now” review queue',
    status: 'Status',
    limits: 'Limits',
    source: 'Source / route',
    notFinding: 'This is not a finding of conflict, breach, coordination or guilt.'
  };

  const statusClass = (status) => {
    const value = String(status || '').toLowerCase();
    if (value.includes('primary') || value.includes('certified')) return 'lt-primary';
    if (value.includes('counter')) return 'lt-counter';
    if (value.includes('reported')) return 'lt-reported';
    if (value.includes('future') || value.includes('open')) return 'lt-open';
    return 'lt-context';
  };

  const eventHtml = (event) => `
    <article class="lt-event ${statusClass(event.status)}" id="${esc(event.id)}">
      <time>${esc(event.date)}</time><h3>${esc(event.label)}</h3>
      <p>${esc(event.proposition)}</p>
      <p class="lt-status"><strong>${esc(copy.status)}:</strong> ${esc(event.status)}</p>
      ${(event.limitations || []).length ? `<details><summary>${esc(copy.limits)}</summary><ul>${event.limitations.map((item) => `<li>${esc(item)}</li>`).join('')}</ul></details>` : ''}
    </article>`;

  const peopleFor = (graph, ids) => ids.map((id) => graph.nodes.find((node) => node.id === id)).filter(Boolean)
    .map((node) => `<a class="lt-chip" href="${esc(href(lang === 'es' ? node.route_es : node.route_en))}">${esc(node.label)}${node.canonical_id ? `<small>${esc(node.canonical_id)}</small>` : ''}</a>`).join('');

  const addStyle = () => {
    if (document.querySelector('[data-legaltech-unitary-style]')) return;
    const style = document.createElement('style');
    style.setAttribute('data-legaltech-unitary-style', '20260904');
    style.textContent = `
      .lt-unitary{padding:3.4rem 0;background:#f4f0e8;border-top:1px solid rgba(25,44,52,.14);border-bottom:1px solid rgba(25,44,52,.14)}
      .lt-shell{max-width:1180px;margin:auto;padding:0 1rem}.lt-unitary h2{font-size:clamp(2rem,4vw,3.45rem);line-height:1.03;max-width:25ch;margin:.25rem 0 1rem}.lt-unitary .lt-lead{max-width:88ch;line-height:1.65}
      .lt-warning{border-left:6px solid #9a5c18;background:#fff9ed;padding:1rem 1.15rem;margin:1.2rem 0;border-radius:0 12px 12px 0;font-weight:700;max-width:92ch}
      .lt-actions{display:flex;flex-wrap:wrap;gap:.55rem;margin:1rem 0}.lt-actions a{display:inline-flex;padding:.65rem .9rem;border-radius:999px;background:#173f36;color:#fff;text-decoration:none;font-weight:800}.lt-actions a:nth-child(2){background:#6b3f72}
      .lt-timeline{display:grid;grid-template-columns:repeat(auto-fit,minmax(265px,1fr));gap:.85rem;margin:1.25rem 0}.lt-event{background:#fff;border:1px solid rgba(25,44,52,.18);border-top:6px solid #63737a;border-radius:14px;padding:1rem;box-shadow:0 8px 24px rgba(25,44,52,.06)}.lt-event.lt-primary{border-top-color:#176b54}.lt-event.lt-counter{border-top-color:#6b3f72}.lt-event.lt-reported{border-top-color:#a56c00}.lt-event.lt-open{border-top-color:#8d3d36}.lt-event time{font-weight:900;letter-spacing:.04em;color:#6a4b13}.lt-event h3{margin:.35rem 0 .5rem;font-size:1.08rem}.lt-event p{line-height:1.55}.lt-status{font-size:.8rem;color:#536660}.lt-event details{font-size:.86rem}.lt-event summary{cursor:pointer;font-weight:800}
      .lt-branches{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem;margin:1rem 0}.lt-card{background:#fff;border:1px solid rgba(25,44,52,.17);border-radius:16px;padding:1.1rem;box-shadow:0 10px 28px rgba(25,44,52,.07)}.lt-card h3{margin-top:0}.lt-card p{line-height:1.6}
      .lt-chipset{display:flex;flex-wrap:wrap;gap:.45rem}.lt-chip{display:inline-flex;flex-direction:column;padding:.5rem .68rem;border:1px solid rgba(25,44,52,.26);border-radius:10px;text-decoration:none;background:#fff;color:inherit;font-weight:800}.lt-chip small{font:700 .68rem ui-monospace,monospace;color:#6a4b13;margin-top:.2rem}
      .lt-test-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:.8rem}.lt-test{background:#13252d;color:#fff;border-radius:14px;padding:1rem}.lt-test h3{color:#fff;margin:0 0 .4rem}.lt-test p{color:#e8f0f2;line-height:1.55;margin:.2rem 0}
      .lt-control-table{width:100%;border-collapse:separate;border-spacing:0;margin:1rem 0;background:#fff;border:1px solid rgba(25,44,52,.16);border-radius:14px;overflow:hidden}.lt-control-table th,.lt-control-table td{padding:.8rem;vertical-align:top;border-bottom:1px solid rgba(25,44,52,.12);line-height:1.5}.lt-control-table th{background:#173f36;color:#fff;text-align:left}.lt-control-table tr:last-child td{border-bottom:0}
      .lt-edge-list{display:grid;gap:.6rem}.lt-edge{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr);align-items:center;gap:.55rem;background:#fff;border:1px solid rgba(25,44,52,.16);border-radius:12px;padding:.7rem}.lt-edge b{text-align:center;color:#7d4b10;font-size:.78rem}.lt-edge span:last-child{text-align:right}.lt-edge small{display:block;font-weight:500;color:#536660;margin-top:.2rem}
      .lt-evidence-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.85rem;margin-top:1rem}.lt-evidence-grid figure{margin:0;background:#fff;border:1px solid rgba(25,44,52,.18);border-radius:14px;padding:.6rem}.lt-evidence-grid img{display:block;width:100%;height:auto;border-radius:9px}.lt-evidence-grid figcaption{padding:.55rem .2rem .15rem;font-weight:750}
      @media(max-width:900px){.lt-branches{grid-template-columns:1fr}.lt-edge{grid-template-columns:1fr}.lt-edge b,.lt-edge span:last-child{text-align:left}.lt-evidence-grid{grid-template-columns:1fr}}
    `;
    document.head.appendChild(style);
  };

  const makeSection = (id, inner) => {
    const section = document.createElement('section');
    section.id = id;
    section.className = 'lt-unitary';
    section.setAttribute('data-legaltech-unitary', '20260904');
    section.innerHTML = `<div class="lt-shell">${inner}</div>`;
    return section;
  };

  const buildChronology = (graph) => {
    const events = graph.events || [];
    return makeSection(lang === 'es' ? 'cronologia-integral' : 'complete-chronology', `
      <p class="eyebrow">${esc(copy.eyebrow)}</p><h2>${esc(copy.chronology)}</h2><p class="lt-lead">${esc(copy.chronologyIntro)}</p>
      <div class="lt-warning">${esc(copy.notFinding)}</div>
      <div class="lt-actions"><a href="${esc(href(lang === 'es' ? '/es/matriz-aviso-conducta-continuada/' : '/en/notice-continued-conduct-matrix/'))}">${esc(copy.matrix)}</a><a href="${esc(href(lang === 'es' ? '/es/revision-canonica/' : '/en/canonical-review/'))}">${esc(copy.register)}</a></div>
      <div class="lt-timeline">${events.map(eventHtml).join('')}</div>
      <div class="lt-branches">
        <article class="lt-card" id="${lang === 'es' ? 'rama-caixabank-actual' : 'current-caixabank-branch'}"><h3>${esc(copy.currentBranch)}</h3><p>${esc(copy.currentBranchText)}</p><div class="lt-chipset">${peopleFor(graph, ['n-tagliavini','n-garcia','n-caixabank','n-ac'])}</div></article>
        <article class="lt-card" id="${lang === 'es' ? 'puente-falcon-ricpe' : 'falcon-ricpe-bridge'}"><h3>${esc(copy.falcon)}</h3><p>${esc(copy.falconText)}</p><div class="lt-chipset">${peopleFor(graph, ['n-falcon','n-uria','n-ricpe','n-cam'])}</div></article>
        <article class="lt-card" id="${lang === 'es' ? 'huella-ph122-2017' : 'ph122-2017-footprint'}"><h3>${esc(copy.ph122)}</h3><p>${esc(copy.ph122Text)}</p><div class="lt-chipset">${peopleFor(graph, ['n-ph122','n-rubio','n-hernandez','n-alonso'])}</div></article>
      </div>
      <div class="lt-card" id="${lang === 'es' ? 'personas-2015' : 'haya-2015-people'}"><h3>2015 · HAYA / SAREB / Uría</h3><div class="lt-chipset">${peopleFor(graph, ['n-gonzalez','n-cohrs','n-tabada','n-guadalupe','n-rubio'])}</div><p>${esc(lang === 'es' ? 'Estos nodos proceden de comunicaciones contemporáneas saneadas. Se registra lo que cada fuente reporta y, al lado, la contraevidencia del 30 de abril; no se publica el cuerpo privado íntegro ni se infiere mandato por contacto.' : 'These nodes come from sanitised contemporaneous communications. Each reported proposition appears beside the 30 April counter-record; private full message bodies are not published and contact is not treated as a mandate.')}</p></div>
    `);
  };

  const buildEthics = () => makeSection(lang === 'es' ? 'tests-deontologicos' : 'professional-tests', `
    <p class="eyebrow">${esc(copy.ethics)}</p><h2>${esc(copy.ethics)}</h2>
    <div class="lt-test-grid">
      <article class="lt-test"><h3>${esc(lang === 'es' ? 'Conflicto a nivel de firma' : 'Firm-wide conflict')}</h3><p>${esc(lang === 'es' ? 'Identificar cada cliente, asunto, fecha, parte adversa, afiliada y pantalla; una coincidencia de firma no basta, pero tampoco puede evaluarse sin el registro.' : 'Identify each client, matter, date, adverse party, affiliate and screen. A shared firm is not enough, but the issue cannot be assessed without the records.')}</p></article>
      <article class="lt-test"><h3>${esc(lang === 'es' ? 'Información de antiguo cliente' : 'Former-client information')}</h3><p>${esc(lang === 'es' ? 'Determinar si información confidencial material fue accesible, usada, compartida o protegida por una pantalla eficaz.' : 'Determine whether material confidential information was accessible, used, shared or protected by an effective screen.')}</p></article>
      <article class="lt-test"><h3>${esc(lang === 'es' ? 'Lealtad, independencia y abstención' : 'Loyalty, independence and withdrawal')}</h3><p>${esc(lang === 'es' ? 'Separar revelación, consentimiento, obligación de declinar o retirarse y medidas de mitigación.' : 'Separate disclosure, consent, any duty to decline or withdraw, and mitigation measures.')}</p></article>
      <article class="lt-test"><h3>${esc(lang === 'es' ? 'Buena fe procesal y exactitud' : 'Procedural good faith and accuracy')}</h3><p>${esc(lang === 'es' ? 'Contrastar la procedencia y exactitud de hechos sobre Concurso 36/2012 utilizados en el pleito actual; una posición de parte no es un hecho judicial.' : 'Test the provenance and accuracy of Concurso 36/2012 propositions used in current litigation; a party position is not a judicial finding.')}</p></article>
      <article class="lt-test"><h3>${esc(lang === 'es' ? 'No imputación colectiva' : 'No collective attribution')}</h3><p>${esc(lang === 'es' ? 'El conocimiento de un abogado o asunto no se transfiere automáticamente a otro; cualquier imputación exige actor, capacidad, fecha, acto, deber y fuente.' : 'Knowledge in one lawyer or matter does not automatically transfer to another; attribution requires actor, capacity, date, act, duty and source.')}</p></article>
    </div>
  `);

  const buildRicpe = () => makeSection(lang === 'es' ? 'cierre-ricpe-27ago2026' : 'ricpe-closure-27aug2026', `
    <p class="eyebrow">${esc(copy.closure)}</p><h2>${esc(copy.closure)}</h2><p class="lt-lead">${esc(copy.closureText)}</p>
    <table class="lt-control-table"><thead><tr><th>${esc(lang === 'es' ? 'Control/documento registrado' : 'Recorded control/document')}</th><th>${esc(lang === 'es' ? 'Alegación de Gil Marer' : 'Gil Marer allegation')}</th><th>${esc(lang === 'es' ? 'Prueba necesaria para decidir' : 'Evidence needed to decide')}</th></tr></thead><tbody>
      <tr><td>${esc(lang === 'es' ? 'Declaración/abstención o proceso de conflicto CAM registrado; certificación RICPE de 20 julio 2021; examen preliminar del Canal Ético.' : 'Recorded CAM conflict declaration/abstention process; 20 July 2021 RICPE certification; preliminary Ethics Channel review.')}</td><td>${esc(lang === 'es' ? 'Los controles pudieron ser meramente formales, tardíos o ineficaces frente a la relación, información y decisiones reales.' : 'Controls may have been formalistic, late or ineffective against the actual relationship, information and decisions.')}</td><td>${esc(lang === 'es' ? 'Declaraciones completas, actas, asistentes/votos, recusaciones, pantallas, data-room/access logs, DD, versiones de materiales y decisiones de financiación.' : 'Complete declarations, minutes, attendance/votes, recusals, screens, data-room/access logs, DD, material versions and financing decisions.')}</td></tr>
      <tr><td>${esc(lang === 'es' ? 'La resolución de 27 agosto dice que no identificó umbral indiciario suficiente y cerró sin investigación.' : 'The 27 August resolution says it found no sufficient indicia threshold and closed without investigation.')}</td><td>${esc(lang === 'es' ? 'La nueva cronología Uría 2015/2017/2019-20/2024 puede constituir material adicional que merece valoración objetiva.' : 'The new 2015/2017/2019-20/2024 Uría chronology may be additional material warranting objective assessment.')}</td><td>${esc(lang === 'es' ? 'Expediente nativo de decisión, documentos realmente examinados, identidad/capacidad del decisor, conflicto, preservación, circulación al Consejo y razones aplicadas a cada pieza nueva.' : 'Native decision file, documents actually examined, decision-maker identity/capacity, conflict, preservation, Board circulation and reasons applied to each new item.')}</td></tr>
    </tbody></table>
    <div class="lt-actions"><a href="${esc(href('/evidence/ricpe-cnmv/2026-08-27/'))}">${esc(lang === 'es' ? 'Ver resolución íntegra e imágenes' : 'View full resolution and page images')}</a><a href="${esc(href(lang === 'es' ? '/es/matriz-aviso-conducta-continuada/' : '/en/notice-continued-conduct-matrix/'))}">${esc(copy.matrix)}</a></div>
    <div class="lt-evidence-grid"><figure><a href="${esc(href('/evidence/ricpe-cnmv/2026-08-27/resolution-pages-public-redacted/page-4.jpg'))}"><img loading="lazy" decoding="async" src="${esc(href('/evidence/ricpe-cnmv/2026-08-27/resolution-pages-public-redacted/page-4.jpg'))}" alt="RICPE certified resolution page 4"></a><figcaption>${esc(lang === 'es' ? 'Página 4 · inadmisión y archivo sin investigación interna' : 'Page 4 · inadmission and archive without internal investigation')}</figcaption></figure><figure><a href="${esc(href('/evidence/ricpe-cnmv/2026-08-27/resolution-pages-public-redacted/page-5.jpg'))}"><img loading="lazy" decoding="async" src="${esc(href('/evidence/ricpe-cnmv/2026-08-27/resolution-pages-public-redacted/page-5.jpg'))}" alt="RICPE certified resolution page 5"></a><figcaption>${esc(lang === 'es' ? 'Página 5 · posible valoración futura con evidencia nueva' : 'Page 5 · future assessment possible with new evidence')}</figcaption></figure></div>
  `);

  const buildPuzzle = (graph) => makeSection(lang === 'es' ? 'puzzle-unitario-actualizado' : 'updated-unitary-puzzle', `
    <p class="eyebrow">${esc(copy.graph)}</p><h2>${esc(copy.graph)}</h2><p class="lt-lead">${esc(copy.graphIntro)}</p>
    <div class="lt-chipset">${peopleFor(graph, ['n-bfa','n-bankia','n-sareb','n-haya','n-cerberus','n-ph122','n-uria','n-ricpe','n-cam','n-caixabank','n-ac'])}</div>
    <div class="lt-edge-list">${(graph.edges || []).map((edge) => {
      const from = graph.nodes.find((node) => node.id === edge.from); const to = graph.nodes.find((node) => node.id === edge.to);
      return `<div class="lt-edge"><span>${esc(from?.label || edge.from)}</span><b>→ ${esc(edge.type)}<small>${esc(edge.status)}</small></b><span>${esc(to?.label || edge.to)}</span></div>`;
    }).join('')}</div>
  `);

  const buildCaixa = () => makeSection(lang === 'es' ? 'caixabank-uria-actual' : 'caixabank-uria-current', `
    <p class="eyebrow">${esc(copy.currentBranch)}</p><h2>${esc(copy.currentBranch)}</h2><p class="lt-lead">${esc(copy.currentBranchText)}</p>
    <div class="lt-warning"><strong>${esc(copy.borja)}</strong><br>${esc(copy.borjaText)}</div>
    <div class="lt-actions"><a href="${esc(href('/es/uria-menendez-sun-park/#rama-caixabank-actual'))}">${esc(lang === 'es' ? 'Abrir cronología Uría completa' : 'Open complete Uría chronology')}</a><a href="${esc(href('/es/matriz-aviso-conducta-continuada/'))}">${esc(copy.matrix)}</a></div>
  `);

  const init = async () => {
    addStyle();
    const graph = await fetch(href('/data/legaltech/uria-bankia-caixabank-unitary-graph-20260904.json'), { cache: 'no-store' }).then((response) => {
      if (!response.ok) throw new Error(`graph ${response.status}`); return response.json();
    });
    const fragments = [];
    if (relative.includes('uria-menendez-sun-park') || relative === 'es/uria-menendez/' || relative === 'es/haya-cerberus/') {
      fragments.push(buildChronology(graph), buildEthics());
    }
    if (relative.includes('puzzle')) fragments.push(buildPuzzle(graph), buildChronology(graph));
    if (relative.includes('ric-private-equity-sun-park')) fragments.push(buildRicpe(), buildPuzzle(graph));
    if (relative === 'es/reclamacion-caixabank-valencia/') fragments.push(buildCaixa());
    fragments.forEach((section, index) => { if (index > 0) section.removeAttribute('data-legaltech-unitary'); main.appendChild(section); });
  };

  init().catch((error) => console.error('Uría unitary LegalTech layer failed', error));
})();
