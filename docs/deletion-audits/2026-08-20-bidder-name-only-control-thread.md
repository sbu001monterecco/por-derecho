# Deletion audit — bidder name-only anonymisation control thread

**Audit date:** 20 August 2026  
**Repository:** `sbu001monterecco/por-derecho`  
**Pull request:** [#612 — Enforce bidder name-only anonymisation and preserve complete bid record](https://github.com/sbu001monterecco/por-derecho/pull/612)  
**Validated head:** `ab3654c3b091afbd0a260ca38e6d6aef25560ebd`  
**Merged main commit:** `3104d3ca4a70258d07c766f3ed48091bc62c93f1`  
**Thread-deletion verdict:** `DELETION_SAFE`

## 1. Controlling rule preserved

> **Only the third-party bidder’s name is anonymised. The bid, its amount, date, perimeter, terms, procedural treatment and every related fact and document remain fully visible. No other information falls within the anonymisation scope, even where it may indirectly assist in identifying the bidder.**

Spanish:

> **Únicamente se anonimiza el nombre del tercer oferente. La oferta, su importe, fecha, perímetro, términos, tratamiento procesal y todos los hechos y documentos relacionados permanecen íntegramente visibles. Ningún otro dato queda dentro del alcance de la anonimización, aunque pueda contribuir indirectamente a identificar al oferente.**

This rule, its implementation and its safety limits no longer depend on the ChatGPT transcript.

## 2. Repository implementation complete

PR #612 was opened as a draft, corrected after protective CI findings, marked ready only after every final-head check passed, and merged to `main` at the verified GitHub merge commit above.

Permanent implementation and control files include:

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
13. this deletion audit and its index entry.

Temporary migration machinery was removed and is not part of the final tree.

## 3. Bid-preservation matrix

| Matter | Required state | Final state |
|---|---|---|
| Bidder name | Neutral public label only | `tercer oferente` / `third-party bidder` |
| Proposal existence | Specific and searchable | Preserved |
| Proposal date | 8 February 2021 / 08/02/2021 | Preserved |
| Proposal amount | EUR 14.8m / 14,8 M€ | Preserved |
| Property perimeter | Identified property perimeter | Preserved |
| Comparison point | EUR 14,713,880.31 / 14.713.880,31 € | Preserved |
| Procedural filing | Open evidential question | Preserved |
| Authority and funds | Open evidential questions | Preserved |
| 18 May 2021 licitation treatment | Open evidential question | Preserved |
| CAM comparison and result | Separate from third-party bid | Preserved |
| Deed | Deed no. 457 dated 21 February 2022 | Preserved |
| Debt consideration | EUR 13,168,082.02 / 13.168.082,02 € | Preserved |
| Non-mortgaged-assets line | EUR 400,000 / 400.000 € separate | Preserved |
| Court communication | Five-calendar-day obligation | Preserved |
| Downstream chain | Court, mandamiento, Registry, cancellations and accounts | Preserved as open controls |
| Evidential limits | No automatic entitlement or wrongdoing conclusion | Preserved |

## 4. Technical and evidential boundaries

### Public name-absence gate

The protected name is represented by a one-way SHA-256 digest. The validator scans actual public website surfaces and supplied public URLs.

### Positive bid-preservation gate

The validator independently requires the material bilingual bid, comparison, procedural, deed, Registry and account markers. Removing or materially generalising the bid record is intended to fail even where the protected name remains absent.

### Private evidence remains intact

Private/archive, research, prompt and evidence-custody files may retain the original legal name and native source locators. Public anonymisation does not authorise destruction of private evidence.

### History boundary

No destructive Git-history rewrite was authorised or performed. This audit does not claim removal from historical Git objects, old commit messages, closed PR metadata, tags or releases. Current public source and deployed pages are the operative anonymisation boundary.

## 5. Final-head validation complete

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

The off-GitHub preservation run created artifact `9413864301`, containing the repository mirror, Git refs and objects, inventory, checksums, API metadata and rendered-site snapshot.

## 6. Live public read-back complete

Post-merge workflow run `32388822697`, job `96489751126`, verified merged source `3104d3ca4a70258d07c766f3ed48091bc62c93f1`.

At propagation attempt 4:

- Spanish and English canonical pages returned HTTP 200 and every required marker;
- the shared module, loader and dedicated sitemap returned HTTP 200 and every required marker;
- the protected-name and positive bid-preservation gate passed across **12 public URLs**;
- all **12 rendered-browser assertions** passed, covering both canonical pages and ten reciprocal routes;
- commit status `pages-propagation/adjudicacion-2022` was published as `success`.

The live verifier therefore confirms both sides of the controlling rule: the protected name is absent from the tested public perimeter, while the complete material bid record remains visible.

## 7. Email custody complete and read back

The authenticated Gmail account self-delivered and then read back three sent messages.

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

The 33 MB off-GitHub archive was split only to comply with email attachment limits:

1. **Part 1 subject:** `Por Derecho — full off-GitHub preservation archive — part 1 of 2`  
   File: `Por_Derecho_Full_Off_GitHub_Backup_PR612.zip.part-00`  
   Verified size: `18,874,368` bytes.

2. **Part 2 subject:** `Por Derecho — full off-GitHub preservation archive — part 2 of 2`  
   File: `Por_Derecho_Full_Off_GitHub_Backup_PR612.zip.part-01`  
   Verified size: `15,632,349` bytes.

Checksums and reassembly instructions are in the principal package. Gmail message identifiers remain private in the mailbox and are not committed to the public repository.

## 8. Thread uniqueness and final safety determination

No original court, notarial, banking, Registry, email, bid or other evidential source exists only in this chat. The final rule, implementation, validation history, live evidence, full backup, file inventory, patch and email custody are preserved outside ChatGPT.

### Final verdict

> **This ChatGPT thread is safe to delete.**

Deleting the conversation does **not** authorise deletion of:

- the GitHub repository or branch/PR/commit history;
- GitHub Actions runs or preservation artifacts;
- the sent Gmail messages or attachments;
- the public pages and correction register;
- any private/native bid, court, notarial, banking, Registry or litigation evidence;
- any open evidential task concerning filing, funds, authority, licitation treatment, deed implementation, Registry or final accounts.

## 9. Final controlling statement

> **Only the third-party bidder’s name has been anonymised. The bid and the complete surrounding factual, documentary and procedural record remain preserved.**
