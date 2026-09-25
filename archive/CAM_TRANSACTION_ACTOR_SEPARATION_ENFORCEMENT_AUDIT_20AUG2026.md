# CAM TRANSACTION ACTOR-SEPARATION — ENFORCEMENT AUDIT

**Run date:** 20 August 2026  
**Branch:** `evidence/cam-actor-separation-rule-enforcement-20aug2026`  
**Status:** `RULE ACTIVATED / SOURCE-GAP CLOSURE RUN / PUBLIC-WORDING REVIEW PENDING ONLY WHERE INDEXABLE`

## 1. User instruction executed

The controlling rule has been promoted into a dedicated retrieval gate:

`archive/CAM_TRANSACTION_ACTOR_SEPARATION_RETRIEVAL_GATE_20AUG2026.md`

Rule:

> **CAM REQUEST / POSITION → AC RECOMMENDATION OR IMPLEMENTATION → JUDGE DECISION OR PROVED OMISSION → CONSEQUENCE**

LAJ / oficina judicial, Registry and notarial acts are independent nodes whenever they occur.

No later approval/deed is treated as automatically retroactively curing an earlier act already refused convalidation.

## 2. Existing canonical transaction controls preserved

The run builds on, and does not replace:

- `archive/CAM_OFFER_TO_TRANSFER_MASTER_RECONSTRUCTION_20AUG2026.md`
- `archive/CAM_JUDICIAL_APPROVAL_SUPERVISION_REGISTER_20AUG2026.md`
- `archive/CAM_2022_DACION_PRIMARY_SOURCE_ADDENDUM_20AUG2026.md`
- `archive/CAM_TRANSACTION_DELETION_CLOSEOUT_20AUG2026.md`

Earlier PR #571 remains controlling for the first full CAM transaction reconstruction; PR #573 closed its deletion-continuity state.

## 3. Repository wording scan

Repository code-search passes were run for literal/near-literal actor-collapsing and convalidation wording, including:

- `"the court/AC"`
- `28-Nov-2018 12-Dec-2018 convalidation ob rem`
- `convalidación`

The current GitHub code-search connector returned no useful historical prose hits.

**Limitation:** this is not proof that no older shorthand exists. Search indexing in this repository is incomplete/lagging for recently merged archive content. Therefore this run does not use a zero-result search as a negative evidential finding. The new retrieval gate and source addendum control over older shorthand where inconsistent.

## 4. P1 source gaps closed during this run

The following primary sources were recovered/read and separately controlled in:

`archive/CAM_OCT2018_MAR2019_PROCEDURAL_ROUTING_SOURCE_ADDENDUM_20AUG2026.md`

### 4.1 15-Jun-2018 LAJ publicity / better-offer Diligencia — CLOSED

- `10. Diligencia Notificación Liquidación 15JUN2018.pdf`
- Gmail `167c817fdf0b45e0`
- SHA-256 `1298d03daca48284de642299ddb86c6b8ed2900f95d5ce05edf2d491e5f8ade5`

Verified LAJ Águeda Reyes Almeida publication act for both transaction limbs, 10-day better-bid period and licitación if a better bid appeared.

**Effect on actor map:** judicial Autos → separate LAJ implementation/publicity act.

### 4.2 17-Oct-2018 AC testimony request — CLOSED

- `0.20181017 Solicitud TESTIMONIO Concursal.pdf`
- Gmail `19fa84e0224689b7`
- SHA-256 `fec8710b0ffaea1b4fc57f07a2cf35cd3a6d9c0c444fd0f59a2ff8f98b174aa2`

Verified AC request for testimony of 16-Apr and 26-Jun Autos.

### 4.3 22-Oct-2018 LAJ testimony-delivery Diligencia — CLOSED

- `0.20181022 DIOR Entrega TESTIMONIO AC.pdf`
- Gmail `19fa84e0224689b7`
- SHA-256 `555ea16fd4ff3457632a4cee27a5309cf5c5fcb5f5f67b190bc3576a98ade839`

