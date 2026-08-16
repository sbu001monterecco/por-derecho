(() => {
  const path = location.pathname;
  const isEn = /\/en\//.test(path);

  const make = (html) => {
    const t = document.createElement('template');
    t.innerHTML = html.trim();
    return t.content.firstElementChild;
  };

  const patchHome = () => {
    const summary = document.querySelector(isEn ? '#sixty-second-summary' : '#resumen-60-segundos');
    const story = document.querySelector(isEn ? '#reverse-engineered-story' : '#historia-reconstruida');
    [summary, story].filter(Boolean).forEach((scope) => {
      scope.querySelectorAll('a[href^="ric-private-equity-sun-park/"]').forEach((a) => {
        const href = a.getAttribute('href') || '';
        if (href.includes('control-titulo-2018-pwc-unidades') || href.includes('title-control-2018-pwc-units')) return;
        a.setAttribute('href', isEn ? 'ricpe-documentary-accountability/' : 'ricpe-responsabilidad-documental/');
        if (/dossier principal|main dossier/i.test(a.textContent || '')) {
          a.textContent = isEn ? 'Open canonical RICPE accountability' : 'Abrir responsabilidad documental RICPE';
        }
      });
    });

    if (story && !story.querySelector('[data-ricpe-governance-note]')) {
      const rows = [...story.querySelectorAll('li')];
      const row2020 = rows.find((li) => /2020/.test(li.querySelector('.reverse-year')?.textContent || ''));
      if (row2020) {
        const note = document.createElement('p');
        note.setAttribute('data-ricpe-governance-note', 'true');
        note.className = 'qualification';
        note.innerHTML = isEn
          ? '<strong>Pre-existing governance:</strong> the official CNMV register places José Acosta Matos on the RICPE board from 4 November 2019, before the June and November 2020 Sun Park investor communications. This makes conflict, related-party, information-flow, abstention, review and approval traceability part of the 2020 question. <a href="ricpe-documentary-accountability/">Open the canonical RICPE record →</a>'
          : '<strong>Gobernanza previa:</strong> el registro oficial de la CNMV sitúa a José Acosta Matos en el consejo de RICPE desde el 4 de noviembre de 2019, antes de las comunicaciones a inversores de junio y noviembre de 2020 sobre Sun Park. Por ello, conflicto, parte relacionada, flujo de información, abstención, revisión y aprobación forman parte de la cuestión de 2020. <a href="ricpe-responsabilidad-documental/">Abrir el registro canónico RICPE →</a>';
        row2020.querySelector('div')?.appendChild(note);
      }
    }
  };

  const patchLegacyRicpe = () => {
    if (!/\/ric-private-equity-sun-park\/?$/.test(path)) return;
    if (!document.querySelector('[data-ricpe-archive-banner]')) {
      const header = document.querySelector('.site-header');
      const banner = make(isEn
        ? '<aside data-ricpe-archive-banner class="priority-band"><div class="shell priority-inner"><p><strong>EXPANDED DOSSIER / BACKGROUND ARCHIVE.</strong> This page preserves the extended RICPE/A&amp;G chronology, professional context and historical material. For the current controlled position on RICPE governance, Sun Park knowledge, finance, ERDF, CNMV/Portfolio and the RICPE→AGM→Orion chain, use the canonical documentary-accountability page.</p><div class="priority-links"><a href="../ricpe-documentary-accountability/">Canonical RICPE accountability →</a><a href="../orion-ricpe-platform-continuity/">Orion / AGM nexus →</a></div></div></aside>'
        : '<aside data-ricpe-archive-banner class="priority-band"><div class="shell priority-inner"><p><strong>EXPEDIENTE AMPLIADO / ARCHIVO DE ANTECEDENTES.</strong> Esta página conserva la cronología ampliada RICPE/A&amp;G, contexto profesional y material histórico. Para la posición actual y controlada sobre gobernanza RICPE, conocimiento Sun Park, financiación, FEDER, CNMV/Portfolio y la cadena RICPE→AGM→Orion, utilice la página canónica de responsabilidad documental.</p><div class="priority-links"><a href="../ricpe-responsabilidad-documental/">Responsabilidad documental RICPE →</a><a href="../orion-ricpe-continuidad/">Nexo Orion / AGM →</a></div></div></aside>');
      header?.insertAdjacentElement('afterend', banner);
    }
    const eyebrow = document.querySelector('.dossier-hero .eyebrow');
    if (eyebrow) eyebrow.textContent = isEn
      ? 'EXPANDED DOSSIER / BACKGROUND ARCHIVE · historical record through 14 August 2026'
      : 'EXPEDIENTE AMPLIADO / ARCHIVO DE ANTECEDENTES · registro histórico hasta 14 agosto 2026';
  };

  const patchRicpePreFiling = () => {
    const es = /\/es\/ricpe-responsabilidad-documental\/?$/.test(path);
    const en = /\/en\/ricpe-documentary-accountability\/?$/.test(path);
    if (!es && !en) return;
    if (document.querySelector('[data-ricpe-prefiling-status]')) return;

    const hero = document.querySelector('.hero');
    const section = make(en
      ? '<section class="section alt" id="formal-communication-17aug" data-ricpe-prefiling-status><div class="shell"><p class="eyebrow">FORMAL COMMUNICATION STATUS · 17 AUGUST 2026</p><h2>Final V5 prepared for digital signature and submission to RICPE.</h2><p>Gil Marer, writing from San Cristóbal de La Laguna, has prepared a 21-page formal communication addressed exclusively to RICPE. It is intended to be digitally signed and submitted through the RICPE Ethical Channel and by corporate email on 17 August 2026.</p><p class="warn"><strong>Current controlled status:</strong> the document is prepared, but at the time of this update no Ethical Channel receipt, case code, signed-file hash or corporate-email transmission record has been recorded. It is therefore not described as filed, received, admitted or examined.</p><p><strong>Status grammar:</strong> prepared ≠ signed ≠ filed ≠ received ≠ admitted ≠ examined ≠ decided. After filing, this record will be updated with the public-safe reference, signed PDF SHA-256 and each later CNMV or other-authority transmission as a separate institutional event. The full binary and access credentials are not published at this stage.</p></div></section>'
      : '<section class="section alt" id="comunicacion-formal-17ago" data-ricpe-prefiling-status><div class="shell"><p class="eyebrow">ESTADO DE LA COMUNICACIÓN FORMAL · 17 AGOSTO 2026</p><h2>V5 final preparada para firma electrónica y presentación ante RICPE.</h2><p>Gil Marer, desde San Cristóbal de La Laguna, ha preparado una comunicación formal de 21 páginas dirigida exclusivamente a RICPE. Está prevista su firma electrónica y presentación por el Canal Ético de RICPE y por correo corporativo el 17 de agosto de 2026.</p><p class="warn"><strong>Estado controlado actual:</strong> el documento está preparado, pero en el momento de esta actualización no consta todavía justificante del Canal Ético, código de expediente, hash del PDF firmado ni registro de envío por correo corporativo. Por ello no se describe como presentado, recibido, admitido o examinado.</p><p><strong>Gramática de estado:</strong> preparado ≠ firmado ≠ presentado ≠ recibido ≠ admitido ≠ examinado ≠ decidido. Tras la presentación, este registro se actualizará con la referencia pública segura, el SHA-256 del PDF firmado y cada remisión posterior a CNMV u otra autoridad como evento institucional separado. En esta fase no se publica el binario completo ni credenciales de acceso.</p></div></section>');
    hero?.insertAdjacentElement('afterend', section);
  };

  const patchUpdates = () => {
    const es = /\/es\/actualizaciones\/?$/.test(path);
    const en = /\/en\/updates\/?$/.test(path);
    if (!es && !en) return;
    const status = document.querySelector('.update-status strong');
    if (status) status.textContent = en ? '17 August 2026' : '17 agosto 2026';

    const hero = document.querySelector('.updates-hero');
    if (!document.querySelector('#ricpe-formal-prefiling-17aug')) {
      const prefiling = make(en
        ? '<section class="updates-section" data-ricpe-prefiling-update><div class="shell"><section class="date-group"><h2>17 August 2026 · RICPE</h2><div class="update-stream"><article class="material-update institutional" id="ricpe-formal-prefiling-17aug"><div class="update-meta"><span class="new">Prepared</span><span>Pending signature</span><span>Pending filing</span></div><h3>Final V5 formal communication prepared for controlled submission to RICPE</h3><p>Gil Marer, writing from San Cristóbal de La Laguna, has prepared a 21-page communication addressed exclusively to RICPE for digital signature and submission through the Ethical Channel and corporate email on 17 August 2026.</p><p><strong>Evidence boundary:</strong> no filing receipt or signed-file hash has yet been recorded, so this update does not say the communication has been filed, received, admitted or examined. After filing, the record will add the public-safe reference, signed-file SHA-256 and any later CNMV or other-authority transmission separately.</p><div class="update-actions"><a class="button" href="../ricpe-documentary-accountability/#formal-communication-17aug">Current RICPE status →</a></div></article></div></section></div></section>'
        : '<section class="updates-section" data-ricpe-prefiling-update><div class="shell"><section class="date-group"><h2>17 agosto 2026 · RICPE</h2><div class="update-stream"><article class="material-update institutional" id="ricpe-formal-prefiling-17aug"><div class="update-meta"><span class="new">Preparada</span><span>Pendiente de firma</span><span>Pendiente de presentación</span></div><h3>Comunicación formal V5 final preparada para presentación controlada ante RICPE</h3><p>Gil Marer, desde San Cristóbal de La Laguna, ha preparado una comunicación de 21 páginas dirigida exclusivamente a RICPE para firma electrónica y presentación por el Canal Ético y correo corporativo el 17 de agosto de 2026.</p><p><strong>Límite probatorio:</strong> todavía no se ha registrado justificante de presentación ni hash del archivo firmado, por lo que esta actualización no afirma que la comunicación haya sido presentada, recibida, admitida o examinada. Tras la presentación se añadirán la referencia pública segura, el SHA-256 del PDF firmado y cada remisión posterior a CNMV u otra autoridad por separado.</p><div class="update-actions"><a class="button" href="../ricpe-responsabilidad-documental/#comunicacion-formal-17ago">Estado actual RICPE →</a></div></article></div></section></div></section>');
      hero?.insertAdjacentElement('afterend', prefiling);
    }

    if (document.querySelector('#ricpe-orion-15aug')) return;
    const section = make(en
      ? '<section class="updates-section" data-canonical-update><div class="shell"><section class="date-group"><h2>15 August 2026 · RICPE / Orion / ERDF</h2><div class="update-stream"><article class="material-update institutional" id="ricpe-orion-15aug"><div class="update-meta"><span class="new">New</span><span>RICPE · AGM · Orion</span><span>ERDF · Portfolio · CNMV</span></div><h3>From project presentation to a documented architecture of governance, knowledge, management and finance</h3><p>The controlled record now begins with RICPE governance in 2019, compares the 2020 investor presentation with RICPE’s July-2021 fragmented-title/conditionality record, and follows the later financing and public-support layers through current MYND operation.</p><p>Orion is no longer treated as a remote or merely analogous vehicle: RICPE founded Orion as sole initial shareholder; Orion’s issue material describes a 17% RICPE convertible participating-finance channel; AGM is identified as strategic/asset manager; and the related-person disclosure reconnects JDAM with FMMM, Shaila Cogolludo, Antonio Cogolludo and Pamalexsha/related interests already present in the Sun Park record. Portfolio later confirmed an internal investigation, while CNMV stated that filing 2024136159 would be processed as a consultation. MYND’s permanent plaque expressly identifies ERDF.</p><p><strong>Boundary:</strong> those documented corporate, governance and finance bridges do not by themselves prove that specific MYND/Sun Park/LPB/Matkator proceeds or value funded Orion. That narrower asset/value trail is now the open financial question.</p><div class="update-actions"><a class="button" href="../ricpe-documentary-accountability/">Canonical RICPE page →</a><a class="button secondary" href="../orion-ricpe-platform-continuity/">Orion / AGM</a><a class="button secondary" href="../portfolio-orion-traceability/">Portfolio</a><a class="button secondary" href="../cnmv-ricpe-verification/">CNMV</a></div></article></div></section></div></section>'
      : '<section class="updates-section" data-canonical-update><div class="shell"><section class="date-group"><h2>15 agosto 2026 · RICPE / Orion / FEDER</h2><div class="update-stream"><article class="material-update institutional" id="ricpe-orion-15aug"><div class="update-meta"><span class="new">Nuevo</span><span>RICPE · AGM · Orion</span><span>FEDER · Portfolio · CNMV</span></div><h3>De una presentación de proyecto a una arquitectura documentada de gobernanza, conocimiento, gestión y financiación</h3><p>El registro controlado comienza ahora con la gobernanza RICPE en 2019, compara la presentación a inversores de 2020 con el registro RICPE de julio de 2021 sobre dominio fragmentado y condicionalidad, y sigue las capas posteriores de financiación y apoyo público hasta la explotación actual de MYND.</p><p>Orion deja de tratarse como vehículo remoto o meramente análogo: RICPE constituyó Orion como accionista único inicial; el Documento de Emisión describe un canal del 17% de financiación participativa convertible RICPE; AGM figura como gestor estratégico/de activos; y el disclosure de personas relacionadas vuelve a conectar a JDAM con FMMM, Shaila Cogolludo, Antonio Cogolludo y Pamalexsha/intereses relacionados ya presentes en el registro Sun Park. Portfolio confirmó después una investigación interna y CNMV indicó que el registro 2024136159 sería tramitado como consulta. La placa permanente de MYND identifica expresamente FEDER.</p><p><strong>Límite:</strong> esos puentes corporativos, de gobierno y financiación documentados no prueban por sí solos que ingresos o valor específico MYND/Sun Park/LPB/Matkator financiaran Orion. Esa trazabilidad patrimonial concreta es ahora la cuestión financiera abierta.</p><div class="update-actions"><a class="button" href="../ricpe-responsabilidad-documental/">Página canónica RICPE →</a><a class="button secondary" href="../orion-ricpe-continuidad/">Orion / AGM</a><a class="button secondary" href="../portfolio-orion-trazabilidad/">Portfolio</a><a class="button secondary" href="../cnmv-ricpe-verificacion/">CNMV</a></div></article></div></section></div></section>');
    hero?.insertAdjacentElement('afterend', section);
  };

  const patchSnca = () => {
    const es = /\/es\/snca-fondos-europeos-trazabilidad\/?$/.test(path);
    const en = /\/en\/snca-eu-funds-traceability\/?$/.test(path);
    if (!es && !en) return;
    [...document.querySelectorAll('li')].forEach((li) => {
      const text = li.textContent || '';
      if (es && text.includes('sin presuponer FEDER u otro fondo específico')) {
        li.innerHTML = '<strong>Instrumento FEDER:</strong> identificar programa/eje o instrumento exacto, porcentaje, gasto elegible certificado y pagado, hitos, verificaciones administrativas/sobre el terreno, auditorías, incidencias y cualquier corrección o reintegro.';
      }
      if (en && /without presuming ERDF|without assuming ERDF/i.test(text)) {
        li.innerHTML = '<strong>ERDF instrument:</strong> identify the exact programme/axis or instrument, percentage, eligible expenditure certified and paid, milestones, administrative/on-the-spot checks, audits, incidents and any correction or recovery.';
      }
    });
    if (!document.querySelector('[data-orion-snca-boundary]')) {
      const headings = [...document.querySelectorAll('h2')];
      const target = headings.find((h) => es ? /RIC, incentivo regional y UE/i.test(h.textContent || '') : /RIC, regional incentive and EU/i.test(h.textContent || ''));
      if (target) {
        const p = document.createElement('p');
        p.setAttribute('data-orion-snca-boundary', 'true');
        p.className = 'warn';
        p.innerHTML = es
          ? '<strong>Perímetro Orion separado:</strong> la continuidad RICPE→AGM→Orion se investiga por separado y no se utiliza aquí como evidencia sobre GC/836/P06/FEDER salvo que exista un enlace financiero, patrimonial, de costes, garantía, activo o beneficiario documentado.'
          : '<strong>Separate Orion perimeter:</strong> RICPE→AGM→Orion continuity is investigated separately and is not used here as evidence concerning GC/836/P06/ERDF unless a documented finance, asset, cost, guarantee, beneficiary or property link is produced.';
        target.parentElement?.appendChild(p);
      }
    }
  };

  patchHome();
  patchLegacyRicpe();
  patchRicpePreFiling();
  patchUpdates();
  patchSnca();
})();