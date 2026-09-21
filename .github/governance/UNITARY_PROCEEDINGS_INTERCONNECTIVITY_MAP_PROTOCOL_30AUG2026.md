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
- `archive/PROCEEDINGS_FULL_IDENTITY_STORYING_GOVERNANCE_30AUG2026.md`;
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

A contextual bridge helps readers understand why legally separate files sit in the same story. Material reconnection may use:

- same expressly recorded `Connection` value;
- shared source-controlled evidence/event/asset/transaction/actor relationship where independently registered.

Stream, geography, institution and chronology remain useful **taxonomy / browse
lenses**. They may group, filter or order nodes, but they must not by themselves
enter the material-reconnection denominator or cause a proposition to be shown
as context that disappears in isolation. A same-stream, same-place or same-date
match needs a separate controlled connection before it becomes material
cross-file context.

A contextual bridge is **not** a procedural edge and must be labelled as such. Common actors, a common hotel, family/employment/corporate proximity, chronological adjacency or common documents do not establish coordination, knowledge, wrongdoing, liability, joinder or identity of proceedings.

## 4. Required node identity

<!-- PROCEEDINGS_FULL_IDENTITY_STORYING_GATE -->

The mandatory full-identity/storying schema controls every node and linked narrative. The compact map view need not display every field at once, but each available field must be preserved in the canonical or linked proceeding record and reachable from the node; every unavailable applicable field must be an explicit gap.

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
- controlled contextual bridges supported by the same exact recorded
  `Connection` value or a separately source-controlled proposition;
- stream, geography and chronology only as visibly non-material browse
  taxonomy;
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

## 12. Shared-continuum / anti-fragmentation convergence rule

The repository must not confuse **legal separateness** with **factual, patrimonial or evidential isolation**. Where multiple proceedings touch the same Sun Park hotel/underlying assets, exploitation/control, secured credit, productive unit, insolvency estate, income, title, possession, enforcement, professional conduct or alleged harm, every unitary digest must test whether those files belong to a **shared asset/control/credit/harm continuum**.

That test is mandatory even where no court has formally joined, accumulated or recognised the files as connected. Absence of formal joinder is not evidence of factual irrelevance. Equally, a shared continuum is not proof of coordination, conspiracy, criminality or liability.

### 12.1 Current priority convergence cluster

Future scans must expressly test and, where sources permit, interlink the following as a high-priority convergence cluster rather than presenting them as hermetically sealed files:

- the three current Audiencia Provincial de Las Palmas appellate tracks identified by the project as concerning: **(i)** the calificación appeal, **(ii)** the challenge/removal/separation of the Administrador Concursal, and **(iii)** the Administrador Concursal fee challenge;
- the Valencia CaixaBank litigation insofar as it concerns the financing/mortgage/financial-product package tied to the hotel and the credit history feeding into or affected by Concurso 36/2012;
- Meeting Point / FTI pre-concurso or insolvency-related proceedings in Las Palmas insofar as sources establish use, marketing, exploitation, available stock, benefit, solvency/liquidity representation, public-funds exposure or other direct relevance to Sun Park / Club SEI / Lava Verde;
- the Arrecife mortgage-enforcement/dación/title chain insofar as it concerns the same secured credit, hotel assets, title or patrimonial effects that intersect with the concurso;
- the Cuatrecasas cambiario / enforcement / La Laguna / Matkator procedural chain insofar as the claim, execution target, advice, security, hotel-related assets or resulting harm connect it to the broader Sun Park/concurso record;
- Fiscalía files and responses across territorial or institutional offices insofar as they receive overlapping allegations/evidence concerning intra-concursal and extra-concursal criminal harm, asset/control loss, procedural conduct or enabling acts;
- historical Montelanza/Molina minority proceedings in Arrecife and their appellate treatment, including the exploitation/possession/desahucio chain and any substitution/change of demanded party from CEXP/Community-related entities to Monterecco/Pink, where verified from primary procedural records; and
- any later successor/private-actor, creditor, Community, AC, judge, operator or professional conduct that relies on, inherits, contradicts, benefits from, or procedurally reacts to those earlier proceedings.

The exact court references, parties, statuses and current custodians must remain source-led. User-supplied descriptions are continuity instructions and investigative propositions until independently reconciled to the Master Register and primary documents.

### 12.2 The three Audiencia Provincial appeals — unitary treatment rule

The three Audiencia Provincial appeals must never be analysed as unrelated solely because each has a different procedural object. The digest must test the common factual and causal spine, including where applicable:

**Concurso 36/2012 → conduct/decisions of the AC and court → estate/productive-unit/credit treatment → calificación narrative → challenge to AC continuation/separation → challenge to AC remuneration → appellate review and consequences.**

For each of the three appeals, identify what facts, actors, filings, decisions, omissions, estate effects, control events, evidence and legal propositions recur across the other two. Maintain a convergence matrix showing **shared fact / proceeding A treatment / proceeding B treatment / proceeding C treatment / contradiction or omission / source status / appellate relevance**.

