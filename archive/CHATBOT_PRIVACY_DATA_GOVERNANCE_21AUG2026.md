# PRIVACY-FIRST PUBLIC-RECORD AI ASSISTANT — DESIGN / DATA-GOVERNANCE CONTROL

**Control date:** 21 August 2026  
**Repository:** `sbu001monterecco/por-derecho`  
**Status:** IMPLEMENTATION CONTROL — DEPLOYMENT REQUIRES SECRETS / PROCESSOR CONFIGURATION  
**Scope:** public text/audio assistant, source-grounded answers, optional aggregate analytics, Spain/EU privacy controls.

## 1. Purpose

Create a bilingual AI assistant that lets a visitor ask the public Project Sun Rock / Por Derecho record a question by text or microphone while preserving the evidential rules already governing the repository.

The assistant is not an evidential intake system, protected whistleblowing channel, legal adviser, adjudicator or general-purpose web chatbot.

## 2. Core answer architecture

`VISITOR TEXT OR AUDIO → TRANSIENT TRANSCRIPTION IF NEEDED → SITEMAP DISCOVERY → RELEVANT PUBLIC PAGES → SOURCE-CONSTRAINED AI ANSWER → SOURCE LINKS`

The answer prompt requires the model to preserve:

- documented fact;
- attributed account/allegation;
- inference;
- open question;
- missing primary bridge;
- procedural event/status;
- final adjudicated finding only where the source actually establishes it.

Permanent non-conflation rules remain controlling. Relationship, employment, investment, advice, financing, supply, franchise and chronology do not prove knowledge or responsibility. Receipt does not mean endorsement; investigation does not mean guilt.

## 3. Data-minimisation design

### Core chat

Project Sun Rock application storage does **not** persist:

- question text;
- raw audio;
- transcript;
- model answer;
- conversation history;
- IP address;
- persistent visitor/session identifier.

Audio exists only long enough to transmit it for transcription and return the transcript to the visitor. No speaker identification or voiceprint is requested.

### Optional analytics

Analytics is a separately selectable purpose. The assistant continues to work when analytics is refused. The client sends a versioned opt-in flag (`20260821a`) and the backend rejects analytics writes unless that versioned opt-in is present; the stored aggregate records only the count by consent-version, not an identifiable consent profile.

No event-level record is stored. The analytics function updates only a **daily aggregate object** containing counts by:

- text vs audio;
- Spanish vs English;
- broad topic;
- page path;
- answer status;
- source-count bucket;
- broad interest category voluntarily selected by the visitor;
- coarse country code supplied by Netlify geolocation.

Raw question/transcript/answer, IP and persistent ID are not fields in the analytics schema. The admin summary suppresses country and interest cells below three observations.

## 4. Provider / residency controls

### Netlify

Serverless functions are configured for `fra` (Frankfurt, EU). Netlify-level rate limiting is used so the application does not need to create its own IP-based tracking database.

### OpenAI API

- API key is server-side only (`OPENAI_API_KEY`).
- Responses requests set `store:false`.
- Default models are overridable by environment (`OPENAI_CHAT_MODEL`, `OPENAI_TRANSCRIBE_MODEL`).
- The API base is overridable (`OPENAI_BASE_URL`).
- Where an eligible OpenAI API project has European residency / advanced data controls configured, use the endpoint and project configuration required by OpenAI for that region.
- Project Sun Rock must not claim Zero Data Retention merely because the application does not store chats. Provider retention depends on the OpenAI account/project configuration.

## 5. Production deployment gates

Before enabling the assistant publicly, confirm and record:

1. **Controller / records of processing.** Add the assistant and optional analytics to the Article 30/RAT record where applicable.
2. **Lawful basis.** Document the legitimate-interest balancing assessment for minimal user-initiated Q&A; analytics remains separate opt-in consent. Reassess if accounts, persistence, identification or new purposes are added.
3. **Processor terms.** Have current data-processing terms in place with the AI and hosting providers and document subprocessor/transfer safeguards.
4. **Residency / retention.** Decide whether the deployment requires an eligible EU-resident / ZDR or Modified Abuse Monitoring OpenAI configuration and verify the actual endpoint/project before representing that status publicly.
5. **DPIA threshold.** Record a DPIA screening. A full DPIA should be performed if the scale, sensitivity, systematic monitoring or later feature set creates likely high risk.
6. **AI transparency.** Keep the visible AI label and explain that answers are automated and source-constrained.
7. **Cookie/storage rule.** Do not introduce non-essential cookies/localStorage or other terminal-device tracking before consent. The current widget does not persist a visitor identifier or analytics preference.
8. **Security.** Set secrets in Netlify's environment-variable store, not in Git; set a strong `CHAT_ANALYTICS_ADMIN_TOKEN`; keep rate limiting enabled; verify deployment logs.
9. **Content boundary.** The assistant must not solicit confidential evidence, identities or special-category data and must route protected reporting away from the collaboration/chat channel.
10. **Change control.** Any addition of chat history, accounts, email capture, CRM integration, remarketing, user-level analytics or cross-session identifiers requires a fresh privacy/legal review before deployment.

## 6. Environment variables

Required:

- `OPENAI_API_KEY`
- `CHAT_ANALYTICS_ADMIN_TOKEN` (only if the private aggregate dashboard is used)

Recommended / optional:

- `OPENAI_CHAT_MODEL` (default `gpt-5.6-luna`)
- `OPENAI_TRANSCRIBE_MODEL` (default `gpt-4o-mini-transcribe`)
- `OPENAI_BASE_URL` (default standard OpenAI API base; use a regional base only where the account/project is actually configured for it)
- `PSR_PUBLIC_BASE` (default canonical GitHub Pages public-record base)
- `PSR_ALLOWED_ORIGINS` (comma-separated additional front-end origins if the API is called cross-origin)

## 7. Deployment boundary

GitHub Pages cannot execute the server-side functions or safely hold an OpenAI API key. The repository therefore contains the complete front end and backend, but the chatbot must be served through a function-capable deployment such as Netlify or have `window.PSR_CHAT_CONFIG.apiBase` point to an authorised backend origin.

The global loader should not expose a dead chatbot merely because the static GitHub Pages copy exists. Activation is deployment/configuration dependent.

## 8. Insight objective

The compliant objective is to learn **what kinds of questions and audiences the public record attracts**, not to discover the identity of a visitor. If future strategy genuinely requires identified follow-up, create a separate voluntary contact workflow with its own purpose, notice and lawful basis rather than silently converting chatbot telemetry into a lead database.
