# PUZZLE continuity, publication and external-viewing protocol

**Control:** `PD-PUZZLE-CONTINUITY-20260905-01`  
**Status:** repository operating policy  
**Applies to:** Worker, Integrator, Verifier, Publication Coordinator, continuity/closeout roles, Puzzle/Uría/RICPE/authority/public-funds surfaces  
**Canonical public routes:** `/en/puzzle/` · `/es/puzzle/`

## 1. Purpose

The PUZZLE is a high-density visual navigation and evidential-reconciliation interface. Its strength comes from showing separate tracks together while retaining the exact legal person, date, capacity, source, proceeding and evidential status for every connection.

It must never become stronger by becoming less accurate. A connection, chronology, common professional, family, corporate, lender, servicer, investor, authority or proceeding does not transfer knowledge, intention, control, benefit, title, causation, liability or criminal participation.

The public interface must remain usable even when the browser cannot render an embedded PDF. The exact original must therefore be directly downloadable and the interactive display must use source-derived page images that work on ordinary desktop, tablet and mobile browsers.

## 2. Four-layer provenance model

Every Puzzle implementation must distinguish these layers visibly.

### Layer 0 — June 2024 original

- `PUZZLE 2024` is the 32-page historical visual.
- The companion introduction dated/filed as the June 2024 explanatory guide is an interpretive/hypothesis-navigation aid.
- Historic allegation language remains attributable to its source/date.
- Neither document is a pericial report or judicial finding merely because it is displayed on the site.

### Layer 1 — June 2026 filed baseline

The current website's controlling June narrative/methodological baseline is:

`01_NEXUS_36_DENUNCIA_PENAL_ACTUALIZADA_PRESENTACION_25JUN2026.pdf`

It is a 69-page party pleading presented on 25 June 2026. The Puzzle must summarise and interlink its method rather than silently substituting later analysis for it:

1. authority/title first;
2. act, payment, expenditure, possession or representation second;
3. individual attribution third;
4. possible legal/criminal characterisation last;
5. material counter-evidence and lawful alternatives retained;
6. production/certified records used to confirm or discard hypotheses; and
7. no accused or third party is required to prove innocence merely because a production question exists.

Related June tracks include Control 22 (18 June 2026) and the separate Control 24 judicial-governance package/traceability chain. Their identity and procedural effect remain distinct.

### Layer 2 — 21 July 2026 procedural companions

The DP 1956/2026 and DP 1901/2026 Puzzle companions dated 21 July 2026 are later procedural lenses. They may sharpen page-by-page reading but must never be labelled as the text filed on 25 June 2026.

### Layer 3 — current record

Later evidence, official responses, proceedings, corporate/governance records and new public-safe evidence may strengthen, narrow, contradict or supersede a historic Puzzle proposition. The historical proposition remains recoverable with its original date and status.

## 3. Exact-original and image custody

The authorised exact original is:

- path: `assets/docs/puzzle/PUZZLE-2024-original.pdf`
- pages: `32`
- bytes: `50,046,618`
- SHA-256: `e441bdb368c0092d5b15ca5ee911eeac266540bde54817e424f3075f4c5fdd47`

The viewer's page images must be rasterisations from this exact parent file. Their manifest must identify the parent hash and state that no semantic editing occurred.

Never:

- replace the original with a visually similar or lower-page-count variant;
- reconstruct a page with generative tools and present it as evidence;
- crop away context and then present the crop as the complete source;
- silently recompress/re-export and call the derivative the original; or
- use a screenshot as a substitute for the exact PDF when the exact PDF is available.

## 4. Browser-independent publication contract

The Puzzle must remain usable when native PDF embedding is unavailable or blocked.

Required public surfaces:

