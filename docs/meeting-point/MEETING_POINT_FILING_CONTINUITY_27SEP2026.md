# Meeting Point — filing continuity, 27 September 2026

**🟠 AMBER — court-handling follow-up remains open; 🟢 preservation is complete and cross-system destination verification is GREEN.**

**Control:** PD-MP-FILING-CONTINUITY-20260927  
**🟢 GREEN — registration:** six receipts list the two-part Document 1 v19 and Document 2 v8 across both 357/2024 and 93/2025.  
**🟠 AMBER — subsequent handling:** association/incorporation and any judicial response remain unverified; a covering-note clarification is prepared but has no verified filing receipt.

This is the current filing-status successor to the **24 September v10/v4 baseline**. Earlier adverse-admission controls, findings and sources remain preserved; they are not silently erased or treated as the current document versions.

## Verified delivery record

The six native receipt PDFs were read directly and fingerprinted. All name the Plaza Nº 3 del Tribunal de Instancia (Sección Mercantil), Las Palmas de Gran Canaria. Times below are reproduced as printed, without an inferred timezone.

| Opaque source ID | Proceeding | Date / time | Listed material |
|---|---|---|---|
| PD-MP-REG-20260927-01 | 357/2024 | 27 September 2026 / 19:33 | Document 1 v19, part 1/2 |
| PD-MP-REG-20260927-02 | 357/2024 | 27 September 2026 / 19:56 | Document 1 v19, part 2/2 |
| PD-MP-REG-20260927-03 | 357/2024 | 27 September 2026 / 20:03 | Document 2 v8 and covering note |
| PD-MP-REG-20260927-04 | 93/2025 | 27 September 2026 / 20:07 | Document 1 v19, part 1/2 |
| PD-MP-REG-20260927-05 | 93/2025 | 27 September 2026 / 20:10 | Document 1 v19, part 2/2 |
| PD-MP-REG-20260927-06 | 93/2025 | 27 September 2026 / 20:14 | Document 2 v8 and covering note bearing the other proceeding reference |

Document 1 v19 has 232 pages, delivered as original PDF pages 1–153 and 154–232. Document 2 v8 has 226 pages. The same substantive pair is identified across the two proceedings. The original document hashes and the six receipt hashes are recorded in [`../../ops/continuity/MEETING_POINT_FILING_STATE_20260927.json`](../../ops/continuity/MEETING_POINT_FILING_STATE_20260927.json).

The two Part 2 receipts list Part 2 alone as the principal document. The final 357/2024 receipt lists the covering note as principal and Document 2 as an attachment. The final 93/2025 receipt lists Document 2 as principal and a covering-note filename referring to 357/2024 as an attachment. The receipt identifies 93/2025 correctly. The uploaded covering note's actual contents and portal-stored attachment bytes have not been independently retrieved; the filename discrepancy is therefore recorded precisely, without claiming a proved substantive misfiling.

## Remaining action

1. Preserve and, if presented, obtain the receipt for the prepared 93/2025 clarification linking its three registrations. **Prepared does not mean filed.** No evidence resend is inferred from the filename alone.
2. Obtain confirmation that each proceeding contains and associates its three submissions, and retain any court instruction on correction, incorporation, access or handling.
3. Preserve and review the court's eventual response. Registration does not establish examination, acceptance of allegations, procedural standing, judicial knowledge, criminal intent, or a merits outcome.

No verified deadline for these follow-up items is established in this receipt audit. They have an identified owner (the presenter) and remain open until source evidence closes them. No external follow-up message or additional filing was performed by this repository update.

## Technical route and version continuity

The citizen portal allowed one principal document and displayed a 10 MB per-file limit; the combined upload encountered an aggregate-size error whose exact ceiling was not independently established. The original Document 1 was split at a clean page boundary without intentionally changing its content; Document 2 retained its approved bytes. Each court therefore received separate submissions with independent receipts. The alternative excess-capacity route produced an index/identifier error and is not recorded as a successful filing.

The final approved document pair remains **v19/v8**. The earlier v10/v4 baseline and its `REVISE` result are historical, version-specific records. A rerun of the old literal-marker checker on v19/v8 returns `BLOCKED` for three exact marker groups (criminal-label wording, Hava Vida and term-sheet wording). That limited result is preserved: it is not an all-PASS report, a re-performance of legal review, a court rejection, or a reason to alter the already filed evidence. The filing receipt audit and the legacy wording checker answer different questions.

## Custody and publication boundary

Under PD-GOV-002 every tracked repository file is treated as public or potentially Pages-readable. Repository privacy and an archive/private filename do not authorise publication of raw legal materials. Git holds this minimised event/control projection and source fingerprints. Authorised private Drive/Library custody holds native receipts, exact registration/verification identifiers, the complete approved PDFs, available covering notes, the unfiled clarification and the detailed preservation manifest. Exact private correspondence and source locators are not copied into Git.

This update changes repository continuity records only. It does not rewrite the rendered website, alter deployment configuration, suppress historical allegations or contrary evidence, or certify any new legal conclusion. Cross-host/private preservation completion has now been checked against actual destination readback: GitHub merge/deployment readback, GitLab merged-file readback, private Library save, private Drive core-document hash readback, and full private Drive archive reconstruction all completed. This preservation result does not verify the court-held attachment bytes or subsequent judicial incorporation/handling.

## Continuación en español

**🟢 Registro acreditado:** seis justificantes identifican la presentación del Documento 1 v19, en dos partes, y del Documento 2 v8 en 357/2024 y 93/2025. **🟠 Tramitación pendiente de comprobación:** falta acreditar la asociación/incorporación efectiva de las entradas y cualquier resolución del órgano. La aclaración del rótulo de la nota adjunta al último envío de 93/2025 está preparada, sin justificante de presentación aportado.

Se preservan los originales, las huellas y el estado histórico v10/v4. Registro no equivale a admisión, examen ni decisión sobre el fondo. Las fuentes nativas y los identificadores privados permanecen en custodia privada autorizada; este registro contiene sólo la proyección mínima necesaria para la continuidad.

## Preservation package fingerprint

The private package has 43 members and 107,339,724 bytes. Archive SHA-256: `1ba719409726367285677bd78506ebdf1524b339daea065b3a364b66b3a40415`. Manifest SHA-256: `d3b6b08dc669eb913b86bb08001bac4b8451c799e6cb7a41b3fbd6c14a08db40`. These fingerprints establish the prepared preservation package, not identity of court-processed attachment bytes. **Preservation scope: 🟢 GREEN.** Private Library save is verified; core private Drive documents have SHA-256 readback verification; the 107,339,724-byte archive was preserved in four Drive parts and remotely downloaded/reassembled to the same archive SHA-256. GitHub PR #1992 is merged/deployed with exact public readback of the two new continuity files; GitLab MR !684 is merged with exact merged-file readback. GitLab Pages/project-wide CI remains separately affected by disclosed inherited failures and is not represented as GREEN.
