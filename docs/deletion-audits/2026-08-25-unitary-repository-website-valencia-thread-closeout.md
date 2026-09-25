# Deletion audit — unitary repository/site digest and Valencia chronology closeout

**Audit date:** 25 August 2026

**Repository:** `sbu001monterecco/por-derecho`

**Current-main baseline independently checked:** `bd701e0c79fe910d02f92f1f57ef3cdcd1bed718`

**Scope:** the unitary repository/website redigest, the Valencia-hearing correction, subsequent repository growth through the pre-7 June 2018 ONA exit dossier, and the final deletion-safety review of the originating ChatGPT thread.

**This record changes no public case proposition, HTML route, evidence classification or private-source custody state.**

## Verdict

**DELETION-SAFE WITH OPEN EVIDENCE AND GOVERNANCE REMEDIATION, once this record is present on `main`.**

The material reasoning, correction, implementation state, limitations and next actions from the thread are recoverable without retaining the conversation. This is not a claim that the evidence corpus is complete, that every operational record is current, that every open pull request is disposable, or that private-source custody and disaster recovery are complete.

## Exact action states

| Object | Action | State | Verification | Open condition |
|---|---|---|---|---|
| Valencia hearing chronology | Corrected repository and public pages | `MERGED → DEPLOYED → EDGE_VERIFIED` | PRs #957/#958; `publication-manifests/valencia-hearing-chronology-correction-20260824.json`; fresh Valencia validator pass; fresh whole-site readback | Obtain and ingest any later signed order or citation changing the listed hearing |
| Current repository/site | Re-digested as one evidential and publication system | `ANALYSED → VERIFIED` | Current-main SHA above; source validators; 503/503 live HTML hash parity | Open evidence and governance items below |
| Public case pages in this closeout | Reviewed | `EXISTING_PAGE_REVIEWED_NO_CHANGE` | Clean comparison before this audit-only change | No case-page publication was authorised or required in this closeout |
| Email, filing and third-party communication | Not undertaken | `NO_ACTION_REQUIRED — NOT SENT` | No send, draft, calendar or filing action in this audit | Separate exact authority remains required for any later external action |

## Locked Valencia chronology

- Original hearing: **6 November 2025 at 10:00 Europe/Madrid**.
- Short-notice event: the opposing expert reported a cancelled flight on the evening before; Aweswell did not oppose suspension because it wished to question him personally.
- Current relisted hearing: **28 January 2027 at 10:00 Europe/Madrid**.
- Proceeding: Juzgado de Primera Instancia nº 27 de Valencia, ORD 1859/2023-9, N.I.G. `46250-42-1-2023-0049579`.
- Status: pending and contested; no merits judgment or adjudicated recovery has been located.
- The former **October 2026 at noon** entry is a superseded repository transcription error, not a second postponement.
- The correspondence does not establish tactical delay. Native correspondence and the unredacted court record remain outside public Git.

The machine-readable authority is `assets/data/valencia-hearing-status-v1.json`. The dedicated validator rejects the superseded date, wrong N.I.G. and wrong court label across the repository.

## Unitary repository and website finding

The public system now presents a substantially coherent recovery-led chain:

1. fragmented civil title and a commercially integrated hotel;
2. separate LPB, Matkator/third-party, CEXP/operation, Community and Aweswell/cross-border perimeters;
3. Community debt, voting, custody and litigation as an authority mechanism requiring document-by-document verification;
4. enforcement pressure, LPB's defensive filing and the court's insolvency declaration as separate legal questions;
5. creditor assignment, material control, property acquisition, insolvency implementation, hotel operation and later finance as connected but non-collapsible lanes;
6. actor-specific private conduct, separate Insolvency Administrator acts/omissions and separate judicial acts/omissions;
7. recovery of property, possession, operating rights, income, estate value, direct investment value, causes of action, damages, interest and equivalent value for the correct right-holder without double counting.

The new bilingual pre-7 June 2018 ONA dossier materially strengthens the counterfactual and causation lane. It records operator, acquisition, bridge, security, due-diligence and court-exit work active by the close of 6 June 2018. Its evidential boundary must remain visible: signed or active routes were conditional; they were not necessarily unconditional facilities, completed funding, a completed sale or a court-approved exit.

