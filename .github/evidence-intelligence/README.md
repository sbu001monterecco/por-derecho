# Por Derecho Tech Platform — evidence-intelligence control plane

**Control date:** 25 August 2026  
**Status:** additive, Pages-neutral, monitored pilot  
**First controlled matter:** `PD-SP-R-0002` — RPL 2523/2025  
**Development ledger:** [Issue #993](https://github.com/sbu001monterecco/por-derecho/issues/993)

## Purpose

The **Tech Platform** is the controlled system joining five separate planes:

1. private native-evidence custody;
2. canonical identities, matters, proceedings, events and propositions;
3. retrieval and evaluation;
4. human-reviewed analysis; and
5. Git-versioned governance and controlled publication.

It is not a direction to place the entire corpus into an LLM. The governing sequence is:

```text
native evidence (private)
  -> stable public-safe IDs and hashes
  -> current matter/proceeding/entity controls
  -> document-first hybrid retrieval
  -> supporting + contrary + limiting + correction + open-gap packet
  -> human review
  -> separately authorised publication
```

## Identity authority

The existing `PD-SP-IDENTITY-REGISTRY-001` remains authoritative for people, organisations, structures, institutions and proceedings:

- `PD-SP-P-####` — person;
- `PD-SP-O-####` — organisation;
- `PD-SP-S-####` — structure;
- `PD-SP-I-####` — institution; and
- `PD-SP-R-####` — proceeding.

The platform does **not** create a competing `PD-ENT-*` system. New evidence-intelligence object types use longer, non-colliding extensions defined in `id-extension-policy.json`.

Identity resolves identity only. It never transfers knowledge, intent, control, benefit, responsibility or liability.

## Public/private boundary

The public repository may contain schemas, stable IDs, hashes, sizes, evidence states, limitations, test questions and public-safe retrieval results. It must not contain live Gmail message IDs, provider attachment IDs, Google Drive file IDs, private URLs, privileged source bodies or reversible private-vault locators.

The private custody manifest for the first pilot is held outside GitHub. `pilots/rpl2523/custody-public-summary.json` exposes only the minimum public-safe integrity record.

## Retrieval proof

The RPL 2523 pilot intentionally starts without a vector database. It combines:

1. mandatory proceeding filtering;
2. exact and BM25-style lexical retrieval;
3. controlled synonym expansion;
4. structured metadata boosts; and
5. source-priority reranking.

This proves retrieval discipline before introducing embeddings. The runner fails if known controlling sections are not retrieved or if a forbidden conclusion appears.

The durable baseline is recorded in `pilots/rpl2523/baseline-result.json`.

## Foreign-matter firewall

Generic architecture may be classified as `TECHNICAL_REFERENCE`. No live third-party matter record, person, company, fact pattern or example may enter Por Derecho entity, proposition, timeline, evaluation or publication data solely because it appeared in an external technical note.

The rule is:

```text
source authority -> matter boundary -> permission -> retrieval
```

not:

```text
semantic similarity -> assumed relationship
```

## Monitoring and future development

- Scheduled and change-triggered platform monitoring: `.github/workflows/tech-platform-monitor.yml`.
- Development roadmap: `TECH_PLATFORM_ROADMAP.md`.
- Future-thread operating prompt: `TECH_PLATFORM_FUTURE_THREAD_PROMPT.md`.
- Permanent operational ledger: Issue #993.
- Thread closeout/deletion record: `docs/deletion-audits/2026-08-25-tech-platform-evidence-intelligence-thread.md`.

A failed monitor is a signal to diagnose drift. It does not authorise deletion, identity remapping, public exposure, automatic private-evidence indexing or automatic website publication.
