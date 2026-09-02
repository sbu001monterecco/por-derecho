# Judicial and prosecutorial authority-register continuity control

**Control date:** 2 September 2026  
**Control ID:** `PD-SP-JUSTICE-AUTHORITY-CURRENT-20260902-01`  
**Status:** mandatory repository-wide governance for courts, judges/magistrates, LAJs, Fiscalía institutions and individual Fiscals/prosecutors

## 1. Controlling invariant

Every historic or current judicial or prosecutorial proceeding/file in the Por Derecho Master Proceedings Register must carry an explicit, source-led authority perimeter. The perimeter must identify, where the source permits:

- the exact proceeding and stable Master/CAEPR reference;
- the court, section, chamber, plaza or Fiscalía office as a separate CAEPR institution;
- every named judge or magistrate linked to the exact act, date and capacity supported by the source;
- every named LAJ linked to the exact act, date and capacity supported by the source;
- every named Fiscal/prosecutor linked to the exact act, date and capacity supported by the source; and
- every unresolved applicable identity as an explicit evidence gap with a defined primary-source closure trigger.

A silent blank is prohibited where a role is applicable but the source identity has not yet been recovered. Use an explicit state such as `PERSON_NOT_YET_SOURCE_IDENTIFIED`, `ROLE_NOT_APPLICABLE`, `PANEL_NOT_YET_VERIFIED` or `CERTIFIED_DOCKET_REQUIRED`.

## 2. One canonical identity, many act-specific occurrences

People and institutions are registered once under immutable CAEPR IDs. The same Judge, LAJ, Fiscal or court may be linked to more than one proceeding and more than one act. Reuse the existing ID; do not create a duplicate because the date, capacity, office or proceeding differs.

Every occurrence remains act-specific. A recurring name, current appointment, senior office, notification signature, court heading or institutional receipt does not transfer authorship, participation, knowledge, agreement, intent, responsibility, merits or outcome to another act or file.

Historic appointments, substitutions, successors and naming reforms are appended with dated boundaries. They are never overwritten by the current office-holder or current court nomenclature.

## 3. Court hierarchy

Court hierarchy is represented by explicit parent/child institution relationships, not by collapsing distinct organs.

The reference implementation is:

- `PD-SP-I-0044` — **Audiencia Provincial de Las Palmas**: master institutional identity;
- `PD-SP-I-0025` — **Audiencia Provincial de Las Palmas — Sección Segunda**: separate child-section identity; and
- `PD-SP-I-0014` — **Audiencia Provincial de Las Palmas — Sección Cuarta**: separate child-section identity.

The master court allows all proceedings at that institution to be discovered together. Each section, chamber or plaza keeps its own ID so that the competent organ for an individual act can be stated exactly. A proceeding links to the most specific source-supported organ and may additionally inherit a navigation-only link to the parent court.

A parent court identity does not prove which section received or decided a file. A child-section identity does not prove the final panel, judge, LAJ or Fiscal without the corresponding source.

## 4. Current derived justice-professional denominator

The dated 31-August-2026 48-person census remains a preserved finite execution. It is no longer treated as the whole current registry denominator.

The current derived control is `assets/data/justice-authority-register-current-v2.json`. It combines, without duplicating identities:

1. the 48-person finite census in `assets/data/justice-professionals-caret-audit-v1.json`; and
2. the 11 later source-identified La Laguna/judicial-cooperation people in `assets/data/matter-identity-registry-v1.la-laguna-judicial-people.json`.

The present source-identified denominator is therefore 59 unique named people: 56 `CARET_CONFIRMED`, three `CARET_PENDING`, zero suspended. This is complete only for the people presently registered from the recovered source corpus. It is not a claim that every historic or current official docket has been obtained.

## 5. Intake rule for every new or changed proceeding

A change introducing or materially changing a judicial/Fiscalía proceeding must, in the same change set:

1. search all CAEPR shards for the court, Fiscalía institution and every exact personal name;
2. reuse immutable IDs or allocate the next unused typed ID without renumbering;
3. bind each person to the exact act/date/capacity and supporting source;
4. register the most specific court/Fiscalía organ and its parent hierarchy where applicable;
5. update the proceeding record, Master Proceedings row or linked specialist control;
6. add reciprocal discoverability from person → proceeding, proceeding → person, court/Fiscalía → proceeding and proceeding → court/Fiscalía;
7. maintain Spanish/English public parity for public-safe material;
8. add explicit gaps for every applicable identity or act that remains unproved; and
9. run the canonical search/authority validator and all affected repository-wide validators.

Discovery of a new person or institution expands the current denominator. No validator may freeze an old dated total as the permanent global denominator.

## 6. Homepage canonical search contract

The bilingual homepages must expose a canonical search box backed by the current CAEPR registry index and the controlled public Master Proceedings projection.

Search must resolve, at minimum:

- canonical name and aliases;
- proceeding reference and secondary reference;
- NIG;
- Master Proceedings ID;
- full `PD-SP-*` identifier;
- typed caret shorthand, for example `^P-0147`, `^I-0044` or `^R-0003`; and
- numeric caret shorthand, for example `^0147` or `^0044`, with all colliding object types shown rather than silently choosing one.

Search results must display the canonical ID and object type. A search hit never upgrades evidence or expands the legal meaning of `^`.

## 7. Completion vocabulary

Use:

- `CURRENT SOURCE-IDENTIFIED DENOMINATOR VERIFIED` only for the presently registered source-backed people/institutions;
- `PROCEEDING AUTHORITY COVERAGE GAPS OPEN` where one or more applicable roles lack a primary-source identity;
- `CERTIFIED COMPLETE DOCKET` only where the official file denominator is actually established; and
- `ALL HISTORIC AND CURRENT AUTHORITY COVERAGE VERIFIED` only when every applicable Master Proceedings row is populated or carries a closed, source-defined non-applicability state and all validators pass.

The repository currently remains in global historic-docket backfill. That gap must remain visible; it must not block registration and searchability of every identity already supported by the controlled corpus.

## 8. Validation and deletion safety

`scripts/validate_canonical_home_search.py` is the deterministic gate for:

- registry shard counts and unique immutable IDs;
- the master Audiencia Provincial identity and its separately registered sections;
- the derived 59-person current denominator;
- homepage loader presence;
- accepted query-class smoke tests; and
- existence and identity markers on the bilingual master-court pages.

A successor thread must be able to recover: person/institution/proceeding identity → stable ID → source/capacity boundary → connected proceedings → parent/child court hierarchy → public route → unresolved gap, without relying on the originating conversation.

## 9. Boundary

This control registers identity, provenance, capacity and navigation. It does not determine wrongdoing, bias, coordination, receipt, personal knowledge, legal correctness, liability or outcome. It authorises no filing, service, email or third-party contact.