1. source-derived page-image viewer as the primary interactive display;
2. direct `Open original PDF` control;
3. direct `Download exact original PDF` control using an ordinary anchor with a `download` hint;
4. a visible static fallback link in the Puzzle HTML itself, independent of JavaScript;
5. direct image access for the currently selected page;
6. deep links `#p1` through `#p32`;
7. previous/next controls and direct page number entry;
8. zoom/fit/presentation/fullscreen controls where supported;
9. keyboard left/right navigation; and
10. a responsive layout with no forced horizontal page overflow at the tested mobile viewport.

The Puzzle page must load its viewer directly with a date-versioned asset URL. It must not depend solely on a long transitive `site.js` loader chain because stale cache keys or upstream runtime failure could make the principal exhibit disappear.

## 5. Anonymous external-viewing gate

A publication may be marked `LIVE_VERIFIED` only after anonymous, non-account readback confirms:

- `/en/puzzle/` and `/es/puzzle/` return successfully;
- the exact PDF is retrievable without a connected Google or GitHub account;
- the page-image manifest is retrievable;
- page 1, an interior page and page 32 load;
- the viewer is visible and has a non-zero rendered image size;
- `#p10` selects page 10;
- direct PDF/download links resolve;
- desktop, tablet and mobile viewports do not hide the primary navigation; and
- the static fallback still exposes the original when JavaScript is disabled.

The automated device smoke uses Chromium/Playwright or equivalent browser automation from a non-authenticated GitHub Actions runner. It is a compatibility test, not proof that every browser/device in existence will render identically.

## 6. Strongest compliant interlinking rule

The Puzzle should maximise *typed* interconnectivity, not accusation density.

Material clusters may include:

- LPB / Aweswell / Matkator / Sun Park / Concurso 36/2012;
- lender-of-record and servicing chain: Caja/Bankia/BFA → SAREB → HAYA → PH122 / Promontoria → later CAM questions;
- Uría and identified lawyers, with dated role and counter-evidence;
- PwC and other professional advisers, with exact client/scope questions;
- RICPE and later investment/governance records;
- CAM / Acosta Matos legal-person and actor-specific branches;
- Community governance and claimed debt/possession/exploitation branches;
- the Insolvency Administrator as a distinct statutory/professional actor;
- the relevant judicial actors as a distinct public-power branch;
- Ministerio Fiscal and other public-authority handling only through dated official acts/omissions;
- public-resource, tax-incentive, subsidy, EU/regional-funding or public-financing consequences where an exact resource and beneficiary can be traced; and
- later structures such as Orion where a documented later corporate/economic bridge exists, subject to a strict temporal firewall.

Every edge must identify one of at least:

- primary/documented relationship;
- reported contact;
- party pleading/position;
- claimant allegation;
- public-source contextual link;
- open production/reconciliation question; or
- counter-evidence/exculpatory record.

## 7. Public funds / public-interest firewall

The site may investigate potential public economic consequences but must distinguish:

- tax incentive/tax expenditure;
- subsidy or grant;
- EU or regional fund;
- public loan/guarantee/financing;
- licensing/tourism/public-administration act; and
- ordinary private capital.

No item is labelled `harm to public funds` merely because a public body, tax regime, RIC/RICPE structure, subsidy application or EU institution appears in the chain.

Before asserting public economic harm, the record should identify where possible:

`legal beneficiary` → `legal basis` → `decision/award` → `amount` → `eligible spend/project` → `actual disbursement or tax effect` → `representation relied upon` → `correction/recovery if any` → `counterfactual public loss`.

Missing links remain production questions.

## 8. Gil Marer / informant / foreign-investor attribution

The site may state that **Gil Marer says he has acted as an alertador/informante**, while also acting as a directly interested and allegedly injured party with personal/economic interests in the underlying matters.

It may state that he invokes, where their conditions are met:

- Directive (EU) 2019/1937;
- Spain's Ley 2/2023;
- Germany's Hinweisgeberschutzgesetz for qualifying German-connected reporting/disclosure; and
- the applicable UK/Great Britain protected-disclosure framework where worker/status, subject-matter, public-interest and channel conditions are satisfied.

