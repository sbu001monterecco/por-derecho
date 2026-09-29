# OpenAI Platform / Por Derecho integration control

**Control:** PD-OPENAI-PLATFORM-SECOND-PAIR-20260929-01
**Status:** PUBLIC-SAFE IMPLEMENTATION HANDOFF

## Role split
ChatGPT is the interactive research, drafting, orchestration and connected-source layer.

The OpenAI API Platform is the future repeatable engineering/evaluation layer for The Second Pair of Eyes: structured source-bound extraction, synthetic-case testing, repeatable evaluations, controlled retrieval over approved corpora, and machine-readable outputs that Git-based CI can validate.

GitLab remains the versioned control and CI plane. OpenAI-generated candidate outputs do not become evidence or authoritative decisions.

## Synthetic first
Do not begin by uploading the full live legal corpus. Start with fictional/public-safe cases that test Source, Authority, Perimeter, Contradiction, Consequence and Reversibility, including false-positive closure, late evidence, wrong competence, contradictory sources and legitimate urgency.

## Evaluation targets
- source and version fidelity;
- allegation/fact/inference separation;
- temporal integrity;
- perimeter separation;
- strongest contrary explanation;
- false-positive closure and false-negative detection;
- competence routing;
- bilingual consistency;
- privacy/access boundaries;
- human override and explicit reopen/change triggers.

## Live-matter gate
A bounded live corpus may be considered only after the synthetic/public-safe controls are credible. Access filtering must occur before retrieval; native sources/hashes remain outside model output; consequential conclusions require human admission; and send/file/publish/contact authority remains separate.

## Cost architecture
Use cost-efficient models for bounded high-volume extraction/classification and reserve stronger reasoning models for small source-bounded questions. Measure verified reusable knowledge per unit cost rather than raw token consumption.

## Required setup decisions
Before live sensitive use: select the OpenAI organization/project, create a dedicated project API key through the secure setup flow, set budget guardrails, decide data-residency/region needs, define allowed source classes, and define retention/logging/deletion/incident procedures.

## Current truth
No API key is committed to this repository. No proprietary foundation model, independent validation, institutional adoption, production multi-customer service or autonomous legal decision-maker is claimed.

## Future-thread instruction
For OpenAI API / Platform work on Por Derecho, read this control together with the Second Pair operating standard and the GitLab partnership readiness control before implementation.
