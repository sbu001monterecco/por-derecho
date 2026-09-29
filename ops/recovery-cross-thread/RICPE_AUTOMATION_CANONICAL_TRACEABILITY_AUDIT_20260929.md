# RICPE public-scan continuity, preservation and canonical-traceability audit

**Control date:** 29 September 2026  
**Audit class:** THREAD-DELETION / AUTOMATION / CANONICALISATION / TRACEABILITY  
**Parent register:** `PD-SP-RICPE-CAPITAL-ACTOR-REGISTRY-001`  
**Investor register:** `PD-SP-RICPE-INVESTOR-REGISTRY-001`

## Executive status

| Control | Status | Finding |
|---|---|---|
| Durable investigative state outside chat prose | 🟢 GREEN | Continuity audit, recursive plan, public-source universe and actor register are preserved in GitHub and GitLab branches. |
| Search/scan prompts are repository-first | 🟢 GREEN | Active RICPE tasks instruct each run to reconstruct state from canonical repository files, not from conversational memory. |
| Scheduler metadata fully detached from originating chat | 🟠 AMBER | ChatGPT task metadata currently exposes a conversation association. The task logic is repository-driven, but this audit must not claim the scheduler object is UI-detached from the chat. |
| Repository-native off-thread source watch | 🟢 GREEN / STAGED | A repository-native scheduled GitHub Actions source-watch workflow and scanner are staged in the continuity branch. Once merged to default branch, the scheduled watch is independent of this chat transcript. |
| GitHub canonical promotion | 🟠 AMBER | PR #2039 is open; branch content is durable but not yet protected-main canonical. |
| GitLab canonical promotion | 🟠 AMBER | MR !722 is open. Current MR pipeline has failed and the branch is behind protected main; no merge/live claim is permitted until reconciled and green. |
| Canonical IDs and crosswalk discipline | 🟢 GREEN | RICACT/RICORG/RICINV references are stable domain objects; global PD-SP-P/O crosswalks are evidence-gated. |
| Provenance / source traceability | 🟢 GREEN | Every promoted fact must retain source URL/document, title, publication/observation date, retrieval date, source type, status and relevant excerpt/proposition. |
| Evidence-state grammar | 🟢 GREEN | PRIMARY_CONFIRMED / DIRECT_PUBLIC_SOURCE / CORROBORATED_PUBLIC_SOURCE / CANDIDATE / CONTRARY / UNRESOLVED states are preserved. |
| Duplicate / alias control | 🟢 GREEN | Never merge identities by surname, geography, family/business network, employer or timing alone. |
| Privacy boundary | 🟢 GREEN | Public professional/business research only; no private home/contact data, leaked datasets, credentials, KYC/banking/source-of-funds or unnecessary family-life data. |
| Adverse-inference firewall | 🟢 GREEN | Investment, employment, Board membership, event attendance or professional service alone carries no adverse inference. |
| Autonomous third-party contact | 🟢 GREEN | Prohibited. Search/scan automation cannot contact investors, employees, family members, advisers, authorities or other third parties. |
| Public-deployment claim | 🟢 GREEN | No public-page/live claim without deployment evidence and anonymous readback. |
| Full public-internet completeness | 🟠 AMBER | No system can truthfully claim that “all public internet databases” are exhaustively scanned. Coverage must be measured by source families, queries, dates, visited-set and explicit gaps. |

## Canonical-addition rule

**Everything materially added by automated or manual research must enter through a canonical object and traceability chain. Free-floating findings are not complete work.**

For every material discovery:

1. **Source object** — identify source family, URL/document, title, publisher/custodian, date, retrieval timestamp and source grade.
2. **Identity object** — allocate/reuse `PD-SP-RICACT-####` / `PD-SP-RICORG-####` and search the global `PD-SP-P-####` / `PD-SP-O-####` registry before crosswalk.
3. **Investor-position object** — use `PD-SP-RICINV-####` only where an investor/shareholder position is evidenced; keep it distinct from personal/corporate identity.
4. **Event object** — capital increase, subscription, transfer, Board appointment, investor event, representation delivery or correction gets a dated event reference where material.
5. **Relationship edge** — state the exact relationship and date; do not infer knowledge, control, family relationship, coordination or liability from graph proximity.
6. **Evidence proposition** — record the proposition supported, evidence state, limitations and contrary material.
7. **Gap object** — unresolved identity, missing primary record or contradictory source remains explicit and generates the next bounded query.
8. **Repository provenance** — preserve through governed branch + PR/MR; retain commit SHA and source path.
9. **Public/private boundary** — public-safe derivative only where proportionate; controlled/private evidence stays outside public projection.
10. **Readback** — if something is represented as publicly deployed, verify the live bytes/content independently.

## Raw automation output is not automatically canonical

A crawler/search result, task message, workflow artifact or search-engine hit is an **intake record**, not a canonical fact. Promotion requires:
- source read;
- identity reconciliation;
- evidence-state classification;
- duplicate check;
- contradiction check;
- canonical ID/event allocation where applicable;
- governed repository change;
- review/CI appropriate to the destination.

## Full traceability minimum fields

`source_id`, `source_family`, `source_url_or_document_ref`, `publisher_or_custodian`, `source_date`, `retrieved_at`, `retrieval_method`, `content_hash_when_bytes_preserved`, `canonical_actor_or_org_ref`, `global_identity_crosswalk_status`, `event_or_capital_ref`, `investor_position_ref_if_any`, `proposition`, `evidence_state`, `contrary_evidence`, `privacy_class`, `repository_path`, `commit_or_mr_pr_ref`, `next_gap_query`.

## Thread deletion conclusion

The substantive continuity package is externalised in repositories and the active research prompts are repository-first. However, because the current ChatGPT task metadata still records a conversation association, this audit deliberately does **not** claim complete scheduler-level detachment from the originating chat. Repository-native scheduled watching is staged as the independent off-thread layer.

Deletion of this conversation must therefore never be treated as deletion of the canonical research record. The repository records, immutable IDs and source-ledger rules are the durable continuation point.
