# Project Sun Rock / Por Derecho — Mandatory Website Link Rule

**Control date:** 23 August 2026  
**Status:** controlling outbound-email rule  
**Applies to:** every Project Sun Rock / Por Derecho outbound email, including first approaches, journalist/editor pitches, routing enquiries, institutional notices, regulatory/professional communications, follow-ups, corrections, supplements, witness/source approaches, investor/compliance outreach and self-emails where otherwise authorised.

## Mandatory rule

Every outbound Project Sun Rock / Por Derecho email must include at least one current public **Por Derecho / Project Sun Rock website link** in the body.

Default public hub:

`https://sbu001monterecco.github.io/por-derecho/`

Where a recipient-specific dossier or language route is more useful, include that route as well or use it as the principal website link. The rule is not mechanical homepage repetition: it is **mandatory public website access plus recipient-specific route selection**.

## Readiness gate

Before final approval verify that:

1. at least one Por Derecho website link is present in the exact email body;
2. the link resolves publicly;
3. the route is in the appropriate language where practical;
4. the linked page has inherited current corrections/evidential boundaries; and
5. the link is listed in the Link Manifest and is therefore covered by the user's exact final authorisation.

**A Project Sun Rock / Por Derecho outbound draft with no Por Derecho website link is NOT READY TO SEND.**

## Route selection

Prefer the route that answers the recipient's first question:

- general orientation → homepage;
- journalists/media → media briefing once live, otherwise homepage/collaborate plus the most relevant dossier;
- creditor/title/standing → lender-of-record;
- Community/CEXP → Community/minutes;
- RIC/RICPE/incentives → funding/investment route;
- lawyers/academics/technical recipients → Legal Notebook/judicial-spine;
- material control/mixed ownership → exact 7-June-2018 dossier.

## Triggering omission — Civismo / Diego Sánchez de la Cruz routing email

The 23-Aug-2026 Civismo / Diego Sánchez de la Cruz routing email was sent with:

- the tailored legal-certainty/investment dossier paragraph;
- the controlled San Telmo webinar link; and
- the two Spanish PNG source maps;

but **accidentally omitted the Por Derecho website link**.

Preserve the historical sent record exactly. Do not claim the website link was present. This omission is the implementation trigger for the mandatory future rule.

The omission does **not** itself authorise a corrective resend or follow-up. Any correction or supplement to the recipient remains subject to `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md` and must be separately approved as an exact package.

## Exceptions

Only omit the website link where inclusion would be unlawful, technically impossible, expressly prohibited by the user for that exact message, or materially unsafe for a witness/source-protection reason. Any exception must be expressly recorded in the readiness record before send.

## Relationship to other controls

Read this rule with:

- `archive/OUTBOUND_EMAIL_COMMUNICATIONS_PROTOCOL_23AUG2026.md`;
- `archive/OUTBOUND_CANONICAL_SOURCE_KIT_MANIFEST_23AUG2026.md`;
- `archive/prompts/RECIPIENT_SPECIFIC_OUTBOUND_EMAIL_PREPARATION_PROMPT_23AUG2026.md`;
- `archive/OUTBOUND_EMAIL_FUTURE_THREAD_START_HERE_23AUG2026.md`; and
- `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md`.

This rule adds a mandatory content/readiness requirement. It does not weaken or replace the final-authorisation gate.

## 5 September 2026 reinforcement — PD-MEDIA-LINK-20260905-01

**User-directed scope:** improve preparation of media re-entry packages and prevent another omission of the website or relevant landing pages. Preparation is not permission to send. This additive reinforcement becomes part of the canonical file when integrated to main; a worker branch is not an active deployment. It preserves the original rule and all exact-authorization, privacy and exception controls.

### Actual body first; manifest second

A media package must pass the standing requirements independently of its proposed manifest. A manifest that omits a mandatory component cannot make the package compliant. Comparing an incomplete draft with an identically incomplete sent copy proves transmission consistency, not correctness.

For every media update include, as visible links in the current email body:

1. the appropriate-language Por Derecho website entry point;
2. at least one distinct, relevant, reader-facing topic landing page; and
3. when describing judicial or public-authority supporting records as available online, the relevant judicial/institutional access routes that actually expose those records or their public-safe references.

