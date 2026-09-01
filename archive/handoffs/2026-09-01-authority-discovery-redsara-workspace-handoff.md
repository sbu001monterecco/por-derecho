# Workspace handoff — authority discovery / Red SARA/AGE register

**Handoff ID:** `PD-WCH-20260901-AUTH-REDSARA-001`  
**Workspace:** `PD-WS-20260901-0002`  
**Status:** `DELETION_SAFE_WITH_OPEN_WORK`  
**Audited main:** `4de5b4c739a5e982e7953723eb0f19e63151f83d`

## Scope and durable result

This workspace repaired the live controlled-search failure for Intervención General references and published a source-derived bilingual Red SARA/AGE filing and authority-response register. PR #1313 merged as `4de5b4c…`; its exact Pages deployment and cache-busted byte readback are recorded in `archive/AUTHORITY_DISCOVERY_REDSARA_LIVE_CLOSEOUT_01SEP2026.md`.

The canonical communications source remains `assets/data/institutional-communications-register-v1.json`. `assets/data/redsara-age-filings-register-v1.json` is a deterministic public-safe projection made by `scripts/build_redsara_age_filings_register.py`, never an independent ledger.

## Current public state

- EN: `/en/red-sara-age-filings-authority-responses/`
- ES: `/es/registros-redsara-age-y-respuestas-autoridades/`
- Site search: exact `184368/2026` resolves to `PD-SP-EVT-0141`; office search returns all three Intervención records.
- 92 individualised REGAGE events, 75 detailed baseline receipts, 100 unique attachment-index rows and 163 incoming canonical institutional events are discoverable within their controlled fields.

## Non-negotiable boundaries

- Receipt/registry evidence proves presentation metadata only; do not infer delivery, incorporation, examination, decision, reliance, payment, effect, causation, intent, offence or guilt.
- The historic 97-record total is 75 detailed + one 22-record aggregate-only batch. It is not a complete 97-row register, and it is not arithmetically reconciled to the separate 92 current event rows without a source-proved crosswalk.
- Do not invent receipt-to-attachment links. The public index supplies filename/SHA-512 and occurrence counts only.
- No private emails, provider locators, direct contact data, native receipt bundles or unredacted attachments belong in public Git.
- `^` is identity/provenance only. Criminal responsibility and knowledge do not transfer through communications, offices, tiers, filings or later benefit.

## Controls and artifacts

- `.github/governance/UNITARY_MULTI_TRACK_CRIMINAL_FIRST_PROSECUTORIAL_FORENSIC_PROTOCOL_01SEP2026.md`
- `assets/data/institutional-communications-register-v1.json`
- `assets/data/redsara-age-filings-register-v1.json`
- `archive/evidence/mf-redsara-anexo4/MF_REDSARA_ANEXO4_CANONICAL_INGEST_16AUG2026.md`
- `scripts/build_redsara_age_filings_register.py`
- `scripts/validate_redsara_authority_discovery.py`
- `archive/AUTHORITY_DISCOVERY_REDSARA_LIVE_CLOSEOUT_01SEP2026.md`

## Open work and first next actions

1. Preserve/acquire source-proved individual records for the 22-record aggregate-only RedSARA batch; keep it aggregate-only until then.
2. Seek a permitted primary source if a receipt-to-attachment mapping is required; do not reverse-engineer it from occurrence counts.
3. Advance P0 gaps `001`–`011`, `013`, `015` and `016` under their existing closure criteria, starting with native 2022 Community service/title/coefficient/proxy/debt/vote evidence.
4. Before altering communications/search data, run the deterministic builder, the specialist validator and the relevant browser smoke; after any merge repeat cache-busted live readback.

## Tooling history

Direct local `git push` was blocked by unavailable credentials. The connected GitHub integration created PR #1313 and merged it successfully. This must not be misreported as a source or institutional failure.

## New-thread bootstrap

> Continue the authority-discovery / Red SARA/AGE workspace from the repository, not chat memory. First read `CURRENT_WORKSPACE_HANDOFF.md`, then this handoff and the named canonical communications controls. Fetch current `main` before editing. Preserve all receipt, privacy, `^`, attribution and non-propagation boundaries. Do not create individual rows for the 22-record aggregate-only batch or infer receipt-to-attachment links. Continue only the recorded P0 evidence acquisition or the user’s new targeted instruction.

## Deletion-safety test

**DELETION-SAFE WITH OPEN WORK.** The public-safe implementation, deployment, exact live-byte evidence, tool limitation and open acquisition path are recorded outside this chat. The underlying evidence gaps remain open.
