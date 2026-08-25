# DIP 2/2026 judicial-route extension — publication control

**Date:** 25 August 2026

**Status:** locally validated; remote CI, deployment and live readback pending

**Authority:** user instruction to digitise and publish the June 2026 judicial complaint and amplification, integrate them with the DIP 2/2026 Fiscalía correspondence, and publish an attributed, evidence-bounded request for independent review.

## Public scope

The existing bilingual route pair is extended rather than duplicated:

- `es/fiscalia-dip-2-2026/index.html`
- `en/fiscalia-dip-2-2026/index.html`

Both home-page update cards, both material-update pages and their Atom feeds
point readers to the extended dossier.

The page now contains:

1. the complete public-safe official DIP 2/2026 Decree and notice;
2. an adjacent reading notebook identifying and explaining the controlling passages of the 9 March notice;
3. the stamped presentation evidence and complete principal judicial complaint signed on 17 and physically presented on 18 June 2026;
4. the stamped presentation evidence and complete self-contained amplification dated 25 June 2026;
5. page-accounted Spanish transcriptions of both judicial pleadings;
6. a reproduced Magistrado-Juez accountability box;
7. a controlled matrix linking the alleged conduct of private actors and the insolvency administrator to the acts or omissions attributed to the Judge;
8. separate Decanato, CGPJ and prosecution-route traceability;
9. an expressly attributed call by Gil Marer for an independent audit of the Acosta Matos perimeter and the institutional response;
10. a controlled Canarias7 historical-publication checkpoint; and
11. the requested San Telmo and PwC contextual images at the bottom, connected to the asserted practical harm and the Article 24 CE effective-protection framework.

## Judicial-complaint evidence

| Evidence ID | Controlled native source | Native size | Public derivative | Public size |
|---|---|---:|---|---:|
| `EVID-2026-DECANATO-REF24-DENUNCIA-001` | signed unified presentation package plus photographed stamped cover | 79 pages + photograph | `evidence/judicial-governance/decanato-reference-24/public-pdfs/denuncia-magistrado-18jun2026-public-redacted.pdf` | 31 pages |
| `EVID-2026-DECANATO-REF24-AMPLIACION-002` | self-contained amplification plus photographed stamped first page | 13 pages + photograph | `evidence/judicial-governance/decanato-reference-24/public-pdfs/ampliacion-denuncia-magistrado-25jun2026-public-redacted.pdf` | 14 pages |

The 31-page public complaint consists of the privacy-safe stamped photograph,
the complete three-page presentation manifesto and all 27 pages of the principal
complaint. The native unified package also contained ten annexes and the DIP
2/2026 Fiscalía records. Their complete inventory remains readable in the
pleading; their bodies are not duplicated because some include private emails,
signatures, direct contact details or official verification locators. The
official Fiscalía records are published in their separate controlled evidence
directory.

The 14-page public amplification consists of the privacy-safe stamped
photograph and all 13 pages of the source. The source itself states that it has
no annexes.

### Public derivative hashes

| Derivative | SHA-256 |
|---|---|
| public complaint PDF | `dcc4ebc473d76475ae3dbbae10ea261adea4b1a99efa7e2a650c61338f61eebe` |
| public amplification PDF | `73bd17df1b2bceb17c33fb1dbdee656a73faf2aaebbb14021bd4fd1c823cb4ed` |
| complaint transcription | `28ab9bbebecb967562610f8b694f7e4eabff7453c96064c119a781ba0d2983bc` |
| amplification transcription | `b93487a039174d5d19e5c7a9f04d104f480080fe047f2bec6e5cecb45a9e942c` |

Native hashes, redaction rules and reproduction instructions are recorded in
`evidence/judicial-governance/decanato-reference-24/README.md`. The native
sources remain outside public Git history.

## Exact procedural formulation

- The principal complaint is dated 17 June and the stamped photograph documents
  physical presentation at the Decanato of Las Palmas de Gran Canaria on 18
  June 2026.
- The complaint requested routing to the competent judicial body and addressed
  the contemplated TSJC route. The public record does not establish that such a
  transfer occurred.
