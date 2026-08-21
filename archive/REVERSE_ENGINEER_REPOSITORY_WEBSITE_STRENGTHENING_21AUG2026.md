# Reverse-engineer repository and website strengthening control — 21 August 2026

## Purpose

This record preserves the governing prompt, findings and implementation boundaries for the 21 August 2026 reverse-engineering review of the Por Derecho repository and public website.

It is an evidence and publication-control record. It does not add a finding of civil, insolvency, regulatory or criminal liability against any person.

## Improved governing prompt

> Reverse-engineer the latest remote `main`, the rendered Por Derecho website and the repository's evidence, publication and operational-control layers before editing. Strengthen the Group's recovery objectives by correcting materially imprecise public wording, improving source traceability and making open actions finite and actor-specific.
>
> Preserve strict separation between LPB and its insolvency estate; Aweswell; Matkator and other extraconcursal property; CEXP and the exploitation layer; Pink Canary Services; CAM, HNT and Canarian Hospitality; each lender or assignee; each professional adviser; the Insolvency Administrator; and each judicial or administrative actor.
>
> Treat the 2012 filing, the declaration of Concurso 36/2012, cash-flow insolvency, asset solvency, the Bankia enforcement trigger, the financial-products dispute, operational interference, the first-instance `calificación culpable`, its pending appeal and later loss of value/control as separate propositions. Do not use `insolvent hotel`, `Sun Park insolvency`, `the hotel was insolvent` or `LPB was insolvent` without immediate source, date, perimeter and procedural qualification.
>
> For every material proposition distinguish: verified primary-document fact; attributed first-hand account; party position; evidence-based inference; legal argument; adverse or exculpatory evidence; and unresolved question. Do not infer shared knowledge, intent or coordination. Attribute each act, omission, authority, benefit and consequence to the exact legal person or individual at the relevant date.
>
> Reuse existing evidence codes, locators, correction registers and canonical pages before creating a new page or repeating a source search. Preserve private addresses, privileged material, native attachments and exact sensitive locators only in controlled custody. Public wording must invite finite contradiction and correction.
>
> Update the smallest authoritative set of repository files, maintain English/Spanish parity, add a regression guard for any corrected systemic error, run source and rendered validation, publish only through a reviewable pull request, verify the exact merged revision on the live host and finish with a deletion-safety record identifying every remaining open action.

## Reverse-engineered architecture

The repository has four interacting layers:

1. bilingual static HTML routes forming the public record;
2. dated JavaScript modules and nested loaders adding cross-site context and controls;
3. archive, evidence, correction, handover and publication-control records preserving provenance and limits; and
4. workflows, validators and operational JSON files asserting source, deployment and deletion states.

The public routes were functioning at baseline `985466e1075890d67e8abbeed724a64cbb29ceca`. During the audit, PRs #721 and #723 advanced `main`; the implementation was rebased and their newer records were preserved. The principal remaining weakness was control drift: later evidence and public corrections had moved ahead of the master handover, deployment log, production-status record and two other validators.

## Material findings and action taken

### Insolvency perimeter

The canonical `/en/lpb-insolvency/` and `/es/insolvencia-lpb/` routes already supplied the correct architecture. A limited group of older pages still used shorthand capable of being read as a substantive finding that LPB or the whole hotel was insolvent.

Corrections applied:

- the judge/supervision pages now describe LPB as the debtor declared in Concurso 36/2012 and identify the asserted cash-flow/enforcement context without treating the whole hotel as the estate;
- the elEconomista timeline now separates Romera's contemporaneous characterisation from the legal identity and status of the LPB judgment;
- visual alt text and RHG collaborator captions now identify LPB's concursal life within a wider mixed-ownership project;
- a repository-wide insolvency-perimeter language validator prevents the identified shorthand from returning.

### Operational memory

- the master handover was advanced to 21 August and now records the corrected CGPJ, FGE, AEAT, Anticorrupción and RICPE/Ithikios status;
- the deployment log records PR #720 and its live read-back;
- production status was advanced from the 18 August release to the latest positively observed 21 August deployment while preserving the older last-known-good rollback anchor.

### Verification defects

- the case-information live workflow now verifies the outer loader and actual nested loader separately;
- the Meeting Point live workflow is expressly permitted to write its intended commit status;
- the recent-live script correction merged separately in PR #721 was preserved rather than overwritten; it tests the confirmed Alzada 286/2026 joinder/`en trámite`, four FGE receipt-only acknowledgements and technical discovery rather than superseded wording.

## Deliberate non-actions

This strengthening does not:

- decide whether LPB was legally insolvent on any specific historical date;
- decide the pending `calificación` appeal;
- establish that Bankia, SAREB, PH122, Haya/Cerberus, CAM, the Insolvency Administrator, a court or any other actor shared a plan or intent;
- merge stale or conflicted evidence branches merely because they are technically mergeable;
- publish privileged advice, private addresses, unread portal content or unverified first-hand accounts; or
- duplicate the existing lender, convergence, immediate-action, Article 82/83 or credit-classification pages.

## Remaining finite actions

1. Cure the Anticorrupción signature/formalisation defect without widening the filing.
2. Open and preserve the RICPE/Ithikios update before characterising it.
3. Track AEAT `00001-00113069`, Alzada 286/2026 and FGE routing against exact references.
4. Reconcile the CGPJ outgoing transmission with the TSJ receiving record.
5. Close or supersede duplicate and stale pull requests individually; do not mass-rebase them.
6. Replace the growing dated-loader/workflow set with a declarative route and module manifest in a separate engineering change.
7. Continue the document-led creditor-identity, assignment, standing, cash-flow and appeal audits without converting working hypotheses into public facts.

## Publication and deletion rule

This record preserves the reasoning that would otherwise exist only in a ChatGPT thread. Deletion safety still requires the implementation commit to be merged, the exact merged source to pass CI and the changed public routes to be read back from the live host.
