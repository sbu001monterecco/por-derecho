# SRLN-2026 — Global Banking website correction / release handoff

**Control date:** 2026-10-31  
**Affected live pages:** https://sun-rock-capital.sbu001.chatgpt.site/global-banking/ and https://sun-rock-capital.sbu001.chatgpt.site/es/global-banking/  
**Linked PDF:** `/assets/AWESWELL_Sun_Rock_Global_Banking_Public_Overview_29Oct2026.pdf`  
**Change state:** DRAFT / NOT DEPLOYED TO CHATGPT WORK SITE. **Do not mark GREEN until live verification.**

## Verified observations (31 October 2026)

- Independent content fetch succeeded for English and Spanish Global Banking pages, home, professional readiness, legal and linked PDF; this is **not a confirmed outage**.
- The five headline opportunities on Global Banking currently read: **Global Coordinator & Bookrunner; Mandated Lead Arranger; Co-Structuring Agent; Facility Agent; Security Agent**.
- This differs from the five central banking/agency discussions for SRLN-2026: **Global Coordinator; Issuing/Paying Agent; Note Trustee or Note Agent; Security Agent; UK Issuer Transaction Account Bank**. Some are only in the supplementary prose.
- Professional Readiness separately names the issuance/payments, note trustee/security, and issuer transaction account functions among **13 professional-appointment functions**. The page should not make readers guess which is being solicited.
- Both EN and ES pages link the same English-language public banking PDF dated 29 October 2026. Regenerate or annotate its language and version when updating content.
- `robots=noindex,nofollow` observed; **do not change** without an explicit distribution/search decision. This is not proof of a technical fault.
- The standalone `chatgpt.site` review publication is **not deployed by GitHub/GitLab commits**. Only an authenticated ChatGPT Work owner-edit plus live readback repairs that URL.

## Requested release — keep existing page design and disclosures

Replace **only** the section headed “Five potential banking mandates / One, several or up to five roles” (retain `id="bank-opportunities"` and all nav destinations) with the following operating-role hierarchy. Keep project, privacy and no-public-offer boundaries intact.

### English — proposed replacement text

**Five core banking and securities-agency opportunities**

**One coordinated banking relationship. Five separately evaluated operating roles.**

A banking group may consider one, several or all five roles through suitably authorised entities and specialist teams. Each role is conditional on diligence, regulatory capability, conflicts, commercial terms and separate written appointment. No provider is represented as selected, and no Note or bank commitment has been made.

**01 · Global Coordinator / potential Bookrunner.** Coordinate the proposed UK institutional capital-markets programme, relevant Series, market-facing banking teams and any agreed eligible-investor placement. Underwriting, bookbuilding and distribution are not assumed.

**02 · Issuing and Paying Agent.** Subject to definitive documents and eligibility, coordinate issuance/settlement and contractual coupon, redemption and payment processing; reconcile payment records with the controlling register and authorised bank accounts. The website never handles investor money.

**03 · Note Trustee or Note Agent (structure to be settled).** Where chosen and legally appropriate, undertake the relevant holder representation, notice, covenant and/or administrative functions defined in the Notes documentation. Trustee, fiscal agent and registrar functions are not interchangeable merely by title.

**04 · Security Agent / Security Trustee (if applicable).** Act only in relation to expressly agreed, legally available and perfected security, with precisely delimited priority, release, custody and enforcement arrangements.

**05 · UK Issuer Transaction Account Bank.** Provide the UK issuer’s legally owned and controlled transaction accounts, authorised payment infrastructure and, if agreed, reserves/escrow/lockbox and permitted drawdown controls. Sponsor, personal, project and issuer funds must remain legally segregated.

**Additional optional specialist mandates.** An eligible bank or another regulated provider may separately discuss lead arranging for acquisition/development finance, co-structuring, a facility agent where a loan facility actually exists, registrar/transfer and calculation functions, custody/settlement, FX, treasury and commercial banking. **LSEG ISM listing/admission coordination** may be integrated into an authorised existing mandate or scoped as an **additional sixth function**, subject to ISM requirements and provider capability. No role or appointment is implied by this description.

**Boundary:** Existing corporate group banking, Spanish project finance and separate sponsor-family private banking remain distinct onboarding, financing and cash pools. Bank coverage is not a guarantee, underwriting commitment or issuance approval.

### Español — texto de sustitución propuesto

**Cinco oportunidades principales de banca y agencia de valores**

**Una relación bancaria coordinada. Cinco funciones operativas evaluadas por separado.**

