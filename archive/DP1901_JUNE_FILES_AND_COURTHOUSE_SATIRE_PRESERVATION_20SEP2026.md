# June Controls 21 / 22 / 24 and courthouse satire: scoped preservation delta

**Date:** 20 September 2026. **Role:** WORKER. **Base:** `0029415c77035785ea65ecf71655f96843ed4036`. **State:** source inventory and findings preserved on a worker branch; not merged or deployed by this record.

The user requested preservation in GitHub of the files and information discovered in the courthouse-image discussion. This record preserves the distinct source versions, the substantive findings and limitations, and the proposed visual concept. It does not replace the canonical proceedings/evidence registers, publish private originals, or create a rival integration lane.

At the fresh Control Tower read, another thread had claimed the bounded `integration/dp1901-platform-recovery-nexus-20260920` lane. Its claim is at [Control Tower comment 5752598831](https://github.com/sbu001monterecco/por-derecho/issues/1428#issuecomment-5752598831). This worker supplies an additive source delta for that lane or its verified successor; it does not change the integration assignment.

## 1. Canonical destinations and exact recovered versions

Reuse:

- [Three-track source inventory](../data/three-track-full-digitisation-20260904.json), control `PD-THREE-TRACK-DIGITISATION-20260904-01`;
- [Three-control continuity graph](../assets/data/control-21-22-24-continuity-v1.json), control `PD-C212224-001`;
- [Control 24 source inventory and public derivatives](../evidence/judicial-governance/decanato-reference-24/README.md);
- [New bounded recovery crosswalk](../evidence/judicial/dp-1901-2026/june-source-recovery-20sep2026.json);
- [DP1901 source closure](../evidence/judicial/dp-1901-2026/PROCEDURAL_IDENTITY_SOURCE_CLOSURE_18SEP2026.md).

Seven exact native PDFs are recovered in private working custody. Their page counts, byte lengths and SHA-256 values are recorded in the recovery crosswalk. Four core source hashes match the existing canonical inventory: Control 22 principal (55 pages), Control 24 unified package (79 pages), its dependent supplement (13 pages), and Control 21 standalone principal (86 pages). The other three are the separate 82-page AC companion package, 163-page private-actor predecessor and 202-page later print package.

**Preservation ceiling:** the source inventory in public Git is not storage of the native PDF binaries. The native pleadings, email bodies, identification data, signatures, private metadata and any privileged material remain outside public Git. A copy in temporary working storage is not a permanent-backup certificate. Any full derivative publication requires source-specific privacy review and the existing publication process.

The existing public Control 24 derivatives contain the complete principal pleading and dependent supplement with their disclosed redactions, not every private annex in the 79-page native package. The three-track dataset is a public-safe structured digest; do not describe it as the raw full original.

## 2. New source-version finding: two non-identical 86-page texts

The standalone 86-page Control 21 PDF matches canonical hash `3f4bd2bbbc963605e4cc94bc73d116157e2bf4a2266e2285b013f38de9e90736`.

The 202-page print bundle has hash `28c238e719dace2197a7e30655a4727bf26ad01e7d6e73832e75e81582179b8e`. Its principal occupies global pages 3–88. A complete page-by-page native-text comparison, after removal of the print wrapper and whitespace, matches **83 of 86** principal pages. The differences are not solely pagination:

| Standalone principal | Global print-package page | Difference |
|---|---:|---|
| 78 | 80 | Annex 6 description replaces the English source expression `tres workstreams` with `tres líneas procesales`. |
| 83 | 85 | Suplico 13 adds Annex 10 to Annexes 5–9 and changes the description to include traceability. |
| 84 | 86 | The continuation expands the wording on alleged manufacture/use of minutes and certifications, ownership/disponibility/cost/benefit, financing/public-resource links, and the visual source/contradiction/verification module. |

Retain both versions. Do not overwrite the canonical standalone source, silently change its hash, call the principal inside the print bundle byte-identical, or decide which exact version reached the judicial file merely from its filename. If the version matters to a pending response, compare the actual receipt, stamped copy, incorporation record and complete judicial corpus.

The 82-page AC bundle likewise has its own earlier 52-page principal and a 29-page companion section. It is not automatically the later 55-page principal with unchanged annexes. The 163-page private-actor predecessor contains a 69-page principal and 94 subsequent pages; its principal does not supersede the later 86-page source.

## 3. Substantive findings that must not be reduced to file-routing criticism

### A. Control 22 — administrator's powers, knowledge, acts and patrimonial effects

**Source:** the exact 55-page principal, especially pages 2–4, the historical/knowledge sections, transaction and accounting sections, and its final requests. Companion material has its own version status.

The complaint is directed to the court-appointed insolvency administrator's own exercise of entrusted powers over LPB: administration, information, protection, defence-related permissions, preservation, liquidation and accounts. It does not merely allege that the administrator failed to stop everything done by other people. It asks which powers were available, what information was received, what was done or omitted, what patrimonial consequence followed, and who may have benefited.

Its principal subjects include the disputed community authority/debt background; early warnings; the January–June 2018 access/possession and security chain; the alleged 7 June displacement; the conditionally funded 2018 exit; the November 2018 OB REM transaction and approximately EUR 400,000; the subsequent non-convalidation; competitive conditions, adjudication, income/fruits, recovery rights and final accounts.

**Classification:** allegations and proposed actor-specific inquiries in a party pleading. Neither the complaint nor a source-hash match establishes misconduct. LPB's estate, Matkator's property and third-party rights must remain distinct. Knowledge held by the administrator is not automatically knowledge held by the judge.

The reproduced January 2018 correspondence identified in the earlier annex reading is a concrete access/possession source, not just an abstract theory. Any substantive publication must retain its original date, author, recipient, context and actual wording in controlled private custody; public summaries must not replace it with an invented order or enlarge its authority.

### B. Control 24 — judicial decisions, knowledge and a proposed change in the function of the threshold

**Sources:** 79-page unified package, with the 27-page principal at native package pages 4–30 and its selected annexes; dependent 13-page supplement of 25 June, especially pages 2–9.

The principal identifies five subjects: the conditional funded exit and judicial knowledge; the difference between recognized credit, mortgage liability, interest and the competitive threshold; the OB REM transaction, non-convalidation and implementation; competition and adjudication; and the precise identity/capacity of each creditor, bidder, adjudicatary and title-holder. Six groups of judicial decisions are identified. This is broader than a bare disagreement with the 2025 separation decisions described in DIP2.

The dependent supplement is particularly important. It corrects the possible imprecision of saying the recognized secured credit was formally raised from about EUR 9.052 million to more than EUR 13 million. The narrower question is whether an instrumental threshold for a better offer, which was not a final determination of default-interest amount/classification, was later treated as final or res judicata and given operative economic effects without the requested documentary reconciliation.

The supplement describes express invocation of STS 227/2019, its application by the same magistrate in the Parodi/Talleres Jinámar matter in January 2020, the LPB decision of May 2020, and an express differentiation maintained in May 2021. **Knowledge of the doctrine is not identical to knowledge that a decision is unjust.** Preserve both the pointed comparison and the stated possible lawful distinctions; the two cases must not be declared identical without examining their procedural objects and full records.

The annexes include contrary positions and judicial material. Some are expressly extracts. The conditional financing proposal must not be transformed into an unconditional or already-disbursed rescue. The approximately EUR 400,000 must not be counted twice or treated as proved misappropriation without the payment/accounting trail.

**Classification:** documented existence/content of the pleading; allegations, comparisons and inquiries within it. Do not convert the complaint's legal hypotheses into criminal findings or numerical guilt probabilities.

### C. Control 21 — alleged manufacture and use of authority, not mere arithmetic

**Sources:** 86-page standalone principal, notably pages 1–8 and 9–14, later substantive sections and requests; separately preserved 202-page print package and 163-page predecessor.

The complaint expressly alleges manufacture and instrumental use of minutes, certifications and balances to present authority, meetings, attendance, representation, votes, agreements, expenditure or debt differently from the events alleged to have occurred. The alleged subsequent uses include voting exclusion, bank authority, security, access, works, litigation and representations to third parties. Preserve this as a serious attributed criminal hypothesis; do not dilute it into an ordinary bookkeeping dispute and do not adopt it as proved.

Its central provenance proposition is non-circular: a minute or certificate cannot, by its own assertion alone, supply independent proof of the authority of the person who convened, signed, certified or relied on it. The complaint asks for the prior title, mandate, appointment, representation, actual expenditure and transmission/use chain.

Its three interacting subjects are: hotel title and unitary operation; community authority/accounts/debt/voting; and the credit-acquisition/access/valuation/liquidation/project sequence. It distinguishes closed dissident units from an entirely closed hotel and seeks a property-by-property examination of what Actúa saw versus the contemporaneous Gesvalt description. A valuation difference alone is not proof of dishonesty.

The five private actors remain individually treated. The administrator is expressly not added as a sixth accused in this pleading. Professional advisers, investors, brands and other documentary custodians do not acquire knowledge, control or culpability merely because the complaint mentions them.

The later RIC/HNT/MYND, financing, public-support, exploitation and income context is relevant to the alleged economic effects and preservation/recovery question. Later economic participation or title cannot be used as automatic proof of earlier knowledge, improper coordination, or retrospective authority for an earlier physical act.

## 4. Procedural identities and the object-contraction questions

Keep three autonomous June filings distinct:

- Ref.22, 18 June: administrator-related; later DP1956 association remains subject to the source-certified intake bridge and its separate provisional-dismissal history.
- Ref.24, 18 June: judge-related notitia/complaint originally directed to the TSJC; its 25 June supplement is dependent on this filing.
- Ref.21, 25 June: autonomous private-actor complaint; contemporaneous material supports the user's Ref.21 → DP1901 account, while the certified electronic creation/reparto and later Ref.24 association mechanism remain outstanding.

The user's firsthand account that Ref.24 was still physically untouched, unscanned and unallocated on 25 June must remain attributed testimony, not silently flattened into a neutral uncertainty about what he observed. Independent certification of the court-system history remains a separate evidence question.

Two questions must not be collapsed: (1) how the private-actor material was treated in DP1901; (2) how the broader judge-related June allegations were delimited against the narrower DIP2/2025-decision account. The 14 September Auto's stated adverse reasoning, including its assessment of evidential foundation, remains visible and must be answered substantively. Its reference to the 29 July Fiscal request establishes a dated intervention, not the report author's identity, full reasons, complete corpus or improper coordination.

The existence of court/Fiscal acts and a contested outcome does not itself prove the clandestine activity envisaged in the proposed satire. Signed Fiscal report, author/assignment, full transmitted corpus, initiating document, electronic association history, operative scope and notification records remain source-production questions. Absence from the reviewed corpus is not proof of destruction or nonexistence.

## 5. Earlier operational discoveries to retain without stale-state promotion

The earlier part of this thread located the same-day national-LAJ and Anticorrupción receipts, after the public 11-of-13 snapshot, and a private census recording 13 of 13 defined personal actions. The active integrator should reconcile those actual receipts and the current private census before changing public status. This worker delta does not silently upgrade the main action ledger or claim admission, downstream incorporation, examination, preservation execution or response.

Preserve the distinctions between the immediate E.G.745 incorporation/preservation notice, the separate substantive E.G.745 response, and counsel-dependent judicial remedies. Preserve the actual three-part provincial sent-email sequence as one communication package, not three additional independent legal actions. Source systems, not public Git, retain private message identifiers and attachment locators.

## 6. Honest coverage statement

The earlier response reported complete textual reading of four core PDFs, totaling 233 page instances, plus the 29-page AC companion and 94-page predecessor annex sections. Preserve that as the reported reading scope, not as a new independent audit of every page, annex or original court document.

This preservation pass independently verifies seven recoverable native PDFs, their page counts/byte lengths/hashes, four canonical core hash matches and the full 86-page standalone-versus-print textual comparison. It does not certify complete visual review of every 202-page bundle annex or authenticate every underlying exhibit. All 680 page instances in the seven files include duplicated and predecessor material; that number is not unique evidence or new filings.

Prior broad claims of a 'full' GitLab website, whole GitHub or entire mailbox scan are not certified here. No exhaustive URL/commit/message denominator has been established by this recovery pass. The GitLab repository remains untouched; its public website is a dated comparator, not today's operational ledger.

## 7. Image work and public/private boundary

The current concept is preserved in [the separate visual brief](visual-briefs/DP1901_SHAME_AND_JUSTICE_CONCEPT_20SEP2026.md). **No new image has been generated.**

Use the existing six-image gallery through its [publication manifest](../publication-manifests/dp1901-cgpj-response-images-20260919.json), not invented replacements. Its corrections remain controlling: the grave is metaphor; the old Decanato background is geographically wrong; the earlier DIP expansion and a Ref.21/Ref.24 composite label are incorrect; ATLANTE artwork is not an official screenshot or proof of causal association.

The earlier 95% image-readiness estimate and 95% substantive-mastery estimate are subjective workflow judgments, not empirical measurement, source-completeness certification, probability of guilt or a guarantee of publication safety.

## 8. Integration acceptance and remaining work

For the active integrator:

1. Reuse the existing source IDs and add the three newly fingerprinted bundle variants as version/custody crosswalk entries, not new historical events.
2. Preserve the exact standalone/embedded principal differences at pages 78, 83 and 84. Do not erase either version or infer the filed copy.
3. Incorporate the substantive-object distinction into the current DP1901/platform recovery matrix without merging procedural identities or transferring attribution.
4. Preserve this concept and its disclosure requirements as unrendered editorial material. Do not publish it as evidentiary photography or an official illustration.
5. Keep native private PDFs and extraction objects out of the public repository. A confidential recovery bundle is distinct from a public derivative; any public full-text/facsimile treatment needs redaction and privacy inspection.
6. Verify the branch's exact committed files and use the existing single integration lane for any main merge, necessary validation, Pages deployment and route readback. Do not label branch preservation as merged or live.

**Readiness:** `READY_TO_INTEGRATE` for these bounded summaries, fingerprints and concept; `SOURCE_REVIEW_REQUIRED` for any new complete public derivative; `NOT_DELETION_SAFE_FOR_ALL_DISCOVERED_ORIGINALS` until durable private custody and all relevant prior artifacts are reconciled.

---

## Síntesis de conservación en español

Se conservan siete versiones PDF recuperadas mediante huellas y delimitación de fuentes. Las cuatro piezas nucleares —55, 79, 13 y 86 páginas— coinciden con las huellas ya registradas. Los originales privados no se publican. El principal autónomo de 86 páginas y el incluido en el paquete de 202 no son idénticos: hay diferencias en las páginas 78, 83 y 84 del principal, relativas a terminología, anexos y al apartado 13 del suplico. Deben mantenerse ambas versiones sin presumir cuál se incorporó judicialmente.

Control 22 examina facultades, conocimiento, actos y perjuicio atribuibles al Administrador Concursal; Control 24 individualiza decisiones judiciales, conocimiento y el posible cambio funcional del umbral; Control 21 denuncia expresamente posible fabricación y uso instrumental de autoridad, actas y deuda, no meras discrepancias aritméticas. Son alegaciones que deben contrastarse, no hallazgos de culpabilidad. La interconexión probatoria no fusiona personas, sociedades, patrimonios ni procedimientos.

La sátira propuesta contrapone la expulsión de la Vergüenza con el entierro metafórico de la Justicia y sus garantías. Permanece sin generar. La conservación en esta rama no equivale a integración en main, despliegue, presentación oficial, admisión ni validación de hechos o responsabilidad.
