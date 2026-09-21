# Repository and website reverse-engineering report

> **SUPERSEDED DATE LAYER — 23 August 2026.** The body below records the 21 August audit state and its earlier 8/9/14-February reconstruction for the creditor-substitution order. The current repository control is **15 February 2018**, with a twenty-day appeal; the earlier metadata layers require direct reinspection and must not be repeated as established fact. Restricted provider locators have been withheld from this public derivative.

**Matter:** Concurso 36/2012, Juzgado de lo Mercantil nº 1 de Las Palmas
**Cut-off:** 21 August 2026
**Current remote reviewed:** `127054053b750cb1d2a32591da3ce5dc04921a04`
**Earlier audited commit:** `a50e034b13ae9942ac18f277bdb8f2274e3b60dd`
**Primary forensic baseline:** `forensic_work/FORENSIC_SCAN_CRITICAL_AUTOS_CONCURSO_36_2012_21AUG2026.md`
**Method:** read-only repository, deploy, structured-data, script-loader and primary-source reconciliation. No repository or website file was changed.

## 1. Executive reverse-engineering finding

The deployed website is not merely stale in isolated prose. It contains a **split evidential architecture**:

1. newer primary-source registers and the 21 August forensic scan correctly resolve several decisive questions;
2. older Markdown digests, JSON/CSV intelligence records and globally loaded JavaScript still contain contrary descriptions;
3. static HTML repeats some of those older descriptions; and
4. the current loaders inject them into otherwise careful pages after render.

This means that a visitor can receive a primary-correct account and a primary-contradicted account on the same live deployment. Passing repository validators do not detect this because they test publication structure and narrow phrases, not the identity, date, function or operative part of each judicial act.

The current public deployment was verified against remote `main`, not assumed from the earlier audit. Representative live files were HTTP 200 and byte-identical to commit `1270540`, including the Spanish RICPE page, Spanish 2022-adjudication page, Article 82 page, asset-recovery page, `assets/site.js`, `assets/data/case-reconstruction-v1.json`, and the publicly reachable `archive/judicial-intelligence/decisions.jsonl`. The errors identified below are therefore **live publication errors**, not merely local working-copy issues.

The remote is 39 commits and 32 changed/added files ahead of `a50e034`. The new asset-recovery and Article 82 work is generally careful, but it did not repair the legacy judicial source graph. The highest-priority conclusion is:

> **Publication should be frozen for new substantive descriptions of the Concurso autos until the P0 identity/date/function corrections below are made in the canonical graph, all derived HTML/JSON/JS is rebuilt from it, and the rendered site is tested.**

## 2. How the present site produces claims

The operative publication chain is:

`primary binary / email or Drive locator` → `archive digest or register` → `assets/data/*.json and archive/judicial-intelligence/*` → `static ES/EN HTML` → `site.js / site-base loader` → `route-specific injected JavaScript` → `GitHub Pages`

There is no enforced one-to-one dependency between a public assertion and a controlled primary binary. Several public claims are hand-authored in more than one layer. A later correction to an archive register therefore does not automatically supersede:

- a JSON record;
- an ES/EN static paragraph;
- an injected route fragment;
- a timeline card; or
- a prior “correction register”.

The principal design defect is not lack of material. It is lack of **source authority and invalidation semantics**. A corrected primary finding does not mark all descendants stale. The same judicial date is also used as a record key even where two distinct acts were issued that day, causing conflation.

## 3. P0 primary-document contradictions

### P0-1 — Auto 164/2021: third-party bidder, not Aweswell, was the €14.8 million proposed bidder; CAM received definitive approval

**Status:** `CONTRADICTED — PROVEN BY PRIMARY DOCUMENT`

The complete 18 May 2021 Auto 164/2021, Drive ID `1SpJkBz23fl-Z6yKbbsIhixsKPrQNXqAc`, records that **third-party bidder** had offered €14.8 million, did not appear and did not lodge the bond. The court reasoned that the licitación could not be held and that it was appropriate to adjudicate definitively to Construcciones Acosta Matos. Its fallo approved the proposal definitively in CAM's favour.

The current canonical court-binary register is correct at `archive/CONCURSO_36_2012_CANONICAL_COURT_BINARY_REGISTER_17AUG2026.md:31–35`. The following descendants are primary-document contradictions:

| Affected source | Current defect | Required correction |
|---|---|---|
| `archive/LPAM_MAGISTRADO_SOURCE_COMPLETION_16AUG2026.md:85–96`, especially `:89`, and `:144–147`, especially `:146` | Says Aweswell made the higher offer and won | Replace with third-party bidder proposal, nonappearance/no bond, and definitive approval to CAM |
| `archive/THREAD_DELETION_CONTINUITY_AUDIT_LPAM_MAGISTRADO_SOURCE_COMPLETION_16AUG2026.md:42` | Repeats false counterevidence | Supersede from primary Auto 164 |
| `archive/CALIFICACION_LPAM_MAGISTRADO_ACTIVATION_16AUG2026.md:68` | Repeats Aweswell result | Correct actor and result |
| `archive/DEPLOYMENT_EVIDENCE_PR219_16AUG2026.md:58` | Treats false text as deployment evidence | Mark deployment evidence superseded |
| `assets/lpam-magistrado-source-control-20260816.js:35` and `:53` | Live ES/EN injection says Aweswell made the higher offer and result favoured Aweswell | Remove and replace before republishing |

The JavaScript error has unusually wide blast radius. `assets/site-base-20260819.js:84` loads the injector, and its route list at `assets/lpam-magistrado-source-control-20260816.js:5–15` injects the false proposition into eleven ES/EN routes, including the calificación, CGPJ/open-message, Mercantile Court, institutional-accountability and Acosta Matos perimeter pages.

**Exact safe replacement:**

> Auto 164/2021 records third-party bidder as the €14.8 million proposed bidder. third-party bidder did not appear and did not lodge the bond. The court stated that the licitación could not be held and definitively approved the CAM proposal. This does not by itself resolve whether every antecedent disclosure, valuation, asset-perimeter or later implementation condition was lawful or satisfied.

The 2022 documentary-reconstruction page is also stale at `es/adjudicacion-2022-reconstruccion-documental/index.html:27,35,37,40,52,60,66` and its English counterpart. It still treats the bidder as anonymous and the licitation result as requiring reconstruction. The party proposal remains useful for its terms, but the court's treatment is no longer open: the primary Auto supplies the name, nonappearance, lack of bond and result.

### P0-2 — Creditor-substitution Auto date and remedy: 8 February 2018, not 15 February; 20-day appeal, not five-day reposición

**Status:** `CONTRADICTED — PROVEN BY PRIMARY DOCUMENT`

The controlled primary Auto, Drive ID `1jwG4inqC8HFOdLbU3RdPY3PKj6SzKA7f`, is dated **8 February 2018** in its body, signed by the judge on 9 February and by the LAJ on 14 February. “15 February” is a filename/notification shorthand, not the decision date. Its stated challenge route is 20 days, not a five-day reposición.

This is a systemic error because a document expressly styled as a correction register propagated the wrong correction. `archive/CORRECTION_REGISTER_RETRACTO_DP1041_ADDENDUM_19AUG2026.md` must itself be marked superseded, not silently edited as though it had always been right.

Key live/public descendants include:

- `es/retracto-credito-litigioso-1041-2017/index.html:20,24,34,43,45,49` and the corresponding English page;
- `es/acreedor-de-registro/credito-litigioso-escritura/index.html:17,24,26,29,31` and the corresponding English page; line 24 also carries the wrong five-day route;
- ES/EN pacto-comisorio/credit-to-title pages at line 33;
- ES/EN lender-of-record liability pages at line 27;
- ES/EN Acosta-Matos-favourable-effect pages at lines 24, 32 and 36;
- ES/EN four-track retracto/tanteo pages, including line 38;
- `assets/data/retracto-credit-1041-2017-v1.json:33,36–40,198,225`;
- `assets/data/art1535-residual-restoration-pathway-v1.json`;
- `assets/data/cam-favourable-direction-of-effect-v1.json:26,121`;
- `assets/data/retracto-primary-act-closure-v1.json`;
- `assets/cam-favourable-pattern-20260819.js`; and
- `assets/retracto-tanteo-four-track-20260819.js`.

**Exact safe replacement:**

> Auto dated 8 February 2018; judge signature dated 9 February; LAJ signature dated 14 February. A 15 February label is a filing/notification alias, not the ruling date. The primary text states a 20-day appeal route.

