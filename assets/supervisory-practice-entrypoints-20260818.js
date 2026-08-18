(() => {
  const path = location.pathname.replace(/\/+$/, '/');
  const isEn = /\/en\//.test(path);
  const t = (es, en) => isEn ? en : es;
  const root = `/por-derecho/${isEn ? 'en' : 'es'}/`;
  const make = (html) => {
    const template = document.createElement('template');
    template.innerHTML = html.trim();
    return template.content.firstElementChild;
  };

  const addHomeGateway = () => {
    if (!new RegExp(`/por-derecho/${isEn ? 'en' : 'es'}/?$`).test(path) || document.getElementById('supervisory-practice-home-18aug')) return;
    const section = make(`
      <section class="ok-practice" id="supervisory-practice-home-18aug">
        <div class="shell">
          <p class="ok-kicker">${t('PRÁCTICA INSTITUCIONAL · EXPEDIENTE ABIERTO', 'INSTITUTIONAL PRACTICE · OPEN FILE')}</p>
          <h2>${t('El mismo expediente, cuatro puertas profesionales.', 'The same record, four professional gateways.')}</h2>
          <p class="ok-intro">${t('Cada oficina empieza por su propia competencia, sus primeros documentos y una pregunta finita. No necesita adoptar la teoría global para verificar su parte.', 'Each office starts with its own competence, first records and finite question. It need not adopt the global theory to verify its part.')}</p>
          <div class="ok-actions"><a href="${root}${isEn ? 'cnmv-ricpe-verification/' : 'cnmv-ricpe-verificacion/'}">CNMV</a><a class="secondary" href="${root}${isEn ? 'regional-incentives-gc836-p06/' : 'incentivos-regionales-gc836-p06/'}">${t('Incentivos Regionales', 'Regional Incentives')}</a><a class="secondary" href="${root}${isEn ? 'snca-eu-funds-traceability/' : 'snca-fondos-europeos-trazabilidad/'}">${t('SNCA / fondos UE', 'SNCA / EU funds')}</a><a class="secondary" href="${root}${isEn ? 'public-authority-unitary-case-reconstruction/' : 'reconstruccion-unitaria-autoridades-publicas/'}">${t('Sala limpia', 'Clean room')}</a></div>
        </div>
      </section>`);
    const summary = document.getElementById(isEn ? 'sixty-second-summary' : 'resumen-60-segundos');
    if (summary) summary.insertAdjacentElement('afterend', section);
    else document.querySelector('main')?.insertAdjacentElement('afterbegin', section);
  };

  const addUpdate = () => {
    const updates = /\/(actualizaciones|updates)\/$/.test(path);
    if (!updates || document.getElementById('open-kimono-supervisory-practice-18aug')) return;
    const section = make(isEn ? `
      <section class="updates-section" data-open-kimono-update><div class="shell"><section class="date-group"><h2>18 August 2026 · supervisory practice</h2><div class="update-stream"><article class="material-update institutional" id="open-kimono-supervisory-practice-18aug"><div class="update-meta"><span class="new">Implemented</span><span>CNMV</span><span>Regional Incentives</span><span>ERDF / SNCA</span></div><h3>Open-file practitioner system: good supervisory practice and a warning of its opposite</h3><p>The public architecture now gives CNMV, RICPE, Regional Incentives and European-funds practitioners bounded routes with competence maps, first documents, decision trees, production lists, contrary-evidence tests and source-specific number controls.</p><p>The implementation also corrects the two controlled MYND funding totals: €6,570,713.56 in the 20-September-2023 prospectus and €6,573,703.10 in a separate accounts reconstruction, leaving the €2,989.54 difference open rather than silently normalising it.</p><p><strong>Boundary:</strong> the best-practice/opposite-practice contrast is a public, falsifiable audit standard. It does not assert that every named institution engaged in every negative practice.</p><div class="update-actions"><a class="button" href="../cnmv-ricpe-verification/">CNMV gateway →</a><a class="button secondary" href="../regional-incentives-gc836-p06/">Regional Incentives</a><a class="button secondary" href="../snca-eu-funds-traceability/">EU funds / SNCA</a></div></article></div></section></div></section>` : `
      <section class="updates-section" data-open-kimono-update><div class="shell"><section class="date-group"><h2>18 agosto 2026 · práctica supervisora</h2><div class="update-stream"><article class="material-update institutional" id="open-kimono-supervisory-practice-18aug"><div class="update-meta"><span class="new">Implementado</span><span>CNMV</span><span>Incentivos Regionales</span><span>FEDER / SNCA</span></div><h3>Sistema de expediente abierto: buena práctica supervisora y advertencia de su opuesto</h3><p>La arquitectura pública ofrece ahora a CNMV, RICPE, Incentivos Regionales y fondos europeos rutas delimitadas con mapas de competencia, primeros documentos, árboles de decisión, listas de producción, prueba de evidencia contraria y control de cifras por fuente.</p><p>La implementación corrige además los dos totales controlados de financiación MYND: €6.570.713,56 en el folleto de 20 septiembre 2023 y €6.573.703,10 en una reconstrucción separada de cuentas, dejando abierta la diferencia de €2.989,54 en lugar de normalizarla.</p><p><strong>Límite:</strong> el contraste entre buena práctica y práctica opuesta es un estándar público y falsable de auditoría. No afirma que cada institución mencionada haya incurrido en todas las prácticas negativas.</p><div class="update-actions"><a class="button" href="../cnmv-ricpe-verificacion/">Puerta CNMV →</a><a class="button secondary" href="../incentivos-regionales-gc836-p06/">Incentivos Regionales</a><a class="button secondary" href="../snca-fondos-europeos-trazabilidad/">Fondos UE / SNCA</a></div></article></div></section></div></section>`);
    const hero = document.querySelector('.updates-hero');
    if (hero) hero.insertAdjacentElement('afterend', section);
  };

  const apply = () => { addHomeGateway(); addUpdate(); };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => setTimeout(apply, 1200), { once: true });
  else setTimeout(apply, 1200);
  setTimeout(apply, 2600);
})();