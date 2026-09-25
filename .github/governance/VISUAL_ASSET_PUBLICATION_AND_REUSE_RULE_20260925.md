# Visual asset publication and reuse rule

**Effective:** 25 September 2026
**Scope:** Por Derecho / Project Sun Rock website, GitHub/GitLab continuity and social-publication work.

## Purpose
A visual prepared for a public evidential, explanatory or institutional-accountability page is a **publication deliverable**, not merely a disposable chat output. Once approved for public use, the workflow must carry it through to a website-servable asset unless a specific privacy, provenance, legal or technical gate blocks publication.

## Default workflow
1. Preserve the native/source image privately.
2. Create a public-safe derivative when necessary.
3. Run privacy review before public ingress: remove home/postal addresses (including Cabildo/home postal address), identity numbers, private emails/phones, signatures, bank identifiers, credentials, private provider locators and other unnecessary personal data.
4. Run evidential review: an image/portrait is an identity or explanatory aid only unless the underlying source independently proves the proposition. Do not use a visual association to imply coordination, knowledge, wrongdoing, causation or liability.
5. For public web delivery, store an approved byte-locked asset in the website repository under `assets/media/` or the existing evidence-specific asset path. Do not rely on a Google Drive link as the production image source.
6. Prefer a high-quality PNG master for graphics/text-heavy infographics and portraits requiring lossless delivery. Add a WebP derivative where it materially improves page weight. HTML should use responsive dimensions, meaningful alt text and lazy loading below the fold.
7. Register filename, dimensions, SHA-256, provenance/status, page placement and publication boundary in the applicable visual/digital-media asset registry.
8. Embed the asset in the intended ES/EN page(s), with a visible caption/source boundary where appropriate. Do not create unnecessary duplicate dossier pages.
9. Validate: repository byte exists; page references resolve; public host returns HTTP 200; rendered image has expected dimensions/content; ES/EN placement is coherent; no prohibited personal data is exposed.
10. Preserve a private continuity copy in Google Drive and mirror the source-control metadata/manifest to GitLab. Where binary mirroring is technically unavailable, mark it AMBER rather than pretending completion; this must not block publication from the canonical website repository once the approved binary has entered that repository.

## Publication presumption
If a visual was expressly prepared and approved for the website, **non-use requires a recorded reason**. Acceptable reasons include unresolved privacy/PII, uncertain provenance/rights, identity ambiguity, evidential overstatement, supersession by a better approved visual, or a concrete technical failure.

## RICPE / MYND application
The current RICPE/MYND visual programme should be used on the existing canonical pages, not left as a Drive-only archive. The preferred structure is:
- thesis/financial-lives infographic on the Series F/G / idoneidad thesis page;
- cross-link or responsive reuse on the multiple-financial-lives page;
- webinar/2020→2021 representation visual on the webinar/main RICPE evidence route;
- CNMV enforcement-status visual/block on the CNMV verification route.

Person portraits supplied for the webinar/representation visual remain source-attributed visual aids. Publication does not convert a portrait into proof of the surrounding allegation.

## Gate
No public page may expose the Cabildo/home postal address or other unnecessary personal information. This privacy gate is mandatory and takes priority over speed.
