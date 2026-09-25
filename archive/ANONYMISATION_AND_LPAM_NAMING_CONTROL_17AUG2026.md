# ANONYMISATION AND LPAM NAMING CONTROL — 17 AUGUST 2026

Status: **CANONICAL PUBLIC-REPOSITORY / WEBSITE IDENTITY RULE**

## Purpose

This repository is public. This control therefore governs both rendered website text and source/control material committed to the public GitHub tree.

The objective is to preserve evidential provenance while avoiding unnecessary publication of private witness identities and, critically, avoiding confusion between two entirely different people who share the given name Patricia.

## 1. The two people must never be confused

### A. Witness from Gil Marer's perimeter — identity reserved publicly

A person within **Gil Marer's personal and business perimeter** has provided/memorialised evidence used in several source-control modules. Their legal identity is retained in native/private evidence and may appear in formal filings where legally required.

In the public repository and public website, describe that person contextually as one of:

- **a person within Gil Marer's personal and business perimeter**;
- **the witness from Gil Marer's perimeter**;
- **the declarant from Gil Marer's perimeter**; or
- **the witness/declarant**, once the role has already been established.

Do not publish their personal name merely for narration, indexing, a public filename, source locator, caption or cross-link.

### B. Laura Patricia Acosta Matos (LPAM) — not anonymised

**Laura Patricia Acosta Matos (LPAM)** is a different person. The relevant reported statements/conduct in the LPAM–Magistrado module are attributed to her.

Public naming rule:

- first relevant reference in a page/module: **Laura Patricia Acosta Matos (LPAM)**;
- later references: **LPAM** or **Laura Patricia Acosta Matos**;
- do not anonymise LPAM merely because the witness is anonymised.

### Absolute ambiguity rule

**Never use “Patricia” alone** in public repository/site text where it could refer to either person.

## 2. Legal adviser identity

A separate private person formerly referred to publicly by the first name `Cristo` in the LPAM source chain is to be described as:

- ES: **un asesor jurídico de Gil Marer en aquel momento** / **un asesor jurídico en el momento relevante**;
- EN: **one of Gil Marer's legal advisers at the relevant time** / **a legal adviser at the relevant time**.

The adviser’s personal identity remains available in the private evidence corpus if required for lawful verification, witness examination or formal filing.

## 3. Evidence integrity is not altered

Public anonymisation does not alter the native evidence. It is not a retraction, deletion of provenance or change to the underlying witness account.

Maintain the distinction:

`NATIVE / SIGNED / FILED SOURCE WITH LEGAL IDENTITY → PUBLIC REPOSITORY DERIVATIVE USING ROLE-BASED IDENTITY`

Where a public derivative is used, preserve dates, source type, source status, evidential limitations, hashes/receipts where appropriate, and the route by which the original can be produced to a competent authority without publicly reproducing the private identity.

## 4. LPAM–Magistrado substantive boundary remains unchanged

The account attributed to the witness is a **reported witness account requiring independent corroboration**. It does not by itself prove friendship, direct access, calls, influence, bias, coordination, corruption, prevaricación or effect on Sentencia 163/2023.

The finite verification route remains:

`REPORTED WORDS → DATE/PLACE/WITNESSES → COMMUNICATIONS → MEETINGS/ACCESS → DISCLOSURE → CORROBORATION OR DISPROOF → ONLY THEN LEGAL SIGNIFICANCE`

## 5. Public declaration archive

Public declaration files derived from the witness should use neutral filenames and headings. Exact named originals, signed copies, voice files, private contact details and original filenames containing unnecessary personal identity belong in the private evidence corpus rather than the public GitHub tree.

Recommended public labels:

- `001_WITNESS_GIL_PERIMETER_TESTIMONIO_2018_20260815.md`
- `002_WITNESS_GIL_PERIMETER_RICPE_VOICE_20260815.md`
- `003_WITNESS_GIL_PERIMETER_CAM_HEARING_20260727.md`

The declaration index should identify the declarant as **Witness from Gil Marer's perimeter — identity reserved**.

## 6. Implementation scope

This control applies to:

- ES/EN Calificación pages;
- LPAM–Magistrado source-control modules;
- Judge/Court and CGPJ pages;
- institutional-accountability and RICPE cross-links;
- homepage/public narrative modules;
- `archive/` source controls and deletion-safe handovers;
- public declaration Markdown and filenames;
- future JavaScript-injected public text; and
- future ChatGPT maintenance of this repository.

Historical Git commits and closed PR discussions may retain earlier wording as immutable repository history. The controlling requirement is that the **current `main` tree and current rendered website** implement this rule. Rewriting Git history is not required and should not be done merely for this editorial correction.

## 7. Quality-control test before merge

Before any future LPAM-related publication is merged, verify:

1. no unnecessary public occurrence of the reserved witness’s legal name;
2. no unnecessary public occurrence of the legal adviser’s first/personal name;
3. no ambiguous use of `Patricia` alone;
4. first reference to LPAM is `Laura Patricia Acosta Matos (LPAM)` where context requires identification;
5. the witness and LPAM are explicitly distinguishable where both appear;
6. allegations remain source-qualified and not upgraded into adjudicated fact; and
7. native/private evidence remains preserved outside the public editorial layer.

This file supersedes any earlier instruction that a named witness identity should be preserved inside public `archive/` Markdown merely because that directory was described as an “internal” repository layer.
