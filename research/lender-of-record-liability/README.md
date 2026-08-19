# Lender-of-record liability architecture

**Status:** canonical research layer — active  
**Last controlled update:** 19 August 2026  
**Public pages:** `/en/lender-of-record/liability/` · `/es/acreedor-de-registro/responsabilidad/`

## Purpose

This dossier reconstructs the Sun Park asset-backed credit chain as a **multi-actor, multi-proceeding and multi-remedy system**. It does not assume that every assignee inherited every liability of the previous lender.

The controlling analytical proposition is:

> The credit and its accessory rights may travel downstream; defects and defences affecting the credit may remain relevant to an assignee; historic personal wrongdoing does not automatically transfer merely because the credit was sold; each downstream actor may incur its own responsibility through its own conduct after acquisition or notice; mandate, responsibility for others and corporate succession require their own proof.

The repository therefore distinguishes:

1. **rights transferred**;
2. **defects or defences attached to the right**;
3. **obligations or personal liability retained upstream**;
4. **new downstream conduct and incremental harm**;
5. **servicer/principal authority and ratification**;
6. **ordinary assignment versus universal corporate succession**;
7. **contractual foreseeability and extra-contractual legal attribution**;
8. **actor-specific limitation and preservation**.

## The chain under review

`original lender / Bankia perimeter → SAREB → PH122 → CAM → HNT`

Haya and the wider Cerberus perimeter are modelled as separate actors whose exact mandate, control and decision authority must be proved rather than inferred from group labels.

## Nine linked layers

| Layer | Core question | Canonical file |
|---|---|---|
| Actor/entity | Who acted, in what capacity and during what period? | [ACTOR-MATRIX.md](ACTOR-MATRIX.md) |
| Instrument/asset | What loan, product, security, claim or economic unit is being discussed? | [CREDIT-SECURITY-GENEALOGY.md](CREDIT-SECURITY-GENEALOGY.md) |
| Transfer chain | What moved, when, for what consideration and subject to what allocation of liability? | [TRANSFER-CHAIN.md](TRANSFER-CHAIN.md) |
| Knowledge/notice | Who knew what, when, from which source and with what limits? | [KNOWLEDGE-NOTICE.md](KNOWLEDGE-NOTICE.md) |
| Conduct/decision | What did each actor do after acquisition or notice? | [CONDUCT-DECISIONS.md](CONDUCT-DECISIONS.md) |
| Legal route | Which distinct legal route could attach to which actor? | [LEGAL-ROUTES.md](LEGAL-ROUTES.md) |
| Proceeding/remedy | Where can a proposition be used and what remedy can that forum grant? | [PROCEEDINGS-REMEDIES.md](PROCEEDINGS-REMEDIES.md) |
| Causation/damages | What incremental harm is legally attributable and how remote is it? | [CAUSATION-DAMAGES.md](CAUSATION-DAMAGES.md) |
| Contradictions/defence | What is the strongest adverse case and what evidence discriminates? | [CONTRADICTIONS-DEFENCES.md](CONTRADICTIONS-DEFENCES.md) |

Limitation is controlled separately in [LIMITATION-PRESERVATION.md](LIMITATION-PRESERVATION.md). P0/P1 source completion is in [P0-EVIDENCE-GAPS.md](P0-EVIDENCE-GAPS.md).

## Operating rule

Every material proposition should answer:

> **Who knew what, when, in what legal capacity; what did that actor subsequently do; what incremental consequence followed; in which proceeding is it relevant; and what source proves each step?**

A statement that cannot answer those questions remains an allegation, inference or evidence gap—not a finding.

## Evidence classifications

- `verified_primary`
- `verified_official`
- `documented_party_statement`
- `corroborated_inference`
- `contested`
- `missing_primary`
- `unknown`

Publication controls:

- `public_safe`
- `internal_only`
- `privilege_review`
- `do_not_publish`

The machine-readable registers are in [`data/`](data/). Run `python research/lender-of-record-liability/validate.py` from the repository root before merge or publication.

## Three visibility levels

1. **Canonical evidence/research:** complete, adverse material included, source and contradiction controlled.
2. **Legal work product:** element-by-element theories, temporal law, limitation and remedy analysis; counsel/privilege review required.
3. **Public pages:** only verified or carefully attributed propositions, with adverse decisions and missing evidence displayed.

The public page is a controlled view. It is not the source of truth.

## Immediate P0 focus

1. Bankia/originating-lender → SAREB instrument and schedule.
2. SAREB → PH122 loans sale and purchase agreement, asset schedule and allocated price.
3. Haya servicing agreement, powers, delegation and committee records.
4. Complete PH122 → CAM deed, schedules, payment, due diligence and warranties.
5. CAM → HNT segregation project, deed, balance and passive/liability schedules.
6. End-to-end debt, payment, cost, satisfaction and surplus ledger.

## Legal and publication limits

This dossier does not declare fraud, collusion, bad faith, criminal responsibility, unlawful appropriation or an automatic group-wide liability. It does not treat “lender of record” as a freestanding Spanish cause of action. It is a forensic organising label for testing distinct Spanish-law routes actor by actor.
