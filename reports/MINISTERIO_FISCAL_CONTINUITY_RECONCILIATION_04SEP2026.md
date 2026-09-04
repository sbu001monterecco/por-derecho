# MINISTERIO FISCAL CONTINUITY RECONCILIATION — 4 SEPTEMBER 2026

**Control:** `PD-MF-CONTINUITY-20260904-02`  
**Repository:** `sbu001monterecco/por-derecho`  
**Base main:** `b8ded173b06f17aaf91569f051dd11e621b139ae`  
**Method:** criminal/prosecutorial-first reconstruction, with formal-filing, email, response and proceeding identities kept separate.  
**Boundary:** registration, delivery, acknowledgement, archive or routing are institutional acts; none of them proves the merits or truth of the underlying criminal allegations.

## 1. Why this reconciliation is necessary

The repository already contains a high-quality RedSARA source register, but the `75`-registration figure is a **bounded source denominator**, not the total historical Ministerio Fiscal corpus. The detailed 154-page Anexo 4 establishes 75 distinct REGAGE records for its source window, with 125 attachment SHA-512 records and 15 registrations without a hashed attachment. Later formal filings, later prosecutor-side email traffic, incoming responses and drafts/self-archive copies must not be added together as though they were one homogeneous count.

The controlling model is therefore layered:

1. formal RedSARA/AGE filings;
2. later formal-registration delta;
3. outgoing SENT email events;
4. incoming prosecution-side acknowledgements/decrees/responses;
5. DRAFT items, excluded from delivery counts;
6. SELF_ARCHIVE provenance, excluded from delivery counts;
7. exact proceeding identity and operative effect.

This preserves the criminal-first unitary theory without turning interconnected evidence into a single procedural file.

## 2. Formal denominator ladder

### 2.1 Detailed Anexo 4 baseline

The existing source-controlled Anexo 4 layer remains the best detailed baseline:

- 75 distinct REGAGE registrations;
- 125 attachment SHA-512 records;
- 15 registrations without hashed attachment;
- source annex SHA-512 `0e86b7af202e25f2a983d95d2a1fc12c1cd0567ad4ab18ace0d5b8e1fec85c0d73f1370454d1537de53530fdfa8825152f157678d9a89a55f228b5c06faac7b9`.

This is a verified denominator for the source annex. It is **not** labelled as the all-time count of Ministerio Fiscal submissions.

### 2.2 March–21 June continuity checkpoint

A later registry-export continuity checkpoint records a further 22 entries after the Anexo 4 window, producing a historical checkpoint of 97 registrations through 21 June 2026 (90 received / 7 rejected in that export). This checkpoint remains subject to final source-by-source reconciliation and must not be mechanically combined with Gmail events.

### 2.3 Post-June formal layer

The post-June denominator remains open. The present continuity ledger preserves eight known August checkpoint identifiers without asserting completeness:

`REGAGE26e00070234288`, `REGAGE26e00070235399`, `REGAGE26e00070235775`, `REGAGE26e00070236067`, `REGAGE26e00070236245`, `REGAGE26e00070236543`, `REGAGE26e00070236749`, `REGAGE26e00070237051`.

The next denominator must be built by exact receipt and status, not by subject-line similarity.

## 3. Gmail continuity: raw candidates are not substantive-event counts

A targeted SENT slice across selected prosecution offices for 20–27 August 2026 returned 17 raw candidates. That number is **not** a unique-event count. In the DI 22/2026 sequence, closely repeated sends were followed by a controlling-version clarification stating that a second copy had been transmitted by operational sending error. The correct unit is therefore the controlled package/event, not the raw email row.

A targeted incoming slice from prosecution-side domains from 20 August onward produced at least nine prosecution-side response candidates after excluding TSJC/court correspondence. That is also not a final all-time denominator. Each incoming item must be classified by:

- organ;
- exact proceeding/reference;
- date/time;
- source package;
- acknowledgement / decree / request / substantive response / routing / other effect;
- whether it creates a new procedural fact or only confirms handling.

DRAFT and SELF_ARCHIVE copies remain excluded from sent/received denominators.

## 4. E.G. 745/2026 — exact source parity confirmed

