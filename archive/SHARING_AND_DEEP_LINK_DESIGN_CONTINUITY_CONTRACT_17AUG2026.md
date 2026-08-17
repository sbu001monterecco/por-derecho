# SHARING AND DEEP-LINK DESIGN CONTINUITY CONTRACT

**Control date:** 17 August 2026  
**Status:** CANONICAL NON-REGRESSION CONTRACT FOR FUTURE REDESIGNS

## Purpose

Sharing is a canonical Por Derecho capability, not legacy UI. Future redesigns may change typography, layout, component names, framework, CSS and JavaScript, but must preserve or improve the user capability and editorial logic recorded here.

## Capabilities that must survive

Future design must preserve or improve:

- LinkedIn sharing;
- WhatsApp sharing;
- Email sharing;
- Copy Link;
- canonical URL handling;
- contextual sharing;
- stable deep-link sharing;
- evidence/proposition sharing;
- ES/EN parity;
- social-preview metadata;
- mobile and keyboard accessibility;
- privacy-preserving implementation without unnecessary social SDKs or trackers.

## Required design family

The design system must be able to express four related modes:

1. **Page Share** — whole-page circulation.
2. **Context Share** — an important section, comparison or finding.
3. **Evidence Share** — a specific evidential object.
4. **Deep Link** — an exact stable anchored location.

The presentation may change. These capabilities must not silently disappear.

## Behavioural sequence

Preserve the editorial sequence:

**important content → comprehension → recognition that another person may need to see it → immediate sharing opportunity → exact destination**

Use value before asking for a share. Do not manufacture emotion or introduce dark patterns. Appropriate behavioural principles are salience, consistency, proximity, low cognitive load, social utility, timely presentation and immediate feedback.

Do not use fake urgency, fake scarcity, fabricated share counts, guilt, obstructive prompts, repeated popups, addictive streaks or deceptive controls.

## Current design baseline

The 17-Aug-2026 baseline grows out of the established book-page pattern: compact `LinkedIn · WhatsApp · Email · Copy link` controls, visually subordinate to the evidence/content, with the flagship book share placed after its thesis and before its navigation actions.

A redesign does **not** have to look like that page. It must understand what the interaction achieves before replacing it.

## Canonical URL rule

- Whole-page sharing uses the declared canonical URL.
- Evidence/context sharing uses `canonical URL + intentional stable anchor`.
- Do not propagate preview URLs, branch URLs, development URLs, tracking parameters, incidental query strings or temporary fragments.

## Exact-object sharing

The long-term architecture should make discrete investigative objects directly citeable and shareable, including ACTAs, judicial acts, authority propositions, ownership propositions, debt propositions, voting/quorum propositions, transactions, funding representations, institutional responses, timeline events, document comparisons and evidence cards.

Where canonical IDs exist, preserve them through redesigns. Presentation identity may change; evidential identity should remain stable.

Examples include namespaces such as `AUTH-*`, `ACTA-*`, `DEBT-*`, `OWN-*`, `UNIT-*`, `VOTE-*`, `AC-*`, `JUD-*`, `PUB-*`, `TXN-*`, `FUND-*` and `ASSET-*`.

## Share-object model

Where technically appropriate a shareable object should expose:

- stable ID;
- canonical URL;
- optional stable anchor;
- human-readable title;
- concise description;
- source/evidence context;
- language;
- share payload;
- optional social image.

Prefer structured metadata over duplicated hard-coded URLs.

## Copy Link is a professional primary action

Copy Link must remain easy to discover for lawyers, journalists, investigators, officials, researchers and advisers. Future variants may include:

- Copy link;
- Copy section link;
- Copy evidence link;
- Copy timeline point;
- Copy proposition reference.

## Social metadata is part of design

Priority pages should preserve or improve title, description, canonical, `og:title`, `og:description`, `og:url`, `og:image`, `og:type`, hreflang and relevant social-card metadata. A redesign must not collapse materially different pages into one generic preview.

## Mobile, accessibility and privacy

The critical mobile journey is **read → tap → send**. Maintain sensible touch targets, wrapping, focus states and feedback. Preserve keyboard access, visible focus, semantic links/buttons and screen-reader labels.

Prefer local URLs, local JavaScript and native browser APIs. Do not introduce third-party social SDKs where normal links achieve the purpose.

## ES / EN parity

Any redesigned share component must support both languages from inception. Do not leave one language on materially inferior legacy behaviour.

## Non-regression gate for redesigns

Before merging any future redesign, explicitly verify:

- page sharing still works;
- WhatsApp still creates useful text;
- Email still creates useful subject/body;
- LinkedIn receives the correct canonical URL;
- Copy Link works;
- existing stable deep links remain resolvable or are redirected/mapped;
- proposition/evidence IDs remain stable;
- ES/EN parity remains;
- Open Graph previews are preserved or improved;
- mobile/accessibility are equal or better;
- no share capability silently disappeared.

If an existing capability genuinely cannot be migrated immediately, record it explicitly as `TEMPORARY DESIGN REGRESSION` with the affected feature, reason and replacement path. Do not quietly drop it.

## Future development opportunities

A future design should look for ways to strengthen this system, for example:

- stable evidence-card permalinks;
- proposition permalink controls;
- shareable timeline events;
- claim-versus-record comparison objects;
- section-specific WhatsApp/email payloads;
- dynamically generated Open Graph images;
- citation/reference formatting;
- print-friendly evidence references;
- QR links where they genuinely help physical presentations or documents.

These are progressive enhancements, not permission to add visual clutter.

## Deletion/continuity test

Before closing a redesign thread, ask:

> If all prior chats disappeared, could a new agent open `main`, discover that sharing/deep linking is a canonical capability, understand the current implementation and know which behaviours must survive and be developed further?

If not, redesign continuity is incomplete.

## Enduring principle

The enduring goal is not to preserve four buttons. It is to preserve and improve this capability:

> **Any important page, proposition, document, chronology point or evidential object should be easy to circulate to the right person, with the correct context, in the correct language, using a stable link.**

Every redesign should make that capability stronger.
