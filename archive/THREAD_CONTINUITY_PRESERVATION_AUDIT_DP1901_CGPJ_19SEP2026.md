# DP 1901 / Ref.21 / Ref.24 / CGPJ — thread continuity & preservation audit

**Audit date:** 19 September 2026  
**Scope:** the ChatGPT thread that published and verified the DP1901 / Ref21 / Ref24 / proposed CGPJ Alzada 286/2026 response package, followed by the user's instruction to keep updating throughout the day until filing.

## Controlling live release

- Repository: `sbu001monterecco/por-derecho`.
- Integration PR: #1637.
- Reviewed candidate: `def444afed408263837b920fb19dc01c0ed088ca`.
- Merge SHA on `main`: `53ee6b0b08e9bcfc2f3cf19ce5aff72f0620165c`.
- Exact-SHA Pages deployment: run `35440808510`, Pages run 1613 — success.
- DP1901 exact live verifier: run `35440809176` — success; `LIVE_BYTES_VERIFIED`, 8/8 controlled resources byte-identical to merge source.
- Publication controller verify: run `35440818318` — success; `VERIFIED_FOR_SCOPE`, fence 11.
- Exact-head PR matrix before merge: 30/30 successful.
- Fiscalía control queue closeout: issue #1621, comment 5741569323.

The 8/8 live-byte denominator is limited to its actual controlled DP1901/DIP2 resources, including both ES/EN DP1901 main pages and both ES/EN 14-Sep Auto/order pages. It is not a claim that every new DOCX/PDF/gallery file received an independent HTTP byte comparison.

## Live routes

- Spanish Auto / response: https://sbu001monterecco.github.io/por-derecho/es/dp-1901-2026-auto-14-septiembre-2026/
  - `#response-full`
  - `#response-pdf`
  - `#visual-gallery`
- English order / response: https://sbu001monterecco.github.io/por-derecho/en/dp-1901-2026-order-14-september-2026/

## Controlling chronology / attribution boundaries

1. Ref.22: 18-Jun-2026 complaint against the Administrador Concursal; later identified as DP1956/2026 / Plaza 1. Do not treat that as certification that DP1956 was necessarily the legally correct destination or that electronic opening occurred on 25-Jun.
2. Ref.24: 18-Jun-2026 written denuncia / notitia criminis concerning the judge lane and directed to the TSJC; dependent 13-page supplement filed 25-Jun.
3. Ref.21: separate private-actor complaint filed 25-Jun.
4. Two separate actions occurred on 25-Jun: filing Ref.21 and adding the dependent supplement to Ref.24.
5. User's controlling firsthand statement: on 25-Jun the physical Ref.24 file remained at Decanato untouched, unscanned and unallocated. Earlier electronic scanning/allocation is not to be presented as an equally supported explanation; official electronic history remains open.
6. User's categorical factual position: DP1901 originated from the private-actor complaint and Ref.24 was associated later. Preserve that as attributed user testimony, not independently certified system history.
7. The handwritten `25`→`18` and added `24` account is a handling/traceability description, not independently proved falsification, backdating or intentional alteration.

## Proposed CGPJ response — preserved identity

- `drafts/cgpj/2026-09-19_DP1901_CGPJ_RESPONSE_PROPOSED.docx` — 48,709 bytes — SHA-256 `81e9d6afaabeab00a343fc9e96d372e0ae88f78b734f1a72e1edb94b33d14ffc`.
- `drafts/cgpj/2026-09-19_DP1901_CGPJ_RESPONSE_PROPOSED.pdf` — 121,140 bytes — SHA-256 `cc72caa9884b1cd362687525c7d086533f8c0a2ab5e0621a68b025975dd9586c`.
- `drafts/cgpj/2026-09-19_DP1901_CGPJ_RESPONSE_PROPOSED.md` — 26,180 bytes — SHA-256 `5264a784d74da5da51e779a08dee086e21234d1e837aeed2e5932178a05eb2b1`.
- Status: **BORRADOR PROPUESTO / NO PRESENTADO / NO REMITIDO**.

The CGPJ submission, any judicial challenge to the 14-Sep Auto and the E.G. 745/2026 response remain separate procedural lanes.

## Images / editorial controls