Every timeline, canonical ID and same-day join should use the body date as decision date, retain signature/service dates in separate fields, and preserve aliases only as retrieval metadata.

### P0-3 — 26 January 2022 did not adjudicate the assets

**Status:** `CONTRADICTED — PROVEN BY PRIMARY DOCUMENT`

There are **two distinct clarification autos dated 26 January 2022**. Neither is the original judicial award. The controlled sequence is:

1. 18 May 2021 — definitive judicial approval in favour of CAM;
2. 15 October 2021 — two separate judicial acts;
3. 26 January 2022 — two separate clarification autos;
4. 14 February 2022 — LAJ testimony of then-current court-office treatment; and
5. 21 February 2022 — notarial deed, Protocol 457.

The most serious canonical error is public `archive/judicial-intelligence/decisions.jsonl:7`, which calls the 26 January document an “Auto/adjudication resolution”, says the corpus identifies judicial adjudication on that date and treats it as the immediate bridge to the deed. `archive/judicial-intelligence/ingestion_queue.csv:10` likewise asks for a nonexistent “signed adjudication resolution” of 26 January.

Live static/dynamic errors include:

- `es/ric-private-equity-sun-park/index.html:339,350` and the English counterpart;
- `assets/sun-park-7june-convergence-20260817.js:301` (“judicial adjudication threshold”);
- `assets/site-base-1728fcf.js:58` and English text at `:99` (“alleged adjudication order”);
- `es/index.html:107,508,767` and English equivalents around `:507,766`; and
- related source-note language that generically calls the January acts “orders” without explaining their clarificatory function.

**Exact safe replacement:**

> The primary award point is the 18 May 2021 definitive approval. Two acts followed on 15 October 2021. Two further autos dated 26 January 2022 clarified terminology, admission/processing and the treatment of objections; they did not newly award the assets, determine the final allowed debt, calculate a surplus or transfer title. Protocol 457 was executed on 21 February 2022.

“Adjudicación de 26 de enero de 2022” should be prohibited as a phrase unless immediately identified as a historical misdescription being corrected.

### P0-4 — Opening Auto named Francisco de Borja Rodríguez-Batllori Laffitte as AC, not Fernando de León Marrero

**Status:** `CONTRADICTED — PROVEN BY PRIMARY DOCUMENT`

The controlled nine-page opening Auto's dispositive paragraph QUARTO states: “Se nombra administrador del concurso … FRANCISCO DE BORJA RODRIGUEZ-BATLLORI LAFFITTE”. Therefore:

- `archive/CONCURSO_36_2012_100_PERCENT_DOCKET_COMPLETENESS_LEDGER_17AUG2026.md:51`; and
- `archive/ALBERTO_LOPEZ_VILLARRUBIA_SIGNED_ACTS_AND_KNOWLEDGE_REGISTER_17AUG2026.md:24`

contain Rank A primary contradictions when they say the Auto appointed Fernando de León Marrero.

Most visible pages happen to use Borja's name correctly, but leaving the error in high-authority internal ledgers creates future propagation risk. The fix must include a supersession note and a test that the opening Auto's appointee is derived from the dispositive text, not from later personnel or a secondary digest.

### P0-5 — The public judicial-intelligence graph still calls located primaries “pending” and omits paired acts

**Status:** `CONTRADICTED / STALE CANONICAL STATE`

The live-public file `archive/judicial-intelligence/decisions.jsonl` is not a reliable canonical source in its current form:

- line 2 marks the controlled 8 February 2018 Auto as `CORPUS_REPORTED_PRIMARY_PENDING`;
- line 4 marks the complete 26 June 2018 Auto pending;
- line 5 marks the complete 24 October 2019 non-convalidation Auto pending;
- line 6 collapses the 24 February 2021 date and omits the separate liquidation-extension act;
- line 7 invents the 26 January 2022 adjudication function; and
- it lacks the paired-act model required by the recovered docket.

`archive/judicial-intelligence/ingestion_queue.csv:5–11` carries corresponding stale OPEN statuses. Because both files are directly reachable on GitHub Pages, this is not a private research inconvenience. It is a public provenance conflict.

The graph should not be patched record-by-record in place. Introduce stable act IDs, one record per act, explicit source/version status, a primary hash and a `supersedes`/`invalidates` relationship. All public prose should be generated or linted against that graph.

### P0-6 — 4 June 2018 clarification source is no longer incomplete

