# ACTA digitisation and publication closeout — 27 August 2026

## Result

All **17 located ACTA control-copy families** are processed into public-safe digitisation packages and prepared for publication. The generated layer contains:

- **246** represented source pages;
- **17** raster-only, irreversibly redacted source facsimile PDFs;
- **246** redacted source-page JPEG images;
- **17** page-sequenced public-redacted OCR text packages;
- **17** rendered text-edition PDFs containing **279** public-edition pages; and
- per-family provenance, redaction logs, integrity manifests and a v2 source-family reconciliation file.

The public index is `evidence/community/actas/public-index.json`. Exact source/derivative hashes and page lists are controlled by the 17 package manifests. The generation and validation code is retained in `scripts/digitise_all_actas.py` and `evidence/community/actas/build_public_packages.py`.

## Meeting-lineage and individual pages

The digitisation is now connected to a separate 20-event meeting-lineage layer at `evidence/community/actas/meeting-lineage-index-v1.json`:

- 40 bilingual individual event pages;
- full embedded public OCR and every redacted source-page image for the 17 digitised families;
- explicit gap pages for 10-Apr-2014, the non-ACTA 11-Jun-2016 working meeting and the unlocated 20-Nov-2018 ACTA;
- visual distinction among Montelanza pre-sale, project-side Multimatrix/LPB→Aweswell/LPB–Gil, alleged adverse Montelanza/Molina–Pamanil, alleged adverse Acosta Matos/CAM, mixed/contested and unresolved lanes; and
- source-based convener/body, attribution status, confidence, basis, previous/next and related-event links.

The adverse-perimeter labels are Gil Marer's attributed position and do not establish joint action, fraud, criminality or guilt. A project-side label does not attribute pre-entry conduct to Gil. The controlling continuity audit is `archive/ACTA_MEETING_PERIMETER_CONTINUITY_AUDIT_27AUG2026.md`.

## Private custody

The 59 private source/supporting files (277,899,789 bytes; zero empty files) are enumerated and hashed by `inventory.private.v2.json`, which deliberately excludes itself from its own hash list. The sources plus manifest are preserved outside the public repository in `ACTA_PRIVATE_SOURCE_CUSTODY_20260827_V2.tar.gz`:

- archive size: **238,610,585 bytes**;
- archive SHA-256: `64bc2d6ef812e5684bc772eac8aa6fee5970d10e0dc5598985d68424d66994ef`; and
- durable private preservation: **completed 27 August 2026**.

No provider locator, native signature, personal identifier or private message body is committed to Git.

## Corrections made

1. **10 August 2012:** a four-page native DOCX ACTA was recovered and authenticated by hash; a related five-page PDF family is also preserved. The ACTA records that no resolution was put to a vote. Its referenced president statement and objection annexes remain unlocated.
2. **26 April 2016:** the public control package now represents the 77-page family, not the earlier 24-page partial package. Two distinct 77-page binaries are render- and text-equivalent; 24-, 47- and 50-page packages remain separately recorded.
3. **5 July 2018:** the exact nine-page source already cited in the repository is digitised and posted. A distinct nine-page binary variant is visually equivalent.
4. **Historical previews:** prior WEBP text-edition links remain intact. The regenerated text previews and new source galleries use non-empty, decoder-validated JPEGs.

## Publication boundary

`located-package-digitised-public` is deliberately not `located-package-complete-public`.

- OCR is not certified and is not manually source-line verified.
- Received copies are not represented as official minute books or certified originals.
- Redacted source facsimiles are raster-only public derivatives; native sources remain outside Git.
- Full-source hashes identify received binaries but do not authenticate the truth, validity or implementation of the minutes.
- Personal identifiers, signatures, direct contact details, banking data and non-essential owner-level data are withheld or burned out.

## Open evidence

- standalone ACTA for the meeting later recited as 20 November 2018;
- president statement and objection annexes referenced in the located 10 August 2012 ACTA;
- manual line-by-line certification of the 17 OCR packages;
- official minute books/certified copies, complete notices, proxies, audio, annex and implementation chains where not already located; and
- authenticity and legal-effect analysis for each source family.

These gaps are recorded; they are not filled by inference and do not reverse the completed digitisation of the located control copies.

## Validation gate

The release gate requires:

1. package validation for all 17 manifests and all generated assets, plus the 20-event/40-page lineage and interlink validator;
2. zero-byte/image-decode rejection;
3. page-count and SHA-256 parity;
4. empty extracted text from every raster-only source facsimile;
5. privacy-pattern and visual redaction review;
6. repository preservation, publication-integrity, audience and production checks; and
7. merge plus live GitHub Pages readback.

The deployment record and final merge/readback result are appended to `archive/DEPLOYMENT_LOG.md` after publication.

## Continuity/deletion rule

After merge, live readback and private custody preservation are recorded, this thread is safe to delete **for continuity purposes**: a future thread can recover the current state, scripts, manifests, public packages, variants and open evidence. That conclusion is not a claim that every historical ACTA/annex exists or that the OCR is evidentially certified.