The operational matter-identity and legal-professional registers materially improve person/entity/capacity separation. IDs and graph links organise evidence; they do not transfer knowledge, intent, control or liability.

## Fresh verification results

### Git and deployment

- Current `main`: `bd701e0c79fe910d02f92f1f57ef3cdcd1bed718`.
- Latest Pages deployment for that exact SHA: workflow run `32904408968`, successful.
- Tracked source: 2,717 files, including 503 HTML files, 488 route `index.html` files, 89 workflows, 57 publication manifests and 44 sitemap XML files.
- Live parity: **503/503 HTML files returned HTTP 200 and matched current source SHA-256 byte for byte**.

### Source gates

- Repository preservation: pass — 2,717 tracked files and the protected actor/institutional presentation retained.
- Audience experience: pass — 488 HTML pages, 6,374 internal links and 1,072 public files inspected by the repository gate.
- Valencia chronology: pass across 2,225 repository text files.
- Operational items, unitary criminal reconstruction, private-source/statement/OSINT governance, professional register and operational identity registry: pass.
- Publication integrity: pass, but its pre-audit run inspected zero changed files. This closeout therefore relies additionally on the whole-site independent hash readback and must run the change-aware gates again for its own diff.

## Open P0/P1 work that must survive deletion

### P0 · Public/private boundary remediation

The repository is public and Pages serves archive/operational material directly. Fresh HTTP probes returned 200 for an archive CSV containing provider-specific Gmail message identifiers, an unsent Cuatrecasas email draft, operational JSON snapshots and an encoded transcript derivative. `robots.txt` allows crawling generally.

Required treatment:

1. preserve any evidentially necessary native/private copy outside public Git before remediation;
2. remove provider-specific message identifiers, private locators, recipient identities, private-source bodies, privileged material and unsent correspondence from current public surfaces where they breach the current policy;
3. distinguish intentionally public, redacted derivatives from material that was merely encoded or placed under `archive/`;
4. address Git-history retention deliberately rather than claiming that a current-tree deletion erases prior publication; and
5. make changed-file privacy checks hard for new material while legacy remediation proceeds in a controlled lane.

This audit records paths and categories, not the private values themselves.

### P0 · Operational truth drift

`ops/CURRENT_STATE.json`, `ops/PRODUCTION_STATUS.json` and `ops/LAST_KNOWN_GOOD.json` still centre PR #922 and SHA `ed98b0ac…`, while current `main` and the live host are at the SHA stated above. The open-PR snapshot says 31; the fresh count is 34.

The status layer must be rebuilt as one current append-only release register or generated snapshot. A historical last-known-good anchor may remain, but it must not masquerade as current production truth.

### P0 · DIP 80 status contradiction

The fourteen dedicated ES/EN living-casebook routes and later Ponente/Rapporteur records are present on `main` and live. Repository closeout records describe PRs #525/#528/#529/#538/#541/#542 and a successful public-edge verification. Nevertheless:

- `publication-manifests/icalpa-dip80-open-kimono-20260818.json` still says `BLOCKED_RECOVERY`; and
- `OPS-2026-002` still describes the casebook as unpublished and blocked on old PR #366.

Reconcile the manifest, operational item and supersession lineage against the ordinary source now on `main`. Do not delete the old failed-materialisation history; mark it superseded and identify the later successful route.

### P0 · Structured recovery denominator remains incomplete

The proposed `LPB-01` through `LPB-07` causation/recovery register has not been materialised as a structured dataset. The public narrative therefore still lacks one reproducible bridge covering:

- original loan, swap, later finance and enforcement;
- credit ownership, servicer, procedural standing and exact legal person by date;
- definitive credit, the EUR 13,168,082.02 transaction function and the separate EUR 400,000 branch;
- consideration, payment, proceeds, fees, creditor payments, income/fruits and any surplus;
- actual-versus-counterfactual monthly cash flow;
- 262-property title, possession, operation and income;
- claimant, defendant, legal basis, forum, remedy and no-double-counting allocation.

Publish quantified conclusions only when the calculation and source denominator are reproducible.

