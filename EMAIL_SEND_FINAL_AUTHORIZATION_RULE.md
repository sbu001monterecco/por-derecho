# Email send — exact final authorization and no-test-send rule

**Control date:** 23 August 2026  
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

Do not send an apology, correction, replacement or explanation merely because an incident was discovered. Any corrective communication requires its own exact final authorization.

## 9. Current repository work

Repository updates, cross-thread rescans and website changes authorize **no email**. All preservation in those packages is repository-only unless the user later approves an exact compliant outbound package under this rule.
