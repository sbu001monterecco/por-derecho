# pd.forensic.v1

The working case is JSON with `schema`, `document`, `blocks`, `annotations`, `history`.

`document`: stable `id`, `title`, original `sha256` or null, document `date`, separate `received` date, `proceedings` array and explicit `coverage` limits.

`blocks`: unique stable `id`, original physical `page`, displayed `text`, optional `rawText`, PDF `bbox`, and `imageGap`. Source block identity must survive edits to annotations. New extraction versions require explicit anchor reconciliation, never silent index reuse.

`annotations`: unique `id`, source `block`, `start` inclusive and `end` exclusive (JavaScript UTF-16 code-unit offsets), `quote` exactly equal to the source slice, one `category`, `review`, `reviewer`, `actor` including capacity, `issue`, `note`, `limitation`, `evidence` array and optional `related` annotation IDs. Separate annotations can overlap. Use linked annotations for separate blocks.

Each evidence relation contains `relation`, `source` identifier, `locator` pinpoint and `url` (possibly blank for a private exhibit). Relations: SUPPORTS, CONTRADICTS, NOTICE, ADOPTS, RELATED, INFERRED_BRIDGE. A relation does not prove its own substance. NOTICE needs actual receipt/knowledge evidence, not merely a source's existence. Preserve adverse and exculpatory evidence.

`history` contains dated CREATE/UPDATE events and the previous annotation for updates. History is a user-editable working audit aid. Preserve exported snapshots and hashes independently; Git authorship is not proof of the authorship of an underlying legal source.

## Public/private boundary

Only generic software, synthetic fixtures and reviewed public-safe research are committed. Private case JSON, raw originals, populated readers, detailed working annotations and provider locators remain in private custody. A future public case requires a separately reviewed/redacted derivative and explicit release review.
