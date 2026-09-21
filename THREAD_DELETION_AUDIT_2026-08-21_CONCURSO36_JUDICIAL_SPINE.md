# THREAD DELETION AUDIT — CONCURSO 36/2012 JUDICIAL SPINE

**Date:** 21 August 2026  
**Thread scope:** reverse-engineering digest of the Por Derecho repository and website, implementation of the recommended Concurso 36/2012 judicial-act / implementation spine, repository update, bilingual public propagation, validation and deletion-safety closeout.  
**Deletion status after this record is merged:** **SAFE TO DELETE — subject to the residual evidence gaps below, which are already preserved outside this chat.**

## 1. Material intelligence created in this thread

The thread materially changed the way the 2021–2022 adjudication chain is controlled.

### A. Canonical judicial-act spine

The controlling question is now:

> **what was requested → what the court actually ordered → conditions and asset/credit perimeter → what was implemented → what document proves implementation → what difference remains unresolved.**

The repository must not treat a formal judicial or notarial act as economically/evidentially self-executing, and it must not treat a documentary difference as automatic proof of invalidity, fraud, bad faith, surplus or criminal responsibility.

### B. January-2022 correction

Unsafe shorthand was identified and locked:

> **Do not use “the 26 January 2022 adjudication order” as a generic label for the whole adjudication / dación authority.**

Deed 457 recites an Auto dated **22/01/2022**, while other controlled reconstruction references use **26/01/2022**. Both dates/functions remain distinct pending recovery of the complete signed January judicial-act family.

### C. Function-of-money control

The following must remain separate unless a legal/documentary bridge is proved:

> recognised insolvency credit ≠ mortgage liability ≠ competitive threshold ≠ debt stated as consideration for the dación ≠ Registry value ≠ possible surplus.

In particular, the current record verifies that **€13,168,082.02** appears in different legal/economic contexts; numerical identity does not itself prove the transition between those functions or the absence of remanente.

### D. Order / asset perimeter control

LPB's insolvency estate must not be silently expanded to the whole mixed-ownership Sun Park complex. Every material order should ultimately be linked finca by finca to LPB assets, with Matkator and third-party property kept separate unless a primary title/order establishes otherwise.

## 2. Repository implementation completed

### Substantive PR

**PR #724 — Canonicalise Concurso 36/2012 judicial-act spine**  
**Merged to `main`:** `40603843619b8bf9ba2492a2ec94b29b1ee0e587`

Canonical recovery paths now on `main`:

- `CURRENT_HANDOVER_CONCURSO36_JUDICIAL_SPINE_21AUG2026.md`
- `archive/CONCURSO36_JUDICIAL_ACTS_IMPLEMENTATION_REGISTER_21AUG2026.md`
- `archive/CORRECTION_REGISTER_CONCURSO36_JUDICIAL_SPINE_ADDENDUM_21AUG2026.md`
- `assets/data/concurso36-judicial-acts-v1.json`
- `es/adjudicacion-2022-reconstruccion-documental/index.html`
- `en/2022-adjudication-documentary-reconstruction/index.html`
- `sitemap-adjudicacion-2022.xml`

The bilingual pages now expose a compact judicial-spine table and explicitly preserve the 22-Jan / 26-Jan distinction.

## 3. Governance defect surfaced and repaired

Initial validation of PR #724 exposed a repository-wide mission-critical gate failure unrelated to the seven judicial-spine files:

- `.github/workflows/verify-meeting-point-final-propagation-live.yml` intentionally used `statuses: write` to post a queryable custom status;
- `scripts/validate_mission_critical_repo.py` had not added that workflow to the existing statuses-write allowlist.

This was repaired separately rather than smuggled into the substantive workstream:

**PR #725 — Sync Meeting Point live verifier with mission-critical status policy**  
**Merged to `main`:** `307a0db41a451c6efa2cb9688987ef96c4a98c83`

The repair did not broaden the workflow permission; it synchronized the repository's explicit policy with an already-existing workflow function.