**Status:** `STALE — PRIMARY NOW LOCATED`

`assets/data/case-reconstruction-v1.json:113–119` and its evidence block at `:212–222` still describe only an incomplete two-page copy, with continuation/signature and actor not promoted. The complete authentic three-page copy has been located in Gmail thread `194a98a11920fefd`, attachment `20180604 Auto Aclaracion Auto Aprobacion Plan Liquidacion.pdf`; the body is dated 4 June and the signature metadata falls on 5/6 June.

This dataset describes itself as `PUBLIC-SEED-NOT-COMPLETE`, yet `es/reconstruccion-unitaria-autoridades-publicas/index.html:52` and its English counterpart call it “FUENTE DE VERDAD / SOURCE OF TRUTH”. That is an internal UX contradiction.

Required correction:

- update document completeness, pages, signatory, source locator and hash;
- separate body date, signature date and file alias;
- replace “source of truth” with “partial public reconstruction; controlled primary register governs” unless and until it is generated from the complete primary graph.

### P0-7 — Same-date acts are being collapsed

**Status:** `UNRESOLVED GRAPH DEFECT WITH PRIMARY-DOCUMENT CONSEQUENCES`

The following must exist as separate act records, even where filenames or later pleadings use the date generically:

| Date | Act A | Act B | Present risk |
|---|---|---|---|
| 16 Apr 2018 | S03 liquidation-plan approval | S30 interest clarification | Plan approval and economic clarification become one fictional act |
| 24 Oct 2019 | S07 locales non-convalidation | S38 Aweswell-standing act | Asset/title effect becomes confused with party standing |
| 12 May 2020 | S27 LPB reposición act | S39 Auto 83/2020 | Grounds and parties merge |
| 24 Feb 2021 | S09 urgent-measures/review act | S22 liquidation extension | Preservation/access dispute becomes an extension order |
| 6 May 2021 | S10 reposición act | S40 Auto 356/2021 nullity | Procedural remedy and nullity analysis merge |
| 15 Oct 2021 | S13 act | S14 act | Finality and implementation language merge |
| 26 Jan 2022 | clarification Auto 1 | clarification Auto 2 | Two clarifications become one original adjudication |
| 26 Apr 2022 | decree lead 1 | decree lead 2 | Primaries not yet controlled; must not be treated as one proved event |
| 20 Jun 2022 | act lead 1 | act lead 2 | Primaries not yet controlled; must not be treated as one proved event |

The date must never be the unique identifier. A future site page must display title/function and canonical act ID next to every date.

## 4. P1 public statements requiring qualification

### 4.1 “Competition was real” and anonymous third bidder

At `es/adjudicacion-2022-reconstruccion-documental/index.html:27,37` and the English counterpart, the page states that competition ceased to be hypothetical and later that it was real. The native third-party bidder proposal contains placeholders/blank execution or acceptance material; filing, authority and available funds are not independently proved. The 18 May Auto now proves the court's actual treatment: third-party bidder did not appear or lodge the bond and CAM was approved.

Use:

> A documented third-party bidder proposal and a judicially designed licitation mechanism existed. The Auto records third-party bidder's nonappearance and absence of bond and definitively approves CAM. Whether third-party bidder had authority, funds or a binding filed offer beyond the material recited by the court remains a separate evidential question.

### 4.2 “Transferencia dominical” / “conveyed”

`es/adjudicacion-2022-reconstruccion-documental/index.html:41,44` and related English and dynamic text treat Protocol 457 as proof of a completed title transfer. The notarial instrument proves what the parties declared and purported/executed. Registry implementation, property-by-property title and the legal effect on non-parties require separate proof.

Use “the deed purports to execute a dación over the enumerated schedule” or “the deed records notarial execution”, reserving “registered owner” for a controlled registry entry.

### 4.3 Categorical missing-bridge and no-possession-order headings

`es/ric-private-equity-sun-park/index.html:334` says the legal bridge “faltaba”; line 387 headlines “No hubo auto judicial de posesión”. The body is more careful than the headings.

Use the exact negative-evidence formula:

> **NO PRIMARY JUDICIAL AUTHORISATION YET IDENTIFIED.** No reviewed primary order has yet been found authorising the specified transition in possession/control/exploitation. This is a corpus finding, not proof that no such act exists in the complete court file.

### 4.4 Criminal/falsity language

