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
    const status = isEs ? 'Sin comunicación recibida hasta la fecha' : 'No communication received to date';

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

    const coagcIndex = index && index.querySelector('a[href="#coagc"] span');
    const coalzIndex = index && index.querySelector('a[href="#coa-lanzarote"] span');
    if (coagcIndex) coagcIndex.textContent = '11';
    if (coalzIndex) coalzIndex.textContent = '12';

    const coagcNumber = document.querySelector('#coagc .ir-number');
    const coalzNumber = document.querySelector('#coa-lanzarote .ir-number');
    if (coagcNumber) coagcNumber.textContent = '11';
    if (coalzNumber) coalzNumber.textContent = '12';

    const navRecords = document.querySelector('.institutional-records-page .main-nav a[href="#records"]');
    if (navRecords) navRecords.textContent = isEs ? 'Doce registros' : 'Twelve records';

    const eyebrow = document.querySelector('.institutional-records-page .ir-hero .eyebrow');
    if (eyebrow) eyebrow.textContent = isEs
      ? 'Registro controlado por fuentes · verificado hasta 16 agosto 2026'
      : 'Source-controlled record · verified through 16 August 2026';

    const lead = document.querySelector('.institutional-records-page .ir-hero .lead');
    if (lead) lead.textContent = isEs
      ? 'Doce registros estables consolidan comunicaciones clave y referencias técnicas delimitadas relativas a los organismos públicos y corporaciones profesionales de derecho público del mapa de control. Cada uno separa competencia, hitos trazables, límites probatorios y una acción finita pendiente.'
      : 'Twelve stable records consolidate key communications and bounded technical references concerning the public authorities and public-law professional corporations in the accountability map. Each separates competence, traceable milestones, evidential limits and one finite pending action.';

    const scope = document.querySelector('.institutional-records-page .ir-status div:first-child strong');
    if (scope) scope.textContent = isEs
      ? 'Doce registros de organismos públicos y corporaciones profesionales de derecho público'
      : 'Twelve records for public authorities and public-law professional corporations';

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
          <div><span>Última verificación</span><strong>16 agosto 2026</strong></div>
          <div><span>Estado</span><strong>Sin comunicación recibida del Consejo hasta la fecha</strong></div>
        </div>
      </div>
      <div class="ir-controls">
        <div class="ir-control proves"><strong>Acredita</strong>La existencia, naturaleza de corporación de derecho público y función canaria de representación y coordinación del Consejo constan en fuentes institucionales oficiales.</div>
        <div class="ir-control limit"><strong>No acredita</strong>La inclusión de esta marca ni la ausencia de comunicación recibida acreditan posición, admisión, archivo, resolución, infracción profesional o decisión sobre el fondo. El silencio no es una decisión de mérito.</div>
        <div class="ir-control action"><strong>Acción finita pendiente</strong>Incorporar cualquier comunicación oficial que se reciba con fecha, referencia, alcance, estado procedimental y límite probatorio, manteniendo separado el carril del Consejo de los expedientes ICALPA.</div>
      </div>
      <div class="ir-links"><a class="official" href="https://consejocanariodeabogados.es/" rel="external noopener">Sitio oficial del Consejo ↗</a></div>
      <p class="ir-source-note">Estado actualizado a 16 agosto 2026: no se publica inferencia alguna a partir de la ausencia de comunicación recibida.</p>
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
          <div><span>Last verified</span><strong>16 August 2026</strong></div>
          <div><span>Status</span><strong>No communication received from the Council to date</strong></div>
        </div>
      </div>
      <div class="ir-controls">
        <div class="ir-control proves"><strong>Proves</strong>Official institutional sources establish the Council’s existence, public-law status and Canary-wide representative and coordinating role.</div>
        <div class="ir-control limit"><strong>Does not prove</strong>Neither inclusion of this identifier nor the absence of a received communication establishes a position, admission, closure, decision, professional breach or merits outcome. Silence is not a merits decision.</div>
        <div class="ir-control action"><strong>Finite pending action</strong>Add any official communication received with its date, reference, scope, procedural status and evidential limit, keeping the Council track separate from the ICALPA files.</div>
      </div>
      <div class="ir-links"><a class="official" href="https://consejocanariodeabogados.es/" rel="external noopener">Official Council website ↗</a></div>
      <p class="ir-source-note">Status updated 16 August 2026: no inference is published from the absence of a received communication.</p>
    </article>
  `;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run, { once: true });
  } else {
    run();
  }
})();
