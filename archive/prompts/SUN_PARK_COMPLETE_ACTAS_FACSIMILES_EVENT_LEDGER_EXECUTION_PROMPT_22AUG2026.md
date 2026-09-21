# Execution prompt — complete Sun Park ACTAs, facsimiles and event ledger

**Date:** 22 August 2026

**Repository:** `sbu001monterecco/por-derecho`

**Mode:** retrieve, verify, preserve, transcribe, redact, publish, test and prove; do not merely summarise

**Deletion status at prompt creation:** **FAIL — the originating thread must be retained until every PASS condition in §15 is proved**

## Mission

Create a durable bilingual document room in which every located Sun Park Owners' Community/CEXP ACTA from 2008–2022 has:

1. a stable event and source ID;
2. a privately preserved native master with integrity metadata;
3. a complete, page-aligned public-safe transcription;
4. a redacted, readable facsimile and page-image set;
5. links from the relevant ES/EN web pages;
6. its notice, agenda, attendance, proxies, annexes, implementation communications, challenges and downstream reliance recorded; and
7. explicit missing-source/status entries where completion is impossible.

Never label a structured digest, OCR fragment, later recital or party summary as `full text`.

## 0. Mandatory recovery checkpoint

Before source work:

1. inspect current `main`, branch and worktree;
2. preserve unrelated user changes;
3. read:
   - `CHATGPT_START_HERE.md`;
   - `evidence/community/COMMUNITY_AUTHORITY_EVENTS_EMAILS_MEETINGS_ACTAS_PUBLIC_REGISTER.md`;
   - `archive/SUN_PARK_COMUNIDAD_ACTAS_AUTHORITY_PROVENANCE_REGISTER_2008_2022_17AUG2026.md`;
   - `archive/SUN_PARK_COMMUNITY_PAMANIL_COMMUNICATIONS_DIGITISATION_REGISTER_22AUG2026.md`;
   - `archive/GIL_RESERVED_DECLARANT_CONTRADICTION_CLARIFICATION_REGISTER_22AUG2026.md`;
   - current `CORRECTION_REGISTER.md` and `MISSING_EVIDENCE_REGISTER.md`; and
   - `archive/THREAD_DELETION_CONTINUITY_AUDIT_FULL_ACTAS_EVENTS_PUBLICATION_22AUG2026.md`;
4. record the exact base SHA and working branch in the deletion audit;
5. keep the verdict `FAIL — NOT SAFE TO DELETE` throughout implementation.

## 1. Source hierarchy

Use this order:

1. native signed ACTA / original minute-book or certified copy;
2. native notice, agenda, proxy, attendance and annex;
3. native direct email/RFC822, registered delivery and implementation record;
4. court/administrative original;
5. later party pleading or contemporaneous analysis;
6. repository digest; and
7. ChatGPT reconstruction.

Never silently let a lower layer overrule a higher one. Record genuine conflicts as variants; do not overwrite history.

## 2. Finite source-universe protocol

Before claiming completeness, record:

- repository commit and files searched;
- connected Drive/account searched, query strings, dates and result IDs;
- connected Gmail/account searched, query strings, message/thread IDs and attachments;
- court, notarial, Community/CEXP, professional or authority files actually inspected;
- systems/accounts not accessible;
- cut-off time; and
- negative results.

`Not found in the finite searched universe` is the strongest permitted negative conclusion unless an authoritative custodian certifies non-existence.

## 3. Native preservation package

For each located source:

1. export/download the native binary without transformation;
2. save it in a controlled **private** evidence vault, not the public Git repository, unless the source is already lawfully public and privacy-reviewed;
3. record exact filename, MIME, byte size, page count, acquisition time, source locator and custodian;
4. compute SHA-256 of the native binary;
5. preserve RFC822 headers/revision history for email/Google-native material;
6. identify duplicate/near-duplicate copies by hash and visual/text comparison;
7. designate a preservation master without deleting variants; and
8. record any certification, signature or minute-book provenance separately.

Do not describe a connected Drive/Gmail object as independently preserved merely because it remains retrievable there.

## 4. Complete transcription standard

### 4.1 Interim OCR-publication state

An OCR-assisted edition may be published before full completion only when all of the following controls are enforced:

