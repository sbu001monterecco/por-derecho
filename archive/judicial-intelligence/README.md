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

## Core datasets

- `courts.csv` — court/proceeding register.
- `decisions.jsonl` — one structured record per material judicial or LAJ act.
- `ingestion_queue.csv` — priority missing primary decisions and metadata.
- `ANALYSIS_PROTOCOL.md` — rules for recurring intelligence analysis.

## Non-fragmentation rule

The same physical/economic asset may appear across insolvency, civil execution, preliminary disclosure, criminal investigation, appellate and administrative contexts. Preserve those links **without treating legally distinct proceedings as one undifferentiated case**.

## Decision reading rule

Every material decision should ultimately have four separate fields:

1. `decided` — what the operative judicial act actually did.
2. `not_decided` — propositions that must not be inferred from it.
3. `evidence_before_court` — what is demonstrably known to have been before the organ.
4. `downstream_effect` — later procedural/economic consequences, stated without automatically assigning legal causation.

## Safety and fairness

Repeated assignment of the same judge, court, section, lawyer, administrator or prosecutor does not prove coordination, conflict or misconduct. Network or recurrence analysis is descriptive unless an independently sourced material relationship is established.

The archive must be capable of reaching either conclusion: that a concern merits further verification **or that the concern is not supported by the record**.
