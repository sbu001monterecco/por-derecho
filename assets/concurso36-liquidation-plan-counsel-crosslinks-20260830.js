(() => {
  const p = window.location.pathname;
  const es = /\/es\//.test(p);
  const relevant = [
    'insolvency-36-2012-court-record', 'concurso-36-2012-registro-procesal',
    'insolvency-36-2012-continuity-governance-7-june', 'concurso-36-2012-continuidad-gobernanza-7-junio',
    'insolvency-36-2012-community-authority', 'concurso-36-2012-autoridad-comunidad',
    'insolvency-36-2012-arrecife-mercantile-bridge', 'concurso-36-2012-puente-arrecife-mercantil',
    'insolvency-36-2012-liquidation-plan-judge-laj-audit', 'concurso-36-2012-auditoria-plan-liquidacion-juez-laj',
    'insolvency-36-2012-luis-miguel-lopez-filings', 'concurso-36-2012-escritos-luis-miguel-lopez'
  ].some(s => p.includes(s));
  if (!relevant || document.querySelector('[data-c36-plan-counsel-crosslinks]')) return;

  const root = document.createElement('section');
  root.className = 'section';
  root.setAttribute('data-c36-plan-counsel-crosslinks', '20260830');
  root.innerHTML = es ? `
    <div class="shell" style="max-width:1180px">
      <div style="border:1px solid #dce2e2;border-left:6px solid #315c7b;border-radius:14px;background:#fff;padding:1rem 1.1rem">
        <p class="eyebrow" style="margin-top:0">CONTROL 36/2012 · PLAN / JUEZ / LAJ / DEFENSA</p>
        <h2 style="margin:.2rem 0 .55rem">El cumplimiento del plan y la historia de los recursos deben leerse juntos.</h2>
        <p style="margin:.2rem 0 .8rem">La existencia de escritos de impugnación no demuestra por sí sola incumplimiento judicial; pero impide tratar el resultado como una ejecución no controvertida del plan. Separar siempre acto del juez, acto LAJ, objeción, respuesta, recurso, firmeza e implementación.</p>
        <p style="margin:0"><a href="/por-derecho/es/concurso-36-2012-auditoria-plan-liquidacion-juez-laj/"><strong>Auditoría plan / juez / LAJ →</strong></a> · <a href="/por-derecho/es/concurso-36-2012-escritos-luis-miguel-lopez/"><strong>Escritos Luis Miguel López →</strong></a> · <a href="/por-derecho/es/concurso-36-2012-registro-procesal/"><strong>Registro procesal →</strong></a></p>
      </div>
    </div>` : `
    <div class="shell" style="max-width:1180px">
      <div style="border:1px solid #dce2e2;border-left:6px solid #315c7b;border-radius:14px;background:#fff;padding:1rem 1.1rem">
        <p class="eyebrow" style="margin-top:0">36/2012 CONTROL · PLAN / JUDGE / LAJ / COUNSEL</p>
        <h2 style="margin:.2rem 0 .55rem">Plan compliance and the remedy history must be read together.</h2>
        <p style="margin:.2rem 0 .8rem">The existence of formal objections does not itself prove judicial non-compliance; but it prevents the outcome from being described as an uncontested implementation of the plan. Always separate judge act, LAJ act, objection, response, review, finality and implementation.</p>
        <p style="margin:0"><a href="/por-derecho/en/insolvency-36-2012-liquidation-plan-judge-laj-audit/"><strong>Plan / judge / LAJ audit →</strong></a> · <a href="/por-derecho/en/insolvency-36-2012-luis-miguel-lopez-filings/"><strong>Luis Miguel López filings →</strong></a> · <a href="/por-derecho/en/insolvency-36-2012-court-record/"><strong>Court record →</strong></a></p>
      </div>
    </div>`;

  const main = document.querySelector('main');
  if (main) main.appendChild(root);
})();