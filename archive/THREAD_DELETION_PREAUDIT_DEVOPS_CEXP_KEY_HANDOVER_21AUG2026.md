# Thread deletion pre-audit — DevOps / repository / live-site / CEXP key-handover thread

**Date:** 21 August 2026  
**Repository:** `sbu001monterecco/por-derecho`  
**Purpose:** preserve a pre-deletion DevOps and continuity snapshot for the current ChatGPT thread before running the final deletion audit.  
**Status:** `READY_FOR_DELETION_AUDIT — NOT YET DELETION-CLEARED`  
**Public website:** `https://sbu001monterecco.github.io/por-derecho/`  
**Main SHA at scan start:** `117456e17e456a413b73dcdf479fa554a3324e38`

---

## 1. Scope

This checkpoint records four separate states which must not be conflated:

1. **current `main`** — the merged source of truth;
2. **open draft branches / PRs** — recoverable work that is not current and is not automatically live;
3. **GitHub Pages public edge** — deployed HTML and runtime assets, which require external verification rather than inference from merge state;
4. **current ChatGPT thread** — any facts, corrections or implementation state that would otherwise be lost if the thread were deleted.

This file does **not** run the final deletion audit, does not change public HTML, does not publish private evidence and does not promote unmerged draft-branch propositions into current findings.

---

## 2. Repository state at the scan

The default branch was `main` at:

`117456e17e456a413b73dcdf479fa554a3324e38`

The latest merged change at that point was the Meeting Point chain continuity/discoverability update. The preceding relevant merged states included:

- prosecution-oriented repository/site/email redigest and deletion-safe handover;
- FTI / Meeting Point live-deployment record;
- exact FTI / Meeting Point live verifier;
- bilingual FTI / Meeting Point insolvency/custody chain;
- prior unitary repository/recovery redigest;
- canonical three-video Calificación Vista processing workflow;
- evidence-provenance controls and other specialist handovers.

Current repository strengths include:

- a canonical current-handover layer;
- extensive correction and missing-evidence registers;
- bilingual public routes;
- machine-readable state files;
- publication-integrity and subject-specific validators;
- explicit production smoke monitoring;
- full Git recovery-bundle tooling with clean-restore testing;
- a separate rendered-site / Git-mirror preservation workflow;
- source-status and public/private boundary controls.

### DevOps weakness: branch protection enforcement

The repository reports the `main` branch as protected in metadata, but the returned branch-protection state shows required-status-check enforcement **off**. The large validator/workflow estate therefore does not, from this metadata alone, amount to a hard merge gate on `main`.

**Deletion-audit implication:** do not state that every merge was required by branch protection to pass every validator. Record actual workflow/status evidence per relevant commit/PR instead.

### DevOps weakness: branch accumulation

Repository configuration does not automatically delete merged branches. Together with the large open-draft backlog, this increases state fragmentation and the risk that a future thread mistakes an old branch for the governing state.

**Required rule:** `main` + later signed/corrected primary source controls; draft branches are proposals only until reconciled and merged.

---

## 3. Public website / deployment state

The canonical public host used by current HTML is:

`https://sbu001monterecco.github.io/por-derecho/`

The current homepage source declares that host in canonical / hreflang / Open Graph metadata.

### FTI / Meeting Point route — verified live

The bilingual FTI / Meeting Point standalone chain was not treated as deployed merely because PR #751 merged. PR #752 added an external GitHub Pages verifier that polled the exact public routes with cache-busting parameters and required HTTP 200 plus controlled source markers.

The recorded run:

- workflow: `Verify FTI Meeting Point chain live`;
- run: `32511560353`;
- head: `4160a55d24c715e6073bb0854caa29251b31e444`;
- result: **SUCCESS**.

The current deployment log records the exact Spanish and English public URLs and the marker set tested.

### Latest `main` after that live verifier

The later merges up to the scan-start SHA were primarily archive/control/discoverability changes, including the dedicated Meeting Point sitemap/robots update and an archive-only prosecution handover. They did not replace the FTI public dossier HTML.

Therefore the FTI live-verification evidence remains relevant to the currently merged dossier, while later sitemap/robots propagation is a separate deploy/indexing concern.

---

## 4. Production monitoring finding

The repository has a scheduled `Production smoke monitor` running every two hours at minute 17. It checks a fixed set of mission-critical routes, marker strings, minimum byte lengths, a deployment probe and the global loader. On failure it uploads route-level evidence and opens or updates one production incident issue.