Un grupo bancario puede estudiar una, varias o las cinco funciones mediante sociedades y equipos debidamente habilitados. Cada función queda sujeta a diligencia, autorizaciones aplicables, conflictos, condiciones comerciales y nombramiento escrito independiente. No se presenta a ninguna entidad como designada ni se presupone emisión o financiación comprometida.

**01 · Coordinador Global / posible Director de Colocación (Bookrunner).** Coordinar el programa propuesto de mercados de capitales institucionales británicos, las series pertinentes, los equipos bancarios y cualquier colocación acordada entre inversores admisibles. No se presupone aseguramiento, colocación ni distribución.

**02 · Agente de Emisión y Pagos.** Conforme a los documentos definitivos y las autorizaciones requeridas, coordinar emisión, liquidación y pagos contractuales de intereses y principal, reconciliándolos con el registro jurídico de titulares y las cuentas autorizadas. La web nunca recibe dinero de inversores.

**03 · Representante de los Bonistas o Agente de Notas (estructura por determinar).** Cuando corresponda legalmente y se acuerde, asumir funciones definidas de representación, notificaciones, seguimiento de obligaciones y/o administración. Las figuras de trustee, agente fiscal y registrador no son automáticamente equivalentes.

**04 · Agente o Trustee de Garantías (si procede).** Actuar únicamente respecto de garantías expresamente pactadas, jurídicamente disponibles y debidamente perfeccionadas, con reglas definidas de rango, liberación y ejecución.

**05 · Banco de la Cuenta Transaccional del Emisor en el Reino Unido.** Proporcionar cuentas del emisor sujetas a titularidad y controles efectivos, infraestructura de pagos y, si se acuerda, reservas, depósito controlado (escrow), cuenta bloqueada y condiciones de disposición. Mantener separados los fondos del emisor, patrocinador, proyectos y clientes privados.

**Otros mandatos especializados opcionales.** Pueden evaluarse de forma independiente la organización de financiación de adquisiciones o promociones, coestructuración, agente de financiación cuando exista una facilidad contratada, registrador, transferencias, cálculos, custodia, liquidación, divisas, tesorería y banca comercial. La **coordinación de admisión/listing ante LSEG ISM** podrá integrarse en un mandato habilitado o contemplarse como **sexta función independiente**, siempre sujeto a los requisitos de ISM y la capacidad del proveedor.

**Límite:** La banca del grupo, la financiación de sociedades españolas y la banca privada familiar exigen procesos, contratos y cuentas separados. Una relación de cobertura no supone garantía, aseguramiento ni aprobación de la emisión.

## Required linked-document and UX changes

1. Revise the linked English **29 October banking overview PDF** to match the new five core roles and separate optional specialist roles; version and date it upon actual publication. Preserve the historic PDF/version and checksum. On the Spanish page, either provide an accurate Spanish PDF or mark the linked file **“PDF en inglés”**.
2. Keep the five **business workstreams** (UK capital, Spanish assets, hotel economics, UK platform, US footprint) separate from the five **bank mandates**. Do not confuse either with the 13 **professional readiness appointment functions**.
3. Check all EN/ES navigation target IDs, language toggle, corporate contact mailto, PDF response and download, legal footer, image assets, keyboard focus and mobile rendering. Do not report them broken unless a real click test fails.
4. Keep PRE-ADMISSION / PRE-ISSUANCE, no-current-bank-mandate, no-public-subscription, no-committed-capital, no-assumed-security and litigation-funding-separation notices unchanged. No named bank endorsement or private information.
5. Review page metadata and OG cards; preserve `noindex,nofollow` unless the owner separately authorises discoverability.
6. After actual Work publication: obtain live EN/ES readback, click/visual QA and PDF text parity; record dated release ID, old/new version, snapshots/hashes and status. Do not state GREEN before this.

## Release-gate statuses

| Gate | State on 31 Oct 2026 |
| --- | --- |
| Public pages and linked PDF accessible via independent fetch | GREEN (availability only) |
| Banking role alignment across EN, ES, PDF and professional-readiness | AMBER — correction prepared |
| Live site update via authenticated ChatGPT Work | RED — not yet deployed |
| Mobile/interactive browser QA | AMBER — not verified |
| Source preservation and change-review record | GREEN only after this draft is committed |
| Overall live change | **NOT GREEN** |

**Change-control rule:** This document is an actionable owner-edit handoff, NOT the site source code and NOT proof of deployment. Preserve original binaries and versions; do not send external email or publish private documents as part of this correction.