`es/ric-private-equity-sun-park/index.html:427,440` uses “material-falsehood control” and says a representation was materially false when spoken. The record supports comparison with contemporaneous mixed title, not speaker knowledge, intent or a legal finding of falsity.

Use:

> The whole-complex representation is not reconciled with, and is materially inconsistent with, the contemporaneous title/judicial record to the extent it described all units as owned, acquired or free of charges. Knowledge, intent and legal characterisation remain unproved unless established by a competent decision.

Any quantified criminal “strength” score in the minified criminal-engineering pages should be withdrawn or recalculated after the source graph is corrected. It is an investigative-priority score, not an evidential grade or probability, and currently inherits corrupted inputs.

### 4.5 The 54/190/18 unit split

`es/ric-private-equity-sun-park/index.html:679` calls the exact split confirmed. Elsewhere, including line 790, the source is correctly framed as a CAM/RICPE pleading or certificate. Until independently reconciled finca-by-finca against registry notes, the number is a **documented representation**, not an independently confirmed title census.

### 4.6 2018 locales and €400,000

The primary Protocol 2150 records a cheque and carta de pago. The AC's 20 December report states that the cheque became effective, that an LPB collection account was opened, and that initial applications included AC remuneration and creditor contact. Those are primary statements and must not be described as wholly missing.

What remains absent is independent bank-clearing evidence, a complete ledger, definitive treatment after the 24 October 2019 non-convalidation act, and the final title/Registry chain.

Exact formulation:

> Protocol 2150 records cheque/receipt and the AC report states that the cheque became effective and describes initial applications. Independent bank and complete insolvency-ledger corroboration, post-nonconvalidation treatment and final title/Registry effect remain unresolved.

This requires correcting stale “native deed/payment pending” statements in the calificación primary-source closure injector and narrowing `es/ingenieria-forense-criminal-sun-park/index.html:83`, which currently says the €400,000 line lacks a complete primary source.

### 4.7 Annex II and liquidation-plan normalisation

The 15-page core liquidation plan is controlled. Annex II is a separate source, face-dated 15 January, notwithstanding a misleading 15 February filename. It duplicates finca 8579, omits 8519, values the 159-unit schedule at €7,065,384.42 and differs by €457,832.55 from the plan/AP 159-unit figure of €6,607,551.87. Later instruments silently use a corrected range.

The live 262-finca map accurately gives plan values at `es/mapa-forense-sun-park-262-fincas/index.html:45` and the corresponding English line, but omits this Annex II defect. A primary-order page must display both schedules and the arithmetic difference rather than normalising them into one list.

### 4.8 BORME CAM→HNT succession language

`es/index.html:749` and `en/index.html:748`, together with pacto-comisorio and minified criminal pages, overread the BORME notice as completed transfer by universal succession. The official notice proves that a proposed segregation was announced/approved in the terms stated. It does not supply the executed project/deed, balance, complete asset/passive/contract/licence schedule or registry implementation.

Use:

> The BORME notice announced/recorded approval of a proposed segregation described as universal succession. Whether and how it was executed and registered, and which assets, liabilities, contracts, licences and claims passed, remains to be proved by the implementation instruments and registers.

### 4.9 Finality and later 2022 acts

The LAJ statement dated 14 February proves the court office's treatment at that time; it does not prove terminal finality against every later act or remedy. The site refers to 26 April decrees as though the primary acts were controlled. They are still docket leads, and two separate decrees are indicated. Later events continue through July 2022 in the available docket material.

`es/ric-private-equity-sun-park/index.html:748–751`, homepage line 508 and their English counterparts must identify which proposition is taken from a controlled primary and which is only a referenced docket entry.

### 4.10 Debt, valuation and surplus vocabulary

The following figures have different legal functions and must not be joined into a single subtraction without an order that authorises that function:

| Figure | Evidential function |
|---:|---|
| €9,052,251.69 | recognised secured-credit figure in the identified source |
| €9,052,877.88 | AP recital; unexplained €626.19 difference |
| €12,251,446.21 | mortgage burden/amount stated in the relevant instrument |
| €13,168,082.02 | 2021 threshold / deed-stated consideration; not automatically allowed credit |
| €9,776,003.13 | whole-complex appraisal, including foreign/third-party fincas |
| €7,096,913.83 | LPB real-estate figure |
| €6,607,551.87 | plan/AP 159-unit figure |
| €7,065,384.42 | Annex II 159-unit figure; €457,832.55 difference |
| €1,145,798.29 | Community component imposed on a bidder; not automatically a judicially allowed claim |

