# Deletion audit — professional register thread and repository/site redigest closeout

**Audit date:** 25 August 2026  
**Repository:** `sbu001monterecco/por-derecho`  
**Current-main baseline independently checked:** `b8bea28db0ece543011706fd054498c146b007e8`  
**Scope:** the ChatGPT thread that reconciled the fullest lawyers/law-firms/procuradores register, corrected the lawyer/procurador distinction, rechecked repository and live-site state, and requested a final deletion-safety verdict plus proposed next actions.

## Verdict

**DELETION-SAFE WITH OPEN REPOSITORY-WIDE REMEDIATION, once this audit is merged to `main`.**

The material decisions, corrections, identity mappings, limitations, implementation state and next actions from the thread are recoverable from the repository without retaining the conversation. This verdict does not mean the evidence corpus is complete, every historic professional has been found, every open pull request is disposable, private-source custody is complete, or the public repository is free of legacy privacy debt.

## Thread-specific professional-register state

The controlling professional layer is `PD-SP-LEGAL-PROF-001` in `assets/data/legal-professionals-register-v1.json`.

Current controlled totals:

- **40** professional records;
- **3** current lawyers;
- **31** former or mandate-review lawyers/legal professionals;
- **2** current procuradoras;
- **4** former procuradores/as.

The thread-specific correction is durable:

- `PD-SP-P-0067` **Adriana Hernández Díaz** is classified as `PROCURADOR_CURRENT` / `Procuradora`, not as current counsel. The register records the documented Juicio Cambiario 1048/2019 / ETJ 163/2020 and DP 748/2026 procedural capacities with a proceeding-specific limitation.
- `PD-SP-P-0086` **María Díaz Vecino** remains a procuradora with scope/personation kept proceeding-specific; source-name variants remain preserved in the identity layer.
- `PD-SP-P-0084` preserves the fuller source-name variant **Tania Alejandra Domínguez Limiñana**.
- `PD-SP-P-0056` preserves **Francisco Javier Pérez Almeida** while the Pérez Alemán-Almeida source form remains a name-reconciliation point.
- **Guillermo Suárez Lacone remains expressly excluded** from the authorised professional roster and received no new immutable professional-person ID through the controlling authorization.

The verified Alas working-professional set is durably represented: Juan Tomás Parrilla Suárez, Armando Betancor Álamo, José María Betancor Álamo, Davinia Sánchez de la Cruz, Joaquín Ruiz de Infante Abella, Cristo Ayose Suárez Pimentel, Ruth Pérez Castilla and Luis A. Barber Marrero. Administrative, proposal-only, billing-only and copied-only contacts are not silently converted into retained counsel.

## Public professional surfaces

The bilingual routes remain the controlled public presentation:

- `/es/profesionales-representantes/`
- `/en/professionals-representatives/`

Their current static counters and dynamic register logic reflect three current lawyers and two current procuradoras. The professional layer remains separate from both the claimant/ownership perimeter and the adverse-private-party perimeter. Professional representation does not transfer client knowledge, conduct, intention, control or liability.

## Repository and website redigest

Two same-day unitary closeouts now provide the broader system baseline:

- `docs/deletion-audits/2026-08-25-unitary-repository-website-valencia-thread-closeout.md` records the whole-site evidential/publication audit and finite governance/evidence remediation programme;
- `docs/deletion-audits/2026-08-25-financing-counsel-email-and-unitary-redigest-closeout.md` carries that programme through the subsequent transaction-development/counsel work and exactly-once outbound-email correction.

Current `main` is `b8bea28db0ece543011706fd054498c146b007e8`. The latest commit is continuity/audit-only: it adds a privacy-minimised transaction-development continuity record and unitary redigest, and expressly makes no website or external-communication changes. The immediately preceding `19fb3b7a...` release added the atomic exactly-once outbound-email guard; publication integrity, the email guard and GitHub Pages deployment succeeded for that release.

The active `Protect main` ruleset blocks branch deletion/non-fast-forward changes and requires pull requests, but it currently requires **zero approving reviews and no named CI status checks**. That protects against direct destructive history changes but does not make critical CI a merge prerequisite.

The current open-PR count is **34**. Every open PR must be treated as a dated candidate delta, not as current truth.

## Open actions — proposed priority order

### P0 — public/private boundary remediation

The unitary audits identified legacy public archive/operational material that can expose provider-specific message identifiers, unsent correspondence or private-source derivatives even though current governance forbids such publication. Continue the controlled remediation programme:

1. preserve evidentially necessary native/private copies outside public Git;
2. remove or redact provider-specific identifiers, private locators, recipient identities, privileged/current-counsel material and unsent correspondence from current public surfaces where policy requires;
3. distinguish intentionally public redacted derivatives from material that is merely encoded or placed under `archive/`;
4. document Git-history persistence rather than implying a current-tree deletion erases historic publication; and
5. make changed-file privacy checks mandatory for future merges.

### P0 — rebuild operational truth

`ops/CURRENT_STATE.json` is still dated 24 August and still identifies `ed98b0ac...` / PR #922 as the baseline current release while current `main` is `b8bea28d...`. Its stored open-PR snapshot says 31 while the fresh count is 34.

Replace the present mixture of historical anchors and current-status claims with one generated/append-only release register. Keep historical last-known-good releases, but label them as historical and derive current SHA, deployment, PR count and key release state automatically.

### P0 — reconcile DIP 80 status lineage

The earlier whole-site audit found dedicated DIP 80 living-casebook routes present and live while older operational/manifest records still described the casebook as blocked/unpublished. Preserve the failed materialisation history, but mark it superseded and point the controlling operational record to the later successful source/live route.

