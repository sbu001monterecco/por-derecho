# Tech Platform / evidence-intelligence thread — deletion audit

**Control date:** 25 August 2026  
**Current-main baseline at audit start:** `6c2fc6d4e68dbda37fad4c311ddd0a4b363796fe`  
**Current verdict:** `DELETION_SAFE_WITH_OPEN_TECH_PLATFORM_ITEMS`  
**Operational ledger:** [Issue #993](https://github.com/sbu001monterecco/por-derecho/issues/993)

## 1. Scope of this thread

This thread developed and tested a new way of thinking about the Por Derecho repository and website:

- GitHub as the auditable control plane rather than an indiscriminate private-evidence warehouse;
- private native-evidence custody separated from public Git;
- canonical identity, matter, proceeding, event and proposition objects;
- document-first, matter-bounded retrieval;
- exact/lexical plus selective semantic retrieval rather than vector-only search;
- support, contrary evidence, limitations, corrections and open gaps in every serious evidence packet;
- scale-specific architecture for approximately 10,000 documents, intermediate scale and multi-million-document scale;
- foreign-matter contamination controls;
- legal-adjacent technical limitations;
- a multidisciplinary benefits and SWOT review; and
- a controlled first implementation on RPL 2523/2025.

## 2. Foreign-matter exclusion

The generic architecture notes supplied from an unrelated private matter were used only as `TECHNICAL_REFERENCE` methodology.

No name, company, policy, fact pattern, event, allegation, chronology or example from that unrelated matter is required for Por Derecho continuity. The public repository contains only the generic source-class and contamination rules. Semantic similarity is not a bridge into Por Derecho.

The originating chat may therefore be deleted without losing a legitimate Por Derecho entity, fact or proposition from that external matter.

## 3. Durable implementation

PR [#990](https://github.com/sbu001monterecco/por-derecho/pull/990) merged as:

`d5e9fd8c65c30a841827dd0ee5487ddc3718bf37`

It preserved:

- `PD-SP-IDENTITY-REGISTRY-001` as the sole person/organisation/structure/institution/proceeding identity authority;
- the prohibition on a competing `PD-ENT-*` identity system;
- public source classes and foreign-matter firewall;
- public-safe document/citation/evaluation schemas;
- a four-document private RPL custody pilot;
- stable hashes, sizes, page counts, evidence states and limitations;
- seven known-answer retrieval tests;
- strict retrieval and identity/public-boundary validators; and
- immutable GitHub Action pins.

The post-merge retrieval workflow run `32868937072` completed successfully. The durable baseline records **26 controlled sections, 7 evaluations, 7 passes and 0 failures** in:

`.github/evidence-intelligence/pilots/rpl2523/baseline-result.json`

Finite-retention workflow artifacts are not the sole continuity record; the tests, parser and baseline summary remain in Git.

## 4. Private custody readback

On 25 August 2026 the private pilot folder was independently listed and contained:

- four native PDFs;
- `PD-SP-CUST-0001_RPL2523_private_custody_manifest.json`; and
- a separate manifest checksum.

All six objects reported `not_shared`. Their provider IDs and private URLs remain outside public Git.

This thread is not required to locate or interpret those private provider identifiers. The public custody summary and private manifest ID provide the durable separation.

## 5. Material limitations preserved

The repository preserves that:

- a hash proves byte identity, not truth, authorship, admissibility, certification or official-file inclusion;
- Gil Marer's principal LexNET appeal receipt remains unlocated;
- a later deposit filing is not promoted into that principal receipt;
- the two located 353,860-byte Pink/Patricia copies are identical to each other, but are not represented as byte-identical to the separately hashed signed LexNET principal;
- the four-document pilot is not the complete RPL file or complete Por Derecho corpus;
- the retrieval pass does not establish any legal merits outcome; and
- embeddings, vector infrastructure and automatic publication remain deferred.

## 6. Earlier prepared bootstrap artefacts

An earlier ZIP and patch were prepared in the chat before the current identity registry and later repository work were fully reconciled. The multidisciplinary review identified a competing identity concept, unwanted compiled/cache files and other matters requiring reconstruction.

Those prepared artefacts are **superseded and non-canonical**. They must not be applied after deletion of this thread. The implemented PR #990 and the current repository are authoritative.

## 7. Future development preserved outside chat

All material future-development conclusions are now assigned in:

- `.github/evidence-intelligence/TECH_PLATFORM_ROADMAP.md`;
- `.github/evidence-intelligence/TECH_PLATFORM_FUTURE_THREAD_PROMPT.md`;
- `.github/workflows/tech-platform-monitor.yml`; and
- Issue #993.

The roadmap preserves:

- the five-plane architecture;
- current, intermediate and multi-million scale gates;
- the private/public and identity invariants;
- citation, correction and contrary-evidence improvements;
- second-matter selection criteria;
- private document-registry and hybrid-retrieval stages;
- source-to-publication dependencies;
- claimant/right/recovery objects; and
- the instruction not to overengineer before a measured threshold.

## 8. Monitoring

The Tech Platform monitor runs:

- daily at `05:17 UTC`;
- on manual dispatch;
- on relevant pull requests; and
- on relevant pushes to `main`.

It re-runs:

- identity/public-boundary validation;
- the seven RPL retrieval evaluations; and
- platform-health checks for required files, ID authority, custody summary, private/public flags, immutable Action pins, cache-file contamination and custody-readback cadence.

GitHub cannot independently read the private Drive vault from this public workflow. Private readback therefore remains a separate controlled check, with a 30-day cadence recorded in the baseline and Issue #993.

## 9. Open items

Open work includes:

- periodic private-vault checksum/readback verification;
- improved citation anchors;
- a legacy-ID crosswalk;
- selection of a second bounded matter;
- a private document registry;
- measured exact/full-text retrieval before embeddings;
- dependency tracking; and
- claimant/right/recovery modelling.

These items are durably recorded in the roadmap and Issue #993. They are not reasons to retain this chat.

## 10. Final deletion-safety determination

No unique substantive architecture conclusion, identity rule, contamination boundary, custody result, retrieval baseline, material limitation, SWOT-derived development priority or monitoring instruction remains solely in this thread.

Deleting the thread does not authorise:

- deletion or demotion of the Tech Platform files;
- deletion or renaming of current immutable IDs;
- disclosure of private custody locators or native evidence;
- ingestion of any unrelated private matter;
- automatic expansion to another matter;
- automatic changes to legal conclusions; or
- automatic website publication.

This thread is therefore **safe to delete with open Tech Platform development items**, once the closeout package containing this audit and scheduled monitor is merged and its checks pass.
