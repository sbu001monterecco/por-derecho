# PROCEEDINGS MASTER REGISTER PROTOCOL

**Status:** internal knowledge-management control  
**Created:** 16 August 2026  
**Updated:** 30 August 2026  
**Canonical table:** `archive/PROCEEDINGS_MASTER_REGISTER.csv`

## Purpose

`PROCEEDINGS_MASTER_REGISTER.csv` is the repository-wide management index for Project Sun Rock / Por Derecho proceedings, institutional files and materially useful reference records.

It is deliberately **not a public-facing “all cases” page**. The underlying repository may be public, and individual proceedings may be discussed on relevant website pages where justified, but the project does not automatically aggregate, advertise or surface this master register through site navigation, sitemaps, cards or a public case-map page.

The objective is operational: a fresh working thread should be able to identify the organ, reference, current custodian, relationship to other files, source status, latest known procedural state and unresolved reference gaps without reconstructing the inventory from conversational memory.

<!-- COUNSEL_PROCURADOR_GOVERNANCE_GATE -->
## Counsel / procurador filing-lineage gate — mandatory

Every repository-wide or proceeding-specific judicial, tribunal, complaint, appeal, Fiscalía, regulatory or connected-proceedings refresh must also apply:

- `archive/COUNSEL_PROCURADOR_FILING_LINEAGE_GOVERNANCE_30AUG2026.md`;
- `assets/data/counsel-procurador-perimeter-register-v1.json`;
- `assets/data/counsel-filing-register-v1.json`;
- `assets/data/procurador-master-register-v1.json`; and
- `assets/data/counsel-procurador-gap-register-v1.json`.

For every relevant act, maintain the source-led chain:

**PARTY → LAWYER → SIDE/PERIMETER → PROCURADOR/A → AUTHORITY/PERSONACIÓN → PROCEEDING → PIEZA/INCIDENTE → FILING → COURT/LAJ RESPONSE → RESULT → APPEAL/FOLLOW-UP → TIMELINE.**

This is not optional metadata. It is part of the evidential and procedural chronology. Keep the project's current/former counsel register separate from the external/opposing/dissident-side professional register. Appearance in the same proceeding never transfers a professional into the project-side perimeter.

The following seed corrections are controlling unless later primary evidence requires a transparent, provenance-preserving correction:

- Juan Carlos Roque Prieto, Esteban Noriega and Álvaro Campanario are **not** project-side counsel; keep them external/opposing/dissident-side and attribute their actual client, proceeding and period from primary sources.
- Cristro Suarez Pimentel is seeded in the project-side **former counsel** register; preserve the user-supplied spelling until primary-source verification establishes the canonical professional identity.
- Juan Tomás Parrilla Suárez is an individual professional independent from Garrigues for registry purposes; do not fuse him with Garrigues absent a specific dated primary source proving the relevant historical relationship.
- Javier and Estefanía are linked as a working professional pair where supported, while their identities, signatures, filings, advice, procurador pairings and responsibilities remain individually attributable.

Every lawyer must have a dedicated chronological filing register. Every procurador/procuradora must be a separately searchable first-class record linked per party, proceeding and period. A lawyer-procurador pairing is never presumed permanent.

Do not leave absent representation data as silent blanks. Use an explicit verified status or create/update the counsel/procurador gap register. An empty filing array or a current procurador count of zero is never evidence that no filing or procurador exists.

A proceeding or professional-lineage refresh may not be described as **complete**, **fully reconciled** or **denominator-complete** until the lawyer, side/perimeter, client/party, procurador status, authority/personación, filing, court/LAJ response, appeal/follow-up and timeline linkage have each been populated or explicitly carried as an evidenced gap.

The CI control `scripts/audit_counsel_procurador_governance.py` is the deletion/drift gate for these invariants. Do not bypass it by silently renaming, merging or removing the controlled professional records.

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

On 30 August 2026, the counsel/procurador filing-lineage gate was made mandatory for all future proceedings maintenance. The professional and procurador registers remain explicitly incomplete until primary-source reconciliation establishes the full denominator.

Known gaps remain gaps. In particular, candidate references such as historical accumulated proceedings, incomplete appellate rolls, destination Fiscalía references and some output/registration numbers are not upgraded to verified proceedings merely to make the table look complete.

## Maintenance workflow

For a normal refresh:

