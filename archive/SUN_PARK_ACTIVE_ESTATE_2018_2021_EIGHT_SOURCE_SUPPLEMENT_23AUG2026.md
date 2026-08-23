# SUN PARK ACTIVE ESTATE 2018–2021 — EIGHT-SOURCE SUPPLEMENT AND 18-SOURCE DIGITISATION CONTROL

**Date:** 23 August 2026  
**Status:** PUBLIC-SAFE REPOSITORY CONTROL — NO PRIVATE SOURCE BINARIES ADDED  
**Namespace:** `ME-PDFSCAN-*`

## 1. Purpose and boundary

This supplement reconciles the eight later PDFs and revalidates their relationship to the first ten PDFs supplied for the JV 1260/2011, DP 1132/2018, DI 248/2018, Concurso 36/2012 and 2019–2021 active-estate/access source families. It records duplicate control, digitisation priority, public-presentation treatment and finite requests for the missing source material identified inside the PDFs and in connected repository threads.

An `OPEN` or `PARTIAL` request means only that the identified source has not been fully located and authenticated in the controlled corpus. It is not evidence that the source does not exist or that any person acted unlawfully.

This register does not authorise publication of private originals, unredacted personal data, privileged material or unverified accusations. Preserve originals outside public Git; place only public-safe derivatives in the repository after redaction and source review.

## 2. Corpus reconciliation

The eighteen uploaded files represent **seventeen unique binaries and sixteen documentary items**:

- the first ten binaries already match the hashes controlled in `SUN_PARK_2011_2019_OPERATOR_CONTROL_DP1132_DI248_NONCONVALIDATION_TEN_SOURCE_SUPPLEMENT_17AUG2026.md`;
- five later binaries already match `MAT-005`–`MAT-009` in `MATKATOR_DP552_EVIDENCE_CUSTODY_LEDGER_16AUG2026.md`;
- one later CAM PDF is an alternate print/facsimile of the same pleading controlled as `MAT-007`, not a new pleading; and
- the two 18-page photographic PDFs are byte-for-byte identical and must be counted once.

Do not re-ingest any exact duplicate as new evidence. Retain a filename/alias record pointing to the canonical evidence item.

### Newly reconciled binaries

| Control | Neutral description | SHA-256 | Pages | Repository treatment |
|---|---|---|---:|---|
| `MAT-005` | 12-May-2020 Auto resolving LPB's reposición against the 24-Oct-2019 Auto | `2caa1492433a74c603efedf9662ca1057eda863cadb81474cf05a8b7a5cfbbfa` | 2 | Existing preservation row; add public-safe full text and source card, not a duplicate binary. |
| `MAT-006` | 18-Dec-2020 Aweswell request concerning conservation and inspection of the active estate; signed 21-Dec | `8ab76545ff263d4226cff7f363ddab6daea354abde932d1ed63d920bdc9037da` | 4 | Existing preservation row; party pleading with missing annex. |
| `MAT-007` | CAM opposition dated 16-Feb-2021 and visibly signed 17-Feb | `de45a090b2ffeccb7a7308cd08e1f75c8418fde3617949b2b3774697bde9742b` | 4 | Existing preservation row; party counter-position with missing annex. |
| `MAT-008` | 24-Feb-2021 Auto resolving Aweswell's reposición | `3b02a944ae5becb154bdc2109935d060de80bb9e862f10ab055582696e5ee40f` | 4 | Existing preservation row; add public-safe full text and source card. |
| `MAT-009` | Printed 23-Feb/8-Mar-2021 expert-access email thread | `e542e8fddcc7f0a78782012c5f07221b9c735cb81b479d6dcac7d77819d02201` | 3 | Existing rendered-PDF preservation row; native email and attachment remain open. |
| `MAT-007-ALT-01` | Later print/facsimile of the `MAT-007` CAM opposition | `0df34c778e634c2abcfccfd88eee6b41ad687a23694705a8cc44d613ebd09540` | 4 | Preserve as a source variant; do not create a second website source card. |
| `SP18-PHOTO-01` | Later-compiled photographic sequence attributed by its cover to an alleged 1-Mar-2018 access event | `e66d1c78166595c9f3899063fdf39767339d608d4184f93cd10993f11e051abc` | 18 | One canonical copy only; underlying photographs, metadata, identities and event context remain open. |

### Mandatory filename corrections

