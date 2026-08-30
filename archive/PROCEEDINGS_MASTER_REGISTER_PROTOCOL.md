# PROCEEDINGS MASTER REGISTER PROTOCOL

**Status:** repository-wide knowledge-management + controlled-publication control  
**Created:** 16 August 2026  
**Updated:** 30 August 2026  
**Canonical table:** `archive/PROCEEDINGS_MASTER_REGISTER.csv`  
**Public publication governance:** `archive/MASTER_PROCEEDINGS_PUBLICATION_GOVERNANCE_30AUG2026.md`

## Purpose

`PROCEEDINGS_MASTER_REGISTER.csv` is the repository-wide management index for Project Sun Rock / Por Derecho proceedings, institutional files and materially useful reference records.

The canonical CSV remains the operational master. A bilingual **controlled public projection** is now mandatory at:

- `/en/master-proceedings-register/`; and
- `/es/registro-maestro-procedimientos/`.

The public projection is a procedural navigation layer in support of the multitrack storyline/timeline, the project's stated position and truth-seeking objectives. It must expose documented intersections, routing, source status and open gaps without collapsing legally distinct proceedings into one case or turning an index entry into a merits finding.

The operational objective remains that a fresh working thread can identify the organ, reference, current custodian, relationship to other files, source status, latest known procedural state and unresolved reference gaps without reconstructing the inventory from conversational memory.

<!-- MASTER_PROCEEDINGS_PUBLICATION_GATE -->
## Controlled public-publication gate — mandatory

Read `archive/MASTER_PROCEEDINGS_PUBLICATION_GOVERNANCE_30AUG2026.md` before changing publication treatment, public routes, field projection, sitewide interlinking or the meaning of inclusion in the public register.

The public pages read the canonical CSV and render a restricted public projection. They must not automatically render internal notes, private source anchors, privileged legal advice, personal contact details or rows explicitly classified as internal/private.

The historic value `INTERNAL_KNOWLEDGE_REGISTER_NOT_AUTO_PUBLISHED` is a legacy non-automatic-publication label and no longer blocks inclusion in the user-authorised aggregate public projection. `INTERNAL_ONLY_NOT_SITE_AGGREGATED` and other unambiguous internal/private treatments remain excluded unless separately reclassified through a source/privacy-aware review.

The public register must remain visibly interlinked with the recovery/story timeline and relevant proceeding-specific pages. Future threads must maintain two-way movement:

**storyline/timeline → procedural track → proceeding/file → underlying source**

and

**proceeding/file → appeal/referral/parent-child links → storyline/timeline context**.

Publication never upgrades evidence. `TRUE`, `FALSE` and `UNVERIFIED`, `Source_Status` and `Open_Reference_Gap` remain first-class public distinctions.

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

The following corrections are controlling unless later primary evidence requires a transparent, provenance-preserving correction:

- Juan Carlos Roque Prieto, Esteban Noriega and Álvaro Campanario are **not** project-side counsel; keep them external/opposing/dissident-side and attribute their actual client, proceeding and period from primary sources.
- The earlier user-supplied alias `Cristro Suarez Pimentel` resolves in current primary correspondence to **Cristo Ayose Suárez Pimentel**; preserve the alias as provenance while using the verified professional identity where appropriate.
- Juan Tomás Parrilla Suárez is an individual professional independent from Garrigues for registry purposes; do not fuse him with Garrigues absent a specific dated primary source proving the relevant historical relationship.
- **Javier Sixto Seijas** and **Estefanía Sixto Seijas** are linked as a working professional pair where supported, while their identities, signatures, filings, advice, procurador pairings and responsibilities remain individually attributable.

Every lawyer must have a dedicated chronological filing register. Every procurador/procuradora must be a separately searchable first-class record linked per party, proceeding and period. A lawyer-procurador pairing is never presumed permanent.