- label it **PUBLIC-REDACTED OCR TEXT EDITION — PARTIAL** in the transcript, PDF, web card and manifest;
- set `status` to `located-package-partial`, `complete_public_text` to `false` and `manual_source_line_verification` to `false`;
- keep received-source pages, public-edition pages and preview counts as distinct fields;
- identify the exact received source variant and every unreconciled variant/annex family;
- use explicit redaction and illegibility markers instead of filling gaps by inference;
- describe the rendered PDF/WEBPs as text-edition derivatives, never source images, facsimiles, originals or certified copies; and
- keep `redacted_facsimile_available` and `source_page_images_available` false until source-derived, irreversibly redacted images pass the controls in §5.

Passing automated OCR, PDF rendering, hash, link or privacy scans does not promote an interim edition to complete. Promotion requires the manual source-line and source-image gates below.

For every ACTA and annex page:

1. OCR at a quality suitable for the source language;
2. manually compare every line against the rendered page;
3. preserve page boundaries as `Page 1`, `Page 2`, etc.;
4. preserve headings, agenda items, resolutions, objections, vote arithmetic, tables and annex labels;
5. mark unreadable content as `[ILLEGIBLE — page/region]`, never guess;
6. replace protected personal material with `[REDACTED — DNI]`, `[REDACTED — SIGNATURE]`, `[REDACTED — PRIVATE ADDRESS]`, etc.;
7. maintain a private unredacted transcription keyed to the same page IDs only where lawful and access-controlled;
8. record OCR/manual-review date and reviewer; and
9. compare the final public text to the redacted source again.

The public heading must say **COMPLETE PUBLIC-SAFE TRANSCRIPTION**. It must also explain that completeness relates to substantive readable text, while protected fields are intentionally redacted.

## 5. Redacted facsimile and page-image standard

For every public-source derivative:

1. render each native page at readable resolution;
2. apply irreversible/burned-in redactions to signatures, identifiers, private contacts, bank data, owner-level protected rows and other restricted material;
3. flatten the result;
4. re-run text extraction/OCR to confirm hidden redacted text cannot be recovered;
5. inspect every page visually for cropping, overlays, rotated pages, missing annexes and accidental disclosure;
6. compute SHA-256 for the public redacted PDF and page-image set;
7. keep native and public hashes explicitly distinct; and
8. provide a download link to the redacted PDF plus an accessible page gallery.

Do not publish source-original image/PDF files merely because the user requested images. Privacy and privilege review controls publication form, not whether the underlying source is indexed.

## 6. ACTA X-ray and event-chain schema

Each ACTA/event page and backend record must include:

- stable `SP-EVT-*` and `SP-SRC-*` IDs;
- exact date, body and meeting type;
- convenor and claimed authority;
- notice method/date and delivery evidence;
- agenda;
- attendees, proxies and represented coefficient, publicly aggregated where necessary;
- excluded voters and the stated basis, without publishing private owner rows;
- voting denominator and source arithmetic;
- each resolution separately;
- objections/reservations;
- signatories/certification chain;
- every annex;
- debt/accounting/exploitation basis relied on;
- implementation email, burofax, contract, invoice, security/access or institutional record;
- challenge, appeal and outcome;
- downstream recipient and whether transmission/reliance is verified, inferred, alleged or unproved;
- adverse evidence and competing version; and
- precise missing completion.

## 7. Required ACTA/source queue

Process every row in the ledger's complete-publication matrix, including:

- 29-Apr, the distinct 15-Jul variants, the recovered 25-Jul source family and 17-Dec 2008;
- 28-May-2009;
- 2-Feb and 22-Jun-2011;
- 10-Aug-2012 or any correctly dated precursor/original;
- 10-Apr and both separate 28-Aug-2014 records;
- all 19-Nov-2015 variants;
- the complete 77-page 26-Apr-2016 source/annex corpus, preserving both distinct render/text-equivalent 77-page binaries and distinguishing them from the 24-, 47- and 50-page partial packages;
- 7-Apr and 12-Jun-2017;
- 18-May and 5-Jul-2018 plus the referenced 20-Nov-2018 source;
- negative search for 2019–2021; and
- 4-Feb-2022.

If a source is missing, publish a clearly labelled missing-source card with searches performed and the finite records needed. Do not fabricate a transcription or silently omit the event.

