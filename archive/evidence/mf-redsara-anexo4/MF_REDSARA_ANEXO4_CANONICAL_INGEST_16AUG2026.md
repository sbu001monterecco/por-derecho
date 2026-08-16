# Ministerio Fiscal / RedSARA — Anexo 4 canonical ingest

**Status:** canonical receipt-level source ledger for the 154-page RedSARA bundle supplied on 16 August 2026.

## Source control
- Source: `ANEXO 4 RedSARA Ministerio Fiscal Comunicaciones Registradas.pdf`
- Pages: **154**; bytes: **6,231,346**; SHA-256: `4636b0da487f9150cd8f229d36f9c44f1bd16c9005f6bfa1415bcbc84595e03f`
- **75** registered communications, from **15 Dec 2025 20:53:36** to **26 Feb 2026 22:35:27**.
- **126** annex listings on receipts; **100** unique filename + SHA-512 pairs.
- Extraction used the native PDF text layer; no OCR.
- Because `por-derecho` is public, the repository derivative redacts the submitter's repeated NIE, street address, direct email and direct phone number. All substantive/legal/registration text, REGAGE references, dates, destinations, subjects, `Expone`/`Solicita`, annex filenames and receipt-listed SHA-512 values are retained.
- The native 6.2 MB PDF is **not** copied into public GitHub. The original binary remains controlling for authenticity/layout; a private-vault custody event is still open.

## Evidential rule
Each page is an official registration receipt and therefore verifies **what text/annex metadata was registered, when, and to which destination**. It does **not** by itself prove the truth of allegations inside the submission, that every annex was substantively examined, or that the requested investigation/action was opened or granted. Underlying offence descriptions, motive/knowledge claims and procedural summaries remain party-authored until independently corroborated.

## What is now recoverable without re-uploading the PDF
- `MF_REDSARA_REGISTRATION_INDEX_SHORT.csv`: all 75 registrations, page ranges, dates, REGAGE numbers, recipients, subjects and annex counts.
- `MF_REDSARA_UNIQUE_ATTACHMENT_INDEX.csv`: all 100 unique annex filename/SHA-512 pairs.
- Five ordered `ANEXO4_REDSARA_TRANSCRIPT.bz2.b64.part-*` files: lossless bzip2+base64 container for the complete **public-safe 154-page text transcript**.
- `ANEXO4_REDSARA_TRANSCRIPT_README.md`: decode/reconstruction instructions and hashes.

## Recipient distribution
- 45: J00001657 - Fiscalia Provincial de Las Palmas
- 8: J00015401 - Fiscalia de la Comunidad Autonoma de Canarias
- 5: J00017154 - Fiscalia de Area de Arrecife de Lanzarote-Puerto del Rosario
- 5: J00001853 - Fiscalia Provincial de Santa Cruz de Tenerife
- 4: J00004991 - Fiscalia Especial contra la Corrupcion y Criminalidad Organizada
- 2: J00024141 - Fiscalía Europea
- 2: J00003992 - Fiscalía General del Estado
- 1: J00004143 - Fiscalia Provincial de Valencia
- 1: J00020146 - Fiscalía de la Sala de lo Penal del Tribunal Supremo
- 1: J00003864 - Fiscalia de la Audiencia Nacional
- 1: EA0052807 - Unidad de Apoyo a la Fiscalía Europea

## High-value references surfaced or sharpened
- **DI 113/2022 — NIG 3501670220220003722.** The 12 Feb 2026 registered request says the file arose from a 2 Jun 2022 filing concerning Construcciones Acosta Matos and was archived. The receipt proves that representation/request; obtain the primary file/archive order before upgrading merits/status.
- **Expediente Gubernativo 33/2025.** A 12 Feb 2026 registered request describes a 28 Feb 2025 archive resolution signed by Beatriz Sánchez Carreras and antecedents received from Anticorrupción, Fiscalía de la Comunidad Autónoma, Secretaría Técnica and Unidad de Apoyo de la FGE. Primary file still required.
- **DIP 20/2026 (Tenerife) — NIG 3803870220260000387.** Several Feb registrations describe a 27 Jan 2026 decree opening pre-procedural investigation and territorial inhibition/remission to Las Palmas. The signed decree/file must control exact scope and later routing.
- **EG 19/2026 (Valencia → Arrecife).** Two 2 Feb registrations describe a 28 Jan 2026 Valencia territorial inhibition and transfer to Arrecife, expressly saying no merits determination/opening occurred in Valencia. Primary decree and Arrecife destination reference/outcome remain open.
- **DP 91/2023 / Rollo 120/2024** and **OC/2024/0532** appear in 21 Dec 2025 traceability/SAIP communications to Madrid/European bodies and should be reconciled against primary files.

## Thematic chronology
- **15–27 Dec 2025:** multi-recipient institutional traceability, SAIP, public-funds/EU protection, DP 91/2023/Rollo 120/2024, OC/2024/0532, Sun Park/MYND and calificación/accounting topics.
- **4–20 Jan 2026:** targeted criminal-notice/preservation wave covering the 2022 Sun Park act, alleged exploitation without title, ETJ 163/2020, judicial-conduct allegations, Meeting Point/Club Sei preservation, financial-asset suppression, liquidation-plan execution, extraprocess use of the non-final calificación judgment, OB REM/funds and Valencia banking/credit-assignment issues.
- **21 Jan–2 Feb 2026:** integration/RIC-CNMV/AC/specialist-Fiscalía phase, including pre-hearing knowledge, CNMV traceability, AC handling/omissions, Community/FMMM records, Pink Canary/operator attribution, Anticorrupción/RIC/UE and EG 19/2026.
- **8–14 Feb 2026:** consolidated packages, new-facts amplification, requests for DI 113/2022 and EG 33/2025, procedural impulse and a request to certify Ministerio Fiscal routing/accumulation.
- **26 Feb 2026:** parallel Las Palmas / Fiscalía de Canarias communications delimit a claimed autonomous extraconcursal penal nucleus and expressly frame the superior-level copy as knowledge/traceability, not an appeal against provincial competence.

## Open source-completion targets
1. Primary DIP 20/2026 decree/file, exact transfer package, destination reference, assigned fiscal and outcome.
2. Primary EG 19/2026 Valencia decree and Arrecife file/reference/outcome.
3. Complete EG 33/2025 file and 28 Feb 2025 archive resolution.
4. Complete DI 113/2022 file/archive order using NIG `3501670220220003722` as retrieval key.
5. Primary DP 91/2023 / Rollo 120/2024 / OC/2024/0532 records.
6. For high-value annexes, recover the native submitted document and compare it to the SHA-512 listed on the relevant receipt.

## Continuity rule
Future threads should search this ledger/index first. Do not ask for this bundle to be re-uploaded merely to recover its text. If exact graphic layout/signature/certification or the redacted contact fields matter, re-query the native source system/original rather than treating the derivative as the original.