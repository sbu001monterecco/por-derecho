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
    if (d.querySelector('.email-exhibit-link')) return;
    const main = d.querySelector('main');
    const opening = d.querySelector('main > section:first-of-type');
    if (!main || !opening) return;

    const en = d.documentElement.lang === 'en';
    const prefix = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
    const target = en
      ? `${prefix}en/evidence-pwc-sun-park-meeting-21-april-2016/`
      : `${prefix}es/evidencia-pwc-junta-sun-park-21-abril-2016/`;
    const sanTelmoDossier = en
      ? `${prefix}en/san-telmo-ricpe-sun-park/`
      : `${prefix}es/san-telmo-ricpe-sun-park/`;
    const onSanTelmoDossier = path.endsWith(en ? '/en/san-telmo-ricpe-sun-park/' : '/es/san-telmo-ricpe-sun-park/');
    const sanTelmoTarget = onSanTelmoDossier ? target : sanTelmoDossier;
    const sanTelmoCta = onSanTelmoDossier
      ? (en ? 'Open the complete 2016 evidence record →' : 'Abrir el expediente probatorio completo de 2016 →')
      : (en ? 'Open the source dossier →' : 'Abrir expediente fuente →');
    const sanTelmoImage = `${prefix}assets/evidence/email-used-20260822/san-telmo-ricpe-sun-park-stamp-v1-${en ? 'EN' : 'ES'}.png?v=20260822g`;
    const sourceCard = `${prefix}assets/evidence/ac-email-21-april-2016/ac2016-email-001-redacted-source-card-v2.webp`;

    const style = d.createElement('style');
    style.textContent = `
      .jpwc{padding:1.2rem 0;background:#fff3ef;color:#13252d;border-top:7px solid #a61b16;border-bottom:7px solid #a61b16}
      .jpwc__card{display:grid;grid-template-columns:1.05fr 1.95fr;gap:1rem;max-width:1180px;margin:auto;padding:1.15rem;border:2px solid #a61b16;border-radius:20px;background:#fff;box-shadow:0 14px 36px rgba(55,16,14,.16)}
      .jpwc__signal{display:flex;flex-direction:column;justify-content:center;padding:1rem;border-radius:15px;background:#a61b16;color:#fff}.jpwc__signal img{display:block;width:100%;max-height:12rem;object-fit:cover;object-position:top;border-radius:9px;border:1px solid rgba(255,255,255,.6)}.jpwc__mark{margin-top:.8rem;font-weight:1000;font-size:clamp(2rem,5vw,4.4rem);line-height:.9;letter-spacing:-.04em}.jpwc__signal p{margin:.75rem 0 0;font-weight:850}.jpwc__signal small{margin-top:.6rem;opacity:.9}
      .jpwc__visual{grid-column:1/-1;display:block;overflow:hidden;border:2px solid #13252d;border-radius:15px;background:#0e171b;color:#fff;text-decoration:none}.jpwc__visual img{display:block;width:100%;height:auto;aspect-ratio:3/2;object-fit:contain;background:#f4f0e7}.jpwc__visual span{display:block;padding:.65rem .85rem;font-size:.86rem;font-weight:850;line-height:1.35}.jpwc__visual:hover,.jpwc__visual:focus-visible{outline:4px solid #e3ac3a;outline-offset:3px}
      .jpwc__copy{padding:.2rem}.jpwc__k{margin:0;color:#7b1511;font-size:.76rem;font-weight:950;letter-spacing:.09em;text-transform:uppercase}.jpwc h2{font-size:clamp(1.65rem,3vw,2.65rem);line-height:1.02;margin:.35rem 0 .65rem}.jpwc__lead{font-size:1.02rem;margin:.25rem 0 .8rem}.jpwc__timeline{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.55rem}.jpwc__timeline div{padding:.7rem;border-radius:12px;background:#f3f5f5;border-top:5px solid #315c7b}.jpwc__timeline b{display:block;color:#7b1511}.jpwc__capacity{display:block;margin-top:.75rem;padding:.7rem .8rem;background:#fff5cc;border-left:5px solid #9a6a20;font-weight:850}.jpwc__action{display:inline-flex;margin-top:.85rem;padding:.72rem 1rem;border-radius:999px;background:#13252d;color:#fff!important;font-weight:950;text-decoration:none}.jpwc__limit{display:block;margin-top:.7rem;color:#55666d;font-size:.82rem;line-height:1.35}
      @media(max-width:880px){.jpwc__card{grid-template-columns:1fr}.jpwc__timeline{grid-template-columns:1fr 1fr}}@media(max-width:560px){.jpwc__timeline{grid-template-columns:1fr}.jpwc__card{border-radius:12px}.jpwc__mark{font-size:2.6rem}}
    `;
    d.head.append(style);

    const section = d.createElement('section');
    section.className = 'jpwc';
    section.dataset.juntaPwcWarning = '20260822';
    section.setAttribute('aria-label', en ? 'Key evidence: PwC and the 2016 Sun Park meeting' : 'Prueba clave: PwC y la Junta Sun Park de 2016');
    section.innerHTML = en ? `
      <div class="shell"><div class="jpwc__card">
        <a class="jpwc__visual" href="${sanTelmoTarget}"><img src="${sanTelmoImage}" width="1800" height="1200" loading="eager" fetchpriority="high" decoding="async" alt=""><span>Eduardo Sánchez (San Telmo) · Sun Park / MYND Yaiza · Francisco de Borja Rodríguez-Batllori (Insolvency Administrator) — source-controlled same-asset professional-overlap graphic. It does not by itself prove coordination, information transfer, unlawfulness or liability. ${sanTelmoCta}</span></a>
        <div class="jpwc__signal"><img src="${sourceCard}" width="1350" height="2400" loading="lazy" alt="Redacted source-card thumbnail for the 21 April 2016 Sun Park email"><span class="jpwc__mark">21 APR</span><p>“I DO NOT AUTHORISE THEIR ENGAGEMENT”</p><small>Later-forwarded copy · native 2016 message sought</small></div>
        <div class="jpwc__copy"><p class="jpwc__k">KEY CONTEMPORANEOUS EVIDENCE · SOURCE-BOUNDED</p><h2>The Administrator refused to authorise a PwC engagement for Luchy/LPB.</h2><p class="jpwc__lead">The reproduced reply says attendance itself needed no permission, adopts an alleged-arrears/no-vote premise, refuses the proposed engagement and asks the copied PwC professionals not to provide services to Luchy without consent.</p>
          <div class="jpwc__timeline"><div><b>18 APR</b>Pamanil’s reproduced message sends notice and asks about attendance.</div><div><b>21 APR · 00:21</b>Gil challenges the figures and again requests documents.</div><div><b>21 APR · 09:08</b>Gil requests signed authority for himself and copied PwC lawyers.</div><div><b>21 APR · 09:47</b>Borja records the LPB/Luchy-specific position.</div></div>
          <strong class="jpwc__capacity">Capacity and governance—not arithmetic: the reply does not determine Gil’s separately claimed Matkator, CEXP, Owners’ Community or personal capacities.</strong>
          <a class="jpwc__action" href="${target}">Open the redacted source, full chain and proof limits →</a><small class="jpwc__limit">The author’s recorded statements do not independently establish the alleged debt, meeting authority, misconduct or criminal intent. The five meeting-package PDFs were recovered from a separate carrier; current evidence does not show that the Administrator received or read them before replying.</small>
        </div>
      </div></div>` : `
      <div class="shell"><div class="jpwc__card">
        <a class="jpwc__visual" href="${sanTelmoTarget}"><img src="${sanTelmoImage}" width="1800" height="1200" loading="eager" fetchpriority="high" decoding="async" alt=""><span>Eduardo Sánchez (San Telmo) · Sun Park / MYND Yaiza · Francisco de Borja Rodríguez-Batllori (Administrador Concursal) — gráfico controlado por fuentes sobre el solapamiento profesional relativo al mismo activo. No prueba por sí solo coordinación, transmisión de información, ilicitud ni responsabilidad. ${sanTelmoCta}</span></a>
        <div class="jpwc__signal"><img src="${sourceCard}" width="1350" height="2400" loading="lazy" alt="Miniatura redactada del correo Sun Park de 21 de abril de 2016"><span class="jpwc__mark">21 ABR</span><p>«NO AUTORIZO SU CONTRATACION»</p><small>Copia reenviada posteriormente · mensaje nativo pendiente</small></div>
        <div class="jpwc__copy"><p class="jpwc__k">PRUEBA CONTEMPORÁNEA CLAVE · FUENTE DELIMITADA</p><h2>El Administrador negó autorizar un encargo PwC para Luchy/LPB.</h2><p class="jpwc__lead">La respuesta reproducida dice que asistir no requería permiso, adopta una premisa alegada de morosidad/sin voto, niega el encargo propuesto y pide a los profesionales de PwC copiados que no presten servicios a Luchy sin consentimiento.</p>
          <div class="jpwc__timeline"><div><b>18 ABR</b>El mensaje reproducido de Pamanil remite convocatoria y pregunta por asistencia.</div><div><b>21 ABR · 00:21</b>Gil impugna las cifras y vuelve a pedir documentación.</div><div><b>21 ABR · 09:08</b>Gil solicita autorización firmada para sí y los abogados PwC copiados.</div><div><b>21 ABR · 09:47</b>Borja registra la posición limitada a LPB/Luchy.</div></div>
          <strong class="jpwc__capacity">Capacidad y gobernanza, no aritmética: la respuesta no resuelve las capacidades alegadas para Matkator, CEXP, la Comunidad o Gil personalmente.</strong>
          <a class="jpwc__action" href="${target}">Abrir la fuente redactada, cadena y límites probatorios →</a><small class="jpwc__limit">Las manifestaciones del autor no acreditan por sí solas la deuda alegada, autoridad de la junta, ilícito o intención penal. Los cinco PDF de la junta se recuperaron de un reenvío separado; la prueba actual no demuestra que el Administrador los recibiera o leyera antes de responder.</small>
        </div>
      </div></div>`;

    opening.insertAdjacentElement('afterend', section);
  };

  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', render, { once: true });
  else render();
})();
