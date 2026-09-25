# Intelligence review layer — evidence-intelligence integration

**Control:** PD-UK-INTEL-LAYER-20260925-01  
**Status:** advisory / Pages-neutral / no new required check  
**Purpose:** wire the Companies House / Insolvency Service-derived review discipline into the existing Por Derecho evidence-intelligence architecture without creating a competing truth system.

## Placement in the architecture

The review layer sits **after source/matter/identity filtering and before a consequential human decision**:

```text
native source / controlled derivative
  -> matter + permission + identity/capacity
  -> canonical proposition / event / relationship
  -> SIGNAL + LINK HYPOTHESIS
  -> independent record-versus-reality verification
  -> support + contrary + correction + source-independence
  -> evidence state + separate calibrated confidence
  -> decisive test + priority + competence
  -> control-effectiveness/residual-risk review where relevant
  -> joined review packet
  -> Second Pair / independent challenge
  -> human decision
  -> separately authorised act or no-action
  -> correction / status history / reopen trigger
```

It does not change native source custody, canonical identity, proposition truth status or publication authority.

## Why it improves the existing platform

The present platform already prevents semantic similarity from becoming a relationship and already requires contrary evidence, corrections and open gaps. This layer adds:

1. a formal **signal state** before narrative;
2. a **source-independence** field so repetition cannot masquerade as corroboration;
3. a structured **record-versus-reality** test;
4. a separate **confidence vocabulary** without changing evidence state;
5. an **authoritative-data annotation state** that makes checking/correction visible;
6. a **control-effectiveness / residual-risk** loop for recurring process failures;
7. a **joined case packet** and evidence-reuse rule;
8. explicit **competence routing** and finite requested acts;
9. a closed-loop **review / correction / reopen** lifecycle.

## Retrieval consequences

A material evidence packet should retrieve not only the nearest supporting passages but also:

- same-origin/derivative sources, so they are not double-counted;
- the strongest independent source available;
- contrary or limiting evidence;
- corrections/supersession;
- the decisive missing evidence;
- relevant knowledge-date controls;
- decision-scope and competence controls.

The retrieval system may propose candidate links. It may not promote a link to independent corroboration without source-origin evidence.

## Graph consequences

Graph visualization is navigation, not adjudication. Each consequential edge should be able to answer:

- What exact source creates the edge?
- Is it the same underlying source repeated elsewhere?
- What date/capacity does the edge actually cover?
- Is the edge recorded, attributed, inferred, independently corroborated, contradicted or rejected?
- What would narrow or defeat it?
- Does the edge establish association only, or a separately sourced act/knowledge/control proposition?

## Context-integrity / truth-inversion integration

For a possible misleading-context use, treat the later quotation or summary as the **formal record** to test and restore the minimum material context from the underlying source. Keep separate:

source words → source context → later use → invited inference → omitted/restored material context → actor-specific knowledge → reliance/effect.

Literal accuracy therefore cannot bypass the record-versus-reality/context test.

## Institutional handoff

The review output for an external authority should be a finite envelope: exact question, competence, source packet, contrary evidence, proof ceiling, decisive requested act and closure/reopen criterion. A large narrative may sit behind that envelope, but the recipient should not have to discover the decisive question by reconstructing the project.

## Data governance

The UK institutional sources are classified as methodological/technical comparators. They must not inject UK company actors or case facts into Sun Park matter records merely through semantic similarity. Private Drive locators, provider IDs and source-account identifiers remain outside public Git.

## Enforcement boundary

This layer is advisory. The schema can be used in shadow mode immediately. Turning it into a required validator or automatic action gate requires the existing enforcement-change procedure and separate user authority.
