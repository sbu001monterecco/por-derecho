(() => {
  const path = window.location.pathname.replace(/\/+$/, '/');
  const isEnglish = path.endsWith('/en/lender-of-record/');
  const isSpanish = path.endsWith('/es/acreedor-de-registro/');
  if (!isEnglish && !isSpanish) return;
  if (document.getElementById('aweswell-name-continuity')) return;

  const timeline = document.querySelector('#chronology .timeline, #cronologia .timeline');
  if (!timeline) return;

  const items = [...timeline.querySelectorAll('.timeline-item')];
  const acquisitionItem = items.find((item) => {
    const heading = item.querySelector('h3')?.textContent || '';
    return heading.includes('1 December 2011') || heading.includes('1 de diciembre de 2011');
  });

  if (acquisitionItem) {
    const paragraphs = [...acquisitionItem.querySelectorAll('p')];
    const target = paragraphs.find((p) =>
      p.textContent.includes('Aweswell–Monterecco') ||
      p.textContent.includes('Aweswell-Monterecco')
    );

    if (target) {
      target.textContent = isEnglish
        ? 'The UK register later records Monterecco Sun Park Limited as the former registered name of the same company now called Aweswell Limited. The remaining open questions concern acquisition consideration, financing, beneficial arrangements and wider group relationships—not a transfer or succession between Monterecco and Aweswell.'
        : 'El registro británico identifica posteriormente Monterecco Sun Park Limited como la denominación anterior de la misma sociedad actualmente llamada Aweswell Limited. Las cuestiones todavía abiertas se refieren a la contraprestación, financiación, acuerdos económicos y relaciones más amplias del grupo—no a una transmisión o sucesión entre Monterecco y Aweswell.';
    }
  }

  const registrationItem = items.find((item) => {
    const heading = item.querySelector('h3')?.textContent || '';
    return heading.includes('11 January / 14 February 2012') ||
      heading.includes('11 de enero / 14 de febrero de 2012');
  });
  if (!registrationItem) return;

  const continuityItem = document.createElement('article');
  continuityItem.className = 'timeline-item';
  continuityItem.id = 'aweswell-name-continuity';
  continuityItem.innerHTML = isEnglish
    ? `
      <h3>2–3 June 2014 — same company, new registered name</h3>
      <p>Companies House records one continuous UK company, number <strong>07716847</strong>. It was incorporated on 25 July 2011 as <strong>Monterecco Sun Park Limited</strong>. A special resolution dated 2 June 2014 changed its name, and Companies House registered <strong>Aweswell Limited</strong> and issued the certificate on 3 June 2014.</p>
      <p>This was a change of corporate name—not a transfer of the LPB shares, a novation, a new investor or a successor company. Section 81 of the Companies Act 2006 preserves the company's rights, obligations and legal proceedings following a registered name change.</p>
      <p>The public filing records the legal mechanism but not the commercial reason for choosing “Aweswell”. A broader, less project-specific holding-company identity is a reasonable interpretation of later usage, but it remains an inference unless supported by a contemporaneous 2014 resolution, board paper or correspondence.</p>
      <p class="source-policy">Official UK record: <a href="https://find-and-update.company-information.service.gov.uk/company/07716847" rel="external noopener">Companies House company overview</a> · <a href="https://find-and-update.company-information.service.gov.uk/company/07716847/filing-history?page=2" rel="external noopener">name-change filing history</a> · <a href="https://www.legislation.gov.uk/ukpga/2006/46/section/81" rel="external noopener">Companies Act 2006, section 81</a>.</p>`
    : `
      <h3>2–3 de junio de 2014 — misma sociedad, nueva denominación registral</h3>
      <p>Companies House registra una única sociedad británica continua, número <strong>07716847</strong>. Se constituyó el 25 de julio de 2011 como <strong>Monterecco Sun Park Limited</strong>. Una resolución especial de 2 de junio de 2014 cambió su denominación, y Companies House registró <strong>Aweswell Limited</strong> y expidió el certificado el 3 de junio de 2014.</p>
      <p>Fue un cambio de denominación social—no una transmisión de las participaciones de LPB, una novación, un nuevo inversor o una sociedad sucesora. El artículo 81 de la Companies Act 2006 mantiene los derechos, obligaciones y procedimientos judiciales de la sociedad después del cambio registral de nombre.</p>
      <p>El asiento público acredita el mecanismo jurídico, pero no explica el motivo comercial de elegir “Aweswell”. Interpretarlo como una identidad de holding más amplia y menos vinculada a un solo proyecto es razonable a partir del uso posterior, pero sigue siendo una inferencia salvo que aparezca una resolución, acta o correspondencia contemporánea de 2014.</p>
      <p class="source-policy">Registro oficial británico: <a href="https://find-and-update.company-information.service.gov.uk/company/07716847" rel="external noopener">ficha de Companies House</a> · <a href="https://find-and-update.company-information.service.gov.uk/company/07716847/filing-history?page=2" rel="external noopener">historial del cambio de denominación</a> · <a href="https://www.legislation.gov.uk/ukpga/2006/46/section/81" rel="external noopener">Companies Act 2006, artículo 81</a>.</p>`;

  registrationItem.insertAdjacentElement('afterend', continuityItem);
})();
