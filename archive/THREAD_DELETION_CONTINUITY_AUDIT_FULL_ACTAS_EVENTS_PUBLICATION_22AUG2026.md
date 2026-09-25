# Thread deletion continuity audit — complete ACTAs, facsimiles and event capture

> **Superseded for current digitisation state on 27-Aug-2026:** this document records the pre-v2 failure state. Current package facts and the deletion-safety rule are controlled by `archive/ACTA_DIGITISATION_PUBLICATION_CLOSEOUT_27AUG2026.md`, `evidence/community/actas/public-index.json` and the post-publication deployment entry. The open certification/missing-source points below remain useful, but the statements that no source facsimiles existed and that the 10-Aug-2012 ACTA was unlocated are no longer current.

**Checkpoint:** 22 August 2026

**Package reconciliation:** 23 August 2026

**Live-publication reconciliation:** 23 August 2026 — PR #811 / merge `5acefbd376133ed7154d21309e4682aab94266a8`

**Repository:** `sbu001monterecco/por-derecho`

**Verdict:** **FAIL — NOT SAFE TO DELETE**

**Reason:** a bilingual document room and fifteen page-sequenced, OCR-assisted public-redacted text-edition packages are merged and live, but every package remains `located-package-partial` and the corpus is still incomplete. The packages are not complete or manually verified line-by-line transcriptions, source facsimiles, source page images, certified copies or independently preserved native masters. Variant reconciliation, all-source preservation, complete event-chain capture, complete package privacy/visual QA and the fresh-thread recovery test remain incomplete.

## 1. User objective preserved

The requested end state is:

- full substantive text of every located ACTA, published as a complete public-safe transcription rather than a digest;
- readable redacted ACTA PDFs/page images on the relevant bilingual web pages;
- all relevant notices, meetings, emails, attachments, implementation acts, challenges and downstream reliance captured and linked;
- native originals preserved with integrity metadata outside the public surface where privacy, tax secrecy, confidentiality or privilege requires it;
- the repository, website and machine-readable source/event manifests updated and verified; and
- deletion permitted only when a fresh thread can continue without the originating conversation.

The controlling implementation prompt is:

`archive/prompts/SUN_PARK_COMPLETE_ACTAS_FACSIMILES_EVENT_LEDGER_EXECUTION_PROMPT_22AUG2026.md`.

The controlling event/source inventory is:

`evidence/community/COMMUNITY_AUTHORITY_EVENTS_EMAILS_MEETINGS_ACTAS_PUBLIC_REGISTER.md`.

## 2. Current completed continuity layer

