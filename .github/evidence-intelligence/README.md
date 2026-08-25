# Por Derecho evidence-intelligence control plane

**Control date:** 25 August 2026  
**Status:** additive, Pages-neutral pilot  
**First controlled matter:** `PD-SP-R-0002` — RPL 2523/2025

## Purpose

This directory introduces the minimum public-safe control layer needed to connect the existing Por Derecho identity registry, evidence maps, retrieval tests and private native-evidence custody without moving restricted source material into the public repository.

The governing sequence is:

```text
native evidence (private)
  -> stable public-safe IDs and hashes
  -> current matter/proceeding/entity controls
  -> document-first hybrid retrieval
  -> supporting + contrary + limiting + open-gap packet
  -> human review
  -> separately authorised publication
```

## Identity authority

The existing `PD-SP-IDENTITY-REGISTRY-001` remains authoritative for people, organisations, structures, institutions and proceedings:

- `PD-SP-P-####` — person
- `PD-SP-O-####` — organisation
- `PD-SP-S-####` — structure
- `PD-SP-I-####` — institution
- `PD-SP-R-####` — proceeding

This pilot does **not** create a competing `PD-ENT-*` system. New evidence-intelligence object types use longer, non-colliding extensions defined in `id-extension-policy.json`.

Identity resolves identity only. It never transfers knowledge, intent, control, benefit, responsibility or liability.

## Public/private boundary

The public repository may contain schemas, stable IDs, hashes, sizes, evidence states, limitations, test questions and public-safe retrieval results. It must not contain live Gmail message IDs, provider attachment IDs, Google Drive file IDs, private URLs, privileged source bodies or reversible private-vault locators.

The private custody manifest for this pilot is held outside GitHub. `custody-public-summary.json` exposes only the minimum public-safe integrity record.

## Retrieval proof

The RPL 2523 pilot intentionally starts without a vector database. It combines:

1. mandatory proceeding filtering;
2. exact and BM25-style lexical retrieval;
3. controlled synonym expansion;
4. structured metadata boosts; and
5. source-priority reranking.

This proves the retrieval discipline before introducing embeddings. The runner fails if known controlling sections are not retrieved or if a forbidden conclusion is produced.

## Foreign-matter firewall

Generic architecture may be classified as `TECHNICAL_REFERENCE`. No live third-party matter record, person, company, fact pattern or example may enter Por Derecho entity, proposition, timeline, evaluation or publication data solely because it appeared in an external technical note.