Verified LAJ order delivering the requested testimonies to the AC.

**Effect on actor map:** AC request → LAJ delivery. This is not a Judge authorisation of the later deed.

### 4.4 21-Nov-2018 AC opposition to CAM reposición — CLOSED

- `Impugnación AC del Recurso de Reposición de CAM (21NOV2018).pdf`
- Gmail `167c817fdf0b45e0`
- SHA-256 `1f99db307e6f94589ddefc7b84567be3f0aaa4700544265a4baca782c6c74229`

Verified that the AC opposed CAM on the separate insufficient-mass/reposición issue and expressly stated the 16-Apr Plan Auto was not final because appealed.

**Effect on actor map / counterevidence:** CAM and AC cannot be modelled as one undifferentiated procedural actor at all times. The source preserves a real procedural conflict while leaving later transaction convergence to be analysed separately.

### 4.5 12-Dec-2018 LAJ preclusion/formalisation Diligencia — CLOSED

- `Diligencia Preclusión Plazo Venta Locales-Piscinas (12DIC2018).pdf`
- Gmail `167c817fdf0b45e0`
- SHA-256 `50d45281df7b432bd1ee2b3c655a5a60057321506eb906988a39b71602f66fdc`

Verified that LAJ Águeda Reyes Almeida declared the 10-day period precluded and directed the AC to formalise the locals/pools sale.

### Critical chronology correction

The AC had already executed the notarial locals/pools deed on **28-Nov-2018**.

Therefore:

> **28-Nov AC deed → 12-Dec LAJ formalisation direction**

not:

> ~~12-Dec LAJ prior authorisation → 28-Nov deed~~

The 12-Dec act cannot chronologically constitute prior authority for an act already done.

This chronology fact is consistent with the need for later convalidation analysis; it does not by itself establish criminality or final invalidity.

### 4.6 10-Jan-2019 LAJ admission of challenges — CLOSED

- `Adjunto1(30).pdf`
- Gmail `16852afcf702f59e`
- SHA-256 `54e17b0b435aee59d92f38f89c1e23830505b45de67bb841a6463328023819d0`

Verified:

- LPB and Aweswell reposiciones against the 12-Dec Diligencia admitted;
- five-day opposition period opened;
- Aweswell nullity request sent to Judge;
- AC quarterly report at 20-Dec-2018 made available;
- AC extension request sent to Judge.

**Effect:** 12-Dec was promptly contested; do not describe it as an uncontested final validation.

### 4.7 1-Feb-2019 party filing — classified, not promoted

- `0.20190201 Solicitud Poliza AC.pdf`
- Gmail `19fa84e0224689b7`
- SHA-256 `68a848bef014cb0c24872aef0f7f43740ed703dbba1a6cb1d6b2d347c6f3cf83`

Classification: **PARTY PLEADING**.

It quotes sale/accounting statements attributed to the AC's quarterly report, including €400,000 and use of part of proceeds for AC fees. Those quoted AC statements remain derivative until the native quarterly report is recovered.

### 4.8 11-Mar-2019 LAJ routing Diligencia — CLOSED

- `0.20190311 DIOR Testimonios Fiscalia Comision Delitos AC.pdf`
- Gmail `19fa84e0224689b7`
- SHA-256 `7931215df22c25a75de30bbabbdddc64a6f12f2c140576fe4bdce399806cfd53`

Verified that liquidation challenges, Fiscalía-testimony request and further AC/opposing filings were procedurally routed to the Judge / left for resolution.

**Knowledge control:** routing to the Judge proves procedural placement, not personal adoption of allegations or a merits conclusion.

## 5. Refined controlling chronology after enforcement

