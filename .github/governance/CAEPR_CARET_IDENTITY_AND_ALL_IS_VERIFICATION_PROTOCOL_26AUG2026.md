# CAEPR caret identity marker + `^` registration/interlink verification command

**Control date:** 26 August 2026  
**Revised:** 30 August 2026  
**Status:** repository operating protocol; manual/advisory enforcement  
**Command token:** `^`

## 1. Purpose and precedence

The project's federated identity system is the **Canonical Actors, Entities and
Proceedings Registry (`CAEPR`)**. The system remains federated: this protocol does
not create a competing universal register, collapse legally distinct objects, or
silently merge records that existing controls keep separate.

This protocol now distinguishes two uses of the caret:

1. **presentation marker** — a caret already printed after an eligible CAEPR
   person/entity/institution/proceeding continues to indicate canonical identity
   resolution for the stated context; and
2. **user command** — when Gil Marer enters `^`, either by itself or against a
   named/material object, it is a mandatory **registration, canonical-identity,
   provenance, relationship, chronology, publication and continuity audit**.

The **command meaning is broader than the presentation-marker meaning**. Any
older repository statement saying that “`^` means identity only” is to be read
as describing the presentation marker, **not** as limiting the user command.
For user-command interpretation, this 30-August-2026 revision controls.

The command is action + verification, not acknowledgement or brainstorm. A
previous ChatGPT statement that an item was registered, uploaded, published,
interlinked, complete or live is not proof. Inspect the underlying repository,
registers, sources and live/public state that are actually available.

## 2. Controlling repository systems

Use the applicable federated register(s) rather than forcing every object into
CAEPR. Relevant controls include, without limitation:

- `assets/data/matter-identity-registry-v1.json` and its typed parts;
- `assets/data/matter-identity-operational-control-v1.json`;
- `ops/CANONICAL_ENTITY_NAMES.json`;
- `archive/PROCEEDINGS_MASTER_REGISTER_PROTOCOL.md` and
  `archive/PROCEEDINGS_MASTER_REGISTER.csv`;
- evidence registers, source/provenance registers and correction registers;
- chronology/event registers and master-timeline controls;
- property/asset, transaction, ACTA/meeting and specialist matter registers;
- relationship/interlink controls and generated/API data;
- publication manifests, deployment logs and public-route controls; and
- `archive/OPEN_SOURCE_INTELLIGENCE_NAMED_PERSON_ENTITY_PROTOCOL_25AUG2026.md`
  plus any later controlling specialist protocol.

## 3. Presentation-marker meaning (`Name^` in repository/public prose)

For an eligible CAEPR object, a displayed `Name^` means only:

> The displayed person, organisation, institution or proceeding has been
> positively identified, reconciled to one immutable CAEPR record and cleared of
> a material unresolved identity collision for the stated context.

It does **not** establish the truth of an allegation, participation, receipt,
knowledge, intent, coordination, ownership/control, legal liability, current
status, procedural outcome, authenticity or evidential weight. Each proposition
retains its own source, date, attribution and status.

Existing CAEPR presentation states remain:

| State | Meaning |
| --- | --- |
| `CARET_CONFIRMED` | eligible CAEPR object resolved to one immutable CAEPR ID for the stated context |
| `CARET_PENDING` | plausible object/match but material identity source or collision remains open |
| `CARET_SUSPENDED` | prior identity resolution requires renewed review after material conflict |
| `CARET_NOT_APPLICABLE` | object is outside the presentation marker's eligible CAEPR scope |

Events, evidence objects, documents, transactions, properties/assets,
communications and propositions may therefore be `CARET_NOT_APPLICABLE` as
**presentation markers** while still being fully eligible targets of the **user
command** below.

## 4. User-command scope (`^`)

When `^` is used as an instruction, apply it to any material object, including:

- person, professional, witness or office-holder;
- legal person, commercial entity, institution, organ, group/perimeter or brand;
- proceeding, appeal, incident, pieza, filing, registration, judicial/LAJ/
  prosecutorial/administrative decision or procedural event;
- evidence item, source document, ACTA/minutes, email, communication, image,
  recording, exhibit or evidence family;
- event, date, milestone, transaction or financial flow;
- property, finca, hotel, unit, asset or security;
- contract, offer, instrument or corporate act;
- allegation, thesis, hypothesis, issue or competing explanation; and
- any other material object whose identity, provenance or relationships matter
  to reconstruction of the record.

