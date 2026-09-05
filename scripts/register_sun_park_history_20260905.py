#!/usr/bin/env python3
"""Bounded historical intake. Registration is not verification of allegations.
Run on the isolated WORKER branch. Never merges, deploys or contacts witnesses.
The supplied 42-claim research scope is paraphrased, not a fresh native review.
"""
from pathlib import Path
from collections import Counter
from html.parser import HTMLParser
import argparse, copy, html, json, re

RELEASE = 'PD-SP-HISTORY-20260905'
HISTORY = 'assets/data/sun-park-history-register-v1.json'
ROUTES = {'es':'es/historia-sun-park-jsp-molina/index.html','en':'en/sun-park-jsp-molina-history/index.html'}
PEOPLE = [('Domingo Bello Cabrera','S01'),('José Sánchez Rodríguez','S09 S10 S11'),('José Miguel Bravo de Laguna','S03'),('José Manuel Romero','S03'),('Atilio Rodríguez','S03'),('Ana Rivero','S02'),('Pablo Rivero','S04'),('Luis Rivero','S11'),('Gonzalo Molina','S03'),('Anastasio Molina','S15 S16'),('Pablo Rivero Correa','S16'),('Antonio Peñate','S16'),('Sandra González Franquis','S08'),('María Izquierdo Bello','S08')]
ORGS = [('Sol Lanzarote, S.A.','S01'),('José Sánchez Peñate, S.A.','S16'),('J.S.P., S.L.','S16'),('Multimatrix','S14 S15'),('Victory Properties','S03'),('Realizaciones Madreselva Canarias','S03'),('ACTUA','S07 S15'),('Entidad urbanística Costa de Papagayo (denominación exacta pendiente)','S02')]
HOTELS = [('Sun Group','S11'),('Sun Park','S01 S03 S04 S11'),('Sun Royal','S02 S10 S11'),('Sun Beach','S11'),('Sun Island','S11'),('Sun Tropical','S11'),('JSP (grupo empresarial; identidad societaria por acto pendiente)','S09 S10 S11')]
# Each line: state | source IDs | English proposition and limitation | Spanish equivalent.
CLAIMS = '''speaker_correction|S15|The two dictations are Patricia's according to Gil's correction; they are not Gil's direct testimony.|Las dos notas dictadas son de Patricia según la corrección de Gil; no son testimonio directo de Gil.
identity_correction|S15 S09 S11|JSP replaces the retracted Lopesan attribution. Group, company and act-specific identity remain distinct.|JSP sustituye la atribución retirada a Lopesan. Grupo, sociedad e identidad por acto siguen siendo distintos.
reported_document|S01|The certification identifies Sol Lanzarote, S.A., represented by Domingo Bello Cabrera, in the new-building declaration. It does not establish all shareholders or financing.|La certificación identifica Sol Lanzarote, S.A., representada por Domingo Bello Cabrera, en la obra nueva; no acredita todos los socios o financiación.
reported_document|S01|Separate the 9 November 1987 deed, 25 November registration and 8 May 2014 certification. One date cannot stand for all three acts.|Se separan escritura de 9-11-1987, asiento de 25-11-1987 y certificación de 8-5-2014; una fecha no sustituye tres actos.
unverified_development|S01 S15|Anastasio Molina's alleged development role remains unverified. Recover land, company, development and first-sale instruments.|El papel promotor atribuido a Anastasio Molina sigue sin verificar; recuperar suelo, sociedades, promoción y primeras ventas.
unverified_engineering|S15|The electrical engineering and possible payment in units attributed to Sebastián Molina Petit require contracts, invoices and titles; neither is established here.|Ingeniería eléctrica y posible pago en unidades atribuidos a Sebastián Molina Petit requieren contratos, facturas y títulos; no quedan acreditados aquí.
contract_recital|S04|The contract recites municipal opening permission in January 1989 and tourism authorisation in May 1991. These differ from construction in 1987 and require original licences.|El contrato refiere apertura municipal de enero de 1989 y autorización turística de mayo de 1991, distintas de la obra de 1987; recuperar licencias originales.
contract_recital|S04|The contract recites Montelanza's incorporation on 27 June 1991. Earlier operation and its legal vehicle need separate reconstruction.|El contrato refiere constitución de Montelanza el 27-6-1991; la operación anterior y su vehículo jurídico requieren reconstrucción separada.
reported_document|S03 S04|CEXP was constituted on 29 April 2008 as a civil community. It cannot be treated as one unchanged operating company existing since 1987.|CEXP se constituyó el 29-4-2008 como comunidad civil; no puede tratarse como empresa explotadora inalterada desde 1987.
capacity_not_ownership|S03|Bravo de Laguna is recorded as representative and CEXP secretary for Realizaciones Madreselva Canarias. Representation does not establish personal beneficial ownership.|Bravo de Laguna figura como representante y secretario de CEXP por Realizaciones Madreselva Canarias; representar no acredita propiedad personal.
source_literal_recheck|S03|The minutes distinguish Rosa Molina for Acciones Canarias, Gonzalo Molina represented by Bravo, and Roque Prieto represented by Sebastián Molina Petit. Short names, mandates and person/company capacity need checking.|El acta distingue Rosa Molina por Acciones Canarias, Gonzalo Molina representado por Bravo y Roque Prieto por Sebastián Molina Petit; verificar nombres abreviados, mandatos y capacidad personal o societaria.
reservation_not_guilt|S03|Reservations recorded for Carmelo Marrero, Sebastián Molina Petit and Agustín Calzada about creating CEXP do not alone prove obstruction, refusal to sell or unlawful common purpose.|Las reservas de Carmelo Marrero, Sebastián Molina Petit y Agustín Calzada sobre crear CEXP no prueban por sí solas obstrucción, negativa a vender o propósito ilícito común.
vote_qualification|S03|74.90% supported the proposal; 10.01% opposed or reserved a decision. The latter category cannot become an individual finding of unanimous opposition.|El 74,90% apoyó; el 10,01% se opuso o reservó decisión. Esta categoría no puede convertirse en oposición individual unánime.
alternative_explanation|S03|The minutes explain the transition by the Victory Properties option and separating sellers' continuing operating risk. Preserve this contemporaneous alternative to the obstruction account.|El acta explica la transición por la opción Victory Properties y separación del riesgo operativo de vendedores; conservar esta explicación contemporánea alternativa al relato de obstrucción.
transaction_scope|S04|The 26 May 2008 operating assignment took effect on 27 May for EUR6,000. This is not an apartment or whole-property purchase price.|La cesión de explotación de 26-5-2008 surtió efecto el 27 por 6.000 euros; no es precio de apartamento o de todos los inmuebles.
contract_recital_not_title|S04|The contract recites operation of 220 apartments and Montelanza ownership of 40 commercial premises and two pools. Each ownership recital needs title verification.|El contrato refiere explotación de 220 apartamentos y propiedad de Montelanza de 40 locales y dos piscinas; cada titularidad precisa cotejo registral.
terms_not_performance|S04|Separate transitional accounting, a transition commission and receipt/payment rules were provided. Their inclusion does not prove actual performance or discharge of liabilities.|Se prevén contabilidad transitoria separada, comisión y reglas de cobros y pagos; incluirlas no prueba cumplimiento efectivo o extinción de pasivos.
inspected_copy_gap|S04|Authority, personnel and commercial-contract annexes are absent from the inspected copy, not necessarily from every archive. Recover all three before claiming full contractual coverage.|Los anexos de facultades, personal y contratos comerciales faltan en la copia revisada, no necesariamente en todos los archivos; recuperar los tres.
shared_context_not_diversion|S02|The 2007 urban-entity minutes connect Montelanza with Sun Park and Sun Royal and name Ana Rivero. Shared representation does not establish diverted bookings.|El acta urbanística de 2007 relaciona Montelanza con Sun Park y Sun Royal y nombra Ana Rivero; representación compartida no prueba desvío de reservas.
accounting_boundary|S02|Costa de Papagayo's deficit and extraordinary budget concern the urban entity. They cannot automatically be used as Sun Park hotel trading losses or owner operating contributions.|Déficit y presupuesto extraordinario de Costa de Papagayo pertenecen a la entidad urbanística; no equivalen automáticamente a pérdidas hoteleras o aportaciones de explotación.
capacity_boundary|S02|José Sánchez Rodríguez is recorded as urban-entity vice-president for Montelanza, not necessarily vice-president within Montelanza itself.|José Sánchez Rodríguez figura como vicepresidente de la entidad urbanística por Montelanza, no necesariamente con ese cargo en la propia sociedad.
limited_business_history|S09|KPMG's interview describes a JSP-Molina food-packaging business relationship. It does not prove a coordinated hotel wrongdoing scheme or identify every Molina participant.|La entrevista de KPMG describe una relación JSP-Molina en envasado alimentario; no prueba un plan hotelero ilícito ni identifica todos los participantes Molina.
unidentified_company|S10|The 89.5% passage does not expressly identify its company. Do not turn it into Sun Park or Montelanza ownership.|El pasaje del 89,5% no identifica expresamente la sociedad; no convertirlo en propiedad de Sun Park o Montelanza.
secondary_history|S11|The 2022 report connects JSP with Sun Park, Sun Royal, Sun Beach, Sun Island and Sun Tropical. It does not establish opening order, title to every property or booking diversion.|La información de 2022 relaciona JSP con Sun Park, Sun Royal, Sun Beach, Sun Island y Sun Tropical; no acredita orden de apertura, todos los títulos o desvío de reservas.
attributed_hypothesis|S15|Preferential booking allocation is part of the historical account reported by Patricia. Test allotments, reservations, availability, staff transfers, instructions and lawful alternatives.|La asignación preferente de reservas forma parte del relato histórico transmitido por Patricia; contrastar cupos, reservas, disponibilidad, personal, instrucciones y alternativas lícitas.
unverified_causation|S03 S15|Links between losses, disagreement, alleged obstruction and the 2008 sale need contemporaneous evidence. Dissatisfaction is not automatically an appropriation plan.|Los nexos entre pérdidas, desacuerdo, obstrucción alegada y venta de 2008 requieren prueba contemporánea; descontento no equivale automáticamente a plan de apropiación.
candidate_identity|S12 S13 S15|Rafael Molina Petit is a biographical candidate for the recalled official, not a confirmed substitution for Javier or Francisco, or proof of hotel ownership or misconduct.|Rafael Molina Petit es candidato biográfico para el funcionario recordado, no sustitución confirmada de Javier o Francisco ni prueba de propiedad hotelera o infracción.
ownership_unverified|S03 S15|Bravo's documented representative capacity does not establish the personal ownership remembered in the account. Retrieve conveyances and company interests.|La representación documentada de Bravo no acredita la propiedad personal recordada; recuperar escrituras y participaciones societarias.
registry_extract_limits|S06|Finca 8718's extract records CAM acquisitions of 33.33% on 23 May 2018 and 66.67% on 31 May, protocols 1083 and 1127 before José del Cerro Peñalver. It states no price or complete seller chain.|La nota de finca 8718 registra adquisiciones CAM del 33,33% el 23-5-2018 y 66,67% el 31-5, protocolos 1083 y 1127 ante José del Cerro Peñalver; no recoge precio ni cadena completa de vendedores.
filename_not_evidence|S06|Expanded seller descriptions in the filename are not wording from the registry. The deeds must establish the seller chain and transaction terms.|Las descripciones de vendedores añadidas al nombre del archivo no son texto registral; las escrituras deben acreditar cadena y condiciones.
price_comparison_unresolved|S06 S07 S15|40,000, 50,000 and 55,000 require currency, dates, properties, rights, offer/completion status and total consideration. Apparent inconsistency neither proves hidden payment nor automatically invalidates a valuation.|40.000, 50.000 y 55.000 requieren moneda, fechas, propiedades, derechos, oferta o venta y contraprestación total; una aparente discrepancia no prueba pago oculto ni invalida automáticamente una valoración.
noncash_benefit_hypothesis|S15|Shares, side payments or other seller benefits remain hypotheses with no instrument established here. Do not attribute them to later hotel brands or investors without transaction evidence.|Acciones, pagos laterales u otros beneficios siguen siendo hipótesis sin instrumento acreditado aquí; no atribuirlos a marcas o inversores posteriores sin prueba transaccional.
draft_not_final|S07|The 10 May 2018 report was commissioned by Aweswell for LPB and marked draft/subject to change. It is not a court finding or confirmed final expert opinion.|El informe de 10-5-2018 fue encargado por Aweswell para LPB y marcado borrador/sujeto a cambios; no es conclusión judicial o pericial final confirmada.
method_limit|S07|The draft questions valuation suitability, allows that an ECO valuation could be correct, and excludes detailed intra-method review. It does not alone prove fabricated comparables or intentional false valuation.|El borrador cuestiona idoneidad, permite que una valoración ECO sea correcta y excluye análisis intrametodológico detallado; no prueba por sí solo comparables inventados o falsedad intencional.
material_counterevidence|S07|The draft credits judicial intervention requiring competing third-party offers with preventing potential harm. Preserve this contrary passage; do not infer every judicial act had the same purpose or silently identify an unnamed judge.|El borrador valora favorablemente exigir ofertas competidoras por intervención judicial; conservar este pasaje contrario, sin inferir propósito único de todos los actos o identificar silenciosamente a un juez no nombrado.
common_purpose_unproven|S15|Patricia alleges continuity of purpose among successive actors. Test each actor's act or omission, capacity, duty, knowledge, communication and benefit; association or outcome alone does not prove coordination.|Patricia alega continuidad de propósito entre actores sucesivos; contrastar acto u omisión, capacidad, deber, conocimiento, comunicación y beneficio de cada uno; asociación o resultado no prueban coordinación.
private_equity_unproven|S15|Participation by private equity in the alleged plan is not established. Later investment does not automatically prove earlier knowing cooperation.|La participación de capital privado en el plan alegado no está demostrada; invertir después no prueba automáticamente cooperación consciente anterior.
source_conflict|S03 S04 S14|The press description of the operating vehicle conflicts with the civil-community documents. Preserve the discrepancy and verify rather than letting a press shorthand replace the legal instruments.|La descripción periodística del vehículo operador entra en conflicto con documentos de comunidad civil; conservar discrepancia y verificar sin sustituir instrumentos por una simplificación periodística.
proposal_not_final_outcome|S08|The BOC records a proposed sanction, defence and mitigation concerning earlier Montelanza matters. It does not establish a final sanction or deliberate diversion of hotel business.|El BOC recoge propuesta sancionadora, defensa y atenuación sobre hechos anteriores de Montelanza; no acredita sanción firme o desvío deliberado del negocio.
filename_authentication_limit|S05|The file named as a 1991 tourism licence includes later annotations; the name and annotations alone authenticate neither the original licence nor a completed change of operator.|El archivo denominado licencia turística de 1991 incluye anotaciones posteriores; nombre y anotaciones no autentican por sí solos licencia original o cambio consumado de operador.
separate_legal_relationships|S01 S03 S04|Integrated operation, ownership of each property, membership and representation are separate relationships that must be dated. One cannot substitute for the others.|Explotación integrada, titularidad de cada propiedad, pertenencia y representación son relaciones distintas y fechables; una no sustituye las otras.
identity_nonmerger|S02 S04 S11 S16|Ana Rivero, Pablo Rivero, Luis Rivero and the candidate Pablo Rivero Correa are not merged by surname. Verify identity, employment and any relationship independently.|Ana Rivero, Pablo Rivero, Luis Rivero y el candidato Pablo Rivero Correa no se fusionan por apellido; verificar identidad, empleo y relaciones independientemente.
opening_order_unverified|S11 S15|Patricia places Sun Park first among the five hotels. Building, completion and opening records for each hotel are needed before publishing that sequence as established.|Patricia sitúa Sun Park primero entre los cinco; hacen falta construcción, finalización y apertura de cada hotel antes de publicar la secuencia como acreditada.
separate_administrative_dates|S08|The BOC publication is 9 December 2008; the resolution is 25 November and the proposal 16 October. These are distinct acts, not a final-sanction finding.|La publicación BOC es de 9-12-2008, la resolución de 25-11 y la propuesta de 16-10; son actos distintos, no constatación de sanción firme.
identified_indirect_account|S15|Patricia attributes part of the early history to a conversation she places in 2012 with Asunción. No direct or personally adopted Asunción statement is held here; Patricia's later hypotheses are not automatically attributed to her.|Patricia atribuye parte de la historia a una conversación de 2012 con Asunción; aquí no consta declaración directa adoptada por Asunción y las hipótesis posteriores de Patricia no se le atribuyen automáticamente.
off_plan_account_unverified|S01 S15|Patricia describes off-plan sales to investors taking one to ten units or more. Investor numbers, parcels, developer control and consideration require original instruments.|Patricia describe ventas sobre plano a inversores de una a diez unidades o más; números, parcelas, control promotor y contraprestación requieren instrumentos originales.
profitability_account_unverified|S15|Earlier successful operation and the remembered phrase Pearl of Playa Blanca are reported characterisations, not audited results or an authenticated quotation by Asunción.|El éxito operativo anterior y la expresión recordada Perla de Playa Blanca son caracterizaciones transmitidas, no resultados auditados o cita autenticada de Asunción.
independent_statement_requested|S15 S16|The project seeks Asunción's own independently checked account and its comparison with her recorded wider-case roles. This is not a summons, contact, adopted statement, presumption of guilt or automatic addition to the five NEXUS 36 private actors.|El proyecto solicita relato propio de Asunción, verificación independiente y contraste con funciones registradas en el asunto general; no es citación, contacto, declaración adoptada, presunción de culpa o ampliación automática de los cinco actores privados de NEXUS 36.'''
SUBJECTS = ['P0001 P0002 P0004','S0018 O0085 O0086','O0084 P0166 S0013','O0084 S0013','P0175 O0084','P0015 S0013','O0014 S0013','O0014','O0006 O0005','P0168 O0089 O0006','P0174 P0168 P0015 O0012 O0015','P0015 O0006','O0006','O0014 O0088 P0168 P0169 P0170','O0014 O0006','O0014 O0006 S0013','O0014 O0006 P0172','O0014 O0006','O0091 P0171 O0014 S0013 S0014','O0091 O0014','P0167 O0091 O0014','P0167 S0018','P0167 S0018','S0012 S0013 S0014 S0015 S0016 S0017 P0173 P0167','P0002 P0004 S0013 S0014 S0015 S0016 S0017','P0002 O0014 O0087','P0016 P0002','P0168','P0144 O0007','P0007 O0009 O0010','O0007 O0087 O0002','O0019 O0042 O0007','O0057 O0058 O0001 O0002','O0090 O0057 O0058','O0057 O0058','P0002 P0009 P0010 P0011 P0012 P0057 O0007 O0005 O0006 O0002 O0003','O0020 O0019','O0087 O0002 O0006','O0014 P0178 P0179','O0014','O0005 O0006 O0002 O0003 S0013','P0171 P0172 P0173 P0176','S0012 S0013 S0014 S0015 S0016 S0017','P0178 P0179 O0014','P0002 P0004','P0175 O0084 S0013','P0002 P0004 S0013','P0002 P0004']
SOURCES = [
('S01','Registered-history certification: Sun Park parent finca 8241; issued 8 May 2014','native_summary',None),
('S02','Costa de Papagayo urban-entity minutes, 9 July 2007','native_summary',None),
('S03','CEXP constitution, minutes and civil-community statutes, 29 April 2008','native_summary',None),
('S04','Montelanza operating-assignment contract, 26 May 2008, effective 27 May','native_summary',None),
('S05','File described as 1991 tourism licence with later annotations','native_summary',None),
('S06','Informational extract, finca 8718, 27 September 2018; protocols 1083 and 1127','native_summary',None),
('S07','Aweswell/LPB valuation-reasonableness expert draft, 10 May 2018','native_summary',None),
('S08','BOC 245/033: 9 December 2008 publication; earlier resolution and proposal','public_official','https://www.gobiernodecanarias.org/boc/2008/245/033.html'),
('S09','José Sánchez Rodríguez interview: food-packaging relationship, pages 262–263','public_interview','https://kpmg.es/los-que-dejan-huella-I/262-263/'),
('S10','José Sánchez Rodríguez interview: unidentified 89.5% company, pages 264–265','public_interview','https://kpmg.es/los-que-dejan-huella-I/264-265/'),
('S11','JSP and the five Sun hotels; historical report, 6 May 2022','public_secondary','https://www.tourinews.es/empresas-turismo/canarias-lanzarote-jose-sanchez-jsp-turismo-apartahoteles_4468849_102.html'),
('S12','Historical official biography: Rafael Molina Petit appointment','public_official','https://www3.gobiernodecanarias.org/noticias/hemeroteca/toma-posesion-rafael-molina-petit-frente-consorcio-rehabilitacion-turistica/'),
('S13','Rafael Molina Petit distinction, report dated 17 December 2019','public_secondary','https://www.eldiario.es/canariasahora/sociedad/rafael-molina-encomienda-merito-gobierno_1_1184961.html'),
('S14','2008 press account described in supplied research; operator-form discrepancy','derivative_source_description',None),
('S15','Patricia dictations; Gil speaker correction and current registration request, 5 September 2026','attributed_user_account',None),
('S16','Existing canonical identities, Asunción profile and justice-professional audit','repository_context','https://github.com/sbu001monterecco/por-derecho/tree/145dd4e16773989bef1ddac6ea0428a8cca4a1ff'),
('S17','Supplied Sun Park historical research report and 42-claim packet, 5 September 2026','derivative_report',None)]
EVENTS = [('1987-11-09','deed','S01','3 4'),('1987-11-25','registration','S01','4'),('1989-01-12','licence_recital','S04','7'),('1991-05','tourism_authorisation_recital','S04','7'),('1991-06-27','incorporation_recital','S04','8'),('2007-07-09','urban_entity_minutes','S02','19 20 21'),('2008-02-18','referenced_prior_meeting','S03','14'),('2008-04-29','CEXP_constitution','S03','9 10 11 12 13 14'),('2018-05-10','expert_draft','S07','33 34 35'),('2008-05-26','assignment_signature','S04','15 16 17 18'),('2008-05-27','assignment_effect','S04','15'),('2008-07-16','press_report','S14','38'),('2008-10-16','administrative_proposal','S08','39 44'),('2008-11-25','publication_resolution','S08','39 44'),('2008-12-09','gazette_publication','S08','39 44'),('2010-10','historical_appointment_context_month','S12','27'),('2011-02-02','source_recorded_community_role','S16','48'),('2011-06-22','source_recorded_representation','S16','42 48'),('2012','recalled_conversation','S15','25 45 47 48'),('2014-04-10','source_recorded_notarial_context','S16','48'),('2014-05-08','certification','S01','4'),('2014-08-28','source_recorded_historical_account','S16','48'),('2018-05-23','protocol_1083_33.33_percent','S06','29'),('2018-05-31','protocol_1127_66.67_percent','S06','29'),('2018-09-27','informational_extract','S06','29 30'),('2019-12-17','award_report','S13','27'),('2022-05-06','five_hotel_report','S11','24 42 43'),('2026-09-05','intake_and_speaker_correction','S15 S17','1 45 48')]
LITERALS = [('Asuncion Ayesbrua / Espurua / Asperua','P0004','TRANSCRIPTION_VARIANT'),('Rosa Molina','P0019','CANDIDATE_ONLY'),('Carmelo Marrero','P0018','CANDIDATE_ONLY'),('Agustín Calzada','P0022','CANDIDATE_ONLY'),('Javier / Francisco Molina, recalled official','P0016','CANDIDATE_ONLY'),('Miguel / José Miguel Bravo de Laguna','P0168','FATHER_SON_REFERENCE_UNRESOLVED'),('Roque Prieto','O0012','PERSON_COMPANY_CAPACITY_RECHECK'),('JHSP / JSP','S0018 O0085 O0086','GROUP_AND_COMPANIES_DISTINCT'),('Lopesan','','RETRACTED_ATTRIBUTION_NO_ADVERSE_LINK'),('San Park','S0013','TRANSCRIPTION_VARIANT'),('San Royal','S0014','TRANSCRIPTION_VARIANT'),('K Beach','S0015','CANDIDATE_ONLY'),('San Tropica Sal Island / Sun Tropical Island','S0016 S0017','AMBIGUOUS_COMPOUND'),('Mindysea / Mind Hotels','O0042','CANDIDATE_ONLY'),('Luchi / Lucia','O0002','TRANSCRIPTION_VARIANT'),('Mascator','O0003','TRANSCRIPTION_VARIANT'),('Molina family / dissidents','','NARRATIVE_GROUP_NOT_COLLECTIVE_GUILT'),('Matos Matos','P0009','TRANSCRIPTION_VARIANT'),('1987 authorising notary','','UNNAMED_SOURCE_GAP'),('2008 signature-legitimising notary','','UNNAMED_SOURCE_GAP'),('Registry certifier or staff signatory','','UNNAMED_SOURCE_GAP'),('Molina company representing Spar','','UNRESOLVED_LEGAL_ENTITY')]
GAPS = [
('PRIMARY','Recheck original instruments, exact ranges and source identities; a derivative report is not a native reread.','Cotejar instrumentos originales, rangos e identidades; un informe derivado no es relectura del original.',list(range(1,43))),
('WITNESS','Obtain Asunción’s own account, firsthand basis, corrections and independent corroboration.','Obtener relato propio de Asunción, conocimiento directo, correcciones y corroboración independiente.',[25,26,45,47,48]),
('HOTELS','Recover all five building/opening sequences and booking, staffing, accounts and contribution records.','Recuperar construcción/apertura de los cinco hoteles, reservas, personal, cuentas y aportaciones.',[24,25,26,43,47]),
('TITLE','Recover development, first sales, company ownership, powers and exact short-name identities.','Recuperar promoción, primeras ventas, socios, poderes e identidad de nombres abreviados.',[3,5,6,8,10,11,12,28,46]),
('HANDOVER','Recover February meeting, Victory option/assignments, annexes I–III and transition accounts.','Recuperar junta de febrero, opción Victory/cesiones, anexos I–III y cuentas transitorias.',[9,13,14,15,16,17,18,38]),
('DEEDS','Obtain protocols 1083 of 23 May 2018 and 1127 of 31 May 2018, seller chains and full consideration.','Obtener protocolos 1083 de 23-5-2018 y 1127 de 31-5-2018, vendedores y contraprestación total.',[29,30,31,32]),
('VALUATION','Obtain ACTUA original, instructions, comparables, final expert report and orders; preserve contrary passages.','Obtener ACTUA original, encargo, comparables, pericial final y resoluciones; conservar pasajes contrarios.',[33,34,35]),
('NOTARY','Resolve three pending named notaries and unidentified 1987/2008/Registry signatories from exact instruments.','Resolver tres notarios nominales pendientes y firmantes no identificados de 1987/2008/Registro con instrumentos exactos.',[3,4,9,15,29,48]),
('OUTCOME','Obtain final administrative outcome and actor-specific evidence of acts, omissions, duties, knowledge and benefits.','Obtener resultado administrativo final y prueba individual de actos, omisiones, deberes, conocimiento y beneficios.',[20,22,23,36,37,39,40,41,44])]
RULES = '''# Historical registration: no unsupported additions and no silent omissions

Control PD-SP-HISTORY-20260905; subject to PD-MTCP-20260904-01. This is a bounded intake, not a claim that all archives have been searched.

Enumerate the inspected sources and ranges, named people/entities, dates, amounts, instruments, claims, alleged acts, alleged omissions and material contrary evidence. Every item requires a reused canonical ID, a source-controlled new ID, or an explicit unresolved/private/out-of-scope disposition with reason. New sources expand the denominator explicitly. Never replace a missing identity, source or signatory with a guess or silence.

Keep persons, companies, hotel brands, groups, communities, operators, property owners and representatives distinct. Candidate short-name matches and legal forms remain pending. Registration and carets establish neither lawful authority, knowledge, intent nor guilt. A notary's authorisation does not verify every party's assertion. An alleged omission needs its exact duty, capacity, opportunity, knowledge/notice, missing act, evidence and alternative explanation. Later benefit is not proof of prior cooperation.

Keep speaker, reported source, recipient, date precision, firsthand basis, correction, personal adoption and corroboration separate. These recordings are Patricia's. She attributes part of the early history to Asunción; her later hypotheses are not attributed to Asunción. Do not invent a direct statement, signature, statement of truth, contact or summons. Independently seek Asunción's own version and permit correction and contrary evidence.

Separate deed, effect, registration, certification, publication, notification and final outcome. Preserve month/year precision. Reconcile currency, property/right, timing, offer/completion and total consideration. Sun Park first-of-five remains unverified. Preserve civil-community, seller-risk, urban-accounting, draft-status and favourable judicial qualifications alongside the allegations they qualify.

Require finite-coverage, canonical-count, typed-link, attribution, bilingual and counterevidence checks, plus negative tests. Validators check the declared intake, not the truth of testimony or omissions in unread documents. A checksum identifies bytes, not truth. No private native PDFs, provider locators or personal identifiers are included. Witness contact and legal filings are not authorised by this registration.

WORKER generation, PR, main merge, deployment and exact-SHA live verification are separate states. The active integrator controls publication; do not call a branch or PR live. Run this script with --check --self-test and the existing operational identity and justice-professional validators. Full repository CI remains a separate gate.
'''
WITNESS = {'en':['When, where and with whom was the 2012 conversation? What was recorded rather than later recalled?','What did Asunción personally observe, and what did she receive from named others?','Who controlled allotments, reservations, staffing and hotel accounts, and what records support or contradict the allocation account?','How do operating conditions, lawful alternatives, accounts and owner contributions explain the results?','What do the 2008 option, conveyances, community constitution and handover show, including retained interests?','How does her own account compare with the source-recorded 2011 roles, 2014 notarial context and DP 3205/2014? A recorded role does not establish lawful authority.','What does she confirm, dispute or correct after seeing exact documents and contrary evidence? Obtain adoption of her own final version, not somebody else’s account.'], 'es':['¿Cuándo, dónde y con quién ocurrió la conversación de 2012? ¿Qué se registró frente a lo recordado posteriormente?','¿Qué observó personalmente Asunción y qué recibió de terceros identificados?','¿Quién controlaba cupos, reservas, personal y cuentas hoteleras, y qué documentos apoyan o contradicen el reparto relatado?','¿Cómo explican resultados las condiciones operativas, alternativas lícitas, cuentas y aportaciones?','¿Qué muestran opción, escrituras, constitución comunitaria y relevo de 2008, incluidos intereses retenidos?','¿Cómo se contrasta su relato con funciones registradas de 2011, contexto notarial de 2014 y DP 3205/2014? Cargo registrado no acredita autoridad legítima.','¿Qué confirma, impugna o corrige ante documentos exactos y prueba contraria? Obtener adopción de su versión final propia, no de un relato ajeno.']}
NARRATIVE = {'en':"Patricia describes a Molina-related development, off-plan sales to investors and initially successful joint operation. She attributes part of the pre-2008 history to a conversation she places in 2012 with Asunción Aizpurúa Sánchez. In that reported account, JSP developed neighbouring hotels, moved key personnel and allegedly prioritised those hotels for bookings, with remaining business allocated to Sun Park. Patricia connects ensuing losses and contributions to owner disagreement, withdrawals, alleged obstruction and the 2008 sale. These causal links require contemporaneous hotel records. She further alleges a continuing objective of control after the acquisition, pursued through community structures, disputed debt, Matos Matas, the Insolvency Administrator and CAM/Acosta Matos, with alleged judicial enablement. Those are Patricia's allegations to test actor by actor, not findings or a collective family attribution. Her later price, concealed-compensation and private-equity hypotheses are not automatically attributed to Asunción. The documented qualifications and alternative explanations below remain part of this connected history.", 'es':"Patricia describe promoción vinculada a intereses Molina, ventas sobre plano y explotación conjunta inicialmente exitosa. Atribuye parte de la historia anterior a 2008 a una conversación que sitúa en 2012 con Asunción Aizpurúa Sánchez. Según el relato transmitido, JSP desarrolló hoteles vecinos, trasladó personal clave y presuntamente les dio prioridad en reservas, destinando el negocio restante a Sun Park. Patricia relaciona pérdidas y aportaciones posteriores con desacuerdos, salidas, obstrucción alegada y venta de 2008. Estos nexos requieren documentos hoteleros contemporáneos. Alega además un objetivo continuado de control tras la adquisición, mediante estructuras comunitarias, deuda controvertida, Matos Matas, Administrador Concursal y CAM/Acosta Matos, con facilitación judicial alegada. Son alegaciones de Patricia a contrastar individualmente, no hechos declarados o atribución familiar colectiva. Sus hipótesis posteriores de precios, contraprestaciones ocultas y capital privado no se atribuyen automáticamente a Asunción. Las precisiones y explicaciones alternativas documentales siguientes forman parte de esta historia conectada."}

