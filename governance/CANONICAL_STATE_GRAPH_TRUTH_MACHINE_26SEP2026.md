# Canonical state graph / Truth Machine recursive registration protocol

**Control ID:** `PD-CANONICAL-STATE-GRAPH-20260926-01`  
**Status:** MANDATORY / additive overlay / no-regression  
**Date:** 26 September 2026  
**Scope:** Project Sun Rock / Por Derecho / Sun Park, including Concurso 36/2012, hotel operation, Community/owner governance, extraconcursal assets, judicial and administrative institutions, professional advisers, capital/public-funds lanes and recovery.

## 1. Purpose

The canonical register is not an address book. It is the **state graph of the matter**.

A person, legal entity, institution, proceeding, event, instrument, source, asset, communication or proposition is analytically useful only when it can be placed on the timeline and connected to the other objects it actually touches.

The operating analogy is a tug-of-war: the important evidence is not merely who is present on either side at one moment, but whether a participant later supports, opposes, abstains, withdraws, changes capacity, changes objective, remains inactive where a sourced duty/opportunity is material, or becomes disconnected from the earlier group. Every such change is potentially relevant. The repository must capture the **dated state transition**, not infer a permanent faction from association.

This protocol exists to make the Truth Machine progressively better at detecting:
- chronology breaks;
- unexplained actor or entity changes;
- role/capacity changes;
- source contradictions;
- adoption or rejection of earlier propositions;
- support/opposition/withdrawal/abstention changes;
- institutional hand-offs;
- event → instrument → decision → implementation discontinuities;
- missing participants;
- missing predecessor/successor events;
- missing source or provenance links;
- missing contrary evidence; and
- later formalisation that does not prove earlier authority.

## 2. Node rule — every material object receives a stable identity

Every material object must resolve to exactly one stable canonical node or to an explicit pending-node record.

Node classes:
1. `PERSON`;
2. `ORGANISATION` / legal person;
3. `INSTITUTION` / public or professional body;
4. `PROCEEDING` / section, incident or appeal where separately material;
5. `EVENT`;
6. `INSTRUMENT` / filing, contract, deed, resolution, report, notice or communication;
7. `SOURCE` / primary or derivative source object;
8. `ASSET_RIGHT` / finca, credit, account, contractual right, income stream or other economic object;
9. `PROPOSITION` / allegation, defence, finding, inference or open question;
10. `OBJECTIVE` / the specific outcome against which a sourced position is being described.

Do not create duplicate identities merely because the same object appears in another legal track. Cross-link it.

If identity is unresolved, allocate a stable pending node with the ambiguity recorded. **Unknown is a state; omission is not.**

## 3. Edge rule — every material relationship is explicit and typed

Material relationships must be encoded as dated, source-backed edges. At minimum, use a typed relation such as:

`SIGNED`, `FILED`, `AUTHORED`, `REPRESENTED`, `INSTRUCTED`, `RECEIVED`, `NOTIFIED`, `SERVED`, `SUPPORTED`, `OPPOSED`, `ADOPTED`, `REJECTED`, `WITHDREW`, `ABSTAINED`, `NO_ACTION_RECORDED`, `APPOINTED`, `REPLACED`, `SUPERSEDED`, `IMPLEMENTED`, `APPEALED`, `REVIEWED`, `BENEFITED`, `SUFFERED_EFFECT`, `TRANSFERRED`, `FINANCED`, `CONTROLLED`, `OPERATED`, `RELATED_TO`, `CONTRADICTS`, `CORROBORATES`.

An edge must not transfer guilt, knowledge, intent, authority or capacity from another edge.

## 4. Position-vector / state-transition rule

Where a sourced act bears on a defined objective or proposition, encode an actor/entity state relative to that **specific object**, not a permanent red/blue faction label.

Allowed descriptive states include:
- `SUPPORTS`;
- `OPPOSES`;
- `ABSTAINS`;
- `WITHDRAWS`;
- `NO_ACTION_RECORDED`;
- `MIXED`;
- `PROCEDURAL_ONLY`;
- `UNKNOWN`.

Each state requires:
- actor/entity canonical ID;
- event/instrument ID;
- objective/proposition ID;
- date or bounded period;
- capacity;
- evidence status;
- source record;
- contrary evidence where material.

