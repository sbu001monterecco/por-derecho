(() => {
  'use strict';

  const script = document.currentScript;
  if (!script) return;
  const assetBase = new URL('.', script.src);
  const repoBase = new URL('../', assetBase);
  const registerDataUrl = new URL('assets/data/proceedings-master-public-v1.json', repoBase).href;
  const prismUrl = new URL('assets/data/proceedings-case-prism-v1.json', repoBase).href;
  const interlinkUrl = new URL('assets/data/proceedings-interlinkability-v1.json', repoBase).href;
  const fiscaliaInterconnectivityUrl = new URL('assets/data/fiscalia-proceedings-interconnectivity-v1.json', repoBase).href;
  const communityAuthorityInterconnectivityUrl = new URL('assets/data/community-acta-authority-interconnectivity-v1.json', repoBase).href;
  const lang = (document.documentElement.lang || 'en').toLowerCase().startsWith('es') ? 'es' : 'en';
  const registerRoute = new URL(lang === 'es' ? 'es/registro-maestro-procedimientos/' : 'en/master-proceedings-register/', repoBase).href;
  const detailRoutes = {
    'LZ-JUD-043': {
      en: new URL('en/dp-3205-2014-arrecife/', repoBase).href,
      es: new URL('es/dp-3205-2014-arrecife/', repoBase).href
    }
  };

  const copy = lang === 'es' ? {
    loading: 'Construyendo el mapa desde el registro canónico…',
    error: 'No se pudo construir el mapa de procedimientos.',
    allTracks: 'Todas las vías', search: 'Buscar ID, referencia, órgano, objeto o estado…',
    map: 'Mapa por vías', chronology: 'Cronología', trace: 'Trazar un procedimiento / registro',
    prism: 'Prisma del caso', lanes: 'Vías paralelas', isolation: 'Prueba de aislamiento',
    records: 'nodos públicos', tracks: 'vías', direct: 'pares directos controlados', gaps: 'nodos con brecha abierta',
    directTitle: 'Relaciones procesales directas',
    contextTitle: 'Puentes de contexto controlados',
    why: 'Por qué están conectados', noDirect: 'No hay relación procesal directa admitida en el registro controlado para este objeto.',
    noContext: 'No hay otro puente contextual exacto en la proyección actual.',
    contextWarning: 'Contexto no significa mismo procedimiento, acumulación, coordinación, conocimiento, ilicitud ni responsabilidad.',
    source: 'Fuente/estado', gap: 'Brecha abierta', now: 'Ahora',
    approximate: 'Orden aproximado por el primer año reconocible en Date_or_Period; no implica causalidad.',
    openRegister: 'Abrir Registro Maestro', openRegisterRecord: 'Abrir este registro canónico', traceThis: 'Trazar registro', empty: 'No hay nodos que coincidan con los filtros.',
    publicBoundary: 'Esta visualización usa una proyección pública minimizada del registro canónico. No convierte referencias en procedimientos ni conexiones contextuales en hechos jurídicos.',
    audience: 'Lente del lector', proposition: 'Proposición / hecho a contrastar', status: 'Relación', treatment: 'Tratamiento en el expediente', period: 'Periodo',
    matrixLead: 'Una misma proposición, leída horizontalmente a través de procedimientos jurídicamente separados.',
    lanesLead: 'Orden cronológico de las proposiciones controladas y las vías en las que aparecen de forma directa, contextual o abierta.',
    isolationLead: 'Selecciona cualquier procedimiento exacto de la proyección pública. El modo aislado conserva únicamente el tratamiento del Prisma codificado como directamente presente en ese expediente; la reconexión muestra por separado las relaciones procesales expresas, los puentes contextuales controlados y las brechas no resueltas.',
    chooseLane: 'Seleccionar procedimiento exacto', visibleAlone: 'Permanece visible en el expediente seleccionado', disappears: 'Contexto material que desaparece al leerlo solo',
    noVisible: 'Ninguna proposición del prisma está marcada como directamente presente en este procedimiento exacto.', noOutside: 'No se identifica contexto material adicional en el prisma controlado.',
    detail: 'Detalle de la dependencia', masterIds: 'IDs canónicos relacionados', openTrace: 'Abrir traza',
    formalBoundary: 'La prueba de aislamiento es metodológica. No demuestra que el órgano recibiera, debiera admitir o debiera valorar el material externo.',
    fullCorpus: 'Corpus completo', restore: 'Restaurar corpus completo', isolatedMode: 'Modo aislado', sourceLinks: 'Fuentes públicas controladas de la proposición',
    sourceScope: 'Estas fuentes respaldan la ruta de auditoría de la proposición; no demuestran por sí solas el tratamiento en esta celda.',
    outsideSelected: 'Fuera del expediente seleccionado', insideSelected: 'Visible en el expediente seleccionado',
    evidenceStatus: 'Estado probatorio de la proposición', attribution: 'Atribución controlada', recordedObject: 'Objeto registrado', contrary: 'Explicación / registro contrario más fuerte', sourceNeeded: 'Fuente necesaria',
    competentOrgan: 'Órgano competente', decisionDepends: 'Qué decisión podría depender', ifConfirmed: 'Si se confirma', ifRefuted: 'Si se refuta',
    representation: 'Linaje de abogado/procurador', prismConnections: 'Dependencias del Prisma para este ID', noPrismConnections: 'No hay dependencia del Prisma codificada para este ID.',
    prismUnavailable: 'La capa del Prisma no está disponible. El mapa canónico sigue accesible, pero las vistas de convergencia y aislamiento no pueden verificarse en esta carga.',
    laneSource: 'Otros estados registrados de vía/expediente', priority: 'Prioridad para esta lente', matrixCaption: 'Matriz de dependencia decisoria por proposición y vía jurídica separada',
    swimCaption: 'Cronología en vías paralelas; cada columna sigue siendo un expediente o carril institucional separado',
    exactProceedings: 'procedimientos exactos públicos', prismCovered: 'con coordenadas expresas en el Prisma', prismNotCovered: 'sin coordenada actual en el Prisma',
    coverageBoundary: 'El selector incluye todos los registros públicos marcados canónicamente como procedimientos. La cobertura del Prisma es un denominador finito y distinto: la ausencia de coordenada significa cobertura no desarrollada o no localizada, no ausencia de relación fáctica.',
    coveredGroup: 'Procedimientos con coordenadas en el Prisma', uncoveredGroup: 'Otros procedimientos exactos — sin coordenada en el Prisma',
    selectedCoverage: 'Cobertura del procedimiento seleccionado', prismCoveredSelected: 'Este procedimiento tiene tratamiento proposicional expreso en el Prisma controlado.',
    noPrismCoverageSelected: 'No hay tratamiento proposicional del Prisma codificado para este procedimiento exacto. No se infiere ninguna celda: el expediente sigue siendo trazable mediante sus campos canónicos y las brechas permanecen expresas.',
    directReconnection: 'Relaciones procesales directas para reconectar', contextReconnection: 'Puentes contextuales controlados para reconectar', unresolvedReconnection: 'Estado no resuelto / cobertura pendiente',
    noDirectSelected: 'No hay relación procesal directa codificada por ID canónico para este procedimiento.', noContextSelected: 'No hay puente contextual controlado con otro nodo público en los campos actuales.',
    directBoundary: 'Solo se muestran relaciones expresamente codificadas como padre/origen, enlace de procedimiento, recurso/revisión o enlace documentado por una fuente especializada controlada.',
    contextBoundary: 'Estos puentes proceden de valores Connection canónicos coincidentes, corredores expresamente controlados por una fuente o pertenencia a una proposición del Prisma. Ayudan a localizar contexto; no acreditan identidad de procedimiento, acumulación, conocimiento, causalidad, ilicitud ni responsabilidad. Para evitar expansión transitiva, los miembros de una proposición no se siguen hacia otras proposiciones; un ID relacionado solo abre otra proposición mediante una coordenada DIRECTA.',
    prismCoordinate: 'Coordenada del Prisma', noPrismCoordinate: 'Sin coordenada del Prisma', selectedFileStatus: 'Estado respecto del expediente seleccionado',
    relationCount: 'relaciones', bridgeCount: 'puentes', clusterCount: 'agrupaciones controladas', counterpartCount: 'contrapartes públicas únicas', nextSource: 'Siguiente fuente necesaria', classification: 'Clasificación controlada', provenance: 'Procedencia', limitations: 'Límites',
    interlinkUnavailable: 'El registro controlado de interconectividad no está disponible para este procedimiento. No se infiere una clasificación por ausencia.',
    notExactClassification: 'Registro público — no es un procedimiento exacto', notExactTrace: 'Este objeto público puede trazarse como registro, pero no está marcado como procedimiento exacto. No se infiere ninguna clasificación, relación procesal directa ni puente contextual.',
    sourceAssertions: 'Afirmaciones de fuente', sourceAssertion: 'afirmación',
    directVerified: 'pares con fuente verificada', directPending: 'par con fuente primaria pendiente',
    finiteAudit: 'Prueba finita del expediente', finiteAuditCoverage: 'pruebas finitas de expediente auditadas',
    finiteAuditBoundary: 'La cobertura de auditoría significa que la pregunta y sus campos de comprobación están definidos. No significa que la proposición, la recepción, el examen, el conocimiento personal o la responsabilidad estén probados.',
    finiteUnavailable: 'No hay una prueba finita completa modelada para este procedimiento exacto. No se infiere ninguna conclusión de esa ausencia.',
    finiteIncomplete: 'Modelo de prueba finita incompleto', finiteReady: 'Prueba finita auditada',
    auditCoverage: 'Cobertura de auditoría', positiveEvidence: 'Prueba positiva separada',
    positiveEvidenceCount: 'expedientes con algún estado positivo expresamente codificado de recepción/tratamiento o evidencia específica de actor',
    finiteQuestion: 'Pregunta finita', currentSourceStatus: 'Estado actual de la fuente', proceduralAvailability: 'Disponibilidad procesal',
    institutionalReceipt: 'Recepción y tratamiento institucional', actorKnowledge: 'Evidencia de conocimiento específica de actor',
    institutionalBoundary: 'RECIBIDO ≠ INCORPORADO AL EXPEDIENTE ≠ EXAMINADO ≠ UTILIZADO EN UNA DECISIÓN.',
    actorBoundary: 'La recepción institucional no prueba por sí sola lectura, comprensión, conocimiento personal, intención, acuerdo, ilicitud ni responsabilidad de una persona concreta.', actorReceiptStatus: 'Recepción específica de actor', actorKnowledgeStatus: 'Conocimiento específico de actor', actorSourceStatus: 'Estado de fuente específica de actor',
    transmission: 'Transmisión', registration: 'Registro', fileIncorporation: 'Incorporación al expediente', recipientAttribution: 'Atribución del destinatario',
    substantiveExamination: 'Examen sustantivo', decisionUse: 'Uso en decisión', noReceiptEvents: 'No hay eventos institucionales fuente-controlados vinculados a esta prueba.',
    noActorEvidence: 'No hay una fuente específica de actor vinculada que establezca conocimiento personal.',
    directRelated: 'Procedimientos relacionados directamente', contextRelated: 'Contexto relacionado — no es enlace procesal',
    noDirectRelated: 'No hay otro procedimiento relacionado directamente en el registro controlado.',
    noContextRelated: 'No hay otro procedimiento contextual relacionado en el registro controlado.',
    proves: 'Acredita dentro de este alcance', doesNotProve: 'No acredita', publicRouteGap: 'Ruta pública de fuente no establecida',
    modelStatus: 'Estado del modelo', receiptEvent: 'Evento institucional', actorProfile: 'Actor / perfil controlado',
    fiscaliaMatrix: 'Matriz transversal de oficinas y expedientes del Ministerio Fiscal', fiscaliaRows: 'filas públicas de oficina/expediente auditadas',
    fiscaliaProfiled: 'con perfil de episodio fuente-controlado', fiscaliaExactRows: 'procedimientos exactos', fiscaliaUnresolvedRows: 'referencias no verificadas como procedimiento exacto', fiscaliaModelBoundary: 'La cobertura del modelo no equivale a recepción, examen o reconocimiento unitario acreditados.',
    officeFile: 'Oficina / expediente', receivedProfile: 'Recibido / estado del perfil', responseTreatment: 'Respuesta / tratamiento', canonicalSourceStatus: 'Estado canónico de fuente', responseProfileStatus: 'Estado del perfil de respuesta', exactnessStatus: 'Condición de procedimiento', recordType: 'Tipo de registro',
    crossFileAcknowledgement: 'Reconocimiento entre expedientes', unansweredGap: 'Sin respuesta / fuente pendiente',
    noUnitaryAcknowledgement: 'No se ha localizado un reconocimiento unitario en el corpus controlado.', fiscaliaMatrixUnavailable: 'La matriz transversal de Fiscalía no está disponible en esta carga.',
    requestedMaterial: 'Solicitado', originOffice: 'Oficina de origen', currentCustodian: 'Custodio actual', datePeriod: 'Fecha / periodo', materialEvidence: 'Alegaciones / material / prueba descritos', materialReceivedInventory: 'Inventario de material recibido', noMaterialItemised: 'No hay material recibido individualizado en esta fila controlada.', materialInventoryGap: 'Brecha del inventario de material', directRelatedProceedings: 'Procedimientos relacionados directamente', contextRelatedProceedings: 'Contexto relacionado — no es enlace procesal', noDirectMatrixRelated: 'No hay otro procedimiento directo individualizado en esta fila.', noContextMatrixRelated: 'No hay otro contexto relacionado individualizado en esta fila.', relatedProceedingsStatus: 'Estado de procedimientos relacionados', relatedAssets: 'Activos relacionados', noRelatedAssets: 'No hay activo separado individualizado en esta fila.', relatedAssetsGap: 'Brecha de activos relacionados', transmissionStatus: 'Estado de transmisión', materialStatus: 'Estado del material recibido', relatedAssetsStatus: 'Estado de activos relacionados', referralStatus: 'Estado de remisión', whatWasReferred: 'Qué fue remitido', registrationStatus: 'Estado de registro', fileIncorporationStatus: 'Estado de incorporación al expediente', recipientAttributionStatus: 'Estado de atribución del destinatario', examinationStatus: 'Estado de examen', whatWasExamined: 'Qué fue efectivamente examinado', decisionUseStatus: 'Estado de uso en decisión', unitaryAcknowledgementStatus: 'Estado de reconocimiento unitario', strongestContrary: 'Explicación contraria más fuerte', rowBoundary: 'Límite de atribución de la fila', sourceProfiles: 'Perfiles fuente', axisBasis: 'Base y límite del grado', basisKind: 'Tipo de base', basisStatement: 'Base controlada', basisSource: 'Procedencia de la base', controlledLimit: 'Límite controlado', controlledEpisodes: 'episodios de respuesta controlados en total', filterScope: 'La búsqueda y el filtro de vía se aplican únicamente al mapa por vías y a la cronología.', fiscaliaCommunications: 'Abrir comunicaciones y respuestas de Fiscalía'
  } : {
    loading: 'Building the map from the canonical register…',
    error: 'The proceedings map could not be built.',
    allTracks: 'All tracks', search: 'Search ID, reference, organ, object or status…',
    map: 'Track map', chronology: 'Chronology', trace: 'Trace one proceeding / record',
    prism: 'Case Prism', lanes: 'Parallel lanes', isolation: 'Isolation test',
    records: 'public nodes', tracks: 'tracks', direct: 'controlled direct pairs', gaps: 'nodes with an open gap',
    directTitle: 'Direct procedural relationships',
    contextTitle: 'Controlled context bridges',
    why: 'Why connected?', noDirect: 'No direct procedural relationship is admitted in the controlled registry for this object.',
    noContext: 'No other exact contextual bridge is available in the current projection.',
    contextWarning: 'Context does not mean the same proceeding, joinder, coordination, knowledge, wrongdoing or liability.',
    source: 'Source/status', gap: 'Open gap', now: 'Now',
    approximate: 'Approximate order by the first recognisable year in Date_or_Period; it does not imply causation.',
    openRegister: 'Open Master Register', openRegisterRecord: 'Open this canonical record', traceThis: 'Trace record', empty: 'No nodes match the current filters.',
    publicBoundary: 'This visualisation uses a minimised public projection of the canonical register. It does not turn references into proceedings or contextual connections into legal facts.',
    audience: 'Reader lens', proposition: 'Proposition / fact to test', status: 'Relationship', treatment: 'Treatment in file', period: 'Period',
    matrixLead: 'One proposition, read horizontally across legally separate proceedings.',
    lanesLead: 'Chronological order of the controlled propositions and the lanes in which they appear as direct, contextual or open.',
    isolationLead: 'Select any exact proceeding in the public projection. Isolated mode keeps only Case Prism treatment encoded as directly present in that file; reconnection separately shows express procedural relationships, controlled contextual bridges and unresolved gaps.',
    chooseLane: 'Select exact proceeding', visibleAlone: 'Remains visible in the selected file', disappears: 'Material context that disappears when read alone',
    noVisible: 'No proposition in this prism is marked as directly present in this exact proceeding.', noOutside: 'No additional material context is identified in the controlled prism.',
    detail: 'Dependency detail', masterIds: 'Related canonical IDs', openTrace: 'Open trace',
    formalBoundary: 'The isolation test is methodological. It does not prove that the organ received, should admit or should assess the external material.',
    fullCorpus: 'Full corpus', restore: 'Restore full corpus', isolatedMode: 'Isolated mode', sourceLinks: 'Controlled public sources for the proposition',
    sourceScope: 'These sources support the proposition-level audit path; they do not by themselves establish treatment in this cell.',
    outsideSelected: 'Outside the selected file', insideSelected: 'Visible in the selected file',
    evidenceStatus: 'Proposition evidence status', attribution: 'Controlled attribution', recordedObject: 'Recorded object', contrary: 'Strongest contrary explanation / record', sourceNeeded: 'Source needed',
    competentOrgan: 'Competent organ', decisionDepends: 'What decision could depend', ifConfirmed: 'If confirmed', ifRefuted: 'If refuted',
    representation: 'Counsel/procurador lineage', prismConnections: 'Case Prism dependencies for this ID', noPrismConnections: 'No Case Prism dependency is encoded for this ID.',
    prismUnavailable: 'The Case Prism layer is unavailable. The canonical map remains accessible, but convergence and isolation views cannot be verified in this load.',
    laneSource: 'Other recorded lane/file statuses', priority: 'Priority for this lens', matrixCaption: 'Decision-dependency matrix by proposition and legally separate lane',
    swimCaption: 'Parallel-lane chronology; every column remains a separate proceeding or institutional lane',
    exactProceedings: 'exact public proceedings', prismCovered: 'with express Case Prism coordinates', prismNotCovered: 'without a current Case Prism coordinate',
    coverageBoundary: 'The selector includes every public record canonically marked as a proceeding. Case Prism coverage is a separate finite denominator: no coordinate means coverage is undeveloped or not located, not that no factual relationship exists.',
    coveredGroup: 'Proceedings with Case Prism coordinates', uncoveredGroup: 'Other exact proceedings — no Case Prism coordinate',
    selectedCoverage: 'Selected-proceeding coverage', prismCoveredSelected: 'This proceeding has express proposition treatment in the controlled Case Prism.',
    noPrismCoverageSelected: 'No Case Prism proposition treatment is encoded for this exact proceeding. No cell is inferred: the file remains traceable through its canonical fields and every gap stays explicit.',
    directReconnection: 'Direct procedural relationships for reconnection', contextReconnection: 'Controlled context bridges for reconnection', unresolvedReconnection: 'Unresolved state / coverage pending',
    noDirectSelected: 'No direct procedural relationship is encoded by canonical ID for this proceeding.', noContextSelected: 'No controlled context bridge to another public node is available in the current fields.',
    directBoundary: 'Only relationships expressly encoded as parent/origin, linked proceeding, appeal/review or documented by a controlled specialist source are shown.',
    contextBoundary: 'These bridges come from matching canonical Connection values, corridors expressly controlled by a source, or Case Prism proposition membership. They help locate context; they do not establish the same proceeding, joinder, knowledge, causation, wrongdoing or liability. To prevent transitive expansion, proposition co-members are not followed into other propositions; a related ID surfaces another proposition only through a DIRECT coordinate.',
    prismCoordinate: 'Case Prism coordinate', noPrismCoordinate: 'No Case Prism coordinate', selectedFileStatus: 'Status relative to selected file',
    relationCount: 'relationships', bridgeCount: 'bridges', clusterCount: 'controlled clusters', counterpartCount: 'unique public counterparts', nextSource: 'Next source needed', classification: 'Controlled classification', provenance: 'Provenance', limitations: 'Limitations',
    interlinkUnavailable: 'The controlled interlinkability register is unavailable for this proceeding. No classification is inferred from absence.',
    notExactClassification: 'Public record — not an exact proceeding', notExactTrace: 'This public object remains traceable as a record, but it is not marked as an exact proceeding. No classification, direct procedural relationship or contextual bridge is inferred.',
    sourceAssertions: 'Source assertions', sourceAssertion: 'assertion',
    directVerified: 'source-verified pairs', directPending: 'source-reported primary-pending pair',
    finiteAudit: 'Exact-file finite test', finiteAuditCoverage: 'exact-file finite tests audited',
    finiteAuditBoundary: 'Audit coverage means that the finite question and its verification fields are defined. It does not mean that the proposition, receipt, examination, personal knowledge or responsibility is proved.',
    finiteUnavailable: 'No complete finite test is modelled for this exact proceeding. No conclusion is inferred from that absence.',
    finiteIncomplete: 'Incomplete finite-test model', finiteReady: 'Finite test audited',
    auditCoverage: 'Audit coverage', positiveEvidence: 'Separate positive evidence',
    positiveEvidenceCount: 'files with at least one expressly encoded positive receipt/treatment status or actor-specific evidence status',
    finiteQuestion: 'Finite question', currentSourceStatus: 'Current source status', proceduralAvailability: 'Procedural availability',
    institutionalReceipt: 'Institutional receipt and treatment', actorKnowledge: 'Actor-specific knowledge evidence',
    institutionalBoundary: 'RECEIVED ≠ INCORPORATED IN FILE ≠ EXAMINED ≠ USED IN A DECISION.',
    actorBoundary: 'Institutional receipt does not by itself prove a named person’s reading, understanding, personal knowledge, intent, agreement, wrongdoing or responsibility.', actorReceiptStatus: 'Actor-specific receipt', actorKnowledgeStatus: 'Actor-specific knowledge', actorSourceStatus: 'Actor-specific source status',
    transmission: 'Transmission', registration: 'Registration', fileIncorporation: 'File incorporation', recipientAttribution: 'Recipient attribution',
    substantiveExamination: 'Substantive examination', decisionUse: 'Decision use', noReceiptEvents: 'No source-controlled institutional events are linked to this test.',
    noActorEvidence: 'No linked actor-specific source establishes personal knowledge.',
    directRelated: 'Directly related proceedings', contextRelated: 'Related context — not a procedural edge',
    noDirectRelated: 'No other directly related proceeding is present in the controlled registry.',
    noContextRelated: 'No other contextually related proceeding is present in the controlled registry.',
    proves: 'Establishes within this scope', doesNotProve: 'Does not establish', publicRouteGap: 'Public source route not established',
    modelStatus: 'Model status', receiptEvent: 'Institutional event', actorProfile: 'Actor / controlled profile',
    fiscaliaMatrix: 'Ministerio Fiscal cross-office / file matrix', fiscaliaRows: 'public office/file rows audited',
    fiscaliaProfiled: 'with a source-controlled episode profile', fiscaliaExactRows: 'exact proceedings', fiscaliaUnresolvedRows: 'references not verified as an exact proceeding', fiscaliaModelBoundary: 'Model coverage is not proof of receipt, examination or unitary acknowledgement.',
    officeFile: 'Office / file', receivedProfile: 'Received / profile state', responseTreatment: 'Response / treatment', canonicalSourceStatus: 'Canonical source status', responseProfileStatus: 'Response-profile status', exactnessStatus: 'Proceeding status', recordType: 'Record type',
    crossFileAcknowledgement: 'Cross-file acknowledgement', unansweredGap: 'Unanswered / source gap',
    noUnitaryAcknowledgement: 'No unitary acknowledgement has been located in the controlled corpus.', fiscaliaMatrixUnavailable: 'The Fiscalía cross-office matrix is unavailable in this load.',
    requestedMaterial: 'Requested', originOffice: 'Origin office', currentCustodian: 'Current custodian', datePeriod: 'Date / period', materialEvidence: 'Described allegations / material / evidence', materialReceivedInventory: 'Received-material inventory', noMaterialItemised: 'No received material is itemised in this controlled row.', materialInventoryGap: 'Material-inventory gap', directRelatedProceedings: 'Directly related proceedings', contextRelatedProceedings: 'Related context — not a procedural edge', noDirectMatrixRelated: 'No other direct proceeding is itemised in this row.', noContextMatrixRelated: 'No other related context is itemised in this row.', relatedProceedingsStatus: 'Related-proceedings status', relatedAssets: 'Related assets', noRelatedAssets: 'No separate asset is itemised in this row.', relatedAssetsGap: 'Related-assets gap', transmissionStatus: 'Transmission status', materialStatus: 'Material-received status', relatedAssetsStatus: 'Related-assets status', referralStatus: 'Referral status', whatWasReferred: 'What was referred', registrationStatus: 'Registration status', fileIncorporationStatus: 'File-incorporation status', recipientAttributionStatus: 'Recipient-attribution status', examinationStatus: 'Examination status', whatWasExamined: 'What was actually examined', decisionUseStatus: 'Decision-use status', unitaryAcknowledgementStatus: 'Unitary-acknowledgement status', strongestContrary: 'Strongest contrary explanation', rowBoundary: 'Row attribution boundary', sourceProfiles: 'Source profiles', axisBasis: 'Grade basis and limitation', basisKind: 'Basis kind', basisStatement: 'Controlled basis', basisSource: 'Basis provenance', controlledLimit: 'Controlled limitation', controlledEpisodes: 'controlled response episodes total', filterScope: 'Search and track filters apply only to the track map and chronology.', fiscaliaCommunications: 'Open Fiscalía communications and responses'
  };

  copy.communityAuthority = lang === 'es' ? 'Abrir ACTAs y expedientes públicos' : 'Open ACTAs and public-authority files';

  const esc = (v) => String(v || '').replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const norm = (v) => String(v || '').trim();
  const key = (v) => norm(v).toLowerCase();
  const localized = (obj, base) => obj ? (obj[`${base}_${lang}`] || obj[lang] || obj[base] || obj.en || obj.es || '') : '';

  const firstYear = (value) => {
    const m = String(value || '').match(/\b(19|20)\d{2}\b/);
    return m ? Number(m[0]) : 9999;
  };

  const labelFor = (r) => norm(r.Reference) || norm(r.Secondary_Reference) || norm(r.Master_ID);
  const subtitleFor = (r) => [norm(r.Proceeding_Class), norm(r.Stream)].filter(Boolean).join(' · ');

  const detailUrlFor = (id) => detailRoutes[id] && detailRoutes[id][lang];
  const detailAnchor = (r, text, className = '') => {
    const url = detailUrlFor(r.Master_ID);
    return url ? `<a${className ? ` class="${className}"` : ''} href="${esc(url)}">${esc(text)}</a>` : esc(text);
  };

  const card = (r, traceButton = true) => `
    <article class="pdim-node" data-node-id="${esc(r.Master_ID)}">
      <div class="pdim-node-head"><span class="pdim-id">${detailAnchor(r, r.Master_ID)}</span><span class="pdim-state" data-state="${esc(norm(r.Is_Proceeding).toUpperCase() || 'UNVERIFIED')}">${esc(norm(r.Is_Proceeding).toUpperCase() || 'UNVERIFIED')}</span></div>
      <h3>${detailAnchor(r, labelFor(r))}</h3>
      <p class="pdim-sub">${esc(subtitleFor(r))}</p>
      <p>${esc([r.Connection, r.Object_or_Purpose].filter(Boolean).join(' — '))}</p>
      <div class="pdim-node-meta"><span>${esc(r.Date_or_Period)}</span><span>${esc(r.Origin_Organ)}</span></div>
      ${traceButton ? `<button type="button" data-trace-id="${esc(r.Master_ID)}">${copy.traceThis} →</button>` : ''}
      ${detailUrlFor(r.Master_ID) ? `<a class="pdim-detail-link" href="${esc(detailUrlFor(r.Master_ID))}">${lang === 'es' ? 'Abrir ficha bilingüe' : 'Open bilingual record'} ↗</a>` : ''}
    </article>`;

  function prismMatchesForId(prism, selected) {
    if (!prism) return [];
    return prism.propositions.flatMap((prop) => prism.lanes.flatMap((lane) => {
      const cell = prop.cells && prop.cells[lane.id];
      return cell && cell.status !== 'OUTSIDE' && Array.isArray(cell.master_ids) && cell.master_ids.includes(selected)
        ? [{prop, lane, cell}] : [];
    }));
  }

  const isExactProceeding = (record) => norm(record && record.Is_Proceeding).toUpperCase() === 'TRUE';

  function catalogLabel(catalog, token) {
    const meta = catalog && catalog[token];
    return localized(meta, 'label') || localized(meta, '') || humanToken(token);
  }

  function provenanceLabel(source) {
    if (!source) return '—';
    const direction = source.assertion_from_master_id || source.assertion_to_master_id
      ? `${norm(source.assertion_from_master_id) || '?'} → ${norm(source.assertion_to_master_id) || '?'}`
      : '';
    return [
      source.kind,
      source.source_id,
      source.path,
      source.record_id,
      source.profile_id,
      source.record_master_id || source.source_record_master_id,
      source.field_or_record_id,
      source.field,
      source.value_token,
      source.assertion_relationship_type,
      source.assertion_direction,
      direction,
      source.anchor,
      source.evidence_status,
      source.status
    ].map(norm).filter(Boolean).join(' · ') || '—';
  }

  function provenanceHtml(item) {
    const assertions = Array.isArray(item && item.source_assertions) && item.source_assertions.length
      ? item.source_assertions
      : (item && item.source ? [item.source] : []);
    if (!assertions.length) return '';
    const count = assertions.length;
    const countLabel = count > 1 ? ` (${count} ${copy.sourceAssertions.toLowerCase()})` : ` (${count} ${copy.sourceAssertion})`;
    return `<div class="pdim-provenance" data-source-assertions data-assertion-count="${count}"><strong>${esc(copy.provenance)}${esc(countLabel)}</strong><ul>${assertions.map((source) => `<li>${esc(provenanceLabel(source))}</li>`).join('')}</ul></div>`;
  }

  function finiteText(container, ...keys) {
    for (const field of keys) {
      if (!container || typeof container !== 'object') continue;
      const direct = container[field];
      if (typeof direct === 'string' && norm(direct)) return norm(direct);
      if (direct && typeof direct === 'object') {
        const nested = localized(direct, '') || localized(direct, 'text') || localized(direct, 'label') || localized(direct, 'value');
        if (norm(nested)) return norm(nested);
      }
      const suffixed = localized(container, field);
      if (norm(suffixed)) return norm(suffixed);
    }
    return '';
  }

  function finiteToken(value) {
    if (typeof value === 'string') return norm(value);
    if (!value || typeof value !== 'object') return '';
    return norm(value.status || value.token || value.state || value.code || value.value);
  }

  function finiteTokenLabel(interlinks, token, value) {
    const own = value && typeof value === 'object' ? (localized(value, 'label') || localized(value, 'text')) : '';
    if (own) return own;
    const catalogs = [
      interlinks && interlinks.finite_test_status_catalog,
      interlinks && interlinks.source_status_catalog,
      interlinks && interlinks.receipt_status_catalog,
      interlinks && interlinks.receipt_knowledge_status_catalog,
      interlinks && interlinks.knowledge_status_catalog,
      interlinks && interlinks.status_catalogs && interlinks.status_catalogs.finite_test,
      interlinks && interlinks.status_catalogs && interlinks.status_catalogs.institutional_receipt,
      interlinks && interlinks.status_catalogs && interlinks.status_catalogs.actor_specific_knowledge
    ];
    for (const catalog of catalogs) {
      if (catalog && catalog[token]) return catalogLabel(catalog, token);
    }
    return humanToken(token || 'STATUS_NOT_MODELLED');
  }

  function finiteOrgan(test) {
    const organ = test && test.competent_organ;
    const candidate = finiteText(organ, 'recorded_candidate', 'candidate', 'name')
      || finiteText(test, 'competent_organ_recorded_candidate', 'competent_organ_candidate', 'competent_organ');
    const status = finiteToken(organ) || finiteToken(test && test.competent_organ_status);
    return {candidate, status};
  }

  function finiteReceiptModel(test, disposition = null) {
    const root = test && (test.receipt_knowledge || test.receipt_and_knowledge || test.receipt_treatment)
      || disposition && disposition.receipt_knowledge;
    if (!root || typeof root !== 'object') return null;
    const institutional = root.institutional_receipt_treatment || root.institutional || root.institutional_axes || root.receipt || root;
    const actor = root.actor_specific_knowledge || root.actor_specific || root.actors || {};
    return {root, institutional, actor};
  }

  const finiteAxisDefinitions = [
    {key:'transmission', label:'transmission', aliases:['transmission_status','transmission']},
    {key:'registration', label:'registration', aliases:['registration_status','registration','receipt_status']},
    {key:'file-incorporation', label:'fileIncorporation', aliases:['file_incorporation_status','file_incorporation','incorporation_status']},
    {key:'recipient-attribution', label:'recipientAttribution', aliases:['recipient_attribution_status','recipient_attribution','recipient_status']},
    {key:'examination', label:'substantiveExamination', aliases:['substantive_examination_status','substantive_examination','examination_status']},
    {key:'decision-use', label:'decisionUse', aliases:['decision_use_status','decision_use','treatment_status']}
  ];

  function finiteAxisValue(institutional, aliases) {
    for (const alias of aliases) {
      if (institutional && Object.prototype.hasOwnProperty.call(institutional, alias)) return institutional[alias];
      if (institutional && institutional.axes && Object.prototype.hasOwnProperty.call(institutional.axes, alias)) return institutional.axes[alias];
    }
    return '';
  }

  function finiteActorStatus(actor, root) {
    return finiteToken(actor && (actor.status || actor.audit_status || actor.evidence_status || actor.source_status))
      || finiteToken(root && (root.actor_specific_status || root.personal_knowledge_status));
  }

  function finiteTestComplete(disposition) {
    const test = disposition && disposition.finite_test;
    if (!test || typeof test !== 'object') return false;
    const organ = finiteOrgan(test);
    const receipt = finiteReceiptModel(test, disposition);
    const related = test.related_proceedings || {};
    const navigation = test.navigation || {};
    const actor = receipt && receipt.actor || {};
    const hasSixAxes = receipt && finiteAxisDefinitions.every((axis) => finiteToken(finiteAxisValue(receipt.institutional, axis.aliases)));
    return Boolean(
      norm(test.id)
      && norm(test.family_template_id)
      && test.family_taxonomy_only === true
      && finiteText(test, 'question', 'finite_question')
      && norm(test.recorded_object)
      && norm(test.attribution)
      && finiteText(test, 'source_needed', 'source_requirement')
      && norm(test.current_source_status || test.source_status)
      && norm(test.source_needed_status)
      && finiteSourceRefs(test).length
      && finiteText(test, 'contrary', 'contrary_explanation', 'strongest_contrary', 'strongest_contrary_or_innocent_explanation')
      && organ.candidate
      && organ.status
      && norm(test.competent_organ && test.competent_organ.basis_field)
      && finiteText(test, 'decision_dependency')
      && finiteText(test, 'procedural_availability')
      && finiteText(test, 'if_confirmed')
      && finiteText(test, 'if_refuted')
      && receipt
      && hasSixAxes
      && norm(receipt.root.cross_file_acknowledgement_status)
      && norm(actor.receipt_status)
      && norm(actor.knowledge_status)
      && norm(actor.source_status)
      && Array.isArray(related.direct_master_ids)
      && Array.isArray(related.context_master_ids)
      && Array.isArray(related.context_cluster_ids)
      && norm(related.treatment_status)
      && Array.isArray(related.connection_statuses)
      && norm(navigation.controlled_trace_fragment)
      && norm(navigation.controlled_isolation_fragment)
      && navigation.controlled_navigation_status === 'AVAILABLE'
    );
  }

  function finiteHasPositiveProof(disposition) {
    const test = disposition && disposition.finite_test;
    const receipt = finiteReceiptModel(test, disposition);
    if (!receipt) return false;
    const values = finiteAxisDefinitions.map((axis) => finiteToken(finiteAxisValue(receipt.institutional, axis.aliases)));
    values.push(finiteActorStatus(receipt.actor, receipt.root));
    const negative = /(?:^|_)(?:NO|NOT|NONE|UNAVAILABLE|UNRESOLVED|OPEN|PENDING)(?:_|$)/;
    const positive = /(?:DOCUMENTED|LOCATED|VERIFIED|ACKNOWLEDG|EXPRESS|RELIED|INCORPORAT|RECEIV|EXAMIN|DECISION_USE)/;
    return values.some((token) => token && !negative.test(token) && positive.test(token));
  }

  function finiteSourceRefs(test) {
    const refs = test && (test.source_refs || test.sources || test.source_routes || test.source_ids);
    if (!refs) return [];
    return (Array.isArray(refs) ? refs : [refs]).map((item) => typeof item === 'string' ? {source_id:item} : item).filter(Boolean);
  }

  function finiteSourceHref(ref) {
    const raw = ref && (ref[`href_${lang}`] || ref.href || ref.href_en || ref.href_es || ref.public_route);
    if (!raw) return '';
    try {
      const url = new URL(raw, repoBase);
      return ['http:', 'https:'].includes(url.protocol) ? url.href : '';
    } catch (_err) { return ''; }
  }

  function finiteSourcesHtml(test, interlinks) {
    const refs = finiteSourceRefs(test);
    if (!refs.length) return `<p class="pdim-finite-empty">${esc(copy.publicRouteGap)}</p>`;
    return `<ul class="pdim-finite-source-list">${refs.map((ref) => {
      const id = norm(ref.source_id || ref.id || ref.record_id || ref.path) || 'SOURCE';
      const status = finiteToken(ref.route_status || ref.evidence_status || ref.status) || 'STATUS_NOT_STATED';
      const label = finiteText(ref, 'label', 'title') || id;
      const href = finiteSourceHref(ref);
      const content = `<strong>${esc(label)}</strong><span>${esc(finiteTokenLabel(interlinks, status, ref))}</span><code>${esc(id)} · ${esc(status)}</code>`;
      return href ? `<li><a data-finite-source-link href="${esc(href)}"${new URL(href).origin === repoBase.origin ? '' : ' rel="external noopener"'}>${content}</a></li>` : `<li data-finite-source-gap>${content}<small>${esc(copy.publicRouteGap)}</small></li>`;
    }).join('')}</ul>`;
  }

  function finiteRelatedEntries(test, disposition, interlinks, selected, byId) {
    const related = test && (test.related_proceedings || test.related || {});
    const suppliedDirect = related.direct || related.direct_master_ids || related.direct_proceedings || test.related_direct || [];
    const suppliedContext = related.context || related.context_master_ids || related.contextual || related.context_proceedings || test.related_context || [];
    const normalise = (items, kind) => (Array.isArray(items) ? items : [items]).filter(Boolean).map((item) => {
      if (typeof item === 'string') return {master_id:item, kind};
      return {...item, master_id:item.master_id || item.related_master_id || item.id, kind};
    }).filter((item) => item.master_id && item.master_id !== selected);
    let direct = normalise(suppliedDirect, 'DIRECT_PROCEDURAL_EDGE');
    let context = normalise(suppliedContext, 'CONTROLLED_CONTEXTUAL_BRIDGE');
    const relationshipById = new Map(((interlinks && interlinks.relationships) || []).map((entry) => [entry.id, entry]));
    const clusterById = new Map(((interlinks && interlinks.context_clusters) || []).map((entry) => [entry.id, entry]));
    if (!direct.length && disposition) {
      direct = (disposition.relationship_ids || []).map((id) => relationshipById.get(id)).filter(Boolean).map((entry) => ({
        master_id:entry.from_master_id === selected ? entry.to_master_id : entry.from_master_id,
        why_en:entry.why_en, why_es:entry.why_es, relationship_id:entry.id, kind:'DIRECT_PROCEDURAL_EDGE'
      }));
    }
    if (!context.length && disposition) {
      context = (disposition.context_cluster_ids || []).map((id) => clusterById.get(id)).filter(Boolean).flatMap((entry) =>
        (entry.member_master_ids || []).filter((id) => id !== selected && byId.has(id)).map((id) => ({
          master_id:id, why_en:entry.why_en, why_es:entry.why_es, context_cluster_id:entry.id, kind:'CONTROLLED_CONTEXTUAL_BRIDGE'
        }))
      );
    }
    const unique = (items) => Array.from(new Map(items.map((item) => [`${item.kind}:${item.master_id}`, item])).values());
    return {direct:unique(direct), context:unique(context)};
  }

  function finiteRelatedHtml(items, byId, emptyText) {
    if (!items.length) return `<li class="pdim-none">${esc(emptyText)}</li>`;
    return items.map((item) => {
      const other = byId.get(item.master_id);
      const why = finiteText(item, 'why', 'reason', 'limitations');
      const controlId = norm(item.relationship_id || item.context_cluster_id || item.source_id);
      return `<li><button type="button" data-trace-id="${esc(item.master_id)}"><strong>${esc(item.master_id)} · ${esc(other ? labelFor(other) : item.master_id)}</strong></button>${why ? `<p>${esc(why)}</p>` : ''}${controlId ? `<code>${esc(controlId)}</code>` : ''}</li>`;
    }).join('');
  }

  function finiteReceiptHtml(test, interlinks, disposition = null) {
    const receipt = finiteReceiptModel(test, disposition);
    if (!receipt) return `<section class="pdim-finite-receipt" data-institutional-receipt-treatment data-model-status="UNAVAILABLE"><h3>${esc(copy.institutionalReceipt)}</h3><p class="pdim-warning">${esc(copy.finiteUnavailable)}</p></section>`;
    const axes = finiteAxisDefinitions.map((axis) => {
      const value = finiteAxisValue(receipt.institutional, axis.aliases);
      const token = finiteToken(value) || 'STATUS_NOT_MODELLED';
      const dataName = `data-${axis.key}-status`;
      return `<div data-receipt-axis="${esc(axis.key)}" ${dataName}="${esc(token)}"><dt>${esc(copy[axis.label])}</dt><dd><span>${esc(finiteTokenLabel(interlinks, token, value))}</span><code>${esc(token)}</code></dd></div>`;
    }).join('');
    const events = receipt.institutional && (receipt.institutional.events || receipt.institutional.event_refs || receipt.institutional.receipt_events)
      || receipt.root.events || receipt.root.event_refs || [];
    const eventList = (Array.isArray(events) ? events : [events]).filter(Boolean);
    const eventsHtml = eventList.length ? `<ol class="pdim-receipt-events">${eventList.map((event) => {
      const item = typeof event === 'string' ? {event_id:event} : event;
      const id = norm(item.event_id || item.id || item.source_id) || 'EVENT';
      const title = finiteText(item, 'summary', 'label', 'office', 'institution') || id;
      const proves = finiteText(item, 'proves', 'proof_scope');
      const doesNot = finiteText(item, 'does_not_prove', 'limitations');
      return `<li data-receipt-event="${esc(id)}"><strong>${esc(copy.receiptEvent)} · ${esc(id)}</strong><span>${esc([norm(item.date || item.event_date), title].filter(Boolean).join(' · '))}</span>${proves ? `<p><b>${esc(copy.proves)}:</b> ${esc(proves)}</p>` : ''}${doesNot ? `<p><b>${esc(copy.doesNotProve)}:</b> ${esc(doesNot)}</p>` : ''}</li>`;
    }).join('')}</ol>` : `<p class="pdim-finite-empty">${esc(copy.noReceiptEvents)}</p>`;
    const crossFileStatus = finiteToken(receipt.root.cross_file_acknowledgement_status) || 'STATUS_NOT_MODELLED';
    const receiptLimit = finiteText(receipt.root, 'limitations');
    const actor = receipt.actor || {};
    const actorStatus = finiteActorStatus(actor, receipt.root) || 'NO_ACTOR_SPECIFIC_SOURCE_LOCATED';
    const actorReceiptStatus = finiteToken(actor.receipt_status) || 'NOT_ESTABLISHED';
    const actorKnowledgeStatus = finiteToken(actor.knowledge_status) || 'NOT_ESTABLISHED';
    const profiles = actor.profiles || actor.profile_refs || actor.assessments || actor.actors || actor.actor_ids || receipt.root.actor_profiles || [];
    const profileList = (Array.isArray(profiles) ? profiles : [profiles]).filter(Boolean);
    const actorHtml = profileList.length ? `<ul class="pdim-actor-profiles">${profileList.map((profile) => {
      const item = typeof profile === 'string' ? {profile_id:profile} : profile;
      const id = norm(item.actor_id || item.profile_id || item.id) || 'ACTOR';
      const status = finiteToken(item.status || item.knowledge_status || item.evidence_status) || actorStatus;
      const capacity = finiteText(item, 'capacity', 'role');
      const proves = finiteText(item, 'proves', 'knowledge_scope', 'proof_scope');
      const doesNot = finiteText(item, 'does_not_prove', 'limitations');
      return `<li data-actor-profile="${esc(id)}" data-personal-knowledge-status="${esc(status)}"><strong>${esc(copy.actorProfile)} · ${esc(id)}</strong>${capacity ? `<span>${esc(capacity)}</span>` : ''}<code>${esc(status)}</code>${proves ? `<p><b>${esc(copy.proves)}:</b> ${esc(proves)}</p>` : ''}${doesNot ? `<p><b>${esc(copy.doesNotProve)}:</b> ${esc(doesNot)}</p>` : ''}</li>`;
    }).join('')}</ul>` : `<p class="pdim-finite-empty">${esc(copy.noActorEvidence)}</p>`;
    const actorSpecificBoundary = finiteText(actor, 'boundary', 'limitations');
    return `<section class="pdim-finite-receipt" data-institutional-receipt-treatment>
      <h3>${esc(copy.institutionalReceipt)}</h3><p class="pdim-finite-rule">${esc(copy.institutionalBoundary)}</p>
      <dl class="pdim-receipt-axes">${axes}</dl><div class="pdim-finite-token" data-cross-file-acknowledgement-status="${esc(crossFileStatus)}"><strong>${esc(copy.crossFileAcknowledgement)}</strong><span>${esc(finiteTokenLabel(interlinks, crossFileStatus, receipt.root))}</span><code>${esc(crossFileStatus)}</code></div>${eventsHtml}${receiptLimit ? `<p class="pdim-finite-rule">${esc(receiptLimit)}</p>` : ''}
      <section class="pdim-finite-actors" data-actor-specific-knowledge data-personal-knowledge-status="${esc(actorKnowledgeStatus)}" data-actor-receipt-status="${esc(actorReceiptStatus)}" data-actor-source-status="${esc(actorStatus)}"><h3>${esc(copy.actorKnowledge)}</h3><p class="pdim-warning">${esc(copy.actorBoundary)}</p>${actorSpecificBoundary ? `<p class="pdim-finite-rule">${esc(actorSpecificBoundary)}</p>` : ''}<div class="pdim-actor-status-grid"><div class="pdim-finite-token"><strong>${esc(copy.actorReceiptStatus)}</strong><span>${esc(finiteTokenLabel(interlinks, actorReceiptStatus, actor.receipt_status))}</span><code>${esc(actorReceiptStatus)}</code></div><div class="pdim-finite-token"><strong>${esc(copy.actorKnowledgeStatus)}</strong><span>${esc(finiteTokenLabel(interlinks, actorKnowledgeStatus, actor.knowledge_status))}</span><code>${esc(actorKnowledgeStatus)}</code></div><div class="pdim-finite-token"><strong>${esc(copy.actorSourceStatus)}</strong><span>${esc(finiteTokenLabel(interlinks, actorStatus, actor))}</span><code>${esc(actorStatus)}</code></div></div>${actorHtml}</section>
    </section>`;
  }

  function finiteTestPanel(disposition, record, byId, interlinks) {
    const selected = record && record.Master_ID;
    const test = disposition && disposition.finite_test;
    const complete = finiteTestComplete(disposition);
    if (!test || typeof test !== 'object') return `<section class="pdim-finite-test is-unavailable" data-finite-test-panel data-master-id="${esc(selected)}" data-finite-test-status="UNAVAILABLE" aria-labelledby="pdim-finite-${esc(selected)}"><p class="pdim-finite-kicker">${esc(copy.finiteAudit)} · ${esc(selected)}</p><h2 id="pdim-finite-${esc(selected)}">${esc(copy.finiteUnavailable)}</h2><p class="pdim-warning">${esc(copy.finiteAuditBoundary)}</p></section>`;
    const question = finiteText(test, 'question', 'finite_question');
    const recordedObject = norm(test.recorded_object);
    const attribution = norm(test.attribution);
    const sourceNeeded = finiteText(test, 'source_needed', 'source_requirement');
    const sourceStatus = norm(test.current_source_status || test.source_status) || 'STATUS_NOT_MODELLED';
    const contrary = finiteText(test, 'contrary', 'contrary_explanation', 'strongest_contrary', 'strongest_contrary_or_innocent_explanation');
    const organ = finiteOrgan(test);
    const procedural = finiteText(test, 'procedural_availability');
    const decision = finiteText(test, 'decision_dependency');
    const confirmed = finiteText(test, 'if_confirmed');
    const refuted = finiteText(test, 'if_refuted');
    const related = finiteRelatedEntries(test, disposition, interlinks, selected, byId);
    const status = complete ? 'AUDITED' : 'INCOMPLETE';
    return `<section class="pdim-finite-test" data-finite-test-panel data-master-id="${esc(selected)}" data-finite-test-status="${status}" aria-labelledby="pdim-finite-${esc(selected)}">
      <header class="pdim-finite-head"><div><p class="pdim-finite-kicker">${esc(copy.finiteAudit)} · ${esc(selected)} · ${esc(labelFor(record))}</p><h2 id="pdim-finite-${esc(selected)}" data-finite-question>${esc(question || copy.finiteUnavailable)}</h2></div><div class="pdim-finite-model-status" data-model-status="${status}"><span>${esc(complete ? copy.finiteReady : copy.finiteIncomplete)}</span><code>${status}</code></div></header>
      <p class="pdim-finite-boundary">${esc(copy.finiteAuditBoundary)}</p>
      <div class="pdim-finite-core">
        <section data-finite-recorded-object data-recorded-object="${esc(recordedObject)}"><h3>${esc(copy.recordedObject)}</h3><p>${esc(recordedObject || '—')}</p></section>
        <section data-finite-attribution data-attribution-status="${esc(attribution || 'STATUS_NOT_MODELLED')}"><h3>${esc(copy.attribution)}</h3><p><code>${esc(attribution || 'STATUS_NOT_MODELLED')}</code></p></section>
        <section class="pdim-finite-source"><h3>${esc(copy.sourceNeeded)}</h3><p>${esc(sourceNeeded || '—')}</p><div class="pdim-finite-token" data-finite-source-status="${esc(sourceStatus)}"><strong>${esc(copy.currentSourceStatus)}</strong><span>${esc(finiteTokenLabel(interlinks, sourceStatus, test))}</span><code>${esc(sourceStatus)}</code></div>${finiteSourcesHtml(test, interlinks)}</section>
        <section data-finite-contrary><h3>${esc(copy.contrary)}</h3><p>${esc(contrary || '—')}</p></section>
        <section data-finite-competent-organ data-competent-organ-status="${esc(organ.status || 'STATUS_NOT_MODELLED')}"><h3>${esc(copy.competentOrgan)}</h3><p>${esc(organ.candidate || '—')}</p><code>${esc(organ.status || 'STATUS_NOT_MODELLED')}</code><h4>${esc(copy.proceduralAvailability)}</h4><p>${esc(procedural || '—')}</p></section>
        <section data-finite-decision-dependency><h3>${esc(copy.decisionDepends)}</h3><p>${esc(decision || '—')}</p></section>
      </div>
      <section class="pdim-finite-related" data-finite-related><h3>${esc(copy.directRelated)}</h3><ul data-finite-related-direct>${finiteRelatedHtml(related.direct, byId, copy.noDirectRelated)}</ul><h3>${esc(copy.contextRelated)}</h3><p class="pdim-warning">${esc(copy.contextBoundary)}</p><ul data-finite-related-context>${finiteRelatedHtml(related.context, byId, copy.noContextRelated)}</ul></section>
      <div class="pdim-finite-outcomes"><section data-finite-if-confirmed><h3>${esc(copy.ifConfirmed)}</h3><p>${esc(confirmed || '—')}</p></section><section data-finite-if-refuted><h3>${esc(copy.ifRefuted)}</h3><p>${esc(refuted || '—')}</p></section></div>
      ${finiteReceiptHtml(test, interlinks, disposition)}
    </section>`;
  }

  function fiscaliaMatrixHtml(interlinks, byId) {
    const matrix = interlinks && interlinks.fiscalia_office_file_matrix;
    if (!matrix) return `<section class="pdim-fiscalia-matrix is-unavailable" data-fiscalia-office-file-matrix data-model-status="UNAVAILABLE"><h3>${esc(copy.fiscaliaMatrix)}</h3><p class="pdim-warning">${esc(copy.fiscaliaMatrixUnavailable)}</p></section>`;
    const rows = Array.isArray(matrix) ? matrix : (matrix.rows || matrix.records || matrix.files || matrix.entries || []);
    const coverage = interlinks.coverage || (Array.isArray(matrix) ? {} : (matrix.coverage || {}));
    const profileCount = Number(
      coverage.fiscalia_office_file_matrix_source_profiled_record_count
      || coverage.source_controlled_episode_profile_count
      || coverage.profiled_row_count
      || coverage.source_profile_count
      || rows.filter((row) => (Array.isArray(row.source_profile_ids) && row.source_profile_ids.length) || row.episode_profile_id || row.profile_id || /SOURCE_CONTROLLED|PROFILED/.test(norm(row.profile_status || row.received_profile_status))).length
    );
    const exactCount = Number(coverage.fiscalia_office_file_matrix_exact_count || rows.filter((row) => norm(row.is_proceeding).toUpperCase() === 'TRUE').length);
    const unresolvedCount = Number(coverage.fiscalia_office_file_matrix_unverified_count || rows.filter((row) => norm(row.is_proceeding).toUpperCase() !== 'TRUE').length);
    const totalEpisodes = Array.isArray(interlinks && interlinks.fiscalia_response_episode_profiles)
      ? interlinks.fiscalia_response_episode_profiles.length : 0;

    const itemList = (items, dataAttribute, emptyText) => {
      const list = Array.isArray(items) ? items : [];
      if (!list.length) return `<span class="pdim-fiscalia-empty">${esc(emptyText)}</span>`;
      return `<ul ${dataAttribute}>${list.map((item) => {
        const value = typeof item === 'string' ? item : finiteText(item, 'text', 'label', 'summary', 'description');
        const itemCodes = typeof item === 'object' && item
          ? [...new Set([norm(item.kind), norm(item.attribution)].filter(Boolean))] : [];
        return `<li>${esc(value || '—')}${itemCodes.map((code) => `<code>${esc(code)}</code>`).join('')}</li>`;
      }).join('')}</ul>`;
    };
    const relatedList = (ids, dataAttribute, emptyText) => {
      const values = Array.isArray(ids) ? ids : [];
      if (!values.length) return `<span class="pdim-fiscalia-empty">${esc(emptyText)}</span>`;
      return `<ul ${dataAttribute}>${values.map((id) => byId.has(id)
        ? `<li><button type="button" data-trace-id="${esc(id)}">${esc(id)} · ${esc(labelFor(byId.get(id)))}</button></li>`
        : `<li><code>${esc(id)}</code></li>`).join('')}</ul>`;
    };
    const axisHtml = (row, axisKey, label) => {
      const value = row[axisKey];
      const status = finiteToken(value) || 'STATUS_NOT_MODELLED';
      const basis = row.institutional_axis_basis && row.institutional_axis_basis[axisKey] || {};
      const basisStatus = finiteToken(basis.status) || 'STATUS_NOT_MODELLED';
      const basisKind = norm(basis.basis_kind) || 'BASIS_NOT_MODELLED';
      const basisText = finiteText(basis, 'basis') || '—';
      const limitation = finiteText(basis, 'limitation', 'limitations') || '—';
      const source = basis.source || {};
      return `<div class="pdim-fiscalia-axis" data-fiscalia-axis="${esc(axisKey)}" data-axis-status="${esc(status)}" data-axis-basis-status="${esc(basisStatus)}" data-axis-basis-kind="${esc(basisKind)}"><dt>${esc(label)}</dt><dd><span>${esc(finiteTokenLabel(interlinks, status, value))}</span> <code>${esc(status)}</code><details class="pdim-axis-basis" data-fiscalia-axis-basis="${esc(axisKey)}"><summary>${esc(copy.axisBasis)}</summary><dl><div><dt>${esc(copy.basisKind)}</dt><dd><code>${esc(basisKind)}</code></dd></div><div><dt>${esc(copy.basisStatement)}</dt><dd>${esc(basisText)}</dd></div><div><dt>${esc(copy.controlledLimit)}</dt><dd>${esc(limitation)}</dd></div><div><dt>${esc(copy.basisSource)}</dt><dd><code>${esc(provenanceLabel(source))}</code></dd></div></dl></details></dd></div>`;
    };

    const rowHtml = rows.map((row, index) => {
      const masterId = norm(row.master_id || row.Master_ID || row.proceeding_master_id || row.public_master_id);
      const office = finiteText(row, 'origin_office', 'office', 'institution', 'receiving_office') || '—';
      const custodian = finiteText(row, 'current_custodian', 'custodian', 'current_office') || '—';
      const file = finiteText(row, 'file', 'file_reference', 'reference', 'official_reference') || masterId || `ROW-${index + 1}`;
      const isProceeding = norm(row.is_proceeding) || 'UNVERIFIED';
      const recordType = norm(row.record_type) || 'RECORD_TYPE_NOT_STATED';
      const canonicalSourceStatus = finiteToken(row.source_status) || 'SOURCE_STATUS_NOT_STATED';
      const profileStatus = finiteToken(row.profile_status) || 'PROFILE_STATUS_NOT_STATED';
      const received = finiteText(row, 'received_or_known', 'received_profile_state', 'received_state', 'profile_state', 'received_or_profile_state')
        || finiteToken(row.received_profile_status || row.profile_status || row.source_status) || 'STATUS_NOT_MODELLED';
      const requested = finiteText(row, 'requested', 'request') || '—';
      const response = finiteText(row, 'institutional_response', 'response_treatment', 'response', 'treatment', 'response_or_treatment') || '—';
      const gap = finiteText(row, 'unanswered_or_source_gap', 'unanswered_source_gap', 'unanswered', 'source_gap', 'open_gap', 'next_source_needed') || '—';
      const datePeriod = norm(row.date_or_period) || '—';
      const materialEvidence = Array.isArray(row.material_allegations_evidence) ? row.material_allegations_evidence : [];
      const materialReceived = Array.isArray(row.material_received) ? row.material_received : [];
      const materialInventoryGap = finiteText(row, 'material_inventory_gap') || '—';
      const directMasterIds = Array.isArray(row.related_direct_master_ids) ? row.related_direct_master_ids : [];
      const contextMasterIds = Array.isArray(row.related_context_master_ids) ? row.related_context_master_ids : [];
      const relatedProceedingsValue = row.related_proceedings_status;
      const relatedProceedingsStatus = finiteToken(relatedProceedingsValue) || 'STATUS_NOT_MODELLED';
      const assets = Array.isArray(row.related_assets) ? row.related_assets : [];
      const relatedAssetsValue = row.related_assets_status || row.related_proceedings_assets_status;
      const relatedAssetsStatus = finiteToken(relatedAssetsValue) || 'STATUS_NOT_MODELLED';
      const relatedAssetsGap = finiteText(row, 'related_assets_gap') || '—';
      const whatWasReferred = finiteText(row, 'what_was_referred') || '—';
      const whatWasExamined = finiteText(row, 'what_was_actually_examined') || '—';
      const unitaryValue = row.unitary_acknowledgement_status;
      const unitary = finiteToken(unitaryValue) || 'STATUS_NOT_MODELLED';
      const strongestContrary = finiteText(row, 'strongest_contrary', 'contrary') || '—';
      const rowBoundary = finiteText(row, 'boundary') || '—';
      const sourceProfiles = Array.isArray(row.source_profile_ids) ? row.source_profile_ids : [];
      const rowId = norm(row.row_id || row.id || masterId) || `FISCALIA-ROW-${index + 1}`;
      const identity = `<strong>${esc([masterId, file].filter(Boolean).join(' · '))}</strong>`;
      const traceIdentity = masterId && byId.has(masterId)
        ? `<button type="button" data-trace-id="${esc(masterId)}">${esc(masterId)} · ${esc(file)} · ${esc(copy.openTrace)}</button>`
        : `${esc(office)} · ${esc(file)}`;
      const axisRows = [
        ['transmission_status', copy.transmissionStatus],
        ['material_received_status', copy.materialStatus],
        ['referral_status', copy.referralStatus],
        ['registration_status', copy.registrationStatus],
        ['file_incorporation_status', copy.fileIncorporationStatus],
        ['recipient_attribution_status', copy.recipientAttributionStatus],
        ['substantive_examination_status', copy.examinationStatus],
        ['decision_use_status', copy.decisionUseStatus],
        ['cross_file_acknowledgement_status', copy.crossFileAcknowledgement]
      ].map(([axisKey, label]) => axisHtml(row, axisKey, label)).join('');
      return `<details class="pdim-fiscalia-row" data-fiscalia-row="${esc(rowId)}" data-master-id="${esc(masterId)}" data-is-proceeding="${esc(isProceeding)}" data-record-type="${esc(recordType)}" data-canonical-source-status="${esc(canonicalSourceStatus)}" data-profile-status="${esc(profileStatus)}" data-related-proceedings-status="${esc(relatedProceedingsStatus)}" data-related-assets-status="${esc(relatedAssetsStatus)}" data-unitary-acknowledgement-status="${esc(unitary)}"><summary><span>${esc(office)}</span>${identity}<span class="pdim-fiscalia-summary-status"><code>${esc(isProceeding)}</code><code>${esc(canonicalSourceStatus)}</code><code>${esc(profileStatus)}</code></span></summary><dl>
        <div><dt>${esc(copy.officeFile)}</dt><dd>${traceIdentity}</dd></div>
        <div><dt>${esc(copy.originOffice)}</dt><dd>${esc(office)}</dd></div>
        <div><dt>${esc(copy.currentCustodian)}</dt><dd>${esc(custodian)}</dd></div>
        <div data-fiscalia-date-period><dt>${esc(copy.datePeriod)}</dt><dd>${esc(datePeriod)}</dd></div>
        <div data-fiscalia-exactness><dt>${esc(copy.exactnessStatus)}</dt><dd><code>${esc(isProceeding)}</code></dd></div>
        <div data-fiscalia-record-type><dt>${esc(copy.recordType)}</dt><dd><code>${esc(recordType)}</code></dd></div>
        <div data-fiscalia-canonical-source><dt>${esc(copy.canonicalSourceStatus)}</dt><dd><code>${esc(canonicalSourceStatus)}</code></dd></div>
        <div data-fiscalia-profile-status><dt>${esc(copy.responseProfileStatus)}</dt><dd><code>${esc(profileStatus)}</code></dd></div>
        <div data-fiscalia-received-known><dt>${esc(copy.receivedProfile)}</dt><dd>${esc(received)}</dd></div>
        <div data-fiscalia-requested><dt>${esc(copy.requestedMaterial)}</dt><dd>${esc(requested)}</dd></div>
        <div data-fiscalia-material-evidence><dt>${esc(copy.materialEvidence)}</dt><dd>${itemList(materialEvidence, 'data-fiscalia-material-evidence-list', copy.noMaterialItemised)}</dd></div>
        <div data-fiscalia-material-inventory><dt>${esc(copy.materialReceivedInventory)}</dt><dd>${itemList(materialReceived, 'data-fiscalia-material-inventory-list', copy.noMaterialItemised)}</dd></div>
        <div data-fiscalia-material-inventory-gap><dt>${esc(copy.materialInventoryGap)}</dt><dd>${esc(materialInventoryGap)}</dd></div>
        <div data-fiscalia-related-direct><dt>${esc(copy.directRelatedProceedings)}</dt><dd>${relatedList(directMasterIds, 'data-fiscalia-related-direct-list', copy.noDirectMatrixRelated)}</dd></div>
        <div data-fiscalia-related-context><dt>${esc(copy.contextRelatedProceedings)}</dt><dd><p class="pdim-warning">${esc(copy.contextWarning)}</p>${relatedList(contextMasterIds, 'data-fiscalia-related-context-list', copy.noContextMatrixRelated)}</dd></div>
        <div data-fiscalia-related-proceedings-status><dt>${esc(copy.relatedProceedingsStatus)}</dt><dd><span>${esc(finiteTokenLabel(interlinks, relatedProceedingsStatus, relatedProceedingsValue))}</span> <code>${esc(relatedProceedingsStatus)}</code></dd></div>
        <div data-fiscalia-related-assets><dt>${esc(copy.relatedAssets)}</dt><dd>${itemList(assets, 'data-fiscalia-related-assets-list', copy.noRelatedAssets)}<span>${esc(finiteTokenLabel(interlinks, relatedAssetsStatus, relatedAssetsValue))}</span> <code>${esc(relatedAssetsStatus)}</code></dd></div>
        <div data-fiscalia-related-assets-gap><dt>${esc(copy.relatedAssetsGap)}</dt><dd>${esc(relatedAssetsGap)}</dd></div>
        <div data-fiscalia-what-referred><dt>${esc(copy.whatWasReferred)}</dt><dd>${esc(whatWasReferred)}</dd></div>
        <div data-fiscalia-what-examined><dt>${esc(copy.whatWasExamined)}</dt><dd>${esc(whatWasExamined)}</dd></div>
        <div data-fiscalia-institutional-response><dt>${esc(copy.responseTreatment)}</dt><dd>${esc(response)}</dd></div>
        <div class="pdim-fiscalia-axis-grid" data-fiscalia-axis-grid><dt>${esc(copy.institutionalReceipt)}</dt><dd><dl>${axisRows}</dl></dd></div>
        <div data-fiscalia-unitary-acknowledgement><dt>${esc(copy.unitaryAcknowledgementStatus)}</dt><dd><span>${esc(finiteTokenLabel(interlinks, unitary, unitaryValue))}</span> <code>${esc(unitary)}</code></dd></div>
        <div data-fiscalia-strongest-contrary><dt>${esc(copy.strongestContrary)}</dt><dd>${esc(strongestContrary)}</dd></div>
        <div data-fiscalia-unanswered-gap><dt>${esc(copy.unansweredGap)}</dt><dd>${esc(gap)}</dd></div>
        <div data-fiscalia-row-boundary><dt>${esc(copy.rowBoundary)}</dt><dd>${esc(rowBoundary)}</dd></div>
        <div data-fiscalia-source-profiles><dt>${esc(copy.sourceProfiles)}</dt><dd>${sourceProfiles.length ? sourceProfiles.map((id) => `<code>${esc(id)}</code>`).join(' ') : `<code>NO_SOURCE_CONTROLLED_PROFILE</code>`}</dd></div>
      </dl></details>`;
    }).join('');
    return `<section class="pdim-fiscalia-matrix" data-fiscalia-office-file-matrix data-row-count="${rows.length}" data-exact-count="${exactCount}" data-unverified-count="${unresolvedCount}" data-profiled-count="${profileCount}" data-response-episode-count="${totalEpisodes}"><header><div><p class="pdim-finite-kicker">P05 · ${esc(copy.fiscaliaMatrix)}</p><h3>${esc(copy.fiscaliaMatrix)}</h3></div><div class="pdim-fiscalia-counts"><strong>${rows.length}</strong><span>${esc(copy.fiscaliaRows)}</span><b>${exactCount} ${esc(copy.fiscaliaExactRows)}</b><b>${unresolvedCount} ${esc(copy.fiscaliaUnresolvedRows)}</b><b>${profileCount} ${esc(copy.fiscaliaProfiled)}</b><b>${totalEpisodes} ${esc(copy.controlledEpisodes)}</b></div></header><p class="pdim-warning"><strong>NOT_LOCATED:</strong> ${esc(copy.noUnitaryAcknowledgement)}</p><p class="pdim-finite-rule">${esc(copy.fiscaliaModelBoundary)}</p><div class="pdim-fiscalia-rows">${rowHtml}</div></section>`;
  }

  function renderTrace(root, selected, byId, prism, interlinks, fiscaliaByMasterId, communityAuthorityByMasterId) {
    const r = byId.get(selected); if (!r) return;
    const disposition = interlinks && (interlinks.node_dispositions || []).find((entry) => entry.master_id === selected);
    const relationshipById = new Map(((interlinks && interlinks.relationships) || []).map((relationship) => [relationship.id, relationship]));
    const clusterById = new Map(((interlinks && interlinks.context_clusters) || []).map((cluster) => [cluster.id, cluster]));
    const registryRelationships = disposition ? (disposition.relationship_ids || []).map((id) => relationshipById.get(id)).filter(Boolean) : [];
    const directHtml = registryRelationships.length ? registryRelationships.map((relationship) => {
      const otherId = relationship.from_master_id === selected ? relationship.to_master_id : relationship.from_master_id;
      const other = byId.get(otherId);
      return `<li data-interlink-disposition data-classification="DIRECT_PROCEDURAL_EDGE"><button type="button" data-trace-id="${esc(otherId)}"><strong>${esc(catalogLabel(interlinks.relationship_type_catalog, relationship.relationship_type))}</strong> · ${esc(otherId)} · ${esc(other ? labelFor(other) : otherId)}</button><p>${esc(localized(relationship, 'why'))}</p>${localized(relationship, 'limitations') ? `<small><strong>${esc(copy.limitations)}:</strong> ${esc(localized(relationship, 'limitations'))}</small>` : ''}${provenanceHtml(relationship)}</li>`;
    }).join('') : `<li class="pdim-none">${copy.noDirect}</li>`;

    const contexts = disposition ? (disposition.context_cluster_ids || []).map((id) => clusterById.get(id)).filter(Boolean) : [];
    const contextHtml = contexts.length ? contexts.map((cluster) => {
      const members = (cluster.member_master_ids || []).filter((id) => id !== selected && byId.has(id));
      return `<li data-interlink-disposition data-classification="CONTROLLED_CONTEXTUAL_BRIDGE"><strong>${esc(localized(cluster, 'label') || catalogLabel(interlinks.context_type_catalog, cluster.context_type))}</strong><p>${esc(localized(cluster, 'why'))}</p><div class="pdim-context-members">${members.map((id) => `<button type="button" data-trace-id="${esc(id)}">${esc(id)} · ${esc(labelFor(byId.get(id)))}</button>`).join('')}</div>${localized(cluster, 'limitations') ? `<small><strong>${esc(copy.limitations)}:</strong> ${esc(localized(cluster, 'limitations'))}</small>` : ''}${provenanceHtml(cluster)}</li>`;
    }).join('') : `<li class="pdim-none">${copy.noContext}</li>`;

    const prismMatches = prismMatchesForId(prism, selected);
    const prismHtml = prismMatches.length ? prismMatches.map(({prop, lane, cell}) => `
      <li><button type="button" data-prism-prop="${esc(prop.id)}" data-prism-lane="${esc(lane.id)}"><strong>${esc(prop.id)} · ${esc(propTitle(prop))}</strong><span>${esc(laneLabel(lane))} · ${esc(statusLabel(prism, cell.status))} · ${esc(treatmentLabel(prism, cell.treatment))}</span></button></li>`).join('')
      : `<li class="pdim-none">${copy.noPrismConnections}</li>`;
    const fileFiniteTest = isExactProceeding(r) ? finiteTestPanel(disposition, r, byId, interlinks) : '';

    const holder = root.querySelector('[data-trace-panel]');
    const fiscaliaConnection = fiscaliaByMasterId && fiscaliaByMasterId[selected];
    const fiscaliaHref = new URL(lang === 'es' ? 'es/fiscalia-comunicaciones-procedimientos/' : 'en/public-prosecution-communications-proceedings/', repoBase).href;
    const communityAuthorityConnection = communityAuthorityByMasterId && communityAuthorityByMasterId[selected];
    const communityAuthorityHref = new URL(lang === 'es' ? 'es/actas-comunidad-autoridades-publicas/' : 'en/community-actas-public-authorities/', repoBase).href;
    holder.setAttribute('tabindex', '-1');
    holder.setAttribute('aria-labelledby', 'pdim-trace-result-title');
    holder.innerHTML = `
      <h2 id="pdim-trace-result-title" class="pdim-trace-result-title">${copy.trace}: ${esc(selected)}</h2>
      <div class="pdim-trace-identity">${card(r, false)}
        <dl><div><dt>${copy.source}</dt><dd>${esc(r.Source_Status || '—')}</dd></div><div><dt>${copy.gap}</dt><dd>${esc(r.Open_Reference_Gap || '—')}</dd></div><div><dt>${copy.now}</dt><dd>${esc([r.Current_Custodian, r.Status, r.Latest_Known_Event].filter(Boolean).join(' — ') || '—')}</dd></div></dl>
      </div>
      <p class="pdim-record-backlink"><a href="${esc(`${registerRoute}#record-${encodeURIComponent(selected)}`)}">${esc(copy.openRegisterRecord)} · ${esc(selected)} →</a></p>
      ${fileFiniteTest}
      ${fiscaliaConnection ? `<p class="pdim-record-backlink"><a data-fiscalia-master-id="${esc(selected)}" href="${esc(fiscaliaHref)}#file=${encodeURIComponent(selected)}">${esc(copy.fiscaliaCommunications)} · ${esc(fiscaliaConnection.event_count)} →</a></p>` : ''}
      ${communityAuthorityConnection ? `<p class="pdim-record-backlink"><a data-community-authority-master-id="${esc(selected)}" href="${esc(communityAuthorityHref)}#authority=${encodeURIComponent(selected)}">${esc(copy.communityAuthority)} →</a></p>` : ''}
      ${disposition ? `<section class="pdim-trace-disposition" data-interlink-disposition data-classification="${esc(disposition.primary_classification)}"><h2>${esc(copy.classification)}: ${esc(catalogLabel(interlinks.classification_catalog, disposition.primary_classification))}</h2><p>${esc(localized(disposition, 'why'))}</p>${localized(disposition, 'limitations') ? `<small><strong>${esc(copy.limitations)}:</strong> ${esc(localized(disposition, 'limitations'))}</small>` : ''}${localized(disposition, 'next_source_needed') ? `<small><strong>${esc(copy.nextSource)}:</strong> ${esc(localized(disposition, 'next_source_needed'))}</small>` : ''}</section>` : isExactProceeding(r) ? `<section class="pdim-trace-disposition" data-interlink-disposition data-classification="REGISTRY_NOT_AVAILABLE"><h2>${esc(copy.unresolvedReconnection)}</h2><p>${esc(copy.interlinkUnavailable)}</p></section>` : `<section class="pdim-trace-disposition" data-interlink-disposition data-classification="NOT_EXACT_PROCEEDING_RECORD"><h2>${esc(copy.classification)}: ${esc(copy.notExactClassification)}</h2><p>${esc(copy.notExactTrace)}</p></section>`}
      <div class="pdim-rel-grid">
        <section><h2>${copy.directTitle}</h2><ul class="pdim-rel-list">${directHtml}</ul></section>
        <section><h2>${copy.contextTitle}</h2><p class="pdim-warning">${copy.contextWarning}</p><ul class="pdim-rel-list">${contextHtml}</ul></section>
      </div>
      <section class="pdim-prism-trace"><h2>${copy.prismConnections}</h2><ul class="pdim-rel-list">${prismHtml}</ul></section>
      <div class="pdim-prism-detail" data-prism-detail aria-live="polite" tabindex="-1"><p>${prism ? esc(localized(prism.boundary, '')) : esc(copy.prismUnavailable)}</p></div>`;
    holder.focus({preventScroll:true});
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    holder.scrollIntoView({behavior: reduced ? 'auto' : 'smooth', block:'start'});
  }

  function renderMap(root, rows, filters) {
    const body = root.querySelector('[data-view-body]');
    const q = key(filters.search.value); const track = filters.track.value;
    const filtered = rows.filter((r) => {
      if (track && r.Stream !== track) return false;
      if (!q) return true;
      return key([r.Master_ID,r.Reference,r.Secondary_Reference,r.Origin_Organ,r.Current_Custodian,r.Connection,r.Object_or_Purpose,r.Status,r.Source_Status].join(' ')).includes(q);
    });
    if (!filtered.length) { body.innerHTML = `<p class="pdim-empty">${copy.empty}</p>`; return; }
    const groups = new Map(); filtered.forEach((r) => { const s = norm(r.Stream) || 'Unclassified'; if (!groups.has(s)) groups.set(s, []); groups.get(s).push(r); });
    body.innerHTML = `<div class="pdim-track-map">${Array.from(groups.entries()).sort((a,b)=>a[0].localeCompare(b[0])).map(([stream, group]) => `<section class="pdim-track"><header><h2>${esc(stream)}</h2><span>${group.length}</span></header><div class="pdim-node-grid">${group.sort((a,b)=>firstYear(a.Date_or_Period)-firstYear(b.Date_or_Period)).map((r)=>card(r)).join('')}</div></section>`).join('')}</div>`;
  }

  function renderChronology(root, rows, filters) {
    const body = root.querySelector('[data-view-body]');
    const q = key(filters.search.value); const track = filters.track.value;
    const filtered = rows.filter((r) => (!track || r.Stream === track) && (!q || key([r.Master_ID,r.Reference,r.Origin_Organ,r.Connection,r.Object_or_Purpose,r.Status].join(' ')).includes(q))).sort((a,b) => firstYear(a.Date_or_Period)-firstYear(b.Date_or_Period) || labelFor(a).localeCompare(labelFor(b)));
    body.innerHTML = `<p class="pdim-note">${copy.approximate}</p><ol class="pdim-chronology">${filtered.map((r) => `<li><time>${esc(r.Date_or_Period || '—')}</time>${card(r)}</li>`).join('')}</ol>`;
  }

  const laneLabel = (lane) => localized(lane, '') || lane.id;
  const propTitle = (prop) => localized(prop, 'title') || prop.id;
  const propQuestion = (prop) => localized(prop, 'question');
  const propPeriod = (prop) => localized(prop, 'period') || prop.period || '';
  const cellNote = (cell) => localized(cell, 'note');
  const humanToken = (value) => norm(value).replaceAll('_', ' ').toLowerCase().replace(/^./, (c) => c.toUpperCase());

  function sortedProps(prism, audience) {
    return prism.propositions.slice().sort((a, b) => {
      const ap = a.audience_priority && Number.isFinite(a.audience_priority[audience]) ? a.audience_priority[audience] : 999;
      const bp = b.audience_priority && Number.isFinite(b.audience_priority[audience]) ? b.audience_priority[audience] : 999;
      return ap - bp || Number(a.sort || 9999) - Number(b.sort || 9999) || a.id.localeCompare(b.id);
    });
  }

  function statusLabel(prism, status) {
    const meta = prism.statuses && prism.statuses[status];
    return localized(meta, '') || status;
  }

  function treatmentLabel(prism, treatment) {
    const meta = prism.treatments && prism.treatments[treatment];
    return localized(meta, '') || humanToken(treatment);
  }

  function attributionLabel(prism, attribution) {
    const meta = prism.attribution_classes && prism.attribution_classes[attribution];
    return localized(meta, '') || humanToken(attribution);
  }

  function evidenceStatusLabel(prism, status) {
    const meta = prism.evidence_statuses && prism.evidence_statuses[status];
    return localized(meta, '') || humanToken(status);
  }

  function audienceLens(prism, state) {
    return prism.audience_lenses.find((a) => a.id === state.audience) || prism.audience_lenses[0];
  }

  function sourceLinks(prism, prop) {
    const catalog = prism.source_catalog || {};
    return (prop.source_ids || []).map((id) => ({id, source: catalog[id]})).filter((item) => item.source).map(({id, source}) => {
      const href = source[`href_${lang}`] || source.href_en || source.href_es;
      const label = source[`label_${lang}`] || source.label_en || source.label_es || id;
      return `<li><a href="${esc(new URL(href, repoBase).href)}"><strong>${esc(label)}</strong><span>${esc(id)} · ${esc(evidenceStatusLabel(prism, source.evidence_status))}</span></a></li>`;
    }).join('');
  }

  function renderPrismDetail(scope, prism, interlinks, byId, propId, laneId) {
    const prop = prism.propositions.find((p) => p.id === propId);
    const lane = prism.lanes.find((l) => l.id === laneId);
    if (!prop || !lane) return;
    const cell = prop.cells && prop.cells[laneId];
    const holder = scope.querySelector('[data-prism-detail]');
    if (!holder) return;
    const ids = cell && Array.isArray(cell.master_ids) ? cell.master_ids : [];
    const action = prop.actionability || {};
    const sources = sourceLinks(prism, prop);
    const gaps = cell && Array.isArray(cell.representation_gap_ids) ? cell.representation_gap_ids : [];
    const evidenceToken = cell.evidence_status || prop.source_status || '—';
    holder.innerHTML = `
      <div class="pdim-prism-detail-head"><div><span class="pdim-id">${esc(prop.id)} · ${esc(propPeriod(prop))}</span><h3>${esc(propTitle(prop))}</h3><p>${esc(propQuestion(prop))}</p></div><div class="pdim-detail-statuses"><span class="pdim-prism-status" data-prism-status="${esc(cell.status)}">${esc(statusLabel(prism, cell.status))}</span><span class="pdim-treatment">${esc(treatmentLabel(prism, cell.treatment))}</span></div></div>
      <dl class="pdim-dependency-grid">
        <div><dt>${copy.why}</dt><dd><strong>${esc(laneLabel(lane))}</strong> — ${esc(cellNote(cell))}</dd></div>
        <div><dt>${copy.evidenceStatus}</dt><dd><span>${esc(evidenceStatusLabel(prism, evidenceToken))}</span><code>${esc(evidenceToken)}</code></dd></div>
        <div><dt>${copy.attribution}</dt><dd>${esc(attributionLabel(prism, prop.attribution))}</dd></div>
        <div><dt>${copy.contrary}</dt><dd>${esc(localized(prop.contrary_record, '') || '—')}</dd></div>
        <div><dt>${copy.decisionDepends}</dt><dd>${esc(localized(cell, 'decision') || localized(prop.decision_dependency, '') || '—')}</dd></div>
        <div><dt>${copy.sourceNeeded}</dt><dd>${esc(localized(action.source_needed, '') || '—')}</dd></div>
        <div><dt>${copy.competentOrgan}</dt><dd>${esc(localized(action.competent_organ, '') || '—')}</dd></div>
        <div><dt>${copy.ifConfirmed}</dt><dd>${esc(localized(action.if_confirmed, '') || '—')}</dd></div>
        <div><dt>${copy.ifRefuted}</dt><dd>${esc(localized(action.if_refuted, '') || '—')}</dd></div>
        <div><dt>${copy.representation}</dt><dd><code>${esc(cell.representation_lineage_status || '—')}</code>${gaps.length ? ` · ${esc(gaps.join(', '))}` : ''}</dd></div>
      </dl>
      ${sources ? `<section class="pdim-source-links"><h4>${copy.sourceLinks}</h4><p>${esc(copy.sourceScope)}</p><ul>${sources}</ul></section>` : ''}
      ${ids.length ? `<div class="pdim-prism-id-list"><strong>${copy.masterIds}</strong>${ids.map((id) => `<button type="button" data-trace-id="${esc(id)}">${esc(id)} · ${copy.openTrace}</button>${detailUrlFor(id) ? `<a class="pdim-detail-link" href="${esc(detailUrlFor(id))}">${lang === 'es' ? 'Ficha' : 'Record'} ↗</a>` : ''}`).join('')}</div>` : ''}
      ${prop.id === 'P05' ? fiscaliaMatrixHtml(interlinks, byId) : ''}`;
    holder.focus({preventScroll:true});
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    holder.scrollIntoView({behavior: reduced ? 'auto' : 'smooth', block:'start'});
  }

  function audienceControl(prism, state) {
    return `<label class="pdim-prism-audience">${copy.audience}<select data-prism-audience>${prism.audience_lenses.map((a) => `<option value="${esc(a.id)}"${a.id === state.audience ? ' selected' : ''}>${esc(localized(a, ''))}</option>`).join('')}</select></label>`;
  }

  function audienceQuestion(prism, state) {
    const lens = audienceLens(prism, state);
    return localized(lens, 'question');
  }

  function audiencePath(prism, state) {
    return localized(audienceLens(prism, state), 'source_path');
  }

  function renderPrism(root, prism, state) {
    const body = root.querySelector('[data-view-body]');
    const props = sortedProps(prism, state.audience);
    body.innerHTML = `
      <section class="pdim-prism-head"><div><p class="pdim-note">${esc(copy.matrixLead)}</p><p><strong>${esc(audienceQuestion(prism, state))}</strong></p><p>${esc(audiencePath(prism, state))}</p></div>${audienceControl(prism, state)}</section>
      <div class="pdim-prism-table-wrap"><table class="pdim-prism-table"><caption>${esc(copy.matrixCaption)}</caption><thead><tr><th scope="col">${copy.proposition}</th>${prism.lanes.map((lane) => `<th scope="col">${esc(laneLabel(lane))}</th>`).join('')}</tr></thead><tbody>${props.map((prop) => `<tr><th scope="row"><span>${esc(propPeriod(prop))}</span><strong>${esc(propTitle(prop))}</strong><small>${esc(evidenceStatusLabel(prism, prop.source_status || ''))}</small></th>${prism.lanes.map((lane) => { const cell = prop.cells[lane.id]; const aria = `${propTitle(prop)} · ${laneLabel(lane)} · ${statusLabel(prism, cell.status)} · ${treatmentLabel(prism, cell.treatment)}`; return `<td><button type="button" class="pdim-prism-cell" aria-label="${esc(aria)}" data-prism-status="${esc(cell.status)}" data-prism-prop="${esc(prop.id)}" data-prism-lane="${esc(lane.id)}"><span>${esc(statusLabel(prism, cell.status))}</span><small>${esc(treatmentLabel(prism, cell.treatment))}</small></button></td>`; }).join('')}</tr>`).join('')}</tbody></table></div>
      <div class="pdim-prism-legend">${Object.entries(prism.statuses).map(([status, meta]) => `<span data-prism-status="${esc(status)}"><b></b>${esc(localized(meta, ''))}</span>`).join('')}</div>
      <div class="pdim-prism-detail" data-prism-detail aria-live="polite" tabindex="-1"><p>${esc(localized(prism.boundary, ''))}</p></div>`;
  }

  function renderParallelLanes(root, prism, state) {
    const body = root.querySelector('[data-view-body]');
    const props = prism.propositions.slice().sort((a,b) => Number(a.sort || 9999) - Number(b.sort || 9999));
    const priority = new Set(sortedProps(prism, state.audience).slice(0, 3).map((p) => p.id));
    body.innerHTML = `
      <section class="pdim-prism-head"><div><p class="pdim-note">${esc(copy.lanesLead)}</p><p><strong>${esc(audienceQuestion(prism, state))}</strong></p><p>${esc(audiencePath(prism, state))}</p></div>${audienceControl(prism, state)}</section>
      <div class="pdim-swimlane-wrap"><table class="pdim-swimlane"><caption>${esc(copy.swimCaption)}</caption><thead><tr><th scope="col">${copy.period}</th><th scope="col">${copy.proposition}</th>${prism.lanes.map((lane) => `<th scope="col" data-lane-heading="${esc(lane.id)}">${esc(laneLabel(lane))}</th>`).join('')}</tr></thead><tbody>${props.map((prop) => `<tr class="${priority.has(prop.id) ? 'is-lens-priority' : ''}"><th scope="row"><time>${esc(propPeriod(prop))}</time><span>${esc(prop.id)}</span>${priority.has(prop.id) ? `<b>${copy.priority}</b>` : ''}</th><td class="pdim-swim-event"><strong>${esc(propTitle(prop))}</strong><span>${esc(propQuestion(prop))}</span></td>${prism.lanes.map((lane) => { const cell = prop.cells[lane.id]; return `<td><button type="button" class="pdim-swim-cell" data-prism-status="${esc(cell.status)}" data-prism-prop="${esc(prop.id)}" data-prism-lane="${esc(lane.id)}"><strong>${esc(statusLabel(prism, cell.status))}</strong><span>${esc(treatmentLabel(prism, cell.treatment))}</span></button></td>`; }).join('')}</tr>`).join('')}</tbody></table></div>
      <div class="pdim-prism-detail" data-prism-detail aria-live="polite" tabindex="-1"><p>${esc(localized(prism.boundary, ''))}</p></div>`;
  }

  function renderIsolation(root, prism, interlinks, state, byId, rows) {
    const body = root.querySelector('[data-view-body]');
    const options = rows.filter(isExactProceeding).map((record) => ({
      id: record.Master_ID,
      record,
      matches: prismMatchesForId(prism, record.Master_ID)
    })).sort((a, b) => labelFor(a.record).localeCompare(labelFor(b.record)) || a.id.localeCompare(b.id));
    const coveredOptions = options.filter((item) => item.matches.length);
    const uncoveredOptions = options.filter((item) => !item.matches.length);
    if (!state.isolationId || (state.isolationId !== '__FULL__' && !options.some((item) => item.id === state.isolationId))) state.isolationId = '__FULL__';
    const selected = options.find((item) => item.id === state.isolationId) || null;
    const dispositionById = new Map((interlinks.node_dispositions || []).map((entry) => [entry.master_id, entry]));
    const finiteAuditCount = options.filter((item) => finiteTestComplete(dispositionById.get(item.id))).length;
    const finitePositiveCount = options.filter((item) => finiteHasPositiveProof(dispositionById.get(item.id))).length;
    const relationshipById = new Map((interlinks.relationships || []).map((relationship) => [relationship.id, relationship]));
    const clusterById = new Map((interlinks.context_clusters || []).map((cluster) => [cluster.id, cluster]));
    const disposition = selected ? dispositionById.get(selected.id) : null;
    const selectedRelationships = disposition ? (disposition.relationship_ids || []).map((id) => relationshipById.get(id)).filter(Boolean) : [];
    const selectedClusters = disposition ? (disposition.context_cluster_ids || []).map((id) => clusterById.get(id)).filter(Boolean) : [];
    const reconnectIds = new Set();
    const linkedPrismPropIds = new Set();
    if (selected) {
      selectedRelationships.forEach((relationship) => {
        reconnectIds.add(relationship.from_master_id);
        reconnectIds.add(relationship.to_master_id);
      });
      selectedClusters.forEach((cluster) => {
        if (cluster.context_type === 'CASE_PRISM_PROPOSITION') {
          const propositionId = norm(cluster.source && cluster.source.record_id);
          if (propositionId) linkedPrismPropIds.add(propositionId);
        } else if (['RECORDED_CONNECTION', 'SOURCE_CONTROLLED_CORRIDOR'].includes(cluster.context_type)) {
          (cluster.member_master_ids || []).forEach((id) => reconnectIds.add(id));
        }
      });
      reconnectIds.delete(selected.id);
    }
    const props = sortedProps(prism, state.audience);
    const direct = [];
    const outside = [];
    if (selected) props.forEach((prop) => {
      const exactMatches = prism.lanes.map((lane) => ({lane, cell: prop.cells[lane.id]})).filter(({cell}) => cell.status !== 'OUTSIDE' && Array.isArray(cell.master_ids) && cell.master_ids.includes(selected.id));
      exactMatches.filter(({cell}) => cell.status === 'DIRECT').forEach(({lane, cell}) => direct.push({prop, cell, lane}));
      const sourceLanes = prism.lanes.filter((lane) => {
        const cell = prop.cells[lane.id];
        if (cell.status === 'OUTSIDE' || (cell.status === 'DIRECT' && Array.isArray(cell.master_ids) && cell.master_ids.includes(selected.id))) return false;
        if (linkedPrismPropIds.has(prop.id)) return true;
        if (!Array.isArray(cell.master_ids)) return false;
        if (cell.master_ids.includes(selected.id)) return true;
        return cell.status === 'DIRECT' && cell.master_ids.some((id) => reconnectIds.has(id));
      });
      if (sourceLanes.length) {
        const lane = sourceLanes[0];
        outside.push({prop, cell: prop.cells[lane.id], lane, sourceLanes});
      }
    });
    const item = ({prop, cell, lane, sourceLanes=[]}) => `<li><button type="button" data-prism-prop="${esc(prop.id)}" data-prism-lane="${esc(lane.id)}"><span class="pdim-prism-status" data-prism-status="${esc(cell.status)}">${esc(statusLabel(prism, cell.status))}</span><strong>${esc(propTitle(prop))}</strong></button><p>${esc(cellNote(cell))}</p>${sourceLanes.length ? `<small><strong>${copy.laneSource}:</strong> ${esc(sourceLanes.map((sourceLane) => `${laneLabel(sourceLane)} — ${statusLabel(prism, prop.cells[sourceLane.id].status)}`).join(' · '))}</small>` : ''}</li>`;
    const mini = `<div class="pdim-isolation-map" data-isolation-mode="${selected ? 'isolated' : 'full'}"><table><caption>${selected ? `${copy.isolatedMode}: ${selected.id}` : copy.fullCorpus}</caption><thead><tr><th scope="col">${copy.proposition}</th>${prism.lanes.map((lane) => `<th scope="col">${esc(laneLabel(lane))}</th>`).join('')}</tr></thead><tbody>${props.map((prop) => `<tr><th scope="row">${esc(prop.id)} · ${esc(propTitle(prop))}</th>${prism.lanes.map((lane) => { const cell = prop.cells[lane.id]; const active = !selected || (cell.status === 'DIRECT' && Array.isArray(cell.master_ids) && cell.master_ids.includes(selected.id)); const selectionState = !selected ? '' : (active ? copy.insideSelected : copy.outsideSelected); const accessibleState = selectionState ? ` · ${selectionState}` : ''; const suppression = selected && !active ? ' disabled aria-disabled="true" tabindex="-1"' : ''; return `<td class="${active ? '' : 'is-suppressed'}"><button type="button"${suppression} aria-label="${esc(`${statusLabel(prism, cell.status)}${accessibleState}`)}" data-prism-status="${esc(cell.status)}" data-prism-prop="${esc(prop.id)}" data-prism-lane="${esc(lane.id)}"><span>${esc(statusLabel(prism, cell.status))}</span>${selected ? `<small>${esc(selectionState)}</small>` : ''}</button></td>`; }).join('')}</tr>`).join('')}</tbody></table></div>`;
    const option = (entry) => `<option value="${esc(entry.id)}" data-prism-coverage="${entry.matches.length ? 'covered' : 'unresolved'}" data-finite-test-coverage="${finiteTestComplete(dispositionById.get(entry.id)) ? 'audited' : 'unavailable'}"${selected && entry.id === selected.id ? ' selected' : ''}>${esc(entry.id)} · ${esc(labelFor(entry.record))}${entry.matches.length ? '' : ` · ${copy.noPrismCoordinate}`}</option>`;
    const optionGroups = `${coveredOptions.length ? `<optgroup label="${esc(`${copy.coveredGroup} (${coveredOptions.length})`)}">${coveredOptions.map(option).join('')}</optgroup>` : ''}${uncoveredOptions.length ? `<optgroup label="${esc(`${copy.uncoveredGroup} (${uncoveredOptions.length})`)}">${uncoveredOptions.map(option).join('')}</optgroup>` : ''}`;
    let reconnection = '';
    if (selected) {
      const directHtml = selectedRelationships.length ? selectedRelationships.map((relationship) => {
        const otherId = relationship.from_master_id === selected.id ? relationship.to_master_id : relationship.from_master_id;
        const other = byId.get(otherId);
        const limitations = localized(relationship, 'limitations');
        return `<li data-interlink-disposition data-classification="DIRECT_PROCEDURAL_EDGE"><button type="button" data-trace-id="${esc(otherId)}"><strong>${esc(catalogLabel(interlinks.relationship_type_catalog, relationship.relationship_type))}</strong> · ${esc(otherId)} · ${esc(other ? labelFor(other) : otherId)}</button><p>${esc(localized(relationship, 'why'))}</p>${limitations ? `<small><strong>${esc(copy.limitations)}:</strong> ${esc(limitations)}</small>` : ''}${provenanceHtml(relationship)}</li>`;
      }).join('') : `<li class="pdim-none">${esc(copy.noDirectSelected)}</li>`;
      const contextCounterpartIds = new Set(selectedClusters.flatMap((cluster) =>
        (cluster.member_master_ids || []).filter((id) => id !== selected.id && byId.has(id))
      ));
      const contextClusterCount = selectedClusters.length;
      const contextCounterpartCount = contextCounterpartIds.size;
      const contextHtml = selectedClusters.length ? selectedClusters.map((cluster) => {
        const members = (cluster.member_master_ids || []).filter((id) => id !== selected.id && byId.has(id));
        const limitations = localized(cluster, 'limitations');
        return `<li data-interlink-disposition data-classification="CONTROLLED_CONTEXTUAL_BRIDGE"><strong>${esc(localized(cluster, 'label') || catalogLabel(interlinks.context_type_catalog, cluster.context_type))}</strong><p>${esc(localized(cluster, 'why'))}</p><div class="pdim-context-members">${members.map((id) => `<button type="button" data-trace-id="${esc(id)}">${esc(id)} · ${esc(labelFor(byId.get(id)))}</button>`).join('')}</div>${limitations ? `<small><strong>${esc(copy.limitations)}:</strong> ${esc(limitations)}</small>` : ''}${provenanceHtml(cluster)}</li>`;
      }).join('') : `<li class="pdim-none">${esc(copy.noContextSelected)}</li>`;
      const unresolved = [];
      if (!selected.matches.length) unresolved.push(`<li data-interlink-disposition data-classification="NO_PRISM_COVERAGE"><strong>${esc(copy.noPrismCoordinate)}</strong><p>${esc(copy.noPrismCoverageSelected)}</p></li>`);
      if (disposition) {
        const classification = disposition.primary_classification;
        unresolved.push(`<li data-interlink-disposition data-classification="${esc(classification)}"><strong>${esc(copy.classification)}: ${esc(catalogLabel(interlinks.classification_catalog, classification))}</strong><p>${esc(localized(disposition, 'why'))}</p>${localized(disposition, 'limitations') ? `<small><strong>${esc(copy.limitations)}:</strong> ${esc(localized(disposition, 'limitations'))}</small>` : ''}${localized(disposition, 'next_source_needed') ? `<small><strong>${esc(copy.nextSource)}:</strong> ${esc(localized(disposition, 'next_source_needed'))}</small>` : ''}${norm(disposition.source_status) ? `<small><strong>${esc(copy.source)}:</strong> ${esc(disposition.source_status)}</small>` : ''}</li>`);
      } else unresolved.push(`<li data-interlink-disposition data-classification="REGISTRY_NOT_AVAILABLE"><strong>${esc(copy.unresolvedReconnection)}</strong><p>${esc(copy.interlinkUnavailable)}</p></li>`);
      if (selected.matches.length) unresolved.push(`<li class="pdim-none"><strong>${esc(copy.selectedCoverage)}</strong><p>${esc(copy.prismCoveredSelected)}</p></li>`);
      const fileFiniteTest = finiteTestPanel(disposition, selected.record, byId, interlinks);
      reconnection = `<section class="pdim-reconnection" data-isolation-reconnection aria-label="${esc(copy.selectedCoverage)}">
        <div class="pdim-reconnection-identity">${card(selected.record, false)}<div><p><strong>${esc(copy.selectedCoverage)}:</strong> ${esc(selected.matches.length ? copy.prismCoordinate : copy.noPrismCoordinate)}</p><a class="pdim-record-link" href="${esc(`${registerRoute}#record-${encodeURIComponent(selected.id)}`)}">${esc(copy.openRegisterRecord)} →</a></div></div>
        ${fileFiniteTest}
        <div class="pdim-reconnection-grid">
          <section data-isolation-direct><h2>${esc(copy.directReconnection)} <small>${selectedRelationships.length} ${esc(copy.relationCount)}</small></h2><p class="pdim-boundary-note">${esc(copy.directBoundary)}</p><ul class="pdim-rel-list">${directHtml}</ul></section>
          <section data-isolation-context data-context-cluster-count="${contextClusterCount}" data-context-counterpart-count="${contextCounterpartCount}"><h2>${esc(copy.contextReconnection)} <small>${contextClusterCount} ${esc(copy.clusterCount)} · ${contextCounterpartCount} ${esc(copy.counterpartCount)}</small></h2><p class="pdim-warning">${esc(copy.contextBoundary)}</p><ul class="pdim-rel-list">${contextHtml}</ul></section>
          <section data-isolation-unresolved><h2>${esc(copy.unresolvedReconnection)}</h2><ul class="pdim-rel-list">${unresolved.join('')}</ul></section>
        </div>
      </section>`;
    }
    body.innerHTML = `
      <section class="pdim-isolation-head"><div><p class="pdim-note">${esc(copy.isolationLead)}</p><p><strong>${esc(audienceQuestion(prism, state))}</strong></p><p class="pdim-warning">${esc(copy.formalBoundary)}</p><div class="pdim-isolation-coverage" data-isolation-coverage><strong>${coveredOptions.length}/${options.length}</strong><span>${esc(copy.prismCovered)}</span><small>${options.length} ${esc(copy.exactProceedings)} · ${uncoveredOptions.length} ${esc(copy.prismNotCovered)}</small><p>${esc(copy.coverageBoundary)}</p></div><div class="pdim-finite-coverage" data-finite-test-coverage data-audit-count="${finiteAuditCount}" data-positive-evidence-count="${finitePositiveCount}"><strong>${finiteAuditCount}/${options.length}</strong><span>${esc(copy.finiteAuditCoverage)}</span><small><b>${esc(copy.positiveEvidence)}:</b> ${finitePositiveCount} ${esc(copy.positiveEvidenceCount)}</small><p>${esc(copy.finiteAuditBoundary)}</p></div></div><div class="pdim-isolation-controls">${audienceControl(prism, state)}<label>${copy.chooseLane}<select data-isolation-id><option value="__FULL__"${selected ? '' : ' selected'}>${copy.fullCorpus}</option>${optionGroups}</select></label><button type="button" data-isolation-restore ${selected ? '' : 'disabled'}>${copy.restore}</button></div></section>
      ${reconnection}
      ${mini}
      <div class="pdim-isolation-grid"><section><h2>${selected ? copy.visibleAlone : copy.fullCorpus}</h2><ul>${selected ? (direct.length ? direct.map(item).join('') : `<li class="pdim-none">${copy.noVisible}</li>`) : `<li><strong>${props.length} ${copy.proposition.toLowerCase()}</strong><p>${esc(localized(prism.boundary, ''))}</p></li>`}</ul></section><section><h2>${copy.disappears}</h2><ul>${selected ? (outside.length ? outside.map(item).join('') : `<li class="pdim-none">${copy.noOutside}</li>`) : `<li class="pdim-none">${copy.noOutside}</li>`}</ul></section></div>
      <div class="pdim-prism-detail" data-prism-detail aria-live="polite" tabindex="-1"><p>${esc(localized(prism.boundary, ''))}</p></div>`;
  }

  async function init() {
    const root = document.querySelector('[data-proceedings-map]'); if (!root) return;
    try {
      const [registerRes, prismRes, interlinkRes, fiscaliaRes, communityAuthorityRes] = await Promise.all([
        fetch(registerDataUrl, {cache:'no-store'}),
        fetch(prismUrl, {cache:'no-store'}).catch(() => null),
        fetch(interlinkUrl, {cache:'no-store'}).catch(() => null),
        fetch(fiscaliaInterconnectivityUrl, {cache:'no-store'}).catch(() => null),
        fetch(communityAuthorityInterconnectivityUrl, {cache:'no-store'}).catch(() => null)
      ]);
      if (!registerRes.ok) throw new Error(`HTTP ${registerRes.status}`);
      const registerPayload = await registerRes.json();
      const rows = Array.isArray(registerPayload && registerPayload.records) ? registerPayload.records : [];
      if (!rows.length || rows.some((record) => !norm(record.Master_ID))) throw new Error('invalid public proceedings projection');
      const byId = new Map(rows.map((r) => [norm(r.Master_ID), r]));
      const tracks = Array.from(new Set(rows.map((r) => norm(r.Stream)).filter(Boolean))).sort((a,b)=>a.localeCompare(b));
      const gaps = rows.filter((r) => norm(r.Open_Reference_Gap)).length;
      let prism = null; let prismFailure = '';
      if (prismRes && prismRes.ok) {
        try {
          const candidate = await prismRes.json();
          const complete = Array.isArray(candidate.lanes) && Array.isArray(candidate.propositions) && candidate.propositions.every((prop) => candidate.lanes.every((lane) => prop.cells && prop.cells[lane.id]));
          if (!complete) throw new Error('incomplete proposition/lane denominator');
          prism = candidate;
        } catch (err) { prismFailure = err.message || String(err); }
      } else prismFailure = prismRes ? `HTTP ${prismRes.status}` : 'fetch failed';
      let interlinks = null; let interlinkFailure = '';
      if (interlinkRes && interlinkRes.ok) {
        try {
          const candidate = await interlinkRes.json();
          if (!Array.isArray(candidate.relationships) || !Array.isArray(candidate.context_clusters) || !Array.isArray(candidate.node_dispositions)) throw new Error('incomplete interlinkability registry');
          interlinks = candidate;
        } catch (err) { interlinkFailure = err.message || String(err); }
      } else interlinkFailure = interlinkRes ? `HTTP ${interlinkRes.status}` : 'fetch failed';
      let fiscaliaByMasterId = {};
      if (fiscaliaRes && fiscaliaRes.ok) {
        try {
          const fiscaliaPayload = await fiscaliaRes.json();
          fiscaliaByMasterId = fiscaliaPayload.by_master_id || {};
        } catch (_err) { fiscaliaByMasterId = {}; }
      }
      let communityAuthorityByMasterId = {};
      if (communityAuthorityRes && communityAuthorityRes.ok) {
        try {
          const communityAuthorityPayload = await communityAuthorityRes.json();
          communityAuthorityByMasterId = communityAuthorityPayload.by_master_id || {};
        } catch (_err) { communityAuthorityByMasterId = {}; }
      }
      const exactIds = new Set(rows.filter(isExactProceeding).map((record) => record.Master_ID));
      if (interlinks) {
        const dispositionIds = new Set(interlinks.node_dispositions.map((entry) => entry.master_id));
        const missing = Array.from(exactIds).filter((id) => !dispositionIds.has(id));
        const unexpected = Array.from(dispositionIds).filter((id) => !exactIds.has(id));
        if (missing.length || unexpected.length) {
          interlinkFailure = `interlinkability denominator mismatch (${missing.length} missing; ${unexpected.length} unexpected)`;
          interlinks = null;
        }
      }
      const decodeHashId = (value) => { try { return decodeURIComponent(value || ''); } catch (_err) { return ''; } };
      const readHash = () => {
        const raw = window.location.hash || '';
        if (raw.startsWith('#trace-proceeding=')) {
          const id = decodeHashId(raw.slice('#trace-proceeding='.length));
          return {view:'trace', id:byId.has(id) ? id : ''};
        }
        if (raw.startsWith('#isolation-test=')) {
          const id = decodeHashId(raw.slice('#isolation-test='.length));
          if (exactIds.has(id)) return {view:'isolation', id};
          if (byId.has(id)) return {view:'trace', id, canonicalize:true};
          return {view:'map', id:'', canonicalize:true};
        }
        const mapped = {'#map':'map', '#mapa':'map', '#trace-proceeding':'trace', '#case-prism':'prism', '#parallel-lanes':'lanes', '#isolation-test':'isolation'}[raw];
        return {view:mapped || 'map', id:''};
      };
      const initialHash = readHash();
      const state = { audience: 'all', isolationId: initialHash.view === 'isolation' && initialHash.id ? initialHash.id : '__FULL__', traceId: initialHash.view === 'trace' ? initialHash.id : '' };
      const viewToHash = {trace:'#trace-proceeding', prism:'#case-prism', lanes:'#parallel-lanes', isolation:'#isolation-test'};
      let view = initialHash.view;
      if (!prism && ['prism','lanes','isolation'].includes(view)) view = 'map';
      if (!interlinks && view === 'isolation') view = 'map';
      const directCoverage = interlinks && interlinks.coverage ? interlinks.coverage : {};
      const directGrade = interlinks
        ? `<small>${esc(directCoverage.direct_relationship_source_verified_pair_count)} ${esc(copy.directVerified)} · ${esc(directCoverage.direct_relationship_source_reported_pending_pair_count)} ${esc(copy.directPending)}</small>`
        : '';

      root.innerHTML = `
        <div class="pdim-stats"><div><strong>${rows.length}</strong><span>${copy.records}</span></div><div><strong>${tracks.length}</strong><span>${copy.tracks}</span></div><div><strong>${interlinks ? interlinks.relationships.length : '—'}</strong><span>${copy.direct}${directGrade}</span></div><div><strong>${gaps}</strong><span>${copy.gaps}</span></div></div>
        <div class="pdim-controls" data-filter-scope="map-chronology"><label>${lang==='es'?'Buscar':'Search'}<input type="search" data-map-search placeholder="${esc(copy.search)}"></label><label>${lang==='es'?'Vía':'Track'}<select data-map-track><option value="">${copy.allTracks}</option>${tracks.map((t)=>`<option>${esc(t)}</option>`).join('')}</select></label><p class="pdim-filter-scope">${esc(copy.filterScope)}</p></div>
        <div class="pdim-tabs" role="tablist" aria-label="${esc(lang === 'es' ? 'Vistas del mapa de procedimientos' : 'Proceedings map views')}"><button id="pdim-tab-map" role="tab" aria-controls="pdim-view-panel" type="button" data-view="map">${copy.map}</button><button id="pdim-tab-chronology" role="tab" aria-controls="pdim-view-panel" type="button" data-view="chronology">${copy.chronology}</button><button id="pdim-tab-trace" role="tab" aria-controls="pdim-view-panel" type="button" data-view="trace">${copy.trace}</button><button id="pdim-tab-prism" role="tab" aria-controls="pdim-view-panel" type="button" data-view="prism" ${prism ? '' : 'disabled aria-disabled="true"'}>${copy.prism}</button><button id="pdim-tab-lanes" role="tab" aria-controls="pdim-view-panel" type="button" data-view="lanes" ${prism ? '' : 'disabled aria-disabled="true"'}>${copy.lanes}</button><button id="pdim-tab-isolation" role="tab" aria-controls="pdim-view-panel" type="button" data-view="isolation" ${prism && interlinks ? '' : 'disabled aria-disabled="true"'}>${copy.isolation}</button></div>
        ${prism ? '' : `<div class="pdim-prism-unavailable" role="status"><strong>${esc(copy.prismUnavailable)}</strong><small>${esc(prismFailure)}</small></div>`}
        ${interlinks ? '' : `<div class="pdim-prism-unavailable" role="status"><strong>${esc(copy.interlinkUnavailable)}</strong><small>${esc(interlinkFailure)}</small></div>`}
        <div id="pdim-view-panel" role="tabpanel" tabindex="-1" data-view-body></div>
        <section class="pdim-trace-panel" data-trace-panel></section>
        <footer class="pdim-footer"><p>${copy.publicBoundary}</p><a href="${esc(registerRoute)}">${copy.openRegister} →</a></footer>`;

      const filters = { search: root.querySelector('[data-map-search]'), track: root.querySelector('[data-map-track]') };
      const draw = (focusSelector = '') => {
        const filtersApply = ['map', 'chronology'].includes(view);
        const filterScope = root.querySelector('[data-filter-scope]');
        if (filterScope) filterScope.hidden = !filtersApply;
        filters.search.disabled = !filtersApply;
        filters.track.disabled = !filtersApply;
        const tracePanel = root.querySelector('[data-trace-panel]');
        if (view !== 'trace' && tracePanel) tracePanel.innerHTML = '';
        if (view === 'chronology') renderChronology(root, rows, filters);
        else if (view === 'trace') {
          const body = root.querySelector('[data-view-body]');
          body.innerHTML = `<div class="pdim-picker"><label>${copy.trace}<select data-trace-select><option value="">—</option>${rows.slice().sort((a,b)=>labelFor(a).localeCompare(labelFor(b))).map((r)=>`<option value="${esc(r.Master_ID)}"${state.traceId === r.Master_ID ? ' selected' : ''}>${esc(r.Master_ID)} · ${esc(labelFor(r))}</option>`).join('')}</select></label></div>`;
          if (state.traceId && byId.has(state.traceId)) renderTrace(root, state.traceId, byId, prism, interlinks, fiscaliaByMasterId, communityAuthorityByMasterId);
        } else if (view === 'prism' && prism) renderPrism(root, prism, state);
        else if (view === 'lanes' && prism) renderParallelLanes(root, prism, state);
        else if (view === 'isolation' && prism && interlinks) renderIsolation(root, prism, interlinks, state, byId, rows);
        else renderMap(root, rows, filters);
        if (focusSelector) window.requestAnimationFrame(() => root.querySelector(focusSelector)?.focus({preventScroll:true}));
      };
      const revealActivePanel = () => window.requestAnimationFrame(() => {
        const panel = root.querySelector('[data-view-body]');
        if (!panel) return;
        panel.focus({preventScroll:true});
        const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        panel.scrollIntoView({behavior: reduced ? 'auto' : 'smooth', block:'start'});
      });
      const setTabState = () => root.querySelectorAll('[data-view]').forEach((button) => {
        const selected = button.dataset.view === view;
        button.setAttribute('aria-selected', selected ? 'true' : 'false');
        button.setAttribute('tabindex', selected ? '0' : '-1');
        if (selected) root.querySelector('[data-view-body]')?.setAttribute('aria-labelledby', button.id);
      });
      const activeHash = () => {
        if (view === 'trace' && state.traceId && byId.has(state.traceId)) return `#trace-proceeding=${encodeURIComponent(state.traceId)}`;
        if (view === 'isolation' && state.isolationId !== '__FULL__' && exactIds.has(state.isolationId)) return `#isolation-test=${encodeURIComponent(state.isolationId)}`;
        return viewToHash[view] || '';
      };
      const replaceActiveHash = () => {
        const hash = activeHash();
        window.history.replaceState(null, '', hash || (window.location.pathname + window.location.search));
      };
      const activateView = (next, updateHash = true, reveal = false) => {
        if (!next || (!prism && ['prism','lanes','isolation'].includes(next))) return;
        if (next === 'isolation' && !interlinks) return;
        view = next; setTabState(); draw();
        if (reveal) revealActivePanel();
        if (updateHash) replaceActiveHash();
      };
      filters.search.addEventListener('input', () => draw()); filters.track.addEventListener('input', () => draw());
      root.querySelectorAll('[data-view]').forEach((button) => button.addEventListener('click', () => activateView(button.dataset.view)));
      root.querySelector('.pdim-tabs').addEventListener('keydown', (ev) => {
        if (!['ArrowLeft','ArrowRight','Home','End'].includes(ev.key)) return;
        const tabs = Array.from(root.querySelectorAll('[data-view]:not([disabled])'));
        const current = tabs.indexOf(document.activeElement); if (current < 0) return;
        ev.preventDefault();
        const target = ev.key === 'Home' ? 0 : ev.key === 'End' ? tabs.length - 1 : (current + (ev.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
        tabs[target].focus(); activateView(tabs[target].dataset.view);
      });
      root.addEventListener('click', (ev) => {
        const traceButton = ev.target.closest('[data-trace-id]');
        if (traceButton && byId.has(traceButton.dataset.traceId)) { state.traceId = traceButton.dataset.traceId; activateView('trace'); return; }
        const restoreButton = ev.target.closest('[data-isolation-restore]');
        if (restoreButton) { state.isolationId = '__FULL__'; draw('[data-isolation-id]'); replaceActiveHash(); return; }
        const prismButton = ev.target.closest('[data-prism-prop][data-prism-lane]');
        if (prismButton && prism) {
          const detailScope = prismButton.closest('[data-trace-panel], [data-view-body]') || root;
          renderPrismDetail(detailScope, prism, interlinks, byId, prismButton.dataset.prismProp, prismButton.dataset.prismLane);
        }
      });
      root.addEventListener('change', (ev) => {
        if (ev.target.matches('[data-trace-select]') && ev.target.value && byId.has(ev.target.value)) { state.traceId = ev.target.value; renderTrace(root, state.traceId, byId, prism, interlinks, fiscaliaByMasterId, communityAuthorityByMasterId); replaceActiveHash(); }
        if (ev.target.matches('[data-prism-audience]')) { state.audience = ev.target.value || 'all'; draw('[data-prism-audience]'); }
        if (ev.target.matches('[data-isolation-id]')) { state.isolationId = exactIds.has(ev.target.value) ? ev.target.value : '__FULL__'; draw('[data-isolation-id]'); replaceActiveHash(); }
      });
      window.addEventListener('hashchange', () => {
        const parsed = readHash();
        state.traceId = parsed.view === 'trace' ? parsed.id : state.traceId;
        state.isolationId = parsed.view === 'isolation' && parsed.id ? parsed.id : '__FULL__';
        activateView(parsed.view, false, true);
        if (parsed.canonicalize) replaceActiveHash();
      });
      setTabState(); draw();
      if (initialHash.canonicalize) replaceActiveHash();
      if (initialHash.view !== 'map' || ['#map','#mapa'].includes(window.location.hash)) revealActivePanel();
    } catch (err) {
      root.innerHTML = `<div class="pdim-error"><strong>${copy.error}</strong><p>${esc(err.message || err)}</p></div>`;
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once:true}); else init();
})();
