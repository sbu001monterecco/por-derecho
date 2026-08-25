# EVIDENCE CUSTODY AND PRESERVATION PROTOCOL

**Date:** 16 August 2026  
**Status:** controlling design decision for evidence custody / preservation.  
**Implementation status:** architecture adopted; private vault and cryptographic manifest are **not yet represented as fully implemented** unless and until native exports, hashes and custody events are actually recorded.

## Purpose

Project continuity and evidential custody are different problems.

The repository can preserve what a future ChatGPT must know, what source must be re-queried, and what a document is said to prove. That does **not** by itself guarantee durable custody of the native evidential binary if a mailbox, connected source, connector or account later becomes unavailable.

The project therefore adopts a separate evidence-preservation architecture:

`NATIVE ORIGINAL → PRIVATE EVIDENCE VAULT → HASH / MANIFEST → CHAIN OF CUSTODY → EVIDENTIAL LEDGER → PUBLIC DOSSIER / FILING / COMMUNICATION`

Never reverse this hierarchy by treating a ChatGPT summary, public page, screenshot derivative or transcription as a substitute for the native source where the original can be preserved.

## Core distinction

### 1. Institutional-memory continuity

The public-safe GitHub repository stores:

- source identifiers;
- evidential classification;
- retrieval instructions;
- provenance and limitations;
- correction history;
- missing-evidence targets;
- analytical consequence;
- publication controls;
- branch/PR/deployment state.

### 2. Evidence custody

Private/restricted evidence should be preserved outside the public repository in a controlled evidence store. Examples include:

- native `.eml` / RFC822 exports;
- original email attachments;
- native OGG/audio files;
- original photographs and screenshots;
- original PDFs and office documents;
- certified court/institutional copies;
- native registry exports;
- later forensic/provider productions.

GitHub should normally hold only the public-safe index to these items, not private or privileged binaries.

## Private evidence vault

The preferred design is a dedicated private storage location independent of any single ChatGPT thread and, where practical, independent of a single connected mailbox.

The vault should preserve originals read-only or otherwise protected from accidental modification. Never overwrite an original with a converted, redacted, translated, OCR'd, annotated or compressed version.

No claim should be made that an item is in the vault until a native copy has actually been exported/copied there and recorded.

## Stable evidence IDs

Each preserved original should receive a stable evidence ID. IDs identify custody records, not evidential truth.

A practical structure is:

`<TRACK>-<SEQUENCE>`

Examples for the elEconomista track may use `EE-001`, `EE-002`, etc., but these remain **prospective identifiers until the corresponding native item is actually preserved and entered in the manifest**.

Derivative files inherit the parent ID with an explicit suffix, for example:

- `EE-003.ORG` — untouched native OGG;
- `EE-003.WAV` — working audio conversion;
- `EE-003.TXT` — controlled transcript;
- `EE-003.AUTH` — authentication/context note;
- `EE-003.RED` — redacted publication derivative.

A derivative must never silently replace the original.

## Cryptographic manifest

For each preserved item record, at minimum:

- evidence ID;
- exact original filename;
- source system;
- source-native message/document ID;
- acquisition/export date and time;
- byte size;
- MIME/file type;
- SHA-256 hash of the preserved binary;
- whether it is ORIGINAL / DERIVATIVE / CERTIFIED COPY / WORKING COPY;
- parent evidence ID where applicable;
- custodian/storage location reference;
- confidentiality/publication class;
- evidential classification;
- brief description;
- preservation method;
- any known integrity limitation.

The hash proves binary identity with the preserved copy; it does **not** prove authorship, truth of content, legality, or authenticity of the underlying communication by itself.

## Chain-of-custody log

Every material custody operation should be recorded as an event rather than silently changing the file:

`obtained → exported → hashed → copied to vault → derivative created → transcribed → authenticated → redacted → disclosed/filed`

For each event record:

- date/time;
- actor/custodian where appropriate;
- evidence ID;
- action performed;
- source and destination;
- resulting hash if a new binary was created;
- reason;
- any exception or integrity concern.

The chain-of-custody record must distinguish **preservation** from **interpretation**.

## Evidential ladder

For every material proposition, a future reviewer should be able to answer:

1. Where is the native original or best available certified source?
2. What is its source-native identifier?
3. What is the SHA-256 of the preserved copy?
4. How and when was it obtained?
5. Is the item being reviewed an original or derivative?
6. What does it establish directly?
7. What does it not establish?
8. What authentication, corroboration or contradiction remains open?
9. Where has it been disclosed or filed, if anywhere?

## Public/private boundary

Do not put private email exports, private audio, privileged advice, tax records, unnecessary personal data, credentials or redistribution-restricted binaries into the public `por-derecho` repository solely for convenience.

The public repository should instead preserve enough information for recovery, including evidence ID, source system, native source key, custody status, evidential effect and retrieval path.

A public hash may be recorded when appropriate, but publishing a hash is not mandatory where it would create an unnecessary linkage or security/privacy concern.

## elEconomista / Javier Romera priority package

The immediate high-value preservation queue for the January-2025 elEconomista track is:

1. **17-Jan-2025 Romera email** — native `.eml` / RFC822 export with full headers.
2. **20-Jan-2025 Romera email** — native `.eml` / RFC822 export with full headers.
3. **Judicial PDF attached to the 20-Jan message** — preserve and hash separately while linking it as a child of the email evidence item.
4. **Three preserved Romera WhatsApp OGG attachments** — export native files before any conversion or transcription; hash each independently.
5. **16-Jan press-pitch email and exact attachment/version universe** — native message plus sent PDF(s).
6. **19-Jan contemporaneous memorialisation** — native message and attachments.
7. **Direct Meeting Point/Club Sei commercial sources** — preserved Meeting Point Hotels brochure, sonnenklar.TV capture and historical Sun Park address source, retaining native/source context.
8. **Complete March-2025 querella annex package** when obtained — preserve pleading separately from any primary transmission exhibit it contains.
9. **Unseen upstream Outlook message(s)** by which the judicial attachment reached Romera/elEconomista, when lawfully obtained; preserve full RFC822 headers/body/attachments.
10. **Native CAM/Acosta Matos / Meeting Point communication** capable of authenticating the January response contradiction, if recovered.

The existing evidence ledger and continuity audit already preserve Gmail IDs, Outlook/RFC822 retrieval keys, filenames and open-evidence routes. This protocol adds the custody design; it does not upgrade missing evidence into preserved evidence.

## Current elEconomista custody status

As at adoption of this protocol:

- repository continuity: **strong / deletion-safe with open evidence**;
- native source systems: Gmail/Drive/File Library remain controlling where evidence is available there;
- native private-vault export: **not to be assumed complete**;
- cryptographic manifest: **not to be assumed complete**;
- three OGGs: known/preserved through source metadata but still require native export, hashing, authentication and controlled transcription;
- upstream physical-transmission message: unresolved/not yet obtained;
- exact physical transmitter/account: unresolved.

## Implementation sequence

When custody work is activated, proceed in this order:

1. define the private vault/storage location and access boundary;
2. create a master evidence manifest template;
3. export the highest-value native evidence without transformation;
4. calculate SHA-256 immediately after export;
5. enter provenance/source-native identifiers and custody metadata;
6. create read-only/master copies and separate working derivatives;
7. log every transformation/disclosure event;
8. cross-reference the public-safe repository ledgers to stable evidence IDs;
9. periodically test recoverability of a sample from manifest → vault → hash verification;
10. back up the vault independently under an appropriate security model.

Do not describe steps 1–10 as completed merely because they are specified here.

## Relationship to thread deletion

A thread may be deletion-safe even while native evidence remains open or is stored in connected source systems, provided the repository preserves the retrieval route and evidential status.

However, deletion-safety is **not equivalent to custody resilience**. For high-value evidence, the long-term target is that loss of a ChatGPT thread, connector, mailbox session or one cloud account does not destroy the ability to produce and authenticate the preserved original.

## Fresh-thread recovery

A future ChatGPT working on evidence preservation should read:

1. `CHATGPT_START_HERE.md`;
2. `archive/THREAD_DELETION_CONTINUITY_PROTOCOL_16AUG2026.md`;
3. this protocol;
4. `archive/CONTINUOUS_MAINTENANCE_MATRIX.md`;
5. `archive/MISSING_EVIDENCE_REGISTER.md`;
6. the relevant specialist evidence ledger;
7. connected Gmail/Drive/File Library or other primary systems.

For elEconomista specifically, also read:

- `archive/ELECONOMISTA_ROMERA_MEDIA_TRACEABILITY_15AUG2026.md`;
- `archive/THREAD_DELETION_CONTINUITY_AUDIT_ELECONOMISTA_ROMERA_CAM_16AUG2026.md`;
- `archive/THREAD_DELETION_CONTINUITY_AUDIT_ELECONOMISTA_LINKEDIN_16AUG2026.md`;
- CR-020/CR-021/CR-023;
- ME-028–ME-032 and ME-049.

## Reserved-declarant private mailbox and voice corpus — 25-Aug-2026 addendum

The reserved declarant's private mailbox is represented publicly only by source alias `RDM-PRIVATE-MAILBOX-01`. A complete paginated search of the currently authorised corporate mailbox located 2,413 messages sent to or from that source alias, with 2,174 messages in 2012–2018. This is a material preservation lead and mirrored subset, not the complete private mailbox and not proof that every match is relevant.

Full acquisition requires the account holder's direct authorisation and the workflow in `archive/RESERVED_DECLARANT_PRIVATE_MAILBOX_ACQUISITION_AND_CUSTODY_PROTOCOL_25AUG2026.md`: native Takeout and/or verified-account API `RAW` export, untouched master, SHA-256 manifest, attachment recovery, label and date-range inventory, error log, cross-mailbox reconciliation, privilege review and public-safe derivatives. Never request or accept a password through chat; never alter mailbox state during acquisition; and never publish the private address, message bodies, subjects, participant list or provider identifiers.

For every voice, dictation or derived declaration, apply `archive/declarations/VOICE_TO_TEXT_STATEMENT_OF_FACT_AND_TRUTH_PROTOCOL_25AUG2026.md`. The custody manifest must link V0 native audio through V1–V4 transcript/adoption versions, preserve speaker boundaries and corrections, and record S0–S4 attribution separately from truth or corroboration. Until the native files and hashes are actually preserved, do not represent that custody step as complete.

## Controlling rule

**Repository memory tells us what evidence exists or is sought. The private custody layer must preserve the native thing itself. Neither layer substitutes for the other.**
