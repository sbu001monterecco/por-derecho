(() => {
  const path = window.location.pathname.replace(/\/+$/, '/');
  const isEnglish = path.endsWith('/en/lender-of-record/');
  const isSpanish = path.endsWith('/es/acreedor-de-registro/');
  if (!isEnglish && !isSpanish) return;
  if (document.getElementById('pink-canary-spanish-name-continuity')) return;

  const timeline = document.querySelector('#chronology .timeline, #cronologia .timeline');
  if (!timeline) return;

  const ukContinuity = document.getElementById('aweswell-name-continuity');
  const registrationItem = [...timeline.querySelectorAll('.timeline-item')].find((item) => {
    const heading = item.querySelector('h3')?.textContent || '';
    return heading.includes('11 January / 14 February 2012') ||
      heading.includes('11 de enero / 14 de febrero de 2012');
  });
  const anchor = ukContinuity || registrationItem;
  if (!anchor) return;

  const item = document.createElement('article');
  item.className = 'timeline-item';
  item.id = 'pink-canary-spanish-name-continuity';
  item.innerHTML = isEnglish
    ? `
      <h3>30 September 2013 — separate Spanish company, same NIF, new name</h3>
      <p>This is a different legal person from UK company no. 07716847. The Spanish company appears in its signed shareholder register for 2012 as <strong>Monterecco Sun Park, S.L.</strong>, NIF <strong>B76564517</strong>. The 2013 entry uses <strong>Pink Canary Services, S.L.</strong> with the same NIF and records a “cambio de denominación social” dated 30 September 2013.</p>
      <p>Sentencia 163/2023 also describes Monterecco Sun Park, S.L. as “currently named Pink Canary Services, S.L.” The legal conclusion is continuity of the same Spanish company—not a transfer of the operating contract, a new operator or a successor company. “S.L.U.” identifies single-member status; it is not a different legal person.</p>
      <p>The exact notarial deed and Mercantile Registry inscription/publication that made the change registrally effective have not yet been located. The 30 September 2013 date is therefore attributed to the signed company book, while the exact registry date remains a source-completion item.</p>
      <p class="source-policy"><strong>Do not confuse the two name changes:</strong> UK <em>Monterecco Sun Park Limited → Aweswell Limited</em>, company no. 07716847; Spain <em>Monterecco Sun Park, S.L. → Pink Canary Services, S.L.</em>, NIF B76564517. Official Spanish background: <a href="https://www.boe.es/diario_borme/txt.php?id=BORME-A-2012-110-38" rel="external noopener">BORME — Monterecco Sun Park, sheet H TF 49739</a> · <a href="https://www.boe.es/diario_boe/txt.php?id=BOE-A-2019-14965" rel="external noopener">later official name/NIF record</a>.</p>`
    : `
      <h3>30 de septiembre de 2013 — sociedad española distinta, mismo NIF, nueva denominación</h3>
      <p>Se trata de una persona jurídica distinta de la sociedad británica nº 07716847. El libro registro de socios firmado identifica a la sociedad española en 2012 como <strong>Monterecco Sun Park, S.L.</strong>, NIF <strong>B76564517</strong>. La anotación de 2013 utiliza <strong>Pink Canary Services, S.L.</strong> con el mismo NIF y registra un “cambio de denominación social” de 30 de septiembre de 2013.</p>
      <p>La Sentencia 163/2023 también describe a Monterecco Sun Park, S.L. como “actualmente denominada Pink Canary Services, S.L.” La conclusión jurídica es la continuidad de la misma sociedad española—no una transmisión del contrato de explotación, un nuevo operador o una sociedad sucesora. “S.L.U.” indica unipersonalidad; no identifica otra persona jurídica.</p>
      <p>Todavía no se han localizado la escritura notarial exacta ni la inscripción/publicación del Registro Mercantil que hicieron registralmente efectivo el cambio. Por ello, la fecha de 30 de septiembre de 2013 se atribuye al libro societario firmado, mientras que la fecha registral exacta permanece como necesidad de completitud documental.</p>
      <p class="source-policy"><strong>No confundir los dos cambios de denominación:</strong> Reino Unido <em>Monterecco Sun Park Limited → Aweswell Limited</em>, sociedad nº 07716847; España <em>Monterecco Sun Park, S.L. → Pink Canary Services, S.L.</em>, NIF B76564517. Contexto oficial español: <a href="https://www.boe.es/diario_borme/txt.php?id=BORME-A-2012-110-38" rel="external noopener">BORME — Monterecco Sun Park, hoja H TF 49739</a> · <a href="https://www.boe.es/diario_boe/txt.php?id=BOE-A-2019-14965" rel="external noopener">registro oficial posterior de nombre/NIF</a>.</p>`;

  anchor.insertAdjacentElement('afterend', item);
})();
