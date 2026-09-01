# Event continuity repository-digest and action protocol — 1 September 2026

**Control ID:** `PD-ECRD-001`  
**Status:** ACTIVE REPOSITORY-WIDE CONTINUITY OPERATING PROTOCOL  
**Machine pair:** `ops/EVENT_CONTINUITY_REPOSITORY_DIGEST_AND_ACTION_V1.json`

## 1. Purpose

Every **material event that is admitted to a continuity-governed chronology, incident register, proceeding register, ACTA lineage, authority-response register, transaction/finance reconstruction, professional/actor graph or public narrative** must terminate in a finite, explicit action list. The event is not continuity-complete merely because a paragraph, date or source has been added.

The required output is called `EVENT_DIGEST_ACTIONS`.

This rule answers a recurring failure mode: evidence can exist somewhere in GitHub while a later thread does not discover it, or a new event can be described without checking the repository, identity registry, filings, authority responses, interlinks and public/live state that give the event its real context.

## 2. What “digest the repository/GitHub” means

For the event in scope, the maintainer must perform a **bounded unitary retrieval pass** across the current repository state, not a blind rewrite of the whole repository. The pass must search the current `main` tree and relevant Git history/PR context for the event's date, reference, proceeding, actors, entities, source IDs, assets and material aliases.

The pass must also inspect the controlling current handoff/routing files and the specialist registers actually implicated by the event. It must not assume that a historical chat, Gmail message, Drive item or private evidence object has been imported into GitHub merely because it was discussed previously.

`Not located` means **not located in the bounded retrieval pass**, not nonexistent.

## 3. Mandatory event fields

Every controlled material event must resolve or explicitly mark open:

- stable `EVENT_ID`;
- exact or bounded date/time;
- incident/event label;
- proceeding / expediente / ACTA / transaction / authority context;
- **all named actors and entities with CAEPR IDs and `^` state**;
- source(s) and provenance;
- evidence state: documented fact, source literal, official outcome, attributed allegation, project interpretation, investigative hypothesis, contrary record or open/unverified;
- actor capacity at the date;
- authority / legal basis where relevant;
- patrimonial, procedural, operational, financial or publication effect where relevant;
- predecessor and successor events;
- contrary/limiting evidence;
- gaps and falsification/production questions;
- direct public route(s), if any;
- continuity state and `EVENT_DIGEST_ACTIONS`.

## 4. Mandatory `EVENT_DIGEST_ACTIONS`

Every event receives a numbered list. Each action must have a stable action ID or event-local sequence number, status and target. At minimum the list must test the following eleven lanes:

1. **CURRENT MAIN / ROUTING** — reconcile live `main`; read `CURRENT_START_HERE.md`, `CURRENT_WORKSPACE_HANDOFF.md` when relevant, and the specialist control for the event.
2. **REPOSITORY / GITHUB DIGEST** — search the current repository plus relevant PR/commit history for the date, expediente/proceeding, source ID, names, aliases, transaction/asset and prior analysis. Record the finite search denominator or query family.
3. **IDENTITY `^` AUDIT** — enumerate every named person, organisation, institution and proceeding; resolve to immutable CAEPR IDs; check aliases, legal form, homonyms, `not_same_as` controls and current caret state. Repair safe identity gaps instead of merely reporting them.
4. **SOURCE / PROVENANCE / CONTRARY RECORD** — locate the strongest available primary source; distinguish native, derivative and public-source evidence; preserve contrary or limiting material; create a production action when the source remains missing.
5. **CHRONOLOGY / CAUSAL BRIDGES** — identify before/event/after nodes and test each claimed causal arrow separately. Chronology alone does not prove knowledge, intent, causation or common plan.
6. **PROCEEDING / FILING / AUTHORITY REGISTER** — where relevant, check the canonised outgoing filings register, filing attachments, incoming public-authority responses, court acts, fiscal/administrative expediente registers and response/result state. A filing and the authority's response are separate objects.
7. **ASSET / MONEY / ROLE LANE** — where relevant, distinguish title, equity, creditor/debtor, financing, RIC/RICPE, mandate, management, brand, construction, income, payment and benefit rather than collapsing them into one relationship.
8. **INTERLINK / DISCOVERABILITY** — verify incoming and outgoing links among the event, actors, entities, proceedings, ACTAs, authorities, source exhibits, finance/asset nodes and corrections/open-proof items. A stable edge needs a stable ID and source or must remain `OPEN`.
9. **PUBLIC / PRIVATE / PUBLICATION STATE** — preserve the public/private boundary; classify repository source, build/deploy state and live Pages state separately; never infer that private connected-source material is public or continuously synchronised.
10. **REPAIR / VALIDATE / VERIFY** — repair safe defects found in the pass; run the relevant integrity/specialist checks; if publication is authorised, verify the affected live routes after merge. Do not convert unrelated open debt into a hard stop for an additive safe repair.
11. **NEXT ACTIONS / CONTINUITY CHECKPOINT** — emit the finite next-action list with owner/tool/source target, dependency/gate and state; preserve the result in the smallest canonical repository record so a successor thread does not need the originating chat.

