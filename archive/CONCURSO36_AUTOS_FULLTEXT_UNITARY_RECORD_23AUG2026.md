# Concurso 36/2012 — Autos, responses and full-text filings: unitary repository/site record

**Control date:** 23 August 2026
**Scope:** the two proceedings concerning the Insolvency Administrator: (A) removal/separation and (B) remuneration/civil liability.
**Controlling public routes:**

- Spanish decisions page: `es/concurso-36-2012-autos-resoluciones/`
- English decisions page: `en/insolvency-36-2012-orders-decisions/`
- Spanish analytical digest: `es/concurso-36-2012-separacion-ac-honorarios/`
- English analytical digest: `en/insolvency-36-2012-administrator-removal-fees/`

> **26 August 2026 implementation overlay.** The 50-record specialist corpus remains unchanged. Its procedural identity layer is now reconciled through `PD-SP-R-0011`–`PD-SP-R-0016`, with Diligencias Preliminares 459/2024 expressly left without a caret pending its exact court and certified docket. DP 1901/2026 (`PD-SP-R-0005`) is corrected as the separate private-actor/CAM route, not the removal or remuneration track. See `archive/CAEPR_AC_REMOVAL_FEES_UNITARY_IMPLEMENTATION_AUDIT_26AUG2026.md`, `archive/AC_REMOVAL_FEES_REVERSE_ENGINEERED_CRIMINAL_THREAD_THESIS_26AUG2026.md`, and the quantitative/gap datasets under `assets/data/`.

## 1. Unitary result

The repository now holds a single, source-addressable corpus of **50 complete redacted transcriptions**: **25 court/LAJ acts** and **25 party filings**. The dedicated public page displays every located Judge, Appeal Court and LAJ decision in full and links all party filings. Ten key decisions also have irreversible, image-only public PDFs.

The corpus does not merge the two causes or the separate criminal/intake-reference lane. It supplies a common evidence architecture while preserving each procedure, actor and procedural effect.

| Lane | IDs | Court / LAJ | Party | Source pages / units | Latest located act |
|---|---|---:|---:|---:|---|
| Removal and appeals | `R01`–`R32` | 16 | 16 | 163 | Party allegations after Auto 223/2026, 23–24 Jul 2026 |
| Remuneration and appeal | `F01`–`F18` | 9 | 9 | 88 | LAJ transfer in RPL 421/2026, 7 Apr 2026 |
| **Total** | 50 stable IDs | **25** | **25** | **251** | — |

## 2. Controlling procedural distinction

| Question | Removal lane | Remuneration lane |
|---|---|---|
| Initial filing | Application under article 100 TRLC, 23 Apr 2025 | Ordinary civil-liability claim seeking EUR 110,956.97 for the estate, 1 Sep 2024 |
| First-instance outcome | Auto 1377/2025 dismisses for Aweswell's lack of active standing | Judgment 4/2026 dismisses for Aweswell's lack of active standing and awards costs |
| Merits reached? | No. The first order expressly says it need not enter the substantive grounds. The reconsideration order adds a limited ex officio observation but no ground-by-ground evidentiary adjudication. | No. The judgment expressly does not examine the remaining defences or the merits of the remuneration claim. |
| Appeal record | RPL 3304/2025 and 3319/2025; combined by Auto 223/2026 | RPL 421/2026; appeal treated as filed and transferred |
| Later merits result located by cut-off? | No | No |

No public text may say that the court found the remuneration lawful or unlawful, or that it rejected the seven removal grounds on their merits. A procedural dismissal is not a merits finding.

## 3. Repository architecture

### Canonical data and full text

- `assets/data/concurso36-autos-fulltext-v1.json` — authoritative 50-record manifest, including source hashes, provenance, copy status, procedure, effects and links.
- `evidence/insolvency-36-2012/concurso-autos/full-text/index.md` — human-readable corpus index and completeness boundary.
- `evidence/insolvency-36-2012/concurso-autos/full-text/*.md` — complete redacted transcriptions with page markers.
- `evidence/insolvency-36-2012/ac-removal-fees/provenance.md` — source-chain, redaction and public-PDF control.

### Public decision PDFs

- Existing/remade: Auto 1377/2025 and Auto 11 November 2025 in `evidence/insolvency-36-2012/ac-removal-fees/`.
- Eight additional Judge/LAJ documents in `evidence/insolvency-36-2012/concurso-autos/public-pdfs/`.
- Every public PDF is raster-only, without searchable text, forms, annotations, XML metadata or inherited verification data.

### Reproducible builders

- `scripts/build_concurso_autos_fulltext.py`
- `scripts/build_public_ac_orders.py`
- `scripts/build_concurso_autos_public_pdfs.py`
- `scripts/build_concurso_autos_pages.py`
- `scripts/validate_concurso_autos_publication.py`

### Whole-file continuation

- `archive/prompts/CONCURSO36_COMPLETE_JUDICIAL_PARTY_RECORD_ACQUISITION_DIGITISATION_PUBLICATION_PROMPT_23AUG2026.md` — controlling umbrella prompt for deriving the complete court-file denominator; obtaining every located Judge/Appeal Court/LAJ act, party filing, annex, receipt, notice and material party communication; preserving native originals; extending the stable corpus; digitising every page; and publishing only verified public-safe derivatives. The present 50-record removal/remuneration archive is its specialist baseline, not the denominator for the whole Concurso 36/2012 file.

