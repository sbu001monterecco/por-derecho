# Ministerio Fiscal communications ↔ proceedings interconnectivity control

Control date: **31 August 2026**  
Status: **IMPLEMENTED IN CURRENT TREE — PUBLICATION VERIFICATION PENDING**

## Outcome

The public site now has a deterministic, reciprocal bridge between:

1. the canonical institutional communications register;
2. the canonical Proceedings Master Register;
3. the public Proceedings Master projection;
4. the Proceedings Interconnectivity Map and Case Prism; and
5. a dedicated bilingual Ministerio Fiscal communications/proceedings working surface.

The bridge is a derived navigation and audit projection. It is not a competing communications register, a competing proceedings master, or a finding about the merits.

## Controlled denominator

- communication events classified: **296/296**;
- events with matter references: **117/117**;
- event-to-proceeding edges after canonical de-duplication: **139**;
- event-to-event sequence or transport edges: **84**;
- exact canonical Fiscalía files: **21**;
- controlled unresolved Fiscalía references: **3**;
- priority institutional chains: **9**;
- public exact proceedings with an express Case Prism coordinate: **43/97**;
- public exact proceedings still without a Case Prism coordinate: **54/97**.

All communication events have an explicit allocation state. Registration receipts or transport messages that cannot be allocated without stronger evidence remain `UNALLOCATED_FORMAL_REGISTRATION` or `UNALLOCATED_TRANSPORT`. A REGAGE identifier remains a supporting registration reference and is not promoted into a proceeding merely because it appears in correspondence.

## Three operational scopes

| Scope | Meaning | Non-inference rule |
|---|---|---|
| `INSIDE_JUDICIAL_PROCEEDING` | A Fiscal report, position, request or communication recorded against a judicial or other non-Fiscalía proceeding | Does not establish the content or outcome of any unlocated report or later act |
| `OUTSIDE_JUDICIAL_PROCEEDING` | A communication, complaint, decree, response or routing act in a distinct Fiscalía intake, investigation, governmental or inspection file | Does not merge the file with any judicial proceeding it may cite |
| `CROSS_FILE_BRIDGE` | One event expressly names both a Fiscalía file and a non-Fiscalía proceeding | Proves the stated reference only; not joinder, examination, agreement, causation or shared merits |

## Reciprocal implementation

- English specialist route: `en/public-prosecution-communications-proceedings/`
- Spanish specialist route: `es/fiscalia-comunicaciones-procedimientos/`
- stable specialist deep link: `#file=<Master_ID>`
- Master Register rows expose the linked event count and specialist route when present;
- Proceedings Map trace panels expose the same reciprocal route;
- specialist file views return to the canonical Master Register and linked judicial traces;
- Case Prism proposition P05 now includes the complete current public Fiscalía denominator: 21 exact files plus the three unresolved-reference objects.

## Source gates preserved

The implementation does not close or soften these known gaps:

1. `DIP 7/2026`, `DIP 12/2026` and `EG 58/2026` remain unresolved-reference identities;
2. the signed Fiscal report and later judicial act in `DP 1901/2026` remain not located;
3. the underlying act for `EG 6/2026` remains source-required;
4. the `EG 58/2026` discrete official act remains source-required;
5. six August receipts retain their destination-normalisation gate;
6. 81 mailbox routes remain `ROUTE_NOT_PUBLICLY_ATTESTED`;
7. 22 RedSARA records remain one aggregate-only unresolved batch; and
8. the `E.G. 745/2026` reposición remains prepared but not verified filed.

Registration is not receipt beyond the state proved by the receipt. Receipt is not examination. Chronology is not causation. Institutional possession is not personal knowledge, agreement, intent, wrongdoing, prevarication, criminality or liability.

## Deterministic controls

The following controls must remain green before publication:

```text
python scripts/build_fiscalia_proceedings_interconnectivity.py --check
python scripts/validate_fiscalia_proceedings_interconnectivity.py
python -m unittest -v scripts/test_build_fiscalia_proceedings_interconnectivity.py
python scripts/reconcile_institutional_communications.py --check
python scripts/validate_institutional_communications.py
python scripts/build_public_proceedings_projection.py --check
python scripts/build_proceedings_case_prism_v2.py --check
python scripts/build_proceedings_interlinkability_v1.py --check
python scripts/audit_master_proceedings_publication.py
python scripts/audit_proceedings_interconnectivity_map.py
node --check assets/fiscalia-proceedings-interconnectivity-20260831.js
node scripts/smoke_fiscalia_proceedings_interconnectivity.mjs
```

The browser smoke is part of the pull-request workflow and verifies both languages, the stable file hash, filters, unresolved-reference presentation, and reciprocal navigation from the Master Register and Proceedings Map.

## Publication state

This control records current-tree implementation only. A later immutable deployment closeout must record the pull request, merge commit, successful GitHub Pages run and live-route read-back. Until then, it must not be cited as proof that the updated pages are live.
