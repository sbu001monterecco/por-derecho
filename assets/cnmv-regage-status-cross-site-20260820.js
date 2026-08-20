(() => {
  const path = window.location.pathname.replace(/index\.html$/, '');
  const canonicalRoutes = [
    '/es/cnmv-ricpe-verificacion/',
    '/en/cnmv-ricpe-verification/'
  ];
  const targets = [
    ...canonicalRoutes,
    '/es/ric-private-equity-sun-park/',
    '/en/ric-private-equity-sun-park/',
    '/es/orion-ricpe-continuidad/',
    '/en/orion-ricpe-platform-continuity/',
    '/es/portfolio-orion-trazabilidad/',
    '/en/portfolio-orion-traceability/',
    '/es/ricpe-responsabilidad-documental/',
    '/en/ricpe-documentary-accountability/',
    '/es/san-telmo-ricpe-sun-park/',
    '/en/san-telmo-ricpe-sun-park/',
    '/es/pwc-canarias-carlos-saavedra-sun-park/',
    '/en/pwc-canarias-carlos-saavedra-sun-park/',
    '/es/grant-thornton/2024-04/',
    '/en/grant-thornton/2024-04/',
    '/es/rsm/nnr4-1025c2f66/',
    '/en/rsm/nnr4-1025c2f66/',
    '/es/actualizaciones/',
    '/en/updates/'
  ];

  const matched = targets.some((route) => path.endsWith(route));
  if (!matched) return;

  const isEnglish = /\/en\//.test(path);
  const isCanonical = canonicalRoutes.some((route) => path.endsWith(route));
  const statusHref = isCanonical
    ? '#cnmv-acciones-360'
    : isEnglish
      ? '/por-derecho/en/cnmv-ricpe-verification/'
      : '/por-derecho/es/cnmv-ricpe-verificacion/';

  const copy = isEnglish
    ? {
        label: 'CNMV · verified procedural update',
        title: 'Email sent · REGAGE26e00074329732 registered · receipt followed up',
        body: 'The 20 August 2026 cross-border communication is now traceable through both email and the AGE registry. A substantive CNMV acknowledgement, corpus incorporation, functional file linkage, preservation confirmation and process owner remain pending. Gil Marer does not currently act for LPB.',
        link: isCanonical ? 'Open the 360 action control →' : 'Open verified status and 360 action control →'
      }
    : {
        label: 'CNMV · actualización procesal verificada',
        title: 'Correo enviado · REGAGE26e00074329732 registrado · justificante remitido',
        body: 'La comunicación transfronteriza de 20 de agosto de 2026 ya es trazable por correo y por registro AGE. Permanecen pendientes el acuse sustantivo de la CNMV, la incorporación al corpus, la vinculación funcional, la confirmación de preservación y la unidad responsable. Gil Marer no comparece actualmente por LPB.',
        link: isCanonical ? 'Abrir el control de acciones 360 →' : 'Abrir estado verificado y control 360 →'
      };

  const style = document.createElement('style');
  style.textContent = `
    .cnmv-regage-cross-site{background:#edf3ee;border-block:1px solid #9bb3a2;padding:1.05rem 0;color:#172b34}
    .cnmv-regage-cross-site__inner{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:1.25rem;align-items:center}
    .cnmv-regage-cross-site__label{margin:0 0 .28rem;font-size:.68rem;letter-spacing:.09em;text-transform:uppercase;font-weight:900;color:#496653}
    .cnmv-regage-cross-site h2{margin:0 0 .35rem;font-size:clamp(1.08rem,2vw,1.42rem);line-height:1.18}
    .cnmv-regage-cross-site p{margin:0;max-width:82ch;font-size:.88rem;line-height:1.55}
    .cnmv-regage-cross-site a{display:inline-flex;align-items:center;justify-content:center;border-radius:999px;background:#13252d;color:#fff;text-decoration:none;font-weight:850;padding:.7rem .9rem;white-space:nowrap}
    .cnmv-regage-360{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.85rem;margin-top:1.2rem}
    .cnmv-regage-360 article{background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:14px;padding:1rem}
    .cnmv-regage-360 h3{margin:.2rem 0 .48rem;font-size:1.04rem}
    .cnmv-regage-360 p{margin:0;font-size:.88rem;line-height:1.55}
    .cnmv-regage-integrity{overflow-wrap:anywhere;background:#172b34;color:#fff;border-radius:11px;padding:.9rem;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.76rem;line-height:1.5}
    .cnmv-regage-capacity{border-left:5px solid #8b6629;background:#fff4df;padding:1rem;border-radius:12px;margin-top:1rem}
    @media(max-width:760px){.cnmv-regage-cross-site__inner,.cnmv-regage-360{grid-template-columns:1fr}.cnmv-regage-cross-site a{justify-self:start;white-space:normal}}
  `;
  document.head.appendChild(style);

  const replaceCanonicalStatus = (main) => {
    if (!isCanonical) return;

    document.title = isEnglish
      ? 'CNMV / RICPE / Sun Park / Orion — registered status and supervisory review | Project Sun Rock'
      : 'CNMV / RICPE / Sun Park / Orion — estado registrado y revisión supervisora | Project Sun Rock';
    const description = document.querySelector('meta[name="description"]');
    if (description) {
      description.content = isEnglish
        ? 'CNMV professional route: 2021 alert, July 2021 missing records, REGAGE26e00074329732, RICPE/Orion reconciliation, preservation and 360 action control.'
        : 'Ruta profesional CNMV: alerta 2021, documentos ausentes de julio de 2021, REGAGE26e00074329732, conciliación RICPE/Orion, preservación y control 360.';
    }

    const sections = [...main.querySelectorAll(':scope > section')];
    const finalStatus = sections.find((section) => {
      const heading = section.querySelector('h2');
      if (!heading) return false;
      const text = heading.textContent.toLowerCase();
      return text.includes('transmisión institucional') || text.includes('institutional transmission');
    });

    if (finalStatus && !document.querySelector('#cnmv-acciones-360')) {
      const actions = document.createElement('section');
      actions.className = 'section alt';
      actions.id = 'cnmv-acciones-360';
      actions.innerHTML = isEnglish
        ? `<div class="shell cnmv"><p class="ok-kicker">360 · CRITICAL ACTION CONTROL</p><h2>The communication is complete; the evidential and supervisory closure is not.</h2><div class="cnmv-regage-360"><article><h3>P0 · CNMV linkage and secure production</h3><p>Obtain a substantive acknowledgement linking REGAGE26e00074329732 to the earlier references, identify the responsible unit and secure channel, and provide the original signed resolution, July 2021 records, native emails/RFC822, metadata, native images and hashes where requested. Transmission is not incorporation.</p></article><article><h3>P1 · Instrument-by-instrument reconciliation</h3><p>Compare RICPE materials, Orion's issue document and the 2026 capital increase; reconcile 42/19/17/22 against 42/21/17/20 and €6,570,713.56 against €6,573,703.10; obtain executed finance, drawdowns, security, repayment, cap table, valuations and related-party approvals.</p></article><article><h3>P1 · Portfolio and RICPE internal processes</h3><p>Place the later official CNMV resolution and registered update before Portfolio, which previously requested authority records. Capture the complete 19 August RICPE notification and obtain preservation, conflict-screening, independent ownership and process-status confirmation.</p></article><article><h3>P2 · Professional custody and cross-border nexus</h3><p>Track PwC, Grant Thornton and RSM without treating silence as admission. Establish actual UK or other foreign distribution, investor, bank, custodian, adviser, insurer, loss or document links before an FCA, ESMA or other foreign-regulator step.</p></article></div><div class="cnmv-regage-capacity"><strong>Capacity control:</strong> Gil Marer acts first in his own name and additionally for Aweswell Limited and subsidiaries for which he retains valid authority. He does not currently act for LPB because his administration and representation powers are suspended in the insolvency proceedings.</div><h3>Registered-file integrity</h3><p class="cnmv-regage-integrity">REGAGE26e00074329732 · presentation 20/08/2026 15:11:09 · SHA-512 48e2e55a7e4553f3d87edcf893e7800c1c2d290ef11287d47675b6b9963d8100e87a6f963c31bcade9daa0ff064597bbf586ee3be8c6ff92b720f74adf10d459</p></div>`
        : `<div class="shell cnmv"><p class="ok-kicker">360 · CONTROL DE ACCIONES CRÍTICAS</p><h2>La comunicación está completa; el cierre probatorio y supervisor no.</h2><div class="cnmv-regage-360"><article><h3>P0 · vinculación CNMV y producción segura</h3><p>Obtener un acuse sustantivo que vincule REGAGE26e00074329732 con las referencias anteriores, identifique unidad responsable y canal seguro, y permita aportar la resolución original firmada, documentos de julio de 2021, correos nativos/RFC822, metadatos, imágenes nativas y hashes cuando se soliciten. Transmisión no equivale a incorporación.</p></article><article><h3>P1 · conciliación instrumento por instrumento</h3><p>Comparar materiales RICPE, documento de emisión Orion y ampliación de 2026; reconciliar 42/19/17/22 frente a 42/21/17/20 y €6.570.713,56 frente a €6.573.703,10; obtener financiación ejecutada, drawdowns, garantías, pagos, cap table, valoraciones y aprobaciones de partes vinculadas.</p></article><article><h3>P1 · procesos Portfolio y canal interno RICPE</h3><p>Poner la resolución oficial posterior y el nuevo registro ante Portfolio, que pidió documentos de autoridad. Capturar íntegramente la notificación RICPE de 19 de agosto y obtener confirmación de preservación, conflicto, responsable independiente y estado procesal.</p></article><article><h3>P2 · custodia profesional y nexo transfronterizo</h3><p>Controlar PwC, Grant Thornton y RSM sin tratar silencio como admisión. Acreditar distribución, inversores, bancos, custodios, asesores, aseguradores, daños o documentos en Reino Unido u otra jurisdicción antes de una actuación FCA, ESMA u otro regulador extranjero.</p></article></div><div class="cnmv-regage-capacity"><strong>Control de capacidad:</strong> Gil Marer comparece primero en su propio nombre y adicionalmente por Aweswell Limited y filiales respecto de las cuales conserva facultades vigentes. No comparece actualmente por LPB, al encontrarse suspendidas sus facultades de administración y representación en el marco concursal.</div><h3>Integridad del archivo registrado</h3><p class="cnmv-regage-integrity">REGAGE26e00074329732 · presentación 20/08/2026 15:11:09 · SHA-512 48e2e55a7e4553f3d87edcf893e7800c1c2d290ef11287d47675b6b9963d8100e87a6f963c31bcade9daa0ff064597bbf586ee3be8c6ff92b720f74adf10d459</p></div>`;
      finalStatus.insertAdjacentElement('beforebegin', actions);
    }

    if (finalStatus) {
      const shell = finalStatus.querySelector('.shell') || finalStatus;
      shell.innerHTML = isEnglish
        ? `<p class="ok-kicker">CONTROLLED PUBLIC STATUS</p><h2>Email sent, AGE registration completed and official receipt followed up.</h2><p>The 20 August 2026 communication was sent to five CNMV mailboxes, registered as <strong>REGAGE26e00074329732</strong>, and followed up in the same email thread with the official receipt. No delivery failure has been located. The only response currently identified is an automatic absence message from the International Affairs perimeter; it is not a substantive acknowledgement.</p><p class="source-box"><strong>Still pending:</strong> CNMV confirmation of corpus incorporation, functional linkage, preservation, coordinating unit, secure channel, correction, requirement, referral or decision. The public site will not describe any of those states as completed until a primary record proves them.</p><div class="ok-actions"><a href="#cnmv-acciones-360">Open the 360 action control</a><a class="secondary" href="../ric-private-equity-sun-park/">Open the RICPE dossier</a></div>`
        : `<p class="ok-kicker">ESTADO PÚBLICO CONTROLADO</p><h2>Correo enviado, registro AGE completado y justificante oficial remitido.</h2><p>La comunicación de 20 de agosto de 2026 fue enviada a cinco buzones CNMV, registrada como <strong>REGAGE26e00074329732</strong> y seguida en el mismo hilo mediante el justificante oficial. No se ha localizado fallo de entrega. La única respuesta identificada es un mensaje automático de ausencia del perímetro de Asuntos Internacionales; no constituye acuse sustantivo.</p><p class="source-box"><strong>Sigue pendiente:</strong> confirmación CNMV de incorporación al corpus, vinculación funcional, preservación, unidad coordinadora, canal seguro, corrección, requerimiento, remisión o decisión. El sitio público no describirá ninguno de esos estados como completado sin una fuente primaria que lo pruebe.</p><div class="ok-actions"><a href="#cnmv-acciones-360">Abrir el control de acciones 360</a><a class="secondary" href="../ric-private-equity-sun-park/">Abrir expediente RICPE</a></div>`;
    }
  };

  const inject = () => {
    if (document.querySelector('[data-cnmv-regage-status="20260820"]')) return;
    const main = document.querySelector('main');
    if (!main) return;
    const firstSection = main.querySelector(':scope > section');
    if (!firstSection) return;

    const section = document.createElement('section');
    section.className = 'cnmv-regage-cross-site';
    section.dataset.cnmvRegageStatus = '20260820';
    section.setAttribute('aria-label', copy.label);
    section.innerHTML = `
      <div class="shell cnmv-regage-cross-site__inner">
        <div>
          <p class="cnmv-regage-cross-site__label">${copy.label}</p>
          <h2>${copy.title}</h2>
          <p>${copy.body}</p>
        </div>
        <a href="${statusHref}">${copy.link}</a>
      </div>`;
    firstSection.insertAdjacentElement('afterend', section);
    replaceCanonicalStatus(main);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inject, { once: true });
  } else {
    inject();
  }
})();
