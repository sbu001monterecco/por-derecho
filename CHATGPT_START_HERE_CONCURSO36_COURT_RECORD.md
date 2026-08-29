# START HERE — Concurso 36/2012 court-record reconstruction

**Date:** 29 August 2026  
**Purpose:** deletion-safe, new-thread-safe autonomous continuation for court decisions, LAJ acts, LexNET notifications, party filings, appeals/quejas, finality and implementation in Concurso 36/2012.

## One-sentence mission

Reconstruct the complete located procedural record of Concurso 36/2012 as closed document families — **filing -> verified receipt -> court/LAJ act -> service -> review/appeal -> finality -> implementation** — and use that record to support the unitary criminal-led forensic/prosecutorial analysis without converting disputed allegations, adverse rulings or missing documents into categorical findings of criminal misconduct.

## Mandatory read order in a new thread

1. `CHATGPT_START_HERE_CONCURSO36_COURT_RECORD.md` — this file.
2. `assets/data/concurso36-court-record-reconstruction-v1.json` — current closed-family registry and autonomous queue.
3. `assets/data/concurso36-complete-record-v1.json` — earlier canonical located-corpus catalogue; **not a certified docket**.
4. `assets/data/concurso36-lexnet-supplement-20260829.json` — controlled 2018 LexNET supplement.
5. `assets/data/concurso36-multitrack-judicial-failure-parallel-lives-20260829.json` — filing/response/consequence crosswalk.
6. `archive/CONCURSO36_MULTITRACK_JUDICIAL_FAILURE_PARALLEL_LIVES_CLOSEOUT_29AUG2026.md` — proof boundaries and open families.
7. The bilingual hubs `/es/concurso-36-2012/` and `/en/insolvency-36-2012/`.

## Current reconstruction milestone

The first high-value 2022 family is now primary-controlled from owner-held LexNET copies:

- **28-Feb-2022 LPB appeal**: LexNET `202210473582179`, filing time 13:54:54, registration later identified as `1477/2022`.
- **2-Mar-2022 Aweswell appeal**: sent LexNET `202210474270428`, acknowledgement `1202210474270428`, registration later identified as `1512/2022`.
- **7-Mar-2022 CAM opposition**: LexNET `202210475416241`.
- **9-Mar-2022 Auto**: judge-signed decision inadmitting both appeals; ten-day queja route; electronic document `A05003250-3507d04a1d026d8373981d6add31646823908885`; notified 11-Mar under LexNET `202210476786626`.
- **29-Mar-2022 Aweswell queja**: sent LexNET `202210481753993`, acknowledgement `1202210481753993`.
- **30-Mar-2022 notice to the Mercantile Court of that queja**: sent LexNET `202210482293471`, acknowledgement `1202210482293471`.
- **4-Apr-2022 DIOR**: joins both parties' queja notices under court registration numbers `2275` and `2314/2022`, transfers them to the parties; electronic document `A05003250-357d33adfb2c55ef416dd56d02b1649076726371`.
- **26-Apr-2022 Decreto — 14-Feb DIOR/testimonios/finality**: dismisses LPB/Aweswell reposicion, treats the 15-Oct/26-Jan reposicion Auto as irrecurrible/firme and states testimonios were issued on a party request; electronic document `A05003250-35127ecbb3101ef0a562bb848041650980940581`.
- **26-Apr-2022 Decreto — 11-Feb DIOR/protest**: dismisses LPB reposicion on the same liquidation-phase appeal reasoning; electronic document `A05003250-35c4420e8dc3a3a7a92c73487a11650980920666`.
- **26-Apr-2022 DIOR — deposits**: procedural refund mandates; electronic document `A05003250-353850865b4edb2b073ddff6c681650980516640`.

This closes important **existence / filing / notice / response** questions. It does **not** yet close the Audiencia Provincial outcomes, exact testimonios, direct revision against the 26-Apr Decretos, or deed/registry implementation.

## Autonomous operating rules

### A. Search and ingestion

- Use connected Gmail for original LexNET/lawyer-notification families when repository sources are incomplete.
- Run searches **month-by-month and to pagination exhaustion**, not one-off keyword searches.
- Search separately for: `Escrito Enviado Lexnet`, `Escrito Recibido Lexnet`, `Mensaje LexNET - Notificación`, `AUTO`, `DECRETO`, `PROVIDENCIA`, `DILIGENCIA DE ORDENACIÓN`, `DIOR`, `TESTIMONIO`, `REPOSICIÓN`, `APELACIÓN`, `QUEJA`, `NULIDAD`, plus `36/2012` and known procurator/notifier senders.
- A forwarding email is custody/provenance, **not a second procedural act**.
- Dedupe by LexNET ID, message-sent ID/ack ID, electronic document ID and document hash. Never dedupe only by filename.
- Preserve same-date distinct signed decisions as distinct records.

### B. Pairing rule

For every material record create or update one family with:

