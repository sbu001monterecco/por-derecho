(() => {
  if (window.__pdAssetRecoveryPreservation20260821) return;
  window.__pdAssetRecoveryPreservation20260821 = true;

  const path = location.pathname.replace(/\/index\.html$/, '/').replace(/\/$/, '/') || '/';
  const isEn = /\/en\//.test(path);
  const basePrefix = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const recoveryHref = isEn
    ? `${basePrefix}en/asset-recovery-intervention-confiscation/`
    : `${basePrefix}es/recuperacion-activos-intervencion-decomiso/`;

  const style = document.createElement('style');
  style.textContent = `
    .pd-ar-gateway{background:linear-gradient(135deg,#071820,#183f49);color:#fff;padding:2rem 0;border-top:1px solid rgba(255,255,255,.12);border-bottom:1px solid rgba(255,255,255,.12)}
    .pd-ar-gateway .pd-ar-inner{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(260px,.55fr);gap:1.3rem;align-items:center}
    .pd-ar-kicker{font-size:.76rem;font-weight:900;letter-spacing:.11em;text-transform:uppercase;color:#e9c987;margin:0 0 .45rem}
    .pd-ar-gateway h2{color:#fff;font-size:clamp(1.8rem,3.4vw,3.15rem);line-height:1.02;margin:.1rem 0 .65rem;max-width:20ch}
    .pd-ar-gateway p{color:#dce8e8;line-height:1.58;margin:.4rem 0}
    .pd-ar-gateway .pd-ar-rule{border-left:5px solid #c7902f;padding-left:1rem;font-weight:800;color:#fff}
    .pd-ar-gateway a.pd-ar-button{display:inline-flex;align-items:center;justify-content:center;text-decoration:none;border-radius:999px;padding:.8rem 1rem;background:#fff;color:#10242d;font-weight:900;text-align:center}
    .pd-ar-status-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.75rem;margin:1rem 0}
    .pd-ar-status-card{border:1px solid rgba(19,37,45,.15);border-left:5px solid #c7902f;border-radius:12px;background:#fff;padding:.9rem 1rem}
    .pd-ar-status-card strong{display:block;color:#13252d;margin-bottom:.25rem}
    .pd-ar-status-card p{margin:0;color:#40545c;line-height:1.5}
    .pd-ar-update{border:1px solid rgba(19,37,45,.15);border-top:6px solid #9c302c;border-radius:16px;background:#fff;padding:1.2rem;margin:1rem 0 1.4rem}
    .pd-ar-update h2,.pd-ar-update h3{margin:.15rem 0 .55rem;color:#13252d}
    .pd-ar-update .pd-ar-chain{font-weight:900;color:#13252d;line-height:1.7}
    @media(max-width:800px){.pd-ar-gateway .pd-ar-inner,.pd-ar-status-grid{grid-template-columns:1fr}}
  `;
  document.head.appendChild(style);

  const gateway = () => {
    const section = document.createElement('section');
    section.className = 'pd-ar-gateway';
    section.dataset.assetRecoveryGateway = '20260821';
    section.innerHTML = `<div class="shell pd-ar-inner"><div><p class="pd-ar-kicker">${isEn ? 'PRESERVE FIRST · TRACE THE VALUE · DECIDE THE MERITS AFTER' : 'PRESERVAR PRIMERO · SEGUIR EL VALOR · DECIDIR EL FONDO DESPUÉS'}</p><h2>${isEn ? 'The remedy must not arrive after the value has gone.' : 'El remedio no puede llegar cuando el valor ya se ha ido.'}</h2><p>${isEn ? 'The record now supports a direct institutional demand: identify what assets, income streams, rights, records and metadata are preserved today, by whom, under which statutory power and from what date.' : 'El registro ya permite una exigencia institucional directa: identificar qué activos, rentas, derechos, documentos y metadatos están preservados hoy, por quién, bajo qué potestad y desde qué fecha.'}</p><p class="pd-ar-rule">${isEn ? 'One economic chain can cross several legal persons and several files. The files may be separate. The value chain is not.' : 'Una cadena económica puede atravesar varias personas jurídicas y varios expedientes. Los expedientes pueden estar separados. La cadena de valor no.'}</p></div><div><a class="pd-ar-button" href="${recoveryHref}">${isEn ? 'Open the intervention & recovery architecture →' : 'Abrir la arquitectura de intervención y recuperación →'}</a></div></div>`;
    return section;
  };

  const injectGateway = () => {
    if (document.querySelector('[data-asset-recovery-gateway]')) return;
    const main = document.querySelector('main');
    if (!main) return;
    const home = /\/(en|es)\/$/.test(path) || /\/por-derecho\/(en|es)\/$/.test(path);
    const recovery = /(recovery-restitution-objectives|objetivos-recuperacion-restitucion)\/$/.test(path);
    const reverse = /(reverse-engineering-360-sun-park-chain|ingenieria-inversa-360-cadena-sun-park)\/$/.test(path);
    const perimeter = /(acosta-matos-perimeter|acosta-matos-perimetro)\/$/.test(path);
    const ricpe = /(ric-private-equity-sun-park|ricpe-documentary-accountability|ricpe-responsabilidad-documental|ricpe-idoneidad-series-f-g)\/$/.test(path);
    if (!(home || recovery || reverse || perimeter || ricpe)) return;

    const section = gateway();
    if (home) {
      const priority = document.querySelector('.priority-band');
      if (priority) priority.insertAdjacentElement('afterend', section); else main.insertAdjacentElement('afterbegin', section);
    } else if (recovery) {
      const target = document.querySelector('#routes, #vias');
      if (target) target.insertAdjacentElement('beforebegin', section); else main.insertAdjacentElement('afterbegin', section);
    } else {
      const hero = main.querySelector(':scope > .dossier-hero, :scope > .hero, :scope > section.hero, :scope > .mhero');
      if (hero) hero.insertAdjacentElement('afterend', section); else main.insertAdjacentElement('afterbegin', section);
    }
  };

  const injectInstitutional = () => {
    if (!/(institutional-records|registros-institucionales)\/$/.test(path) || document.querySelector('[data-asset-recovery-institutional]')) return;
    const main = document.querySelector('main');
    if (!main) return;
    const section = document.createElement('section');
    section.className = 'section';
    section.dataset.assetRecoveryInstitutional = '20260821';
    section.innerHTML = `<div class="shell"><p class="pd-ar-kicker" style="color:#8a651f">${isEn ? '20–21 AUGUST 2026 · PROCEDURAL CORRECTIONS + PRESERVATION' : '20–21 AGOSTO 2026 · CORRECCIONES PROCESALES + PRESERVACIÓN'}</p><h2>${isEn ? 'The record moved. So must the institutional map.' : 'El registro se movió. El mapa institucional también debe hacerlo.'}</h2><div class="pd-ar-status-grid"><article class="pd-ar-status-card"><strong>${isEn ? 'Fiscalía Anticorrupción' : 'Fiscalía Anticorrupción'}</strong><p>${isEn ? 'Receipt acknowledged. Admission remains pending. A signature/formality cure was requested before processing.' : 'Acuse de recibo. La admisión sigue pendiente. Se requirió subsanar firma/formalidad antes de tramitar.'}</p></article><article class="pd-ar-status-card"><strong>AEAT · 00001-00113069</strong><p>${isEn ? 'The 20 August notice states that the transparency-access procedure has entered processing at AEAT. No substantive access decision is yet established.' : 'La notificación de 20 de agosto comunica el comienzo de tramitación del acceso en AEAT. Aún no consta resolución sustantiva de acceso.'}</p></article><article class="pd-ar-status-card"><strong>CGPJ · DI 169/2026 / Alzada 286/2026</strong><p>${isEn ? 'Dedicated Recursos and Secretaría General routes are distinguished from a later general-information email that bounced with a 550 rejection. Attempted transmission is not counted as delivery.' : 'Se distinguen las vías a Recursos y Secretaría General de un envío posterior al buzón general de información rechazado con error 550. Intento de envío no equivale a entrega.'}</p></article><article class="pd-ar-status-card"><strong>${isEn ? 'Canary Government · transversal reconciliation' : 'Gobierno de Canarias · reconciliación transversal'}</strong><p>${isEn ? 'The 20 August preservation request asks which body reconciled RIC → RICPE/HNT financing → regional incentives → FEDER/EU funds, and on which primary records.' : 'La solicitud de preservación de 20 de agosto pregunta qué órgano reconcilió RIC → financiación RICPE/HNT → incentivos regionales → FEDER/fondos UE y sobre qué fuentes primarias.'}</p></article></div><p><a class="button" href="${recoveryHref}">${isEn ? 'See the statutory preservation and intervention powers' : 'Ver las potestades legales de preservación e intervención'}</a></p></div>`;
    const hero = main.querySelector('.hero');
    if (hero) hero.insertAdjacentElement('afterend', section); else main.insertAdjacentElement('afterbegin', section);
  };

  const injectUpdates = () => {
    if (!/(updates|actualizaciones)\/$/.test(path) || document.querySelector('[data-asset-recovery-update]')) return;
    const main = document.querySelector('main');
    if (!main) return;
    const wrap = document.createElement('section');
    wrap.className = 'section';
    wrap.dataset.assetRecoveryUpdate = '20260821';
    wrap.innerHTML = `<div class="shell"><article class="pd-ar-update"><p class="pd-ar-kicker" style="color:#8a651f">21 ${isEn ? 'AUGUST' : 'AGOSTO'} 2026 · ${isEn ? 'MATERIAL STRATEGY UPDATE' : 'ACTUALIZACIÓN ESTRATÉGICA MATERIAL'}</p><h2>${isEn ? 'From accountability to preservation: the asset-recovery architecture is now explicit.' : 'De la responsabilidad a la preservación: la arquitectura de recuperación de activos ya es explícita.'}</h2><p>${isEn ? 'The project now maps the Spanish mechanisms capable of preserving and administering value before final merits are decided: criminal judicial intervention, early seizure/attachment for confiscation, CNMV intervention/substitution for the regulated categories identified by statute, and ORGA asset recovery/management.' : 'El proyecto ya mapea los mecanismos españoles capaces de preservar y administrar valor antes de decidir definitivamente el fondo: intervención judicial penal, embargo/aprehensión tempranos para asegurar decomiso, intervención/sustitución CNMV para las categorías reguladas legalmente y recuperación/gestión de activos por ORGA.'}</p><p class="pd-ar-chain">${isEn ? 'asset/right → control → corporate layer → financing → works → operation → revenue → refinancing → distribution → present holder' : 'activo/derecho → control → capa societaria → financiación → obras → explotación → ingresos → refinanciación → distribución → titular actual'}</p><p><strong>${isEn ? 'Governing demand:' : 'Exigencia rectora:'}</strong> ${isEn ? 'identify what is preserved now, by which authority, under which power, against which asset or record, and from what date.' : 'identificar qué está preservado hoy, por qué autoridad, bajo qué potestad, respecto de qué activo o documento y desde qué fecha.'}</p><p><a href="${recoveryHref}">${isEn ? 'Open the full architecture →' : 'Abrir la arquitectura completa →'}</a></p></article></div>`;
    const hero = main.querySelector('.hero');
    if (hero) hero.insertAdjacentElement('afterend', wrap); else main.insertAdjacentElement('afterbegin', wrap);
  };

  const inject = () => { injectGateway(); injectInstitutional(); injectUpdates(); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', inject, {once:true}); else inject();
})();
