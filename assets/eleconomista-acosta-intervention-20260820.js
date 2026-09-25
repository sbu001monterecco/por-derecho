(()=>{
  const path=location.pathname;
  const isEs=/\/es\/eleconomista-javier-romera-enero2025\/?(?:index\.html)?$/i.test(path);
  const isEn=/\/en\/eleconomista-javier-romera-january2025\/?(?:index\.html)?$/i.test(path);
  if(!isEs&&!isEn)return;
  const en=isEn;
  const t=en?{
    title:'elEconomista · January 2025 · the Acosta Matos intervention allegation | Project Sun Rock',
    desc:'Document-led reconstruction of Project Sun Rock’s allegation that the CAM/Acosta Matos response perimeter materially caused an advanced elEconomista investigation to stop in January 2025 after an appealed LPB judgment was supplied and treated as if it answered the wider Sun Park story.',
    eyebrow:'MEDIA · ADVANCED VERIFICATION → CAM/ACOSTA MATOS RESPONSE → MONDAY JUDICIAL MATERIAL → PUBLICATION STOPS',
    h1:'Project Sun Rock accuses the Acosta Matos perimeter of causing an advanced elEconomista investigation to stop in January 2025.',
    lead:'This is <strong>not an accusation against Javier Romera or elEconomista</strong>. The controlled sequence shows an active pre-publication verification process; a Laura/CAM-side intervention; Romera’s direct confirmation that he had been asked to wait until Monday for judicial material; and, on Monday, receipt of a materially adverse but already-appealed <strong>Judgment 163/2023 concerning LPB</strong>, which he described as an “order” about the “Sun Park insolvency” before saying that “with this” the newspaper could not publish. <strong>Project Sun Rock’s allegation</strong> is that the investigated perimeter used or procured that judgment as an interested countermeasure that materially achieved the stopping of the proposed story. The physical transmitter and any person who assisted in procuring, transmitting or framing the document remain open evidential questions.',
    scopeEyebrow:'SCOPE OF THE ALLEGATION · ACOSTA MATOS, NOT THE NEWSROOM',
    scopeH2:'The allegation is about intervention in the publication process.',
    directH:'What the direct record establishes',
    directP:'Romera was actively reviewing the material, editing the proposed press note and applying his “bien atado” verification standard. On 17 January he directly confirmed that he had been asked to wait until Monday for judicial orders. On Monday 20 January he confirmed receipt of an “order” and immediately communicated: “with this we cannot publish it.” This proves an advanced verification process and the editorial consequence; it does not prove that publication had been guaranteed.',
    allegationH:'Project Sun Rock’s allegation',
    allegationP:'The CAM/Acosta Matos response perimeter, with <strong>Laura Patricia Acosta Matos as the identified intervention point</strong>, deliberately used or procured an adverse LPB judgment in the response process so that it would operate as a dispositive answer to a much broader Sun Park investigation. We allege that this intervention materially caused the proposed publication to stop.',
    openH:'What remains to be proved',
    openP:'Who located or procured the judgment; who decided how it should be characterised to the newsroom; who physically transmitted it and from which account; what accompanying text was used; and whether any lawyer, adviser, representative or other intermediary assisted. <strong>No collaborator is identified as fact without primary evidence.</strong>',
    noAcc:'<strong>No allegation against the journalist or newspaper:</strong> we do not accuse Javier Romera or elEconomista of collusion, censorship, bad faith or any offence. The present hypothesis is that the newsroom may itself have received a materially incomplete or misleading characterisation of the scope of an adverse court document from an interested response channel.',
    madridEyebrow:'MADRID 2025 · THE CRIMINAL THEORY NARROWED; THE JOURNALISTIC QUESTION REMAINED',
    madridH2:'What the Madrid case did — and did not — decide',
    madridP1:'The March 2025 complaint prepared through Sixto Abogados alleged, among other things, that Laura personally sent the judicial material and intended to prevent the planned publication; it also proposed Javier Romera as a witness. Those were <strong>pleaded allegations, not findings</strong>. The filed exhibits we have now recovered included Romera’s 20 January email, a public insolvency-register extract naming <strong>LUCHY PLAYA BLANCA, S.L.</strong>, and the actual 31-page Judgment 163/2023.',
    madridP2:'The 5 May 2025 Madrid archive order rejected the secrecy-offence route at threshold. It said the filed material did <strong>not establish that Laura was the physical sender</strong>; it held that CAM had legitimate access to the judgment as a party/creditor; it expressly corrected the document as a <strong>“Sentencia –y no el Auto–”</strong>; and it observed that a hypothetical transmission could be <strong>“interesada”</strong> without constituting the offence alleged.',
    madridP3:'Reform and then appeal were pursued in May/June 2025 and Fiscalía opposed the appeal. The current controlled Gmail/repository search has not located a later appellate decision, so this page does <strong>not</strong> describe the 5 May archive as a final appellate merits determination. More importantly, that criminal threshold decision did not decide the journalistic question: whether the judgment was accurately contextualised to the newsroom, whether its pending appeal was explained, or whether it actually answered the wider story.',
    twoEyebrow:'THE ORIGINAL STORY + A SECOND STORY',
    twoH2:'Stopping the first investigation has itself become a new line of public-interest inquiry.',
    story1H:'Story 1 · What was happening around Sun Park?',
    story1P:'Meeting Point/FTI and Club Sei commercialisation; mixed ownership and extraconcursal units; CAM control and title chronology; RIC/RICPE investor representations; professional gatekeepers; regional incentives, RIC and FEDER/public-funding controls. Judgment 163/2023 did not adjudicate those questions.',
    story2H:'Story 2 · How did the newsroom investigation stop?',
    story2P:'Why was a judgment about one corporate owner treated as if it resolved “Sun Park”? Who procured and framed the document? Was the fact of appeal disclosed? What was said by CAM/Acosta Matos and Meeting Point? What did the newsroom receive natively, and what independent verification was carried out before the decision not to publish?',
    renewed:'<strong>20 August 2026:</strong> Project Sun Rock renewed the request to elEconomista to reopen the file, supplied new source maps and a public video source, requested preservation of the native incoming message and offered a short primary-source pack. The same source-led invitation is open to <strong>elEconomista or any other independent newsroom</strong> willing to investigate and give all affected parties a right of reply.',
    whoH:'Who procured, framed and physically transmitted the judgment?',
    qEyebrow:'NO ACCUSATION AGAINST THE NEWSROOM',
    qH:'elEconomista can help resolve the evidence gap; it is not the target of this allegation.',
    qIntro:'The central production question is now external to the newspaper’s good faith: <strong>what exactly entered the newsroom from the CAM/Acosta Matos response side, through whom, and with what description of the judgment’s scope and appeal status?</strong>',
    mapEyebrow:'TWO SOURCE MAPS · ALSO USED IN PROFESSIONAL-CUSTODY REQUESTS',
    mapH:'Why the underlying story is now more documentable',
    mapIntro:'These are source maps, not findings. They identify records and preservation questions that can be checked independently by journalists and professional custodians.',
    map1:'<strong>PwC · 2016 knowledge checkpoint.</strong> A source-controlled map of early professional knowledge concerning Sun Park’s ownership, private units, exploitation, Community and insolvency architecture. It does not state that PwC independently found any named person guilty of wrongdoing.',
    map2:'<strong>San Telmo · RICPE · Sun Park.</strong> A source-controlled map of the 30 November 2021 public statement in which San Telmo partner Eduardo Sánchez said, in the relevant passage, that “el despacho” had put clients into the first investment. The statement does not by itself prove coordination, transfer of insolvency information or unlawfulness.',
    video:'Watch the public source from approximately 08:08 →',
    mediaCap:'Visual summary of the January 2025 sequence. It is an explanatory graphic, not evidence, and the generated human figure is not a photograph or documentary likeness of Javier Romera.'
  }:{
    title:'elEconomista · enero 2025 · acusación sobre la intervención Acosta Matos | Project Sun Rock',
    desc:'Reconstrucción documental de la acusación de Project Sun Rock: el canal de respuesta CAM/Acosta Matos habría provocado materialmente que una investigación avanzada de elEconomista se detuviera en enero de 2025 tras aportarse una sentencia recurrida sobre LPB como si contestara la historia más amplia de Sun Park.',
    eyebrow:'MEDIOS · CONTRASTE AVANZADO → RESPUESTA CAM/ACOSTA MATOS → DOCUMENTACIÓN JUDICIAL EL LUNES → PUBLICACIÓN DETENIDA',
    h1:'Project Sun Rock acusa al perímetro Acosta Matos de haber provocado que una investigación avanzada de elEconomista se detuviera en enero de 2025.',
    lead:'Esta <strong>no es una acusación contra Javier Romera ni contra elEconomista</strong>. La secuencia controlada muestra un proceso activo y avanzado de contraste previo a publicación; una intervención desde el lado Laura/CAM; la confirmación directa de Romera de que le habían pedido esperar hasta el lunes para recibir resoluciones judiciales; y, el lunes, la recepción de una <strong>Sentencia 163/2023 materialmente adversa pero ya recurrida sobre LPB</strong>, que Romera describió como un “auto” sobre el “concurso de Sun Park” antes de comunicar que “con esto” no podían publicar. <strong>La acusación de Project Sun Rock</strong> es que el perímetro investigado utilizó o procuró esa sentencia como una contramedida interesada que consiguió materialmente detener la historia propuesta. El transmisor físico y cualquier persona que ayudara a procurar, transmitir o enmarcar el documento siguen siendo cuestiones probatorias abiertas.',
    scopeEyebrow:'ALCANCE DE LA ACUSACIÓN · ACOSTA MATOS, NO LA REDACCIÓN',
    scopeH2:'La acusación se refiere a la intervención en el proceso de publicación.',
    directH:'Lo que acredita el registro directo',
    directP:'Romera estaba revisando activamente el material, editando la nota propuesta y aplicando su estándar de verificación “bien atado”. El 17 de enero confirmó directamente que le habían pedido esperar hasta el lunes para recibir autos judiciales. El lunes 20 confirmó la recepción de un “auto” e inmediatamente comunicó: “con esto no podemos publicarlo”. Esto acredita un proceso avanzado de contraste y la consecuencia editorial; no acredita que la publicación estuviera garantizada.',
    allegationH:'La acusación de Project Sun Rock',
    allegationP:'El canal de respuesta CAM/Acosta Matos, con <strong>Laura Patricia Acosta Matos como punto de intervención identificado</strong>, utilizó o procuró deliberadamente una sentencia adversa sobre LPB dentro del proceso de respuesta para que operara como contestación dispositiva a una investigación mucho más amplia sobre Sun Park. Alegamos que esa intervención causó materialmente que la publicación propuesta se detuviera.',
    openH:'Lo que todavía debe probarse',
    openP:'Quién localizó o procuró la sentencia; quién decidió cómo debía caracterizarse ante la redacción; quién la transmitió físicamente y desde qué cuenta; qué texto la acompañó; y si intervino algún abogado, asesor, representante u otro intermediario. <strong>No identificamos a ningún colaborador como hecho sin prueba primaria.</strong>',
    noAcc:'<strong>Sin acusación contra el periodista o el medio:</strong> no acusamos a Javier Romera ni a elEconomista de connivencia, censura, mala fe o delito. La hipótesis actual es que la propia redacción pudo recibir desde un canal de respuesta interesado una caracterización materialmente incompleta o engañosa del alcance de un documento judicial adverso.',
    madridEyebrow:'MADRID 2025 · SE ESTRECHÓ LA TESIS PENAL; QUEDÓ ABIERTA LA PREGUNTA PERIODÍSTICA',
    madridH2:'Lo que el procedimiento de Madrid decidió — y lo que no decidió',
    madridP1:'La querella de marzo de 2025 preparada a través de Sixto Abogados alegó, entre otras cosas, que Laura había remitido personalmente la documentación judicial y pretendía impedir la publicación prevista; también propuso a Javier Romera como testigo. Eran <strong>alegaciones de parte, no hallazgos judiciales</strong>. Los anexos presentados, que ahora hemos recuperado, incluían el correo de Romera de 20 de enero, una extracción del Registro Público Concursal que nombraba a <strong>LUCHY PLAYA BLANCA, S.L.</strong> y la Sentencia 163/2023 completa de 31 páginas.',
    madridP2:'El Auto de archivo de Madrid de 5 de mayo de 2025 rechazó en fase inicial la concreta vía de revelación de secretos. Dijo que la documentación aportada <strong>no acreditaba que Laura fuera la remitente física</strong>; consideró que CAM tenía acceso legítimo a la sentencia como parte/acreedora; corrigió expresamente que era una <strong>“Sentencia –y no el Auto–”</strong>; y observó que una eventual transmisión podía ser <strong>“interesada”</strong> sin constituir el delito denunciado.',
    madridP3:'En mayo/junio de 2025 se promovieron reforma y después apelación, y Fiscalía se opuso a la apelación. El barrido controlado actual de Gmail/repositorio no ha localizado una resolución posterior de la Audiencia Provincial, por lo que esta página <strong>no</strong> presenta el archivo de 5 de mayo como una resolución final de apelación sobre el fondo. Y, sobre todo, aquella decisión penal de umbral no resolvió la pregunta periodística: si la sentencia fue contextualizada correctamente ante la redacción, si se explicó que estaba recurrida o si contestaba realmente la historia mucho más amplia.',
    twoEyebrow:'LA HISTORIA ORIGINAL + UNA SEGUNDA HISTORIA',
    twoH2:'La forma en que se detuvo la primera investigación se ha convertido en una nueva línea de interés público.',
    story1H:'Historia 1 · ¿Qué estaba ocurriendo alrededor de Sun Park?',
    story1P:'Comercialización Meeting Point/FTI y Club Sei; titularidad mixta y fincas extraconcursales; cronología de control y título de CAM; representaciones RIC/RICPE a inversores; custodios profesionales; incentivos regionales, RIC y controles FEDER/fondos públicos. La Sentencia 163/2023 no resolvía esas cuestiones.',
    story2H:'Historia 2 · ¿Cómo se detuvo la investigación periodística?',
    story2P:'¿Por qué una sentencia sobre una sociedad propietaria terminó tratándose como si resolviera “Sun Park”? ¿Quién procuró y enmarcó el documento? ¿Se comunicó que estaba recurrido? ¿Qué dijeron CAM/Acosta Matos y Meeting Point? ¿Qué recibió nativamente la redacción y qué verificación independiente se hizo antes de decidir no publicar?',
    renewed:'<strong>20 de agosto de 2026:</strong> Project Sun Rock ha pedido formalmente a elEconomista que reabra el expediente, ha facilitado nuevos mapas de fuentes y una fuente audiovisual pública, ha solicitado la preservación del mensaje entrante nativo y ha ofrecido un paquete corto de fuentes primarias. La misma invitación basada en fuentes queda abierta a <strong>elEconomista o a cualquier otro medio independiente</strong> dispuesto a investigar y dar derecho de respuesta a todas las partes afectadas.',
    whoH:'¿Quién procuró, enmarcó y transmitió físicamente la sentencia?',
    qEyebrow:'SIN ACUSACIÓN CONTRA LA REDACCIÓN',
    qH:'elEconomista puede ayudar a cerrar el vacío probatorio; no es el objetivo de esta acusación.',
    qIntro:'La cuestión de producción central queda fuera de la buena fe del medio: <strong>¿qué entró exactamente en la redacción desde el lado de respuesta CAM/Acosta Matos, a través de quién y con qué descripción del alcance de la sentencia y de su estado de apelación?</strong>',
    mapEyebrow:'DOS MAPAS DE FUENTES · TAMBIÉN UTILIZADOS ANTE CUSTODIOS PROFESIONALES',
    mapH:'Por qué la historia subyacente es hoy mucho más documentable',
    mapIntro:'Son mapas de fuentes, no hallazgos. Identifican registros y preguntas de preservación que periodistas y custodios profesionales pueden comprobar independientemente.',
    map1:'<strong>PwC · punto de conocimiento de 2016.</strong> Mapa source-controlled del conocimiento profesional temprano sobre la arquitectura de propiedad, unidades privadas, explotación, Comunidad y concurso de Sun Park. No afirma que PwC determinara independientemente la culpabilidad de ninguna persona nombrada.',
    map2:'<strong>San Telmo · RICPE · Sun Park.</strong> Mapa source-controlled de la manifestación pública de 30 de noviembre de 2021 en la que el socio de San Telmo Eduardo Sánchez dijo, en el tramo relevante, que “el despacho” había introducido clientes en la primera inversión. La frase no prueba por sí sola coordinación, transmisión de información concursal o ilicitud.',
    video:'Ver la fuente pública desde aproximadamente 08:08 →',
    mediaCap:'Resumen visual de la secuencia de enero de 2025. Es una pieza explicativa, no prueba, y la figura humana generada no es una fotografía ni una representación documental de Javier Romera.'
  };

  const ready=()=>{
    document.title=t.title;
    const meta=document.querySelector('meta[name="description"]'); if(meta)meta.setAttribute('content',t.desc);
    const style=document.createElement('style');
    style.id='eleconomista-acosta-intervention-style';
    style.textContent=`
      .am-scope{border-top:8px solid #7b171d;background:#fff8f7}.am-scope .shell,.am-madrid .shell,.am-two .shell{max-width:1180px}.am-kicker{font-size:.76rem;letter-spacing:.1em;font-weight:900;color:#7b171d;text-transform:uppercase}.am-cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem;margin:1.25rem 0}.am-card{background:#fff;border:1px solid rgba(20,35,45,.16);border-radius:15px;padding:1.1rem}.am-card h3{margin:.1rem 0 .55rem}.am-allegation{border-top:5px solid #7b171d}.am-direct{border-top:5px solid #315c7b}.am-open{border-top:5px solid #c89432}.am-noacc{margin-top:1.1rem;border-left:5px solid #315c7b;background:#f2f7fa;padding:1rem 1.1rem}.am-madrid{background:#f6f3eb}.am-madrid .am-order{border-left:5px solid #7b171d;background:white;padding:1rem 1.15rem;margin:1rem 0}.am-two{background:#111d25;color:#fff}.am-two h2,.am-two h3{color:#fff}.am-two .am-kicker{color:#f0c666}.am-two-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;margin:1.2rem 0}.am-story{border:1px solid rgba(255,255,255,.22);border-radius:15px;padding:1.1rem;background:rgba(255,255,255,.06)}.am-renewed{border-left:5px solid #f0c666;background:rgba(255,255,255,.09);padding:1rem 1.1rem}.am-source-maps{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1.25rem}.am-source-map{margin:0;background:#fff;border:1px solid rgba(20,35,45,.16);border-radius:16px;padding:1rem}.am-source-map img{display:block;width:100%;height:auto}.am-source-map figcaption{margin-top:.8rem;font-size:.9rem;line-height:1.55;color:#4b5963}.am-source-map a{font-weight:800}.am-media{max-width:760px;margin:0 auto}.am-media img{display:block;width:100%;height:auto;border-radius:16px;border:1px solid rgba(20,35,45,.16);box-shadow:0 18px 48px rgba(20,35,45,.16)}.am-media figcaption{margin-top:.8rem;font-size:.9rem;line-height:1.5;color:#4b5963}@media(max-width:760px){.am-cards,.am-two-grid,.am-source-maps{grid-template-columns:1fr}}
    `;
    document.head.appendChild(style);

    const hero=document.querySelector('.mhero .shell');
    if(hero){
      hero.innerHTML=`<p class="eyebrow">${t.eyebrow}</p><h1>${t.h1}</h1><p class="lead">${t.lead}</p>`;
    }
    const heroSection=document.querySelector('.mhero');
    if(heroSection&&!document.querySelector('#acosta-intervention')){
      heroSection.insertAdjacentHTML('afterend',`<section class="section am-scope" id="acosta-intervention"><div class="shell"><p class="am-kicker">${t.scopeEyebrow}</p><h2>${t.scopeH2}</h2><div class="am-cards"><article class="am-card am-direct"><h3>${t.directH}</h3><p>${t.directP}</p></article><article class="am-card am-allegation"><h3>${t.allegationH}</h3><p>${t.allegationP}</p></article><article class="am-card am-open"><h3>${t.openH}</h3><p>${t.openP}</p></article></div><p class="am-noacc">${t.noAcc}</p></div></section>`);
    }

    if(en&&!document.querySelector('.media-visual')&&!document.querySelector('.am-media-wrap')){
      const scope=document.querySelector('#acosta-intervention');
      if(scope)scope.insertAdjacentHTML('afterend',`<section class="section am-media-wrap"><div class="shell"><figure class="am-media"><a href="../../assets/eleconomista-bien-atada-infografia-hq-20260819.webp" target="_blank" rel="noopener"><img src="../../assets/eleconomista-bien-atada-infografia-hq-20260819.webp" width="1024" height="1536" alt="Visual summary of the elEconomista and Javier Romera documentary sequence between 17 and 20 January 2025." loading="eager" decoding="async"></a><figcaption>${t.mediaCap} <a href="../../assets/eleconomista-bien-atada-infografia-hq-20260819.webp" target="_blank" rel="noopener">Open full resolution →</a></figcaption></figure></div></section>`);
    }

    const mapExists=document.querySelector('#mapas,#source-maps');
    if(en&&!mapExists){
      const media=document.querySelector('.am-media-wrap')||document.querySelector('#acosta-intervention');
      if(media)media.insertAdjacentHTML('afterend',`<section class="section alt" id="source-maps"><div class="shell"><p class="am-kicker">${t.mapEyebrow}</p><h2>${t.mapH}</h2><p>${t.mapIntro}</p><div class="am-source-maps"><figure class="am-source-map"><a href="../../assets/jdam-pwc-knowledge-2016-EN.svg" target="_blank" rel="noopener"><img src="../../assets/jdam-pwc-knowledge-2016-EN.svg" width="1600" height="1000" alt="English source map of the 2016 PwC professional-knowledge checkpoint and later Sun Park perimeter actors." loading="lazy"></a><figcaption>${t.map1}</figcaption></figure><figure class="am-source-map"><a href="../../assets/jdam-san-telmo-ricpe-sun-park-EN.svg" target="_blank" rel="noopener"><img src="../../assets/jdam-san-telmo-ricpe-sun-park-EN.svg" width="1600" height="1000" alt="English source map of the San Telmo, RICPE and Sun Park parallel professional-life questions." loading="lazy"></a><figcaption>${t.map2}<br><a href="https://www.youtube.com/watch?v=mHn9IJU0qI4&t=488s" target="_blank" rel="noopener">${t.video}</a></figcaption></figure></div></div></section>`);
    }

    const correction=document.querySelector(en?'#correction':'#correccion');
    if(correction&&!document.querySelector('#madrid-2025-media')){
      correction.insertAdjacentHTML('beforebegin',`<section class="section am-madrid" id="madrid-2025-media"><div class="shell"><p class="am-kicker">${t.madridEyebrow}</p><h2>${t.madridH2}</h2><p>${t.madridP1}</p><div class="am-order"><p>${t.madridP2}</p></div><p>${t.madridP3}</p></div></section><section class="section am-two" id="two-stories"><div class="shell"><p class="am-kicker">${t.twoEyebrow}</p><h2>${t.twoH2}</h2><div class="am-two-grid"><article class="am-story"><h3>${t.story1H}</h3><p>${t.story1P}</p></article><article class="am-story"><h3>${t.story2H}</h3><p>${t.story2P}</p></article></div><p class="am-renewed">${t.renewed}</p></div></section>`);
    }

    [...document.querySelectorAll('section h2')].forEach(h=>{
      const x=(h.textContent||'').trim().toLowerCase();
      if((en&&x==='who sent the document?')||(!en&&x==='¿quién envió el documento?'))h.textContent=t.whoH;
      if((en&&x==='the difficult question for eleconomista')||(!en&&x==='la pregunta difícil para eleconomista')){
        h.textContent=t.qH;
        const s=h.closest('section');
        const eyebrow=s&&s.querySelector('.eyebrow'); if(eyebrow)eyebrow.textContent=t.qEyebrow;
        const first=s&&h.nextElementSibling; if(first&&first.tagName==='P')first.innerHTML=t.qIntro;
      }
    });
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',ready,{once:true}); else ready();
})();
