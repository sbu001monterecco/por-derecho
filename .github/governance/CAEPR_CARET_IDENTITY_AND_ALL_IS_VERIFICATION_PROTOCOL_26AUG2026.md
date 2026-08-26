# CAEPR caret identity and `all is^` verification protocol

**Control date:** 26 August 2026

**Status:** repository operating protocol; manual/advisory enforcement

**Applies to:** people, organisations, institutions and proceedings named in Por
Derecho analysis, registers, dossiers, prompts, reports and public-safe
presentations

## 1. Purpose

The project's existing federated identity system is named the **Canonical
Actors, Entities and Proceedings Registry (`CAEPR`)**. The system remains
federated; this protocol does not create a competing register or silently merge
objects that existing controls keep separate.

The literal marker `^` provides a compact visible indication that the marked
object has passed canonical identity resolution for the stated context. It is a
pointer to identity work, not a substitute for that work.

The controlling data and protocols are:

- `assets/data/matter-identity-registry-v1.json` and its typed parts;
- `assets/data/matter-identity-operational-control-v1.json`;
- `ops/CANONICAL_ENTITY_NAMES.json`;
- `archive/PROCEEDINGS_MASTER_REGISTER_PROTOCOL.md` and
  `archive/PROCEEDINGS_MASTER_REGISTER.csv`;
- `archive/OPEN_SOURCE_INTELLIGENCE_NAMED_PERSON_ENTITY_PROTOCOL_25AUG2026.md`;
  and
- the relevant correction, evidence-status and specialist proceeding controls.

## 2. Exact meaning of `^`

`Name^` means only:

> The displayed person, organisation, institution or proceeding has been
> positively identified, reconciled to one immutable CAEPR record and cleared of
> a material unresolved identity collision for the stated context.

It does not establish or certify:

- the truth of an allegation or factual proposition;
- an actor's capacity on every date or in every proceeding;
- participation, authorship, receipt, knowledge, intention or coordination;
- a relationship, group, beneficial ownership or control;
- civil, criminal, concursal, regulatory or professional liability;
- current corporate, professional, institutional or procedural status;
- the outcome, finality, merits or legal effect of a proceeding; or
- the authenticity, completeness or evidential weight of a source.

Every such proposition keeps its own source, date, attribution and status.

## 3. Resolution states

Use the following audit states without overwriting the underlying source-status
vocabulary:

| State | Meaning |
| --- | --- |
| `CARET_CONFIRMED` | eligible object resolved to one immutable CAEPR ID for the stated context |
| `CARET_PENDING` | plausible object or match, but a material identity attribute, source or collision remains open |
| `CARET_SUSPENDED` | previously marked object requires renewed review because later evidence creates a material identity conflict |
| `CARET_NOT_APPLICABLE` | item is a source literal, quotation, conceptual structure, event, document or other object outside the marker's defined scope |

These states are context-sensitive. A company may be `CARET_CONFIRMED` as the
legal person named in a deed yet still have an open current-status question. A
person may be identified but have an unresolved mandate or capacity. A
proceeding may be identified while its current status or finality remains open.

## 4. Eligibility thresholds by object type

### Person

A person is eligible only when the exact identity meets the repository's
identity-admission threshold: ordinarily an unequivocal official identifier or
at least two compatible independent attributes, plus no material contradictory
match. Name and geography alone are insufficient. Homonyms and incomplete names
remain `CARET_PENDING`.

### Organisation or other entity

An exact legal person is eligible only when its legal name and distinguishing
identity are sufficiently resolved. Former names, brands, branches, professional
perimeters, funds, SPVs and corporate groups must remain separate unless the
marked object is expressly that non-legal perimeter rather than an exact legal
person. A record carrying an unresolved exact-entity or legal-form status is not
eligible for an exact-legal-person caret.

### Institution or public organ

An institution is eligible when the marked organ is resolved at the level used
in the proposition. Identification of a national institution does not by itself
identify a territorial office, chamber, section, unit, official or decision
maker.

### Proceeding or institutional file

A proceeding is eligible only when its legally useful identity is established
and reconciled with the Proceedings Master Register. The minimum normally
includes the competent organ, reference and proceeding/file class; parties,
parent/child relationship, jurisdiction or year must also be resolved where
needed to eliminate ambiguity.

A registration receipt, output number, draft, email subject, transmission,
filename, internal control label or unresolved candidate is not converted into a
proceeding by adding `^`. Appeals, incidents, piezas and parent proceedings
retain distinct IDs where the master-register protocol requires them.

### Excluded object types

Conceptual structures, alleged perimeters, chronology events, assets, evidence
objects, propositions and source literals do not receive `^` merely because they
are indexed elsewhere. If text also names an eligible CAEPR person, entity,
institution or proceeding, mark that resolved object outside the source literal.

## 5. Marker placement and accessibility

- Place the literal caret immediately after the canonical display label:
  `CaixaBank, S.A.^`, `Gil Marer^`, `Concurso 36/2012^`.
- Do not insert the marker into a quotation, official title, source literal,
  filename, search string, URL, formal citation or identifier.
- Where a source literal differs, preserve it and reconcile separately, for
  example: `“Luchi Playa Blanca” [source literal] — Luchy Playa Blanca, S.L.U.^`.
