# Reusable prompt — ingest the reserved-declarant private-mailbox transfer

Use this prompt when the expected private transfer email or a later replacement from `RDM-PRIVATE-MAILBOX-01` may have arrived. It may be run in the originating thread or a fresh thread.

## Prompt

Read `AGENTS.md`, `CHATGPT_START_HERE.md`, `ops/REPOSITORY_PRESERVATION_CONTRACT.json`, `ops/CANONICAL_ENTITY_NAMES.json`, `archive/RDM_PRIVATE_MAILBOX_PENDING_INBOUND_CONTROL_25AUG2026.md`, `archive/RESERVED_DECLARANT_PRIVATE_MAILBOX_ACQUISITION_AND_CUSTODY_PROTOCOL_25AUG2026.md`, `archive/EVIDENCE_CUSTODY_AND_PRESERVATION_PROTOCOL_16AUG2026.md`, `archive/MISSING_EVIDENCE_REGISTER.md`, `archive/MISSING_EVIDENCE_REGISTER_VOICE_OSINT_MAILBOX_ADDENDUM_25AUG2026.md`, `archive/CORRECTION_REGISTER.md` and `archive/RECENT_EMAIL_PRIMARY_SOURCE_INGEST_QUEUE_20AUG2026.md`. Fetch current `origin/main` before editing and use a clean isolated branch/worktree.

The source is publicly identified only as `RDM-PRIVATE-MAILBOX-01`. Resolve the actual sender and receiving account privately from the current authenticated instruction and connected Gmail history. Never reconstruct or publish their addresses from Git, and never copy a private address, exact subject, message/thread ID, Drive ID, exact filename, private link or raw source body into public Git history.

### 1. Locate and verify the incoming message

Search the authenticated project mailbox for the newest plausible incoming collection report or evidence-transfer message from the account holder, beginning with the reported window after **25 August 2026, 22:49 UTC** and continuing through the current time. Search Inbox and All Mail, use sender history plus restrained topic families such as the reserved-declarant archive, Sun Park, Luchy Playa Blanca, Comunidad, Concurso 36/2012 and private evidence transfer, and paginate to completion within the bounded window.

If there are multiple candidates, compare sender, thread history, timing, subject context and the account holder's prior direct correspondence. Do not guess between plausible senders or messages. Ask Gil to disambiguate if necessary.

If no qualifying message is found:

- record privately the queries, locations, cutoff and pagination result;
- update the public-safe control only to `PENDING — NO VERIFIED RECEIPT AS OF [UTC timestamp]`;
- distinguish “not located in the searched corpus” from “does not exist”;
- do not send or draft a reminder unless the current user expressly requests it; and
- stop without claiming ingestion or completion.

If a qualifying message is found, read the complete message and its thread before classifying it. Verify privately the sender, recipient, timestamp, provider message/thread identifiers, subject, attachment list, links and whether the item is a sent original, forward, draft, notification or cover note. Classify the event separately as `TRANSMISSION`, `DELIVERY`, `ACKNOWLEDGMENT`, `ROUTING`, `REVIEW`, `SUBSTANTIVE EVIDENCE`, `CORRECTION` or a combination supported by the record.

### 2. Preserve before analysing

Preserve the message and every accessible attachment or linked file in an authorised private, durable evidence location—not in public GitHub. Where the connector supports it, retain RFC 2822/RAW or `.eml` content. Otherwise retain the provider locator privately and state the export limitation.

For every received object, record privately:

- private evidence ID;
- source and parent-message relationship;
- original filename, MIME type and byte size;
- created/sent/modified timestamps and timezone;
- sender/creator/owner and recipients or sharing state;
- provider message/thread/file identifiers and original private locator;
- SHA-256 of every downloaded native binary;
- acquisition method, time, tool and custodian;
- whether it is native, forwarded, exported, converted, OCR-derived, linked-only or inaccessible; and
- privilege, confidentiality, personal-data and retention status.

Keep an untouched master and a separate working copy. Do not overwrite a native source with OCR, redaction, PDF conversion or extracted text. A Drive link is a locator, not custody; a cover email is a retrieval lead, not proof of the attachment's propositions; a forwarded copy does not substitute for a native original.

If any attachment or link is unavailable, record the precise private failure and retry boundary. Do not label the transfer complete.

### 3. Establish the denominator and reconcile scope

Extract the collection report's claimed scope and compare it with what was actually received or accessible. Build a private denominator containing at least:

- Gmail years and locations searched;
- query families and whether pagination completed;
- messages and unique threads located;
- sent, received, archived, Spam, Trash and draft coverage where available;
- attachments located, accessible, unsupported, missing and hash-deduplicated;
- Drive files by owned/shared/linked status and file type;
- duplicate messages, forwarded copies, MIME variants and distinct file versions;
- connector/API/export errors and retries; and
- items likely absent from the connected counterpart corpus.

Reconcile the incoming corpus against the previously located connected-counterpart subset and existing private evidence using header `Message-ID`, normalized date/participants, body/attachment hashes and provenance. Preserve the provenance of every duplicate. Do not treat filename equality, related content or a forwarded chain as byte-identical evidence.

