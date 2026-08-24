(()=>{
  const d=document;
  const path=location.pathname.replace(/\/+$/,'/');
  const es=/\/es\//.test(path);
  const isHome=/\/(en|es)\/$/.test(path);
  const isPwc=/\/(en|es)\/pwc-canarias-carlos-saavedra-sun-park\/$/.test(path);
  const isRicpe=/\/(en|es)\/ric-private-equity-sun-park\/$/.test(path);
  const isAc=/\/en\/insolvency-36-2012-insolvency-administrator\/$/.test(path)||/\/es\/concurso-36-2012-administrador-concursal\/$/.test(path);
  const isTakeover=/\/en\/sun-park-takeover-7-june-2018\/$/.test(path)||/\/es\/toma-control-sun-park-7-junio-2018\/$/.test(path);
  const isAccountability=/\/en\/insolvency-36-2012-institutional-accountability\/$/.test(path)||/\/es\/concurso-36-2012-responsabilidad-institucional\/$/.test(path);
  if(!isHome&&!isPwc&&!isRicpe&&!isAc&&!isTakeover&&!isAccountability)return;

  const base=es?'/por-derecho/es/':'/por-derecho/en/';
  const routes={
    actors:base+(es?'actores-partes-abogados-representantes/':'actors-parties-lawyers-representatives/'),
    ac:base+(es?'concurso-36-2012-administrador-concursal/':'insolvency-36-2012-insolvency-administrator/'),
    court:base+(es?'concurso-36-2012-juzgado-mercantil-1/':'insolvency-36-2012-mercantile-court-1/'),
    accountability:base+(es?'concurso-36-2012-responsabilidad-institucional/':'insolvency-36-2012-institutional-accountability/'),
    takeover:base+(es?'toma-control-sun-park-7-junio-2018/':'sun-park-takeover-7-june-2018/'),
    pwc:base+'pwc-canarias-carlos-saavedra-sun-park/',
    ricpe:base+'ric-private-equity-sun-park/'
  };

  const c=es?{
    eyebrow:'ACUSACIÓN PENAL RECTORA · CINCO ACTORES PRIVADOS + AC + JUEZ',
    title:'Cinco + AC + Juez: la administración de hecho y su habilitación institucional alegadas por Gil Marer.',
    intro:'Gil Marer acusa directamente a cinco personas privadas de haber formado, a más tardar en 2018, una estructura coordinada de administradores de hecho o en la sombra sobre la esfera patrimonial y empresarial de Luchy Playa Blanca y la plataforma hotelera integrada. Atribuye separadamente al Administrador Concursal y al Magistrado-Juez actos afirmativos y omisiones que habrían habilitado, preservado y consolidado el mecanismo.',
    criminalK:'FORMULACIÓN PENAL CONTROLANTE · PUBLICADA POR GIL MARER',
    criminalT:'No se alega mera pasividad: se alegan instrucción, ejecución, habilitación, adopción y sabotaje de la salida.',
    criminalB:'La acusación conecta deuda y voto, acceso y seguridad, llaves, mantenimiento, obras y valoración, información, estrategia concursal, operación, ingresos, título y resultado. Gil sostiene que Aweswell había cumplido o podía cumplir las condiciones bajo su control y que el obstáculo operativo estaba en preservar y entregar garantías/colateral, obtener cifra de deuda y autoridad concursal/judicial y mantener acceso, explotación y valoración. Alega que un aparato coercitivo de gobierno paralelo y control patrimonial, funcionalmente comparable a un acreedor en posesión, destruyó o bloqueó esos inputs para impedir el pago/refinanciación. ONA, Ben Oldman y Lagune/Elaia conservan su estado documental separado; la acusación no es sentencia ni prueba de desembolso.',
    context:{
      home:'Vista principal del mecanismo económico y de sus puntos de control documental.',
      pwc:'Esta vista conecta el conocimiento profesional de 2016 con el posterior contacto confirmado PwC–Administrador Concursal.',
      ricpe:'Esta vista conecta la historia de Comunidad/control con las posteriores preguntas de título, due diligence, capital y operación RICPE.',
      ac:'Esta vista separa al AC del perímetro privado y somete su papel a la secuencia conocimiento → poder → acto/omisión → consecuencia.',
      takeover:'Esta vista coloca el 7 de junio de 2018 como bisagra de control material dentro de la cadena alegada.',
      accountability:'Esta vista separa el perímetro privado, el control concursal y la revisión judicial para evitar atribuciones por asociación.'
    },
    privateK:'PERÍMETRO PRIVADO IDENTIFICADO · 5',
    privateT:'Cinco administradores de hecho o en la sombra alegados dentro de una cadena funcional',
    privateB:'Gil alega una actuación coordinada, pero no atribuye automáticamente cada acto a los cinco: función, autoridad, conocimiento, instrucción, intención, beneficio y causalidad deben probarse persona por persona. Parentesco o vínculo empresarial no sustituyen esa prueba.',
    locked:'FECHAS MÍNIMAS BLOQUEADAS: acreditan implicación no más tarde de la fecha indicada; no afirman que ese fuera el primer día real.',
    actors:[
      {n:'01',name:'Francisco Mario Matos Matas',stage:'22 JUN 2011 → ADMINISTRACIÓN / CUSTODIA',rel:'ESPOSO DE SHAILA MARÍA COGOLLUDO RAMOS',text:'El acta de 22 de junio de 2011 lo identifica como administrador de la Comunidad. Gil le atribuye continuidad en deuda, voto, cuentas, información, acceso y ejecución material dentro de la estructura de hecho alegada. La responsabilidad exige actos propios, no parentesco.'},
      {n:'02',name:'Antonio Cogolludo Rojas',stage:'10 ABR 2014 → REPRESENTACIÓN / COMUNIDAD',rel:'PADRE DE SHAILA MARÍA COGOLLUDO RAMOS',text:'El acta notarial de 10 de abril de 2014 lo identifica como representante de Cristina Molina Petit. Gil le atribuye después funciones de presidencia, acceso, llaves, seguridad e implementación. Cada acto y fecha siguen sometidos a prueba.'},
      {n:'03',name:'Shaila María Cogolludo Ramos',stage:'8 ABR 2014 → COMUNICACIONES / ADMINISTRACIÓN',rel:'HIJA DE ANTONIO COGOLLUDO ROJAS · ESPOSA DE FMMM',text:'Una comunicación Pamanil de 8 de abril de 2014 aparece firmada por FMMM y Shaila. La continuidad Pamanil/Comunidad y el nodo de voto y tesorería de 2018 sustentan la función de administración material que Gil le atribuye.'},
      {n:'04',name:'José Daniel Acosta Matos',stage:'2017–2018 → PROYECTO / CONTROL',text:'Entrada documentada en el perímetro CAM/Comunidad, visitas anteriores al 7 de junio y presidencia comunitaria en 2022. Gil le atribuye integración de proyecto, financiación, control, futura explotación y resultado; no presencia física el 7 de junio.'},
      {n:'05',name:'Laura Patricia Acosta Matos',stage:'2017–2018 → JURÍDICO / CONCURSO / SUCESIÓN',text:'Papel jurídico y concursal, acceso, representación CAM y continuidad posterior en Hotel New Trend. Gil le atribuye instrucciones y funciones directas de control; identidad, mandato, presencia y acto concreto permanecen como campos separados.'}
    ],
    hingeK:'7 JUN 2018 · BISAGRA DE CONTROL MATERIAL',
    hingeT:'El expediente público describe cerradura rota, cadenas, candados, bombines sustituidos, seguridad y exclusión. Gil Marer alega que ese episodio fue una toma forzosa y destructiva del control hotelero dentro de un mecanismo económico más amplio. Este diseño no convierte la alegación en sentencia penal; tampoco se ha localizado un auto de posesión o desalojo a favor de CAM.',
    chainK:'LA CADENA QUE DEBE RECONCILIARSE',
    chainT:'Título → autoridad → deuda/voto → acceso → valoración/obras → capital → operación/ingresos → beneficiario',
    steps:[
      ['TÍTULO','¿Quién era titular de cada finca?'],
      ['AUTORIDAD COMUNIDAD','¿Quién podía representar, votar y obligar?'],
      ['DEUDA / VOTO','¿Qué deuda fue verificada y qué voto fue excluido?'],
      ['ACCESO','¿Quién ordenó, ejecutó o toleró el control material?'],
      ['VALORACIÓN / OBRAS','¿Qué perímetro se valoró, reformó o presentó?'],
      ['CAPITAL','¿Qué se dijo a inversores, financiadores y autoridades?'],
      ['OPERACIÓN / INGRESOS','¿Quién explotó, cobró y asumió obligaciones?'],
      ['BENEFICIARIO / RESULTADO','¿Quién recibió propiedad, control, valor e ingresos?']
    ],
    acK:'+ AC · PUNTO DE CONTROL JUDICIALMENTE DESIGNADO',
    acName:'Francisco de Borja Rodríguez-Batllori Laffitte',
    acRole:'ADMINISTRADOR CONCURSAL · CONCURSO 36/2012',
    acIntro:'No es un sexto actor privado. Era el cargo legal con poder fiduciario dentro del concurso; Gil alega que su participación fue afirmativa y omisiva, no una mera falta de vigilancia.',
    acLenses:[
      ['CONOCIMIENTO','Qué conocía —y desde cuándo— sobre deuda comunitaria, título fragmentado, Matkator/terceros, control de 2018, auto de 2019, RICPE y explotación.'],
      ['PODER / DEBER','Qué podía o debía verificar, preservar, advertir, pedir, impugnar, corregir o someter al Juzgado dentro de sus funciones.'],
      ['ACTO / OMISIÓN / EFECTO','Qué pidió, comunicó, autorizó, decidió, implementó, adoptó, ratificó, dejó sin corregir o no revirtió; y qué consecuencia patrimonial siguió.']
    ],
    acAllegation:'Acusación directa de Gil Marer: el AC habría suministrado y utilizado la vía de autoridad, coordinado por correos y reuniones, autorizado accesos y medidas, adoptado o ratificado resultados y omitido delimitar, supervisar, restaurar y rendir cuentas, habilitando conscientemente la administración de hecho alegada.',
    acBoundary:'Límite: Gil formula una imputación penal expresa; la página no la convierte en hallazgo judicial. La negativa del AC y su relato de acceso limitado son prueba contraria obligatoria. Alcance, conocimiento, deber, intención, contribución causal y beneficio requieren prueba individual.',
    judicialK:'SUPERVISIÓN JUDICIAL / TUTELA JUDICIAL EFECTIVA',
    judicialT:'Gil atribuye directamente al Magistrado-Juez Alberto López Villarrubia no sólo omisiones, sino resoluciones, negativas, cierres probatorios y demoras que, junto con la falta de tutela y restauración, habrían preservado el control privado y saboteado o frustrado una salida desarrollada, multivía y respaldada por financiación. Gil lo califica como prevaricación judicial consciente en las modalidades jurídicamente aplicables. La reunión directa de Irigoyen documentada por su informe contemporáneo es la del 13 de junio de 2018; otras visitas siguen pendientes de prueba. La acusación no es una declaración judicial y cada acto exige matriz propia.',
    noticeK:'2016 · PUNTO DE CONOCIMIENTO PROFESIONAL',
    noticeQ:'“LA VÍA PENAL CONTRA ESTA GENTE”',
    noticeT:'Mientras PwC/Carlos Saavedra asesoraban sobre Sun Park y la controversia comunitaria, el cliente comunicó alegaciones graves y dio una instrucción expresa de acudir a la vía penal. PwC respondió «Tomamos nota de vuestra decisión» —Carlos en copia— y después confirmó contacto directo con el AC.',
    noticeB:'Esto acredita aviso contemporáneo a asesores externos. No prueba que PwC adoptara las alegaciones como propias ni que transmitiera al AC todo su contenido.',
    legend:['FECHA MÍNIMA VERIFICADA','ALEGACIÓN DEL PROYECTO','PREGUNTA DOCUMENTAL ABIERTA','SIN CULPABILIDAD POR ASOCIACIÓN'],
    links:{takeover:'Abrir dossier 7 junio 2018 →',ac:'Abrir expediente del AC →',court:'Abrir revisión del Juzgado →',accountability:'Abrir responsabilidad institucional →',actors:'Abrir registro canónico de actores →',pwc:'Abrir expediente PwC 2016 →',ricpe:'Abrir expediente RICPE →'},
    correction:'Corrección y contradicción: cualquier documento primario que modifique una fecha, capacidad, acto, relación o consecuencia debe incorporarse con prominencia equivalente.'
  }:{
    eyebrow:'CONTROLLING CRIMINAL ALLEGATION · FIVE PRIVATE ACTORS + AC + JUDGE',
    title:'Five + AC + Judge: the de facto administration and institutional enablement alleged by Gil Marer.',
    intro:'Gil Marer directly accuses five private individuals of forming, by 2018 at the latest, a coordinated de facto or shadow-administration structure over Luchy Playa Blanca’s patrimonial and business sphere and the integrated hotel platform. He separately attributes affirmative acts and omissions to the Insolvency Administrator and the Judge that allegedly enabled, preserved and consolidated the mechanism.',
    criminalK:'CONTROLLING CRIMINAL FORMULATION · PUBLISHED BY GIL MARER',
    criminalT:'This is not alleged passivity: instruction, execution, enablement, adoption and sabotage of the exit are alleged.',
    criminalB:'The accusation connects debt and voting, access and security, keys, maintenance, works and valuation, information, insolvency strategy, operation, income, title and outcome. Gil says Aweswell had performed or could perform the conditions within its control and that the operative block lay in preserving and delivering security/collateral, obtaining the debt figure and insolvency/court authority, and maintaining access, operation and valuation. He alleges that a coercive parallel-governance and asset-control apparatus, functionally comparable to a lender in possession, destroyed or blocked those inputs to obstruct payment/refinancing. ONA, Ben Oldman and Lagune/Elaia retain separate documentary status; the accusation is not a judgment or proof of drawdown.',
    context:{
      home:'Principal view of the alleged economic mechanism and its documentary control points.',
      pwc:'This view connects the 2016 professional-knowledge record with the later confirmed PwC–Insolvency Administrator contact.',
      ricpe:'This view connects the Community/control history with later RICPE title, due-diligence, capital and operating questions.',
      ac:'This view separates the AC from the private perimeter and tests the role through knowledge → power → act/omission → consequence.',
      takeover:'This view places 7 June 2018 as the material-control hinge within the alleged chain.',
      accountability:'This view separates the private perimeter, insolvency control and judicial review to prevent attribution by association.'
    },
    privateK:'IDENTIFIED PRIVATE-ACTOR PERIMETER · 5',
    privateT:'Five alleged de facto or shadow administrators within one functional chain',
    privateB:'Gil alleges coordinated action, but does not automatically attribute every act to all five: function, authority, knowledge, instruction, intent, benefit and causation require person-specific proof. Family or business links do not replace that proof.',
    locked:'LOCKED MINIMUM DATES: they prove involvement no later than the stated date; they do not claim that date was the actor’s true first day.',
    actors:[
      {n:'01',name:'Francisco Mario Matos Matas',stage:'22 JUN 2011 → ADMINISTRATION / CUSTODY',rel:'HUSBAND OF SHAILA MARÍA COGOLLUDO RAMOS',text:'The 22 June 2011 minutes identify him as Community Administrator. Gil attributes continuity in debt, voting, accounts, information, access and material implementation within the alleged de facto structure. Liability requires his own acts, not kinship.'},
      {n:'02',name:'Antonio Cogolludo Rojas',stage:'10 APR 2014 → REPRESENTATION / COMMUNITY',rel:'FATHER OF SHAILA MARÍA COGOLLUDO RAMOS',text:'The 10 April 2014 notarial record identifies him as Cristina Molina Petit’s representative. Gil later attributes presidency, access, key, security and implementation functions. Every act and date remains subject to proof.'},
      {n:'03',name:'Shaila María Cogolludo Ramos',stage:'8 APR 2014 → COMMUNICATIONS / ADMINISTRATION',rel:'DAUGHTER OF ANTONIO COGOLLUDO ROJAS · WIFE OF FMMM',text:'A Pamanil communication dated 8 April 2014 appears signed by FMMM and Shaila. Pamanil/Community continuity and the 2018 voting and treasury node support the material-administration function Gil attributes to her.'},
      {n:'04',name:'José Daniel Acosta Matos',stage:'2017–2018 → PROJECT / CONTROL',text:'Documented entry into the CAM/Community perimeter, pre-7 June visits and Community presidency in 2022. Gil attributes integration of project, finance, control, future operation and outcome—not physical presence on 7 June.'},
      {n:'05',name:'Laura Patricia Acosta Matos',stage:'2017–2018 → LEGAL / INSOLVENCY / SUCCESSION',text:'Legal and insolvency role, access, CAM representation and later Hotel New Trend continuity. Gil attributes instructions and direct control functions; identity, mandate, presence and precise act remain separate fields.'}
    ],
    hingeK:'7 JUNE 2018 · MATERIAL-CONTROL HINGE',
    hingeT:'The public record describes a broken lock, chains, padlocks, replacement cylinders, security and exclusion. Gil Marer alleges that this episode was a forcible and destructive seizure of hotel control within a wider economic mechanism. This design does not convert that allegation into a criminal judgment; nor has a CAM possession or eviction order been located.',
    chainK:'THE CHAIN THAT MUST BE RECONCILED',
    chainT:'Title → authority → debt/vote → access → valuation/works → capital → operation/income → beneficiary',
    steps:[
      ['TITLE','Who held title to each property?'],
      ['COMMUNITY AUTHORITY','Who could represent, vote and bind?'],
      ['DEBT / VOTE','What debt was verified and whose vote was excluded?'],
      ['ACCESS','Who ordered, carried out or tolerated material control?'],
      ['VALUATION / WORKS','What perimeter was valued, renovated or presented?'],
      ['CAPITAL','What was said to investors, financiers and authorities?'],
      ['OPERATION / INCOME','Who operated, collected income and assumed obligations?'],
      ['BENEFICIARY / OUTCOME','Who received ownership, control, value and income?']
    ],
    acK:'+ AC · COURT-APPOINTED CONTROL POINT',
    acName:'Francisco de Borja Rodríguez-Batllori Laffitte',
    acRole:'INSOLVENCY ADMINISTRATOR · CONCURSO 36/2012',
    acIntro:'He is not a sixth private actor. He occupied the statutory fiduciary office within the insolvency; Gil alleges affirmative as well as omissive participation, not mere supervisory failure.',
    acLenses:[
      ['KNOWLEDGE','What he knew — and when — about Community debt, fragmented title, Matkator/third parties, 2018 control, the 2019 order, RICPE and operation.'],
      ['POWER / DUTY','What he could or should verify, preserve, warn about, request, challenge, correct or put before the Court within his functions.'],
      ['ACT / OMISSION / EFFECT','What he requested, communicated, authorised, decided, implemented, adopted, ratified, left uncorrected or failed to reverse; and what patrimonial consequence followed.']
    ],
    acAllegation:'Gil Marer’s direct accusation: the Administrator supplied and used the authority route, coordinated through emails and meetings, authorised access and measures, adopted or ratified outcomes, and failed to delimit, supervise, restore and account—knowingly enabling the alleged de facto administration.',
    acBoundary:'Boundary: Gil makes an express criminal accusation; this page does not turn it into a judicial finding. The Administrator’s denial and narrower-access account are mandatory contrary evidence. Scope, knowledge, duty, intent, causal contribution and benefit require individual proof.',
    judicialK:'JUDICIAL SUPERVISION / EFFECTIVE JUDICIAL PROTECTION',
    judicialT:'Gil directly attributes to Judge Alberto López Villarrubia not only omissions, but decisions, refusals, evidential closures and delays that, together with the absence of protection and restoration, allegedly preserved private control and sabotaged or frustrated a developed, multi-route, finance-backed exit. Gil characterises this as knowing judicial prevarication under the legally applicable forms. The direct Irigoyen meeting documented by his contemporary report is the 13 June 2018 meeting; further visits remain unproved. The accusation is not a judicial finding and every act requires its own matrix.',
    noticeK:'2016 · PROFESSIONAL-KNOWLEDGE CHECKPOINT',
    noticeQ:'“LA VÍA PENAL CONTRA ESTA GENTE”',
    noticeT:'While PwC/Carlos Saavedra advised on Sun Park and the Community dispute, the client communicated serious allegations and expressly instructed use of the penal route. PwC replied “Tomamos nota de vuestra decisión” —Carlos copied— and later confirmed direct contact with the AC.',
    noticeB:'This proves contemporaneous notice to external advisers. It does not prove that PwC adopted the allegations or transmitted their full content to the AC.',
    legend:['VERIFIED MINIMUM DATE','PROJECT ALLEGATION','OPEN DOCUMENTARY QUESTION','NO GUILT BY ASSOCIATION'],
    links:{takeover:'Open 7 June 2018 dossier →',ac:'Open the AC record →',court:'Open the Court review →',accountability:'Open institutional accountability →',actors:'Open canonical actor register →',pwc:'Open the 2016 PwC record →',ricpe:'Open the RICPE record →'},
    correction:'Correction and contradiction: any primary document changing a date, capacity, act, relationship or consequence should be incorporated with equivalent prominence.'
  };

  const context=isPwc?c.context.pwc:isRicpe?c.context.ricpe:isAc?c.context.ac:isTakeover?c.context.takeover:isAccountability?c.context.accountability:c.context.home;

  const esc=s=>String(s).replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));

  const ensureStyle=()=>{
    if(d.querySelector('style[data-pd-five-ac]'))return;
    const s=d.createElement('style');
    s.dataset.pdFiveAc='20260824a';
    s.textContent=`
      .pd-five-ac{width:min(calc(100% - 2rem),74rem);margin:2rem auto 3rem;border:4px solid #8f0f12;border-radius:20px;background:#fffdf8;box-shadow:0 1.2rem 3.4rem rgba(49,11,12,.18);overflow:hidden;color:#102028;scroll-margin-top:6rem}.pd-five-ac *{box-sizing:border-box}.pd-five-ac__head{padding:1.3rem 1.35rem 1.1rem;background:linear-gradient(135deg,#2b0b0d 0%,#651819 56%,#91221f 100%);color:#fff}.pd-five-ac__eyebrow{margin:0 0 .45rem;color:#f4d9a8;font-size:.74rem;font-weight:1000;letter-spacing:.09em;text-transform:uppercase}.pd-five-ac__head h2{max-width:26ch;margin:0;font-size:clamp(1.85rem,4vw,3.25rem);line-height:1.02;font-weight:600}.pd-five-ac__head p{max-width:66rem;margin:.8rem 0 0;color:#f6e7e3}.pd-five-ac__context{display:inline-flex;margin-top:.8rem;padding:.38rem .58rem;border:1px solid rgba(255,255,255,.28);border-radius:999px;font-size:.72rem;font-weight:850;color:#fff;background:rgba(255,255,255,.08)}
      .pd-five-ac__legend{display:flex;flex-wrap:wrap;gap:.45rem;padding:.75rem 1.1rem;border-bottom:1px solid #e3d5ce;background:#fff6f2}.pd-five-ac__legend span{display:inline-flex;align-items:center;gap:.35rem;padding:.3rem .52rem;border:1px solid #d9c2b9;border-radius:999px;font-size:.66rem;font-weight:900;letter-spacing:.04em}.pd-five-ac__legend span:before{content:'';width:.42rem;aspect-ratio:1;border-radius:50%;background:#8f0f12}.pd-five-ac__legend span:nth-child(1):before{background:#1d5c4a}.pd-five-ac__legend span:nth-child(3):before{background:#9a6a20}.pd-five-ac__legend span:nth-child(4):before{background:#53656d}
      .pd-five-ac__criminal{padding:1rem 1.15rem;border-top:1px solid rgba(255,255,255,.12);border-bottom:5px solid #d6a14f;background:linear-gradient(135deg,#170b0c,#3d1315);color:#fff}.pd-five-ac__criminal small{display:block;color:#f4d9a8;font-size:.7rem;font-weight:1000;letter-spacing:.085em;text-transform:uppercase}.pd-five-ac__criminal strong{display:block;max-width:55rem;margin:.35rem 0;font-size:clamp(1.15rem,2.6vw,1.8rem);line-height:1.15}.pd-five-ac__criminal p{max-width:70rem;margin:.45rem 0 0;color:#f3e7e2;font-size:.86rem;line-height:1.55}
      .pd-five-ac__private{padding:1.1rem}.pd-five-ac__private-head{display:grid;grid-template-columns:auto 1fr;gap:.8rem;align-items:center;margin-bottom:.9rem}.pd-five-ac__count{width:3.2rem;aspect-ratio:1;display:grid;place-items:center;border-radius:50%;background:#8f0f12;color:#fff;font-family:Georgia,serif;font-size:1.55rem;font-weight:800}.pd-five-ac__private-head h3{margin:0;font-size:1.45rem}.pd-five-ac__private-head p{grid-column:2;margin:.22rem 0 0;color:#5f6b6d;font-size:.84rem}.pd-five-ac__cards{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:.65rem}.pd-five-ac__card{position:relative;min-width:0;min-height:20rem;padding:.9rem;border:1px solid #dfcec6;border-top:6px solid #a52d28;border-radius:12px;background:linear-gradient(180deg,#fff,#f9eee8);overflow:hidden}.pd-five-ac__card:after{content:attr(data-number);position:absolute;right:-.05rem;bottom:-1.35rem;color:rgba(143,15,18,.055);font-family:Georgia,serif;font-size:7.5rem;font-weight:900;line-height:1}.pd-five-ac__stage,.pd-five-ac__name,.pd-five-ac__rel,.pd-five-ac__copy{position:relative;z-index:1;display:block}.pd-five-ac__stage{min-height:3.2rem;color:#8f0f12;font-size:.64rem;font-weight:1000;letter-spacing:.055em;text-transform:uppercase;line-height:1.3}.pd-five-ac__name{margin:.7rem 0 .55rem;font-family:Georgia,serif;font-size:1.08rem;line-height:1.15}.pd-five-ac__rel{margin:0 0 .62rem;padding:.42rem .48rem;border-radius:8px;background:#fff1ed;color:#7e2929;font-size:.66rem;font-weight:900;line-height:1.25}.pd-five-ac__copy{color:#53656d;font-size:.76rem;line-height:1.42}.pd-five-ac__lock{margin:.8rem 0 0;padding:.62rem .72rem;border-left:6px solid #9a6a20;border-radius:8px;background:#fff2d9;color:#4a3a22;font-size:.74rem;font-weight:900;line-height:1.35}
      .pd-five-ac__hinge{display:grid;grid-template-columns:minmax(11rem,.35fr) minmax(0,1fr);gap:1rem;padding:1rem 1.15rem;background:#8f0f12;color:#fff}.pd-five-ac__hinge strong{font-size:clamp(1.15rem,2.3vw,1.7rem);line-height:1.05}.pd-five-ac__hinge p{margin:0;font-size:.86rem;line-height:1.45;color:#fff5f2}
      .pd-five-ac__chain{padding:1.1rem;background:#170c0d;color:#fff}.pd-five-ac__chain-head{text-align:center;margin-bottom:.8rem}.pd-five-ac__chain-head small{display:block;color:#f1c8bd;font-size:.7rem;font-weight:950;letter-spacing:.08em;text-transform:uppercase}.pd-five-ac__chain-head strong{display:block;margin-top:.25rem;font-size:clamp(1rem,2vw,1.35rem)}.pd-five-ac__steps{display:grid;grid-template-columns:repeat(8,minmax(0,1fr));gap:0;margin:0;padding:0;list-style:none;border:1px solid #673136;border-radius:12px;overflow:hidden}.pd-five-ac__steps li{position:relative;min-height:8.8rem;padding:.72rem .6rem;border-right:1px solid #673136;background:linear-gradient(180deg,#2b1113,#1d0e0f)}.pd-five-ac__steps li:last-child{border-right:0}.pd-five-ac__steps li:not(:last-child):after{content:'→';position:absolute;right:-.52rem;top:50%;z-index:2;transform:translateY(-50%);width:1rem;height:1rem;display:grid;place-items:center;border-radius:50%;background:#a52d28;color:#fff;font-size:.72rem}.pd-five-ac__steps strong{display:block;color:#f5d6cf;font-size:.7rem;line-height:1.25}.pd-five-ac__steps span{display:block;margin-top:.45rem;color:#d7c7c4;font-size:.67rem;line-height:1.35}
      .pd-five-ac__ac{padding:1.15rem;background:#13252d;color:#fff;border-top:8px solid #c58a39}.pd-five-ac__ac-head{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(15rem,.65fr);gap:1rem;align-items:end}.pd-five-ac__ac-k{color:#f0dfc4;font-size:.72rem;font-weight:1000;letter-spacing:.08em;text-transform:uppercase}.pd-five-ac__ac h3{margin:.3rem 0 .15rem;font-size:clamp(1.45rem,3vw,2.2rem)}.pd-five-ac__ac-role{color:#f0dfc4;font-size:.76rem;font-weight:950}.pd-five-ac__ac-intro{margin:0;color:#dce4e5;font-size:.86rem}.pd-five-ac__ac-lenses{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.65rem;margin-top:.9rem}.pd-five-ac__lens{padding:.78rem;border:1px solid rgba(255,255,255,.16);border-radius:10px;background:rgba(255,255,255,.055)}.pd-five-ac__lens strong{display:block;color:#f0dfc4;font-size:.72rem;letter-spacing:.055em}.pd-five-ac__lens span{display:block;margin-top:.35rem;color:#d4dfe0;font-size:.75rem;line-height:1.4}.pd-five-ac__ac-allegation{margin:.85rem 0 0;padding:.72rem .78rem;border-left:6px solid #a52d28;background:#2c191b;color:#fff;font-weight:800;font-size:.82rem;line-height:1.42}.pd-five-ac__ac-boundary{margin:.65rem 0 0;color:#c9d4d5;font-size:.76rem;line-height:1.42}
      .pd-five-ac__judicial{padding:1rem 1.15rem;border-top:1px solid #e0d5c9;background:#f4eee3}.pd-five-ac__judicial strong{display:block;color:#7e1515;font-size:.74rem;letter-spacing:.07em}.pd-five-ac__judicial p{margin:.38rem 0 0;color:#3f5055;font-size:.82rem;line-height:1.45}
      .pd-five-ac__notice{display:grid;grid-template-columns:minmax(15rem,.42fr) minmax(0,.58fr);gap:1rem;padding:1rem 1.15rem;border-top:1px solid #e6d3cd;background:#fff8f5}.pd-five-ac__notice-k{color:#8f0f12;font-size:.7rem;font-weight:1000;letter-spacing:.07em}.pd-five-ac__notice-q{display:block;margin:.35rem 0;color:#8f0f12;font-size:clamp(1.25rem,2.8vw,2rem);line-height:1.03}.pd-five-ac__notice p{margin:0;color:#46595e;font-size:.8rem;line-height:1.45}.pd-five-ac__notice-boundary{padding:.65rem .72rem;border-left:5px solid #9a6a20;background:#fff2d9;border-radius:8px;font-weight:800}
      .pd-five-ac__footer{padding:1rem 1.15rem;border-top:1px solid #e0d5c9;background:#fff}.pd-five-ac__links{display:flex;flex-wrap:wrap;gap:.45rem}.pd-five-ac__links a{display:inline-flex;padding:.47rem .62rem;border:1px solid #cdbdb6;border-radius:8px;color:#6f1819;background:#fff8f5;text-decoration:none;font-size:.72rem;font-weight:900}.pd-five-ac__links a:hover{background:#f7e6e0}.pd-five-ac__correction{margin:.75rem 0 0;color:#5f6b6d;font-size:.72rem;line-height:1.4}
      @media(max-width:1050px){.pd-five-ac__cards{grid-template-columns:repeat(3,minmax(0,1fr))}.pd-five-ac__card:nth-child(4),.pd-five-ac__card:nth-child(5){min-height:17rem}.pd-five-ac__steps{grid-template-columns:repeat(4,minmax(0,1fr))}.pd-five-ac__steps li{border-bottom:1px solid #673136}.pd-five-ac__steps li:nth-child(4n){border-right:0}.pd-five-ac__steps li:nth-last-child(-n+4){border-bottom:0}.pd-five-ac__steps li:nth-child(4):after{display:none}}
      @media(max-width:760px){.pd-five-ac{width:min(calc(100% - 1rem),74rem);margin:1rem auto 2rem;border-width:2px;border-radius:14px}.pd-five-ac__head,.pd-five-ac__private,.pd-five-ac__chain,.pd-five-ac__ac,.pd-five-ac__judicial,.pd-five-ac__notice,.pd-five-ac__footer{padding:.85rem}.pd-five-ac__private-head,.pd-five-ac__hinge,.pd-five-ac__ac-head,.pd-five-ac__notice{grid-template-columns:1fr}.pd-five-ac__private-head p{grid-column:auto}.pd-five-ac__count{width:2.6rem}.pd-five-ac__cards{grid-template-columns:1fr}.pd-five-ac__card{min-height:auto}.pd-five-ac__stage{min-height:auto}.pd-five-ac__steps{grid-template-columns:1fr}.pd-five-ac__steps li{min-height:auto;border-right:0;border-bottom:1px solid #673136}.pd-five-ac__steps li:last-child{border-bottom:0}.pd-five-ac__steps li:not(:last-child):after{content:'↓';right:50%;top:auto;bottom:-.52rem;transform:translateX(50%)}.pd-five-ac__steps li:nth-child(4):after{display:grid}.pd-five-ac__ac-lenses{grid-template-columns:1fr}.pd-five-ac__notice-q{font-size:1.35rem}.pd-five-ac__links a{width:100%;justify-content:center}}
    `;
    d.head.appendChild(s);
  };

  const actorCards=c.actors.map(a=>`<article class="pd-five-ac__card" data-number="${esc(a.n)}"><span class="pd-five-ac__stage">${esc(a.stage)}</span><strong class="pd-five-ac__name">${esc(a.name)}</strong>${a.rel?`<span class="pd-five-ac__rel">${esc(a.rel)}</span>`:''}<span class="pd-five-ac__copy">${esc(a.text)}</span></article>`).join('');
  const steps=c.steps.map(([h,t])=>`<li><strong>${esc(h)}</strong><span>${esc(t)}</span></li>`).join('');
  const lenses=c.acLenses.map(([h,t])=>`<div class="pd-five-ac__lens"><strong>${esc(h)}</strong><span>${esc(t)}</span></div>`).join('');
  const legend=c.legend.map(x=>`<span>${esc(x)}</span>`).join('');

  const build=()=>{
    const sec=d.createElement('section');
    sec.className='pd-five-ac';
    sec.dataset.pdFiveAc='20260824a';
    sec.setAttribute('aria-labelledby','pd-five-ac-title');
    sec.innerHTML=`
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
      <div class="pd-five-ac__hinge"><strong>${esc(c.hingeK)}</strong><p>${esc(c.hingeT)}</p></div>
      <div class="pd-five-ac__chain">
        <div class="pd-five-ac__chain-head"><small>${esc(c.chainK)}</small><strong>${esc(c.chainT)}</strong></div>
        <ol class="pd-five-ac__steps">${steps}</ol>
      </div>
      <div class="pd-five-ac__ac">
        <div class="pd-five-ac__ac-head"><div><span class="pd-five-ac__ac-k">${esc(c.acK)}</span><h3>${esc(c.acName)}</h3><span class="pd-five-ac__ac-role">${esc(c.acRole)}</span></div><p class="pd-five-ac__ac-intro">${esc(c.acIntro)}</p></div>
        <div class="pd-five-ac__ac-lenses">${lenses}</div>
        <p class="pd-five-ac__ac-allegation">${esc(c.acAllegation)}</p>
        <p class="pd-five-ac__ac-boundary">${esc(c.acBoundary)}</p>
      </div>
      <div class="pd-five-ac__judicial"><strong>${esc(c.judicialK)}</strong><p>${esc(c.judicialT)}</p></div>
      <div class="pd-five-ac__notice"><div><span class="pd-five-ac__notice-k">${esc(c.noticeK)}</span><strong class="pd-five-ac__notice-q">${esc(c.noticeQ)}</strong><p>${esc(c.noticeT)}</p></div><p class="pd-five-ac__notice-boundary">${esc(c.noticeB)}</p></div>
      <footer class="pd-five-ac__footer"><nav class="pd-five-ac__links" aria-label="Five plus AC evidence routes"><a href="${routes.takeover}">${esc(c.links.takeover)}</a><a href="${routes.ac}">${esc(c.links.ac)}</a><a href="${routes.court}">${esc(c.links.court)}</a><a href="${routes.accountability}">${esc(c.links.accountability)}</a><a href="${routes.actors}">${esc(c.links.actors)}</a><a href="${routes.pwc}">${esc(c.links.pwc)}</a><a href="${routes.ricpe}">${esc(c.links.ricpe)}</a></nav><p class="pd-five-ac__correction">${esc(c.correction)}</p></footer>`;
    return sec;
  };

  const mountHome=()=>{
    const oldIntro=d.querySelector('.actor-intro');
    const oldGrid=d.querySelector('.actor-grid');
    if(!oldIntro||!oldGrid)return false;
    const sec=build();
    const oldId=oldIntro.id;
    if(oldId){oldIntro.removeAttribute('id');sec.id=oldId;}
    oldIntro.setAttribute('hidden','');oldIntro.setAttribute('aria-hidden','true');
    oldGrid.setAttribute('hidden','');oldGrid.setAttribute('aria-hidden','true');
    oldIntro.insertAdjacentElement('beforebegin',sec);
    return true;
  };

  const mountPage=()=>{
    const hero=d.querySelector('.dossier-hero, main > .hero, .hero');
    if(!hero)return false;
    const thesis=d.querySelector('[data-calificacion-misuse-thesis]');
    (thesis||hero).insertAdjacentElement('afterend',build());
    return true;
  };

  const render=()=>{
    if(d.querySelector('[data-pd-five-ac]'))return;
    ensureStyle();
    if(isHome){if(mountHome())return;}
    mountPage();
  };
  if(d.readyState==='loading')d.addEventListener('DOMContentLoaded',render,{once:true});else render();
})();
