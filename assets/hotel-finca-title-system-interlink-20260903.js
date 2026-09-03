(() => {
  'use strict';
  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  if (path.includes('/fincas-hoteleras-clasificacion-lesion-titulo-sobre-titulo/') || path.includes('/hotel-fincas-asset-classification-title-on-title-injury/')) return;

  const lang = (document.documentElement.lang || (path.includes('/en/') ? 'en' : 'es')).toLowerCase().startsWith('en') ? 'en' : 'es';
  const exact = [
    '/es/matkator-8584-titulo-hotel-remate-restitucion/','/en/matkator-8584-hotel-title-remate-restitution/',
    '/es/registro-activos-derechos-matkator/','/en/matkator-asset-rights-register/',
    '/es/matkator-dp552-dp711-etj163-continuidad/','/en/matkator-dp552-dp711-etj163-continuity/',
    '/es/etj-163-2020/','/en/etj-163-2020/',
    '/es/dp-748-2026/','/en/dp-748-2026/',
    '/es/cambiario-1048-2019/','/en/cambiario-1048-2019/',
    '/es/cuatrecasas-sun-park/','/en/cuatrecasas-sun-park/',
    '/es/acosta-matos-perimetro/','/en/acosta-matos-perimeter/',
    '/es/adjudicacion-2022-reconstruccion-documental/','/en/2022-adjudication-documentary-reconstruction/',
    '/es/ingenieria-inversa-360-cadena-sun-park/','/en/reverse-engineering-360-sun-park-chain/'
  ];
  const fragments = [
    'concurso-36-2012','calificacion','rpl-2523','rpl-3304','rpl-3319','administrador-concursal',
    'ona-hotels','salida-financiada','funded-exit','toma-control','takeover','acosta-matos','hotel-new-trend',
    'canarian-hospitality','mynd','comunidad','acta','ricpe','ric-private-equity','feder','incentivos','incentives',
    'intervencion','aeat','onif','cnmv','fiscalia','eg-745','yaiza','cabildo','recuperacion','asset-recovery',
    'digest-penal','criminal-digest','ingenieria-forense','criminal-engineering'
  ];
  const isHome = /\/(?:por-derecho\/)?(?:es\/|en\/)?$/.test(path);
  const relevant = isHome || exact.some(p => path.includes(p)) || fragments.some(f => path.includes(f));
  if (!relevant) return;

  const routes = lang === 'en' ? {
    main:'/por-derecho/en/hotel-fincas-asset-classification-title-on-title-injury/',
    example:'/por-derecho/en/matkator-8584-hotel-title-remate-restitution/',
    assets:'/por-derecho/en/matkator-asset-rights-register/',
    dp:'/por-derecho/en/dp-748-2026/',
    c36:'/por-derecho/en/concurso-36-2012-liquidation-plan-judge-laj-audit/',
    acosta:'/por-derecho/en/acosta-matos-perimeter/'
  } : {
    main:'/por-derecho/es/fincas-hoteleras-clasificacion-lesion-titulo-sobre-titulo/',
    example:'/por-derecho/es/matkator-8584-titulo-hotel-remate-restitucion/',
    assets:'/por-derecho/es/registro-activos-derechos-matkator/',
    dp:'/por-derecho/es/dp-748-2026/',
    c36:'/por-derecho/es/concurso-36-2012-auditoria-plan-liquidacion-juez-laj/',
    acosta:'/por-derecho/es/acosta-matos-perimetro/'
  };

  const text = lang === 'en' ? {
    ey:'SCOPE CORRECTION · ALL HOTEL TITLES · TITLE-ON-TITLE INJURY',
    title:'Finca 8584 is the worked ETJ example, not the limit of the asset class.',
    lead:'The currently source-locked Matkator set comprises fincas 8584 and 8588. The same ownership, physical-space, consent, operator, revenue, procedural, beneficiary and remedy test applies to every later-identified Matkator title and title-by-title across Sun Park/MYND Yaiza.',
    a:'Asset class', b:'Claimant position', c:'Cross-proceeding effect',
    av:'A registered private title, inseparable common rights, a regulated hotel-operation node and an evidential/restitution platform — not merely an autonomous apartment or current room number.',
    bv:'The claimant alleges a completed procedural fraud in the Cuatrecasas/Matkator La Laguna proceedings. That is a party position, not an adjudicated finding.',
    cv:'La Laguna and Concurso 36/2012 remain separate. The alleged chain from title disposition to impaired restitution, hotel-control benefit and insolvency/recovery consequences must be proved arrow by arrow.',
    boundary:'Valid consensual acquisitions, disputed consent, alleged non-consensual integration, judicial dispositions and unresolved titles must be classified separately. No universal illegality or concert is stated as proved.',
    open:'Open class control', ex:'8584 example', ar:'Matkator register', dp:'DP 748', c36:'Concurso 36/2012', ac:'Acosta Matos'
  } : {
    ey:'CORRECCIÓN DE ALCANCE · TODAS LAS FINCAS HOTELERAS · LESIÓN TÍTULO-SOBRE-TÍTULO',
    title:'Finca 8584 es el ejemplo ETJ trabajado, no el límite de la clase de activo.',
    lead:'El conjunto Matkator actualmente bloqueado por fuentes comprende fincas 8584 y 8588. El mismo examen de titularidad, espacio físico, consentimiento, operador, ingresos, procedimiento, beneficiario y remedio se aplica a todo título Matkator que se identifique y, título por título, a Sun Park/MYND Yaiza.',
    a:'Clase de activo', b:'Posición de la parte', c:'Efecto interprocedimental',
    av:'Título privativo, derechos comunes inseparables, nodo de explotación hotelera regulada y plataforma probatoria/restitutoria; no sólo apartamento autónomo o habitación actual.',
    bv:'La parte alega una estafa procesal consumada en los procedimientos Cuatrecasas/Matkator de La Laguna. Es posición de parte, no declaración judicial.',
    cv:'La Laguna y Concurso 36/2012 permanecen separados. La cadena alegada desde disposición del título a menor restitución, beneficio de control y consecuencias concursales debe probarse flecha por flecha.',
    boundary:'Adquisición consensual válida, consentimiento discutido, integración no consentida alegada, disposición judicial y título no resuelto deben clasificarse separadamente. No se afirma ilicitud universal ni concierto probado.',
    open:'Abrir control de clase', ex:'Ejemplo 8584', ar:'Registro Matkator', dp:'DP 748', c36:'Concurso 36/2012', ac:'Acosta Matos'
  };

  const addStyle = () => {
    if (document.getElementById('pd-hotel-finca-system-style')) return;
    const s = document.createElement('style');
    s.id = 'pd-hotel-finca-system-style';
    s.textContent = `
      .pd-hfs-panel{background:linear-gradient(135deg,#0f252c,#174148 68%,#79591c);color:#fff;padding:2.2rem 0;position:relative;z-index:1}
      .pd-hfs-panel h2{color:#fff;max-width:1030px;margin:.25rem 0 .7rem}.pd-hfs-panel p{color:#e9f0ef;max-width:1100px;line-height:1.62}
      .pd-hfs-ey{font-size:.73rem;font-weight:850;letter-spacing:.06em;text-transform:uppercase;color:#f1d477}
      .pd-hfs-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.72rem;margin:1rem 0}
      .pd-hfs-card{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.25);border-radius:14px;padding:.9rem}
      .pd-hfs-card strong{display:block;color:#f1d477;margin-bottom:.28rem}.pd-hfs-boundary{border-left:4px solid #f1d477;padding-left:.85rem;font-size:.9rem}
      .pd-hfs-links{display:flex;gap:.52rem;flex-wrap:wrap;margin-top:1rem}.pd-hfs-links a{display:inline-block;background:#f1d477;color:#10262d;text-decoration:none;border-radius:999px;padding:.52rem .78rem;font-weight:850}
      .pd-hfs-home{max-width:1180px;margin:1.25rem auto;border-radius:22px;overflow:hidden;box-shadow:0 18px 44px rgba(16,38,45,.22)}
      @media(max-width:780px){.pd-hfs-grid{grid-template-columns:1fr}.pd-hfs-panel{padding:1.6rem 0}}
    `;
    document.head.appendChild(s);
  };

  const render = () => {
    if (document.querySelector('[data-hotel-finca-system-control]')) return;
    addStyle();
    const section = document.createElement('section');
    section.className = 'pd-hfs-panel' + (isHome ? ' pd-hfs-home' : '');
    section.setAttribute('data-hotel-finca-system-control','20260903');
    section.innerHTML = `<div class="shell"><p class="pd-hfs-ey">${text.ey}</p><h2>${text.title}</h2><p>${text.lead}</p><div class="pd-hfs-grid"><article class="pd-hfs-card"><strong>${text.a}</strong><span>${text.av}</span></article><article class="pd-hfs-card"><strong>${text.b}</strong><span>${text.bv}</span></article><article class="pd-hfs-card"><strong>${text.c}</strong><span>${text.cv}</span></article></div><p class="pd-hfs-boundary">${text.boundary}</p><div class="pd-hfs-links"><a href="${routes.main}">${text.open}</a><a href="${routes.example}">${text.ex}</a><a href="${routes.assets}">${text.ar}</a><a href="${routes.dp}">${text.dp}</a><a href="${routes.c36}">${text.c36}</a><a href="${routes.acosta}">${text.ac}</a></div></div>`;
    const main = document.querySelector('main');
    if (isHome && main) {
      const first = main.querySelector('section');
      if (first && first.nextSibling) main.insertBefore(section, first.nextSibling); else main.prepend(section);
    } else {
      const first = main && main.querySelector('section');
      if (first && first.nextSibling && (path.includes('matkator') || path.includes('dp-748') || path.includes('etj-163') || path.includes('cuatrecasas'))) main.insertBefore(section, first.nextSibling);
      else {
        const footer = document.querySelector('footer');
        if (footer && footer.parentNode) footer.parentNode.insertBefore(section, footer); else document.body.appendChild(section);
      }
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', render, {once:true}); else render();
})();
