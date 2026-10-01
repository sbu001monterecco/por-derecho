# Adverse-party / related-perimeter media archive control — 29 Sep 2026

## Status
ACTIVE CANONICAL MEDIA-ACQUISITION CONTROL.

This control extends, rather than replaces:
- `data/digital-media-asset-register-v1.json`
- `assets/data/sun-park-historic-media-register-v1.json`
- `archive/MEDIA_PUBLIC_NARRATIVE_ACCOUNTABILITY_AUDIT_15AUG2026.md`
- the private Google Drive `Por Derecho Evidence Manifest — live custody register`.

## Purpose
Create a durable, source-specific archive of public representations by, about, or materially connected to the monitored Sun Park / MYND Yaiza / Acosta Matos / Canarian Hospitality / RICPE perimeter, including mainstream media, specialist/trade media, alternative/local media, corporate channels and public social-media posts in the Canary Islands, Spain and relevant international outlets.

The archive is evidentiary and analytical. It is not a blacklist.

## Evidentiary boundary
A publication proves that a representation was published or displayed by the identified source at the captured time. It does **not** by itself prove the truth of the underlying ownership, title, financial, employment, financing, regulatory, intent, coordination, legality or causation proposition.

Every record MUST carry:
1. directly-establishes;
2. does-not-establish;
3. source basis / attribution;
4. acquisition method;
5. completeness limitations;
6. version/capture date;
7. immutable-file hash when available;
8. link to relevant primary-evidence questions.

## Storage architecture
### Private custody — Google Drive
Canonical bytes/render captures belong in the Private Evidence Vault:
`09_ADVERSE_PARTY_MEDIA_ARCHIVE/`

Required capture package where technically and lawfully possible:
- original/canonical URL and redirect chain;
- page/post screenshot (prefer full-page plus key viewport);
- print-to-PDF;
- native HTML/MHTML/WARC when obtainable;
- response/header metadata where available;
- media/image/video originals where lawfully downloadable;
- SHA-256, byte size, MIME type and acquisition timestamp;
- source-basis note;
- version number and supersession relationship.

Never overwrite an earlier capture after a source changes; create a new version.

### Private machine-readable control — GitLab
GitLab carries registers, acquisition logs, source maps, research queues and evidence-boundary controls. Full copyrighted article text should not be mirrored merely for convenience; preserve lawful source captures in the private evidence vault and use metadata, narrow excerpts and analytical summaries in repository records.

### Public mirror — GitHub
GitHub receives public-safe metadata, source links, hashes of separately preserved captures where disclosure is appropriate, and analytical boundaries. It should not become a republication archive of copyrighted articles.

## Capture states
- DISCOVERED_NOT_CAPTURED
- SOURCE_LOCATED
- PUBLIC_RENDER_EXTRACTED
- SCREENSHOT_CAPTURED
- PDF_CAPTURED
- HTML_WARC_CAPTURED
- PRESERVED_NOT_HASHED
- PRESERVED_HASHED
- SUPERSEDED_VERSION
- SOURCE_REMOVED_OR_CHANGED

Only `PRESERVED_HASHED` means an immutable captured file has been byte-identified.

## Source-basis taxonomy
- FIRST_PARTY_CORPORATE
- FIRST_PARTY_SOCIAL
- EXECUTIVE_SOCIAL
- PRESS_RELEASE_OR_COMPANY_STATEMENT
- NEWSWIRE
- NEWSROOM_REPORT
- INTERVIEW
- TRADE_MEDIA
- SPONSORED_OR_COMMERCIAL_CONTENT
- SYNDICATED_OR_REPUBLISHED
- OFFICIAL_PUBLIC_RECORD
- THIRD_PARTY_SOCIAL
- ARCHIVE_COPY
- SOURCE_BASIS_UNRESOLVED

Source basis must be recorded separately from publisher prestige or reach.

## Monitored entity/topic perimeter
Initial entity and topic keys include:
- Grupo Acosta Matos / Construcciones Acosta Matos;
- Canarian Hospitality;
- MYND Hotels / MYND Yaiza;
- Sholeo Lodges;
- RIC Private Equity / RIC Capital;
- Hotel New Trend;
- Radisson projects where the monitored perimeter is named;
- identified individual public spokespeople/executives when they publish or are interviewed;
- Sun Park / Playa Blanca / Lanzarote;
- RIC, regional incentives, FEDER/EU funding, hotel acquisition/reform, ownership/operator/manager representations, employment, investment, expansion, sustainability and public-institutional endorsements.

Actor status (adverse / witness / related / neutral) MUST come from the canonical actor register or an explicit controlling instruction. A media appearance alone never assigns adverse status.

## Priority outlet map
Retain the pre-existing media-audit tiers and broaden discovery:
- Canary/Lanzarote: Canarias7; La Provincia; Diario de Avisos; Atlántico Hoy; La Voz de Lanzarote/EKN; Diario de Lanzarote; Canarias Empresarial; Canarias Noticias/Noticias Canarias; SER Canarias/Lanzarote; RTVC/Televisión Canaria.
- Spain/trade: HOSTELTUR; Cinco Días; elEconomista; Europa Press; Forbes España/Forbes Travel; Preferente; Tourinews and other tourism/investment trade press.
- First-party/social: Canarian Hospitality, Grupo Acosta Matos, RICPE/RIC Capital, MYND, Sholeo and relevant executive LinkedIn/corporate pages.
- International: Radisson and international hospitality/travel/investment media where the same projects or actors appear.

## Discovery and de-duplication rule
Do not count five rewrites of one press release as five independent confirmations. Cluster materially similar items by:
- announcement/event;
- originating statement/release;
- publication time;
- distinctive wording;
- supplied photographs;
- quoted spokesperson;
- outbound links.

Maintain both:
1. publication-level records (who published what); and
2. source-family records (what appears to be the originating information package).

## Social-media capture rule
For LinkedIn and similar platforms capture, where visible:
- account/display name;
- canonical post URL/activity ID;
- exact visible date/time or platform timestamp;
- text;
- edit marker;
- outbound link card;
- images/video;
- visible reactions/comments/share counts;
- referenced/reposted parent item;
- screenshot(s) showing the account identity and post together.

A search-engine/public-render extraction is a discovery copy, not a substitute for a native rendered screenshot.

## Versioning rule
If a page/post changes, disappears, is edited, or its headline/image/byline changes:
- preserve the prior capture;
- create a new version;
- record discovery time and material differences;
- never silently replace prior evidence.

## Seed acquisition — 28 Sep 2026 strategic-plan publication
Private Evidence Manifest:
- `MEDIA-CE-20260928-001` — Canarias Empresarial article.
- `MEDIA-CE-20260928-002` — Canarias Empresarial LinkedIn promotion.
Both are currently SOURCE-LOCATED / WEB CAPTURE / DERIVATIVE pending native screenshots/source bytes and hashing.

The same announcement has been discovered in additional outlets and is queued for source-family de-duplication before evidentiary weight is assigned.

## Completion test
A publication is GREEN only when its source identity, date, URL, source basis, capture package, SHA-256/size (where immutable bytes exist), directly-establishes, does-not-establish, version status and primary-evidence cross-links are all resolved. Discovery alone is not GREEN.
