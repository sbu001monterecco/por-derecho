# Thread deletion audit — San Telmo / RICPE / Sun Park attribution and website correction

**Original audit date:** 19 August 2026  
**Closure date:** 20 August 2026  
**Project:** Por Derecho / Project Sun Rock  
**Final status:** **SAFE TO DELETE**

## 1. Material correction now locked

The bilingual homepage interview section had attributed the statement “nosotros en el despacho … metimos unos cuantos clientes” to Enrique Guerra and described Eduardo Sánchez only as interviewer/recipient.

The source-controlled attribution is now locked as follows:

- **Eduardo Sánchez** is the speaker of the client-introduction statement at **08:08–08:12**;
- **“Enrique Guerra, en #UnCaféenSanTelmo”** is the programme title and identifies Guerra as guest;
- the wider project statements by Guerra remain separate from Sánchez’s quotation;
- the video establishes the quotation; the RICPE–Sun Park identification relies on separately cited records;
- the material does not by itself establish client allocation specifically to Sun Park, coordination, transfer or misuse of insolvency information, unlawfulness or liability.

## 2. Website and repository changes preserved

The repository now contains:

- a rendered English and Spanish homepage correction loaded through `assets/site.js`;
- the dedicated bilingual correction asset `assets/san-telmo-attribution-correction-20260819.js`;
- rebuilt English and Spanish San Telmo–RICPE–Sun Park dossier pages;
- a proposition-by-proposition evidence ledger;
- an explicit clarification that the image’s “same asset” wording means the same hotel complex / connected project perimeter, not one undivided legal asset or the whole LPB insolvency estate;
- preservation of Matkator and third-party perimeter distinctions;
- primary-source timecodes and transcript-page references;
- GitHub Pages canonical and social-sharing metadata;
- the dedicated bilingual `sitemap-san-telmo.xml` and `robots.txt` registration;
- repository regression validation, exact-marker HTTP verification and rendered-browser verification;
- a right-of-reply and equal-prominence correction route.

The approved image was retained unchanged.

## 3. Deliberate implementation choice

The large pre-existing homepages are corrected at render time through the common site loader rather than being rewritten wholesale. This reduced collision risk with concurrent homepage work while ensuring that public readers receive the corrected attribution. The correction asset replaces the complete visible interview section, not merely a footnote.

Because the correction is rendered by JavaScript, source availability alone was not treated as the final proof. The repository now also opens the live English and Spanish homepages in headless Chrome and verifies the post-JavaScript DOM that a reader receives.

## 4. Merge and validation lineage

### PR #552 — substantive website correction

- PR: `https://github.com/sbu001monterecco/por-derecho/pull/552`
- merge SHA: `d1d17da58006b12a07493ee5e3e6e1a2de98338f`
- result: merged after the publication-integrity and repository validation checks passed;
- effect: corrected rendered homepage attribution, rebuilt both dossier routes, added source boundaries, discovery controls and deletion-audit handoff.

### PR #555 — durable live-verification status

- PR: `https://github.com/sbu001monterecco/por-derecho/pull/555`
- merge SHA: `2a72e8fe166f1b0fd1ef26dd5fdd9a226b35b2d1`
- result: merged after the publication-integrity gate and off-GitHub preservation snapshot passed;
- effect: authorised status-only write access for the exact San Telmo public-edge verifier under the mission-critical workflow allowlist and made the result durably observable as `pages-propagation/san-telmo-attribution`.

### PR #557 — rendered-browser verification

- PR: `https://github.com/sbu001monterecco/por-derecho/pull/557`
- merge SHA: `b3234f22fd9f8ce60525e16245396708357356ed`
- result: merged after the publication-integrity gate, San Telmo regression validation and off-GitHub preservation snapshot passed;
- effect: added a Playwright/Chrome public-edge check for both rendered homepages and made the durable San Telmo status depend on both source-level and rendered-DOM success.

## 5. Source-level public-edge verification

Workflow run `32313398051` completed successfully on its first attempt at `2026-08-19T23:28:42.286038+00:00` against merge SHA `2a72e8fe166f1b0fd1ef26dd5fdd9a226b35b2d1`.

The verifier confirmed HTTP 200 and all required exact markers for:

| Public resource | Bytes | Result |
|---|---:|---|
| `/assets/site.js` | 7,090 | PASS |
| `/assets/san-telmo-attribution-correction-20260819.js` | 6,368 | PASS |
| `/en/san-telmo-ricpe-sun-park/` | 10,290 | PASS |
| `/es/san-telmo-ricpe-sun-park/` | 10,450 | PASS |
| `/sitemap-san-telmo.xml` | 1,237 | PASS |
| `/robots.txt` | 2,032 | PASS |

## 6. Rendered-homepage verification closure

Workflow run `32313962301` completed successfully against merge SHA `b3234f22fd9f8ce60525e16245396708357356ed`.

The workflow first repeated the source-level verification successfully on its first attempt. It then used Playwright with Google Chrome `151.0.7922.137` and recorded `RENDERED_DOM_LIVE_VERIFIED` at `2026-08-19T23:36:49.661Z`.

### English homepage `/en/`

The real rendered DOM returned HTTP 200 and confirmed:

- `data-pd-san-telmo-attribution="20260819"` was applied;
- “Speaker correction.” was present;
- “Eduardo Sánchez” and `08:08–08:12` were present;
- “The programme title identifies Enrique Guerra as the guest” was present;
- the former stale attribution to Guerra and the former description of Eduardo as merely interviewer/recipient were absent;
- the dossier button resolved to `/por-derecho/en/san-telmo-ricpe-sun-park/`;
- the primary source resolved to `https://www.youtube.com/watch?v=mHn9IJU0qI4&t=488s`.

### Spanish homepage `/es/`

The real rendered DOM returned HTTP 200 and confirmed:

- `data-pd-san-telmo-attribution="20260819"` was applied;
- “Corrección de atribución.” was present;
- “Eduardo Sánchez” and `08:08–08:12` were present;
- “El título del programa identifica a Enrique Guerra como invitado” was present;
- the former stale description of Eduardo as merely interviewer/recipient was absent;
- the dossier button resolved to `/por-derecho/es/san-telmo-ricpe-sun-park/`;
- the primary source resolved to `https://www.youtube.com/watch?v=mHn9IJU0qI4&t=488s`.

The workflow published the durable success status:

- context: `pages-propagation/san-telmo-attribution`;
- state: `success`;
- description: `San Telmo attribution and rendered homepages verified live`;
- target run: `https://github.com/sbu001monterecco/por-derecho/actions/runs/32313962301`.

## 7. Canonical public routes

- English: `https://sbu001monterecco.github.io/por-derecho/en/san-telmo-ricpe-sun-park/`
- Spanish: `https://sbu001monterecco.github.io/por-derecho/es/san-telmo-ricpe-sun-park/`

## 8. Continuing evidential rules

No later thread should reverse these boundaries without a source-backed repository change:

- quotation ≠ proof of the precise destination of every introduced client;
- professional association ≠ coordination;
- project connection ≠ transfer or misuse of insolvency information;
- unanswered question ≠ established wrongdoing;
- silence ≠ admission;
- “same asset” in the retained image means the same hotel complex / connected project perimeter and does not erase the distinct LPB, Matkator or third-party legal perimeters.

## 9. Deletion verdict

All material attribution decisions, evidential boundaries, implementation choices, public routes, repository validation controls, source-level live checks, rendered-browser verification, merge identities and live-verification evidence now exist outside this chat thread in the repository and public website.

**SAFE TO DELETE THIS CHAT THREAD.**