- Handwritten daily reference no. 24 is used only as a material registry-
  location link. It is **not** a NIG, Diligencias Previas number, allocation
  number, case number or proof that proceedings were opened.
- The amplification is dated 25 June and its photographed first page carries a
  Decanato stamp and a handwritten link to reference 24.
- No controlled public record presently establishes allocation, onward
  transmission, NIG, opening, rejection or closure. Non-location does not prove
  loss, retention, mishandling or responsibility.

## CGPJ route separation

The 26 June communication `REGAGE26e00059624765` informed the CGPJ of the
Decanato–TSJC traceability problem. Later confirmation that an identified
five-file judicial package was joined to Appeal 286/2026 establishes joinder of
that package only. It does not establish examination or adoption of its
allegations and does not by itself identify the destination of the 18 June
complaint. The page keeps DI 169/2026 / Appeal 286/2026 separate from the
Decanato material reference.

## Claims and safeguards

- The pleadings establish what Gil Marer alleged and requested; they are not
  findings of the Decanato, a court, Fiscalía or the CGPJ.
- The actor matrix identifies documentary links and finite questions. It does
  not infer a clandestine agreement merely from sequence, professional office,
  adverse decisions, acquaintance, silence or institutional routing.
- The Magistrado-Juez box publishes alleged commissions and omissions together
  with adverse record, lawful alternatives and the evidence needed to resolve
  them.
- Gil Marer's allegation that local prosecutorial action has been neutralised,
  and his risk hypothesis of institutional capture, are expressly attributed.
  Neither is stated as proved.
- The requested independent audit is framed as an evidence-preservation,
  conflict, routing and decision-traceability exercise. It is not a demand for a
  predetermined criminal outcome.
- The archived Canarias7 headline and the historical URL's later 404 status are
  documented. A 404 does not prove retraction, pressure, censorship, accuracy,
  falsity or the outcome of the reported matter.
- Article 24 CE is used as legal and practical context for the asserted harm.
  The page does not state that a court has adjudicated a violation of effective
  judicial protection in this route.

## Requested bottom images

The page uses the existing repository assets without altering their evidential
status:

- `assets/evidence/email-used-20260822/san-telmo-ricpe-sun-park-stamp-v1-ES.png`
- `assets/evidence/email-used-20260822/san-telmo-ricpe-sun-park-stamp-v1-EN.png`
- `assets/evidence/email-used-20260822/pwc-five-actors-plus-ac-2016-knowledge-checkpoint-ES.png`
- `assets/evidence/email-used-20260822/pwc-five-actors-plus-ac-2016-knowledge-checkpoint-EN.png`

The images are contextual summaries, not independent proof. Their captions link
to the longer source-controlled dossiers and distinguish alleged practical
damage from an adjudicated Article 24 finding.

## Privacy and reproduction

Public derivatives remove personal identifiers, direct contact details,
signatures and unnecessary electronic-verification material. The stamped
photographs are pixel-redacted before insertion. Signature pages are rasterised
after redaction so hidden text cannot retain the removed identifiers.

`scripts/build_decanato_reference24_public_evidence.py` validates source page
counts, produces both PDFs and transcriptions, scrubs metadata and fails if the
controlled private strings remain extractable. Repeated builds must reproduce
the recorded public hashes byte for byte.

## Communications boundary

No email, letter or LinkedIn post is sent, drafted in an external service or
published by this step. Those communications are the next proposed workstream
after exact live deployment verification and require separate recipient and
send approval.

## Closeout fields

- Pull request: pending
- Merge SHA: pending
- Pages deployment: pending
- Live readback: pending
- Current state: `DRAFT / LOCAL_VALIDATED`

Local checks passed repository preservation, publication integrity, audience
experience, mission-critical controls, operational continuity, public-link and
bilingual-structure checks. A clean temporary evidence rebuild reproduced both
PDFs and both transcriptions byte for byte. All 45 public pages rendered; the
signature redactions and receipt photographs were inspected, and controlled
private strings were absent from extracted public text. Remote CI and exact live
readback remain required before closeout.
