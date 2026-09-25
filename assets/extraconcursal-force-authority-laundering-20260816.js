(() => {
  const path = window.location.pathname.replace(/\/+$/, '') + '/';
  const routes = {
    esCal: '/es/calificacion-concurso-36-2012-vidas-paralelas/',
    enCal: '/en/insolvency-classification-parallel-lives/',
    esTake: '/es/toma-control-sun-park-7-junio-2018/',
    enTake: '/en/sun-park-takeover-7-june-2018/',
    esAc: '/es/concurso-36-2012-administrador-concursal/',
    enAc: '/en/insolvency-36-2012-insolvency-administrator/',
    esJudge: '/es/concurso-36-2012-magistrado-juez/',
    enJudge: '/en/insolvency-36-2012-mercantile-court-1/',
    esDp: '/es/dp-1901-2026/',
    esFiscal: '/es/carta-abierta-ministerio-fiscal/',
    enFiscal: '/en/open-letter-public-prosecution-service/',
    esInst: '/es/concurso-36-2012-responsabilidad-institucional/',
    enInst: '/en/insolvency-36-2012-institutional-accountability/'
  };
  const key = Object.entries(routes).find(([,v]) => path.endsWith(v));
  if (!key) return;
  if (document.querySelector('[data-extraconcursal-force-20260816]')) return;
  const isEs = key[0].startsWith('es');
  const isCal = key[0].endsWith('Cal');
  const isTake = key[0].endsWith('Take');
  const isAc = key[0].endsWith('Ac');
  const isJudge = key[0].endsWith('Judge');
  const isDp = key[0] === 'esDp';
  const isFiscal = key[0].endsWith('Fiscal');

  const d = isEs ? {
    eyebrow: 'MI ALEGACIÓN · DESBORDAMIENTO EXTRACONCURSAL · CONTROL POR FUERZA · AUTORIDAD RECICLADA',
    title: isCal ? 'La calificación no puede empezar después de la desposesión: mi acusación es que la autoridad concursal fue instrumentalizada para legitimar un control privado extraconcursal.'
      : isTake ? 'Mi acusación: CAM obtuvo el control del hotel de forma ilegal, fraudulenta, no autorizada y materialmente forzada antes del título.'
      : isAc ? 'Mi acusación contra el Administrador Concursal: una autoridad limitada a LPB fue usada como puente hacia el control privado del hotel.'
      : isJudge ? 'Mi acusación contra el Magistrado-Juez: el desbordamiento no fue sólo tolerado; después fue judicialmente normalizado mientras se culpabilizaba a quienes denunciábamos la pérdida de control.'
      : isFiscal ? 'Mi acusación contra la secuencia fiscal: la posición de la calificación se convirtió en una fuente circular de credibilidad contra el denunciante y a favor del marco AC/CAM.'
      : isDp ? 'DP 1901/2026 puede comprobar si una autoridad limitada a LPB fue convertida en cobertura institucional para una toma privada extraconcursal.'
      : 'Mi acusación: autoridad concursal limitada → control privado extraconcursal → legitimación institucional circular.',
    lead: '<strong>LPB estaba en Concurso 36/2012. Sun Park entero no.</strong> Matkator y otros titulares seguían fuera de la masa; tampoco el negocio hotelero completo se convirtió por arrastre en patrimonio administrable por el AC. Alego que CAM y actores individualizables del perímetro Acosta Matos/Comunidad-seguridad obtuvieron en 2018 control material del hotel mediante acceso forzado, seguridad, cerraduras, exclusión y control de llaves/accesos, sin una entrega judicial del conjunto hotelero que hayamos localizado.',
    allegation: '<strong>Mi acusación penal y patrimonial:</strong> aquella toma fue, en mi criterio, ilegal, fraudulenta, no autorizada, impuesta por la fuerza y funcionalmente clandestina respecto de los titulares/poseedores desplazados. No afirmo que una sentencia penal ya lo haya declarado. Exijo que se determine finca por finca, acto por acto y persona por persona.',
    factsTitle: 'Lo que ya hace esta acusación comprobable',
    facts: [
      ['PERÍMETRO', '<strong>Concurso 36/2012 = LPB, no Sun Park entero.</strong> La autoridad del AC sobre LPB no creaba título sobre Matkator, otros propietarios, todos los derechos CEXP ni la empresa hotelera como totalidad.'],
      ['7 JUN 2018', '<strong>Umbral de control material.</strong> El registro controlado soporta un cambio de acceso/control material y operativo; la posesión práctica total del hotel es mi alegación/inferencia y el alcance finca por finca sigue abierto.'],
      ['AUTORIDAD NO LOCALIZADA', '<strong>No hemos localizado una entrega judicial del conjunto hotelero a CAM vigente el 7 de junio.</strong> Si existe, debe producirse con fecha, partes, términos y fincas.'],
      ['DECLARACIÓN AC · 31 JUL', '<strong>El AC negó ordenar la rotura del acceso codificado, pero admitió accesos, una puerta forzada y una autorización general a la Comunidad; sobre cerraduras rotas para ejecutarla dijo que “lo da por bueno”.</strong>'],
      ['SEGURIDAD / LLAVES', '<strong>Alego que el mecanismo autorizado o tolerado por el AC entregó al perímetro privado el control efectivo de llaves, seguridad y acceso.</strong> La entrega física concreta de cada llave debe probarse con el acta, contrato, guardias, cerrajero y registro de llaves.'],
      ['TÍTULO POSTERIOR', '<strong>La adjudicación de 2022 no viaja hacia atrás.</strong> No convierte por sí sola un acto material de 2018 en autorizado.']
    ],
    lawTitle: 'Por qué “era acreedor” no resuelve la posesión',
    law: 'El Código Civil separa el derecho alegado de la autotutela material: el art. 441 exige acudir a la autoridad competente si se pretende privar de la tenencia a quien resiste; el art. 444 trata separadamente los actos clandestinos, sin conocimiento del poseedor o con violencia; y el art. 446 protege la posesión frente a perturbación. Por eso mi alegación debe examinarse como problema de <strong>título + autoridad + posesión + fuerza/exclusión</strong>, no como una consecuencia automática del crédito hipotecario.',
    actorsTitle: 'La acusación institucional, actor por actor',
    actors: [
      ['CAM / PRIVADOS', '<strong>Alego usurpación/coacción y fraude como hipótesis que debe probarse.</strong> El test no es “CAM terminó siendo adjudicataria”, sino qué derecho tenía el 7 de junio, qué espacios tomó, qué violencia/exclusión se empleó, qué poseedores se opusieron y qué beneficio siguió.'],
      ['ADMINISTRADOR CONCURSAL', '<strong>Alego desbordamiento consciente de autoridad.</strong> Borja representaba/administraba LPB, no Sun Park entero. Su solicitud de seguridad, sus autorizaciones/admisiones y su posterior aprobación de la ejecución material deben auditarse como posible uso de autoridad LPB para habilitar o ratificar control sobre patrimonio y derechos ajenos a la masa.'],
      ['MINISTERIO FISCAL', '<strong>Alego circularidad institucional.</strong> El Fiscal Ricardo de Mosteyrín respaldó el paquete adverso de calificación el 12-03-2019; después, el archivo DI 248 de 07-05-2019 invocó que “este Ministerio” ya había considerado culpable el concurso y responsable a Gil cuando Gil/Aweswell pedían investigar precisamente al AC/CAM.'],
      ['MAGISTRADO ALBERTO LÓPEZ VILLARRUBIA', '<strong>Alego legitimación judicial consciente si el expediente prueba conocimiento de las premisas contrarias.</strong> La Sentencia 163/2023 convirtió determinadas proposiciones AC/Fiscal en hechos judiciales y consecuencias punitivas. Mi acusación de prevaricación depende de demostrar resolución por resolución que conocía la injusticia, no de que una decisión fuera simplemente adversa.']
    ],
    circularTitle: 'El circuito de autolegitimación que alego',
    circular: 'CRÉDITO / UNIDADES PARCIALES → COMUNIDAD Y SEGURIDAD → AUTORIDAD DEL AC DERIVADA DE LPB → ACCESO FORZADO / CERRADURAS / EXCLUSIÓN / CONTROL MATERIAL → LA PROPIA AUTORIZACIÓN AC PASA A EXPLICAR O NORMALIZAR EL RESULTADO → EL CONFLICTO SE REDUCE A “CIVIL” SIN CREAR TÍTULO CAM → EL CONTROL PRIVADO CONTINÚA Y APARECEN PROYECTO / OBRAS / COMERCIALIZACIÓN → EL AC ACUSA A GIL/PINK EN CALIFICACIÓN → FISCAL RESPALDA → LA MISMA POSICIÓN FISCAL SE USA EN EL ARCHIVO DE LA DENUNCIA CONTRA AC/CAM → EL JUEZ ADOPTA PARTE DEL RELATO COMO HALLAZGOS EN 163/2023 → LA SENTENCIA ADQUIERE AUTORIDAD PORTÁTIL → DP 1901/2026 / DP 1956/2026 / VÍA JUDICIAL DEBEN COMPROBAR CONOCIMIENTO, AUTORIDAD, USO, DAÑO Y BENEFICIO.',
    calTitle: 'Por qué esto golpea el núcleo de la calificación',
    cal: [
      ['CAUSALIDAD', 'Después de perderse el control material, no puede imputarse una omisión, deterioro, falta de ingresos, fracaso de rescate o falta de acceso a Gil/LPB sin demostrar qué capacidad real conservaban.'],
      ['COLABORACIÓN', 'No puede llamarse “falta de colaboración” a aquello cuya producción o acceso dependía materialmente del AC, seguridad, CAM, Comunidad u otros controladores. Los retrasos documentales reales siguen siendo visibles.'],
      ['RENTAS / EXPLOTACIÓN', 'La economía del hotel debe partirse antes/después de la toma. Quién podía admitir huéspedes, contratar, mantener habitaciones, controlar reservas o generar ingresos es parte del nexo causal.'],
      ['INVERSIÓN DE ROLES', '<strong>Alego una inversión víctima-responsable:</strong> quienes denunciábamos desplazamiento de control y desbordamiento concursal fuimos convertidos en el centro de la culpa, mientras el acto que alteró quién podía controlar el activo quedó fuera de una auditoría causal equivalente.'],
      ['TERCEROS', 'El art. 166 LC no hace automáticamente cómplice a CAM, pero obliga a preguntar si actos relevantes para la culpabilidad tuvieron cooperación de terceros y por qué esa contribución fue o no individualizada.'],
      ['PORTABILIDAD', 'La Sentencia 163/2023 no sólo produjo consecuencias dentro de la calificación: sus hallazgos adquirieron autoridad institucional utilizable fuera del procedimiento. El beneficio/uso privado debe trazarse, no presumirse.']
    ],
    harmTitle: 'El daño extraconcursal no cabe dentro de la caja LPB',
    harm: [
      ['MATKATOR', 'Posesión, acceso, obras, transformación, frutos, ingresos, financiación y restitución de sus fincas deben auditarse fuera de la masa LPB.'],
      ['OTROS PROPIETARIOS / CEXP', 'Cada derecho necesita título y consentimiento propios. Seguridad comunitaria no equivale a transferencia universal de posesión ni de explotación.'],
      ['NEGOCIO HOTELERO', 'Clientes, reservas, recepción, personal, datos, fondo de comercio, operador ONA y capacidad de salida constituían una plataforma económica que no se reduce a la titularidad registral de fincas LPB.'],
      ['AWESWELL', 'La pérdida de rescate, financiación, control y valor del accionista/inversor extranjero es un plano separado de la pérdida de la masa y exige standing, causalidad y no doble recuperación.'],
      ['FRUTOS / BENEFICIO ACTUAL', 'Debe trazarse qué uso, ingresos, obras, financiación o valor actual dependen de qué activo o derecho disputado. No se suma todo el valor actual del hotel como daño.']
    ],
    dpTitle: 'Lo que DP 1901/2026 debe obtener para que esto deje de ser una batalla de relatos',
    dp: [
      'Acta, audio, votos, contrato, payer e instrucciones de seguridad de 18 de mayo de 2018.',
      'Registro de llaves, códigos, cerraduras, cerrajero, guardias, CCTV, órdenes y facturas antes/durante/después del 7 de junio.',
      'Mapa finca por finca de propiedad, posesión y consentimiento para LPB, Matkator y terceros.',
      'Declaración audiovisual y expediente completo DP 1132/2018 / Auto 804, incluida la prueba sobre la autorización del AC.',
      'Comunicaciones completas del AC sobre acceso, seguridad, daños, restitución, ONA, valoración y medidas de protección.',
      'Qué documentos estaban efectivamente ante el Fiscal de calificación, la Fiscal de DI248 y el Magistrado al adoptar cada premisa.',
      'Cadena de utilización exterior: notaría, Registro, proyectos, operadores, inversores, RICPE, administraciones y medios.',
      'Cuenta de frutos, reservas, ingresos, costes, obras y beneficio desde el control material hasta el título formal.'
    ],
    offencesTitle: 'Hipótesis penales: sólo con sus elementos',
    offences: '<strong>CAM/privados:</strong> usurpación (art. 245 CP) y coacciones (art. 172 CP) son hipótesis si se prueban inmueble/derecho ajeno, falta de autorización y los medios exigidos. <strong>Fraude procesal:</strong> art. 250.1.7 CP requiere manipulación/fraude procesal, error judicial y resolución perjudicial. <strong>AC:</strong> art. 252 CP exige poderes de administración, exceso/infracción y perjuicio patrimonial. <strong>Juez:</strong> art. 446 CP exige resolución injusta dictada a sabiendas. La secuencia fiscal se publica como alegación de circularidad/instrumentalización, no como delito automáticamente etiquetado.',
    defenceTitle: 'La defensa más fuerte — y la pregunta que no desaparece',
    defence: '<strong>Defensa:</strong> CAM/Comunidad pueden decir que existía consentimiento, derechos de propietario/acreedor, una medida legítima de seguridad y que la actuación quedó respaldada por la versión del AC y decisiones posteriores. <strong>Pregunta residual:</strong> ¿qué documento autorizaba, exactamente el 7 de junio, privar o condicionar la posesión/acceso de cada titular y controlar el hotel como una unidad, y cómo podía un poder del AC limitado a LPB producir ese resultado fuera de LPB?',
    boundary: '<strong>Control probatorio:</strong> “ilegal”, “fraudulento”, “usurpación”, “coacción”, “fraude procesal”, “administración desleal”, “prevaricación”, “instrumentalización criminal” y “lavado/reciclaje de autoridad concursal” se presentan aquí como <strong>alegaciones de Gil Marer o hipótesis jurídicas</strong>, salvo los hechos documentales descritos separadamente. La finalidad es hacer la acusación falsable mediante documentos, no sustituir una sentencia penal.',
    links: {
      takeover: '../toma-control-sun-park-7-junio-2018/',
      ac: '../concurso-36-2012-administrador-concursal/',
      judge: '../concurso-36-2012-magistrado-juez/',
      dp: '../dp-1901-2026/',
      cal: '../calificacion-concurso-36-2012-vidas-paralelas/'
    }
  } : {
    eyebrow: 'MY ALLEGATION · EXTRACONCURSAL OVERREACH · FORCIBLE CONTROL · RECYCLED AUTHORITY',
    title: isCal ? 'The classification cannot begin after the dispossession: I allege insolvency authority was instrumentalised to legitimise private extraconcursal control.'
      : isTake ? 'My allegation: CAM obtained control of the hotel illegally, fraudulently, without authorisation and through materially forcible means before title.'
      : isAc ? 'My allegation against the Insolvency Administrator: authority limited to LPB was used as a bridge to private control of the hotel.'
      : isJudge ? 'My allegation against the Judge: the overreach was not merely left uncorrected; it was later normalised judicially while blame was imposed on those alleging loss of control.'
      : isFiscal ? 'My allegation about the prosecution sequence: the classification position became a circular source of adverse credibility against the complainant and in favour of the AC/CAM frame.'
      : 'My allegation: limited insolvency authority → private extraconcursal control → circular institutional legitimisation.',
    lead: '<strong>LPB was in Concurso 36/2012. Sun Park as a whole was not.</strong> Matkator and other owners remained outside the estate; the whole hotel business did not automatically become property administered by the AC. I allege CAM and individually provable Acosta Matos / Community-security actors obtained material control in 2018 through forced access, security, locks, exclusion and control of keys/access, without a judicial delivery of the whole hotel that we have located.',
    allegation: '<strong>My criminal and patrimonial allegation:</strong> that takeover was, in my view, illegal, fraudulent, unauthorised, imposed by force and functionally clandestine as against displaced owners/possessors. I do not claim a criminal court has already declared that. I demand an asset-by-asset, act-by-act and person-by-person determination.',
    factsTitle: 'What already makes the allegation testable',
    facts: [
      ['PERIMETER', '<strong>Concurso 36/2012 = LPB, not the whole of Sun Park.</strong> AC authority over LPB did not create title over Matkator, other owners, all CEXP rights or the hotel business as a whole.'],
      ['7 JUN 2018', '<strong>Material-control threshold.</strong> The controlled record supports a shift in de facto access/material/operational control; whole-hotel practical possession is my allegation/inference and exact property reach remains open.'],
      ['AUTHORITY NOT LOCATED', '<strong>We have not located a judicial delivery of the whole hotel to CAM effective on 7 June.</strong> If one exists, it should be produced with date, parties, terms and property perimeter.'],
      ['AC STATEMENT · 31 JUL', '<strong>The AC denied ordering the coded-access break, but admitted access, a forced door and a general Community authorisation; regarding broken locks used to implement it, he said in substance that he approved it.</strong>'],
      ['SECURITY / KEYS', '<strong>I allege the mechanism authorised or tolerated by the AC delivered effective key/security/access control to the private perimeter.</strong> Literal physical delivery of each key remains for the minutes, security contract, guards, locksmith and key ledger to prove.'],
      ['LATER TITLE', '<strong>2022 adjudication does not travel backwards.</strong> It does not by itself make a 2018 material act authorised.']
    ],
    lawTitle: 'Why “CAM was a creditor” does not resolve possession',
    law: 'The Civil Code separates an asserted right from material self-help: Article 441 requires recourse to competent authority when one seeks to deprive a resisting possessor of possession; Article 444 separately addresses clandestine acts, acts without the possessor’s knowledge and acts with violence; Article 446 protects possession against disturbance. My allegation therefore has to be tested as <strong>title + authority + possession + force/exclusion</strong>, not as an automatic consequence of the mortgage credit.',
    actorsTitle: 'The institutional allegation, actor by actor',
    actors: [
      ['CAM / PRIVATE ACTORS', '<strong>I allege usurpation/coercion and fraud as hypotheses requiring proof.</strong> The test is not “CAM later became adjudicatee”, but what right existed on 7 June, what areas were taken, what force/exclusion was used, which possessors opposed it and what benefit followed.'],
      ['INSOLVENCY ADMINISTRATOR', '<strong>I allege knowing overreach of authority.</strong> Borja represented/administered LPB, not the whole of Sun Park. His security request, authorisations/admissions and later approval of material implementation must be audited as possible use of LPB authority to enable or ratify control over property and rights outside the estate.'],
      ['PUBLIC PROSECUTION SERVICE', '<strong>I allege institutional circularity.</strong> Prosecutor Ricardo de Mosteyrín endorsed the adverse classification package on 12 Mar 2019; later, the 7 May 2019 DI248 archive invoked that “this Ministry” had already treated the insolvency as culpable and Gil as responsible when Gil/Aweswell were asking for the AC/CAM perimeter to be investigated.'],
      ['JUDGE ALBERTO LÓPEZ VILLARRUBIA', '<strong>I allege knowing judicial legitimisation if the file proves knowledge of the contrary premises.</strong> Judgment 163/2023 converted selected AC/Fiscal propositions into judicial findings and punitive consequences. My prevaricación allegation depends on proving knowing injustice resolution by resolution, not merely an adverse decision.']
    ],
    circularTitle: 'The self-legitimation circuit I allege',
    circular: 'CREDIT / PARTIAL UNITS → COMMUNITY AND SECURITY → AC AUTHORITY DERIVED FROM LPB → FORCED ACCESS / LOCKS / EXCLUSION / MATERIAL CONTROL → THE AC’S OWN AUTHORISATION BECOMES PART OF THE EXPLANATION OR NORMALISATION OF THE RESULT → THE CONFLICT IS REDUCED TO “CIVIL” WITHOUT CREATING CAM TITLE → PRIVATE CONTROL CONTINUES AND PROJECT / WORKS / COMMERCIALISATION APPEAR → AC ACCUSES GIL/PINK IN CLASSIFICATION → PROSECUTOR ENDORSES → THE SAME PROSECUTION POSITION IS USED IN ARCHIVING THE COMPLAINT AGAINST AC/CAM → JUDGE ADOPTS PART OF THE STORY AS FINDINGS IN 163/2023 → THE JUDGMENT GAINS PORTABLE AUTHORITY → DP 1901/2026 / DP 1956/2026 / JUDICIAL TRACK MUST TEST KNOWLEDGE, AUTHORITY, USE, HARM AND BENEFIT.',
    calTitle: 'Why this strikes at the core of the classification',
    cal: [
      ['CAUSATION', 'After material control was lost, an omission, deterioration, loss of income, rescue failure or access failure cannot be attributed to Gil/LPB without proving what actual capacity they retained.'],
      ['COLLABORATION', 'Conduct whose production/access materially depended on the AC, security, CAM, Community or other controllers cannot automatically be called Gil/LPB non-cooperation. Real documentary delays remain visible.'],
      ['RENT / OPERATION', 'Hotel economics must split before/after takeover. Who could admit guests, contract, maintain rooms, control bookings or generate income is part of causation.'],
      ['ROLE REVERSAL', '<strong>I allege a victim/responsible-party inversion:</strong> those alleging displacement of control and insolvency overreach became the focus of blame while the act changing who could control the asset did not receive equivalent causal scrutiny.'],
      ['THIRD PARTIES', 'Former Article 166 LC does not automatically make CAM an accomplice, but it does require asking whether culpability-relevant acts involved third-party cooperation and why that contribution was or was not individualised.'],
      ['PORTABILITY', 'Judgment 163/2023 did not only have effects inside classification: its findings acquired portable institutional authority. Private use/benefit must be traced, not presumed.']
    ],
    harmTitle: 'Extraconcursal harm does not fit inside the LPB box',
    harm: [
      ['MATKATOR', 'Possession, access, works, transformation, fruits, income, financing and restitution concerning its properties must be audited outside the LPB estate.'],
      ['OTHER OWNERS / CEXP', 'Each right needs its own title and consent. Community security does not equal a universal transfer of possession or operation.'],
      ['HOTEL BUSINESS', 'Customers, bookings, reception, personnel, data, goodwill, the ONA operator and financed-exit capacity formed an economic platform not reducible to LPB registered properties.'],
      ['AWESWELL', 'Loss of rescue, financing, control and foreign-investor/shareholder value is separate from estate loss and requires standing, causation and no double recovery.'],
      ['CURRENT FRUITS / BENEFIT', 'Trace which present use, income, works, financing or value depends on which disputed asset/right. Do not add all current hotel value as damage.']
    ],
    dpTitle: 'What DP 1901/2026 should obtain so this stops being a battle of narratives',
    dp: [
      '18 May 2018 Community/security minutes, audio, votes, contract, payer and instructions.',
      'Keys, codes, locks, locksmith, guards, CCTV, orders and invoices before/during/after 7 June.',
      'Property-by-property ownership, possession and consent map for LPB, Matkator and third parties.',
      'Complete audiovisual and certified DP 1132/2018 / Auto 804 record, including evidence about AC authorisation.',
      'Complete AC communications on access, security, damage, restoration, ONA, valuation and protective measures.',
      'What documents were actually before the classification Prosecutor, DI248 Prosecutor and Judge when each premise was adopted.',
      'External-use chain: notary, Registry, projects, operators, investors, RICPE, public authorities and media.',
      'Account of fruits, bookings, revenues, costs, works and benefit from material control to formal title.'
    ],
    offencesTitle: 'Criminal hypotheses: elements only',
    offences: '<strong>CAM/private actors:</strong> usurpation (Art 245 CP) and coercion (Art 172 CP) are hypotheses if another’s immovable/right, lack of authority and the required means are proved. <strong>Procedural fraud:</strong> Art 250.1.7 CP requires manipulation/procedural fraud, judicial error and a prejudicial resolution. <strong>AC:</strong> Art 252 CP requires powers of administration, infringement/excess and patrimonial harm. <strong>Judge:</strong> Art 446 CP requires a knowingly unjust resolution. The prosecution sequence is published as an allegation of circularity/instrumentalisation, not an automatically labelled offence.',
    defenceTitle: 'The strongest defence — and the question that remains',
    defence: '<strong>Defence:</strong> CAM/Community may say there was consent, owner/creditor rights, legitimate security and later support from the AC’s version and court outcomes. <strong>Residual question:</strong> exactly what document, effective on 7 June, authorised depriving or conditioning each holder’s possession/access and controlling the hotel as a unit, and how could an AC power limited to LPB produce that result outside LPB?',
    boundary: '<strong>Evidential control:</strong> “illegal”, “fraudulent”, “usurpation”, “coercion”, “procedural fraud”, “disloyal administration”, “prevaricación”, “criminal instrumentalisation” and “insolvency-authority laundering/recycling” are presented here as <strong>Gil Marer’s allegations or legal hypotheses</strong>, except for separately identified documentary facts. The purpose is to make the allegation falsifiable through evidence, not to substitute for a criminal judgment.',
    links: {
      takeover: '../../es/toma-control-sun-park-7-junio-2018/',
      ac: '../insolvency-36-2012-insolvency-administrator/',
      judge: '../insolvency-36-2012-mercantile-court-1/',
      dp: '../../es/dp-1901-2026/',
      cal: '../insolvency-classification-parallel-lives/'
    }
  };

  const style = document.createElement('style');
  style.textContent = `
  .efa26{padding:1.2rem 0 2.8rem}.efa26 .efa-wrap{max-width:1120px;margin:0 auto}.efa26 .efa-shell{background:#fff;border:2px solid #13252d;border-radius:22px;padding:clamp(1.1rem,3vw,1.65rem);box-shadow:0 18px 42px rgba(19,37,45,.09)}
  .efa26 .efa-eyebrow{font-size:.74rem;letter-spacing:.085em;text-transform:uppercase;font-weight:900;color:#8f2d27}.efa26 h2{font-size:clamp(1.9rem,4vw,2.8rem);line-height:1.04;margin:.4rem 0 .9rem}.efa26 .efa-lead{font-size:1.08rem;line-height:1.58}.efa26 .efa-allegation{background:#f4e4e1;border-left:7px solid #8f2d27;border-radius:14px;padding:1rem 1.15rem;font-size:1.04rem}
  .efa26 h3{margin:1.55rem 0 .7rem}.efa26 .efa-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.8rem}.efa26 .efa-card{border:1px solid rgba(19,37,45,.16);border-radius:14px;padding:1rem;background:#f8f8f6}.efa26 .efa-card b{display:block;font-size:.72rem;letter-spacing:.065em;text-transform:uppercase;color:#6b5841;margin-bottom:.35rem}.efa26 .efa-law{background:#f3efe4;border-left:6px solid #c89432;border-radius:14px;padding:1rem 1.15rem;margin:1rem 0}.efa26 .efa-actors{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.8rem}.efa26 .efa-actor{background:#13252d;color:#fff;border-radius:14px;padding:1rem}.efa26 .efa-actor b{display:block;font-size:.73rem;letter-spacing:.06em;text-transform:uppercase;color:#d6b16b;margin-bottom:.35rem}.efa26 .efa-chain{background:#0e222a;color:#fff;border-radius:16px;padding:1rem 1.15rem;font-weight:750;line-height:1.6;overflow-wrap:anywhere}.efa26 .efa-harm{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:.7rem}.efa26 .efa-harm article{border-top:4px solid #526b59;background:#f5f7f6;border-radius:12px;padding:.9rem}.efa26 .efa-harm b{font-size:.72rem;letter-spacing:.06em;color:#526b59}.efa26 .efa-dp{background:#13252d;color:#fff;border-radius:16px;padding:1rem 1.2rem}.efa26 .efa-dp li{margin:.45rem 0}.efa26 .efa-offences{border:1px dashed #8f2d27;border-radius:14px;padding:1rem;background:#fffafa}.efa26 .efa-defence{background:#eef1ef;border-left:6px solid #526b59;border-radius:14px;padding:1rem 1.15rem}.efa26 .efa-boundary{font-size:.9rem;color:#555;margin-top:1rem}.efa26 .efa-links{display:flex;flex-wrap:wrap;gap:.55rem;margin-top:1rem}
  @media(max-width:900px){.efa26 .efa-harm{grid-template-columns:1fr 1fr}.efa26 .efa-grid,.efa26 .efa-actors{grid-template-columns:1fr}}@media(max-width:600px){.efa26 .efa-harm{grid-template-columns:1fr}.efa26 .efa-shell{border-radius:0}}
  `;
  document.head.appendChild(style);

  const cards = d.facts.map(([a,b])=>`<article class="efa-card"><b>${a}</b><div>${b}</div></article>`).join('');
  const actors = d.actors.map(([a,b])=>`<article class="efa-actor"><b>${a}</b><div>${b}</div></article>`).join('');
  const cal = d.cal.map(([a,b])=>`<article class="efa-card"><b>${a}</b><div>${b}</div></article>`).join('');
  const harm = d.harm.map(([a,b])=>`<article><b>${a}</b><div>${b}</div></article>`).join('');
  const dp = d.dp.map(x=>`<li>${x}</li>`).join('');
  const section = document.createElement('section');
  section.className = 'section efa26';
  section.dataset.extraconcursalForce20260816 = '1';
  section.innerHTML = `<div class="shell efa-wrap"><div class="efa-shell"><div class="efa-eyebrow">${d.eyebrow}</div><h2>${d.title}</h2><p class="efa-lead">${d.lead}</p><div class="efa-allegation">${d.allegation}</div><h3>${d.factsTitle}</h3><div class="efa-grid">${cards}</div><h3>${d.lawTitle}</h3><div class="efa-law">${d.law}</div><h3>${d.actorsTitle}</h3><div class="efa-actors">${actors}</div><h3>${d.circularTitle}</h3><div class="efa-chain">${d.circular}</div><h3>${d.calTitle}</h3><div class="efa-grid">${cal}</div><h3>${d.harmTitle}</h3><div class="efa-harm">${harm}</div><h3>${d.dpTitle}</h3><div class="efa-dp"><ol>${dp}</ol></div><h3>${d.offencesTitle}</h3><div class="efa-offences">${d.offences}</div><h3>${d.defenceTitle}</h3><div class="efa-defence">${d.defence}</div><p class="efa-boundary">${d.boundary}</p><div class="efa-links"><a class="button secondary" href="${d.links.takeover}">${isEs?'7 junio 2018':'7 June 2018'}</a><a class="button secondary" href="${d.links.ac}">AC</a><a class="button secondary" href="${d.links.judge}">${isEs?'Magistrado-Juez':'Judge / Court'}</a><a class="button secondary" href="${d.links.dp}">DP 1901/2026</a><a class="button secondary" href="${d.links.cal}">${isEs?'Calificación':'Classification'}</a></div></div></div>`;

  let anchor = null;
  if (isCal) anchor = document.querySelector('[data-cal-creditor-control-20260816]') || document.querySelector('[data-calificacion-radical-20260816]');
  else if (isTake) anchor = document.querySelector('#administrador-y-juez') || document.querySelector('#hechos-7-junio');
  else if (isAc || isJudge || isFiscal || isDp) anchor = document.querySelector('main .hero') || document.querySelector('main section');
  else anchor = document.querySelector('main .hero') || document.querySelector('main section');
  if (anchor) anchor.insertAdjacentElement('afterend', section);
})();