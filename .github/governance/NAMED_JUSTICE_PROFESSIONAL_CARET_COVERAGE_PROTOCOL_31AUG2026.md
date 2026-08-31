# Named justice-professional caret coverage protocol

**Control date:** 31 August 2026

**Control ID:** `PD-SP-JUSTICE-PROFESSIONALS-CARET-20260831-01`

**Status:** repository governance for Ministerio Fiscal / Fiscalía members, judges, magistrates, LAJs, notaries and named Property Registry personnel

## 1. Controlling rule

Every exact personal name published in one of the controlled justice-professional functions must resolve to one and only one CAEPR person ID, or remain an expressly unresolved source literal. Only a `CARET_CONFIRMED` identity may display `^`.

`^` confirms canonical identity only. It does not confirm:

- office or capacity on every date;
- authorship of an act not connected by a source;
- participation in a hearing, panel or file;
- receipt, examination, knowledge or agreement;
- correctness or incorrectness of an act;
- intention, coordination, wrongdoing, guilt, liability or outcome.

## 2. Covered functions

This control applies when a public or archive surface identifies a person as:

1. a member, office-holder or signatory of the Ministerio Fiscal / Fiscalía;
2. a judge or magistrate;
3. a Letrado or Letrada de la Administración de Justicia, including an office described historically as Secretario Judicial;
4. a notary; or
5. an individually named registrar, substitute registrar or Property Registry staff member.

Institutional labels such as `Ministerio Fiscal`, `Fiscalía`, `Juzgado`, `Audiencia Provincial`, `Registro de la Propiedad de Tías`, `Registrador` or `personal del Registro` do not create a person identity. The relevant institution may have its own CAEPR ID, but a generic function never receives a person caret.

## 3. Minimum identity gate

Before `CARET_CONFIRMED`, the record must contain:

- exact canonical name and controlled aliases;
- a stable `PD-SP-P-####` identifier;
- at least one O1/O2-quality identity source, or two compatible independent attributes where no single official identifier is available;
- the exact dated capacity or act supported by the source;
- a homonym and spelling check proportionate to the risk;
- a capacity boundary preventing transfer to other dates, offices or proceedings; and
- a public attribution/index occurrence carrying `data-caepr-id` and `data-caret-state`.

A secondary reference may create `CARET_PENDING`. It may not justify `^`.

## 4. Act and office separation

- Current office does not prove personal handling of a historical or current file.
- Signature of a notice does not make its signatory author of the substantive decision.
- Signature of a procedural LAJ act does not prove knowledge of later external use.
- A panel roster does not establish the formation that finally decided another proceeding.
- Notarial authorisation does not establish the truth of every party statement, judicial approval, payment, performance or Registry effect.
- A Registry entry or certificate must identify the individual signatory before a person is added; the Registry as institution remains separate.

## 5. Public presentation

For an ordinary public occurrence outside a verbatim source transcription:

```html
<a data-caepr-id="PD-SP-P-####" data-caret-state="CARET_CONFIRMED" href="../matter-identity-registry/#PD-SP-P-####">Exact name<sup>^</sup></a>
```

For a pending source literal:

```html
<span data-caepr-id="PD-SP-P-####" data-caret-state="CARET_PENDING">Exact source literal · pending</span>
```

Do not insert carets inside quoted judgments, deeds, pleadings or other verbatim transcriptions. Add the caret in the adjacent attribution, heading, index or metadata layer so the source text remains unaltered.

Every page presenting one or more carets must make the identity-only boundary visible or link directly to a page that states it.

## 6. Denominator and “all is ^” rule

The machine authority is [`assets/data/justice-professionals-caret-audit-v1.json`](../../assets/data/justice-professionals-caret-audit-v1.json).

An `ALL IS^` statement is permitted only when, for the stated finite scope:

- every eligible exact named person has a CAEPR ID;
- every record is `CARET_CONFIRMED`;
- pending and suspended counts are zero;
- the public ES/EN census contains the same people, roles, states and limits;
- the validator passes; and
- no generic or unnamed office has been counted as a person.

If any pending or suspended record exists, the only permitted summary is `PARTIAL — NOT ALL IS^`, with exact counts and source gaps.

## 7. Intake and change control

Any change that introduces a covered personal name must, in the same change set:

1. search all registry shards for an existing canonical identity;
2. reuse the existing stable ID or allocate the next unused ID without renumbering;
3. add the source and capacity boundary;
4. add or update the role audit row;
5. maintain Spanish/English parity;
6. add reciprocal links from the relevant proceeding or institutional surface;
7. preserve an unresolved literal without `^` if the gate is not met; and
8. run `python3 scripts/validate_justice_professionals_caret.py` plus the repository-wide validators.

Discovery of a new person does not silently change an earlier finite denominator. The audit receives a new dated execution or explicit revision note.

## 8. Correction and right of reply

Documented corrections to name, accent, capacity, date, signature, panel formation or source attribution must be incorporated without erasing prior versions. A person may identify contrary evidence or an innocent explanation. The correction must be as visible as the proposition it changes.

## 9. Initial execution

The 31-August-2026 execution records:

- 48 exact named people;
- 45 `CARET_CONFIRMED`;
- 3 `CARET_PENDING` notarial literals;
- 0 exact named Property Registry people in the reviewed corpus; and
- verdict `PARTIAL — NOT ALL IS^`.

The absence of an exact Registry staff name means only that no such name was located in the stated corpus at the control date. It is not a claim that no identifiable person exists in the official records.
