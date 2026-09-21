(() => {
  'use strict';

  const path = window.location.pathname.replace(/\/+$/, '');
  const esPath = '/por-derecho/es/calificacion-concurso-36-2012-vidas-paralelas';
  const enPath = '/por-derecho/en/insolvency-classification-parallel-lives';
  const isEs = path.endsWith(esPath);
  const isEn = path.endsWith(enPath);
  if (!isEs && !isEn) return;

  const css = `
    #canonical-calificacion-map{background:#eef2f1;border-top:1px solid rgba(19,37,45,.12);border-bottom:1px solid rgba(19,37,45,.12)}
    #canonical-calificacion-map .ccm-shell{max-width:1080px;margin:0 auto;padding:3.2rem 1.25rem}
    #canonical-calificacion-map .ccm-eyebrow{font-size:.78rem;letter-spacing:.09em;text-transform:uppercase;font-weight:800;color:#6b5841;margin:0 0 .55rem}
    #canonical-calificacion-map h2{font-size:clamp(1.8rem,3vw,2.65rem);line-height:1.08;margin:.2rem 0 .8rem;color:#13252d}
    #canonical-calificacion-map h3{margin:.2rem 0 .6rem;color:#13252d}
    #canonical-calificacion-map p{line-height:1.62}
    #canonical-calificacion-map .ccm-status{background:#13252d;color:#fff;border-radius:18px;padding:1.25rem 1.35rem;margin:1rem 0 1.25rem;box-shadow:0 10px 28px rgba(19,37,45,.12)}
    #canonical-calificacion-map .ccm-status strong{display:block;font-size:.82rem;letter-spacing:.07em;text-transform:uppercase;color:#e5d29e;margin-bottom:.45rem}
    #canonical-calificacion-map .ccm-status p{margin:.35rem 0}
    #canonical-calificacion-map .ccm-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.9rem;margin:1rem 0}
    #canonical-calificacion-map .ccm-card{background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:15px;padding:1rem;border-top:5px solid #13252d}
    #canonical-calificacion-map .ccm-card.fiscal{border-top-color:#8c6b2f}
    #canonical-calificacion-map .ccm-card.court{border-top-color:#526b59}
    #canonical-calificacion-map .ccm-card .ccm-label{display:block;font-size:.72rem;letter-spacing:.07em;text-transform:uppercase;font-weight:800;color:#6b5841;margin-bottom:.3rem}
    #canonical-calificacion-map .ccm-card p:last-child{margin-bottom:0}
    #canonical-calificacion-map .ccm-note{background:#f3efe4;border-left:5px solid #8c6b2f;border-radius:13px;padding:1rem 1.1rem;margin:1rem 0}
    #canonical-calificacion-map .ccm-note.strong{background:#fff;border:2px solid #13252d;border-left-width:6px}
    #canonical-calificacion-map .ccm-note p:last-child{margin-bottom:0}
    #canonical-calificacion-map details{background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:14px;margin:.8rem 0;overflow:hidden}
    #canonical-calificacion-map summary{cursor:pointer;font-weight:800;padding:1rem 1.1rem;color:#13252d;background:#fafafa}
    #canonical-calificacion-map details[open] summary{border-bottom:1px solid rgba(19,37,45,.12)}
    #canonical-calificacion-map .ccm-detail{padding:1rem 1.1rem}
    #canonical-calificacion-map .ccm-detail ol,#canonical-calificacion-map .ccm-detail ul{padding-left:1.25rem}
    #canonical-calificacion-map .ccm-detail li{margin:.45rem 0;line-height:1.5}
    #canonical-calificacion-map .ccm-table-wrap{overflow-x:auto;margin:1rem 0}
    #canonical-calificacion-map table{border-collapse:separate;border-spacing:0;width:100%;min-width:820px;font-size:.91rem}
    #canonical-calificacion-map th,#canonical-calificacion-map td{padding:.72rem .7rem;vertical-align:top;text-align:left;border-right:1px solid #dfe3e3;border-bottom:1px solid #dfe3e3;line-height:1.45}
    #canonical-calificacion-map th{background:#13252d;color:#fff}
    #canonical-calificacion-map th:first-child{border-top-left-radius:11px}
    #canonical-calificacion-map th:last-child{border-top-right-radius:11px}
    #canonical-calificacion-map td:first-child{border-left:1px solid #dfe3e3;font-weight:700}
    #canonical-calificacion-map tr:last-child td:first-child{border-bottom-left-radius:11px}
    #canonical-calificacion-map tr:last-child td:last-child{border-bottom-right-radius:11px}
    #canonical-calificacion-map .ccm-pill{display:inline-block;border-radius:999px;padding:.17rem .48rem;font-size:.68rem;letter-spacing:.04em;text-transform:uppercase;font-weight:800;white-space:nowrap}
    #canonical-calificacion-map .ccm-pill.rejected{background:#e2ebe5;color:#243d2c}
    #canonical-calificacion-map .ccm-pill.narrowed{background:#eee5d4;color:#5d4921}
    #canonical-calificacion-map .ccm-pill.adverse{background:#f0ddda;color:#6c2e27}
    #canonical-calificacion-map .ccm-pill.none{background:#e9ecec;color:#465255}
    #canonical-calificacion-map .ccm-people{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.9rem;margin:1rem 0}
    #canonical-calificacion-map .ccm-person{background:#fff;border:1px solid rgba(19,37,45,.16);border-radius:15px;padding:1rem}
    #canonical-calificacion-map .ccm-person h3{border-bottom:1px solid rgba(19,37,45,.12);padding-bottom:.55rem}
    #canonical-calificacion-map .ccm-person ul{padding-left:1.15rem}
    #canonical-calificacion-map .ccm-person li{margin:.42rem 0;line-height:1.45}
    #canonical-calificacion-map .ccm-source{font-size:.9rem;color:#4d585b}
    #canonical-calificacion-map .ccm-linkrow{display:flex;gap:.6rem;flex-wrap:wrap;margin-top:1rem}
    #canonical-calificacion-map .ccm-linkrow a{display:inline-block;border:1px solid #13252d;border-radius:999px;padding:.48rem .78rem;text-decoration:none;font-weight:700;color:#13252d;background:#fff}
    #canonical-calificacion-map .ccm-linkrow a:hover{background:#13252d;color:#fff}
    @media(max-width:860px){#canonical-calificacion-map .ccm-grid,#canonical-calificacion-map .ccm-people{grid-template-columns:1fr}#canonical-calificacion-map .ccm-shell{padding:2.5rem 1rem}}
  `;

  const spanish = `
    <div class="ccm-shell">
      <p class="ccm-eyebrow">MAPA CANÓNICO · AC → FISCALÍA → SENTENCIA → PERSONA → APELACIÓN</p>
      <h2>Qué se alegó, qué se decidió y por qué no puede presentarse como un único bloque validado</h2>
      <p>Esta síntesis se apoya en el informe completo de la administración concursal de 11 de febrero de 2019; el dictamen fiscal de 12 de marzo de 2019; las oposiciones separadas de LPB y Gil Marer y la oposición conjunta de PINK y Patricia; la Sentencia 163/2023; y tres instrumentos de apelación para cuatro intereses apelantes: Gil Marer, PINK y Patricia conjuntamente, y LPB. Separa la acusación original de lo que el juzgado rechazó, redujo o mantuvo.</p>

      <div class="ccm-status" role="note" aria-label="Estado procesal actual">
        <strong>Estado procesal — materialmente adverso y recurrido</strong>
        <p>La Sentencia 163/2023 declaró culpable el concurso de LPB e impuso consecuencias graves a Gil Marer y PINK. El recurso RPL 2523/2025 está ante la Sección Cuarta de la Audiencia Provincial de Las Palmas.</p>
        <p>Una providencia señaló el <strong>4 de junio de 2026</strong> para deliberación y fallo. En la comprobación finita realizada en Gmail y Google Drive hasta el <strong>17 de agosto de 2026</strong> no se localizó sentencia de apelación ni resolución de terminación. Eso no demuestra que no exista. La resolución de primera instancia no se presenta aquí como firme ni como condena penal.</p>
        <p>Las copias presentadas de los recursos de Gil y de PINK/Patricia están localizadas. La presentación del recurso separado de LPB el 2 de noviembre de 2023 está respaldada por el correo contemporáneo de su letrado y por la posterior cadena del depósito, pero todavía no se ha localizado su PDF presentado ni su justificante de presentación.</p>
      </div>

      <div class="ccm-note strong">
        <h3>Las tres correcciones que el lector debe retener</h3>
        <p><strong>Gil no fue declarado responsable de la presentación tardía.</strong> El juzgado la atribuyó exclusivamente al anterior administrador, Uri Omid.</p>
        <p><strong>PINK fue declarada cómplice únicamente en el bloque de rentas.</strong> No fue condenada por contabilidad, presentación tardía, colaboración ni por ninguno de los dos bloques de alzamiento.</p>
        <p><strong>“Connivencia” tuvo tratamientos distintos.</strong> El juzgado la consideró no corroborada en el bloque de alzamiento, pero la infirió en el bloque separado de rentas y complicidad. Ninguna de esas dos frases puede trasladarse a la otra rama.</p>
      </div>

      <div class="ccm-grid" aria-label="Tres niveles institucionales">
        <article class="ccm-card">
          <span class="ccm-label">11 febrero 2019 · AC</span>
          <h3>Una acusación amplia</h3>
          <p>Francisco de Borja Rodríguez-Batllori sostuvo una falta general de colaboración, créditos no reclamados, rentas PINK impagadas, incumplimiento contable, dos teorías de alzamiento, presentación tardía y otras presunciones. Solicitó 15 años para Gil, €3.032.010,34, cobertura del déficit y complicidad de PINK y Patricia.</p>
        </article>
        <article class="ccm-card fiscal">
          <span class="ccm-label">12 marzo 2019 · Ministerio Fiscal</span>
          <h3>Cinco epígrafes en dos páginas</h3>
          <p>El Fiscal pidió culpabilidad por agravación de la insolvencia, irregularidades contables, alzamiento, presentación tardía y falta de colaboración; identificó a Uri y Gil como responsables y a Patricia y PINK como cómplices, y pidió 15 años, daños y déficit.</p>
        </article>
        <article class="ccm-card court">
          <span class="ccm-label">28 septiembre 2023 · Sentencia 163/2023</span>
          <h3>Estimación parcial, no validación total</h3>
          <p>El juzgado rechazó ramas sustanciales, corrigió la construcción de €737.338,85, redujo la colaboración y mantuvo hallazgos adversos sobre rentas, libros contables y una falta documental más estrecha.</p>
        </article>
      </div>

      <details>
        <summary>Inventario completo de las alegaciones de la administración concursal</summary>
        <div class="ccm-detail">
          <ol>
            <li><strong>Marco general de falta de colaboración:</strong> habría impedido conocer con precisión las causas económicas de la insolvencia.</li>
            <li><strong>Créditos frente a terceros:</strong> Sun Energy Spaces (€101.724,93); saldos de clientes (€518.908,69), incluidos €4.891,93, €41.516,76 y €472.500; y el crédito/dividendo CEXP de €737.338,85.</li>
            <li><strong>Contrato de explotación y rentas PINK:</strong> renta aproximada de €24.575 mensuales, impago, falta de reclamación o resolución y daños pedidos por €3.032.010,34.</li>
            <li><strong>Incumplimiento sustancial contable:</strong> insuficiencia o falta de legalización de libros obligatorios, aunque el propio informe registró diarios y balances en PDF de 2008–2011 y parte de 2012.</li>
            <li><strong>Documentos falsos o inexactitudes graves:</strong> el AC dijo no conocer hechos relevantes bajo este epígrafe.</li>
            <li><strong>Convenio fallido y liquidación:</strong> contexto procesal; no terminó siendo una causa personal autónoma contra Gil.</li>
            <li><strong>Primer alzamiento:</strong> inexistencia de bienes embargables de PINK en España, posible cobro en Inglaterra o por una matriz británica y continuación de actividad en “connivencia”.</li>
            <li><strong>Segundo alzamiento:</strong> depósito/saldo de €19.140,25 supuestamente dispuesto en perjuicio de acreedores.</li>
            <li><strong>Salidas fraudulentas de bienes:</strong> el AC dijo no conocer hechos relevantes bajo este epígrafe.</li>
            <li><strong>Situación patrimonial ficticia:</strong> el AC dijo no conocer hechos relevantes bajo este epígrafe.</li>
            <li><strong>Presentación tardía del concurso.</strong></li>
            <li><strong>Falta de colaboración específica:</strong> libros sociales, escrituras, soportes, extractos y documentación de créditos.</li>
            <li><strong>Cuentas anuales:</strong> falta de formulación, auditoría, aprobación o depósito.</li>
            <li><strong>Personas y consecuencias:</strong> Uri y Gil afectados; PINK y Patricia como cómplices; daños y déficit.</li>
          </ol>
          <p class="ccm-source">La publicación completa debe mostrar también los epígrafes en los que el AC no formuló una acusación, para no ensanchar retrospectivamente su informe.</p>
        </div>
      </details>

      <details>
        <summary>Qué alegó exactamente el Fiscal y la contradicción literal de su primer epígrafe</summary>
        <div class="ccm-detail">
          <p>El dictamen fiscal de dos páginas enumeró:</p>
          <ol>
            <li>una “situación de insolvencia agravada por dolo o culapa del administrador concursal”;</li>
            <li>irregularidades relevantes en la contabilidad;</li>
            <li>alzamiento de bienes;</li>
            <li>incumplimiento del plazo para solicitar el concurso; y</li>
            <li>incumplimiento del deber de colaboración con la administración concursal.</li>
          </ol>
          <p>La primera frase atribuye literalmente la agravación al <strong>administrador concursal</strong>, pero el mismo escrito identifica después como responsables a los administradores sociales. Puede ser un error de redacción. El hecho verificado es el texto; el error, por sí solo, no prueba intención.</p>
          <p>El dictamen no contiene una conciliación separada, crédito por crédito y alegación por alegación, de los documentos contrarios ya incorporados al expediente. Gil sostiene que el Fiscal dio autoridad institucional a una acusación máxima sin realizar en el texto firmado una auditoría independiente visible.</p>
        </div>
      </details>

      <div class="ccm-table-wrap" role="region" aria-label="Tratamiento judicial de las alegaciones" tabindex="0">
        <table>
          <thead><tr><th>Bloque</th><th>Lo que decidió la Sentencia 163/2023</th><th>Resultado</th></tr></thead>
          <tbody>
            <tr><td>Créditos frente a terceros</td><td>Rechazó la culpabilidad general: cobrar exigía demanda, estimación y ejecución fructuosa, resultados inciertos. Corrigió la tesis de que €737.338,85 era, en parte, una deuda de LPB consigo misma.</td><td><span class="ccm-pill rejected">Rechazado</span></td></tr>
            <tr><td>Firma del contrato / renta inferior a hipoteca</td><td>Concluyó que la mera firma del contrato o que la renta no cubriera la cuota hipotecaria no bastaban para considerar culpable la conducta.</td><td><span class="ccm-pill narrowed">Reducido</span></td></tr>
            <tr><td>Falta de reclamación de rentas</td><td>Mantuvo que Gil debió reclamar o resolver y que el impago agravó la insolvencia; declaró a PINK cómplice.</td><td><span class="ccm-pill adverse">Adverso · apelado</span></td></tr>
            <tr><td>Libros contables obligatorios</td><td>Mantuvo un incumplimiento sustancial pese al material contable entregado, por considerar ausentes o insuficientes los libros oficiales, en especial el Libro Diario.</td><td><span class="ccm-pill adverse">Adverso · apelado</span></td></tr>
            <tr><td>PINK / Inglaterra / “connivencia” como alzamiento</td><td>Lo rechazó: la conducta se atribuía a PINK, no a LPB; no podía contarse dos veces el impago; y la connivencia alegada no estaba corroborada en esta rama.</td><td><span class="ccm-pill rejected">Rechazado</span></td></tr>
            <tr><td>Depósito de €19.140,25</td><td>Aceptó la explicación sobre financiación, swap y pignoración/restricción de disposición.</td><td><span class="ccm-pill rejected">Rechazado</span></td></tr>
            <tr><td>Presentación tardía</td><td>La atribuyó exclusivamente a Uri. Expresamente excluyó a Gil por su actuación de abril y junio de 2012.</td><td><span class="ccm-pill narrowed">Uri, no Gil</span></td></tr>
            <tr><td>Falta de colaboración</td><td>Reconoció que LPB entregó la documentación contable que poseía. Mantuvo solo la falta de soportes de €518.908,69 y €737.338,85 tras la liquidación.</td><td><span class="ccm-pill narrowed">Reducido · apelado</span></td></tr>
            <tr><td>Formulación/depósito de cuentas anuales</td><td>Rechazó la presunción: constaban las cuentas 2008–2010, el AC reconoció las de 2011 y no probó el no depósito.</td><td><span class="ccm-pill rejected">Rechazado</span></td></tr>
            <tr><td>Patricia como cómplice</td><td>Rechazó la petición por falta de argumentación suficiente en el informe del AC.</td><td><span class="ccm-pill rejected">Rechazado</span></td></tr>
            <tr><td>Cobertura del déficit</td><td>La rechazó porque AC y Fiscal la pidieron sin la justificación causal y cuantitativa necesaria; el juzgado no podía construirla de oficio sin afectar a la defensa.</td><td><span class="ccm-pill rejected">Rechazado</span></td></tr>
          </tbody>
        </table>
      </div>

      <h3>Consecuencias, persona por persona</h3>
      <div class="ccm-people">
        <article class="ccm-person">
          <h3>LPB</h3>
          <ul>
            <li>Su concurso fue declarado culpable.</li>
            <li>Bloques operativos: rentas, libros contables, presentación tardía atribuida a Uri y colaboración documental reducida.</li>
            <li>No fue condenada penalmente.</li>
          </ul>
        </article>
        <article class="ccm-person">
          <h3>Gil Marer</h3>
          <ul>
            <li>Hallazgos adversos: rentas, libros contables y colaboración reducida.</li>
            <li><strong>No</strong> presentación tardía.</li>
            <li>10 años desde firmeza; pérdida de derechos de crédito; €3.032.010,34 más intereses.</li>
            <li>Todo ello está recurrido.</li>
          </ul>
        </article>
        <article class="ccm-person">
          <h3>PINK</h3>
          <ul>
            <li>Cómplice solo en el bloque de rentas.</li>
            <li>Pérdida de derechos de crédito.</li>
            <li>Sin segunda condena duplicada de €3.032.010,34 en esta sentencia.</li>
            <li>No alzamiento, contabilidad, presentación tardía ni colaboración.</li>
          </ul>
        </article>
      </div>

      <div class="ccm-note">
        <h3>La tesis de instrumentalización, formulada con precisión</h3>
        <p>Gil sostiene que la calificación funcionó como un mecanismo de <strong>inversión y desvío de la verdad</strong>: cooperación presentada como obstrucción; créditos inciertos presentados como pérdida culpable; un depósito pignorado presentado como fuga; y esfuerzos de preservación o salida omitidos del marco causal, mientras el control material y el beneficio económico se desplazaban hacia otros actores.</p>
        <p>Lo verificado es la secuencia documental, las contradicciones, las correcciones judiciales y los hallazgos que sobrevivieron. La intención coordinada, la falsedad consciente, la prevaricación o la instrumentalización criminal no han sido declaradas por un tribunal y exigen prueba adicional de conocimiento, capacidad, causalidad y finalidad.</p>
      </div>

      <p class="ccm-source"><strong>Fuentes de control:</strong> informe AC completo (47 páginas); dictamen fiscal (2 páginas); oposición de LPB de 23-abr-2019; oposición de Gil de 6-jun-2019; oposición conjunta PINK/Patricia de 23-mar-2021, presentada por LexNET el 24-mar-2021; Sentencia 163/2023; recurso de Gil; recurso conjunto PINK/Patricia; presentación reportada y cadena del depósito del recurso separado de LPB, pendiente de recuperar su PDF y justificante; providencia de RPL 2523/2025; correos contemporáneos de cooperación, acceso y salida; y los registros canónicos del repositorio. No se publican direcciones, documentos de identidad, teléfonos, emails privados, firmas ni datos bancarios innecesarios.</p>

      <div class="ccm-linkrow">
        <a href="/por-derecho/es/calificacion-concurso-36-2012-vidas-paralelas/conocimiento-previo-rescate/">Conocimiento previo de rescate</a>
        <a href="/por-derecho/es/concurso-36-2012-administrador-concursal/">Administrador concursal</a>
        <a href="/por-derecho/es/concurso-36-2012-ap-seccion-4/">Apelación · Sección Cuarta</a>
        <a href="/por-derecho/es/toma-control-sun-park-7-junio-2018/">Control material · junio 2018</a>
      </div>
    </div>`;

  const english = `
    <div class="ccm-shell">
      <p class="ccm-eyebrow">CANONICAL MAP · AC → PROSECUTION → JUDGMENT → PERSON → APPEAL</p>
      <h2>What was alleged, what was decided, and why the package cannot be presented as wholly validated</h2>
      <p>This summary is grounded in the complete 11 February 2019 insolvency-administrator report; the 12 March 2019 prosecution opinion; the separate LPB and Gil Marer oppositions and the joint PINK/Patricia opposition; Judgment 163/2023; and three appeal instruments covering four appellant interests: Gil Marer, PINK and Patricia jointly, and LPB. It separates the original accusation from what the court rejected, narrowed, or retained.</p>

      <div class="ccm-status" role="note" aria-label="Current procedural status">
        <strong>Procedural status — materially adverse and under appeal</strong>
        <p>Judgment 163/2023 classified LPB’s insolvency as culpable and imposed serious consequences on Gil Marer and PINK. Appeal RPL 2523/2025 is before Section Four of the Las Palmas Provincial Court.</p>
        <p>A procedural order fixed <strong>4 June 2026</strong> for deliberation and judgment. The finite Gmail and Google Drive checks through <strong>17 August 2026</strong> did not locate an appellate judgment or terminating resolution. That does not prove that none exists. The first-instance judgment is not presented here as final or as a criminal conviction.</p>
        <p>The filed copies of the Gil and joint PINK/Patricia appeals are located. LPB’s separate appeal is supported as filed on 2 November 2023 by counsel’s contemporaneous email and the later deposit chain, but its filed PDF and filing receipt have not yet been located.</p>
      </div>

      <div class="ccm-note strong">
        <h3>The three corrections every reader should retain</h3>
        <p><strong>Gil was not held responsible for late filing.</strong> The court attributed that ground exclusively to former administrator Uri Omid.</p>
        <p><strong>PINK was held an accomplice only in the rent branch.</strong> It was not sanctioned for accounting, late filing, cooperation, or either alleged asset-concealment branch.</p>
        <p><strong>“Connivance” received different treatment in different branches.</strong> The court found it uncorroborated in the asset-concealment branch but inferred it in the separate rent/complicity branch. Neither statement can be transferred wholesale to the other branch.</p>
      </div>

      <div class="ccm-grid" aria-label="Three institutional levels">
        <article class="ccm-card">
          <span class="ccm-label">11 February 2019 · Insolvency administrator</span>
          <h3>A broad accusation package</h3>
          <p>Francisco de Borja Rodríguez-Batllori alleged general non-cooperation, unpursued receivables, unpaid PINK rent, accounting breach, two asset-concealment theories, late filing and other presumptions. He sought 15 years for Gil, €3,032,010.34, deficit liability and complicity findings against PINK and Patricia.</p>
        </article>
        <article class="ccm-card fiscal">
          <span class="ccm-label">12 March 2019 · Public Prosecution Service</span>
          <h3>Five headings in two pages</h3>
          <p>The prosecutor requested culpability for aggravated insolvency, accounting irregularities, asset concealment, late filing and non-cooperation; identified Uri and Gil as responsible and Patricia and PINK as accomplices; and sought 15 years, damages and deficit coverage.</p>
        </article>
        <article class="ccm-card court">
          <span class="ccm-label">28 September 2023 · Judgment 163/2023</span>
          <h3>Partial acceptance, not total validation</h3>
          <p>The court rejected major branches, corrected the €737,338.85 construction, narrowed cooperation, and retained adverse findings on rent, official accounting books and a narrower documentary issue.</p>
        </article>
      </div>

      <details>
        <summary>Complete inventory of the insolvency administrator’s allegations</summary>
        <div class="ccm-detail">
          <ol>
            <li><strong>General non-cooperation frame:</strong> allegedly prevented precise identification of the economic causes of insolvency.</li>
            <li><strong>Third-party receivables:</strong> Sun Energy Spaces (€101,724.93); customer balances (€518,908.69), including €4,891.93, €41,516.76 and €472,500; and the €737,338.85 CEXP receivable/dividend.</li>
            <li><strong>PINK operating agreement and rent:</strong> approximate €24,575 monthly rent, non-payment, failure to claim or terminate, and €3,032,010.34 damages sought.</li>
            <li><strong>Substantial accounting breach:</strong> alleged absence or insufficient legalisation of mandatory books, although the report itself recorded PDF journals and trial balances for 2008–2011 and part of 2012.</li>
            <li><strong>False documents or serious inaccuracies:</strong> the administrator said no relevant facts were known under this heading.</li>
            <li><strong>Failed arrangement and liquidation:</strong> procedural context; it did not become a separate operative personal ground against Gil.</li>
            <li><strong>First asset-concealment theory:</strong> no attachable PINK assets in Spain, possible receipts in England/through a UK parent, and continued activity in “connivance”.</li>
            <li><strong>Second asset-concealment theory:</strong> a €19,140.25 deposit/balance allegedly disposed of to creditor prejudice.</li>
            <li><strong>Fraudulent asset exits:</strong> no relevant facts were said to be known.</li>
            <li><strong>Fictitious patrimonial situation:</strong> no relevant facts were said to be known.</li>
            <li><strong>Late filing.</strong></li>
            <li><strong>Specific non-cooperation:</strong> corporate books, deeds, supporting records, bank statements and receivable evidence.</li>
            <li><strong>Annual accounts:</strong> alleged failure to formulate, audit, approve or deposit them.</li>
            <li><strong>Persons and consequences:</strong> Uri and Gil affected; PINK and Patricia as accomplices; damages and deficit coverage.</li>
          </ol>
          <p class="ccm-source">The complete presentation must also show the statutory branches in which the administrator made no factual accusation, so the report is not broadened retrospectively.</p>
        </div>
      </details>

      <details>
        <summary>What the prosecutor actually alleged and the literal contradiction in the first heading</summary>
        <div class="ccm-detail">
          <p>The two-page opinion listed:</p>
          <ol>
            <li>a “situation of insolvency aggravated by intent or fault of the insolvency administrator”;</li>
            <li>relevant accounting irregularities;</li>
            <li>asset concealment;</li>
            <li>failure to request insolvency within the legal period; and</li>
            <li>failure to cooperate with the insolvency administrator.</li>
          </ol>
          <p>The first sentence literally attributes aggravation to the <strong>insolvency administrator</strong>, while the same document then identifies the company administrators as responsible. It may be a drafting error. The verified fact is the text; the error alone does not prove intent.</p>
          <p>The opinion does not contain a separate, receivable-by-receivable and allegation-by-allegation reconciliation of the contrary documents already in the record. Gil alleges that the prosecutor gave institutional authority to a maximum-severity accusation without a visible independent audit in the signed text.</p>
        </div>
      </details>

      <div class="ccm-table-wrap" role="region" aria-label="Judicial treatment of the allegations" tabindex="0">
        <table>
          <thead><tr><th>Branch</th><th>What Judgment 163/2023 decided</th><th>Outcome</th></tr></thead>
          <tbody>
            <tr><td>Third-party receivables</td><td>Rejected general-clause culpability: recovery required litigation, success and effective enforcement, all uncertain. Corrected the theory that €737,338.85 was partly LPB owing itself.</td><td><span class="ccm-pill rejected">Rejected</span></td></tr>
            <tr><td>Signing the agreement / rent below mortgage</td><td>Held that signing the agreement, or rent not covering the mortgage instalment, did not by itself make the conduct culpable.</td><td><span class="ccm-pill narrowed">Narrowed</span></td></tr>
            <tr><td>Failure to claim rent</td><td>Retained the finding that Gil should have claimed or terminated and that non-payment aggravated insolvency; held PINK an accomplice.</td><td><span class="ccm-pill adverse">Adverse · appealed</span></td></tr>
            <tr><td>Mandatory accounting books</td><td>Retained a substantial breach despite material supplied, treating the official books—particularly the Daily Journal—as absent or insufficient.</td><td><span class="ccm-pill adverse">Adverse · appealed</span></td></tr>
            <tr><td>PINK / England / “connivance” as concealment</td><td>Rejected it: the conduct was attributed to PINK, not debtor LPB; rent could not be counted twice; and alleged connivance was uncorroborated in this branch.</td><td><span class="ccm-pill rejected">Rejected</span></td></tr>
            <tr><td>€19,140.25 deposit</td><td>Accepted the financing, swap and pledge/restricted-disposal explanation.</td><td><span class="ccm-pill rejected">Rejected</span></td></tr>
            <tr><td>Late filing</td><td>Attributed it exclusively to Uri. Expressly excluded Gil because of his April and June 2012 steps.</td><td><span class="ccm-pill narrowed">Uri, not Gil</span></td></tr>
            <tr><td>Non-cooperation</td><td>Accepted that LPB delivered the accounting material it possessed. Retained only missing support for €518,908.69 and €737,338.85 after liquidation.</td><td><span class="ccm-pill narrowed">Narrowed · appealed</span></td></tr>
            <tr><td>Annual-account formulation/deposit</td><td>Rejected the presumption: 2008–2010 accounts were filed, 2011 formulation was acknowledged, and non-deposit was not proved.</td><td><span class="ccm-pill rejected">Rejected</span></td></tr>
            <tr><td>Patricia as accomplice</td><td>Rejected for insufficient argumentation in the administrator’s report.</td><td><span class="ccm-pill rejected">Rejected</span></td></tr>
            <tr><td>Deficit liability</td><td>Rejected because the administrator and prosecutor requested it without the necessary causal and quantitative justification; the court would not construct the missing case itself.</td><td><span class="ccm-pill rejected">Rejected</span></td></tr>
          </tbody>
        </table>
      </div>

      <h3>Consequences, person by person</h3>
      <div class="ccm-people">
        <article class="ccm-person">
          <h3>LPB</h3>
          <ul>
            <li>Its insolvency was classified as culpable.</li>
            <li>Operative branches: rent, official accounting books, late filing allocated to Uri, and narrowed documentary non-cooperation.</li>
            <li>It was not criminally convicted.</li>
          </ul>
        </article>
        <article class="ccm-person">
          <h3>Gil Marer</h3>
          <ul>
            <li>Adverse findings: rent, accounting books and narrowed non-cooperation.</li>
            <li><strong>Not</strong> late filing.</li>
            <li>10 years from finality; loss of credit rights; €3,032,010.34 plus interest.</li>
            <li>All remain under appeal.</li>
          </ul>
        </article>
        <article class="ccm-person">
          <h3>PINK</h3>
          <ul>
            <li>Accomplice only in the rent branch.</li>
            <li>Loss of credit rights.</li>
            <li>No duplicated €3,032,010.34 award in this judgment.</li>
            <li>No asset concealment, accounting, late-filing or cooperation finding.</li>
          </ul>
        </article>
      </div>

      <div class="ccm-note">
        <h3>The instrumentalisation thesis, stated precisely</h3>
        <p>Gil alleges that the classification process operated as a mechanism of <strong>truth inversion and truth diversion</strong>: cooperation presented as obstruction; uncertain receivables presented as culpable loss; a pledged deposit presented as flight; and preservation/exit work omitted from the causal frame while practical control and economic benefit moved toward other actors.</p>
        <p>What is verified is the documentary sequence, the contradictions, the judicial corrections and the findings that survived. Coordinated intent, knowing falsehood, judicial misconduct or criminal instrumentalisation have not been adjudicated and require additional proof of knowledge, capacity, causation and purpose.</p>
      </div>

      <p class="ccm-source"><strong>Controlled sources:</strong> complete 47-page administrator report; two-page prosecution opinion; LPB opposition dated 23-Apr-2019; Gil opposition dated 6-Jun-2019; joint PINK/Patricia opposition dated 23-Mar-2021 and filed through LexNET on 24-Mar-2021; Judgment 163/2023; Gil appeal; joint PINK/Patricia appeal; the reported filing and deposit chain for LPB’s separate appeal, with its PDF and receipt still to recover; RPL 2523/2025 procedural order; contemporaneous cooperation, access and exit correspondence; and canonical repository registers. Unnecessary addresses, identity numbers, private phone numbers, emails, signatures and banking details are not published.</p>

      <div class="ccm-linkrow">
        <a href="/por-derecho/en/insolvency-classification-parallel-lives/prior-judicial-knowledge-rescue/">Prior rescue knowledge</a>
        <a href="/por-derecho/en/insolvency-36-2012-insolvency-administrator/">Insolvency administrator</a>
        <a href="/por-derecho/en/insolvency-36-2012-ap-section-4/">Appeal · Section Four</a>
        <a href="/por-derecho/en/sun-park-takeover-7-june-2018/">Material control · June 2018</a>
      </div>
    </div>`;

  const render = () => {
    if (document.getElementById('canonical-calificacion-map')) return;

    const style = document.createElement('style');
    style.id = 'canonical-calificacion-map-style';
    style.textContent = css;
    document.head.appendChild(style);

    const section = document.createElement('section');
    section.id = 'canonical-calificacion-map';
    section.className = 'section';
    section.setAttribute('data-source-control', 'AC-11FEB2019|Fiscal-12MAR2019|Sentencia-163-2023|RPL-2523-2025|17AUG2026');
    section.innerHTML = isEs ? spanish : english;

    const target = document.getElementById('di248');
    if (target && target.parentNode) {
      target.parentNode.insertBefore(section, target);
      return;
    }

    const main = document.querySelector('main');
    if (main) main.appendChild(section);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', render, { once: true });
  } else {
    render();
  }
})();
