# Ministerio Fiscal / Fiscalía full digitisation and publication execution prompt — 19 September 2026

## Mission
Close the prosecutorial documentary record from 2012 onward across **all identifiable Ministerio Fiscal/Fiscalía offices**, fully digitise every located source, and publish every public-safe PDF through bilingual embedded viewers with source-bounded context, evidential limits and reciprocal interconnectivity.

## One-lane rule
Use current GitHub main and Control Tower #1428. Maintain **one current-main Fiscalía integration lane**. Research workers may run in parallel but must return deltas to that lane. Never create competing Fiscalía publication PRs. If an active lane is stale, preserve its unique delta, replay it once from current main, mark the predecessor superseded and stop feeding it.

## Sources
Read all three connected Gmail accounts, connected Drive and authorised Library/private custody. Continue pagination and exact/variant searches. Cover every office actually evidenced, including FGE, Inspección Fiscal, Delitos Económicos, Anticorrupción, Canarias superior/autonomous, Las Palmas Provincial, Arrecife/Puerto del Rosario, Audiencia Nacional-linked routes, Tenerife where source-proved, and any additional office or specialist unit found. Empty bounded search = BOUNDED-NOT-LOCATED, never non-existence.

## Per-document control
For every act/message/attachment preserve native provenance, account/message/thread or Drive ID privately, office, sender/recipient, act/transmission/receipt/registration dates, filename/MIME/size/hash/page count, signatory/capacity, file/proceeding, document type and parent-attachment relationship. Deduplicate by bytes while retaining each transmission occurrence. Keep separate states for sent, registered, received, routed, incorporated, examined, decided, served, final and implemented.

## Digitisation
Preserve native bytes unchanged. Extract native text. Use governed OCR only for image-only/poor pages and keep OCR/transcription separate from the original. Visually verify material dates, signatures, references and dispositive text before relying on OCR. Maintain: NATIVE_PRESERVED → TEXT_EXTRACTED/OCR_DERIVATIVE → SUBSTANTIVELY_REVIEWED → PUBLIC_DERIVATIVE_READY → PUBLIC_VIEWER_LIVE. CERTIFIED_FILE_COMPLETE is separate and requires a certified denominator/index.

## PDF publication
Canonical public register: `assets/data/ministerio-fiscal-pdf-room-20260918.json`.
Office coverage ledger: `assets/data/ministerio-fiscal-office-digitisation-20260919.json`.
Rooms: `/es/ministerio-fiscal-documentos-pdf/` and `/en/public-prosecution-pdf-document-room/`.
Every public-safe PDF must land atomically with: registry row, both embedded viewers, what-it-is context, why-it-matters, what-it-establishes, what-it-does-not-establish, proceeding link, wider Ministerio Fiscal/E.G. 745 link, any supported actor/event/gap links, sitemap/search and validator coverage. Private natives remain private; create separately hashed/redacted derivatives.

## Interconnectivity
Reconcile source → communication/event → office/file → proceeding → actor/capacity → proposition → contrary record → gap → next action. Keep offices and proceedings distinct. Cross-linking never proves knowledge, intent, coordination, responsibility or guilt.

## Priority corpus
2019 calificación; DI 248/2018; DI 113/2022; DI 22/2026; DIP 2/2026; EG 49/2026; EG 58/2026; EG 86/2026; EG 112/2026; EG 352/2025 where sourced; EG 745/2026; DP 1901/2026 Fiscal-report lane; DP 1956/2026 if Fiscal material exists; 2–3 Aug 2026 REGAGE routes; remittal/routing/joinder chains; and older 2012–2018 Fiscalía material connected to Concurso 36/2012 / Sun Park.

## Merge/deploy
Refresh main immediately before any write and merge. One logical release = one integration PR. Require exact-head Release acceptance, Publication integrity, PDF-room/full-digitisation validation and affected specialist checks. Do not weaken gates. When green and current/mergeable, merge normally. For public changes verify the exact merged SHA in Pages and anonymously read back both rooms, all new PDF URLs/viewers and affected reciprocal links before LIVE_VERIFIED. Run preservation once for a materially new main.

## CI leverage
Do not fix broad CI fan-out inside an evidence PR. Record unnecessary generic triggers and, if justified, use one separate backend-only PR with proof that path filters preserve required coverage.

## Output
Each pass records offices searched, queries/cursors, documents found, natives acquired, hashes/pages, duplicates, substantive reviews, derivatives, viewers, links, closed gaps, authority-only gaps, conflicts, integration head/CI, merge/deploy/readback and E.G. 745 consequences. Never claim all-office completeness until the office/file denominator and all cursors/certified indexes support it.
