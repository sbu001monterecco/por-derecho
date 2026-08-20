# Public redaction log

**Evidence ID:** `SP-2018-02-27-AC-SECURITY-REQUEST`  
**Method:** render original at 300 dpi → burn redaction rectangles into pixels → create raster PDF → OCR the already-redacted raster → strip/replace metadata → render and inspect final PDF.

## Redactions

| Marker | Location | Removed category | Reason | Operative meaning retained? |
|---|---|---|---|---|
| R1 | Header — sender field | Direct professional electronic address | Unnecessary direct contact data | Yes: sender name, capacity, firm and message remain visible |
| R2 | Header — recipient field | Direct organisational/professional electronic address | Unnecessary direct contact data | Yes: the body identifies the recipient’s Community role |
| R3 | Header — copy field | Direct professional electronic address | Unnecessary direct contact data | Yes: the operative request is unaffected |

## Information deliberately retained

- sender and recipient names where evidentially material;
- stated professional and institutional capacities;
- date, time and subject;
- the complete operative message;
- firm identity and standard business footer;
- the original scan appearance, including visible typographical forms.

## Validation

- the three removed address strings are absent from the final PDF’s searchable text layer;
- the final PDF is a one-page A4 document and contains no forms or JavaScript;
- visual inspection confirms that the redaction rectangles fully cover the original address glyphs;
- manual transcript and translation are stored separately because OCR is a retrieval aid, not the authoritative transcript.

## Boundary

The public derivative does not replace or alter the restricted original. No unredacted copy is committed to the public GitHub repository.