The project’s position that atomising those appeals can obscure a common causal and evidential picture must be preserved as an attributed litigation/forensic contention, not silently converted into an established finding about judicial motive or intent.

### 12.3 Fragmentation / atomisation audit

For every material proceeding, ask:

1. What material fact, asset effect, credit event, control event, filing, allegation or evidence exists elsewhere in the corpus that this proceeding should at least be tested against?
2. Was that cross-proceeding relevance acknowledged, rejected, not raised, not located, or left unresolved?
3. Did compartmentalised treatment produce a different factual premise in another file?
4. Did one file treat a party/entity/asset/credit/Community/operator relationship differently from another?
5. Did fragmentation affect standing, debtor identity, authority, title, possession, estate value, productive-unit continuity, solvency/creditor treatment, criminal-harm analysis, damages or appellate review?
6. Who, if anyone, obtained a documented procedural or patrimonial benefit from the separation of the narratives?
7. Is that benefit a neutral consequence, contested project inference, or supported actor-specific evidence of knowing use or enablement?
8. What source would be needed to move the proposition from hypothesis → attributed contention → documented fact?

Never write “hidden”, “ignored”, “enabled”, “misused”, “benefited”, “atomised deliberately” or equivalent as an established fact merely because the files were treated separately. Preserve the project’s allegation, identify the alleged beneficiary/enabler, and test it against primary sources, contrary evidence and actor-specific knowledge/intent.

### 12.4 Historical-to-current lineage rule

Earlier possession, exploitation, desahucio, mortgage, cambiario, enforcement, tax, tourism, Community and criminal files must be reverse-traced into the concurso and forward-traced into later control, adjudication, operator, creditor, AC, judicial, Fiscalía and appellate consequences wherever the evidence supports the chain.

A change of party name, successor, assignment, renaming, creditor transfer, operator change or procedural substitution must never break the graph. Preserve lineage explicitly as **same legal person renamed**, **successor/assignee**, **different legal person**, **procedural substitution**, or **unresolved**; never merge by narrative convenience.

### 12.5 Ministerio Fiscal unitary-recognition audit

Where multiple Fiscalía offices/files received overlapping allegations or evidence, maintain a matrix of **office/file → material allegations/evidence received → related proceedings/assets → referral/response → whether cross-file relevance was acknowledged → open gap**. The project’s contention that no single unitary acknowledgement of the full intra- and extra-concursal harm emerged must be tested as a corpus-wide proposition and must not be upgraded beyond the located record.

### 12.6 Governing anti-fragmentation sentence

> **Keep the proceedings legally distinct, but never analytically isolated where the evidence shows a shared asset, credit, control, exploitation, estate, transaction, actor, event or harm continuum. Fragmentation itself is an audit object: test what was separated, what should have been cross-recognised, who benefited, what was lost or obscured, and what actor-specific evidence supports any allegation of knowing atomisation or enablement.**

## 13. Current exact-proceeding closure contract

The enforceable artifact pair is interconnectivity schema **1.7.0** and public
interlinkability projection **1.1.0**. Exact-head CI must reject a stale version
or a projection that satisfies only the earlier structural contract.

The current public denominator is 97 exact proceedings/files. Each must have one
and only one controlled disposition and one finite test. The finite test must
state the question, source needed, current source status, recorded candidate
organ/custodian and its evidential limit, controlled related proceedings,
file-specific decision dependency, strongest contrary explanation, and distinct
consequences if confirmed or refuted. It must expose both the canonical public
record route and either a proceeding-specific public primary-source route or an
explicit primary-source route gap. The finite question, decision dependency,
strongest contrary explanation and both consequences must be bilingual and
exact-file-specific. Repeated registry-maintenance, source-retrieval or
record-correction boilerplate, even when prefixed with a different reference,
does not count as a unique finite test. A family template may classify a file;
it may not supply its substantive actionability fields.
A recorded custodian/organ remains a candidate only. The model must not treat
that candidate as legally competent, empowered or obliged to act. Confirmed or
refuted consequences must be conditional on exact competence and a lawful
procedural or institutional route.
The strongest contrary explanation remains hypothetical and may not attribute
an act to the recorded candidate without a primary source. Family taxonomy must
use canonical record type before mixed Stream substrings: an administrative /
professional perimeter is not a disciplinary file, judicial governance is not
professional discipline, and civil professional liability remains civil.
Membership of a relationship or context cluster is not proof that the material
was received, admissible, examined or relied upon in the selected file.

