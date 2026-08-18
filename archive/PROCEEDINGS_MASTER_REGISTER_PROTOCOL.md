# PROCEEDINGS MASTER REGISTER PROTOCOL

**Status:** internal knowledge-management control  
**Created:** 16 August 2026  
**Updated:** 18 August 2026  
**Canonical table:** `archive/PROCEEDINGS_MASTER_REGISTER.csv`

## Purpose

`PROCEEDINGS_MASTER_REGISTER.csv` is the repository-wide management index for Project Sun Rock / Por Derecho proceedings, institutional files and materially useful reference records.

It is deliberately **not a public-facing “all cases” page**. The underlying repository may be public, and individual proceedings may be discussed on relevant website pages where justified, but the project does not automatically aggregate, advertise or surface this master register through site navigation, sitemaps, cards or a public case-map page.

The objective is operational: a fresh working thread should be able to identify the organ, reference, current custodian, relationship to other files, source status, latest known procedural state and unresolved reference gaps without reconstructing the inventory from conversational memory.

## Controlling correction overlays

A later source-control correction can temporarily control over a stale CSV row until the complete master CSV is safely rewritten. Such an overlay must identify the exact row/reference, the superseded proposition, the corrected proposition and the required downstream propagation.

**Current mandatory overlay:** for `GC-CRI-009 / DP 1956/2026`, read `archive/knowledge-project/DP1956_STATUS_REOPENING_CORRECTION_18AUG2026.md` before using the CSV row. The older CSV wording that a reform/subsidiary appeal was reported is superseded. The current controlled position is provisional dismissal recorded on 21 July 2026, with no filed reform/subsidiary appeal currently established in the controlled corpus. The public site must not expose privileged legal advice about litigation choices.

## Scope

The master register may contain:

- civil, mercantile, insolvency, criminal, contentious-administrative and appellate proceedings;
- Fiscalía diligencias, expedientes, referrals and governmental files;
- municipal, Cabildo, tourism, transparency and other administrative files;
- AEAT/tax, CNMV/regulatory, SNCA/public-funds, Intervención, Tesoro and public-aid files;
- CGPJ, LAJ/court-office, professional-regulator and ombudsman files;
- police/Guardia Civil registrations where no assigned case has yet been located;
- private Law 2/2023/compliance-channel files where operationally relevant;
- technical, registration or output references **only when explicitly marked as not themselves being a separate proceeding**;
- unresolved candidate references when preserving the lead is useful and the source limitation is made explicit.

## What a row means

A row does **not** mean that the project alleges wrongdoing, that an organ admitted the merits, or that every referenced item is a formal judicial proceeding.

Use `Is_Proceeding` as follows:

- `TRUE` — sufficient source support currently exists for a distinct proceeding/institutional file.
- `FALSE` — useful reference, registration, output, technical identifier or transmission family, but not a separate proceeding.
- `UNVERIFIED` — the corpus contains a plausible proceeding/file reference, but the primary source needed to establish its exact identity or status has not yet been recovered.

`Record_Type`, `Proceeding_Class` and `Source_Status` must be read together.

## Source discipline

Apply the repository source hierarchy:

1. signed primary documents;
2. court/institutional originals;
3. registered submissions and receipts;
4. direct correspondence;
5. registry/corporate records;
6. contemporaneous third-party material;
7. internal reconstructions;
8. ChatGPT-generated analysis.

Never convert:

- a `REGAGE` receipt into a separate investigation;
- a notification/output number into the underlying expediente unless the source says so;
- an internal “Control 21/22/24” label into an official proceeding;
- a filename or party-created heading into an official court reference without verification;
- a referral into admission or a merits decision;
- an appeal draft into a filed appeal without filing/receipt evidence;
- a provisional dismissal into a final merits determination or free dismissal;
- a legal possibility of reopening into a prediction that reopening will occur;
- an appeal into a separate merits universe where it is simply a child of the original file;
- common actors, the same hotel, or common documents into proof that legally distinct proceedings are one case.

## Deduplication and relationship rules

1. **One row per legally or institutionally distinct proceeding/file.**
2. Appeals, rolls, piezas separadas and incidents receive their own row where operationally useful and should carry `Parent_Master_ID`.
3. A single complaint routed through several organs is not multiplied into separate proceedings unless each organ assigns a distinct file.
4. Multiple registrations of the same corpus may be grouped in one `REGISTRATION_ONLY` row.
5. Supporting acts can be retained as `FALSE` rows if the reference is important for retrieval or routing.
6. Preserve historical IDs in `Legacy_ID`; do not silently renumber the specialist Canary Islands register.
7. If two references may identify the same file, mark the relationship/open gap rather than merging by guess.
8. If one secondary filename conflicts with a primary or repeated native reference, preserve the conflict in `Notes`/`Open_Reference_Gap`.
9. Current custodian is distinct from origin organ. Transfers, inhibitions and referrals should update both fields.
10. A current status is only as current as its primary source. `Last_Scan_Date` records the inventory scan, not necessarily a merits-event date.
11. When a correction overlay exists, it controls over the stale row until the row is physically rewritten and the overlay records completion.