Do not leave absent representation data as silent blanks. Use an explicit verified status or create/update the counsel/procurador gap register. An empty filing array or incomplete procurador list is never evidence that no filing or procurador exists.

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
- technical, registration or output references **only when explicitly marked as not themselves being a separate proceeding**; and
- unresolved candidate references when preserving the lead is useful and the source limitation is made explicit.

## What a row means

A row does **not** mean that the project alleges wrongdoing, that an organ admitted the merits, or that every referenced item is a formal judicial proceeding.

Use `Is_Proceeding` as follows:

- `TRUE` — sufficient source support currently exists for a distinct proceeding/institutional file.
- `FALSE` — useful reference, registration, output, technical identifier or transmission family, but not a separate proceeding.
- `UNVERIFIED` — the corpus contains a plausible proceeding/file reference, but the primary source needed to establish its exact identity or status has not yet been recovered.

`Record_Type`, `Proceeding_Class` and `Source_Status` must be read together. The public register must display these distinctions prominently enough that aggregation cannot be mistaken for adjudication or admission.

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
- an appeal into a separate merits universe where it is simply a child of the original file; or
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
12. Public aggregation does not alter parent/child boundaries, jurisdictional boundaries or evidential status.

## Public-treatment rule

The controlled public register is now a permanent publication surface.

Legacy default:

`INTERNAL_KNOWLEDGE_REGISTER_NOT_AUTO_PUBLISHED`

means that the row was historically not auto-promoted. Following the express 30-Aug-2026 instruction, that legacy value is eligible for inclusion in the controlled public projection, subject to field-level safety and evidence controls.

Explicit private/internal treatment remains excluded, including:

`INTERNAL_ONLY_NOT_SITE_AGGREGATED`

and any equivalent unambiguous private/internal-only label.

The public projection should ordinarily expose procedural identity, track, organ/custodian, reference, period, object, status, relationship, source status and open gap. It should not automatically expose internal notes, privileged advice, private source anchors, personal contact information or strategy.

## Current baseline

The 16 August 2026 master refresh reconciles the existing Canary Islands cross-island register with additional repository/site, Gmail, Google Drive and File Library findings. It preserves the existing Lanzarote, Gran Canaria and Tenerife IDs while adding national, Madrid, Valencia, regulatory, tax, professional, public-funds and newly recovered historical references.

On 18 August 2026, a controlled status correction was added for `GC-CRI-009 / DP 1956/2026`: the older “reform/subsidiary appeal reported” wording must not be reused. See the mandatory overlay above.

On 30 August 2026, the counsel/procurador filing-lineage gate was made mandatory for all future proceedings maintenance. The professional and procurador registers remain explicitly incomplete until primary-source reconciliation establishes the full denominator.

Also on 30 August 2026, the Master Proceedings Register became a **controlled bilingual public procedural spine**. Its public pages are interlinked into the sitewide navigation and the recovery timeline through `assets/master-proceedings-publication-20260830.js`; the canonical CSV remains the source of truth and explicitly internal/private rows remain outside the public projection.

Known gaps remain gaps. Candidate references such as historical accumulated proceedings, incomplete appellate rolls, destination Fiscalía references and some output/registration numbers are not upgraded to verified proceedings merely to make the table or public page look complete.

## Maintenance workflow

For a normal refresh:

1. Read `CHATGPT_START_HERE.md`, this protocol, `archive/MASTER_PROCEEDINGS_PUBLICATION_GOVERNANCE_30AUG2026.md`, the master CSV, `CORRECTION_REGISTER.md` and `MISSING_EVIDENCE_REGISTER.md`.
2. Read `archive/COUNSEL_PROCURADOR_FILING_LINEAGE_GOVERNANCE_30AUG2026.md` and the four linked counsel/procurador data registers before attributing any lawyer, procurador, filing or professional relationship.
3. Read any controlling correction overlay for the affected row before reusing the CSV text.
4. Read the specialist register/ledger for the affected track.
5. Inspect current `main`, the public register routes and current website source/data for new or changed references.
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
   - public treatment classification where a row must be withheld or newly released; and
   - timeline/storyline context where a material procedural relationship changes the public narrative.
