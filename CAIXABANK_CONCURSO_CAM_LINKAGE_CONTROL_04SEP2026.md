# CaixaBank Valencia ↔ Concurso 36/2012 ↔ CAM linkage control

Date: 2026-09-04
Status: PUBLISHED / MERGED TO MAIN + 04SEP2026 ACTOR DELTA PENDING MERGE
Publication PR: #1438
Merge commit: 6a6820cc05ff6ff72dc6b281da9b7d7d8ec2c21d
Public/private boundary: PUBLIC-SAFE framing only. No private litigation communications, privileged material or unsupported criminal conclusion is reproduced.

## Purpose

Add an evidence-led bridge to the canonical Spanish CaixaBank Valencia dossier explaining why the banking claim and defence must be reconciled with Concurso 36/2012, the Bankia → SAREB → PH122 → CAM credit chain, the disputed gatekeeping acts of the Administrador Concursal and the wider Acosta Matos perimeter.

## Canonical proceeding

- Aweswell Limited v CAIXABANK, S.A.
- Procedimiento Ordinario 1859/2023-9
- Juzgado de Primera Instancia nº 27 de Valencia
- N.I.G. 46250-42-1-2023-0049579
- Current hearing: 28 January 2027 at 10:00
- Pending and contested; no merits judgment is represented as having been issued.

## Documentary anchors already present in the repository

1. The CaixaBank Valencia dossier separates the upstream corporate/product route Caja Insular / BFA / Bankia → CaixaBank from the later asset route Bankia → SAREB → PH122 → CAM and requires a single economic reconciliation without collapsing legal capacities.
2. The dossier records that CaixaBank requested the testimony of Francisco de Borja Rodríguez-Batllori Laffitte, Administrador Concursal of Concurso 36/2012, and that Aweswell later adhered to that request.
3. The Administrador gatekeeper dossier records the Por Derecho allegation that, in PP 1041/2017, the AC terminated LPB counsel's mandate in the disclosure route concerning PH122 → CAM, after which a withdrawal was filed in LPB's name and CAM did not oppose it. The certified PP 1041 record remains P0.
4. The lender-chain responsibility dossier treats the current strongest case as actor-specific but connected credit → control → title conduct, not as automatic inherited liability.
5. The court bundle identifies **Asier Barañano Revuelta (ROAC 18046), PKF Attest**, as a direct CaixaBank-side expert actor: he signed the PKF Attest expert-engagement acceptance dated 24 January 2024 and co-signed the CaixaBank-side expert report dated 17 October 2024 with Zigor Bilbao.

## Confirmed expert actor — Asier Barañano Revuelta

**Actor status:** CONFIRMED / DIRECT LITIGATION ROLE / CAIXABANK-SIDE EXPERT.

- Canonical name: **Asier Barañano Revuelta**.
- Search aliases: Asier Baraño Revuelta; Asier Baranano Revuelta.
- ROAC: **18046**.
- Firm: **PKF Attest**.
- Professional public role: partner in audit / auditor.
- 24 Jan 2024: signed PKF Attest acceptance of the expert engagement for PO 1859/2023.
- 17 Oct 2024: co-signed the CaixaBank-side expert report with **Zigor Bilbao**.

### Registered graph edges

- `ASIER BARAÑANO REVUELTA → PKF ATTEST` — professional affiliation — **CONFIRMED**.
- `PKF ATTEST → CAIXABANK / PO 1859/2023` — party expert engagement — **CONFIRMED**.
- `ASIER BARAÑANO REVUELTA → CAIXABANK / PO 1859/2023` — signed acceptance + co-signed expert report — **CONFIRMED**.
- `ASIER BARAÑANO REVUELTA ↔ ZIGOR BILBAO` — co-signatories / co-responsible professionals — **CONFIRMED**.

### Control boundary

