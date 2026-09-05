(() => {
  'use strict';

  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  const isEN = document.documentElement.lang?.toLowerCase().startsWith('en') || path.includes('/en/');
  const isHome = /^\/(?:por-derecho\/)?(?:es\/|en\/)?$/.test(path);
  if (!isHome || document.querySelector('[data-pd-home-mission="20260904"]')) return;

  const root = '/por-derecho/' + (isEN ? 'en/' : 'es/');
  const routes = {
    dp1901: root + 'dp-1901-2026/',
    dp1956: root + 'dp-1956-2026/',
    c22: root + (isEN ? 'control-22-insolvency-administrator-complaint/' : 'control-22-denuncia-administrador-concursal/'),
    c24: root + (isEN ? 'control-24-insolvency-judge-complaint-36-2012/' : 'control-24-denuncia-juez-concurso-36-2012/'),
    judge: root + (isEN ? 'insolvency-36-2012-mercantile-court-1/' : 'concurso-36-2012-magistrado-juez/'),
    ac: root + (isEN ? 'insolvency-36-2012-insolvency-administrator/' : 'concurso-36-2012-administrador-concursal/'),
    fees: root + (isEN ? 'insolvency-36-2012-administrator-removal-fees/' : 'concurso-36-2012-separacion-ac-honorarios/'),
    fiscal: root + 'fiscalia-dip-2-2026/',
    authority: root + (isEN ? 'public-authority-unitary-case-reconstruction/' : 'reconstruccion-unitaria-autoridades-publicas/'),
    updates: root + (isEN ? 'updates/' : 'actualizaciones/'),
    data: '/por-derecho/data/three-track-full-digitisation-20260904.json'
  };

  const t = isEN ? {
    mission: 'MISSION-CRITICAL HOMEPAGE · SOURCE-CONTROLLED · BILINGUAL',
    h1: 'One asset. Multiple legal lives. One evidence-led public record.',
    intro: 'Project Sun Rock is the command surface for a recovery record centred on Sun Park / MYND Yaiza. The homepage must let a first-time reader understand the asset, the three principal accountability lanes, the shared chronology, the institutional handling and the recovery/future paths without collapsing legally distinct proceedings.',
    rules: [
      ['ONE ASSET', 'Sun Park / MYND Yaiza is the physical centre; ownership, insolvency estate, operation, Community authority and third-party rights remain legally distinct.'],
      ['THREE CORE LANES', 'DP 1901/2026 · DP 1956/2026 · Control 24 are interconnected by evidence and chronology, not merged by responsibility.'],
      ['ONE METHOD', 'Documented fact, attributed allegation, inference, adverse material, procedural status and open proof remain visibly separated.']
    ],
    rail: ['60 seconds','Case map','DP 1901','DP 1956','Control 24','Evidence','Institutions','Future'],
    railHrefs: ['#sixty-second-summary','#pd-home-case-map',routes.dp1901,routes.dp1956,routes.c24,'#record','#institutional-map','#future'],
    caseEy: 'CASE MAP · HOW THE SAME FACTS MOVE THROUGH DIFFERENT LEGAL LANES',
    caseTitle: 'Shared storyline. Separate attribution.',
    caseIntro: 'Read horizontally through time, then vertically through the legal lane. The same event can be relevant to different actors for different reasons; the bridge must be proved separately each time.',
    lanes: [
      ['PRIVATE ACTORS','DP 1901/2026 · Control 21','Who created, used, transmitted or monetised apparent authority, access, project value or downstream benefit?',routes.dp1901],
      ['INSOLVENCY ADMINISTRATOR','DP 1956/2026 · Control 22','What did the administrator know, verify, protect, report, implement, account for or leave uncorrected within his own duties?',routes.dp1956],
      ['JUDICIAL LAYER','Control 24','What reached the court, which resolutions followed, and what documentary bridge explains their effects?',routes.c24]
    ],
    timelineTitle: 'Shared factual spine',
    timeline: [
      ['2011–2016','Community authority · debt/vote · operation · notice'],
      ['2017–Jun 2018','CAM/credit entry · access/measurements · security · funded exit'],
      ['7 Jun 2018','Alleged material change of access/control'],
      ['2018–2019','OB REM · €400k · non-validation'],
      ['2020–2022','Credit/threshold · estate · bidding · adjudication'],
      ['2022–2026','HNT/MYND · RIC/RICPE · operation · authorities']
    ],
    networkTitle: 'Action-to-action network',
    networkIntro: 'The core tracks are connected to the people, institutional and recovery surfaces that explain capacity, handling and consequence.',
    network: [
      ['Insolvency Administrator','Actor/capacity page',routes.ac],
      ['Judge','Judicial role and decision page',routes.judge],
      ['Control 22 complaint','18 Jun complaint / AC layer',routes.c22],
      ['Removal & fees','Separate insolvency accountability lane',routes.fees],
      ['Fiscalía / DIP 2/2026','Prosecutorial handling',routes.fiscal],
      ['Institutional clean room','Public-authority reconstruction',routes.authority],
      ['Full digitisation','Structured source/status control',routes.data],
      ['Updates','Current changes and corrections',routes.updates]
    ],
    boundary: 'INTERLINKED ≠ MERGED · SHARED EVIDENCE ≠ SHARED LIABILITY · FILING ≠ ADMISSION · LATER TITLE / OPERATION / FINANCING ≠ VALIDATION OF PREDECESSOR AUTHORITY',
    route: 'Open',
    viewData: 'Open structured control',
    heroBadge: 'Evidence-first · multitrack · source/status separated',
    heroCaseMap: 'Open the case map'
  } : {
    mission: 'PORTADA MISSION-CRITICAL · FUENTE CONTROLADA · BILINGÜE',
    h1: 'Un activo. Varias vidas jurídicas. Un solo expediente público basado en prueba.',
    intro: 'Project Sun Rock es la superficie de mando del expediente de recuperación centrado en Sun Park / MYND Yaiza. La portada debe permitir que un lector nuevo entienda el activo, las tres vías principales de responsabilidad, la cronología compartida, el tratamiento institucional y las rutas de recuperación/futuro sin fundir procedimientos jurídicamente distintos.',
    rules: [
      ['UN ACTIVO', 'Sun Park / MYND Yaiza es el centro físico; propiedad, masa concursal, explotación, autoridad comunitaria y derechos de terceros siguen siendo planos jurídicos distintos.'],
      ['TRES VÍAS NÚCLEO', 'DP 1901/2026 · DP 1956/2026 · Control 24 están interconectadas por prueba y cronología, no fusionadas por responsabilidad.'],
      ['UN MÉTODO', 'Hecho documentado, alegación atribuida, inferencia, material adverso, estado procesal y prueba abierta permanecen visiblemente separados.']
    ],
    rail: ['60 segundos','Mapa del caso','DP 1901','DP 1956','Control 24','Prueba','Instituciones','Futuro'],
    railHrefs: ['#resumen-60-segundos','#pd-home-case-map',routes.dp1901,routes.dp1956,routes.c24,'#registro','#mapa-institucional','#futuro'],
    caseEy: 'MAPA DEL CASO · CÓMO LOS MISMOS HECHOS SE LEEN EN VÍAS JURÍDICAS DISTINTAS',
    caseTitle: 'Storyline compartido. Atribución separada.',
    caseIntro: 'Lea horizontalmente a través del tiempo y luego verticalmente por carril jurídico. Un mismo hecho puede ser relevante para actores distintos por razones distintas; el puente debe probarse separadamente cada vez.',
    lanes: [
      ['ACTORES PRIVADOS','DP 1901/2026 · Control 21','¿Quién creó, usó, transmitió o monetizó autoridad aparente, acceso, valor de proyecto o beneficio posterior?',routes.dp1901],
      ['ADMINISTRADOR CONCURSAL','DP 1956/2026 · Control 22','¿Qué conoció, verificó, protegió, comunicó, implementó, contabilizó o dejó sin corregir el Administrador dentro de sus propios deberes?',routes.dp1956],
      ['CAPA JUDICIAL','Control 24','¿Qué llegó al órgano judicial, qué resoluciones siguieron y qué puente documental explica sus efectos?',routes.c24]
    ],
    timelineTitle: 'Columna factual compartida',
    timeline: [
      ['2011–2016','Autoridad comunitaria · deuda/voto · explotación · avisos'],
      ['2017–jun 2018','Entrada CAM/crédito · accesos/mediciones · seguridad · salida financiada'],
      ['7 jun 2018','Cambio material alegado de acceso/control'],
      ['2018–2019','OB REM · €400k · no convalidación'],
      ['2020–2022','Crédito/umbral · masa · licitación · adjudicación'],
      ['2022–2026','HNT/MYND · RIC/RICPE · explotación · autoridades']
    ],
    networkTitle: 'Red acción→acción',
    networkIntro: 'Las vías núcleo se conectan con las superficies de personas, instituciones y recuperación que explican capacidad, tratamiento y consecuencia.',
    network: [
      ['Administrador Concursal','Página de actor/capacidad',routes.ac],
      ['Juez','Rol judicial y resoluciones',routes.judge],
      ['Denuncia Control 22','Denuncia 18 jun / capa AC',routes.c22],
      ['Separación y honorarios','Vía concursal separada de responsabilidad',routes.fees],
      ['Fiscalía / DIP 2/2026','Tratamiento fiscal',routes.fiscal],
      ['Sala institucional neutral','Reconstrucción de autoridades públicas',routes.authority],
      ['Digitalización íntegra','Control estructurado de fuentes/estado',routes.data],
      ['Actualizaciones','Cambios y correcciones actuales',routes.updates]
    ],
    boundary: 'INTERCONECTADO ≠ FUNDIDO · PRUEBA COMPARTIDA ≠ RESPONSABILIDAD COMPARTIDA · PRESENTACIÓN ≠ ADMISIÓN · TÍTULO / EXPLOTACIÓN / FINANCIACIÓN POSTERIORES ≠ VALIDACIÓN DE AUTORIDAD PRECEDENTE',
    route: 'Abrir',
    viewData: 'Abrir control estructurado',
    heroBadge: 'Evidence-first · multitrack · fuente/estado separados',
    heroCaseMap: 'Abrir mapa del caso'
  };

  const style = document.createElement('style');
  style.id = 'pd-home-mission-style';
  style.textContent = `
    body.pd-home-mission{background:#f7f4ee}
    body.pd-home-mission .site-header{backdrop-filter:saturate(1.1) blur(10px)}
    body.pd-home-mission main>.hero{position:relative;overflow:hidden;background:linear-gradient(135deg,#0d2029 0%,#193845 47%,#5d4621 100%);padding:clamp(3.6rem,7vw,6.5rem) 0;color:#fff}
    body.pd-home-mission main>.hero:before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 15% 15%,rgba(255,255,255,.12),transparent 34%),radial-gradient(circle at 85% 85%,rgba(213,170,78,.16),transparent 32%);pointer-events:none}
    body.pd-home-mission main>.hero .shell{position:relative;z-index:1}
    body.pd-home-mission main>.hero h1,body.pd-home-mission main>.hero p,body.pd-home-mission main>.hero .eyebrow{color:#fff}
    body.pd-home-mission main>.hero h1{font-size:clamp(2.9rem,6.5vw,5.8rem);line-height:.94;letter-spacing:-.045em;max-width:11.5ch}
    body.pd-home-mission main>.hero .lead{font-size:clamp(1.08rem,1.8vw,1.3rem);max-width:64rem;opacity:.94}
    body.pd-home-mission main>.hero .hero-photo{border-radius:24px;overflow:hidden;background:#07161c;box-shadow:0 25px 60px rgba(0,0,0,.28);border:1px solid rgba(255,255,255,.18)}
    body.pd-home-mission main>.hero .hero-photo img{display:block;width:100%;height:auto;filter:saturate(.9) contrast(1.03)}
    body.pd-home-mission main>.hero .hero-photo figcaption{background:rgba(6,21,27,.88);color:#f5f1e8;padding:.8rem 1rem}
    .pd-home-hero-badge{display:inline-flex;align-items:center;gap:.45rem;margin:.85rem 0 0;padding:.48rem .72rem;border:1px solid rgba(255,255,255,.22);background:rgba(255,255,255,.1);border-radius:999px;color:#fff;font-weight:850;font-size:.78rem;letter-spacing:.03em}
    .pd-home-hero-map{margin-top:.8rem!important}
    .pd-home-hero-map a{display:inline-flex!important}
    .pd-home-rail{position:sticky;top:0;z-index:38;background:rgba(247,244,238,.95);backdrop-filter:blur(12px);border-bottom:1px solid rgba(19,37,45,.14);box-shadow:0 8px 24px rgba(19,37,45,.06)}
    .pd-home-rail-inner{max-width:1180px;margin:auto;padding:.55rem 1rem;display:flex;gap:.45rem;overflow-x:auto;scrollbar-width:thin}
    .pd-home-rail a{white-space:nowrap;text-decoration:none;color:#13252d;background:#fff;border:1px solid rgba(19,37,45,.12);border-radius:999px;padding:.48rem .7rem;font-size:.78rem;font-weight:850}
    .pd-home-rail a:nth-child(2),.pd-home-rail a:nth-child(3),.pd-home-rail a:nth-child(4),.pd-home-rail a:nth-child(5){border-color:#b9872f;background:#fff8e9}
    .pd-home-mission-section{padding:clamp(2rem,5vw,4rem) 0;background:#f7f4ee}
    .pd-home-mission-shell{max-width:1180px;margin:auto;padding:0 1rem}
    .pd-home-mission-card{border-radius:28px;overflow:hidden;background:#fff;box-shadow:0 22px 55px rgba(19,37,45,.11);border:1px solid rgba(19,37,45,.11)}
    .pd-home-mission-head{padding:clamp(1.4rem,4vw,2.6rem);background:linear-gradient(135deg,#13252d,#2c4d58 58%,#72551c);color:#fff}
    .pd-home-mission-head *{color:#fff}
    .pd-home-mission-ey{font-size:.72rem;font-weight:900;letter-spacing:.095em;text-transform:uppercase;color:#f4d98c!important}
    .pd-home-mission-head h2{font-size:clamp(2rem,4.2vw,3.6rem);line-height:1;letter-spacing:-.035em;max-width:17ch;margin:.45rem 0 .8rem}
    .pd-home-mission-head p{max-width:76rem;font-size:1.02rem;line-height:1.65;opacity:.96}
    .pd-home-rule-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.8rem;padding:1rem;background:#eef2f1}
    .pd-home-rule{background:#fff;border-radius:18px;padding:1rem;border-top:4px solid #b9872f}
    .pd-home-rule strong{display:block;color:#7d342f;font-size:.75rem;letter-spacing:.08em;margin-bottom:.35rem}
    .pd-home-rule span{color:#293a40;line-height:1.48;font-size:.9rem}
    .pd-home-case{padding:1.2rem}
    .pd-home-case-header{max-width:820px;margin-bottom:1rem}
    .pd-home-case-header .ey{font-size:.72rem;font-weight:900;letter-spacing:.08em;color:#8a3a32;text-transform:uppercase}
    .pd-home-case-header h3{font-size:clamp(1.7rem,3.5vw,2.6rem);margin:.25rem 0 .45rem;color:#13252d}
    .pd-home-case-header p{color:#45575d;line-height:1.62}
    .pd-home-lanes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.85rem}
    .pd-home-lane{position:relative;background:linear-gradient(180deg,#fff,#f8faf9);border:1px solid rgba(19,37,45,.14);border-radius:20px;padding:1.1rem;min-height:235px;display:flex;flex-direction:column;box-shadow:0 10px 24px rgba(19,37,45,.06)}
    .pd-home-lane:before{content:"";position:absolute;left:0;top:0;bottom:0;width:5px;border-radius:20px 0 0 20px;background:#b9872f}
    .pd-home-lane:nth-child(2):before{background:#3d6c73}.pd-home-lane:nth-child(3):before{background:#7c3942}
    .pd-home-lane .tag{font-size:.69rem;font-weight:900;letter-spacing:.09em;color:#8a3a32;text-transform:uppercase}
    .pd-home-lane h4{font-size:1.25rem;margin:.35rem 0;color:#13252d}.pd-home-lane p{color:#3f5157;line-height:1.52;font-size:.91rem}
    .pd-home-lane a{margin-top:auto;align-self:flex-start;text-decoration:none;background:#13252d;color:#fff;border-radius:999px;padding:.48rem .72rem;font-size:.78rem;font-weight:850}
    .pd-home-timeline-wrap{margin-top:1.1rem;padding:1rem;border-radius:20px;background:#13252d;color:#fff}
    .pd-home-timeline-wrap h4{color:#fff;margin:.15rem 0 .75rem;font-size:1.1rem}
    .pd-home-timeline{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:.45rem;position:relative}
    .pd-home-time{position:relative;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.13);border-radius:14px;padding:.8rem;min-height:114px}
    .pd-home-time strong{display:block;color:#f1d78d;font-size:.76rem;margin-bottom:.3rem}.pd-home-time span{color:#f3f5f5;font-size:.8rem;line-height:1.38}
    .pd-home-network{padding:1.2rem;border-top:1px solid rgba(19,37,45,.1);background:#fbfaf7}
    .pd-home-network-head{display:flex;justify-content:space-between;gap:1rem;align-items:end;flex-wrap:wrap;margin-bottom:.85rem}
    .pd-home-network-head h3{margin:0;color:#13252d;font-size:1.55rem}.pd-home-network-head p{margin:.25rem 0 0;max-width:720px;color:#52646a}
    .pd-home-network-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.7rem}
    .pd-home-node{display:block;text-decoration:none;background:#fff;border:1px solid rgba(19,37,45,.12);border-radius:16px;padding:.9rem;color:#13252d;min-height:110px;transition:transform .18s ease,box-shadow .18s ease,border-color .18s ease}
    .pd-home-node:hover{transform:translateY(-2px);box-shadow:0 10px 22px rgba(19,37,45,.08);border-color:#b9872f}
    .pd-home-node strong{display:block;color:#13252d}.pd-home-node span{display:block;color:#63747a;font-size:.82rem;margin-top:.3rem;line-height:1.4}
    .pd-home-boundary{padding:.9rem 1.2rem;background:#fff5db;border-top:1px solid #ead19a;color:#654711;font-size:.78rem;font-weight:900;letter-spacing:.045em;text-align:center}
    body.pd-home-mission main>section:not(.hero):not(.pd-home-mission-section){scroll-margin-top:74px}
    body.pd-home-mission #resumen-60-segundos,body.pd-home-mission #sixty-second-summary{position:relative}
    @media(max-width:980px){.pd-home-rule-grid,.pd-home-lanes{grid-template-columns:1fr}.pd-home-network-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.pd-home-timeline{grid-template-columns:repeat(3,minmax(0,1fr))}}
    @media(max-width:640px){body.pd-home-mission main>.hero h1{font-size:clamp(2.6rem,14vw,4rem)}.pd-home-network-grid,.pd-home-timeline{grid-template-columns:1fr}.pd-home-rail{top:0}.pd-home-mission-section{padding:1.2rem 0}.pd-home-mission-card{border-radius:20px}.pd-home-mission-head{padding:1.25rem}.pd-home-case,.pd-home-network{padding:.9rem}}
  `;
  document.head.appendChild(style);
  document.body.classList.add('pd-home-mission');

  const header = document.querySelector('.site-header');
  const main = document.querySelector('main');
  const hero = main?.querySelector(':scope > .hero');
  if (!main || !hero) return;

  const rail = document.createElement('nav');
  rail.className = 'pd-home-rail';
  rail.dataset.pdHomeMission = '20260904';
  rail.setAttribute('aria-label', isEN ? 'Mission-critical homepage routes' : 'Rutas mission-critical de portada');
  rail.innerHTML = `<div class="pd-home-rail-inner">${t.rail.map((label,i)=>`<a href="${t.railHrefs[i]}">${label}</a>`).join('')}</div>`;
  header?.after(rail);

  const heroCopy = hero.querySelector('.hero-grid > div');
  if (heroCopy) {
    const badge = document.createElement('div');
    badge.className = 'pd-home-hero-badge';
    badge.textContent = t.heroBadge;
    const actions = heroCopy.querySelector('.actions');
    actions ? actions.before(badge) : heroCopy.appendChild(badge);
    if (actions && !actions.querySelector('[data-pd-home-map-link]')) {
      const a = document.createElement('a');
      a.className = 'button secondary pd-home-hero-map';
      a.href = '#pd-home-case-map';
      a.dataset.pdHomeMapLink = '20260904';
      a.textContent = t.heroCaseMap;
      actions.appendChild(a);
    }
  }

  const section = document.createElement('section');
  section.className = 'pd-home-mission-section';
  section.id = 'pd-home-case-map';
  section.dataset.pdHomeMission = '20260904';
  section.innerHTML = `
    <div class="pd-home-mission-shell">
      <div class="pd-home-mission-card">
        <header class="pd-home-mission-head">
          <div class="pd-home-mission-ey">${t.mission}</div>
          <h2>${t.h1}</h2>
          <p>${t.intro}</p>
        </header>
        <div class="pd-home-rule-grid">
          ${t.rules.map(r=>`<div class="pd-home-rule"><strong>${r[0]}</strong><span>${r[1]}</span></div>`).join('')}
        </div>
        <div class="pd-home-case">
          <div class="pd-home-case-header"><div class="ey">${t.caseEy}</div><h3>${t.caseTitle}</h3><p>${t.caseIntro}</p></div>
          <div class="pd-home-lanes">
            ${t.lanes.map(l=>`<article class="pd-home-lane"><div class="tag">${l[0]}</div><h4>${l[1]}</h4><p>${l[2]}</p><a href="${l[3]}">${t.route} →</a></article>`).join('')}
          </div>
          <div class="pd-home-timeline-wrap">
            <h4>${t.timelineTitle}</h4>
            <div class="pd-home-timeline">${t.timeline.map(e=>`<div class="pd-home-time"><strong>${e[0]}</strong><span>${e[1]}</span></div>`).join('')}</div>
          </div>
        </div>
        <div class="pd-home-network">
          <div class="pd-home-network-head"><div><h3>${t.networkTitle}</h3><p>${t.networkIntro}</p></div><a class="button secondary" href="${routes.data}">${t.viewData}</a></div>
          <div class="pd-home-network-grid">${t.network.map(n=>`<a class="pd-home-node" href="${n[2]}"><strong>${n[0]}</strong><span>${n[1]}</span></a>`).join('')}</div>
        </div>
        <div class="pd-home-boundary">${t.boundary}</div>
      </div>
    </div>`;
  hero.after(section);
})();
