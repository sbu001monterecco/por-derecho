# A-SCAN 360 — CASE PRISM AND READER-LENS PROTOCOL

**Date:** 30 August 2026  
**Status:** repository-wide additive governance  
**Canonical proceedings source:** `archive/PROCEEDINGS_MASTER_REGISTER.csv`  
**Derived public Case Prism source:** `assets/data/proceedings-case-prism-v1.json`  
**Public routes:** `/en/proceedings-map/` and `/es/mapa-procedimientos/`

## 1. Purpose

Por Derecho must do more than store a large evidential corpus. It must let different readers see the same controlled facts from the perspective of their lawful function without changing the facts, evidence status or legal boundaries.

The A-SCAN 360 method therefore runs five simultaneous tests:

1. **Architecture** — what the reader sees first and how the record can be traversed.
2. **Authority** — who acted, in what capacity, for which legal person/body and with what authority.
3. **Attribution** — documented fact, authority statement, party submission, Por Derecho allegation, inference, contrary evidence and open question must remain distinct.
4. **Audience** — court, Ministerio Fiscal, judicial supervision, regulator/public authority, journalist/researcher and other readers receive different priorities/questions over the same source-controlled record.
5. **Actionability** — each serious proposition should resolve to a finite question, source, competent organ, connected proceeding and possible consequence if confirmed or refuted.

The 360° pass then cross-reads proceedings, actors, assets, credit, control, exploitation, productive unit, income/value, public money, professional conduct, judicial/LAJ response, Fiscalía response, alleged harm, contrary explanations and source gaps.

## 2. Three traversals are mandatory

Run the corpus:

- **beginning → end**;
- **end → beginning**; and
- **one material proposition → every proceeding/institution that touches it → consequence → source**.

A separate docket number must not terminate the factual trace. A shared asset/actor must not create an invented procedural edge.

## 3. Public Case Prism — why it exists

The repository already required `CONVERGENCE_CLUSTER` and `FRAGMENTATION_AUDIT` views. Before this control, the public proceedings renderer primarily exposed track, chronology and single-proceeding trace views. That mismatch is an implementation gap.

The Case Prism closes that gap by giving each controlled proposition a row and each legal/institutional lane a column. Every coordinate must be explicit; an unexplained blank or dash is prohibited. Each coordinate must state one relationship status:

- `DIRECT` — direct within the controlled lane;
- `CONTEXT` — materially relevant cross-reading context only;
- `OPEN` — bridge to test / incomplete source control;
- `NOT_LOCATED` — relevant treatment not located in the controlled corpus; or
- `OUTSIDE` — outside that lane.

A cell must independently state how the selected file treats the proposition: directly in file, expressly acknowledged, relied upon, contradicted/adversely treated, materially relevant context, not raised/not located, outside procedural scope or unresolved. Relationship and treatment are different axes.

A cell must also carry a bilingual plain-language reason, evidence status, decision dependency, counsel/procurador lineage status and relevant canonical Master IDs where appropriate. Each proposition must expose its attribution class, strongest contrary record, controlled public source path, source needed, competent organ and consequences if confirmed or refuted.

Every canonical evidence-status token displayed to a reader must have an English and Spanish label. The renderer may preserve the canonical token for auditability, but it must not substitute that token for the reader-facing bilingual explanation.

## 4. Case Prism is not a joinder engine

The visualization must never imply that:

- separate proceedings are legally one case;
- an organ received material merely because the project can connect it;
- material was admissible merely because it was relevant;
- a contextual bridge proves knowledge, coordination, wrongdoing or liability;
- benefit proves agreement or criminal purpose; or
- a missing treatment proves suppression or concealment.

Formal notice, filing, admission, transmission and procedural usability remain separate source questions.

## 5. Parallel-proceedings lane view

The same controlled propositions must also be readable in approximate chronological order with each legal lane rendered as a stable independent column. Event cards with wrapping lane tags do not satisfy this requirement.

The purpose is to make two propositions visible at the same time:

> **same event ≠ same proceeding**

and

> **different proceeding ≠ factual isolation**.

Chronological adjacency is not causation.

## 6. Isolation test / fragmentation audit

For each selected exact canonical proceeding, the public renderer must distinguish:

### Visible inside the selected lane
Only propositions marked `DIRECT` for that lane and keyed to the selected exact proceeding.

### Material context outside the selected lane
Controlled propositions visible elsewhere and tied to the selected exact
proceeding through its own non-`DIRECT` coordinate or through a source-controlled
direct relationship / contextual cluster. The interface must not treat every
proposition in the wider corpus as material merely because the selected file has
one Case Prism coordinate. It must visibly suppress/fade the wider corpus and
provide an immediate full-corpus restore.

