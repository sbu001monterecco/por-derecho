(() => {
  const RICPE_PATH = /\/(es|en)\/ric-private-equity-sun-park\/?$/;

  function externalLink(href, label) {
    return `<a href="${href}" rel="external noopener">${label}</a>`;
  }

  function renderRicpeIdentityCorrection() {
    if (!RICPE_PATH.test(window.location.pathname)) return;

    const isSpanish = document.documentElement.lang === 'es';
    const sectionId = isSpanish ? 'identidad-estado-vital-custodia' : 'identity-vital-status-custody';

    const heroEyebrow = document.querySelector('.dossier-hero .eyebrow');
    if (heroEyebrow) {
      heroEyebrow.textContent = isSpanish
        ? 'Registro unitario · actualizado 15 agosto 2026'
        : 'Unified record · updated 15 August 2026';
    }

    const nav = document.querySelector('.main-nav');
    if (nav && !nav.querySelector(`a[href="#${sectionId}"]`)) {
      const link = document.createElement('a');
      link.href = `#${sectionId}`;
      link.textContent = isSpanish ? 'Identidades' : 'Identities';
      const responsibilityLink = nav.querySelector(isSpanish ? 'a[href="#responsabilidad"]' : 'a[href="#responsibility"]');
      nav.insertBefore(link, responsibilityLink || nav.querySelector('.nav-update'));
    }

    const heroActions = document.querySelector('.dossier-hero .actions');
    if (heroActions && !heroActions.querySelector(`a[href="#${sectionId}"]`)) {
      const button = document.createElement('a');
      button.className = 'button secondary';
      button.href = `#${sectionId}`;
      button.textContent = isSpanish ? 'Identidad y custodia' : 'Identity and custody';
      heroActions.appendChild(button);
    }

    document.querySelectorAll('.genealogy-person strong').forEach((strong) => {
      if (strong.textContent.trim() !== 'José Acosta') return;
      const card = strong.closest('.genealogy-person');
      if (!card || card.dataset.identityCorrected === 'true') return;
      card.dataset.identityCorrected = 'true';
      strong.textContent = isSpanish
        ? 'José Acosta / José Daniel Acosta Matos — identidad por certificar'
        : 'José Acosta / José Daniel Acosta Matos — identity to be certified';
      const detail = card.querySelector('span');
      if (detail) {
        detail.textContent = isSpanish
          ? 'RIC publica «José Acosta» como consejero; la CNMV registra «ACOSTA MATOS, JOSÉ» y fuentes públicas identifican a José Daniel Acosta Matos como presidente del Grupo Acosta Matos. La coincidencia es altamente probable, pero debe conciliarse formalmente mediante nombre completo, NIF, nombramiento y aceptación antes de atribuir actos personales.'
          : 'RIC publishes “José Acosta” as a director; the CNMV records “ACOSTA MATOS, JOSÉ”, while public sources identify José Daniel Acosta Matos as president of Grupo Acosta Matos. The match is highly probable, but it must be formally reconciled through full name, tax ID, appointment and acceptance before personal acts are attributed.';
      }
    });

    if (document.getElementById(sectionId)) return;

    const responsibility = document.getElementById(isSpanish ? 'responsabilidad' : 'responsibility');
    const genealogy = document.getElementById(isSpanish ? 'genealogia' : 'genealogy');
    if (!responsibility && !genealogy) return;

    const section = document.createElement('section');
    section.className = 'section';
    section.id = sectionId;
    section.setAttribute('aria-labelledby', `${sectionId}-title`);

    const borme2020 = externalLink(
      'https://www.boe.es/diario_borme/txt.php?id=BORME-A-2020-157-35',
      isSpanish ? 'BORME de agosto de 2020' : 'August 2020 BORME record'
    );
    const borme2024 = externalLink(
      'https://www.boe.es/diario_borme/txt.php?id=BORME-A-2024-32-35',
      isSpanish ? 'BORME de febrero de 2024' : 'February 2024 BORME record'
    );
    const mediaExact = externalLink(
      'https://maspalomas24h.com/art/6002/luto-empresarial-por-la-muerte-de-gerardo-acosta-armas-en-las-palmas',
      isSpanish ? 'información que identifica a Gerardo Acosta Armas' : 'report identifying Gerardo Acosta Armas'
    );
    const mediaVariant = externalLink(
      'https://www.atlanticohoy.com/empresas/gran-canaria-se-viste-luto-despedir-empresario-gerardo-acosta-matos_1528751_102.html',
      isSpanish ? 'titular de prensa con la variante «Gerardo Acosta Matos»' : 'press headline using the variant “Gerardo Acosta Matos”'
    );
    const cnmv = externalLink(
      'https://www.cnmv.es/portal/consultas/ecr/sociedad?nif=A76335900&vista=4',
      isSpanish ? 'registro CNMV de administradores de RICPE' : 'CNMV register of RICPE directors'
    );
    const ey = externalLink(
      'https://www.ey.com/es_es/newsroom/2023/02/jose-daniel-acosta-matos-presidente-grupo-acosta-matos-xxvi-premio-emprendedor-ano-ey-canarias',
      isSpanish ? 'perfil público de José Daniel Acosta Matos' : 'public profile of José Daniel Acosta Matos'
    );

    section.innerHTML = isSpanish ? `
      <div class="shell">
        <div class="section-head">
          <div>
            <p class="kicker">Corrección de identidad · 15 agosto 2026</p>
            <h2 id="${sectionId}-title">Estado vital y custodia: no confundir al fundador fallecido con Gerardo Zacarías Acosta Matos.</h2>
          </div>
          <p>La precisión nominal no es ornamental. Determina a quién puede dirigirse una solicitud, quién podía adoptar una decisión en cada fecha y quién conserva hoy los archivos corporativos.</p>
        </div>

        <aside class="pressure-maxim" role="note" aria-label="Corrección de identidad Gerardo Acosta">
          <strong>Corrección controlada:</strong>
          <span>Las informaciones publicadas el 10–11 de marzo de 2024 se refieren al fundador y antiguo presidente <b>Gerardo Nicanor Acosta Armas</b>. Un titular utilizó la forma «Gerardo Acosta Matos», pero la historia societaria oficial distingue a Gerardo Nicanor de su hijo <b>Gerardo Zacarías Acosta Matos</b>. No se ha localizado en este rastreo un obituario fiable a nombre exacto de Gerardo Zacarías; esa ausencia no prueba por sí sola que viva, conserve capacidad o siga en el cargo.</span>
        </aside>

        <div class="control-table-wrap" role="region" aria-label="Matriz de identidad, estado vital y custodia" tabindex="0">
          <table class="control-table">
            <thead><tr><th>Persona</th><th>Estado documental localizado</th><th>Tratamiento correcto</th></tr></thead>
            <tbody>
              <tr>
                <td><strong>Gerardo Nicanor Acosta Armas</strong></td>
                <td>Fundador del grupo y antiguo presidente de CAM. El ${borme2020} registra su cese como presidente y consejero el 7 de agosto de 2020. Medios publicaron en marzo de 2024 su fallecimiento.</td>
                <td>No se dirige requerimiento personal al fallecido. Sus actos históricos se reconstruyen mediante actas, poderes, correspondencia y contabilidad; la preservación y producción se exige a sucesores, sociedades y custodios actuales.</td>
              </tr>
              <tr>
                <td><strong>Gerardo Zacarías Acosta Matos</strong></td>
                <td>Persona distinta. El ${borme2020} lo identifica dentro del consejo de CAM y el ${borme2024} como vicepresidente y consejero de Grupo Patrimonial Acosta Matos con nombramiento publicado en febrero de 2024.</td>
                <td>No se le describe como fallecido. RICPE y las sociedades pertinentes deben certificar nombre completo, NIF, estado vital cuando sea material, cargos, ceses, poderes, participación en decisiones Sun Park y custodia documental actual.</td>
              </tr>
              <tr>
                <td><strong>José Daniel Acosta Matos</strong><br><small>«José Acosta» / «ACOSTA MATOS, JOSÉ»</small></td>
                <td>El ${cnmv} y la web de RIC utilizan formas abreviadas; el ${ey} identifica a José Daniel al frente del Grupo Acosta Matos. La correspondencia de identidades es altamente probable, pero debe acreditarse formalmente.</td>
                <td>Hasta la conciliación mediante NIF, nombramiento y aceptación no se fusionan identidades como hecho definitivo. Si se confirma, deben producirse declaraciones de conflicto, abstenciones, asistencia, votos, información recibida y participación en decisiones RICPE sobre Sun Park.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="proof-split" role="group" aria-label="Fuentes y deber de custodia">
          <div><strong>Discrepancia mediática documentada</strong><span>Contrástense la ${mediaExact} y el ${mediaVariant}. La variante de un titular no puede prevalecer sobre la identificación societaria oficial ni trasladarse a Gerardo Zacarías.</span></div>
          <div><strong>La muerte no extingue la prueba</strong><span>Deben preservarse nombre/NIF, fechas de cargos, sucesión, representante legal, correos, dispositivos corporativos, actas, poderes, archivos de proyecto, data rooms y migraciones de documentos. El custodio actual debe identificarse aun cuando la persona haya fallecido o la sociedad haya sido reestructurada.</span></div>
        </div>

        <div class="privacy-callout">
          <strong>Frontera probatoria.</strong>
          <span>No se infiere conducta ilícita de un apellido, parentesco, cargo, fallecimiento o sucesión societaria. La atribución es individual y por acto, fecha, capacidad, conocimiento, decisión, omisión y beneficio acreditados. La ausencia de una noticia de fallecimiento tampoco prueba estado vital ni vigencia de un cargo.</span>
        </div>
      </div>
    ` : `
      <div class="shell">
        <div class="section-head">
          <div>
            <p class="kicker">Identity correction · 15 August 2026</p>
            <h2 id="${sectionId}-title">Vital status and custody: do not confuse the deceased founder with Gerardo Zacarías Acosta Matos.</h2>
          </div>
          <p>Name precision is not cosmetic. It determines who can receive a demand, who could make a decision at each date and who now holds the corporate record.</p>
        </div>

        <aside class="pressure-maxim" role="note" aria-label="Gerardo Acosta identity correction">
          <strong>Controlled correction:</strong>
          <span>Reports published on 10–11 March 2024 concerned founder and former president <b>Gerardo Nicanor Acosta Armas</b>. One headline used “Gerardo Acosta Matos”, but the official corporate history distinguishes Gerardo Nicanor from his son <b>Gerardo Zacarías Acosta Matos</b>. This scan found no reliable exact-name obituary for Gerardo Zacarías; that absence does not itself prove that he is alive, capable or still in office.</span>
        </aside>

        <div class="control-table-wrap" role="region" aria-label="Identity, vital status and custody matrix" tabindex="0">
          <table class="control-table">
            <thead><tr><th>Person</th><th>Located documentary status</th><th>Correct treatment</th></tr></thead>
            <tbody>
              <tr>
                <td><strong>Gerardo Nicanor Acosta Armas</strong></td>
                <td>Group founder and former CAM president. The ${borme2020} records his cessation as president and director on 7 August 2020. Media reported his death in March 2024.</td>
                <td>No personal demand is addressed to the deceased. His historical acts are reconstructed through minutes, powers, correspondence and accounts; preservation and production are directed to successors, companies and present custodians.</td>
              </tr>
              <tr>
                <td><strong>Gerardo Zacarías Acosta Matos</strong></td>
                <td>A different person. The ${borme2020} identifies him on CAM's board and the ${borme2024} records him as vice-president and director of Grupo Patrimonial Acosta Matos in February 2024.</td>
                <td>He is not described as deceased. RICPE and the relevant companies should certify full name, tax ID, vital status where material, offices, cessations, powers, participation in Sun Park decisions and present record custody.</td>
              </tr>
              <tr>
                <td><strong>José Daniel Acosta Matos</strong><br><small>“José Acosta” / “ACOSTA MATOS, JOSÉ”</small></td>
                <td>The ${cnmv} and RIC's website use abbreviated forms; the ${ey} identifies José Daniel as head of Grupo Acosta Matos. The identity match is highly probable but requires formal proof.</td>
                <td>Until reconciled through tax ID, appointment and acceptance, the identities are not merged as a final fact. If confirmed, conflict declarations, recusals, attendance, votes, information received and participation in RICPE's Sun Park decisions must be produced.</td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="proof-split" role="group" aria-label="Sources and custody duty">
          <div><strong>Documented media discrepancy</strong><span>Compare the ${mediaExact} with the ${mediaVariant}. A headline variant cannot override the official corporate identification or be transferred to Gerardo Zacarías.</span></div>
          <div><strong>Death does not extinguish evidence</strong><span>Preserve name/tax ID, office dates, succession, legal representative, email, corporate devices, minutes, powers, project files, data rooms and record migrations. The present custodian must be identified even where a person has died or a company has been restructured.</span></div>
        </div>

        <div class="privacy-callout">
          <strong>Evidential boundary.</strong>
          <span>No unlawful conduct is inferred from a surname, family relationship, office, death or corporate succession. Attribution remains individual and tied to proven act, date, capacity, knowledge, decision, omission and benefit. Absence of a death report does not prove vital status or continuation in office.</span>
        </div>
      </div>
    `;

    if (responsibility) responsibility.insertAdjacentElement('beforebegin', section);
    else genealogy.insertAdjacentElement('afterend', section);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderRicpeIdentityCorrection, { once: true });
  } else {
    renderRicpeIdentityCorrection();
  }

  window.addEventListener('load', () => setTimeout(renderRicpeIdentityCorrection, 200), { once: true });
})();
