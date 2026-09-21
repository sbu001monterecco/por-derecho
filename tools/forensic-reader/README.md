# Forensic Working Document — v1

A dependency-free, local-first bilingual passage-annotation reader. This public directory contains software and a clearly synthetic demonstration, NOT a private case or an evidentiary finding.

## Use

Open `index.html` in a browser. Open a privately preserved `pd.forensic.v1` case JSON, or use a privately supplied standalone populated reader. Select words within one source block, press **Capture selection**, add categories, actors/capacities, issues/proceedings, notes, contrary explanations and evidence links, then save the annotation. Connect annotations across blocks using their IDs. The original source text is not edited.

**Save case + annotations** exports a JSON snapshot. It does not write to GitHub, Drive or GitLab. Save and preserve that file before closing. The page does not persist private content in browser storage. Collaborators should exchange versioned snapshots rather than edit competing copies without reconciliation.

An original PDF can be opened locally only after its SHA-256 matches the case's pinned original hash. Browser WebCrypto requires a supported secure context. A hash proves byte identity, not provenance, signature validity or truth.

## Categories

VERIFY = factual proposition to check; CONTRADICTED = identified documentary contradiction; CONTEXT = omission/context/tension; KNOWLEDGE = knowledge/act/acknowledgment; ADOPTION = adoption or cross-proceeding link; SUPPORTED = corroborated proposition; RHETORIC = rhetoric/legal position. Colour is paired with text labels. Initial paragraph review units are lightly dotted, not certified findings.

A red contradiction requires a source identifier and pinpoint. This is a structural guard, not an automated assessment of the evidence. Reviewed status requires an identified reviewer. Repetition, benefit, shared actors or a hyperlink alone does not establish knowledge, intent or coordination.

## Privacy and limits

No dependencies, analytics, remote upload, automatic source search, cloud synchronization or credential storage. Outbound evidence links open only on user action. Preserve private sources, working analysis and private locators outside public Git, including public branches and PRs. Do not mistake `noindex` or an unlinked path for access control.

This is a focused working tool, not an enterprise e-discovery, multi-user access-control, certified chain-of-custody or legally tamper-proof system. JSON history is editable. PDF image-only regions need separate review; extracted text is not a complete facsimile. No autonomous culpability classifications.

## Verification

The initial private-fixture DOM test passed 16 checks: 22 pages, 181 blocks, 172 provisional annotations, filtering/search, exact-span navigation, unsupported-red rejection, edit history, JSON round trip, insecure-context fail-closed PDF handling, Spanish UI, mobile overflow, word capture, CSV and no script/network errors. These counts describe that private fixture, not public demo contents or complete legal review. Browser navigation was restricted in the build environment; secure-origin native PDF viewing and hosted deployment require separate verification.

The synthetic regression test is `python tools/forensic-reader/test_reader.py`; install Playwright and supply an approved Chromium executable through `CHROMIUM`. It renders content without navigating around browser policy. Run existing repository release gates separately.
