(() => {
  'use strict';

  const room = document.querySelector('[data-acta-room]');
  if (!room) return;

  const locale = document.documentElement.lang === 'es' ? 'es' : 'en';
  const manifestUrl = room.dataset.manifest;
  const repoRoot = room.dataset.repoRoot || '../../../';
  const list = room.querySelector('[data-acta-list]');
  const search = room.querySelector('[data-acta-search]');
  const filter = room.querySelector('[data-acta-filter]');
  const resultCount = room.querySelector('[data-acta-count]');
  const stats = {
    total: room.querySelector('[data-stat-total]'),
    complete: room.querySelector('[data-stat-complete]'),
    partial: room.querySelector('[data-stat-partial]'),
    open: room.querySelector('[data-stat-open]')
  };

  const copy = {
    en: {
      status: {
        'located-package-complete-public': 'Complete public-safe package',
        'located-package-digitised-public': 'Located copy digitised and posted',
        'located-package-partial': 'Located · public package partial',
        'referenced-original-not-located': 'Referenced · original not located',
        'no-acta-located': 'No ACTA located',
        'non-acta-event': 'Separate event · not an ACTA'
      },
      body: { owners: 'Owners’ Community', cexp: 'CEXP', event: 'Working event', reference: 'Later recital' },
      availability: { transcript: 'Public-safe text', pdf: 'Text-edition PDF', images: 'Rendered edition pages', facsimile: 'Redacted source facsimile', sourceImages: 'Redacted source-page images', integrity: 'Integrity record', sourcePages: 'Received source', publicPages: 'Public text edition' },
      available: 'Available', pending: 'Pending', pages: n => `${n} page${n === 1 ? '' : 's'}`,
      verificationPending: 'Available · line verification pending',
      actions: { detail: 'Open complete event page', source: 'Source-language transcript', translation: 'English reading', pdf: 'Public text-edition PDF', facsimile: 'Redacted source facsimile', manifest: 'Integrity manifest', provenance: 'Source provenance', redactions: 'Redaction log', previews: 'Show rendered edition pages', sourcePreviews: 'Show redacted source pages', hide: 'Hide pages' },
      perimeter: {
        pre_sale_montelanza: 'Montelanza · pre-sale',
        project_lpb_aweswell_gil: 'Project · Multimatrix/LPB → Aweswell/LPB–Gil',
        adverse_montelanza_molina: 'Alleged adverse · Montelanza/Molina–Pamanil',
        adverse_acosta_matos: 'Alleged adverse · Acosta Matos/CAM',
        mixed_or_contested: 'Mixed or contested',
        unresolved: 'Unresolved'
      },
      attributionBoundary: 'Documentary/editorial lane—not a finding of validity, joint conduct, fraud or guilt.',
      shown: (shown, total) => `${shown} of ${total} records shown`,
      empty: 'No record matches this search and filter.',
      image: (title, page) => `${title}, rendered page ${page} of the public-safe text edition`,
      page: page => `Page ${page}`,
      integrityNote: 'A repository hash identifies a received digital copy; it is not proof of an official certified original or an uninterrupted forensic chain of custody.',
      translationPending: 'A complete source-language text may be available while an English reading remains pending.'
    },
    es: {
      status: {
        'located-package-complete-public': 'Paquete público seguro completo',
        'located-package-digitised-public': 'Copia localizada digitalizada y publicada',
        'located-package-partial': 'Localizada · paquete público parcial',
        'referenced-original-not-located': 'Referenciada · original no localizado',
        'no-acta-located': 'No se localizó ACTA',
        'non-acta-event': 'Evento separado · no es ACTA'
      },
      body: { owners: 'Comunidad de Propietarios', cexp: 'CEXP', event: 'Reunión de trabajo', reference: 'Mención posterior' },
      availability: { transcript: 'Texto público seguro', pdf: 'PDF de edición textual', images: 'Páginas de la edición textual', facsimile: 'Facsímil fuente expurgado', sourceImages: 'Imágenes fuente expurgadas', integrity: 'Registro de integridad', sourcePages: 'Fuente recibida', publicPages: 'Edición textual pública' },
      available: 'Disponible', pending: 'Pendiente', pages: n => `${n} página${n === 1 ? '' : 's'}`,
      verificationPending: 'Disponible · cotejo línea por línea pendiente',
      actions: { detail: 'Abrir página completa del evento', source: 'Transcripción en lengua fuente', translation: 'Lectura en inglés', pdf: 'PDF de edición textual pública', facsimile: 'Facsímil fuente expurgado', manifest: 'Manifiesto de integridad', provenance: 'Procedencia de fuente', redactions: 'Registro de expurgación', previews: 'Mostrar páginas de la edición textual', sourcePreviews: 'Mostrar páginas fuente expurgadas', hide: 'Ocultar páginas' },
      perimeter: {
        pre_sale_montelanza: 'Montelanza · pre-venta',
        project_lpb_aweswell_gil: 'Proyecto · Multimatrix/LPB → Aweswell/LPB–Gil',
        adverse_montelanza_molina: 'Adverso alegado · Montelanza/Molina–Pamanil',
        adverse_acosta_matos: 'Adverso alegado · Acosta Matos/CAM',
        mixed_or_contested: 'Mixto o controvertido',
        unresolved: 'No resuelto'
      },
      attributionBoundary: 'Carril documental/editorial; no es hallazgo de validez, actuación conjunta, fraude o culpabilidad.',
      shown: (shown, total) => `${shown} de ${total} registros visibles`,
      empty: 'Ningún registro coincide con la búsqueda y el filtro.',
      image: (title, page) => `${title}, página ${page} de la edición textual pública segura`,
      page: page => `Página ${page}`,
      integrityNote: 'Un hash del repositorio identifica una copia digital recibida; no acredita un original oficial certificado ni una cadena de custodia forense ininterrumpida.',
      translationPending: 'Puede estar disponible el texto íntegro en lengua fuente mientras queda pendiente la lectura en inglés.'
    }
  }[locale];

  const fallbackEvents = [
    ['SP-ACTA-2008-04-29', '2008-04-29', 'owners', 'located-package-partial', '29 April 2008', '29 abril 2008',
      'Located five-page Community source. Public extraction and source-variant reconciliation remain open.',
      'Fuente comunitaria de cinco páginas localizada. Siguen pendientes la extracción pública y la conciliación de variantes.'],
    ['SP-ACTA-2008-07-15', '2008-07-15', 'owners', 'located-package-partial', '15 July 2008', '15 julio 2008',
      'Located Community source; public-safe transcription, page images and annex reconciliation remain open.',
      'Fuente comunitaria localizada; siguen pendientes la transcripción pública segura, imágenes y conciliación de anexos.'],
    ['SP-ACTA-2008-07-25', '2008-07-25', 'owners', 'located-package-partial', '25 July 2008', '25 julio 2008',
      'Located four-page Gmail source family. Full locator/hash, authentication and public-package controls remain open.',
      'Familia fuente de cuatro páginas localizada en Gmail. Siguen abiertos el localizador/hash íntegro, autenticación y controles del paquete público.'],
    ['SP-ACTA-2008-12-17', '2008-12-17', 'owners', 'located-package-partial', '17 December 2008', '17 diciembre 2008',
      'Located ten-page ACTA source. Authentication, source-family reconciliation and the complete public-safe package remain open.',
      'Fuente ACTA de diez páginas localizada. Siguen abiertas autenticación, conciliación de familia fuente y paquete público seguro íntegro.'],
    ['SP-ACTA-2009-05-28', '2009-05-28', 'owners', 'located-package-partial', '28 May 2009', '28 mayo 2009',
      'Located Community source; a complete public-safe package has not yet passed the publication gate.',
      'Fuente comunitaria localizada; el paquete público seguro íntegro aún no ha superado el control de publicación.'],
    ['SP-ACTA-2011-02-02', '2011-02-02', 'owners', 'located-package-partial', '2 February 2011', '2 febrero 2011',
      'Located threshold minutes concerning Community offices and the stated boundary with hotel operation.',
      'Acta umbral localizada sobre cargos comunitarios y el límite consignado respecto de la explotación hotelera.'],
    ['SP-ACTA-2011-06-22', '2011-06-22', 'owners', 'located-package-partial', '22 June 2011', '22 junio 2011',
      'Located 16-page source. The earlier public material is a structured redacted digest, not a complete line-by-line transcription; byte variants and the full publication package remain under reconciliation.',
      'Fuente de 16 páginas localizada. El material público anterior es una síntesis estructurada y expurgada, no una transcripción íntegra línea por línea; siguen conciliándose variantes y el paquete completo.'],
    ['SP-ACTA-2012-08-10', '2012-08-10', 'reference', 'located-package-partial', '10 August 2012 · located ACTA copy', '10 agosto 2012 · copia ACTA localizada',
      'A four-page native DOCX ACTA and a related five-page PDF family are now located. The ACTA records that no resolution was put to a vote. Its referenced president statement and objection annexes remain unlocated.',
      'Se han localizado un ACTA DOCX nativa de cuatro páginas y una familia PDF relacionada de cinco páginas. El ACTA consigna que no se sometió acuerdo a votación. Siguen sin localizarse sus anexos referenciados de declaración y objeción de presidencia.'],
    ['SP-ACTA-2014-04-10', '2014-04-10', 'owners', 'located-package-partial', '10 April 2014', '10 abril 2014',
      'Contested notarial Community record; public-safe image/text package and later procedural reconciliation remain open.',
      'Registro notarial comunitario controvertido; quedan abiertos el paquete público seguro y la conciliación procesal posterior.'],
    ['SP-ACTA-2014-08-28-CP', '2014-08-28', 'owners', 'located-package-partial', '28 August 2014 · Owners’ Community', '28 agosto 2014 · Comunidad de Propietarios',
      'Located Community record. It must remain separate from the CEXP record of the same date.',
      'Registro comunitario localizado. Debe permanecer separado del acta CEXP de la misma fecha.'],
    ['SP-ACTA-2014-08-28-CEXP', '2014-08-28', 'cexp', 'located-package-partial', '28 August 2014 · CEXP', '28 agosto 2014 · CEXP',
      'Located signed CEXP record. It is not Owners’ Community minutes and does not by itself prove effective operation or possession.',
      'Acta CEXP firmada localizada. No es acta de la Comunidad ni prueba por sí sola explotación o posesión efectiva.'],
    ['SP-ACTA-2015-11-19', '2015-11-19', 'owners', 'located-package-partial', '19 November 2015', '19 noviembre 2015',
      'Located 38-page source family. Two named variants remain unresolved; any public edition must preserve that qualification.',
      'Familia fuente de 38 páginas localizada. Persisten dos variantes nominales sin conciliar; la edición pública debe reflejarlo.'],
    ['SP-ACTA-2016-04-26', '2016-04-26', 'owners', 'located-package-partial', '26 April 2016', '26 abril 2016',
      'The controlling 77-page family is digitised. Two distinct 77-page binaries are render- and text-equivalent; 24-, 47- and 50-page packages remain separately identified as partial variants.',
      'La familia de control de 77 páginas está digitalizada. Dos binarios distintos de 77 páginas son equivalentes en renderizado y texto; los paquetes de 24, 47 y 50 páginas permanecen identificados por separado como variantes parciales.'],
    ['SP-MEETING-2016-06-11', '2016-06-11', 'event', 'non-acta-event', '11 June 2016 · Las Palmas working meeting', '11 junio 2016 · reunión de trabajo en Las Palmas',
      'Recorded working meeting. It is not an Owners’ Community or CEXP ACTA and must not be inserted into either minutes book.',
      'Reunión de trabajo grabada. No es ACTA de la Comunidad ni de CEXP y no debe incorporarse a ninguno de esos libros.'],
    ['SP-ACTA-2017-04-07-CEXP', '2017-04-07', 'cexp', 'located-package-partial', '7 April 2017 · CEXP', '7 abril 2017 · CEXP',
      'Located signed CEXP governance record; public-safe package completion remains open.',
      'Registro firmado de gobernanza CEXP localizado; queda pendiente completar el paquete público seguro.'],
    ['SP-ACTA-2017-06-12', '2017-06-12', 'owners', 'located-package-partial', '12 June 2017 · Owners’ Community', '12 junio 2017 · Comunidad de Propietarios',
      'Located Community minutes. Final annex, audio and later-email reconciliation remain open.',
      'Acta comunitaria localizada. Queda por conciliar anexos, audio y un correo profesional posterior.'],
    ['SP-ACTA-2018-05-18', '2018-05-18', 'owners', 'located-package-partial', '18 May 2018', '18 mayo 2018',
      'The located copy reports 86.715% represented and presents 0.385% as vote-qualified. The 0.385% remains a source-recorded figure, not independently verified ownership arithmetic; titles, proxies and denominator still require finca-by-finca reconciliation.',
      'La copia localizada consigna 86,715% representado y presenta 0,385% con voto. El 0,385% sigue siendo una cifra del documento, no aritmética dominical verificada de forma independiente; faltan títulos, poderes y denominador finca por finca.'],
    ['SP-ACTA-2018-07-05', '2018-07-05', 'owners', 'located-package-partial', '5 July 2018', '5 julio 2018',
      'The located nine-page control copy is digitised and posted. A distinct binary variant is visually equivalent; manual line certification, annexes and any audio remain open.',
      'La copia de control localizada de nueve páginas está digitalizada y publicada. Una variante binaria distinta es visualmente equivalente; siguen abiertos la certificación manual línea por línea, anexos y eventual audio.'],
    ['SP-RECITAL-2018-11-20', '2018-11-20', 'reference', 'referenced-original-not-located', '20 November 2018 · later recital', '20 noviembre 2018 · mención posterior',
      'The 2022 minutes refer to this meeting. That later recital does not substitute for the unlocated original minutes.',
      'El acta de 2022 menciona esta junta. Esa referencia posterior no sustituye el original no localizado.'],
    ['SP-ACTA-2022-02-04', '2022-02-04', 'owners', 'located-package-partial', '4 February 2022', '4 febrero 2022',
      'A seven-page source is located as one of two known variants. The relationship between variants and the annexed project figures remains unresolved.',
      'Se localizó una fuente de siete páginas como una de dos variantes conocidas. Sigue sin resolverse su relación y las cifras del proyecto anexo.']
  ].map(row => ({
    id: row[0], date: row[1], body: row[2], status: row[3],
    title_en: row[4], title_es: row[5], notes_en: row[6], notes_es: row[7],
    complete_public_text: false, preview_pages: []
  }));

  const allowedStates = new Set([
    'located-package-complete-public', 'located-package-digitised-public', 'located-package-partial',
    'referenced-original-not-located', 'no-acta-located', 'non-acta-event'
  ]);

  function normaliseBody(value, fallback = 'owners') {
    if (['owners', 'cexp', 'event', 'reference'].includes(value)) return value;
    const source = String(value || '').toLowerCase();
    if (source.includes('working') || source.includes('trabajo')) return 'event';
    if (source.includes('recital') || source.includes('mención') || source.includes('refer')) return 'reference';
    if (source.includes('cexp') && !source.includes('propietarios')) return 'cexp';
    return fallback;
  }

  function normaliseIndexEvent(incoming, base = {}) {
    const limitations = incoming.limitations || {};
    const publicArtifacts = incoming.public_artifacts || {};
    const previewCount = Number(incoming.preview_count || incoming.pdf_pages || publicArtifacts.preview_count || publicArtifacts.pdf_pages);
    let previews = incoming.preview_pages || publicArtifacts.preview_pages || [];
    if ((!Array.isArray(previews) || !previews.length) && incoming.preview_dir && Number.isInteger(previewCount) && previewCount > 0) {
      previews = Array.from({ length: previewCount }, (_, index) => `${String(incoming.preview_dir).replace(/\/$/, '')}/page-${String(index + 1).padStart(3, '0')}.webp`);
    }
    return {
      ...base,
      ...incoming,
      body: normaliseBody(incoming.body, base.body),
      title_en: incoming.title_en || base.title_en,
      title_es: incoming.title_es || base.title_es,
      notes_en: incoming.notes_en || limitations.en || incoming.source_variant_note_en || incoming.source_variant_note || base.notes_en,
      notes_es: incoming.notes_es || limitations.es || incoming.source_variant_note_es || incoming.source_variant_note || base.notes_es,
      transcript_source: incoming.transcript_source || incoming.transcript_path || publicArtifacts.transcript_es || base.transcript_source,
      transcript_es: incoming.transcript_es || incoming.transcript_path || publicArtifacts.transcript_es || base.transcript_es,
      transcript_en: incoming.transcript_en || base.transcript_en,
      public_pdf: incoming.public_pdf || incoming.public_pdf_path || publicArtifacts.pdf || base.public_pdf,
      redacted_source_facsimile: incoming.redacted_source_facsimile || publicArtifacts.redacted_source_facsimile || base.redacted_source_facsimile,
      manifest: incoming.manifest || incoming.manifest_path || base.manifest,
      provenance: incoming.provenance || incoming.provenance_path || publicArtifacts.provenance || base.provenance,
      redaction_log: incoming.redaction_log || incoming.redaction_log_path || publicArtifacts.redaction_log || base.redaction_log,
      source_page_count: incoming.source_variant_page_count || incoming.source_pages || incoming.source_page_count || incoming.page_count || base.source_page_count,
      page_count: previewCount || incoming.page_count || base.page_count,
      preview_pages: Array.isArray(previews) ? previews : [],
      source_preview_pages: Array.isArray(incoming.source_preview_pages || publicArtifacts.source_preview_pages) ? (incoming.source_preview_pages || publicArtifacts.source_preview_pages) : [],
      source_sha256: incoming.source_sha256 || incoming.source_hash_sha256 || (incoming.source && incoming.source.sha256) || base.source_sha256,
      detail_page_es: incoming.detail_page_es || base.detail_page_es,
      detail_page_en: incoming.detail_page_en || base.detail_page_en,
      perimeter: incoming.perimeter || base.perimeter || 'unresolved',
      attribution_status: incoming.attribution_status || base.attribution_status,
      phase_es: incoming.phase_es || base.phase_es,
      phase_en: incoming.phase_en || base.phase_en,
      complete_public_text: incoming.complete_public_text === true,
      status: allowedStates.has(incoming.status) ? incoming.status : (base.status || 'located-package-partial')
    };
  }

  const safeUrl = value => {
    if (typeof value !== 'string' || !value.trim()) return null;
    const url = value.trim();
    if (/^(https:\/\/|mailto:)/i.test(url)) return url;
    if (/^[a-z][a-z0-9+.-]*:/i.test(url)) return null;
    return repoRoot + url.replace(/^(\.\/|\/)+/, '');
  };

  const textFor = (event, key) => event[`${key}_${locale}`] || event[key] || event[`${key}_es`] || event[`${key}_en`] || '';
  const previewList = event => Array.isArray(event.preview_pages) ? event.preview_pages.filter(page => typeof page === 'string' || (page && typeof page.url === 'string')) : [];
  const sourcePreviewList = event => Array.isArray(event.source_preview_pages) ? event.source_preview_pages.filter(page => typeof page === 'string' || (page && typeof page.url === 'string')) : [];

  function gatedState(event) {
    const requested = allowedStates.has(event.status) ? event.status : 'located-package-partial';
    if (requested === 'located-package-digitised-public') {
      const sourcePreviews = sourcePreviewList(event);
      const sourcePageCount = Number(event.source_page_count || event.source_variant_page_count);
      const coherentSourcePages = Number.isInteger(sourcePageCount) && sourcePageCount > 0 && sourcePreviews.length === sourcePageCount;
      const digitised = event.digitisation_complete_for_located_copy === true && Boolean(event.transcript_source || event.transcript_es || event.transcript);
      const facsimile = event.redacted_facsimile_available === true && Boolean(safeUrl(event.redacted_source_facsimile));
      return digitised && facsimile && event.source_page_images_available === true && coherentSourcePages ? requested : 'located-package-partial';
    }
    if (requested !== 'located-package-complete-public') return requested;
    const previews = previewList(event);
    const pageCount = Number(event.page_count);
    const coherentPreviews = Number.isInteger(pageCount) && pageCount > 0 && previews.length === pageCount;
    const hasText = event.complete_public_text === true && event.manual_source_line_verification === true && Boolean(event.transcript_source || event.transcript_es || event.transcript);
    const hasPdf = Boolean(safeUrl(event.public_pdf));
    const hasSourceFacsimile = event.redacted_facsimile_available === true && event.source_page_images_available === true;
    return hasText && hasPdf && coherentPreviews && hasSourceFacsimile ? requested : 'located-package-partial';
  }

  function statusClass(state) {
    if (state === 'located-package-complete-public') return 'complete';
    if (state === 'located-package-digitised-public') return 'complete';
    if (state === 'located-package-partial') return 'partial';
    if (state === 'non-acta-event') return 'event';
    return 'missing';
  }

  function element(tag, className, value) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (value !== undefined) node.textContent = value;
    return node;
  }

  function actionLink(label, href, secondary = false) {
    const link = element('a', secondary ? 'secondary' : '', label);
    link.href = href;
    if (/^https:\/\//.test(href)) link.rel = 'noopener';
    return link;
  }

  function availabilityRow(label, value) {
    const row = element('div');
    row.append(element('span', '', label), element('strong', '', value));
    return row;
  }

  function renderRecord(event) {
    const state = gatedState(event);
    const article = element('article', 'acta-record');
    article.dataset.state = state;
    article.dataset.body = event.body || 'owners';
    article.dataset.perimeter = event.perimeter || 'unresolved';
    article.dataset.search = [event.id, event.date, textFor(event, 'title'), textFor(event, 'notes'), textFor(event, 'phase'), copy.body[event.body], copy.perimeter[event.perimeter]].join(' ').toLowerCase();

    const head = element('header', 'acta-record-head');
    const heading = element('div');
    const meta = element('div', 'acta-record-meta');
    meta.append(element('span', 'acta-record-id', event.id || '—'));
    meta.append(element('span', '', copy.body[event.body] || copy.body.owners));
    if (event.date) meta.append(element('time', '', event.date));
    heading.append(meta, element('h2', '', textFor(event, 'title') || event.id));
    head.append(heading, element('span', `acta-status ${statusClass(state)}`, copy.status[state]));

    const body = element('div', 'acta-record-body');
    const narrative = element('div');
    const perimeter = element('div', 'acta-perimeter-ribbon');
    perimeter.dataset.perimeter = event.perimeter || 'unresolved';
    perimeter.append(
      element('strong', '', copy.perimeter[event.perimeter] || copy.perimeter.unresolved),
      element('span', '', textFor(event, 'phase') || copy.attributionBoundary)
    );
    narrative.append(perimeter);
    narrative.append(element('p', 'acta-record-summary', textFor(event, 'notes')));

    const detailPage = safeUrl(locale === 'es' ? event.detail_page_es : event.detail_page_en);
    const sourceTranscript = safeUrl(event.transcript_source || event.transcript_es || event.transcript);
    const translation = safeUrl(event.transcript_en);
    const publicPdf = safeUrl(event.public_pdf);
    const sourceFacsimile = safeUrl(event.redacted_source_facsimile);
    const manifest = safeUrl(event.manifest);
    const provenance = safeUrl(event.provenance);
    const redactionLog = safeUrl(event.redaction_log);
    const previews = previewList(event);
    const sourcePreviews = sourcePreviewList(event);
    const pageCount = Number(event.page_count);
    const actions = element('div', 'acta-room-actions');
    if (detailPage) actions.append(actionLink(copy.actions.detail, detailPage));
    if (sourceTranscript) actions.append(actionLink(copy.actions.source, sourceTranscript));
    if (locale === 'en' && translation && translation !== sourceTranscript) actions.append(actionLink(copy.actions.translation, translation, true));
    if (publicPdf) actions.append(actionLink(copy.actions.pdf, publicPdf, true));
    if (sourceFacsimile) actions.append(actionLink(copy.actions.facsimile, sourceFacsimile, true));
    if (manifest) actions.append(actionLink(copy.actions.manifest, manifest, true));
    if (provenance) actions.append(actionLink(copy.actions.provenance, provenance, true));
    if (redactionLog) actions.append(actionLink(copy.actions.redactions, redactionLog, true));
    if (actions.childElementCount) narrative.append(actions);
    if (event.complete_public_text === true && locale === 'en' && !translation) narrative.append(element('p', 'acta-record-note', copy.translationPending));

    const availability = element('aside', 'acta-record-availability');
    const transcriptStatus = sourceTranscript ? (event.manual_source_line_verification === false ? copy.verificationPending : copy.available) : copy.pending;
    availability.append(
      availabilityRow(copy.availability.transcript, transcriptStatus),
      availabilityRow(copy.availability.pdf, publicPdf ? copy.available : copy.pending),
      availabilityRow(copy.availability.images, previews.length ? copy.pages(previews.length) : copy.pending),
      availabilityRow(copy.availability.facsimile, sourceFacsimile ? copy.available : copy.pending),
      availabilityRow(copy.availability.sourceImages, sourcePreviews.length ? copy.pages(sourcePreviews.length) : copy.pending),
      availabilityRow(copy.availability.integrity, manifest || event.source_sha256 ? copy.available : copy.pending)
    );
    const sourcePageCount = Number(event.source_page_count);
    if (Number.isInteger(sourcePageCount) && sourcePageCount > 0) availability.append(availabilityRow(copy.availability.sourcePages, copy.pages(sourcePageCount)));
    if (Number.isInteger(pageCount) && pageCount > 0) availability.append(availabilityRow(copy.availability.publicPages, copy.pages(pageCount)));
    if (Number.isInteger(pageCount) && pageCount > 0 && previews.length && previews.length !== pageCount) {
      availability.append(availabilityRow(locale === 'es' ? 'Control de páginas' : 'Page control', `${previews.length}/${pageCount}`));
    }
    body.append(narrative, availability);
    article.append(head, body);

    if (previews.length) {
      const previewWrap = element('div', 'acta-preview-wrap');
      const toggle = element('button', 'acta-room-toggle', copy.actions.previews);
      toggle.type = 'button';
      toggle.setAttribute('aria-expanded', 'false');
      const grid = element('div', 'acta-preview-grid');
      grid.hidden = true;
      const gridId = `previews-${String(event.id).toLowerCase().replace(/[^a-z0-9-]/g, '-')}`;
      grid.id = gridId;
      toggle.setAttribute('aria-controls', gridId);
      previews.forEach((item, index) => {
        const rawUrl = typeof item === 'string' ? item : item.url;
        const href = safeUrl(rawUrl);
        if (!href) return;
        const page = typeof item === 'object' && item.page ? item.page : index + 1;
        const link = element('a', 'acta-preview');
        link.href = href;
        const image = document.createElement('img');
        image.loading = 'lazy';
        image.decoding = 'async';
        image.alt = copy.image(textFor(event, 'title') || event.id, page);
        image.src = href;
        link.append(image, element('span', '', copy.page(page)));
        grid.append(link);
      });
      toggle.addEventListener('click', () => {
        const expanded = toggle.getAttribute('aria-expanded') === 'true';
        toggle.setAttribute('aria-expanded', String(!expanded));
        toggle.textContent = expanded ? copy.actions.previews : copy.actions.hide;
        grid.hidden = expanded;
      });
      previewWrap.append(toggle, grid);
      article.append(previewWrap);
    }
    if (sourcePreviews.length) {
      const previewWrap = element('div', 'acta-preview-wrap');
      const toggle = element('button', 'acta-room-toggle', copy.actions.sourcePreviews);
      toggle.type = 'button';
      toggle.setAttribute('aria-expanded', 'false');
      const grid = element('div', 'acta-preview-grid');
      grid.hidden = true;
      const gridId = `source-previews-${String(event.id).toLowerCase().replace(/[^a-z0-9-]/g, '-')}`;
      grid.id = gridId;
      toggle.setAttribute('aria-controls', gridId);
      sourcePreviews.forEach((item, index) => {
        const rawUrl = typeof item === 'string' ? item : item.url;
        const href = safeUrl(rawUrl);
        if (!href) return;
        const page = typeof item === 'object' && item.page ? item.page : index + 1;
        const link = element('a', 'acta-preview');
        link.href = href;
        const image = document.createElement('img');
        image.loading = 'lazy';
        image.decoding = 'async';
        image.alt = `${textFor(event, 'title') || event.id}, ${copy.availability.sourceImages}, ${copy.page(page)}`;
        image.src = href;
        link.append(image, element('span', '', copy.page(page)));
        grid.append(link);
      });
      toggle.addEventListener('click', () => {
        const expanded = toggle.getAttribute('aria-expanded') === 'true';
        toggle.setAttribute('aria-expanded', String(!expanded));
        toggle.textContent = expanded ? copy.actions.sourcePreviews : copy.actions.hide;
        grid.hidden = expanded;
      });
      previewWrap.append(toggle, grid);
      article.append(previewWrap);
    }
    return article;
  }

  let events = fallbackEvents;

  function render() {
    const needle = search.value.trim().toLowerCase();
    const selected = filter.value;
    const visible = events.filter(event => {
      const state = gatedState(event);
      const haystack = [event.id, event.date, textFor(event, 'title'), textFor(event, 'notes'), textFor(event, 'phase'), copy.body[event.body], copy.perimeter[event.perimeter]].join(' ').toLowerCase();
      const matchesText = !needle || haystack.includes(needle);
      let matchesFilter = selected === 'all';
      if (selected === 'owners' || selected === 'cexp' || selected === 'event' || selected === 'reference') matchesFilter = event.body === selected;
      if (selected.startsWith('perimeter:')) matchesFilter = event.perimeter === selected.slice('perimeter:'.length);
      if (selected === 'complete') matchesFilter = state === 'located-package-complete-public' || state === 'located-package-digitised-public';
      if (selected === 'open') matchesFilter = state !== 'located-package-complete-public' && state !== 'located-package-digitised-public';
      return matchesText && matchesFilter;
    });

    list.replaceChildren();
    if (!visible.length) list.append(element('p', 'acta-room-empty', copy.empty));
    else visible.forEach(event => list.append(renderRecord(event)));
    resultCount.textContent = copy.shown(visible.length, events.length);

    const states = events.map(gatedState);
    stats.total.textContent = String(events.length);
    stats.complete.textContent = String(states.filter(state => state === 'located-package-complete-public' || state === 'located-package-digitised-public').length);
    stats.partial.textContent = String(states.filter(state => state === 'located-package-partial').length);
    stats.open.textContent = String(states.filter(state => state !== 'located-package-complete-public' && state !== 'located-package-digitised-public').length);
  }

  search.addEventListener('input', render);
  filter.addEventListener('change', render);
  const initialQuery = new URLSearchParams(window.location.search).get('q');
  if (initialQuery) search.value = initialQuery;
  render();

  if (manifestUrl) {
    fetch(manifestUrl, { cache: 'no-store' })
      .then(response => {
        if (!response.ok) throw new Error(`manifest ${response.status}`);
        return response.json();
      })
      .then(data => {
        const supplied = Array.isArray(data) ? data : (data.events || data.items);
        if (!Array.isArray(supplied) || !supplied.length) throw new Error('empty manifest');
        const suppliedById = new Map(supplied.filter(event => event && event.id).map(event => [event.id, event]));
        const merged = fallbackEvents.map(base => {
          const incoming = suppliedById.get(base.id);
          if (!incoming) return base;
          suppliedById.delete(base.id);
          return normaliseIndexEvent(incoming, base);
        });
        suppliedById.forEach(incoming => merged.push(normaliseIndexEvent(incoming)));
        events = merged.map(event => ({ ...event, status: gatedState(event) }));
        render();
      })
      .catch(() => {
        room.dataset.manifestState = 'fallback';
      });
  }
})();
