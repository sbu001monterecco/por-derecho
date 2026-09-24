# R33 cumulative processing ledger and continuity adjunct

Control: **PD-R33-CONTINUITY-20260924-01**. Date: **24 September 2026**.
Parent controls remain **PD-AC-CLAIMS-R33-20260922-01** and **PD-LAW-TRUTH-20260922-01**.
This is one execution-history adjunct to C36-SPECIALIST-R33, not a new claims, actor, source or proceeding register.

## Executed correction

The historical v3 package is recovered from private Library custody. Its ZIP, populated case JSON and matrix match the retained hash manifest. The embedded native PDF matches the existing signed-source hash. The ZIP member JSON/CSV equal the separately retained objects. Earlier Drive-only nondiscovery remains an accurate historical observation, not the current custody state.

Initial review: 181 blocks, 172 annotations (148 index + 24 focused). Run 2: 186 blocks, 261 annotations (148 index + 113 focused), with every initial ID retained and 89 additions. Historical v3: 206 blocks, 276 statement annotations and 206 paragraph composites, totaling 482 annotations. The CSV contains 276 statement rows. Eight stored CONTRADICTS edges are four statement/paragraph pairs; they are provisional inherited relations, not eight independently verified contradictions.

All 915 stored quotation anchors across the three versions validate. All 251 deterministic-successor spans also bind to actual preserved Run-2 blocks. These counts include repeated text and do not measure independent evidence. Native PDF visual/signature verification was not repeated by this tool.

The complete 276-to-251 statement crosswalk yields 215 unique exact-text candidates, 3 ambiguous exact matches, 16 split/merge/scope candidates and 42 unlocated text counterparts. Six successor units have no selected candidate. Unmatched text is not lost evidence: all old/new objects and rows remain preserved, and image transcription, segmentation and scope require review. Equal wording is not semantic equivalence or independent corroboration.

## Executable adjunct

`legaltech/unitary_review/r33_continuity.py` supplies:

- validated quotations, explicit UTF-16/codepoint offsets, version occurrence IDs and source-span fingerprints;
- complete many-to-many crosswalks retaining ambiguity and disabling automatic assessment transfer;
- source-tree inventories with hashes and explicit unreadable, oversized, binary, symlink and type exclusions;
- bounded paginated retrieval, total candidates, next offset and declared host/snapshot scope, without a misleading host-completeness percentage;
- changed-inventory detection and cycle-safe dependency re-review queues;
- required fields for a separate human/source relation review, never automatic evidential promotion;
- append-only event construction, expected-tip checks and hash-chain verification.

The actual finite traversal visited 482 preserved annotation nodes plus three custody/denominator/publication-metadata targets. All 482 retained their prior substantive assessments. The three repository targets are integration tasks, not completed website changes.

A bounded retrieval exercise ran the 251 proposals against one shared R33 claim-family control on each pinned host. The two files are byte-identical and count as ONE content source. It is a technical test, not a new primary-source or exhaustive repository investigation. The populated output remains private.

## Reproduction

Requires Python 3.10+ and only its standard library. Run from repository root:

```sh
python -m unittest discover -s recovery_tests -p 'test_r33_continuity.py' -v
python -m legaltech.unitary_review.r33_continuity \
  --case /private/initial-case.json \
  --case /private/run2-case.json \
  --case /private/v3-case.json \
  --case /private/segmentation-case.json \
  --out /private/new-version-directory
```

The CLI never executes embedded HTML, retrieves credentials, contacts external services, edits input files, or overwrites an existing output directory. For recovered HTML, extract only the JSON script data and preserve the exact carrier separately. Verify carriers against their retained hashes.

For substantive comparisons, call `bind_successor(proposal, parent_case)` before relying on self-hashed segmentation; call `crosswalk` separately for statement and paragraph levels. Keep original annotations and assessment history even when a text match is exact.

For incremental work: take two explicit `snapshot` inventories; use `source_delta` to identify changed paths; supply source-grounded dependency edges to `invalidated`; record each human/source decision or no-change result through `append_event`, using the current ledger tip; verify and save a new private version. A caller-declared revision is not remote authentication. File persistence and provider concurrency must be controlled separately.

## Processing ledger contract

Every event records input versions, actual examined sources, affected propositions, before/after state, contrary evidence, dependencies, reason, integration and publication state. Keep HISTORICAL_REPORTED separate from EXECUTED. Count evidence review, segmentation, integrity checks, translation, presentation, preservation, tooling and no-change separately. A historical processing timestamp is not proof of the first ChatGPT upload.

The complete 15-event ledger, original case objects, private source identifiers, source-linked rows and review queue are in controlled private custody. The sibling JSON is only its public-safe projection and checksum pointer. It does not replace the private ledger or imply public disclosure of it. Hash linking detects changes relative to a pinned tip; it is not inherently tamper-proof or a certified evidence chain.

## Integration and propagation

This contribution is a **tested worker implementation**, not main integration or a public release. Thirty-nine local regression tests pass. No remote mandatory CI, merge, deployment or live readback is asserted. Existing !542 and !556 remain the relevant integration lanes; preserve their distinct code, source and public-reader obligations. Do not blindly merge stale branches or create an alternative release chain.

Apply the recovery correction additively to the historical activation control when that lane is reconciled. Link this ledger adjunct from the existing R33/AC canon and professional Truth Machine control through the current integrator, without replacing claim IDs. Update publication metadata only after actual adoption, and refresh any affected reader through its own existing release gates. Three pending metadata targets are explicitly recorded; none is marked completed merely because this worker package exists.

All populated work product, native evidence, private locators and original carriers stay outside Git. Repository code and this aggregate record are public-safe. No automatic lie, intent, guilt or credibility score; no inference of receipt, reading, authority or liability from a link; no email, court filing, social post or external contact.
