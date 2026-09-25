(() => {
  'use strict';

  const current = document.currentScript;
  if (!current || !document.body) return;

  const root = new URL('../', current.src);
  const normalizedPath = window.location.pathname.replace(/\/+$/, '/') || '/';
  const rootPath = root.pathname.replace(/\/+$/, '/');
  const relativePath = normalizedPath.startsWith(rootPath)
    ? normalizedPath.slice(rootPath.length)
    : normalizedPath.replace(/^\/+/, '');

  const routeConfig = {
    'en/uria-menendez-sun-park/': { lang: 'en' },
    'es/uria-menendez-sun-park/': { lang: 'es' },
    'en/puzzle/': { lang: 'en' },
    'es/puzzle/': { lang: 'es' },
    'es/uria-menendez/': { lang: 'es' },
    'es/haya-cerberus/': { lang: 'es' }
  };

  const bodyRegistry = document.body.getAttribute('data-evidence-visibility-registry');
  const configured = routeConfig[relativePath];
  if (!configured && !bodyRegistry) return;

  const lang = (configured && configured.lang) || document.documentElement.lang || 'en';
  const registryPath = bodyRegistry || 'data/evidence-visibility/uria-ricpe-sun-park-20260904.json';
  const registryUrl = new URL(registryPath, root);

  const copy = {
    en: {
      eyebrow: 'Evidence visibility · native source + searchable text + source images',
      title: 'See the evidence, not only the summary',
      intro: 'Every registered item declares the state of its original source, searchable text, evidence images and redaction review. Pending images are shown as an explicit evidence gap—never replaced by a synthetic reconstruction.',
      original: 'Original',
      text: 'Searchable text',
      visual: 'Evidence images',
      redaction: 'Redaction',
      pending: 'Evidence image pending native source materialisation. No synthetic substitute is shown.',
      openText: 'Open searchable text',
      openStandard: 'Read the evidence-visibility standard',
      registered: 'Registered evidence package',
      unavailable: 'Evidence-visibility register could not be loaded.',
      gaps: 'Open visual/source action',
      partial: 'This package is not yet visually complete.'
    },
    es: {
      eyebrow: 'Visibilidad de la prueba · fuente nativa + texto buscable + imágenes',
      title: 'Ver la prueba, no sólo el resumen',
      intro: 'Cada elemento registrado declara el estado de la fuente original, el texto buscable, las imágenes probatorias y la revisión de redacción. Las imágenes pendientes se muestran como una laguna expresa: nunca se sustituyen por una reconstrucción sintética.',
      original: 'Original',
      text: 'Texto buscable',
      visual: 'Imágenes de prueba',
      redaction: 'Redacción',
      pending: 'Imagen de prueba pendiente de materialización de la fuente nativa. No se muestra ningún sustituto sintético.',
      openText: 'Abrir texto buscable',
      openStandard: 'Leer el estándar de visibilidad de la prueba',
      registered: 'Paquete de prueba registrado',
      unavailable: 'No se pudo cargar el registro de visibilidad de la prueba.',
      gaps: 'Acción visual/de fuente abierta',
      partial: 'Este paquete todavía no está visualmente completo.'
    }
  };
  const t = lang.toLowerCase().startsWith('es') ? copy.es : copy.en;

  const addStyles = () => {
    if (document.getElementById('pd-evidence-visibility-styles')) return;
    const style = document.createElement('style');
    style.id = 'pd-evidence-visibility-styles';
    style.textContent = `
      .pd-evis{padding:3.5rem 0;background:linear-gradient(180deg,rgba(20,88,72,.035),rgba(20,88,72,.08));border-top:1px solid rgba(90,90,90,.22)}
      .pd-evis__inner{width:min(1180px,calc(100% - 2rem));margin:0 auto}
      .pd-evis__eyebrow{font-size:.78rem;letter-spacing:.09em;text-transform:uppercase;font-weight:800;opacity:.72}
      .pd-evis__lead{max-width:80ch;font-size:1.08rem;line-height:1.65}
      .pd-evis__notice{margin:1.25rem 0;padding:.9rem 1rem;border-left:5px solid #a46a00;background:rgba(164,106,0,.08);max-width:86ch}
      .pd-evis__grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:1rem;margin-top:1.4rem}
      .pd-evis__card{border:1px solid rgba(90,90,90,.28);border-radius:15px;padding:1rem;background:var(--surface,#fff);box-shadow:0 7px 22px rgba(0,0,0,.045)}
      .pd-evis__card h3{font-size:1.02rem;margin:.2rem 0 .75rem}
      .pd-evis__meta{display:grid;grid-template-columns:auto 1fr;gap:.34rem .65rem;font-size:.84rem;margin:0 0 .85rem}
      .pd-evis__meta dt{font-weight:800}
      .pd-evis__meta dd{margin:0;overflow-wrap:anywhere}
      .pd-evis__badge{display:inline-block;border:1px solid currentColor;border-radius:999px;padding:.16rem .5rem;font-weight:800;font-size:.72rem;letter-spacing:.02em}
      .pd-evis__visual-pending{min-height:118px;display:grid;place-items:center;text-align:center;padding:1rem;border:2px dashed rgba(128,92,24,.52);border-radius:12px;background:rgba(164,106,0,.055);font-size:.88rem;line-height:1.45}
      .pd-evis__figures{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:.65rem}
      .pd-evis__figure{margin:0}
      .pd-evis__figure img{display:block;width:100%;height:auto;border:1px solid rgba(90,90,90,.25);border-radius:8px}
      .pd-evis__figure figcaption{font-size:.72rem;margin-top:.3rem}
      .pd-evis__links{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.85rem}
      .pd-evis__links a{display:inline-flex;align-items:center;min-height:38px;padding:.45rem .68rem;border:1px solid currentColor;border-radius:9px;text-decoration:none;font-weight:750;font-size:.82rem}
      .pd-evis__gap{margin:.8rem 0 0;font-size:.8rem;line-height:1.45;opacity:.86}
      @media (max-width:560px){.pd-evis{padding:2.4rem 0}.pd-evis__inner{width:min(100% - 1.1rem,1180px)}}
    `;
    document.head.appendChild(style);
  };

  const statusText = (value) => String(value || 'UNREGISTERED').replaceAll('_', ' ');

  const buildAssetLink = (asset) => {
    const a = document.createElement('a');
    a.href = new URL(asset.path, root).href;
    a.textContent = t.openText;
    if (asset.kind) a.setAttribute('data-asset-kind', asset.kind);
    return a;
  };

  const buildCard = (record) => {
    const card = document.createElement('article');
    card.className = 'pd-evis__card';
    card.id = `evidence-visibility-${record.evidence_id.toLowerCase()}`;

    const heading = document.createElement('h3');
    heading.textContent = record.title;
    card.appendChild(heading);

    const meta = document.createElement('dl');
    meta.className = 'pd-evis__meta';
    const rows = [
      [t.original, record.original_asset && record.original_asset.status],
      [t.text, record.searchable_text && record.searchable_text.status],
      [t.visual, record.visual_evidence && record.visual_evidence.status],
      [t.redaction, record.redaction && record.redaction.status]
    ];
    rows.forEach(([label, value]) => {
      const dt = document.createElement('dt');
      dt.textContent = label;
      const dd = document.createElement('dd');
      const badge = document.createElement('span');
      badge.className = 'pd-evis__badge';
      badge.textContent = statusText(value);
      dd.appendChild(badge);
      meta.append(dt, dd);
    });
    card.appendChild(meta);

    const visual = record.visual_evidence || {};
    const images = Array.isArray(visual.images) ? visual.images : [];
    if (images.length) {
      const figures = document.createElement('div');
      figures.className = 'pd-evis__figures';
      images.forEach((image) => {
        const figure = document.createElement('figure');
        figure.className = 'pd-evis__figure';
        const link = document.createElement('a');
        link.href = new URL(image.path, root).href;
        const img = document.createElement('img');
        img.loading = 'lazy';
        img.decoding = 'async';
        img.src = link.href;
        img.alt = image.caption || `${record.title}, page ${image.page || ''}`.trim();
        link.appendChild(img);
        figure.appendChild(link);
        if (image.caption) {
          const caption = document.createElement('figcaption');
          caption.textContent = image.caption;
          figure.appendChild(caption);
        }
        figures.appendChild(figure);
      });
      card.appendChild(figures);
    } else {
      const pending = document.createElement('div');
      pending.className = 'pd-evis__visual-pending';
      pending.textContent = t.pending;
      card.appendChild(pending);
    }

    const assets = record.searchable_text && Array.isArray(record.searchable_text.assets)
      ? record.searchable_text.assets
      : [];
    if (assets.length) {
      const links = document.createElement('div');
      links.className = 'pd-evis__links';
      assets.forEach((asset) => links.appendChild(buildAssetLink(asset)));
      card.appendChild(links);
    }

    const openGap = Array.isArray(record.gaps)
      ? record.gaps.find((gap) => gap.status === 'OPEN' || gap.status === 'BLOCKED')
      : null;
    if (openGap) {
      const gap = document.createElement('p');
      gap.className = 'pd-evis__gap';
      const strong = document.createElement('strong');
      strong.textContent = `${t.gaps}: `;
      gap.append(strong, document.createTextNode(openGap.next_action));
      card.appendChild(gap);
    }

    return card;
  };

  const render = (packageData) => {
    addStyles();

    const section = document.createElement('section');
    section.className = 'pd-evis';
    section.id = 'evidence-visibility';

    const inner = document.createElement('div');
    inner.className = 'pd-evis__inner';

    const eyebrow = document.createElement('p');
    eyebrow.className = 'pd-evis__eyebrow';
    eyebrow.textContent = t.eyebrow;

    const title = document.createElement('h2');
    title.textContent = t.title;

    const intro = document.createElement('p');
    intro.className = 'pd-evis__lead';
    intro.textContent = t.intro;

    const notice = document.createElement('div');
    notice.className = 'pd-evis__notice';
    notice.textContent = `${t.registered}: ${packageData.package_id}. ${t.partial}`;

    const grid = document.createElement('div');
    grid.className = 'pd-evis__grid';
    (packageData.records || []).forEach((record) => grid.appendChild(buildCard(record)));

    const standardLinks = document.createElement('div');
    standardLinks.className = 'pd-evis__links';
    const standard = document.createElement('a');
    standard.href = new URL(
      lang.toLowerCase().startsWith('es') ? 'es/visibilidad-evidencia/' : 'en/evidence-visibility/',
      root
    ).href;
    standard.textContent = t.openStandard;
    standardLinks.appendChild(standard);

    inner.append(eyebrow, title, intro, notice, grid, standardLinks);
    section.appendChild(inner);

    const main = document.querySelector('main');
    if (main) main.appendChild(section);
  };

  fetch(registryUrl, { credentials: 'same-origin' })
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then(render)
    .catch((error) => {
      console.warn('Por Derecho evidence visibility register unavailable:', error);
      addStyles();
      const main = document.querySelector('main');
      if (!main) return;
      const section = document.createElement('section');
      section.className = 'pd-evis';
      section.id = 'evidence-visibility';
      const inner = document.createElement('div');
      inner.className = 'pd-evis__inner';
      const title = document.createElement('h2');
      title.textContent = t.title;
      const message = document.createElement('p');
      message.textContent = t.unavailable;
      inner.append(title, message);
      section.appendChild(inner);
      main.appendChild(section);
    });
})();
