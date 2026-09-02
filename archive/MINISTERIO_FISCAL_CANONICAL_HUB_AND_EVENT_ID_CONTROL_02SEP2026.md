# Ministerio Fiscal canonical hub, office hierarchy and event-ID control — 2 September 2026

**Control date:** 2 September 2026  
**Status:** IMPLEMENTED AS APPEND-ONLY CANONICAL SURFACE; HISTORICAL SOURCE COMPLETENESS REMAINS OPEN  
**Public routes:** `/es/ministerio-fiscal/` · `/en/public-prosecution-service/`

## 1. Purpose

The Ministerio Fiscal record is one institutional history rendered through separate canonical objects. It must not be reduced to one 2026 expediente and it must not collapse distinct offices, files, filings, responses or transports.

The hub therefore renders, from the existing canonical registers:

1. the generic Ministerio Fiscal identity;
2. the State/central offices and specialist units;
3. the Fiscalía de la Comunidad Autónoma de Canarias;
4. the provincial offices in Las Palmas and Santa Cruz de Tenerife;
5. the Fiscalía de Área de Arrecife de Lanzarote–Puerto del Rosario;
6. the European Public Prosecutor's Office and the source-verified IGAE support unit as a **separate supranational branch**, not as children of the Spanish Ministerio Fiscal; and
7. the exact prosecution-file and communication-event chains linked to those offices.

## 2. Canonical identifier doctrine

The external official identifier and the Por Derecho identifier are different fields and must both survive.

| Object | Canonical Por Derecho ID | External reference layer |
|---|---|---|
| institution / office | `PD-SP-I-####` | official name, DIR3 where controlled |
| prosecution expediente / file | `PD-SP-R-####` | DI, DIP, EG, ST, CC/CA, NIG or other Fiscalía reference |
| filing / response / decree / notice / acknowledgement / routing act | `PD-SP-EVT-####` | REGAGE/RedSARA/AGE receipt, official outgoing/incoming reference, date |
| source artifact | `PD-SP-SRC-*` where allocated | source filename, hash, signed-act metadata, custody locator where publishable |
| master proceedings identity | territorial `*-FIS-*` ID | cross-register identity only |

The caret (`^`) is identity-only. An office or exact expediente can be caret-confirmed. A document transport does not receive a synthetic caret identity merely because it was sent or registered.

## 3. Office hierarchy

The root identity remains `PD-SP-I-0002 — Ministerio Fiscal / Fiscalía`.

The hub groups already-canonical offices without merging them:

- State/central: `PD-SP-I-0029`, `PD-SP-I-0036`, `PD-SP-I-0034`, `PD-SP-I-0030`, `PD-SP-I-0031`, `PD-SP-I-0032`, `PD-SP-I-0033`.
- Autonomous-community: `PD-SP-I-0028`.
- Provincial: `PD-SP-I-0020`, `PD-SP-I-0027`.
- Area: `PD-SP-I-0026`.
- Separate supranational branch: `PD-SP-I-0045`, `PD-SP-I-0046`.

The hierarchy is a navigation relationship only. It does not transfer receipt, knowledge, examination, intent, responsibility or merits treatment between offices.

## 4. Fiscalía expediente identity closure

Before this package, the Fiscalía interconnectivity projection exposed **21 exact Fiscalía files + 3 unresolved references**, but three exact master-register files did not yet have a dedicated CAEPR `PD-SP-R` identity. This package closes that identity gap append-only:

- `GC-FIS-011 / DI 273/2013` → `PD-SP-R-0044`.
- `GC-FIS-012 / Fiscalía 39/2014` → `PD-SP-R-0045`, retained as `CARET_PENDING` because exact office/scope and primary file remain open.
- `GC-FIS-015 / EG 352/2025` → `PD-SP-R-0046`.

After this backfill, every one of the 24 Fiscalía-file/reference rows exposed by `assets/data/fiscalia-proceedings-interconnectivity-v1.json` resolves to one canonical `PD-SP-R` object. Identity completeness is not merits completeness: unresolved source states remain unresolved.

## 5. Response and event registration control

`assets/data/institutional-communications-register-v1.json` remains the append-only event source. The hub does not create a second communications register.

The controlled 31-August mailbox/REGAGE baseline states that every one of the fixed 231 private-manifest source rows already has a corresponding public-safe register row and that located acts, notices and receipts are separate linked rows. It separately records 156 mailbox events and the 75 detailed REGAGE receipt baseline.

The rule enforced here is:

> every located filing, response, decree, notice, acknowledgement or routing act has one immutable `PD-SP-EVT-####`; an unlocated response remains a source gap and is never synthesised merely to make the chronology look complete.

The hub surfaces the current canonical event IDs and their external references side-by-side.

## 6. Explicit completeness boundaries

This package does **not** convert these known gaps into evidence:

- the separately reported 22 later RedSARA/AGE records remain aggregate-only until their individual official source rows are recovered;
- `EG 58/2026` remains source-required;
- `DIP 7/2026` and `DIP 12/2026` remain stable unresolved references pending their native files and exact owning office/scope;
- the DP 1901/2026 Fiscal report and later judicial act remain source-required in the current baseline;
- receiving-office treatment after several remissions remains open unless supported by a separate source;
- internal routing/association is not inferred from a central or territorial receipt;
- the principal mailbox reconciliation was 2018–2026, so the 2011–2017 historical Fiscalía lane remains a finite backfill programme rather than a completeness claim.

A registration receipt proves the registry state shown by the receipt. It does not by itself prove internal delivery, allocation, incorporation, examination, admission, investigation or merits.

## 7. Public architecture

The new hub is the institutional front door. The pre-existing `/es/fiscalia-comunicaciones-procedimientos/` and `/en/public-prosecution-communications-proceedings/` pages remain the reciprocal communications/proceedings graph and now link back to the hub.

The hub provides:

- stable office anchors (`#office-PD-SP-I-…`);
- stable expediente anchors (`#file-PD-SP-R-…`);
- stable event anchors (`#event-PD-SP-EVT-…`);
- office-filtered views using `?office=PD-SP-I-0020#records`;
- searchable expediente and event tables;
- direct links to the canonical identity register;
- side-by-side Por Derecho and official external identifiers; and
- visible integrity state for unique event IDs, CAEPR expediente coverage and the 22-record aggregate-only RedSARA gap.

## 8. Continuity rule

Future Fiscalía work starts by reconciling these files, not by rescanning from zero:

- `assets/data/matter-identity-registry-v1.json`
- `assets/data/ministerio-fiscal-hub-config-v1.json`
- `assets/data/institutional-communications-register-v1.json`
- `assets/data/fiscalia-proceedings-interconnectivity-v1.json`
- `archive/PROCEEDINGS_MASTER_REGISTER.csv`
- `evidence/fiscalia/2026/MF_MAILBOX_REGAGE_CONTROL_31AUG2026.md`

New source-proved events are appended with new immutable IDs. Existing IDs are never recycled or renumbered.
