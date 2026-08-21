# Thread-deletion audit — Controls 21, 22 and 24 full-text archive

Audit date: **21 August 2026**.

## Durable state created

- Exact source filenames, page counts, byte sizes and SHA-256 values are recorded in `archive/controls/master-manifest.json`.
- Complete public text editions exist for the filed complaint text of Controls 21, 22 and 24, the filed Control 21 guide/amendment, and the filed Control 24 complement.
- Each page is traceable to the source PDF page; public redactions are explicit.
- Filing dates, later procedural identifiers, version candidates and route exclusions are recorded in the per-control README files and crosswalk.
- Annex boundaries and the Control 21 printed-index/page-boundary discrepancy are preserved.
- Source PDFs, stamped copies, custody emails and personal identifiers remain outside public Git.

## Non-reconstructable state deliberately not stored publicly

- private mailbox content and message identifiers;
- stamped images containing personal contact data and signature;
- unredacted source binaries;
- privileged communications and unrestricted annex dumps;
- credentials or connector state.

## Rebuild rule

`scripts/build_control_full_text_public.py` may rebuild the public text only when the private source files match the fixed SHA-256 values embedded in the script. A mismatched binary fails closed. Any later filing must receive a separate manifest entry; it must not silently replace these dated texts.
