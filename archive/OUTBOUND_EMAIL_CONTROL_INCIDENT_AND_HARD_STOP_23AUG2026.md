# Outbound email control incident and hard stop — 23 August 2026

**Status:** CONTROLLING INCIDENT RECORD / HARD STOP  
**Public-data rule:** no private address, Gmail identifier or unnecessary personal data is reproduced here.

## 1. Incident recorded

The connected-mail rescan located two transmissions used as tests when no external test transmission should have occurred:

1. an empty message with the subject **“DO NOT SEND”** was transmitted to a real external address; and
2. a one-character test message was transmitted to a reserved invalid address and bounced.

Neither message contained the substantive evidential package, attachments or a developed allegation. That limits the content exposure but does not remove the control failure.

## 2. Controlling determination

A label such as “DO NOT SEND”, “TEST”, “DRAFT” or “PLACEHOLDER” is never permission to transmit. It is a prohibition marker.

No real or deliberately invalid external address may be used to test:

- recipient resolution;
- formatting;
- attachments;
- delivery behavior;
- bounce handling;
- connector availability;
- draft rendering; or
- authorization controls.

Testing must remain local, in draft state or inside an explicitly non-transmitting validation system.

## 3. Mandatory pre-send hard stop

Before any external send, the working record must contain one fresh and exact authorization for one immutable package. The package must identify:

- all To, Cc and Bcc recipients;
- the final subject;
- the complete final body;
- every attachment by filename and hash where available;
- every external link;
- the language order;
- whether the act is a new message, reply, correction, resend or follow-up; and
- the authorization timestamp and authorizing person.

Any change to any field invalidates the authorization and requires a new exact authorization.

## 4. Mandatory automatic refusal conditions

The send path must fail closed where any of the following is true:

- body is empty or effectively empty;
- body consists only of one character, punctuation, whitespace or a placeholder;
- subject or body contains “DO NOT SEND”, “DON'T SEND”, “NO ENVIAR”, “TEST”, “PRUEBA”, “DRAFT”, “BORRADOR”, “PLACEHOLDER” or an equivalent stop marker;
- any recipient was added after authorization;
- an attachment, link, language block or quoted thread differs from the authorized package;
- the instruction is to prepare, preview, test, check, hold, stage, draft or confirm rather than to send;
- the only authorization is inferred from an earlier message, repository rule, general publication permission or a different outbound package;
- an invalid, reserved or throwaway external address is being used as a delivery test; or
- there is uncertainty whether the user has seen the final recipient list and final package.

## 5. Incident response

- Do not send a correction, apology, explanation or replacement merely because this incident was discovered.
- Any corrective communication requires its own exact final authorization.
- Preserve the native sent-message and bounce evidence in the connected mailbox.
- Treat an empty transmission as a transmission event, not as “nothing happened”.
- Record future connector defects or unexpected sends as incidents immediately.

## 6. Relationship to existing rules

This file strengthens, and does not replace, `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md` and `archive/OUTBOUND_EMAIL_FUTURE_THREAD_START_HERE_23AUG2026.md`.

No outbound communication is authorized by this incident record.