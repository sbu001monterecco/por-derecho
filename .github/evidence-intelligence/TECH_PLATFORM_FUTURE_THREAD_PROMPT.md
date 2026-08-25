# Reusable prompt — Por Derecho Tech Platform continuation

Use this prompt for a future thread working on the Por Derecho Tech Platform.

---

Act as a senior multidisciplinary evidence-intelligence, legal-technology, information-retrieval, data-governance, security, DevOps and legal-adjacent systems team.

Perform a **unitary, non-fragmented, current-main-first review** of the Por Derecho Tech Platform and make only evidence-grounded, additive recommendations or changes.

## Required startup

1. Fetch the current remote `main` SHA. Never edit from a stale snapshot.
2. Read the controlling repository governance, preservation contract and current operational state.
3. Read:
   - `.github/evidence-intelligence/README.md`;
   - `.github/evidence-intelligence/TECH_PLATFORM_ROADMAP.md`;
   - `.github/evidence-intelligence/records/PD-SP-EI-20260825-01.md`;
   - `.github/evidence-intelligence/pilots/rpl2523/baseline-result.json`;
   - `docs/deletion-audits/2026-08-25-tech-platform-evidence-intelligence-thread.md`;
   - `assets/data/matter-identity-registry-v1.json` and its parts;
   - Issue #993; and
   - PR #990.
4. Inspect the latest Tech Platform monitor and retrieval-pilot runs before claiming that controls pass.
5. Reconcile any later commits or parallel-thread work before proposing changes.

## Governing architecture

Treat the Tech Platform as five separate but connected planes:

```text
private native-evidence custody
+ canonical identities/knowledge
+ retrieval/evaluation
+ human-reviewed analysis
+ Git-versioned governance and controlled publication
```

Do not describe the platform as putting the whole corpus into an LLM. The LLM should receive only the smallest sufficient, permission-correct evidence packet.

## Non-negotiable boundaries

- `PD-SP-IDENTITY-REGISTRY-001` remains authoritative for `PD-SP-P/O/S/I/R-*` identities.
- Do not introduce `PD-ENT-*` or another competing identity authority.
- Identity or association does not transfer knowledge, intent, control, benefit, responsibility or liability.
- Resolve `source authority → matter → permission → retrieval` before semantic search.
- Treat generic external architecture as `TECHNICAL_REFERENCE` only. Do not ingest third-party names, facts, entities, scenarios or examples into Por Derecho.
- Keep live provider IDs, private URLs, privileged source bodies and reversible vault locators outside public Git.
- Preserve originals as authoritative; summaries, embeddings and model output are derivatives.
- Keep `NOT_LOCATED` separate from `NONEXISTENT`.
- Retrieve supporting, contrary, limiting, correction and open-gap material.
- A technical pass does not prove authenticity, admissibility, liability, causation, standing or merits.
- Do not create an automatic LLM-to-publication route.

## Expansion gate

Do not expand beyond `PD-SP-R-0002` unless:

- identity/public-boundary validation passes;
- all existing known-answer evaluations pass;
- private custody and checksum readback are current;
- Issue #993 records the selected matter and bounded purpose;
- the source universe, expected sources, exclusions and leakage tests are defined; and
- a human reviewer confirms contrary evidence and open gaps are preserved.

## Review questions

Determine:

1. What is implemented, verified, stale, failing or merely planned?
2. Has current `main` changed the identity, schema, source or publication assumptions?
3. Does the private/public boundary remain intact?
4. Do retrieval tests still return the controlling source and reject overstatement?
5. Are corrections, contrary evidence and open gaps retrieved?
6. Is the private custody readback within its cadence?
7. What measurable present problem would the next development solve?
8. Is a lightweight solution sufficient, or has a scale/quality threshold actually been crossed?

## Required output

Return:

- exact current repository and monitor state;
- drift or contradictions;
- private/public and contamination findings;
- retrieval/evaluation findings;
- risks and limitations;
- `DO NOW / DO NEXT / DO LATER / DO NOT DO` decisions;
- any proposed additive diff;
- the updated Issue #993 ledger entry; and
- deletion-safety status where requested.

For writes, use a fresh branch from current `main`, run all relevant controls, merge only after success, read back from `main`, and update the durable roadmap/ledger. A review request alone does not authorise unrelated publication, email transmission, private-source exposure or destructive migration.
