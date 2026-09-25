# CAEPR public-surface propagation and continuity gate

**Control date:** 2 September 2026  
**Control ID:** `PD-SP-CARET-SURFACE-20260902-01`  
**Status:** repository operating control; strict for declared surfaces, advisory for archive-wide discovery  
**Parent control:** `.github/governance/CAEPR_CARET_IDENTITY_AND_ALL_IS_VERIFICATION_PROTOCOL_26AUG2026.md`

## 1. Problem this gate closes

A person, organisation, institution or proceeding may already have one immutable
CAEPR identity and `CARET_CONFIRMED` status while a public page still prints the
name as unregistered prose. That is a **public-occurrence propagation gap**. It
must not be misreported as either:

- a missing canonical identity; or
- proof that the occurrence is correctly interlinked merely because the registry
  contains the name.

The controlled layers are separate:

1. canonical identity admission;
2. source-specific act/capacity attribution;
3. public occurrence markup and link;
4. publication/deployment state; and
5. live rendered verification.

A pass at one layer does not silently pass the others.

## 2. Required public occurrence contract

For each occurrence declared in
`assets/data/caret-public-surface-coverage-v1.json`, the public editorial surface
must contain one element that has all of the following:

- the exact immutable `data-caepr-id`;
- `data-caret-state="CARET_CONFIRMED"`;
- the source-safe canonical display name or an expressly registered alias;
- a visible `<sup>^</sup>` presentation marker;
- the immutable CAEPR ID printed visibly on the page; and
- a working link to the canonical identity register or a dedicated canonical
  dossier.

The displayed caret resolves identity only. It does not prove authorship beyond
the linked act, knowledge, receipt, mandate scope, control, intent, coordination,
legal correctness, wrongdoing, liability or outcome.

## 3. First-reference and repetition rule

The first material editorial reference on a controlled page should carry the
full occurrence contract. Later repetitions may use a shorter form where the
page remains unambiguous and the identity block is discoverable without closed
progressive disclosure.

A source quotation, literal transcript, OCR extract, filename, embedded JSON-LD
or archived primary record is not rewritten merely to add a caret. The identity
marker belongs in the editorial attribution/index layer. A source literal may be
shown next to a canonical identity without being silently normalised.

## 4. Exact entity and ambiguity controls

Do not promote generic labels such as `Auren`, `PwC`, `Stoneweg`, `Ona Hotels`,
`Meeting Point`, a surname, initials or an uncertain legal-form variant merely
because an exact confirmed entity exists nearby.

In particular:

- `PD-SP-O-0046` remains the generic **Auren professional perimeter**;
- `PD-SP-O-0070` is the distinct exact entity **AUREN REESTRUCTURACIONES SLP**
  appointed in signed Auto 97/2025; and
- a public occurrence must use the ID supported by that occurrence's source,
  not whichever record is more convenient.

Aliases preserve search and provenance. They do not create a second identity or
permit cross-entity transfer.

## 5. New identity versus propagation repair

Before creating a new CAEPR record, test whether the source occurrence resolves
to an existing person, organisation, institution or proceeding, including all
registered aliases and `not_same_as` controls.

- Existing confirmed identity + missing page marker/link = **repair the public
  occurrence**.
- Existing pending identity = preserve `CARET_PENDING`; obtain the stated primary
  source before promotion.
- No reliable existing identity = create a durable source-recovery item; do not
  guess a name or ID.
- Material collision = preserve both candidates and suspend or qualify the
  affected occurrence until resolved.

## 6. Validator modes

`scripts/validate_caret_public_surface.py` operates in two modes in the same run:

### Strict declared-surface mode

It fails the affected change when a declared occurrence lacks its correct ID,
confirmed state, visible caret, visible ID or canonical link; when a declared ID
does not exist; or when a pending/suspended record is presented as confirmed.

### Advisory archive-wide discovery mode

It scans public HTML for exact confirmed canonical names that appear without any
machine-readable occurrence declaration on that page. These are written to the
artifact report as candidates. Advisory candidates do not automatically fail an
unrelated PR because quotations, historic pages and deliberate first-reference
choices require human/source review.

The advisory backlog may become strict only through an explicit, finite coverage
manifest after false-positive review. Do not turn a repository-wide heuristic
into an unsupported mass edit.

## 7. Source-recovery queue

This gate reuses, rather than duplicates, the existing source queues. Current
named identity gaps include the three `CARET_PENDING` notarial literals in
`assets/data/justice-professionals-evidence-production-queue-v1.json`. Unknown
judicial, LAJ, Fiscalía or Property Registry signatories remain source-production
questions until a primary signed/authenticated record identifies the exact
person, date, act and capacity.

No missing-source task authorises external contact, filing, service or publication
of restricted material.

## 8. Change and merge process

For a public-occurrence repair:

1. fetch and identify current remote `main`;
2. reuse the immutable CAEPR ID and do not alter unrelated registry records;
3. update Spanish and English surfaces together where both exist;
4. add or update the finite coverage manifest;
5. run `python3 scripts/validate_caret_public_surface.py`;
6. run `python3 scripts/validate_operational_identity_registry.py` and the normal
   preservation/publication checks required by `AGENTS.md`;
7. preserve the base SHA, changed paths, unresolved source gaps and publication
   state in a handover/closeout record;
8. use a branch and PR; never force-push `main`; and
9. after an authorised merge, verify the exact merge SHA and cache-busted live
   ES/EN routes before claiming `LIVE_VERIFIED` or deletion safety.

## 9. Continuity and successor-thread bootstrap

A successor thread handling caret coverage must load, from current `main`:

1. `AGENTS.md` and `CHATGPT_START_HERE.md`;
2. the parent caret protocol;
3. this gate;
4. `assets/data/matter-identity-registry-v1.json` and all declared parts;
5. `assets/data/caret-public-surface-coverage-v1.json`;
6. `assets/data/justice-professionals-evidence-production-queue-v1.json`; and
7. the latest caret public-surface handover/closeout.

The successor must distinguish:

- `REGISTERED_AND_CONFIRMED`;
- `REGISTERED_BUT_PUBLIC_OCCURRENCE_GAP`;
- `CARET_PENDING_SOURCE_REQUIRED`;
- `UNKNOWN_PERSON_SOURCE_REQUIRED`;
- `PR_READY_NOT_LIVE`; and
- `MERGED_LIVE_VERIFIED`.

A chat statement, branch, commit or open PR is not live publication. A deployment
success without route/readback verification is not proof that the intended
identity marker is visible.

## 10. Deletion-safety sentence

The originating thread is continuity-safe only when every material finding,
repair, limitation, validator rule and open source-production task is recoverable
from durable repository controls. It is **not** publication- or live-deletion-safe
until the authorised merge and exact-route readback are recorded.