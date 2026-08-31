# Ministerio Fiscal — current-tree privacy remediation ledger

**Control date:** 31 August 2026
**Scope:** bounded current-tree remediation; no Git-history rewrite
**Status:** provider locators and unnecessary personal contact data removed from the bounded Ministerio Fiscal/calificación and communications-register surface listed below; this is not a repository-wide zero claim

## 1. Purpose and boundary

This ledger records a data-minimisation correction to the current repository tree. It does not alter the evidential propositions, official procedural references, source hashes, dates, destinations or custody boundaries of the controlled records.

The following classes are no longer reproduced exactly in the remediated current-tree files:

- mailbox-provider message identifiers;
- private file-provider object identifiers;
- exact private-mailbox subjects;
- exact private attachment or archive filenames;
- personal email addresses;
- the complainant's NIE and street notification address.

Public institutional contact details, official proceeding or registration references, source byte counts and SHA-256 values are outside this bounded removal class unless independently restricted by another control.

## 2. Public-safe replacement rule

Provider identifiers are replaced by non-provider references in the `MF-DSP-*`, `MF-DIP20-*`, `MF-EG95-*`, `MF-DI248-*`, `MF-EG19-*`, `MF-EG49-*`, `MF-CAL-*`, `MF-C36-*`, `MF-GAP-*` and `MF-AN-*` namespaces. Exact subjects and filenames are replaced by functional categories. No reverse mapping is committed to the repository.

These labels are continuity aids only. They do not prove provider delivery, receipt, incorporation, allocation, review or any institutional act beyond the proposition separately supported by the controlling native source.

### 2.1 Durable private resolution

The public references are not dangling aliases. They resolve through two access-controlled, off-Git custody records:

- `MF-PRIVATE-NATIVE-LOCATORS-20260831-V1`: 231 institutional-mail/receipt rows, SHA-256 `bdd12a8fa62b5058525e1c37053fb7899ac24a60d12ff48ab8b74bda617cd6f6`;
- `MF-CAL-PRIVATE-LOCATOR-MAP-20260831-V1`: 111 mapping rows plus header, SHA-256 `8acd4fa2290c3217a99c5ca0eb5d82c8d3e84414a45bb63939fdf5c66abc22d7`.

Both are outside Git in an access-controlled directory (`0700`) with file mode `0600`. A future authorised thread resolves:

`PUBLIC REFERENCE → THIS LEDGER / PUBLIC CONTEXT OR HASH → PRIVATE RESOLVER ROW → NATIVE MESSAGE OR DRIVE OBJECT`.

It must consult those custody records before rescanning Gmail/Drive and must not use Git history as the normal recovery mechanism.

### 2.2 Public-reference crosswalk

