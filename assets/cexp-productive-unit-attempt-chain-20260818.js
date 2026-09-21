(() => {
  'use strict';

  const path = (window.location.pathname.replace(/\/+$/, '') || '/') + '/';
  const fullRoutes = [
    '/en/insolvency-36-2012-insolvency-administrator/',
    '/es/concurso-36-2012-administrador-concursal/',
    '/en/insolvency-classification-parallel-lives/',
    '/es/calificacion-concurso-36-2012-vidas-paralelas/',
    '/en/lpb-solvency-record/',
    '/es/expediente-solvencia-lpb/',
    '/en/community-instrumentalisation/',
    '/es/comunidad-instrumentalizacion/',
    '/en/recovery-restitution-objectives/',
    '/es/objetivos-recuperacion-restitucion/'
  ];
  const compactRoutes = [
    '/en/lpb-insolvency/',
    '/es/insolvencia-lpb/',
    '/en/insolvency-36-2012-institutional-accountability/',
    '/es/concurso-36-2012-responsabilidad-institucional/',
    '/en/sun-park-takeover-7-june-2018/',
    '/es/toma-control-sun-park-7-junio-2018/',
    '/en/actua-2018-spatial-test/',
    '/es/actua-2018-prueba-espacial/',
    '/en/sun-park-forensic-map-262-properties/',
    '/es/mapa-forense-sun-park-262-fincas/'
  ];
  const full = fullRoutes.some(route => path.endsWith(route));
  const compact = !full && compactRoutes.some(route => path.endsWith(route));
  if (!full && !compact) return;
  if (document.getElementById('cexp-productive-unit-attempt-chain')) return;

  const es = path.includes('/es/');
  const base = 'https://sbu001monterecco.github.io/por-derecho';
  const links = es ? {
    value: `${base}/es/expediente-solvencia-lpb/`,
    cexp: `${base}/es/comunidad-instrumentalizacion/`,
    ac: `${base}/es/concurso-36-2012-administrador-concursal/`,
    cal: `${base}/es/calificacion-concurso-36-2012-vidas-paralelas/`
  } : {
    value: `${base}/en/lpb-solvency-record/`,
    cexp: `${base}/en/community-instrumentalisation/`,
    ac: `${base}/en/insolvency-36-2012-insolvency-administrator/`,
    cal: `${base}/en/insolvency-classification-parallel-lives/`
  };

  const addStyles = () => {
    if (document.getElementById('cexp-attempt-chain-styles')) return;
    const style = document.createElement('style');
    style.id = 'cexp-attempt-chain-styles';
    style.textContent = `
      .catc{--ink:#13252d;--gold:#c89432;--paper:#f6f1e6;--green:#526b59;--red:#8b443c}
      .catc .catc-shell{max-width:1120px;margin:0 auto}
      .catc .catc-panel{border:1px solid rgba(19,37,45,.2);border-top:8px solid var(--green);border-radius:20px;background:#fff;padding:1.25rem 1.4rem;box-shadow:0 12px 32px rgba(19,37,45,.07)}
      .catc .catc-kicker{margin:0 0 .4rem;font-size:.72rem;letter-spacing:.085em;text-transform:uppercase;font-weight:950;color:#66583f}
      .catc h2{margin:.05rem 0 .7rem;color:var(--ink);font-size:clamp(1.55rem,2.9vw,2.35rem);line-height:1.08}
      .catc .catc-lead{font-size:1.05rem;line-height:1.58}
      .catc .catc-status{display:flex;flex-wrap:wrap;gap:.4rem;list-style:none;padding:0;margin:.8rem 0 1rem}
      .catc .catc-status li{border-radius:999px;padding:.3rem .58rem;font-size:.67rem;font-weight:900;letter-spacing:.035em;text-transform:uppercase;background:#e4ebe6;color:var(--ink)}
      .catc .catc-status li.open{background:#eee5d4}
      .catc .catc-timeline{display:grid;gap:.68rem;margin:1rem 0}
      .catc .catc-event{display:grid;grid-template-columns:120px 1fr;gap:.8rem;border:1px solid rgba(19,37,45,.14);border-radius:14px;padding:.85rem 1rem;background:#fff}
      .catc .catc-date{font-weight:950;color:var(--ink)}
      .catc .catc-event strong{color:var(--ink)}
      .catc .catc-tag{display:inline-block;margin:.25rem .25rem 0 0;border-radius:999px;padding:.18rem .45rem;background:var(--paper);font-size:.65rem;font-weight:900;letter-spacing:.03em;text-transform:uppercase}
      .catc .catc-conclusion{border-left:7px solid var(--gold);background:var(--paper);border-radius:14px;padding:1rem 1.1rem;margin:1rem 0}
      .catc .catc-boundary{border-left:5px solid var(--red);background:#fff7f5;border-radius:14px;padding:1rem 1.1rem;margin:1rem 0}
      .catc .catc-actions{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.9rem}
      .catc .catc-actions a{display:inline-block;text-decoration:none;border-radius:999px;padding:.62rem .86rem;background:var(--ink);color:#fff;border:1px solid var(--ink);font-weight:850}
      .catc .catc-actions a.secondary{background:#fff;color:var(--ink)}
      .catc.catc-compact .catc-panel{padding:1rem 1.15rem;border-top-width:6px}
      .catc.catc-compact h2{font-size:clamp(1.3rem,2.4vw,1.85rem)}
      @media(max-width:700px){.catc .catc-event{grid-template-columns:1fr}.catc .catc-panel{padding:1rem}}
    `;
    document.head.appendChild(style);
  };

  const enFull = `
    <div class="catc-panel">
      <p class="catc-kicker">CONTEMPORANEOUS ATTEMPT CHAIN · CEXP VALUE · 2015–2018</p>
      <h2>The productive-unit value was not a late reconstruction. The record documents repeated attempts to put the CEXP economics, credits and operating structure before the relevant decision-makers.</h2>
      <p class="catc-lead">The controlled record now supports a stronger proposition than a generic claim of later reconstruction: between 2015 and 2018 LPB/Aweswell and their advisers repeatedly raised Community/CEXP governance, exploitation costs, income rights, access, recognised CEXP-related receivables and productive-unit economics. Some steps have direct AC responses; others have stamped-document metadata, expert work product or express preparation for judicial/AC presentation.</p>
      <ul class="catc-status"><li>Contemporaneous chain verified</li><li>Direct AC response located</li><li>Expert note dated 11 Jun 2018</li><li class="open">Formal admission/decision varies by item</li></ul>
      <div class="catc-timeline">
        <div class="catc-event"><div class="catc-date">23 Nov 2015</div><div><strong>Request for AC involvement in the Community problem.</strong> A direct exchange records a request that the insolvency administrator intervene around Community governance. The AC replied by limiting what he regarded as within his functions while offering a narrower note/authorisation route.<br><span class="catc-tag">verified external response</span></div></div>
        <div class="catc-event"><div class="catc-date">25 May 2017</div><div><strong>Stamped material prepared for transmission to the AC and Mercantile Court.</strong> The contemporaneous email record identifies a stamped document and an express instruction to send it promptly to the AC and formally to the court as further evidence of collaboration. The substantive content of that stamped item remains source-by-source controlled.<br><span class="catc-tag">stamped-document metadata</span><span class="catc-tag">presentation attempt</span></div></div>
        <div class="catc-event"><div class="catc-date">19–22 Jan 2018</div><div><strong>The AC himself addressed CEXP-related economics.</strong> The record shows requests for support concerning LPB accounting entries against CEXP, including a recorded “Dividend to Collect from C.E. Sun Park” of €737,338.85, while the AC also asserted operative control over LPB’s access/instructions. This establishes knowledge of a material CEXP economic layer, not its final legal treatment.<br><span class="catc-tag">AC knowledge</span><span class="catc-tag">accounting record</span></div></div>
        <div class="catc-event"><div class="catc-date">11 Jun 2018</div><div><strong>Independent economic work was prepared for court use and a request was made to seek judicial compulsion of the AC.</strong> A 15-page expert note analysed LPB’s CEXP economic rights and the operating-cost mechanism. It expressly identified the €737,338.85 CEXP-related receivable in the AC’s January 2013 report and developed a materially wider preliminary economic analysis. The note is marked draft/confidential, so the public site uses its methodology and existence without publishing privileged/confidential strategy.<br><span class="catc-tag">expert work product</span><span class="catc-tag">court-use purpose</span></div></div>
        <div class="catc-event"><div class="catc-date">15 Jun 2018</div><div><strong>The CEXP right was expressly framed as a real LPB receivable to be defended before the judge.</strong> A contemporaneous sent communication states the group’s position that the right appeared in the definitive insolvency texts, derived from CEXP and had to be defended judicially; it also records the contemporaneous allegation that the AC had failed to give it proper effect. The recognition point still requires the definitive-text primary source for final verification.<br><span class="catc-tag">contemporaneous party position</span><span class="catc-tag">judicial defence attempt</span></div></div>
        <div class="catc-event"><div class="catc-date">20 Jun–8 Jul 2018</div><div><strong>Expert quantification, property/participation mapping and cost allocation continued after the June rupture.</strong> The evidence set includes an expert-report circulation, CEXP participation/square-metre/benefit mapping, statutes and exploitation-contract material, a request to initiate recovery of LPB’s CEXP rights, and a comparison of exploitation costs against Owners’ Community costs.<br><span class="catc-tag">expert material</span><span class="catc-tag">operating-economics reconstruction</span></div></div>
        <div class="catc-event"><div class="catc-date">12–21 Nov 2018</div><div><strong>The CEXP calculation was prepared for judicial presentation and the Judge/AC were targeted for notification.</strong> The record includes preparation of a CEXP-credit calculation for presentation to the judge, a contemporaneous notification effort directed to the Judge and AC, and circulation of updated/final expert materials.<br><span class="catc-tag">judicial/AC notification attempt</span><span class="catc-tag">expert update</span></div></div>
        <div class="catc-event"><div class="catc-date">14 Dec 2018</div><div><strong>Formal follow-up on hotel exploitation information.</strong> Counsel prepared a formal request to the AC concerning exploitation of the hotel complex, continuing the accounting/operating-information track after the change in physical control.<br><span class="catc-tag">formal information request</span></div></div>
      </div>
      <div class="catc-conclusion"><strong>Controlled conclusion.</strong> The evidence now supports saying that the CEXP/productive-unit case was repeatedly advanced during the life of the concurso and was not invented after the calificación. In identified instances it met an express AC role limitation, operative-control restrictions, a contemporaneous allegation of non-action, or a perceived need to seek judicial intervention. This materially strengthens the request for a document-by-document explanation of what was received, acted upon, valued, rejected, omitted or left unresolved.</div>
      <div class="catc-boundary"><strong>What this still does not prove.</strong> The chain does not establish that every document was formally filed, admitted or read by the Judge; that every CEXP value belonged to LPB’s estate; or that deliberate suppression by the AC is proved. The strongest present formulation is repeated advancement plus item-specific obstruction/non-action evidence, with admission and procedural effect to be verified per document.</div>
      <div class="catc-actions"><a href="${links.value}">LPB value record</a><a class="secondary" href="${links.cexp}">CEXP / Community record</a><a class="secondary" href="${links.ac}">AC accountability</a><a class="secondary" href="${links.cal}">Calificación</a></div>
    </div>`;

  const esFull = `
    <div class="catc-panel">
      <p class="catc-kicker">CADENA CONTEMPORÁNEA DE INTENTOS · VALOR CEXP · 2015–2018</p>
      <h2>El valor de la unidad productiva no es una reconstrucción tardía. El expediente documenta intentos reiterados de introducir la economía, los créditos y la estructura operativa de la CEXP ante quienes debían decidir.</h2>
      <p class="catc-lead">El registro controlado permite ya una formulación más fuerte que una mera reconstrucción posterior: entre 2015 y 2018 LPB/Aweswell y sus asesores plantearon reiteradamente la gobernanza Comunidad/CEXP, los costes de explotación, derechos de ingresos, acceso, créditos vinculados a CEXP y la economía de la unidad productiva. Algunos hitos tienen respuesta directa de la AC; otros cuentan con metadatos de documentos sellados, trabajo pericial o preparación expresa para presentación judicial/ante la AC.</p>
      <ul class="catc-status"><li>Cadena contemporánea verificada</li><li>Respuesta directa AC localizada</li><li>Nota pericial 11 Jun 2018</li><li class="open">Admisión/decisión formal varía por documento</li></ul>
      <div class="catc-timeline">
        <div class="catc-event"><div class="catc-date">23 Nov 2015</div><div><strong>Solicitud de implicación de la AC en el problema comunitario.</strong> Un intercambio directo documenta la petición de intervención en la gobernanza de la Comunidad. La AC respondió delimitando lo que consideraba dentro de sus funciones y ofreciendo una vía más limitada de nota/autorización.<br><span class="catc-tag">respuesta externa verificada</span></div></div>
        <div class="catc-event"><div class="catc-date">25 May 2017</div><div><strong>Material sellado preparado para remisión a la AC y al Juzgado Mercantil.</strong> El correo contemporáneo identifica un documento sellado y la instrucción expresa de remitirlo cuanto antes a la AC y formalmente al juzgado como prueba adicional de colaboración. Su contenido sustantivo se mantiene sometido a control de fuente.<br><span class="catc-tag">metadatos documento sellado</span><span class="catc-tag">intento de presentación</span></div></div>
        <div class="catc-event"><div class="catc-date">19–22 Jan 2018</div><div><strong>La propia AC trató la economía vinculada a CEXP.</strong> El registro muestra requerimientos de soporte sobre apuntes contables de LPB frente a CEXP, incluido un “Dividendo a Cobrar de C.E. Sun Park” de 737.338,85 €, mientras la AC también ejercía control operativo sobre acceso/instrucciones de LPB. Esto acredita conocimiento de una capa económica CEXP material, no su tratamiento jurídico final.<br><span class="catc-tag">conocimiento AC</span><span class="catc-tag">registro contable</span></div></div>
        <div class="catc-event"><div class="catc-date">11 Jun 2018</div><div><strong>Se preparó trabajo económico independiente para uso judicial y se pidió promover que el juez compeliera a la AC.</strong> Una nota pericial de 15 páginas analizó los derechos económicos de LPB frente a CEXP y el mecanismo de costes de explotación. Identificó expresamente el crédito CEXP de 737.338,85 € en el informe de la AC de enero de 2013 y desarrolló un análisis económico preliminar más amplio. La nota está marcada borrador/confidencial; por ello la web publica su existencia y metodología, no estrategia confidencial.<br><span class="catc-tag">trabajo pericial</span><span class="catc-tag">finalidad judicial</span></div></div>
        <div class="catc-event"><div class="catc-date">15 Jun 2018</div><div><strong>El derecho CEXP se formuló expresamente como crédito real de LPB a defender ante el juez.</strong> Una comunicación contemporánea enviada recoge la posición de que el derecho figuraba en los textos definitivos, derivaba de la CEXP y debía defenderse judicialmente; también deja constancia de la alegación contemporánea de que la AC no le había dado efecto adecuado. El punto de reconocimiento exige aún contraste con el texto definitivo primario.<br><span class="catc-tag">posición contemporánea de parte</span><span class="catc-tag">intento de defensa judicial</span></div></div>
        <div class="catc-event"><div class="catc-date">20 Jun–8 Jul 2018</div><div><strong>Continuaron la cuantificación pericial, el mapa finca/participación y la distribución de costes.</strong> El conjunto localizado incluye circulación de informe pericial, mapas de participación/superficie/beneficios CEXP, estatutos y contrato de explotación, solicitud de iniciar el cobro de derechos de LPB y comparación de costes de la explotadora frente a costes de la Comunidad de Propietarios.<br><span class="catc-tag">material pericial</span><span class="catc-tag">reconstrucción económica operativa</span></div></div>
        <div class="catc-event"><div class="catc-date">12–21 Nov 2018</div><div><strong>El cálculo CEXP se preparó para presentación judicial y se dirigieron actuaciones de notificación al Juez/AC.</strong> El registro incluye preparación de un cálculo de crédito CEXP para llevar al juez, un esfuerzo contemporáneo de notificación al Juez y a la AC y circulación de materiales periciales actualizados/finales.<br><span class="catc-tag">intento notificación juez/AC</span><span class="catc-tag">actualización pericial</span></div></div>
        <div class="catc-event"><div class="catc-date">14 Dec 2018</div><div><strong>Seguimiento formal sobre información de explotación hotelera.</strong> Se preparó una solicitud formal a la AC sobre la explotación del complejo, prolongando la línea contable/operativa tras el cambio de control físico.<br><span class="catc-tag">solicitud formal de información</span></div></div>
      </div>
      <div class="catc-conclusion"><strong>Conclusión controlada.</strong> La prueba permite afirmar ya que la cuestión CEXP/unidad productiva fue planteada reiteradamente durante la vida del concurso y no nació después de la calificación. En hitos identificados encontró una delimitación expresa de funciones por la AC, restricciones de control operativo, una alegación contemporánea de inacción o la necesidad percibida de promover intervención judicial. Esto refuerza materialmente la exigencia de explicar documento por documento qué se recibió, valoró, actuó, rechazó, omitió o dejó sin resolver.</div>
      <div class="catc-boundary"><strong>Lo que todavía no prueba.</strong> La cadena no acredita que cada documento fuera formalmente presentado, admitido o leído por el juez; que todo valor CEXP perteneciera a la masa de LPB; ni que esté probada una supresión deliberada por la AC. La formulación más fuerte hoy es avance reiterado más prueba de obstáculo/no actuación en hitos concretos, quedando por verificar admisión y efecto procesal documento a documento.</div>
      <div class="catc-actions"><a href="${links.value}">Valor y cuentas LPB</a><a class="secondary" href="${links.cexp}">CEXP / Comunidad</a><a class="secondary" href="${links.ac}">Responsabilidad AC</a><a class="secondary" href="${links.cal}">Calificación</a></div>
    </div>`;

  const enCompact = `<div class="catc-panel"><p class="catc-kicker">CEXP ATTEMPT CHAIN · 2015–2018</p><h2>The productive-unit case was repeatedly advanced during the concurso—not invented after it.</h2><p>Direct AC correspondence, stamped-document metadata, the January 2018 CEXP accounting exchange, June 2018 expert/court-use work, later recovery and mapping work, and November–December judicial/AC follow-up now form a dated chain. Formal admission and effect remain document-specific.</p><div class="catc-actions"><a href="${links.ac}">Open the AC accountability chain</a><a class="secondary" href="${links.value}">LPB value record</a></div></div>`;
  const esCompact = `<div class="catc-panel"><p class="catc-kicker">CADENA DE INTENTOS CEXP · 2015–2018</p><h2>La cuestión de la unidad productiva fue planteada reiteradamente durante el concurso; no nació después.</h2><p>Correspondencia directa con la AC, metadatos de documentos sellados, el intercambio contable CEXP de enero de 2018, trabajo pericial/judicial de junio y actuaciones posteriores de cobro, mapeo y notificación forman ya una cadena fechada. La admisión y efecto formal siguen siendo específicos de cada documento.</p><div class="catc-actions"><a href="${links.ac}">Abrir cadena de responsabilidad AC</a><a class="secondary" href="${links.value}">Valor LPB</a></div></div>`;

  const mount = () => {
    if (document.getElementById('cexp-productive-unit-attempt-chain')) return;
    const main = document.querySelector('main');
    if (!main) return;
    addStyles();
    const section = document.createElement('section');
    section.id = 'cexp-productive-unit-attempt-chain';
    section.className = `section catc${compact ? ' catc-compact' : ''}`;
    section.innerHTML = `<div class="shell catc-shell">${full ? (es ? esFull : enFull) : (es ? esCompact : enCompact)}</div>`;
    const headline = document.getElementById('cexp-productive-unit-value-headline');
    const thesis = main.querySelector('[data-calificacion-misuse-thesis]');
    if (headline) headline.insertAdjacentElement('afterend', section);
    else if (thesis) thesis.insertAdjacentElement('afterend', section);
    else {
      const first = Array.from(main.children).find(node => node.tagName === 'SECTION');
      if (first) first.insertAdjacentElement('afterend', section); else main.prepend(section);
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount, { once: true });
  else mount();
  window.setTimeout(mount, 2200);
})();
