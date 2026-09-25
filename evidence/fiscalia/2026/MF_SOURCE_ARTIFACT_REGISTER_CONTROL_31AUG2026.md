# Ministerio Fiscal source-artifact register control — 31 August 2026

## Status and scope

This control fixes the byte identity and public treatment of the **ten binaries supplied for the 31-August-2026 Ministerio Fiscal continuity review**. The canonical machine-readable inventory is:

- `evidence/fiscalia/2026/MF_SOURCE_ARTIFACT_REGISTER_31AUG2026.csv`

The native binaries are **not committed**. The register deliberately uses opaque content-derived IDs and public-safe labels. It does not reproduce native filenames, private locators, addresses, personal identifiers, contact details, or signature identities.

This is an **artifact register**, not a communications-event register, filing ledger, proceedings register, or merits assessment.

## Controlling separation rules

1. **Artifact identity means exact bytes.** SHA-256 is the public content address; SHA-512 is retained because the RedSARA receipt controls use it for attachment reconciliation.
2. **A transmission is a separate event.** One artifact may have zero, one, or multiple transmissions. A later transmission of the same bytes does not create a new source artifact, and two transmission events do not merge their recipient files.
3. **`FILED_EXACT_BINARY` requires an exact bridge.** A REGAGE reference appears in `associated_regage_exact_proof` only where the receipt attachment hash binds that exact binary to the registration.
4. **A draft is not a filing.** An unsigned DOCX, outbound copy, or authoring source is not treated as signed, sent, registered, or filed because a related PDF or later document was transmitted.
5. **Metadata is bounded.** PDF/OOXML creation fields and supplier labels are date clues, not proof of authorship, signature, dispatch, institutional receipt, or publication.

## Reconciliation result

| Control result | Count | Meaning |
|---|---:|---|
| Supplied source artifacts | 10 | Ten unique byte sequences were independently registered. |
| Unique SHA-256 values | 10 | No exact duplicate exists within this ten-artifact intake. |
| Exact filed binaries | 2 | One unsigned party pleading and one integrity-signed party communication have exact receipt-attachment hash bridges. |
| Exact registration events bound to those binaries | 3 | One event for the January pleading; two events for the same February communication. |
| Cryptographically integrity-validated PDF | 1 | Full-document byte-range validation succeeded; certificate trust-chain status remains unestablished. |
| Internal analytical or continuity derivatives | 5 | These are source aids, not filings or independent proof of their underlying propositions. |
| Party copies or drafts without an exact filing bridge | 3 | March request copy, early-June follow-up copy, and July unsigned authoring source remain distinct from proved transmissions. |

## Exact-match and variant findings

- **`MFSA-150FB16C44A9`** is byte-identical, by the receipt-index SHA-512 control, to an attachment registered under `REGAGE26e00010479093`. The local acquisition label was only an alias; it was not a new version.
- **`MFSA-BECFFDD70F53`** is byte-identical, by the receipt-index SHA-512 control and occurrence count, to the same attachment registered in two events: `REGAGE26e00020918896` and `REGAGE26e00020919686`. This proves two registrations of one artifact, not joinder, review, or a common outcome.
- **`MFSA-39C62C2596FB`** is an unsigned DOCX authoring source. The later signed PDF registered on 2 August 2026 is a different artifact and has its own independently controlled hash. The signed-PDF filing must not be assigned to this DOCX.
- **`MFSA-DB8B84FD2D12`** is related by title and subject to a PDF recorded elsewhere, but byte identity and complete content equivalence have not been tested. It remains a companion variant, not an exact match.
- **`MFSA-11CF264FC836`** and **`MFSA-196BB02F77C1`** address the same media-traceability subject but have different hashes, sizes, and text. Neither is silently treated as the duplicate or superseding original of the other. Their current public analytical treatment is governed by the later media traceability control.
- **`MFSA-69147AEDC665`** and **`MFSA-E9599CAEF556`** have no exact receipt/hash bridge in the current repository control set. Reported or intended dispatch cannot be promoted to `SENT`, `REGISTERED`, or `FILED` for those binaries.

## Signature control

Only `MFSA-BECFFDD70F53` carries a cryptographic PDF signature that validated for integrity across the full document in the acquisition review. The environment did not establish the signer's certificate trust chain; the register therefore says **integrity valid, certificate trust not established**, rather than making an identity or legal-validity finding.

The other three PDFs had no PDF digital signature. The six DOCX artifacts had no OOXML package signature. `UNSIGNED` in this register means only that no cryptographic signature was found in the reviewed binary. It does not decide authorship, intention, whether a paper copy was signed, or whether a different signed rendition exists.

## Privacy and publication rule

- Every native artifact remains outside the public repository.
- Artifacts containing personal identifiers, addresses, contact data, or signature metadata require a purpose-limited redacted derivative before any publication.
- Internal handovers, analytical reports, and working annexes are not made native-public merely because no necessary personal identifier was observed in a finite text review.
- A public-safe summary may cite the artifact ID, hash, format, size, page basis, controlled filing state, and evidential limit. It must not reconstruct private filenames or private source locators.
- A DOCX page count is render-dependent; only the PDF counts are native page-tree counts.

## Evidential limits

Content-addressing proves that a later reviewer is discussing the same bytes. It does **not** by itself prove authenticity, truth, completeness, authorship, service, institutional knowledge, examination, reliance, legal sufficiency, or outcome.

An exact RedSARA attachment match proves registration of that artifact through the recorded route. It does not prove that a named person read it, that the recipient accepted its allegations, that a particular proceeding incorporated it, or that any requested measure was required.

Internal reports and continuity documents are derivatives. Their statements must be tested against the underlying primary source, contrary material, and current procedural record. Adverse outcomes, silence, routing gaps, repeat contact, or functional benefit to a private perimeter are not proof of coordination, capture, obstruction, prevarication, or criminality without the additional actor-specific evidence required for those propositions.

## Repository anchors used for reconciliation

- `archive/evidence/mf-redsara-anexo4/MF_REDSARA_UNIQUE_ATTACHMENT_INDEX.csv`
- `archive/evidence/mf-redsara-anexo4/MF_REDSARA_REGISTRATION_INDEX_SHORT.csv`
- `archive/CANARIAS7_FAJARDO_MEDIA_TRACEABILITY_15AUG2026.md`
- `evidence/fiscalia/2026/FGE_INSPECCION_EG_745_2026_ANNEX_EVIDENCE_GAP_MATRIX_29AUG2026.md`
- `evidence/fiscalia/2026/2026-08-26_FGE_INSPECCION_EG_745_2026_METADATA.json`
- `evidence/fiscalia/2026/EG_745_2026_ERROR_OMISSION_MISCLASSIFICATION_REGISTER_31AUG2026.md`

## Validation contract

The CSV is valid only if all of the following remain true:

1. exactly 10 data rows and 10 unique artifact IDs;
2. every artifact ID suffix equals the first 12 hexadecimal characters of its SHA-256, uppercased;
3. every SHA-256 is a 64-character lowercase hexadecimal digest and every SHA-512 is a 128-character lowercase hexadecimal digest;
4. byte and page counts are positive integers, with page basis explicitly stated;
5. only the three receipt events listed above appear in the exact-proof REGAGE field;
6. no original native filename, personal identifier, address, contact detail, signer identity, or private locator appears in the public-safe register; and
7. every row preserves an artifact/transmission boundary and an evidential limit.

Validation of structure, digest syntax, content-derived IDs, numeric fields, allow-listed REGAGE references, and public-safe string exclusions was performed on 31 August 2026. This is a register validation, not independent authentication of the native documents or their allegations.
