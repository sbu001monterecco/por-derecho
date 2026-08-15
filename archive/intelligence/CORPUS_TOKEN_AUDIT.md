# Corpus and token audit — planning baseline

**Status:** preliminary planning audit, not a certified census.

## Core conclusion

The principal resource problem is not simply lack of information. It is **duplication, fragmentation, version proliferation and incomplete canonicalisation**. The wrong strategy is to repeatedly feed the entire archive into an expensive model. The right strategy is search-first, deduplicated, hierarchical processing that leaves behind durable source-linked knowledge.

## Sources considered

The audit in the originating work considered accessible or partially accessible material across:

- Gmail;
- Google Drive;
- ChatGPT Library / conversation files;
- OneDrive / Microsoft storage where connector access permits;
- GitHub / public website / repository;
- existing documentary archives and generated intelligence packs.

A full byte-accurate census was not completed. Connector pagination and limitations mean all figures below are planning ranges.

## Observed mailbox scale

At the time of the audit Gmail exposed label counts including approximately:

- Inbox: 44,192 messages;
- Sent: 27,384 messages;
- Important: 57,475 messages;
- Drafts: 686.

These categories overlap and **must not be added to derive a unique message total**. Historical project material extends well before 2020 and continues intensively through 2026. Self-archive emails and repeated attachments make message-level counts especially misleading.

## Working corpus estimates

Planning ranges developed in the audit:

| Measure | Low | Central | High |
|---|---:|---:|---:|
| Raw textual corpus equivalent | 60M | 110M | 200M tokens |
| After exact/version/thread deduplication | 35M | 65M | 120M |
| Genuinely useful project knowledge | 20M | 40M | 75M |
| P0/P1 primary/high-value material | 10M | 22M | 40M |
| Additional search-first processing needed | 15M | 30M | 55M |
| Analysis/structured-output tokens | 4M | 8M | 15M |
| Sensible initial programme envelope | 25M | 50M | 80M |
| Prudent full-programme allowance | 50M | 100M | 150M |

These are **model-processing/token-equivalent planning estimates**, not claims that exact counts have been measured in the storage systems.

## Public figure

The public Knowledge Project currently uses a deliberately wider and qualified range:

> approximately **35–120 million unique source-text-equivalent tokens**, with a central working estimate near **65 million**, subject to continuing deduplication and census work.

The 100M figure is a **prudent programme ceiling**, not a target to consume.

## Duplication patterns observed

Material duplication occurs through:

- Gmail attachment + Drive copy;
- DOCX + PDF representations;
- signed/unsigned copies;
- `PARA_FIRMA`, `FINAL`, numbered versions and later corrected versions;
- documentary annex packs that repeat canonical sources;
- quoted email chains;
- self-archive emails of ChatGPT work;
- Spanish/English/Hebrew editions of substantially the same source content;
- generated handover/intelligence packs repeating earlier analysis.

The same item can be important for custody but should not be processed repeatedly as if it were new knowledge.

## Priority classes

Recommended ingestion priorities:

- `P0` — canonical primary evidence / decisive sources;
- `P1` — high-value contemporaneous evidence;
- `P2` — important contextual evidence;
- `P3` — analytical/secondary work product;
- `P4` — duplicate/low-value;
- `P5` — archive/custody only.

## Three processing scenarios

### A. Brute force

Read every unique document in full. Useful only as an upper-bound baseline. Not recommended.

### B. Hierarchical ingestion

For each source:

metadata → deduplicate/version → classify → extract entities/dates/amounts → identify propositions → summarise holdings/limits → preserve citations → update canonical ledgers.

### C. Search-first intelligence

Use existing search/indexing/connectors to retrieve only the material required to resolve known propositions and gaps, then persist the results so repeated full rereading is unnecessary.

**Recommended strategy: C, supported by B for high-value sources.**

## Token tiers

Do not use the most capable/expensive model for every operation.

### Tier 1 — cheap extraction

Deduplication support, metadata, dates, entities, document type, basic amounts and classification.

### Tier 2 — structured legal/evidential extraction

Holdings, propositions, relationships, chronology, contradictions, what a document establishes and does not establish.

### Tier 3 — serious cross-document reasoning

Credit/title reconstruction, institutional knowledge, causation, competing explanations, cross-proceeding analysis.

### Tier 4 — highest-value human + frontier-model review

Only the decisive questions/documents and publication-sensitive conclusions.

## Staged resource programme

### 10M proof phase

Canonicalise the highest-value evidence and measure yield.

### 25M cumulative

Complete major judicial, title, credit, money and institutional-knowledge rails.

### 50M cumulative

Aim for a usable whole-case knowledge system supporting legal work, the website, the book, journalists and diligence.

### Up to 100M

Proceed only if measured residual knowledge gaps justify it.

## Core KPI

# Verified reusable knowledge per million tokens

Supporting metrics:

- canonical sources / 1M tokens;
- verified propositions / 1M tokens;
- contradictions resolved;
- open questions closed;
- duplicate processing avoided;
- outputs generated without rereading original sources.

## External resource ask

A defensible future request to an AI provider, donor or partner should not say “we need unlimited tokens.” It should explain:

- preliminary unique corpus scale;
- how much is already structured;
- why deduplication/canonicalisation lowers cost;
- the staged 10M/25M/50M gates;
- measurable outputs;
- the distinction between AI processing resources and proprietary project assets.

Potential useful contributions include AI/API credits, cloud/storage, compute, engineering, research assistance, legal review and cash funding. The highest-value contribution may differ by workstream.

## Economic interpretation

The project should not claim that the AI model itself is the proprietary asset. Potential value lies in the lawfully usable corpus, provenance, reconstructed chronology, methodology, human expertise, structured knowledge, workflows, source relationships and future products/services actually developed.