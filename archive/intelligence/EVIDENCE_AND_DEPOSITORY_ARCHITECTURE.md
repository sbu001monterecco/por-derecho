# Evidence and depository architecture

## Objective

Convert a very large, duplicated and fragmented archive into a persistent evidential knowledge system that is navigable by humans and reusable by AI without repeatedly rereading the same material.

## Core distinction

The repository must separate:

1. **Sources** — original documents/evidence.
2. **Propositions** — individual factual assertions supported, contradicted or left unresolved by sources.
3. **Events** — dated acts/occurrences.
4. **Entities** — people, companies, courts, authorities, advisers and other actors.
5. **Proceedings/matters** — the legal/administrative containers in which acts occur.
6. **Narratives/outputs** — website, book, media, legal, investor and research products derived from the layers above.

The website is an output layer. It must not become its own circular source of truth.

## Proposed top-level repository structure

```text
/00_GOVERNANCE
    evidence-standard
    publication-standard
    corrections
    right-of-reply
    privacy-redaction
    privilege
    AI-use
    source-ranking

/01_CANONICAL_SOURCES
    judicial
    registry
    notarial
    banking
    corporate
    accounting
    tax
    administrative
    correspondence
    technical

/02_OBJECTS
    SR-A001_SUN_PARK
    SR-C001_LPB_MORTGAGE_CREDIT
    properties
    rights
    companies

/03_ENTITIES
    people
    companies
    institutions
    courts
    professional-actors

/04_EVENTS
    master-chronology

/05_PROCEEDINGS
    concurso
    civil
    enforcement
    criminal
    fiscal
    administrative
    regulatory
    professional

/06_LEDGERS
    fact
    title
    credit
    money
    knowledge
    custody
    decision
    power
    consequence

/07_INTELLIGENCE
    contradictions
    premise-provenance
    memory-breaks
    alternative-explanations
    adverse-evidence
    falsification
    missing-documents

/08_OUTPUTS
    website
    book
    journalist
    lawyer
    investor
    donor
    academic

/09_RESTRICTED
    privileged
    personal-data
    litigation-strategy
    confidential

/10_ARCHIVE
    duplicates
    versions
    superseded
    AI-working-products
```

The public GitHub repository must not actually contain restricted source material simply because `/09_RESTRICTED` exists conceptually. Restricted material requires an access-controlled environment.

## Canonical source record

Every high-value source should eventually carry fields equivalent to:

```text
SOURCE_ID:
TITLE:
DATE:
CREATOR / AUTHORITY:
SOURCE_TYPE:

ORIGINAL_LOCATION:
GMAIL_ID:
DRIVE_ID:
ONEDRIVE_ID:
LIBRARY_ID:

SHA256:
CANONICAL_VERSION:
VERSION_FAMILY:
DUPLICATES:

PRIMARY / SECONDARY:
AUTHENTICITY_STATUS:

ENTITIES:
EVENTS:
PROCEEDINGS:
ASSETS / RIGHTS:

PROPOSITIONS_SUPPORTED:
PROPOSITIONS_CONTRADICTED:

WHAT_THIS_SOURCE_ESTABLISHES:
WHAT_THIS_SOURCE_DOES_NOT_ESTABLISH:

PUBLICATION_STATUS:
PUBLIC_REDACTION_REQUIRED:

LAST_HUMAN_REVIEW:
LAST_AI_ANALYSIS:
SUPERSEDED_BY:
```

## Atomic proposition record

Each material proposition should be independently addressable:

```text
PROPOSITION_ID:
TEXT:
STATUS:
CONFIDENCE / EVIDENTIAL CLASS:
SOURCE_IDS:
PINPOINTS:
RELATED_EVENT:
RELATED_ENTITIES:
RELATED_PROCEEDING:
CONTRADICTED_BY:
ALTERNATIVE_EXPLANATION:
WHAT_WOULD_CHANGE_THIS_CLASSIFICATION:
LAST_REVIEWED:
DEPENDENT_OUTPUTS:
```

The field **WHAT WOULD CHANGE THIS CLASSIFICATION?** is mandatory for important disputed propositions. It converts a static narrative into an investigation/falsification system.

