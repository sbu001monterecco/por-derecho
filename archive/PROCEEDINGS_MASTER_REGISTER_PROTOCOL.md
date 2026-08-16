# PROCEEDINGS MASTER REGISTER PROTOCOL

**Status:** internal knowledge-management control  
**Created:** 16 August 2026  
**Canonical table:** `archive/PROCEEDINGS_MASTER_REGISTER.csv`

## Purpose

`PROCEEDINGS_MASTER_REGISTER.csv` is the repository-wide management index for Project Sun Rock / Por Derecho proceedings, institutional files and materially useful reference records.

It is deliberately **not a public-facing “all cases” page**. The underlying repository may be public, and individual proceedings may be discussed on relevant website pages where justified, but the project does not automatically aggregate, advertise or surface this master register through site navigation, sitemaps, cards or a public case-map page.

The objective is operational: a fresh working thread should be able to identify the organ, reference, current custodian, relationship to other files, source status, latest known procedural state and unresolved reference gaps without reconstructing the inventory from conversational memory.

For Matkator / DP 552/2025 → DP 711/2025 / ETJ 163/2020 / fincas 8584–8588–8497–8498 and the linked 2018/2020/2021 access/conservation record, the specialist controls are:

- `archive/MATKATOR_DP552_ETJ163_MASA_ACTIVA_SOURCE_DIGEST_16AUG2026.md`;
- `archive/MATKATOR_DP552_DP711_PROCEDURAL_CONTINUITY_ADDENDUM_16AUG2026.md`; and
- `archive/MATKATOR_TEN_SOURCE_WORKSPACE_FINGERPRINTS_16AUG2026.md` where binary/version identity matters.

These controls must be read before changing the relevant master rows. They control the two expansion-PDF versions, the DP 552→DP 711 relationship, the decided/not-decided boundary of the signed Autos, the three-plane LPB/Matkator/Aweswell separation and the current primary-source gaps.

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
- a complaint, expansion, party legal characterisation or damages calculation into a judicial finding;
- a draft/pre-file version into a separate filed pleading without a receipt;
- a referral into admission or a merits decision;
- an appeal into a separate merits universe where it is simply a child of the original file;
- common actors, the same hotel, or common documents into proof that legally distinct proceedings are one case.

A signed order proves its operative act and stated reasoning. It does not prove every allegation it summarises. A procedural/timing/utility ruling is not automatically a merits determination of the underlying property, damage, access or responsibility issue.

## Deduplication and relationship rules

1. **One row per legally or institutionally distinct proceeding/file.**
2. Appeals, rolls, piezas separadas and incidents receive their own row where operationally useful and should carry `Parent_Master_ID`.
3. A single complaint routed through several organs is not multiplied into unrelated proceedings; when different courts assign distinct references, preserve the origin/destination parent-child chain.
4. Multiple registrations of the same corpus may be grouped in one `REGISTRATION_ONLY` row.
5. Supporting acts can be retained as `FALSE` rows if the reference is important for retrieval or routing.
6. Preserve historical IDs in `Legacy_ID`; do not silently renumber the specialist Canary Islands register.
7. If two references may identify the same file, mark the relationship/open gap rather than merging by guess.
8. If one secondary filename conflicts with a primary or repeated native reference, preserve the conflict in `Notes`/`Open_Reference_Gap`.
9. Current custodian is distinct from origin organ. Transfers, inhibitions and referrals should update both fields.
10. A current status is only as current as its primary source. `Last_Scan_Date` records the inventory scan, not necessarily a merits-event date.
11. Different versions of substantially the same pleading remain one procedural sequence unless filing evidence proves separate presentations. Preserve version history in the specialist digest/fingerprint schedule.
12. A transmission-family row records document movement; it does not merge the originating and receiving proceedings.

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

The Matkator refresh records:

- **TF-CRI-006 / DP 552/2025** as the verified Tenerife origin;
- **LZ-JUD-031 / DP 711/2025** as the verified Lanzarote destination/continuity child after inhibition;
- the later procedural evidence for provisional dismissal, reform denial and appeal filing, while leaving the signed acts and AP outcome open;
- **TF-CIV-002 / ETJ 163/2020** and the 13-Mar-2025 transmission/new-fact filing; and
- the linked cross-proceeding transmission family and evidence gaps.

Known gaps remain gaps. Candidate references, incomplete appellate rolls, destination Fiscalía references and some output/registration numbers are not upgraded merely to make the table look complete.

## Maintenance workflow

For a normal refresh:

1. Read `CHATGPT_START_HERE.md`, this protocol, the master CSV, `CORRECTION_REGISTER.md` and `MISSING_EVIDENCE_REGISTER.md`.
2. Read the specialist register/ledger for the affected track. For Matkator/DP552/DP711/ETJ163, read the three canonical controls listed above before relying on the CSV summary.
3. Inspect current `main` and current website source/data for new or changed references.
4. Search Gmail for exact proceeding numbers, NIGs, organ names, notification subjects and attached native filenames.
5. Search Google Drive for the same references and for primary institutional originals.
6. Search File Library for older uploads, source bundles and documents that may pre-date the current repository.
7. Prefer opening the native court/institutional document before changing `Source_Status`, `Status`, `Current_Custodian` or `Is_Proceeding`.
8. Search for evidence that contradicts, narrows or supersedes the current row as well as evidence that supports it.
9. Deduplicate and link parent/child files rather than creating parallel descriptions of the same proceeding.
10. Update the CSV and propagate:
   - material factual corrections → `archive/CORRECTION_REGISTER.md`;
   - unresolved primary-source needs → `archive/MISSING_EVIDENCE_REGISTER.md`;
   - specialist judicial/Fiscalía/admin ledgers where applicable;
   - public ES/EN pages only if a publication change is independently justified.
11. Use branch → diff/review → PR → merge for substantive repository changes.
12. Do **not** create or promote a public aggregate proceedings page unless the user expressly asks for one.
13. Apply the universal thread-deletion continuity gate before finishing.

## Reusable maintenance prompt

> **Run the Por Derecho proceedings-maintenance scan.** Start from current `main`, `archive/PROCEEDINGS_MASTER_REGISTER_PROTOCOL.md` and `archive/PROCEEDINGS_MASTER_REGISTER.csv`. Then scan the current public-site source/data, Gmail, Google Drive and File Library for any court, Fiscalía, government, regulator, professional-body, ombudsman, police, tax, transparency, public-funds or compliance proceeding/file/reference that is new or has changed. Verify against primary institutional originals where possible. Treat REGAGE receipts, notifications, output numbers, internal “Control” labels and technical references as supporting references unless evidence shows an assigned proceeding. Deduplicate by organ + legal file + reference, preserve parent/child appeal and incident relationships, and never merge distinct proceedings merely because they concern Sun Park or the same actors. Where Matkator/DP552/DP711/ETJ163 is involved, first apply the canonical source digest, procedural-continuity addendum and fingerprint schedule, including their version controls and decided/not-decided limits. Update the master register’s reference, NIG, source status, latest known state, current custodian, linked proceedings and reference gaps. Propagate material corrections to `CORRECTION_REGISTER.md` and primary-source gaps to `MISSING_EVIDENCE_REGISTER.md`. Do not create, link or promote a public aggregate proceedings page unless explicitly requested. Use a branch and PR for repository changes and finish by confirming deletion-safety.

## Suggested recurring review

A periodic scan is useful because new notifications can change status without changing the core theory. A **weekly** review is a sensible default for general maintenance; high-velocity periods can be checked more often, but the register should not be updated from unverified alerts alone.

## Continuity rule

This master is an index, not a substitute for the underlying evidence. Future threads must re-query Gmail, Drive, File Library and the controlling institutional originals where primary evidence is needed.

The master is deletion-safe only when material new references, corrections, relationship decisions and open source gaps have been incorporated here or in the linked canonical registers.