# Thread continuity & preservation audit — Ministerio Fiscal canonical register — 19 September 2026

## Verdict

**Thread/workspace continuity is preserved in GitHub for all analysis, register architecture, pages, controls and repository mutations created in this thread.**

**Binary-source completeness is NOT yet 100%.** Four historical Gmail-source PDFs located during this thread were not previously present as repository binaries. They have now been re-read/materialised and SHA-256 locked during this audit, but remain outside GitHub binary custody pending a compatible binary-upload path. Their identities, provenance state, size and hashes are preserved below and in the companion manifest.

This audit therefore distinguishes:

- **PRESERVED_IN_GITHUB** — repository source/data/page/control actually present on `main`;
- **PRESERVED_BY_REFERENCE** — source represented by a controlled repository record but native binary is elsewhere;
- **MATERIALISED_HASH_LOCKED_NOT_YET_GITHUB_BINARY** — original bytes were recovered in this audit and hashed, but the binary itself is not committed to GitHub;
- **EXTERNAL_OFFICIAL_SOURCE** — current institutional/BOE source cited by URL, not copied as a repository binary.

## 1. Thread-created GitHub state

The principal implementation from this thread was merged through **PR #1638**:

- merge commit: `d22c71b0136aca91009a5eb59c6a1af46ea7f99d`
- canonical cross-register: `assets/data/ministerio-fiscal-canonical-register-20260919.json`
- Spanish register page: `es/ministerio-fiscal/registro-canonico/index.html`
- English register page: `en/public-prosecution-service/canonical-register/index.html`
- GitLab restoration queue: `archive/MINISTERIO_FISCAL_GITLAB_RESTORE_MIRROR_QUEUE_19SEP2026.md`
- validator: `scripts/validate_ministerio_fiscal_canonical_register_20260919.py`
- deployment probe: `deployment-probes/ministerio-fiscal-canonical-register-20260919.json`
- Spanish hub integration: `es/ministerio-fiscal/index.html`
- English hub integration: `en/public-prosecution-service/index.html`
- Spanish office-coverage update: `es/ministerio-fiscal-cobertura-oficinas/index.html`
- English office-coverage update: `en/public-prosecution-office-coverage/index.html`

Post-merge verification confirmed the register on `main` with:

- 15 offices;
- 16 institutional/specialist entities;
- 19 named Fiscalía people/officeholders;
- 19 file/proceeding references;
- 15 events;
- 26 evidence/source objects.

## 2. Existing repository sources used and preserved

The thread relied on, and did not overwrite or duplicate, existing source-controlled repository material including:

- `assets/data/ministerio-fiscal-directory-v1.json`
- `assets/data/ministerio-fiscal-office-digitisation-20260919.json`
- `archive/MINISTERIO_FISCAL_CANONICAL_HUB_DIRECTORY_CONTROL_02SEP2026.md`
- `evidence/fiscalia/2026/EG58_08SEP2026_JOINER_CONTROL.md`
- `archive/CALIFICACION_FISCALIA_SOURCE_GAP_CLOSURE_ADDENDUM_16AUG2026.md`
- `archive/CALIFICACION_AC_REPORT_RADICAL_TRANSPARENCY_LEDGER_16AUG2026.md`
- `archive/public_office_communications/fiscalia_tenerife/2026-01-30_DIP20/2026-01-27_30__FISCALIA_TENERIFE__DIP20_2026__CONTROLLED_RECORD_ES_EN.md`
- `archive/evidence/mf-redsara-anexo4/MF_REDSARA_ANEXO4_CANONICAL_INGEST_16AUG2026.md`
- E.G. 745/2026 controlled source/digitisation material already under `evidence/fiscalia/2026/` and the dedicated public rooms.

These remain authoritative at their own evidence ceilings.

## 3. Historical Gmail binaries discovered in this thread

The following originals were located from the Patricia Gmail account during the Fiscalía chronology scan.

