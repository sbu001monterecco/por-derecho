# Correction register — CGPJ general Information delivery — 21 August 2026

**Status:** controlling source-status correction.  
**Correction date:** 21 August 2026.  
**Applies to:** the late-20-August CGPJ routing record and its bilingual public synthesis.

## 1. Corrected proposition

The earlier record described a three-email CGPJ sequence and correctly warned that sent did not mean received. A later primary delivery-status notice now permits a more precise statement:

> **Three outbound attempts were made on 20 August 2026. The Appeals Section and General Secretariat messages were sent and no delivery-failure notice was located in the connected mailbox as at this correction date; that does not prove receipt, association or examination. The general Information-channel attempt later generated a final delivery-failure notice stating that the address was not found or unable to receive mail and that the message was not delivered.**

The Information attempt must therefore not be described as a valid routing checkpoint or as a communication capable of having reached the CGPJ through that address.

## 2. Source chain

| Event | Public source reference | Time | Controlled status |
|---|---|---:|---|
| Appeals Section message | `CGPJ-DSP-20260820-01` | 20 Aug 2026, 22:34:59 UTC | Sent. No delivery-failure notice located. Receipt/association/examination not proved. |
| General Secretariat message | `CGPJ-DSP-20260820-02` | 20 Aug 2026, 22:36:49 UTC | Sent. No delivery-failure notice located. Receipt/association/examination not proved. |
| General Information attempt | `CGPJ-DSP-20260820-03` | 20 Aug 2026, 22:38:42 UTC | Sent from the private mailbox, but later superseded for delivery status by the final failure notice below. |
| Delivery Status Notification (Failure) | `CGPJ-DSP-20260820-03-FAIL` | 20 Aug 2026, 23:02:21 UTC / 21 Aug 2026, 00:02:21 BST | Address not found or unable to receive mail; message not delivered. |

The institutional recipient addresses and exact provider locators remain preserved in the controlled private-mailbox record. The public website does not need to reproduce them to explain the correction.

## 3. Permitted public wording

- “Three outbound attempts were made; one later failed delivery.”
- “The Appeals Section and General Secretariat messages were sent, but receipt, association and examination remain unproved.”
- “The general Information-channel attempt was not delivered and cannot be treated as an institutional routing checkpoint.”
- “No bounce is not proof of receipt.”

## 4. Prohibited or unsupported wording

- “All three CGPJ emails were delivered.”
- “The CGPJ received all three emails.”
- “The Appeals Section or General Secretariat joined or examined the messages.”
- “The delivery failure proves deliberate blocking, obstruction or misconduct.”
- “The failed Information address proves that no other CGPJ route exists.”

## 5. Supersession

This correction controls over any wording in:

- `archive/CGPJ_FISCALIA_ROUTING_CLOSEOUT_20AUG2026.md`, especially sections 6–8, insofar as the third attempt was presented as an effective routing checkpoint;
- `CURRENT_HANDOVER_CGPJ_FISCALIA_ROUTING_20AUG2026.md`;
- `/es/actualizacion-cgpj-fiscalia-20-agosto-2026/`;
- `/en/cgpj-public-prosecution-routing-update-20-august-2026/`.

The underlying substantive routing strategy is otherwise unchanged: criminal/economic-source questions remain separated from CGPJ-specific integrity, transmission and competence-classification controls.

## 6. Finite next controls

1. Seek acknowledgement or association only from the Appeals Section and General Secretariat routes actually sent without a located failure notice.
2. Identify a currently valid institutional Information or Inspection route only if additional routing is still necessary.
3. Do not resend to the failed address.
4. Re-query the connected mailbox before asserting receipt, silence or any later response.
