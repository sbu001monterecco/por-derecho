(() => {
  const root = document.querySelector('[data-case-lab]');
  if (!root) return;

  const es = document.documentElement.lang === 'es';
  const state = {
    layer: 'title',
    time: 't0',
    role: 'ac',
    decision: es ? 'Sin decisión' : 'No decision',
    outcome: 'reconciled'
  };

  const text = es ? {
    layer: 'Capa visual', time: 'Momento de conocimiento', role: 'Perspectiva', decision: 'Decisión humana', outcome: 'Resultado explorado',
    stages: {t0:'Expediente inicial',t1:'Alerta incorporada',t2:'Prueba complementaria'},
    roles: {ac:'Administrador Concursal',judge:'Decisor judicial',prosecutor:'Revisión fiscal, si procede',reviewer:'Revisión institucional'},
    outcomes: {reconciled:'Preocupación reconciliada',restructured:'Operación reestructurada',unresolved:'Se procede sin reconciliación'},
    opened: 'Documento abierto', layerChanged:'Capa del mapa cambiada', roleChanged:'Perspectiva profesional cambiada', timeChanged:'Momento de conocimiento cambiado', outcomeChanged:'Resultado explorado', decisionChanged:'Decisión humana registrada'
  } : {
    layer: 'Visual layer', time: 'Knowledge point', role: 'Viewpoint', decision: 'Human decision', outcome: 'Outcome explored',
    stages: {t0:'Initial record',t1:'Alert received',t2:'Supplementary evidence'},
    roles: {ac:'Insolvency practitioner',judge:'Judicial decision-maker',prosecutor:'Prosecutorial review, where applicable',reviewer:'Institutional review'},
    outcomes: {reconciled:'Concern reconciled',restructured:'Transaction restructured',unresolved:'Proceed without reconciliation'},
    opened: 'Document opened', layerChanged:'Map layer changed', roleChanged:'Professional viewpoint changed', timeChanged:'Knowledge point changed', outcomeChanged:'Outcome explored', decisionChanged:'Human decision recorded'
  };

  const reportFields = {
    layer: document.querySelector('[data-report-layer]'),
    time: document.querySelector('[data-report-time]'),
    role: document.querySelector('[data-report-role]'),
    decision: document.querySelector('[data-report-decision]'),
    outcome: document.querySelector('[data-report-outcome]'),
    documents: document.querySelector('[data-report-documents]')
  };
  const reportLog = document.querySelector('[data-report-log]');

  function log(message) {
    if (!reportLog) return;
    const li = document.createElement('li');
    const stamp = new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
    li.textContent = `${stamp} — ${message}`;
    reportLog.prepend(li);
  }

  function visibleDocumentCount() {
    return Array.from(document.querySelectorAll('[data-doc]')).filter((doc) => !doc.hidden).length;
  }

  function updateReport() {
    if (reportFields.layer) {
      const activeLayer = document.querySelector('[data-layer-button][aria-pressed="true"]');
      reportFields.layer.textContent = activeLayer ? activeLayer.textContent.trim() : state.layer;
    }
    if (reportFields.time) reportFields.time.textContent = text.stages[state.time];
    if (reportFields.role) reportFields.role.textContent = text.roles[state.role];
    if (reportFields.decision) reportFields.decision.textContent = state.decision;
    if (reportFields.outcome) reportFields.outcome.textContent = text.outcomes[state.outcome];
    if (reportFields.documents) reportFields.documents.textContent = String(visibleDocumentCount());
  }

  const map = document.querySelector('[data-perimeter-map]');
  document.querySelectorAll('[data-layer-button]').forEach((button) => {
    button.addEventListener('click', () => {
      document.querySelectorAll('[data-layer-button]').forEach((item) => item.setAttribute('aria-pressed', 'false'));
      button.setAttribute('aria-pressed', 'true');
      state.layer = button.dataset.layerButton;
      if (map) map.dataset.layer = state.layer;
      log(`${text.layerChanged}: ${button.textContent.trim()}`);
      updateReport();
    });
  });

  const timeSummary = document.querySelector('[data-time-summary]');
  const timeCopy = es ? {
    t0:'Solo están disponibles el inventario inicial, los títulos básicos, la hipoteca, el acuerdo operativo y la valoración. La advertencia del tercero todavía no forma parte del expediente decisorio.',
    t1:'La comunicación del tercero y la discrepancia registral ya constan. El profesional debe decidir si la pregunta de perímetro requiere verificación, acotación, motivación reforzada o escalado.',
    t2:'Se aporta prueba complementaria posterior a la primera propuesta. Debe tratarse como nueva evidencia, no como si hubiera estado disponible desde el inicio.'
  } : {
    t0:'Only the initial inventory, basic title documents, mortgage, operating agreement and valuation are available. The third party’s warning is not yet part of the decision record.',
    t1:'The third-party communication and registry discrepancy are now in the file. The professional must decide whether the perimeter question calls for verification, narrowing, enhanced reasons or escalation.',
    t2:'Supplementary evidence is produced after the first proposal. It must be treated as new evidence, not as if it had been available from the outset.'
  };

  function setTime(stage, announce = true) {
    state.time = stage;
    document.querySelectorAll('[data-time-button]').forEach((item) => item.setAttribute('aria-pressed', String(item.dataset.timeButton === stage)));
    document.querySelectorAll('[data-doc]').forEach((doc) => {
      const available = Number(doc.dataset.available || 0);
      const current = Number(stage.slice(1));
      doc.hidden = available > current;
    });
    if (timeSummary) timeSummary.textContent = timeCopy[stage];
    if (announce) log(`${text.timeChanged}: ${text.stages[stage]}`);
    updateReport();
  }

  document.querySelectorAll('[data-time-button]').forEach((button) => {
    button.addEventListener('click', () => setTime(button.dataset.timeButton));
  });

  document.querySelectorAll('[data-doc]').forEach((doc) => {
    doc.addEventListener('click', () => {
      doc.classList.toggle('is-open');
      const title = doc.querySelector('h3');
      if (title) log(`${text.opened}: ${title.textContent.trim()}`);
    });
  });

  document.querySelectorAll('[data-role-button]').forEach((button) => {
    button.addEventListener('click', () => {
      state.role = button.dataset.roleButton;
      document.querySelectorAll('[data-role-button]').forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
      document.querySelectorAll('[data-role-panel]').forEach((panel) => panel.classList.toggle('is-active', panel.dataset.rolePanel === state.role));
      log(`${text.roleChanged}: ${text.roles[state.role]}`);
      updateReport();
    });
  });

  const decisionOutput = document.querySelector('[data-lab-decision-output]');
  document.querySelectorAll('[data-lab-decision]').forEach((button) => {
    button.addEventListener('click', () => {
      document.querySelectorAll('[data-lab-decision]').forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
      state.decision = button.dataset.title;
      if (decisionOutput) decisionOutput.innerHTML = `<strong>${button.dataset.title}</strong><br>${button.dataset.output}`;
      log(`${text.decisionChanged}: ${state.decision}`);
      updateReport();
    });
  });

  document.querySelectorAll('[data-outcome-button]').forEach((button) => {
    button.addEventListener('click', () => {
      state.outcome = button.dataset.outcomeButton;
      document.querySelectorAll('[data-outcome-button]').forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
      document.querySelectorAll('[data-outcome-panel]').forEach((panel) => panel.classList.toggle('is-active', panel.dataset.outcomePanel === state.outcome));
      log(`${text.outcomeChanged}: ${text.outcomes[state.outcome]}`);
      updateReport();
    });
  });

  const printButton = document.querySelector('[data-print-report]');
  if (printButton) printButton.addEventListener('click', () => window.print());

  const stageLinks = Array.from(document.querySelectorAll('.pdl-stage-link'));
  const acts = Array.from(document.querySelectorAll('.pdl-act'));
  if ('IntersectionObserver' in window && acts.length) {
    const observer = new IntersectionObserver((entries) => {
      const visible = entries.filter((entry) => entry.isIntersecting).sort((a,b) => b.intersectionRatio - a.intersectionRatio)[0];
      if (!visible) return;
      stageLinks.forEach((link) => link.classList.toggle('is-active', link.getAttribute('href') === `#${visible.target.id}`));
    }, {rootMargin:'-28% 0px -58% 0px', threshold:[0,.2,.5]});
    acts.forEach((act) => observer.observe(act));
  }

  setTime('t0', false);
  updateReport();
})();
