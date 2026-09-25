(() => {
  const route = window.location.pathname.replace(/\/+$/, '') + '/';
  const es = route.endsWith('/es/calificacion-concurso-36-2012-vidas-paralelas/');
  const en = route.endsWith('/en/insolvency-classification-parallel-lives/');
  if (!es && !en) return;
  if (document.querySelector('[data-eg49-fiscal-response-20260816]')) return;

  const esc = (s) => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

  const decree3 = `FISCALÍA GENERAL DEL ESTADO
UNIDAD DE DELITOS CONTRA LA ADMINISTRACION PÚBLICA

N.º Expediente de EG: 49/2026
Interesado: GIL MARER
N.º registro salida: 226/2026

DECRETO

ANTECEDENTES

En fecha 3 de junio de 2026 ha tenido entrada en esta Unidad especializada de delitos contra la Administración pública de la Fiscalía General del Estado la comunicación efectuada por D. Gil Marer, por la que se solicita al Fiscal de Sala Coordinador “someter a trazabilidad una solicitud concreta: que se valore la posición fiscal de 2019 [en relación a la calificación del concurso ordinario 36/2012, seguido ante el Juzgado de lo Mercantil nº 1 de Las Palmas] y su posible proyección actual deben mantenerse, revisarse, matizarse, elevarse, derivarse o coordinarse a la vista del conocimiento documental e institucional existente”.

FUNDAMENTOS DE DERECHO

A la vista del marco normativo que regula las funciones del Fiscal de Sala Coordinador de delitos contra la Administración pública (art. 20 de la Ley 50/1981, de 30 de diciembre, por la que se regula el Estatuto Orgánico del Ministerio Fiscal), y de lo dispuesto en la Instrucción FGE 1/2015, 13 de julio, sobre algunas cuestiones en relación con las funciones de los Fiscales de Sala Coordinadores y los Fiscales de Sala Delegados, no cabe sino concluir que el mismo no goza de facultades legales para desarrollar la actuación que se le demanda.

En otro orden de cosas, debe además subrayarse que los procedimientos de deliberación interna a través de los que el Ministerio Fiscal conforma sus criterios de actuación se rigen por lo dispuesto en la Ley 50/1981, de 30 de diciembre, por la que se regula el Estatuto Orgánico del Ministerio Fiscal y el Real Decreto 305/2022, de 3 de mayo, por el que se aprueba el Reglamento del Ministerio Fiscal, sin que éste prevista -ni resulte viable- la intervención de terceros.

Por todo lo anterior,

ACUERDO incoar el presente expediente gubernativo, no acceder a la solicitud formulada por D. Gil Marer el pasado 2 de junio de 2026 (nº registro 323/2026) y el archivo del mismo.

En Madrid, a 3 de junio de 2026.

El Fiscal de Sala Coordinador de la Unidad de Delitos Contra la Administración Pública de la Fiscalía General del Estado

Fdo. Emilio Jesús Sánchez Ulled

Firma digital: 2026.06.03 14:34:38 +02'00'`;

  const decree8 = `FISCALÍA GENERAL DEL ESTADO
UNIDAD DE DELITOS CONTRA LA ADMINISTRACION PÚBLICA

N.º Expediente de EG: 49/2026
Interesado: GIL MARER
N.º registro salida: 230/2026

DECRETO

ANTECEDENTES

En fecha 4 de junio de 2026 ha tenido entrada en esta Unidad especializada de delitos contra la Administración Pública de la Fiscalía General del Estado comunicación efectuada por F. Gil Marer, por la que -en apretada síntesis- se reitera la solicitud previamente efectuada en fecha 3 de junio de 2026, en la que se instaba al Fiscal de Sala Coordinador a “someter a trazabilidad una solicitud concreta: que se valore la posición fiscal de 2019 [en relación a la calificación del concurso ordinario 36/2012, seguido ante el Juzgado Mercantil nº 1 de Las Palmas] y si su posible proyección actual deben mantenerse, revisarse, matizarse, elevarse, derivarse o coordinarse a la vista del conocimiento constitucional e institucional existente”.

Esta última solicitud motivó la incoación por el de Sala Coordinador de delitos contra la Administración Pública del Expediente Gubernativo 49/2026, así como su archivo de plano por Decreto de 3 de junio de 2026, por las siguientes razones:

“A la vista del marco normativo que regula las funciones del Fiscal de Sala Coordinador de delitos contra la Administración pública (art. 20 de la Ley 50/1981, de 30 de diciembre, por la que se regula el Estatuto Orgánico del Ministerio Fiscal), y de lo dispuesto en la Instrucción FGE 1/2015, 13 de julio, sobre algunas cuestiones en relación con las funciones de los Fiscales de Sala Coordinadores y los Fiscales de Sala Delegados, no cabe sino concluir que el mismo no goza de facultades legales para desarrollar la actuación que se le demanda.

En otro orden de cosas, debe además subrayarse que los procedimientos de deliberación interna a través de los que el Ministerio Fiscal conforma sus criterios de actuación se rigen por lo dispuesto en la Ley 50/1981, de 30 de diciembre, por la que se regula el Estatuto Orgánico del Ministerio Fiscal y el Real Decreto 305/2022, de 3 de mayo, por el que se aprueba el Reglamento del Ministerio Fiscal, sin que éste prevista -ni resulte viable- la intervención de terceros.”

FUNDAMENTOS DE DERECHO

Las razones que el pasado 3 de junio de 2026 motivaron el archivo de la solicitud formulada en aquella misma fecha por D. Gil Marer justifican que ahora se adopte idéntica decisión, pues la nueva solicitud formulada en fecha 4 de junio de 2026 se limita a reiterar la anterior petición sin añadir datos o elementos novedosos que justifiquen revisar la conclusión previamente alcanzada.

Por todo lo anterior,

ACUERDO reabrir el expediente gubernativo nº 49/2026 al objeto de acumular la solicitud formulada en fecha 4 de junio de 2026 por D. Gil Marer, no acceder a la nueva solicitud efectuada por el peticionario y proceder de nuevo al archivo del expediente.

En Madrid, a 8 de junio de 2026.

El Fiscal de Sala Coordinador de la Unidad de Delitos Contra la Administración Pública de la Fiscalía General del Estado

Fdo. Emilio Jesús Sánchez Ulled

Firma digital: 2026.06.09 11:23:52 +02'00'`;

  const t = es ? {
    eyebrow: 'FUENTE PRIMARIA · FISCALÍA GENERAL DEL ESTADO · EG 49/2026',
    title: 'La respuesta de Fiscalía, íntegra, y la pregunta textual que no responde',
    intro: 'Publicamos la transcripción íntegra de los dos decretos localizados de EG 49/2026. Fiscalía sí respondió: no es correcto describir este episodio como silencio. Pero la respuesta fue sobre competencia, procedimiento interno y archivo; no resolvió la cuestión textual ni reexaminó en el fondo el dictamen fiscal de 12 de marzo de 2019.',
    doc3: 'Decreto de 3 JUN 2026 · salida 226/2026',
    doc8: 'Decreto de 8 JUN 2026 · salida 230/2026 · firmado digitalmente 9 JUN',
    open: 'Leer transcripción íntegra',
    fidelity: 'Control de fidelidad: la transcripción se ha obtenido de los PDF nativos recibidos desde la cuenta oficial de Fiscalía. Los PDF originales permanecen preservados en custodia probatoria privada. SHA-256: 3 JUN = 4e5d3486cc052ea699029a8744e21a2040918f4e03a085cc066a3b6ff8f12b88 · 8 JUN = 32a06dbf5745edc2e7ea6f9c88a22231d8238ce1e1a9faa5418db2eab253a383.',
    qTitle: 'Nuestra pregunta textual sigue sin respuesta',
    qLead: 'El dictamen firmado el 12 de marzo de 2019 por Ricardo de Mosteyrín Sampalo contiene literalmente esta frase:',
    quote: '“situación de insolvencia agravada por dolo o culpa del administrador concursal”',
    question: '¿Es “administrador concursal” un error material o de redacción? Si lo es, ¿qué sujeto debía figurar? Si no lo es, ¿por qué el dictamen atribuye literalmente la agravación al dolo o culpa del administrador concursal y después identifica como responsables a Gil Marer y Uri Omid?',
    scope: '<strong>Lo que los decretos sí responden:</strong> el Fiscal de Sala Coordinador dice carecer de facultades legales para realizar la actuación solicitada; invoca además el régimen interno de deliberación del Ministerio Fiscal y archiva. <strong>Lo que no responden:</strong> si “administrador concursal” es un error; cuál era el sujeto pretendido; si el dictamen de 2019 debe corregirse; ni cuál es hoy la valoración de fondo, proposición por proposición, de sus motivos tras la evidencia posterior. Esto es una <em>discordancia documentada de alcance de la respuesta</em>, no silencio.',
    selfTitle: 'Qué queremos decir por “el informe contra sí mismo”',
    selfBody: 'Es una abreviatura editorial, no una afirmación de que un documento pueda “autoincriminarse” jurídicamente. Significa que el propio informe acusatorio de 47 páginas de la Administración Concursal contiene hechos que matizan, debilitan o contradicen partes de su propia narrativa acusatoria. Ejemplos: reproduce cooperación expresa de Gil; recoge vías de rescate/recapitalización/operadores; reconoce diarios PDF y balances ya recibidos; y en tres ramas legales dice que nada constaba. Radical transparencia exige poner esos hechos al lado de la acusación, igual que exige publicar los extremos que sí perjudican a Gil y los que la Sentencia 163/2023 sí mantuvo.'
  } : {
    eyebrow: 'PRIMARY SOURCE · SPANISH PROSECUTION SERVICE · EG 49/2026',
    title: 'The Fiscalía response, in full, and the textual question it does not answer',
    intro: 'We publish full transcriptions of the two located EG 49/2026 decrees. Fiscalía did respond: this episode should not be described as silence. But the response addressed competence, internal procedure and closure; it did not resolve the textual issue or conduct a fresh merits review of the 12 March 2019 prosecutorial opinion.',
    doc3: 'Decree 3 JUN 2026 · outgoing 226/2026',
    doc8: 'Decree 8 JUN 2026 · outgoing 230/2026 · digitally signed 9 JUN',
    open: 'Read full transcription',
    fidelity: 'Fidelity control: the transcription was produced from the native PDFs received from the official Fiscalía account. The original PDFs remain preserved in private evidence custody. SHA-256: 3 JUN = 4e5d3486cc052ea699029a8744e21a2040918f4e03a085cc066a3b6ff8f12b88 · 8 JUN = 32a06dbf5745edc2e7ea6f9c88a22231d8238ce1e1a9faa5418db2eab253a383.',
    qTitle: 'Our textual question remains unanswered',
    qLead: 'The opinion signed on 12 March 2019 by Ricardo de Mosteyrín Sampalo literally contains this phrase:',
    quote: '“situación de insolvencia agravada por dolo o culpa del administrador concursal”',
    question: 'Is “insolvency administrator” a material or drafting error? If it is, which subject was intended? If it is not, why does the opinion literally attribute aggravation to the intent or fault of the insolvency administrator and then identify Gil Marer and Uri Omid as responsible?',
    scope: '<strong>What the decrees do answer:</strong> the Coordinating Chamber Prosecutor says he lacks legal authority to perform the requested action; he also invokes the Fiscalía’s internal deliberative regime and closes the file. <strong>What they do not answer:</strong> whether “insolvency administrator” is an error; which subject was intended; whether the 2019 opinion should be corrected; or the current proposition-by-proposition merits assessment after the later evidence. That is a <em>documented scope mismatch</em>, not silence.',
    selfTitle: 'What we mean by “the report against itself”',
    selfBody: 'It is editorial shorthand, not a claim that a document can legally “incriminate itself”. It means the insolvency administrator’s own adverse 47-page report contains facts that qualify, weaken or contradict parts of its accusatory framing. Examples: it reproduces Gil’s express cooperation; records rescue/recapitalisation/operator avenues; acknowledges PDF journals and trial balances already received; and says nothing was known/alleged under three statutory branches. Radical transparency requires placing those facts beside the accusation, just as it requires publishing the material adverse to Gil and the findings Judgment 163/2023 did retain.'
  };

  const style = document.createElement('style');
  style.textContent = `
    [data-eg49-fiscal-response-20260816]{margin:2.2rem 0;padding:1.4rem;border:1px solid rgba(120,120,120,.28);border-radius:18px;background:rgba(127,127,127,.045)}
    [data-eg49-fiscal-response-20260816] .eg49-eyebrow{font-size:.76rem;letter-spacing:.08em;font-weight:800;opacity:.72}
    [data-eg49-fiscal-response-20260816] h2{margin:.45rem 0 .7rem;font-size:clamp(1.45rem,3vw,2.15rem)}
    [data-eg49-fiscal-response-20260816] .eg49-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:1rem;margin:1.15rem 0}
    [data-eg49-fiscal-response-20260816] .eg49-card,[data-eg49-fiscal-response-20260816] .eg49-aside{padding:1rem;border:1px solid rgba(120,120,120,.25);border-radius:14px;background:var(--card-bg,rgba(127,127,127,.04))}
    [data-eg49-fiscal-response-20260816] details summary{cursor:pointer;font-weight:800;margin:.35rem 0}
    [data-eg49-fiscal-response-20260816] pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit;font-size:.9rem;line-height:1.5;padding:.8rem;background:rgba(127,127,127,.055);border-radius:10px}
    [data-eg49-fiscal-response-20260816] .eg49-quote{font-size:1.08rem;font-weight:800;padding:.8rem 1rem;border-left:4px solid currentColor;margin:.75rem 0}
    [data-eg49-fiscal-response-20260816] .eg49-hash{font-size:.76rem;overflow-wrap:anywhere;opacity:.76}
  `;
  document.head.appendChild(style);

  const section = document.createElement('section');
  section.dataset.eg49FiscalResponse20260816 = 'true';
  section.innerHTML = `
    <div class="eg49-eyebrow">${t.eyebrow}</div>
    <h2>${t.title}</h2>
    <p>${t.intro}</p>
    <div class="eg49-grid">
      <article class="eg49-card"><h3>${t.doc3}</h3><p>EG 49/2026 · Emilio Jesús Sánchez Ulled</p><details><summary>${t.open}</summary><pre>${esc(decree3)}</pre></details></article>
      <article class="eg49-card"><h3>${t.doc8}</h3><p>EG 49/2026 · Emilio Jesús Sánchez Ulled</p><details><summary>${t.open}</summary><pre>${esc(decree8)}</pre></details></article>
    </div>
    <p class="eg49-hash">${t.fidelity}</p>
    <aside class="eg49-aside"><h3>${t.qTitle}</h3><p>${t.qLead}</p><div class="eg49-quote">${t.quote}</div><p><strong>${t.question}</strong></p><p>${t.scope}</p></aside>
    <aside class="eg49-aside" style="margin-top:1rem"><h3>${t.selfTitle}</h3><p>${t.selfBody}</p></aside>
  `;

  const anchor = document.querySelector('[data-calificacion-radical-20260816]') || document.querySelector('main article') || document.querySelector('main');
  if (anchor && anchor.parentNode) anchor.insertAdjacentElement('afterend', section);
})();