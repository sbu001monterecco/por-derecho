# Evidence Visibility, Image, OCR, Redaction and Continuity Standard

**Control ID:** `PD-EVIS-20260904-01`  
**Effective date:** 4 September 2026  
**Status:** canonical and repository-wide  
**Applies to:** every Por Derecho role, branch, workstream, evidence package, public page and continuity handoff

## 1. Purpose

Por Derecho is an evidence-visible repository, not a summary-only repository. Every evidence-bearing source must, as far as lawfully and technically possible, be preserved and represented through three coordinated layers:

1. **Native source preservation** — the original file or a custody-controlled native copy, with filename, provenance, size and cryptographic fingerprint.
2. **Searchable text** — native text extraction, transcription or OCR, plus translation where material.
3. **Visual evidence** — source-derived page images or image files that let a reader inspect the underlying record itself.

No one layer substitutes for the others. Searchable text does not replace the source image. A page image does not replace searchable text. A public derivative does not replace preservation of the native source.

## 2. Scope

This standard applies to evidence-bearing:

- PDFs, word-processing files, spreadsheets and presentations;
- emails, message threads, notifications and electronic filing receipts;
- deeds, registry records, judicial filings, orders, appeals and hearing records;
- photographs, scans, screenshots, web captures and social-media communications;
- audio/video files, their transcripts and material source-derived stills;
- annexes, exhibits, embedded images and attachments;
- public-source records used as corroboration or comparison.

It applies prospectively to every new evidence item and retrospectively through a controlled legacy backfill queue. It does not authorize publication of material that is privileged, unlawfully obtained, unsafe to expose, or subject to a justified privacy restriction.

## 3. Mandatory evidence-object triad

Each registered evidence item must declare the state of all three layers, even when one is pending.

### 3.1 Native source

The record must state:

- evidence ID and title;
- original filename and file type;
- source/custodian class and acquisition or verification date;
- repository path, connected-source reference or custody reference;
- byte size, page count or duration when known;
- SHA-256 of the preserved binary when available;
- whether the binary is the exact filed/sent/received object or only a recovered variant;
- any unresolved byte-level variants.

A filename or hash alone is not a substitute for custody or identity analysis. Same-named files with different hashes must never be silently conflated.

### 3.2 Searchable text

Every text-bearing item must have one of these explicit states:

- `PUBLISHED`
- `PARTIAL`
- `PENDING`
- `NOT_APPLICABLE`

Searchable text may be produced by native extraction, careful transcription or OCR. The method and limitations must be recorded. OCR is a reading aid, not an authenticated replacement for the visual source. Corrections to OCR must preserve an audit trail and must not silently alter source wording.

Where Spanish material is important to English readers, the repository should publish both the Spanish source text and an English translation. A translation must be labelled as a translation and linked to the source-language image/text.

### 3.3 Visual evidence

Every evidence-bearing file must declare one of these visual states:

- `PUBLISHED`
- `PARTIAL`
- `SOURCE_PENDING`
- `BLOCKED_WITH_REASON`
- `NOT_APPLICABLE`

For documents, the default is one source-derived image per page. A contact sheet, thumbnail strip or cropped excerpt may supplement but never replace the full-page images. For a standalone image, the original or public derivative is itself the visual evidence.

Visual derivatives must:

- preserve page order, orientation and enough resolution for meaningful inspection;
- retain page boundaries and avoid misleading crops;
- identify the parent evidence ID and page number;
- have their own fingerprints;
- distinguish a full page from an excerpt or highlight;
- remain linked to the searchable text and native source record.

**Synthetic, reconstructed or AI-generated imagery must never be presented as an evidence image.** Explanatory graphics are permitted only when conspicuously labelled as diagrams or illustrations and kept separate from source evidence.

## 4. Embedded images, annexes and attachments

A parent document does not exhaust the evidence object when it contains embedded evidential material.

- Embedded images and exhibits must be extracted or separately registered where they carry independent evidential meaning.
- The parent page image must still be retained to preserve context.
- Email attachments must be linked to the parent communication and separately processed under the triad.
- A filing receipt must be linked to the filing it may evidence, without claiming byte-for-byte filing identity unless established.
- A screenshot of an email or message should preserve visible sender, recipient, date/time and thread context where publication permits.

## 5. Redaction and public/private derivatives

Redaction is a controlled derivative process, not deletion.

Where full public display is inappropriate:

1. preserve the unredacted native original in the appropriate custody layer;
2. create a public derivative;
3. render visual images from the public derivative;
4. produce searchable text corresponding to the public derivative;
5. assign a distinct hash to every derivative;
6. record what category of information was redacted and why;
7. link the derivative to the original evidence ID without exposing restricted content.

Every evidence record must state:

- `redaction_status`;
- `redaction_reason`;
- `sensitivity_level`;
- `public_version_of`, where applicable;
- whether redaction was manual or automated;
- reviewer and review date when a public derivative is approved.

Permitted public treatments include masking private addresses, personal contact details, signatures, account numbers, access codes, sensitive health information, minors' data, privileged communications and irrelevant third-party data. Redaction must be as narrow as reasonably possible and must not alter evidential meaning without an express limitation note.

A black box placed over text is insufficient if hidden text remains recoverable in the file layer. Public derivatives must be technically flattened or otherwise checked against reversible redaction.