`15-Jan CAM offer → 9-Feb AC Plan/endorsement → 16-Apr Judge approval + separate interest act → 4-Jun Judge bidder mechanics → 15-Jun LAJ publicity/better-offer implementation → 26-Jun Judge apartment-realisation suspension → 17-Oct AC asks for testimonies → 22-Oct LAJ orders delivery → 24-Oct CAM burofax pressure [native still missing] → 21-Nov AC opposes CAM on separate reposición issue → 28-Nov AC executes locals/pools deed → 12-Dec LAJ later declares preclusion and directs formalisation → 10-Jan LAJ admits LPB/Aweswell challenges and routes nullity to Judge → 9-Jan Registry qualification/date family to reconcile precisely with notification/custody → 1-Feb party liability/sale challenge → 11-Mar LAJ routes challenges/Fiscalía request to Judge → 20-Mar AC seeks convalidation → 24-Oct-2019 Judge refuses convalidation → 2021 re-tender/licitation/approval chain → 21-Feb-2022 apartment dación → downstream title/accounting/cure still open.`

### Date-order note

The Registry qualification is currently controlled as dated 9-Jan-2019. The 10-Jan LAJ Diligencia follows it chronologically by one day; transmission/receipt dates should be mapped before asserting who had the Registry qualification at each exact procedural moment.

## 6. Strongest evidential consequence of the rule

The strongest current presentation is not `the court/AC sold the locals`.

It is:

> **The Judge approved a conditioned disposal architecture; the LAJ implemented the publicity mechanics; the Judge later suspended the mortgaged-apartment limb; the AC obtained testimonies of the judicial acts; CAM then pressed for execution; the AC executed the locals/pools deed on 28-Nov-2018; the LAJ's preclusion/formalisation Diligencia came only on 12-Dec, after the deed; LPB/Aweswell promptly challenged that Diligencia; the Registry identified an `ob rem` obstacle; the AC sought convalidation; and the Judge later refused convalidation.**

This is stronger because it is actor-specific and preserves the judicial/LAJ acts that cut both for and against the competing theories.

## 7. What the run does NOT establish

The enforcement run does not establish, merely from these sources:

- collusion;
- prevaricación;
- estafa procesal;
- fraud by CAM/AC/Judge/LAJ;
- personal knowledge of every underlying fact by the Judge;
- that the 12-Dec LAJ act was itself unlawful;
- that the entire Plan was suspended rather than the exact scope of the 26-Jun act;
- that the €400,000 was misapplied;
- that later 2021/2022 acts did or did not cure every earlier consequence.

Those require separate elements/sources.

## 8. P1 queue after enforcement

Highest priority remaining:

1. native **24-Oct-2018 CAM burofax**;
2. exact publication evidence and last-publication date underlying 12-Dec computation;
3. complete LPB/Aweswell reposiciones against 12-Dec and all oppositions;
4. the judicial/LAJ resolution chain disposing of those reposiciones/nullity, reconciled with 24-Oct-2019 refusal;
5. native AC fourth / 20-Dec-2018 quarterly liquidation report;
6. standalone Registry qualification + filing/notification/receipt chronology;
7. €400,000 bank receipt + estate ledger + exact application/refund/recredit history;
8. post-24-Oct-2019 title/possession/accounting corrective acts;
9. 2021 bidder disclosure/inspection/data-room parity;
10. complete 15-Oct-2021 and January-2022 act families;
11. 21-Feb-2022 post-closing court/Registry filings and cancellations;
12. independent final mortgage-cap/debt/`sobrante` calculation.

## 9. Public website propagation decision

No public page is changed automatically by this enforcement run.

Reason: the new chronology materially improves evidential precision, but publication should be propagated only where a current public page contains wording that is demonstrably inaccurate or where a dedicated evidence-led update is strategically justified. The repository search connector did not reliably surface historical page prose in this pass.

Future public wording must apply the retrieval gate and source addendum.

## 10. Root bootstrap status

The mandatory rule is now a dedicated canonical retrieval gate. A future root-bootstrap maintenance pass should add an explicit `CHATGPT_START_HERE.md` pointer to that gate when the full-file editing path is safely available. Until then the gate itself is canonical and is cross-linked from this enforcement audit and the parallel deletion audit.

This is an implementation limitation, not a source/evidence gap.