def ident(s): return 'PD-SP-'+s[0]+'-'+s[1:]
def prop(n): return f'PD-SP-PROP-{1200+n:04d}'
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,obj):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def control(obj,key,value):
    if isinstance(obj,dict): obj[key]=value
    elif isinstance(obj,list): obj.append(dict(key=key,**value) if isinstance(value,dict) else dict(key=key,value=value))
    else: raise ValueError('Unexpected control container')

def context_routes(root):
    pairs=[('asuncion-aizpurua-sanchez','asuncion-aizpurua-sanchez'),('montelanza-monte-lanza-sl','montelanza-monte-lanza-sl'),('montelanza-cuentas-2008','montelanza-accounts-2008'),('registro-identidad-materia','matter-identity-registry'),('registro-identidad-profesionales-justicia','justice-professionals-identity-register'),('cronologia-control-material-sun-park','sun-park-material-control-chronology'),('dp-3205-2014-arrecife','dp-3205-2014-arrecife')]
    paths={l:[] for l in ROUTES}
    for a,b in pairs:
        paths['es'].append('es/'+a+'/index.html');paths['en'].append('en/'+b+'/index.html')
    es='es/comunidad-instrumentalizacion/actas-2011-2022/index.html'
    paths['es'].append(es)
    text=(root/es).read_text()
    candidates=[]
    for tag in re.findall(r'<link\b[^>]*>',text,re.I):
        if re.search(r'hreflang=[\"\']en[\"\']',tag):
            m=re.search(r'href=[\"\']([^\"\']+)',tag)
            if m:
                path=m[1].split('/por-derecho/')[-1].lstrip('/')
                if path.endswith('/'):path+='index.html'
                candidates.append(path)
    existing=[p for p in candidates if (root/p).is_file()]
    if not existing: raise ValueError('No verified English counterpart for ACTAs page')
    paths['en'].append(existing[0])
    for p in sum(paths.values(),[]):
        if not (root/p).is_file():raise ValueError('Missing context page '+p)
    return paths

