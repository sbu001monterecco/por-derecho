# Por Derecho media dashboard — continuity and deployment plan

**Control:** PD-MEDIA-DASHBOARD-20260905-01  
**Date:** 5 September 2026  
**State:** private local prototype and public-safe review previews; no new dispatch, production release, authentication service or background monitoring.  
**Read source main:** `e482e29325091bcc32af3fd2b2624335c6699e19`  
**Integration:** WORKER under PD-MTCP-20260904-01; coordinate through Control Tower #1428 and existing media rules task #1462. This plan does not acquire an integration lock.

## Continue the existing system

Read `AGENTS.md`, `CHATGPT_START_HERE.md`, `MEDIA_CAMPAIGN_NEW_THREAD_START.md`, `ops/CURRENT_COLLABORATION_STATE.json`, current Control Tower comments, and these controls:

- `CHATBOT_MEDIA_INQUIRY_DESK_CONTROL_28AUG2026.md`: **Ask the Record / Pregunta al expediente**, PD-CHATBOT-MEDIA-DESK-20260828-01.
- `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md`.
- `archive/OUTBOUND_WEBSITE_LINK_MANDATORY_RULE_23AUG2026.md`, including the worker reinforcement PD-MEDIA-LINK-20260905-01 after integration.
- `archive/OUTBOUND_MEDIA_CORE_PACKAGE_MANDATORY_RULE_23AUG2026.md`.
- `archive/PRE_SEND_GMAIL_PERSON_OUTLET_HISTORY_GATE_23AUG2026.md`.
- `archive/MAXIMUM_MEDIA_DISTRIBUTION_MULTI_RECIPIENT_RULE_23AUG2026.md`.

The older inquiry-desk specification is not a recovered runnable chatbot. This dashboard adds operational continuity and a public documentary entrance. It does not implement AI, voice or an authenticated inquiry service; this static scope requires no API credential.

Earlier current/not-sent/ready/awaiting-response notes are dated snapshots. Refresh the mailbox before acting. The earlier missing-website/core package remains an historical packaging failure despite successful transmission. A later supplement is a separate event.

## Two outputs: separate before publishing

**Private operational dashboard:** outlet, person, exact endpoint, source message, campaign membership, actual send, Sent-copy verification level, delivery incident, reply, next action, controlled links and attachment manifest. The supplied local HTML/CSV/JSON/workbook is a manually generated snapshot. It has no authentication, synchronization, send action or monitoring. It is private only by custody and must not be uploaded to a public host or attached to media emails.

**Public source desk:** approved documentary entry points, source-reading guidance, corrections and material cleared for publication. The ES/EN review previews contain no recipient directory, mailbox correspondence, provider locator, response content or campaign-performance metric. They have no form, tracking or mail action. English text labels Spanish sources rather than inventing English slugs.

The repository contains `.nojekyll` and is a static site. Preserve its current Pages/build mode; do not introduce Jekyll/Liquid or another deployment workflow. Frontend hiding, noindex or a JavaScript password is not private access control. Any later private service must enforce access on the server/storage.

Proposed public routes, **not certified live**: `/es/medios/` and `/en/media/`. The integrator must inspect the full current route/navigation/search/sitemap inventory first. Extend an existing canonical media/press entrance if one exists, rather than create a competing route. Preserve base path `/por-derecho/`.

## Data and event model

Keep these objects distinct:

| Object | Minimum fields and invariant |
|---|---|
| Outlet | Stable ID, name, geography, sections and historical aliases. |
| Person | Name, role as of its source date, outlet relation. Old role is not current role. |
| Endpoint | Exact normalized address, route type, person/outlet link, historical source, current verification, suppression reason. Several addresses do not mean several people. |
| Message event | Existing canonical ID after reconciliation, private native locator, actual time/offset, direction, recipients and campaign/package relation. |
| Send verification | Separate sender/recipient/body-link, attachment-metadata, and downloaded-byte checks. Metadata is not byte-for-byte verification. |
| Delivery event | Sender acceptance, rejection, acknowledgement, personal reply and editorial decision are separate facts. |
| Editorial response | Source, question or condition, requested channel, restrictions and next action. Silence is not acceptance. |
| Package | Actual body, mandatory links, versioned files/sizes/hashes, evidence limits, privacy review and exact approval. |
| Inquiry | Verified journalist, actual question, proceeding/source links, deadline, draft and review state. Future authenticated feature only. |
| Snapshot | As-of date/time, source ranges, completed queries, remaining cursors, inherited versus fresh checks, explicit omissions. |

Append events and preserve native records privately. Match existing communications, proceedings and source IDs before allocating new canonical records. Do not derive public canonical events from contact counts or aggregate claims. Backfill of individual campaign events remains open until actual canonical reconciliation is performed.

## Private checkpoint and honest coverage

The previous private campaign audit has 62 addresses: 58 individual sends, 4 prior-failure exclusions, 2 current delivery failures, 2 receipt acknowledgements and 54 other deliveries unconfirmed at its cutoff. These figures are one campaign, not all media correspondence and not a fresh readback of all 58 messages in this update.

The working directory is extended to 68 with six recoverable historical addresses from four additional media organisations. They are not retrospective members of that campaign or newly authorised recipients. Two existing newsroom endpoints specifically requested by the user were re-read and retained without duplication. One recovered contact is an institutional/designated-channel contact at a media company, not automatically a reporter.

Five preliminary references that could not be recovered are quarantined outside the confirmed directory. Two international specialist-media findings remain outside the Canary/Spain count. Promotional lists, corporate PR, family, advisers, newsletters, NGO press routes and mere mentions in forwarded bodies are not silently converted into journalist endpoints.

The search included Canary, national, sectoral, platform and blog/regional domains, named terms and historical press-release subjects. Some broad queries retain continuation cursors in the private coverage record. This is not an exhaustive mailbox audit. No additional verified blogger endpoint was established by the scoped blog-domain check. Zero results mean only that a query located nothing.

Where a publisher invited later court or administrative decisions, the next draft must answer that condition with exact decisions and limits. Where a designated institutional channel was requested, retain it separately from editorial contact. Neither is simple silence. None of the new private recipient addresses or actual provider identifiers belongs in this public file.

## Mandatory body and attachment controls

For a Spanish Sun Park/MYND media update, the actual new email body must visibly contain the website entry, relevant topic landing, judicial/institutional access routes when describing records online, and the controlled webinar:

- `https://sbu001monterecco.github.io/por-derecho/es/`
- `https://sbu001monterecco.github.io/por-derecho/es/ric-private-equity-sun-park/`
- `https://sbu001monterecco.github.io/por-derecho/es/reconstruccion-unitaria-autoridades-publicas/`
- `https://sbu001monterecco.github.io/por-derecho/es/registros-institucionales/`
- `https://www.youtube.com/watch?v=mHn9IJU0qI4&t=488s`

A PDF-only link, quoted prior email, external official-source link or GitHub source file does not replace the actual-body website requirement. Recheck source access and relevant fragments at readiness; a cached browser page is not deployed-byte verification.

The approved campaign pack used the original documentary PDF, PwC map, San Telmo/RICPE map and existing `pd-dma-0003-web-email-es.png` spoof. Preserve bytes, versions and provenance; do not generate a new image. The spoof is satire, not evidence of a transaction. Source maps are not independent expert or judicial findings. Future changes require the standing core controls and exact package approval.

Explain that the public site links chronology, proceedings, decisions, submissions, responses and publishable supporting references. Distinguish public copies, redacted versions, summaries and pending/private documents. Do not claim all complete dockets are public or that an authority endorses the project's position.

