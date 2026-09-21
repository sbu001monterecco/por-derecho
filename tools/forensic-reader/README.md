# Forensic Working Document — v1

A dependency-free, local-first bilingual passage-annotation reader. This public directory contains software and a clearly synthetic demonstration, NOT a private case or an evidentiary finding.

## Use

Open `index.html` in a browser. Open a privately preserved `pd.forensic.v1` case JSON, or use a privately supplied standalone populated reader. Select words within one source block, press **Capture selection**, add categories, actors/capacities, issues/proceedings, notes, contrary explanations and evidence links, then save the annotation. Connect annotations across blocks using their IDs. The original source text is not edited.

**Save case + annotations** exports a JSON snapshot. It does not write to GitHub, Drive or GitLab. Save and preserve that file before closing. The page does not persist private content in browser storage. Collaborators should exchange versioned snapshots rather than edit competing copies without reconciliation.

An original PDF can be opened locally only after its SHA-256 matches the case's pinned original hash. Browser WebCrypto requires a supported secure context. A hash proves byte identity, not provenance, signature validity or truth.

## Categories

VERIFY = factual proposition to check; CONTRADICTED = identified documentary contradiction; CONTEXT = omission/context/tension; KNOWLEDGE = knowledge/act/acknowledgment; ADOPTION = adoption or cross-proceeding link; SUPPORTED = corroborated proposition; RHETORIC = rhetoric/legal position. Colour is paired with text labels. Initial paragraph review units are lightly dotted, not certified findings.

A red contradiction requires a source identifier and pinpoint. This is a structural guard, not an automated assessment of the evidence. Reviewed status requires an identified reviewer. Repetition, benefit, shared actors or a hyperlink alone does not establish knowledge, intent or coordination.

## Truth reconstruction / “Liar Liar” mode

Version 1.1 adds a human-reviewed **evidence-constrained restatement** layer on top of the unchanged source and existing annotations. The satire is the entry point; the evidential rule is serious: the tool does **not** decide that an author lied and does not calculate a truth percentage.

For a selected passage the reviewer can record one atomic claim, its current status (`UNTESTED / SUPPORTED / PARTIAL / CONTRADICTED / UNRESOLVED / RHETORICAL_OR_LEGAL`), material omitted context, the real actor/power/capacity question, a knowledge state, the causal bridge and a proposed minimum restatement. A restatement can be `PROPOSED / ACCEPTED / EDITED / REJECTED / UNRESOLVED`.

Fail-closed controls:
- `CONTRADICTED` requires a pinpointed `CONTRADICTS` evidence relation.
- `ACCEPTED` or `EDITED` requires `REVIEWED` status, an identified reviewer and non-empty restatement text.
- The Truth Delta is a count of review states and evidential flags, never a numerical “truth score”.
- Unresolved propositions remain unresolved. The tool must prefer an explicit uncertainty statement over an invented correction.
- AI-generated claim decomposition or restatements, when added later, must enter as proposals only and cannot promote themselves into reviewed case facts.

The current public implementation is deliberately dependency-free and zero-network. A future AI adapter may use local browser inference, a local desktop service, or an explicitly approved remote model, but the evidence/review contract remains the same. See `research/forensic-working-documents-20260921/LIAR_LIAR_READINESS.md`.

## Privacy and limits

No dependencies, analytics, remote upload, automatic source search, cloud synchronization or credential storage. Outbound evidence links open only on user action. Preserve private sources, working analysis and private locators outside public Git, including public branches and PRs. Do not mistake `noindex` or an unlinked path for access control.

This is a focused working tool, not an enterprise e-discovery, multi-user access-control, certified chain-of-custody or legally tamper-proof system. JSON history is editable. PDF image-only regions need separate review; extracted text is not a complete facsimile. No autonomous culpability classifications.

## Verification

The initial private-fixture DOM test passed 16 checks: 22 pages, 181 blocks, 172 provisional annotations, filtering/search, exact-span navigation, unsupported-red rejection, edit history, JSON round trip, insecure-context fail-closed PDF handling, Spanish UI, mobile overflow, word capture, CSV and no script/network errors. These counts describe that private fixture, not public demo contents or complete legal review. Browser navigation was restricted in the build environment; secure-origin native PDF viewing and hosted deployment require separate verification.

The synthetic regression test is `python tools/forensic-reader/test_reader.py`; install Playwright and supply an approved Chromium executable through `CHROMIUM`. It renders content without navigating around browser policy. Run existing repository release gates separately.