The private originals are not committed. Builders accept a controlled local source directory and produce only minimised public artifacts.

## 4. Decision matrix

| ID | Date | Decision-maker | Instrument | Exact controlled effect | Public PDF |
|---|---|---|---|---|---|
| R02 | 28 Apr 2025 | LAJ Águeda Reyes Almeida | Diligencia | Joins the removal filing and transfers it to the AC for five days | yes |
| R04 | 20 May 2025 | LAJ Águeda Reyes Almeida | Diligencia | Joins the AC opposition and puts the file before the judge | yes |
| R05 | 12 Sep 2025 | Magistrate-Judge Alberto López Villarrubia | Auto 1377/2025 | Dismisses the removal application on standing without entering the substantive grounds | yes |
| R06 | 12 Sep 2025 | Magistrate-Judge Alberto López Villarrubia | Auto | Refuses clarification of a separate 25 July providencia; not the reconsideration order | yes |
| R09 | 11 Nov 2025 | Magistrate-Judge Alberto López Villarrubia | Auto | Rejects LPB and Aweswell reconsideration motions; opens non-suspensive appeal | yes |
| R30 | 15 Jul 2026 | Appeal Court Section Four | Auto 223/2026 | Combines RPL 3319/2025 into RPL 3304/2025 and orders missing procedural steps | yes |
| F02 | 7 Oct 2024 | LAJ, Mercantile Court 2 | Decree 113/2024 | Transfers the claim to the court handling Insolvency 36/2012 | yes |
| F03 | 28 Nov 2024 | LAJ Águeda Reyes Almeida | Decree | Admits the EUR 110,956.97 ordinary claim and summons defendants | yes |
| F13 | 21 Jan 2026 | Magistrate-Judge Alberto López Villarrubia | Judgment 4/2026 | Dismisses on active standing, with costs; does not reach remuneration legality | yes |
| F14 | 21 Jan 2026 | LAJ Águeda Reyes Almeida | Decree | Refuses clarification of the 1 September 2025 decree | yes |

The dedicated page also displays the complete text of the other 15 located court/LAJ acts, including appeal formation, summons, transfers, scheduling and accumulation directions.

## 5. Internal-source discrepancies preserved

The archive does not silently correct source text. Each affected record contains an editorial note. Controlled examples include:

1. `R01` and `F01` use “Disposición Adicional Tercera”; the repository identifies the statutory label as the Third Transitional Provision of Law 25/2015.
2. `R01` appears to omit a Document 6 reference.
3. `R02` attributes the incoming application to representation of Gil Marer although the application is captioned for Aweswell.
4. `R07` has a similar representation/caption mismatch in the supplied editable copy.
5. `R05` contains an internal article-reference mismatch.
6. `R09` contains a name mismatch in one paragraph although its operative part separately rejects both motions.
7. `R16` refers to an order dated 11 November 2026; the appealed order in the record is dated 11 November 2025.
8. `R20` dates the initial removal application to 23 March 2025; the source application is dated 23 April 2025.
9. `F02` contains court/LAJ identification inconsistencies in the operative/signature blocks.

These are documentary observations, not allegations of intent.

## 6. Redaction and publication boundary

The public text removes only data unnecessary to understand the proceeding:

- repeated administrative headers and court verification identifiers;
- personal/contact, bank, policy and electronic-signature data;
- names of procedural professionals not needed for the substance.

It retains decision-makers, parties, the Insolvency Administrator, procedure/roll numbers, dates, allegations, reasoning, outcomes and appeal information. Redaction markers remain visible in text; public PDFs replace removed pixels and are rebuilt without a text layer.

## 7. Known gaps at the cut-off

1. No standalone source file was located for the 1 September 2025 decree or the March 2025 procedural direction cited in the remuneration clarification incident.
2. No minutes or recording of the 20 January 2026 preliminary hearing were located.
3. No signed later merits decision was located in RPL 421/2026.
4. No signed merits outcome after Auto 223/2026 was located in combined RPL 3304/2025 and 3319/2025.
5. Several later party documents were supplied as editable counsel copies. They are digitised, but their records state when the corpus lacks an independent filing receipt.

## 8. Validation contract

The publication validator must prove:

- 50 manifest records, unique IDs and existing full-text files;
- 25 court/LAJ and 25 party records;
- no unmarked email, DNI/NIE/NIF, phone, NIG/IUP, IBAN or verification-code leakage;
- all ten public PDFs match controlled hashes/page counts and contain only raster images;
- both bilingual routes contain all 25 inline court/LAJ texts and all 25 filing links;
- every relative page link resolves;
- both routes appear in the route registry, site indexes and sitemaps; and
- no page turns an allegation into a finding or a standing dismissal into a merits ruling.

## 9. Controlling public formulation

Aweswell and LPB challenged the Insolvency Administrator through a removal application, a separate remuneration/civil-liability action and later appeals. The removal application and remuneration claim were each dismissed for active-standing reasons. The located decisions did not adjudicate the substantive removal allegations or the material legality and amount of the remuneration. The complete redacted source record is now available for independent reading; liability, causation, quantum and the pending appeal outcomes remain matters for proof and competent decision.
