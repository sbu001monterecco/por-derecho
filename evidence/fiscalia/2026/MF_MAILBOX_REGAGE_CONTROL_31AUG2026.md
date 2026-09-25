# Ministerio Fiscal mailbox / REG-AGE control baseline — 31 August 2026

**Control date:** 31 August 2026

**Window:** 1 January 2018–31 August 2026; pagination-complete rescan of 1–31 August 2026

**Purpose:** reconcile official notices and decisions, user-originated communications, formal registration proof and repository registration without promoting one proof class into another.

## 1. Controlling result

The defined Gmail search was completed across the exact institutional mailboxes and office-name/reference variants for Arrecife–Puerto del Rosario, Fiscalía Provincial de Las Palmas, Fiscalía de la Comunidad Autónoma de Canarias/Fiscal Superior, Fiscalía Provincial de Santa Cruz de Tenerife, Fiscalía General del Estado, Fiscalía Anticorrupción, Fiscalía de la Audiencia Nacional and Inspección Fiscal. The reference search covered the located DI, DIP, EG, DP and ST numbers and REG-AGE identifiers. Drafts, duplicates, corrections, incoming notices and formal receipts were separated.

The result is bounded to the searchable account and queries available on the control date. It does not prove that an unlocated message never existed, that a message was read, that an internal transfer occurred or that an institution considered the merits.

**Implementation closeout (31 August 2026):** the repository now contains the complete public-safe registration of every row in the fixed private locator snapshot:

- `assets/data/institutional-communications-mailbox-index-v1.json` independently rows all **156** located Gmail events: 42 outbound, 101 inbound, 10 self-archive controls and 3 unsent drafts; 81 routes remain expressly unclassified rather than guessed;
- `assets/data/institutional-communications-register-v1.json` contains **296** linked rows: 75 baseline receipts, 156 transport events and 65 separately registered receipts/acts/notices/correspondence events;
- DI 22/2026 has 11 act rows, including two acts on 11 February and two on 13 February, linked to eight notice transports;
- the August family has seven distinct REG-AGE receipt rows; six one-to-one public destination-label mappings remain a declared normalization gate; and
- private native locators are durably controlled under opaque custody reference `PD-SP-CUST-0001` (231 rows; aggregate SHA-256 `bdd12a8fa62b5058525e1c37053fb7899ac24a60d12ff48ab8b74bda617cd6f6`; provider/storage identifiers withheld).

The expression **75/97 is not complete independent REG-AGE registration**. It must not be used to imply that all 97 reported registration records have individual source rows. This separate gap does not alter the completed 156/156 mailbox-event denominator.

Exact Gmail locators, mailbox addresses, private subject lines and native attachment names are held in the controlled record **outside public Git**. They are deliberately omitted here. This public baseline identifies only the minimum office, date, expediente, act and proof level needed for continuity.

## 2. Proof-state key

| Label | Meaning |
|---|---|
| **SIGNED ACT LOCATED** | An official decision bearing an electronic-signature or signed-act control was read. |
| **OFFICIAL NOTICE + ACT LOCATED** | An incoming official notice and its decision attachment were located; a scan may still require native-text/signature verification. |
| **REG-AGE PRESENTED** | A receipt proves presentation time, destination code, stated object, attachment count/name and hash where printed. It does not prove admission or merits treatment. |
| **OFFICIAL ACKNOWLEDGEMENT** | An office acknowledged receipt or prospective handling. It does not prove formal filing, allocation or merits review. |
| **SOURCE REQUIRED** | A reference is known, but the particular act, complete file, routing record or later decision remains unlocated. |

## 3. Verified Provincial decisions — DI 113/2022 and DI 22/2026

### DI 113/2022

| Act date | Official event | Proof level | Repository reconciliation |
|---|---|---|---|
| 8 Feb 2023 | Signed archive decision, NIG `3501670220220003722`. The act records the complaint's relationship to earlier Arrecife proceedings and gives the official reasons for archive. | **SIGNED ACT LOCATED**, delivered in an official notice bundle on 25 Feb 2026 | Corrected to primary-source verified in the proceedings layer and separately event-registered. |
| 23–25 Feb 2026 | Decision and notice on the request for information/copies; the office supplied the archive act and stated its position on the remaining requested material. | **OFFICIAL NOTICE + SIGNED ACT LOCATED** | Access decision and notice are separate linked rows; neither is collapsed into the historic archive act or earlier filing. |

