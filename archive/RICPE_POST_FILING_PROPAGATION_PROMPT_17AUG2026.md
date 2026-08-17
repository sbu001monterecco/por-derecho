# RICPE filing and authority-propagation prompt

Use this prompt after the RICPE communication has been digitally signed and submitted, and again after each later CNMV or authority transmission.

---

## Executable prompt

**Treat the signed RICPE communication and every related receipt as a controlled filing event. Execute the repository and website propagation; do not merely summarise what should be done.**

### 1. Start from current controlled state

Open `sbu001monterecco/por-derecho` and read, in this order:

1. `CHATGPT_START_HERE.md`;
2. `archive/THREAD_DELETION_CONTINUITY_PROTOCOL_16AUG2026.md`;
3. `archive/CONTINUOUS_MAINTENANCE_MATRIX.md`;
4. `archive/MISSING_EVIDENCE_REGISTER.md`;
5. `archive/CORRECTION_REGISTER.md`;
6. `archive/RICPE_GOVERNANCE_FUNDING_RECONCILIATION_16AUG2026.md`;
7. `archive/RICPE_FORMAL_COMMUNICATION_PREFILING_CONTROL_17AUG2026.md`;
8. the current RICPE/CNMV/public-funds/Orion specialist ledgers relevant to the transmission.

Inspect current `main` before relying on chat history. Reconcile concurrent repository changes rather than overwriting them.

### 2. Recover and authenticate the actual filed object

Obtain the exact digitally signed PDF, not an unsigned draft or a re-exported copy.

Record and verify:

- exact filename;
- file size;
- SHA-256;
- digital signer and certificate identity;
- signature date/time and validation result;
- document page count;
- whether the filed attachment is byte-identical across the Ethical Channel and corporate email routes.

If the signed binary is missing, do not claim a controlled signed filing. Mark `SIGNED BINARY REQUIRED` and continue only with the transmission evidence that actually exists.

### 3. Prove filing before calling it filed

For the RICPE Ethical Channel, recover:

- submission date and time;
- receipt or platform certificate;
- public-safe case/reference number;
- the exact attachment name and, where possible, attachment hash;
- current status shown by the platform;
- any acknowledgment or request for information.

Preserve the access code/password privately. **Never publish the password, access key or any credential.**

For corporate email, recover:

- native `.eml` or equivalent;
- full headers and Message-ID;
- recipients and copied recipients;
- sent timestamp;
- exact attachment and hash;
- delivery, rejection, bounce and automatic acknowledgment records.

Do not describe the document as filed merely because it was prepared, signed, uploaded locally or attached to an unsent draft.

### 4. Keep every procedural stage separate

Use this controlled vocabulary:

`PREPARED → SIGNED → FILED/SUBMITTED → RECEIVED/ACKNOWLEDGED → ADMITTED/REJECTED → EXAMINED/INVESTIGATED → DECIDED → REMEDY/FOLLOW-UP`.

Never convert:

- submission into admission;
- receipt into examination;
- an investigation opening into verification of the allegations;
- a referral into acceptance of competence;
- silence into agreement;
- or an institutional reference number into a merits decision.

### 5. Update the canonical repository record

Update `archive/RICPE_FORMAL_COMMUNICATION_PREFILING_CONTROL_17AUG2026.md` in place so that it becomes the controlling filing chronology. Do not create a competing timeline.

Add:

- signed-file metadata and SHA-256;
- Ethical Channel filing evidence;
- corporate-email evidence;
- acknowledgment and status;
- conflict/preservation/investigation information actually received;
- exact unresolved items;
- any correction between the prepared and filed versions.

If the filed PDF differs from the pre-signature V5 by more than the cryptographic signature container, produce a page/text diff and explain every substantive difference before treating it as the same communication.

Update `archive/CONTINUOUS_MAINTENANCE_MATRIX.md`, the proceedings/outward-communications register where applicable, and the missing-evidence or correction registers only where the new primary records change those controls.

### 6. Update the public website safely

Update the Spanish and English canonical RICPE pages and the ES/EN updates pages/Atom feeds.

Publicly record only:

- that the communication was filed, once proved;
- date/time;
- public-safe reference;
- signed PDF SHA-256;
- institutional recipient and filing route;
- current procedural status;
- a concise description of what was requested;
- and the controlled distinction between allegations, documentary questions and institutional response.

Do **not** publish:

- Ethical Channel password/access key;
- personal identity numbers, home address, private phone/email or signature image;
- private email headers containing unnecessary personal data;
- the signed binary unless Gil Marer expressly authorises publication and privacy/defamation review is complete;
- or language implying admission, investigation, referral or regulatory acceptance beyond the actual record.

Maintain bilingual parity. The English page may not weaken or strengthen the Spanish evidential status.

### 7. Record CNMV transmission separately

When the communication is later shared with CNMV, treat it as a new institutional event.

Recover and record:

- exact CNMV route used;
- sender and capacity;
- date/time;
- subject and purpose;
- exact attached documents and hashes;
- registration/reference number;
- acknowledgment;
- later classification, consultation, supervisory handling or response that can lawfully be confirmed.

State precisely whether the submission is an alert, consultation, complaint, supplementary evidence or another route. Do not call it a referral from RICPE unless RICPE actually referred it and evidence proves that event.

Update the canonical CNMV ledger/page and cross-link the RICPE filing without implying that CNMV validated title, financing, double-funding, conflict or criminal allegations.

### 8. Record every other authority separately

For each later authority, create or update an event with:

`date/time → sender/capacity → exact body/unit → competence/purpose → exact attachments/hashes → filing reference → acknowledgment → routing → examination → decision`.

Use competence-specific framing:

- CNMV — investment-vehicle supervision, investor information and related governance within its remit;
- AEAT/Canary RIC authorities — fiscal eligibility/idoneity and tax representations;
- regional-incentive/FEDER/SNCA/IGAE bodies — beneficiary, eligible cost, payment, employment, controls and EU/public financial interests;
- Ministerio Fiscal or judicial bodies — alleged offences and evidence within their competence;
- labour bodies — employment commitments and actual employment evidence;
- other professional or administrative bodies — only their defined remit.

Do not describe several separate submissions as one common investigation or coordinated institutional conclusion unless an official record establishes that coordination.

### 9. Preserve the strongest evidence discipline

For every material proposition classify it as:

1. `VERIFIED FACT`;
2. `PARTY ALLEGATION`;
3. `EVIDENCE-BASED INFERENCE`;
4. `OPEN QUESTION`;
5. `CORRECTED/SUPERSEDED`.

Do not turn multiple finance layers into established double/triple funding. Preserve the cost-by-cost, asset-by-asset, job-by-job and approval-by-approval reconciliation question.

Do not turn the FMMM→AGM/Orion trajectory into responsibility by association. Preserve the finite professional-duty and continuity questions.

Do not let later title or operation retrospectively answer what RICPE knew, verified and represented in 2019–2021.

### 10. Use protected GitHub workflow and verify deployment

Create a dedicated branch from current `main`.

Then:

1. edit only the canonical records and public pages actually affected;
2. review the diff for overstatement, privacy leakage, wrong references and stale status language;
3. open a PR explaining the exact primary evidence and what the filing does **not** prove;
4. merge when protections and checks permit;
5. verify the exact merge commit on `main`;
6. verify GitHub Pages completed successfully at that commit or a descendant containing it;
7. inspect the critical ES/EN routes;
8. update `archive/DEPLOYMENT_LOG.md`.

Do not state that the website is live merely because the PR merged.

### 11. Return an execution report

Report:

- exact signed filename and SHA-256;
- signature validation status;
- RICPE Ethical Channel reference/date/time/status;
- corporate-email Message-ID and delivery status;
- CNMV and other authority references, each separately;
- repository files changed;
- public routes changed;
- PR number, merge commit and Pages build result;
- information intentionally kept private;
- unresolved filing or evidence gaps;
- and whether the thread is `DELETION-SAFE`, `DELETION-SAFE WITH OPEN EVIDENCE` or `NOT DELETION-SAFE`.

## Non-negotiable rule

**Record the institutional event with maximum precision, but never allow “prepared”, “signed”, “filed”, “received”, “examined”, “referred” and “decided” to become interchangeable.**