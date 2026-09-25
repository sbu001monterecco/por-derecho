# UNITARY PUBLIC SHELL — CONTROL RECORD

**Date:** 18 August 2026  
**Status:** `IMPLEMENTATION BRANCH — EVIDENCE ARCHITECTURE PRESERVED`  
**Purpose:** convert the mature internal evidence architecture into a clearer reader-facing shell without deleting, flattening or relabelling the underlying dossiers.

## 1. Problem being solved

The repository has strong source hierarchy, correction control, missing-evidence registers, publication manifests, live-verification workflows and specialist retrieval gates. The public website has consequently accumulated many additive modules, bridges, dossiers and navigation choices. The risk is no longer lack of evidence; it is that evidential sophistication becomes harder to navigate than necessary.

The shell therefore changes **orientation**, not **substantive findings**.

## 2. New public architecture

### Case Control Room

Bilingual canonical routes:

- `/en/case-control-room/`
- `/es/sala-control-caso/`

The Control Room organises the public record into six separate but interacting systems:

1. registered property / 262-finca perimeter;
2. CEXP / productive-unit economics;
3. Concurso 36/2012 — AC / Court / calificación;
4. material control / 7 June 2018;
5. RICPE / RIC / HNT / later funding and support;
6. institutional response / answer-holders.

It presents three reader modes: **Understand → Audit → Respond**.

### Controlled search

Bilingual routes:

- `/en/search/`
- `/es/buscar/`

Search combines a curated canonical index with every route in the main sitemap as fallback. Curated aliases cover high-value discovery terms such as CEXP, `737338`, `8588`, Borja, ACTÚA, Series F and DP 1901. Search metadata is not evidential proof; canonical pages and source controls continue to govern.

### Homepage navigation

The homepage's long-form content is preserved. The dynamic shell reduces the primary navigation to a small number of reader tasks and inserts a direct Case Control Room gateway. It does not delete homepage sections or competing/adverse evidence.

### Global utility

Substantive pages receive compact global shortcuts to the Control Room and search. Existing contextual dossier navigation remains untouched.

## 3. Evidential boundaries

This release does **not**:

- establish any new criminal, civil, professional or institutional liability;
- convert a missing record into proof that the record never existed;
- merge LPB's estate with Matkator, third-party property or all CEXP assets;
- convert coexistence of financing/support into a finding of double funding or misuse;
- promote a party allegation or expert work product into an official outcome;
- overwrite the current procedural status recorded on canonical proceedings pages;
- replace primary sources, correction registers or specialist ledgers with the Control Room summary.

## 4. What would change the public interpretation

The Control Room makes falsifiability explicit. High-value evidence capable of materially narrowing or changing the present interpretation includes:

- the complete primary 2013 AC source and definitive texts resolving the CEXP `€737,338.85` item;
- delivery receipts / LexNET / docket entries / reasoned orders for the 2015–2018 CEXP attempt chain;
- a contemporaneous title/perimeter reconciliation bridging fragmented title, whole-project representation and later award/operation;
- the complete Series F/G application, idoneidad decision(s), AEAT scope and source-and-use evidence;
- any primary record contradicting or contextualising a published inference.

## 5. Technical migration boundary

`assets/site.js` is deliberately **not** rewritten in this release. Its current loader chain contains mature ordering and dependency assumptions. The unitary shell is instead bootstrapped from the already-global sharing bridge and is internally route-aware.

This creates a safe migration point. Once the new shell is green in desktop/mobile regression and deployed, legacy global modules can be migrated incrementally into route bundles without combining that risky refactor with a reader-architecture launch.

## 6. Regression standard

`.github/workflows/validate-unitary-public-shell.yml` runs a Playwright route-archetype test when the shell, shared navigation, shared CSS or selected cross-site reader/navigation modules change. It checks both languages and desktop/mobile rendering, including:

- consolidated homepage navigation;
- Control Room system count;
- controlled search functionality;
- global utility on representative existing dossiers;
- horizontal overflow;
- duplicate IDs on the new routes;
- screenshots plus machine-readable results.

## 7. Non-regression rule

Future public-site work should favour **compression, canonical ownership and progressive disclosure** over adding another competing cross-site narrative. A new module must answer one of the following:

- Does it add genuinely new evidence?
- Does it correct or narrow an existing proposition?
- Does it materially improve reader orientation or institutional answerability?

If none applies, prefer improving an existing canonical route rather than adding another public layer.
