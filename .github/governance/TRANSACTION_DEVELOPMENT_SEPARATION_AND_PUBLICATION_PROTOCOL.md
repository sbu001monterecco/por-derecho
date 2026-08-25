# Transaction-development separation, custody and publication protocol

**Control date:** 25 August 2026
**Status:** governance-only operating policy
**Repository visibility:** public; this file contains no native private evidence
**Pages status:** excluded from the rendered GitHub Pages surface by its `.github/` path

## Purpose

Prospective financing, investment, acquisition, sale, operating-partner and other
new-transaction activity is a separate workstream from the legal-dispute,
asset-recovery and public-accountability record.

A commercial contact may later become relevant to the legal matter, but no such
connection may be presumed from chronology, group affiliation, professional
role, interest in an asset or willingness to hold a meeting.

## Track classification

Every new item must be placed in one of these tracks before it is analysed or
linked:

- **T — transaction development:** introductions, mandate screening, NDAs,
  teasers, investment criteria, financing conversations, meeting arrangements
  and prospective counterparties.
- **L — legal/evidential:** pleadings, decisions, complaints, source evidence,
  recovery strategy and public-accountability analysis.
- **X — controlled overlap candidate:** an item for which a later, specific and
  sourced fact may make a T item materially relevant to an L proposition. X is a
  review queue, not a finding and not publication authority.

The default classification for an attempt to enter a new transaction is **T**.

## Storage matrix

| Material | Authoritative location | Public repository | Rendered website |
| --- | --- | --- | --- |
| Native message, screenshot, email, profile image or attachment | Access-controlled mailbox or evidence store | Prohibited | Prohibited |
| Counterparty identity map and private locator | Access-controlled system | Prohibited | Prohibited |
| Anonymized continuity derivative | `.github/governance/records/` | Permitted only after privacy review | Prohibited |
| Public-safe transaction proposition | Purpose-specific record after approval | Only when necessary and authorized | Only after separate express publication authority |
| Unannounced pipeline, asset identity, pricing, structure or negotiation position | Access-controlled transaction workspace | Prohibited | Prohibited |

A repository filename containing “private”, “internal”, “archive” or “evidence”
does not make content confidential. Every committed byte must be safe for public
inspection.

## Ingestion and custody

1. Preserve the native artifact privately without alteration.
2. Record its source channel and date, and preserve a checksum or native
   provider locator privately where available.
3. A self-email is an outbound transmission. It may occur only after the exact
   final To/Cc/Bcc, action type, subject, body, attachment filename/version/hash
   and links have been presented and freshly authorized under
   `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md`.
4. Assign an opaque source ID that does not encode a person, organisation,
   address, asset or provider identifier.
5. If repository continuity is needed, store only a minimized paraphrase. Do not
   commit the verbatim private body, exact screenshot, name, title, employer,
   portrait, profile URL, email address, phone number, provider message ID,
   private subject, signature or exact private locator.
6. State what the item proves and, just as importantly, what it does not prove.
7. Record a next action without converting commercial interest into commitment,
   approval, mandate fit, knowledge of the legal record or acceptance of any
   allegation.

## Cross-linking gate

Do not link a T record to a legal allegation, actor page, evidence map, pleading,
authority submission or public route unless all of the following are satisfied:

1. a later, specific event makes the connection materially relevant;
2. the connection is supported by a primary source or verified direct
   communication rather than group branding, succession, employment, chronology
   or speculation;
3. the exact proposition is classified as documented fact, attributed
   statement, inference, disputed position or unresolved question;
4. actor-specific knowledge, duty, conduct and causation remain distinct;
5. confidential and personal information is minimized;
6. contrary or limiting evidence is preserved; and
7. the user gives express authority for the new private-source derivative and,
   separately, for any website publication.

If one condition is missing, keep the item in T or X and do not cross-link it.

## Communications and meetings

- Keep pre-NDA exchanges to administrative matters and the minimum high-level
  information needed to establish prima facie mandate fit.
- Disclose asset identity, ownership, operating structure, transaction history,
  control route, legal issues, financial information and supporting documents
  only after confidentiality is executed and the receiving vehicle, recipients
  and onward-disclosure perimeter are confirmed.
- Prefer a written scheduling trail and a video meeting with a generated meeting
  link. Do not supply or infer a telephone number merely because a counterparty
  requests a call.
- Create a diary invitation only after the attendee identity, email address,
  time zone and time have been resolved or expressly accepted.
- A willingness to meet proves no investment approval, commitment, mandate,
  conflict clearance, NDA acceptance or merits view.

## Publication hard stop

Transaction-development material is **not for the Por Derecho website** by
default. Do not add it to HTML, navigation, sitemaps, assets, public evidence
pages, actor dossiers, feeds or rendered downloads.

A later publication requires a new purpose-specific assessment, data
minimization, source-status language, rights review, current user authority and
all relevant publication-integrity checks. A legal-dispute publication approval
does not authorize transaction-pipeline publication, and vice versa.

## Review states

Use one of:

- `T_PRIVATE_NATIVE_PRESERVED`
- `T_PUBLIC_SAFE_DERIVATIVE_ONLY`
- `X_REVIEW_NO_LINK`
- `X_LINK_AUTHORIZED_REPOSITORY_ONLY`
- `X_PUBLICATION_SEPARATELY_AUTHORIZED`

No other state implies website publication.