### DI 22/2026

| Act / notice date | Official event located | Proof level | Repository reconciliation |
|---|---|---|---|
| 11 Feb 2026 | Initial opening-and-archive decision; a second decision joined a further filing and maintained archive. | **SIGNED ACT LOCATED** | Two distinct signed acts are separately event-registered and remain linked to one expediente identity. |
| 13 Feb 2026 | Decision joining an Anticorrupción remission and maintaining archive. | **SIGNED ACT LOCATED** | Separately event-registered. |
| 13 Feb 2026 | Separate decision joining additional material linked to other prosecutorial routes and maintaining archive. | **SIGNED ACT LOCATED** | Separately event-registered; not merged with the other 13-Feb act. |
| 16 Feb; notified 18 Feb 2026 | Decision joining further submissions and maintaining archive. The face of the act contains an apparent year typo that should be preserved as source text, not silently corrected. | **SIGNED ACT LOCATED** | Decision is separately event-registered; the linked transport remains a distinct row. |
| 19 Feb 2026 | Decision refusing the requested certification/copies on the stated grounds. | **SIGNED ACT LOCATED** | Separately event-registered. |
| 2 Mar 2026 | Decision joining later Anticorrupción remissions and maintaining archive. | **SIGNED ACT LOCATED** | Separately event-registered. |
| 3 Mar 2026 | Decision joining the separately framed extraconcursal submission and maintaining archive. | **SIGNED ACT LOCATED** | Separately event-registered. |
| 3 Jun 2026 | Officially notified decision joining a further filing and maintaining the prior position. | **OFFICIAL NOTICE + ACT LOCATED** | Separately event-registered with office-only attribution; native signature metadata remains to be normalised. |
| 30 Jun; notified 2 Jul 2026 | Officially notified decision joining a further filing and an Anticorrupción remission, with no new diligence ordered. | **OFFICIAL NOTICE + ACT LOCATED** | Separately event-registered with office-only attribution; native signature metadata remains to be normalised. |
| 8 Jul; notified 10 Jul 2026 | Officially notified decision joining another Anticorrupción remission, with no new diligence ordered. | **OFFICIAL NOTICE + ACT LOCATED** | Separately event-registered with office-only attribution; native signature metadata remains to be normalised. |

These acts prove the decisions and their stated reasoning. They do not by themselves prove the completeness of the expediente, what internal work occurred, unlawful intent, coordination, obstruction, prevarication or criminality.

## 4. Other located expediente-level official events

