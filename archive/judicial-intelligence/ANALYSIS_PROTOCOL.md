# Continuous Judicial Analysis Protocol

This protocol governs recurring analysis of newly added court decisions.

## Trigger

Run this protocol whenever a new judgment, order, decree, providencia, LAJ act, appeal, Fiscalía report or official docket record is added.

## Step 1 — Source control

Record:
- filename;
- issuing organ;
- proceeding and NIG;
- date/time;
- signatory and role;
- source/origin;
- hash where available;
- whether the copy is complete, partial, photographed or certified.

No substantive inference until provenance is recorded.

## Step 2 — Extract the judicial act

For the new document identify separately:
- what was requested;
- who requested it;
- opposition/positions;
- evidence expressly mentioned;
- applicable legal provisions expressly relied upon;
- reasoning;
- operative part;
- appeal route/deadline if stated.

## Step 3 — Decided / not decided

Produce two mandatory statements:

`DECIDED:` the narrowest accurate statement of the legal act.

`NOT DECIDED:` important propositions that the act does not resolve and must not later be attributed to it.

## Step 4 — Evidence-before-court delta

Compare with prior ledger state and answer:
- What new evidence was before this organ?
- Was it already before another court?
- Is there evidence it was transmitted between proceedings?
- Did the decision address it, omit it, reject it procedurally, or treat it as irrelevant?

Do not infer that silence equals rejection on the merits.

## Step 5 — Premise propagation

Check whether the act adopts a factual/legal premise from an earlier proceeding.

For every inherited premise record:
- origin decision;
- exact original holding;
- whether later use is narrower, equal to or broader than the original holding;
- whether the premise was ever substantively adjudicated.

Flag `PREMISE_EXPANSION` where a later actor appears to rely on a proposition broader than the earlier decision actually established. This is an analytic flag, not a misconduct finding.

## Step 6 — Fragmentation analysis

Tag the factual issues touched by the act, including where relevant:
- creditor identity / assignment;
- ownership / registry title;
- possession / control;
- Comunidad authority;
- hotel operation / income;
- insolvency causation;
- preservation of the estate;
- valuation;
- liquidation / adjudication;
- dación / satisfaction;
- extraconcursal Matkator rights;
- RIC/investment/public-funding context;
- alleged procedural fraud;
- accounting / surplus;
- calificación.

Then identify other proceedings containing the same issue.

## Step 7 — Consequence map

Separate:
- `FORMAL_EFFECT` — procedural/legal result;
- `EVIDENTIAL_EFFECT` — evidence admitted, excluded, stranded or newly connected;
- `PATRIMONIAL_EFFECT` — any demonstrable change to title, control, enforcement, income or recovery position;
- `DOWNSTREAM_RELIANCE` — later decision/institution relying on the act.

Do not label a patrimonial effect as judicial causation unless legally and factually demonstrated.

## Step 8 — Contradiction and convergence checks

Compare the new act against all prior records for:
- conflicting asset descriptions;
- conflicting creditor identities/amounts;
- inconsistent title assumptions;
- inconsistent descriptions of who operated the hotel;
- inconsistent treatment of the Comunidad;
- inconsistent treatment of evidence availability;
- different legal classifications of the same factual episode.

Classify each result as:
- `EXPLAINED_DIFFERENCE`;
- `UNRESOLVED_CONTRADICTION`;
- `APPARENT_CONTRADICTION_REQUIRES_CONTEXT`;
- `NO_CONTRADICTION`.

## Step 9 — Fairness / alternative explanation

For every anomaly produce the strongest non-misconduct explanation, including where applicable:
- jurisdictional limits;
- different evidential record;
- different procedural posture;
- res judicata/preclusion rules;
- timing;
- staffing/caseload;
- ordinary judicial discretion;
- party failure to put the material before the court.

Only after this step may stronger hypotheses be ranked.

## Step 10 — Hypothesis ranking

Use only these labels:
- `SUPPORTED`;
- `PLAUSIBLE_REQUIRES_MORE_EVIDENCE`;
- `WEAK`;
- `NOT_SUPPORTED`;
- `DISPROVED`.

Potential hypotheses can include fragmentation, delay, inconsistent classification, convergence, conflict risk, deliberate non-intervention or coordination. Never use `SUPPORTED` for coordination/capture without affirmative evidence beyond outcome similarity or repeated professional appearance.

## Step 11 — Public-site eligibility

A finding is public-site eligible only if:
- supported by a primary/official source or clearly labelled party position;
- wording distinguishes decided from not-decided;
- pending appeal/finality status is disclosed;
- personal data not necessary to public understanding is excluded;
- a right-of-reply/correction route remains available.

## Step 12 — Book / Por Derecho extraction

Maintain two distinct derivative notes:

**Reason to Believe:** narrative significance, scenes, chronology, institutional paradoxes and first-person experience.

**Por Derecho:** neutral methodological lesson about legal memory, provenance, traceability, reviewability and effective remedies. Do not use the Foundation layer to advocate a promoter's live private claim.
