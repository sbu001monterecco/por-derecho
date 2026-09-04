(() => {
  'use strict';
  const path = window.location.pathname.replace(/\/index\.html$/, '/');
  const es = path.endsWith('/es/reclamacion-caixabank-valencia/documentos/');
  const en = path.endsWith('/en/caixabank-valencia-claim/documents/');
  if (!es && !en) return;

  const DEMANDA = 'https://1drv.ms/b/c/bdf43392f576e62f/IQA_jgn9nZ7HS5RT7byXZwJ4AXG2kA1SGMZOfENKOQAc_80';
  const CONTESTACION = 'https://1drv.ms/b/c/bdf43392f576e62f/IQDp2mBSGL5GQ5cNBhcEiVKrAcn8t1WXaYOaZCDghdJjo8Q';
  const AC2021 = 'https://1drv.ms/b/c/bdf43392f576e62f/IQBAYqfoXeLLSYqnpI5fm2CDAa1iTqAOPpKsimc7sp94dZc';

  const esc = (s) => s.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const button = (href, label, cls='button') => `<a class="${cls}" href="${esc(href)}" target="_blank" rel="noopener noreferrer">${esc(label)}</a>`;

  const html = es ? `
    <section class="section" id="fuentes-integras-publicas" data-caixabank-full-source-pdfs="20260904a">
      <div class="shell record">
        <div class="source" style="border:2px solid rgba(19,37,45,.28)">
          <p class="eyebrow">FUENTES PRIMARIAS · ABRIR EL DOCUMENTO PRESENTADO</p>
          <h2>Los escritos principales ya pueden leerse íntegramente antes de contactar.</h2>
          <p>Estos enlaces son <strong>copias PDF de los escritos fuente localizados en el expediente</strong>, alojadas en modo de lectura pública. La demanda y la contestación se ofrecen para que un abogado pueda comprobar el texto completo, no sólo el resumen de esta sala.</p>
          <div class="linkrow" style="margin:.9rem 0 1rem">
            ${button(DEMANDA, 'Abrir demanda completa · 27 págs. →')}
            ${button(CONTESTACION, 'Abrir contestación CaixaBank completa · 47 págs. →')}
            ${button(AC2021, 'Abrir escrito AC 25-Ene-2021 · 2 págs. →', 'button secondary')}
          </div>
          <div class="warn"><strong>Pericial PKF (96 págs.).</strong> La copia fuente completa está localizada y controlada, pero no se publica sin depuración porque su página de presentación contiene DNI, dirección y teléfonos de terceros y sus anexos incorporan material de proveedores comerciales. El análisis sustantivo y sus conclusiones están expuestos abajo. Se preparará una copia pública que omita únicamente esos datos/materiales, sin alterar la opinión pericial.</div>
          <p class="small" style="margin-top:.8rem"><strong>Control documental:</strong> el PDF fuente prevalece sobre cualquier resumen. Los enlaces son sólo lectura, sin caducidad configurada. Las posiciones de las partes siguen siendo alegaciones controvertidas.</p>
        </div>
      </div>
    </section>` : `
    <section class="section" id="full-filed-sources" data-caixabank-full-source-pdfs="20260904a">
      <div class="shell record">
        <div class="source" style="border:2px solid rgba(19,37,45,.28)">
          <p class="eyebrow">PRIMARY SOURCES · OPEN THE FILED DOCUMENT</p>
          <h2>The core Spanish pleadings are now available in full before first contact.</h2>
          <p>These are <strong>full source PDFs located in the case record</strong>. The Spanish filings control; this English page remains a translated legal guide rather than a certified translation.</p>
          <div class="linkrow" style="margin:.9rem 0 1rem">
            ${button(DEMANDA, 'Open full Aweswell claim · 27 pp. →')}
            ${button(CONTESTACION, 'Open full CaixaBank defence · 47 pp. →')}
            ${button(AC2021, 'Open AC filing 25-Jan-2021 · 2 pp. →', 'button secondary')}
          </div>
          <div class="warn"><strong>PKF expert report (96 pp.).</strong> The complete source has been located and controlled, but the unredacted PDF is not made public because it contains third-party national-ID/contact data and licensed commercial-source annex material. Its substantive positions and conclusions are summarized below; the Spanish original remains the controlling source.</div>
          <p class="small" style="margin-top:.8rem"><strong>Document control:</strong> source PDFs prevail over summaries. Links are view-only with no configured expiry. Party pleadings remain contested positions.</p>
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