Same stream, geography, institution or chronological proximity is browse
taxonomy only. Without an additional controlled connection it cannot populate
the material-context or disappearing-proposition list.

The isolation view is methodological. It does not prove that an organ knew, should have known, should admit, should investigate or should decide external material.

For each proceeding/laned object the underlying audit question is:

> **If this file is read alone, what controlled material context becomes invisible, and what is the precise evidential status of that context?**

## 7. Reader lenses

The public Case Prism may offer reader lenses including:

- Court / magistrate;
- Audiencia Provincial;
- Ministerio Fiscal;
- CGPJ / judicial supervision;
- regulator / public authority; and
- journalist / researcher;
- affected owner / creditor; and
- professional / funder.

A reader lens may change:

- proposition priority/order;
- the leading finite question; and
- explanatory emphasis.

It must never change:

- the proposition itself;
- source status;
- canonical Master IDs;
- the direct/context/open classification;
- legal-person identity; or
- evidential boundaries.

## 8. Current high-priority lanes

The Case Prism currently includes the controlled public-safe lanes needed to make the anti-fragmentation architecture intelligible:

- Concurso 36/2012;
- Calificación / RPL 2523/2025;
- AC separation/removal / RPL 3304/2025 + accumulated/linked RPL 3319/2025;
- AC fees/remuneration / RPL 421/2026;
- Arrecife control/mortgage/title;
- Valencia / CaixaBank (`VAL-CIV-001`);
- Meeting Point / FTI contextual restructuring;
- Tenerife / Matkator / Cuatrecasas;
- Ministerio Fiscal;
- CGPJ / LAJ supervision; and
- historical possession/exploitation.
- administrative / RIC / Regional Incentives / ERDF and other controlled public-money routes.

This is a controlled priority denominator, not a claim that every repository proceeding belongs in every Case Prism row.

## 9. Current proposition families

The public Case Prism is intentionally finite. Its current propositions cover:

- Concurso 36/2012 as procedural spine;
- secured credit / enforcement / title;
- 7 June 2018 access/material-control context;
- the three Audiencia appellate objects and their common insolvency-administration dependency;
- Ministerio Fiscal institutional-response chronology;
- Matkator / Cuatrecasas / Tenerife separation-and-context rule;
- historical possession/exploitation genealogy;
- Meeting Point / FTI contextual restructuring with the Sun Park bridge still open; and
- judicial-supervision treatment versus merits competence.
- Community authority;
- debt/voting denominator;
- pre-7 June 2018 funded exit;
- 2020 project promotion;
- the July-2021 `54 / 190 / 18` title record;
- 2022 adjudication/deed/registration;
- productive-unit, income and value consequences;
- AC conduct versus remuneration; and
- RIC / incentives / ERDF programme dependencies.

New propositions require source/status review before admission to the public Case Prism.

## 10. Contrary evidence / innocent explanation

Every future Case Prism expansion must actively test lawful authority, valid title, legitimate creditor rights, legitimate procedural discretion, drafting error, incomplete source access, independent institutional reasoning, benefit without agreement and other materially contrary explanations.

The Case Prism is strongest when it makes uncertainty and contrary evidence visible rather than forcing a theory.

## 11. Implementation truth

Governance, schema, renderer and deployed website are separate verification layers.

A view is not “implemented” merely because its name appears in schema or governance. The actual public renderer must expose it and CI must test its presence.

Future A-SCAN 360 closeouts must separately report:

- repository source;
- canonical registration;
- direct procedural-edge coverage;
- convergence/context coverage;
- Case Prism proposition coverage;
- fragmentation/isolation coverage;
- audience-lens coverage;
- bilingual publication;
- deployment; and
- live readback.

## 12. Exact-file actionability and institutional-memory coverage

The proposition matrix and the exact-proceeding audit answer different
questions and must keep separate denominators.

The controlling implementation pair for this closure is
`proceedings-interconnectivity-schema-v1.json` **1.7.0** and
`proceedings-interlinkability-v1.json` **1.1.0**. A renderer, builder, audit or
publication record that validates an older contract may not close the current
denominator.

- **Proposition membership** asks whether an exact proceeding has been admitted
  to at least one non-`OUTSIDE` coordinate in the finite 19 × 12 shared
  proposition matrix. The current controlled denominator remains **26 / 97**;
  the other **71** exact proceedings must remain visible as no-coordinate gaps
  unless a source-reviewed proposition and lane are admitted. A generic shared
  asset, geography, office or chronology may not close that denominator.