### P1 · Discovery and canonicalisation

Fresh sitemap analysis found:

- 456 indexable HTML files;
- 135 indexable files absent from every sitemap;
- 33 HTML files without a canonical link;
- 10 duplicate-canonical groups; and
- 8 duplicate-title groups.

Each route needs an explicit decision: canonical/indexable and in a sitemap, or deliberately `noindex` with a stable supporting role. The new pre-7 June ONA pair is live but currently among the sitemap omissions.

### P1 · Runtime consolidation

`assets/site.js` can statically reach 130 JavaScript modules totalling approximately 1.77 MB. This layered loader preserves many historical fixes but creates order, duplication and regression risk. Consolidate through one declarative route/module manifest without removing routes, locked actor presentation, evidential qualifications or sent-link compatibility.

### P1 · Open pull-request triage

Fresh inventory: 34 open PRs, 19 drafts. Local current-main merge analysis found 26 conflicting and 8 mechanically clean; every open PR is behind `main`. No PR should be merged wholesale merely because Git reports a clean merge.

For each PR: close as superseded, extract a unique validated delta onto current `main`, or preserve as historical evidence. PR #1016 is recent and mechanically clean but still requires current-main review and its own evidence/privacy/identity checks.

## Deletion-safety dimensions

| Dimension | Result |
|---|---|
| `THREAD_REASONING_CONTINUITY` | **Safe after this audit is on `main`** — the unitary findings, corrections, limitations and open programme are preserved here and in the cited canonical controls |
| `IMPLEMENTATION_STATE_CONTINUITY` | **Safe** — Valencia states and the current read-only audit state are explicit |
| `PRIMARY_EVIDENCE_COMPLETENESS` | **Open** — court, banking, accounting, property, income, ONA-condition and private-mail sources remain incomplete |
| `LIVE_PUBLICATION_VERIFICATION` | **Verified for current HTML** — 503/503 exact source/live matches at the audited SHA |
| `COMMUNICATION_VERIFICATION` | **Not applicable to this audit** — no email, message, filing or calendar action occurred |
| `CUSTODY_RESILIENCE` | **Qualified** — public-safe derivatives and source maps do not substitute for native private evidence and independent custody |
| `DISASTER_RECOVERY_SAFETY` | **Not re-certified here** — the continuing backup control remains separate |

## Canonical future-thread start order

1. `AGENTS.md`.
2. `CHATGPT_START_HERE.md`.
3. Fresh `origin/main` and live-host check.
4. `ops/REPOSITORY_PRESERVATION_CONTRACT.json`.
5. `archive/UNIVERSAL_PUBLICATION_AND_THREAD_DELETION_SAFETY_PROTOCOL_18AUG2026.md`.
6. `.github/governance/CHATGPT_ACTION_STATE_AND_THREAD_CLOSEOUT_GOVERNANCE_25AUG2026.md`.
7. `CURRENT_HANDOVER_UNITARY_RECOVERY_21AUG2026.md` and `reports/UNITARY_EVIDENCE_DIGEST_24AUG2026.md`, treated as dated routing/control records rather than current-main substitutes.
8. `assets/data/valencia-hearing-status-v1.json` for the Valencia chronology.
9. This deletion audit for the current thread's closeout and open remediation programme.

## Final closeout

**What was done:** current repository and live site were re-digested as one system; the Valencia lock, current deployment, all HTML routes, source gates, sitemaps, runtime, operational drift, privacy debt and open PR inventory were independently checked.

**What was not done:** no case page was changed; no allegation was intensified; no private source was published; no email, filing, calendar event or third-party communication was created or sent; no open PR was merged or closed; no claim of complete evidence or disaster-recovery safety was made.

**What proves the state:** the current-main SHA, exact-SHA Pages workflow, 503/503 live hash matches, validator output, current Git tree and the controlling Valencia manifest/data record.

**What remains open:** the public/private remediation, operational-state rebuild, DIP 80 status reconciliation, structured recovery denominator, sitemap/canonical clean-up, runtime consolidation, PR triage and the source-acquisition programme listed above.

Once this file is merged and read back from `main`, deletion of the originating chat does not remove a unique material decision, correction, limitation or next action.