The correct public status remains:

> **No primary evidence of payment of a judicially required surplus has yet been identified.** The record does not presently justify stating that nonpayment is proved, nor does it justify declaring a surplus due without first identifying the court-authorised valuation, allowed debt and operative condition.

## 5. Claims presently supportable and worth preserving

The reverse-engineering exercise does not require wholesale retraction. The following core propositions are substantially aligned with the controlled record if their current qualifications remain visible:

- LPB was the insolvency debtor; the whole mixed-ownership Sun Park complex did not thereby become insolvency-estate property.
- “Sun Park”, “hotel” and “unidad productiva” are not substitutes for a finca-by-finca title schedule.
- The 26 June 2018 suspension was limited to identified fincas and did not suspend every liquidation act.
- The 24 October 2019 act was a non-convalidation ruling; it was not a criminal finding.
- Protocol 457 enumerates 159 mortgaged LPB fincas and omits identified third-party property; it does not by itself establish final allowed debt, all mortgage cancellation, Registry implementation or surplus performance.
- The 2018 material-control/possession question is analytically separate from 2021 approval and 2022 deed/title implementation.
- No reviewed primary Auto has yet been identified that expressly transfers Matkator's extraconcursal property into the estate or authorises CAM to exploit all third-party units.
- The site is right to separate recognised credit, mortgage exposure, bidder threshold, deed-stated consideration, Registry values and surplus.
- Matkator fincas 8584 and 8588 have a controlled title basis and are omitted from the 2022 deed schedule; other units such as 8497/8498 require their own disputed registry chain. The property-level status must not be generalised.
- “No primary evidence of payment has yet been identified” is the correct surplus formulation.
- Later investor/operator statements may be compared with contemporaneous title, but only as attributed representations.
- The recent Article 82 pages correctly distinguish potential remedies and do not treat insolvency conclusion as automatic erasure of title, restitution or damages issues.

## 6. Current remote delta versus the earlier audit

Commit `1270540` is 39 commits ahead of `a50e034`, with 32 changed/added files and approximately +2,118/−18 lines. Important additions include:

- ES/EN asset-recovery, intervention and confiscation pages;
- ES/EN insolvency-administrator/Article 82 pages;
- `MASTER_FORENSIC_GAP_CLOSURE_RESUMABLE_PROTOCOL`;
- `RECENT_REPOSITORY_WEBSITE_EMAIL_PUBLICATION_AUDIT_21AUG2026.md`;
- asset-recovery loaders and changes to `assets/site.js`; and
- recent-scope verification scripts.

These additions are generally careful about preservation not proving proceeds and about distinguishing legal routes. They do not supersede the legacy claim graph. The recent audit itself was conducted against an earlier current point (`7ae8…`), not `1270540`, and expressly concerns recent publication. It must not be cited as an audit of the Concurso autos or legacy source accuracy.

One new phrase should be clarified before wider publication: the Article 82 pages refer to “two distinct €400,000 trails”. Without identifiers, that can sound like two proved payments or transactions. Name the two instruments/claims precisely, or state that one is the locales instrument and the other is a separate alleged implementation trail still requiring reconciliation.

## 7. Why the current validation suite passes the wrong site

The following scripts passed against current `main`:

- `scripts/audit_adjudicacion_legacy_language.py` — PASS, 462 files, no matches;
- `scripts/validate_publication_integrity.py` — PASS, 29 manifests; zero changed files inspected in the local invocation; and
- `scripts/validate_mission_critical_repo.py` — PASS, 51 workflows.

They do not test the facts at issue. The legacy-language audit uses a narrow phrase list and excludes at least one adjudication-provenance injector. It has no rule for wrong date, wrong appointee, wrong bidder/winner, wrong judicial function, same-date conflation, stale missing-primary status or overreading a BORME notice. The publication check can inspect zero changed files when a base SHA is not supplied and validates shape/existence rather than evidential accuracy. The mission-critical check is operational.

Add evidential CI controls:

1. prohibit “26 January 2022” within a configurable token window of “adjudication/award” unless in a correction block;
2. prohibit “15 February 2018” as the creditor-substitution ruling date;
3. prohibit “Aweswell” as the €14.8 million bidder/winner in Auto 164;
4. assert the opening Auto's appointed AC against a canonical primary field;
5. fail when a controlled primary remains `PRIMARY_PENDING`;
6. require one canonical ID per act and allow multiple acts per date;
7. require every public decision record to carry primary locator, SHA-256, page count, completeness and operative-function label;
8. lint negative-evidence propositions for “yet identified / reviewed corpus” language;
9. render routes in a headless browser and scan the final DOM, because JavaScript injects the worst contradiction after static HTML validation; and
10. fail deployment if any file labelled `REPOSITORY-ONLY` or `DO-NOT-PUBLISH-YET` is located under the public Pages tree.

## 8. Publication and privacy consequences

The repository is itself the public website source. `robots.txt` allows crawling. The `archive/` path is deployed and directly reachable; the live `decisions.jsonl` was verified by HTTP. A label such as `REPOSITORY-ONLY`, `PRIVATE`, `DO-NOT-PUBLISH-YET` or “not linked from navigation” provides **no privacy control** when the file remains in the public repository or Pages artefact.

The public tree presently contains hundreds of archive files, numerous email-address strings and many Gmail/Drive locators. Six PDFs under `assets/docs` appear intentionally public/redacted, but none is the core set of Concurso autos needed to substantiate the site's strongest judicial propositions. Meanwhile, `assets/data/case-reconstruction-v1.json` visibly contains publication-control labels although the JSON is served publicly.

Recommended boundary:

**Public evidence layer**

- redacted judicial orders and deeds after page-by-page review;
- operative extracts, faithful translations, hashes, completeness status and source provenance;
- property/debt tables with minimum personal data;
- attributed public statements and correction log; and
- public-record correspondence only where necessary and proportionate.

**Private evidential vault**

- unredacted deeds and Registry notes containing personal identifiers;
- bank account, cheque, payment and full ledger material;
- credit-assignment economics and tax/investor data;
- private emails, access logs, telephone/address data;
- legally privileged or litigation-strategy material; and
- originals whose authenticity is preserved but whose publication is unnecessary.

If sensitive material has already been committed publicly, deleting it from the current branch alone does not remove it from Git history or mirrors. Any history remediation should be separately authorised, counsel-guided and preceded by a preservation-grade evidential copy. This report does not recommend destructive rewriting without that process.

## 9. Proposed replacement page

Create ES/EN routes titled:

**Concurso 36/2012 — What the Court Actually Ordered**
**Concurso 36/2012 — Lo que el Juzgado realmente acordó**

Its only organising unit should be:

> Primary judicial text → legal function → condition/reservation → later event → evidence of compliance/non-compliance → unresolved question

Each act card should contain:

- canonical act ID, exact body date, signature/service dates and aliases;
- judge/LAJ, court, proceeding, document type, pages, completeness, annex status and hash;
- applicant/support/opposition/heard/not-yet-verified;
- facts accepted by the court, separately from party allegations;
- legal provisions and reasoning;
- short Spanish operative quotation and faithful English translation;
- controlled function label: `AUTHORISATION`, `APPROVAL`, `ACKNOWLEDGEMENT`, `CONDITIONAL APPROVAL`, `PROVISIONAL MEASURE`, `RECITAL`, `PROCEDURAL DIRECTION`, `CLARIFICATION`, `FINAL DISPOSITION`;
- asset scope by finca and category;
- every condition/reservation/report-back/registration/payment requirement;
- a conspicuous field: “What had to happen before the effect later attributed to this order could lawfully occur?”;
- subsequent event and primary proof of performance;
- evidential label and missing-document ticket; and
- link to a redacted facsimile, where publication is justified.

Required modules:

1. **Order reader** — the operative part and its legal function, not a chronology-only summary.
2. **Same-date disambiguator** — displays every act issued on that date.
3. **Asset-scope gate** — LPB / Matkator / other owners / locales / common elements / exploitation / movables / keys / receivables / goodwill / licences.
4. **18 May 2021 → 21 February 2022 chain** — separates approval, appeals, clarifications, LAJ testimony and deed.
5. **Condition tracker** — including any payment, reporting, consignation, surplus and Registry step.
6. **Debt/value ledger** — keeps legal functions separate and displays the €626.19 and €457,832.55 discrepancies.
7. **2018 control gap** — uses the exact label `NO PRIMARY JUDICIAL AUTHORISATION YET IDENTIFIED` for each unbridged material transition.
8. **Corrections register** — records the false text, replacement, primary basis, affected descendants and deployment date.
9. **Missing-document register** — P0/P1/P2 retrieval, holder and closure criterion.

