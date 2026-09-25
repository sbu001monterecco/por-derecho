# Close-out — repository, website and recent-email publication audit — 21 August 2026

**Status:** complete and production-verified.  
**Controlling audit:** `RECENT_REPOSITORY_WEBSITE_EMAIL_PUBLICATION_AUDIT_21AUG2026.md`.  
**Final main before this close-out:** `e8dc8ebbd4e7687dbe5eb226aa92b163728862cd`.

## 1. Final publication decision

The reverse-engineered review identified two immediate publication actions across the current repository state:

1. **Asset preservation and recovery became a first-class public workstream.** PR #681 added the bilingual intervention / preservation / confiscation architecture, authority matrix, current procedural-status layer and site-wide gateway.
2. **The canonical CGPJ routing page required a delivery-status correction.** PR #680 now states that three outbound attempts were made: the Appeals Section and General Secretariat messages were sent with receipt, association and examination unproved; the general Information attempt later generated a final non-delivery notice and is not a valid routing checkpoint.

No additional accusatory or duplicative page was justified.

## 2. Merged implementation chain

| PR | Merge commit | Function |
|---|---|---|
| #681 | `7ae8bd2ccf481d4b9dbe481372928d07e9ad2739` | Made asset preservation and recovery explicit through bilingual public pages, a machine-readable authority matrix, source-controlled legal modules and site-wide gateways. |
| #680 | `c65c87b107478b67b36daec678efe54c167bbb4c` | Published the bilingual CGPJ delivery correction, controlling correction register, current handover, ranked publication audit and sitemap update. |
| #682 | `e8dc8ebbd4e7687dbe5eb226aa92b163728862cd` | Added retained no-cache rendered-production verification for the four bilingual routes, both sitemaps and the global loader. |

## 3. Rendered-production verification

**Workflow:** `Verify 21 August asset recovery and CGPJ live`  
**Run:** `32430308100`  
**Job:** `96620399720`  
**Verified at:** `2026-08-20T23:50:45.953782Z`  
**Attempt:** 1 of 5  
**Result:** PASS  
**Artifact:** `recent-live-20260821`  
**Artifact ID:** `9428832473`  
**Artifact digest:** `sha256:bf32e47f2ab962d56b59a42ce9ede8772a0dbe765feec4de88ae3a3da9bcf167`  
**Artifact expiry:** 19 September 2026.

All seven checks returned HTTP 200 from `GitHub.com`, with no missing markers:

| Check | Bytes | SHA-256 |
|---|---:|---|
| English asset-recovery page | 13,108 | `dfa75e6ae3b641fca251a6e77e00d519c49076227daf082a785b1b062d2be3c0` |
| Spanish asset-recovery page | 13,578 | `dca99aa561b2360a2c821706303fc27418e1a3f3682f6c31106ccca581a28c9e` |
| English CGPJ delivery-correction page | 12,787 | `efe84fde9c3da623cf576a835384f968d03368231fcbe0a56bec895092f5e542` |
| Spanish CGPJ delivery-correction page | 13,063 | `63f0c08681c873c2d2f0d8486e4f8176b0452ed58eb79acae362340a638ef7ac` |
| Asset-recovery sitemap | 1,193 | `05b8f0ba759b5360d3b5f74d1c91c522a2d01ee2b8c5a8aca5aefc1206c7bc31` |
| CGPJ sitemap | 8,465 | `eecd5d1690160970a7a977633ca61e174805011a7964b6df1a2fcea3e9922056` |
| Global asset-recovery loader | 8,537 | `ec90f0243c9f81af9cb5ab04065f85a786659cc30e1e7351decb889c1fc9dcef` |

The production responses all reported `Last-Modified: Thu, 20 Aug 2026 23:44:48 GMT`. Cache-busting query parameters and no-cache/no-store request headers were used.

## 4. Intentionally not republished

- **TSJC Government File 38/2026:** the existing bilingual decision and appeal pages already preserve the subject-line/reference discrepancy and filed appeal status accurately.
- **Audiencia de Cuentas files 60/2026 and 145/2026 / entry 1619/2026:** the existing bilingual page already distinguishes the decision not to initiate an audit from any merits determination and distinguishes entry from admission.
- **26 February / 22 March 2018 recording chain and pre-7 June approaches:** already integrated through the controlled transcript and anonymised on-site-manager dossiers.
- **PwC, Grant Thornton and RSM/San Telmo routes:** already presented with source and response-state limits; substantive replies remain to be monitored.
- **AEAT expediente `00001-00113069`:** current main publishes only the supported procedural status—processing commenced at AEAT and no substantive access decision is established. No standalone page or inference about subject, delay responsibility, connection or outcome is authorised until the originating 5 January request or a complete expediente index is located.
- **Montelanza accounts, Cuatrecasas term-sheet material, legal-consultation recordings and private interpretive correspondence:** held behind source-reconciliation and privilege controls.

## 5. Evidential boundaries preserved

- no bounce does not prove receipt;
- a final bounce proves only that the specific attempt did not deliver;
- the failed Information attempt does not establish deliberate blocking, misconduct or failure of the other routes;
- preservation and intervention powers do not themselves establish criminal or civil merits;
- an official processing notice is not a substantive access decision;
- later corporate or financial layering neither proves illegality nor automatically ends economic traceability.

## 6. Final status

> **Repository updated and rendered website verified.**

The public record now contains the material asset-preservation architecture and the corrected CGPJ delivery status. The exact routes, sitemaps and global loader were independently fetched from the production GitHub Pages host and matched all required markers. Search-engine or external-cache lag is no longer material to the deployment conclusion.