- Editorial filename labels such as `DeudaFalsa`, `Destruccion Masa` or `Entrada ilegal` are not judicial findings and must not become repository titles.
- The CAM opposition is an `impugnación`, not a CAM recurso. Its body is dated 16 February and its visible signatures 17 February 2021; the filename's 15-Feb date does not control.
- The 24-Feb-2021 Auto refers once to 23 October 2019 while the surrounding source chain identifies the earlier Auto as 24 October 2019. Preserve the discrepancy until the signed anchor source is checked.
- The 1-Mar-2018 photographic PDF's filename identifies an additional person who is not named inside the PDF. Do not infer identity from the filename.

## 3. Digitisation decision

Digitise every unique documentary item, but separate preservation, repository searchability and website publication:

1. **Preservation master:** exact private binary, original filename, byte size, SHA-256, acquisition and variant/duplicate links. Never overwrite it.
2. **Search derivative:** neutral canonical alias; page-faithful UTF-8 transcription with page markers; OCR only where needed; `[illegible]`/`[redacted]` controls; no silent correction of dates or names.
3. **Public derivative:** redacted PDF or page images when the evidential value exceeds privacy, privilege and mischaracterisation risk.
4. **Source card:** date, author/organ, procedural role, what the document establishes, what it does not establish, missing annexes, hash and links to related positions/outcome.
5. **Bilingual presentation:** Spanish source record controls; English page summarises without creating a second evidential meaning.

Recommended repository destination for this sequence:

`evidence/insolvency-36-2012/masa-activa-2019-2021/`

with `full-text/`, `public-pdfs/`, `index.md` and `provenance.md`, following the existing `concurso-autos` pattern.

## 4. Website selection

Create one balanced bilingual dossier: **“Estado y conservación de la masa activa, 2019–2021 / Condition and preservation of the active estate, 2019–2021.”**

| Source class | Website treatment |
|---|---|
| Signed court/Fiscalía acts | Full redacted PDF plus full page-cited transcript and a prominent `decided / not decided` box. |
| Opposing party pleadings | Source cards and full redacted repository transcripts; display the opposing pleading and resulting order in the same sequence. Do not present an allegation-only PDF as proof. |
| Complaint bundles / mixed LexNET packets | Component-level cards only after separating complaint, receipt, opposition and official outcome. |
| Email | Preserve fully; publish only a redacted notice/request chronology or short extracts unless privilege/confidentiality review authorises more. |
| Photographic packet | Do not publish the accusatory cover as fact. At most use a small face-blurred, neutrally captioned gallery after originals/metadata and identity review. |
| Exact duplicate or facsimile variant | No separate public item; show one canonical source record with variant hashes. |

The 2019–2021 dossier should be ordered as follows:

1. signed 24-Oct-2019 non-convalidation Auto (missing anchor);
2. 12-May-2020 Auto;
3. 18-Dec-2020 Aweswell application;
4. Aweswell reposición and 13-Jan-2021 Providencia (missing);
5. CAM and AC counter-positions with annexes (partly missing);
6. 24-Feb-2021 Auto;
7. 23-Feb/8-Mar-2021 expert-access email and documented outcome (native/outcome incomplete); and
8. matrix: `party assertion | counter-position | court observation | holding | unresolved source`.

## 5. Finite scan and native-file requests

Existing general requests remain active, especially `ME-001`, `ME-003`, `ME-005`–`ME-008`, `ME-011`–`ME-012`, `ME-020`, `ME-041`–`ME-050`, `ME-055`, `ME-058`, `ME-061` and `ME-CAM7J-001`–`ME-CAM7J-014`. The entries below narrow this eighteen-file corpus without superseding those controls.