It must not transform those statements into a legal determination that he has protected-informant status unless a competent authority has so determined.

The site may separately state Gil Marer's position that **Aweswell Limited is a foreign investor/economic interest in Spain**. Foreign-investor status, investor standing and whistleblower protection are separate questions and must remain separate in the graph.

## 9. Predatory-inclusion thesis

`Predatory inclusion` is Gil Marer's attributed analytical expression, not a repository finding.

The theory may be displayed strongly when accompanied by the finite test:

`legacy exposure` → `material fact + disclosure reason/duty` → `actor-specific knowledge` → `omission/misleading presentation` → `entry of new actor/resource` → `reliance/enabling effect` → `benefit/causation`.

Every stage must preserve an innocent/lawful alternative.

A later participant's lack of knowledge may simultaneously:

- support the alleged *unwitting-layer* aspect of the theory; and
- be exculpatory of that later participant's intention or liability.

No director, investor, lender, professional adviser, auditor, authority, market operator or institutional participant becomes a wrongdoer by being connected to a later structure.

## 10. Public-law / private-actor separation

The Puzzle may show a unitary multi-track architecture, but private parties, the Insolvency Administrator, judges, prosecutors, registrars, notaries, public administrations and funders must remain legally distinct.

A public actor's failure, disagreement, dismissal, archive, procedural decision or adverse ruling is not proof of capture or complicity. Any allegation of enabling, omission, bias, prevaricación, fraude procesal/concursal, corruption or other offence must be tied to:

- the exact actor;
- exact dated legal capacity;
- exact act/omission;
- notice/knowledge evidence;
- applicable duty/power;
- causal contribution;
- required mental element where relevant;
- counter-evidence/lawful explanation; and
- current procedural outcome.

## 11. Continuity / non-loss rule

The following are append-only in substance:

- source identity and hashes;
- original dates;
- filing/presentation provenance;
- adverse and exculpatory propositions;
- open production questions;
- canonical actor/entity IDs;
- prior legal capacities;
- proceeding links; and
- rights-of-reply/correction records.

A correction supersedes an inaccurate proposition; it does not erase why the earlier proposition existed.

A thread, branch, PR, page redesign or proceeding change must never silently delete a material unresolved question, counter-evidence item or source-control limitation. If a surface is superseded, the new surface must carry a compatibility/reverse link or an explicit supersession record.

## 12. Open-work classification

Every unresolved Puzzle item must be put into one of:

- `SOURCE_MATERIALISATION_PENDING`;
- `IDENTITY_OR_LEGAL_PERSON_RECONCILIATION_PENDING`;
- `REDACTION_OR_REUSE_RIGHTS_PENDING`;
- `OFFICIAL_PROCEDURAL_RECORD_PENDING`;
- `PUBLIC_FUNDS_RECONCILIATION_PENDING`;
- `COUNTER_EVIDENCE_REVIEW_PENDING`;
- `CROSS_ROUTE_PROPAGATION_PENDING`;
- `DEVICE_OR_LIVE_VERIFICATION_PENDING`; or
- `CLOSED_WITH_REASON`.

No material gap may be closed by rewriting an allegation as a fact or by reducing the evidential standard.

## 13. Closeout states

Use only these completion states:

- `SOURCE_CONTROLLED`;
- `IMPLEMENTED_ON_BRANCH`;
- `PR_OPEN`;
- `MERGED`;
- `PAGES_DEPLOYED`;
- `ANONYMOUS_HTTP_VERIFIED`;
- `CROSS_DEVICE_SMOKE_VERIFIED`;
- `LIVE_VERIFIED`;
- `PARTIAL_WITH_RECORDED_GAP`.

A successful merge is not the same as a successful Pages deployment. A successful Pages deployment is not the same as successful anonymous and cross-device readback.
