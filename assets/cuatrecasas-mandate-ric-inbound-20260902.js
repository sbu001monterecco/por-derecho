(() => {
  const path = window.location.pathname.replace(/\/+$/, '');
  if (path.includes('/cuatrecasas-mandate-ric-continuity') || path.includes('/cuatrecasas-mandato-continuidad-ric')) return;

  const eligible = [
    'cuatrecasas-sun-park',
    'cuatrecasas-dp748-civil-action',
    'cuatrecasas-dp748-accion-civil',
    'reverse-engineering-360-sun-park-chain',
    'ingenieria-inversa-360-cadena-sun-park',
    'unitary-record',
    'registro-unitario',
    'ric-private-equity-sun-park',
    'ricpe-cnmv-dossier-2021',
    'cnmv-ricpe-verification',
    'same-hotel-multiple-financial-lives',
    'mismo-hotel-multiples-vidas-financieras',
    'public-authority-unitary-case-reconstruction',
    'master-proceedings-register',
    'registro-maestro-procedimientos'
  ];
  if (!eligible.some(slug => path.includes('/' + slug))) return;
  if (document.querySelector('[data-cuatrecasas-mandate-ric-inbound="20260902"]')) return;

  const isEs = /\/es\//.test(path);
  const bridge = isEs ? '../cuatrecasas-mandato-continuidad-ric/' : '../cuatrecasas-mandate-ric-continuity/';
  const etj = isEs ? '../cuatrecasas-dp748-accion-civil/' : '../cuatrecasas-dp748-civil-action/';
  const record = '../../evidence/cuatrecasas/2026-09-02-mandate-inversion-execution-perimeter.json';

  let context;
  if (path.includes('dp748') || path.includes('civil-action') || path.includes('accion-civil')) {
    context = isEs
      ? 'Distinción de control: el remate actual se refiere a una sola finca (8.584), mientras la ejecución dineraria identifica a Matkator como ejecutada. El nuevo puente separa el bien actualmente realizado del perímetro patrimonial potencial de la deuda y del impacto económico indirecto sobre Aweswell.'
      : 'Control distinction: the current remate concerns one property (8,584), while the monetary enforcement identifies Matkator as executed debtor. The new bridge separates the asset presently realised from the potential debtor-wide patrimonial perimeter and the indirect economic impact on Aweswell.';
  } else if (path.includes('ric') || path.includes('cnmv') || path.includes('financial-lives') || path.includes('vidas-financieras')) {
    context = isEs
      ? 'El nuevo puente conecta el aviso RIC/CNMV de 2021 con el mandato Sun Park preexistente sin retrotraer conocimiento de incentivos o fondos posteriores, y añade la inversión del mandato mediante la ejecución frente a Matkator.'
      : 'The new bridge connects the 2021 RIC/CNMV notice to the pre-existing Sun Park mandate without backdating knowledge of later incentives or funding, and adds the mandate-inversion issue created by enforcement against Matkator.';
  } else {
    context = isEs
      ? 'El nuevo puente muestra una sola arquitectura: mandato Aweswell → hostigamiento hotelero/Sun Park → Concurso LPB como workstream → instrumentos de honorarios/Matkator → ETJ → aviso RIC/CNMV → financiación posterior.'
      : 'The new bridge shows one architecture: Aweswell mandate → Sun Park/hotel-mobbing record → LPB insolvency as a workstream → fee instruments/Matkator → ETJ → RIC/CNMV notice → later funding.';
  }

  const section = document.createElement('section');
  section.className = 'section';
  section.setAttribute('data-cuatrecasas-mandate-ric-inbound', '20260902');
  section.innerHTML = `
    <div class="shell" style="max-width:1160px">
      <div style="background:linear-gradient(135deg,#10272f,#183f45 65%,#73551c);color:#fff;border-radius:20px;padding:1.2rem 1.3rem;box-shadow:0 16px 36px rgba(16,39,47,.16)">
        <p style="margin:0 0 .35rem;color:#f1d37e;font-size:.76rem;font-weight:800;letter-spacing:.05em;text-transform:uppercase">${isEs ? 'NUEVO PUENTE UNITARIO · 2 SEP 2026' : 'NEW UNITARY BRIDGE · 2 SEP 2026'}</p>
        <h2 style="color:#fff;margin:.2rem 0 .55rem">${isEs ? 'Mandato → ejecución Matkator → continuidad RIC/CNMV' : 'Mandate → Matkator enforcement → RIC/CNMV continuity'}</h2>
        <p style="color:#edf4f2;margin:.4rem 0 1rem;line-height:1.55">${context}</p>
        <p style="margin:.4rem 0"><a href="${bridge}" style="display:inline-block;background:#f1d37e;color:#10272f;text-decoration:none;font-weight:800;border-radius:999px;padding:.55rem .85rem">${isEs ? 'Abrir archivo puente →' : 'Open bridge file →'}</a> <a href="${etj}" style="display:inline-block;color:#fff;font-weight:700;margin-left:.6rem">${isEs ? 'ETJ / acción civil →' : 'ETJ / civil action →'}</a> <a href="${record}" style="display:inline-block;color:#fff;font-weight:700;margin-left:.6rem">${isEs ? 'Registro canónico →' : 'Canonical record →'}</a></p>
        <p style="font-size:.82rem;color:#dce7e5;margin:.8rem 0 0">${isEs ? 'Límite: Matkator es la ejecutada; Aweswell no se convierte por ello automáticamente en ejecutada ni quedan sus bienes propios sujetos a embargo sin base jurídica independiente.' : 'Boundary: Matkator is the executed debtor; Aweswell does not thereby automatically become an executed debtor and its separate assets are not exposed without an independent legal basis.'}</p>
      </div>
    </div>`;

  const main = document.querySelector('main');
  if (!main) return;
  const hero = main.querySelector('section');
  if (hero && hero.nextSibling) main.insertBefore(section, hero.nextSibling);
  else main.prepend(section);
})();