If the user writes only `^` in a new thread, retrieve the relevant continuity
context where available and identify the immediately relevant prior/referenced
matter before running this protocol. Do not ask the user to repeat information
that durable continuity sources can resolve.

## 5. Mandatory command audit

For each `^` target perform all applicable checks below.

### A. REGISTER

Determine whether the object is formally represented in the correct one or more
repository registers, indexes, evidence controls, chronology controls,
proceedings registers, identity registers, relationship controls, source
registers and publication manifests.

A prose mention is **not** equivalent to registration.

### B. UNIQUE CANONICAL IDENTITY

Verify that the object has a stable, unique, canonical repository identifier in
the appropriate register or a documented reason why its object class uses a
different durable key.

Reconcile, without destroying provenance:

- spelling/OCR variants and abbreviations;
- aliases, former/current names and trading/brand names;
- legal-person versus group/perimeter/brand distinctions;
- different capacities or roles of the same person/entity;
- proceeding references, parent/child proceedings, appeals, incidents and
  piezas; and
- duplicates/near-duplicates, `same_as` and `not_same_as` relationships.

Never solve a collision by silently merging distinct people, entities,
proceedings or sources.

### C. PROVENANCE AND EVIDENCE STATUS

Identify what supports the object's identity, significance and each material
relationship. Prefer primary/local sources where available.

Keep separate and visibly status-grade:

- documented/established source fact;
- court/authority statement or procedural fact;
- party allegation;
- Gil Marer's attributed contention;
- analytical deduction/inference/hypothesis; and
- unresolved question/source gap.

Repeated cross-linking does not transform an allegation or inference into fact.

### D. RELATIONSHIP GRAPH

Determine what the object is and should be linked to, including relevant:

- people and witnesses;
- companies/legal persons, groups and institutions;
- professional advisers and public organs;
- proceedings, appeals, incidents and procedural pieces;
- filings and decisions;
- evidence, ACTAs, emails and communications;
- events, dates and chronology milestones;
- transactions, contracts and financial flows;
- properties/assets and security interests;
- allegations, competing explanations and legal/forensic issues;
- repository dossiers, generated data/API records; and
- website/publication pages.

Relationship edges must carry provenance/status where material. A chronology,
family, employer, corporate-name or page-neighbour relationship does not by
itself prove knowledge, coordination, wrongdoing or liability.

### E. BIDIRECTIONAL INTERLINKING

Do not test only whether A points to B. Where materially appropriate, verify that
B can discover or link back to A, either directly or through a canonical graph/
index. Record intentionally one-way links where the architecture requires them.

### F. PROCEEDING + EVIDENCE CONTEXT

Where relevant, establish:

- exact proceeding(s), organ, reference, class and procedural capacity;
- parent/child/appeal/incident relationships;
- supporting and contradicting evidence;
- preceding/following events;
- filings/decisions that mention or depend on the object; and
- allegations/legal issues whose proof depends upon it.

A receipt number, filename, transmission or internal control label is not
silently promoted into a proceeding.

### G. CHRONOLOGY

Ensure significant objects can be reached from the master chronology and, where
appropriate, proceeding-specific, entity-specific, asset-specific and
evidence-specific timelines. Dates remain source-graded and conflicting dates
remain visible until resolved.

### H. PUBLICATION / LIVE STATE

Verify these as separate layers:

1. repository existence;
2. formal registration/indexing;
3. relationship/interlink presence;
4. publication-manifest/build inclusion;
5. source commit/deployment state;
6. actual live route/resource availability; and
7. discoverability from the relevant public page/navigation/API where required.

**Repository existence is not proof of website publication.** A build manifest is
not proof of successful deployment. A successful deployment is not proof that a
specific route is reachable or byte-equivalent to the intended source.

Do not publish private/restricted material merely to satisfy a caret audit.

### I. GAP / DUPLICATION AUDIT

Check for and report:

- missing registration or wrong register;
- missing, unstable or duplicate ID;
- ambiguous identity/capacity/legal person;
- orphan record;
- duplicate/near-duplicate without reconciliation;
- broken/missing cross-link or backlink;
- missing provenance/source citation;
- missing chronology/proceeding/evidence/asset relationship;
- unsupported relationship edge;
- missing publication-manifest/live link; and
- inconsistent name, date, role, capacity, status or procedural reference.