| Date | Expediente / route | Located event and proof ceiling | Reconciliation state |
|---|---|---|---|
| 7 May 2019 | DI 248/2018 | Signed archive act is controlled in the repository; this mailbox pass found no earlier direct-mail event at the exact current office addresses. | **Independently row-registered** at expediente level; complete certified file and requested-versus-performed diligence matrix remain required. |
| 27 Jan 2025 | CC/CA 12/2025 | Official central citizen-attention correspondence located. The mailbox event is proved; no broader merits disposition is inferred. | **Reference and event independently registered;** merits outcome remains unproved. |
| 3 Mar 2025 | EG 33/2025 | Official notice with an inception/opening document located. | **Expediente and discrete events independently registered;** complete file and later disposition required. |
| 25 Jul–26 Sep 2025; 20 Aug 2026 | EG 352/2025 | Complaint transmission, official receipt/reference and later notice located. The 20-Aug response says admission remained pending a compliant electronic signature; it is not a merits rejection. | **Expediente and discrete transport/correspondence events independently registered;** the cure/admission state remains bounded by the source. |
| 14 Jan 2026 | DI preprocesal 114/2025 | Official notice and three-page scanned archive decision located; NIG `3501670220250003875`. | **Expediente and discrete events independently registered.** Native searchable/signature-verifiable copy remains desirable. |
| 27 Jan; notified 30 Jan 2026 | DIP 20/2026 | Official route records opening and remission from Tenerife to Fiscalía Provincial de Las Palmas. This is a routing act, not a merits determination. | **Expediente, official acts and transport independently registered.** Receiving-office association and treatment remain required. |
| 11 Feb 2026 | EG 6/2026 | Official notice located. The present mailbox control establishes correspondence provenance only; it does not add unreviewed merits content. | **Reference and notice events independently registered; source-level decision digest remains required.** |
| 6–9 Mar 2026 | DIP 2/2026 | Signed archive decision and official notice located; a later registered correction challenged an appeal-status premise. | **Expediente and discrete decision/notice/correction events independently registered;** separate opening act and post-correction treatment remain required. |
| 30 Mar 2026 | EG 44/2026 | Signed decision opened and archived the superior-office file on the stated competence grounds and recorded copies/routes to other offices. | **Expediente and discrete official events independently registered.** Receiving-office treatment remains required. |
| 3 and 8–9 Jun 2026 | EG 49/2026 | Two signed central decisions located; the second accumulated a renewed request and maintained the prior disposition. | **Expediente and both decisions independently event-registered;** linked transport remains separate. |
| 6 Jul 2026 | ST 553/2026 | Signed official acknowledgement located. | **Reference and discrete acknowledgement/transport events independently registered.** Acknowledgement is not merits review. |
| 12 Jul 2026 | DP 1901/2026 | Primary judicial order gave Fiscalía five days to report on admission. | **Independently row-registered** as a judicial route; the signed Fiscal report and later judicial act are **SOURCE REQUIRED**. |
| 10 Aug 2026 | Fiscalía AN, EG 86/2026 | Official notice, signed initiation/archive-for-competence decision, registered source package and filing receipt located. The act remits territorially to Arrecife; it is not a merits dismissal of the allegations. | **Decision/notice/filing/transport events independently registered.** Destination association/treatment remains open. |
| 19 Aug; clarified 23 Aug and notified 25 Aug 2026 | EG 112/2026 | Signed opening/archive decision and signed clarification located. The clarification recognises the historic aforado module but maintains closure because the later communications were not treated as a new judge-related criminal allegation; it gives a territorial route for other matters. | **Expediente, decisions and transport events independently registered.** Transfer and receiving-office treatment remain required. |
| 21 Aug 2026 | EG 95/2026 | Official Tenerife notice with an opening/archive decree attachment located. | **Expediente, decision and transport events independently registered.** Native text/signature normalisation remains required. |
| 26 Aug 2026 | E.G. 745/2026 | Official Inspección notice and archive decree located. | **Expediente, source filing, decision, notice and transport events independently registered.** Complete administrative file/index and routing record remain required. |

Additional official acknowledgements under ST 104/2025 were located on several dates in 2025. They prove central receipt/handling checkpoints only and are now independently event-registered. EG 58/2026 is referenced elsewhere in the corpus, but this pass did not locate and read a discrete official act sufficient to add a verified decision event; it remains **SOURCE REQUIRED** here and is preserved as an unresolved proceeding/reference candidate rather than a merits event.

## 5. August 2026 mailbox completion control

| Office route | Located August result | Proof boundary |
|---|---|---|
| Fiscalía Provincial de Las Palmas | User-originated communications on 20, 26 and 27 Aug; duplicate/correction chain separated. No official August reply located. | Sent email proves transmission through email only, not formal filing, allocation, association with DI 22 or merits review. |
| Fiscalía de Área de Arrecife–Puerto del Rosario | User-originated communications on 20, 26 and 27 Aug. No official August reply located. | No inference from silence; receiving expediente and treatment remain unproved. |
| Fiscalía de la Comunidad Autónoma de Canarias / Fiscal Superior | Official EG 112 decision and clarification located, together with the user response chain. | The decisions prove their stated classifications; they do not prove transfer or examination by the office named as territorially competent. |
| Fiscalía Provincial de Santa Cruz de Tenerife | Official EG 95 notice/decree located after the 20-Aug communication. | A notice/decision is not proof that every module or attachment was examined. |
| Fiscalía General del Estado / Secretaría Técnica | Four official acknowledgements to 20-Aug central communications located. | Central receipt and prospective handling only; no proof of internal transfer, association, allocation or merits review. |
| Fiscalía Anticorrupción | Official 20-Aug response located requiring a compliant electronic signature before admission. | Receipt acknowledged; admission and merits decision not proved. |
| Fiscalía de la Audiencia Nacional | Official 10-Aug EG 86 competence/remission package located. Later 20 and 26 Aug user communications located; no later official reply. | Routing to Arrecife is proved; receipt/association and merits treatment at destination are not. |
| Inspección Fiscal | Official E.G. 745 notice/decree located on 26 Aug. A 20-Aug Inspection-directed communication received a central FGE acknowledgement on 21 Aug. | Central acknowledgement does not prove transfer to Inspection or inclusion in the E.G. 745 decision corpus. |

