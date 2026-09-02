(() => {
  'use strict';
  const currentScript = document.currentScript;
  if (!currentScript) return;
  const path = window.location.pathname;
  const isEs = path.includes('/es/registro-identidad-profesionales-justicia/');
  const isEn = path.includes('/en/justice-professionals-identity-register/');
  if (!isEs && !isEn) return;
  if (document.documentElement.dataset.justiceCurrentOverlay === '20260902c') return;
  document.documentElement.dataset.justiceCurrentOverlay = '20260902c';

  const lang = isEn ? 'en' : 'es';
  const assetBase = new URL('.', currentScript.src);
  const dataUrl = (name) => new URL(`data/${name}`, assetBase).href;
  const siteRoot = new URL('../', assetBase);
  const route = (record) => new URL(String(record.routes?.[lang] || (lang === 'es' ? '/es/registro-identidad-materia/' : '/en/matter-identity-registry/')).replace(/^\//, ''), siteRoot).href;
  const fileName = (pathValue) => String(pathValue || '').split('/').pop();

  const updateText = (authority) => {
    const counts = authority.derived_counts || {};
    const scores = document.querySelectorAll('.jp-score strong');
    [counts.unique_named_people, counts.confirmed, counts.pending, counts.suspended].forEach((value, index) => {
      if (scores[index]) scores[index].textContent = String(value ?? '—');
    });
    const note = document.querySelector('.jp-note');
    if (note) note.innerHTML = lang === 'es'
      ? `<strong>Veredicto actual: PARCIAL — NO TODO ES^.</strong> ${counts.confirmed} de ${counts.unique_named_people} personas fuente-identificadas tienen identidad ^ confirmada. Las ${counts.pending} identidades pendientes permanecen sujetas a fuente primaria suficiente; los huecos de autoridad por procedimiento se conservan expresamente como SOURCE_GAP.`
      : `<strong>Current verdict: PARTIAL — NOT ALL IS^.</strong> ${counts.confirmed} of ${counts.unique_named_people} source-identified people have confirmed ^ identities. The ${counts.pending} pending identities remain subject to sufficient primary-source verification; proceeding-level authority gaps remain explicit as SOURCE_GAP.`;
  };

  const classify = (record) => record.role === 'JUDGE_OR_MAGISTRATE' ? 'judge' : record.role === 'LAJ' ? 'laj' : (/magistrad|judge|presidenta/i.test(`${record.capacity_boundary || ''} ${record.verification_detail || ''}`) ? 'judge' : 'laj');

  Promise.all([
    fetch(dataUrl('justice-authority-register-current-v2.json'), { cache: 'no-store' }).then(r => { if (!r.ok) throw new Error(`authority ${r.status}`); return r.json(); }),
    fetch(dataUrl('proceeding-justice-authority-coverage-20260902.json'), { cache: 'no-store' }).then(r => { if (!r.ok) throw new Error(`coverage ${r.status}`); return r.json(); }),
    fetch(dataUrl('proceeding-page-routes-20260902.json'), { cache: 'no-store' }).then(r => { if (!r.ok) throw new Error(`routes ${r.status}`); return r.json(); })
  ]).then(async ([authority, coverage, routeMap]) => {
    updateText(authority);
    const shardDescriptors = (authority.person_sources || []).filter(d => fileName(d.path) !== 'justice-professionals-caret-audit-v1.json');
    const shards = await Promise.all(shardDescriptors.map(d => fetch(dataUrl(fileName(d.path)), { cache: 'no-store' }).then(r => { if (!r.ok) throw new Error(`${fileName(d.path)} ${r.status}`); return r.json(); })));
    const records = shards.flatMap(doc => doc.records || []);

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

    const roles = authority.derived_counts?.by_role || {};
    append(lang === 'es' ? '#judicatura' : '#judiciary', records.filter(r => classify(r) === 'judge'), lang === 'es' ? `${roles.JUDGE_OR_MAGISTRATE} / ${roles.JUDGE_OR_MAGISTRATE} CONFIRMADOS` : `${roles.JUDGE_OR_MAGISTRATE} / ${roles.JUDGE_OR_MAGISTRATE} CONFIRMED`);
    append('#laj', records.filter(r => classify(r) === 'laj'), lang === 'es' ? `${roles.LAJ} / ${roles.LAJ} CONFIRMADOS` : `${roles.LAJ} / ${roles.LAJ} CONFIRMED`);

    const relatedByPerson = new Map();
    (coverage.records || []).forEach(item => {
      ['judge_or_magistrate', 'laj', 'fiscal'].forEach(key => {
        ((item[key] || {}).person_ids || []).forEach(id => {
          if (!relatedByPerson.has(id)) relatedByPerson.set(id, []);
          relatedByPerson.get(id).push(item.master_id);
        });
      });
    });
    relatedByPerson.forEach((masterIds, personId) => {
      const anchor = document.querySelector(`[data-caepr-id="${personId}"]`);
      if (!anchor || anchor.parentElement?.querySelector(`[data-related-proceedings-for="${personId}"]`)) return;
      const holder = document.createElement('span'); holder.dataset.relatedProceedingsFor = personId; holder.className = 'jp-related-proceedings';
      holder.style.cssText = 'display:inline-flex;gap:.35rem;align-items:center;flex-wrap:wrap;margin-right:.45rem';
      const label = document.createElement('small'); label.textContent = lang === 'es' ? 'Procedimientos:' : 'Proceedings:'; holder.appendChild(label);
      [...new Set(masterIds)].sort().forEach(mid => {
        const rel = routeMap.routes?.[mid]?.[lang]; if (!rel) return;
        const a = document.createElement('a'); a.href = new URL(rel, siteRoot).href; a.textContent = mid; a.title = lang === 'es' ? 'Abrir página del procedimiento' : 'Open proceeding page'; holder.appendChild(a);
      });
      anchor.insertAdjacentElement('afterend', holder);
    });

    const firstContentSection = document.querySelector('main > .section');
    if (firstContentSection && !document.querySelector('[data-current-derived-register-note]')) {
      const counts = authority.derived_counts || {};
      const p = document.createElement('p'); p.setAttribute('data-current-derived-register-note', '20260902c'); p.className = 'jp-note jp-good';
      p.innerHTML = lang === 'es'
        ? `Control actual derivado: <a href="../../assets/data/justice-authority-register-current-v2.json">${counts.unique_named_people} personas</a> · ${counts.confirmed} ^ confirmadas · ${counts.pending} pendientes. La cobertura histórica completa de expedientes oficiales permanece como brecha expresa.`
        : `Current derived control: <a href="../../assets/data/justice-authority-register-current-v2.json">${counts.unique_named_people} people</a> · ${counts.confirmed} ^ confirmed · ${counts.pending} pending. Complete historic official-docket coverage remains an express gap.`;
      firstContentSection.querySelector('.shell')?.appendChild(p);
    }
  }).catch(error => console.error('Justice-professionals current overlay failed', error));
})();
