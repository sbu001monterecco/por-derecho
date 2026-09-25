# Person-perimeter separation, authorization and publication protocol

**Protocol ID:** `PD-PERIMETER-GOV-001`  
**Control date:** 25 August 2026  
**Status:** governance approved; implementation of person-specific public classifications remains authorization-controlled  
**Repository visibility:** public; this protocol contains no private identity map or native private evidence  
**Pages status:** excluded from the rendered GitHub Pages surface by its `.github/` path

## 1. Purpose

The immutable identity registry answers **which controlled identity a source refers to**. It must not be used as a single undifferentiated public list of people.

Perimeter classification answers a different and narrower question: **in what dated legal, economic, professional, institutional or evidential capacity is the identity relevant?**

The two layers must remain separate. An immutable ID does not itself authorize public naming, perimeter membership or an attribution of responsibility.

## 2. Mandatory public architecture

Any public identity view that groups natural persons must present the following visibly separate sections, filters or pages, in this order:

1. **Our perimeter / Perímetro propio**;
2. **Adverse private parties and documented opposing interests / Partes privadas adversas e intereses opuestos documentados**;
3. **Professionals and representatives / Profesionales y representantes**;
4. **Institutions and officeholders / Instituciones y cargos**;
5. **Witnesses, experts and document custodians / Testigos, peritos y custodios documentales**.

The following remain outside those rendered legal-matter lists by default:

6. **Transaction-development contacts / Contactos de desarrollo de operaciones** — private;
7. **Unresolved identities and private candidates / Identidades no resueltas y candidatos privados** — private.

A public interface must not imply that categories 3–5 form part of either private-party perimeter merely because their work, decision, evidence or representation affects the dispute.

## 3. Controlled classification values

### Our side

- `OUR_CORE` — claimant, beneficial/economic rights-holder, director, declarant or person directly asserting or defending the project-side rights.
- `OUR_REPRESENTED_INTEREST` — entity or interest whose rights, assets, income, control or losses are being protected or recovered, with the exact capacity and period recorded.

### Adverse private side

- `ADVERSE_FORMAL_PARTY` — private person or entity formally opposing a project-side interest in a proceeding, claim, creditor, purchaser, ownership or governance capacity.
- `ADVERSE_PRIVATE_FUNCTIONAL_ACTOR` — private person whose source-supported, dated conduct is materially alleged or documented as adverse in governance, control, possession, asset, income, voting, security, transaction or implementation activity.

### Separate non-perimeter roles

- `OUR_CURRENT_PROFESSIONAL`
- `OUR_FORMER_PROFESSIONAL`
- `ADVERSE_PARTY_PROFESSIONAL`
- `INSTITUTIONAL_OFFICEHOLDER`
- `WITNESS_EXPERT_CUSTODIAN`
- `TRANSACTION_DEVELOPMENT_PRIVATE`
- `UNRESOLVED_PRIVATE_CANDIDATE`

A person may have more than one dated capacity, but each capacity must be recorded separately. The public interface must not collapse different periods or capacities into a permanent moral label.

## 4. Admission tests

### 4.1 Our perimeter

A person or entity may be classified in our perimeter only where a source-supported capacity establishes that it:

- owns, controls or asserts a relevant project-side right or asset;
- is a claimant, appellant, complainant, declarant or represented project-side interest;
- bears a claimant-specific loss or recovery claim; or
- has an expressly documented project-side governance or representation capacity for the stated period.

Being friendly, helpful, professionally engaged, a witness, an adviser or interested in a transaction is not enough.

### 4.2 Adverse private parties and documented opposing interests

A person or entity may be classified in the adverse private perimeter only where a source-supported, dated basis establishes at least one of:

- formal opposing-party status;
- adverse creditor, purchaser, claimant, ownership or governance status;
- a documented opposing interest in a material proceeding or decision;
- an actor-specific allegation or documented act concerning material private control, possession, voting, access, asset, income or implementation activity.

The classification must identify:

- the exact identity and entity/capacity;
- the date or period;
- the adverse basis;
- the source class and public-safe reference;
- the evidential status;
- contrary or limiting evidence; and
- what is expressly not inferred.

Adverse classification is not a finding of illegality, guilt, intent, coordination, control or liability.

## 5. Mandatory separations

### Professionals

A lawyer, procurador, accountant, auditor, consultant, banker or other professional is not automatically part of either private-party perimeter. Classify the person by professional role unless independent, actor-specific evidence justifies another dated capacity.

Representation of an adverse party does not make the professional an adverse private actor. Representation of our side does not make the professional part of our ownership or claimant perimeter.

### Institutions and officeholders

Judges, judicial officers, fiscales, police, regulators, public authorities and the court-appointed insolvency-administrator track remain separate from private adverse parties. Their acts, omissions, decisions, custody or reliance may be challenged actor by actor without merging them into a private perimeter.

### Witnesses, experts and custodians