For Spanish Sun Park / MYND / RICPE updates the baseline link set is:

- Website: `https://sbu001monterecco.github.io/por-derecho/es/`
- Topic: `https://sbu001monterecco.github.io/por-derecho/es/ric-private-equity-sun-park/`
- Judicial/institutional reconstruction: `https://sbu001monterecco.github.io/por-derecho/es/reconstruccion-unitaria-autoridades-publicas/`
- Institutional records: `https://sbu001monterecco.github.io/por-derecho/es/registros-institucionales/`

Select a different verified topic route when appropriate. The baseline is not an assertion that every linked record is complete or currently accessible. Recheck each route, its content and any required fragment/source before approval and before a later authorised send. A repository file, GitHub raw/blob link, BOE, BORME, YouTube, a link contained only in a PDF or quoted old email, or a link shown only in the assistant's response does not satisfy this body requirement.

### Mandatory media core remains mandatory

The two language-correct PNG source maps, controlled timestamped San Telmo webinar and evidence limitation required by `archive/OUTBOUND_MEDIA_CORE_PACKAGE_MANDATORY_RULE_23AUG2026.md` remain required. A documentary PDF supplements, rather than replaces, that core. Do not silently omit components for brevity or inferred editorial preference. A source conflict in a graphic must be resolved, flagged or covered by the exact exception mechanism; a transport check does not certify its assertions.

### Accurate website-coverage statement

Use wording materially equivalent to:

> La web de Por Derecho reúne la cronología y las fichas de los procedimientos judiciales y de las actuaciones ante las autoridades públicas, con referencias, resoluciones, escritos, respuestas y documentos de apoyo publicables, además de enlaces entre los distintos expedientes. Distingue los hechos documentados, nuestras alegaciones, las decisiones —incluidas las desfavorables— y la documentación todavía pendiente o reservada. La presencia de un órgano en el registro no implica su respaldo a nuestras conclusiones.

Limit this wording to the actual inspected publication matrix. Do not say that all complete court or administrative files are published without proving that coverage. Distinguish public copies, redacted derivatives, summaries, references, private/request-only records and unresolved source gaps. A filing is not a court finding; receipt, routing, publication and institutional endorsement are different states.

### Required private readiness record

Record each required URL, purpose, body occurrence, language, public-access/content check, timestamp and source/fragment result. An inaccessible browser result is unverified, not proof of a broken page or proof of live availability. Record any cached-view limitation; do not claim exact live-byte verification from a cached page.

Inspect real attachments; record exact filename, version, bytes and SHA-256. Check both plain text and rendered HTML when both are sent. No private email, recipient list, provider locator or unsent package belongs in the public repository.

The offline helper `scripts/validate_media_link_core.py` checks decoded MIME bodies and real PNG attachments, and can compare approved attachment hashes. It does not access Gmail or send anything. Its pass is only `CONTENT_GATE_PASS_ONLY`; it does not prove live URLs, rendered visibility, source accuracy, complete dual Gmail history, privacy clearance, authorization or sending. Those remain separate mandatory checks. It is not automatically installed in Gmail transport or CI by this document.

### Regression and mismatch rule

The mechanical tests must reject missing website links; homepage without a topic landing; missing judicial/institutional access links when required; required links present only in attachments; missing PNGs; altered approved attachment hashes; and HTML/plain-text link mismatch.

Before approval and sending, apply:

`STANDING REQUIREMENTS → ACTUAL BODY / MIME / ATTACHMENTS → VERIFIED LINK AND ATTACHMENT MANIFEST → COMPLETE PERSON + OUTLET HISTORY → EXACT FINAL USER AUTHORIZATION`.

After an authorised send, retrieve the native Sent copy and repeat the required-link and attachment comparisons. A positive connector response is not sufficient. Any missing required component means **SENT BUT NOT VERIFIED AS CORRECT**, even if the incomplete package was successfully transmitted. Preserve that distinction and never silently repair a historical email.

Discovery of a previous omission authorises no correction, follow-up, resend or automatic retry. A separate exact package and fresh final authorization remain necessary.
