# UNITARY PROCEEDINGS INTERCONNECTIVITY MAP — GOVERNANCE PROTOCOL

**Date:** 30 August 2026  
**Status:** repository-wide additive proceedings/interlink/publication control  
**Canonical node source:** `archive/PROCEEDINGS_MASTER_REGISTER.csv`  
**Public routes:** `/en/proceedings-map/` and `/es/mapa-procedimientos/`

## 1. Purpose

Por Derecho must be capable of explaining the complete proceedings corpus as one **unitary, non-fragmented procedural/evidential graph** while preserving the separate legal identity, jurisdiction, procedural effect and evidential status of every proceeding/file.

The objective is not a single giant case and not a decorative spider diagram. The objective is a **map of maps** that lets a reader move:

- from beginning → end;
- from end → beginning;
- parent → child / appeal / incidente / pieza;
- child / appeal → originating proceeding;
- chronology/storyline → proceeding → source/evidence;
- proceeding → evidence/event/asset/actor context → other materially connected proceedings; and
- any displayed connection → a plain-language explanation of **why the connection is being shown**.

This protocol supplements, and does not displace:

- `archive/PROCEEDINGS_MASTER_REGISTER_PROTOCOL.md`;
- `archive/MASTER_PROCEEDINGS_PUBLICATION_GOVERNANCE_30AUG2026.md`;
- the counsel/procurador filing-lineage governance;
- the CAEPR / `^` registration-and-interlink audit; and
- source, correction, chronology, publication and privacy controls.

## 2. One master, multiple views

Do **not** create a second competing proceedings master merely to draw the map.

The canonical proceedings/file inventory remains `archive/PROCEEDINGS_MASTER_REGISTER.csv`. The interconnectivity layer is a derived relationship/navigation projection. New relationship facts not adequately representable in the CSV must be source-controlled in the appropriate relationship/evidence register and linked back to the canonical Master IDs; they must never be invented by the renderer.

The public mind-map is a controlled projection of public-eligible data. Internal/private rows and fields remain excluded under the existing publication gate.

## 3. Two classes of connection — never blur them

### A. DIRECT PROCEDURAL EDGE

A direct procedural edge exists only where the controlled record expressly supports a legal/institutional relationship such as:

- parent / child;
- appeal / review of;
- incidente / pieza of;
- referral / inhibition / transfer / destination file;
- accumulated / joined relationship;
- procedural follow-up expressly linked by the source; or
- another source-backed legal/institutional lineage.

The public renderer may derive reverse navigation from an explicit forward relation. For example, if B records A as `Parent_Master_ID`, A may show B as an incoming child. That is inversion of recorded data, not a new factual inference.

### B. CONTEXTUAL BRIDGE / LENS

A contextual bridge helps readers understand why legally separate files sit in the same story. Examples include:

- same procedural track/stream;
- same expressly recorded `Connection` value;
- same geography or institution;
- same chronology period;
- shared source-controlled evidence/event/asset/transaction/actor relationship where independently registered.

A contextual bridge is **not** a procedural edge and must be labelled as such. Common actors, a common hotel, family/employment/corporate proximity, chronological adjacency or common documents do not establish coordination, knowledge, wrongdoing, liability, joinder or identity of proceedings.

## 4. Required node identity

Every proceeding/file node shown by the map must retain, where populated and public-safe:

- `Master_ID` / stable repository identity;
- `Is_Proceeding` (`TRUE`, `FALSE`, `UNVERIFIED`);
- record type / proceeding class;
- stream/track;
- organ / current custodian;
- reference / secondary reference / NIG;
- date/period;
- connection and object/purpose;
- current recorded status / latest event;
- source status; and
- open reference/evidence gap.

Do not upgrade `FALSE` or `UNVERIFIED` merely because the object is useful in a map.

## 5. Required edge contract

Every material relationship edge, whether stored or derived, must be capable of answering:

1. **From what?** canonical source node/key.
2. **To what?** canonical destination node/key.
3. **What type of relationship?** procedural edge or contextual lens.
4. **Direction?** forward, reverse-derived, bidirectional or deliberately one-way.
5. **Why is it shown?** concise human explanation.
6. **What supports it?** source/register field or evidence anchor.
7. **What is its status?** verified/documented, source-reported, attributed, hypothesis/open, or not applicable as a merits proposition.
8. **May it be public?** public-safe treatment separate from internal registration.

No visual line may silently imply a stronger proposition than its source supports.

## 6. Mandatory reader modes

The public presentation should be a **map of maps**, not a hairball, and should support at least:

### 6.1 Procedural families / tracks
Group proceedings under their recorded stream/track so readers can see parallel lanes without conflating them.

### 6.2 Chronology / journey
Sort by the earliest reliable year/date available in the register and let the reader move from earliest known procedural events to current files. Missing or broad dates remain visibly approximate.

### 6.3 Trace one proceeding
Selecting one node should show:

- its identity and current recorded status;
- upstream parent/origin relations;
- downstream children/appeals/follow-ups captured by explicit data;
- reverse-discovered incoming relations;
- contextual lenses such as same track / same recorded connection / geography;
- open gaps; and
- a plain-language **Why connected?** explanation for every listed relationship class.

