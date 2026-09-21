# Legal-adviser draft, privilege and publication firewall

Adopted: 28 August 2026
Status: controlling public-repository governance rule
Scope: every human or automated intake, scan, analysis, transformation, commit, publication manifest and Pages publication involving material supplied by or exchanged with the project side's lawyers, legal advisers or law firms.

## Purpose

Por Derecho may use legal-adviser material internally to understand proceedings and strategy without turning that material into public evidence. Lawyer-originated working material is an analytical input, not a publication input.

This rule supplements the repository-wide public/private boundary. It does not reduce the existing preservation obligation for independently existing court, authority, public-register or third-party evidence merely because a lawyer transmitted it.

## 1. Default classification

The following are presumptively **INTERNAL — LEGAL WORK PRODUCT / DO NOT PUBLISH**:

- lawyer or law-firm emails and covering messages;
- legal advice, opinions and procedural recommendations;
- draft pleadings, appeals, claims, complaints, submissions and applications;
- draft letters to courts, prosecutors, regulators, tax authorities or other institutions;
- marked-up, redline, tracked-change and annotated documents;
- proposed allegations, formulations, witness text and litigation narratives;
- lawyer-created chronologies, legal analyses, internal issue lists and strategy notes;
- attachments that are unfinished, proposed, under review or intended for later filing;
- settlement, procedural, evidential or tactical discussions.

These materials may be read, indexed privately and analysed for context. They must not be copied, quoted, paraphrased as evidence, screenshotted, OCR-published, committed, added to public manifests or exposed through Git history or Pages.

## 2. Draft-versus-filed gate

Every lawyer-supplied legal document must be classified before any repository use:

1. **DRAFT / PROPOSED / UNFILED** — internal only; publication prohibited.
2. **FINAL BUT UNFILED / UNSERVED** — internal only unless an independent public-source basis exists; publication prohibited by default.
3. **VERIFIED FILED / SERVED / FORMALLY SUBMITTED** — may be considered separately for publication, subject to redaction, provenance, privacy and publication authority.
4. **OFFICIALLY ISSUED BY COURT OR AUTHORITY** — assess as the issuing institution's document, not as lawyer work product, while keeping the lawyer's covering communication private.

A later filing does not make earlier drafts, comments, tracked changes or covering emails retrospectively publishable.

## 3. Wrapper/source separation

A lawyer may forward or attach an independently existing source. Treat the objects separately.

Example classification:

- lawyer's email, comments and annotations: **INTERNAL — DO NOT PUBLISH**;
- attached court order already issued by the court: separate provenance assessment;
- attached authority notification: separate provenance assessment;
- attached third-party/public document: separate provenance assessment.

The lawyer wrapper never becomes publishable merely because the underlying source is publication-eligible.

## 4. Derived-information firewall

Do not evade the firewall by paraphrasing confidential legal material.

If a fact, allegation, legal theory, characterization or strategic proposition is known only from a lawyer communication or draft, it must not be promoted into a public factual proposition or evidence summary on that basis.

Before public use, locate an independent publication-eligible source supporting the proposition and cite that source instead. If no independent source exists, keep the proposition internal.

## 5. Required provenance fields

For any item received through counsel that is being considered for repository or website use, determine at minimum:

- `origin`: lawyer-created | client-created | court-created | authority-created | third-party-created | public-source;
- `status`: draft | final-unfiled | filed | served | officially-issued | public | unknown;
- `wrapper_present`: yes | no;
- `lawyer_annotations_present`: yes | no;
- `publication_class`: internal-legal-work-product | quarantined-status-unknown | private-evidence | publication-eligible-evidence | public-source;
- `independent_source_available`: yes | no;
- `redaction_required`: yes | no | unknown.

Only `publication-eligible-evidence` and `public-source` may enter the public publication pipeline.

## 6. Uncertainty rule

If draft/final/filed status, privilege, confidentiality, provenance or publication authority is uncertain, classify the item as:

**QUARANTINED — DO NOT PUBLISH**

Do not infer publication permission from an earlier general authorization, from the fact that the document was emailed to the project, from the fact that a filing is planned, or from a filename containing words such as `final`.

## 7. Repository and Git-history rule

The prohibition applies to the entire public repository, not merely rendered Pages.

Do not place protected material in:

- source or archive directories;
- evidence folders;
- hidden or unlinked pages;
- JSON, CSV or Markdown data;
- OCR/transcript outputs;
- generated search indexes;
- build artifacts;
- publication manifests;
- commit messages, PR bodies or review comments that reproduce privileged substance.

Deleting a protected file in a later commit is not an adequate privacy cure because the content may remain recoverable in Git history. If protected material is discovered in history, treat it as privacy-remediation debt and assess containment/history-remediation separately before claiming closure.

## 8. Publication threshold

Before publishing a lawyer-supplied legal document, require a positive basis establishing that the object being published is the verified filed, served, officially issued or independently public version and that the confidential lawyer wrapper and drafting history are excluded.

The controlling presumption is:

> **LAWYER EMAIL / ADVICE / DRAFT / MARK-UP / STRATEGY = READ AND ANALYSE, BUT NEVER PUBLISH.**

## 9. Final-version verification

A filename containing `final`, `signed`, `ready`, `clean`, `v5`, `v6` or similar wording is not sufficient proof of filing or service.

Where publication depends on filing status, prefer one or more of:

- court or authority receipt/registration record;
- official electronic filing receipt;
- court docket or case-file copy;
- service confirmation;
- independently obtained filed copy;
- other reliable institutional evidence tying the exact document/version to filing or service.

Preserve the distinction between the privately held lawyer draft and the independently verified filed document even where their substantive text is identical.

## 10. Interaction with adviser listings

This firewall does not prevent the public site from identifying an approved or historical legal adviser where that listing is separately authorized and accurate. Adviser identity/status and privileged mandate content are different propositions.

A public adviser listing must not reveal live mandate details, draft strategy, confidential instructions, advice, work product or private communications merely because the firm or lawyer is named publicly.