- **Exact-file actionability** asks whether every public exact proceeding has a
  finite test. The controlled target is **97 / 97**. Each test must preserve the
  exact ID and must contain file-specific, bilingual values for the finite
  question, source needed, current source status, recorded candidate
  organ/custodian and its limits, direct/context memberships, decision
  dependency, strongest contrary explanation and consequences if confirmed or
  refuted. It must also expose the canonical public-record route and an explicit
  proceeding-specific public primary-source route or primary-source route gap.
  A recorded custodian/organ is only a candidate: it may never be described as
  legally competent, empowered or obliged to act by the model. Consequences
  must refer conditionally to the legally competent organ and a lawful route.
  The strongest contrary explanation must remain expressly hypothetical and
  may not attribute an act to that recorded candidate without a primary source.
  Family taxonomy must follow the canonical record type before a mixed Stream
  substring: administrative/professional context is not professional discipline,
  and civil professional liability remains a civil judicial file.
  These content fields must be independently non-empty and the decision
  dependency, contrary explanation and two consequences must be unique to the
  exact file. A family template is taxonomy only: generic registry-maintenance,
  source-retrieval or “correct the record” boilerplate cannot count as 97 / 97
  actionability. Completion of the data structure is not completion of the
  missing evidence.
- **Institutional receipt and knowledge classification** asks whether every
  exact-file test states what is and is not established across nine independent
  institutional axes: transmission, material received/inventory, referral,
  registration, file incorporation, recipient attribution, substantive
  examination, decision use and cross-file acknowledgement. The controlled
  target is **97 / 97 nine-axis provenance records**. Every axis must carry its
  own controlled status, bilingual basis, bilingual limitation and exact source
  pointer or explicit source-not-located object; one source or grade may not be
  silently inherited by another axis. A positive grade must cite the exact
  episode field that substantively supports that axis; an episode-specific field
  is required where a global axis default would cite unrelated text. Transmission and referral are independent
  grades: neither proves the other or destination receipt. Positive-evidence
  counts remain separate. Actor-specific receipt and actor-specific knowledge
  are additional, separate non-positive controls unless an actor-specific source
  identifies the person, act/material, time and permissible scope. Institutional
  receipt never proves personal receipt; presentation never proves file
  incorporation; incorporation never proves substantive examination;
  examination never proves reliance; and none of those states proves intent,
  agreement, wrongdoing or liability.
- **Ministerio Fiscal institutional memory** uses a separate current denominator
  of **24 / 24 public Master Register Fiscalía rows**. Source-controlled episode
  profiles may connect an office/file only through reviewed event-to-matter
  relationships. Raw reference-string equality is not proof of receipt,
  incorporation, examination or cross-file recognition. The current model
  contains nine source-controlled response episodes: eight profile rows in the
  24-row Fiscalía matrix and one `DP 1901/2026` judicial-file profile kept
  outside that matrix. Remaining files and events must carry explicit
  `NOT_LOCATED` or unresolved treatment rather than disappear. The 24-row
  denominator must remain split into **21 exact file rows and three unresolved
  references**, and the matrix must expose, separately and bilingually for every
  row: source-attributed material allegations/evidence; material received plus
  the item-level inventory gap; direct and contextual proceedings; related
  assets plus the asset gap; what was referred; what was actually examined; the
  institutional response; cross-file acknowledgement; unitary acknowledgement;
  the strongest contrary explanation; and the unanswered/source gap. Empty
  positive arrays plus an explicit gap are valid; collapsing these columns into
  one narrative summary is not.
- **Route coverage** is complete only as a controlled navigation disposition:
  every one of the 97 public exact IDs must resolve to the Master Register, exact
  trace and isolation state. A dedicated narrative dossier is a different,
  separately counted route. A null or not-established dossier route must not be
  replaced by an invented page or by a nearby proceeding's dossier.

The exact-file layer must continue to report source-backed direct edges
separately from source-reported relationships awaiting primary completion. It
must also preserve the open counsel/procurador denominators and every
`SOURCE_NOT_LOCATED` state. Those evidence gaps do not defeat structural audit
coverage, but structural coverage must never be described as proof that the
underlying evidence, knowledge, treatment or merits are complete.

The tracked operational `archive/PROCEEDINGS_MASTER_REGISTER.csv` remains a
separately recorded, accepted publication-boundary gap while it is reachable
from the public host. It is not an intended renderer input or live invariant,
and its exposure prevents a `DELETION_SAFE` claim for the interlinking release.

## 13. Governing sentence

> **Preserve every proceeding as the legally distinct object that it is, while enabling a conscientious reader to see on one screen which controlled facts, sources, assets and consequences cross those procedural boundaries. Make fragmentation visible without presuming wrongdoing, and make every visual status no stronger than the source that supports it.**
