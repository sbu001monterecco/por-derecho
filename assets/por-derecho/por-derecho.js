(() => {
  const navToggle = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-nav]');
  if (navToggle && nav) {
    navToggle.addEventListener('click', () => {
      const open = nav.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', String(open));
    });
  }

  const decisions = document.querySelectorAll('[data-decision]');
  const output = document.querySelector('[data-decision-output]');
  const audit = document.querySelector('[data-audit]');
  decisions.forEach((button) => {
    button.addEventListener('click', () => {
      decisions.forEach((item) => item.setAttribute('aria-pressed', 'false'));
      button.setAttribute('aria-pressed', 'true');
      if (output) {
        output.innerHTML = `<strong>${button.dataset.title}</strong><br>${button.dataset.output}`;
      }
      if (audit) {
        const li = document.createElement('li');
        li.textContent = `${button.dataset.audit}: se conserva la advertencia y la motivación humana.`;
        audit.prepend(li);
      }
    });
  });

  const resolvedToggle = document.querySelector('[data-resolved-toggle]');
  const resolvedPanel = document.querySelector('[data-resolved-panel]');
  if (resolvedToggle && resolvedPanel) {
    resolvedToggle.addEventListener('click', () => {
      const willOpen = resolvedPanel.hasAttribute('hidden');
      resolvedPanel.toggleAttribute('hidden');
      resolvedToggle.setAttribute('aria-expanded', String(willOpen));
      resolvedToggle.textContent = willOpen ? resolvedToggle.dataset.close : resolvedToggle.dataset.open;
    });
  }
})();