- [x] the user's requested full-ACTA/event-capture scope is now source-controlled;
- [x] stable source/event/reliance ID patterns are defined;
- [x] the newly located Drive/Gmail source variants and message IDs are recorded without publishing private addresses or bodies;
- [x] missing sources and finite-search limitations are explicit;
- [x] public/private/privilege boundaries are explicit;
- [x] `structured digest` is expressly distinguished from `complete public-safe transcription`;
- [x] a bilingual document-room interface, restricted public index and conservative missing/partial fallback chronology have been implemented locally;
- [x] `public-index.json` and fifteen per-package manifests enumerate fifteen `located-package-partial` packages, covering 179 package-source pages and yielding 209 rendered text-edition PDF pages plus 209 WEBP previews;
- [x] each package includes page-sequenced public-redacted OCR/extracted text, provenance, redaction log, manifest, rendered text-edition PDF and previews, with `complete_public_text: false`;
- [x] those PDF/WEBP derivatives are expressly labelled as text editions, not native ACTA images, source page images or source facsimiles;
- [x] every manifest records the package-source and PDF SHA-256 values and records source-page-count verification, PDF reopen and full PDF-page rendering;
- [x] the packaged 24-page 26-Apr-2016 variant remains expressly separate from, and is not presented as a substitute for, the separately recorded 77-page master;
- [x] current contradiction locks for 2011/Pamanil/Pink/keys/entity capacity are preserved; and
- [x] PR [#811](https://github.com/sbu001monterecco/por-derecho/pull/811) passed all seven applicable PR-head checks and was squash-merged as `5acefbd376133ed7154d21309e4682aab94266a8`;
- [x] GitHub Pages run [32608569055](https://github.com/sbu001monterecco/por-derecho/actions/runs/32608569055) and all seven exact-merge-SHA workflows completed successfully;
- [x] both public rooms, the public index, the representative 2011 PDF, the corrected 2011/2016 page images and the room JS/CSS were downloaded from Pages and matched repository SHA-256 values; the stale 2011 `page-018.webp` returned HTTP 404; and
- [x] this audit keeps the deletion verdict at FAIL.

## 3. Material work still incomplete

- [ ] independent native export and hash manifest for every located source/variant;
- [ ] complete native-message locator/authentication for the recovered four-page 25-Jul-2008 source family; exact source recovery for the 10-Aug-2012 and 20-Nov-2018 records; completion of the 10-Apr-2014 primary/procedural family; and a verified public package for the located 5-Jul-2018 source;
- [ ] complete source/variant reconciliation for all other ACTAs;
- [ ] manually verified, page-aligned public-safe transcriptions for every located ACTA/annex;
- [ ] source-faithful, irreversibly redacted facsimile PDFs and source page-image galleries with hidden-text tests;
- [ ] complete the ten representative visual PDF reviews still marked not completed; automated text/PDF privacy-pattern scans pass all fifteen packages, but all fifteen OCR text layers remain uncertified and none is manually source-line verified;
- [ ] source-faithful capture/linking of every notice, agenda, proxy, annex, email, meeting, implementation act, challenge and downstream reliance;
- [ ] one-to-one ES/EN ACTA pages and complete public packages for every located source family; the current bilingual room/index and fifteen partial source-language packages are not corpus completion;
- [ ] complete private/native and public machine-readable manifests, plus source-to-public-page and variant validation across the whole corpus;
- [ ] repository privacy/privilege/PII review, build, link, accessibility, PDF and visual QA;
- [ ] fresh-thread recovery test.

## 4. Exact PASS checklist

This audit may change to `PASS` only when **every** condition below is linked to evidence:

- [ ] all controlling instructions, corrections, speaker-attribution limits and current allegations from the thread are preserved in durable source-controlled records;
- [ ] the finite repository/Drive/Gmail/other-custodian search universe, queries, cut-off and negative results are recorded;
- [ ] every 2008–2022 ACTA/event has a stable ID and located-source or explicit missing-source status;
- [ ] every located native ACTA/notice/attachment is independently preserved with locator, filename, MIME, bytes, pages and SHA-256;
- [ ] every source variant is retained and reconciled;
- [ ] every located publishable ACTA/annex has a manually verified complete public-safe page-aligned transcription;
- [ ] every located publishable ACTA has a visually verified irreversible-redaction PDF and page-image gallery with hashes;
- [ ] every notice, agenda, meeting, proxy, annex, implementation communication, challenge and reliance record is linked or explicitly missing;
- [ ] private/privileged/tax-reserved source bodies remain controlled and public derivatives pass PII, hidden-text and privilege review;
- [ ] equivalent ES/EN document-room pages, relevant hubs, deep links, sitemap/search and machine-readable manifest are complete;
- [ ] corrected propositions, adverse evidence, legal-person/capacity distinctions and allegation labels are visible;
- [ ] source, repository, link, HTML/accessibility, hash, PDF-redaction and visual tests pass;
- [x] the exact reviewed diff is merged to `main` with successful required CI;
- [x] final `main` SHA, PR/merge and Pages deployment identifiers are recorded;
- [x] live readback succeeds for all changed ES/EN routes and representative public PDF/image families;
- [ ] a fresh thread reconstructs the work and next action using only durable records/source locators; and
- [ ] no material source, instruction, correction or implementation state remains only in this chat.

## 5. Deletion instruction

**Do not delete the originating thread at this checkpoint.**

A repository commit containing this audit is necessary for continuity but is not sufficient for PASS. Merge and live publication of indexes alone are also insufficient: the source-preservation, complete-transcription, redacted-facsimile, event-chain, privacy and recovery conditions above must all be proved.
