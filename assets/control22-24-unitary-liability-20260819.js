(() => {
  const path = location.pathname.replace(/\/+$/, '/') || '/';
  const es = path.includes('/es/');
  const targets = [
    '/es/concurso-36-2012-administrador-concursal/',
    '/en/insolvency-36-2012-insolvency-administrator/',
    '/es/concurso-36-2012-magistrado-juez/',
    '/en/insolvency-36-2012-mercantile-court-1/',
    '/es/acosta-matos-perimetro/',
    '/en/acosta-matos-perimeter/',
    '/es/concurso-36-2012-responsabilidad-institucional/',
    '/en/insolvency-36-2012-institutional-accountability/',
    '/es/dp-1956-2026/',
    '/en/dp-1956-2026/'
  ];
  if (!targets.some((p) => path.endsWith(p)) || document.getElementById('control22-24-unitary-20260819')) return;

  const isAC = path.includes('administrador-concursal') || path.includes('insolvency-administrator');
  const isJudge = path.includes('magistrado-juez') || path.includes('mercantile-court-1');
  const isCAM = path.includes('acosta-matos-perimet');
  const is1956 = path.includes('dp-1956-2026');

  const detail = es
    ? '/por-derecho/es/control-22-24-ac-juez-acosta-matos-digesto-unitario/'
    : '/por-derecho/en/control-22-24-ia-judge-acosta-matos-unitary-digest/';
  const retracto = es
    ? '/por-derecho/es/retracto-credito-litigioso-1041-2017/'
    : '/por-derecho/en/litigious-credit-retracto-1041-2017/';

  let title;
  let body;
  if (isAC) {
    title = es ? 'Control 22 re-leído desde 2016: máxima hipótesis sobre la Administración Concursal' : 'Control 22 re-read from 2016: maximum hypothesis concerning the insolvency administration';
    body = es
      ? 'La reconstrucción ya no empieza con el 7 de junio de 2018. Añade el crédito/retracto 2017–18: informe favorable de la AC → reconocimiento de CAM → pérdida posterior de valor de la vía informativa de LPB, sin beneficio equivalente para la masa actualmente identificado. La hipótesis máxima es posible administración desleal sistémica con efecto repetidamente favorable a CAM, sujeta a prueba de poder, conocimiento, daño, causalidad y elemento subjetivo.'
      : 'The reconstruction no longer starts with 7 June 2018. It adds the 2017–18 credit/retracto module: favourable IA report → CAM recognition → later loss of value in LPB’s information route, with no equivalent estate benefit currently identified. The maximum hypothesis is possible systemic disloyal administration with repeatedly CAM-favourable effect, subject to proof of power, knowledge, harm, causation and the required subjective element.';
  } else if (isJudge) {
    title = es ? 'Control 24: intervención activa, deferencia y no-neutralización bajo una sola prueba' : 'Control 24: active intervention, deference and non-neutralisation under one test';
    body = es
      ? 'El nuevo módulo 2017–18 muestra una asimetría anterior: para que LPB comprobara sus derechos se ordenó exhibición; para reconocer a CAM el Mercantil descansó expresamente en la verificación favorable de la AC. Debe leerse junto a suspensión, no convalidación, restauración, competencia y adjudicación. Esto sostiene una fuerte pregunta de supervisión selectiva y efecto CAM-favorable; no prueba por sí solo prevaricación ni parcialidad criminal.'
      : 'The new 2017–18 module shows an earlier asymmetry: production was ordered so LPB could test its rights; for CAM recognition the Commercial Court expressly relied on favourable IA verification. It must be read with suspension, non-convalidation, restoration, competition and award. This supports a strong selective-supervision/CAM-favourable-effect question; it does not by itself prove prevarication or criminal bias.';
  } else if (isCAM) {
    title = es ? 'Acosta Matos: de acreedor reconocido a beneficiario recurrente de una cadena más larga' : 'Acosta Matos: from recognised creditor to recurring beneficiary of a longer chain';
    body = es
      ? 'La nueva lectura conecta crédito/retracto, control material, no neutralización, competencia y adjudicación. CAM aparece repetidamente como beneficiario de posiciones que se consolidan mientras LPB pierde opciones o protección. Esa continuidad justifica investigar conocimiento, petición, inducción, cooperación o acuerdo; beneficiarse no demuestra por sí solo participación penal.'
      : 'The new reading connects credit/retracto, material control, non-neutralisation, competition and award. CAM repeatedly appears as beneficiary of positions that consolidate while LPB loses options or protection. That continuity justifies investigation of knowledge, request, inducement, cooperation or agreement; benefit alone does not prove criminal participation.';
  } else if (is1956) {
    title = es ? 'Control 22: el sobreseimiento provisional no cierra el análisis unitario' : 'Control 22: provisional dismissal does not close the unitary analysis';
    body = es
      ? 'El estado controlado sigue siendo sobreseimiento provisional comunicado el 21 de julio de 2026. La reconstrucción de 19 de agosto añade un módulo material anterior —PH122→CAM / DP 1041 / verificación favorable de la AC— y conserva como P0 el puente certificado Control 22→DP 1956. La relevancia procesal de cualquier prueba nueva corresponde a la autoridad competente.'
      : 'The controlled status remains provisional dismissal communicated on 21 July 2026. The 19 August reconstruction adds a material earlier module — PH122→CAM / PP 1041 / favourable IA verification — and keeps the certified Control 22→DP 1956 routing bridge as P0. The procedural relevance of any new evidence is for the competent authority.';
  } else {
    title = es ? 'Control 22 + Control 24: convergencia funcional con CAM como beneficiario recurrente' : 'Control 22 + Control 24: functional convergence with CAM as recurring beneficiary';
    body = es
      ? 'El nuevo digesto coloca en una sola cronología los deberes y decisiones de la AC, la supervisión judicial y los beneficios recurrentes del perímetro CAM, sin fusionar responsabilidades. La hipótesis pública más fuerte es posible facilitación concertada a investigar; acuerdo criminal y conspiración siguen sin prueba directa.'
      : 'The new digest places IA duties/decisions, judicial supervision and recurring CAM-perimeter benefits on one chronology without merging responsibility. The strongest public hypothesis is possible concerted facilitation to investigate; criminal agreement and conspiracy remain without direct proof.';
  }

  const section = document.createElement('section');
  section.id = 'control22-24-unitary-20260819';
  section.className = 'section';
  section.innerHTML = `
    <div class="shell">
      <div style="border:1px solid rgba(60,23,21,.25);border-left:6px solid #7a2824;border-radius:16px;padding:1.2rem 1.35rem;background:#fff8f6">
        <p style="margin:0 0 .45rem;font-size:.76rem;font-weight:900;letter-spacing:.07em;text-transform:uppercase;color:#7a2824">${es ? 'ACTUALIZACIÓN UNITARIA · 19 AGO 2026' : 'UNITARY UPDATE · 19 AUG 2026'}</p>
        <h2 style="margin:.15rem 0 .7rem">${title}</h2>
        <p>${body}</p>
        <p style="font-size:.92rem"><strong>${es ? 'Límite:' : 'Boundary:'}</strong> ${es ? 'máxima hipótesis investigativa, no porcentaje de culpabilidad ni declaración penal.' : 'maximum investigative hypothesis, not a guilt percentage or criminal finding.'}</p>
        <p style="display:flex;gap:.65rem;flex-wrap:wrap"><a class="button" href="${detail}">${es ? 'Abrir digesto Control 22 + 24 →' : 'Open Control 22 + 24 digest →'}</a><a class="button secondary" href="${retracto}">${es ? 'Módulo DP 1041 / retracto →' : 'PP 1041 / retracto module →'}</a></p>
      </div>
    </div>`;

  const main = document.querySelector('main');
  if (!main) return;
  const hero = main.querySelector('.hero');
  if (hero && hero.nextSibling) main.insertBefore(section, hero.nextSibling);
  else main.prepend(section);
})();
