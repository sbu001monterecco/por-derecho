(() => {
  const script = document.currentScript;
  const base = script && script.src ? new URL('.', script.src) : new URL('/assets/', location.href);
  if (!document.querySelector('link[data-source-funds-css]')) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = new URL('source-of-funds-notice-20260820.css', base).href;
    link.dataset.sourceFundsCss = '20260820';
    document.head.append(link);
  }

  const lang = document.documentElement.lang === 'en' ? 'en' : 'es';
  const copy = {
    es: {
      kicker: 'Aviso permanente · procedencia, autoridad y trazabilidad',
      title: 'La procedencia del dinero y de los servicios también forma parte de la prueba.',
      lead: 'Quien financie, reciba, administre, transmita, asegure, audite, asesore o facture en relación con activos, derechos, obras, ayudas, ingresos o litigios vinculados a este expediente debe verificar identidad, beneficiario efectivo, título, autoridad, finalidad y origen y destino de los fondos.',
      compactLead: 'Financiadores, beneficiarios, operadores y asesores deben verificar identidad, beneficiario efectivo, título, autoridad, finalidad y origen y destino de los fondos antes de actuar.',
      rule: 'Antes de actuar:',
      steps: ['verificar', 'preservar', 'documentar', 'abstenerse o escalar cuando proceda'],
      boundary: 'La mera prestación de servicios, recepción de fondos o aparición en este registro no prueba irregularidad. Este aviso no determina conocimiento jurídico ni sustituye una comunicación individual. Toda responsabilidad exige prueba de deber, conocimiento, acto u omisión, causalidad y daño.',
      mark: 'Segundo par de ojos · control neutral',
      read: 'Leer el aviso completo',
      reply: 'Aportar corrección o documentación',
      scopeAnchor: 'alcance',
      replyAnchor: 'respuesta'
    },
    en: {
      kicker: 'Standing notice · provenance, authority and traceability',
      title: 'The source of money and professional services is part of the evidence too.',
      lead: 'Anyone financing, receiving, administering, transferring, insuring, auditing, advising or invoicing in connection with assets, rights, works, public support, income or proceedings linked to this record should verify identity, beneficial ownership, title, authority, purpose, and the source and destination of funds.',
      compactLead: 'Funders, beneficiaries, operators and advisers should verify identity, beneficial ownership, title, authority, purpose, and the source and destination of funds before acting.',
      rule: 'Before acting:',
      steps: ['verify', 'preserve', 'document', 'decline or escalate where appropriate'],
      boundary: 'Providing services, receiving funds or appearing in this record does not prove wrongdoing. This notice does not determine legal knowledge or replace individual notice. Any responsibility requires evidence of duty, knowledge, act or omission, causation and loss.',
      mark: 'Second pair of eyes · neutral control',
      read: 'Read the full notice',
      reply: 'Submit a correction or document',
      scopeAnchor: 'scope',
      replyAnchor: 'response'
    }
  }[lang];

  const canonical = new URL(lang === 'en'
    ? '../en/source-of-funds-professional-services-notice/'
    : '../es/aviso-procedencia-fondos-servicios-profesionales/', base);
  const icon = new URL('por-derecho/second-pair-eyes.svg', base);

  const node = (tag, className, text) => {
    const el = document.createElement(tag);
    if (className) el.className = className;
    if (text !== undefined) el.textContent = text;
    return el;
  };

  document.querySelectorAll('[data-source-of-funds-notice]').forEach((root, index) => {
    if (root.dataset.rendered === 'true') return;
    root.dataset.rendered = 'true';
    const variant = root.dataset.sourceOfFundsNotice === 'compact' ? 'compact' : 'full';
    const aside = node('aside', `sfn sfn--${variant}`);
    aside.setAttribute('role', 'note');
    const titleId = `sfn-title-${index + 1}`;
    aside.setAttribute('aria-labelledby', titleId);

    const grid = node('div', 'sfn__grid');
    const mark = node('div', 'sfn__mark');
    const img = document.createElement('img');
    img.src = icon.href;
    img.alt = '';
    img.width = 112;
    img.height = 84;
    mark.append(img, node('span', '', copy.mark));

    const body = node('div', 'sfn__body');
    body.append(node('p', 'sfn__kicker', copy.kicker));
    const h2 = node('h2', '', copy.title);
    h2.id = titleId;
    body.append(h2, node('p', 'sfn__lead', variant === 'compact' ? copy.compactLead : copy.lead));

    const rule = node('div', 'sfn__rule');
    rule.append(node('strong', '', copy.rule));
    const steps = node('div', 'sfn__steps');
    copy.steps.forEach(step => steps.append(node('span', '', step)));
    rule.append(steps);
    body.append(rule, node('p', 'sfn__boundary', copy.boundary));

    const actions = node('div', 'sfn__actions');
    const read = node('a', 'sfn__button', copy.read);
    read.href = `${canonical.href}#${copy.scopeAnchor}`;
    const reply = node('a', 'sfn__button sfn__button--secondary', copy.reply);
    reply.href = `${canonical.href}#${copy.replyAnchor}`;
    actions.append(read, reply);
    body.append(actions);
    grid.append(mark, body);
    aside.append(grid);
    root.replaceChildren(aside);
  });
})();
