# Public redaction and digitisation log

**Evidence ID:** `SP-2018-02-27-AC-SECURITY-REQUEST`
**Canonical repository method:** manually verify source image → create diplomatic transcript without silent correction → replace three direct electronic addresses with R1–R3 redaction markers → generate deterministic searchable PDF in ReportLab invariant mode → inspect text layer, structure and rendered page.

## Redactions

| Marker | Location | Removed category | Reason | Operative meaning retained? |
|---|---|---|---|---|
| R1 | Header — sender field | Direct professional electronic address | Unnecessary direct contact data | Yes: sender name/capacity and operative message are preserved in the source record |
| R2 | Header — recipient field | Direct organisational/professional electronic address | Unnecessary direct contact data | Yes: the body identifies the recipient’s Community role |
| R3 | Header — copy field | Direct professional electronic address | Unnecessary direct contact data | Yes: the operative request is unaffected |

## Information deliberately retained

- sender and recipient names where evidentially material;
- stated professional and institutional capacities;
- date, time and subject;
- complete operative wording;
- the visible source forms `Le escrito` and `accedo`, marked `[sic]`;
- source hash and evidence ID.

## Canonical repository PDF

The committed PDF is a clean digital derivative, not a representation that the original was natively digital. It is built reproducibly from the checked transcript by `/tools/build_ac_security_request_public_pdf.py` using `reportlab==4.4.9` with invariant output enabled and hash-locked embedded DejaVu Sans/Serif fonts.

Validation:

- no direct email address is present in visible text or the searchable layer;
- one A4 page, no forms, JavaScript or encryption;
- rendered page visually reviewed;
- exact SHA-256: `129cfdd2b74fe7f5e35b0db7890878aa10c5b81e6d4d6c9d3eaf0845eb820607` (88,176 bytes).

## Supplementary facsimile working copy

A raster-redacted facsimile was separately produced by burning the three redactions into pixels before OCR. It was visually checked and its searchable layer was tested. Its SHA-256 is `91e8366e65496ff63d11877af6f81f90a89472c37c386db94622b4d1de180551`. It is retained as a working/public-delivery copy and is not the canonical repository object.

## Boundary

Neither public derivative replaces or alters the restricted original. No unredacted copy is committed to the public GitHub repository.
