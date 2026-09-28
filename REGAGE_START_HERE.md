# REG-AGE / RedSara: filing-status lookup first

Control: **PD-REGAGE-LOOKUP-20260928-01**. Source snapshot: 28 September 2026. This is a retrieval control, not a new event register or authority to file/contact anyone.

## Current E.G. 745/2026 correction

The substantive reposición was filed on **21 September 2026**, principal **REGAGE26e00082068814** (existing event **PD-SP-EVT-0203**). All ten linked deliveries appear as **Recibido** in the current export. The separate **REGAGE26e00082033336** of 20 September is preservation/identification, not the principal appeal. Older prepared/unverified wording is historical and must not be used to revive a missing-filing warning. Read the existing receipt controls under `evidence/preservation/eg745-redsara-revision-20260921/receipts/` and `ops/2026-09-19_DP1901_EG745_FILING_STATUS_REGISTER.md` for the filing evidence. Registration is not admission, incorporation, examination or a merits decision.

## Mandatory preflight before a missing-filing or deadline alert

1. Refresh the relevant hosts' current main and read `ops/REGAGE_CURRENT_LOOKUP.json`.
2. Retrieve the current full private registry using custody alias **PD-REGAGE-EXPORT-20260928**; its working index is named **REGAGE_CURRENT_LOOKUP**. Match exact REGAGE first, then normalized proceeding aliases and the whole delivery family.
3. Reconcile against `assets/data/institutional-communications-register-v1.json`, the existing RedSara register, the scan checkpoint and native receipt/document evidence. Preserve all existing canonical IDs and the immutable 75-receipt baseline.
4. Search email/history only for missing evidence or later developments. An empty bounded search is **not** proof of non-filing. Do not advise a duplicate submission while contradictory completed-filing evidence remains unresolved.
5. Report the source snapshot, search scope, references checked and evidence ceiling. A public cache miss requires the private registry lookup; it is not a negative legal conclusion.

The private snapshot contains **407 unique references: 361 Recibido, 20 Enviado, 26 Rechazado**, dated 7 December 2025–27 September 2026. These are literal portal transport states. They are not 407 independently verified native receipts or proof of legal merits. The original CSV is unchanged; 122 malformed rows were repaired deterministically for indexing. Exact subjects, personal identifiers and provider/custody locators remain private. Public Git contains only this minimized control and previously public filing references.

`python3 scripts/lookup_regage_registry.py 'FGE 745 of 2026'` reads the known-family cache. For all 407 entries use `--private-index /authorized/path/REGAGE_CURRENT_LOOKUP.json`. `--self-test` verifies aliases, the ten deliveries, preservation separation and the negative-search boundary. This script performs no network request or write.

For each later export, preserve the source bytes/hash and compare exact IDs; append status observations instead of deleting or renumbering history. Preserve prepared, sent, registered, received, routed, incorporated, examined, decided and relief as separate states. A later transport rejection does not erase the original presentation event.

## Español

**Consultar el registro antes de afirmar que falta una presentación.** La reposición de E.G. 745/2026 ya se presentó el 21 de septiembre con principal **REGAGE26e00082068814** y diez entregas. **REGAGE26e00082033336** corresponde a una comunicación distinta de preservación. Los estados anteriores de preparación/no verificación son históricos; no desvirtúan la prueba posterior de presentación. Consultar el registro privado actual, los identificadores exactos y sus acuses antes de alertar sobre un plazo o proponer duplicidades. **No localizado en una búsqueda limitada no equivale a no presentado.** Recibido/Enviado/Rechazado no acreditan admisión de fondo ni decisión favorable.

## Platform boundary

This control does not decide the hosts' unrelated authority/parity disputes, alter CI protections or change account-level ChatGPT settings. A Library/Drive file is a durable retrieval source, not automatic injection into every running thread. Merge, deployment and live verification require their own evidence. No email, RedSara submission or other external legal action is authorized by this update.
