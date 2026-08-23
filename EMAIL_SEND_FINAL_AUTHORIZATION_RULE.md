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

Approval to investigate, draft, file in the repository, publish a website change, create an audit, preserve evidence, prepare a completion record or approve a different package is **not** email authorization. Repository publication is never, by itself, authority to send an email.

## 2. Mandatory media-core hard stop

For every outbound email to a journalist, editor, newsroom, media organisation, media-related foundation/think-tank contact, journalistic routing address or other recipient being approached in a media capacity, read and apply:

`archive/MEDIA_CORE_PACKAGE_MANDATORY_RULE_23AUG2026.md`

Unless the user expressly approves a precise omission for that exact message, the exact media package must contain:

1. the appropriate-language PwC 2016 knowledge-point PNG source map;
2. the appropriate-language San Telmo / RICPE / Sun Park PNG source map;
3. the direct controlled San Telmo webinar URL timestamped at approximately 08:08;
4. at least one current Por Derecho / Project Sun Rock website link; and
5. the evidential-limits wording for the maps and webinar.

A media email missing any of these elements is **not ready**, even where it is described as Level 0, link-led, brief, a routing enquiry, a reply, a correction or a follow-up. Earlier discretionary wording such as “normally”, “consider” or “where relevant” does not override this section.

A general instruction such as “send” approves only a package that already complies with this hard stop. It does not silently waive the missing component. An exception must name the exact omitted component and exact recipient/message.

Required pre-send result:

```text
PWC_SOURCE_MAP_FOUND = YES
SAN_TELMO_SOURCE_MAP_FOUND = YES
WEBINAR_LINK_FOUND = YES
POR_DERECHO_LINK_FOUND = YES
EVIDENTIAL_LIMITS_TEXT_FOUND = YES
```

If any value is `NO` without an exact user-approved exception:

**SEND STATUS: BLOCKED — MANDATORY MEDIA CORE PACKAGE INCOMPLETE.**

## 3. No external test sends

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

## 4. Mandatory refusal conditions

The send path must stop where any of the following is true:

- the body is empty or effectively empty;
- the body consists only of one character, punctuation, whitespace or placeholder text;
- the subject or body contains a stop/test/draft marker;
- the user asked to prepare, preview, stage, hold, test, check, verify or confirm rather than to send;
- any recipient was added or changed after approval;
- the subject, body, attachment, link, language order or quoted thread differs from the approved package;
- the proposed action changes from a draft to a send, or from a new message to a reply, resend, correction, forward or follow-up;
- the only supposed approval is earlier general consent, publication permission, repository authority, a preservation instruction or approval of another version;
- the final package has not been presented or unambiguously identified to the user;
- a media-facing package fails the mandatory media-core preflight and no exact user-approved exception exists; or
- there is any uncertainty whether the authorization applies to this exact transmission.

Any change after approval invalidates the approval and requires a new final authorization.

## 5. Permitted before final approval

- Search and read connected email when otherwise authorized by the task.
- Prepare and revise an email draft.
- Identify proposed recipients, attachments and links.
- Render or validate the draft locally without transmission.
- Repository-file a redacted draft, recipient plan or attachment manifest where privacy controls permit.
- Present the complete final outbound package to the user for approval.

A draft must remain a draft. Do not press Send, schedule delivery, resend, forward, self-email or use a connector action that transmits it until the fresh exact authorization is received.

## 6. Approval and change control

- One authorization permits, at most, one transmission of the approved package unless the user expressly authorizes multiple sends.
- A successful send consumes the authorization. A resend, correction or follow-up requires a new authorization.
- A failed or uncertain send does not authorize an automatic retry.
- Silence, an out-of-office reply, an acknowledgement, a bounce, prior correspondence or a request for more information does not authorize a new recipient or transmission.
- Do not infer self-email authority from a generic preservation, backup or deletion-closeout protocol.
- Do not infer an exception to the Media Core Package from brevity, previous receipt, recipient familiarity or the words “send” or “continue”.

## 7. Post-send verification

When an authorized send is performed:

- do not state that it succeeded unless the mail tool confirms success;
- preserve the native sent-message evidence and exact package summary privately;
- classify a bounce, out-of-office response or automated acknowledgement only as the limited event it proves;
- do not treat delivery as proof of opening, reading, competent routing, acceptance or merits review;
- for a media email, verify both exact source-map attachments, the webinar URL, at least one Por Derecho link and the evidential-limits text in the actual sent copy; and
- do not expose private addresses, message identifiers or full private content in the public repository.

A failed or uncertain send remains `NOT VERIFIED AS SENT` until the connected mailbox confirms the event.

A media email may be marked complete only as:

**SEND STATUS: SENT + VERIFIED — COMPLETE MEDIA CORE PACKAGE PRESENT.**

## 8. Incident control

The 23 August 2026 connected-mail rescan located an empty “DO NOT SEND” transmission to a real external address and a one-character test to a reserved invalid address. Neither carried the substantive evidence package. The incident and corrective hard stop are preserved in:

`archive/OUTBOUND_EMAIL_CONTROL_INCIDENT_AND_HARD_STOP_23AUG2026.md`

A separate 23 August 2026 media-package control failure initially omitted the two standard source maps and controlled webinar from a media email. A separately authorized correction supplied the complete package. The permanent response is:

`archive/MEDIA_CORE_PACKAGE_MANDATORY_RULE_23AUG2026.md`

Do not send an apology, correction, replacement or explanation merely because an incident was discovered. Any corrective communication requires its own exact final authorization.

## 9. Current repository work

The CAM closeout, cross-thread rescan, media-core rules and website updates authorize **no email**. All preservation in this package is repository-only unless the user later approves an exact outbound package under this rule.