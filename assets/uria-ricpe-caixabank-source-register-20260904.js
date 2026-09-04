(() => {
  'use strict';
  const path = location.pathname.replace(/\/index\.html$/, '/');
  const relevant = path.includes('/ric-private-equity-sun-park/')
    || path.includes('/ricpe-')
    || path.includes('/acosta-matos-')
    || path.includes('/acosta-matos-perimet')
    || path.includes('/reclamacion-caixabank-valencia/')
    || path.includes('/caixabank-valencia-claim/')
    || path.includes('/uria');
  if (!relevant || document.querySelector('[data-uria-ricpe-caixabank-source-register]')) return;

  const isEnglish = document.documentElement.lang === 'en' || path.includes('/en/');
  const prefix = path.includes('/por-derecho/') ? '/por-derecho/' : '/';
  const main = document.querySelector('main');
  if (!main) return;

  const routes = {
    caixDocs: isEnglish ? `${prefix}en/caixabank-valencia-claim/documents/` : `${prefix}es/reclamacion-caixabank-valencia/documentos/`,
    trial: isEnglish ? `${prefix}en/caixabank-valencia-claim/hearing-28-january-2027/` : `${prefix}es/reclamacion-caixabank-valencia/senalamiento-28-enero-2027/`,
    ricpe: isEnglish ? `${prefix}en/ric-private-equity-sun-park/` : `${prefix}es/ric-private-equity-sun-park/`,
    controls: isEnglish ? `${prefix}en/ricpe-documentary-accountability/` : `${prefix}es/ricpe-responsabilidad-documental/`
  };
  const DEFENCE = 'https://1drv.ms/b/c/bdf43392f576e62f/IQDp2mBSGL5GQ5cNBhcEiVKrAcn8t1WXaYOaZCDghdJjo8Q';

  const sources = isEnglish ? [
    ['CaixaBank defence · 47 pages','abbaf13c655058635fbd37395ad2e8699c1c91918b6ef75c8a07b90b9b97b73b','PUBLIC RAW COPY',DEFENCE,'Full filed defence; controls any summary.'],
    ['Trial diligence · 6 Nov 2025','944ac006d360e37907c5f056821238ee6975c9f85a4779b30f84e59ba9952c6b','PUBLIC REDACTED IMAGES',routes.trial,'Public derivative removes unnecessary third-party verification/personal elements.'],
    ['RICPE certification · 20 Jul 2021','7c746d998780775542a5fe5265f02622f42b290918003f03ee20c8f367759bf8','SOURCE REGISTERED',routes.ricpe,'262-property breakdown; 54 CAM; wider acquisition conditional; no LOI; complete DD not started.'],
    ['CAM filing · 21 Jul 2021','76f5ba3210b9a78d641c318f60d214025c6231b99fe77734933f90da6ed3c8b9','SOURCE REGISTERED',routes.ricpe,'CAM says it never claimed sole ownership and owned only 54 units at that date.'],
    ['RICPE audited accounts · 2023','91d8999df59e96a08cbd3e2d97226f410d9514ab08011f4e24cbdfcc546be7c9','SOURCE REGISTERED',routes.controls,'Later MYND financing and documented formal related-party conflict process.'],
    ['RICPE ethics-channel closure · 27 Aug 2026','db9979715cac4aeb8ded81a998227cfd894144dcd0a50fe81d4b1369904c9bb4','CONTROLLED DERIVATIVE',routes.ricpe,'Raw certificate contains personal contact/system data; public site publishes the operative decision and evidentiary status, not unnecessary personal data.'],
    ['Control 21 consolidated filing · 9 Jul 2026','d13ddbc3c55c0d7f4753b25e0444275ec5bf1b21e0b378fcfd6315550ba78f09','CONTROLLED DERIVATIVE',routes.controls,'Raw filing contains personal identification data; the Uría/PwC/RICPE production request is published as a controlled proposition.']
  ] : [
    ['Contestación CaixaBank · 47 páginas','abbaf13c655058635fbd37395ad2e8699c1c91918b6ef75c8a07b90b9b97b73b','COPIA ÍNTEGRA PÚBLICA',DEFENCE,'Escrito presentado íntegro; prevalece sobre cualquier resumen.'],
    ['Diligencia de señalamiento · 6 nov 2025','944ac006d360e37907c5f056821238ee6975c9f85a4779b30f84e59ba9952c6b','IMÁGENES PÚBLICAS REDACCIONADAS',routes.trial,'La derivada pública elimina elementos personales/de verificación de terceros no necesarios.'],
    ['Certificación RICPE · 20 jul 2021','7c746d998780775542a5fe5265f02622f42b290918003f03ee20c8f367759bf8','FUENTE REGISTRADA',routes.ricpe,'262 fincas; 54 CAM; adquisición amplia condicionada; sin LOI; DD completa no iniciada.'],
    ['Escrito CAM · 21 jul 2021','76f5ba3210b9a78d641c318f60d214025c6231b99fe77734933f90da6ed3c8b9','FUENTE REGISTRADA',routes.ricpe,'CAM dice que nunca se atribuyó titularidad única y que poseía sólo 54 unidades en esa fecha.'],
    ['Cuentas auditadas RICPE · 2023','91d8999df59e96a08cbd3e2d97226f410d9514ab08011f4e24cbdfcc546be7c9','FUENTE REGISTRADA',routes.controls,'Financiación posterior MYND y proceso formal documentado de conflicto de parte vinculada.'],
    ['Cierre Canal Ético RICPE · 27 ago 2026','db9979715cac4aeb8ded81a998227cfd894144dcd0a50fe81d4b1369904c9bb4','DERIVADA CONTROLADA',routes.ricpe,'El certificado bruto contiene contacto personal/datos del sistema; la web publica la decisión operativa y su estado probatorio, no datos personales innecesarios.'],
    ['Control 21 consolidado · 9 jul 2026','d13ddbc3c55c0d7f4753b25e0444275ec5bf1b21e0b378fcfd6315550ba78f09','DERIVADA CONTROLADA',routes.controls,'El escrito bruto contiene identificación personal; se publica de forma controlada la solicitud de producción Uría/PwC/RICPE.']
  ];

  const esc = s => String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const style = document.createElement('style');
  style.dataset.uriaRicpeCaixabankSourceRegisterStyle = '20260904';
  style.textContent = `
    [data-uria-ricpe-caixabank-source-register]{margin:1.25rem auto;padding:1.05rem 0}
    [data-uria-ricpe-caixabank-source-register] h2{font-size:clamp(1.45rem,3vw,2.25rem);margin:.2rem 0 .5rem}
    [data-uria-ricpe-caixabank-source-register] .lead{max-width:900px;line-height:1.55}
    .urc-source-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.65rem;margin-top:.85rem}
    .urc-source{display:block;text-decoration:none;color:inherit;background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:12px;padding:.78rem;overflow-wrap:anywhere}
    .urc-source:hover{border-color:#13252d}
    .urc-source strong{display:block;margin-bottom:.2rem}.urc-source small{display:block;margin:.28rem 0;color:#48545a}.urc-source code{font-size:.67rem}
    .urc-source em{display:inline-block;font-style:normal;font-weight:900;font-size:.65rem;border-radius:999px;background:#eef2f3;padding:.24rem .45rem}
    @media(max-width:760px){.urc-source-grid{grid-template-columns:1fr}}
  `;
  document.head.append(style);

  const section = document.createElement('section');
  section.className = 'shell';
  section.dataset.uriaRicpeCaixabankSourceRegister = '20260904';
  const title = isEnglish ? 'Source register — every core exhibit in the current Uría / RICPE / CaixaBank reconstruction' : 'Registro de fuentes — todos los anexos núcleo de la reconstrucción actual Uría / RICPE / CaixaBank';
  const lead = isEnglish
    ? 'Every recovered core file is registered below by SHA-256. A public raw file is linked where publication is safe. Where the source contains unnecessary personal, account, system or privileged material, the site publishes a controlled derivative and keeps the original in evidence custody.'
    : 'Cada archivo núcleo recuperado queda registrado abajo por SHA-256. Cuando la publicación íntegra es segura, se enlaza la fuente completa. Cuando contiene datos personales, bancarios, de sistema o material potencialmente reservado innecesario, la web publica una derivada controlada y mantiene el original en custodia probatoria.';
  section.innerHTML = `<p class="kicker">${isEnglish ? 'EVIDENCE CUSTODY · 4 SEPTEMBER 2026' : 'CUSTODIA PROBATORIA · 4 SEPTIEMBRE 2026'}</p><h2>${title}</h2><p class="lead">${lead}</p><div class="urc-source-grid">${sources.map(([name,sha,status,href,note])=>`<a class="urc-source" href="${esc(href)}" ${href.startsWith('http')?'target="_blank" rel="noopener noreferrer"':''}><strong>${esc(name)}</strong><em>${esc(status)}</em><small>${esc(note)}</small><code>SHA-256 ${esc(sha)}</code></a>`).join('')}</div>`;

  const anchor = document.querySelector('[data-ricpe-cam-conflict-substance-statement]') || document.querySelector('[data-borja-witness-claimant-clarification]') || document.querySelector('#pregunta-unitaria') || main.querySelector(':scope > section:first-of-type');
  if (anchor) anchor.insertAdjacentElement('afterend', section);
  else main.append(section);
})();
