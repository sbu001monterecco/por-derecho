# PWC 2016 TRANSCRIPT / MANDATE PERIMETER / GITHUB PAGES AUDIT

**Date:** 17 August 2026  
**Status:** CONTINUITY AUDIT — PRIMARY-SOURCE RESCAN + REPOSITORY/DEPLOYMENT VERIFICATION

## Purpose

Preserve the results of the 17 August 2026 rescan independently of the originating ChatGPT thread. This audit addresses: (a) the 11 June 2016 PwC/Sun Park meeting transcript; (b) recorder anonymisation; (c) the alleged two uses of `rituales`; (d) Matkator invoicing versus the wider known mandate/client/matter perimeter; (e) PwC Canarias/Tenerife versus Madrid/UK roles; and (f) verification of the PwC/actor-register publication and GitHub Pages deployment.

## A. 11 June 2016 transcript — recovered source family

Connected Google Drive contains at least the following 11 June 2016 transcript derivatives:

- Google Doc ID `SP-PRV-LCTR-GD-57D4661439C25F624CC0` — long HappyScribe transcription;
- Google Doc ID `SP-PRV-LCTR-GD-F02B7DFC102414C22724` — separate transcript derivative;
- PDF transcript derivative, Drive ID `SP-PRV-LCTR-GD-014031C630471470CFBE`.

The original source filenames contain the identity of the Project-side recorder. **Derived/public repository references must not repeat that name.** Canonical description:

> `11 June 2016 PwC / Sun Park meeting transcript — recorded by a Project-side attendee [identity redacted in derived/public references].`

The long transcription is approximately 149 pages in its current derivative and has already been substantially digitised/indexed in the public repository transcript page. This audit does not claim that the original audio itself has yet been recovered.

## B. “rituales” search result

The Project recalled that one speaker used `rituales` twice. The 17 August rescan did **not** verify this in the available transcript text:

- long exported text: 0 exact `rituales` hits; 0 `ritual` stem hits;
- second exported text derivative: 0 exact/stem hits;
- located PDF transcript derivative: 0 exact/stem hits.

**Status:** `UNVERIFIED — ORIGINAL AUDIO REQUIRED`.

Do not manufacture, insert or publish two occurrences simply to conform the transcript to memory. If the original audio is recovered, record exact timestamps, speaker label and surrounding context for both alleged occurrences.

## C. Mandate / client / billing perimeter — primary evidence

### Invoice

The 14 June 2016 Landwell-PricewaterhouseCoopers Tax & Legal Services, S.L. invoice is addressed to **Matkator, S.L.** and totals **€17,606.90** for professional legal advice. It is signed by **Carlos Saavedra Rodriguez, Partner-Director**.

### Work appendix

The contemporaneous PDF `ANEXO FRA. MATKATOR FACTURA MAYO 2016.pdf`, recovered from PwC correspondence, identifies `PwC - Carlos Saavedra y Miguel Hernández` and records substantive legal work on:

- CCPP Sun Park owners and Community documentation;
- legal strategy and limitation periods for unpaid charges;
- mortgage-enforcement effects;
- holiday-home/common-area legal regime;
- litigation evidence;
- Registry documentation and Community debts;
- the Luchy insolvency proceeding;
- possible conflicts connected with Luchy’s parent, transcribed as `Oswell`;
- internal PwC conflict/risk assessment; and
- a Madrid client-risk meeting.

### Transcript opening

The long 11 June transcript opens with a Project-side speaker explaining, in substance, that the work was being conducted at the level of an investment company transcribed as `Oswell`, that a company transcribed as `Macatos` had contracted them, and that they had been sent by `Oswell`.

**Evidence-controlled conclusion:** Matkator is the verified invoice addressee/billing vehicle, but the primary 2016 record supports a substantively wider PwC-known matter/mandate perimeter embracing **Luchy Playa Blanca, Sun Park/Community and the parent/investor perimeter**. The transcript spellings `Oswell` / `Macatos` are transcription candidates for Aweswell / Matkator and must not be silently corrected when presented as quotations.

**Remaining legal-evidence gap:** exact contractual client(s), engagement parties and privilege/confidentiality holders must be established from the engagement letter, KYC/client-acceptance and conflict records. Do not overstate this as a conclusive contractual finding that Aweswell alone was “the client”; equally, do not reduce the known PwC mandate to Matkator merely because Matkator received the invoice.