`family_id -> party filing -> LexNET receipt -> annexes -> court/LAJ response -> service -> challenge -> appeal/queja/revision -> finality -> implementation -> remaining gap`.

Never call a family closed merely because a decision exists; the challenge/finality/implementation legs must also be tested.

### C. Judicial-treatment taxonomy

Use exactly these reader-facing states:

1. `ADVERSE_SUBSTANTIVE_RESPONSE`
2. `PROTECTIVE_RESPONSE`
3. `PROCEDURAL_ONLY_DISPOSITION`
4. `PARTIAL_RESPONSE`
5. `RESPONSE_NOT_LOCATED`
6. `CONTRADICTORY_OPERATIVE_STATE`
7. `IMPLEMENTATION_OR_ACCOUNTING_CHAIN_OPEN`

Do not translate `RESPONSE_NOT_LOCATED` into “ignored”. Do not translate an adverse ruling into criminal judicial misconduct without the separate offence elements.

### D. Evidence / allegation boundary

- A filing proves that a party made an allegation/request and, where controlled, when it entered the court channel; it does not prove the allegation true.
- A signed Auto/Decreto proves what the decision said and did; it does not by itself prove corruption, prevaricacion, collusion, malicious prosecution or criminal capture.
- The two 15-Oct-2021 Autos contain a verified textual contradiction; criminal significance is a separate test.
- `Institutional neutralisation/shielding` is first an **effect test**: narrowing, fragmentation, procedural termination, adverse reframing or non-reconciliation while a challenged private architecture continues. Upgrade to criminal attribution only with actor-specific duty, knowledge, intent/purpose, causal effect and contrary-evidence analysis.
- LPB estate rights, Matkator rights and other third-party rights remain separate.
- The insolvency proceeding is not universal title to the whole hotel.

### E. Publication governance

- Work on a branch, open a PR, require the dedicated validator to pass, merge, then verify `main` and Pages.
- Do not overwrite `concurso36-complete-record-v1.json`. New discoveries enter controlled supplements/reconstruction registry until cross-supplement dedupe supports a future `v2`.
- Public pages may show exact procedural metadata, operative summaries and source fingerprints after privacy/redaction review; do not publish private phone numbers, private strategy emails or unnecessary personal data.
- Preserve adverse and protective counterweights.
- No email, court filing, authority contact or third-party outreach is authorised merely by this continuity file.

## P0 autonomous queue

Proceed in this order unless a newly recovered primary source changes priority:

1. **2022 appeal/queja family** — locate LPB's queja receipt; Audiencia Provincial docket identity, section, admission/outcome; exact 11-Feb and 14-Feb DIORs; testimonios; direct-revision filings/outcomes; bind to deed and registry.
2. **7-Jun-2018 physical-control court-notice family** — find the exact Concurso filing/receipt, if any, reporting locks/access/security/possession/operation change; pair with judicial/LAJ response and 26-Jun protective order.
3. **Feb-Oct-2021 protection/nullity/bid/RICPE family** — close 24-Feb protection order and underlying filing/annexes; AC/CAM responses; nullity/reposicion; Ottawa/improved bid; July RICPE documentary chain; 15-Oct decisions; 26-Jan clarification.
4. **Funded exits 2017-2018** — classify every ONA, Stoneweg/Varia, Elaia, Ben Oldman and other document as draft / sent to counsel / filed / received / ruled upon / lapsed / superseded.
5. **Certified denominator** — pursue the signed electronic chronological index / official relation of procedural acts / equivalent certified per-piece export and reconcile it against the reconstructed LexNET registry and public repository.

## Definition of done for canonical v2

Do **not** publish `concurso36-complete-record-v2.json` until:

- all supplements have been deduped by LexNET/document/electronic IDs and hashes;
- unique counts exist for party filings, judicial/LAJ acts and notifications/receipts;
- material filings have response links or explicit orphan status;
- material decisions have service/challenge/finality links;
- title/credit/possession/testimonio decisions have implementation links or explicit implementation gaps;
- the distinction between reconstructed located corpus and certified official docket remains visible.

## Expired ChatGPT uploads

Some older files uploaded directly into earlier ChatGPT conversations have expired from the conversation file store. **Do not block the reconstruction on them** where Gmail/repository custody supplies the same family. If a specific expired upload is necessary to prove or compare a proposition, ask for that exact file to be re-uploaded; do not pretend its contents are still available.

## Recommended short prompt for a new thread

> **Continue the autonomous Concurso 36/2012 court-record reconstruction from `CHATGPT_START_HERE_CONCURSO36_COURT_RECORD.md`. Close the next P0 filing/decision/notification families end-to-end, update the repository and bilingual site through PR/CI/Pages, preserve all evidence boundaries and continuity governance, and leave the project deletion-safe and ready for the next short handoff.**

That prompt is intentionally short. A new thread should recover the operating state from the repository rather than requiring the originating chat.