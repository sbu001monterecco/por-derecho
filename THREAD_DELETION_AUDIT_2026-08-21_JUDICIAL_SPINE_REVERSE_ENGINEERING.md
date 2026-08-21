# Thread deletion audit — Judicial spine reverse-engineering

> **HISTORICAL AUDIT — SUPERSEDED IN PART LATER 21 AUGUST 2026.** The previously missing Auto 164/2021, both 15-October Autos and both 26-January clarification Autos are now controlled. Protocol 457 internally recites 26 January on page 10 and 22 January on page 11; the signed judicial originals are dated 26 January. Current control is `archive/CONCURSO_36_2012_PRIMARY_AUTOS_REDIGEST_HANDOVER_21AUG2026.md`.

**Date:** 21 August 2026  
**Thread scope:** reverse-engineering digest of the Por Derecho repository/live website followed by implementation of the recommended Concurso 36/2012 judicial-spine architecture.

## Material project intelligence generated in this thread

1. The principal architectural weakness identified was the absence of one canonical **judicial-order spine** linking authorization, competition, orders, deed, Registry and accounts.
2. Generic shorthand such as **“the 26 January 2022 adjudication order”** is unsafe because the repository records a deed recital referring to **22 January 2022** while other materials refer to **26 January 2022**. The safe current treatment is a **January 2022 order/clarification family** pending instrument-by-instrument recovery.
3. Canonical money-function rule: **recognized insolvency credit ≠ mortgage liability ≠ third-bidder threshold ≠ debt stated as consideration for dation ≠ Registry value ≠ eventual surplus/remanente**.
4. Three linked reconstruction controls were adopted: **Order→Asset**, **Order→Money**, and **Order→Implementation**.
5. P0 evidential chain: original signed 18/05/2021 Auto; both 15/10/2021 orders and docket sequence; complete January-2022 family; 2021–2022 testimonios and downstream use; post-deed court/Registry chain; AC accounting bridge including EUR 400,000 and any surplus/remanente.
6. LPB estate property must not be merged by shorthand with Matkator or other third-party property.

## Repository preservation performed

The following files were created on the current implementation branch and are intended for `main`:

- `CONCURSO36_JUDICIAL_ACTS_IMPLEMENTATION_REGISTER_21AUG2026.md`
- `assets/data/concurso36-judicial-spine-v1.json`
- `es/concurso-36-2012-columna-judicial/index.html`
- `en/concurso-36-2012-judicial-spine/index.html`
- `sitemap-judicial-spine.xml`
- this deletion audit

The implementation was rebased onto fresh `main` after a concurrent-update conflict was detected; no concurrent work was force-overwritten.

## Existing canonical controls relied upon

- `archive/MISSING_EVIDENCE_REGISTER.md`, especially existing ME-005–ME-008, ME-011 and ME-012;
- `archive/CORRECTION_REGISTER.md`;
- `CHATGPT_START_HERE.md` and its evidence/source-status discipline;
- the existing bilingual 2022 adjudication reconstruction.

The new judicial-spine files consolidate and route those controls; they do **not** duplicate the Missing Evidence Register or convert open items into findings.

## Evidential and publication safeguards preserved

- Missing evidence is not evidence of non-existence or wrongdoing.
- Later recitals do not outrank signed original judicial acts.
- Apparent contradictions remain open to contextual resolution.
- The EUR 14.8m third-party proposal is not proof that the bidder had to prevail.
- Deed 457 is primary evidence of what it states/effects within scope, not automatic proof that every debt component was legally correct.
- Registration is not automatic proof of compliance with every prior judicial or accounting condition.
- No surplus/remanente is asserted as established or excluded pending primary accounts.
- Adverse and exculpatory evidence must continue to propagate with equal source-status discipline.

## Deletion-safety decision

**SAFE TO DELETE THIS CHAT THREAD once the implementation PR is merged into `main` and the merged state is verified.**

After merge, the repository will contain the substantive reasoning, correction, priorities and public implementation needed for continuity without reliance on this chat.

## Future pickup instruction

A future thread touching the 2021–2022 adjudication/judicial chain should begin with:

1. `CONCURSO36_JUDICIAL_ACTS_IMPLEMENTATION_REGISTER_21AUG2026.md`;
2. `assets/data/concurso36-judicial-spine-v1.json`;
3. `archive/MISSING_EVIDENCE_REGISTER.md`;
4. `archive/CORRECTION_REGISTER.md`;
5. the bilingual 2022 adjudication page;
6. any newly recovered signed judicial originals.

Any recovered primary act must update the existing canonical node and propagate corrections rather than generating a competing parallel chronology.
