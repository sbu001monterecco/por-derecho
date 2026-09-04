# Caret Evidence Pointer and Interlinking Rule — 04 September 2026

**Control ID:** `PD-CARET-EVIDENCE-20260904-01`  
**Applies with:** `PD-EVIS-20260904-01` and the Evidence Visibility, Image/OCR, Redaction and Continuity Standard.  
**Purpose:** make the `^` mark a controlled evidential pointer across Por Derecho pages without allowing a visual cross-link to inflate the underlying proof.

## 1. Meaning of `^`

A caret immediately attached to an evidence proposition or evidence label — for example `^PD-EVIS-SP-20190606-SUNPARK264-MAIL` — means:

> **Registered evidence pointer. Open the named evidence record and apply only the evidential scope, provenance state, redaction state, limitations and source gaps recorded there.**

The caret is **not** a judicial finding, authenticity certificate beyond the recorded provenance, or shorthand for guilt, illegality, common purpose, legal authority, identity, causation, knowledge, coordination or liability.

### Existing identity-only carets

Where an existing page uses `^` solely to control a named-person identity, that legacy scope remains **identity only** unless the page explicitly links the caret to a `PD-EVIS-*` evidence record. Identity confirmation does not import conduct or responsibility.

## 2. Three mandatory layers

Every evidential proposition should be capable of resolving through three distinct layers:

1. **Narrative / event page** — explains why the item matters.
2. **Evidence register record** — states provenance, lifecycle, redaction, searchable text, visual state, relations and gaps.
3. **Native or controlled source** — the original/native source where available, or an explicitly labelled source-pending record where it is not.

No narrative page may be the sole proof of its own evidential proposition. A site page may organise or explain evidence; it cannot bootstrap itself into direct evidence.

## 3. “Establishes” versus “does not establish”

The human-readable evidence register must state both:

- **What this establishes** — the narrow proposition directly supported by the source at its current provenance level.
- **What this does not establish** — material inferences a reader might otherwise overread from the item.

The machine-readable visibility record must preserve the same boundary through source description, integrity note, limitations, redaction state, lifecycle state and open gaps.

If the native source is not recovered or hashed, the public record must say so. The absence of a native source cannot be hidden by a polished screenshot, transcription, summary or visual board.

## 4. Controlled relationship classes

Interlinking must use one of these meanings, whether encoded as page copy, data attributes, graph labels or register prose:

- **DOCUMENTED** — the source itself expressly records the linked fact/entity/event.
- **CORROBORATED** — an independent source materially confirms the same narrow proposition.
- **SEQUENCE_CONTEXT** — items are shown in chronology or operational sequence; **no causal inference is imported**.
- **INFERENTIAL** — a reasoned connection is proposed but not directly recorded by the source.
- **ATTRIBUTED_ALLEGATION** — a named party/user/source alleges the connection; it is not adopted as a repository finding.
- **OPEN_QUESTION** — a question justified by the evidence but unresolved.
- **SOURCE_GAP** — a claimed or expected source has not been recovered/verified and is excluded from the proof graph until it is.

A visual line, arrow, adjacency, common colour or common page does not upgrade the class.

## 5. Bidirectional interlinking

For every public evidence use:

- the **narrative/event page must point to the `^PD-EVIS-*` record or evidence page**; and
- the **evidence record must list every public route on which that item is materially relied upon**.

Evidence pages should also link back to the event, person, entity and proceeding pages required to understand the context.

This makes the site traversable in both directions:

**claim/event → evidence → source/provenance → related events/pages**, and  
**evidence → where it is relied upon → what is claimed from it → what remains open**.

## 6. Sequence is not causation

A chronological chain may be useful investigative context. It must be labelled **SEQUENCE_CONTEXT** unless a source independently supplies the causal bridge.

For the Sun Park control/digital-identity sequence, the following may be displayed together:

`7 June 2018 material-control event`  
→ `9 July 2018 later physical-condition record`  
→ `6 June 2019 SUN PARK Gmail communication`  
→ `Google recovery-domain display`  
→ `2021/2022 Google Business Profile ownership requests and rejection`

That presentation does **not**, by itself, establish:

- a single operator or decision-maker across the period;
- that later digital acts flowed from the 7 June 2018 event;
- that a domain linkage identifies an individual account operator;
- that a Google ownership request proves legal ownership or authority;
- that a rejected request proves unlawful intent;
- common purpose, criminality or liability.

Those propositions require separate evidence records.

## 7. Source-pending and source-gap rule

A source that has been described, remembered, indexed or depicted in a generated/composite image but whose native source is not currently recovered must be marked **SOURCE_PENDING** or **SOURCE_GAP**.

It must not be promoted to direct evidence merely because:
- a filename suggests an attribution;
- a later summary describes it;
- a generated image resembles an email or Google interface;
- an adjacent item is authentic;
- a person/entity name appears in user instructions.

When the native source is recovered, create or supersede the evidence record, preserve full headers/metadata/attachments as applicable, fingerprint the bytes and only then derive public visuals.

## 8. Images, OCR and generated visuals

Evidence visuals must be source-derived.

- Native PDF/email/page → render/crop/redact → public derivative.
- The derivative must remain traceable to the native/source record.
- OCR/transcription is searchable assistance and is not a replacement for the pixels/native bytes.
- AI-generated, reconstructed, illustrative or composited screens may be used only as **illustration**, clearly labelled as such, and must never be represented as an original email, original Google screen, original photograph or DIRECT EVIDENCE.
- If a generated exhibit contains wording not visibly present in the source, it is not a source-derived evidence image.

## 9. Privacy-minimisation rule

Public evidential value does not justify unnecessary personal exposure.

For the current Sun Park digital-identity evidence:
- blank former-customer names and email addresses;
- suppress unnecessary phone numbers;
- preserve only the minimum recovery-address information needed for the domain-level evidential point;
- honour specific user redaction instructions for former staff/client names and positions;
- preserve the unredacted/native copy separately under controlled custody.

A public derivative must state that redaction has occurred where that fact is material to understanding the exhibit.

## 10. Integrity vocabulary

Use precise labels:

- `PRESERVED_IN_REPOSITORY`
- `PRESERVED_EXTERNAL_CONNECTED_SOURCE`
- `SOURCE_PENDING`
- `SOURCE_PRESERVED`
- `TEXT_EXTRACTED`
- `IMAGE_RENDERED`
- `PUBLIC_REDACTED_DERIVATIVE`
- `REGISTERED`
- `PUBLISHED`
- `LIVE_VERIFIED`
- `SOURCE_GAP`

Do not describe a public GitHub blob as private, sealed, immutable or forensic-original merely because it has a Git SHA. Distinguish repository blob identity from a content SHA-256 and from native-source custody.

## 11. Supersession and correction

Evidence records are append-only in meaning, but may be corrected through explicit supersession:

- keep the old ID discoverable;
- record the successor/variant;
- explain the correction;
- do not silently change an evidential claim after publication;
- update all reverse links.

If a later native source contradicts a transcription or contextual inference, the native source controls and the public narrative must be corrected.

## 12. Deployment gate

A caret evidence package is ready for deployment only when:

1. every new `PD-EVIS-*` ID is unique;
2. its machine-readable record validates against the current evidence-visibility schema;
3. every public route listed in a record exists or is created in the same deployment;
4. public derivatives have completed required redaction review;
5. source gaps remain visibly labelled and are not rendered as direct evidence;
6. no generated visual is in the direct-evidence path;
7. forward and reverse interlinks are either deployed together or explicitly listed in a post-deploy handoff;
8. the branch is rebased/refreshed against `main` immediately before merge if another thread has deployed concurrently.

**Concurrent deployment rule:** preparation branches may be built in parallel, but they must not be merged based on a stale `main`. Rebase/refresh, rerun validation and inspect page conflicts immediately before integration.
