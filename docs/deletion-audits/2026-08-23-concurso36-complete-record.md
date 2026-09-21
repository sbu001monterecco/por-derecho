# Concurso 36/2012 — unitary publication and live-readback closeout

Date: 23 August 2026

Controlling label: **INVENTORY PARTIAL — CERTIFIED DOCKET OR RECORDS STILL MISSING**

Publication label: **PUBLICATION COMPLETE FOR THE IDENTIFIED PUBLIC-SAFE CORPUS — NOT THE WHOLE COURT FILE**

## 1. Outcome

The repository and bilingual website now expose a denominator-aware, source-addressable reconstruction of the presently identified Concurso 36/2012 record. Publication does not certify that every judicial act, court-office act, filing or communication in the official proceeding has been obtained.

The controlled catalogue contains:

- 127 canonical records: 72 historical, 50 specialist removal/remuneration records and 5 supplemental records;
- 40 judicial acts, 39 LAJ/court-office acts, 34 party filings, 2 party communications and 12 records in other controlled classes;
- 49 complete historical copies, 21 historical records with a missing complete copy and 2 with uncertain copy status;
- 50 page-complete public-safe specialist transcripts and 11 public-safe PDFs.

The repository preserves judge/LAJ acts, party filings, party communications, implementation records, later characterisations and missing evidence as separate classes. A party allegation is not a judicial finding; a court order is not proof of implementation; absence from the located corpus is not proof that a document never existed.

## 2. Publication chain

