# Deletion audit — bidder name-only anonymisation control thread

**Audit date:** 20 August 2026  
**Repository:** `sbu001monterecco/por-derecho`  
**Pull request:** [#612 — Enforce bidder name-only anonymisation and preserve complete bid record](https://github.com/sbu001monterecco/por-derecho/pull/612)  
**Validated head:** `ab3654c3b091afbd0a260ca38e6d6aef25560ebd`  
**Merged main commit:** `3104d3ca4a70258d07c766f3ed48091bc62c93f1`  
**Thread-deletion verdict:** `DELETION_SAFE`

## Controlling rule

> **Only the third-party bidder’s name is anonymised. The bid, its amount, date, perimeter, terms, procedural treatment and every related fact and document remain fully visible.**

Spanish:

> **Únicamente se anonimiza el nombre del tercer oferente. La oferta, su importe, fecha, perímetro, términos, tratamiento procesal y todos los hechos y documentos relacionados permanecen íntegramente visibles.**

The rule, implementation, evidential boundaries and verification record no longer depend on the ChatGPT transcript.

## Repository implementation complete

PR #612 was opened as a draft, corrected after protective CI findings, marked ready only after every final-head check passed, and merged to `main` at the verified GitHub merge commit above.

The durable implementation includes:

- bilingual canonical and corrections pages;
- the shared publication/provenance module;
- a public-surface protected-name gate using a one-way digest;
- an independent positive bid-preservation gate;
- source, manifest, browser-render and live-edge workflows;
- the publication manifest and this deletion audit.

Temporary migration machinery was removed from the final tree.

## Material bid record preserved

The final public record retains:

- the proposal’s existence and date, 8 February 2021;
- EUR 14.8 million / 14,8 M€;
- the identified property perimeter;
- the EUR 14,713,880.31 / 14.713.880,31 € comparison point;
- procedural filing, authority, funds and 18 May 2021 licitation-treatment questions;
- the distinction between the third-party proposal and CAM’s eventual result;
- deed no. 457 dated 21 February 2022;
- EUR 13,168,082.02 / 13.168.082,02 € as stated debt consideration;
- the separate EUR 400,000 / 400.000 € non-mortgaged-assets line;
- the five-calendar-day court-communication obligation;
- the downstream Court, mandamiento, Registry, cancellation and final-account questions;
- the limitation that the present record does not automatically prove admission, funding, entitlement, wrongful exclusion or wrongdoing.

## Evidential and history boundaries

Private/archive, research, prompt and evidence-custody files may retain the original legal name and native source locators. Public anonymisation does not authorise destruction of private evidence.

No original court, notarial, banking, Registry, email, bid or other evidential source was deleted. No destructive Git-history rewrite was authorised or performed. This audit does not claim removal from historical Git objects, old commit messages, closed PR metadata, tags or releases.

## Final-head validation

All seven final-head checks passed:

| Check | Run | Result |
|---|---:|---|
| Public bidder name-only and bid-preservation | `32388468524` | PASS |
| Publication integrity | `32388468523` | PASS |
| Visual asset identity | `32388468478` | PASS |
| Off-GitHub preservation snapshot | `32388468545` | PASS |
| Adjudication provenance and cross-links | `32388468443` | PASS |
| Criminal-engineering information architecture | `32388468457` | PASS |
| Unitary public shell | `32388468399` | PASS |

The preservation run created artifact `9413864301`, containing the repository mirror, Git refs and objects, inventory, checksums, API metadata and rendered-site snapshot.

## Live public read-back

Post-merge workflow run `32388822697`, job `96489751126`, verified merged source `3104d3ca4a70258d07c766f3ed48091bc62c93f1`.

At propagation attempt 4:

- Spanish and English canonical pages returned HTTP 200 and every required marker;
- the shared module, loader and dedicated sitemap returned HTTP 200 and every required marker;
- the protected-name and positive bid-preservation gate passed across **12 public URLs**;
- all **12 rendered-browser assertions** passed, covering both canonical pages and ten reciprocal routes;
- commit status `pages-propagation/adjudicacion-2022` was published as `success`.

The live verifier therefore confirms both sides of the rule: the protected name is absent from the tested public perimeter, while the complete material bid record remains visible.

## Email custody complete and read back

The authenticated Gmail account self-delivered and read back three sent messages.

### Principal package

**Subject:** `Por Derecho — final bidder name-only repository update and deletion-safety package`  
**Sent:** 20 August 2026 at 16:00:47  
**Verified attachments:**

- `Por_Derecho_Bidder_Name_Only_Final_Implementation_20AUG2026.zip`
- `FINAL_IMPLEMENTATION_AND_DELETION_SAFETY_REPORT_20AUG2026.md`
- `FINAL_DELETION_VERDICT.txt`
- `PR-612-bidder-name-only.patch`
- `final-verification.json`
- `Por_Derecho_Full_Off_GitHub_Backup_PR612.parts.sha256`
- `por-derecho-off-github-backup-pr612.zip.sha256`

### Full preservation archive

The off-GitHub archive was split only to comply with email attachment limits:

1. `Por_Derecho_Full_Off_GitHub_Backup_PR612.zip.part-00` — `18,874,368` bytes — sent at 16:01:20.
2. `Por_Derecho_Full_Off_GitHub_Backup_PR612.zip.part-01` — `15,632,349` bytes — sent at 16:01:47.

Checksums and reassembly instructions are in the principal package. Gmail message identifiers remain private in the authenticated mailbox and are not committed to the public repository.

## Final safety determination

All unique instructions, implementation decisions, changed-file scope, evidential boundaries, validation results, live-publication proof, full backup, patch, inventory and email custody are preserved outside ChatGPT.

> **This ChatGPT thread is safe to delete.**

Deleting the conversation does **not** authorise deletion of:

- repository, branch, PR or commit history;
- GitHub Actions runs or preservation artifacts;
- the sent Gmail messages or attachments;
- public pages and correction records;
- private/native bid, court, notarial, banking, Registry or litigation evidence;
- open evidential tasks concerning filing, funds, authority, licitation treatment, deed implementation, Registry or final accounts.

## Final controlling statement

> **Only the third-party bidder’s name has been anonymised. The bid and the complete surrounding factual, documentary and procedural record remain preserved.**