1. Read `CHATGPT_START_HERE.md`, this protocol, the master CSV, `CORRECTION_REGISTER.md` and `MISSING_EVIDENCE_REGISTER.md`.
2. Read `archive/COUNSEL_PROCURADOR_FILING_LINEAGE_GOVERNANCE_30AUG2026.md` and the four linked counsel/procurador data registers before attributing any lawyer, procurador, filing or professional relationship.
3. Read any controlling correction overlay for the affected row before reusing the CSV text.
4. Read the specialist register/ledger for the affected track.
5. Inspect current `main` and current website source/data for new or changed references.
6. Search Gmail for exact proceeding numbers, NIGs, organ names, notification subjects and attached native filenames, including counsel/procurador names and filing receipts where relevant.
7. Search Google Drive for the same references and for primary institutional originals.
8. Search File Library for older uploads, source bundles and documents that may pre-date the current repository.
9. Prefer opening the native court/institutional document before changing `Source_Status`, `Status`, `Current_Custodian`, `Is_Proceeding` or professional attribution.
10. Search for evidence that contradicts, narrows or supersedes the current row as well as evidence that supports it.
11. Deduplicate and link parent/child files rather than creating parallel descriptions of the same proceeding.
12. Update the CSV and propagate:
   - material factual corrections → `archive/CORRECTION_REGISTER.md` or a controlling correction overlay where safe full-file rewriting is not available;
   - unresolved primary-source needs → `archive/MISSING_EVIDENCE_REGISTER.md`;
   - counsel/procurador attribution and unresolved lineage → the dedicated counsel/procurador registers and gap register;
   - specialist judicial/Fiscalía/admin ledgers where applicable;
   - public ES/EN pages only if a publication change is independently justified.
13. Reverse-engineer each material judicial/LAJ decision back to its input filing(s), professional attribution and authority/personación where the sources permit; link any appeal/follow-up and master timeline event.
14. Run `python scripts/audit_counsel_procurador_governance.py` before describing counsel/procurador continuity as reconciled.
15. Use branch → diff/review → PR → merge for substantive repository changes.
16. Do **not** create or promote a public aggregate proceedings page unless the user expressly asks for one.
17. Apply the universal thread-deletion continuity gate before finishing.

## Reusable maintenance prompt

> **Run the Por Derecho proceedings-maintenance scan.** Start from current `main`, `archive/PROCEEDINGS_MASTER_REGISTER_PROTOCOL.md` and `archive/PROCEEDINGS_MASTER_REGISTER.csv`, then apply any controlling correction overlays identified by the protocol. Apply the mandatory counsel/procurador filing-lineage governance and update the dedicated professional filing, procurador and gap registers. Scan the current public-site source/data, Gmail, Google Drive and File Library for any court, Fiscalía, government, regulator, professional-body, ombudsman, police, tax, transparency, public-funds or compliance proceeding/file/reference that is new or has changed. Verify against primary institutional originals where possible. Treat REGAGE receipts, notifications, output numbers, internal “Control” labels, draft appeals and technical references as supporting references unless evidence shows an assigned/filed proceeding. Deduplicate by organ + legal file + reference, preserve parent/child appeal and incident relationships, and never merge distinct proceedings merely because they concern Sun Park or the same actors. For every material act establish or gap-log PARTY → LAWYER → SIDE/PERIMETER → PROCURADOR/A → AUTHORITY/PERSONACIÓN → PROCEEDING/PIEZA → FILING → COURT/LAJ RESPONSE → APPEAL/FOLLOW-UP → TIMELINE. Update the master register’s reference, NIG, source status, latest known state, current custodian, linked proceedings and reference gaps. Propagate material corrections to `CORRECTION_REGISTER.md` and primary-source gaps to `MISSING_EVIDENCE_REGISTER.md`. Do not create, link or promote a public aggregate proceedings page unless explicitly requested. Use a branch and PR for repository changes and finish by confirming deletion-safety.

## Suggested recurring review

A periodic scan is useful because new notifications can change status without changing the core theory. A **weekly** review is a sensible default for general maintenance; high-velocity periods can be checked more often, but the register should not be updated from unverified alerts alone.

## Continuity rule

This master is an index, not a substitute for the underlying evidence. Future threads must re-query Gmail, Drive, File Library and the controlling institutional originals where primary evidence is needed.

The counsel/procurador filing-lineage gate is part of this protocol's mandatory continuity architecture. Future proceedings work must not silently omit professional perimeter, procurador, authority/personación, filing-response or appeal/timeline lineage merely because those fields have not yet been populated.

The master is deletion-safe only when material new references, corrections, professional attribution decisions, relationship decisions and open source gaps have been incorporated here or in the linked canonical registers.
