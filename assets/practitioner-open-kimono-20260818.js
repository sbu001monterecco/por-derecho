(() => {
  const path = location.pathname.replace(/\/+$/, '/');
  const isEn = /\/en\//.test(path);
  const t = (es, en) => isEn ? en : es;
  const root = `/por-derecho/${isEn ? 'en' : 'es'}/`;

  const make = (html) => {
    const template = document.createElement('template');
    template.innerHTML = html.trim();
    return template.content.firstElementChild;
  };

  const ensureCss = () => {
    if (document.querySelector('link[data-open-kimono-css]')) return;
    const current = document.currentScript;
    if (!current) return;
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = new URL('practitioner-open-kimono-20260818.css?v=20260818b', current.src).href;
    link.dataset.openKimonoCss = '20260818';
    document.head.appendChild(link);
  };

  const hero = () => document.querySelector('main > .dossier-hero, main > .cnmv-hero, main > .hero, main > section.hero');

  const patchRicpeIdentity = () => {
    if (!/\/ric-private-equity-sun-park\/$/.test(path)) return;
    document.querySelectorAll('[data-ricpe-archive-banner]').forEach(node => node.remove());
    const eyebrow = document.querySelector('.dossier-hero .eyebrow');
    if (eyebrow) eyebrow.textContent = t(
      'Comunicación formal presentada · 17 agosto 2026 · registro unitario',
      'Formal communication submitted · 17 August 2026 · unitary record'
    );
  };

  const patchKnowledgeWording = () => {
    const main = document.querySelector('main');
    if (!main) return;
    const walker = document.createTreeWalker(main, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(node => {
      const parent = node.parentElement;
      if (!parent || /SCRIPT|STYLE|CODE/.test(parent.tagName)) return;
      let value = node.nodeValue || '';
      value = value
        .replace(/Qué sabía RICPE/g, 'Qué documentó RICPE internamente')
        .replace(/qué sabía RICPE/g, 'qué documentó RICPE internamente')
        .replace(/What RICPE knew/g, 'What RICPE documented internally')
        .replace(/what RICPE knew/g, 'what RICPE documented internally');
      node.nodeValue = value;
    });
  };

  const patchFundingNumbers = () => {
    const main = document.querySelector('main');
    if (!main) return;
    const walker = document.createTreeWalker(main, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(node => {
      const parent = node.parentElement;
      if (!parent || /SCRIPT|STYLE|CODE/.test(parent.tagName)) return;
      let value = node.nodeValue || '';
      if (isEn && value.includes('€6,573,703.10') && !value.includes('€6,570,713.56')) {
        value = value.replace(/€6,573,703\.10/g, '€6,570,713.56 (20-Sep-2023 prospectus) / €6,573,703.10 (separate accounts reconstruction; €2,989.54 difference open)');
      }
      if (!isEn && value.includes('€6.573.703,10') && !value.includes('€6.570.713,56')) {
        value = value.replace(/€6\.573\.703,10/g, '€6.570.713,56 (folleto 20-sep-2023) / €6.573.703,10 (reconstrucción separada de cuentas; diferencia €2.989,54 abierta)');
      }
      node.nodeValue = value;
    });
  };

  const practiceType = () => {
    if (/ric-private-equity-sun-park|ricpe-responsabilidad-documental|ricpe-documentary-accountability/.test(path)) return 'ricpe';
    if (/cadena-instrumentalizacion-ric-fondos-incentivos|institutionalisation-chain-ric-eu-incentives|mismo-hotel-multiples-vidas-financieras|same-hotel-multiple-financial-lives|intervencion-general-siinf/.test(path)) return 'funds';
    if (/reconstruccion-unitaria-autoridades-publicas|public-authority-unitary-case-reconstruction/.test(path)) return 'authority';
    return null;
  };

  const practiceCopy = (type) => {
    if (type === 'ricpe') return {
      title: t('Expediente abierto: así se ve una revisión corporativa supervisable.', 'Open file: what a supervisable corporate review looks like.'),
      intro: t('“Open kimono” significa mostrar el itinerario real de decisión: quién originó, quién verificó, quién conoció la reserva, quién se abstuvo, qué cambió y qué documento permitió avanzar. No exige publicar información protegida; exige que la decisión sea reconstruible por un tercero competente.', '“Open kimono” means showing the real decision trail: who originated, who checked, who received the reservation, who recused, what changed and which record allowed progression. It does not require publishing protected material; it requires a decision a competent third party can reconstruct.'),
      good: [
        t('Declaración de parte relacionada, conflicto y abstención, persona por persona.', 'Related-party, conflict and recusal record, person by person.'),
        t('Due diligence, valoración, reservas, condiciones y dispensas fechadas y aprobadas.', 'Dated and approved due diligence, valuation, reservations, conditions and waivers.'),
        t('Memoria contemporánea que explique julio de 2021 → reentrada.', 'A contemporaneous memorandum explaining July 2021 → re-entry.'),
        t('Cifras vinculadas a su fuente: €6.570.713,56 y €6.573.703,10 no se normalizan.', 'Figures tied to source: €6,570,713.56 and €6,573,703.10 are not normalised.'),
        t('Evidencia contraria y correctora tratada con la misma visibilidad.', 'Contrary and corrective evidence given equal visibility.')
      ],
      bad: [
        t('El resultado final —MYND abierto— usado como validación retrospectiva.', 'The final outcome —MYND open— used as retrospective validation.'),
        t('Actas o aprobaciones inaccesibles, sin custodios, versiones o trazas.', 'Inaccessible approvals without custodians, versions or audit trail.'),
        t('Conflicto tratado como biografía, no como control formal.', 'Conflict treated as biography rather than a formal control.'),
        t('Presentación, recepción, examen y decisión fusionados en una sola palabra.', 'Submission, receipt, review and decision collapsed into one status.'),
        t('Silencio utilizado como exoneración o culpabilidad.', 'Silence used as exoneration or guilt.')
      ]
    };
    if (type === 'funds') return {
      title: t('Expediente abierto: así se audita dinero público sin prejuzgar.', 'Open file: how public money is audited without prejudgment.'),
      intro: t('La mejor práctica no empieza por “hubo fraude” ni termina en “eran instrumentos distintos”. Empieza por beneficiario, activo, título, coste elegible, factura, pago, empleo, otra financiación, verificación, certificación y eventual corrección o reintegro.', 'Best practice does not start with “there was fraud” or end with “the instruments were different”. It starts with beneficiary, asset, title, eligible cost, invoice, payment, employment, other financing, verification, certification and any correction or recovery.'),
      good: [
        t('Mapa finca/derecho y perímetro físico de la operación.', 'Property/right map and physical operation perimeter.'),
        t('Source-and-use consolidado con cada instrumento y cada factura.', 'Consolidated source-and-use by instrument and invoice.'),
        t('Empleo definido por persona, empleador, periodo y FTE.', 'Employment defined by person, employer, period and FTE.'),
        t('Concesión, pago, elegibilidad final, verificación y cierre separados.', 'Award, payment, final eligibility, verification and closure separated.'),
        t('Incidencias, correcciones y reintegros preservados, también cuando exoneran.', 'Issues, corrections and recoveries preserved, including exculpatory outcomes.')
      ],
      bad: [
        t('Placa FEDER tratada como expediente completo.', 'An ERDF plaque treated as the complete file.'),
        t('Concesión tratada como pago y cumplimiento final.', 'An award treated as payment and final compliance.'),
        t('Personas jurídicas distintas usadas para evitar la conciliación económica.', 'Separate legal persons used to avoid economic reconciliation.'),
        t('Empleos sumados sin población, periodo o definición.', 'Jobs added without population, period or definition.'),
        t('Ausencia de tabla de otras ayudas, acumulación, facturas y pagos.', 'No table of other aid, cumulation, invoices and payments.')
      ]
    };
    return {
      title: t('Expediente abierto: una autoridad muestra qué recibió, qué comprobó y qué decidió.', 'Open file: an authority shows what it received, checked and decided.'),
      intro: t('La transparencia institucional útil no consiste en publicar secretos o datos personales. Consiste en una cadena auditable de recepción, competencia, verificación, evidencia contraria, decisión, remisión y estado, sin apropiarse de la competencia de otro órgano.', 'Useful institutional transparency is not publication of secrets or personal data. It is an auditable chain of receipt, competence, verification, contrary evidence, decision, referral and status, without appropriating another authority’s competence.'),
      good: [
        t('Pregunta limitada al ámbito legal del órgano.', 'A question limited to the body’s lawful remit.'),
        t('Documento primario, proposición exacta y límite probatorio.', 'Primary record, exact proposition and evidential boundary.'),
        t('Registro de qué se verificó de forma independiente y qué se heredó.', 'A record of what was independently checked and what was inherited.'),
        t('Remisión documentada sin presentarla como decisión de fondo.', 'Documented referral not presented as a merits decision.'),
        t('Corrección pública cuando cambia una fecha, cifra o estado.', 'Public correction when a date, figure or status changes.')
      ],
      bad: [
        t('Repetición institucional tratada como verificación independiente.', 'Institutional repetition treated as independent verification.'),
        t('Registro, acuse, análisis y cierre convertidos en una caja negra.', 'Registration, acknowledgment, analysis and closure turned into a black box.'),
        t('Una autoridad utilizada para validar hechos fuera de su competencia.', 'One authority used to validate facts outside its competence.'),
        t('Evidencia adversa omitida o degradada.', 'Adverse evidence omitted or downgraded.'),
        t('Silencio o secreto legal convertido en conclusión de mérito.', 'Silence or lawful secrecy converted into a merits conclusion.')
      ]
    };
  };

  const addPractice = () => {
    if (document.getElementById('open-kimono-practice')) return;
    if (/cnmv-ricpe-verificacion|cnmv-ricpe-verification|snca-fondos-europeos-trazabilidad|snca-eu-funds-traceability|incentivos-regionales-gc836-p06|regional-incentives-gc836-p06/.test(path)) return;
    const type = practiceType();
    if (!type) return;
    if (type === 'ricpe' && /ric-private-equity-sun-park/.test(path) && !document.getElementById('psr-ricpe-cockpit')) return;
    const copy = practiceCopy(type);
    const section = make(`
      <section class="ok-practice" id="open-kimono-practice" aria-labelledby="open-kimono-title">
        <div class="shell">
          <p class="ok-kicker">${t('OPEN KIMONO · INSPIRACIÓN DE BUENA SUPERVISIÓN', 'OPEN KIMONO · GOOD SUPERVISORY PRACTICE')}</p>
          <h2 id="open-kimono-title">${copy.title}</h2>
          <p class="ok-intro">${copy.intro}</p>
          <div class="ok-two">
            <article class="ok-panel ok-good"><span class="ok-status verified">${t('Modelo positivo', 'Positive model')}</span><h3>${t('Buenas prácticas que el expediente invita a aplicar', 'Good practice the file invites')}</h3><ul>${copy.good.map(item => `<li>${item}</li>`).join('')}</ul></article>
            <article class="ok-panel ok-bad"><span class="ok-status open">${t('Advertencia', 'Warning')}</span><h3>${t('La práctica opuesta: señales de un expediente no supervisable', 'The opposite: warning signs of an unsupervisable file')}</h3><ul>${copy.bad.map(item => `<li>${item}</li>`).join('')}</ul></article>
          </div>
          <p class="ok-boundary"><strong>${t('Límite:', 'Boundary:')}</strong> ${t('este contraste no afirma que una institución o persona haya incurrido en todas las prácticas negativas. Proporciona un test público y falsable para evaluar el expediente real.', 'this contrast does not assert that an institution or person engaged in every negative practice. It provides a public, falsifiable test for the actual file.')}</p>
          <div class="ok-actions"><a href="${root}${isEn ? 'public-authority-unitary-case-reconstruction/' : 'reconstruccion-unitaria-autoridades-publicas/'}">${t('Abrir sala limpia institucional', 'Open institutional clean room')}</a><a class="secondary" href="${root}${isEn ? 'regional-incentives-gc836-p06/' : 'incentivos-regionales-gc836-p06/'}">${t('Práctica de Incentivos Regionales', 'Regional Incentives practice')}</a><a class="secondary" href="${root}${isEn ? 'snca-eu-funds-traceability/' : 'snca-fondos-europeos-trazabilidad/'}">${t('Práctica de fondos UE', 'EU-funds practice')}</a></div>
        </div>
      </section>`);
    const cockpit = document.getElementById('psr-ricpe-cockpit');
    if (cockpit) cockpit.insertAdjacentElement('afterend', section);
    else {
      const targetHero = hero();
      if (targetHero) targetHero.insertAdjacentElement('afterend', section);
      else document.querySelector('main')?.insertAdjacentElement('afterbegin', section);
    }
  };

  const addCrossAuthorityMatrix = () => {
    if (!/reconstruccion-unitaria-autoridades-publicas|public-authority-unitary-case-reconstruction/.test(path)) return;
    if (document.getElementById('open-kimono-authority-matrix')) return;
    const section = make(`
      <section class="ok-practice" id="open-kimono-authority-matrix" aria-labelledby="authority-matrix-title">
        <div class="shell">
          <p class="ok-kicker">${t('MATRIZ DE DEPENDENCIAS · QUIÉN PUEDE COMPROBAR QUÉ', 'DEPENDENCY MATRIX · WHO CAN CHECK WHAT')}</p>
          <h2 id="authority-matrix-title">${t('Una misma premisa factual; competencias y decisiones distintas.', 'One factual premise; different competences and decisions.')}</h2>
          <p class="ok-intro">${t('La repetición de una premisa entre expedientes no sustituye su verificación primaria. Esta matriz dirige cada cuestión al órgano que dispone del registro o la competencia correspondiente.', 'Repetition of a proposition across files does not replace primary verification. This matrix directs each question to the body holding the relevant record or competence.')}</p>
          <div class="ok-matrix-wrap"><table class="ok-matrix"><thead><tr><th>${t('Órgano / función', 'Body / function')}</th><th>${t('Pregunta finita', 'Finite question')}</th><th>${t('Registro que debería resolverla', 'Record that should resolve it')}</th><th>${t('No decide por sí solo', 'Does not decide by itself')}</th><th>${t('Ruta', 'Route')}</th></tr></thead><tbody>
            <tr><td>CNMV</td><td>${t('Información, gobierno, conflictos, DD, reentrada y financiación RICPE.', 'RICPE information, governance, conflicts, DD, re-entry and funding.')}</td><td>${t('Expediente supervisor + archivos internos de la entidad.', 'Supervisory file + entity internal records.')}</td><td>${t('Título civil o elegibilidad de una subvención.', 'Civil title or grant eligibility.')}</td><td><a href="${root}${isEn ? 'cnmv-ricpe-verification/' : 'cnmv-ricpe-verificacion/'}">CNMV →</a></td></tr>
            <tr><td>RICPE</td><td>${t('Quién originó, aprobó, se abstuvo, dispensó y desembolsó.', 'Who originated, approved, recused, waived and drew funds.')}</td><td>${t('Comité, Consejo, DD, valoración, contratos, drawdowns.', 'Committee, Board, DD, valuation, contracts and drawdowns.')}</td><td>${t('Regularidad de otro expediente público.', 'Regularity of another public file.')}</td><td><a href="${root}${isEn ? 'ric-private-equity-sun-park/' : 'ric-private-equity-sun-park/'}">RICPE →</a></td></tr>
            <tr><td>${t('Incentivos Regionales', 'Regional Incentives')}</td><td>${t('Beneficiario, disponibilidad, inversión elegible, otras ayudas, empleo y liquidación.', 'Beneficiary, availability, eligible investment, other aid, jobs and settlement.')}</td><td>GC/836/P06</td><td>${t('Delito o propiedad universal del hotel.', 'Crime or universal ownership of the hotel.')}</td><td><a href="${root}${isEn ? 'regional-incentives-gc836-p06/' : 'incentivos-regionales-gc836-p06/'}">GC/836/P06 →</a></td></tr>
            <tr><td>FEDER / ERDF</td><td>${t('Operación, gasto certificado, cofinanciación, pago, indicadores y correcciones.', 'Operation, certified expenditure, co-financing, payment, indicators and corrections.')}</td><td>${t('Sistema de gestión, certificación y auditoría.', 'Management, accounting/certification and audit systems.')}</td><td>${t('Lo que no figure en la placa o publicidad.', 'Anything not shown by the plaque or publicity.')}</td><td><a href="${root}${isEn ? 'snca-eu-funds-traceability/' : 'snca-fondos-europeos-trazabilidad/'}">${t('Fondos UE', 'EU funds')} →</a></td></tr>
            <tr><td>SNCA / IGAE</td><td>${t('Recepción, verificación, remisión, preservación y resultado antifraude/control.', 'Intake, checks, referral, preservation and anti-fraud/control outcome.')}</td><td>${t('Infofraude, REG-AGE, expedientes de control y remisión.', 'Infofraud, REG-AGE, control and referral files.')}</td><td>${t('Aceptación automática de la denuncia.', 'Automatic acceptance of the report.')}</td><td><a href="${root}${isEn ? 'snca-eu-funds-traceability/' : 'snca-fondos-europeos-trazabilidad/'}">SNCA →</a></td></tr>
            <tr><td>AEAT / RIC</td><td>${t('Materialización, activo, valoración, mantenimiento y compatibilidad fiscal.', 'Materialisation, asset, valuation, holding period and tax compatibility.')}</td><td>${t('Expediente RIC, informes y declaraciones.', 'RIC file, reports and returns.')}</td><td>${t('Título civil de cada finca o elegibilidad FEDER.', 'Civil title to each unit or ERDF eligibility.')}</td><td><a href="${root}${isEn ? 'institutionalisation-chain-ric-eu-incentives/' : 'cadena-instrumentalizacion-ric-fondos-incentivos/'}">RIC →</a></td></tr>
            <tr><td>${t('Juzgado / AC', 'Court / Insolvency Administrator')}</td><td>${t('Masa LPB, autoridad, conocimiento y efecto sobre valor/activos.', 'LPB estate, authority, knowledge and effect on value/assets.')}</td><td>${t('Concurso 36/2012 y comunicaciones del AC.', 'Insolvency 36/2012 and administrator communications.')}</td><td>${t('Bienes extraconcursales por arrastre.', 'Extra-insolvency assets by implication.')}</td><td><a href="${root}${isEn ? 'insolvency-36-2012-institutional-accountability/' : 'concurso-36-2012-responsabilidad-institucional/'}">${t('Concurso', 'Insolvency')} →</a></td></tr>
            <tr><td>${t('Catastro / Registro', 'Cadastre / Registry')}</td><td>${t('Referencia, finca, titular, alteración y perímetro en fecha concreta.', 'Reference, unit, holder, alteration and perimeter at a given date.')}</td><td>${t('Catastro, Registro, escrituras y planos.', 'Cadastre, Registry, deeds and plans.')}</td><td>${t('Control financiero, subvención o intención.', 'Financial control, grant compliance or intent.')}</td><td>${t('Fuente especializada', 'Specialist source')}</td></tr>
          </tbody></table></div>
          <p class="ok-warning"><strong>${t('Advertencia:', 'Warning:')}</strong> ${t('si cada órgano hereda la misma premisa sin volver al documento de origen, la acumulación de sellos puede amplificar una afirmación no verificada. Eso es una hipótesis de control a comprobar, no una conclusión de connivencia.', 'if each body inherits the same proposition without returning to the originating record, accumulated institutional stamps can amplify an unverified assertion. That is a control hypothesis to test, not a conclusion of collusion.')}</p>
        </div>
      </section>`);
    const institution = document.getElementById('por-institucion');
    if (institution) institution.insertAdjacentElement('beforebegin', section);
    else document.querySelector('main')?.insertAdjacentElement('beforeend', section);
  };

  const apply = () => {
    ensureCss();
    patchRicpeIdentity();
    patchKnowledgeWording();
    patchFundingNumbers();
    addPractice();
    addCrossAuthorityMatrix();
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => setTimeout(apply, 900), { once: true });
  else setTimeout(apply, 900);
  setTimeout(apply, 1800);
  setTimeout(apply, 3200);
})();