### Open incident #600

Issue #600 — `[PRODUCTION] GitHub Pages smoke check failed` — remains open.

The issue was opened on 20 August 2026 and received six automated failure updates, with the last recorded failure update at `2026-08-20T22:53:06Z`.

The workflow implementation **does not contain a recovery step that closes the incident or appends an explicit success/recovered message**. A later healthy run can therefore leave the issue open indefinitely.

### Correct interpretation

- the open issue is evidence of repeated production-smoke failures on 20 August;
- it is **not, by itself, proof that the site remains unhealthy on 21 August**;
- the successful FTI external verifier on 21 August proves at least that the tested FTI routes were publicly healthy at that later point;
- final deletion audit should either obtain a fresh mission-critical production-smoke result or explicitly preserve the monitoring ambiguity.

### Recommended DevOps improvement

Add recovery semantics to the smoke workflow:

`FAIL → open/update incident`

`RECOVERED → comment with successful run + close incident (or mark resolved)`

This makes incident state reflect production state rather than only failure history.

---

## 5. Backup / disaster-recovery state

### Repository recovery bundle

`.github/workflows/repository-backup-bundle.yml`:

- creates a full `git bundle --all`;
- verifies the bundle;
- hashes it;
- clean-restores it to a mirror and worktree;
- runs `git fsck --full`;
- compares refs;
- runs `scripts/validate_mission_critical_repo.py`;
- performs a local static-site smoke test;
- uploads the recovery bundle for 90 days;
- optionally mirrors all refs to an independent remote if `POR_DERECHO_BACKUP_MIRROR_URL` is configured.

If the independent mirror secret is absent, the workflow emits a warning. Static repository inspection does not establish whether the secret is currently configured.

### Off-GitHub preservation workflow

`.github/workflows/off-github-preservation.yml` builds a fuller preservation package containing:

- complete Git mirror;
- Git integrity/ref inventories;
- rendered public-site snapshot via `wget`;
- GitHub API metadata;
- checksums;
- packaged artifact with 90-day retention.

It explicitly records that GitHub's full account-data export still requires an interactive account-holder action.

### Deletion-audit implication

Do **not** equate “backup workflow exists” with “independent off-GitHub disaster-recovery copy currently verified.” The final audit should distinguish:

- workflow capability;
- last successful recovery-bundle run;
- independent mirror configured/not verified;
- preservation artifact retained/not verified;
- account-data export performed/not verified.

---

## 6. Open draft-PR state at scan time

Open drafts are a material continuity risk because several contain substantial work not yet reconciled with current `main`.

Exact comparisons made during this scan:

| PR / branch | State vs current `main` at scan | Interpretation |
|---|---|---|
| #750 `codex/fti-meeting-point-media-record-20260821` | diverged; **12 ahead / 5 behind** | contains additional FTI/media reconciliation pages, prompt/timeline and its own deletion audit; do not treat as current publication |
| #749 `codex/concurso36-primary-autos-redigest-20260821` | diverged; **2 ahead / 5 behind** | large primary-auto redigest/publication package; not merged/live |
| #747 `codex/community-criminal-nonderogation-20260821` | diverged; **1 ahead / 7 behind** | Community criminal-instrumentalisation non-derogation proposal; not current public state |
| #737 `codex/reverse-engineering-corrections-20260821` | diverged; **9 ahead / 16 behind** | CEXP-governance/public corrections + prior deletion-audit package; requires proposition-level reconciliation |
| #736 `fiscalia-tenerife-eg95-2026-deletion-safe` | diverged; **10 ahead / 17 behind** | Fiscalía Tenerife EG95 archive/public-page package; not merged/current |

The current prosecution handover already gives the correct policy: reuse proposition-level material from relevant drafts only after reconciliation against current `main`, signed originals and the correction register. Do not wholesale-merge an old branch because it is favourable.

### Deletion-audit implication

The final thread deletion audit must explicitly record:

- which open PRs are merely backlog;
- which contain unique evidence/analysis that would be lost if their branches were deleted;
- which have already been superseded by later merged controls;
- that deletion of the ChatGPT thread does **not** imply closure, merge or abandonment of those PRs.

---

## 7. Runtime / maintainability assessment

The current repository redigest already identifies layered `assets/site.js` correction/loader propagation as the principal maintainability risk.

The production smoke script now checks the global loader directly, confirming that runtime composition has become mission-critical.