## D. Which PwC perimeter did the work?

The operative 2016 evidence points to **PwC Spain / Canarias / Tenerife**, including the Landwell-PwC Tenerife invoice and a concentrated `@es.pwc.com` correspondence trail from Miguel Hernández Lorenzo concerning `Luchy Playa Blanca`, `Sun Park`, insolvency obligations, the Matkator invoice and the invoice appendix.

The May appendix records `REUNIÓN EN MADRID. RIESGO CLIENTE`; on the evidence reviewed here, Madrid is best classified as **risk/conflict escalation, coordination and notice unless a separate operational mandate is independently proved**.

PwC UK belongs to a separate/later project source family. It must not be conflated with the 2016 Tenerife legal work. For this track, UK relevance should be treated as separate work and/or notice where primary evidence establishes it, not as proof that PwC UK performed the 2016 Canarias mandate.

## E. Audit of the previously claimed PwC / actor-register work

The following claims were re-opened from `main` and verified:

| Claim | Audit result |
|---|---|
| PwC canonical evidence gate exists | **VERIFIED** — `archive/PWC_LEGAL_PRIOR_ADVISER_KNOWLEDGE_LATER_ADVERSE_POSITION_EVIDENCE_GATE_17AUG2026.md` |
| Full-name actor/party/lawyer register exists | **VERIFIED** — `archive/SUN_PARK_ACTOR_PARTY_LAWYER_REPRESENTATIVE_FULL_NAME_REGISTER_17AUG2026.md` |
| Spanish PwC public page exists | **VERIFIED** — `/es/pwc-legal-asesoramiento-previo-posicion-adversa/` |
| English PwC public page exists | **VERIFIED** — `/en/pwc-legal-prior-advice-adverse-position/` |
| PR #291 was merged | **VERIFIED** |
| Claimed squash commit exists | **VERIFIED** — `df3001926ad6e3447ada1a589b921179e28d50f8` |
| Commit describes PwC gate/page + actor register + bilingual publication/cross-links | **VERIFIED** from the commit metadata/diff |
| 2016 transcript is digitised/indexed in the repository | **SUBSTANTIALLY VERIFIED** — a public transcript/index page exists with 176 extracted entries / approximately 149 pages from the derivative source family |
| Recorder anonymisation was already complete | **NOT VERIFIED / CORRECTION REQUIRED** — the legacy public transcript page and legacy source references expose the recorder’s personal name. New canonical rule is to redact it from derived/public references. |
| `rituales` twice is already verified | **NO** — not found in the available transcript text; audio verification remains open. |

## F. GitHub Pages run 32042769468

The user-supplied workflow run was inspected.

- `build`: **SUCCEEDED**;
- `deploy`: **FAILED**;
- failure mechanism: repeated HTTP **429 Too Many Requests** while GitHub attempted to obtain `actions/deploy-pages` during deployment setup;
- evidential meaning: this was **not a content build failure and not evidence that the PwC/actor pages broke the site**.

Subsequent `main` Pages runs were inspected and succeeded, including the deployment associated with the PwC/actor-register publication (#291). The failed run was therefore superseded by healthy later deployments.

**Canonical conclusion:** do not change site code or workflow merely to “fix” run `32042769468`; its specific failure was transient GitHub rate limiting. Only reopen workflow remediation if a later run shows a reproducible repository/workflow defect.

## G. Corrections / next retrieval gates

1. Remediate the legacy public transcript page so the recorder’s personal name is removed from visible derived/public text while preserving provenance internally.
2. Recover the original 11 June 2016 audio if possible and test `rituales` at audio level.
3. Recover PwC engagement/KYC/client-acceptance/conflict records to determine the exact legal client and engagement parties.
4. Keep the later-adverse-position allegation separately gated: prior paid advice and knowledge are verified; later adverse mandate/conflict/misuse must be proved act-by-act.

## H. Branch carrying this audit

Created on branch:

`agent/pwc-2016-transcript-evidence-pages-fix`

This audit and the strengthened PwC evidence gate are intended to prevent future threads from reverting to the weaker formulations: `Matkator invoice = entire client perimeter`, `PwC UK/Madrid performed the 2016 Canarias work`, or `rituales twice = verified fact`.