| Context | Stable public references | Public resolution key |
|---|---|---|
| 20-Aug nine-office dispatch | `MF-DSP-20260820-01`; `MF-DSP-20260820-02`; `MF-DSP-20260820-02-C1`; `MF-DSP-20260820-02-S1`; `MF-DSP-20260820-03`; `MF-DSP-20260820-03-C1`; `MF-DSP-20260820-03-S1`; `MF-DSP-20260820-03-T1`; `MF-DSP-20260820-04`; `MF-DSP-20260820-05`; `MF-DSP-20260820-06`; `MF-DSP-20260820-07`; `MF-DSP-20260820-08`; `MF-DSP-20260820-08-R1`; `MF-DSP-20260820-09` | dispatch date, office, direction, correction/supersession relationship and public register row |
| DIP 20/2026 | `MF-DIP20-MSG-01`; `MF-DIP20-SRC-DECR-01`; `MF-DIP20-SRC-OFF-02` | official reference plus decree SHA-256 `efd4eee1…` and notice SHA-256 `be32d01f…` |
| EG 95/2026 | `MF-EG95-MSG-IN-01`; `MF-EG95-MSG-OUT-01`; `MF-EG95-SRC-DECR-01`; `MF-EG95-SRC-ANNEX-A`; `MF-EG95-SRC-ANNEX-B` | official reference, direction/date and hashes in the canonical EG95 source manifest |
| DI 248 / EG 19 / EG 49 / Concurso 36 sources | `MF-DI248-SRC-EXP-01`; `MF-DI248-SRC-CAL-01`; `MF-DI248-SRC-ARCH-01`; `MF-EG19-SRC-DEC-01`; `MF-EG49-SRC-DEC-01`; `MF-EG49-SRC-DEC-02`; `MF-C36-SRC-PLAN-01`; `MF-C36-SRC-NONCONV-01` | official file/date plus retained hashes where available |
| Canonical calificación package | `MF-CAL-SRC-P1`; `MF-CAL-SRC-P2`; `MF-CAL-SRC-P3`; `MF-CAL-SRC-P3A`; `MF-CAL-SRC-P3B`; `MF-CAL-SRC-P4`; `MF-CAL-SRC-P5`; `MF-CAL-SRC-P6`; `MF-CAL-SRC-P6A`; `MF-CAL-SRC-P7`; `MF-CAL-SRC-P8`; `MF-CAL-SRC-P9`; `MF-CAL-SRC-JUDGMENT-01`; `MF-CAL-SRC-APPEAL-GIL-01` | P-number, actor/document role, date, page/byte controls, IdLexNet or SHA-256 where recorded |
| Calificación allegation ledgers | `MF-CAL-SRC-A01-AC`; `MF-CAL-SRC-A01-ART75`; `MF-CAL-SRC-A02-AC`; `MF-CAL-SRC-A02-OPP`; `MF-CAL-SRC-A02-JUDGMENT`; `MF-CAL-SRC-A02-APPEAL`; `MF-CAL-SRC-A03-AC`; `MF-CAL-SRC-A03-RESCISSION`; `MF-CAL-SRC-A03-EXPERT`; `MF-CAL-SRC-A03-JUDGMENT`; `MF-CAL-SRC-A03-OPP-GIL`; `MF-CAL-SRC-A03-APPEAL-PINK`; `MF-CAL-SRC-A03-APPEAL-GIL`; `MF-CAL-SRC-A04-ACCOUNTS`; `MF-CAL-SRC-A04-BDO-CORR`; `MF-CAL-SRC-A04-ANNUAL-ACCOUNTS`; `MF-CAL-SRC-A04-BDO-INTRO-PDF`; `MF-CAL-SRC-A04-BDO-INTRO-NATIVE` | allegation number, source role, document date and canonical alias; exact hashes remain where previously recorded |
| Opposition, appeal and status mail | `MF-CAL-AP-SRC-01`; `MF-CAL-AP-SRC-02`; `MF-CAL-AP-SRC-03`; `MF-CAL-OPP-SRC-LPB-01`; `MF-CAL-OPP-SRC-GIL-01`; `MF-CAL-OPP-SRC-GIL-03`; `MF-CAL-OPP-SRC-GIL-DRAFT-01`; `MF-CAL-OPP-SRC-PINK-01`; `MF-CAL-APP-SRC-GIL-01`; `MF-CAL-APP-SRC-GIL-02`; `MF-CAL-APP-SRC-PINK-01`; `MF-CAL-APP-SRC-PINK-02`; `MF-CAL-APP-SRC-SUMMARY-01` | sender role/date, RPL 2523/2025, LexNET/size and retained source hashes |
| Extraconcursal, vista and gap sources | `MF-CAL-EXT-SRC-01`; `MF-CAL-EXT-SRC-02`; `MF-CAL-EXT-SRC-03`; `MF-CAL-EXT-SRC-04`; `MF-CAL-EXT-SRC-05`; `MF-CAL-EXT-SRC-06`; `MF-CAL-VISTA-SRC-01`; `MF-CAL-VISTA-SRC-02`; `MF-CAL-VISTA-SRC-03`; `MF-CAL-VISTA-SRC-04`; `MF-CAL-FORCE-SRC-01`; `MF-CAL-FORCE-SRC-02`; `MF-CAL-FORCE-SRC-03`; `MF-GAP-SRC-GC01`; `MF-GAP-SRC-GC02`; `MF-GAP-SRC-GC03`; `MF-GAP-SRC-GC04`; `MF-GAP-SRC-GC05`; `MF-GAP-SRC-GC06`; `MF-GAP-SRC-GC07`; `MF-GAP-SRC-GC08`; `MF-GAP-SRC-GC09` | date/actor/source role plus nine retained SHA-256 and byte-count controls in the gap ledger |
| Audiencia Nacional and EG745 supporting sources | `MF-AN-SRC-DP91-01`; `MF-AN-SRC-R120-01`; `MF-AN-SRC-R120-02`; `MF-EG745-SRC-ESC-01`; `MF-EG745-SRC-HANDOVER-01` | official proceeding/reference, date and source class |

