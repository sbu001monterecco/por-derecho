# RICPE — email confirmation and signed-file provenance

**Control date:** 17 August 2026  
**Institutional event:** RICPE Ethical Channel filing  
**Status:** `FILED/SUBMITTED + PLATFORM EMAIL CONFIRMATION`  
**Privacy:** communication access credentials, verification codes, NIE and private mail content not needed for provenance are excluded from this public record.

## 1. Native platform-confirmation email

A Gmail scan of the connected mailbox recovered a native incoming email from the RICPE Ethical Channel platform:

- **Sender:** `noreply@ithikios.com`;
- **Subject:** `Recepción nueva comunicación`;
- **Timestamp:** 17 August 2026, 22:51:17 UTC;
- **Recipient:** Gil Marer's controlled mailbox;
- **Attachment:** none.

The message states in substance:

> “Gracias por usar nuestro canal. Su comunicación ha sido comunicada y en breve recibirá información.”

It also states that a communication code has been assigned and that the status may be consulted through the RICPE Ethical Channel status portal.

### Evidential meaning

This email independently corroborates the final on-screen confirmation already supplied by Gil Marer. Together they establish:

- a communication was submitted through the RICPE Ethical Channel;
- the platform acknowledged it;
- a communication code was assigned;
- a follow-up route exists.

They do **not** establish substantive admission, opening or scope of investigation, conflict-screening result, preservation measures, Board treatment, merits acceptance, referral to CNMV or another authority, or remedy.

The communication code and secret key are deliberately excluded from this public repository record. They remain in Gil Marer's private credential records.

## 2. Signed PDF recovered from the contemporaneous Gmail chain

The Gmail scan also recovered a self-addressed message created before the channel confirmation and carrying the signed communication as an attachment:

- **Subject:** `Re: Revisión final completada - RIC PE`;
- **Timestamp:** 17 August 2026, approximately 22:27:58 UTC in the Gmail record;
- **Attachment filename:** `01_RICPE_Comunicacion_Unica_Consejo_17AGO2026_FINAL_FIRMADA.pdf`;
- **MIME:** `application/pdf`;
- **File size:** `447975` bytes;
- **SHA-256:** `b455075ceda7841471ef5f4ebfbb784ccd00357439aa8bf282e736fe4757832c`;
- **Pages:** `22`;
- **Page size:** A4;
- **Encrypted:** no.

### Digital-signature validation

Local PDF signature inspection records:

- one detached PKCS#7 signature;
- signer certificate identifies **Gil Marer**; personal identifier in the certificate is not reproduced here;
- signing time: **17 August 2026, 22:24:15 UTC**;
- signing hash algorithm: SHA-256;
- the total PDF is covered by the signed byte ranges;
- **cryptographic signature validation: valid**;
- the local validator could not complete certificate-chain validation because the issuing certificate was not available in its trust store (`issuer unknown`).

This distinction must be preserved: signature-integrity validation succeeded; trust-chain validation was not independently completed in this local environment.

## 3. Material variance from the earlier controlled pre-signature PDF

The earlier repository-controlled pre-signature Final V6 object was:

`01_RICPE_Comunicacion_Unica_Consejo_17AGO2026_FINAL_V6_PARA_FIRMA.pdf`

with:

- 21 pages;
- SHA-256 `b09c8754be21fe618b815f09d87c6ebbb569db53854b03d67c8ad72e020665f6`.

The signed PDF recovered from Gmail is **not merely the 21-page PDF plus a cryptographic signature container**. It is 22 pages and text comparison shows substantive editorial differences in addition to repagination and line wrapping. Examples include changes in the formulation of the LPB concursal-perimeter paragraph, Community/FMMM descriptions, the 2017–2018 chronology and additional Board questions.

Therefore:

1. the 21-page pre-signature V6 remains the controlled drafting baseline;
2. the 22-page signed PDF is a later signed object and must be treated as a distinct version;
3. because the Ethical Channel confirmation email does not expose attachment metadata or a file hash, **byte-identical proof that this 22-page signed PDF was the attachment uploaded to the channel remains open**;
4. the temporal sequence — signed PDF at approximately 22:24/22:27 UTC, followed by platform confirmation at 22:51:17 UTC — makes it a strong candidate for the filed attachment, but temporal proximity is not a substitute for platform attachment metadata or a downloaded filing certificate.

Future references should therefore use:

`SIGNED PDF RECOVERED FROM CONTEMPORANEOUS GMAIL — STRONG FILED-OBJECT PROVENANCE; CHANNEL BYTE IDENTITY NOT YET INDEPENDENTLY CONFIRMED`.

## 4. Corporate-email route

The Gmail scan did **not** locate a separate outgoing corporate email to a RICPE corporate-domain recipient carrying this communication.

Current controlled status is therefore:

- Ethical Channel submission: **confirmed**;
- platform confirmation email: **confirmed**;
- signed PDF in contemporaneous sender-controlled Gmail: **confirmed**;
- separate corporate-email transmission to RICPE: **not found in the current scan**.

Do not state that the communication was sent by both routes unless a native sent email or equivalent delivery record is later recovered.

## 5. Private credential emails

The scan also found self-addressed credential-record emails created after filing. They confirm that Gil Marer separately preserved his private follow-up credentials.

The secret key, verification code and any access credential must remain outside the public repository and website. No credential value is reproduced in this file.

## 6. Next evidence targets

1. Download/save any platform certificate or receipt showing the final submission time and attachment metadata.
2. If the platform permits it, preserve the attachment name/size/hash shown in the case record.
3. Preserve the exact 22-page signed PDF privately under its recovered SHA-256.
4. If corporate email is later used, preserve the native `.eml`, Message-ID, recipients, exact attachment hash and delivery/bounce records.
5. Record any later admission, conflict review, preservation order, investigation scope, Board treatment or request for information as a separate procedural event.
6. Treat any later CNMV or other-authority transmission as a separate filing with its own exact attachments, hashes and reference.

## 7. Controlled status

`DELETION-SAFE WITH OPEN CHANNEL-ATTACHMENT IDENTITY` — the Ethical Channel submission and platform email acknowledgment are corroborated; the signed 22-page PDF is cryptographically valid and preserved by hash from the contemporaneous Gmail chain; exact byte identity between that PDF and the channel attachment remains to be proved from platform/receipt metadata.