(() => {
  'use strict';
  const current = document.currentScript;
  if (!current) return;
  const path = window.location.pathname;
  const isEs = path.includes('/es/registro-identidad-profesionales-justicia/');
  const isEn = path.includes('/en/justice-professionals-identity-register/');
  if (!isEs && !isEn) return;
  if (document.documentElement.dataset.justiceCurrentOverlay === '20260902b') return;
  document.documentElement.dataset.justiceCurrentOverlay = '20260902b';
  const lang = isEn ? 'en' : 'es';
  const assetBase = new URL('.', current.src);
  const dataUrl = (name) => new URL(`data/${name}`, assetBase).href;
  const siteRoot = new URL('../', assetBase);
  const route = (record) => new URL(String(record.routes?.[lang] || (lang === 'es' ? '/es/registro-identidad-materia/' : '/en/matter-identity-registry/')).replace(/^\//, ''), siteRoot).href;
  const updateText = () => {
    const scores = document.querySelectorAll('.jp-score strong');
    [['61', 0], ['58', 1], ['3', 2], ['0', 3]].forEach(([value, index]) => { if (scores[index]) scores[index].textContent = value; });
    const note = document.querySelector('.jp-note');
    if (note) note.innerHTML = lang === 'es'
      ? '<strong>Veredicto actual: PARCIAL — NO TODO ES^.</strong> 58 de 61 personas fuente-identificadas tienen identidad ^ confirmada. Las tres identidades pendientes siguen siendo Carmen Martínez Socias, Nicolás Quintana Plasencia y Pedro Eugenio Botella Torres. El backfill histórico añade Ángela López-Yuste Padial y Emma Galcerán Solsona desde copias judiciales primarias.'
      : '<strong>Current verdict: PARTIAL — NOT ALL IS^.</strong> 58 of 61 source-identified people have confirmed ^ identities. The three pending identities remain Carmen Martínez Socias, Nicolás Quintana Plasencia and Pedro Eugenio Botella Torres. The historic backfill adds Ángela López-Yuste Padial and Emma Galcerán Solsona from primary judicial copies.';
  };
  const classify = (record) => /magistrad|judge|presidenta/i.test(`${record.capacity_boundary || ''} ${record.verification_detail || ''}`) ? 'judge' : 'laj';
  Promise.all([
    fetch(dataUrl('matter-identity-registry-v1.la-laguna-judicial-people.json'), { cache: 'no-store' }).then(r => { if (!r.ok) throw new Error(`laguna ${r.status}`); return r.json(); }),
    fetch(dataUrl('matter-identity-registry-v1.historic-arrecife-judicial-people-20260902.json'), { cache: 'no-store' }).then(r => { if (!r.ok) throw new Error(`historic ${r.status}`); return r.json(); })
  ]).then(([laguna, historic]) => {
    updateText();
    const records = [...(laguna.records || []), ...(historic.records || [])];
    const append = (sectionSelector, rows, countText) => {
      const section = document.querySelector(sectionSelector); const list = section?.querySelector('.jp-list');
      if (!section || !list) return;
      rows.forEach(record => {
        if (list.querySelector(`[data-caepr-id="${record.id}"]`)) return;
        const link = document.createElement('a'); link.className = 'jp-person'; link.dataset.caeprId = record.id; link.dataset.caretState = record.identity_resolution; link.href = route(record);
        link.append(document.createTextNode(record.name)); const sup = document.createElement('sup'); sup.textContent = '^'; link.appendChild(sup); list.appendChild(link);
      });
      const eyebrow = section.querySelector('.eyebrow'); if (eyebrow) eyebrow.textContent = countText;
    };
    append(lang === 'es' ? '#judicatura' : '#judiciary', records.filter(r => classify(r) === 'judge'), lang === 'es' ? '20 / 20 CONFIRMADOS' : '20 / 20 CONFIRMED');
    append('#laj', records.filter(r => classify(r) === 'laj'), lang === 'es' ? '16 / 16 CONFIRMADOS' : '16 / 16 CONFIRMED');
    const firstContentSection = document.querySelector('main > .section');
    if (firstContentSection && !document.querySelector('[data-current-derived-register-note]')) {
      const p = document.createElement('p'); p.setAttribute('data-current-derived-register-note', '20260902b'); p.className = 'jp-note jp-good';
      p.innerHTML = lang === 'es' ? 'Control actual derivado: <a href="../../assets/data/justice-authority-register-current-v2.json">61 personas</a> · 58 ^ confirmadas · 3 pendientes. La cobertura histórica completa de expedientes oficiales permanece como brecha expresa.' : 'Current derived control: <a href="../../assets/data/justice-authority-register-current-v2.json">61 people</a> · 58 ^ confirmed · 3 pending. Complete historic official-docket coverage remains an express gap.';
      firstContentSection.querySelector('.shell')?.appendChild(p);
    }
  }).catch(error => console.error('Justice-professionals current overlay failed', error));
})();
