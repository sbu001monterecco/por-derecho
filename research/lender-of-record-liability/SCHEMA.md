# Schema and data contract

## Unit of analysis

The system is proposition-centred, not folder-centred. A single source may support several records without being copied or re-characterised.

Each record must identify:

- deterministic ID;
- evidence status;
- publication status;
- source references;
- actor, instrument and proceeding references where relevant;
- direct proposition;
- express limit or contrary proposition;
- open fields or next action.

## ID prefixes

| Prefix | Record |
|---|---|
| `ACT-` | actor/entity |
| `INS-` | instrument, security, claim or economic unit |
| `TR-` | transfer/succession event |
| `KN-` | knowledge/notice event |
| `CD-` | conduct/decision event |
| `PROC-` | proceeding/forum |
| `SRC-` | source |
| `GAP-` | evidence gap |

IDs are stable. Correct the data behind an ID rather than silently replacing it. If a date-bearing ID is itself disproved by primary-source reinspection, replace it consistently, preserve the former identifier in `legacy_ids`, mark the reason in the source notes, and update every cross-reference in the same change.

## Date discipline

- Use ISO `YYYY-MM-DD` only where the day is supported.
- Otherwise set `date: null`, add `date_precision`, and preserve the documentary label in `date_label`.
- Do not convert upload, email-forward or repository dates into transaction dates.
- Any corrected date must be propagated to the correction register and public pages.

## Status discipline

`verified_primary` means the proposition is directly established by a primary document currently controlled.

`verified_official` means directly established by an official public source.

`documented_party_statement` means the statement was made and is documented; its substantive truth is not thereby established.

`corroborated_inference` means more than one source supports an inference, but the conclusion is not directly stated.

`contested` means a material dispute or adverse source exists.

`missing_primary` means the proposition is presently carried only as a route or partial reconstruction and the decisive instrument is absent.

`unknown` means no responsible conclusion can yet be stated.

## Capacity discipline

Do not collapse:

- owner;
- creditor;
- servicer;
- agent;
- employee;
- fund manager;
- beneficial investor;
- enforcement claimant;
- insolvency creditor;
- property owner;
- operator;
- successor company.

Authority, dependency, instruction and ratification must be evidenced separately.

## Causation discipline

Every damages proposition is represented as:

`conduct → immediate consequence → intermediate event → claimed harm → intervening causes → mitigation → confidence`

Loss is allocated to an actor-specific time window. No actor is assigned the entire history merely because it appears in the chain.

## Public-safety discipline

Public data must not contain:

- private email addresses or telephone numbers;
- raw privileged advice;
- passport/account/personal identifiers;
- unsupported criminal labels;
- conclusions that suppress an adverse ruling;
- exact confidential transaction material that has not been cleared for publication.

The validator blocks a small set of obvious unsafe patterns, but human legal review remains mandatory.