## 3. Remediated current-tree files

- `archive/FISCALIA_NINE_OFFICE_DISPATCH_REGISTER_20AUG2026.csv`
- `archive/FISCALIA_NINE_OFFICE_DISPATCH_CONTROL_20AUG2026.md`
- `archive/public_office_communications/fiscalia_tenerife/2026-01-30_DIP20/2026-01-27_30__FISCALIA_TENERIFE__DIP20_2026__CONTROLLED_RECORD_ES_EN.md`
- `archive/public_office_communications/fiscalia_tenerife/2026-08-21_EG95/2026-08-21__FISCALIA_TENERIFE__EG95__SCOPE_AND_SOURCE_MANIFEST.md`
- `archive/MF_EXTRACONCURSAL_REQUERIMIENTO_31JUL2026_FULL_TEXT_20AUG2026.md`
- `archive/THREAD_DELETION_CLOSEOUT_DP748_ICAM_CCACM_SNCA_21AUG2026.md`
- `archive/THREAD_DELETION_AUDIT_CGPJ_FISCALIA_ROUTING_20AUG2026.md`
- `archive/CGPJ_FISCALIA_ROUTING_CLOSEOUT_20AUG2026.md`
- `archive/CORRECTION_REGISTER_CGPJ_INFORMATION_DELIVERY_21AUG2026.md`
- `archive/public_office_communications/fiscalia_tenerife/2026-08-21_EG95/2026-08-21__FISCALIA_TENERIFE__INCOMING_EMAIL__CONTROLLED_TEXT.md`
- `archive/public_office_communications/fiscalia_tenerife/2026-08-21_EG95/2026-08-21__FISCALIA_TENERIFE__OUTGOING_EMAIL__CONTROLLED_TEXT.md`
- `archive/public_office_communications/fiscalia_tenerife/2026-08-21_EG95/2026-08-21__FISCALIA_TENERIFE__EG_95_2026__CONTROLLED_TRANSCRIPTION_AND_FULL_ENGLISH_TRANSLATION.md`
- `archive/public_office_communications/intervencion_general/2026-03-06_SALIDA_184368_2026_FULL_TEXT.md`
- `archive/public_office_communications/intervencion_general/2026-06-11_SALIDA_497011_2026_FULL_TEXT.md`
- `archive/CALIFICACION_FISCALIA_SOURCE_GAP_CLOSURE_ADDENDUM_16AUG2026.md`
- `archive/evidence/mf-redsara-anexo4/MF_REDSARA_UNIQUE_ATTACHMENT_INDEX.csv`
- `scripts/test_reconcile_institutional_communications.py` (actual provider locator removed from the test fixture and replaced by a clearly synthetic valid-format value)
- `scripts/build_decanato_reference24_public_evidence.py`
- `scripts/validate_fiscalia_di273_2013_publication.py`
- `scripts/validate_ricpe_saip_batch_20260824.py`
- `archive/CALIFICACION_DI248_CONTRADICTION_LEDGER_16AUG2026.md`
- `archive/CALIFICACION_EG49_FISCAL_RESPONSE_DECREE_PUBLICATION_CONTROL_16AUG2026.md`
- `archive/CALIFICACION_CANONICAL_AC_FISCAL_JUDGMENT_PERSON_MATRIX_17AUG2026.md`
- `archive/SUN_PARK_GAP_CLOSURE_SCAN_DP1132_DI248_NONCONVALIDATION_17AUG2026.md`
- `archive/CALIFICACION_ALLEGATION_01_COLLABORATION_FALSEHOOD_LEDGER_16AUG2026.md`
- `archive/CALIFICACION_ALLEGATION_02_THIRDPARTY_CEXP_CREDITS_LEDGER_16AUG2026.md`
- `archive/CALIFICACION_ALLEGATION_03_PINK_OPERATING_RENT_CAUSATION_LEDGER_16AUG2026.md`
- `archive/CALIFICACION_ALLEGATION_04_JONATHAN_CLS_BDO_SOURCE_CORRECTION_16AUG2026.md`
- `archive/CALIFICACION_APPEAL_STATUS_DAMAGE_OPENING_ALLEGATIONS_16AUG2026.md`
- `archive/CALIFICACION_AP_STATUS_SOURCE_INDEX_16AUG2026.md`
- `archive/THREAD_DELETION_CONTINUITY_AUDIT_CALIFICACION_AP_STATUS_DAMAGE_16AUG2026.md`
- `archive/CALIFICACION_OPPOSITIONS_APPEALS_FIVE_PARTY_SOURCE_CONTROL_23AUG2026.md`
- `archive/CALIFICACION_EXTRACONCURSAL_TAKEOVER_BORJA_SECURITY_SOURCE_UPGRADE_16AUG2026.md`
- `archive/CALIFICACION_UNITARY_REPOSITORY_WEBSITE_AUDIT_PROMPT_17AUG2026.md`
- `archive/CALIFICACION_VISTA_VIDEO02_03_SOURCE_CROSSREF_17AUG2026.md`
- `archive/THREAD_DELETION_CONTINUITY_AUDIT_CALIFICACION_EXTRACONCURSAL_FORCE_CUSTODY_ADDENDUM_16AUG2026.md`
- `assets/calificacion-allegation01-collaboration-audit-20260816.js`
- `archive/CALIFICACION_FISCALIA_2012_2019_2026_SOURCE_BUNDLE_RETRIEVAL_GATE_16AUG2026.md`
- `archive/THREAD_DELETION_CONTINUITY_AUDIT_CALIFICACION_EG49_DECREE_16AUG2026.md`
- `archive/CALIFICACION_AC_REPORT_RADICAL_TRANSPARENCY_LEDGER_16AUG2026.md`
- `archive/CALIFICACION_CONCURSO36_PARALLEL_LIVES_PUBLICATION_CONTROL_16AUG2026.md`
- `archive/CALIFICACION_GMAIL_DRIVE_ACTOR_KNOWLEDGE_SOURCE_ADDENDUM_17AUG2026.md`
- `archive/CAIXABANK_VALENCIA_CALIFICACION_COUNTEREVIDENCE_16AUG2026.md`
- `archive/HANDOVER_MF_FISCALIA_FIRST_FRAME_JUSTICE_MAP_15AUG2026.md`
- `archive/FISCALIA_DI273_2013_CAUSAL_ATTRIBUTION_AND_ARCHIVE_RECOVERY_CONTROL_26AUG2026.md`
- `docs/deletion-audits/2026-08-26-fiscalia-di273-2013-causal-attribution.md`
- `evidence/fiscalia/2026/FGE_INSPECCION_EG_745_2026_ANNEX_EVIDENCE_GAP_MATRIX_29AUG2026.md`
- `archive/PROCEEDINGS_MASTER_REGISTER.csv`
- `archive/MISSING_EVIDENCE_REGISTER.md`
- `archive/MISSING_EVIDENCE_REGISTER_CALIFICACION_REPEAT_SCAN_APPEND_17AUG2026.md`
- `archive/THREAD_DELETION_CONTINUITY_AUDIT_CALIFICACION_REPEAT_SOURCE_SCAN_17AUG2026.md`
- `archive/CALIFICACION_VISTA_DOCUMENT_CROSS_REFERENCE.md`
- `archive/CALIFICACION_VISTA_TESTIMONY_DIGEST.md`
- `archive/CALIFICACION_VISTA_VIDEO_02_03_INTAKE_17AUG2026.md`
- `archive/CALIFICACION_VISTA_25JUL2023_VIDEO01_EVIDENCE_INGEST_17AUG2026.md`
- `archive/CALIFICACION_VISTA_25JUL2023_THREE_VIDEO_MASTER_INDEX_17AUG2026.md`
- `archive/CALIFICACION_VISTA_SOURCE_MANIFEST.md`
- `archive/CALIFICACION_VISTA_THREE_VIDEO_PROCESSING_PROTOCOL_21AUG2026.md`
- `archive/ESPEJO_SIMO_ACCOUNTING_CALIFICACION_EVIDENCE_DOSSIER_17AUG2026.md`
- `archive/CALIFICACION_RECOVERY_AGENCY_SOURCE_REFRESH_16AUG2026.md`
- `archive/CALIFICACION_ALLEGATION_03_UNITARY_COMMUNITY_PRIVATE_ACTORS_AC_CAUSATION_16AUG2026.md`
- `archive/CALIFICACION_JAN2026_THREE_SOURCE_PROPAGATION_AND_PICKUP_16AUG2026.md`
- `archive/CALIFICACION_ALLEGATION_03_DP1132_PRIVATE_ACTOR_SOURCE_COMPLETION_16AUG2026.md`
- `archive/AWESWELL_ACCOUNTS_CALIFICACION_INCORPORATION_CONTROL_18AUG2026.md`
- `archive/SUN_PARK_NONCONVALIDATION_CALIFICACION_OLAF_PINK_CONTINUUM_FIVE_SOURCE_INGEST_17AUG2026.md`
- `archive/CALIFICACION_ALLEGATION_04_ACCOUNTING_BOOKS_SUBSTANTIAL_BREACH_LEDGER_16AUG2026.md`
- `archive/CALIFICACION_RECORDED_OPEN_EVIDENCE_INTELLIGENCE_REGISTER_17AUG2026.md`

