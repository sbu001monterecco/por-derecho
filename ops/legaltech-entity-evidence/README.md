# Canonical identity, search and evidence intake — control 4 September 2026

## Purpose

This module turns repository pages, evidence manifests, Library holdings and sanitised mailbox hits into one governed discovery pipeline. It deliberately separates **discovery**, **identity resolution**, **matter-specific relationship proof**, **search publication** and **evidence publication**.

## Non-negotiable legal rules

1. A name hit is not an identity finding.
2. A shared document, email thread, employer or adviser is not proof of mandate, knowledge, information flow, control, conflict, concertation, intent or liability.
3. Every relationship edge must state matter, capacity, date/period, source and evidential boundary.
4. Diacritic, punctuation and spelling variants are retrieval aliases only. They do not create another person or entity.
5. Similar names remain separate. In particular, **Uría Menéndez is not Uriel Abogados**.
6. Public search is generated from canonical shards. Page-specific JavaScript may add presentation, but may not become the only identity register.
7. Mailbox and Library discovery is private by default. Raw bodies, attachments, addresses, phone numbers, account data, verification codes and privileged material may not enter the public repository automatically.

## Pipeline

### 1. Repository census

`scripts/build_entity_census.py` scans controlled text formats. It extracts explicit canonical labels, legal-entity patterns and role/name patterns; resolves aliases against the canonical registry; and assigns an immutable fingerprint to unresolved candidates.

CI runs the census on every relevant pull request, on `main`, and daily. It fails on duplicate IDs, canonical-name collisions, stale shard counts, unresolved `YES_NOW` decisions, unknown `data-canonical-id` references, and the Uría/Uriel collision regression.

### 2. Mailbox intake

A credentialed connector or private worker searches changed messages and attachments. It must emit only records conforming to `email-intake-schema.json`; `scripts/import_email_entity_candidates.py` rejects raw/sensitive keys and merges only sanitised metadata: hashes, dates, hit location and source class. It must distinguish direct sender/recipient hits from message-body, quoted-body, attachment-text and later-summary hits.

The public repository never stores the raw mailbox content. A mailbox hit enters `candidate-decisions.json` as `MAYBE_HOLD` unless exact identity and matter-specific role are supported by an admissible/publication-safe source.

### 3. Review queue

Open `review.html`. The controls are:

- **YES / REGISTER NOW** — source-supported identity; allocate/resolve one immutable ID and publish only proved roles.
- **MAYBE / HOLD** — preserve a redacted locator and obtain disambiguating evidence.
- **NO / REJECT** — retain the rejection fingerprint to stop recurring false positives.

The page stores decisions locally and exports a JSON bundle. Static GitHub Pages cannot safely write to the repository; the exported bundle is reviewed in a pull request.

### 4. Evidence triage

`evidence-triage-v1.json` is the first high-priority Library selection. Each item is classified as full public/redacted, excerpt, image capture, metadata only, private only or no evidence use. Derived summaries and graphics cannot prove the underlying proposition.

## Search design

`assets/canonical-home-search-20260904.js` provides:

- accent and punctuation normalisation;
- exact canonical names, aliases, NIF/NIG and immutable IDs;
- collapsed phrase matching (`UriaMenendez`);
- all-token and prefix matching;
- bounded one-edit typo tolerance for longer tokens;
- recursive indexing of public matter roles and evidence IDs;
- stable-ID deduplication;
- a collision-safe appendable API for later controlled shards;
- matter-boundary language in the interface.

## Current Uría correction

Uría was previously visible in page-specific assets but absent from the identity shards consumed by homepage search. The new organisation and professional-person shards register the firm and six source-supported lawyers. `Javier González` remains in the review queue because the located record does not uniquely identify the person or establish a client/mandate.
