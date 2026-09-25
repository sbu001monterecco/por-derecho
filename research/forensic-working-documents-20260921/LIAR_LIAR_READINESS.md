# Liar Liar / Truth Reconstruction — technology and readiness review

**Date:** 21 September 2026  
**Scope:** architecture research for the Por Derecho Forensic Working Document. This is not a vendor endorsement, procurement decision, factual finding about any case, or authorization to upload case material to a third party.

## Product rule

The memorable surface may say **Liar Liar**. The professional engine is **evidence-constrained restatement**.

The system must never infer “the author lied” from contradiction alone. Its job is to make every material proposition carry the evidence, contrary evidence, actor/capacity, chronology, knowledge state, causal bridge and uncertainty necessary for a defensible restatement.

## Patterns worth importing

### 1. AI proposes; humans promote
Casefleet's current Proposed Facts workflow requires an AI-proposed fact to have a source citation and requires the user to accept it before it becomes a case fact. Its newer drafting workflow also presents verified citation badges alongside generated drafting. This is the right control pattern for our claim decomposition and restatement layer.

- https://support.casefleet.com/en/articles/13057134-using-the-ai-assistant-to-create-facts
- https://support.casefleet.com/en/articles/16442382-draft-with-verified-citations-in-casey

Everlaw Storybuilder similarly connects specific document highlights and testimony to Facts and makes the curated evidence available to writing/analysis tools.

- https://support.everlaw.com/hc/en-us/articles/14988585590939-Add-Evidence-to-your-Story
- https://support.everlaw.com/hc/en-us/articles/42469701435803-Storybuilder-Fact-Timelines
- https://support.everlaw.com/hc/en-us/articles/25402606829083-Storybuilder-and-Writing-Assistant

Relativity Case Strategy extracts **potential** facts and builds draft chronologies/witness material rather than treating model output as established fact.

- https://help.relativity.com/RelativityOne/Content/Relativity/aiR_for_Case_Strategy/aiR_for_Case_Strategy.htm

### 2. Keep the original immutable and produce a separate derivative
Microsoft Word's legal-blackline model is conceptually useful: compare original and revised versions in a third document while the originals remain unchanged. Our “truth-telling edition” should work the same way: source unchanged, derivative restatement separately reviewable.

- https://support.microsoft.com/en-us/word/compare-document-differences-using-the-legal-blackline-option
- https://support.microsoft.com/en-us/word/compare-and-merge-two-versions-of-a-document

### 3. Browser-local AI is now practical
Transformers.js v4 and ONNX Runtime Web support in-browser model execution and WebGPU acceleration. WebLLM provides browser-native LLM inference, structured JSON generation and worker support. These technologies make a private optional local inference tier technically realistic.

- https://huggingface.co/blog/transformersjs-v4
- https://huggingface.co/docs/transformers.js/guides/webgpu
- https://onnxruntime.ai/docs/tutorials/web/ep-webgpu.html
- https://webllm.mlc.ai/docs/
- https://github.com/mlc-ai/web-llm

**Readiness decision:** do not bundle a large model into the v1.1 public reader. First stabilize the schema, proposal gate and evaluation harness. Later add AI through an adapter so the same JSON contract can be served by a browser model, a local desktop service or an explicitly approved remote model.

### 4. Provenance should be first-class
W3C PROV models entities, agents, activities and derivation. RO-Crate provides a JSON-LD packaging model for research objects. We do not need to adopt either wholesale immediately, but the future export should be able to answer: which source span produced which claim, which evidence altered its state, which activity generated a restatement and which reviewer accepted it.

- https://www.w3.org/TR/prov-o/
- https://www.w3.org/TR/prov-overview/
- https://www.researchobject.org/ro-crate/specification

### 5. Verification must be a separate gate from generation
Recent claim-verification research reinforces the need for a separate verifier. A 2025 survey identifies continuing weaknesses in veracity annotation and claim decomposition. RefNLI shows that entailment/contradiction models can misfire badly when two passages only appear to refer to the same context. Therefore no NLI score may directly create a red contradiction.

- https://aclanthology.org/2025.findings-emnlp.1170/
- https://aclanthology.org/2025.findings-naacl.450/
- https://aclanthology.org/2024.clicit-1.124/

A useful design metaphor is “proof-carrying claims”: rendering a claim as verified only after deterministic checks confirm its evidence anchors. The application can implement this without trusting a model's self-assessment.