The two Intervención General transcriptions retain the official institutional text and public-office contact block but omit the private recipient email and notification address from the current tree. Their native signed PDFs remain controlling in private custody.

The three public-output redaction/check scripts no longer embed the protected NIE, personal contact or private street-name values as raw literals. Generic identity/email type patterns and one-way SHA-256 comparison values preserve the redaction and fail-closed checks without reproducing the protected values in Git.

The independently identified DP 1901/2026 NIG transcription error was also corrected in its three current-tree occurrences. The controlling NIG is `3501643220260016977`.

### 3.1 Official-route values retained

Public institutional routing addresses remain where operationally necessary: the official Fiscalía AN, Fiscalía Tenerife and CGPJ functional mailboxes reproduced in the routing controls are institutional contact routes, not private provider locators or personal contact data. Official REGAGE identifiers, NIGs, expediente numbers, DIR3 codes and cryptographic hashes are likewise retained. An opaque value already beginning `SP-PRV-LCTR-` is a public-safe token, not a raw Gmail/Drive identifier.

## 4. Native custody and evidential continuity

Native messages, attachments and signed source documents remain under private custody. Their exact provider metadata and personal contact fields must be consulted only in the controlled private source when necessary and proportionate. The SHA-256 values retained in the repository continue to support binary identification without publishing the provider locator or private filename.