### J. REPAIR, DON'T JUST REPORT

Where authorised and technically possible, repair safe gaps in the repository,
registers, interlinks or publication controls in the same run. Preserve existing
valid IDs, source literals, provenance, correction history and audit trails.
Never manufacture facts, force an unresolved match, suppress contrary evidence,
or silently overwrite a conflict.

Where a gap cannot safely be repaired, leave a durable open item stating the
missing source/action and why it remains unresolved.

### K. CONTINUITY / DELETION SAFETY

The object should remain reconstructable after deletion of the originating
ChatGPT thread. Durable repository state should allow a later thread to answer:

> **what is it → why does it matter → what is its canonical ID/key → which
> register(s) hold it → where did it come from → what supports/contradicts it →
> what does it connect to → where does it sit in chronology/proceedings → what is
> its publication/live status → what remains open?**

Chat deletion safety is not source-deletion authority. Native evidence, private
custody archives and backups remain governed by their own retention controls.

## 6. Command result/status contract

A `^` audit must return one or more of these operational statuses rather than a
bare “yes”:

- **VERIFIED** — required registration/identity/provenance/interlink checks for
  the stated scope are established;
- **PARTIALLY VERIFIED** — some layers verified, one or more material checks
  remain open;
- **GAP FOUND** — a registration/ID/link/provenance/publication defect exists;
- **UNRESOLVED / SOURCE REQUIRED** — reliable resolution is not presently
  supportable; and
- **REPAIRED** — a verified safe defect was corrected and the resulting state
  was re-read/checked.

The output should identify, as applicable:

- canonical object and ID/key;
- register(s);
- aliases/collisions reconciled;
- source/provenance state;
- significant incoming/outgoing relationships;
- proceeding/chronology position;
- repository/publication/live state;
- gaps and fixes; and
- remaining open items.

## 7. `confirm all is^` / finite-scope audit

`confirm all is^` remains a verification command, never a direction to
manufacture completeness.

Use the scope expressly stated by Gil Marer. If none is stated, use the complete
current deliverable and its materially relied-upon objects. Do not silently call
a finite deliverable “the entire repository.”

For CAEPR-eligible presentation objects, retain the existing denominator logic
and `CARET_CONFIRMED` / `CARET_PENDING` / `CARET_SUSPENDED` states. For the broader
user-command audit, report excluded presentation-marker object types separately
but **do audit their registration/interlinks** where material.

Use `ALL IS^ — VERIFIED FOR THE STATED SCOPE` only when the stated denominator
has zero material exceptions. Otherwise use `PARTIAL — NOT ALL IS^`.

## 8. Corrections and lifecycle

- Preserve immutable IDs when correcting spelling/display labels unless evidence
  establishes that distinct objects were wrongly merged.
- If a material collision appears, suspend the affected identity/edge, preserve
  a correction record and remove any misleading presentation marker where
  necessary.
- Do not transfer identity, evidence, intent, role or liability across a parent/
  subsidiary, firm/lawyer, institution/office, proceeding/appeal, relative/
  namesake, asset/operator or source/derived-document relationship.
- Recheck time-sensitive status/capacity before claiming it is current.
- Later evidence may change one relationship/proposition without invalidating the
  canonical object itself; update only the layer the source actually changes.

## 9. Governance / publication boundary

This protocol is an operating control. It does not by itself authorise external
email/contact, filing, source destruction, credential use, publication of
restricted material, or unsupported mass-editing of historical pages.

Automated validators should begin advisory/shadow mode and follow `AGENTS.md`
and `.github/governance/AGENT_PUBLISHING_COMPATIBILITY.md` before becoming a
required gate.

## 10. Governing sentences

> **Presentation:** `Name^` confirms canonical CAEPR identity resolution for the
> stated context; it never proves conduct, responsibility, relationship, status
> or outcome.

> **Command:** when Gil Marer uses `^` as an instruction, verify the target as a
> first-class repository object: registered, uniquely keyed, provenance-graded,
> procedurally/chronologically situated, bidirectionally interlinked where
> material, publication-aware, gap-audited, repaired where safe, and
> reconstructable without the originating chat.

> **Verification:** prior ChatGPT assurances are not evidence. Verify the
> underlying repository and live/public state before saying “registered”,
> “interlinked”, “published”, “live”, “complete” or “deletion-safe”.