### Risk

A growing stack of runtime injections can create:

- order-dependent behaviour;
- duplicated or superseded copy;
- public/repository drift;
- cache/version skew;
- hard-to-reason canonical state;
- a validator passing one source layer while a later loader changes the rendered result.

### Direction

Continue toward a declarative build/state registry in which each proposition/page module has:

- canonical owner/source;
- current status;
- deterministic build order;
- bilingual mapping;
- provenance/correction metadata;
- explicit public/private flag;
- generated sitemap/discovery registration;
- rendered-output verification.

This should reduce dependence on accumulated client-side repair layers.

---

## 8. Current thread: deletion-continuity reconciliation

The substantive unique fact from this thread was already captured and remains on current `main` in:

`archive/JV1260_CEXP_KEY_HANDOVER_CAPACITY_CLARIFICATION_17AUG2026.md`

That controlling record preserves:

- JV 1260/2011 as the procedural family;
- the presently identified physical/notarial handover event as 28 May 2012, subject to the complete notarial/court record;
- Gil Marer's direct evidence that he was present and personally handed over the relevant keys;
- his asserted capacity for that physical act as **President of CEXP**;
- the anti-conflation rule preventing automatic attribution of that act to MRSP/Monterecco, LPB, Pink Canary Services or other entities;
- contemporaneous compliance / no self-help retaking as direct-witness evidence;
- post-handover lock/use/rental allegations as corroboration-required investigative leads;
- the maintenance-key / appellate-inference issue;
- a finite P1 recovery package for the complete notarial, court, key and capacity record.

This was re-fetched from `main` during the current scan and is therefore not merely remembered from the source conversation.

### No new merits proposition generated by the DevOps scan

The current scan adds operational state only. It does not change the merits of JV1260/AP89, CEXP authority, later owner use, CAM causation or any criminal allegation.

---

## 9. Final deletion-audit gates

Before marking this thread `DELETION-SAFE`, run the final audit against these gates:

### A. Thread-only facts

- [ ] identify every material factual clarification introduced in this thread;
- [ ] map each one to a merged repository file or controlled external source;
- [ ] confirm no required fact depends solely on chat memory.

### B. Repository state

- [ ] record final `main` SHA immediately before audit closure;
- [ ] confirm this pre-audit checkpoint is merged;
- [ ] verify no concurrent merge changed a controlling file after the scan;
- [ ] distinguish merged current state from all open drafts.

### C. Live site

- [ ] obtain fresh public-edge evidence for mission-critical routes or preserve the explicit limitation;
- [ ] confirm canonical host / bilingual roots;
- [ ] verify any route materially changed by this thread, if any;
- [ ] do not infer rendered state solely from repository state.

### D. Production incident

- [ ] inspect issue #600 and latest production smoke evidence;
- [ ] record whether current production is healthy, degraded or unverified;
- [ ] do not let the stale-open-incident design create a false outage statement.

### E. Backups / preservation

- [ ] distinguish workflow capability from last successful artifact;
- [ ] verify recovery-bundle / restore evidence where deletion closure depends on it;
- [ ] verify independent mirror/off-GitHub state or record it as open;
- [ ] preserve hashes/identifiers without publishing private evidence.

### F. Open PRs

- [ ] snapshot the relevant open draft PRs and ahead/behind state;
- [ ] identify unique unsuperseded content;
- [ ] do not count unmerged public pages as live;
- [ ] do not close or delete branches merely to simplify the audit.

### G. External actions

- [ ] record any email, Drive, filing, workflow, PR or other external action actually performed in this thread;
- [ ] distinguish proposed actions from completed actions;
- [ ] confirm no unsent draft or uncommitted user-approved change is being mistaken for completion.

---

## 10. Pre-audit conclusion

Current status:

`READY_FOR_DELETION_AUDIT — NOT YET DELETION-CLEARED`

The substantive thread clarification is already durable on `main`. The repository and public site have strong continuity controls and a verified live FTI/Meeting Point deployment. The principal operational issues to carry into the final audit are:

1. open-draft state fragmentation;
2. no hard required-status enforcement visible on `main` branch-protection metadata;
3. a production smoke incident that does not auto-resolve on recovery;
4. runtime-loader layering / canonical-state drift risk;
5. backup capability versus independently verified off-GitHub copy must remain distinguished.

No public website change is required merely to make this thread deletion-auditable.