| ID | Exact production / scan request | Why needed | Cross-reference | Status |
|---|---|---|---|---|
| `ME-PDFSCAN-001` | Signed complete Auto of 24-Oct-2019, metadata/authentication page, service record and any correction resolving the 23/24-Oct discrepancy. | Anchor for non-convalidation and every later reference. | `ME-012`, `ME-061` | OPEN |
| `ME-PDFSCAN-002` | LPB's complete 4-Nov-2019 reposición, filing/service proof and its `bloques documentales 1–2`. | The 12-May-2020 Auto did not decide the new demolition/access requests on their merits. | `ME-012` | OPEN |
| `ME-PDFSCAN-003` | Full AP Las Palmas Auto of 23-Jul-2019, finality certificate and exact calculation record used for the third-bidder improvement condition. | Controls the res-judicata and interest proposition. | `ME-011`, `ME-012` | OPEN |
| `ME-PDFSCAN-004` | Interest certificate, Community-debt certificate, all party submissions and the later signed order definitively fixing amounts required from a third bidder. | Prevents a provisional/framework amount being described as a final debt or price. | `ME-011` | OPEN |
| `ME-PDFSCAN-005` | Aweswell's missing `DOCUMENTO Nº1`, the earlier `bloques documentales`, and every native before/after photograph with filename, hash and EXIF. | Tests ownership, location, date, condition, authorship and alleged damage. | `ME-041`, `ME-048`, `ME-050` | OPEN |
| `ME-PDFSCAN-006` | Providencia 13-Jan-2021; Aweswell filings/receipts 654 and 690/2021; complete reposición; LAJ/DIOR 4-Feb-2021; service and deposit records. | Reconstructs what relief was requested and exactly what the 24-Feb Auto reviewed. | `ME-012` | OPEN |
| `ME-PDFSCAN-007` | AC's complete opposition/filing, certificates dated 15-Jan-2019 and 9-Feb-2021, underlying information requests/replies and every relevant quarterly report. | Tests AC knowledge, preservation activity and the positions quoted by the court. | `ME-006`, `ME-007`, `ME-011`, `ME-CAM7J-006` | OPEN |
| `ME-PDFSCAN-008` | CAM's missing `DOCUMENTO NÚMERO UNO`: Community certification and underlying notices, minutes, attendance, title/proxy, votes, security contract, instructions, logs, invoices and payment trail. | Tests the asserted Community authority and access/security chain. | `ME-044`, `ME-046`, `ME-CAM7J-003`–`004` | OPEN |
| `ME-PDFSCAN-009` | Certified deed/Registry schedule showing the exact CAM units owned at each material date; claimed municipal licence, applicant, approved plans, unit list, conditions, inspections, contractor invoices and works diary. | Tests CAM's 54-unit and licensed-own-units counter-position. | `ME-CAM7J-002`, `ME-CAM7J-010` | OPEN |
| `ME-PDFSCAN-010` | Independent finca-by-finca overlay for 8,508–8,536, 8,653, 8,654, the LPB perimeter, common areas and third-party units, mapped to every photograph and work. | The court could not identify ownership of photographed interiors. | `ME-012`, `ME-039`, `ME-058` | OPEN |
| `ME-PDFSCAN-011` | Access/key/security request-and-response ledger for LPB, Aweswell, experts and notary, including every authority, refusal, guard log and inspection record. | Determines whether and why neutral inspection was enabled or prevented. | `ME-046`, `ME-050`, `ME-CAM7J-004`, `ME-CAM7J-006` | OPEN |
| `ME-PDFSCAN-012` | Native RFC822/Google Takeout export of the complete 23-Feb/8-Mar-2021 thread, full headers/MIME, attachment manifest and original photographic report; later replies, written authority/refusal, videoconference notes, expert/notarial report, instructions, invoices and access outcome. | Authenticates notice and closes the request→response→outcome chain. | `MAT-009`, `ME-006`, `ME-050` | PARTIAL — rendered PDF only |
| `ME-PDFSCAN-013` | 2-Feb-2021 Registro Público Concursal publication, direct-sale authorisation, improved offer, auction file, bidder access/due diligence, valuation and final signed treatment. | Tests the reasoning that the bidder accepted the asset's condition. | `ME-008`, `ME-011`, `ME-012` | OPEN |
| `ME-PDFSCAN-014` | Any later appeal preservation or responsibility action against CAM/AC; implementation after non-convalidation, deed/Registry rectification, possession, inventory, remediation and complete EUR 400,000 accounting. | Tests whether the issue was corrected, litigated or economically reconciled. | `ME-008`, `ME-011`, `ME-020`, `ME-050`, `ME-CAM7J-008`, `ME-CAM7J-013` | OPEN |
| `ME-PDFSCAN-015` | Exact filed/native version of the 1-Mar-2018 photo annex; all 50 underlying photographs/video with EXIF; photographer/compiler statement; identity proof; door condition; witnesses; access/security/police/notarial records; filing receipt and official treatment. | The later compilation and its filename do not prove date, identity, force, authority or legal character. | `ME-042`, `ME-045`, `JDAM_JOAN_CRUZ_SUN_PARK_ACCESS_EVIDENCE_NODE_19AUG2026.md` | PARTIAL — compiled derivative located |
| `ME-PDFSCAN-016` | Filing-stamped/certified source for the CAM opposition, LexNET receipt, annex inventory and cryptographic verification; reconcile `MAT-007` with alternate facsimile `MAT-007-ALT-01`. | Preserves variant provenance without double-counting the pleading. | `MAT-007`, `ME-007` | PARTIAL — two derivatives located |
| `ME-PDFSCAN-017` | Complete JV 1260/2011 court file: demand annexes, admission/service, 23-Feb-2012 extension annexes and admission order, defence, hearing/audio, evidence, first-instance judgment, AP 89/2014, finality and enforcement/outcome. | Closes the procedural-equivalence and result questions; party pleadings alone do not. | `ME-047` | PARTIAL |
| `ME-PDFSCAN-018` | Complete 2014 Fiscalía complaint package: all exhibits represented only by cover sheets, filing receipt, Fiscalía 39/2014 investigation and archive/outcome, plus DP 332/2014 transmission/use. | The current PDF contains complaint text and exhibit covers, not the exhibits or outcome. | `ME-002`, `ME-003` | PARTIAL |
| `ME-PDFSCAN-019` | Complete native DI 248/2018 file: complaint/expansions, receipts, ordered and performed diligences, statements, expert/supporting material, 7-May-2019 decree, service and any Article 773 LECrim judicial refiling/outcome. | Prevents an investigative archive from being treated as acquittal or a judicial merits decision. | `ME-001` | PARTIAL |
| `ME-PDFSCAN-020` | Complete 2019 non-convalidation/AC sequence: original 7-May judicial decree quoted by the parties, AC filing 1760/19, 13-May Aweswell/LPB responses, ratification/decision, service, appeals and implementation. | Party quotations do not replace the official act or later treatment. | `ME-005`–`ME-008`, `ME-012`, `ME-020` | PARTIAL |
| `ME-PDFSCAN-021` | Reconcile the one-page 2-May-2018 order fragment in the earlier ten-file set with the complete signed DP 1132 opening/severance order and certified docket. | A fragment without the operative part must not control the order's meaning. | `ME-045`, `MAT-010`, `ME-CAM7J-009` | PARTIAL |
| `ME-PDFSCAN-022` | Component-level originals for the mixed 1-Aug-2018 bundle: court act, each LexNET receipt, each opposition/party filing, exhibits, service and resulting signed decision. | A mixed packet is neither one complaint nor one merits ruling. | `ME-045` | PARTIAL |

