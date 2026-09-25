(() => {
  'use strict';
  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  const es = path.endsWith('/es/reclamacion-caixabank-valencia/documentos/');
  const en = path.endsWith('/en/caixabank-valencia-claim/documents/');
  if (!es && !en) return;

  const DEMANDA = '/por-derecho/assets/evidence/caixabank-valencia-publica-20260905/caixabank-demanda-oct2023-publica-20260905.pdf';
  const CONTESTACION = '/por-derecho/assets/evidence/caixabank-valencia-publica-20260905/caixabank-contestacion-ene2024-publica-20260905.pdf';
  const AC2021 = '/por-derecho/assets/evidence/caixabank-valencia-publica-20260905/caixabank-ac-25ene2021-publica-20260905.pdf';
  const DOC8 = 'https://1drv.ms/b/c/bdf43392f576e62f/IQCDS99BESLrToUHiLW7-WvgAatOtLDaQUPRm_z-LRajyJI';
  const DOC9 = 'https://1drv.ms/b/c/bdf43392f576e62f/IQCmADXdZu4tSriWJqneZ-eHAVHg_JszZ1-zvna_pyNihg8';

  const esc = (s) => s.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const button = (href, label, cls='button') => `<a class="${cls}" href="${esc(href)}" target="_blank" rel="noopener noreferrer">${esc(label)}</a>`;

  const html = es ? `
    <section class="section" id="fuentes-integras-publicas" data-caixabank-full-source-pdfs="20260904b">
      <div class="shell record">
        <div class="source" style="border:2px solid rgba(19,37,45,.28)">
          <p class="eyebrow">FUENTES PRIMARIAS · ABRIR EL DOCUMENTO PRESENTADO</p>
          <h2>Los escritos principales pueden leerse completos, con disociación de datos, antes de contactar.</h2>
          <p>Estos enlaces son <strong>copias PDF de los escritos fuente localizados en el expediente</strong>, alojadas en modo de lectura pública. La demanda y la contestación se ofrecen para que un abogado pueda comprobar el texto completo, no sólo el resumen de esta sala.</p>
          <div class="linkrow" style="margin:.9rem 0 1rem">
            ${button(DEMANDA, 'Abrir demanda completa · 27 págs. →')}
            ${button(CONTESTACION, 'Abrir contestación CaixaBank completa · 47 págs. →')}
            ${button(AC2021, 'Abrir escrito AC 25-Ene-2021 · 2 págs. →', 'button secondary')}
          </div>
          <h3>Otros anexos que pasan el control de publicación</h3>
          <div class="linkrow" style="margin:.6rem 0 1rem">
            ${button(DOC8, 'Abrir Doc. 8 · material regulatorio oficial · 32 págs. →', 'button secondary')}
            ${button(DOC9, 'Abrir Doc. 9 · nota conjunta BdE/CNMV · 7 págs. →', 'button secondary')}
          </div>
          <div class="warn"><strong>Documentos no publicados en bruto.</strong> El contrato de gestión de riesgos, la póliza de pignoración y el informe interno de riesgo contienen números de cuenta/identificadores operativos; el Informe AC 2013 incorpora información de múltiples acreedores/terceros; «Info Administrador» contiene datos personales y material comercial/licenciado; y la pericial PKF de 96 páginas contiene DNI/contacto de terceros y anexos de proveedor. Esos documentos permanecen resumidos o pendientes de una derivada pública verdaderamente depurada, sin presentar una falsa “redacción”.</div>
          <p class="small" style="margin-top:.8rem"><strong>Control documental:</strong> el PDF fuente prevalece sobre cualquier resumen. Los enlaces publicados son sólo lectura y sin caducidad configurada. Las posiciones de las partes siguen siendo alegaciones controvertidas.</p>
        </div>
      </div>
    </section>` : `
    <section class="section" id="full-filed-sources" data-caixabank-full-source-pdfs="20260904b">
      <div class="shell record">
        <div class="source" style="border:2px solid rgba(19,37,45,.28)">
          <p class="eyebrow">PRIMARY SOURCES · OPEN THE FILED DOCUMENT</p>
          <h2>The core Spanish pleadings are available in full before first contact.</h2>
          <p>These are <strong>full source PDFs located in the case record</strong>. The Spanish filings control; this English page remains a translated legal guide rather than a certified translation.</p>
          <div class="linkrow" style="margin:.9rem 0 1rem">
            ${button(DEMANDA, 'Open full Aweswell claim · 27 pp. →')}
            ${button(CONTESTACION, 'Open full CaixaBank defence · 47 pp. →')}
            ${button(AC2021, 'Open AC filing 25-Jan-2021 · 2 pp. →', 'button secondary')}
          </div>
          <h3>Other annexes cleared for public viewing</h3>
          <div class="linkrow" style="margin:.6rem 0 1rem">
            ${button(DOC8, 'Open Doc. 8 · official regulatory material · 32 pp. →', 'button secondary')}
            ${button(DOC9, 'Open Doc. 9 · joint BdE/CNMV note · 7 pp. →', 'button secondary')}
          </div>
          <div class="warn"><strong>Sources not bulk-published.</strong> The financial-risk contract, pledge and internal risk sheet expose account/operational identifiers; the 2013 AC report includes multi-creditor/third-party data; “Info Administrador” includes personal and licensed commercial-source material; and the 96-page PKF report contains third-party national-ID/contact data and provider annexes. Those records remain summarized or await a genuinely public-safe derivative rather than a misleading pseudo-redaction.</div>
          <p class="small" style="margin-top:.8rem"><strong>Document control:</strong> source PDFs prevail over summaries. The three core reading copies are same-site public redacted PDFs; regulatory annexes use their separately identified external viewers. Party pleadings remain contested positions.</p>
        </div>
      </div>
    </section>`;

  const insert = () => {
    if (document.querySelector('[data-caixabank-full-source-pdfs]')) return;
    const main = document.querySelector('main');
    if (!main) return;
    const firstAlt = main.querySelector('.section.alt');
    if (firstAlt) firstAlt.insertAdjacentHTML('afterend', html);
    else main.insertAdjacentHTML('afterbegin', html);
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', insert, {once:true});
  else insert();
})();
