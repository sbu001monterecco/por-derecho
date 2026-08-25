# Por Derecho Tech Platform — controlled development roadmap

**Control date:** 25 August 2026  
**Operational ledger:** [Issue #993](https://github.com/sbu001monterecco/por-derecho/issues/993)  
**Governing approach:** evidence first, document first, matter bounded, public/private separated, measured before scaled

## 1. Objective

Develop a durable evidence-intelligence operating system that helps Por Derecho locate, test, explain and reuse the smallest sufficient evidence set for each question while preserving legal-person, proceeding, claimant, confidentiality and publication boundaries.

The platform is not one application. It is the controlled relationship among:

```text
private native evidence
+ canonical identities and knowledge
+ retrieval and evaluation
+ human-reviewed analysis
+ GitHub governance and controlled publication
```

## 2. Current baseline

### Completed

- `PD-SP-IDENTITY-REGISTRY-001` is the authoritative identity system.
- PR #990 merged the first bounded evidence-intelligence tranche.
- `PD-SP-R-0002` is the first controlled proceeding.
- Four native RPL documents, one private manifest and one separate checksum were preserved outside public Git.
- The private pilot was read back as not shared on 25 August 2026.
- The deterministic retrieval proof passed 7/7 tests over 26 controlled sections.
- Public source classes and the foreign-matter firewall are in place.
- No automatic LLM-to-publication path exists.

### Deliberately not implemented

- bulk private-evidence migration into GitHub;
- embeddings or a vector database;
- PostgreSQL or a dedicated search cluster;
- a graph database;
- automatic website generation;
- automatic publication;
- multi-million-document infrastructure.

## 3. Permanent invariants

1. Current remote `main` is always the editing baseline.
2. The `PD-SP-P/O/S/I/R-*` identity authority is not replaced by a competing namespace.
3. Identity, association, family relationship, corporate link or co-occurrence never transfers knowledge, intent, control or liability.
4. Source authority and matter permission are resolved before retrieval.
5. Private native evidence and provider locators remain outside public Git.
6. Original evidence remains authoritative over summaries, embeddings and model output.
7. `NOT_LOCATED` never becomes `NONEXISTENT` without independent proof.
8. Retrieval packets preserve supporting, contrary, limiting, correction and open-gap material.
9. A passing technical test does not establish admissibility, liability, causation, standing or merits.
10. Publication requires a separate human decision.

## 4. Development phases

| Phase | Status | Deliverable | Entry gate | Exit measure |
|---|---|---|---|---|
| 0 — Preserve and reconcile | **COMPLETE FOR PILOT** | Identity-safe schemas, private four-document custody, public-safe hashes | Current `main`; authority confirmed | PR #990 merged; private readback complete |
| 1 — Stabilise and monitor | **ACTIVE** | Scheduled monitor, permanent baseline, deletion-safe continuity, Issue #993 | Pilot passes | Repeated monitor passes; private readback within cadence |
| 2 — Bounded second matter | **NOT STARTED** | One additional matter with explicit sources, questions and exclusions | RPL gate remains satisfied; human matter selection | Known-answer baseline passes; no leakage or entity drift |
| 3 — Private document registry | **NOT STARTED** | Private registry with versions, hashes, pages, sections and ACLs | Custody design approved | Controlled imports trace to native originals |
| 4 — Lightweight hybrid retrieval | **NOT STARTED** | Exact/full-text plus selective semantic retrieval and reranking | Lexical baseline measured; gap demonstrated | Better must-find and contrary-evidence recall without leakage |
| 5 — Dependency and recovery graph | **NOT STARTED** | Source → proposition → event → page; claimant/right/recovery objects | Canonical document and proposition model stable | Corrections and new evidence identify downstream review tasks |
| 6 — Scale decision | **DEFERRED** | PostgreSQL/pgvector, Elastic/OpenSearch or other infrastructure decision | Measured corpus, concurrency or quality threshold | Costed architecture justified by evidence, not aspiration |

## 5. Active priorities

### P0 — integrity and monitoring

- Keep `.github/workflows/tech-platform-monitor.yml` passing.
- Investigate every hard failure before expanding scope.
- Preserve the retrieval baseline in Git, not only in finite-retention workflow artifacts.
- Verify private-manifest and checksum recoverability at least every 30 days and after any custody change.
- Keep all third-party Actions pinned to immutable commit SHAs.

### P1 — retrieval quality

- Add page/section/paragraph or character-offset citation anchors where controlled sources permit.
- Measure must-find document recall, top-result accuracy and contrary-evidence recall.
- Add correction and supersession recall tests.
- Add negative tests for identity conflation, temporal-capacity drift and foreign-matter leakage.

### P1 — canonical model

- Add a legacy-ID crosswalk without renaming current public IDs.
- Extend schemas for relationships, assets, rights, custody events, contradictions, corrections and evidence gaps.
- Preserve bilingual labels and translation-review state.

### P2 — operational usefulness

- Build a counsel/institution evidence-packet template.
- Design source-to-publication dependency tracking.
- Design claimant/right/recovery objects with overlap and double-count controls.
- Establish baseline time-to-evidence metrics before estimating cost savings.

## 6. Selecting the next controlled matter

No second matter is automatic. Select it using:

- strategic relevance;
- bounded source universe;
- availability of primary and contrary evidence;
- stable entity/proceeding identities;
- measurable known-answer questions;
- manageable privilege and privacy boundaries; and
- a clear reason why the pilot improves present work.

The selection and scope must be recorded in Issue #993 before implementation.

## 7. Scale gates

### Current / approximately 10,000-document class

Prefer a lightweight path:

```text
private evidence store
+ document registry
+ metadata and full-text search
+ selective embeddings only if measured useful
+ reranking
+ GPT
+ GitHub governance
```

### Intermediate scale

Consider dedicated hybrid search when PostgreSQL/full-text quality, latency, filtering or concurrency becomes inadequate.

### Multi-million scale

Use object storage, distributed parsing, dedicated metadata/search infrastructure and hierarchical document → section → passage retrieval. Do not build this merely because it is technically possible.

## 8. Metrics

Track:

- time to locate a controlling primary source;
- must-find recall;
- exact citation rate;
- contrary-evidence recall;
- correction/supersession recall;
- entity-conflation incidents;
- temporal-capacity errors;
- foreign-matter leakage;
- privilege/private-locator leakage;
- index freshness after a source change;
- private-vault readback status; and
- time to prepare a bounded institutional evidence packet.

Leakage targets for foreign matters, private locators and privileged sources are zero.

## 9. Monitoring response

A monitor failure creates a diagnosis task. It does not authorise:

- force-pushing or reverting `main` without comparison;
- deleting or renaming IDs;
- moving private evidence into Git;
- automatically changing conclusions;
- automatically re-indexing uncontrolled sources; or
- automatically publishing model output.

Issue #993 is the durable queue for findings and development decisions.
