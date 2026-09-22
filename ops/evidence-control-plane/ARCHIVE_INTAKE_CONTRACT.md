# Controlled archive intake contract

## Scope

This contract applies to ZIP, RAR, 7z, TAR and similar archive carriers recovered from email, Drive, Library, local custody or other authorised sources.

## Evidence rule

The archive carrier is itself an evidence object. Preserve it unchanged before extraction.

Required sequence:

1. identify provider/source, message/file ID where lawfully retainable, filename, MIME type, size and acquisition time;
2. acquire the native bytes through an authorised route;
3. calculate and record SHA-256 before extraction;
4. place a working copy in an isolated staging area;
5. enumerate members without executing any file;
6. reject path traversal, absolute paths, device files, symlinks to outside staging and unsafe names;
7. bound recursion, member count, expanded size and compression ratio to avoid archive bombs;
8. hash every extracted member and preserve its original archive path;
9. identify nested archives as separate child carriers and recurse only under the same safeguards;
10. classify privacy/privilege/publication restrictions before any repository admission;
11. deduplicate by hash while preserving every provenance edge;
12. create member-level canonical evidence IDs only after intake; extraction alone does not authenticate contents;
13. retain the carrier hash, member manifest, extraction tool/version and any errors;
14. never interpret an unsupported connector preview as evidence that the native archive is absent.

## Status boundaries

- `DISCOVERED` means a carrier reference was located.
- `ACQUIRED` means native bytes were actually retrieved.
- `HASHED` means integrity fingerprinting completed.
- `EXTRACTED` means member enumeration/extraction completed safely.
- `SUBSTANTIVELY_REVIEWED` requires content review; it cannot be inferred from successful extraction.
- public release requires an independent privacy/publication decision.

## Mailbox application

Historical mailbox archives are recovered source carriers, not bulk truth imports. Every member inherits the carrier provenance but must receive its own evidential status, source date, actor/capacity attribution where relevant, contrary-evidence review and publication classification.

## Preservation failure handling

If an archive cannot be acquired through the current connector, create a `PRESERVATION_GAP` or source-recovery task with the exact message/file reference and limitation. Do not silently mark it reviewed or missing.
