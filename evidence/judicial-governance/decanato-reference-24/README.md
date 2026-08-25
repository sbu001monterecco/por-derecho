# Decanato daily reference 24 — judicial complaint and amplification

**Control date:** 25 August 2026

**Public status:** complete principal pleading and complete amplification digitised; stamped presentation evidence included; personal data and signatures removed

**Procedural status:** presentation documented; onward allocation/disposition not located in the controlled public corpus

## Controlling formulation

The complaint was signed on **17 June 2026** and physically presented at the
Decanato of the Courts of Las Palmas de Gran Canaria on **18 June 2026**. The
stamped copy carries handwritten daily reference **no. 24** and the handwritten
direction to the investigating court allocated in turn.

Reference 24 is used here only as a material registry-location link. It is **not**
a NIG, a Diligencias Previas number, a formal allocation number or proof that a
judicial proceeding was opened. The later pleading uses `CONTROL 24` in its
source title; the public analysis does not adopt that wording as the name of a
formal case.

The amplification is dated **25 June 2026** and its photographed first page
carries a Decanato stamp and handwritten reference to 24. No controlled public
record presently establishes the complaint's subsequent allocation, NIG,
transfer, rejection, opening or closure. Non-location does not prove loss,
retention, mishandling or responsibility by any person.

## Evidence inventory

| Evidence ID | Native source | Native pages | Public derivative | Public pages | Classification |
|---|---|---:|---|---:|---|
| `EVID-2026-DECANATO-REF24-DENUNCIA-001` | Signed unified presentation package + photographed stamped cover | 79 + photograph | `public-pdfs/denuncia-magistrado-18jun2026-public-redacted.pdf` | 31 | party pleading + primary physical-presentation evidence |
| `EVID-2026-DECANATO-REF24-AMPLIACION-002` | Self-contained amplification + photographed stamped first page | 13 + photograph | `public-pdfs/ampliacion-denuncia-magistrado-25jun2026-public-redacted.pdf` | 14 | party pleading + primary physical-presentation evidence |

The 31-page complaint derivative contains, in order:

1. the privacy-safe photograph of the stamped presentation copy;
2. the three-page presentation manifesto from the signed unified package; and
3. all 27 pages of the principal complaint.

The native 79-page package also carried ten evidentiary annexes and the DIP
2/2026 Fiscalía records. Their complete inventory remains visible in the
manifesto and principal pleading. Their bodies are not duplicated in this
derivative because some contain private email bodies, signatures, direct contact
data or official verification locators. The official DIP 2/2026 decree and
notice are published separately under `evidence/fiscalia/dip-2-2026/`.

The 14-page amplification derivative contains the privacy-safe photograph of
the stamped first page followed by all 13 native pages. The source states that
the amplification has no annexes.

## Public transcriptions

- `full-text/denuncia-magistrado-18jun2026-public-transcription.md` — 31 public
  pages, including a controlled description of the stamped photograph and the
  complete text of the manifesto and principal complaint.
- `full-text/ampliacion-denuncia-magistrado-25jun2026-public-transcription.md` —
  14 public pages, including a controlled description of the stamped photograph
  and the complete 13-page text.

The Spanish source text controls. The English site provides analysis and
navigation; it does not purport to be a certified legal translation.

## Hashes and source custody

Native sources remain outside public Git history.

| Source or derivative | SHA-256 |
|---|---|
| Native signed 79-page unified package | `1cae1912a20202c5f5779db07e77c7e1d3f0ae514676e07d3ace4dd56f6f76a0` |
| Native photographed 18 June stamped cover | `749986511106962e6e2f227de87507cd72d22c30d86f99be7071bf49bee8c8f1` |
| Native 13-page amplification | `04051e33000f830c32ba06e31996ba4e6812c7d54c199ee03696b85e68589679` |
| Native photographed stamped amplification page | `33f138497ee2fec33499112b7c4dcbe592b37cc8c9075f43cb4eb576f940ba74` |
| Public complaint PDF | `dcc4ebc473d76475ae3dbbae10ea261adea4b1a99efa7e2a650c61338f61eebe` |
| Public amplification PDF | `73bd17df1b2bceb17c33fb1dbdee656a73faf2aaebbb14021bd4fd1c823cb4ed` |
| Public complaint transcription | `28ab9bbebecb967562610f8b694f7e4eabff7453c96064c119a781ba0d2983bc` |
| Public amplification transcription | `b93487a039174d5d19e5c7a9f04d104f480080fe047f2bec6e5cecb45a9e942c` |

Repeated builds reproduce the four public hashes above byte for byte.

## Redactions and privacy

The public derivatives remove only:

- the complainant's personal identifier;
- direct postal and email contact data;
- visual/electronic signatures and signature identifiers; and
- any verification material unnecessary to understand the pleadings.

Substantive allegations, legal qualifications, alternative explanations,
requested inquiries, named public/professional actors and the complete annex
inventory remain readable. The first-page receipt photographs are pixel-redacted
before insertion; redacted signature pages are rasterised to prevent hidden OCR
from retaining the removed identifier.

## Evidential classification and route separation

- The stamped photographs establish physical presentation and the material
  reference shown on the copies. They do not establish onward allocation.
- The pleadings establish what Gil Marer alleged and requested. They are not
  findings by a court, Fiscalía or the CGPJ.
- The complaint concerning the Judge remains separate from the complaint
  concerning the Insolvency Administrator and the private-actor routes.
- The 26 June filing `REGAGE26e00059624765` informed the CGPJ of the
  Decanato–TSJC traceability problem. Later confirmation that an identified
  five-file judicial package was joined to Appeal 286/2026 proves joinder of that
  package, not verification or adoption of its allegations, and does not by
  itself establish the onward destination of the 18 June complaint.

## Reproduction

Run `scripts/build_decanato_reference24_public_evidence.py` with the four
controlled native inputs. The script validates source page counts, builds the
two privacy-safe PDFs, generates page-accounted transcriptions, scrubs metadata
and fails if controlled private strings remain extractable.