- Use the marker on the first identity-sensitive reference and again wherever
  ambiguity could reasonably recur. Do not make prose unreadable by marking
  every pronoun or harmless repetition.
- A page, table or report using `^` must provide a visible legend. Digital
  surfaces should expose the immutable CAEPR ID and resolution state in
  machine-readable data or adjacent text; punctuation alone is not an
  accessibility or referential-integrity system.
- Absence of `^` means only that the presentation does not assert completed
  canonical resolution. It is not proof that the object is fictitious,
  unrelated or unidentified elsewhere.

## 6. Command protocol: `confirm all is^`

The instruction `confirm all is^` is a verification command, never a direction
to manufacture a complete result.

### Scope

Use the scope expressly stated by Gil Marer. If none is stated, use the complete
current deliverable and every distinct named person, organisation, institution
and proceeding on which it relies. Do not silently interpret it as the entire
historic repository unless the prompt says repository-wide.

### Required run

1. Extract every in-scope named reference.
2. Classify its object type and whether the reference is canonical wording,
   alias, former name, source literal or unresolved candidate.
3. Deduplicate aliases and variants without collapsing distinct legal people,
   entities, organs, capacities or proceedings.
4. Resolve each candidate to an immutable CAEPR ID and the relevant current
   correction/source controls.
5. Apply the object-specific eligibility threshold.
6. Record `CARET_CONFIRMED`, `CARET_PENDING`, `CARET_SUSPENDED` or
   `CARET_NOT_APPLICABLE` with a reason.
7. Add or retain `^` only for `CARET_CONFIRMED` objects in eligible display
   positions.
8. Report the denominator, result and exceptions before making a completion
   claim.

### Denominator and report

The denominator is the number of unique in-scope eligible candidate objects
after alias deduplication. Report quoted/source-literal-only and other
`CARET_NOT_APPLICABLE` items separately; do not use them to inflate or depress
the eligibility percentage.

Required result:

| Field | Required content |
| --- | --- |
| Scope | exact file, page, prompt, report, register or repository slice checked |
| Denominator | unique eligible candidate objects, with counts by type |
| `^` count | objects in `CARET_CONFIRMED` state and correctly marked |
| Coverage | `^ count / denominator × 100`, without rounding away an exception |
| Exceptions | object, current state, ambiguity, source gap and next source needed |
| Non-applicable | quoted literals or excluded object types handled outside the denominator |

Use `ALL IS^ — VERIFIED FOR THE STATED SCOPE` only where the exception count is
zero. Otherwise use `PARTIAL — NOT ALL IS^`. Never add carets merely to reach
100%, and never describe a finite-scope result as universal repository coverage.

## 7. Corrections and lifecycle

- Preserve the immutable ID when a spelling, former name or display label is
  corrected, unless evidence establishes that two distinct objects were
  mistakenly merged.
- If a material collision or contradiction arises, change the presentation
  state to `CARET_SUSPENDED`, remove the displayed caret where necessary and
  preserve a correction record explaining why.
- Do not silently transfer a caret from a parent company to a subsidiary, a firm
  to a lawyer, an institution to an office, a proceeding to an appeal, or a
  person to a relative or namesake.
- Recheck time-sensitive identity attributes before claiming a current role,
  status or capacity even where the identity itself remains caret-confirmed.
- A later source may change a role or proposition without invalidating the
  object's identity. Update only the layer the source actually changes.

## 8. Governance and enforcement boundary

This protocol is a manual operating control. It does not itself:

- rewrite existing registry schemas or append `^` to stored canonical names;
- mass-edit historical pages or source transcriptions;
- change public routes, navigation, sitemaps, metadata or deployment;
- activate a required CI check or repository ruleset; or
- authorise publication, email, filing, contact or another external action.

Any automated validator must first run in advisory/shadow mode on representative
person, entity, institution, proceeding, quotation and bilingual-page changes.
Promotion to a required gate needs the separate authority and compatibility
process in `AGENTS.md` and
`.github/governance/AGENT_PUBLISHING_COMPATIBILITY.md`.

## 9. Recommended implementation sequence

1. **Schema review:** add non-destructive identity-resolution and caret-eligibility
   fields to the federated CAEPR parts without changing canonical names.
2. **Proceedings reconciliation:** map the complete Proceedings Master Register to
   immutable `PD-SP-R-####` IDs; preserve unresolved references instead of
   forcing matches.
3. **Report generator:** build an advisory tool that extracts unique named
   references and produces the denominator/exception table for a chosen scope.
4. **Shadow validation:** test alias deduplication, `not_same_as`, former-name,
   source-literal and parent/child-proceeding cases before any enforcement.
5. **Public presentation:** only under separate website authority, introduce a
   bilingual visible legend and accessible machine-readable CAEPR references on
   selected canonical surfaces before considering broader propagation.
6. **Correction audit:** record every later caret suspension, split or merge in
   the correction register and re-run affected finite-scope coverage reports.

## Governing sentence

> `^` confirms canonical identity resolution for a stated context; it never
> proves conduct, responsibility, status or outcome. `All is^` is earned by a
> zero-exception audit, never asserted by instruction.