An event may mark a lane `NOT_APPLICABLE`, but it may not silently omit the lane.

## 5. Action-state vocabulary

Use only the following terminal or working states unless a specialist control defines a stricter subset:

- `DONE`
- `OPEN_SOURCE_REQUIRED`
- `OPEN_REPOSITORY_RECONCILIATION`
- `OPEN_IDENTITY_RESOLUTION`
- `OPEN_INTERLINK`
- `OPEN_PUBLICATION_VERIFICATION`
- `BLOCKED_AUTHORITY_OR_PRIVACY`
- `NOT_APPLICABLE`
- `SUPERSEDED`

`DONE` means the described action was actually performed for the current event and current repository state. It does not mean the merits of the underlying dispute are resolved.

## 6. Minimum machine shape

Each controlled event should be representable as:

```json
{
  "event_id": "...",
  "event_date": "...",
  "actors": [{"id": "PD-SP-P-....", "caret_state": "...", "capacity": "..."}],
  "sources": ["..."],
  "evidence_state": "...",
  "event_digest_actions": [
    {"seq": 1, "lane": "CURRENT_MAIN_ROUTING", "status": "DONE", "target": "..."}
  ],
  "continuity_state": "..."
}
```

The machine pair defines the complete lane and status vocabulary.

## 7. Relationship to CAEPR `^`

The CAEPR caret protocol remains identity-only. This event protocol makes the operational consequence explicit: **every controlled event must enumerate and check the `^` state of all named actors/entities in its denominator**. A caret does not prove the person's role in that event; the dated capacity/role edge still requires its own source.

Where a pre-existing immutable CAEPR record lacks an embedded presentation-marker status but identity has since been resolved, the canonical companion `assets/data/matter-identity-caret-resolution-v1.json` may supply the current caret state without creating a duplicate identity.

## 8. Repository, connectors and private evidence

The event digest is repository-first for continuity, but it is not repository-only when the task expressly requires an authorised connected source. Use Gmail, Drive, Calendar or other connected sources only where relevant and authorised, and record only public-safe derivatives in GitHub.

Do **not** assume:

- Google Drive is a continuous event sink;
- historical ChatGPT conversations have been imported;
- every Gmail/Drive source discussed in chat exists in Git;
- a generated graphic or temporary sandbox file has been preserved;
- an OpenAI API workbench or credential is configured.

## 9. Public-site and satire/caricature events

For a satire/caricature publication event, the action list additionally checks the satire publication standard, PD-DMA exact-file identity, the named-person/entity caret denominator, the source/role edge behind every visible label, ES/EN parity, the non-advertisement disclosure and the correction/right-of-reply path.

A disclaimer never cures an invented person, firm, hotel, ownership edge, role, figure or causal claim.

## 10. Enforcement boundary

This is a **mandatory operating protocol** for new or materially updated controlled events. It does not, by itself, activate a new repository-wide required CI check or third-party approval gate. Under `AGENTS.md`, any new hard CI/ruleset enforcement still requires separate explicit authority and shadow validation.

A continuity audit must report any controlled event lacking its finite action list as `OPEN_REPOSITORY_RECONCILIATION` and should repair the omission when safely within scope.
