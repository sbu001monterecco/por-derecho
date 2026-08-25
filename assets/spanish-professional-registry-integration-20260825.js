(() => {
  'use strict';
  if (window.__pdSpanishProfessionalIntegration20260825) return;
  window.__pdSpanishProfessionalIntegration20260825 = true;
  const path = location.pathname.replace(/index\.html$/,'');
  const isEn = document.documentElement.lang === 'en' || /\/en\//.test(path);
  const prefix = path.includes('/por-derecho/') ? '/por-derecho' : '';
  const target = isEn ? `${prefix}/en/matter-identity-registry/spanish-lawyers/` : `${prefix}/es/registro-identidad-materia/abogados-espanoles/`;
  const ownerNetwork = isEn ? `${prefix}/en/matter-identity-registry/non-lpb-matkator-owner-network/` : `${prefix}/es/registro-identidad-materia/perimetro-propietarios-no-lpb-matkator/`;
  const identityRoute = isEn ? '/en/matter-identity-registry/' : '/es/registro-identidad-materia/';
  const actorRoute = isEn ? '/en/actors-parties-lawyers-representatives/' : '/es/actores-partes-abogados-representantes/';
  const overrides = {
    'PD-SP-P-0052':'Miguel Méndez Itarte',
    'PD-SP-P-0054':'Zulay Carmen Rodríguez Cabrera',
    'PD-SP-P-0060':'Javier Sixto-Seijas',
    'PD-SP-P-0061':'Estefanía Sixto Seijas',
    'PD-SP-P-0063':'Daniel Irigoyen Fujiwara'
  };
  const withdrawn = new Set(['PD-SP-P-0065','PD-SP-P-0066']);

  const injectBanner = () => {
    if (!path.endsWith(identityRoute) && !path.endsWith(actorRoute)) return;
    if (document.querySelector('[data-spanish-professional-register-banner]')) return;
    const main = document.querySelector('main'); if (!main) return;
    const section = document.createElement('section');
    section.dataset.spanishProfessionalRegisterBanner = '20260825';
    section.style.cssText = 'background:#13252d;color:#fff;padding:1.15rem 0;border-bottom:1px solid rgba(255,255,255,.14)';
    section.innerHTML = `<div class="shell" style="display:flex;gap:1rem;align-items:center;justify-content:space-between;flex-wrap:wrap"><div><strong>${isEn?'Spanish counsel, professionals and court-derived owner network':'Abogados, profesionales y red judicial de propietarios'}</strong><div style="font-size:.9rem;line-height:1.45;opacity:.88;margin-top:.2rem">${isEn?'Current/former Spanish counsel plus the non-LPB/Matkator owner, claimant and representation network—each classified by source and attribution boundary.':'Abogados españoles actuales/anteriores y la red no-LPB/Matkator de propietarios, demandantes y representantes—cada relación clasificada por fuente y límite.'}</div></div><div style="display:flex;gap:.55rem;flex-wrap:wrap"><a href="${target}" style="display:inline-flex;background:#fff;color:#13252d;border-radius:999px;padding:.65rem .88rem;text-decoration:none;font-weight:900">${isEn?'Professionals →':'Profesionales →'}</a><a href="${ownerNetwork}" style="display:inline-flex;border:1px solid rgba(255,255,255,.5);color:#fff;border-radius:999px;padding:.65rem .88rem;text-decoration:none;font-weight:900">${isEn?'Owner/court network →':'Red propietarios/autos →'}</a></div></div>`;
    const first = main.querySelector(':scope > section:first-of-type');
    if (first) first.insertAdjacentElement('afterend',section); else main.prepend(section);
  };

  const reconcileRows = () => {
    if (!path.endsWith(identityRoute)) return;
    const rows = [...document.querySelectorAll('tr[data-identity-id]')];
    if (!rows.length) return false;
    rows.forEach(row => {
      const id = row.dataset.identityId;
      const nameNode = row.querySelector('.id-name-button strong');
      if (nameNode && overrides[id]) nameNode.textContent = overrides[id];
      if (withdrawn.has(id)) {
        row.dataset.publicDisplay = 'withdrawn-transaction-only';
        row.hidden = true;
        row.setAttribute('aria-hidden','true');
      }
    });
    const status = document.querySelector('[data-registry-status]');
    if (status && !status.dataset.professionalBoundaryAdded) {
      status.dataset.professionalBoundaryAdded = 'true';
      status.insertAdjacentText('beforeend', isEn ? ' Transaction-only contacts withdrawn from the rendered legal-matter list remain subject to separate historical-Git cleanup.' : ' Los contactos exclusivamente transaccionales retirados de la lista jurídica renderizada siguen sujetos a una limpieza histórica separada de Git.');
    }
    return true;
  };

  const start = () => {
    injectBanner();
    if (!reconcileRows() && path.endsWith(identityRoute)) {
      const observer = new MutationObserver(() => { if (reconcileRows()) observer.disconnect(); });
      observer.observe(document.body,{childList:true,subtree:true});
      setTimeout(()=>observer.disconnect(),15000);
    }
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded',start,{once:true}); else start();
})();