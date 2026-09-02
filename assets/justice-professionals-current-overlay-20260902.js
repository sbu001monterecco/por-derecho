(() => {
  'use strict';
  const current = document.currentScript;
  if (!current) return;
  const path = window.location.pathname;
  const isEs = path.includes('/es/registro-identidad-profesionales-justicia/');
  const isEn = path.includes('/en/justice-professionals-identity-register/');
  if (!isEs && !isEn) return;
  if (document.documentElement.dataset.justiceCurrentOverlay === '20260902') return;
  document.documentElement.dataset.justiceCurrentOverlay = '20260902';

  const lang = isEn ? 'en' : 'es';
  const dataUrl = new URL('data/matter-identity-registry-v1.la-laguna-judicial-people.json', new URL('.', current.src)).href;
  const siteRoot = new URL('../', new URL('.', current.src));
  const route = (record) => new URL(String(record.routes?.[lang] || (lang === 'es' ? '/es/registro-identidad-materia/' : '/en/matter-identity-registry/')).replace(/^\//, ''), siteRoot).href;

  const updateText = () => {
    const scores = document.querySelectorAll('.jp-score strong');
    [['59', 0], ['56', 1], ['3', 2], ['0', 3]].forEach(([value, index]) => { if (scores[index]) scores[index].textContent = value; });
    const heroEyebrow = document.querySelector('.jp-hero .eyebrow');
    if (heroEyebrow) heroEyebrow.textContent = lang === 'es'
      ? 'CAEPR · CENSO ACTUAL DERIVADO · CORTE 2 SEP 2026'
      : 'CAEPR · CURRENT DERIVED CENSUS · CUT-OFF 2 SEP 2026';
    const note = document.querySelector('.jp-note');
    if (note) note.innerHTML = lang === 'es'
      ? '<strong>Veredicto actual: PARCIAL — NO TODO ES^.</strong> 56 de 59 personas fuente-identificadas tienen identidad ^ confirmada. Las tres identidades pendientes siguen siendo Carmen Martínez Socias, Nicolás Quintana Plasencia y Pedro Eugenio Botella Torres. La ampliación incorpora 11 jueces/LAJ de La Laguna y cooperación judicial posteriores al censo finito de 31-agosto.'
      : '<strong>Current verdict: PARTIAL — NOT ALL IS^.</strong> 56 of 59 source-identified people have confirmed ^ identities. The three pending identities remain Carmen Martínez Socias, Nicolás Quintana Plasencia and Pedro Eugenio Botella Torres. The current derivation adds 11 later La Laguna and judicial-cooperation judges/LAJs to the finite 31-August census.';
  };

  const classify = (record) => /magistrad|judge/i.test(`${record.capacity_boundary || ''} ${record.verification_detail || ''}`) ? 'judge' : 'laj';

  fetch(dataUrl, { cache: 'no-store' })
    .then((response) => {
      if (!response.ok) throw new Error(`justice supplement ${response.status}`);
      return response.json();
    })
    .then((data) => {
      updateText();
      const judges = (data.records || []).filter((record) => classify(record) === 'judge');
      const lajs = (data.records || []).filter((record) => classify(record) === 'laj');
      const append = (sectionSelector, records, countText) => {
        const section = document.querySelector(sectionSelector);
        const list = section?.querySelector('.jp-list');
        if (!section || !list) return;
        records.forEach((record) => {
          if (list.querySelector(`[data-caepr-id="${record.id}"]`)) return;
          const link = document.createElement('a');
          link.className = 'jp-person';
          link.dataset.caeprId = record.id;
          link.dataset.caretState = record.identity_resolution;
          link.href = route(record);
          link.append(document.createTextNode(record.name));
          const sup = document.createElement('sup');
          sup.textContent = '^';
          link.appendChild(sup);
          list.appendChild(link);
        });
        const eyebrow = section.querySelector('.eyebrow');
        if (eyebrow) eyebrow.textContent = countText;
      };
      append(lang === 'es' ? '#judicatura' : '#judiciary', judges, lang === 'es' ? '18 / 18 CONFIRMADOS' : '18 / 18 CONFIRMED');
      append('#laj', lajs, lang === 'es' ? '16 / 16 CONFIRMADOS' : '16 / 16 CONFIRMED');

      const firstContentSection = document.querySelector('main > .section');
      if (firstContentSection && !document.querySelector('[data-current-derived-register-note]')) {
        const paragraph = document.createElement('p');
        paragraph.setAttribute('data-current-derived-register-note', '20260902');
        paragraph.className = 'jp-note jp-good';
        paragraph.innerHTML = lang === 'es'
          ? 'Control actual derivado: <a href="../../assets/data/justice-authority-register-current-v2.json">59 personas</a> · <a href="../registro-judicial-audiencia-provincial-las-palmas/">Audiencia Provincial de Las Palmas^ PD-SP-I-0044</a>. La cobertura histórica completa de expedientes oficiales permanece como brecha expresa.'
          : 'Current derived control: <a href="../../assets/data/justice-authority-register-current-v2.json">59 people</a> · <a href="../las-palmas-provincial-court-register/">Las Palmas Provincial Court^ PD-SP-I-0044</a>. Complete historic official-docket coverage remains an express gap.';
        firstContentSection.querySelector('.shell')?.appendChild(paragraph);
      }
    })
    .catch((error) => console.error('Justice-professionals current overlay failed', error));
})();
