(() => {
  const d = document;
  const current = d.currentScript;
  const path = location.pathname.replace(/\/+$/, '/');
  const es = /\/es\//.test(path);
  const isHome = /\/(en|es)\/$/.test(path);
  const isPwc = /\/(en|es)\/pwc-canarias-carlos-saavedra-sun-park\/$/.test(path);
  const isRicpe = /\/(en|es)\/ric-private-equity-sun-park\/$/.test(path);
  const isAc = /\/en\/insolvency-36-2012-insolvency-administrator\/$/.test(path)
    || /\/es\/concurso-36-2012-administrador-concursal\/$/.test(path);
  const isTakeover = /\/en\/sun-park-takeover-7-june-2018\/$/.test(path)
    || /\/es\/toma-control-sun-park-7-junio-2018\/$/.test(path);
  const isAccountability = /\/en\/insolvency-36-2012-institutional-accountability\/$/.test(path)
    || /\/es\/concurso-36-2012-responsabilidad-institucional\/$/.test(path);
  if (!isHome && !isPwc && !isRicpe && !isAc && !isTakeover && !isAccountability) return;

  const assetBase = current?.src
    ? new URL('.', current.src)
    : new URL('/por-derecho/assets/', location.href);
  const asset = (name) => new URL(name, assetBase).href;
  const base = es ? '/por-derecho/es/' : '/por-derecho/en/';
  const routes = {
    actors: base + (es ? 'actores-partes-abogados-representantes/' : 'actors-parties-lawyers-representatives/'),
    ac: base + (es ? 'concurso-36-2012-administrador-concursal/' : 'insolvency-36-2012-insolvency-administrator/'),
    court: base + (es ? 'concurso-36-2012-juzgado-mercantil-1/' : 'insolvency-36-2012-mercantile-court-1/'),
    accountability: base + (es ? 'concurso-36-2012-responsabilidad-institucional/' : 'insolvency-36-2012-institutional-accountability/'),
    takeover: base + (es ? 'toma-control-sun-park-7-junio-2018/' : 'sun-park-takeover-7-june-2018/'),
    pwc: base + 'pwc-canarias-carlos-saavedra-sun-park/',
    ricpe: base + 'ric-private-equity-sun-park/'
  };

  const c = es ? {
    eyebrow: 'ACUSACIÓN PENAL RECTORA · CINCO ACTORES PRIVADOS + AC + JUEZ',
    title: 'Cinco actores, Administrador Concursal y Juez: funciones separadas, una cadena que debe probarse.',
    intro: 'Gil Marer acusa directamente a cinco personas privadas de haber formado, a más tardar en 2018, una estructura coordinada de administradores de hecho o en la sombra sobre la esfera patrimonial y empresarial de Luchy Playa Blanca y la plataforma hotelera integrada. Atribuye separadamente al Administrador Concursal y al Magistrado-Juez actos afirmativos, comisiones y omisiones que habrían habilitado, preservado y consolidado el mecanismo.',
    criminalK: 'FORMULACIÓN PENAL CONTROLANTE · PUBLICADA POR GIL MARER',
    criminalT: 'No se alega mera pasividad: se alegan instrucción, ejecución, habilitación, adopción, ratificación y sabotaje de la salida.',
    criminalB: 'La acusación conecta deuda y voto, acceso y seguridad, llaves, mantenimiento, obras y valoración, información, estrategia concursal, operación, ingresos, título y resultado. Gil sostiene que Aweswell había cumplido o podía cumplir las condiciones bajo su control y que el obstáculo operativo estaba en preservar y entregar garantías/colateral, obtener cifra de deuda y autoridad concursal/judicial y mantener acceso, explotación y valoración. Es una acusación directa, no una sentencia ni una prueba de desembolso o propósito común.',
    context: {
      home: 'Vista principal del mecanismo económico, sus cinco actores privados y sus dos puntos institucionales de control.',
      pwc: 'Conecta el conocimiento profesional de 2016 con el contacto confirmado PwC–Administrador Concursal.',
      ricpe: 'Conecta Comunidad/control con las posteriores preguntas de título, due diligence, capital y operación RICPE.',
      ac: 'Separa al AC del perímetro privado y somete su papel a conocimiento → poder/deber → comisión/omisión → consecuencia.',
      takeover: 'Coloca el 7 de junio de 2018 como bisagra de control material dentro de la cadena alegada.',
      accountability: 'Separa el perímetro privado, el control concursal y la revisión judicial para evitar atribuciones por asociación.'
    },
    privateK: 'PERÍMETRO PRIVADO IDENTIFICADO · 5',
    privateT: 'Cinco administradores de hecho o en la sombra alegados dentro de una cadena funcional',
    privateB: 'Gil alega actuación coordinada, pero no atribuye automáticamente cada acto a los cinco: función, autoridad, conocimiento, instrucción, intención, beneficio y causalidad deben probarse persona por persona. Parentesco o vínculo empresarial no sustituyen esa prueba.',
    locked: 'FECHAS MÍNIMAS BLOQUEADAS: acreditan implicación no más tarde de la fecha indicada; no afirman que ese fuera el primer día real.',
    actors: [
      {
        n: '01',
        name: 'Francisco Mario Matos Matas',
        stage: '22 JUN 2011 → ADMINISTRACIÓN / CUSTODIA',
        rel: 'ESPOSO DE SHAILA MARÍA COGOLLUDO RAMOS',
        text: 'El acta de 22 de junio de 2011 lo identifica como administrador de la Comunidad. Gil le atribuye continuidad en deuda, voto, cuentas, información, acceso y ejecución material dentro de la estructura de hecho alegada. La responsabilidad exige actos propios, no parentesco.',
        image: asset('actors/francisco-mario-matos-matas.jpg'),
        imageAlt: 'Francisco Mario Matos Matas',
        imageNote: 'Activo de identidad canónico del repositorio; no identificado por inferencia facial.'
      },
      {
        n: '02',
        name: 'Antonio Cogolludo Rojas',
        stage: '10 ABR 2014 → REPRESENTACIÓN / COMUNIDAD',
        rel: 'PADRE DE SHAILA MARÍA COGOLLUDO RAMOS',
        text: 'El acta notarial de 10 de abril de 2014 lo identifica como representante de Cristina Molina Petit. Gil le atribuye después funciones de presidencia, acceso, llaves, seguridad e implementación. Cada acto y fecha siguen sometidos a prueba.'
      },
      {
        n: '03',
        name: 'Shaila María Cogolludo Ramos',
        stage: '8 ABR 2014 → COMUNICACIONES / ADMINISTRACIÓN',
        rel: 'HIJA DE ANTONIO COGOLLUDO ROJAS · ESPOSA DE FMMM',
        text: 'Una comunicación Pamanil de 8 de abril de 2014 aparece firmada por FMMM y Shaila. La continuidad Pamanil/Comunidad y el nodo de voto y tesorería de 2018 sustentan la función de administración material que Gil le atribuye.'
      },
      {
        n: '04',
        name: 'José Daniel Acosta Matos',
        stage: '2017–2018 → PROYECTO / CONTROL',
        text: 'Entrada documentada en el perímetro CAM/Comunidad, visitas anteriores al 7 de junio y presidencia comunitaria en 2022. Gil le atribuye planificación, financiación, control, futura explotación y resultado; no presencia física el 7 de junio.'
      },
      {
        n: '05',
        name: 'Laura Patricia Acosta Matos',
        stage: '2017–2018 → JURÍDICO / CONCURSO / SUCESIÓN',
        text: 'Papel jurídico y concursal, acceso, representación CAM y continuidad posterior en Hotel New Trend. Gil le atribuye instrucciones y funciones directas de control; identidad, mandato, presencia y acto concreto permanecen como campos separados.'
      }
    ],
    institutionalK: 'INMEDIATAMENTE DEBAJO · DOS NODOS INSTITUCIONALES SEPARADOS',
    institutionalT: 'Administrador Concursal y Magistrado-Juez: imágenes, funciones, comisiones, omisiones y límites',
    institutionalB: 'No son un sexto y séptimo actor privado. Tenían funciones jurídicas distintas. La matriz exige vincular cada conducta privada con el conocimiento, poder/deber, acto afirmativo u omisión y consecuencia atribuidos a cada nodo institucional.',
    commissionK: 'ACTOS AFIRMATIVOS / COMISIONES ALEGADAS',
    omissionK: 'OMISIONES ALEGADAS',
    ac: {
      role: 'ADMINISTRADOR CONCURSAL · GATEKEEPER FIDUCIARIO · CONCURSO 36/2012',
      name: 'Francisco de Borja Rodríguez-Batllori Laffitte',
      image: asset('actors/francisco-de-borja-rodriguez-batllori.jpg'),
      imageAlt: 'Francisco de Borja Rodríguez-Batllori Laffitte, Administrador Concursal en el Concurso 36/2012',
      copy: 'Su relevancia depende de qué verificó, solicitó, autorizó, transmitió, implementó, adoptó, ratificó, toleró, informó, preservó o intentó revertir mientras administraba la masa de LPB; no de haber ejecutado personalmente cada acto privado.',
      commissions: [
        'Usar la mayoría LPB para promover la ruta comunitaria de seguridad y acceso de 18 de mayo de 2018.',
        'Participar en correos, reuniones, peticiones y autorizaciones utilizados para acceso, vigilancia o mantenimiento.',
        'Adoptar o ratificar después el resultado de acceso/cerraduras y utilizar insumos comunitarios de deuda, certificados o cálculos.'
      ],
      omissions: [
        'No delimitar ni supervisar suficientemente el alcance de seguridad, acceso, llaves y mantenimiento.',
        'No recuperar después del aviso el control, proteger los patrimonios LPB/no-LPB, preservar la explotación y exigir cuentas.',
        'No completar o preservar la salida financiada ni informar íntegramente al Juzgado de la alteración material alegada.'
      ],
      allegation: 'Acusación directa de Gil Marer: el AC habría suministrado y utilizado la vía de autoridad, coordinado por correos y reuniones, autorizado accesos y medidas, adoptado o ratificado resultados y omitido delimitar, supervisar, restaurar y rendir cuentas, habilitando conscientemente la administración de hecho alegada.',
      boundary: 'Prueba contraria obligatoria: el AC negó haber ordenado la toma principal de cerraduras y describió una autorización más estrecha de mantenimiento/supervisión. Deben probarse alcance, primer aviso, capacidad, deber, conocimiento, intención, contribución causal y toda medida protectora o restaurativa.'
    },
    judge: {
      role: 'MAGISTRADO-JUEZ · SUPERVISIÓN Y TUTELA JUDICIAL EFECTIVA',
      name: 'Alberto López Villarrubia',
      image: asset('actors/alberto-lopez-villarrubia.jpg'),
      imageAlt: 'Alberto López Villarrubia',
      copy: 'Gil sostiene que el problema no se reduce a resoluciones desfavorables: el test es conocimiento → competencia → remedio disponible → acto, negativa, cierre, demora u omisión → efecto sobre activo, explotación, salida y derechos extraconcursales.',
      commissions: [
        'Dictar resoluciones, negativas o direcciones procesales que Gil alega preservaron o legitimaron el resultado de control privado.',
        'Mantener un curso procesal que no dio eficacia a la salida financiable tras el aviso profesional comunicado en junio de 2018.',
        'Dejar sin conciliación material cuestiones de control, título, rescate y causalidad que Gil califica como habilitación judicial afirmativa.'
      ],
      omissions: [
        'No otorgar protección efectiva y oportuna frente al cambio de control material alegado.',
        'No preservar el hotel operativo y las rutas ONA, financiación puente/bancaria o venta.',
        'No exigir cuenta completa de acceso, cerraduras, seguridad, obras, ingresos, control ni revertir el resultado cuando aún habría remedio.'
      ],
      allegation: 'Acusación directa de Gil Marer: resoluciones, negativas, cierres probatorios, demoras y omisiones habrían preservado el mecanismo privado y saboteado o frustrado una salida desarrollada, multivía y respaldada por financiación. Gil lo califica como prevaricación consciente en las modalidades jurídicamente aplicables.',
      boundary: 'Prueba contraria obligatoria: el informe Irigoyen no es acta judicial; las rutas tenían condiciones; constan la suspensión de 26 de junio de 2018, la no convalidación de 24 de octubre de 2019 y aspectos parcialmente favorables en 2021. Resolución adversa, error o demora no prueban por sí solos prevaricación, propósito o causalidad.'
    },
    linkageK: 'MATRIZ DE VINCULACIÓN ACTOR POR ACTOR',
    linkageT: 'Conducta privada alegada → comisión/omisión del AC → acto/omisión judicial → prueba que debe cerrar el enlace',
    linkageB: 'Cada fila impide dos errores opuestos: borrar la acusación por falta de una pieza o transferir automáticamente a una persona los actos de otra. No se publica una asociación abstracta; se exige un puente documental individualizado.',
    linkageLabels: ['Actor privado', 'Función/conducta privada alegada', 'Vínculo AC: actos, comisiones y omisiones', 'Vínculo judicial: actos y omisiones', 'Límite y prueba decisiva'],
    linkageRows: [
      {
        name: 'Francisco Mario Matos Matas',
        private: 'Administración comunitaria, registros, deuda/voto, custodia, seguridad, cuentas, información y continuidad/beneficio posteriores.',
        ac: 'Gil vincula la petición/uso de la ruta Comunidad–seguridad, reuniones y certificados/deuda con la falta de verificación independiente de autoridad, alcance y exactitud y con la falta de restitución o cuenta tras el aviso.',
        judge: 'Gil vincula resoluciones, negativas, cierres y demoras con la permanencia sin resolver de autoridad comunitaria, deuda/voto, acceso y efectos. No está probado que FMMM procurara una decisión judicial.',
        proof: 'Instrucciones nativas, órdenes a proveedores, papel físico exacto, conocimiento, propósito y beneficio. Orion/AGM posterior no prueba el acuerdo anterior.'
      },
      {
        name: 'Antonio Cogolludo Rojas',
        private: 'Relevo de autoridad como presidente/representante y participación directa alegada en seguridad, acceso, llaves e implementación del 7 de junio.',
        ac: 'Gil enlaza la solicitud/ratificación de seguridad usando la posición LPB con la falta de delimitación del mandato del presidente y proveedores, supervisión del acceso y reversión después del exceso denunciado.',
        judge: 'Gil enlaza la falta de examen y remedio sobre mandato, proveedores, presencia e instrucciones con la consolidación del resultado. No está probado que Antonio procurara o conociera una decisión judicial.',
        proof: 'Comunicaciones exactas, límites del mandato, orden a seguridad/cerrajero, presencia y conducta, conocimiento e intención.'
      },
      {
        name: 'Shaila María Cogolludo Ramos',
        private: 'Continuidad administrativa Pamanil/Comunidad, comunicaciones, tesorería, cuentas, voto y posible habilitación individual.',
        ac: 'Gil vincula el uso de deuda, cuentas, actas o certificados comunitarios con no verificar autoría, capacidad, exactitud y efecto, ni separar su conducta personal de la de FMMM, Antonio o sociedades.',
        judge: 'Gil vincula cierres o falta de producción de registros nativos con la ausencia de una atribución persona por persona. No existe transferencia automática de actos familiares o societarios.',
        proof: 'Instrucción/presencia exacta en 2018, documentos preparados o transmitidos, autoridad, conocimiento, beneficio e intención.'
      },
      {
        name: 'José Daniel Acosta Matos',
        private: 'Planificación, aproximaciones previas, coordinación de la ruta acreedor/proyecto, financiación, futura explotación, presidencia comunitaria posterior y resultado.',
        ac: 'Gil vincula correos, reuniones, autorizaciones y posiciones de liquidación con el puente alegado entre crédito/proyecto y control; acusa no separar derechos de acreedor de autoridad sobre el hotel completo y terceros.',
        judge: 'Gil enlaza el aviso profesional del 13 de junio sobre la salida con decisiones y omisiones posteriores que habrían preservado control/proyecto y bloqueado dependencias institucionales. No está probado que JDAM procurara esas decisiones.',
        proof: 'Comunicaciones y mandato nativos, puente planificación–orden operativa, conocimiento y propósito. Su presencia física el 7 de junio no está establecida.'
      },
      {
        name: 'Laura Patricia Acosta Matos',
        private: 'Papel jurídico/concursal CAM, acceso, participación e instrucción directa alegadas el 7 de junio y continuidad CAM/HNT posterior.',
        ac: 'Gil vincula autorizaciones de entrada/acceso y la ruta de seguridad/mantenimiento con la adopción o falta de reversión tras puerta forzada y cerraduras. La comunicación exacta AC–LPAM y su mandato deben producirse.',
        judge: 'Gil enlaza falta de tutela, investigación y remedio sobre la atribución contemporánea y la posterior continuidad con el resultado consolidado. No está probado contacto impropio, procura o conocimiento judicial por LPAM.',
        proof: 'Mandato, presencia, instrucción exacta, registros de llamadas/mensajes, conocimiento y propósito. La identidad narrativa correcta no reescribe el literal fuente «Laura Matos».'
      }
    ],
    linkageBoundary: 'NINGUNA FILA DECLARA CULPABILIDAD. La acusación directa se conserva; cada vínculo exige prueba de capacidad, acto propio, conocimiento, deber, intención, causalidad y beneficio. El archivo provisional de 2018 y su confirmación, la negativa del AC, los derechos crediticios/títulos válidos de CAM, la adjudicación posterior y cada acto judicial correctivo deben leerse en su alcance exacto.',
    evidence: [
      {
        src: asset('evidence/email-used-20260822/pwc-five-actors-plus-ac-2016-knowledge-checkpoint-ES.png'),
        alt: 'Gráfico documental de cinco actores privados y Administrador Concursal en el punto de conocimiento profesional comunicado a PwC en 2016',
        caption: 'Índice visual controlado por fuentes: cinco actores privados + AC + aviso profesional de 2016. Orienta la lectura; no determina culpabilidad.'
      },
      {
        src: asset('acosta-matos-family-hotel-plans.jpg'),
        alt: 'Cuatro personas alrededor de una mesa con planos y diseños ante el logotipo de Acosta Matos',
        caption: 'Imagen reproducida por El Economista/RICPE. Gil identifica a José Daniel y Laura Patricia en la escena y asume esa atribución editorial; la imagen no prueba por sí sola título, mandato, delito o coordinación.'
      }
    ],
    hingeK: '7 JUN 2018 · BISAGRA DE CONTROL MATERIAL',
    hingeT: 'El expediente público describe cerradura rota, cadenas, candados, bombines sustituidos, seguridad y exclusión. Gil Marer alega que fue una toma forzosa y destructiva del control hotelero dentro de un mecanismo económico más amplio. No se ha localizado un auto de posesión o desalojo a favor de CAM; “no localizado” no significa inexistente.',
    chainK: 'LA CADENA QUE DEBE RECONCILIARSE',
    chainT: 'Título → autoridad → deuda/voto → acceso → valoración/obras → capital → operación/ingresos → beneficiario',
    steps: [
      ['TÍTULO', '¿Quién era titular de cada finca?'],
      ['AUTORIDAD COMUNIDAD', '¿Quién podía representar, votar y obligar?'],
      ['DEUDA / VOTO', '¿Qué deuda fue verificada y qué voto fue excluido?'],
      ['ACCESO', '¿Quién ordenó, ejecutó o toleró el control material?'],
      ['VALORACIÓN / OBRAS', '¿Qué perímetro se valoró, reformó o presentó?'],
      ['CAPITAL', '¿Qué se dijo a inversores, financiadores y autoridades?'],
      ['OPERACIÓN / INGRESOS', '¿Quién explotó, cobró y asumió obligaciones?'],
      ['BENEFICIARIO / RESULTADO', '¿Quién recibió propiedad, control, valor e ingresos?']
    ],
    noticeK: '2016 · PUNTO DE CONOCIMIENTO PROFESIONAL',
    noticeQ: '“LA VÍA PENAL CONTRA ESTA GENTE”',
    noticeT: 'Mientras PwC/Carlos Saavedra asesoraban sobre Sun Park y la controversia comunitaria, el cliente comunicó alegaciones graves y dio una instrucción expresa de acudir a la vía penal. PwC respondió «Tomamos nota de vuestra decisión» —Carlos en copia— y después confirmó contacto directo con el AC.',
    noticeB: 'Esto acredita aviso contemporáneo a asesores externos. No prueba que PwC adoptara las alegaciones como propias ni que transmitiera al AC todo su contenido.',
    legend: ['FECHA MÍNIMA VERIFICADA', 'ALEGACIÓN DIRECTA ATRIBUIDA', 'PRUEBA CONTRARIA OBLIGATORIA', 'PRUEBA DECISIVA PENDIENTE'],
    links: { takeover: '7 junio 2018', ac: 'Expediente AC', court: 'Matriz judicial', accountability: 'Responsabilidad institucional', actors: 'Registro de actores', pwc: 'PwC 2016', ricpe: 'RICPE / Sun Park' },
    correction: 'Derecho de respuesta, corrección, aportación exculpatoria y contradicción abierto para cada persona y entidad. Relación no equivale a responsabilidad; prueba pendiente no borra la acusación.'
  } : {
    eyebrow: 'CONTROLLING CRIMINAL ALLEGATION · FIVE PRIVATE ACTORS + ADMINISTRATOR + JUDGE',
    title: 'Five actors, the Insolvency Administrator and the Judge: separate functions, one chain that must be proved.',
    intro: 'Gil Marer directly accuses five private individuals of having formed, by 2018 at the latest, a coordinated de facto or shadow-administration structure over Luchy Playa Blanca’s patrimonial and business sphere and the integrated hotel platform. He separately attributes affirmative acts, commissions and omissions to the Insolvency Administrator and Judge that allegedly enabled, preserved and consolidated the mechanism.',
    criminalK: 'CONTROLLING CRIMINAL FORMULATION · PUBLISHED BY GIL MARER',
    criminalT: 'The allegation is not mere passivity: it alleges instruction, execution, enablement, adoption, ratification and sabotage of the exit.',
    criminalB: 'The allegation connects debt and voting, access and security, keys, maintenance, works and valuation, information, insolvency strategy, operation, income, title and result. Gil says Aweswell performed or could perform the conditions within its control and that the operative blockage concerned preserving and delivering security/collateral, obtaining the debt figure and insolvency/judicial authority, and maintaining access, operation and valuation. It is a direct allegation, not a judgment or proof of drawdown or common purpose.',
    context: {
      home: 'Principal view of the economic mechanism, its five private actors and two institutional control points.',
      pwc: 'Connects professional knowledge in 2016 with later confirmed PwC–Administrator contact.',
      ricpe: 'Connects the Community/control history with later title, diligence, capital and RICPE-operation questions.',
      ac: 'Separates the Administrator from the private perimeter and tests knowledge → power/duty → commission/omission → consequence.',
      takeover: 'Places 7 June 2018 as the material-control hinge inside the alleged chain.',
      accountability: 'Separates the private perimeter, insolvency control and judicial review to prevent guilt by association.'
    },
    privateK: 'IDENTIFIED PRIVATE PERIMETER · 5',
    privateT: 'Five alleged de facto or shadow administrators in a functional chain',
    privateB: 'Gil alleges coordinated action but does not automatically attribute every act to all five. Function, authority, knowledge, instruction, intent, benefit and causation must be proved person by person. Kinship or corporate connection does not replace that proof.',
    locked: 'LOCKED MINIMUM DATES: they establish involvement no later than the date shown; they do not assert that it was the true first day.',
    actors: [
      {
        n: '01',
        name: 'Francisco Mario Matos Matas',
        stage: '22 JUN 2011 → ADMINISTRATION / CUSTODY',
        rel: 'HUSBAND OF SHAILA MARÍA COGOLLUDO RAMOS',
        text: 'The 22 June 2011 minutes identify him as Community Administrator. Gil attributes continuity in debt, voting, accounts, information, access and material implementation within the alleged de facto structure. Liability requires his own acts, not kinship.',
        image: asset('actors/francisco-mario-matos-matas.jpg'),
        imageAlt: 'Francisco Mario Matos Matas',
        imageNote: 'Canonical repository identity asset; not identified through facial inference.'
      },
      {
        n: '02',
        name: 'Antonio Cogolludo Rojas',
        stage: '10 APR 2014 → REPRESENTATION / COMMUNITY',
        rel: 'FATHER OF SHAILA MARÍA COGOLLUDO RAMOS',
        text: 'The 10 April 2014 notarial record identifies him as Cristina Molina Petit’s representative. Gil later attributes presidency, access, key, security and implementation functions. Every act and date remains subject to proof.'
      },
      {
        n: '03',
        name: 'Shaila María Cogolludo Ramos',
        stage: '8 APR 2014 → COMMUNICATIONS / ADMINISTRATION',
        rel: 'DAUGHTER OF ANTONIO COGOLLUDO ROJAS · WIFE OF FMMM',
        text: 'A Pamanil communication dated 8 April 2014 appears signed by FMMM and Shaila. Pamanil/Community continuity and the 2018 voting and treasury node support the material-administration function Gil attributes to her.'
      },
      {
        n: '04',
        name: 'José Daniel Acosta Matos',
        stage: '2017–2018 → PROJECT / CONTROL',
        text: 'Documented entry into the CAM/Community perimeter, pre-7 June visits and Community presidency in 2022. Gil attributes planning, finance, control, future operation and outcome—not physical presence on 7 June.'
      },
      {
        n: '05',
        name: 'Laura Patricia Acosta Matos',
        stage: '2017–2018 → LEGAL / INSOLVENCY / SUCCESSION',
        text: 'Legal and insolvency role, access, CAM representation and later Hotel New Trend continuity. Gil attributes instructions and direct control functions; identity, mandate, presence and precise act remain separate fields.'
      }
    ],
    institutionalK: 'IMMEDIATELY BELOW · TWO SEPARATE INSTITUTIONAL NODES',
    institutionalT: 'Insolvency Administrator and Judge: images, functions, commissions, omissions and boundaries',
    institutionalB: 'They are not a sixth and seventh private actor. Their legal functions were distinct. The matrix links each private act to the knowledge, power/duty, affirmative act or omission and consequence attributed to each institutional node.',
    commissionK: 'ALLEGED AFFIRMATIVE ACTS / COMMISSIONS',
    omissionK: 'ALLEGED OMISSIONS',
    ac: {
      role: 'INSOLVENCY ADMINISTRATOR · FIDUCIARY GATEKEEPER · PROCEEDING 36/2012',
      name: 'Francisco de Borja Rodríguez-Batllori Laffitte',
      image: asset('actors/francisco-de-borja-rodriguez-batllori.jpg'),
      imageAlt: 'Francisco de Borja Rodríguez-Batllori Laffitte, Insolvency Administrator in Proceeding 36/2012',
      copy: 'His relevance depends on what he verified, requested, authorised, transmitted, implemented, adopted, ratified, tolerated, reported, preserved or tried to reverse while administering LPB’s estate—not on personally carrying out every private act.',
      commissions: [
        'Using LPB’s majority position to advance the 18 May 2018 Community security and access route.',
        'Participating in emails, meetings, requests and authorisations used for access, supervision or maintenance.',
        'Adopting or ratifying the later access/lock result and using Community debt, certificate or calculation inputs.'
      ],
      omissions: [
        'Failing adequately to delimit and supervise security, access, keys and maintenance.',
        'Failing after notice to recover control, protect LPB/non-LPB property, preserve operation and require an account.',
        'Failing to complete or preserve the finance-backed exit or fully report the alleged material change to the Court.'
      ],
      allegation: 'Gil Marer’s direct allegation: the Administrator supplied and used the authority route, coordinated through emails and meetings, authorised access and measures, adopted or ratified results, and omitted delimitation, supervision, restoration and accounting, thereby knowingly enabling the alleged de facto administration.',
      boundary: 'Mandatory contrary record: the Administrator denied ordering the principal lock takeover and described narrower maintenance/supervision authority. Scope, first notice, capacity, duty, knowledge, intent, causal contribution and every protective or restorative measure require proof.'
    },
    judge: {
      role: 'JUDGE · SUPERVISION AND EFFECTIVE JUDICIAL PROTECTION',
      name: 'Alberto López Villarrubia',
      image: asset('actors/alberto-lopez-villarrubia.jpg'),
      imageAlt: 'Alberto López Villarrubia',
      copy: 'Gil says the issue is not merely adverse rulings. The test is knowledge → competence → available remedy → act, refusal, closure, delay or omission → effect on the asset, operation, exit and non-estate rights.',
      commissions: [
        'Issuing rulings, refusals or procedural directions that Gil alleges preserved or legitimised the private-control result.',
        'Maintaining a procedural course that did not give effect to the financeable exit after the professional notice reported in June 2018.',
        'Leaving material-control, title, rescue and causation issues unreconciled in ways Gil characterises as affirmative judicial enablement.'
      ],
      omissions: [
        'Failing to provide timely effective protection against the alleged material change of control.',
        'Failing to preserve the operating hotel and ONA, bridge/bank-finance or sale routes.',
        'Failing to require a complete account of access, locks, security, works, income and control, or reverse the result while a remedy allegedly remained.'
      ],
      allegation: 'Gil Marer’s direct allegation: rulings, refusals, evidential closures, delay and omissions preserved the private mechanism and sabotaged or frustrated a developed, multi-route, finance-backed exit. Gil characterises this as knowing judicial prevarication in the legally applicable forms.',
      boundary: 'Mandatory contrary record: Irigoyen’s report is not a judicial minute; the routes had conditions; the 26 June 2018 suspension, 24 October 2019 non-validation and partly favourable 2021 aspects are material. An adverse ruling, error or delay does not by itself prove prevarication, purpose or causation.'
    },
    linkageK: 'ACTOR-BY-ACTOR LINKAGE MATRIX',
    linkageT: 'Alleged private conduct → Administrator commission/omission → judicial act/omission → proof needed to close the link',
    linkageB: 'Every row prevents two opposite errors: erasing the allegation because one item is missing, or automatically transferring one person’s acts to another. This is not abstract association; it demands an individual documentary bridge.',
    linkageLabels: ['Private actor', 'Alleged private function/conduct', 'Administrator link: acts, commissions and omissions', 'Judicial link: acts and omissions', 'Boundary and decisive proof'],
    linkageRows: [
      {
        name: 'Francisco Mario Matos Matas',
        private: 'Community administration, records, debt/voting, custody, security, accounts, information and later continuity/benefit.',
        ac: 'Gil links the request/use of the Community–security route, meetings and debt/certificates with failure independently to verify authority, scope and accuracy and failure to restore or account after notice.',
        judge: 'Gil links rulings, refusals, closures and delay with Community authority, debt/voting, access and effects remaining unresolved. It is not proved that FMMM procured a judicial decision.',
        proof: 'Native instructions, provider orders, exact physical role, knowledge, purpose and benefit. Later Orion/AGM association does not prove the earlier agreement.'
      },
      {
        name: 'Antonio Cogolludo Rojas',
        private: 'Authority relay as president/representative and alleged direct participation in security, access, keys and 7 June implementation.',
        ac: 'Gil links the security request/ratification using LPB’s position with failure to delimit the president/provider mandate, supervise access and reverse the alleged excess after notice.',
        judge: 'Gil links the lack of examination and remedy concerning mandate, providers, presence and instructions with consolidation of the result. It is not proved that Antonio procured or knew of a judicial decision.',
        proof: 'Exact communications, mandate limits, security/locksmith orders, presence and conduct, knowledge and intent.'
      },
      {
        name: 'Shaila María Cogolludo Ramos',
        private: 'Pamanil/Community administrative continuity, communications, treasury, accounts, voting and possible individual enablement.',
        ac: 'Gil links use of Community debt, accounts, minutes or certificates with failure to verify authorship, capacity, accuracy and effect, or separate her conduct from FMMM, Antonio or companies.',
        judge: 'Gil links closures or failure to produce native records with the absence of person-by-person attribution. Family or corporate acts do not transfer automatically.',
        proof: 'Exact 2018 instruction/presence, documents prepared or transmitted, authority, knowledge, benefit and intent.'
      },
      {
        name: 'José Daniel Acosta Matos',
        private: 'Planning, prior approaches, creditor/project-route coordination, finance, future operation, later Community presidency and outcome.',
        ac: 'Gil links emails, meetings, authorisations and liquidation positions with the alleged bridge from credit/project to control; he alleges failure to separate creditor rights from whole-hotel and third-party authority.',
        judge: 'Gil links the 13 June professional notice about the exit with later decisions and omissions allegedly preserving control/project and blocking institutional dependencies. It is not proved that JDAM procured those decisions.',
        proof: 'Native communications and mandate, planning-to-operative-order bridge, knowledge and purpose. His physical presence on 7 June is not established.'
      },
      {
        name: 'Laura Patricia Acosta Matos',
        private: 'CAM legal/insolvency role, access, alleged direct participation and instruction on 7 June, and later CAM/HNT continuity.',
        ac: 'Gil links entry/access authorisations and the security/maintenance route with adoption or failure to reverse after a forced door and changed locks. The exact Administrator–LPAM communication and mandate must be produced.',
        judge: 'Gil links lack of protection, investigation and remedy concerning the contemporaneous attribution and later continuity with the consolidated result. Improper contact, procurement or judicial knowledge by LPAM is not proved.',
        proof: 'Mandate, presence, exact instruction, call/message records, knowledge and purpose. The correct narrative identity does not rewrite the source literal “Laura Matos”.'
      }
    ],
    linkageBoundary: 'NO ROW DECLARES GUILT. The direct allegation is preserved; each link requires proof of capacity, personal act, knowledge, duty, intent, causation and benefit. The 2018 provisional dismissal and confirmation, the Administrator’s denial, CAM’s valid credit/titles, later adjudication and every corrective judicial act must be read within their exact scope.',
    evidence: [
      {
        src: asset('evidence/email-used-20260822/pwc-five-actors-plus-ac-2016-knowledge-checkpoint-EN.png'),
        alt: 'Documentary graphic of five private actors and the Insolvency Administrator at the professional-knowledge checkpoint communicated to PwC in 2016',
        caption: 'Source-controlled visual index: five private actors + Administrator + 2016 professional notice. It orients the record; it does not determine guilt.'
      },
      {
        src: asset('acosta-matos-family-hotel-plans.jpg'),
        alt: 'Four people around a table with plans and designs in front of an Acosta Matos logo',
        caption: 'Image reproduced by El Economista/RICPE. Gil identifies José Daniel and Laura Patricia in the scene and assumes that editorial attribution; the image alone does not prove title, mandate, wrongdoing or coordination.'
      }
    ],
    hingeK: '7 JUN 2018 · MATERIAL-CONTROL HINGE',
    hingeT: 'The public record describes a broken lock, chains, padlocks, replacement cylinders, security and exclusion. Gil Marer alleges a forcible and destructive takeover of hotel control within a broader economic mechanism. No CAM possession or eviction order has been located; “not located” does not mean nonexistent.',
    chainK: 'THE CHAIN THAT MUST BE RECONCILED',
    chainT: 'Title → authority → debt/voting → access → valuation/works → capital → operation/income → beneficiary',
    steps: [
      ['TITLE', 'Who owned each property?'],
      ['COMMUNITY AUTHORITY', 'Who could represent, vote and bind?'],
      ['DEBT / VOTING', 'What debt was verified and what vote excluded?'],
      ['ACCESS', 'Who ordered, carried out or tolerated material control?'],
      ['VALUATION / WORKS', 'What perimeter was valued, altered or presented?'],
      ['CAPITAL', 'What was said to investors, funders and authorities?'],
      ['OPERATION / INCOME', 'Who operated, collected and assumed obligations?'],
      ['BENEFICIARY / RESULT', 'Who received title, control, value and income?']
    ],
    noticeK: '2016 · PROFESSIONAL-KNOWLEDGE CHECKPOINT',
    noticeQ: '“THE CRIMINAL ROUTE AGAINST THESE PEOPLE”',
    noticeT: 'While PwC/Carlos Saavedra advised on Sun Park and the Community dispute, the client communicated grave allegations and expressly instructed a criminal route. PwC replied that it took note of the decision—with Carlos copied—and later confirmed direct contact with the Administrator.',
    noticeB: 'This proves contemporaneous notice to external advisers. It does not prove that PwC adopted the allegations as its own or transmitted their full contents to the Administrator.',
    legend: ['VERIFIED MINIMUM DATE', 'ATTRIBUTED DIRECT ALLEGATION', 'MANDATORY CONTRARY RECORD', 'DECISIVE PROOF OUTSTANDING'],
    links: { takeover: '7 June 2018', ac: 'Administrator record', court: 'Judicial matrix', accountability: 'Institutional accountability', actors: 'Actor register', pwc: 'PwC 2016', ricpe: 'RICPE / Sun Park' },
    correction: 'Right of reply, correction, exculpatory production and challenge remains open to every person and entity. Relationship is not responsibility; missing proof does not erase the allegation.'
  };

  const contextKey = isPwc ? 'pwc'
    : isRicpe ? 'ricpe'
      : isAc ? 'ac'
        : isTakeover ? 'takeover'
          : isAccountability ? 'accountability'
            : 'home';
  const context = c.context[contextKey];
  const esc = (value) => String(value).replace(/[&<>"']/g, (char) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
  }[char]));

  const ensureStyle = () => {
    if (d.querySelector('link[data-pd-five-ac-css]')) return;
    const link = d.createElement('link');
    link.rel = 'stylesheet';
    link.href = asset('five-actor-accountability-20260824.css?v=20260824b');
    link.dataset.pdFiveAcCss = '20260824b';
    d.head.appendChild(link);
  };

  const portrait = (actor) => actor.image ? `
    <span class="pd-five-ac__portrait-wrap">
      <img class="pd-five-ac__portrait" src="${esc(actor.image)}" alt="${esc(actor.imageAlt)}" loading="eager" decoding="async">
      <small class="pd-five-ac__portrait-note">${esc(actor.imageNote)}</small>
    </span>` : '';

  const actorCards = c.actors.map((actor) => `
    <article class="pd-five-ac__card" data-number="${esc(actor.n)}" data-private-actor-card="${esc(actor.n)}">
      ${portrait(actor)}
      <span class="pd-five-ac__stage">${esc(actor.stage)}</span>
      <strong class="pd-five-ac__name">${esc(actor.name)}</strong>
      ${actor.rel ? `<span class="pd-five-ac__rel">${esc(actor.rel)}</span>` : ''}
      <span class="pd-five-ac__copy">${esc(actor.text)}</span>
    </article>`).join('');

  const institutionCard = (node, type) => `
    <article class="pd-five-ac__institution-card" data-institution-card="${type}">
      <div class="pd-five-ac__institution-person">
        <img class="pd-five-ac__institution-portrait" src="${esc(node.image)}" alt="${esc(node.imageAlt)}" loading="eager" decoding="async">
        <div>
          <span class="pd-five-ac__institution-role">${esc(node.role)}</span>
          <strong class="pd-five-ac__institution-name">${esc(node.name)}</strong>
          <p class="pd-five-ac__institution-copy">${esc(node.copy)}</p>
        </div>
      </div>
      <div class="pd-five-ac__accountability-columns">
        <div class="pd-five-ac__accountability-column"><strong>${esc(c.commissionK)}</strong><ul>${node.commissions.map((item) => `<li>${esc(item)}</li>`).join('')}</ul></div>
        <div class="pd-five-ac__accountability-column"><strong>${esc(c.omissionK)}</strong><ul>${node.omissions.map((item) => `<li>${esc(item)}</li>`).join('')}</ul></div>
      </div>
      <p class="pd-five-ac__institution-allegation">${esc(node.allegation)}</p>
      <p class="pd-five-ac__institution-boundary">${esc(node.boundary)}</p>
    </article>`;

  const steps = c.steps.map(([heading, text]) => `<li><strong>${esc(heading)}</strong><span>${esc(text)}</span></li>`).join('');
  const legend = c.legend.map((item) => `<span>${esc(item)}</span>`).join('');
  const linkageHead = `<div class="pd-five-ac__linkage-row pd-five-ac__linkage-row--head">${c.linkageLabels.map((label) => `<span class="pd-five-ac__linkage-cell">${esc(label)}</span>`).join('')}</div>`;
  const linkageRows = c.linkageRows.map((row) => `
    <div class="pd-five-ac__linkage-row" data-linkage-row>
      <span class="pd-five-ac__linkage-cell" data-label="${esc(c.linkageLabels[0])}"><strong class="pd-five-ac__linkage-actor">${esc(row.name)}</strong></span>
      <span class="pd-five-ac__linkage-cell" data-label="${esc(c.linkageLabels[1])}">${esc(row.private)}</span>
      <span class="pd-five-ac__linkage-cell" data-label="${esc(c.linkageLabels[2])}">${esc(row.ac)}</span>
      <span class="pd-five-ac__linkage-cell" data-label="${esc(c.linkageLabels[3])}">${esc(row.judge)}</span>
      <span class="pd-five-ac__linkage-cell" data-label="${esc(c.linkageLabels[4])}">${esc(row.proof)}</span>
    </div>`).join('');
  const evidence = c.evidence.map((item) => `
    <figure><img src="${esc(item.src)}" alt="${esc(item.alt)}" loading="lazy" decoding="async"><figcaption>${esc(item.caption)}</figcaption></figure>`).join('');

  const build = () => {
    const section = d.createElement('section');
    section.className = 'pd-five-ac';
    section.dataset.pdFiveAc = '20260824b';
    section.dataset.fiveActorAccountabilityStatic = 'enhanced';
    section.setAttribute('aria-labelledby', 'pd-five-ac-title');
    section.innerHTML = `
      <header class="pd-five-ac__head">
        <p class="pd-five-ac__eyebrow">${esc(c.eyebrow)}</p>
        <h2 id="pd-five-ac-title">${esc(c.title)}</h2>
        <p>${esc(c.intro)}</p>
        <span class="pd-five-ac__context">${esc(context)}</span>
      </header>
      <div class="pd-five-ac__criminal" role="note"><small>${esc(c.criminalK)}</small><strong>${esc(c.criminalT)}</strong><p>${esc(c.criminalB)}</p></div>
      <div class="pd-five-ac__legend" aria-label="Evidence-status legend">${legend}</div>
      <div class="pd-five-ac__private">
        <div class="pd-five-ac__private-head"><span class="pd-five-ac__count" aria-hidden="true">5</span><div><span class="pd-five-ac__eyebrow">${esc(c.privateK)}</span><h3>${esc(c.privateT)}</h3></div><p>${esc(c.privateB)}</p></div>
        <div class="pd-five-ac__cards">${actorCards}</div>
        <p class="pd-five-ac__lock">${esc(c.locked)}</p>
      </div>
      <section class="pd-five-ac__institutional" aria-labelledby="pd-five-ac-institutional-title">
        <header class="pd-five-ac__institutional-head"><span class="pd-five-ac__eyebrow">${esc(c.institutionalK)}</span><h3 id="pd-five-ac-institutional-title">${esc(c.institutionalT)}</h3><p>${esc(c.institutionalB)}</p></header>
        <div class="pd-five-ac__institutional-grid">${institutionCard(c.ac, 'administrator')}${institutionCard(c.judge, 'judge')}</div>
      </section>
      <section class="pd-five-ac__linkage" aria-labelledby="pd-five-ac-linkage-title">
        <header class="pd-five-ac__linkage-head"><span class="pd-five-ac__eyebrow">${esc(c.linkageK)}</span><h3 id="pd-five-ac-linkage-title">${esc(c.linkageT)}</h3><p>${esc(c.linkageB)}</p></header>
        <div class="pd-five-ac__linkage-table" role="table" aria-label="${esc(c.linkageT)}">${linkageHead}${linkageRows}</div>
        <p class="pd-five-ac__linkage-boundary">${esc(c.linkageBoundary)}</p>
      </section>
      <div class="pd-five-ac__evidence-visuals">${evidence}</div>
      <div class="pd-five-ac__hinge"><strong>${esc(c.hingeK)}</strong><p>${esc(c.hingeT)}</p></div>
      <div class="pd-five-ac__chain"><div class="pd-five-ac__chain-head"><small>${esc(c.chainK)}</small><strong>${esc(c.chainT)}</strong></div><ol class="pd-five-ac__steps">${steps}</ol></div>
      <div class="pd-five-ac__notice"><div><span class="pd-five-ac__notice-k">${esc(c.noticeK)}</span><strong class="pd-five-ac__notice-q">${esc(c.noticeQ)}</strong><p>${esc(c.noticeT)}</p></div><p class="pd-five-ac__notice-boundary">${esc(c.noticeB)}</p></div>
      <footer class="pd-five-ac__footer"><nav class="pd-five-ac__links" aria-label="Five actors, Administrator and Judge evidence routes"><a href="${routes.takeover}">${esc(c.links.takeover)}</a><a href="${routes.ac}">${esc(c.links.ac)}</a><a href="${routes.court}">${esc(c.links.court)}</a><a href="${routes.accountability}">${esc(c.links.accountability)}</a><a href="${routes.actors}">${esc(c.links.actors)}</a><a href="${routes.pwc}">${esc(c.links.pwc)}</a><a href="${routes.ricpe}">${esc(c.links.ricpe)}</a></nav><p class="pd-five-ac__correction">${esc(c.correction)}</p></footer>`;
    return section;
  };

  const announceReady = () => d.dispatchEvent(new CustomEvent('pd:five-actor-visual-ready', {
    detail: { marker: '20260824b' }
  }));

  const mountHome = () => {
    const oldIntro = d.querySelector('.actor-intro');
    const oldGrid = d.querySelector('.actor-grid');
    if (!oldIntro || !oldGrid) return false;
    const section = build();
    const oldId = oldIntro.id;
    if (oldId) {
      oldIntro.removeAttribute('id');
      section.id = oldId;
    }
    oldIntro.hidden = true;
    oldIntro.setAttribute('aria-hidden', 'true');
    oldGrid.hidden = true;
    oldGrid.setAttribute('aria-hidden', 'true');
    oldIntro.insertAdjacentElement('beforebegin', section);
    announceReady();
    return true;
  };

  const mountPage = () => {
    const hero = d.querySelector('.dossier-hero, main > .hero, .hero');
    if (!hero) return false;
    const thesis = d.querySelector('[data-calificacion-misuse-thesis]');
    (thesis || hero).insertAdjacentElement('afterend', build());
    announceReady();
    return true;
  };

  const render = () => {
    ensureStyle();
    if (d.querySelector('section[data-pd-five-ac]')) {
      announceReady();
      return;
    }
    if (isHome && mountHome()) return;
    mountPage();
  };

  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', render, { once: true });
  else render();
})();
