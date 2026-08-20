# Deletion audit — bidder name-only anonymisation control thread

**Audit date:** 20 August 2026  
**Repository:** `sbu001monterecco/por-derecho`  
**Current base audited:** `main` at `2599fa333b501b8a5ffdf7c7e16784df352f816a`  
**Implementation branch:** `chore/bidder-name-only-control-2026-08-20`  
**Pull request:** [#612 — Enforce bidder name-only anonymisation and preserve complete bid record](https://github.com/sbu001monterecco/por-derecho/pull/612)  
**Current thread-deletion verdict:** `NOT YET SAFE — FINAL MERGE, LIVE READ-BACK AND EMAIL CUSTODY REQUIRED`

## 1. Scope of this thread

This thread did not introduce a new underlying court, notarial, banking, Registry or transactional source. Its unique work product is a governance and implementation correction to the public treatment of the documented third-party proposal dated 8 February 2021.

The controlling instruction is preserved outside ChatGPT:

> **Only the third-party bidder’s name is anonymised. The bid, its amount, date, perimeter, terms, procedural treatment and every related fact and document remain fully visible. No other information falls within the anonymisation scope, even where it may indirectly assist in identifying the bidder.**

Spanish controlling formulation:

> **Únicamente se anonimiza el nombre del tercer oferente. La oferta, su importe, fecha, perímetro, términos, tratamiento procesal y todos los hechos y documentos relacionados permanecen íntegramente visibles. Ningún otro dato queda dentro del alcance de la anonimización, aunque pueda contribuir indirectamente a identificar al oferente.**

## 2. Durable implementation preserved in GitHub

The implementation is preserved on the remote branch and in PR #612. The PR is mergeable against the current `main`; the five commits added to `main` after the branch was created affect separate files and are retained by the synthetic merge result.

Permanent implementation and control files:

1. `.github/workflows/public-bidder-anonymisation.yml`
2. `.github/workflows/validate-adjudicacion-provenance.yml`
3. `.github/workflows/verify-adjudicacion-2022-live.yml`
4. `archive/THIRD_PARTY_BIDDER_PUBLIC_ANONYMISATION_CONTROL_20AUG2026.md`
5. `assets/adjudicacion-provenance-cross-site-20260819.js`
6. `es/adjudicacion-2022-reconstruccion-documental/index.html`
7. `en/2022-adjudication-documentary-reconstruction/index.html`
8. `es/correcciones-control-versiones/index.html`
9. `en/corrections-version-control/index.html`
10. `scripts/rewrite_public_bidder_anonymisation.py`
11. `scripts/validate_public_bidder_anonymisation.py`
12. `publication-manifests/bidder-name-only-control-20260820.json`
13. `docs/deletion-audits/2026-08-20-bidder-name-only-control-thread.md`
14. `docs/deletion-audits/README.md`

Temporary one-time migration machinery was removed before PR publication and does not appear in the net changed-file set.

## 3. Bid-preservation matrix

| Matter | Required state | PR #612 state |
|---|---|---|
| Bidder name | Neutral public label only | Preserved as `tercer oferente` / `third-party bidder` |
| Proposal existence | Specific and searchable | Preserved |
| Proposal date | 8 February 2021 / 08/02/2021 | Preserved |
| Proposal amount | EUR 14.8m / 14,8 M€ | Preserved |
| Property perimeter | Identified property perimeter | Preserved |
| Comparison point | EUR 14,713,880.31 / 14.713.880,31 € | Preserved |
| Procedural filing | Open evidential question | Preserved |
| Corporate authority and funds | Open evidential questions | Preserved |
| 18 May 2021 licitation treatment | Open evidential question | Preserved |
| CAM comparison and eventual result | Distinct from the third-party bid | Preserved |
| Deed | Deed no. 457 dated 21 February 2022 | Preserved |
| Debt consideration | EUR 13,168,082.02 / 13.168.082,02 € | Preserved |
| Non-mortgaged-assets line | EUR 400,000 / 400.000 € kept separate | Preserved |
| Court communication | Five-calendar-day obligation | Preserved |
| Downstream chain | Court, mandamiento, Registry, cancellations, accounting and final accounts | Preserved as open controls |
| Evidential limits | No automatic admission, funding, entitlement, wrongful exclusion or wrongdoing conclusion | Preserved |

## 4. Technical controls preserved

### Public name-absence gate

The protected name is represented by a one-way SHA-256 digest. The validator scans only actual public website surfaces: the `es/`, `en/` and `assets/` trees, selected root publication files and explicitly supplied public URLs.

The gate deliberately excludes private/archive, research, prompt and evidence-custody files. Those systems may retain the original legal name and native source references for evidential retrieval. The public anonymisation control must not destroy private evidence.

### Positive bid-preservation gate

The validator independently requires bilingual markers for:

- date and amount;
- identified perimeter;
- EUR 14,713,880.31 comparison point;
- procedural filing, authority/funds and licitation-treatment questions;
- deed no. 457;
- EUR 13,168,082.02 and EUR 400,000;
- the five-day court-communication trail;
- Registry and final-account questions;
- express name-only wording in both canonical pages and both corrections registers;
- equivalent name-only wording in the shared JavaScript publication module.

Deletion or material generalisation of a required bid fact is therefore intended to fail independently of the name-absence check.

### Rewrite boundary

The rewrite utility is a protected-name-token substitution tool. It is not a paragraph, sentence, event or evidential-content redaction tool. It preserves the surrounding bid record and line structure.

### History boundary

This work does not claim that the protected name has been removed from historical Git objects, old commit messages, closed PR metadata, tags or releases. No destructive Git-history rewrite has been authorised. Current public source and deployed public pages are the operative anonymisation boundary.

## 5. PR and validation history

PR #612 was opened as a draft against `main` and was confirmed mergeable.

The initial PR checks correctly exposed two configuration defects rather than a substantive loss of the bid record:

1. the first version of the validator scanned private archival evidence, where the original legal name must remain recoverable; and
2. the new publication manifest used a non-standard state and omitted `expected_routes`.

Those defects were corrected on the PR branch:

- commit `4e5ea47226dc226b55cef8aa0e952dde13c6f879` narrowed the name gate to public publication surfaces while expressly preserving private evidence;
- commit `e0e1b90438da3ffb6a688d94ec857267fe543bef` aligned the manifest with the repository publication-state schema and declared bilingual route parity.

Replacement PR checks must be green before the draft is marked ready or merged. The final run IDs and conclusions, merge SHA and deployed read-back are to be recorded in PR #612’s durable closeout metadata.

## 6. Current deletion boundary

The unique instructions, implementation decisions, changed-file scope, preservation requirements, limitations and activation history are no longer held only in ChatGPT. They are preserved in the remote branch, PR #612, this audit and the publication manifest.

No original evidential file was supplied only inside this thread. Deleting the ChatGPT conversation would therefore not delete the underlying bid or any primary evidence.

However, the user has requested a fully completed repository update and email custody. The final deletion gate is therefore stricter than mere remote-branch preservation.

### Current verdict

> **Do not delete this thread yet. It becomes deletion-safe only after PR #612 is merged, the deployed Spanish and English pages and shared publication module pass public-edge read-back, and the complete final file package is sent to the authenticated account by email.**

## 7. Final activation and closeout steps

1. Obtain green replacement checks on the final PR head.
2. Mark PR #612 ready for review.
3. Merge PR #612 to `main` using the verified final head SHA.
4. Confirm the post-merge workflows and GitHub Pages propagation.
5. Read back the Spanish and English canonical pages, both corrections pages and the shared JavaScript module, including protected-name absence and all positive bid markers.
6. Generate the final implementation, workflow, live-readback and deletion-safety package.
7. Send the complete package by Gmail self-delivery and verify the sent message and attachments.
8. Add final merge, live-verification and email-custody evidence to PR #612’s durable closeout metadata.

## 8. Final controlling statement

> **Only the third-party bidder’s name is anonymised. The bid and the complete surrounding factual, documentary and procedural record remain preserved.**
