# Outbound email public landing-page rule

**Control ID:** PD-OUTBOUND-LANDING-20260930-01  
**Adopted:** 30 September 2026  
**Status:** MANDATORY outbound-email governance  
**Scope:** every human-authored Por Derecho / Project Sun Rock / AWESWELL / Sun Rock substantive outbound email, including new messages, replies, forwards, corrections, supplements, follow-ups and self-preservation emails. Automated provider/system messages are outside this rule.

## 1. Mandatory link

Every in-scope outbound email must contain **at least one live Por Derecho public URL** hosted on **GitHub Pages and/or GitLab Pages**.

A message with no qualifying Por Derecho URL is not send-ready.

**Fail-closed state:**
`SEND STATUS: BLOCKED — LANDING PAGE LINK MISSING`

The user may waive this requirement only by expressly identifying the exact transmission and expressly authorising omission of the link. A waiver is one-use only.

## 2. The link must be a landing page, not decoration

The URL must give the recipient a useful, public-safe starting point for the subject of the email.

For a law firm, lawyer, accountant, auditor, adviser or other professional recipient, the default is a **recipient- or firm-specific landing page**.

For a Colegio, Consejo, regulator, court-adjacent body, Fiscalía or public authority, use a **body-specific or matter-specific institutional landing page**.

For a joint email to several institutions or firms, use:
- one common landing page that materially covers every principal recipient; or
- one qualifying landing page per materially distinct recipient entity.

A homepage link alone is insufficient where a more specific controlled page exists.

## 3. Dedicated-page preference and fallback

Priority order:

1. exact recipient/firm/institution landing page;
2. exact matter/proceeding landing page materially centred on that recipient;
3. recipient-class coordination page that visibly identifies the recipient and the relevant issue.

If none exists, the email is normally **blocked pending creation of a public-safe landing page**. A generic fallback may be used only with an exact user-authorised waiver and an explicit open task to create the dedicated page.

## 4. Mirror rule

Minimum: one verified live host.

Preferred: both public mirrors when materially equivalent and live:
- GitHub Pages;
- GitLab Pages.

Where both are used, describe them as continuity/preservation/resilience mirrors. Do not imply either provider is compromised.

Where only one host is used, do not claim dual-host resilience.

## 5. Pre-send gate

Before the exact package is presented as ready:

1. choose the landing page for each material recipient entity;
2. live-read the exact URL;
3. confirm HTTP/render availability;
4. confirm the page is current enough for the email;
5. confirm the page does not expose private Gmail/Drive locators, credentials, privileged material, tax-reserved material or unnecessary personal data;
6. confirm the page preserves allegation/finding and actor-separation boundaries;
7. place the exact URL visibly in the email body;
8. include it in the package's Link Manifest;
9. include the link in the user's final exact-package approval.

A stale, broken, misleading, overbroad or privacy-unsafe page fails the gate.

## 6. Post-send read-back

Native Sent verification must confirm:
- at least one qualifying Por Derecho URL is present;
- every material recipient entity has a qualifying common or dedicated landing page;
- the exact URL matches the approved package;
- every required GitHub/GitLab mirror link is present where the package required both.

If the message was transmitted without the required link:
`SEND STATUS: SENT — LINK-GATE NONCOMPLIANT`

Do not automatically resend or correct. Any corrective message requires a new exact package and fresh user authorisation.

## 7. Continuity register

For every sent email, preserve privately:
- recipient entity;
- selected landing page;
- host(s);
- live-read date;
- exact sent URL(s);
- native Sent verification result.

Public Git may preserve only public-safe route paths/URLs and aggregate status. Do not publish private recipient addresses or provider message IDs.

## 8. Existing recipient-class rules remain additive

This rule expands, rather than replaces:
- `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md`;
- `governance/FORMER_COUNSEL_PUBLIC_MIRROR_CYBER_RESILIENCE_EMAIL_RULE_26SEP2026.md`;
- media-specific mandatory link/attachment rules;
- recipient-specific evidence/package rules.

If a narrower rule requires two mirrors, two mirrors remain mandatory. This global rule is the minimum floor.

## 9. Prospectivity and legacy sends

Emails already sent before adoption are not automatically reclassified as defective merely because they lacked a Por Derecho URL under a rule that did not yet apply.

Audit them as:
`LEGACY_SENT_BEFORE_GLOBAL_LINK_RULE`

No resend is authorised by adoption of this rule. The **next** authorised message in that thread must comply with this rule.

## 10. Recipient-specific baseline routes identified at adoption

Current public-safe examples include:

- Consejo Canario:  
  `https://sbu001monterecco.github.io/por-derecho/es/consejo-canario-coordinacion-deontologica-2026/`
- ICALPA:  
  `https://sbu001monterecco.github.io/por-derecho/es/icalpa-correspondencia-2025-2026/`
- ICATF:  
  `https://sbu001monterecco.github.io/por-derecho/es/icatf-correspondencia-2025-2026/`
- ICAM / CCACM:  
  `https://sbu001monterecco.github.io/por-derecho/es/cuatrecasas-icam-ccacm-2026/`
  or the broader institutional map where the email is not firm-specific:
  `https://sbu001monterecco.github.io/por-derecho/es/registros-institucionales-colegios-abogacia-2026/`
- CGAE / national Bar coordination: until a dedicated CGAE page is published and live-verified, use the institutional Bar-body map above only if the user expressly approves that interim route; otherwise create a dedicated CGAE landing page before the next send.

Firm-specific existing routes should be preferred over generic institutional maps, including the controlled pages for Cuatrecasas, Garrigues, PwC, RSM/San Telmo, Grant Thornton/Cuyás and other firms where available.

## 11. No-authorisation boundary

A live landing page, public repository update or link selection does not authorise email transmission. The exact-package final-authorisation rule remains controlling.
