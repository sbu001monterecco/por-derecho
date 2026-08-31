# Sun Park ACTA owner-role and lineage control — 31 August 2026

**Status:** PREPARED LOCALLY; NOT PUSHED, MERGED, DEPLOYED OR LIVE  
**Base:** `a54c74b204d6f7596d3da9e41af569c08c676736` (`origin/main`)  
**Scope:** Owners' Community ACTA/event records from 2008 onward, plus an explicit pre-2008 source-gap control.

## Result

The bilingual ACTA document room and the relevant event pages now distinguish two separate dimensions:

1. the principal historical lineage attributed to the record; and
2. the evidence for who called the meeting, managed/chaired it, authored or attested the ACTA, and held or circulated the resulting record.

The visible lineage controls use colour together with a printed code and label. Colour is never the sole carrier of meaning.

| Code | Principal lineage | Evidential limit |
|---|---|---|
| A | Original Montelanza/JPS, before the 2008 sale and before Multimatrix | Does not attribute later project-side conduct to Gil Marer or Patricia Jones |
| B0 | Multimatrix/LPB project phase before the documented Gil/Patricia phase | Kept separate from B1 to prevent retroactive personal attribution |
| B1 | Aweswell/LPB, Gil Marer and Patricia Jones project perimeter | Person-specific roles are stated only where the source records them |
| C1 | Alleged adverse Montelanza/Molina–Roque Prieto/FMMM/Pamanil/Cogolludo phase | “Adverse” is Gil Marer's attributed position, not a judicial finding |
| C2 | Later alleged Acosta Matos/CAM phase | The transition is an attributed documentary sequence, not proof of legal or corporate succession |
| D | Mixed, contested or unresolved | An evidence status, not a fourth ownership perimeter |

Montelanza, Molina-linked people or entities, Pamanil, CAM, Acosta Matos actors, Aweswell, LPB, Multimatrix, CEXP and every named individual remain legally distinct. The sequence proves no common control, agreement, fraud, criminal purpose or guilt.

## Role-separation rule

For every controlled Owners' Community record, the interface separately states:

- **caller / convener** — who issued or is attributed with the notice or call;
- **meeting management** — who opened, chaired or managed the meeting;
- **ACTA authorship / attestation** — who acted as secretary, drafted, finalised, signed or attested the record; and
- **custody / circulation** — who held the book or copy, administered the record, or circulated it where the source supports that function.

Attendance, representation, signature, finance, objection or later benefit does not by itself establish any other role. “Secretary-administrator” is retained as the source capacity when the record combines those offices; it is not silently converted into proof of sole drafting or official-book custody.

## Controlled denominator and pre-2008 finding

The role matrix covers 17 Owners' Community ACTA/event records:

- five records in the 2008–2009 formation/transition period;
- eleven located or substantially referenced records from 2011 to 2018; and
- the 4-Feb-2022 Community record.

No Owners' Community ACTA earlier than 29-Apr-2008 has been located or identified by date in the controlled corpus. Earlier statutes, title instruments and historical references are not reclassified as meeting minutes.

The standalone 20-Nov-2018 notice and ACTA remain unlocated. That entry is therefore reference-only and preserves the later recital without fabricating caller, chair, author or custody facts.

## Deterministic controls

- `scripts/acta_owner_role_matrix.py` is the bilingual role and principal-lineage source of truth.
- `scripts/build_acta_meeting_lineage.py` injects the controls into the bilingual document-room pages, relevant event pages and machine index.
- `scripts/validate_acta_meeting_lineage.py` checks all 17 records, four role fields, principal-lineage machine values, bilingual text, room matrix and CSS selectors.
- `assets/acta-document-room-20260822.css` supplies the coded colour treatment and responsive role matrix.

## Verification

Passed locally on 31-Aug-2026:

- `python3 scripts/build_acta_meeting_lineage.py`
- `python3 scripts/validate_acta_meeting_lineage.py`
- `python3 scripts/validate_repository_preservation.py`
- `python3 scripts/validate_publication_integrity.py`
- `python3 scripts/validate_audience_experience.py`
- Python byte-compilation of the builder, matrix and specialist validator
- `git diff --check`

The checked-in Playwright render script could not run in this worktree because its optional `playwright` package is absent, and no browser-control runtime was available. This is recorded as a visual-runtime limitation, not converted into a visual pass. The deterministic HTML/CSS, bilingual, responsive-selector and repository-wide gates passed.

## Publication boundary

This change is locally prepared only. A push, pull request, merge, Pages deployment and live readback require separate publication authority and remain pending.