A fresh byte-and-page audit was performed on the connected official attachment `OFICIO Y DECRETO EXP. 745-26.pdf` before any new publication was made.

**Verified native source:**

- organ: Inspección Fiscal, Fiscalía General del Estado;
- reference: E.G. 745/2026;
- pages: 3;
- bytes: 1,111,997;
- SHA-256: `1e09c8eb3bce26e28dc5f22e5d6ebad3f458212cf8d85f5920e869fa42554abe`;
- SHA-512: `e31f92fcf4462aa79d963e62d20b5afb7d84820785daeb823eb313c24c356a40d9846498ed770bb39368bfdfba07dda6214827b85f32a316d0bfbf843cff8196`;
- associated Inspection registration already recorded publicly: `REGAGE26e00070235775`.

The SHA-256 and file size **match the existing NAT-FIS-004 public source control exactly**. The existing bilingual E.G. 745/2026 dossier is therefore the correct route for this connected attachment; no duplicate proceeding identity is created.

### 4.1 What the three pages establish

Page 1 is an Inspección Fiscal notification dated 26 August 2026 attaching the decree for E.G. 745/2026. Page 2 states that an email entered Inspección Fiscal on 3 August, reproduces the request for an independent inspection review of post-knowledge conduct by the Fiscalía Provincial de Las Palmas, characterises the filing as confused/incoherent, cites article 66.1(c) of Law 39/2015 and says no concrete irregularity attributable to a particular prosecutor in a particular matter was specified. It then orders archive of the governmental file and notification. Page 3 states the optional reconsideration and direct contentious-administrative review routes and the periods stated in the decree.

Those are source facts. Whether the originating filing was in fact sufficiently concrete, whether cure/subsanación should have been offered, and whether any review route succeeds are separate legal/evidential questions. The decree does not prove or disprove the wider allegations on their merits.

### 4.2 Correction control

A provisional working interpretation suggesting a second `745/2026` source was **not carried forward**. Direct re-hashing of the mounted connected attachment plus visual inspection of all three rendered pages confirmed exact parity with the existing public source fingerprint. The repository must therefore preserve one E.G. 745/2026 / NAT-FIS-004 identity for this document unless a genuinely different certified source is later produced.

This is the continuity rule in practice: a suspicious-looking metadata discrepancy is not promoted into a new proceeding or contradiction until the actual bytes and pages have been checked.

## 5. Criminal-first but procedurally non-fragmented

The Ministerio Fiscal control plane should be read as one evidence graph with separate procedural nodes. At minimum, E.G. 745/2026 / NAT-FIS-004, DI 22/2026, EG 112/2026 and Exp. Gub. 86/2026 remain distinct tracks even when they concern overlapping Sun Park facts or receive overlapping evidence packages.

For every bridge, the repository must answer:

`source → delivery channel → recipient organ → proceeding/reference → allocation or handling → act/omission → operative effect → later use → contrary explanation → open proof`.

The criminal-first lane asks whether disputed authority, documents, professional/institutional powers, procedural instruments and patrimonial consequences were knowingly used in a way capable of criminal relevance. It does not transform every concursal, civil, disciplinary or administrative issue into crime. Those other routes remain downstream evidential/remedial outputs from the same source graph.

## 6. P0 closure programme for Ministerio Fiscal continuity

1. Reconcile every formal registration after 21 June against the 97-entry checkpoint and later receipts.
2. Deduplicate August SENT traffic by exact package, timestamp, recipient function and controlling-version message.
3. Classify each inbound prosecution-side response by organ, exact proceeding and operative effect.
4. Attach every event to the Master Proceedings Register; do not merge tracks by shared subject matter alone.
5. Preserve E.G. 745/2026 / NAT-FIS-004 exact-source parity and its archive/review state.
6. Maintain privacy minimisation: do not publish unnecessary personal email, address, phone, signature-certificate identifiers or other protected data from native official documents.
7. Add a bilingual public continuity route making the denominator ladder and channel distinctions explicit.
8. Continue the criminal-first unitary graph into the wider source/evidence matrix, but retain actor-specific and proceeding-specific proof gates.

## 7. Publication boundary

This reconciliation is repository and website maintenance only. It does not send an email, file a recurso, submit a RedSARA registration, contact an authority or alter the official status of any proceeding.
