(() => {
  'use strict';

  const path = location.pathname.replace(/index\.html$/, '').replace(/\/+$/, '/');
  const routes = new Set([
    '/por-derecho/es/reclamacion-caixabank-valencia/',
    '/por-derecho/es/reclamacion-caixabank-valencia/ob-rem-ac-cam-28nov2018/',
    '/por-derecho/es/adjudicacion-2022-reconstruccion-documental/',
    '/por-derecho/es/acreedor-de-registro/responsabilidad/',
    '/por-derecho/es/administrador-concursal-puerta-credito-titulo/',
    '/por-derecho/en/caixabank-valencia-claim/',
    '/por-derecho/en/caixabank-valencia-claim/ob-rem-ac-cam-28nov2018/',
    '/por-derecho/en/2022-adjudication-documentary-reconstruction/',
    '/por-derecho/en/lender-of-record/liability/',
    '/por-derecho/en/insolvency-administrator-credit-to-title-gatekeeper/'
  ]);
  if (!routes.has(path)) return;

  const es = path.includes('/es/');
  const focus = path.includes('caixabank-valencia') && !path.includes('ob-rem') ? 'bank'
    : (path.includes('ob-rem') || path.includes('adjudicacion') || path.includes('adjudication')) ? 'asset'
    : 'bridge';

  const copy = es ? {
    kicker: 'VALENCIA ↔ CRÉDITO ↔ OB REM · MAPA DE DOS RAMAS',
    title: 'Una relación económica, dos ramas jurídicas que después vuelven a encontrarse',
    lead: 'Valencia examina la rama bancaria y de producto. OB REM examina qué ocurrió cuando la rama crédito/garantía llegó a CAM. No son la misma acción y ninguna invalida automáticamente a la otra.',
    origin: '2008–2010 · paquete de financiación LPB',
    originSub: 'Hipoteca 8,6 M€ · swap 5 M€ nocional · refinanciación · préstamo 850.000 € · prenda 405.000 € · cuentas',
    split: 'PUNTO DE SEPARACIÓN A RECONSTRUIR',
    splitSub: 'Qué derechos, saldos, garantías, defensas y responsabilidades siguieron cada rama.',
    leftEyebrow: 'RAMA A · RESPONSABILIDAD BANCARIA',
    left1: 'Caja / BFA / Bankia',
    left2: '→ CaixaBank',
    left3: 'Valencia · PO 1859/2023-9',
    left4: 'Pendiente: swap, refinanciación, prenda, cuentas, causalidad, restitución / daños.',
    rightEyebrow: 'RAMA B · CRÉDITO / GARANTÍA',
    right1: 'Bankia → SAREB → PH122 → CAM',
    right2: '28-NOV-2018 · OB REM + locales · 400.000 €',
    right3: '24-OCT-2019 · no convalidación',
    right4: '→ 2021 re-aprobación · → 2022 implementación de título',
    bridgeTitle: 'La reconciliación que une las dos ramas',
    q1: '¿Qué saldo exacto salió de Bankia?',
    q2: '¿Qué responsabilidades quedaron aguas arriba?',
    q3: '¿Qué garantías, defensas y pagos viajaron con el crédito?',
    q4: '¿Qué adquirió CAM, a qué precio y con qué due diligence?',
    rule: 'REGLA DE LECTURA',
    ruleText: 'La demanda de Valencia localizada no formula la operación OB REM como causa de acción y no se afirma que CaixaBank participara en la escritura de 2018. Un resultado en Valencia puede obligar a recalcular o reexaminar la rama posterior, pero no anula automáticamente SAREB→PH122→CAM, la operación OB REM o la adjudicación. Del mismo modo, la validez o invalidez de un acto OB REM no decide por sí sola el litigio de Valencia.',
    cta1: 'Valencia',
    cta2: 'OB REM',
    cta3: 'Adjudicación 2022',
    cta4: 'Cadena acreedora',
    cta5: 'AC · compuerta crédito→título'
  } : {
    kicker: 'VALENCIA ↔ CREDIT ↔ OB REM · TWO-BRANCH MAP',
    title: 'One economic relationship, two legal branches that later meet again',
    lead: 'Valencia tests the banking/product branch. OB REM tests what happened when the credit/security branch reached CAM. They are not the same cause of action and neither automatically invalidates the other.',
    origin: '2008–2010 · LPB financing package',
    originSub: '€8.6m mortgage · €5m notional swap · refinancing · €850k facility · €405k pledge · accounts',
    split: 'THE SPLIT THAT MUST BE RECONSTRUCTED',
    splitSub: 'Which rights, balances, securities, defences and liabilities followed each branch.',
    leftEyebrow: 'BRANCH A · BANKING LIABILITY',
    left1: 'Caja / BFA / Bankia',
    left2: '→ CaixaBank',
    left3: 'Valencia · PO 1859/2023-9',
    left4: 'Pending: swap, refinancing, pledge, accounts, causation, restitution / damages.',
    rightEyebrow: 'BRANCH B · CREDIT / SECURITY',
    right1: 'Bankia → SAREB → PH122 → CAM',
    right2: '28-NOV-2018 · OB REM + premises · €400,000',
    right3: '24-OCT-2019 · non-validation',
    right4: '→ 2021 re-approval · → 2022 title implementation',
    bridgeTitle: 'The reconciliation that joins both branches',
    q1: 'What exact balance left Bankia?',
    q2: 'Which liabilities stayed upstream?',
    q3: 'Which securities, defences and payments travelled with the credit?',
    q4: 'What did CAM acquire, at what price and with what due diligence?',
    rule: 'READING RULE',
    ruleText: 'The located Valencia pleading does not plead the OB REM transaction as a cause of action, and no claim is made here that CaixaBank participated in the 2018 deed. A Valencia outcome may require recalculation or consequential review downstream, but it does not automatically invalidate SAREB→PH122→CAM, the OB REM transaction or the adjudication. Equally, validity or invalidity of an OB REM act does not itself decide Valencia.',
    cta1: 'Valencia',
    cta2: 'OB REM',
    cta3: '2022 adjudication',
    cta4: 'Creditor chain',
    cta5: 'IA · credit→title gatekeeper'
  };

  const href = es ? {
    valencia: '/por-derecho/es/reclamacion-caixabank-valencia/',
    obrem: '/por-derecho/es/reclamacion-caixabank-valencia/ob-rem-ac-cam-28nov2018/',
    adjud: '/por-derecho/es/adjudicacion-2022-reconstruccion-documental/',
    lender: '/por-derecho/es/acreedor-de-registro/responsabilidad/',
    ac: '/por-derecho/es/administrador-concursal-puerta-credito-titulo/'
  } : {
    valencia: '/por-derecho/en/caixabank-valencia-claim/',
    obrem: '/por-derecho/en/caixabank-valencia-claim/ob-rem-ac-cam-28nov2018/',
    adjud: '/por-derecho/en/2022-adjudication-documentary-reconstruction/',
    lender: '/por-derecho/en/lender-of-record/liability/',
    ac: '/por-derecho/en/insolvency-administrator-credit-to-title-gatekeeper/'
  };

  const style = document.createElement('style');
  style.textContent = `
    .pd-split-visual{--ink:#13252d;--paper:#fff;--gold:#8c6b2f;--red:#8c2f2c;--line:#cbd4d3;max-width:1160px;margin:1.4rem auto 2rem;padding:0 1rem}
    .pd-split-shell{border:1px solid rgba(19,37,45,.16);border-radius:24px;background:linear-gradient(180deg,#fff 0%,#f7f8f6 100%);box-shadow:0 16px 42px rgba(19,37,45,.08);overflow:hidden}
    .pd-split-head{padding:1.35rem 1.4rem 1rem}.pd-split-kicker{font-size:.78rem;letter-spacing:.08em;font-weight:900;color:var(--red);margin:0 0 .4rem}.pd-split-head h2{font-size:clamp(1.45rem,3vw,2.35rem);line-height:1.07;margin:.1rem 0 .6rem;color:var(--ink)}.pd-split-head p{max-width:880px;margin:0;color:#4b5758}
    .pd-origin{margin:0 1.4rem 1rem;padding:1rem 1.15rem;background:var(--ink);color:#fff;border-radius:16px;text-align:center;position:relative}.pd-origin strong{display:block;font-size:1.05rem}.pd-origin span{display:block;margin-top:.25rem;opacity:.86;font-size:.92rem}
    .pd-origin:after{content:'';position:absolute;left:50%;bottom:-24px;width:2px;height:24px;background:var(--gold)}
    .pd-split-point{width:min(560px,calc(100% - 2.8rem));margin:24px auto 1.15rem;padding:.8rem 1rem;border:1px solid rgba(140,107,47,.35);background:#fffaf0;border-radius:999px;text-align:center;position:relative;box-shadow:0 0 0 0 rgba(140,107,47,.24);animation:pdSplitPulse 3.2s ease-in-out infinite}.pd-split-point strong{display:block;font-size:.82rem;letter-spacing:.055em;color:#654c1f}.pd-split-point span{font-size:.86rem;color:#5a5e5b}
    .pd-fork{position:relative;display:grid;grid-template-columns:1fr 1fr;gap:1.2rem;padding:1.1rem 1.4rem .7rem}.pd-fork:before{content:'';position:absolute;top:0;left:25%;right:25%;height:2px;background:linear-gradient(90deg,var(--gold),#aeb9b7,var(--red))}.pd-lane{background:#fff;border:1px solid rgba(19,37,45,.14);border-radius:18px;padding:1rem;position:relative;transition:transform .2s ease,box-shadow .2s ease}.pd-lane:before{content:'';position:absolute;top:-1.1rem;left:50%;width:2px;height:1.1rem;background:var(--line)}.pd-lane .eyebrow{font-size:.76rem;font-weight:900;letter-spacing:.06em;margin-bottom:.65rem}.pd-bank .eyebrow{color:#715a26}.pd-asset .eyebrow{color:var(--red)}.pd-step{border-left:3px solid #d5dcdb;padding:.45rem .65rem;margin:.38rem 0;background:#fbfbfa;border-radius:0 10px 10px 0}.pd-step strong{display:block;color:var(--ink)}.pd-step small{display:block;color:#596463;line-height:1.35}
    .pd-split-visual[data-focus="bank"] .pd-bank,.pd-split-visual[data-focus="asset"] .pd-asset,.pd-split-visual[data-focus="bridge"] .pd-reconcile{box-shadow:0 0 0 3px rgba(140,107,47,.15),0 12px 28px rgba(19,37,45,.09);transform:translateY(-2px)}
    .pd-reconcile{margin:.7rem 1.4rem 1rem;padding:1rem 1.1rem;background:#eef2f0;border-radius:16px;border:1px dashed #9da9a6}.pd-reconcile h3{margin:0 0 .7rem;color:var(--ink);font-size:1.05rem}.pd-qgrid{display:grid;grid-template-columns:1fr 1fr;gap:.55rem}.pd-q{background:#fff;border-radius:12px;padding:.7rem .8rem;border:1px solid rgba(19,37,45,.12);font-size:.9rem;font-weight:700}
    .pd-rule{margin:0 1.4rem 1rem;border-left:6px solid var(--red);background:#fff4f3;padding:.9rem 1rem;border-radius:0 14px 14px 0}.pd-rule strong{display:block;font-size:.76rem;letter-spacing:.06em;color:var(--red);margin-bottom:.25rem}.pd-rule p{margin:0;color:#473b3a;font-size:.92rem}
    .pd-links{display:flex;gap:.5rem;flex-wrap:wrap;padding:0 1.4rem 1.35rem}.pd-links a{display:inline-flex;align-items:center;text-decoration:none;font-weight:800;font-size:.86rem;padding:.55rem .75rem;border-radius:999px;border:1px solid var(--ink);color:var(--ink);background:#fff}.pd-links a:hover,.pd-links a:focus{background:var(--ink);color:#fff}
    @keyframes pdSplitPulse{0%,100%{box-shadow:0 0 0 0 rgba(140,107,47,.12)}50%{box-shadow:0 0 0 9px rgba(140,107,47,0)}}
    @media(max-width:760px){.pd-fork{grid-template-columns:1fr}.pd-fork:before{left:50%;right:auto;width:2px;height:100%;top:0}.pd-lane:before{display:none}.pd-qgrid{grid-template-columns:1fr}.pd-split-point{border-radius:16px}.pd-split-visual{padding:0 .65rem}.pd-origin,.pd-fork,.pd-reconcile,.pd-rule,.pd-links{margin-left:.75rem;margin-right:.75rem}.pd-fork{padding-left:.75rem;padding-right:.75rem}}
    @media(prefers-reduced-motion:reduce){.pd-split-point{animation:none}.pd-lane{transition:none}}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.className = 'pd-split-visual';
  section.dataset.focus = focus;
  section.id = 'valencia-obrem-two-branch-map';
  section.setAttribute('aria-label', copy.title);
  section.innerHTML = `
    <div class="pd-split-shell">
      <div class="pd-split-head">
        <p class="pd-split-kicker">${copy.kicker}</p>
        <h2>${copy.title}</h2>
        <p>${copy.lead}</p>
      </div>
      <div class="pd-origin"><strong>${copy.origin}</strong><span>${copy.originSub}</span></div>
      <div class="pd-split-point"><strong>${copy.split}</strong><span>${copy.splitSub}</span></div>
      <div class="pd-fork">
        <article class="pd-lane pd-bank">
          <div class="eyebrow">${copy.leftEyebrow}</div>
          <div class="pd-step"><strong>${copy.left1}</strong></div>
          <div class="pd-step"><strong>${copy.left2}</strong></div>
          <div class="pd-step"><strong>${copy.left3}</strong><small>${copy.left4}</small></div>
        </article>
        <article class="pd-lane pd-asset">
          <div class="eyebrow">${copy.rightEyebrow}</div>
          <div class="pd-step"><strong>${copy.right1}</strong></div>
          <div class="pd-step"><strong>${copy.right2}</strong></div>
          <div class="pd-step"><strong>${copy.right3}</strong><small>${copy.right4}</small></div>
        </article>
      </div>
      <div class="pd-reconcile">
        <h3>${copy.bridgeTitle}</h3>
        <div class="pd-qgrid"><div class="pd-q">${copy.q1}</div><div class="pd-q">${copy.q2}</div><div class="pd-q">${copy.q3}</div><div class="pd-q">${copy.q4}</div></div>
      </div>
      <div class="pd-rule"><strong>${copy.rule}</strong><p>${copy.ruleText}</p></div>
      <nav class="pd-links" aria-label="${copy.bridgeTitle}">
        <a href="${href.valencia}">${copy.cta1}</a><a href="${href.obrem}">${copy.cta2}</a><a href="${href.adjud}">${copy.cta3}</a><a href="${href.lender}">${copy.cta4}</a><a href="${href.ac}">${copy.cta5}</a>
      </nav>
    </div>
  `;

  const main = document.querySelector('main');
  if (!main) return;
  const hero = main.querySelector('.hero');
  if (hero) hero.insertAdjacentElement('afterend', section);
  else main.prepend(section);
})();