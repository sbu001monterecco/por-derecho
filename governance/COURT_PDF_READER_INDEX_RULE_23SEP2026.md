# Court PDF reader/index rule — 23 Sep 2026

## Mandatory rule
Every PDF sent to or received from a court, Fiscalía, Tribunal, Audiencia, Decanato, judicial office or procedural counterparty that enters the controlled Por Derecho corpus must have a reader/index record.

Minimum fields:
1. immutable document ID;
2. exact document title;
3. date signed / filed / received, each kept separate;
4. proceeding and court/Fiscalía;
5. sender / recipient / filing capacity;
6. page count;
7. original SHA-256 where controlled;
8. public-derivative SHA-256 if a redacted/flattened copy is published;
9. publication status: PUBLIC / CONTROLLED / PRIVATE / WITHHELD;
10. clickable PDF viewer/link when publication is authorised;
11. text/transcription link when available;
12. page-level deep links for every cited proposition;
13. upstream/downstream proceeding links;
14. actor/capacity links;
15. Truth Machine proposition IDs;
16. contrary/supporting evidence links;
17. evidential limits and unresolved questions.

## Viability gate
A page must not claim a PDF is available unless live readback confirms:
- HTTP/browser retrieval works;
- the expected page count is visible;
- cited page deep-links land on the correct document;
- the PDF is not an expired or session-only URL;
- sensitive fields requiring minimisation are removed before public release.

## Indexing hierarchy
COURT/FISCALÍA → PROCEEDING → DOCUMENT → PAGE/BLOCK → PROPOSITION → EVIDENCE RELATIONS → CLAIM FAMILY → LATER FILINGS.

## R33 special rule
The R33 page-5 apology must maintain direct viewer links to:
- R33 opposition, page 5;
- 4-Jan-2019 draft concerning AC conduct / reserve of responsibility and separation;
- 6-Jun-2019 opposition to calificación;
- 19-Feb-2020 Article 215.2 providencia;
- 21-Sep-2020 Joaquín withdrawal/apology;
- AC-removal history;
- counsel-continuity matrix;
- querella-reference ledger.

## No-overstatement rule
A draft is evidence that a draft existed and of what it contemporaneously said. It is not automatically a filed pleading.
A licence to file a querella is not proof that the querella was filed.
A filing is not proof of admission.
Admission is not proof of the allegation.
An allegation is not a finding.
