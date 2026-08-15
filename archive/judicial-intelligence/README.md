# Judicial Intelligence Archive / Archivo de Inteligencia Judicial

Status: living evidential register. Initialised: 2026-08-15.

Purpose: preserve and continuously analyse the judicial history touching Sun Park / Luchy Playa Blanca / Aweswell / Matkator / Pink Canary Services and connected patrimonial questions without collapsing separate jurisdictions or converting allegations into findings.

## Governing question

**Who decided what, on what record, at what time, with what formal, evidential and patrimonial effect?**

## Evidential classes

- `VERIFIED_PRIMARY`: directly established by a signed court resolution or official court record.
- `VERIFIED_PROCEDURAL`: establishes a filing, transfer, appeal, archive, admission step or other procedural event, but not the truth of the underlying allegation.
- `CORPUS_REPORTED_PRIMARY_PENDING`: repeatedly identified in the controlled corpus, but the signed primary resolution still needs to be deposited/linked here.
- `PARTY_POSITION`: assertion or legal characterisation by a party.
- `OPEN_QUESTION`: material gap requiring source retrieval.
- `SUPERSEDED_OR_CORRECTED`: earlier proposition corrected by later evidence.

## Core datasets and protocols

- `courts.csv` — judicial court/proceeding register, now covering located Lanzarote, Gran Canaria and Tenerife tracks.
- `decisions.jsonl` — one structured record per material judicial or LAJ act.
- `ingestion_queue.csv` — priority missing primary decisions and metadata.
- `ANALYSIS_PROTOCOL.md` — rules for recurring intelligence analysis.
- `../SUN_PARK_COMUNIDAD_PROCEEDINGS_REGISTER_CANARY_ISLANDS_15AUG2026.md` — canonical cross-island register of judicial, Fiscalía, governance, administrative, tourism, transparency, professional and registered-only files currently located in the repository/site.
- `../P18_SUN_PARK_COMUNIDAD_CROSS_ISLAND_PROCEEDINGS_INTELLIGENCE_15AUG2026.md` — controlling protocol for complete cross-island proceeding discovery, classification and transmission mapping.
- `../P17_JUDGE_LAJ_COMMUNICATIONS_INTELLIGENCE_CONCURSO36_15AUG2026.md` — controlling protocol for judge, LAJ and court-office communications inside Concurso 36/2012.

## Cross-island completeness rule

“All proceedings” means all proceedings and institutional files currently located in the scanned controlled repository and website at the stated cut-off. It does not prove that no other court case, appeal, incident, Fiscalía file, administrative file or professional proceeding exists.

Geography must be represented in layers: originating facts/asset; first-instance or administrative organ; appellate/supervisory organ; and current custodian. A Lanzarote-origin dispute decided by the Audiencia Provincial in Gran Canaria remains a Lanzarote-origin proceeding with a Gran Canaria appellate stage.

## Non-fragmentation rule

The same physical/economic asset may appear across insolvency, civil execution, preliminary disclosure, criminal investigation, appellate, Fiscalía, administrative, tourism, transparency, professional and judicial-governance contexts. Preserve those links **without treating legally distinct proceedings as one undifferentiated case**.

A document or premise is not treated as having reached another proceeding unless a filing, testimonio, remisión, oficio, service record, deed, registry entry or other transmission mechanism is located.

## Decision reading rule

Every material decision should ultimately have four separate fields:

1. `decided` — what the operative judicial act actually did.
2. `not_decided` — propositions that must not be inferred from it.
3. `evidence_before_court` — what is demonstrably known to have been before the organ.
4. `downstream_effect` — later procedural/economic consequences, stated without automatically assigning legal causation.

## Safety and fairness

Repeated assignment of the same judge, court, section, lawyer, administrator or prosecutor does not prove coordination, conflict or misconduct. Network or recurrence analysis is descriptive unless an independently sourced material relationship is established.

A provisional archive does not create civil or tourism title. A tourism/municipal file does not decide private ownership. A Community act does not automatically confer authority over every unit. A technical reference is not automatically a professional-disciplinary file. A registered police communication is not an investigation unless an assigned file or substantive act is located.

The archive must be capable of reaching either conclusion: that a concern merits further verification **or that the concern is not supported by the record**.
