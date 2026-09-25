(() => {
  const path = window.location.pathname.replace(/\/+$/, '') + '/';
  const esCal = path.endsWith('/es/calificacion-concurso-36-2012-vidas-paralelas/');
  const enCal = path.endsWith('/en/insolvency-classification-parallel-lives/');
  const esJudge = path.endsWith('/es/concurso-36-2012-magistrado-juez/') || path.endsWith('/es/concurso-36-2012-juzgado-mercantil-1/');
  const enJudge = path.endsWith('/en/insolvency-36-2012-mercantile-court-1/');
  const es = esCal || esJudge;
  const en = enCal || enJudge;
  if (!es && !en) return;
  if (document.querySelector('[data-cal-source-correction-20260816]')) return;

  const marker = document.createElement('div');
  marker.dataset.calSourceCorrection20260816 = '4';
  marker.hidden = true;
  document.body.appendChild(marker);

  if (esCal || enCal) {
    const actorParagraphs = document.querySelectorAll('.actor-card p');
    for (const p of actorParagraphs) {
      const text = p.textContent || '';
      if (esCal && text.includes('debe completarse el informe original íntegro de calificación del AC')) {
        p.innerHTML = '<strong>Estado de fuente actualizado:</strong> el informe de calificación de la AC de 11 de febrero de 2019, de 47 páginas, ya ha sido leído íntegramente. Sigue abierta la reconciliación/certificación del universo completo de anexos y, sobre todo, la prueba proposición por proposición de qué documento contrario recibió o conoció personalmente cada actor antes de formular o adoptar cada afirmación impugnada.';
      }
      if (enCal && (text.includes('complete original AC classification report') || text.includes('full original AC classification report'))) {
        p.innerHTML = '<strong>Updated source status:</strong> the insolvency administrator’s 47-page classification report of 11 February 2019 has now been read in full. What remains open is reconciliation/certification of the complete annex universe and, above all, proposition-by-proposition proof of which contrary document each actor personally received or knew before making or adopting each challenged statement.';
      }
    }

    const docParagraphs = document.querySelectorAll('.docbox p');
    for (const p of docParagraphs) {
      const text = p.textContent || '';
      if (esCal && text.includes('Siguen pendientes de completar el informe/anexos íntegros del AC')) {
        p.innerHTML = '<strong>Estado probatorio actualizado:</strong> ya se han revisado íntegramente el informe AC de 47 páginas, el dictamen fiscal de 12 de marzo de 2019, la ampliación de DI 248 de enero de 2019, el decreto de archivo de DI 248 de 7 de mayo de 2019, la Sentencia 163/2023 y los recursos controlados. Siguen abiertos la certificación/reconciliación de todos los anexos del informe AC, el expediente completo de DI 248, la prueba certificada de la vista de 25 de julio de 2023, la matriz completa de prueba efectivamente ante cada actor y el expediente/resolución actual de la Audiencia Provincial.';
      }
      if (enCal && (text.includes('complete AC report/annexes') || text.includes('full AC report/annexes'))) {
        p.innerHTML = '<strong>Updated evidential status:</strong> the 47-page AC report, the 12 March 2019 Fiscal opinion, the January 2019 DI 248 expansion, the 7 May 2019 DI 248 archive decree, Judgment 163/2023 and the controlled appeals have now been reviewed. Still open are certification/reconciliation of the complete AC annex universe, the complete DI 248 file, the certified 25 July 2023 hearing record, the full evidence-before-each-actor matrix and the current Audiencia Provincial record/resolution.';
      }
    }
  }

  const mediaArticleUrl = 'https://www.lavozdelanzarote.com/actualidad/politica/el-juez-pone-fin-al-proceso-concursal-de-inalsa-aprobando-el-convenio-con-los-acreedores-que-implica-una-quita-del-21-72-por-ciento_82691_102.html';
  const localImageUrl = asset('alberto-lopez-villarrubia-supplied-17aug2026.webp?v=20260817d');

  const style = document.createElement('style');
  style.dataset.judgeImageLocationFix = '20260817d';
  style.textContent = `
    #lpam-magistrado-source-control .lpam-judge-photo{
      display:block;position:static!important;top:auto!important;
      width:min(100%,760px);max-width:760px;margin:1rem 0 1.45rem;
      background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:18px;overflow:hidden;
      box-shadow:0 10px 28px rgba(19,37,45,.08)
    }
    #lpam-magistrado-source-control .lpam-judge-photo img{
      display:block;width:100%;height:auto;aspect-ratio:760/428;object-fit:cover;object-position:center;background:#f1f2f2
    }
    #lpam-magistrado-source-control .lpam-judge-photo figcaption{
      padding:.8rem .95rem;font-size:.82rem;line-height:1.42;color:#586267
    }
    #lpam-magistrado-source-control .lpam-judge-photo figcaption a{color:inherit;text-decoration:underline}
    #lpam-magistrado-source-control .judge-image-error{
      margin:0;padding:1rem 1.1rem;background:#f3efe4;color:#13252d;font-size:.92rem;line-height:1.5
    }
    #lpam-magistrado-source-control .judge-image-error a{color:inherit;text-decoration:underline;font-weight:700}
    .judge-approved-grid.judge-approved-grid-no-photo{display:block!important;grid-template-columns:1fr!important}
    .judge-approved-grid.judge-approved-grid-no-photo>div{width:100%;min-width:0}
    @media(max-width:850px){
      #lpam-magistrado-source-control .lpam-judge-photo{width:100%;margin:1rem 0 1.2rem;border-radius:14px}
    }
  `;
  document.head.appendChild(style);

  const relocateJudgePhoto = () => {
    const figure = document.querySelector('.judge-approved-photo');
    const target = document.querySelector('#lpam-magistrado-source-control .record');
    if (!figure || !target) return false;

    const image = figure.querySelector('img');
    const caption = figure.querySelector('figcaption');
    if (!image || !caption) return false;

    image.removeAttribute('srcset');
    image.width = 760;
    image.height = 428;
    image.loading = 'eager';
    image.decoding = 'async';
    image.fetchPriority = 'high';
    image.alt = es
      ? 'Fotografía publicada por La Voz de Lanzarote y utilizada en el módulo documental relativo al magistrado Alberto López Villarrubia'
      : 'Photograph published by La Voz de Lanzarote and used in the documentary module concerning Magistrate-Judge Alberto López Villarrubia';

    image.addEventListener('error', () => {
      image.remove();
      if (!figure.querySelector('.judge-image-error')) {
        const notice = document.createElement('p');
        notice.className = 'judge-image-error';
        notice.innerHTML = es
          ? `La copia visual local no pudo cargarse. <a href="${mediaArticleUrl}" rel="external noopener">Abrir la publicación original en La Voz de Lanzarote →</a>`
          : `The local visual copy could not be loaded. <a href="${mediaArticleUrl}" rel="external noopener">Open the original La Voz de Lanzarote publication →</a>`;
        figure.prepend(notice);
      }
    }, { once: true });

    image.src = localImageUrl;

    caption.innerHTML = es
      ? `<strong>Fuente mediática:</strong> <a href="${mediaArticleUrl}" rel="external noopener">La Voz de Lanzarote</a>, 18 de septiembre de 2013. La página de origen revisada no identifica a un fotógrafo individual. Copia local optimizada a partir de la imagen aportada por Gil Marer para este expediente; la identificación empleada por Por Derecho procede del registro documental y de la atribución del aportante, no de reconocimiento facial realizado por ChatGPT.`
      : `<strong>Media source:</strong> <a href="${mediaArticleUrl}" rel="external noopener">La Voz de Lanzarote</a>, 18 September 2013. The reviewed source page does not identify an individual photographer. Optimised local copy derived from the image supplied by Gil Marer for this dossier; Por Derecho's identification comes from the documentary record and the supplier's attribution, not facial identification performed by ChatGPT.`;

    figure.classList.add('lpam-judge-photo');
    figure.dataset.mediaCredit = 'la-voz-de-lanzarote-20130918';
    figure.dataset.locationFix = 'lpam-magistrado-source-control';
    figure.dataset.imageSource = 'verified-local-webp';

    const heading = target.querySelector('h2');
    if (heading) heading.insertAdjacentElement('afterend', figure);
    else target.prepend(figure);

    const grid = document.querySelector('.judge-approved-grid');
    if (grid) grid.classList.add('judge-approved-grid-no-photo');
    return true;
  };

  if (!relocateJudgePhoto()) {
    const observer = new MutationObserver(() => {
      if (relocateJudgePhoto()) observer.disconnect();
    });
    observer.observe(document.body, { childList: true, subtree: true });
    window.setTimeout(() => observer.disconnect(), 15000);
  }

  function asset(filename) {
    const base = document.querySelector('script[src*="site.js"]')?.src || window.location.href;
    return new URL(filename, base).href;
  }
})();