Every exact proceeding must also receive an institutional receipt/knowledge
classification with provenance for nine independent axes: transmission,
material received/inventory, referral, registration, file incorporation,
recipient attribution, substantive examination, decision use and cross-file
acknowledgement. Each axis requires its own status, bilingual basis, bilingual
limitation and controlled source pointer or explicit source-not-located object.
Each positive grade must reproduce the exact episode field that supports that
axis; episode-and-axis overrides are mandatory when a global default would cite
unrelated text.
Transmission and referral must be graded independently; proof of sending,
routing or presentation cannot be copied into referral, destination receipt,
registration, incorporation or examination. Classification coverage and
positive evidence are different denominators. An explicit `NOT_LOCATED`,
`NO_PROOF_OF_AWARENESS`, unresolved or not-applicable state closes an audit slot
without proving the underlying fact or its opposite. Actor-specific receipt and
knowledge remain separate non-positive fields unless an actor-specific source
identifies the person, material/act, time and evidential scope. Neither field may
be inherited from an institution, colleague, family member, professional firm,
common asset, chronology, signature, routing act or downstream benefit.

### Public renderer parity is a hard implementation denominator

Declaring or generating the nine-axis model is not sufficient. Every exact-file
finite-test panel exposed through both trace and isolation must render, in the
controlled order, all nine institutional grades: transmission, material
received, referral, registration, file incorporation, recipient attribution,
substantive examination, decision use and cross-file acknowledgement. Each
rendered grade must expose its raw controlled status, bilingual basis, bilingual
limitation and controlled source/source-gap provenance. Colour, a summary token
or the separate Fiscalía matrix cannot substitute for those fields.

An exact-file panel may be labelled `AUDITED` only when the canonical status
location exists, the status equals its basis status, both languages are present,
the limitation is present and the source carries its controlled kind and record
ID. A missing or mismatched axis must fail closed as `INCOMPLETE` and reduce the
audited denominator. The six core statuses remain stored in
`institutional_axes`; material received and referral use their independent basis
grades; cross-file acknowledgement remains a separate root status. Flexible
legacy aliases may be displayed for diagnosis but may not qualify a panel as
audited.

Actor receipt, actor knowledge and actor-source availability must be rendered as
three independent values outside the nine-axis institutional grid. A located
source, actor identifier or profile must never become personal receipt or
knowledge without an explicit actor-specific grade. The public renderer,
generated contract, schema requirements, specialist audit, exhaustive bilingual
browser check and live page must therefore be tested as separate lifecycle
layers. A green schema or data build does not establish renderer or live-page
completion.

For Ministerio Fiscal, maintain a 24-row office/file matrix keyed to the public
Master Register: 21 exact file rows and three unresolved-reference rows.
Event-to-file links require a reviewed relation such as a
file-native act/notice, filing receipt/presentation, referral/routing, response,
later submission reference or context only. A matching number or raw
`matter_references` string is not by itself an institutional-memory edge. Nine
current response episodes are source-controlled: eight profile matrix rows and
one separate `DP 1901/2026` judicial-file profile. Absent episode coverage
remains an express source gap. Each of the 24 rows must independently expose:

- source-attributed material allegations/evidence;
- material received and the missing item-level inventory;
- direct proceedings and contextual proceedings as separate arrays/statuses;
- related assets and an explicit asset gap;
- transmission and referral as separate grades, plus what was referred;
- registration, incorporation, recipient attribution and what was actually
  examined;
- institutional response and decision-use grade;
- cross-file acknowledgement and unitary acknowledgement as separate states;
- strongest contrary explanation; and
- unanswered question/source gap.

Each available institutional grade must be traceable to its own source, basis
and limitation. A source-profile absence must remain an explicit gap rather than
being filled from another office/file or from raw reference equality.

Navigation coverage is 97 / 97 through the Master Register, exact trace and
isolation fragments. Dedicated bilingual narrative-dossier coverage remains a
separate positive count and may be partial. The public Case Prism must also
render an exact-file Decision-Dependency Register derived from the 97 controlled
finite tests. It is complete only when all 97 entries expose the finite question,
source needed/current status, strongest contrary explanation, competent-organ
candidate/status, decision dependency, confirmed/refuted consequences and
Master/trace/isolation navigation. This 97 / 97 record-level denominator does
not expand the shared Case Prism proposition matrix: that matrix currently
remains 43 / 97 exact proceedings covered and 54 no-coordinate gaps until new
proposition membership is source-reviewed. Both denominators must be displayed
and tested independently.

For first-read institutional access, the bilingual homepages, Proceedings Map,
Master Register, Calificación routes, insolvency-administrator routes, Fiscalía
routes and material proceeding-specific dossiers must provide a direct path to
the neutral institutional reconstruction and Case Prism. Where a page has one or
more already controlled exact Master IDs, it must also expose the corresponding
Master row, trace and isolation routes. A page spanning several files may use
generic Master/Prism navigation; it must not manufacture a single-file mapping.
Every such navigation block must state that navigation does not establish
joinder, receipt, admissibility, knowledge, reliance, wrongdoing or merits.

The two direct relationship pairs still graded source-reported/pending primary
completion, the counsel/procurador denominators, source-not-located fields and
the accepted public accessibility of the tracked operational CSV remain open
limitations. They may not be silently upgraded to obtain a global word such as
“complete” or `DELETION_SAFE`.
