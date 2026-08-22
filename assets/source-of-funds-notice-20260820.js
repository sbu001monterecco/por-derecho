(() => {
  const script = document.currentScript;
  const base = script && script.src ? new URL('.', script.src) : new URL('/assets/', location.href);
  if (!document.querySelector('link[data-source-funds-css]')) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = new URL('source-of-funds-notice-20260820.css?v=20260822d', base).href;
    link.dataset.sourceFundsCss = '20260820';
    document.head.append(link);
  }

  const lang = document.documentElement.lang === 'en' ? 'en' : 'es';
  const copy = {
    es: {
      kicker: 'Advertencia profesional · antes de actuar',
      title: '¿Quién paga y qué se está defendiendo?',
      compactTitle: 'Antes de aceptar instrucciones o pagos',
      lead: 'Si fondos, ingresos, activos o valor vinculados a un perímetro controvertido se utilizan para pagar la defensa, conservación o promoción de ese mismo perímetro, la cadena de financiación e instrucciones debe identificarse, verificarse y conservarse.',
      compactLead: 'Verifique quién paga, quién se beneficia y qué posición controvertida se está financiando para defender.',
      rule: 'Antes de actuar:',
      steps: ['quién instruye', 'quién paga', 'quién se beneficia', 'qué autoridad existe', 'qué finalidad se persigue'],
      direction: 'Antes de aceptar instrucciones o fondos: verificar · preservar · documentar · abstenerse o escalar cuando proceda.',
      boundary: 'Este es un aviso de verificación y preservación, no una acusación de irregularidad. Prestar servicios, recibir fondos o aparecer en el registro documental no acredita por sí solo conocimiento, participación o responsabilidad.',
      mark: 'El Ojo de la Trazabilidad',
      alt: 'El Ojo de la Trazabilidad: revisión del origen, autoridad y destino del dinero',
      read: 'Leer el aviso profesional completo →',
      compactRead: 'Por qué importa →',
      reply: 'Aportar corrección o documentación',
      scopeAnchor: 'alcance',
      replyAnchor: 'respuesta'
    },
    en: {
      kicker: 'Professional warning · before you act',
      title: 'Who is paying—and what is being defended?',
      compactTitle: 'Before accepting instructions or payment',
      lead: 'If funds, income, assets or value connected with a disputed perimeter are being used to pay for the defence, preservation or advancement of that same perimeter, the funding and instruction chain must be identified, verified and preserved.',
      compactLead: 'Verify who pays, who benefits and what contested position the money is being used to defend.',
      rule: 'Before acting:',
      steps: ['who instructs', 'who pays', 'who benefits', 'what authority exists', 'what purpose is served'],
      direction: 'Before accepting instructions or funds: verify · preserve · document · decline or escalate where appropriate.',
      boundary: 'This is a verification and preservation notice, not an allegation of wrongdoing. Providing services, receiving funds or appearing in the documentary record does not itself establish knowledge, participation or responsibility.',
      mark: 'The Traceability Eye',
      alt: 'The Traceability Eye: review of the source, authority and destination of money',
      read: 'Read the full professional notice →',
      compactRead: 'Why this matters →',
      reply: 'Submit a correction or document',
      scopeAnchor: 'scope',
      replyAnchor: 'response'
    }
  }[lang];

  const canonical = new URL(lang === 'en'
    ? '../en/source-of-funds-professional-services-notice/'
    : '../es/aviso-procedencia-fondos-servicios-profesionales/', base);
  const icon = new URL('por-derecho/second-pair-eyes.svg?v=20260822b', base);

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
    img.alt = copy.alt;
    img.width = 112;
    img.height = 84;
    mark.append(img, node('span', '', copy.mark));

    const body = node('div', 'sfn__body');
    body.append(node('p', 'sfn__kicker', copy.kicker));
    const h2 = node('h2', '', variant === 'compact' ? copy.compactTitle : copy.title);
    h2.id = titleId;
    body.append(h2, node('p', 'sfn__lead', variant === 'compact' ? copy.compactLead : copy.lead));

    const rule = node('div', 'sfn__rule');
    rule.append(node('strong', '', copy.rule));
    const steps = node('div', 'sfn__steps');
    copy.steps.forEach(step => steps.append(node('span', '', step)));
    rule.append(steps);
    body.append(rule, node('p', 'sfn__direction', copy.direction), node('p', 'sfn__boundary', copy.boundary));

    const actions = node('div', 'sfn__actions');
    const read = node('a', 'sfn__button', variant === 'compact' ? copy.compactRead : copy.read);
    read.href = `${canonical.href}#${copy.scopeAnchor}`;
    const reply = node('a', 'sfn__button sfn__button--secondary', copy.reply);
    reply.href = `${canonical.href}#${copy.replyAnchor}`;
    actions.append(read);
    if (variant === 'full') actions.append(reply);
    body.append(actions);
    grid.append(mark, body);
    aside.append(grid);
    root.replaceChildren(aside);

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduceMotion || !('IntersectionObserver' in window)) {
      aside.classList.add('sfn--visible');
    } else {
      const observer = new IntersectionObserver(entries => {
        if (!entries.some(entry => entry.isIntersecting)) return;
        aside.classList.add('sfn--visible');
        observer.disconnect();
      }, { threshold: 0.18 });
      observer.observe(aside);
    }
  });
})();