## Target pipeline

```
immutable source
    ↓
review unit / selected passage
    ↓
atomic claim proposal(s)
    ↓
actor + capacity + date + proceeding normalization
    ↓
evidence retrieval
    ↓
support / contradiction / notice / adoption relations
    ↓
context + power + knowledge + causation tests
    ↓
evidence-constrained restatement proposal
    ↓
independent mechanical guards
    ↓
human REVIEWED decision
    ↓
truth-telling edition + transformation ledger + annotated original
```

## AI adapter contract

Future AI must return structured proposals, never free-floating prose that becomes case data automatically. Minimum output per proposed claim:

- source block and exact offsets;
- exact quote;
- atomic claim;
- proposed actor/capacity;
- proposed dates;
- evidence source IDs and pinpoints;
- support/contradiction classification;
- omitted-context candidates;
- knowledge-state candidate;
- causal-bridge candidate;
- proposed restatement;
- uncertainty / unresolved questions;
- model/runtime/version metadata.

The deterministic application validates offsets, quote equality, source IDs, pinpoints and allowed enums before showing the proposal. The reviewer then accepts, edits or rejects it.

## Retrieval architecture

**Small case / immediate:** exact text search + manual evidence links.

**Medium case:** local embeddings for candidate retrieval, with lexical search retained. Run embeddings in a Web Worker so model work cannot freeze the UI.

**Large case:** a separate private indexing layer, ideally SQLite/FTS plus embeddings. SQLite's WASM build can use browser-side OPFS, but this changes the current no-persistence threat model and therefore must be opt-in and separately documented.

- https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers
- https://www.sqlite.org/wasm/doc/trunk/about.md
- https://www.sqlite.org/wasm/doc/trunk/persistence.md

## Storage rule

The current explicit JSON export remains the default because it is simple and inspectable. Browser persistence (IndexedDB/OPFS) can improve productivity later but must not silently become custody. If added, the UI must distinguish **working cache** from **preserved export**, show its location/status, and permit explicit wipe/export.

- https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API
- https://developer.mozilla.org/en-US/docs/Web/API/Window/showSaveFilePicker

## Phased readiness

### Phase 1 — implemented in feature branch
- truth-reconstruction panel;
- atomic claim;
- status / omitted context / real power-capacity;
- knowledge and causation states;
- evidence-constrained restatement;
- human acceptance gate;
- non-numeric Truth Delta;
- CSV/JSON carriage;
- synthetic regression coverage;
- zero network preserved.

### Phase 2 — deterministic claim workbench
- split one passage into multiple atomic claims;
- stable claim IDs separate from annotation IDs;
- transformation ledger;
- side-by-side original / analysis / restatement view;
- legal-blackline-style export;
- deterministic anchor verifier and “proof-carrying” badges.

### Phase 3 — local retrieval assistance
- worker-based exact/semantic retrieval;
- optional local embedding model;
- bilingual Spanish/English entity and date normalization;
- candidate contradiction triage only;
- context-identity guard before NLI.

### Phase 4 — AI proposal adapters
- browser-local WebLLM/Transformers.js adapter;
- optional approved remote adapter using schema-constrained structured output;
- model/version/prompt provenance recorded for every proposal;
- no auto-accept;
- adversarial regression set with supportive, contrary and ambiguous examples.

### Phase 5 — case-scale graph and exports
- claim ↔ evidence ↔ actor ↔ capacity ↔ proceeding ↔ date graph;
- W3C-PROV-compatible provenance export;
- transformation ledger;
- Word/DOCX legal-blackline derivative;
- bilingual truth-telling edition;
- reviewer sign-off and snapshot hashes.

## Evaluation before enabling AI

Measure at least:
1. source-span precision;
2. citation/pinpoint validity;
3. atomic-claim completeness;
4. false-contradiction rate;
5. missed-contradiction rate;
6. actor/capacity conflation rate;
7. date/proceeding conflation rate;
8. unsupported knowledge upgrades;
9. unsupported causation upgrades;
10. reviewer accept/edit/reject rates;
11. reproducibility across repeated runs;
12. preservation of adverse/exculpatory evidence.

The release gate should fail if an AI proposal can become reviewed without an explicit human action or if a displayed “verified” state can exist without mechanically valid source anchors.