The expert role does **not** establish that Barañano was an employee/officer of CaixaBank or Bankia, participated in the underlying 2008–2010 lending/product decisions, had any role in Bankia → SAREB → PH122 → CAM, or had any connection to CAM, RICPE, Cerberus/Promontoria or the Administrador Concursal. Those links remain unproven unless primary evidence establishes them.

A separate private evidence trail records a 2022 firm-level Project Sun Rock contact with PKF Attest. That material is preserved as a conflict/independence-check lead and is **not reproduced publicly**. It does not establish that Barañano personally knew of the prior contact or that any conflict, lack of objectivity or misconduct occurred.

Full DD control: `ASIER_BARANANO_REVUELTA_CAIXABANK_DD_04SEP2026.md`.

## Publication thesis

The published section states that the existing record supports:

- an objectively adverse alignment of acts and outcomes;
- a concrete evidentiary nexus sufficient to investigate whether conduct was independent or consciously complementary; and
- a need to analyse knowledge, communication, instruction, decision, benefit and causation across the three connected nodes.

It does NOT state collusion, conspiracy, concert, fraud, false documentation, unfair administration, procedural fraud or criminal responsibility as established fact.

## Civil / insolvency layer

The section identifies potential relevance to:

- nullity, restitution, damages, causation and quantum in Valencia;
- reconciliation of the real balance entering and leaving Concurso 36/2012;
- possible estate damage from proven unlawful or insufficiently diligent acts/omissions;
- possible unjustified benefit or over-recovery if proven by the complete ledger; and
- actor-specific allocation of incremental damage and retained/transmitted obligations.

## Criminal layer — conditional only

The section states that criminal relevance arises only if primary evidence proves the elements of a specific offence for the relevant date and actor, including as applicable intentional deception, conscious use/manipulation of materially false documentation, deliberate concealment of determinant information, knowing excess in administration of another's assets, procedural fraud, or conscious participation in an unlawful patrimonial result.

Coincident interests, adverse litigation positions, membership in a corporate chain and judicially authorised acts are not treated as criminal proof by themselves.

## P0 production needed to move from alignment to coordination

1. Certified PP 1041/2017 file, including withdrawal, authority, instructions, signature, metadata, communications, ratification and estate-interest analysis.
2. CaixaBank request/designation of Borja as witness, exact object of testimony, procedural communications and non-privileged documentary preparation trail.
3. Full Bankia → SAREB → PH122 → CAM instruments, balances, payments, guarantees, price, due diligence, servicing and instructions.
4. AC ↔ CAM / creditor-perimeter communications, verification, valuation, alternatives, control, implementation and final accounts.
5. One reproducible economic ledger from principal and swap through execution, concurso, assignments, dación/adjudication and final recovery, without double counting.
6. PKF Attest / Barañano expert chain: original/certified 24 Jan 2024 acceptance; 17 Oct 2024 report and annexes; precise instructions; source corpus supplied to the experts; reproducible calculations; authorship/work allocation; and, where legally obtainable, relevant conflict/independence acceptance records.

## Implementation

- Existing module: `assets/caixabank-valencia-concurso-cam-linkage-20260904.js`
- Actor DD: `ASIER_BARANANO_REVUELTA_CAIXABANK_DD_04SEP2026.md`
- Loader: `assets/site.js`
- Mount point: immediately after `#caixabank-borja-witness-control`
- Public route affected: `/es/reclamacion-caixabank-valencia/`
- Excluded route: `/es/reclamacion-caixabank-valencia/senalamiento-28-enero-2027/`

## Defence / innocent explanation preserved

The section expressly preserves the alternative explanation that CaixaBank selected the AC solely for institutional knowledge; that the AC acted within lawful powers, judicial supervision and estate interests; that CAM acquired and exercised a credit through legally authorised mechanisms; and that PKF Attest/Barañano performed the expert engagement professionally and objectively on the material supplied. Those explanations are to be tested against the contemporary records rather than presumed true or false.