Unless a complete authorised Takeout or RAW/API acquisition has been reconciled across labels, attachments and errors, retain the overall status `PARTIAL / NOT ACQUIRED OR RECONCILED IN FULL`.

### 4. Review evidence neutrally and entity by entity

Triage every material item by:

- legal person and capacity;
- actor and dated role;
- proceeding or transaction;
- chronology;
- documentary proposition;
- supporting, adverse, contradictory or exculpatory effect;
- privilege/privacy restriction;
- authentication state;
- relationship to an existing repository evidence item or missing-evidence ID; and
- next finite verification question.

Use the canonical first reference **Luchy Playa Blanca, S.L.U. (LPB)**. Keep LPB, Matkator, S.L.U., the Comunidad de Propietarios Sun Park, the Comunidad de Explotación/CEXP, Pink Canary Services, S.L.U. (formerly Monterecco Sun Park, S.L.U.), Aweswell/Oswell, Patricia/Gil personally, the Insolvency Administrator, lawyers/firms, Community actors and other third parties separate. Do not transfer authority, knowledge, intention, benefit, responsibility or criminality through relationship, copied-recipient status, chronology or shared surname.

For each material proposition classify `DOCUMENTARY FACT`, `ATTRIBUTED ACCOUNT`, `PARTY ALLEGATION`, `EVIDENCE-BASED INFERENCE`, `OFFICIAL OUTCOME`, `CONTRARY RECORD`, `CORRECTED/SUPERSEDED` or `UNRESOLVED QUESTION`. A pleading proves the pleaded position; an email proves the communication shown; neither automatically proves judicial acceptance or the underlying event.

Search the complete thread, earlier/later messages, attachments, Drive versions and existing repository controls for material that weakens, corrects or contextualises each favourable item. Preserve adverse evidence rather than excluding it.

### 5. Build the private ingest outputs

Create or update privately:

1. the source/custody manifest;
2. the search and error log;
3. the message/thread/attachment/Drive denominator;
4. the deduplication and version map;
5. the privilege/privacy review queue;
6. the actor/entity/proceeding index;
7. the proposition-to-source and contradiction matrix; and
8. the finite gap and retrieval-action register.

Use stable private IDs. Create public opaque IDs only where a public-safe repository derivative is necessary. Do not put the private crosswalk into Git.

### 6. Update the repository evidence-wise

After preservation and source review, make the smallest additive public-safe repository update. At minimum:

- update `archive/RDM_PRIVATE_MAILBOX_PENDING_INBOUND_CONTROL_25AUG2026.md` with a truthful receipt/ingest state;
- update `ME-090` and `ME-MAIL-RDM-001` without closing them prematurely;
- update the mailbox acquisition/custody protocol with verified method and coverage only;
- add genuinely new P0/P1 retrieval items to the recent-email ingest queue using opaque source references and restrained public-safe descriptions;
- update `CORRECTION_REGISTER.md` before propagating any material correction;
- update affected specialist ledgers only where the source has been inspected and classified; and
- record all remaining custody, privilege, authentication and completeness gaps.

Public Git may contain only coarse counts, opaque IDs, public-safe propositions, source-status limitations and necessary corrective derivatives. Do not commit raw email bodies, addresses, subjects, recipient lists, provider IDs, private filenames, private Drive links, signatures, personal tax/bank data, privileged advice or live legal strategy.

Do not update the public website merely because evidence arrived. A website or raw-source publication requires current scope authority, privacy/privilege/redaction review, bilingual parity, branch/PR checks, exact-SHA deployment verification and live readback.

### 7. External-action boundary

This prompt authorises no email send, forward, reply, Drive share, permission change, third-party contact, filing or publication. Do not infer send authority from receipt, a draft, an earlier message, repository authority or an out-of-office redirect. Apply `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md` to any later proposed email.

### 8. Validation and completion report

Review the complete diff and every new public proposition. Run:

- `python3 scripts/validate_repository_preservation.py`
- `python3 scripts/validate_publication_integrity.py`
- `python3 scripts/validate_audience_experience.py`

Run specialist validators selected by changed paths. A local commit, push, PR, merge or deployment requires the authority and workflow applicable in the current authenticated request; this stored prompt is not authority by itself.

Finish with:

- receipt status and private verification time;
- source method and coverage;
- counts received versus claimed, expressed publicly only at a safe aggregate level;
- native-custody and hash status;
- duplicates, inaccessible items and errors;
- privilege/restriction counts;
- material new supporting, adverse and corrective propositions, each with its evidence class;
- repository files updated;
- public-site action, normally `NONE` unless separately authorised;
- outstanding `ME-090` / `ME-MAIL-RDM-001` gaps; and
- deletion-continuity and independent evidence-custody status.

Never say “all emails,” “complete archive,” “fully preserved,” “authenticated,” “published,” “sent” or “live” unless the relevant denominator and verification gate are satisfied.