This page should be generated from one versioned canonical dataset, not copied into ES/EN HTML and again into JavaScript. Dynamic code may render the data; it must not contain independent factual prose.

## 10. Exact remediation order

1. **Snapshot and preserve** current remote `1270540`, deployed hashes and the present contradictions as correction evidence.
2. **Correct the canonical act graph first:** 8 February date/remedy; 18 May third-party bidder/CAM result; two 26 January clarifications; original AC; complete 4 June copy; all same-date pairs.
3. **Supersede, do not silently overwrite, false high-authority registers**, especially the 19 August retracto correction register and LPAM magistrado digest.
4. **Rebuild all descendants:** JSON/CSV, ES/EN static pages, route injectors, timelines, source notes and ingestion queues.
5. **Remove factual prose from route JavaScript** or generate it from the canonical graph.
6. **Correct the public P1 qualifications:** third-party bidder mechanics, deed versus Registry title, locales payment status, BORME implementation, 54/190/18 attribution, finality and negative-evidence language.
7. **Add rendered-DOM and canonical-primary CI tests** before deploy.
8. **Publish the dedicated court-orders page and redacted primary set** only after privacy review.
9. **Move private/repository-only material outside the public Pages repository** and conduct a separate exposure/history assessment.
10. **Re-run a bidirectional audit:** every public claim must resolve to a primary act; every corrected primary field must enumerate all public descendants.

## 11. Release-blocking correction checklist

The next publication should not be described as forensically reconciled until all boxes below are closed:

- [ ] Auto 164 live injection no longer says Aweswell bid/won.
- [ ] third-party bidder nonappearance/no-bond and CAM definitive approval appear wherever the licitation is described.
- [ ] The creditor-substitution Auto is dated 8 February 2018 everywhere; 9/14/15 February are separately typed metadata.
- [ ] The appeal route is 20 days everywhere.
- [ ] No page calls 26 January 2022 the original adjudication.
- [ ] Both 26 January autos and both 15 October acts have separate IDs.
- [ ] The opening Auto's appointed AC is Francisco de Borja Rodríguez-Batllori Laffitte in every ledger.
- [ ] The 4 June 2018 source is marked complete and the “source of truth” label is removed or earned.
- [ ] Every located primary is removed from `PRIMARY_PENDING` and OPEN ingestion status.
- [ ] Locales text acknowledges Protocol 2150 and the AC report while preserving bank/ledger/title gaps.
- [ ] Annex II's duplicate, omission and €457,832.55 mismatch are visible.
- [ ] BORME language is limited to notice/approval, not assumed completed implementation.
- [ ] Negative claims say “not yet identified in the reviewed corpus”.
- [ ] “Materially false”/intent language is replaced with documentary inconsistency unless adjudicated.
- [ ] Publicly served files contain no `REPOSITORY-ONLY` or `DO-NOT-PUBLISH-YET` content.
- [ ] Final rendered DOM, not only source files, passes evidential regression tests.

## 12. Bottom-line answer to the central question

Starting only from the actual orders, the site **cannot yet present an unbroken legal and evidential chain asset by asset, condition by condition and euro by euro**. The principal breaks are now identifiable rather than speculative:

1. the site misidentified the bidder and result of the decisive 18 May 2021 Auto;
2. it displaced the original approval to two 26 January 2022 clarification autos;
3. it does not yet prove every step between judicial approval, deed execution, Registry implementation and later CAM→HNT position;
4. it does not identify a judicial bridge for third-party/Matkator property or 2018 whole-complex control and exploitation;
5. it does not yet reconcile the 2018 locales payment/title chain after non-convalidation;
6. it does not establish the legally operative debt/valuation pair from which a surplus could be calculated, nor primary evidence of any required surplus payment;
7. it normalises inconsistent liquidation schedules; and
8. its own public canonical records remain factually stale.

Those breaks should be published as finite document questions, not filled with allegations. Correcting the source graph before adding narrative is the shortest route to a defensible, non-defamatory and genuinely forensic site.
