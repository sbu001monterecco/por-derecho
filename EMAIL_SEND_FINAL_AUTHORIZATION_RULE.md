# Email send — exact final authorization and no-test-send rule

**Control date:** 25 August 2026  
**Status:** CONTROLLING USER-SPECIFIC OUTBOUND-EMAIL HARD STOP

## 1. Core rule

No email may be sent, resent, forwarded, corrected, followed up, scheduled or self-emailed without the user's **fresh explicit final approval of one exact outbound package**.

The exact package must identify:

1. every To, Cc and Bcc recipient;
2. whether the act is a new message, reply, correction, resend, forward, follow-up or self-email;
3. the exact final subject;
4. the complete final body in its final language order;
5. every attachment, including the precise filename and version and, where available, its hash; and
6. every included external link.

Before the package can be presented as ready or sent, it must also pass the pagination-complete dual Gmail history gate in:

`archive/PRE_SEND_GMAIL_PERSON_OUTLET_HISTORY_GATE_23AUG2026.md`

That gate requires a fresh, independent search for both the proposed person and their outlet/employer/organisation, including prior direct and indirect approaches, replies, bounces, redirects, colleague/fallback collisions and other-channel contact evidenced by email. Neither half may be omitted.

Approval to investigate, draft, file in the repository, publish a website change, create an audit, preserve evidence, prepare a completion record or approve a different package is **not** email authorization. Repository publication is never, by itself, authority to send an email.

## 2. No external test sends

No real, reserved, invalid, throwaway or deliberately non-working external address may be used to test:

- recipient resolution;
- formatting;
- delivery;
- bounce handling;
- connector availability;
- attachments;
- links;
- authorization logic; or
- draft rendering.

Testing must remain local, in draft state or in an explicitly non-transmitting validation system.

An empty message, a one-character message or a message labelled **“DO NOT SEND”**, **“TEST”**, **“DRAFT”**, **“PLACEHOLDER”**, **“NO ENVIAR”**, **“PRUEBA”** or **“BORRADOR”** must fail closed. A prohibition or placeholder label is never permission to transmit.

## 3. Mandatory refusal conditions

The send path must stop where any of the following is true:

- the body is empty or effectively empty;
- the body consists only of one character, punctuation, whitespace or placeholder text;
- the subject or body contains a stop/test/draft marker;
- the user asked to prepare, preview, stage, hold, test, check, verify or confirm rather than to send;
- any recipient was added or changed after approval;
- the subject, body, attachment, link, language order or quoted thread differs from the approved package;
- the proposed action changes from a draft to a send, or from a new message to a reply, resend, correction, forward or follow-up;
- the only supposed approval is earlier general consent, publication permission, repository authority, a preservation instruction or approval of another version;
- the final package has not been presented or unambiguously identified to the user; or
- the person-and-organisation Gmail history scan is missing, stale, not pagination-complete, leaves a collision unclassified or does not establish a verified current professional route;
- there is any uncertainty whether the authorization applies to this exact transmission.

Any change after approval invalidates the approval and requires a new final authorization.

## 4. Mandatory recipient-class content rules

Exact final authorization does not cure a package that violates a controlling recipient-class content rule.

For every media recipient—journalist, editor, newsroom, media organisation, media-routing address or journalistic contact—the package must first satisfy:

`archive/OUTBOUND_MEDIA_CORE_PACKAGE_MANDATORY_RULE_23AUG2026.md`

Media recipient selection and concurrent same-outlet preparation are controlled by:

`archive/MAXIMUM_MEDIA_DISTRIBUTION_MULTI_RECIPIENT_RULE_23AUG2026.md`

That rule permits separate named packages through an outlet-published general newsroom route when it is labelled honestly as `A la atención de [name]`; it never turns that route into a claimed personal address and never bundles approval for several transmissions.

It must also satisfy:

`archive/PRE_SEND_GMAIL_PERSON_OUTLET_HISTORY_GATE_23AUG2026.md`

That means the actual draft must contain:

- the appropriate-language PwC PNG attachment;
- the appropriate-language San Telmo / RICPE / Sun Park PNG attachment;
- the controlled timestamped San Telmo webinar link;
- at least one current Por Derecho website link; and
- the evidential limitation applicable to the maps and webinar.

A general instruction to **“send”** approves only a compliant package; it is not an implied waiver of a missing mandatory component.

A waiver is valid only where the user expressly identifies the exact recipient, exact transmission and exact component to omit. Any such waiver is one-use and must be recorded in the readiness record.

If the media-core check fails and no exact waiver exists:

**SEND STATUS: BLOCKED — MANDATORY MEDIA CORE PACKAGE INCOMPLETE.**

## 5. Permitted before final approval

- Search and read connected email when otherwise authorized by the task.
- Prepare and revise an email draft.
- Identify proposed recipients, attachments and links.
- Render or validate the draft locally without transmission.
- Repository-file a redacted draft, recipient plan or attachment manifest where privacy controls permit.
- Present the complete final outbound package to the user for approval.

Research and drafting may begin from a preliminary history check, but the package must not be marked ready or presented for final approval until the fresh person-and-organisation Gmail scan is complete and every continuation token is exhausted.

A draft must remain a draft. Do not press Send, schedule delivery, resend, forward, self-email or use a connector action that transmits it until the fresh exact authorization is received.

## 6. Approval and change control

- One authorization permits, at most, one transmission of the approved package unless the user expressly authorizes multiple sends.
- A successful send consumes the authorization. A resend, correction or follow-up requires a new authorization.
- A failed or uncertain send does not authorize an automatic retry.
- Silence, an out-of-office reply, an acknowledgement, a bounce, prior correspondence or a request for more information does not authorize a new recipient or transmission.
- Do not infer self-email authority from a generic preservation, backup or deletion-closeout protocol.
- Do not infer an exception to a mandatory attachment, webinar or website-link rule from brevity, recipient tailoring, urgency or the user's later use of the word “send”.

## 7. Post-send verification

When an authorized send is performed:

- do not state that it succeeded unless the mail tool confirms success;
- preserve the native sent-message evidence and exact package summary privately;
- classify a bounce, out-of-office response or automated acknowledgement only as the limited event it proves;
- do not treat delivery as proof of opening, reading, competent routing, acceptance or merits review; and
- do not expose private addresses, message identifiers or full private content in the public repository.

The sent-copy record must also preserve privately the completed person-and-organisation history-gate classification that controlled the send.

For a media recipient, sent-copy verification must additionally confirm the two exact PNG filenames, the controlled webinar URL, at least one Por Derecho URL and the evidential limitation.

A failed or uncertain send remains `NOT VERIFIED AS SENT` until the connected mailbox confirms the event.

## 8. Incident control

The 23 August 2026 connected-mail rescan located an empty “DO NOT SEND” transmission to a real external address and a one-character test to a reserved invalid address. Neither carried the substantive evidence package. The incident and corrective hard stop are preserved in:

`archive/OUTBOUND_EMAIL_CONTROL_INCIDENT_AND_HARD_STOP_23AUG2026.md`

A separate 23 August 2026 media-package incident, in which mandatory media attachments and the webinar were wrongly treated as optional before a later authorised correction, is controlled by:

`archive/OUTBOUND_MEDIA_CORE_PACKAGE_MANDATORY_RULE_23AUG2026.md`

The 25 August 2026 readiness-without-transmission incident and its corrective state-machine control are preserved in:

`archive/OUTBOUND_EMAIL_NOT_SENT_AFTER_READINESS_INCIDENT_25AUG2026.md`

Do not send an apology, correction, replacement or explanation merely because an incident was discovered. Any corrective communication requires its own exact final authorization.

## 9. Current repository work

