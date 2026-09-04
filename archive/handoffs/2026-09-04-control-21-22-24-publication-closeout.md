# Control 21–22–24 publication closeout — 4 September 2026

## Scope state

`PUBLICATION_CLOSEOUT_IN_PROGRESS`

This record closes the publication cycle that canonicalised the Control 21 / Control 22 / Control 24 interlink architecture around Concurso Ordinario 36/2012, bound the reader-facing three-track digitisation to the canonical governance graph, and repaired the public third-party bidder name-only privacy breach without changing the bid facts.

## Current-main rule

**Current main wins.** The SHAs below are provenance checkpoints, not permission to use stale content. Every successor thread must fetch remote `main` first and then read the canonical files from that current head.

## Provenance checkpoints

- Control 21–22–24 continuity package: PR #1418.
- Continuity checkpoint closeout: PR #1419.
- Reader/canonical cross-binding: PR #1420, merge `667868ee71a98105ad7766d9afb37a5bd10fe921`.
- Public bidder name-only anonymisation repair: PR #1432, merge `c9c3dd328e388468d3757441335e5f380ea71dff`.
- Closeout bootstrap `main`: `c9c3dd328e388468d3757441335e5f380ea71dff`.

## Canonical boot sequence

1. Fetch current remote `main`.
2. Read `assets/data/control-21-22-24-continuity-v1.json` (`PD-C212224-001`).
3. Read `data/three-track-full-digitisation-20260904.json` (`PD-THREE-TRACK-DIGITISATION-20260904-01`).
4. Read `.github/governance/CONTROL_21_22_24_CONTINUITY_INTERLINK_PROTOCOL_04SEP2026.md`.
5. Read this closeout and the preceding Control 21–22–24 handoffs.
6. Preserve the bridge/status invariants below before editing any page, registry or generated index.

## Evidential and procedural invariants

- Control 21 → DP 1901/2026 remains `UNVERIFIED_CANDIDATE_BRIDGE` until a source-certified intake/reparto bridge is controlled.
- Control 22 → DP 1956/2026 remains `UNVERIFIED_CANDIDATE_BRIDGE` until a source-certified intake/reparto bridge is controlled.
- Control 24 is the 18 June 2026 Decanato daily-reference-24 registration record; its 25 June 2026 judge-related filing is a dependent supplement in the same registration record, not a separate proceeding.
- Control 24 formal destination/reparto/NIG/DP remains `UNKNOWN` unless primary documentary proof resolves it.
- The user-reported private-actor filing object dated 25 June 2026 and the Control 24 judge supplement dated 25 June 2026 remain distinct with `NO_BRIDGE` until source reconciliation proves otherwise.
- The judge filing is `denuncia / notitia criminis`, not a formal querella merely because later judge-directed querella work exists.
- DP 1956/2026 provisional dismissal is not acquittal, `sobreseimiento libre` or final merits exoneration.
- Interlinking never transfers knowledge, intent, causation, guilt, liability, procedural status or evidential weight from one actor/route to another.
- Fiscalía neutralisation/ineffectiveness language, where used, remains an attributed allegation or inference, not an established institutional fact.

## Public reader routes

- ES DP 1901: `/por-derecho/es/dp-1901-2026/`
- EN DP 1901: `/por-derecho/en/dp-1901-2026/`
- ES DP 1956: `/por-derecho/es/dp-1956-2026/`
- EN DP 1956: `/por-derecho/en/dp-1956-2026/`
- ES Control 24: `/por-derecho/es/control-24-denuncia-juez-concurso-36-2012/`
- EN Control 24: `/por-derecho/en/control-24-insolvency-judge-complaint-36-2012/`

Canonical proceeding aliases/routes remain part of the graph and must not be removed simply because richer reader routes exist.

## Validation checkpoints

### PR #1420 cross-binding

Successful PR-head checks included:
- Control 21-22-24 continuity governance — run `33827538587`.
- Validate three-track full digitisation — run `33827538589`.
- Validate audience experience — run `33827538572`.
- Audit private-source, statement and OSINT governance — run `33827538575`.
- Off-GitHub Preservation Snapshot — run `33827538516`.

### PR #1432 bidder privacy repair

Successful PR-head checks included:
- Public bidder name-only and bid-preservation gate — run `33831128946`.
- Control 21-22-24 continuity governance — run `33831129037`.
- Validate three-track full digitisation — run `33831128841`.
- Validate Control 22 and Control 24 digitisation — run `33831128833`.
- Audit private-source, statement and OSINT governance — run `33831128877`.
- Production smoke monitor — run `33831128956`.

The deterministic repository-owned rewrite changed only the protected third-party bidder name tokens on eight public surfaces, using neutral Spanish/English labels, while preserving bid amount/date/comparison/notice/deposit and other factual markers. No underlying evidence or Control 21/22/24 procedural/evidential state was changed.

### Post-merge `main` verification

At creation of this closeout, post-merge runs for `c9c3dd328e388468d3757441335e5f380ea71dff` were queued. Before merging this closeout, replace this paragraph with the completed post-merge continuity, bidder, three-track and Pages results, or explicitly state any superseding descendant `main` SHA and validate that descendant instead.

## Open substantive evidence gaps

These are not publication failures and must stay visible:

1. Source-certified Control 21 → DP 1901/2026 intake/reparto bridge.
2. Source-certified Control 22 → DP 1956/2026 intake/reparto bridge.
3. Certified reparto/current formal destination for Control 24.
4. Decanato/TSJC/CGPJ trace sufficient to establish Control 24 routing without inference.
5. Source-level reconciliation of the potentially distinct 25 June 2026 private-actor filing object and judge supplement.
6. Canonical registration of any still-missing stamped source copies, source hashes, transcriptions and joinder metadata.
7. Reconciliation of CGPJ/DI 169/2026 nomenclature wherever source wording differs from public shorthand.

## Unrelated repository debt

Broad repository workflows may still report historical or cross-project debt outside this publication scope. Do not silently weaken this Control 21–22–24 governance to make unrelated checks green. Classify and repair those debts in their own controlled changes. Examples seen during this cycle included legacy workflow-integrity configuration and Arrecife/identity-registry drift.

## Successor-thread rule

A successor thread must not reconstruct this architecture from chat memory. It must start from current remote `main`, the canonical machine graph, the bound three-track reader dataset, the governance protocol and this closeout. If any rendered page disagrees with canonical state, treat that disagreement as a governance failure and repair canonical/source truth first.