No delivery-failure message was located for the controlling 20-Aug institutional dispatch. That absence does not convert the emails into registered filings. Draft messages were excluded from the sent denominator.

## 6. Seven-destination REG-AGE control of 2–3 August 2026

Seven primary receipts prove presentation of the same controlled attachment to the stated central, superior, territorial and specialist destination codes. The receipts preserve the attachment's common SHA-512 and the individual registration timestamps. They prove **REG-AGE presentation** only.

The family includes routes to FGE, an Inspection-directed central filing, Fiscalía Superior de Canarias, Anticorrupción, the Fiscal de Sala for Economic Crimes, Arrecife and Fiscalía Provincial de Las Palmas. For the Inspection-directed filing, the formal recipient code on the receipt is the central FGE code; internal transfer to Inspection is not proved by the receipt. The seven receipts are now separately registered in the append-only event layer; six one-to-one public destination-label mappings remain a declared normalization gate rather than a guessed association.

Automated processing confirmations do not establish admission, assignment, reading, joinder, preservation or a merits decision. Later bare REG-AGE notifications with no controlled destination/package bridge must remain unclassified and must not be silently attributed to Ministerio Fiscal.

## 7. E.G. 745/2026 filing-status lock

The 2-August underlying presentation and its attachment identity are proved. The 26-August E.G. 745 notice/decree is proved. The post-notification control located:

- no sent recurso potestativo de reposición;
- no matching REG-AGE receipt for a reposición;
- no equivalent official filing acknowledgement; and
- only repository drafts/prepared materials.

The controlling status is therefore:

> **REPOSICIÓN PREPARED / OUTSTANDING — NOT VERIFIED AS FILED**

A draft, an email, a public webpage or a link to an open letter does not change this status. It may change only when the exact filed bytes and a valid official receipt or equivalent filing proof are controlled.

## 8. Repository reconciliation — completed public-safe event layer

| Reconciliation class | Items presently in that class | What must happen next |
|---|---|---|
| **Independently row-registered** | Every one of the 231 fixed private-manifest source rows has a corresponding public-safe register row; located acts/notices/receipts are separate linked rows. | Advance only append-only, preserving stable IDs and transport/filing/act separation. |
| **Decomposed official layers** | DI 113, DI 22, DI 114, DIP 20, EG 33, EG 6, EG 44, EG 49, EG 86, EG 95, EG 112, E.G. 745, ST 104, ST 553, CC/CA 12 and the August receipt family have discrete source-proved rows at the available proof ceiling. | Complete the finite source/normalization gates; do not upgrade notice/receipt into merits review. |
| **Aggregate-only** | Only the separately reported 22 later RedSARA/AGE records remain aggregate-only because their individual receipt/status source table is not controlled. | Recover the individual official export before creating rows. |
| **Source-required** | EG 58/2026 discrete official act; complete files/indices for the named expedientes; DP 1901 Fiscal report and later order; receiving-office proof after remissions; internal routing/association records; post-correction treatment; any E.G. 745 reposición receipt. | Obtain the finite primary source before changing status. Absence, silence or an unexposed route is not proof of non-existence or wrongdoing. |

The durable solution is implemented as linked layers: one canonical row per expediente/reference, a 296-row append-only communications register, the 156-row public mailbox index, the 75-row detailed receipt baseline, the ten-row supplied source-artifact register, the overlap checkpoint and the 231-row private custody manifest. The validator rejects `FILED` unless formal receipt or equivalent proof is linked and rejects synthetic decomposition of the 22 aggregate-only records. Future passes start at the checkpoint's seven-day overlap and scan forward, avoiding another unbounded reconstruction unless scope or pagination changes.

## 9. Non-inference boundary

Repeated institutional contact, repeated adverse outcomes, silence, routing gaps, aggregate joinder and an institutionally protective practical effect are not, without additional evidence, proof of coordination, capture, obstruction, prevarication, bad faith or criminality. Any such proposition requires actor-specific proof of duty and competence, the act or omission, access and knowledge, the legally required mental element, causation where relevant, and testing of contrary explanations against the complete file.