## 6. Status model

Each record must use a lifecycle status:

- `SOURCE_PENDING` — identified but no custody-controlled native source is yet available to the repository.
- `SOURCE_PRESERVED` — native source or controlled external source has been fingerprinted and registered.
- `TEXT_EXTRACTED` — searchable source text exists.
- `IMAGE_RENDERED` — source-derived visual evidence exists.
- `REDACTED_PUBLIC_DERIVATIVE` — approved public derivative and its text/images exist.
- `LINKED` — actor/entity/proceeding/event/page relations are registered.
- `LIVE_VERIFIED` — declared public routes and assets were independently read back.
- `BLOCKED_WITH_REASON` — a specific lawful or technical reason prevents completion.

A package may contain records at different stages. A package must not be called visually complete while any in-scope record remains `SOURCE_PENDING`, `PARTIAL` or `BLOCKED_WITH_REASON`.

## 7. Linkage and continuity requirements

Every record must link, where applicable, to:

- people and professional roles;
- companies, institutions and other entities;
- proceedings and procedural events;
- dates/timelines;
- allegations, counter-evidence and innocent explanations;
- source notes and translations;
- relevant public pages and Puzzle/network views;
- parent/child evidence objects and variants.

Continuity handoffs must carry:

- package ID and branch/commit;
- current lifecycle status per record;
- exact open gaps;
- next action;
- owner role;
- publication/redaction boundary;
- whether live readback has occurred.

A thread, branch or role handoff is not complete merely because a summary was written. The structured register and visual/text states must survive the handoff.

## 8. Responsibilities by repository role

### Worker

- identifies and preserves native sources;
- registers each item before relying on it;
- extracts searchable text and identifies visual/redaction requirements;
- may not mark a pending source as visually published;
- hands off exact gaps and provenance.

### Integrator

- reconciles duplicate and variant files;
- ensures triad metadata and cross-links survive integration;
- renders or imports source-derived images where the source is available;
- prevents a text-only worker delta from being treated as complete;
- keeps private originals out of public Git where required.

### Verifier

- verifies file existence, hash consistency, page/image order, OCR linkage and redaction safety;
- checks that public images correspond to the public derivative;
- performs live route and asset readback;
- reports partial or blocked states rather than inferring completion.

### Publication Coordinator

- authorizes public derivatives and route state;
- ensures visual evidence and searchable text are presented together;
- prevents unsupported claims of filing identity, completeness or legal effect;
- records the deployed commit and live verification state.

### Continuity / closeout role

- preserves the structured register, not only prose;
- carries every open visual, OCR, translation, provenance and redaction gap forward;
- does not close or delete a thread while its unique evidence state is absent from the repository.

## 9. Public presentation standard

Substantive evidence pages should provide, in a clear evidence section:

- thumbnail and full-page image access;
- source filename, date and evidence ID;
- original/public-derivative status;
- searchable text or OCR link;
- translation link where available;
- provenance and integrity note;
- redaction label where applicable;
- related actors, entities and proceedings;
- open evidential limitations.

Where visual evidence is pending, the page must say so expressly and must not display a synthetic substitute. The standard public message is:

> Evidence image pending native source materialisation. No synthetic substitute is shown.

## 10. Legacy backfill

The repository contains a large historic corpus. Adoption of this standard does not imply that every legacy file already has page images or OCR.

Legacy backfill is prioritised as follows:

1. current judicial filings, orders, notifications and receipts;
2. deeds, registry records and decisive documentary anchors;
3. emails/messages central to knowledge, notice, instruction or chronology;
4. records already cited on public pages;
5. remaining evidence packages.

Each legacy package must be registered with truthful `PENDING`, `PARTIAL` or `BLOCKED_WITH_REASON` states until complete.

## 11. Deletion and replacement safety

No source, image, OCR text or translation may be removed merely because a newer derivative exists.

Replacement requires:

- preservation of the superseded fingerprint and relationship;
- reason for replacement;
- proof that unique source content and public links remain available;
- continuity note for previously circulated URLs.

Redaction derivatives supplement the custody record; they do not erase it.

## 12. Enforcement

The machine-readable contract is:

- `.github/evidence-intelligence/schemas/evidence-visibility.schema.json`
- `.github/governance/EVIDENCE_VISIBILITY_ROLE_CONTINUITY_OVERLAY_04SEP2026.json`
- `scripts/validate_evidence_visibility.py`

Registered packages live under `data/evidence-visibility/`. The validator rejects false completeness, missing linked assets, unreasoned visual gaps and incomplete redaction metadata.

## 13. Current Uría / RICPE / HAYA rollout

The initial package is:

`data/evidence-visibility/uria-ricpe-sun-park-20260904.json`

The connected native binaries referenced in the Uría/RICPE/HAYA publication are not presently stored in the Git tree. Their hashes and searchable source notes are retained where available, and their visual states are therefore registered as `SOURCE_PENDING`. This standard does not invent page images. The next controlled step is to materialise the relevant native sources, assess redaction, render source-derived page images, link OCR/translation and verify the public routes.

## 14. Controlling rule

**Every evidence-bearing item must be preservable, searchable, visible and linkable—or must carry a precise, reviewable reason why one of those states is still pending.**
