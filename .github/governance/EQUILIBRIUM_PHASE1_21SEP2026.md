# Equilibrium Phase 1 — governance-only transaction

**Control ID:** `PD-EQ-20260921-PHASE1`  
**Observed:** 21 September 2026, 21:06:57 UTC  
**Base main:** `fa81fb53a08a6e191d8ac26cf130c402e31548f4`  
**Classification:** governance-only; no public runtime or public-content change

## Authority and boundaries

Gil Marer authorised one Phase-1 governance-only GitHub transaction, on the express conditions that it must not alter public content, must not merge unless every applicable gate is green, and must not start Presidencia publication.

This candidate therefore changes only the four paths listed in `ACTIVE_WRITER_LEASE.json`. It does not change HTML, ES/EN/DE routes, navigation, assets, sitemaps, Pages configuration, deployment workflows, publication manifests, evidence text, case propositions, filing state or any external communication. It does not send email, file a document, contact an authority or publish to social media.

## Fresh baseline

GitHub current `main` advanced during the audit from `bf1401b86eec72f9e877340c34081669cd70bed1` to `fa81fb53a08a6e191d8ac26cf130c402e31548f4` while the Ref21/Ref22/Ref24 digitisation work completed. Phase 1 therefore uses the later SHA and does not overwrite or reopen that substantive work.

The live open-PR census returned 56 candidates, and every returned PR was individually read back as open. That denominator is current for the stated observation time. It is not a statement that all 56 contain unique mergeable work.

The checked-in operational controls remain older observations:

- `ops/CURRENT_STATE.json` records main `1e96f0d97323ba4c10ad0b7341d28017d6fa26dd` and 61 open PRs;
- `ops/CURRENT_COLLABORATION_STATE.json` retains a 20 September integrator assignment; and
- `ops/PR_RECONCILIATION_LEDGER.json` was observed on 25 August.

This narrow package records that drift but does not rewrite those non-allowlisted files. Treating the stale values as current would be false; expanding the diff to repair them would cease to be the bounded governance-only acceptance package validated here.

## Installed controls

1. `ACTIVE_WRITER_LEASE.json` gives this transaction one time-bounded, machine-readable lane and makes later threads resolve its live state from GitHub rather than from chat memory.
2. `EQUILIBRIUM_ACCEPTANCE.json` supplies explicit criteria, denominators, failures and pending states. It deliberately reports `NOT_YET_AT_EQUILIBRIUM` until the candidate is current, reviewed and green.
3. The existing manual governance compatibility validator recognises these controls and must still prove that the diff contains no protected public-runtime path.

These controls are advisory v1. They do not activate a new repository-wide required check, reviewer dependency, ruleset, secret, credential, service or deployment dependency.

## Merge conditions

Immediately before merge:

1. resolve live `main` and compare the complete candidate diff;
2. stop and reconcile if `main` advanced;
3. confirm only the four authorised governance paths changed;
4. run the governance-only compatibility validator and applicable repository gates;
5. require every applicable exact-head check to be successful; and
6. register the candidate in Control Tower issue `#1428`.

If any applicable gate fails or remains indeterminate, leave the PR open and do not merge. A merge, if permitted, closes this lease dynamically; the closeout must record the exact tested head, merge SHA and gate result in Control Tower. No Pages route readback is claimed or required for a package that changes no rendered public surface.
