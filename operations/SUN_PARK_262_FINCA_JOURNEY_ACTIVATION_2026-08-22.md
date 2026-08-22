# Sun Park — 262-finca journey activation record

**Created:** 2026-08-22
**State:** DRAFT — source implementation only; not merged, deployed or live-verified
**Scope:** public-safe, bilingual finca-by-finca journey from 2008 onward, mapped to the canonical 262-row physical register.

## What this release adds

- A generated public projection at `assets/data/sun-park-262-finca-journey-v1.json`, built from the immutable 262-row physical register, the acquisition overlay and a controlled evidence ledger.
- Direct bilingual routes:
  - `/en/262-properties-journey-2008-present/`
  - `/es/fincas-262-recorrido-2008-hoy/`
- Search, finca/type/block/coverage filtering, source-status cards and a deliberately separate whole-complex context timeline from 2008 onward.
- Cross-links from the physical 262-map and Registry-method routes, search-index entries and sitemap coverage.
- Repair of the obsolete English 262-map route previously retained in the Registry page and one machine-readable case record.

## Evidence boundary

The projection covers every one of the 262 physical rows. It does **not** claim that every row has a completed historical title chain.

At creation, it contains:

- 11 fincas with one or more source-bound property-event entries;
- 8 fincas with limited source pointers only;
- 1 explicit unit/finca identifier conflict (8557 / 707–708), preserved rather than resolved;
- 249 rows explicitly marked `NOT_YET_RECONSTRUCTED`.

Whole-complex transaction, valuation, Community/CEXP, insolvency and corporate records remain `COMPLEX_CONTEXT`. They may be shown alongside a selected property for chronology, but they must never be treated as an event proving that property’s title, payment, possession, authority, debt, fraud or intent.

## Public/private firewall

The public projection excludes raw deeds, Registry extracts, personal addresses, signatures, identity numbers, bank/payment fields, private emails, recordings/transcripts, privileged advice and private-storage references. A source-family summary can be labelled `DOCUMENTED_REPRESENTATION`; it is not a substitute for re-opening the primary source under the controlled evidence process.

The source-status grammar is binding:

- `VERIFIED_OFFICIAL` / `PUBLIC_REPORT` are limited to what that source actually records;
- `DOCUMENTED_REPRESENTATION` is a controlled summary, not a current legal conclusion;
- `PARTY_ALLEGATION` is a party position, not proof of its merits;
- `WORKING_LEAD` is an unresolved recovery target;
- absence of a property event is an explicit gap, not evidence of absence.

## Priority completion queue

1. 2008 seller → finca → deed → Registry presentation/entry map.
2. 8497/8498 causal title, 2022–2025 Registry reconciliation and each party’s response.
3. 8584/8588 native deed/note and current/historic certified Registry chain, with title, possession, operation and later rights kept separate.
4. 8587 dated acquisition/title/Registry source recovery.
5. 8503–8507 JSP historical note/deed/Registry binding and no assumed bridge to any later perimeter.
6. 8499–8500 original worksheet, meaning of `CP`, authority, title, price/payment and Registry chain.
7. 8557 / 707–708 physical/Registry crosswalk reconciliation before attaching any owner, meeting or operational history.
8. Complete 2011/2016/2018/2022 meeting, authority, debt, concurso and corporate schedules before assigning any individual property effect.

## Release controls

- `scripts/build_262_finca_journey.py` regenerates the public artifact deterministically.
- `scripts/validate_262_finca_journey.py` checks 262/262 identity, source IDs, status grammar, priority safeguards, ES/EN direct pages, cross-links, route registry, sitemap and stale-route remediation.
- The dedicated GitHub Actions workflow must pass along with the repository-wide publication-integrity gate before a PR is considered ready.
- Merge and GitHub Pages verification require separate, explicit approval. A source branch or green PR is not a live publication claim.
