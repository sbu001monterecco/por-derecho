# Private transaction-development workspace charter

**Task:** `P2-TX-WS-01`  
**Public-repository status:** charter only; the actual workspace and named contents remain private.

## Purpose

Provide a controlled private home for current and prospective financing, investment, banking, acquisition, sale, co-investment, operator and external-adviser work that is separate from the Por Derecho litigation, evidence and public-accountability repository.

## Minimum private workspace structure

1. `00_governance/`
   - access register;
   - confidentiality and privilege rules;
   - retention schedule;
   - conflicts/onboarding status;
   - disclosure approvals.
2. `01_counterparties/`
   - one folder per verified legal entity or group;
   - current contacts and capacities;
   - source locators and communication status.
3. `02_opportunities/`
   - one folder per opportunity using a neutral internal code;
   - authority/control statement;
   - transaction status;
   - valuation and model versions;
   - disclosure perimeter.
4. `03_financing_playbook/`
   - named institution matrix;
   - historic route files;
   - current shortlist and scoring;
   - stale-term flags.
5. `04_nda_and_engagements/`
   - current and superseded NDAs;
   - execution copies;
   - law-firm engagement and conflict records;
   - permitted-recipient matrix.
6. `05_meetings_and_actions/`
   - calendar invitation;
   - attendee/capacity record;
   - consented transcript or notes;
   - post-meeting summary;
   - action ledger.
7. `06_custody_and_exports/`
   - native exports;
   - hashes where actually generated;
   - provider-independent backup state;
   - chain-of-custody events.

## Access roles

Define, at minimum:

- project principal;
- group-side legal coordinator;
- external counsel by active engagement and need to know;
- financial adviser or analyst by approved workstream;
- read-only reviewer;
- administrator/custodian.

No role receives access by personal relationship alone. Access requires a current purpose, capacity and confidentiality basis.

## Information classes

- `TX-0 PUBLIC` — independently announced and verified transaction facts approved for publication.
- `TX-1 PUBLIC_SAFE_DERIVATIVE` — anonymised method/status suitable for public Git.
- `TX-2 CONFIDENTIAL` — current counterparties, opportunities, NDAs, models and negotiations.
- `TX-3 LEGAL_PRIVILEGED_OR_RESTRICTED` — legal advice, conflict analyses, engagement documents and protected strategy.
- `TX-4 NATIVE_EVIDENCE` — native emails, exports, attachments, signatures, provider metadata and custody records.

Public Git may contain only `TX-0` after a separate publication decision or `TX-1` where continuity requires it.

## Required controls

- Each document has owner, source, date, version, confidentiality class and supersession status.
- Historic proposals and terms are marked stale until revalidated.
- One group may contain several legal entities; their mandates and approvals remain separate.
- No asset is described as controlled, available or deliverable without an authority statement.
- Every disclosure records recipient, capacity, purpose, legal basis and document/version set.
- External circulation requires the applicable NDA and approval perimeter.
- Native email and provider locators are never copied into public Git.

## Public continuity

Public repository continuity uses opaque IDs such as `TXD-YYYYMMDD-NN`. It may state:

- broad objective;
- generic institution or product class;
- stage taxonomy;
- privacy and authority rules;
- open next action.

It must omit:

- names and addresses;
- private subjects and message identifiers;
- unannounced assets;
- exact current pricing, leverage, valuations or negotiation positions;
- native documents;
- claims of approval or commitment not evidenced by definitive records.

## Promotion to public statement

A transaction fact may move to `TX-0 PUBLIC` only where:

1. the relevant transaction or relationship has been formally announced or independently verifiable;
2. the legal entity and capacity are correct;
3. confidentiality and contractual restrictions permit publication;
4. the statement distinguishes signed, conditional, approved, completed and funded states;
5. a separate publication decision has been recorded.

## External-action boundary

Creating or using this workspace does not authorise contact with any third party, sending an email, accepting terms, scheduling a meeting or disclosing a document.