- Publication PR: [#870](https://github.com/sbu001monterecco/por-derecho/pull/870)
- Substantive merge: `86708da90a015d128d32ee681587f1ccdd323455`
- Initial exact Pages deployment: run `32667895000`, Pages deployment `#981`
- Post-deployment visibility repair PR: [#871](https://github.com/sbu001monterecco/por-derecho/pull/871)
- Visibility-repair merge: `30a60bc507e76792a565fe599afb0db92665149b`
- Post-deployment-hotfix Pages run: `32668816716`, Pages deployment `#982`
- Post-deployment-hotfix Pages artifact: `sha256:215fa8595233aac36fa1c01b8214e744d7ea707d7b07cfc1f4273f6ebdb20841`
- Live-closeout PR: [#872](https://github.com/sbu001monterecco/por-derecho/pull/872)
- Live-closeout merge: `6793691a8e141b1842b0156e45b6522b9fb0126d`
- Exact closeout Pages deployment: run `32670629109`, Pages deployment `#983`
- Exact closeout Pages artifact: `sha256:461795a850201c648e2ddf211d190128fa1497bdd6693c41840df0180aae2cfc`
- Exact public-corpus verifier: run `32670629833`, job `97270843044`, `85/85 PASS`
- Exact-verifier artifact: `sha256:cf236161908a5bc866e6c91adc80fde2381be323ad344157c6aa3d39bf1cae2a`
- Permanent production smoke: run `32670629825`, job `97270843093`, `42/42 PASS`
- Production-smoke artifact: `sha256:b7e80708a930a0a84ed553bc941be0a177977e67e28b30eb262db1f5a72404c9`

PR #870 passed 29/29 pre-merge checks. PR #871 passed 19/19 pre-merge checks. PR #872 passed all 12 triggered workflow suites. After deployment, the closeout workflow first attested that Pages run #983 had `head_sha` equal to `6793691a…`; its first public pass saw 84/85 surfaces while one edge object settled, and its second no-cache pass verified 85/85 exact bytes. The permanent monitor then passed 42/42 routes. The earlier San Telmo public-edge and 26-placement source-of-funds controls also remain green after propagation.

## 3. Controlling source and prompt

- Unitary digest: `archive/CONCURSO36_COMPLETE_RECORD_EXECUTION_DIGEST_23AUG2026.md`
- Judge/LAJ/communications register: `archive/JUDGE_LAJ_COMMUNICATIONS_REGISTER_CONCURSO36.md`
- Machine catalogue: `assets/data/concurso36-complete-record-v1.json`
- Complete specialist corpus: `assets/data/concurso36-autos-fulltext-v1.json`
- Improved acquisition/digitisation/publication prompt: `archive/prompts/CONCURSO36_COMPLETE_JUDICIAL_PARTY_RECORD_ACQUISITION_DIGITISATION_PUBLICATION_PROMPT_23AUG2026.md`
- Exact deployment verifier: `scripts/verify_concurso36_complete_record_live.py`

The prompt is deliberately read-only for connected sources. It prohibits sending, replying, forwarding, filing or using self-email as a transfer mechanism. Any production request is a draft until separately authorised and filed through the legally correct channel.

## 4. What the live verifier proves

The closeout verifier binds 85 public surfaces byte-for-byte to the checked-out Git tree:

- 18 canonical bilingual HTML routes;
- 4 JSON control manifests/catalogues;
- 50 specialist full-text transcripts;
- 2 security-request transcripts; and
- 11 public-safe PDFs.

It also rechecks the 127/50/10 controlled counts, rejects duplicate public target paths, preserves the inventory-partial label, prohibits a complete-court-file claim, and validates the security PDF hash and no-email boundary. On `main`, its workflow first requires a successful GitHub Pages run whose `head_sha` equals the exact merge SHA. The permanent 42-route production monitor separately checks all canonical bilingual reader routes every two hours and on relevant source changes.

The improved umbrella prompt additionally prevents a null search from becoming a finding of silence or knowledge, preserves native message/thread/attachment evidence states, screens possible privilege before substantive use, and requires an atomic versioned migration whenever new evidence changes the frozen `127 / 50 / 12 / 85` release counts.

## 5. Highest-priority evidence actions

### P0 — obtain the official denominator and procedural chains

1. Request the certified chronological docket/index for every section and incident of Concurso 36/2012. Reconcile every official entry to a catalogue record; create a new gap record for each unmatched entry.
2. Obtain complete filing, service, LexNET/ATLANTE, notification and finality chains for every dispositive judicial or LAJ act. Preserve native files and receipts before preparing any public derivative.
3. Obtain the 20 January 2026 preliminary-hearing minutes and recording, and the 25 July 2023 hearing minutes, audiovisual index and evidence rulings.
4. Obtain the complete 18 May 2021 competing-offer/hearing record, including offers, bonds, minutes, audio/video, objections and the property-by-property decision basis.
5. Obtain the official reparto/allocation record for the 18 June 2026 AC complaint associated with daily intake reference 22: NIG, destination organ, admission/status and later acts. Keep reference 24 separate.
6. Recover the 15 current P0 historical missing-copy IDs: `E004`, `E053`, `E056–E058`, `E060–E068` and `E071`.

### P1 — close title, credit, money and implementation bridges

7. Obtain the underlying AP complaint 375/22 order and reconcile every July 2022 date layer.
8. Obtain the Protocol 457 five-day court return, Registry presentation trail and complete property-by-property implementation/accounting.
9. Obtain the complete PH122-to-CAM assignment deed, notice, consideration and final debt bridge; keep the controlled creditor-substitution order date at 15 February 2018 unless a distinct authenticated act is re-inspected.
10. Reconstruct the EUR 400,000 title, cash, restitution and accounting chain, allocated to the legally correct claimant and without double recovery.
11. Obtain later insolvency-administrator reports, estate ledgers, annual/final accounts and the conclusion order.
12. Recover the six P1 historical missing-copy IDs `E015`, `E026`, `E027`, `E031`, `E034`, `E045`; authenticate uncertain `E019` and `E022`.
13. Obtain court-stamped copies and independent receipts for `R07`, `R08`, `R24`, `R25` and `F08`; preserve the narrower corroboration recorded for `R17`, `R23` and `R27`.

### P2 — resolve pending merits and native communications

14. Track the merits outcomes in RPL 421/2026 and accumulated RPL 3304/2025 plus 3319/2025. A standing disposition must not be reported as a merits decision.
15. Preserve native RFC822/EML messages, headers, attachments, delivery/receipt records and filing acknowledgements for each relevant party communication; publish only privacy-safe derivatives whose evidential value requires publication.
16. Maintain actor-specific analysis of the insolvency administrator through the removal application, fee claim, Decanato daily intake 22, DP 1901/2026, DP 1956/2026, DIP 80/2026 and their actual amendments or cross-evidence. Do not merge those lanes without an official joinder/reparto act.

## 6. Legal and evidential boundaries

- The removal application and fee claim must remain distinct proceedings.
- Decisions based on standing or procedure do not decide the unexamined merits.
- The 2018 provisional dismissal and appellate confirmation remain visible beside later criminal allegations.
- Criminal guilt, knowing administrator cooperation and omissionary judicial prevarication are not adjudicated facts in this publication.
- Laura Isabel and Laura Patricia/LPAM remain distinct identities unless authenticated primary evidence resolves a specific reference.
- LPB estate assets remain legally distinct from CEXP, Matkator and other third-party rights.
- No family, professional or commercial association is treated as proof of instruction, knowledge or common purpose.

## 7. Deletion-safety meaning

`DELETION_SAFE_WITH_OPEN_EVIDENCE` is now earned for the identified public-safe corpus: the exact merge was deployed, 85/85 controlled surfaces matched repository bytes, and 42/42 production routes passed. It means that the publication, provenance, validation and remaining gaps are recoverable from Git and the live site. It does not mean that the judicial file, evidence investigation, appeals, recovery claims or criminal allegations are closed.

No email was sent as part of this publication or closeout.
