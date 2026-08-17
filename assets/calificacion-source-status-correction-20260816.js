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
  marker.dataset.calSourceCorrection20260816 = '1';
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

  const applyJudgeMediaCredit = () => {
    const caption = document.querySelector('.judge-approved-photo figcaption');
    if (!caption) return false;
    caption.innerHTML = es
      ? `<strong>Fuente mediática:</strong> <a href="https://www.lavozdelanzarote.com/actualidad/politica/el-juez-pone-fin-al-proceso-concursal-de-inalsa-aprobando-el-convenio-con-los-acreedores-que-implica-una-quita-del-21-72-por-ciento_82691_102.html" rel="external noopener">La Voz de Lanzarote</a>, 18 de septiembre de 2013. La página de origen revisada no muestra crédito de fotógrafo individual. Imagen aportada a este expediente por Gil Marer; la identificación utilizada por Por Derecho procede del registro documental y de la atribución del aportante, no de reconocimiento facial realizado por ChatGPT.`
      : `<strong>Media source:</strong> <a href="https://www.lavozdelanzarote.com/en/news/politics/the-judge-ends-inalsa-s-bankruptcy-proceedings-by-approving-the-agreement-with-creditors-which-implies-a-reduction-of-21-72-percent_82691_102.html" rel="external noopener">La Voz de Lanzarote</a>, 18 September 2013. The source page reviewed shows no individual photographer credit. Image supplied to this dossier by Gil Marer; Por Derecho's identification comes from the documentary record and the supplier's attribution, not facial identification performed by ChatGPT.`;
    caption.dataset.mediaCredit = 'la-voz-de-lanzarote-20130918';
    return true;
  };

  if (!applyJudgeMediaCredit()) {
    const observer = new MutationObserver(() => {
      if (applyJudgeMediaCredit()) observer.disconnect();
    });
    observer.observe(document.body, { childList: true, subtree: true });
    window.setTimeout(() => observer.disconnect(), 15000);
  }
})();