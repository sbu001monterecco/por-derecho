(() => {
  'use strict';

  const run = () => {
    const lang = (document.documentElement.lang || '').toLowerCase().startsWith('es') ? 'es' : 'en';
    addInstitutionalMark(lang);
    addInstitutionalRecord(lang);
  };

  const make = (html) => {
    const template = document.createElement('template');
    template.innerHTML = html.trim();
    return template.content.firstElementChild;
  };

  const addInstitutionalMark = (lang) => {
    if (document.querySelector('.identity-logo-card[data-institution="ccca"]')) return;

    const icalpa = document.querySelector('.identity-logo-card[href*="#icalpa"]');
    if (!icalpa) return;

    const isEs = lang === 'es';
    const href = isEs ? 'registros-institucionales/#ccca' : 'institutional-records/#ccca';
    const aria = isEs
      ? 'Abrir el registro de Project Sun Rock, controlado por fuentes, sobre el Consejo Canario de Colegios de Abogados'
      : 'Open Project Sun Rock’s source-controlled record for the Canary Council of Bar Associations';
    const status = isEs ? 'Sin comunicación directa recibida del Consejo sobre esta coordinación' : 'No direct Council communication received on this coordination question';

    const card = make(`
      <a class="identity-logo-card" data-institution="ccca" href="${href}" aria-label="${aria}">
        <span class="identity-logo-frame"><span class="identity-wordmark" aria-hidden="true">CCCA<small>${isEs ? 'Consejo Canario' : 'Canary Council'}</small></span></span>
        <span class="identity-logo-copy"><strong>Consejo Canario de Colegios de Abogados — CCCA</strong><small>${status}</small></span><span class="identity-external" aria-hidden="true">→</span>
      </a>
    `);

    icalpa.insertAdjacentElement('afterend', card);
  };

  const addInstitutionalRecord = (lang) => {
    const records = document.querySelector('.institutional-records-page #records');
    if (!records || document.getElementById('ccca')) return;

    const icalpa = document.getElementById('icalpa');
    if (!icalpa) return;

    const isEs = lang === 'es';

    const index = document.querySelector('.ir-index');
    const icalpaIndex = index && index.querySelector('a[href="#icalpa"]');
    if (icalpaIndex && !index.querySelector('a[href="#ccca"]')) {
      icalpaIndex.insertAdjacentElement('afterend', make(
        `<a href="#ccca"><span>10</span> ${isEs ? 'Consejo Canario de Colegios de Abogados' : 'Canary Council of Bar Associations'}</a>`
      ));
    }

    const article = make(isEs ? spanishRecord() : englishRecord());
    icalpa.insertAdjacentElement('afterend', article);
  };

  const spanishRecord = () => `
    <article class="ir-record" id="ccca">
      <div class="ir-record-head">
        <div>
          <span class="ir-number">10</span>
          <h2>Consejo Canario de Colegios de Abogados — CCCA</h2>
          <p><strong>Competencia:</strong> corporación de derecho público de ámbito canario que representa y coordina a los Colegios de Abogados de Canarias dentro de las funciones atribuidas por su normativa y Estatutos. Se mantiene separada de ICALPA y de cualquier expediente colegial de primera instancia.</p>
        </div>
        <div class="ir-meta">
          <div><span>Última verificación</span><strong>21 septiembre 2026</strong></div>
          <div><span>Estado</span><strong>Sin comunicación directa recibida sobre esta coordinación</strong></div>
        </div>
      </div>
      <div class="ir-controls">
        <div class="ir-control proves"><strong>Acredita</strong>La existencia, naturaleza de corporación de derecho público y función canaria de representación y coordinación del Consejo constan en fuentes institucionales oficiales.</div>
        <div class="ir-control limit"><strong>No acredita</strong>La inclusión de esta marca ni la ausencia de comunicación recibida acreditan posición, admisión, archivo, resolución, infracción profesional o decisión sobre el fondo. El silencio no es una decisión de mérito.</div>
        <div class="ir-control action"><strong>Acción finita pendiente</strong>Incorporar cualquier comunicación oficial que se reciba con fecha, referencia, alcance, estado procedimental y límite probatorio, manteniendo separado el carril del Consejo de los expedientes ICALPA.</div>
      </div>
      <div class="ir-links"><a href="../consejo-canario-coordinacion-deontologica-2026/">Registro de coordinación profesional →</a><a class="official" href="https://consejocanariodeabogados.es/" rel="external noopener">Sitio oficial del Consejo ↗</a></div>
      <p class="ir-source-note">Estado actualizado a 21 septiembre 2026: no se publica inferencia alguna a partir de la ausencia de comunicación directa del Consejo.</p>
    </article>
  `;

  const englishRecord = () => `
    <article class="ir-record" id="ccca">
      <div class="ir-record-head">
        <div>
          <span class="ir-number">10</span>
          <h2>Consejo Canario de Colegios de Abogados — CCCA</h2>
          <p><strong>Competence:</strong> a Canary Islands public-law corporation representing and coordinating the Bar Associations of the Canary Islands within the functions assigned by its governing law and statutes. It is kept separate from ICALPA and from any first-instance Bar disciplinary file.</p>
        </div>
        <div class="ir-meta">
          <div><span>Last verified</span><strong>21 September 2026</strong></div>
          <div><span>Status</span><strong>No direct Council communication received on this coordination question</strong></div>
        </div>
      </div>
      <div class="ir-controls">
        <div class="ir-control proves"><strong>Proves</strong>Official institutional sources establish the Council’s existence, public-law status and Canary-wide representative and coordinating role.</div>
        <div class="ir-control limit"><strong>Does not prove</strong>Neither inclusion of this identifier nor the absence of a received communication establishes a position, admission, closure, decision, professional breach or merits outcome. Silence is not a merits decision.</div>
        <div class="ir-control action"><strong>Finite pending action</strong>Add any official communication received with its date, reference, scope, procedural status and evidential limit, keeping the Council track separate from the ICALPA files.</div>
      </div>
      <div class="ir-links"><a href="../canary-council-deontological-coordination-2026/">Professional coordination record →</a><a class="official" href="https://consejocanariodeabogados.es/" rel="external noopener">Official Council website ↗</a></div>
      <p class="ir-source-note">Status updated 21 September 2026: no inference is published from the absence of direct Council communication.</p>
    </article>
  `;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run, { once: true });
  } else {
    run();
  }
})();