GitHub derivatives:
- PD-DMA-0007 — `assets/visuals/dp1901-20260919/01-single-grave.png` — SHA-256 `a6bbe9e4f53fd2e1c6566454bd9d32b7860ffdee78eded2394be8d8244cf6dea`.
- PD-DMA-0008 — `02-decanato.png` — `9d06dc1340f8aa050ae71780eb24a265b7b5ce467e9178c7b1aa976a4ddfd54a`.
- PD-DMA-0009 — `03-fiscal-corpus.png` — `c3c5c5783f949f0e6b8af7010313ccc5e30e708e98e64ba4e59bf23ca7657b88`.
- PD-DMA-0010 — `04-atlante.png` — `ddbc5e4a5f25f025d5577b7efcd0f7fb84dd36d65732a915288db3a608305e4e`.
- PD-DMA-0011 — `05-composite-annex.png` — `329eb2050a8ba0f5a15138d34261cf73d4f257f18cd5ed3f1b8ec5f3e472b554`.
- PD-DMA-0012 — `06-traceability-overview.png` — `0a196b6cf699a9171ad98b44b00bc12faf87e86bc33cf1b09ba3795e18c92ee9`.

Mandatory controls:
- “single grave/fosa” is metaphorical; it does not prove destruction, intent or legal extinction.
- Decanato historical artwork depicts Catalunya, not Canarias.
- Fiscalía artwork incorrectly expands DIP as “Previas”; the Auto uses “Diligencias de Investigación Preprocesales”.
- ATLANTE artwork does not prove an exact 8–17 July association window.
- Composite panel 2 incorrectly labels the judge lane Ref21/25-Jun; controlling chronology is Ref24/18-Jun plus dependent supplement on 25-Jun.
- Incoming arrows do not establish the exact corpus reviewed by Ministerio Fiscal.
- Crests/institutional settings do not imply official authorship.
- Neutral lead visual remains `assets/visuals/dp1901-routing-collision-20260919.svg`.

## Google Drive preservation

Dedicated owner-only preservation folder at audit time:
https://drive.google.com/drive/folders/1Kg8LhvFbMAQEo7tLDKB8mgUnQG27E1tU

Parent: `Por Derecho Backups`.

Readback confirmed 17 files:
- this audit + machine-readable manifest;
- 3 proposed response artifacts (DOCX/PDF/Markdown);
- 6 original explanatory image sources;
- 6 deployed GitHub web derivatives.

A Drive root listing also exposed at least one `TEMP_DP1901_*` transfer file. It is not relied upon as preservation evidence. This audit did not delete it.

## Open evidence / non-closure

- Signed 29-Jul-2026 Ministerio Fiscal report, author, assignment, reasoning and exact corpus.
- DP1901 initiating/reparto record and certified Ref21/Ref24 electronic association history.
- Native/certified 14-Sep Auto and notification/access metadata.
- Certified bridge for any union, reassignment, routing or segregation among Ref21, Ref22, Ref24, DP1901 and DP1956.
- Native CGPJ attachment for the 26-Jun communication remains technically unverified where earlier retrieval returned 403 / truncated text.
- Six historical images are not approved formal evidentiary annexes; neutral traceability artwork remains preferred for eventual filing.

## Procedural boundary

No CGPJ filing, judicial appeal, E.G. 745 response, authority email, RedSARA/AGE submission or court contact was performed by this thread. Public publication is not filing or service.

The user instructed that the public package is to be updated throughout the day until filing. Any successor must refresh current `main`, preserve merge `53ee6b0b...` as a verified predecessor, keep the three procedural lanes distinct and use the repository's single integration/controller path.

## GitLab continuity

GitLab remains canonical when access is restored, but it is blocked at this audit. Do not blindly overwrite later GitHub work. Reconcile this verified release and any same-day GitHub successors against restored GitLab state before updating GitLab.

## Deletion-safety conclusion

The scoped substantive thread state is recoverable from:
1. GitHub release history and PR #1637;
2. issue #1621 closeout;
3. this source-controlled audit;
4. the dedicated Google Drive preservation folder containing the actual response and image package.

Subject to successful merge/readback of this audit record, the thread is **preservation-safe for retirement/deletion for this scoped DP1901/CGPJ publication workstream**. This is not a conclusion that the underlying legal/evidentiary investigation is complete.
