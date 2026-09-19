# Ministerio Fiscal PDF viewer, context and interconnectivity control — 18 September 2026

## Objective

Every **public-safe PDF derivative currently committed under `evidence/fiscalia/**`** must be:

1. viewable directly in an in-page PDF viewer;
2. accompanied by a source-bounded contextual explanation;
3. accompanied by a clear “what this does not prove” boundary; and
4. interconnected with the related proceeding, actor and E.G. 745 response routes.

The canonical machine-readable register is:

`assets/data/ministerio-fiscal-pdf-room-20260918.json`

The bilingual public document rooms are:

- ES: `/es/ministerio-fiscal-documentos-pdf/`
- EN: `/en/public-prosecution-pdf-document-room/`

## Current public-safe PDF denominator

The current `evidence/fiscalia/**` tree contains **five public-safe PDFs**:

- DI 273/2013 complaint — 8 pages;
- DIP 2/2026 closure decree — 10 pages;
- DIP 2/2026 notice — 1 page;
- E.G. 112/2026 clarification decree — 3 pages;
- E.G. 745/2026 public redacted facsimile PDF — 3 pages.

The validator must fail if another PDF appears under `evidence/fiscalia/**` without being added to the register and both public rooms.

## Important boundary

“All PDFs viewable” applies to public-safe derivatives. Native prosecutorial files that remain private, contain direct personal/certificate/contact data, or have not yet been obtained are **not silently published** to satisfy a UI requirement.

Examples presently outside the public-safe denominator include:

- private/source-controlled E.G. 49/2026 native decrees;
- the 12 March 2019 Fiscal calificación opinion where no controlled public PDF derivative is currently present under `evidence/fiscalia/**`;
- the missing signed 29 July 2026 DP 1901 Fiscal report.

Those sources remain evidence-production/public-derivative tasks, not false “viewer complete” claims.

## Interconnectivity rule

Each PDF card must answer:

- **What is this document?**
- **Why does it matter?**
- **What does it establish?**
- **What does it not establish?**
- **Where do I go next?**

The “go next” links must include at least one proceeding-specific route and one wider Ministerio Fiscal/E.G. 745 route where materially relevant.

## Future rule

Any future source-controlled public-safe Ministerio Fiscal/Fiscalía PDF must be added to the register and room in the same change set that commits the PDF. The CI gate is intended to prevent orphan PDFs, direct-download-only publication, and PDFs without context.

## 19 September all-office extension

The public PDF room remains a **public-safe derivative denominator**, not the complete prosecutorial corpus. The wider office-by-office control is now `assets/data/ministerio-fiscal-office-digitisation-20260919.json` with bilingual coverage pages at `/es/ministerio-fiscal-cobertura-oficinas/` and `/en/public-prosecution-office-coverage/`.

The extension separates office/file discovery, native custody, text extraction/OCR, substantive review, public-derivative readiness, viewer-live status and certified-file completeness. A source may be fully digitised in private custody while still being absent from the public room; that is a privacy/publication boundary, not a missing-source claim.

All future public-safe PDFs remain subject to the existing atomic rule: PDF + registry + both bilingual viewers + context + evidential boundary + related links + sitemap/search + validation in one reviewed change.
