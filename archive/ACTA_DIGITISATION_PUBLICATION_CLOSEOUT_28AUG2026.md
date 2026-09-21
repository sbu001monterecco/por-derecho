# ACTA digitisation and publication closeout — 28 August 2026

## Publication status

This is the live-verified closeout record for the 28-Aug-2026 ACTA, meeting and communications continuity release. It supersedes the corpus counts and open-evidence status in the 27-Aug-2026 closeout without rewriting that historical record.

| Control | Value |
|---|---:|
| Initial task-base `main` SHA | `f20e86c53b1c579f8adfe01646869b91504bb11d` |
| Final integrated PR-base `main` SHA | `c456bc48dadd4dbaf5eac913b840083f1e0d9bc2` |
| Publication pull request | [#1182](https://github.com/sbu001monterecco/por-derecho/pull/1182); reviewed head `24b7f47aee83df5e2981a0505443361ddfeb99ab`; 42 required successes + 3 conditional skips; zero failures |
| Publication merge SHA | `67b144e6fd1d2312f8d4ab1830c28eb17eca8d5f`; tree `f53bdb61323bc137f1f52f1810a3bc6e70c63345` |
| Exact GitHub Pages deployment run | [33217481784 / #1253](https://github.com/sbu001monterecco/por-derecho/actions/runs/33217481784) — completed/success on the exact merge SHA |
| Live-site readback | **PASS 158/158 exact SHA-256 at `2026-08-28T22:41:05Z`; 96/96 desktop/mobile checks on the identical reviewed tree; 6/6 distinct perimeter colour pairs** |

The reviewed publication is merged, deployed and read back. Publication completion does not close the historical, annex, variant, transcription, authenticity, legal-validity or custody-resilience gaps listed below.

## Prior publication reconciliation

- PR [#1139](https://github.com/sbu001monterecco/por-derecho/pull/1139) merged at `06b8d7ac025b605ae0a677b85cb22ed0531a29c6`. Its exact Pages run `33124598726` succeeded, but six other workflow conclusions were failures. It is therefore accurate to record the ACTA Pages deployment as successful, not to describe the entire PR check set as all-green.
- PR [#1140](https://github.com/sbu001monterecco/por-derecho/pull/1140) merged at exact commit `298a1141662c278db9413d9e282469c36ca52ad8`; its exact Pages run `33125127220` completed successfully. Nine of ten checks were green and publication-integrity failed. Later repair PRs restored the relevant validation baseline. The 28-Aug candidate began from task base `f20e86c53b1c579f8adfe01646869b91504bb11d` and was integrated onto final PR base `c456bc48dadd4dbaf5eac913b840083f1e0d9bc2` (after an earlier validated integration on `8f7e002001370fc006bb019eb3078603c2a5ee4d`); neither historical merge is treated as the present candidate in isolation.
- Those historical merge/deployment facts did not by themselves satisfy the publication gate for the expanded 23-event release. That distinct gate is now closed through PR #1182, exact merge `67b144e6…`, Pages run `33217481784` and the 158/158 live readback.

## Controlled result

The publication preserves the previous 20-event/17-family corpus, adds the newly located 15-Jul-2008 17:00 CEXP meeting as a separate event and the full 10-Apr-2014 protocol 422B package as a located ACTA family, and adds two separately controlled RIC Private Equity Investment Partners (`RICPE`) event records without treating a notice as minutes. The controlled layer now contains:

- **23** controlled events;
- **46** bilingual individual event pages;
- **19** located ACTA/minutes source families plus **one** located non-ACTA RICPE notice package, for **20** controlled public source packages;
- **50** canonical source/variant records with **50** unique canonical `SP-SRC-*` identifiers: **49** are single-file records with a record-level SHA-256, while the partial typed 2014 record groups three located PNG pages with separate component hashes; eight records are related non-variant documents and do not increase the 19-family denominator, and the RICPE notice does not increase it because it is not minutes;
- **412** represented source pages;
- **20** raster-only, irreversibly redacted source facsimile PDFs;
- **412** redacted source-page JPEGs;
- **20** page-sequenced public text editions;
- **20** text-edition PDFs containing **448** pages;
- **860** current JPEG derivatives when the 412 source-page images and 448 text-edition page images are counted together; and
- **209** separately retained legacy WebP derivatives, which are not added to the current-JPEG denominator (**1,069** image derivatives across both formats).

The 19 ACTA/minutes controlling source binaries total **104,678,428 bytes**. Adding the 191,251-byte RICPE notice makes **104,869,679 bytes** across the 20 controlling public source packages. The machine controls are:

- `evidence/community/actas/public-index.json`;
- `evidence/community/actas/source-family-reconciliation-v2.json`;
- `evidence/community/actas/meeting-lineage-index-v1.json`;
- `evidence/community/actas/event-family-continuity-v1.json`;
- `evidence/community/actas/private-ocr-custody-control-v1.json`; and
- `publication-manifests/community-acta-document-room-20260823.json`.

Every located ACTA/minutes family and the separately classified RICPE notice package has a provenance record, manifest, redaction log, source-page gallery, raster-only redacted source facsimile, page-sequenced public text edition and text-edition PDF. Gap/non-ACTA status remains explicit: the 10-Jun-2016 professional working meeting is not classified as an ACTA; the standalone source for the later-recited 20-Nov-2018 meeting remains unlocated; the primary records of the 29-Dec-2021 RICPE meeting/resolution are unlocated; and the located RICPE notice proves a scheduled 11-Mar-2022 first call (12-Mar contingent second call) and agenda only, not occurrence, quorum, votes, resolutions or outcome.

## Perimeter distribution

The adverse labels below record Gil Marer's attributed theory and the project's documentary classification. They are not findings of conspiracy, fraud, criminal purpose, civil liability or guilt. Attendance, objection, receipt or later reliance does not establish who called or controlled a meeting.

| Primary lane | Count | Machine subtypes |
|---|---:|---|
| A · Montelanza pre-sale | 1 | `A` = 1 |
| B · Multimatrix/LPB → Aweswell/LPB–Gil project succession | 7 | `B` = 7 |
| C · attributed adverse sequence | 8 | `C1` AAS/FMMM/Pamanil = 5; `C2` Acosta Matos/CAM = 3 |
| D · mixed, contested or unresolved | 7 | `D-MIXED` = 5; `D-OPEN` = 2 |

`SP-ACTA-2008-07-15-CEXP` is classified `D-MIXED`: the six-page source records both Montelanza and LPB participation and an LPB representative taking the CEXP presidency. That evidence does not safely support a binary call/control attribution. The event remains separate from the 12:00 Owners' Community meeting on the same date. `SP-RECITAL-2021-12-29-RICPE` is `D-OPEN` because only a later notice recital is located; `SP-MEETING-2022-03-11-RICPE` is `D-MIXED` because the corporate RICPE notice is outside the three established project/Community lanes and does not prove that the scheduled meeting occurred.

## Newly located and newly controlled sources

The recovery batch contains **62 private custody files / 88,718,139 bytes**. That file count includes byte-identical custody copies, connector renderings and three malformed acquisition artifacts; it is not a count of 62 distinct historical instruments. The private inventory controls every file by relative custody path, size and SHA-256. Numbered items 1–34 below are the complete public-safe logical enumeration of that batch; item 35 records the later, separately controlled RICPE final-audit source.

The checksum-verified private custody archive contains **67 tar entries**, is **78,026,971 bytes**, and has SHA-256 `c7840c0108eae0114de3d151c22bc0850a69fc76a1e49139dba6f4334c89740b`. Its backing 62-file inventory has SHA-256 `5ac2669b38cccf6323aee35282b5b2dc90f9b8c05bc50dd50ab0327e00a1d58f`. The archive, inventory and private public-locator crosswalk were uploaded to and checksum-read-back from an owner-only Drive folder whose control response reports `shared=false` and owner-only permission. This is an owner-only custody/readback control, not a provider-independent second-copy or disaster-recovery finding. No Drive/file identifier or raw locator is reproduced in this public record.

### Private automated OCR custody for the three marker-only packages

The three fully withheld public packages have separate, owner-only **private automated OCR custody**. The public-safe machine control is `evidence/community/actas/private-ocr-custody-control-v1.json`; it contains no OCR text, native page image, provider identifier, private locator or storage path.

| Source package | Automated OCR coverage | Private manifest SHA-256 | Private package-inventory SHA-256 |
|---|---:|---|---|
| 15-Jul-2008 17:00 CEXP | 6/6 pages | `4dfddba414f10b93c8645086fc51c812adca43ba4440c53f49cc29de7a17225d` | `10a66cb3d8e16b08b607d445e69b136e01f7661b447892826b40b9bc4d839794` |
| 10-Apr-2014 protocol 422B | 155/155 pages | `9b844aa847a6279aa621b7edcf35040d50f0f5cf6cb92c7044c3715b60f68a5a` | `c82096c2bc8d7a5808f07b3f5c43d1d4a4ba75ce5a0adfb6d0c25a4a538f3ca3` |
| 11-Feb-2022 RICPE notice | 5/5 pages | `eca6a3ed88ec60848b422e1f0494c50455aa4781e56aca1b4faca6b6b900ba40` | `b37d3afbd0ec578bfb196511036b8e5836c638f8d7b74a8cda4d7de5c18b1098` |

All 166 rendered private page images decoded, were nonblank, retained page order and page association, and produced nonzero OCR output; there were zero zero-character OCR pages. Spanish was requested, but the controlled runtime lacked the Spanish language data and used English as a recorded fallback. These are automated quality controls only: `manual_line_by_line_verification` and `source_authenticity_established` remain `false` for all three packages.

The deterministic v2 private OCR custody archive is **40,592,332 bytes**, contains **351 entries**, and has SHA-256 `d9752bec6c53813a9f27fb18356168908b1123954fe04af9cdbcee18ebfdadcf`. A byte-for-byte repeat build reproduced that tuple. The RICPE native control, its private recovery inventory, its OCR manifest/inventory and the v2 archive were uploaded and read back under owner-only controls reported `shared=false`; the previously deposited material remains owner-only. No provider identifier, storage path or OCR text is reproduced here. This custody control does not certify wording, authenticate any source, identify an official minute-book copy or establish legal validity.

### 2008

1. **29-Apr-2008 third capture of the existing five-page instrument** — 1,085,328 bytes; SHA-256 `7c70b45a14459fdda32f9150008bd26662c051b77da8189d6f7720b20de5ab8e`; visually compared page by page with the controlling `733b0c…` copy and classified as the same instrument in a lower-quality, materially distinct capture. Its precise relationship to the separate `a0224f…` alternate capture has not been tested.
2. **15-Jul-2008 17:00–17:30 universal CEXP meeting source** — image-only PDF, 252,353 bytes, six A4 pages, SHA-256 `06b61e5c4b1a125a3412585f606a53b3bcc5dafcad840aedd6b41aa9a1ebffda`; Spanish pages 1–3 and sworn-English-translation pages 4–6. The source was visually inspected and has private automated OCR custody for all 6/6 pages under the control above. Manual line-by-line verification remains open, and the English-language OCR fallback prevents any certification claim. The translation's literal `29-Apr-1008` date is preserved as an apparent source error rather than silently corrected.

### 2014

3. **10-Apr-2014 protocol 422B package** — native PDF, 4,730,410 bytes, 155 pages, SHA-256 `12fcefd550f69462613e91aec49ac32b69cf3c2351463a751363c663f37af32b`. Internally it is an `ACTA DE PRESENCIA` for an **ordinary** Owners' Community meeting; `Extraordinario` in one carrier filename is an erroneous carrier label. Two later carrier copies are byte-identical to the controlled package. The original June-2014 Drive share now returns 404, so the later copies do not prove byte identity with the first circulation. Private automated OCR custody covers 155/155 pages; manual verification, authenticity and original-circulation identity remain open.
4. **Partial 16-Apr-2014 typed six-page version** — only pages 1, 5 and 6 are located as native PNGs: p1, 651,003 bytes / SHA-256 `8ccd619b3bdb0d7b34876ff446b678e8ba3ea8f937e379c1ae6d9a58ee636c4f`; p5, 718,590 / `a907da8eaaf64fdae3e206c96fc63d4b6c8e5c1d547a30d3afe1df6bc3d24e23`; p6, 453,547 / `cdd2cd4942fdf2df9d4d4f75374ccc342c3308a4b660f19e2d646fa53bb985f3`. The complete native version and pages 2–4 remain unlocated.
5. **122-page later email package** — 977,708 bytes; SHA-256 `6d6fc47eed3c74b66b141678ab6cdd0feec1d288177183b5facd7fafdd7d0b95`.
6. **Service/notice package A** — eight pages, 360,602 bytes; SHA-256 `1da9e5a3ec3b6d0df642a0134c4d919e19c618ae153436e19e20774394a94821`.
7. **Service/notice package B** — two pages, 321,479 bytes; SHA-256 `c378f2a4f2e2bc1c85311ab2e87e74262cf8f2cea8c80b8361fa747d8d9b16b1`.
8. **Meeting communication A** — one page, 302,059 bytes; SHA-256 `82f3b889e4a00926305c81fb80561608c75880e8ce30f620b92f2c3b652e0db8`.
9. **Meeting communication B** — one page, 300,050 bytes; SHA-256 `4bef7f5cacd9ed4b2d21bf14db754ba713637bda0952d73f20e54f5c2c2d09ac`.
10. **Separate notarial response** — six pages, 132,823 bytes; SHA-256 `80473a7499af3c1ac30763e9bdef7555d9358752e99dd6373ddabe230abe57ae`; party communication, not minutes and not a substitute for protocol 422B.
11. **Official-accounts attachment** — two pages, 557,665 bytes; SHA-256 `a8b19c17ae2f40ccb7f92916391cc585a558fa283b83ea58df271ba06534dabe`.
12. **8-Apr pre-meeting email edition** — two pages, 71,339 bytes; SHA-256 `552635920c991da2f94fe6e1877353e6dbd0e1d0b8e260b8d97e727e4c0a5a57`.
13. **Convocation A** — two pages, 58,371 bytes; SHA-256 `d756a34d6d9a2980423399c846fcd3684aae7fb2efbf9b9405593e829fb2a8f7`; a fourth custody copy is byte-identical.
14. **Recipient-specific convocation B** — two pages, 58,568 bytes; SHA-256 `b318f044efdd9a4ab269127ced5fee874637419cee857a1be1af6db9187023a1`.
15. **English translation of enclosed documents** — three pages, 47,845 bytes; SHA-256 `fc173f1f091d189a18a4d688f4ba8f9573a2ead41633a4263c7c8596b6f98743`.
16. **Recipient package, corporate A** — four pages, 3,153,094 bytes; SHA-256 `ee6615b3e48c1bf2d76d774691e8fe2914a7a044e4fb631040d7ab35a70c3342`.
17. **Recipient package, corporate B** — four pages, 2,303,858 bytes; SHA-256 `79c119850f1f6ceb09fdea278e284e3203103e697aff9b52626ed5694ed90cbd`.
18. **Recipient package, small sample** — two pages, 234,949 bytes; SHA-256 `9154877fc628489b62770bc932780f71dfa105b6daaf2ad47237a9f1b6cdcbe9`.
19. **24-Mar notice/source** — 84,845 bytes; controlled SHA-256 begins `132a8ce98…`. It asserts a 2-Feb-2012 officer-election date that conflicts with the controlled 2-Feb-2011 lineage and comes from a lawyer-origin package; its provenance, privilege boundary and factual status require review.
20. **Three incomplete acquisition artifacts** — 6,142, 57,344 and 69,632 bytes; preserved privately with their hashes and parser errors. They are rejected as complete PDFs and are not counted as located complete sources.

### 2012 and 2016 workstream

21. **10-Aug-2012 native DOCX ACTA** — three byte-identical custody copies, each 24,597 bytes, SHA-256 `b978bd03ca4a8138f9d1a704cb4717f9cbfb1a090632b6f7dbb33c25b9c4871d`; this source was already a located family but the repeated custody instances are now reconciled.
22. **10-Aug-2012 president's statement** — five pages, 345,778 bytes, SHA-256 `d9ee034878d352efdb5a5bccd63d6f4f84f9a77f840cc993741dcf9046806705`; now located both as a standalone source and within protocol 422B pages 66–70. The separate written objection remains unlocated.
23. **Ten original SPACTA camera JPEGs** used in the April-2016 notice/source chain — originals recovered and controlled by per-file hashes in the private inventory. Two first connector downloads were re-encoded; both connector renderings are preserved separately and are not substituted for the originals.
24. **Native SPACTA-007 DOCX** — two byte-identical copies, each 94,764 bytes; SHA-256 `78470bf8d35385edfc1d9dafed83b826a53240601865095faedebd5484b7ff54`.
25. **Native SPACTA-008 XLSX** — two byte-identical copies, each 186,195 bytes; SHA-256 `c55c0b9e02b4b9a127377a9e04e3cac185c43192021c6450938b1a8b829f749e`.
26. **Distinct debt-analysis workbook** — two byte-identical copies, each 151,328 bytes; SHA-256 `d023567925965ae5f4abc7fb951471f0cd9e4132f992ef4d656acfd77291dcb6`. Its four-sheet structure differs from the five-sheet SPACTA-008 workbook; it is analytical material, not proof that its calculations are correct.
27. **10-Jun-2016 AMR part 1** — 10,923,142 bytes; SHA-256 `82bac13927942b8ac738f9c53caf88b60644de7ca079fc359f0399b183c94436`; ffprobe duration 7,047.1845 seconds, approximately 117m 27.2s.
28. **10-Jun-2016 AMR part 2** — 851,270 bytes; SHA-256 `2935d00121717b3f800c975b1c9d479023ac7c808931d23a3f6c42b29b68d8e4`; ffprobe duration 549.202625 seconds, approximately 9m 9.2s.
29. **A second-named AMR custody copy** — byte-identical to part 2: 851,270 bytes and SHA-256 `2935d00121717b3f800c975b1c9d479023ac7c808931d23a3f6c42b29b68d8e4`. It is a duplicate, not a third recording part.
30. **2021 transcript derivative** — 102 pages, 1,814,598 bytes; SHA-256 `bf78d979269177df690321fc94013a0f4b6a36776441ae390c943cd87dd625d1`.
31. **2026 transcript derivative** — 149 pages, 4,075,485 bytes; SHA-256 `e9fc64f3c0ceb10296c39ba8b293e6d4cca70d27a603ff762b5090d07cf78783`.
32. **2011 and 2015 conflict-control copies** — repeated custody copies of the currently reproducible 2011 16-page binary (`299b8673…`) and the two 2015 four-page procedural extracts (`69fd5cb5…`, `e8d0636…`). They preserve, but do not resolve, the historic same-size/different-hash conflicts described below.
33. **Private visual review contact sheet** — derivative only; it is not a historical source and is not published.

The two unique AMR parts total **7,596.387125 seconds**, approximately **126m 36.4s**. That measured duration conflicts with the later 144-minute transcript label. The native filenames and same-day scheduling evidence support 10-Jun-2016; later `11JUN` derivative labels are retained as an error history. Authenticity, creation metadata, recording authority, speaker/capacity mapping, content, transcript alignment and privilege/confidentiality remain open. No audio or voice content is public.

### 2022

34. **4-Feb-2022 controlling seven-page copy** — 3,369,527 bytes; SHA-256 `bcde60e1bc42bdc6448eb28f1258894746f717a44a342927269549c06ec0666e`. The other two known seven-page binaries remain separately classified as variants; only the controlling binary was included in this recovery custody batch.
35. **11-Feb-2022-dated RICPE extraordinary-shareholders notice and agenda** — received five-page PDF, 191,251 bytes, SHA-256 `3858b928d4eee8a4f5e9b21f5452c9e58cbbfbd22debccb38bfe3dd07db303c4`, controlled as `SP-SRC-NOTICE-RICPE-2022-02-11-5P`. Two located Drive objects are byte-identical and therefore constitute duplicate custody instances, not two sources or variants. The received document attributes to the company board, through its secretary, a proposed extraordinary shareholders' meeting for 11-Mar-2022 on first call and 12-Mar-2022 on contingent second call, and recites a 29-Dec-2021 shareholders' meeting/capital-increase resolution. It proves the received notice/agenda wording and byte custody only. It does not independently prove authorship, actual issuance, service, recipient knowledge, that either meeting occurred, who attended, quorum, votes, outcome, implementation, authenticity, authority or legal validity. This final-audit source is additional to the 62-file/88,718,139-byte recovery batch described above; its native control and private recovery inventory are preserved owner-only.

## 10-Apr-2014 source map

The 155-page protocol 422B source is kept page-sequenced. The map does not turn an incorporated document into minutes or prove the truth of its contents.

| PDF pages | Source function |
|---|---|
| 1–54 | Internal notarial `ACTA DE PRESENCIA`, 28 stamped folios |
| 55 | Attendance / owner / coefficient / voting material |
| 56–57 | Notice and proxies |
| 58–63 | Objection and burofax chain |
| 64–65 | Debtor/detail material |
| 66–70 | Five-page 10-Aug-2012 president's statement — now located |
| 71–80 | Circulation/withholding material plus the four-page 10-Aug-2012 ACTA |
| 81 | Account summary |
| 82–153 | Accounting chain and owner-level/private data |
| 154 | 2014 budget |
| 155 | Simple-copy certification |

The internal record identifies LPB, represented by Gil Marer, as `convocante` in stated capacities. That supports a documented caller attribution, not lawful authority, complete service, quorum, voting entitlement, validity or implementation. Pages 1–54 plus incorporated material make the source a notarial presence package for an ordinary meeting. A filename supplied by a later carrier cannot change that internal classification.

## Variants and contradictions register

This is the complete release-level list. A hash match establishes byte identity; visual/text equivalence does not.

1. **29-Apr-2008:** controlling five-page `733b0c…`; alternate five-page `a0224f…`; newly located third capture `7c70b4…`. The third capture is the same instrument but a distinct binary/capture; its exact relation to `a0224f…` remains untested.
2. **15-Jul-2008 12:00 Community:** nine-page control `613a1e…` and partial six-page `e031e5…`.
3. **15-Jul-2008 17:00 CEXP:** separate six-page `06b61e…`, not a variant of the 12:00 Community event; its sworn translation contains the apparent `29-Apr-1008` error.
4. **25-Jul-2008:** four-page control `4939ff…` and partial three-page `a735bd…`; a prior filename carried an erroneous 2011 label.
5. **2-Feb-2011:** coherent six-page control `7c8e0d…`, alternate scan `bf85e3…`, and differently ordered six-page transmission `612a9b…`.
6. **22-Jun-2011:** control 4,549,723 bytes / `299b867…`; render-equivalent 4,551,801-byte `2e30ad…`; differently ordered/annotated `037ad9…`. A historical same-size 4,549,723-byte hash beginning `1451e2…` has not been reproduced and is not silently replaced.
7. **10-Aug-2012:** three byte-identical DOCX copies; the five-page statement and one-page proxy are related documents, not ACTA substitutes. The ACTA says no resolution was put to a vote. The statement is now located; the announced written objection is not.
8. **10-Apr-2014:** full 155-page protocol `12fcefd…`; partial 16-Apr typed version survives only as PNG pages 1, 5 and 6. The partial typed text materially conflicts on meeting times, percentages, notary role, and additional bank-signatory/administrator-hiring resolutions. Low image-correlation against all 100 scanned incorporated pages supports that it is distinct. The six-page notarial response `80473a…` is a related party communication, not minutes. Two later protocol carriers are byte-identical; the original Drive share is unavailable. `Extraordinario` in one carrier filename conflicts with the internal ordinary-meeting record.
9. **28-Aug-2014 CEXP:** `e0b9c6…` and `51d3a1…` are different PDF conversions of the same three-page instrument; a same-size/different-hash historical control conflict also remains flagged.
10. **19-Nov-2015:** clean 38-page control `d67f88…`, annotated 38-page `a9d926…`, and two four-page procedural extracts `69fd5c…` / `e8d063…` that are not treated as minutes variants. Historical hashes beginning `8d23…` and `59ff…` for the same reported sizes have not been reproduced.
11. **26-Apr-2016:** 77-page control `68ff55…` and different 77-page `549dae…` render and extract text equivalently but are not byte-identical. The 50-page `c6f7b8…`, 47-page `03d0ff…` and 24-page `d084df…` packages are partial and do not replace the controls.
12. **10-Jun-2016 professional meeting:** two unique AMR parts plus one byte-identical duplicate; measured total approximately 126m 36.4s conflicts with the later 144-minute label. Native 10-Jun filenames and contemporaneous Friday scheduling conflict with later 11-Jun derivative labels. The event remains a professional meeting, not an ACTA.
13. **7-Apr-2017 CEXP:** current two-page control `da872a…`; a historical same-size/different-hash conflict remains unresolved.
14. **18-May-2018:** nine-page control `15466a…`, second nine-page package `a90318…`, and partial eight-page variants `2a91b3…` / `ce7c1d…`.
15. **5-Jul-2018:** nine-page control `c7c31a…` and visually identical nine-page `3b718d…`; byte identity is not claimed. The one-page notice `2a31ed…` is separate.
16. **20-Nov-2018:** only a 2022 recital is located. It is not converted into a reconstructed notice, agenda, vote or ACTA.
17. **4-Feb-2022:** seven-page control `bcde60…`; visible-highlight variant `d13092…`; third known seven-page `56355a…`. Their exact material relationship remains open.
18. **RICPE 2021/2022 chain:** two located copies of the five-page 11-Feb-2022 notice are byte-identical at `3858b9…`; they are custody duplicates, not materially distinct variants. The notice later recites a 29-Dec-2021 shareholders' meeting/capital-increase resolution but is not a substitute for that meeting's primary notice, attendance, minutes or resolution. It schedules 11/12-Mar-2022 but is not evidence that the scheduled meeting occurred or produced an outcome.
19. **Cross-source date conflict:** the 24-Mar-2014 notice asserts 2-Feb-2012 for an officer election otherwise controlled at 2-Feb-2011. The contradiction is preserved and not used to rewrite the canonical event without stronger primary proof.

## Privacy and publication boundary

- Native sources remain private. No native file containing signatures, DNI/NIE, addresses, telephone numbers, email addresses, owner-level data, coefficient tables, banking material or embedded metadata is published.
- The new six-page 2008 CEXP source, all 155 pages of protocol 422B and the five-page RICPE notice use full-page precautionary raster redaction in the public derivatives. Their public text editions contain explicit page/redaction markers, not public OCR or a claim of readable or manually verified transcription. Separate private automated OCR custody covers 166/166 pages, with English-language fallback and no manual line verification or authenticity finding.
- Every public source facsimile is raster-only. Public source-page JPEGs are generated from the redacted raster layer, not copied from the native file.
- The 2014 typed PNG pages, recipient/service packages, owner/coefficient data, accounting chain and private communications remain private unless a separately reviewed redacted derivative is produced.
- The 2016 AMRs, transcript derivatives, voices and inferred speaker identities remain private.
- Provider locators and the private reverse locator map remain outside Git. Public records use opaque tokens only.
- SHA-256 establishes copy integrity for the controlled binary. It does not establish authorship, authenticity, truth, valid authority, legal effect or implementation.
- `located-package-digitised-public` does not mean `located-package-complete-public`. All 20 packages retain `complete_public_text: false` and `manual_source_line_verification: false`.

## Complete open-evidence list

1. Standalone notice, agenda, attendance/proxy/coefficient material and ACTA for the meeting later recited as 20-Nov-2018.
2. Primary notice, attendance, minutes, resolution and implementation evidence for the 29-Dec-2021 RICPE shareholders' meeting/capital-increase resolution later recited in the 11-Feb-2022 notice.
3. Evidence of occurrence or non-occurrence, attendance, quorum, voting, minutes, resolutions, circulation and implementation for the RICPE meeting scheduled for 11-Mar-2022 first call / 12-Mar-2022 contingent second call. The located notice and agenda do not answer those questions.
4. The written objection announced in the 10-Aug-2012 ACTA. The president's statement is now located and must no longer be listed as missing.
5. The complete native six-page typed 16-Apr-2014 ACTA version and its pages 2–4.
6. The original June-2014 Drive-shared binary and proof of its initial circulation/receipt; the historical share now returns 404.
7. Full procedural/notarial/court files needed to compare protocol 422B, the typed version, the interim suspension and PO 562/2014.
8. Official diligenced minute books, certified copies and original signature/native histories for every event.
9. Complete meeting notices, agendas, recipient lists, service proofs, acknowledgements and withholding chains.
10. Complete attendance records, proxies, representations, owner lists, coefficient denominators, debt status and voting-entitlement calculations.
11. Referenced or omitted annexes, presentations, statements, budgets and objections not already controlled.
12. Complete implementation chains: instructions, invoices, demands, ledgers, bank records, contracts, security/access logs, key/locksmith records, licences, tax filings and authority relied upon.
13. Audio for the 26-Apr-2016 meeting and other event audio/transcript sources not located in the finite search.
14. For the 10-Jun-2016 AMRs: authenticity, native creation metadata, recording authority, speaker/attendee/capacity map, content review, transcript alignment, privilege/confidentiality and line-by-line verification.
15. The actual 25-Jul-2023 testimony later anticipated in the professional-workstream material.
16. Complete source-level correspondence before and after every event, including direct versus indirect receipt and third-party forwarding.
17. Reconciliation of every material variant, including the unreproduced 2011, 2014, 2015 and 2017 same-size/different-hash controls.
18. Manual line-by-line OCR/transcription verification for all 20 public packages. No package is certified.
19. Source-authenticity analysis, including comparison against official originals/books and signature authority.
20. Event-by-event legal-authority, quorum, voting-entitlement, resolution-text, validity and legal-effect analysis.
21. Evidence needed to distinguish proposal from vote, vote from valid resolution, resolution from implementation, and implementation from later reliance.
22. Evidence supporting or contradicting knowledge, intent, causation, benefit and any civil or criminal characterization. None is inferred from perimeter colour or attendance alone.
23. Any historical ACTA, meeting or annex outside the finite repository/Drive/email search that has not yet been located. Absence remains `unlocated` or `open`, never proof of non-existence.
24. Corporate-capacity and relationship proof sufficient to move either RICPE event from `D-OPEN`/`D-MIXED` into a primary A/B/C perimeter; location within the wider Sun Park evidence universe is not enough.
25. Provider-independent second-copy restoration and readback for the private custody corpus; the owner-only Drive readback is not a disaster-recovery finding.
26. Exact inclusion/supersession/duplicate/omission reconciliation among the historical twenty-file SPACTA subset, the 27-August 59-file private denominator and the current 28-August 62-file recovery inventory.
27. Any separately required privacy-remediation/history-retention decision concerning prior locator exposure; the public-safe recovery neither erases history nor authorises native publication or deletion.

## Validation and deployment gate

The publication gate was closed against the exact publication commit as follows:

1. deterministic source and public-package rebuilds produce no unexplained drift;
2. all 20 manifests pass page-count, byte/hash, raster-only, privacy and non-empty-image checks;
3. all 23 events and 46 bilingual routes pass canonical, hreflang, x-default, internal-link, fragment, chronology, actor and sitemap checks;
4. all six perimeter subtypes expose a written bilingual label, short code, machine value and accessible non-colour distinction;
5. desktop and mobile render checks pass, including the new 2008 CEXP, 2014 and RICPE pages;
6. repository preservation, publication-integrity and privacy checks pass;
7. a reviewed pull request is merged only when required checks are green;
8. the exact merge SHA is matched to a successful Pages deployment; and
9. all 46 event pages, all 40 PDFs and representative images are read back from the live site.

All nine gates passed. PR #1182 merged only after 42 required checks succeeded and three conditional checks skipped; no required check failed. ACTA renderer run `33216999958` passed the 96 route/viewport checks and six distinct perimeter colour pairs on reviewed head `24b7f47…`; the reviewed head and merge share tree `f53bdb6…`. Pages run `33217481784` then deployed exact merge `67b144e…`, and deterministic live readback passed 158/158 resources.

## Live verification

PR [#1182](https://github.com/sbu001monterecco/por-derecho/pull/1182) merged reviewed head `24b7f47aee83df5e2981a0505443361ddfeb99ab` as `67b144e6fd1d2312f8d4ab1830c28eb17eca8d5f`; both resolve to tree `f53bdb61323bc137f1f52f1810a3bc6e70c63345`. Exact Pages run [33217481784 / #1253](https://github.com/sbu001monterecco/por-derecho/actions/runs/33217481784) completed successfully for that merge. At `2026-08-28T22:41:05Z`, `scripts/verify_acta_live_readback.mjs` obtained HTTP 200, nonzero expected media types and exact source SHA-256 equality for **158/158** controls: 46 event pages, two rooms, 20 text PDFs, 20 source facsimiles, 20 package manifests, 20 first text JPEGs, 20 first source JPEGs and ten global controls. The reviewed ACTA renderer passed **96/96** desktop/mobile route checks and **6/6** distinct perimeter colour pairs on the identical tree; representative Spanish live-browser inspection also rendered the deployed document room and 28-August corpus without a publication error.

## Six-part completion and deletion-safety conclusion

1. **All located control copies digitised and published:** **YES, IN PUBLIC-SAFE FORM.** All 19 located ACTA/minutes control families and the one located non-ACTA RICPE notice package are live. Native sources remain private, and all 20 packages retain `complete_public_text: false` and `manual_source_line_verification: false`.
2. **Every historical ACTA located:** **NO.** The standalone 20-Nov-2018 ACTA, the primary 29-Dec-2021 RICPE meeting/resolution records, any minutes/outcome from the scheduled 11/12-Mar-2022 RICPE meeting, and potentially other historical sources/annexes remain unlocated. The finite search cannot establish non-existence.
3. **OCR manually certified:** **NO.** All 20 packages have `manual_source_line_verification: false`. The three full-page-redacted packages expose no source OCR publicly; their separate private automated OCR custody covers 166/166 pages but uses an English-language fallback and is expressly uncertified.
4. **Source authenticity established:** **NO.** Controlled hashes establish integrity of received copies only; official books/originals, authorship, signatures, provenance and variant relationships remain partly open.
5. **Legal validity established:** **NO.** Occurrence, power to convene, notice, quorum, voting entitlement, resolution wording, validity, implementation, later reliance, knowledge, intent, causation, benefit and legal characterization remain separate questions.
6. **Continuity safe for deletion:** **YES ONLY FOR THE ORIGINATING CHAT/TRANSIENT WORK CONTEXT.** The reviewed merge, exact Pages deployment, live readback and source-controlled closeout evidence are complete. Native sources, private custody archives, locator controls, evidence records and backups are **not** authorised for deletion; provider-independent second-copy restoration remains open. `Safe for deletion` must never be restated as evidential deletion authority, historical completeness, certified OCR, authenticity, legal validity or disaster-recovery safety.

Final formulation: **“All located ACTA/minutes families and the located non-ACTA RICPE notice package are fully digitised and published in public-safe form, with remaining historical, annex, variant, transcription, authenticity, legal-validity and custody-resilience gaps explicitly preserved.”** The formulation **“all ACTAs complete”** is not supported.
