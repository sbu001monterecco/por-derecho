# Por Derecho repository stewardship rules

These rules apply to every human or automated change in this repository. They preserve the public record; they do not turn allegations into findings.

## 1. Start from the actual source of truth

- Fetch and read the current remote `main` before analysing or editing. Never publish an older worktree, chat reconstruction or stale branch over later work.
- Treat the Git tree as the preservation authority, CI as the reproducibility authority, `main` as the merge authority and the public host as the deployment authority.
- Reconcile new work additively. Never use a broad reset, force push or whole-file replacement to resolve overlap with later work.

## 2. Preservation before simplification

- Do not delete, rename, hide, collapse, materially abridge or unlink an existing route, source, exhibit, archive control, evidential qualification or actor relationship unless Gil Marer has expressly authorised that exact change.
- A redesign or summary is an additional reader layer, not permission to remove the complete record.
- A file deletion or rename within a protected path requires a repository record under `operations/preservation-authorizations/` identifying the exact old path, the express authorization and any replacement or redirect.
- Preserve Spanish/English parity, source-language meaning, dates, provenance, corrections, contrary evidence, open proof and right-of-reply material.

## 3. Locked first-read accountability presentation

Unless Gil Marer later gives specific express authorization, both homepages and every route listed in `ops/REPOSITORY_PRESERVATION_CONTRACT.json` must retain prominently, outside closed progressive disclosure:

1. five separate private-actor cards for Francisco Mario Matos Matas, Antonio Cogolludo Rojas, Shaila María Cogolludo Ramos, José Daniel Acosta Matos and Laura Patricia Acosta Matos;
2. immediately below, Francisco de Borja Rodríguez-Batllori Laffitte as the court-appointed, judicial-adjacent Insolvency Administrator—not a private actor and not the judge;
3. Alberto López Villarrubia separately as Magistrate-Judge exercising judicial power;
4. five actor-specific linkage rows addressing alleged acts/commissions and omissions, evidence, contrary record and proof boundaries; and
5. the source-controlled images already assigned to Francisco Mario Matos Matas, the Insolvency Administrator and the Magistrate-Judge. Do not fabricate portraits for people without a verified repository asset.

The public identity is **Laura Patricia Acosta Matos**. Do not use “Laura Isabel” as a public identity. Do not transfer conduct, knowledge, intention or responsibility automatically between people because of a family, company, professional or institutional relationship.

## 4. Evidence and publication boundaries

- Label documented fact, attributed allegation, inference, official outcome, contrary record and unresolved proof distinctly.
- Preserve direct allegations strongly and visibly where the controlling source supports them, but never describe guilt or criminal liability as adjudicated when it is not.
- Keep distinct legal persons, capacities, titles, operators, creditors, property owners, insolvency estates, professional firms, private actors, the Insolvency Administrator and the Magistrate-Judge distinct.
- Do not publish raw private email bodies, message IDs, unnecessary personal identifiers, privileged advice, unredacted protected records, private tax/fee ledgers, unsent correspondence or live legal strategy.

## 5. Required change process

Before merge:

1. compare the proposed tree with current `main` and review every deletion or rename;
2. run `python3 scripts/validate_repository_preservation.py`;
3. run `python3 scripts/validate_publication_integrity.py`;
4. run `python3 scripts/validate_audience_experience.py` and the relevant specialist validators;
5. preserve the exact routes, files, public markers, limitations and open evidence in a publication or closeout record; and
6. require the Publication integrity gate and relevant rendered checks to pass.

After merge, verify the exact merge SHA was deployed and check the rendered ES/EN homepages plus every affected direct route. A thread is deletion-safe only when no unique reasoning, correction, source, limitation or recovery instruction remains solely in that thread.

The machine-readable contract is `ops/REPOSITORY_PRESERVATION_CONTRACT.json`. The controlling publication/deletion state machine remains `archive/UNIVERSAL_PUBLICATION_AND_THREAD_DELETION_SAFETY_PROTOCOL_18AUG2026.md`.