Repository updates, cross-thread rescans and website changes authorize **no email**. All preservation in those packages is repository-only unless the user later approves an exact compliant outbound package under this rule.

## 10. Mandatory operational state machine

Every outbound email action must follow this non-skippable sequence:

`PREPARED → AUTHORIZED → SENT → VERIFIED`

The states mean:

### `PREPARED`

The exact package has been assembled and checked, but no transmission action has occurred.

Phrases such as **“prepare”**, **“ready to send”**, **“confirm readiness”**, **“be prepared to send”**, **“check it”**, **“verify it”** or **“hold it ready”** keep the package in `PREPARED`. They do not authorize transmission even where the phrase also contains the words “to send”.

Every preparation-only response must display prominently:

**SEND STATUS: PREPARED — NOT SENT.**

### `AUTHORIZED`

The user has given a fresh, unambiguous instruction to transmit the exact approved package, such as **“send it now”**, **“forward this now”** or another instruction that clearly performs the action rather than merely asking for readiness.

If the language is genuinely ambiguous, the state remains `PREPARED`; no send action may occur, and the response must say that no transmission occurred.

### `SENT`

The connected mail tool has been invoked exactly once for the authorized package and has returned a positive transmission result with a concrete message or thread reference.

A package is not `SENT` merely because it was described as ready, a draft exists, a send was intended, or a prior assistant said it would be sent.

### `VERIFIED`

The native message has been retrieved from the connected Sent mailbox and compared with the approved package under section 11 below.

No success statement may be made before this state is reached. The assistant must never collapse `SENT` and `VERIFIED` into one unsupported claim.

## 11. Mandatory native sent-message read-back

Immediately after every authorized send, the assistant must retrieve the native sent message using the returned message ID or thread ID. If the send action does not return a usable identifier, it must perform a precise Sent-mail search using the exact recipient, subject and immediate timestamp window.

The read-back must compare the native sent copy against the approved package and verify all of the following:

1. sender account;
2. every To, Cc and Bcc recipient;
3. transmission mode: new email, reply, correction, resend, forward, follow-up or self-email;
4. exact subject;
5. non-empty body and at least one distinctive expected body marker;
6. language order and quoted-thread/source-message inclusion where applicable;
7. sent timestamp;
8. every required external link;
9. attachment count;
10. every attachment filename and, where available, size, version or hash; and
11. for a forward, preservation of every required original attachment and the correct source message.

A positive send-tool response is necessary but is **not sufficient** for verification.

If any required recipient, body element, link or attachment is missing, altered, duplicated or unexpected, the transmission must be classified:

**SEND STATUS: SENT BUT NOT VERIFIED AS CORRECT.**

A required attachment that is absent from the native sent copy is a failed package even if Gmail accepted the message.

After successful comparison, report a private verification receipt containing, at minimum:

- `SEND STATUS: VERIFIED AS SENT CORRECTLY`;
- sent timestamp;
- recipients and recipient classes;
- subject;
- transmission mode;
- attachment count and exact filenames; and
- the native message/thread reference, kept out of the public repository.

Do not claim delivery, opening, reading, competent routing, acceptance or agreement unless later evidence separately proves that narrower event.

## 12. Failure, mismatch and retry handling

- No automatic or silent retry is permitted after a failed, uncertain or incomplete transmission.
- First diagnose and report whether the failure occurred before transmission, during the send action, or during native sent-copy verification.
- Discovery that a prepared package was never sent does not itself authorize a first send.
- Discovery of a malformed sent package does not authorize a correction, resend or follow-up.
- A new exact package and fresh final authorization are required for every retry, correction or replacement.
- The assistant must preserve the distinction between `NOT SENT`, `SENT BUT NOT VERIFIED AS CORRECT`, `VERIFIED AS SENT CORRECTLY`, `BOUNCED`, `AUTOMATED ACKNOWLEDGEMENT`, and any later substantive reply.