def generate(root):
    if (root/HISTORY).exists():raise ValueError('Already registered; reconcile a new delta instead of overwriting')
    data=root/'assets/data';index=load(data/'matter-identity-registry-v1.json');parts={};all_records={}
    for p in index['parts']:
        part=load(data/p['path']);parts[p['path']]=part
        for r in part['records']:
            if r['id'] in all_records:raise ValueError('Duplicate baseline ID')
            all_records[r['id']]=r
    if len(all_records)!=351:raise ValueError('Concurrent canonical changes: reconcile allocations before generation')
    context=context_routes(root);new=[]
    for typ,code,start,rows in [('PERSON','P',166,PEOPLE),('ORGANISATION','O',84,ORGS),('STRUCTURE','S',12,HOTELS)]:
        records=[]
        for n,(name,ss) in enumerate(rows,start):
            i=f'PD-SP-{code}-{n:04d}'
            if i in all_records:raise ValueError('Concurrent ID collision '+i)
            r=dict(id=i,type=typ,name=name,aliases=[],status='CARET_PENDING',identity_resolution='CARET_PENDING',identity_sources=[RELEASE+'/'+s for s in ss.split()],identity_boundary='Source-controlled name; exact identity, capacity and company equivalence need independent checks. No automatic ownership, knowledge or liability.',routes={l:'/'+p.removesuffix('index.html')+'#'+i for l,p in ROUTES.items()})
            records.append(r);new.append(r);all_records[i]=r
        path=f'matter-identity-registry-v1.sun-park-history-{typ.lower()}-20260905.json'
        parts[path]=dict(schema='por-derecho.matter-identity-registry.part.v1',registry_id=index['registry_id'],type=typ,records=records)
        index['parts'].append(dict(path=path,type=typ,count=len(records)))
    counts=Counter(r['type'] for r in all_records.values());index['counts']={**dict(counts),'total':len(all_records)};index['control_date']='2026-09-05'
    control(index.setdefault('extensions',{}),'sun_park_history',dict(registry_id=RELEASE,path='sun-park-history-register-v1.json',types=['SOURCE','EVENT','PROPOSITION']))
    if isinstance(index.get('coverage',{}).get('required_names'),list):
        for r in new:
            if r['name'] not in index['coverage']['required_names']:index['coverage']['required_names'].append(r['name'])
    rows=CLAIMS.splitlines()
    if len(rows)!=48 or len(SUBJECTS)!=48:raise ValueError('Finite claim denominator changed')
    claims=[]
    for n,row in enumerate(rows,1):
        state,ss,en,es=row.split('|');claims.append(dict(id=prop(n),legacy_id=f'HIST-C{n:03}',state=state,en=en,es=es,sources=ss.split(),subjects=[ident(s) for s in SUBJECTS[n-1].split()],basis='PARAPHRASE_OF_SUPPLIED_RESEARCH_OR_ATTRIBUTED_ACCOUNT_NOT_FRESH_NATIVE_REVIEW',adopted_by_asuncion=False))
    events=[]
    for n,(date,kind,ss,nn) in enumerate(EVENTS,1):events.append(dict(id='SP-ACTA-2008-04-29' if date=='2008-04-29' else f'PD-SP-EVT-{1200+n:04d}',date=date,precision={4:'YEAR',7:'MONTH',10:'DAY'}[len(date)],kind=kind,sources=ss.split(),claims=[prop(int(v)) for v in nn.split()]))
    gaps=[dict(id='SP-HIST-GAP-'+i,en=en,es=es,state='OPEN',claims=[prop(n) for n in ns],external_contact_authorised=False) for i,en,es,ns in GAPS]
    for c in claims:
        c['events']=[e['id'] for e in events if c['id'] in e['claims']];c['gaps']=[g['id'] for g in gaps if c['id'] in g['claims']]
    used={i for c in claims for i in c['subjects']}|{r['id'] for r in new}|{f'PD-SP-P-{n:04d}' for n in range(14,26)}|{f'PD-SP-P-{n:04d}' for n in range(137,145)}|{ident(s) for s in 'O0004 O0009 O0010 O0013 O0016 O0018 O0021'.split()}
    identities=[]
    for i in sorted(used):
        r=all_records[i];refs=[c['id'] for c in claims if i in c['subjects']]
        identities.append(dict(id=i,name=r['name'],type=r['type'],state=r.get('identity_resolution','REGISTERED'),claims=refs,scope='CLAIM_CONTEXT_NOT_GUILT' if refs else 'WIDER_CONTEXT_ONLY'))
        r.setdefault('related_registers',[]).append(dict(registry_id=RELEASE,path='sun-park-history-register-v1.json',claim_refs=refs,relationship='CONTEXT_NOT_TRANSFER_OF_KNOWLEDGE_OR_LIABILITY'))
    a=all_records['PD-SP-P-0004']
    for name in ['Asunción Ayesbrua','Asunción Espurua']:
        if name not in a['aliases']:a['aliases'].append(name)
    a['reported_account_control']=dict(speaker='PD-SP-P-0002',recalled_year='2012',direct_or_adopted_statement=False,claim=prop(45))
    ops=load(data/'matter-identity-operational-control-v1.json')
    for r in new:ops['exact_identity_queue'].append(dict(id=r['id'],priority='P1',question_en='Verify source-specific identity and capacity of '+r['name']+'; retain candidate-only aliases.',question_es='Verificar identidad y capacidad por fuente de '+r['name']+'; conservar alias candidatos.',source_control=RELEASE))
    control(ops.setdefault('linked_controls',{}),'sun_park_history',dict(path='sun-park-history-register-v1.json',registry_id=RELEASE))
    literals=[dict(id=f'SP-HIST-L{n:02d}',literal=s,candidates=[ident(v) for v in ii.split()],state=state) for n,(s,ii,state) in enumerate(LITERALS,1)]
    sources=[dict(id=i,canonical_id=f'PD-SP-SRC-{1200+n:04d}',title=t,type=typ,url=url,review_basis='SUPPLIED_RESEARCH_METADATA_OR_ATTRIBUTED_ACCOUNT; NOT_A_NEW_NATIVE_REVIEW',publication='SUMMARY_METADATA_ONLY') for n,(i,t,typ,url) in enumerate(SOURCES,1)]
    sources[6]['existing_source_id']='C36-EXW-DRAFT-2018-05-10-VALUATION-REASONABLENESS';sources[6]['sha256']='ccf1d76f6791ce47e0af02162df5317f786a8ad6ec08c50784a83fabf52911a4'
    edges=[]
    for c in claims:
        for i in c['subjects']:edges.append(dict(source=c['id'],target=i,type='CLAIM_CONTEXT_NOT_GUILT',state=c['state'],sources=c['sources']))
        for s in c['sources']:edges.append(dict(source=c['id'],target=s,type='SOURCE_SUPPORT_OR_QUALIFICATION',state=c['state'],sources=[s]))
    edges.append(dict(source='PD-SP-P-0002',target='PD-SP-P-0004',type='REPORTS_CONVERSATION_NOT_ADOPTED_STATEMENT',state='IDENTIFIED_SECOND_HAND_ACCOUNT',sources=['S15']))
    for n in range(13,18):edges.append(dict(source='PD-SP-S-0012',target=f'PD-SP-S-{n:04d}',type='REPORTED_GROUP_MEMBERSHIP_NOT_TITLE',state='SECONDARY_HISTORY',sources=['S11']))
    notaries=load(data/'justice-professionals-caret-audit-v1.json')['roles']['NOTARY']
    totals=dict(identities=len(identities),new_identities=len(new),claims=len(claims),events=len(events),sources=len(sources),literals=len(literals),relationships=len(edges),gaps=len(gaps),notaries=len(notaries),notaries_pending=sum(n['state']=='CARET_PENDING' for n in notaries))
    obj=dict(schema='por-derecho.sun-park-history.v1',registry_id=RELEASE,date='2026-09-05',lifecycle='WORKER_SOURCE_NOT_MAIN_OR_LIVE',scope=dict(description='42 supplied claim topics plus six explicit clarifications; associated named targets, not a full-archive census',counts=totals,required_identity_ids=sorted(used),required_literal_ids=[x['id'] for x in literals],native_sources_reread=False,private_originals_included=False),attribution=dict(speaker='PD-SP-P-0002',corrected_by='PD-SP-P-0001',reported_source='PD-SP-P-0004',conversation='2012',precision='RECALLED_YEAR',direct_or_adopted_asuncion_statement=False,witness_contacted=False,later_hypotheses_attributed_to_asuncion=False),claims=claims,sources=sources,events=events,identities=identities,literals=literals,relationships=edges,gaps=gaps,notaries=notaries,routes=ROUTES,context_routes=context)
    for p,v in parts.items():save(data/p,v)
    save(data/'matter-identity-registry-v1.json',index);save(data/'matter-identity-operational-control-v1.json',ops);save(root/HISTORY,obj)
    for lang,path in ROUTES.items():
        p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(render(lang,obj),encoding='utf-8')
        for related in context[lang]:
            p=root/related;t=p.read_text();mark='sun-park-history-20260905'
            if mark in t:raise ValueError('Existing backlink requires reconciliation')
            block='<section id="'+mark+'"><h2>'+('Connected Sun Park history' if lang=='en' else 'Historia conectada de Sun Park')+'</h2><p>'+route_link(path,'Sun Park · JSP · Molina · Asunción')+' — '+('Sources, dates, identities, independent-statement questions and contrary evidence; links do not imply guilt.' if lang=='en' else 'Fuentes, fechas, identidades, preguntas de declaración independiente y prueba contraria; enlazar no implica culpabilidad.')+'</p></section>'
            at=t.rfind('</main>')
            if at<0:raise ValueError('No main closing tag '+related)
            p.write_text(t[:at]+block+t[at:])
    # Reconcile existing static/structured counts, without changing historical dates elsewhere.
    for lang in ROUTES:
        p=root/context[lang][3];t=p.read_text();seq=[index['counts'][k] for k in ['total','PERSON','ORGANISATION','STRUCTURE','INSTITUTION','PROCEEDING']]
        t=re.sub(r'data-static-registry-counts="[^"]+"','data-static-registry-counts="'+'-'.join(map(str,seq))+'"',t)
        for k,n in zip(['TOTAL','PERSON','ORGANISATION','STRUCTURE','INSTITUTION','PROCEEDING'],seq):t=re.sub(r'(data-registry-stat="'+k+r'">)\d+',lambda m:m[1]+str(n),t)
        def ld(m):
            v=json.loads(m[1])
            if v.get('@type')=='Dataset' and isinstance(v.get('variableMeasured'),list):
                v['dateModified']='2026-09-05'
                for item,n in zip(v['variableMeasured'],seq):item['value']=n
            return '<script type="application/ld+json">'+json.dumps(v,ensure_ascii=False)+'</script>'
        t=re.sub(r'<script type="application/ld\+json">(.*?)</script>',ld,t,flags=re.S);p.write_text(t)
    rule='archive/SUN_PARK_HISTORY_NO_OMISSION_OR_UNSUPPORTED_ADDITION_05SEP2026.md';(root/rule).write_text(RULES)
    for filename in ['AGENTS.md','CHATGPT_START_HERE.md','archive/knowledge-project/SUN_PARK_CANONICAL_REGISTER_READ_FIRST.md','archive/MISSING_EVIDENCE_REGISTER.md']:
        p=root/filename;p.write_text(p.read_text()+'\n\n## Sun Park historical intake — 5 September 2026\n\n'+RELEASE+': read `'+rule+'` and `'+HISTORY+'`. Every named target, date, act, omission, claim and contrary item needs a canonical disposition. Preserve Patricia → reported Asunción provenance; unresolved names/notaries stay explicit. Run `python3 scripts/register_sun_park_history_20260905.py --check --self-test`. WORKER source is not deployment.\n')
    p=root/'archive/knowledge-project/SUN_PARK_CANONICAL_REGISTER.json';legacy=load(p);control(legacy.setdefault('source_control_extensions',{}),'sun_park_history_20260905',dict(registry_id=RELEASE,path=HISTORY,routes=ROUTES,policy='Crosswalk to canonical IDs, not a parallel actor register'));save(p,legacy)
    (root/'archive/SUN_PARK_HISTORY_WORKER_READINESS_05SEP2026.md').write_text('# Sun Park historical WORKER readiness\n\n'+json.dumps(totals,indent=2)+'\n\nThe 42 supplied research topics are paraphrased with qualifications and six explicit additions. Native documents were not freshly reviewed in this implementation. All new identities stay CARET_PENDING; Asunción and eight existing notary IDs are reused. Sixteen existing pages and the legacy register receive reciprocal links. No private source documents or provider locators are included.\n\nCorrections preserved: Patricia is the speaker; Asunción has not personally adopted the account; JSP replaces the withdrawn Lopesan attribution; expert draft date is 2018-05-10, not 2008; administrative proposal/resolution/publication differ; first-of-five remains unverified; representation is not ownership; 89.5% has an unidentified company; EUR6,000 is operating assignment; urban accounts are not hotel accounts; seller-risk and favourable judicial passages are retained.\n\nRun historical self-tests and existing operational identity/justice-professional validators. Full repository CI, active-integrator reconciliation, main merge, deployment and live verification remain separate gates. A WORKER commit or PR must not be called live. No witness contact, legal filing, statement adoption or summons has occurred.\n')
    return check(root,obj)