This remediation does not convert a mailbox send record into filing proof. Filing status must continue to depend on REG-AGE/RedSARA receipt evidence or another primary official registration record, applying the repository's existing filing-proof control.

## 5. Residual Git-history exposure

This is a current-tree correction only. Earlier Git commits, tags, pull-request diffs, caches, forks or existing clones may retain the superseded strings. No history rewrite, force-push, provider deletion or purge of third-party copies was authorized or performed. Accordingly, publication of the corrected tree must not be described as erasure of all historical copies.

Any later decision to rewrite history requires a separate proportionality, preservation, coordination and deployment plan because it could disrupt evidential continuity and downstream clones.

### 5.1 Bounded result and separate legacy debt

The scoped current-tree scan covers the 153 path-named Ministerio Fiscal/Fiscalía/EG/DI/DIP/REGAGE files, all MF-adjacent calificación controls implicated by this matter, the institutional-communications register/checkpoint/schema/scripts, and the three core master registers inspected here. It does not certify the whole repository provider-free.

Remaining raw locator candidates in the bounded path-name scan are outside the Ministerio Fiscal scope and are reported separately rather than silently treated as clean: historic CGPJ DI 169/alzada controls and ICALPA DIP 79/80 deletion-audit records still reproduce Gmail message/thread identifiers and private artifact labels. Wider non-MF legacy surfaces also exist in media, banking, counsel, Concurso and research controls. Those are separate remediation debt and require their own custody-safe pass.

Heuristic hits that are not exposures include: official REGAGE/NIG/expediente references; SHA-256/SHA-512 values; schema names describing prohibited fields; synthetic runtime-only test identifiers; generic words such as `Gmail` or `Drive` used to describe a finite search; repository filenames containing `GMAIL_DRIVE`; and already opaque `SP-PRV-LCTR-*` references.

## 6. Verification rule

The release gate is:

1. zero current-tree occurrence of the superseded provider locators, exact private subjects and exact private filenames identified in this remediation;
2. zero current-tree occurrence of the removed NIE, street address and personal email values in the bounded files;
3. zero occurrence of the malformed DP 1901/2026 NIG; and
4. successful repository privacy and publication-integrity validators applicable to the changed surface.

Silence, adverse outcomes, repeated contact or routing gaps remain evidentially neutral unless additional primary evidence supports a stronger proposition.