## 8. Communications, meetings and implementation queue

Digitise and link, subject to privacy/privilege review:

- historic ACTA transmission to Garrigues (15-Mar-2012);
- 2012 Community statement/circulation and the referenced 10-Aug meeting;
- 2014 Pamanil email/notarial response and competing governance chain;
- November-2015 debt/convocation/reply/ACTA chain;
- April-2016 PwC transmission, convocation images/package, records request and AC-authority communication;
- 10–11-Jun-2016 analytical files, the 11-Jun recorded working meeting and 22-Jun scheduling thread;
- 2017 Pamalexsha agreements and ACTA circulation;
- 2018 ACTA circulation and security/access/DP1132 implementation; and
- May-2022 transmission of 2016/2022 ACTAs.

For private or potentially privileged communications, publish only public-safe metadata and a narrow evidential consequence unless deliberate privilege review authorises more. Preserve native bodies and headers privately.

## 9. Legal/entity and allegation controls

Never collapse:

- Owners' Community;
- CEXP;
- LPB;
- Monterecco/Pink;
- Pamanil/Pamalexsha;
- the insolvency estate/AC;
- CAM/HNT/later operator; or
- individual owners, officers, representatives and advisers.

Preserve these corrections:

- 2-Feb and 22-Jun-2011 are separate events;
- `Pamanil did nothing` is superseded as a literal statement, while actual integrated maintenance remains unproved;
- Gil's allegation of fraudulent/economic-crime use is a party allegation requiring actor-by-actor proof;
- Gil's total-nullity *ab initio* Pink-contract position is unadjudicated and must be shown with own-unit, severability, factual-operation, restitution, preclusion and adverse-decision counterarguments;
- physical keys, CEXP maintenance/master keys, custody, possession and legal authority are distinct;
- a meeting/ACTA filename is not its legal effect;
- an adverse procedural result is episode-specific and must remain visible; and
- transmission of an ACTA does not prove institutional adoption or lawful authority.

## 10. Bilingual public information architecture

Keep stable routes and create one-to-one ES/EN equivalents.

Minimum structure:

1. Community hub;
2. 2008–2022 chronology;
3. document-room index;
4. one ACTA page per stable event/source family;
5. one communications/meetings index;
6. one downstream-reliance register; and
7. one missing-source and correction register.

Every ACTA page must expose:

- a public-safe full-text HTML transcription;
- redacted PDF download;
- accessible page-image gallery;
- source/integrity panel;
- X-ray/event-chain fields;
- allegations/adverse evidence/open questions; and
- links to the previous/next event and the exact EN/ES counterpart.

Update navigation, sitemap, site search/index, `CHATGPT_START_HERE.md`, machine-readable manifests and all relevant hub/deep links. Avoid a JavaScript-only content layer when evidence text should be indexable and linkable.

## 11. Event and attachment machine-readable manifest

The public document-room contract is `evidence/community/actas/public-index.json`. Treat it as a generated/maintained public index derived from the canonical register, not as evidence and not as the private native-source manifest. Keep it free of private source locators, privileged bodies and restricted attachment URLs. The package/document-room implementation is responsible for creating and validating it.

The public index must expose, at minimum:

`id, slug, date, body, meeting_type, status, title_es, title_en, notes_es, notes_en, complete_public_text, manual_source_line_verification, source_variant_page_count, public_pdf_page_count, preview_count, transcript_path, provenance_path, redaction_log_path, manifest_path, public_pdf_path, public_pdf_sha256, preview_pages, artifact_kind, redacted_facsimile_available, source_page_images_available, privacy_level, limitations`.

Never include private Drive/Gmail locators, native private filenames, personal contact data, privileged message bodies or restricted attachment URLs in the public index.

Maintain a separate access-controlled private/native manifest with:

`event_id, source_id, date, body, type, native_locator_private, native_filename, native_sha256, native_bytes, pages, variant_of, public_transcript_url_es, public_transcript_url_en, public_pdf_url, public_pdf_sha256, page_gallery_url, notice_ids, annex_ids, communication_ids, implementation_ids, challenge_ids, reliance_ids, evidence_status, publication_status, privilege_status, pii_review, source_reviewed_at, open_items`.