### P0 — materialise the quantitative recovery denominator

Create a reproducible structured recovery dataset joining:

- definitive credit and each credit-owner/servicer/standing transition;
- the EUR 13,168,082.02 transaction threshold/function and separate EUR 400,000 locales branch;
- consideration and proof of payment;
- estate proceeds, professional fees, creditor payments, income/fruits and any surplus;
- actual-versus-counterfactual cash flow;
- all 262-property title/possession/operation/income lanes;
- claimant/right-holder, defendant, cause of action, forum, remedy, interest and no-double-counting allocation.

No quantified recovery conclusion should outrun a reproducible source denominator.

### P1 — sitemap/canonical discovery cleanup

The prior fresh site audit identified 135 indexable HTML files absent from all sitemaps, 33 HTML files without canonical links, 10 duplicate-canonical groups and 8 duplicate-title groups. Decide explicitly for each route: canonical/indexable and discoverable, or supporting/noindex. Include newly materialised high-value routes such as the pre-7 June 2018 ONA pair where appropriate.

### P1 — open-PR triage

There are 34 open PRs. For each: either close as superseded, extract the unique validated delta onto fresh `main`, or preserve as historical evidence. Do not merge a PR merely because Git reports it mergeable.

PR #1016 is the most recent substantive candidate and proposes two new immutable people IDs and a non-LPB/Matkator owner/court-party network. Review it against current `main`, privacy/person-admission governance, AP 89/2014 source fidelity and the now-stable 40-record professional register before any merge.

### P1 — make core CI required by the main ruleset

The active main ruleset requires PRs but currently no approving review and no required named status checks. Add a small stable mandatory gate set rather than every specialist workflow. Candidate required checks:

- publication integrity / deletion-safety invariants;
- repository preservation contract;
- privacy/private-source governance;
- canonical identity referential integrity;
- changed-file specialist validator when a protected register is touched.

Keep the set small enough to avoid making unrelated historical live-readback jobs permanent merge blockers.

### P1 — runtime consolidation

The earlier redigest found the shared site loader reaches a large layered JavaScript graph. Consolidate loader order through one declarative route/module manifest while preserving existing sent-link compatibility, locked actor presentation and evidential qualifiers.

### P1/P2 — professional archive backfill

The professional roster is complete to the current controlled source set, not absolutely complete for all historical time. Continue targeted archive review for older retained professionals and procuradores. New names should enter first as source/role review and only join the public authorised register after exact identity, capacity, client, proceeding and period are sufficiently established.

## Deletion-safety dimensions

| Dimension | Result |
|---|---|
| `THREAD_REASONING_CONTINUITY` | **Safe after merge** — professional decisions, corrections, exclusions, source limits and next actions are repository-controlled |
| `IMPLEMENTATION_STATE_CONTINUITY` | **Safe** — PR #1010/#1014 results and current register state are recoverable from `main` |
| `PROFESSIONAL_IDENTITY_CONTINUITY` | **Safe with open backfill** — immutable IDs, aliases and role distinctions are preserved; historic discovery can continue |
| `LIVE_PUBLICATION_CONTINUITY` | **Safe/qualified** — the latest commit is audit/continuity-only and changes no website; the immediately preceding release has successful Pages deployment and publication-integrity checks; the earlier unitary audit supplies the last full exact whole-site parity readback |
| `COMMUNICATION_VERIFICATION` | **No communication action in this closeout** — this audit does not send email, file a document or create a calendar event |
| `PRIMARY_EVIDENCE_COMPLETENESS` | **Open** — legal, banking, accounting, title, income, professional and certified-court source gaps remain |
| `PUBLIC_PRIVATE_BOUNDARY` | **Open P0 remediation** — legacy repository material still requires controlled review |
| `DISASTER_RECOVERY_SAFETY` | **Not re-certified here** — off-GitHub/native-source custody remains a separate control plane |

## Future-thread start order

1. `AGENTS.md`.
2. `CHATGPT_START_HERE.md`.
3. Fresh `origin/main` and live-host/deployment check.
4. `ops/REPOSITORY_PRESERVATION_CONTRACT.json`.
5. `archive/UNIVERSAL_PUBLICATION_AND_THREAD_DELETION_SAFETY_PROTOCOL_18AUG2026.md`.
6. `.github/governance/CHATGPT_ACTION_STATE_AND_THREAD_CLOSEOUT_GOVERNANCE_25AUG2026.md`.
7. `assets/data/legal-professionals-register-v1.json` and the professional identity extension parts for any lawyer/procurador question.
8. `.github/governance/records/LEGAL_PROFESSIONAL_REGISTER_AUTHORIZATION_20260825.md`.
9. the two same-day unitary deletion audits identified above for the current system-wide baseline.
10. This audit for the professional-register thread closeout and current action priorities.

## Final closeout

**What was preserved:** the fullest authorised professional roster under the current source set; lawyer/procurador corrections; Alas working-professional coverage; former/current procurador coverage; name variants; explicit exclusion; bilingual public routes; validation state; current-main/deployment state; and the repository-wide next-action programme.

**What was not done:** no new allegation was made; no professional was moved into a principal adverse/claimant perimeter; no email, filing or calendar action occurred; no open substantive PR was merged; no claim of evidential completeness was made.

**Deletion decision:** once this audit is merged to `main` and read back, deletion of the originating ChatGPT thread does not remove a unique material decision, correction, implementation state, limitation or proposed next action.