def route_link(path,label):return '<a href="/por-derecho/'+path.removesuffix('index.html')+'">'+html.escape(label)+'</a>'
def render(lang,d):
    h=html.escape;en=lang=='en';title='Sun Park, JSP and Molina: connected history' if en else 'Sun Park, JSP y Molina: historia conectada'
    def refs(ii):return ' · '.join('<a href="#'+i+'">'+h(i)+'</a>' for i in ii)
    body='<section id="account"><h2>'+('Identified second-hand account' if en else 'Relato indirecto con fuente identificada')+'</h2><p><strong>'+('Patricia reports a conversation with Asunción Aizpurúa Sánchez, pending Asunción’s own account and independent verification. This is not Gil’s direct testimony or an adopted statement by Asunción.' if en else 'Patricia refiere una conversación con Asunción Aizpurúa Sánchez, pendiente del relato propio de Asunción y verificación independiente. No es testimonio directo de Gil ni declaración adoptada por Asunción.')+'</strong></p><p>'+h(NARRATIVE[lang])+'</p><p>'+refs(['S01','S03','S04','S07','S09','S10','S11','S15',prop(45)])+'</p></section>'
    body+='<section id="asuncion-independent-account"><h2>'+('Asunción: request for an independently checked statement' if en else 'Asunción: solicitud de relato contrastado independientemente')+'</h2><p>'+('No contact or summons has been made through this release. The questions seek her own knowledge, documents, corrections and personally adopted final account.' if en else 'Esta entrega no ha realizado contacto o citación. Las preguntas buscan su conocimiento propio, documentos, correcciones y versión final adoptada personalmente.')+'</p><ol>'+''.join('<li>'+h(q)+'</li>' for q in WITNESS[lang])+'</ol><p>'+route_link(d['context_routes'][lang][0],'Asunción · PD-SP-P-0004')+' · '+route_link(d['context_routes'][lang][6],'DP 3205/2014')+'</p></section>'
    body+='<section id="chronology"><h2>'+('Dates and distinct acts' if en else 'Fechas y actos distintos')+'</h2>'
    for e in sorted(d['events'],key=lambda x:x['date']):body+='<article id="'+e['id']+'"><h3>'+e['date']+' · '+h(e['kind'])+'</h3><p>'+e['precision']+' · '+refs(e['sources']+e['claims'])+'</p></article>'
    body+='</section><section id="identities"><h2>'+('People, entities and notaries' if en else 'Personas, entidades y notarios')+'</h2><p>'+('Registration does not establish knowledge, agreement, lawful authority or guilt. Candidate identities remain pending.' if en else 'Registrar no acredita conocimiento, acuerdo, autoridad legítima o culpabilidad. Las identidades candidatas siguen pendientes.')+'</p><div class="table-wrap"><table><thead><tr><th>ID / nombre</th><th>Estado / status</th><th>Referencias</th></tr></thead><tbody>'
    for i in d['identities']:
        caret='<sup>^</sup>' if i['state']=='CARET_CONFIRMED' else ''
        target='/por-derecho/'+d['context_routes'][lang][3].removesuffix('index.html')+'#'+i['id']
        body+='<tr id="'+i['id']+'"><td><a data-caepr-id="'+i['id']+'" data-caret-state="'+h(i['state'])+'" href="'+target+'">'+h(i['name'])+caret+'</a><br>'+i['id']+'</td><td>'+h(i['state'])+'</td><td>'+refs(i['claims'])+('' if i['claims'] else h(i['scope']))+'</td></tr>'
    body+='</tbody></table></div><h3>'+('Notary coverage' if en else 'Cobertura notarial')+'</h3><p>'+('Eight existing named notaries are linked: five identity-confirmed and three pending. The unidentified 1987 deed authoriser, 2008 signature legitimiser and Registry signatory remain explicit gaps. Notarial form does not verify all party assertions or consideration.' if en else 'Se enlazan ocho notarios nominales: cinco con identidad confirmada y tres pendientes. Autorizante de 1987, legitimación de 2008 y firmante registral no identificados siguen como lagunas explícitas. La forma notarial no verifica todas las manifestaciones o contraprestaciones.')+'</p><p>'+route_link(d['context_routes'][lang][4],'Notarios / justice-professionals register')+'</p></section>'
    body+='<section id="literals"><h2>'+('Source literals and candidate identities' if en else 'Literales de fuente e identidades candidatas')+'</h2>'
    for x in d['literals']:body+='<p id="'+x['id']+'"><strong>'+h(x['literal'])+'</strong> — '+h(x['state'])+' · '+refs(x['candidates'])+'</p>'
    body+='</section><section id="claims"><h2>'+('Claims and qualifications' if en else 'Afirmaciones y precisiones')+'</h2><p>'+('The 42 supplied research topics are paraphrased with their limits; six additions clarify this intake. This is not a new native-source review. Identity and source links provide context, not proof of every allegation.' if en else 'Se parafrasean los 42 temas de investigación recibidos con sus límites; seis adiciones precisan esta recepción. No es nueva revisión de originales. Los vínculos de identidad y fuente aportan contexto, no prueba de toda alegación.')+'</p>'
    for c in d['claims']:body+='<article id="'+c['id']+'"><h3>'+c['legacy_id']+' · '+h(c['state'])+'</h3><p>'+h(c[lang])+'</p><p>'+refs(c['sources']+c['subjects']+c['events']+c['gaps'])+'</p></article>'
    body+='</section><section id="sources"><h2>'+('Sources and provenance' if en else 'Fuentes y procedencia')+'</h2>'
    for s in d['sources']:
        body+='<article id="'+s['id']+'"><h3>'+s['id']+' · '+h(s['title'])+'</h3><p>'+h(s['review_basis'])+'</p>'
        if s['url']:body+='<p><a rel="noopener noreferrer" href="'+h(s['url'],quote=True)+'">'+('Published source' if en else 'Fuente publicada')+'</a></p>'
        if s.get('sha256'):body+='<p><small>SHA-256: '+s['sha256']+'</small></p><p>'+h(s['existing_source_id'])+'</p>'
        body+='<p>'+refs([c['id'] for c in d['claims'] if s['id'] in c['sources']])+'</p></article>'
    body+='</section><section id="gaps"><h2>'+('Open evidence and production questions' if en else 'Lagunas y solicitudes probatorias abiertas')+'</h2>'
    for g in d['gaps']:body+='<article id="'+g['id']+'"><h3>'+g['id']+' · OPEN</h3><p>'+h(g[lang])+'</p><p>'+refs(g['claims'])+'</p></article>'
    body+='</section><section id="related"><h2>'+('Connected records and safeguards' if en else 'Registros conectados y garantías')+'</h2><p>'+' · '.join(route_link(p,p.split('/')[-2]) for p in d['context_routes'][lang])+'</p><p>'+route_link(HISTORY,'Canonical register / registro canónico')+' · '+route_link('archive/SUN_PARK_HISTORY_NO_OMISSION_OR_UNSUPPORTED_ADDITION_05SEP2026.md','No omission / sin omisiones')+'</p></section>'
    other='es' if en else 'en';base='https://sbu001monterecco.github.io/por-derecho/'
    style='body{margin:0;font:18px/1.65 system-ui,sans-serif;background:#f6f7f9;color:#172437}header,main,footer{max-width:1100px;margin:auto;padding:24px}section{margin:24px 0;background:white;padding:24px;border:1px solid #d4dde5;border-radius:8px}h1{font-size:clamp(2rem,5vw,3rem);line-height:1.2}h2{font-size:1.45rem}h3{font-size:1rem}a{color:#18517a}p,li{overflow-wrap:anywhere}.table-wrap{overflow:auto}table{width:100%;border-collapse:collapse;font-size:.85rem}td,th{padding:10px;border-bottom:1px solid #d4dde5;text-align:left;vertical-align:top}article{padding:12px 0;border-top:1px solid #e2e7eb}small{font-size:.75rem}:target{outline:2px solid #ac8b48;scroll-margin:16px}@media(max-width:600px){header,main,footer{padding:12px}section{padding:16px}}'
    return '<!doctype html>\n<html lang="'+lang+'"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+h(title)+' | Por Derecho</title><link rel="canonical" href="'+base+ROUTES[lang].removesuffix('index.html')+'"><link rel="alternate" hreflang="'+other+'" href="'+base+ROUTES[other].removesuffix('index.html')+'"><style>'+style+'</style></head><body><header><nav>'+route_link(lang+'/index.html','Por Derecho')+' · <a href="#claims">Evidence / evidencia</a> · <a href="#identities">People / personas</a> · '+route_link(ROUTES[other],other.upper())+'</nav><h1>'+h(title)+'</h1><p>5 September 2026 · '+RELEASE+'</p></header><main>'+body+'</main><footer><p>'+('Corrections and contrary evidence remain part of the history. No third-party contact was made by this release.' if en else 'Correcciones y prueba contraria forman parte de la historia. Esta entrega no contacta con terceros.')+'</p></footer></body></html>\n'

