# Por Derecho Evidence Control Plane — bootstrap v1

## Purpose

This module introduces a platform-independent evidential control contract above the existing repository, custody, publication and case-analysis controls.

It is additive. It does **not** replace the existing canonical registries, correction registers, proceeding registers, source inventories, publication gates, private-custody rules or host-specific release machinery.

## Authority boundary

At this bootstrap checkpoint:

- existing repository authority declarations remain controlling;
- the private GitLab repository remains the current canonical repository authority where existing controls say so;
- GitHub remains a reviewed continuity/public-safe control and publication surface where existing controls say so;
- the logical Evidence Control Plane is a portable data contract, **not yet a migration of canonical host authority**;
- no public page, allegation, filing, email, social post or external communication is authorised by this module.

Host authority, access state, evidential state and publication state are separate axes and must never be conflated.

## Core object model

The portable model recognises these first-class object types:

`SOURCE`, `EVIDENCE_OBJECT`, `DERIVATIVE`, `ACTOR`, `ENTITY`, `EVENT`, `ASSERTION`, `RELATIONSHIP`, `CONTRADICTION`, `HYPOTHESIS`, `PROCEEDING`, `INVESTIGATIVE_ACTION`, `PRESERVATION_EVENT`, `PUBLICATION`, `WORKSPACE`.

A document, email, recording, image, archive or witness recollection is an evidence/source object. A proposition derived from it is a separate assertion. A legal characterisation is never silently promoted from either one.

## Mandatory reasoning boundary

Every consequential assertion should make it possible to answer:

1. What is the exact source?
2. Who is speaking or attributing the proposition, and in what capacity?
3. What event time does it concern?
4. When did the project first know or record it?
5. What supports it?
6. What contradicts, narrows or may exculpate it?
7. What does it **not** establish?
8. What earlier proposition does it supersede, if any?
9. What downstream objects depend on it?
10. What new review is triggered if its status changes?

Source authentication is not truth verification. An allegation is not a finding. An investigation is not guilt. Association is not coordination. Irregularity is not automatically criminal conduct.

## Custody and provenance are separate

**Chain of custody** records where an object came from, where it was stored, who/system handled it and integrity checks.

**Chain of evidence/provenance** records transformations and analytical activity: extraction, transcription, translation, redaction, OCR, parsing, entity resolution, assertion creation, contradiction analysis and publication.

Native evidence must remain distinguishable from every derivative.

## Bitemporal rule

Material records should carry both:

- `event_time`: when the underlying event is said to have occurred; and
- `knowledge_time`: when the project acquired, learned, recorded or verified the proposition.

Later knowledge must not be backdated into the historical event.

## Corrections and supersession

Material history is append-only conceptually. Corrections create explicit typed edges such as `SUPERSEDES`, with reason, date and source. Older material remains preserved as provenance and must not silently continue as current truth.

## Contrary and exculpatory evidence

Contradictions are first-class records, not footnotes. Significant hypotheses must carry supporting, contradicting, neutral and missing evidence, including evidence that could falsify the hypothesis.

## Dependency-triggered reanalysis

When an assertion changes status, every dependent chronology, actor record, proceeding, institutional communication, hypothesis, public page and publication package should enter a re-review queue. Correction propagation must not depend on memory.

## Workspace / writer discipline

One writer per integration lane remains the rule. A ChatGPT thread, GitHub agent, GitLab/Duo worker or human may research in parallel, but canonical mutation must be serialised and attributable. Stale instructions remain provenance, not current operational authority.

## Archive intake

ZIP and other archive carriers are evidence objects in their own right. The native archive is preserved and hashed before controlled extraction. Member paths and hashes are retained. Extraction does not authenticate the member contents and does not authorise publication.

See `ARCHIVE_INTAKE_CONTRACT.md`.

## Projection and parity

GitHub and GitLab are projections/custodians of canonical evidential state, not blindly bidirectional writable mirrors. Differences must be classified explicitly as:

- `PARITY_GAP`
- `INTEGRITY_GAP`
- `PROVENANCE_GAP`
- `IDENTITY_GAP`
- `PROJECTION_GAP`
- `STATUS_GAP`
- `PRESERVATION_GAP`

An explained, intentional divergence is not a gap if it is recorded and bounded.

## Initial finite use cases

The bootstrap creates no merits finding. It opens structured recovery/review targets for:

- the reported 2016 keys/administrator conversation and its alleged native audio/transcript;
- the original April 2018 complaint in which extortion-related terminology was already alleged;
- the complete DP 1132/2018 coercion/access-control source set;
- historical mailbox ZIP/archive carriers and their member-level provenance;
- the GitHub/GitLab public actor-projection discrepancy;
- future corrections whose dependencies must be automatically re-reviewed.

## Validation

Run:

```bash
python3 scripts/validate_evidence_control_plane.py
```

The validator proves the bootstrap contract is internally coherent. It does not prove corpus completeness, allegation merits, host parity, public deployment or legal conclusions.
