# Current Legal and Professional Advisers — Classification Control

**Control date:** 28 August 2026  
**Purpose:** Canonical classification record for the Por Derecho / Project Sun Rock repository and public website. This file is intended to prevent current, historical, prospective or approved advisers from being accidentally classified as adverse parties merely because their names or firms appear in litigation, correspondence, evidence or third-party materials.

## Mandatory classification rule

Every lawyer, law firm, procurador or professional adviser must be assigned an explicit role/status before public presentation or actor-matrix classification. The approved status vocabulary is:

1. `OUR CURRENT ADVISER`
2. `OUR APPROVED LEGAL ADVISER — NO LIVE MANDATE IMPLIED`
3. `OUR HISTORICAL ADVISER`
4. `PROSPECTIVE / ENGAGEMENT STATUS TO BE CONFIRMED`
5. `THIRD-PARTY LAWYER / PROFESSIONAL`
6. `ADVERSE-PARTY LAWYER / PROFESSIONAL`
7. `ROLE UNDER VERIFICATION`

No person or firm may be moved into `ADVERSE-PARTY LAWYER / PROFESSIONAL` merely because they appear in an adverse proceeding, correspondence with an adverse party, or an evidentiary record. Where evidence is insufficient, use `ROLE UNDER VERIFICATION` rather than adverse classification.

## Our current legal advisers

### Carlos Llamas Sanz

- **Status:** `OUR CURRENT ADVISER`
- **Public name:** Carlos Llamas Sanz
- **Public professional description:** Abogado / Lawyer — Carlos Llamas Legal Compliance
- **Role:** Current coordinating legal adviser across litigation, contentious/procedural matters, property and transactional work, financing-related legal strategy, and the wider Project Sun Rock / Aweswell legal workstreams.
- **Safeguard:** Do not classify Carlos Llamas Sanz as an adverse-party lawyer in any actor map, proceeding page, evidence graph or lawyer index merely because he appears in correspondence concerning adverse parties or contested proceedings.

### Javier Sixto

- **Status:** `OUR CURRENT ADVISER`
- **Firm:** Sixto Abogados
- **Role:** Current lawyer acting on Aweswell / Pink-related contentious and procedural matters, including the insolvency-administrator-separation and AEAT / Pink workstreams.
- **Safeguard:** Must remain on the adviser side of any actor graph unless a later verified source requires a status change.

### Estefanía Sixto Seijas

- **Status:** `OUR CURRENT ADVISER`
- **Firm:** Sixto Abogados
- **Role:** Current member of the legal team working with Javier Sixto on Aweswell / Pink and related legal workstreams.
- **Safeguard:** Must not be grouped with adverse counsel because of appearances in litigation correspondence or procedural records.

### Adriana Hernández Díaz

- **Status:** `OUR CURRENT ADVISER / PROCEDURAL REPRESENTATION SUPPORT — PRECISE PROFESSIONAL CAPACITY TO BE DISPLAYED ONLY WHEN VERIFIED`
- **Role:** Correspondence evidences coordination with the group's lawyers in court filings and procedural steps.
- **Safeguard:** Do not describe as adverse counsel. Public-facing professional title should be added only from a verified professional source or formal filing.

### Cristo Suárez Pimentel

- **Status:** `OUR ADVISER — CURRENT / HISTORICAL SCOPE TO BE EXPRESSED MATTER-BY-MATTER`
- **Firm:** Pimentel Abogados
- **Role:** Adviser within the group's legal perimeter in matters evidenced by correspondence. Recent correspondence concerns review and re-ordering of outstanding matters.
- **Safeguard:** Do not classify as adverse merely because his name occurs in legacy litigation or older case materials.

## Fieldfisher — firm-level approved adviser classification

### Fieldfisher Spain and Fieldfisher UK

- **Status:** `OUR APPROVED LEGAL ADVISER — NO LIVE MANDATE IMPLIED`
- **Public presentation:** **Fieldfisher — Approved Legal Adviser to the Group***
- **Geographic scope:** Spain and United Kingdom.
- **Named-lawyer public rule:** **Do not publicly list specific Fieldfisher lawyers.** Public website references should be at firm level only unless the Group later expressly authorises individual attribution.
- **Repository rule:** Individual lawyer names may be retained in the repository record where necessary to preserve correspondence provenance, chronology, conflict-check history, introductions or professional-contact continuity. Their presence in the repository does not itself establish a live retainer, live instruction or active workstream.

### Required public asterisk

> ***Approved Legal Adviser** denotes a law firm approved by the Group as part of its legal-adviser perimeter. It does **not** by itself mean that the firm has a live current mandate, is presently instructed on a matter, or is carrying out an active legal workstream at the date of publication.*

This qualification must travel with any public-facing Fieldfisher reference unless the surrounding text already makes the same limitation unmistakably clear.

## Public website drafting rule

Recommended public adviser entry:

**Fieldfisher — Approved Legal Adviser to the Group***  
Spain and United Kingdom.

***Approved Legal Adviser** denotes a firm approved by the Group as part of its legal-adviser perimeter. It does not by itself mean that the firm has a live current mandate, is presently instructed on a matter, or is carrying out an active legal workstream at the date of publication.*

Do not display individual Fieldfisher lawyer names on the public adviser page.

## Actor-map / evidence-graph safeguard

Where a lawyer or firm has multiple contextual appearances, the actor model must store `relationship_to_group` separately from `appears_in_matter_with`. Example: a law firm may appear in correspondence involving a counterparty without becoming adverse counsel. Relationship classification must be sourced independently from mere co-occurrence.

For Fieldfisher use:

```yaml
entity: Fieldfisher
relationship_to_group: OUR APPROVED LEGAL ADVISER — NO LIVE MANDATE IMPLIED
jurisdictions:
  - Spain
  - United Kingdom
public_named_individuals: false
live_mandate_implied: false
active_workstream_implied: false
public_footnote_required: true
```

## Non-adverse classification control

The following names/firms must not be accidentally presented as adverse actors while the above classifications remain current:

- Carlos Llamas Sanz / Carlos Llamas Legal Compliance
- Javier Sixto / Sixto Abogados
- Estefanía Sixto Seijas / Sixto Abogados
- Adriana Hernández Díaz, subject to precise-capacity verification
- Cristo Suárez Pimentel / Pimentel Abogados, matter-by-matter current/historical scope
- Fieldfisher Spain
- Fieldfisher UK

Any automated or manual classification process that conflicts with this file should flag the conflict for review rather than silently reclassifying the adviser.
