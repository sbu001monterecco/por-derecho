# RICPE / Canary private-capital public internet source universe

**Control date:** 29 September 2026  
**Status:** ACTIVE RECURSIVE PUBLIC-SOURCE CENSUS  
**Parent continuity:** `RICPE_INVESTOR_THREAD_CONTINUITY_PRESERVATION_AUDIT_20260929.md`  
**Canonical actor register:** `assets/data/ricpe-capital-ecosystem-actor-register-v1.json`

## Objective
Build the fullest lawful public-source picture of RIC Private Equity / RICPE, its current and historical people, Board, management, investor-relations function, investors/shareholder positions, capital events, advisers, depositary, valuation/risk/compliance providers, project counterparties, introducers, event networks and relevant Canary private-capital ecosystem.

No single search result is treated as complete. The process is recursive: every new person, organisation, capital event, document, event or relationship creates bounded follow-up searches until the branch reaches a documented terminal state.

## Canonical identity rule
Every named public-source person receives an immutable `PD-SP-RICACT-####` actor reference immediately. Every named public-source organisation receives an immutable `PD-SP-RICORG-####` reference. These are RICPE-domain occurrence/census references, not replacements for the global CAEPR identity registry.

Each actor/org reference must:
1. search the global `PD-SP-P-####` / `PD-SP-O-####` registry first;
2. crosswalk to an existing global identity where established;
3. retain a candidate crosswalk separately where identity is plausible but not proved;
4. never merge people merely because surname, employer, geography, family/business network or timing looks similar;
5. keep source-literal partial names as unresolved rather than guessing the missing name.

Investor positions remain separately identified by `PD-SP-RICINV-####`. An investor-position reference is not automatically a person identity.

## Public source universe

### A. Official / primary registries — scan first
- CNMV registered-entity record for RICPE no. 295: administrators, historical dates, share classes, audits and downloadable filings/DFIs where exposed.
- BOE / BORME: incorporations, appointments/cessations, powers, capital increases/reductions, statutory changes, mergers/spin-offs and related companies.
- Registro Mercantil public notices and legally accessible registry extracts.
- Gobierno de Canarias / BOC: RIC idoneidad decrees, tax-incentive/public-support records, corporate/project references and public appointments.
- BDNS / Sistema Nacional de Publicidad de Subvenciones, regional incentives and public-grant databases.
- EU/FEDER public project and beneficiary databases where applicable.
- Plataforma de Contratación del Sector Público and Canary/local procurement portals where relevant.
- Cabildo / Ayuntamiento transparency, licences, planning, tourism, grants and public-file indexes.
- CENDOJ / public judicial decisions where names/entities are lawfully public and materially relevant.

### B. Issuer / counterparty primary web sources
- RICPE current website: team, Board, history, partners, portfolio/investments, annual reports, prospectus, DFI/KID, RIC, investor-relations, news/events, sustainability, shareholder-meeting materials and PDFs.
- RICPE historical PDFs, media files, sitemaps and archived versions.
- Project-company / operator / borrower sites and public corporate materials.
- Adviser, auditor, depositary, valuation/risk/compliance and law-firm public pages.

### C. Professional and capital-network sources
- Public LinkedIn/company/profile pages and other public professional biographies.
- CEOE Tenerife, CEOE Canarias, FEPECO, Ashotel, chambers of commerce, RECABA/business-angel networks, family-business associations and investment-event pages.
- Public conference agendas, speaker lists, attendee/sponsor lists and webinar/video descriptions.
- Universities/business schools and professional-association biographies where they corroborate role/history.

### D. Press / trade / archive sources
- Canary and Spanish business press, hotel/real-estate trade press, corporate interviews and event coverage.
- Public YouTube/Vimeo/podcast/webinar pages and transcripts where available.
- Internet Archive / archived public websites, cached/publicly indexed historic pages.
- Search-engine indexed PDFs and public document metadata.
- Commercial corporate-information pages only as secondary leads; formal conclusions require primary-source reconciliation.

## Query expansion
For each canonical actor/org, recursively search:
- exact full name;
- verified aliases / shortened professional names;
- company + role;
- company + BORME / CNMV / BOC;
- event + date + person;
- PDF/document metadata;
- old employer / new employer;
- director/secretary/administrator/representative roles;
- capital increase / subscription / investor relations / RIC;
- Tenerife / Gran Canaria / Lanzarote + relevant event networks;
- counterparties, advisers, introducers and co-investors.

## Evidence-state grammar
- `PRIMARY_CONFIRMED`
- `DIRECT_PUBLIC_SOURCE`
- `CORROBORATED_PUBLIC_SOURCE`
- `CANDIDATE_IDENTITY_OR_LINK`
- `CONTRARY_OR_CONFLICTING_SOURCE`
- `UNRESOLVED`
- `RETIRED_DUPLICATE`

Search repetition or graph proximity never upgrades evidence by itself.

## Recursive stop conditions
A branch stops only when: identity/role is primary-confirmed; the proposition is disproved; a duplicate is reconciled; the public source is exhausted for the present question; or the branch is no longer material.

## Privacy and proportionality
Use professional/business public information only. Do not aggregate private home addresses, personal phone numbers, private family-life information, leaked datasets, credentials, private banking/KYC/source-of-funds data, or other sensitive personal information merely because it can be found online. Do not contact any person automatically.

## Output on every scan
- new actors/orgs discovered;
- new or changed public roles;
- canonical RICACT/RICORG reference;
- global PD-SP-P/O crosswalk status;
- source URL/title/date;
- relationship/event/capital node created;
- contradictions;
- next bounded queries;
- whether repository update is warranted.