| Audit ID | Original filename | Historical context | Size | SHA-256 | GitHub binary state |
|---|---|---|---:|---|---|
| MF-THR-BIN-001 | `DenPenFISCALIA 2014 Desahucio DOCUMENTO.pdf` | 2014 Fiscalía complaint preserved in 11-Jun-2016 email | 214,283 | `d90871143be51cf4865091380719dbdee679a7e14a3a743537c35f4140f5ea1c` | MATERIALISED_HASH_LOCKED_NOT_YET_GITHUB_BINARY |
| MF-THR-BIN-002 | `ampliacionfiscalialaspalmas.pdf` | 14-Jan-2019 ampliación Fiscalía | 399,533 | `7e0ac2d60725660e18b76f939771659cb2f66402c6ade5148f4feadd9144a64f` | MATERIALISED_HASH_LOCKED_NOT_YET_GITHUB_BINARY |
| MF-THR-BIN-003 | `BORJAFISCALIAOK.pdf` | complaint package concerning insolvency administrator, forwarded 26-Dec-2018 | 352,646 | `6d1da3c44a3de3d54f399ef742412a1d96d6b9e2d7b1a14d503824d633897d98` | MATERIALISED_HASH_LOCKED_NOT_YET_GITHUB_BINARY |
| MF-THR-BIN-004 | `Personacion Raymond..pdf` | September 2016 Fiscalía personación/declaration route | 35,083 | `213df7df20343f48368f1ce9ae87f103c857f1bd35206f827c4c0376b2fb908e` | MATERIALISED_HASH_LOCKED_NOT_YET_GITHUB_BINARY |

### Important preservation boundary

The public repository already records these source families at a descriptive/provenance level. That is **not equivalent to native binary preservation**. Until the four hashes above correspond to actual GitHub blobs/paths, the correct completeness statement is: **thread continuity complete; historical binary preservation partial**.

The working copies materialised during this audit are temporary execution-environment copies and must not be treated as durable repository custody.

## 4. Current official-source layer

The thread also used current official web/BOE sources to verify current officeholders and specialist structures. Those are represented as external-source URLs in the canonical register. They were not copied into GitHub as website snapshots, and they do not need to be represented as user-owned evidential binaries.

Key external sources include the official Ministerio Fiscal directories/pages for FGE, Las Palmas, Tenerife, Canarias, Delitos Económicos and Anticorrupción, plus BOE appointment decisions concerning specialist delegations.

## 5. Private-source privacy controls

No Gmail message ID, Gmail thread ID, provider-local URL or private attachment download token is published in the canonical public register.

The register exposes only:

- source class;
- documentary label;
- date/context where safe;
- proof function;
- public-safe repository path where one exists;
- hash/provenance controls where needed.

This remains the required policy when the four outstanding binaries are eventually placed into repository custody: native/private evidence should live in a non-public evidence path or a repository with appropriate access control, while the public pages use redacted/controlled derivatives.

## 6. GitLab continuity

The GitLab restoration queue is present in GitHub and expressly forbids blind overwrite:

`archive/MINISTERIO_FISCAL_GITLAB_RESTORE_MIRROR_QUEUE_19SEP2026.md`

When GitLab access returns:

1. fetch current GitLab `main`;
2. compare against then-current GitHub `main`;
3. preserve newer GitLab work;
4. port only the source-controlled net delta;
5. include this continuity audit and the binary-preservation manifest;
6. run GitLab validators/pipeline;
7. verify the bilingual Ministerio Fiscal routes;
8. record GitLab commit/MR/pipeline IDs.

## 7. Deletion / retirement decision

**This ChatGPT thread is NOT yet deletion-safe if the objective is to have every recovered historical native file itself stored in GitHub.**

It **is continuity-safe for the intellectual/work-product layer** because the analysis, canonical identity architecture, register, pages, source references, hashes, open gaps and GitLab restoration instructions are now repository-controlled.

Deletion-safe status becomes **YES** only when either:

- the four materialised Gmail binaries are committed to an appropriate durable repository evidence location and their SHA-256 values match this audit; or
- a separately documented durable private-evidence store is designated as canonical custody for those exact hashes and GitHub intentionally remains metadata-only.

## 8. No-regression instructions

Future work must not:

- claim all historical Gmail originals are in GitHub while MF-THR-BIN-001 through -004 lack repository blob paths;
- renumber existing `PD-MF-OFF-####`, Master IDs or existing CAEPR `PD-SP-P-####` identities;
- convert E.G. 19/2026 or E.G. 58/2026 into invented Master IDs before reconciliation;
- infer personal handling from office leadership;
- convert registration/remittal into merits review;
- expose private provider locators in public data;
- overwrite a restored GitLab `main` without reconciliation.

## 9. Audit conclusion

**Repository continuity: PASS.**

**Thread-created work-product preservation on GitHub: PASS.**

**All referenced native historical source files on GitHub: FAIL / OPEN — four specifically identified PDF binaries remain to be committed or assigned to a separately controlled durable private-evidence store.**

This is a bounded failure with exact filenames, sizes and SHA-256 values preserved, not an unknown gap.
