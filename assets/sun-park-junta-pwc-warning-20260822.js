(() => {
  const d = document;
  const normalise = value => {
    let path = value.replace(/\/index\.html$/, '/');
    if (!path.endsWith('/')) path += '/';
    return path;
  };
  const path = normalise(location.pathname);
  const routes = new Set([
    '/es/concurso-36-2012-administrador-concursal/',
    '/en/insolvency-36-2012-insolvency-administrator/',
    '/es/pwc-canarias-carlos-saavedra-sun-park/',
    '/en/pwc-canarias-carlos-saavedra-sun-park/',
    '/es/reunion-pwc-fmmm-11-junio-2016/',
    '/es/acosta-matos-perimetro/',
    '/en/acosta-matos-perimeter/',
    '/es/ricpe-responsabilidad-documental/',
    '/en/ricpe-documentary-accountability/',
    '/es/san-telmo-ricpe-sun-park/',
    '/en/san-telmo-ricpe-sun-park/'
  ]);
  if (![...routes].some(route => path.endsWith(route))) return;

  const render = () => {
    if (d.querySelector('[data-junta-pwc-warning]')) return;
    const main = d.querySelector('main');
    const opening = d.querySelector('main > section:first-of-type');
    if (!main || !opening) return;

    const en = d.documentElement.lang === 'en';
    const prefix = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
    const target = en
      ? `${prefix}en/evidence-pwc-sun-park-meeting-21-april-2016/`
      : `${prefix}es/evidencia-pwc-junta-sun-park-21-abril-2016/`;

    const style = d.createElement('style');
    style.textContent = `
      .jpwc{padding:1.2rem 0;background:#fff3ef;color:#13252d;border-top:7px solid #a61b16;border-bottom:7px solid #a61b16}
      .jpwc__card{display:grid;grid-template-columns:1.05fr 1.95fr;gap:1rem;max-width:1180px;margin:auto;padding:1.15rem;border:2px solid #a61b16;border-radius:20px;background:#fff;box-shadow:0 14px 36px rgba(55,16,14,.16)}
      .jpwc__signal{display:flex;flex-direction:column;justify-content:center;padding:1.2rem;border-radius:15px;background:#a61b16;color:#fff}.jpwc__mark{font-weight:1000;font-size:clamp(2rem,5vw,4.4rem);line-height:.9;letter-spacing:-.04em}.jpwc__signal p{margin:.75rem 0 0;font-weight:850}.jpwc__signal small{margin-top:.6rem;opacity:.9}
      .jpwc__copy{padding:.2rem}.jpwc__k{margin:0;color:#7b1511;font-size:.76rem;font-weight:950;letter-spacing:.09em;text-transform:uppercase}.jpwc h2{font-size:clamp(1.65rem,3vw,2.65rem);line-height:1.02;margin:.35rem 0 .65rem}.jpwc__lead{font-size:1.02rem;margin:.25rem 0 .8rem}.jpwc__timeline{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.55rem}.jpwc__timeline div{padding:.7rem;border-radius:12px;background:#f3f5f5;border-top:5px solid #315c7b}.jpwc__timeline b{display:block;color:#7b1511}.jpwc__action{display:inline-flex;margin-top:.85rem;padding:.72rem 1rem;border-radius:999px;background:#13252d;color:#fff!important;font-weight:950;text-decoration:none}.jpwc__limit{display:block;margin-top:.7rem;color:#55666d;font-size:.82rem;line-height:1.35}
      @media(max-width:880px){.jpwc__card{grid-template-columns:1fr}.jpwc__timeline{grid-template-columns:1fr 1fr}}@media(max-width:560px){.jpwc__timeline{grid-template-columns:1fr}.jpwc__card{border-radius:12px}.jpwc__mark{font-size:2.6rem}}
    `;
    d.head.append(style);

    const section = d.createElement('section');
    section.className = 'jpwc';
    section.dataset.juntaPwcWarning = '20260822';
    section.setAttribute('aria-label', en ? 'Key evidence: PwC and the 2016 Sun Park meeting' : 'Prueba clave: PwC y la Junta Sun Park de 2016');
    section.innerHTML = en ? `
      <div class="shell"><div class="jpwc__card">
        <div class="jpwc__signal"><span class="jpwc__mark">21 APR</span><p>“I DO NOT AUTHORISE THEIR ENGAGEMENT”</p><small>Insolvency Administrator’s email · 2016</small></div>
        <div class="jpwc__copy"><p class="jpwc__k">KEY CONTEMPORANEOUS EVIDENCE · READ AS ONE EVENT</p><h2>PwC agreed to attend. The next day the Insolvency Administrator refused authority.</h2><p class="jpwc__lead">The sequence connects late delivery of the notice, PwC’s legal work, planned attendance, Borja Rodríguez-Batllori’s refusal and the disputed loss of voting rights.</p>
          <div class="jpwc__timeline"><div><b>15 APR</b>Notice photographs reach the complex; the analysis is sent to PwC.</div><div><b>20 APR</b>Carlos confirms Carlos, Miguel and Elena will travel to Lanzarote.</div><div><b>21 APR</b>Borja refuses PwC’s engagement and tells the three not to act.</div><div><b>26 APR</b>Meeting and disputed Community resolutions.</div></div>
          <a class="jpwc__action" href="${target}">Open the complete evidence and criminal-law test →</a><small class="jpwc__limit">The email proves the refusal and warning. It does not, by itself, prove concealment, a false debt or a criminal offence.</small>
        </div>
      </div></div>` : `
      <div class="shell"><div class="jpwc__card">
        <div class="jpwc__signal"><span class="jpwc__mark">21 ABR</span><p>«NO AUTORIZO SU CONTRATACIÓN»</p><small>Correo del Administrador Concursal · 2016</small></div>
        <div class="jpwc__copy"><p class="jpwc__k">PRUEBA CONTEMPORÁNEA CLAVE · LECTURA UNITARIA</p><h2>PwC confirmó que asistiría. Al día siguiente, el Administrador Concursal negó la autorización.</h2><p class="jpwc__lead">La secuencia une la llegada tardía de la convocatoria, el trabajo jurídico de PwC, la asistencia prevista, la negativa de Borja Rodríguez-Batllori y la privación de voto discutida.</p>
          <div class="jpwc__timeline"><div><b>15 ABR</b>Llegan al complejo fotos de la convocatoria; el análisis se envía a PwC.</div><div><b>20 ABR</b>Carlos confirma que Carlos, Miguel y Elena viajarán a Lanzarote.</div><div><b>21 ABR</b>Borja niega el encargo PwC y ordena a los tres no actuar.</div><div><b>26 ABR</b>Junta y acuerdos comunitarios controvertidos.</div></div>
          <a class="jpwc__action" href="${target}">Abrir prueba completa y test penal →</a><small class="jpwc__limit">El correo prueba la negativa y el apercibimiento. No prueba por sí solo ocultación, deuda falsa ni delito.</small>
        </div>
      </div></div>`;

    opening.insertAdjacentElement('afterend', section);
  };

  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', render, { once: true });
  else render();
})();