13. Reverse-engineer each material judicial/LAJ decision back to its input filing(s), professional attribution and authority/personación where the sources permit; link any appeal/follow-up and master timeline event.
14. Confirm that the public projection automatically reflects public-eligible CSV changes without exposing excluded internal/private rows or private fields.
15. Run `python scripts/audit_counsel_procurador_governance.py` and `python scripts/audit_master_proceedings_publication.py` before describing continuity as reconciled.
16. Use branch → diff/review → PR → merge for substantive repository changes.
17. Maintain the bilingual public aggregate register and its sitewide timeline/navigation interlinks; do not silently remove or de-promote them.
18. Apply the universal thread-deletion continuity gate before finishing.

## Reusable maintenance prompt

> **Run the Por Derecho proceedings-maintenance scan.** Start from current `main`, `archive/PROCEEDINGS_MASTER_REGISTER_PROTOCOL.md`, `archive/MASTER_PROCEEDINGS_PUBLICATION_GOVERNANCE_30AUG2026.md` and `archive/PROCEEDINGS_MASTER_REGISTER.csv`, then apply any controlling correction overlays identified by the protocol. Apply the mandatory counsel/procurador filing-lineage governance and update the dedicated professional filing, procurador and gap registers. Scan the current public-site source/data, Gmail, Google Drive and File Library for any court, Fiscalía, government, regulator, professional-body, ombudsman, police, tax, transparency, public-funds or compliance proceeding/file/reference that is new or has changed. Verify against primary institutional originals where possible. Treat REGAGE receipts, notifications, output numbers, internal “Control” labels, draft appeals and technical references as supporting references unless evidence shows an assigned/filed proceeding. Deduplicate by organ + legal file + reference, preserve parent/child appeal and incident relationships, and never merge distinct proceedings merely because they concern Sun Park or the same actors. For every material act establish or gap-log PARTY → LAWYER → SIDE/PERIMETER → PROCURADOR/A → AUTHORITY/PERSONACIÓN → PROCEEDING/PIEZA → FILING → COURT/LAJ RESPONSE → APPEAL/FOLLOW-UP → TIMELINE. Update the master register’s reference, NIG, source status, latest known state, current custodian, linked proceedings and reference gaps. Preserve explicit private/internal rows outside the public aggregate; otherwise maintain the bilingual public register as the procedural spine and propagate material relationship changes into the multitrack storyline/timeline. Propagate material corrections to `CORRECTION_REGISTER.md` and primary-source gaps to `MISSING_EVIDENCE_REGISTER.md`. Use a branch and PR for repository changes, run both proceedings/publication and counsel/procurador audits, and finish by confirming publication and deletion-safety.

## Suggested recurring review

A periodic scan is useful because new notifications can change status without changing the core theory. A **weekly** review is a sensible default for general maintenance; high-velocity periods can be checked more often, but the register should not be updated from unverified alerts alone.

## Continuity rule

This master is an index, not a substitute for the underlying evidence. Future threads must re-query Gmail, Drive, File Library and the controlling institutional originals where primary evidence is needed.

The bilingual public register is now part of this protocol's mandatory continuity architecture. Future proceedings work must assess both the canonical CSV and its public projection, preserve explicit internal/private exclusions, maintain parent/child and appeal/referral relationships, and keep the page interlinked with the multitrack storyline/timeline.

The counsel/procurador filing-lineage gate remains part of the same mandatory architecture. Future proceedings work must not silently omit professional perimeter, procurador, authority/personación, filing-response or appeal/timeline lineage merely because those fields have not yet been populated.

The master is deletion-safe only when material new references, corrections, professional attribution decisions, relationship decisions, public-treatment decisions and open source gaps have been incorporated in the canonical controls and the public register continues to render from those controls without regression.
