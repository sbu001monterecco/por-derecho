# Person identity admission, privacy and publication rule

**Control:** `PD-SP-IDENTITY-PRIVACY-001`  
**Control date:** 25 August 2026  
**Status:** controlling rule  
**Applies to:** the Por Derecho / Project Sun Rock identity registry, actor and professional pages, evidence graphs, action matrices, public repository and rendered website.

## 1. Purpose and boundary

The public identity registry is limited to people whose identity is materially relevant to the legal, evidential, institutional, recovery or public-accountability matter. A person is not eligible merely because they appear in an email, attended a meeting, work for a connected organisation, received a teaser, discussed financing, showed commercial interest or otherwise touched the wider project.

Inclusion identifies a person for evidential navigation. It is not an allegation and does not transfer knowledge, intention, control, benefit, responsibility or liability.

## 2. Three-register architecture

1. **Private master identity register — outside public Git.** Exact names, aliases, private contact data, source locators, identity verification, private evidence and any public-pseudonym mapping.
2. **Public legal-matter identity registry.** Only identities that pass the legal-matter test and have an authorised display level.
3. **Private transaction/contact register.** Investors, lenders, bankers, introducers, NDA/teaser recipients, prospective operators, commercial advisers and transaction-development contacts. A later legal overlap requires a new specific source and fresh review.

A public Git repository is publication. A file is not private because it is unrendered, under `.github/`, described as internal or excluded from navigation.

## 3. Default and admission gate

Every newly discovered natural person defaults to `PRIVATE_CANDIDATE_NOT_AUTHORISED`.

Public admission requires all of:

1. a specific actor-level legal, evidential, institutional or recovery nexus;
2. an identified source supporting the role and proposition;
3. materiality;
4. necessity of naming rather than using an organisation, role, aggregate perimeter or anonymous label;
5. identity and capacity verification;
6. privilege, confidentiality, witness-contact, litigation-strategy, safety, reputational, transaction-contamination and re-identification review;
7. an authorised display level and scope.

No automated scan, bulk import or general instruction may silently expand a person from private or anonymous to partly or fully named.

## 4. Classification

- `L_CORE` — party, officeholder or central legal actor.
- `L_MATERIAL` — materially relevant lawyer, procurador, expert, witness/declarant, source, custodian, corporate officer or public decision-maker.
- `L_RECOVERY` — materially relevant to a claimant-specific asset, right, income or loss.
- `X_OVERLAP_REVIEW` — possible transaction/legal overlap requiring a new sourced assessment.
- `T_TRANSACTION_ONLY` — banking, investment, sale, financing, NDA, onboarding or other transaction-development contact.
- `I_INCIDENTAL` — copied recipient, administrator, family/friend, media contact or incidental mention.
- `U_UNRESOLVED` — identity or relevance not established.

Only `L_CORE`, `L_MATERIAL` and `L_RECOVERY` are eligible for public admission.

## 5. Display states

- `PRIVATE_ONLY` — no public repository or website record.
- `ANONYMISED_PUBLIC` — opaque non-identifying label; do not combine unique employer, title, date, place or transaction details.
- `PARTIAL_NAME_PUBLIC` — only the authorised limited form, after re-identification review.
- `FULL_NAME_PUBLIC` — exact verified public name.
- `FULL_NAME_PUBLIC_ROLE_ONLY` — exact professional name with a neutral, minimal role and no privileged or current-strategy detail.
- `WITHDRAWN_PUBLIC` — removed from current public display; ID reserved and never reassigned.

Partial naming is normally pseudonymisation rather than true anonymity. A legacy ID previously mapped to a full name in Git history must not be reused as if it had become anonymous.

## 6. Spanish lawyers and professional advisers

Spanish lawyers and law firms must appear on a distinct professional-capacity surface, separated from adverse actors and from collective criminal allegations.

- Current Spanish counsel may be shown by full verified professional name under `FULL_NAME_PUBLIC_ROLE_ONLY` where expressly instructed, but current strategy, fees, private correspondence, work allocation and privileged advice remain excluded.
- Former Spanish counsel may be shown by full name, firm, period and sourced matter capacity. Professional appearance is not proof of fault, authorship of every document, representation of every connected entity or firm-wide knowledge.
- Procuradores remain distinct from lawyers.
- Billing, collections, copied, administrative and proposal-only contacts are not labelled substantive or retained counsel without mandate, filing or authorship evidence.
- UK lawyers are excluded from the Spanish-counsel register.

## 7. Historical owners and Community participants

Ownership, attendance, representation, a vote or collective naming in a complaint establishes context, not collective knowledge or wrongdoing. Each public description must state the exact sourced capacity and preserve that allegations remain allegations.

## 8. Authorisation and change control

Before a new person or material visibility expansion, retain an approval card containing:

```text
Candidate / ID:
Legal classification:
Exact legal nexus and date range:
Supporting source classes:
Why naming is necessary:
Limiting or contrary evidence:
Privacy / privilege / re-identification risks:
Display state:
Repository scope:
Website scope:
Exact public wording:
```

Fresh review is required when an anonymous person becomes named, a neutral role becomes an alleged-conduct role, a new sensitive source or proceeding is linked, or transaction material is moved into the legal track.

## 9. Legacy and correction rule

Every existing person remains subject to legacy admission review. A correction updates the same identity; IDs are never recycled. Contrary, innocent and exculpatory identity evidence must remain visible.

Removing or anonymising a name on current `main` reduces current exposure but does not erase earlier public commits, forks, caches or search indexes. History rewriting and de-indexing require a separate assessment and express destructive-change authority.