### 6.4 Reverse trace
A reader starting with a current or terminal file must be able to work backwards to its documented origins rather than being forced to know the chronology first.

### 6.5 Evidence/storyline exit
The map must make clear that it is a navigation layer. A material proposition still requires the underlying filing, decision, institutional original or other appropriate source.

## 7. Internal graph discipline

Internal proceedings analysis must run in both directions:

**ROOT / EARLIEST → descendants / consequences**

and

**CURRENT / TERMINAL → inputs / parents / triggering events / earlier proceedings**.

For each proceeding ask, at minimum:

- What triggered or preceded it?
- What filing, complaint, referral, decision or event created the next procedural step?
- What proceeding(s) are its parent, child, appeal, incidente, pieza, destination or follow-up?
- Which actors/parties/professionals/institutions are independently registered in it?
- Which evidence families, events, assets, transactions or communications are relied upon across another proceeding?
- Does another proceeding rely on, contradict, review or procedurally react to the same event/source?
- Is the connection direct/procedural or only contextual?
- Is the relationship discoverable from both ends?
- What contrary evidence or unresolved source gap limits the connection?
- Is there a proceeding-specific or public route that should link into/out of the map?

## 8. Unitary digest workflow

A repository-wide proceedings interconnectivity pass is not complete after reading only the CSV. It must reconcile, as applicable:

1. current `main` and continuity/start-here controls;
2. Proceedings Master Register + protocol + correction overlays;
3. specialist proceeding registers/ledgers and court/Fiscalía/administrative files;
4. filings, decisions, LexNET/registration records and counsel/procurador lineage;
5. evidence/source registers, ACTAs, communications and chronology controls;
6. asset/property/transaction/public-funds/operator/banking tracks where they materially bridge proceedings;
7. public website routes, storyline/timeline, proceeding-specific pages and evidence pages;
8. public treatment/privacy/source-status boundaries;
9. incoming and outgoing cross-links; and
10. repository → manifest/build → deployment → actual live route as separate verification layers.

Search supporting and contradicting material. `NOT LOCATED` must never be silently rewritten as `DID NOT EXIST`.

## 9. Completion standard

Do not describe the map as procedurally complete merely because every CSV row renders.

Use:

- **NODE COVERAGE** — public-eligible canonical rows represented;
- **DIRECT EDGE COVERAGE** — explicit parent/linked relationships represented and reversible;
- **CONTEXT COVERAGE** — available source-controlled contextual bridges exposed without overclaiming;
- **ORPHAN/GAP COUNT** — nodes lacking a currently evidenced direct relation or carrying open primary-source gaps; and
- **LIVE COVERAGE** — routes/assets actually deployed and reachable.

A node with no direct edge is not automatically erroneous; it may be an independent track or an unresolved relationship gap. Make that distinction visible.

## 10. Canonical reusable prompt

> **Run a unitary, non-fragmented, bidirectional Por Derecho proceedings-interconnectivity digest and map.** Start from current `main`, the Proceedings Master Register/protocol, all correction overlays and specialist proceeding/evidence/chronology registers, then reconcile the repository and the live bilingual website as one procedural/evidential graph while preserving every proceeding/file as a legally distinct object. Traverse the corpus twice: **beginning → end** and **end → beginning**. For every proceeding/file resolve its canonical ID, organ/court, reference/class, dates/status, parent/child/appeal/incidente/pieza/referral relationships, parties and professional lineage, filings/decisions, evidence families, events, assets/transactions, public routes and unresolved gaps. Build only source-backed relationship edges; distinguish **direct procedural edges** from **contextual bridges** and label every edge with direction, provenance/status and a plain-language “why connected?” explanation. Never infer joinder, knowledge, coordination, wrongdoing or liability merely from common actors, the same hotel/asset, chronology, family/employment/corporate proximity or shared documents. Deduplicate aliases without collapsing distinct legal persons, organs or proceedings. Make every material relationship discoverable in both directions where appropriate. Produce and maintain a **map of maps** with: procedural-family/track view, chronology/journey view, single-proceeding trace, reverse trace, related-proceedings/bridge panel, source/gap visibility and exits to the underlying evidence/storyline. Internally, gap-log orphan nodes, duplicate IDs, missing backlinks, missing provenance and missing chronology/evidence/asset relationships; repair safe defects rather than merely reporting them. Externally, publish only the controlled public-safe projection and keep uncertainty visible. Verify repository source, canonical registration, relationship layer, publication/build, deployment and actual live route separately. Do not claim “complete”, “fully interlinked” or “live” until the stated denominator and each relevant verification layer have passed.

## 11. Continuity rule

Future proceedings work that adds or materially changes a proceeding, relationship, appeal/referral, status, evidence bridge or public route must assess both the Master Register and the Proceedings Interconnectivity Map. The map is reconstructable from durable repository state; no future thread should need the originating ChatGPT conversation to understand its architecture, evidential boundaries or reverse-trace requirement.
