# Project Sun Rock / Por Derecho — Pre-send Gmail person-and-organisation history gate

**Control date:** 23 August 2026
**Status:** CONTROLLING OUTBOUND-EMAIL HARD GATE
**Scope:** every proposed new email, reply, resend, correction, forward, follow-up, routing enquiry or self-email

## 1. Non-negotiable rule

Before an outbound package may be described as ready, presented for final approval or sent, connected Gmail must be searched **fresh and independently for both**:

1. the proposed person; and
2. the proposed outlet, employer, institution, company or other organisation.

The purpose is to determine whether Por Derecho / Project Sun Rock has approached the person, the organisation, another relevant person at that organisation or a route associated with either one; whether anything came back; and whether the proposed transmission would duplicate, contradict, bypass or collide with existing communication.

The person search does not substitute for the organisation search. The organisation search does not substitute for the person search. A public-role check, repository note, memory, CRM row, website search or generic domain query does not substitute for the connected-Gmail scan.

## 2. Minimum Gmail scope

Every scan must use `in:anywhere` or the connected-mail equivalent that covers the entire accessible Gmail corpus, including sent, received, archived, draft, spam and trash material where the connector exposes it.

Search, as applicable:

- exact name with and without accents;
- initials, abbreviations, byline forms, known former names and unambiguous professional variants;
- every verified current or historical professional address;
- every relevant domain and subdomain;
- organisation, outlet, programme, publication, trading and legal-entity names;
- generic, specialist and routing mailboxes;
- current and relevant former staff names where they may reveal an outlet-level or organisation-level approach;
- `to`, `from`, `cc` and `bcc` header roles;
- subject and body text;
- forwarded or quoted content;
- bounces, redirects, out-of-office replies and automated acknowledgements; and
- email notifications evidencing contact through another professional channel.

Search terms must be tailored to the target. A single exact-name query or a single `@domain` query is not exhaustive.

## 3. Pagination-complete and thread-complete

Every search must be paginated until the connector returns no continuation or next-page token.

**A retained continuation token means the scan is incomplete.** Do not call the result exhaustive, do not present the package as ready and do not send.

Relevant results must be read at message/thread level. Snippets alone are insufficient where the classification depends on the actual sender, recipients, quoted history, response, bounce, redirect, attachment, alternative channel or substantive content.

## 4. Required classifications

Record privately, at minimum:

- scan cutoff and completion time;
- query families used for the person;
- query families used for the organisation;
- page-completeness result for every query family;
- direct person-specific email history;
- direct organisation-domain or mailbox history;
- colleague, editor, fallback, Cc/Bcc, quoted-body or forwarded-history collision;
- bounce, redirect, out-of-office, acknowledgement or substantive-response status;
- other-channel contact evidenced by email;
- whether the proposed message is a genuine first approach, a new person-specific lane at a previously touched organisation, a follow-up, a reply, a correction or a duplicate; and
- the routing and spacing decision.

Use narrow conclusions. Say `NO PERSON-SPECIFIC EMAIL LOCATED IN THE COMPLETED GMAIL SCAN AT THE STATED CUTOFF`, not `never contacted`, unless evidence really supports the broader statement. A no-result Gmail scan is not proof that no offline or other-channel contact occurred.

Do not publish private email addresses, Gmail message IDs, private bodies or unnecessary personal data in the public repository.

## 5. Fail-closed outcomes

Apply this exact result if either half of the scan is missing, any pagination token remains, a relevant result has not been read, identity or routing is unresolved, or a collision has not been classified:

**SEND STATUS: BLOCKED — PERSON/ORGANISATION GMAIL HISTORY GATE INCOMPLETE.**

A prior approach does not always prohibit a later email. It does require an explicit classification, recipient-specific justification, duplicate/outlet-spacing decision and accurate message type before the package can advance.

If a proposed named recipient lacks a verified current professional route:

**SEND STATUS: BLOCKED — PROFESSIONAL ROUTE NOT VERIFIED.**

Do not guess a private or professional address. A generic newsroom or information address does not count as a verified direct route to a named person unless the outlet expressly identifies it for that person or the user expressly approves the generic routing package as such.

## 6. Timing, invalidation and authorization

Run the completed dual scan:

1. before the draft is marked ready or presented for exact final approval; and
2. again immediately before an authorised send if any material time has elapsed, new mail may have arrived, or the person, organisation, route, thread, subject, body, attachments, links or message type changed.

Any material change or newly located history invalidates the prior classification and returns the package to research/readiness review.

Completion of this gate is necessary but never sufficient to send. `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md` still requires fresh user authorization of the exact final package. No scan result, queue position, prepared draft or earlier general instruction authorises transmission.

## 7. Readiness-record fields

Every Outbound Package Readiness Record must contain:

```text
PERSON GMAIL SCAN = COMPLETE / INCOMPLETE
ORGANISATION GMAIL SCAN = COMPLETE / INCOMPLETE
PAGINATION = EXHAUSTED / TOKEN REMAINS
DIRECT PERSON HISTORY = ...
DIRECT ORGANISATION HISTORY = ...
COLLEAGUE / FALLBACK / OTHER-CHANNEL COLLISION = ...
RESPONSE / BOUNCE / REDIRECT STATUS = ...
MESSAGE CLASSIFICATION = ...
ROUTING / SPACING DECISION = ...
HISTORY-GATE RESULT = PASS / BLOCKED
```

No send action may be invoked unless `PERSON GMAIL SCAN`, `ORGANISATION GMAIL SCAN` and `PAGINATION` are complete, the collision decision is recorded, the professional route is verified, all other package rules pass and the exact package has fresh final authorization.
