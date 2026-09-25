# pd.forensic.v1

The working case is JSON with `schema`, `document`, `blocks`, `annotations`, `history`.

`document`: stable `id`, `title`, original `sha256` or null, document `date`, separate `received` date, `proceedings` array and explicit `coverage` limits.

`blocks`: unique stable `id`, original physical `page`, displayed `text`, optional `rawText`, PDF `bbox`, and `imageGap`. Source block identity must survive edits to annotations. New extraction versions require explicit anchor reconciliation, never silent index reuse.

`annotations`: unique `id`, source `block`, `start` inclusive and `end` exclusive (JavaScript UTF-16 code-unit offsets), `quote` exactly equal to the source slice, one `category`, `review`, `reviewer`, `actor` including capacity, `issue`, `note`, `limitation`, `evidence` array and optional `related` annotation IDs. Separate annotations can overlap. Use linked annotations for separate blocks.

Each evidence relation contains `relation`, `source` identifier, `locator` pinpoint and `url` (possibly blank for a private exhibit). Relations: SUPPORTS, CONTRADICTS, NOTICE, ADOPTS, RELATED, INFERRED_BRIDGE. A relation does not prove its own substance. NOTICE needs actual receipt/knowledge evidence, not merely a source's existence. Preserve adverse and exculpatory evidence.


### Optional truth-reconstruction object

An annotation may include a `truth` object. This is a backwards-compatible optional extension of `pd.forensic.v1`; absence means that no truth-reconstruction test has been recorded for that annotation.

Fields:

- `claim`: one atomic, testable proposition distilled from the exact quoted source span.
- `status`: `UNTESTED | SUPPORTED | PARTIAL | CONTRADICTED | UNRESOLVED | RHETORICAL_OR_LEGAL`.
- `omittedContext`: material context omitted, compressed or separated from the proposition.
- `powerCapacity`: the real actor, legal/economic capacity, practical power or control question that must be reconstructed before attributing conduct.
- `knowledge`: `NOT_ASSESSED | KNOWLEDGE_PROVED | NOTICE_PROVED | INSTITUTIONALLY_AVAILABLE_ONLY | INFERRED_ONLY | NOT_RELEVANT`.
- `causation`: `NOT_ASSESSED | PROVED | SUPPORTED_INFERENCE | UNSUPPORTED_INFERENCE | NOT_RELEVANT`.
- `restatement`: the minimum evidence-constrained wording that incorporates the material evidence, contrary evidence, actor/capacity, chronology and uncertainty.
- `decision`: `PROPOSED | ACCEPTED | EDITED | REJECTED | UNRESOLVED`.

Mechanical guards:
- `status=CONTRADICTED` requires at least one `CONTRADICTS` evidence relation with a source identifier and pinpoint.
- `decision=ACCEPTED` or `EDITED` requires the annotation itself to be `REVIEWED`, a non-empty reviewer identity/role and a non-empty restatement.
- A truth record is analytical work product. It does not alter the source block and is not itself evidence.
- A future AI process may create only `PROPOSED` truth records. Human review is required before acceptance or editing is treated as reviewed work product.
- Do not convert `INSTITUTIONALLY_AVAILABLE_ONLY` or `INFERRED_ONLY` into personal knowledge. Do not convert a contradiction into intent.

`history` contains dated CREATE/UPDATE events and the previous annotation for updates. History is a user-editable working audit aid. Preserve exported snapshots and hashes independently; Git authorship is not proof of the authorship of an underlying legal source.

## Public/private boundary

Only generic software, synthetic fixtures and reviewed public-safe research are committed. Private case JSON, raw originals, populated readers, detailed working annotations and provider locators remain in private custody. A future public case requires a separately reviewed/redacted derivative and explicit release review.