A person whose principal relevance is testimony, expert evidence, technical knowledge, contemporaneous receipt or document custody belongs in the witness/expert/custodian section unless a separate dated capacity is independently established.

### Transaction development

A prospective investor, buyer, lender, banker, operator, introducer or ordinary commercial counterparty belongs in `TRANSACTION_DEVELOPMENT_PRIVATE` by default. Such a person is neither our legal perimeter nor an adverse party merely because they discussed the asset, financing, a sale, due diligence or a meeting.

A later legal/evidential connection requires the full cross-linking gate in `.github/governance/TRANSACTION_DEVELOPMENT_SEPARATION_AND_PUBLICATION_PROTOCOL.md` and a separate public-display authorization.

## 6. Natural-person publication authorization

Before a natural person is newly added, kept fully named, partially named, pseudonymised, aggregated, moved between public categories or withdrawn, the decision record must contain:

1. immutable identity ID or private candidate ID;
2. exact private identity and aliases in the access-controlled identity system;
3. exact organization, capacity and relevant date or period;
4. legal/evidential proposition and source basis;
5. what the evidence establishes and does not establish;
6. public naming necessity and proportionality;
7. privacy and residual re-identification assessment;
8. proposed public category;
9. proposed public label;
10. one approved display mode;
11. Gil Marer’s person-specific authorization reference and date; and
12. review, correction and withdrawal status.

Discovery, a scan instruction, inclusion in an earlier registry, a general instruction to update the repository or silence does not substitute for this person-specific decision.

A blank, general, incomplete or ambiguous decision means `PRIVATE_ONLY`.

## 7. Display modes

Use only:

- `PRIVATE_ONLY`
- `PUBLIC_AGGREGATE_ANONYMOUS`
- `PUBLIC_ROLE_PSEUDONYM`
- `PUBLIC_PARTIAL_NAME`
- `PUBLIC_FULL_NAME`
- `PUBLIC_WITHDRAWN`

Initials, a unique employer, a job title, a date, a meeting, a person ID or a distinctive role combination may permit re-identification. Treat them as pseudonymisation unless a documented assessment supports genuine anonymity.

## 8. Data architecture

### Neutral identity layer

The canonical immutable identity registry remains a neutral identity-resolution layer. It may preserve private identity continuity, aliases and non-equivalence controls but must not be treated as public-list authority.

### Private classification authority

The complete person-to-category mapping, exact identity, native source locators, personal data and authorization evidence belong in an access-controlled system outside Git.

### Public projection

The public website must be generated from an approved, minimized projection containing only:

- the immutable public-safe ID where appropriate;
- authorized category;
- authorized display mode;
- authorized public label;
- dated capacity;
- public-safe source/proposition references;
- evidential-status and non-inference language; and
- authorization/review state that does not reveal private source locators.

A directory named `private`, `internal`, `.github`, `archive` or `evidence` does not provide confidentiality in a public repository.

## 9. Legacy and withdrawal controls

- Do not reuse an immutable identity ID.
- Withdrawing a public presentation does not delete the private identity or native evidence.
- Do not silently rewrite Git history as a privacy remedy.
- Record that earlier commits, workflow artifacts, caches and third-party copies may retain historical exposure.
- Replace unnecessary person-level propositions with aggregate, document, event, role or entity propositions where possible.
- Preserve compatibility routes and sent links where required, while minimizing the current display under express authority.

## 10. Current specific controls

Pending a separately authorized person-by-person implementation:

- `PD-SP-P-0065` is controlled as `TRANSACTION_DEVELOPMENT_PRIVATE`; it is not eligible for either principal public perimeter merely because of historic banking or transaction-development contact.
- `PD-SP-P-0066` is controlled as `TRANSACTION_DEVELOPMENT_PRIVATE`; it is not eligible for either principal public perimeter merely because of historic banking or transaction-development contact.

These controls do not themselves alter the current public registry file or claim that no later legal/evidential fact could ever become material. Any later change requires a specific source-supported reassessment and express authorization.

## 11. Implementation sequence

Before changing the public list:

1. audit all existing public people and every newly discovered candidate;
2. prepare the person-by-person authorization matrix privately;
3. obtain the exact decisions;
4. create a minimized public classification projection;
5. render the two principal perimeters separately, followed by the three separate non-perimeter role lists;
6. keep transaction and unresolved candidates private;
7. update ES/EN pages, filters, exports, counts, schemas, validators and correction channels together;
8. test privacy, identity integrity, referential integrity, preservation and desktop/mobile rendering;
9. merge only the authorized scope; and
10. verify the exact merge SHA on both live language routes.

## 12. Future-thread rule

Any future thread that scans emails, files, the repository or the website for people must:

- treat newly discovered names as private candidates;
- resolve exact identity and capacity without automatically publishing;
- classify ours, adverse, professional, institutional, witness/custodian, transaction and unresolved roles separately;
- request person-specific display authorization before mutation; and
- preserve the neutral immutable ID even where the public display is withdrawn or anonymised.
