(()=> {
  const root = document.querySelector('[data-cua-primary-record]');
  if (!root) return;

  const lang = document.documentElement.lang === 'es' ? 'es' : 'en';
  const E = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  })[c]);

  const href = (p) => '../../' + String(p).replace(/^\//, '');
  const label = (p) => String(p)
    .replace(/^\/en\//, '')
    .replace(/^\/es\//, '')
    .replace(/\/$/, '')
    .replaceAll('-', ' ');

  fetch('../../assets/data/cuatrecasas-primary-record-v1.json')
    .then((r) => {
      if (!r.ok) throw Error(r.status);
      return r.json();
    })
    .then((index) => Promise.all(index.shards.map((f) =>
      fetch('../../assets/data/' + f).then((r) => {
        if (!r.ok) throw Error(r.status);
        return r.json();
      })
    )))
    .then((parts) => {
      const all = parts.flatMap((d) => d.documents);
      const receipts = Object.fromEntries(
        all.filter((x) => x.id.startsWith('CUA-REC-')).map((x) => [x.id, x])
      );
      const docs = all
        .filter((x) => !x.id.startsWith('CUA-REC-'))
        .sort((a, b) => a.date.localeCompare(b.date) || a.id.localeCompare(b.id));

      const quarters = {};
      docs.forEach((x) => (quarters[x.quarter] ??= []).push(x));

      root.innerHTML = Object.keys(quarters).sort().map((quarter) => {
        const cards = quarters[quarter].map((x) => {
          const title = lang === 'es' ? x.title_es : x.title_en;
          const establishes = lang === 'es' ? x.establishes_es : x.establishes;
          const doesNot = lang === 'es' ? x.does_not_es : x.does_not;
          const defensive = lang === 'es' ? x.defensive_relevance_es : x.defensive_relevance_en;
          const pubNote = lang === 'es' ? x.publication_note_es : x.publication_note_en;

          const receipt = x.receipt && receipts[x.receipt]
            ? '<p><strong>' + (lang === 'es' ? 'Prueba de presentación:' : 'Filing proof:') +
              '</strong> ' + E(x.receipt) + ' · ' +
              (lang === 'es'
                ? 'acuse LexNET controlado como metadato privado'
                : 'LexNET receipt controlled as private metadata') +
              '.</p>'
            : '';

          const links = (x.links || []).length
            ? '<p class="context"><strong>' +
              (lang === 'es' ? 'Contextos relacionados:' : 'Related contexts:') +
              '</strong> ' +
              (x.links || []).map((p) =>
                '<a href="' + E(href(p)) + '">' + E(label(p)) + '</a>'
              ).join(' · ') +
              '</p>'
            : '';

          const viewer = x.viewer_pdf
            ? '<details class="pdfbox"><summary>' +
              (lang === 'es' ? 'Abrir visor PDF' : 'Open PDF viewer') +
              ' · ' + E(x.id) +
              '</summary><p class="pubnote">' + E(pubNote || '') + '</p>' +
              '<iframe loading="lazy" title="PDF ' + E(x.id) + '" src="' +
              E(href(x.viewer_pdf)) +
              '#view=FitH&toolbar=1&navpanes=1"></iframe>' +
              '<p class="hash">PDF SHA-256 ' +
              E(x.viewer_pdf_sha256 || x.hash || '') +
              '</p></details>'
            : '';

          return '<article class="doc" id="' + E(x.id.toLowerCase()) + '">' +
            '<div class="top"><span class="id">' + E(x.id) +
            '</span><span class="status">' + E(x.status) + '</span></div>' +
            '<h3>' + E(title) + '</h3>' +
            '<p class="meta">' + E(x.date) + ' · ' + E(x.type) + ' · ' +
            E(x.authorship) + ' · ' + E(x.copy_status || '') + '</p>' +
            '<p><strong>' + (lang === 'es' ? 'Acredita:' : 'Establishes:') +
            '</strong> ' + E(establishes) + '</p>' +
            '<p><strong>' + (lang === 'es' ? 'No acredita:' : 'Does not establish:') +
            '</strong> ' + E(doesNot) + '</p>' +
            (defensive
              ? '<p class="def"><strong>' +
                (lang === 'es' ? 'Relevancia defensiva:' : 'Defensive relevance:') +
                '</strong> ' + E(defensive) + '</p>'
              : '') +
            receipt + links + viewer + '</article>';
        }).join('');

        return '<section class="quarter"><h2>' + E(quarter) + '</h2>' + cards + '</section>';
      }).join('');
    })
    .catch((e) => {
      root.innerHTML = '<p>' +
        (lang === 'es'
          ? 'No se pudo cargar el registro documental.'
          : 'The documentary register could not be loaded.') +
        '</p>';
      console.error(e);
    });
})();