A change of state is a first-class event. Preserve `previous_state → transition_event → new_state`.

Do not infer `NO_ACTION_RECORDED` as culpable omission. A duty/opportunity and causal significance must be separately sourced and tested.

## 5. Event-family rule

A material event family is not complete merely because one resolution or filing exists.

For every material event, traverse where applicable:

`precursor request / factual condition → filing / instrument → receipt → allocation → actor/capacity → hearing/contradiction → decision → signature → service/notice → appeal/review → finality → implementation → asset/economic effect → later adoption/use → contrary/corrective act → current state`.

If one element is missing, keep an explicit gap object. Do not silently skip it.

## 6. Recursive anti-orphan rule

The Truth Machine must repeatedly search for:
- a material person named in a source but absent from the people registry;
- a material legal person/body named in a source but absent from the entity/institution registry;
- an event with free-text actor names but no immutable actor IDs;
- an actor with material acts but no event backlinks;
- a proceeding without its institution/court edge;
- a filing without its decision/result edge;
- a decision without service/appeal/finality status;
- an implementation without the authority chain it purports to implement;
- an asset or credit without owner/holder/date/source genealogy;
- a later state that lacks its predecessor;
- a contradiction without a supersession/correction edge;
- a claimed corroboration that is actually the same source lineage; and
- a public narrative that cannot be traversed back to canonical nodes.

Every pass must either resolve the orphan or register it as a finite gap with a next source target.

## 7. Bidirectional-link rule

Important links must be traversable both ways.

Examples:
- person → event and event → person;
- organisation → instrument and instrument → organisation;
- event → proceeding and proceeding → event;
- decision → source and source → decision;
- asset → transfer and transfer → asset;
- allegation → supporting/contrary source and source → allegation;
- predecessor event → successor event and successor → predecessor.

A human-readable page link alone is not a substitute for the machine edge where the object is material.

## 8. Distinct identity / capacity / responsibility rule

Keep these separate:
- identity;
- office/capacity;
- source signatory;
- institutional act;
- preparation/provenance;
- implementation;
- alleged causal responsibility;
- legal responsibility.

Example: Juan Avello Formoso's signature on the 19-Dec-2017 liquidation order is a source fact. It does not by itself establish who prepared the draft or resolve Alberto López Villarrubia's alleged causal responsibility for his own antecedent/subsequent acts. Conversely, a wider allegation does not permit misattributing Avello's signature.

## 9. Current critical-chain overlay

The initial machine overlay is `assets/data/canonical-state-graph-overlay-v1.json`. It begins with the material Concurso sequence:
- 6-Jun-2012 opening;
- 22-Mar-2017 opening of convenio;
- 19-Apr/27-Apr-2017 viability/proposal/presentation;
- 28-Jun-2017 Junta/outcome state as an explicit partially sourced event;
- 19-Dec-2017 opening of liquidation;
- 15-Jan/18-Jan-2018 CAM offer and AC liquidation plan;
- 16-Apr-2018 plan approval;
- 15-Jun-2018 publicity/better-offer implementation;
- 26-Jun-2018 partial suspension.

This overlay does not replace the frozen source catalogues. It crosswalks them and exposes missing typed edges.

## 10. Truth Machine recursive cycle

For every substantive intake and at scheduled gap-closure passes:

**discover → canonicalise → crosswalk → link → detect transition → test direction/effect → retrieve contrary evidence → register gap → correct/supersede → propagate backlinks → validate → repeat.**

The objective is not to make the allegation harder to challenge. It is to make unsupported propositions—whether favourable or adverse—harder to maintain.

## 11. Publication / privacy boundary

Public Git may contain stable IDs, public-safe summaries, source classes, hashes already approved for publication, and evidential boundaries.

Native Gmail/Drive locators, privileged advice, personal contact details, authentication material, unredacted private sources and private financial records remain outside public Git.

## 12. No-completeness claim

Until the certified docket/denominator and the recursive orphan audit close, do not claim that every historical act or participant is known.

The correct status is:
- canonical graph active;
- identified material nodes progressively normalised;
- explicit gaps retained;
- completeness not certified.