## 6. Scan / export specification for every thread

When a gap is pursued in email, Drive, Library, counsel files, devices or another ChatGPT thread:

1. Prefer the **native source** (`.eml`, original image/video, office file, signed electronic PDF, native spreadsheet) over a screenshot or print.
2. If paper is the only source, scan every page—including backs, covers, envelopes, stamps and blank separator pages—in colour at 300–400 dpi without cropping, enhancement or recompression.
3. Export email with full RFC822 headers, MIME structure and every attachment as a separate original file; do not treat a Gmail print view as the native email.
4. Export messaging threads with account/participant identifiers, timestamps, timezone, attachments and platform metadata, subject to privacy review.
5. Hash each source immediately; record filename, bytes, SHA-256, acquisition route, date, custodian and parent/variant/duplicate relationship.
6. Keep a negative-search log: repository terms, exact filenames, dates, senders/recipients, proceeding numbers, Drive/Gmail queries, folders/accounts reviewed and OCR limitations.
7. Do not turn a filename, party allegation, receipt, opening act, archive decision or later commercial result into a merits finding.

## 7. Public redaction gate

Before public release, remove unnecessary personal email addresses, telephone numbers, private addresses, DNI/NIE/NIF values, electronic verification codes, signatures, access tokens and unrelated third-party identities. Keep the court/organ, proceeding, corporate parties, judicial author and materially necessary professional roles where source attribution requires them.

Any proposed publication of lawyer correspondence, private email, witness material or faces requires a separate privilege/confidentiality, privacy, safety and source-necessity review.

## 8. Next implementation gate

Repository search derivatives and source cards may be prepared immediately. Public raw-PDF links, face images and the final page architecture require an explicit editorial decision. No claim should be made that a GitHub change is live until the deployed URL is checked independently.