class Anchors(HTMLParser):
    def __init__(self):super().__init__();self.ids=set();self.hrefs=[]
    def handle_starttag(self,t,a):
        d=dict(a)
        if d.get('id'):self.ids.add(d['id'])
        if t=='a' and d.get('href'):self.hrefs.append(d['href'])

def check(root,d=None,pages=True):
    def need(ok,msg):
        if not ok:raise AssertionError(msg)
    if d is None:d=load(root/HISTORY)
    data=root/'assets/data';idx=load(data/'matter-identity-registry-v1.json');records=[]
    for p in idx['parts']:
        shard=load(data/p['path']);need(len(shard['records'])==p['count'],'shard count');records+=shard['records']
    ids={r['id'] for r in records};counts=Counter(r['type'] for r in records);need(len(ids)==len(records),'duplicate IDs');need(idx['counts']['total']==len(records),'total');need(all(idx['counts'][k]==v for k,v in counts.items()),'type counts')
    need(len(d['claims'])==48 and {c['legacy_id'] for c in d['claims']}=={f'HIST-C{n:03}' for n in range(1,49)},'claim omission');need(len(d['sources'])==17,'source omission');need(len(d['events'])==28,'date omission');need(len(d['literals'])==22,'literal omission');need(len(d['gaps'])==9,'gap omission')
    need({i['id'] for i in d['identities']}==set(d['scope']['required_identity_ids']),'identity omission');need({x['id'] for x in d['literals']}==set(d['scope']['required_literal_ids']),'literal disposition loss')
    queue={r['id'] for r in load(data/'matter-identity-operational-control-v1.json')['exact_identity_queue']};new=[r for r in records if r.get('identity_boundary','').startswith('Source-controlled name;')];need(len(new)==29,'new identity count');need(all(r['identity_resolution']=='CARET_PENDING' and r['status']=='CARET_PENDING' and r['id'] in queue for r in new),'false identity confirmation or unqueued identity')
    a=d['attribution'];need(a['speaker']=='PD-SP-P-0002' and a['reported_source']=='PD-SP-P-0004','speaker/source error');need(not a['direct_or_adopted_asuncion_statement'] and not a['witness_contacted'] and not a['later_hypotheses_attributed_to_asuncion'],'false adoption/contact/attribution');need(not d['scope']['native_sources_reread'],'false native review')
    nodes=ids|{x['id'] for k in ['claims','sources','events','gaps','literals'] for x in d[k]}
    for n,c in enumerate(d['claims']):
        state,ss,en,es=CLAIMS.splitlines()[n].split('|');need(c['state']==state and c['en']==en and c['es']==es,'unsupported promotion or qualification loss');need(not c['adopted_by_asuncion'],'false claim adoption');need(all(v in nodes for k in ['sources','subjects','events','gaps'] for v in c[k]),'dangling claim')
    for e in d['events']:
        need(bool(re.fullmatch(r'\d{4}(?:-\d{2}){0,2}',e['date'])),'invalid date');need(e['precision']=={4:'YEAR',7:'MONTH',10:'DAY'}[len(e['date'])],'date precision');need(all(v in nodes for k in ['sources','claims'] for v in e[k]),'dangling event')
    ev={e['kind']:e for e in d['events']};need(ev['expert_draft']['date']=='2018-05-10','expert year error');need(ev['CEXP_constitution']['id']=='SP-ACTA-2008-04-29','duplicate legacy acta');need(ev['recalled_conversation']['date']=='2012','invented encounter day')
    for k,v in [('administrative_proposal','2008-10-16'),('publication_resolution','2008-11-25'),('gazette_publication','2008-12-09')]:need(ev[k]['date']==v,'conflated BOC date')
    for e in d['relationships']:need(e['source'] in nodes and e['target'] in nodes and e['type'] and e['state'] and all(s in nodes for s in e['sources']),'bad typed edge')
    for g in d['gaps']:need(g['state']=='OPEN' and not g['external_contact_authorised'],'false gap closure/contact')
    text=json.dumps(d,ensure_ascii=False);need(not re.search(r'drive\.google\.com|gmail\.com|mail\.google\.com|file_0000|sk-proj-|BEGIN .*PRIVATE KEY',text),'private locator or secret')
    ns=load(data/'justice-professionals-caret-audit-v1.json')['roles']['NOTARY'];need(d['notaries']==ns and len(ns)==8 and sum(n['state']=='CARET_PENDING' for n in ns)==3,'notary loss/promotion');need(all(n['id'] in d['scope']['required_identity_ids'] for n in ns),'notary omitted')
    if pages:
        required={x['id'] for k in ['claims','sources','events','gaps','literals','identities'] for x in d[k]}
        for lang,path in ROUTES.items():
            txt=(root/path).read_text();p=Anchors();p.feed(txt);need(required<=p.ids,'missing visible record');need('asuncion-independent-account' in p.ids,'missing witness questions')
            for href in p.hrefs:
                if href.startswith('#'):need(href[1:] in p.ids,'bad local anchor')
                elif href.startswith('/por-derecho/'):
                    target=href[len('/por-derecho/'):].split('#')[0];dest=root/target
                    if not target or target.endswith('/'):dest=dest/'index.html'
                    need(dest.exists(),'missing route '+target)
            for path in d['context_routes'][lang]:need('sun-park-history-20260905' in (root/path).read_text(),'missing reciprocal link')
    return dict(result='PASS',scope='Declared intake integrity, not proof of allegations or full-archive completeness',counts=d['scope']['counts'],canonical_total=len(records))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--check',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args();result=check(a.root) if a.check else generate(a.root)
    if a.self_test:
        d=load(a.root/HISTORY)
        tests=[('claim omission',lambda x:x['claims'].pop()),('identity omission',lambda x:x['identities'].pop()),('source omission',lambda x:x['sources'].pop()),('date omission',lambda x:x['events'].pop()),('literal omission',lambda x:x['literals'].pop()),('false direct adoption',lambda x:x['attribution'].__setitem__('direct_or_adopted_asuncion_statement',True)),('false contact',lambda x:x['attribution'].__setitem__('witness_contacted',True)),('wrong speaker',lambda x:x['attribution'].__setitem__('speaker','PD-SP-P-0001')),('false first-hotel finding',lambda x:x['claims'][42].__setitem__('state','PROVEN')),('contrary qualification removed',lambda x:x['claims'][34].__setitem__('en','')),('dangling link',lambda x:x['relationships'][0].__setitem__('target','NONEXISTENT')),('notary loss',lambda x:x['notaries'].pop())]
        for name,mutation in tests:
            broken=copy.deepcopy(d);mutation(broken)
            try:check(a.root,broken,False)
            except AssertionError:pass
            else:raise AssertionError('Negative test not detected: '+name)
        result['negative_tests_rejected']=len(tests)
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
