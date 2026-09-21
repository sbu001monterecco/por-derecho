(() => {
  'use strict';
  const path = location.pathname.replace(/\/index\.html$/, '/');
  const relevant = path.includes('/es/reclamacion-caixabank-valencia/') || path.includes('/en/caixabank-valencia-claim/');
  if (!relevant || path.includes('/senalamiento-28-enero-2027/') || document.querySelector('[data-borja-witness-claimant-clarification]')) return;

  const isEnglish = document.documentElement.lang === 'en' || path.includes('/en/');
  const main = document.querySelector('main');
  if (!main) return;

  const style = document.createElement('style');
  style.dataset.borjaWitnessClaimantClarificationStyle = '20260904';
  style.textContent = `
    [data-borja-witness-claimant-clarification]{margin:1.1rem auto;border:2px solid #8c1d18;border-left-width:8px;background:#fff8f6;border-radius:16px;padding:1.1rem 1.2rem;box-shadow:0 10px 28px rgba(20,30,35,.08)}
    [data-borja-witness-claimant-clarification] .kicker{margin:0 0 .35rem;color:#8c1d18;font-weight:950;letter-spacing:.08em;text-transform:uppercase;font-size:.72rem}
    [data-borja-witness-claimant-clarification] h2{margin:.1rem 0 .65rem;font-size:clamp(1.45rem,3vw,2.2rem);line-height:1.05}
    [data-borja-witness-claimant-clarification] p{line-height:1.55;margin:.55rem 0}
    [data-borja-witness-claimant-clarification] blockquote{margin:.8rem 0;padding:.8rem 1rem;background:#fff;border-left:5px solid #13252d;font-size:1.12rem;font-weight:850}
    [data-borja-witness-claimant-clarification] .status{display:inline-block;margin-top:.55rem;padding:.32rem .58rem;border-radius:999px;background:#13252d;color:#fff;font-size:.69rem;font-weight:900;letter-spacing:.04em}
  `;
  document.head.append(style);

  const section = document.createElement('section');
  section.className = 'shell';
  section.dataset.borjaWitnessClaimantClarification = '20260904';
  section.setAttribute('aria-label', isEnglish ? 'Claimant clarification on Borja witness attribution' : 'Aclaración de la parte actora sobre la atribución del testigo Borja');

  section.innerHTML = isEnglish ? `
    <p class="kicker">ATTRIBUTION CORRECTION · GIL MARER STATEMENT · 4 SEPTEMBER 2026</p>
    <h2>Formal joint proposal does not mean Aweswell positively chose Borja as its witness.</h2>
    <p><strong>Court-record fact:</strong> the later court citation formally records Francisco de Borja Rodríguez-Batllori Laffitte as a witness proposed by both claimant and defendant. That procedural fact is preserved.</p>
    <p><strong>Claimant-side provenance and statement:</strong> claimant records identify CaixaBank as the party that sought his testimony. Gil Marer states, speaking for himself and the claimant legal team, that Aweswell did not want, independently select or positively endorse Borja as its witness. The claimant side reluctantly adhered because it was under pressure from several parallel proceedings and did not want to risk prejudicing the Valencia case, antagonising the court or creating an avoidable procedural problem.</p>
    <blockquote>“We needed him like a hole in the head.” — Gil Marer, informal description of the claimant side's position</blockquote>
    <p><strong>Mandatory synthesis:</strong> CaixaBank sought Borja's testimony; the court later recorded him procedurally as proposed by both sides after claimant adherence. Gil Marer states that adherence was reluctant and procedural, not affirmative witness sponsorship, endorsement or reliance.</p>
    <span class="status">COURT-RECORD FACT + CLAIMANT FIRST-PERSON CLARIFICATION</span>
  ` : `
    <p class="kicker">CORRECCIÓN DE ATRIBUCIÓN · DECLARACIÓN DE GIL MARER · 4 SEPTIEMBRE 2026</p>
    <h2>La propuesta formal conjunta no significa que Aweswell eligiera positivamente a Borja como testigo propio.</h2>
    <p><strong>Hecho del expediente judicial:</strong> la cédula posterior registra formalmente a Francisco de Borja Rodríguez-Batllori Laffitte como testigo propuesto por la parte actora y demandada. Ese hecho procesal se conserva.</p>
    <p><strong>Procedencia documental y declaración de la actora:</strong> los registros de la parte actora identifican a CaixaBank como quien solicitó su testimonio. Gil Marer declara, hablando por sí mismo y por el equipo jurídico de la actora, que Aweswell no quería, no seleccionó de forma independiente ni respaldó positivamente a Borja como testigo propio. La actora se adhirió de forma renuente porque estaba sometida a la presión simultánea de varios procedimientos y no quiso asumir el riesgo de perjudicar el asunto de Valencia, incomodar al Juzgado o crear un problema procesal evitable.</p>
    <blockquote>“Lo necesitábamos como un agujero en la cabeza.” — Gil Marer, descripción informal de la posición de la actora</blockquote>
    <p><strong>Síntesis obligatoria:</strong> CaixaBank pidió el testimonio de Borja; después el Juzgado lo registró procesalmente como propuesto por ambas partes tras la adhesión de la actora. Gil Marer declara que esa adhesión fue renuente y procesal, no patrocinio, respaldo ni confianza afirmativa en ese testigo.</p>
    <span class="status">HECHO DEL EXPEDIENTE + ACLARACIÓN EN PRIMERA PERSONA DE LA ACTORA</span>
  `;

  const anchor = document.querySelector('#caixabank-borja-witness-control') || document.querySelector('#caixabank-concurso-cam-linkage') || main.querySelector(':scope > section:first-of-type');
  if (anchor) anchor.insertAdjacentElement('afterend', section);
  else main.prepend(section);
})();
