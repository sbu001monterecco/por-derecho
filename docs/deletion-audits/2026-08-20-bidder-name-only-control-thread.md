# Deletion audit — bidder name-only anonymisation control thread

**Audit date:** 20 August 2026  
**Repository:** `sbu001monterecco/por-derecho`  
**Baseline audited:** `main` at `27aa30b462590b553118612ed7c15cb061109d89`  
**Implementation branch:** `chore/bidder-name-only-control-2026-08-20`  
**Thread-deletion verdict:** `SAFE WITH REMOTE BRANCH PRESERVED — PUBLICATION/CI STILL PENDING`

## 1. Scope of this thread

This thread did not introduce a new evidential document. Its unique work product was a governance and implementation correction to the existing public treatment of the documented third-party proposal dated 8 February 2021.

The controlling instruction is now preserved outside ChatGPT:

> **Only the third-party bidder’s name is anonymised. The bid, its amount, date, perimeter, terms, procedural treatment and every related fact and document remain fully visible. No other information falls within the anonymisation scope, even where it may indirectly assist in identifying the bidder.**

Spanish controlling formulation:

> **Únicamente se anonimiza el nombre del tercer oferente. La oferta, su importe, fecha, perímetro, términos, tratamiento procesal y todos los hechos y documentos relacionados permanecen íntegramente visibles. Ningún otro dato queda dentro del alcance de la anonimización, aunque pueda contribuir indirectamente a identificar al oferente.**

## 2. Durable implementation preserved in GitHub

Before this deletion-audit record was added, the branch was exactly 18 commits ahead of the audited `main` baseline, zero commits behind, and contained 11 permanent changed files. Temporary one-time migration files had been removed and therefore did not appear in the net diff.

Permanent implementation files:

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

The implementation is held on a remote GitHub branch and is therefore independent of this ChatGPT thread.

## 3. Bid-preservation matrix

| Matter | Required state | Branch state |
|---|---|---|
| Bidder name | Replaced by a neutral label only | Preserved as `tercer oferente` / `third-party bidder` |
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

## 4. Technical controls now preserved

### Name-absence gate

The protected name remains represented by a one-way SHA-256 digest. The validator scans the current repository text tree, relevant paths and any supplied public URLs. The protected name is not placed in plaintext in the validator, workflow, report or test fixture.

### Bid-preservation gate

The validator independently requires positive bilingual markers for:

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

The rewrite utility is explicitly a name-token substitution tool. It is not a paragraph, sentence, event or evidential-content redaction tool. It preserves line structure and surrounding content except for the protected token and a strictly necessary grammatical substitution.

## 5. Audit actually performed

The following checks were completed against the remote branch:

- current `main` baseline was re-established before implementation;
- the final implementation branch was compared against that exact baseline;
- the net implementation diff contained only the 11 permanent files listed above;
- no one-time migration script or one-time migration workflow remained in the net diff;
- both canonical pages were read back from the branch and checked for the date, amount, perimeter, comparison figure, procedural questions, deed, separate EUR 400,000 line, court-notification and downstream controls;
- both corrections registers were checked for the express statement that only the bidder’s name remains anonymised and the bid remains visible;
- the shared bilingual JavaScript module was checked for the same rule and corrected so its raw-source marker is searchable without an escaped-apostrophe mismatch;
- the validator was checked to prevent self-matching of its own superseded-wording definitions;
- workflow labels and live-source markers were aligned with name-only anonymisation and bid preservation.

## 6. Validation boundary

No pull request was opened and nothing was merged to `main`, because branch push, pull-request creation and merge are separate publication actions. Therefore:

- full pull-request CI has **not** run;
- the updated full-tree gate has **not** produced a GitHub Actions result for this branch;
- GitHub Pages has **not** deployed these branch changes;
- no live public read-back can yet be claimed;
- no historical Git-object, commit-message, pull-request-metadata, tag or release clearance is claimed;
- no destructive Git-history rewrite is authorised.

These are activation and history-audit boundaries, not missing thread content.

## 7. Thread uniqueness and deletion safety

All unique instructions, implementation decisions, changed-file scope, preservation requirements, validation architecture, limitations and next steps from this thread are now preserved in the remote repository branch and in this audit.

No original court, notarial, banking, Registry, email or other evidential file was supplied only inside this thread. Deleting the ChatGPT conversation therefore does not delete or alter the underlying evidence.

### Verdict

> **This ChatGPT thread is safe to delete provided the remote branch `chore/bidder-name-only-control-2026-08-20` is retained until the change is reviewed, merged or otherwise durably archived.**

Deletion of the thread must not be described as publication completion. The branch is implemented and reviewable, but `main`, CI and the live website remain unchanged until separately activated.

## 8. Remaining activation steps

1. Open one draft pull request from `chore/bidder-name-only-control-2026-08-20` to `main` when separately authorised.
2. Run the full repository, adjudication-provenance, browser-render and bidder name-only/bid-preservation checks.
3. Review the exact diff and merge only after all required checks pass.
4. Run the existing public-edge verifier after GitHub Pages propagation.
5. Record the PR number, merge SHA, workflow runs and live read-back in the publication manifest.
6. Keep any Git-history audit separate; do not rewrite history without a distinct preservation and authorisation process.

## 9. Final controlling statement

> **Only the third-party bidder’s name has been anonymised. The bid and the complete surrounding factual, documentary and procedural record remain preserved.**
