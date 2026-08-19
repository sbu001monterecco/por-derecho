# RICPE Ethics Channel — Current Status and Evidence Handover

**Current-status date:** 19 August 2026  
**Supersedes for current procedural status:** the pre-submission / submission-not-yet-evidenced status in `RICPE_ETHICS_CHANNEL_FILING_17AUG2026.md`  
**Public classification:** procedural-status evidence only  
**Thread-deletion status:** SAFE only after this change is merged to `main` and the live RICPE page is verified.

## 1. Current controlled status

The controlled status as at 19 August 2026 is:

**signed → filed/submitted → platform acknowledgement received → further same-case platform notification received**

The following remain **NOT ESTABLISHED by the notification evidence alone**:

- admission on the merits;
- opening of a formal investigation;
- conflict-screening outcome or recusals;
- preservation / legal-hold measures;
- referral to or treatment by the non-conflicted Board;
- appointment of an independent investigator;
- acceptance of any allegation;
- any finding, remedy or merits decision.

The website and repository must preserve the grammar:

**filed ≠ acknowledged ≠ further communication ≠ admitted ≠ investigated ≠ accepted ≠ decided.**

## 2. Evidence chain

### 17 August 2026 — filing and acknowledgement

A native Ithikios / RICPE channel email titled **“Recepción nueva comunicación”** was received at **22:51:17 UTC**. It stated that the communication had been communicated/submitted and that further information would follow. This corroborates the filing event already preserved by the final platform screen and the contemporaneous signed-document custody record.

Gmail evidence pointer:

- Gmail message ID: `1a011ec10e3528b9`
- Sender: `noreply-ithikios <noreply@ithikios.com>`
- Subject: `Recepción nueva comunicación`
- Timestamp: `2026-08-17T22:51:17+00:00`

### 19 August 2026 — further same-case notification

A second native Ithikios / RICPE channel email was received at **12:38:57 UTC** with subject **“Has recibido más información de una comunicación”**. Its body states, in substance, that additional information had been sent/provided in the same communication and directs the reporter to consult it through the channel.

Gmail evidence pointer:

- Gmail message ID: `1a01a082a340a6a5`
- Sender: `noreply-ithikios <noreply@ithikios.com>`
- Subject: `Has recibido más información de una comunicación`
- Timestamp: `2026-08-19T12:38:57+00:00`
- Attachments: none

This establishes a **further procedural movement in the same channel communication**. The email notification does not expose the substance of the additional information, so the repository must not infer what RICPE, its System Officer, Board or any investigator has decided or done beyond what is expressly evidenced.

## 3. Private case-code handling

The exact channel communication/access code is retained in the private Gmail / channel custody record and **must not be published in this public repository or website**, because the channel itself describes it as information used to consult the communication.

For non-secret public correlation only, the repository records the one-way SHA-256 fingerprint of the exact code:

`e53bda34973e530520bde39648768a1e32a358d8984294b21258789faebe6a24`

This fingerprint permits later evidential reconciliation without exposing the code itself.

## 4. Relationship to the signed communication

The controlling signed document remains:

- `01_RICPE_Comunicacion_Unica_Consejo_17AGO2026_FINAL_FIRMADA.pdf`
- 22 pages
- SHA-256: `b455075ceda7841471ef5f4ebfbb784ccd00357439aa8bf282e736fe4757832c`

The public repository continues not to store that signed PDF because of personal/signature material. Its private custody and cryptographic hash remain the reference.

## 5. Website placement rule

The 19 August status is not an isolated complaint update. It is the current endpoint of the RICPE–Acosta Matos / Sun Park chronology and must surface on the main bilingual RICPE / A&G dossier.

The runtime module `assets/ricpe-filed-status-20260817.js` has therefore been updated so that, after merge/deployment, it:

1. places a high-visibility current-status section immediately after the hero on both:
   - `/en/ric-private-equity-sun-park/`
   - `/es/ric-private-equity-sun-park/`;
2. updates existing RICPE formal-communication status blocks where present;
3. updates the existing 17-August update card where present;
4. states explicitly what the evidence establishes and what remains unproved;
5. withholds the exact channel code and displays only the one-way correlation fingerprint.

## 6. Evidential interpretation

### Established by the present evidence

- a formal communication was submitted through the RICPE channel on 17 August 2026;
- the platform issued a native acknowledgement email;
- on 19 August 2026 the platform issued a further email relating to the same communication;
- the later email states that additional information had been provided in that communication.

### Not established by the present evidence

- who authored the additional channel information;
- its substantive content;
- whether RICPE formally admitted the matter;
- whether an investigation has opened;
- whether preservation measures have been imposed;
- whether conflicts have been screened or recusals made;
- whether the President or non-conflicted Board has received or considered the communication;
- whether any allegation has been accepted or rejected;
- whether any remedy or regulatory referral has been decided.

## 7. Next evidence event

The next event to capture is the **actual text/content visible inside the channel** behind the 19 August notification. That content must be preserved separately, with date/time and source attribution, before changing any of the open-status fields above.

## 8. Deletion-safety handover

This record preserves the material thread-only conclusions required for continuity:

- why the 19 August email matters;
- how it relates to the 17 August filing;
- the exact evidence pointers needed to recover both Gmail records;
- the public/private boundary around the channel code;
- the correct non-prejudicial interpretation;
- the required website placement; and
- the finite next evidence step.

Once this branch is merged and the deployed RICPE page is verified to show the 19 August status, the ChatGPT thread that generated this update is **deletion-safe**.