(() => {
  if (document.getElementById('acosta-matos-canonical-people')) return;

  const path = window.location.pathname;
  if (!path.includes('/en/actors-parties-lawyers-representatives/')) return;

  const sections = Array.from(document.querySelectorAll('main > section'));
  const conflictSection = sections.find((section) => {
    const heading = section.querySelector('h2');
    return heading && heading.textContent.trim() === 'People named in the same 2018 conflict screen';
  });
  const lawyersSection = sections.find((section) => {
    const heading = section.querySelector('h2');
    return heading && heading.textContent.trim().startsWith('Lawyers, administrators, representatives and advisers');
  });

  if (!conflictSection && !lawyersSection) return;

  const section = document.createElement('section');
  section.className = 'section';
  section.id = 'acosta-matos-canonical-people';
  section.setAttribute('data-canonical-reference-register', 'PD-SP-P');

  section.innerHTML = `
    <div class="shell record">
      <p class="eyebrow">CANONICAL PERSON REFERENCES · 1 SEPTEMBER 2026</p>
      <h2>Acosta Matos and connected perimeter — canonical person references</h2>
      <p class="warn"><strong>Identity/reference register only.</strong> Inclusion below preserves the canonical person record and source-class distinction. It does not make proposed witnesses adverse actors, does not transfer responsibility among relatives or associates, and does not change the evidential status of any act.</p>
      <ul class="names" aria-label="Acosta Matos and connected perimeter canonical person references">
        <li><a href="../acosta-matos-family/"><strong>José Daniel Acosta Matos<sup>^</sup></strong></a> — <code>PD-SP-P-0011</code></li>
        <li><a href="../acosta-matos-family/"><strong>Laura Patricia Acosta Matos<sup>^</sup></strong></a> — <code>PD-SP-P-0012</code></li>
        <li><a href="../acosta-matos-family/"><strong>Javier Acosta Matos<sup>^</sup></strong></a> — <code>PD-SP-P-0093</code></li>
        <li><a href="../acosta-matos-family/"><strong>Gerardo Zacarías Acosta Matos<sup>^</sup></strong></a> — <code>PD-SP-P-0094</code></li>
        <li><a href="../acosta-matos-family/"><strong>Gerardo Nicanor Acosta Armas</strong></a> — <span class="status open">family founder record · immutable PD-SP-P ID not exposed in the current canonical source</span></li>
        <li><a href="../acosta-matos-family/#aguiar-acosta-proposed-witness-pair"><strong>Fernando Aguiar Acosta<sup>^</sup></strong></a> — <code>PD-SP-P-0088</code> · proposed witness</li>
        <li><a href="../acosta-matos-family/#aguiar-acosta-proposed-witness-pair"><strong>Laura Aguiar Acosta<sup>^</sup></strong></a> — <code>PD-SP-P-0095</code> · proposed witness</li>
        <li><a href="../francisco-mario-matos-matas/"><strong>Francisco Mario Matos Matas<sup>^</sup></strong></a> — <code>PD-SP-P-0009</code></li>
        <li><a href="../antonio-cogolludo-rojas/"><strong>Antonio Cogolludo Rojas<sup>^</sup></strong></a> — <code>PD-SP-P-0007</code></li>
        <li><a href="../shaila-maria-cogolludo-ramos/"><strong>Shaila María Cogolludo Ramos<sup>^</sup></strong></a> — <code>PD-SP-P-0008</code></li>
        <li><a href="../asuncion-aizpurua-sanchez/"><strong>Asunción Aizpurúa Sánchez<sup>^</sup></strong></a> — <code>PD-SP-P-0004</code></li>
        <li><a href="../joan-cruz-nuez/"><strong>Joan Cruz Nuez<sup>^</sup></strong></a> — <code>PD-SP-P-0145</code></li>
      </ul>
      <p><strong>Reference rule:</strong> where an immutable <code>PD-SP-P-…</code> identifier is confirmed by a canonical person record, it is printed immediately beside the name. No identifier is inferred or fabricated where the current canonical source does not expose one.</p>
    </div>`;

  if (conflictSection) {
    conflictSection.insertAdjacentElement('afterend', section);
  } else {
    lawyersSection.insertAdjacentElement('beforebegin', section);
  }
})();
