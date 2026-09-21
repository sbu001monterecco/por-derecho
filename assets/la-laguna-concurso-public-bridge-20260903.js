(() => {
  'use strict';
  const path = window.location.pathname.replace(/\/+$/, '/') || '/';
  const match = path.match(/^\/por-derecho\/(es|en)\/(cuatrecasas-sun-park|etj-163-2020|dp-748-2026|cambiario-1048-2019|cuatrecasas-dp748-transparencia-2026|cuatrecasas-dp748-transparency-2026)\//);
  if (!match || document.getElementById('pd-la-laguna-concurso-bridge-20260903')) return;

  const lang = match[1];
  const en = lang === 'en';
  const base = '/por-derecho/';
  const mapHref = en ? `${base}en/la-laguna-concurso-map-2026/` : `${base}es/la-laguna-concurso-mapa-2026/`;
  const etjHref = `${base}${lang}/etj-163-2020/`;
  const dpHref = `${base}${lang}/dp-748-2026/`;
  const cambHref = `${base}${lang}/cambiario-1048-2019/`;
  const cuaHref = `${base}${lang}/cuatrecasas-sun-park/`;
  const dpSource = `${base}docs/cuatrecasas/DP748/2026-09-01_auto_16jul2026_fulltext_source_safe.md`;
  const etjSource = `${base}docs/cuatrecasas/ETJ163/2026-09-03_cuatrecasas_impugnacion_reposicion_fulltext_source_safe.md`;

  const section = document.createElement('section');
  section.id = 'pd-la-laguna-concurso-bridge-20260903';
  section.setAttribute('aria-label', en ? 'La Laguna to Concurso 36/2012 public-source bridge' : 'Puente público La Laguna a Concurso 36/2012');
  section.innerHTML = en ? `
    <div class="shell" style="max-width:1180px">
      <div style="border:1px solid #dfe3e3;border-top:6px solid #315f80;border-radius:18px;background:#fff;padding:1.25rem 1.35rem;margin:1.6rem 0">
        <p style="margin:.1rem 0 .35rem;font-size:.76rem;font-weight:800;letter-spacing:.05em;text-transform:uppercase;color:#80621d">Public-source bridge · updated 3 September 2026</p>
        <h2 style="margin:.2rem 0 .65rem">La Laguna ⇄ Sun Park / Concurso 36/2012</h2>
        <p style="max-width:980px">The public record now connects the legally separate proceedings without conflating them: <strong>Cambiario 1048/2019 → ETJ 163/2020 ⇄ DP 748/2026</strong>, alongside the documented Cuatrecasas mandate, finca 8584 and the wider Sun Park/Concurso history.</p>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.75rem;margin:.9rem 0">
          <div style="padding:.9rem;border-radius:13px;background:#eef8f4"><strong>PROVED · procedural lineage</strong><br>Cambiario creates the monetary title; ETJ enforces it; DP 748 is the separate criminal lane alleging autonomous conduct linked to that enforcement.</div>
          <div style="padding:.9rem;border-radius:13px;background:#fffaf0"><strong>ALLEGATION · primary check pending</strong><br>Matkator's filed 5 May 2025 nullity application raises the known-contact / service-by-edict issue. It is not a judicial finding.</div>
          <div style="padding:.9rem;border-radius:13px;background:#fff7f5"><strong>SOURCE GAP · insolvency effect</strong><br>Assignee/beneficiary, any Acosta Matos/HNT link, direct estate effect and shared purpose remain unproved.</div>
        </div>
        <p><strong>1 Sep:</strong> the 16 July DP 748 order maintained provisional dismissal but expressly preserved reopening with other indicia. <strong>3 Sep:</strong> Cuatrecasas told the ETJ court that adjudication is immediately pending and requested power to assign the auction award to a third party. No completed assignment or recipient is proved.</p>
        <p style="font-size:.91rem"><strong>Counter-evidence retained:</strong> genuine unpaid fees, 2018 promissory notes for invoices/costs and direct collection efforts are documented. The public question is therefore not “no debt”, but the regularity of the title/enforcement route and any later materially misleading act.</p>
        <p style="font-size:.91rem"><strong>Boundary:</strong> the site does not state that ETJ is legally inside Concurso 36/2012, that finca 8584 belongs to LPB's estate, or that any named third party is the adjudicatee or beneficiary.</p>
        <p style="display:flex;flex-wrap:wrap;gap:.55rem"><a href="${mapHref}"><strong>Open the full interconnection map</strong></a><span>·</span><a href="${cambHref}">Cambiario</a><span>·</span><a href="${etjHref}">ETJ</a><span>·</span><a href="${dpHref}">DP 748</a><span>·</span><a href="${cuaHref}">Cuatrecasas</a><span>·</span><a href="${dpSource}">16 July order</a><span>·</span><a href="${etjSource}">3 September filing</a></p>
        <p style="font-size:.82rem;color:#53636a;margin-bottom:0">Sources already received/filed and procedural status are public. Concrete arguments for future filings are not published before filing.</p>
      </div>
    </div>` : `
    <div class="shell" style="max-width:1180px">
      <div style="border:1px solid #dfe3e3;border-top:6px solid #315f80;border-radius:18px;background:#fff;padding:1.25rem 1.35rem;margin:1.6rem 0">
        <p style="margin:.1rem 0 .35rem;font-size:.76rem;font-weight:800;letter-spacing:.05em;text-transform:uppercase;color:#80621d">Puente público source-first · actualizado 3 septiembre 2026</p>
        <h2 style="margin:.2rem 0 .65rem">La Laguna ⇄ Sun Park / Concurso 36/2012</h2>
        <p style="max-width:980px">El registro público conecta ahora los procedimientos jurídicamente separados sin confundirlos: <strong>Cambiario 1048/2019 → ETJ 163/2020 ⇄ DP 748/2026</strong>, junto con el mandato documentado de Cuatrecasas, finca 8584 y la historia más amplia de Sun Park/Concurso.</p>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:.75rem;margin:.9rem 0">
          <div style="padding:.9rem;border-radius:13px;background:#eef8f4"><strong>PROBADO · linaje procesal</strong><br>Cambiario forma el título monetario; ETJ lo ejecuta; DP 748 es la vía penal separada que alega conductas autónomas vinculadas a esa ejecución.</div>
          <div style="padding:.9rem;border-radius:13px;background:#fffaf0"><strong>ALEGACIÓN · comprobación primaria pendiente</strong><br>La nulidad de Matkator presentada el 5 mayo 2025 plantea la cuestión contacto conocido / emplazamiento edictal. No es un hallazgo judicial.</div>
          <div style="padding:.9rem;border-radius:13px;background:#fff7f5"><strong>SOURCE GAP · efecto concursal</strong><br>Cesionario/beneficiario, eventual vínculo Acosta Matos/HNT, efecto directo sobre la masa y propósito compartido siguen sin probarse.</div>
        </div>
        <p><strong>1 sep:</strong> el Auto de DP 748 firmado el 16 julio mantuvo el sobreseimiento provisional pero preservó expresamente la reapertura con otros indicios. <strong>3 sep:</strong> Cuatrecasas dijo al órgano ETJ que la adjudicación es el acto inmediatamente pendiente y pidió facultad de ceder el remate a un tercero. No se acredita cesión consumada ni destinatario.</p>
        <p style="font-size:.91rem"><strong>Contraprueba conservada:</strong> están documentados honorarios reales impagados, pagarés de 2018 para facturas/costes y esfuerzos directos de cobro. La cuestión pública no es, por tanto, “no había deuda”, sino la regularidad de la formación del título, la vía ejecutiva y cualquier acto materialmente engañoso posterior.</p>
        <p style="font-size:.91rem"><strong>Límite:</strong> el sitio no afirma que ETJ esté jurídicamente dentro de Concurso 36/2012, que finca 8584 pertenezca a la masa de LPB ni que un tercero determinado sea adjudicatario o beneficiario.</p>
        <p style="display:flex;flex-wrap:wrap;gap:.55rem"><a href="${mapHref}"><strong>Abrir mapa completo de interconexión</strong></a><span>·</span><a href="${cambHref}">Cambiario</a><span>·</span><a href="${etjHref}">ETJ</a><span>·</span><a href="${dpHref}">DP 748</a><span>·</span><a href="${cuaHref}">Cuatrecasas</a><span>·</span><a href="${dpSource}">Auto 16 julio</a><span>·</span><a href="${etjSource}">Escrito 3 septiembre</a></p>
        <p style="font-size:.82rem;color:#53636a;margin-bottom:0">Se publican las fuentes ya recibidas/presentadas y el estado procesal. La argumentación concreta de próximos escritos no se publica antes de su presentación.</p>
      </div>
    </div>`;

  const main = document.querySelector('main');
  if (!main) return;
  const hero = main.querySelector('section');
  if (hero && hero.nextSibling) main.insertBefore(section, hero.nextSibling);
  else main.prepend(section);
})();