Preserve the unitary account and attributed allegations while keeping distinct entities, proceedings, assets and branches separate. Ownership, operation, private investment, fiscal incentives, grant awards and adjudicated responsibility are different propositions. Keep adverse decisions and material alternative/exculpatory explanations visible.

## Deployment stages and acceptance

### A. Private local dashboard

Deliver search/filterable HTML, source-linked workbook, CSV/JSON, campaign denominators, pending actions, links and attachment hashes. Keep it local; no login, synchronization, secret or send button is implied. A refresh generates a new version rather than silently mutating an old sent record.

Accept only after unique endpoint and duplicate checks, six newcomers outside the prior campaign, exact preservation of the 62-row source CSV, reconciling state counts, no failed/unrecoverable endpoint labeled ready, HTML escaping, functional browser search/filter/export, and desktop/mobile review. File navigation is restricted in the model browser, so local browser testing uses the exact HTML loaded as content; it is not a production URL or deployed-file access test.

### B. Public static source desk

The active integrator refreshes main and reconciles the existing media-rule worker delta, inventories routes, selects the canonical entrance, applies the current shared navigation/footer/accessibility controls and adds reciprocal links, search and sitemap entries. Preserve all existing material, source IDs and the canonical communications register.

`public_projection.py` accepts only a finite reviewed source-ID configuration. It rejects extra fields/private URLs and never reads the operational register. Release is blocked by default; approval fields are operator assertions, not proof of approval. A successful projection proves neither factual accuracy, live access nor deployment. No public correspondence metrics or outlet-level response statuses are part of this release.

The ES/EN HTML files are review prototypes with explicit not-deployed banners, not finished production routes. They have no private data or active forms. Approve final public wording and page navigation separately before converting them into a release.

Required checks: privacy across commit diff, output HTML/JSON/JS, source maps, Actions logs and artifacts; no recipient-address hashes masquerading as anonymisation; ES/EN meaning and source-language labels; functional topic/court/institutional links; accurate privacy notice; no unexpected forms/network calls/analytics; full-tree preservation checks and actual deployed readback. Do not claim every source file is public merely because its reference appears.

Only the active integrator opens/merges the publication PR. Record source main, exact delta, full relevant CI, merge SHA, Pages run and readback of actual public pages, language switching and source links. Worker commits and scoped tests are not deployment.

### C. Authenticated internal CRM and inquiry desk

Choose and approve private persistent storage/hosting before migration. Require server-side authentication, role-based access, least privilege, audit, backup/restore, retention, deletion and incident handling. Mailbox/API credentials stay server-side outside this repository. No private data import is public-release permission.

Integrate the existing Ask the Record method: Source → Authority → Perimeter → Contradiction → Consequence → Reversibility. Preserve direct answer, evidence status, project position, contrary record, significance, exact sources, missing evidence and next route. Private release to a journalist, anonymous Q&A publication and attributed publication require separate approvals. No automatic email, filing or public answer. AI/voice remains a separately tested later scope.

### Rollback and closeout

Record pre-release main and the public projection version. Roll back only the new approved public view/navigation delta; never rewrite mailbox history. Failed delivery or uncertainty does not trigger another send. Close only after changed paths, tests, public-data review, merge, Pages and live verification are recorded, with remaining gaps.

## Validation and resumption

Run `python3 -m unittest discover -s ops/media-dashboard -p 'test_public_projection.py' -v`. Tests use synthetic input, never private mailbox fixtures. Local tests do not certify full repository CI, current public access or canonical register backfill.

Private deliverables and their checksums are in the owner-only handover archive, not this repository. Keep that archive under owner-controlled storage, never in a PR, public issue or Pages artifact. Older upload references may expire; the baseline audit and exact attachment ZIP were available for this update, so no replacement upload was needed for them. Availability in a transient runtime is not durable archival certification.

**No new emails, Gmail drafts, authority contacts, merge or production deployment are authorised or performed by this plan.**