The public `public-index.json` contract uses the restricted fields specified in the canonical register: stable `id`, date/body/status, bilingual title/notes, strict completion boolean, public transcript/PDF/page-image/integrity links and correctly identified public hash data only.

Validate that every web source card maps to exactly one manifest row and every manifest URL resolves.

## 12. Privacy, privilege and legal review gate

Before public commit:

- scan text, PDFs, images, metadata and OCR layers for personal identifiers and restricted fields;
- verify that redaction is irreversible;
- withhold private owner balances and payment rows;
- withhold tax-reserved material;
- withhold raw audio and unverified speaker labels;
- apply privilege/confidentiality review to Garrigues, PwC, lawyer/client and litigation-strategy material;
- distinguish allegations from findings in ES and EN; and
- record the reviewer and decision.

If the full source cannot safely be published, publish a complete public-safe transcription with explicit redaction markers and a correspondingly redacted facsimile. If privilege prevents even that, retain only the public-safe metadata/index and explain the restriction.

## 13. Validation

Run, record and require success for:

- source-to-transcription page count and page-heading parity;
- manual line comparison completion;
- OCR confidence/unreadable-region log;
- PII/identifier/signature/private-contact scan across repository text and built site;
- PDF hidden-text/redaction extraction test;
- image visual review;
- hash manifest validation;
- all internal/download/image/alternate-language links;
- HTML validity, accessibility, responsive layout and print view;
- site build/test suite;
- git diff/no-unrelated-change review;
- public repository readback after merge; and
- live GitHub Pages readback of every new/changed route and representative PDF/image.

Do not equate a successful local build with public availability.

## 14. Publication and evidence proof

1. commit only the intended files;
2. push an auditable branch;
3. open a PR with source/privacy/completion table;
4. inspect the exact PR diff;
5. require checks to pass;
6. merge only the reviewed result;
7. re-read the final `main` SHA;
8. verify GitHub Pages deployment/checkpoint;
9. fetch every live ES/EN page and public derivative; and
10. update the deletion audit with immutable commit/PR/deployment identifiers.

## 15. Exact deletion PASS checklist

The originating thread remains **FAIL — NOT SAFE TO DELETE** until every box is evidenced:

- [ ] all controlling instructions, corrections, speaker-attribution limits and current allegations from the thread are preserved in durable source-controlled records;
- [ ] the finite repository/Drive/Gmail/other-custodian search universe, queries, cut-off and negative results are recorded;
- [ ] every 2008–2022 ACTA/event in the canonical ledger has a stable ID and a located-source or explicit missing-source status;
- [ ] every located native ACTA/notice/attachment has been independently preserved with complete locator, filename, MIME, bytes, pages and SHA-256;
- [ ] all variants/duplicates are retained and reconciled; no source was silently overwritten;
- [ ] every located publishable ACTA and annex has a manually verified complete public-safe transcription with page alignment and explicit redaction/illegibility markers;
- [ ] every located publishable ACTA has a visually verified, irreversibly redacted PDF and page-image gallery, with public derivative hashes;
- [ ] notices, agendas, meetings, proxies, annexes, implementation emails/burofaxes, challenges and downstream reliance are linked or explicitly marked missing;
- [ ] private/privileged/tax-reserved materials remain controlled and the public repository/build passes identifier, hidden-text and privilege review;
- [ ] ES and EN document-room pages, relevant hubs, deep links, sitemap/search and machine-readable manifest are complete and equivalent;
- [ ] allegations, adverse evidence, legal-person distinctions and corrected propositions are visible on the relevant pages;
- [ ] repository tests, link checks, HTML/accessibility checks, hash validation, PDF redaction tests and visual QA pass;
- [ ] the exact intended diff is committed, reviewed, merged to `main` and all required CI checks succeed;
- [ ] the final `main` SHA, PR/merge identifiers and GitHub Pages deployment are recorded;
- [ ] live public readback succeeds for every new/changed ES/EN page and a representative set of every public PDF/image family;
- [ ] a fresh-thread recovery test, using only repository records and preserved source locators, reconstructs the task, status, corrections, remaining gaps and next action without relying on chat memory; and
- [ ] the deletion audit is changed from `FAIL` to `PASS` only after all preceding evidence links are present.

Open evidentiary questions may remain after PASS, but no unrecorded source, instruction, correction, implementation state or recovery dependency may remain only in the chat.