## 4. Validation completed

After the governance repair and branch refresh, the final PR #724 head passed all of the triggered controls before merge:

- Publication integrity gate — **PASS**
- Public bidder name-only and bid-preservation gate — **PASS**
- Validate visual asset identity registry — **PASS**
- Off-GitHub Preservation Snapshot — **PASS**
- Validate adjudication provenance and cross-links — **PASS**
- Validate unitary public shell — **PASS**

GitHub `main` was re-read after merge and confirms the Spanish judicial-spine section and expanded missing-chain controls are present in source.

External search/cache retrieval did not provide a reliable rendered-page confirmation during this thread. This is therefore recorded as **source-on-main confirmed; external rendered propagation not independently asserted here**. No deployment defect is inferred from search/cache lag.

## 5. Existing missing-evidence queues retained

No duplicate evidence queue was created. The judicial spine routes to the existing canonical Missing Evidence Register entries:

- **ME-005** — actual 2018, 2021 and 2022 testimonios;
- **ME-006** — service/delivery logs for testimony episodes;
- **ME-007** — underlying CAM/AC testimony requests;
- **ME-008** — downstream notarial/Registry use of testimonios;
- **ME-011** — AC full accounting bridge/workbook: credit, interest, €400k, dación, cash, costs, sobrante;
- **ME-012** — complete primary 2020–2022 Mercantile orders/evidence-before-court.

These open items are not a reason to retain this chat because they are now recoverable from the repository's canonical queue and handover.

## 6. P0 continuation sequence preserved

A fresh thread should continue in this order:

1. recover and bind the complete signed **18-May-2021** source family;
2. recover both complete signed **15-Oct-2021** acts plus service/finality;
3. recover the complete signed **January-2022** act family and resolve 22-Jan / 26-Jan without assuming identity;
4. recover the complete 2021/2022 testimonios and their downstream notarial/Registry use;
5. recover deed-457 communication to the Mercantile Court, ensuing act/mandamiento and Registry chain;
6. reconstruct the **€13,168,082.02 legal-function bridge**;
7. reconcile the **€400,000** bank/ledger/title line;
8. reconcile final liquidation accounts / remanente;
9. create the finca-by-finca **Order → Asset** crosswalk.

## 7. Redundant off-thread recovery record

In accordance with `archive/THREAD_DELETION_CONTINUITY_PROTOCOL_16AUG2026.md`, a self-email was **sent successfully** through the authenticated Gmail account after the substantive merge.

**Subject:** `Por Derecho closeout — Concurso 36/2012 judicial spine merged 21AUG2026`

The email preserves:

- PR #724 and substantive merge SHA;
- PR #725 and governance-repair merge SHA;
- canonical repository paths;
- public route paths;
- the 22-Jan / 26-Jan correction;
- the core analytical rule;
- ME-005/006/007/008/011/012;
- the P0 continuation sequence;
- the validation state;
- the explicit limitation that source-on-main is confirmed while external rendered propagation was not independently asserted.

No raw Gmail message/thread identifier is published in this public repository.

## 8. Source-status and privacy check

This thread did **not** add raw confidential evidence, privileged lawyer material, witness audio, full private transcripts, unnecessary personal data or an unverified criminal conclusion to the public repository.

The new public JSON is expressly a partial analytical seed and does not outrank signed primary sources, the global Correction Register, its judicial-spine addendum or the Missing Evidence Register.

## 9. Deletion decision

Once this audit file is merged to `main`, this chat is no longer a sole custody point for any material project intelligence created here.

The substantive result is recoverable from:

1. merged repository state on `main`;
2. canonical specialist judicial register;
3. root current handover;
4. correction addendum;
5. machine-readable public seed;
6. bilingual adjudication pages;
7. existing Missing Evidence Register;
8. the redundant self-email recovery pointer; and
9. this deletion audit.

**FINAL THREAD STATUS: SAFE TO DELETE AFTER THIS AUDIT MERGES.**