## Public-treatment rule

Default:

`INTERNAL_KNOWLEDGE_REGISTER_NOT_AUTO_PUBLISHED`

This means:

- no automatic public aggregate page;
- no automatic navigation link;
- no automatic sitemap promotion;
- no publication merely because a row exists.

It does **not** mean the information is secret. A proceeding can be referenced on a relevant public page if normal evidence, fairness, privacy, legal-risk and editorial controls are satisfied.

Private compliance files may use:

`INTERNAL_ONLY_NOT_SITE_AGGREGATED`

## Current baseline

The 16 August 2026 master refresh reconciles the existing Canary Islands cross-island register with additional repository/site, Gmail, Google Drive and File Library findings. It preserves the existing Lanzarote, Gran Canaria and Tenerife IDs while adding national, Madrid, Valencia, regulatory, tax, professional, public-funds and newly recovered historical references.

On 18 August 2026, a controlled status correction was added for `GC-CRI-009 / DP 1956/2026`: the older “reform/subsidiary appeal reported” wording must not be reused. See the mandatory overlay above.

Known gaps remain gaps. In particular, candidate references such as historical accumulated proceedings, incomplete appellate rolls, destination Fiscalía references and some output/registration numbers are not upgraded to verified proceedings merely to make the table look complete.

## Maintenance workflow

For a normal refresh:

1. Read `CHATGPT_START_HERE.md`, this protocol, the master CSV, `CORRECTION_REGISTER.md` and `MISSING_EVIDENCE_REGISTER.md`.
2. Read any controlling correction overlay for the affected row before reusing the CSV text.
3. Read the specialist register/ledger for the affected track.
4. Inspect current `main` and current website source/data for new or changed references.
5. Search Gmail for exact proceeding numbers, NIGs, organ names, notification subjects and attached native filenames.
6. Search Google Drive for the same references and for primary institutional originals.
7. Search File Library for older uploads, source bundles and documents that may pre-date the current repository.
8. Prefer opening the native court/institutional document before changing `Source_Status`, `Status`, `Current_Custodian` or `Is_Proceeding`.
9. Search for evidence that contradicts, narrows or supersedes the current row as well as evidence that supports it.
10. Deduplicate and link parent/child files rather than creating parallel descriptions of the same proceeding.
11. Update the CSV and propagate:
   - material factual corrections → `archive/CORRECTION_REGISTER.md` or a controlling correction overlay where safe full-file rewriting is not available;
   - unresolved primary-source needs → `archive/MISSING_EVIDENCE_REGISTER.md`;
   - specialist judicial/Fiscalía/admin ledgers where applicable;
   - public ES/EN pages only if a publication change is independently justified.
12. Use branch → diff/review → PR → merge for substantive repository changes.
13. Do **not** create or promote a public aggregate proceedings page unless the user expressly asks for one.
14. Apply the universal thread-deletion continuity gate before finishing.

## Reusable maintenance prompt

> **Run the Por Derecho proceedings-maintenance scan.** Start from current `main`, `archive/PROCEEDINGS_MASTER_REGISTER_PROTOCOL.md` and `archive/PROCEEDINGS_MASTER_REGISTER.csv`, then apply any controlling correction overlays identified by the protocol. Scan the current public-site source/data, Gmail, Google Drive and File Library for any court, Fiscalía, government, regulator, professional-body, ombudsman, police, tax, transparency, public-funds or compliance proceeding/file/reference that is new or has changed. Verify against primary institutional originals where possible. Treat REGAGE receipts, notifications, output numbers, internal “Control” labels, draft appeals and technical references as supporting references unless evidence shows an assigned/filed proceeding. Deduplicate by organ + legal file + reference, preserve parent/child appeal and incident relationships, and never merge distinct proceedings merely because they concern Sun Park or the same actors. Update the master register’s reference, NIG, source status, latest known state, current custodian, linked proceedings and reference gaps. Propagate material corrections to `CORRECTION_REGISTER.md` and primary-source gaps to `MISSING_EVIDENCE_REGISTER.md`. Do not create, link or promote a public aggregate proceedings page unless explicitly requested. Use a branch and PR for repository changes and finish by confirming deletion-safety.

## Suggested recurring review

A periodic scan is useful because new notifications can change status without changing the core theory. A **weekly** review is a sensible default for general maintenance; high-velocity periods can be checked more often, but the register should not be updated from unverified alerts alone.

## Continuity rule

This master is an index, not a substitute for the underlying evidence. Future threads must re-query Gmail, Drive, File Library and the controlling institutional originals where primary evidence is needed.

The master is deletion-safe only when material new references, corrections, relationship decisions and open source gaps have been incorporated here or in the linked canonical registers.