## Evidential statuses

Recommended public-safe statuses:

- `DOCUMENTED` — directly supported by identified evidence.
- `PROCEDURAL_FACT` — filing, order, status, receipt or other procedural fact.
- `PARTY_POSITION` — attributed claim or submission.
- `INFERENCE` — conclusion drawn from identified facts.
- `DISPUTED` — materially contested.
- `CONTRADICTED` — evidence points materially against the proposition.
- `UNDER_VERIFICATION` — potentially important but not yet sufficiently established.
- `DOCUMENT_GAP` — the proposition depends on a missing/unproduced source.
- `CORRECTED` — prior formulation amended.
- `SUPERSEDED` — historical version retained for audit but no longer current.

## Ledgers

### Fact ledger
Atomic facts and their source chain.

### Title ledger
Property-by-property ownership, rights and transfers.

### Credit ledger
Origin, assignment, economic owner, registered/legal holder, procedural holder, balances and satisfaction.

### Money / quantum ledger
Amounts, valuations, payments, debt calculations, income, consideration and disputed bridges.

### Knowledge ledger
Who received/possessed which material information, when, by what channel, and what action followed.

### Custody ledger
Where originals/copies are stored; hashes; version families; chain-of-custody information where relevant.

### Decision ledger
Every material judicial/administrative decision, including:

- what was before the decision-maker;
- operative outcome;
- facts expressly found;
- reasoning;
- what was **not** decided;
- appeal/review status;
- downstream consequence.

### Power ledger
The authority claimed or exercised by actors at each material date: title, mandate, vote, proxy, judicial power, administrative competence, possession/control.

### Consequence ledger
First-, second- and higher-order consequences of decisions/acts for ownership, control, income, rights, procedural options, public representations and later decision-making.

## Adverse evidence / counter-case

The repository must actively preserve the strongest evidence against the project's preferred thesis. For every central proposition, record:

- strongest alternative explanation;
- evidence supporting it;
- evidence weakening the project's interpretation;
- whether the matter has been judicially determined;
- what evidence remains missing;
- what would falsify the present thesis.

This is both an evidential and publication-safety requirement.

## Negative propositions

Record not only what a source establishes, but what it does **not** establish. Example pattern:

> A particular enforcement-termination order establishes termination/satisfaction of that procedural vehicle. It does not automatically adjudicate the validity of every antecedent act, property right, estate question, third-party right, restitution claim or separate cause of action unless the text actually does so.

Negative propositions should be source-specific and legally disciplined, not generic disclaimers.

## Publication classes

At minimum:

- `PUBLIC`
- `PUBLIC_REDACTED`
- `RESEARCH_INTERNAL`
- `PRIVILEGED_RESTRICTED`

A source should not appear publicly merely because an AI found it relevant.

## Publication firewall

Before a material proposition is published, test:

1. **Source** — what evidence supports it?
2. **Status** — fact, procedural fact, allegation, inference, dispute or gap?
3. **Counter-case** — what points the other way?
4. **Legal** — is the wording defensible and proportionate?
5. **Privacy/confidentiality** — what must remain restricted/redacted?
6. **Necessity** — is naming an individual necessary?
7. **Language** — conduct/evidence versus declaration of culpability.
8. **Update** — could an appeal or new decision materially alter the proposition?

## Minimum viable evidential depository

Initial target:

- 250–500 canonical high-value primary sources;
- 1,500–3,000 atomic propositions;
- 100–200 core entities;
- master chronology;
- all material judicial decisions;
- `SR-A001` and `SR-C001`;
- core title/credit/money/knowledge/decision/consequence ledgers;
- adverse-evidence register;
- top 50 unresolved questions;
- publication state for every object.

This should capture a disproportionate share of useful knowledge without processing every stored byte.

## Anti-token-waste rule

Once a document's relevant propositions, citations and metadata have been safely persisted, future AI work should retrieve the canonical record and return to the original only where verification, a new question or a changed interpretation requires it.

**Duplicates are not deleted from custody. They are demoted from knowledge objects to custody/version objects.**