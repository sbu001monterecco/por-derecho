# Sun Park owner-perimeter classification protocol — 26 August 2026

**Control:** `PD-SP-OWNER-PERIMETERS-001`  
**Machine source:** `assets/data/sun-park-owner-perimeter-classification-v1.json`  
**Status:** backend control; public propagation requires a separate reviewed publication step.

## Why this control exists

The non-LPB/Matkator ownership universe must not be flattened into one label such as “minority owners”, “Molina family”, “dissidents” or “adverse parties”. The evidence programme needs to distinguish at least three questions:

1. **Who owned which finca/unit at which date?**
2. **Which owners or representatives were actually aligned with the documented Montelanza/Molina litigation, Community or governance perimeter, and when?**
3. **Which owners acquired units directly from LPB after the 2008 acquisition and before later ownership changes?**

Those questions can overlap, but they are not interchangeable.

## Controlling distinction

`NON-LPB/MATKATOR OWNER ≠ MONTELANZA/MOLINA DISSIDENT`.

A proven minority owner belongs first to an ownership-provenance class. A separate dated edge is required before the same owner is classified as part of the attributed Montelanza/Molina dissident/adverse perimeter. Representation, litigation status, Community office and alleged enablement each require their own edge.

## Perimeter A — our owner/control side

Use for Aweswell/Oswell, LPB and Matkator only within the role and date actually proved. Do not collapse LPB into Matkator; do not treat Aweswell as title-holder of every finca merely because it is on the user-side control chain.

Visual token: **blue**.

## Perimeter B — our advisers and representatives

Use the separate legal-professional register and mandate-specific sources. Advisers are not owners. Former advisers are not assumed to represent the user now. Advice, representation, filing authority and knowledge remain engagement-specific.

Visual token: **green**.

## Perimeter C — Montelanza/Molina judicial litigation core

The strongest bounded core is the AP 89/2014 / JV 1260/2011 set of seven claimant-owners concerning eighteen bungalows. This is a litigation-defined perimeter, not the complete minority-owner denominator and not proof of a collective criminal agreement.

Visual token: **dark red**.

## Perimeter D — wider Montelanza/Molina dissident/represented perimeter

This broader perimeter is built from Community records, party pleadings, representation records and later continuity evidence. Every edge must record source grade and date. The word “dissident/adverse” is an attributed analytical description of alignment against LPB/our side in the relevant governance/litigation context, not a judicial finding of wrongdoing.

Visual token: **red**, with a different pattern from the AP89 core.

## Perimeter E — other non-LPB/Matkator minority owners

This is the default class for a proven minority owner where the evidence does **not yet** support Montelanza/Molina alignment. It prevents the analytical error of treating every minority owner as a dissident.

Visual token: **amber**.

## Perimeter F — the reported twelve LPB transferee units

Gil's present position is that LPB sold twelve apartments/units after entering the ownership structure following the 2008 acquisition. This must be reconstructed as a separate provenance cohort.

At present the backend records **12 as a reported denominator requiring finca-by-finca primary-source reconciliation**, not as a completed title schedule. Each unit needs:

- exact finca/unit;
- transfer date;
- deed and Registry reference;
- seller and purchaser identity;
- consideration if material;
- any later transfer;
- any Community/litigation representative; and
- any later overlap with the Montelanza/Molina perimeter.

An owner from this cohort can later overlap with the dissident perimeter, but the direct-LPB-transferee provenance must remain separately visible.

Visual token: **purple**.

The presently recalled Multimatrix/later-ownership endpoint must not be encoded as verified until a primary or otherwise controlled source establishes the exact chain and entity names.

## Perimeter G — later CAM/Acosta Matos concentration

Later CAM/Acosta Matos ownership, representation or material-control evidence belongs to a later temporal layer. It must not be back-projected into 2011 merely because later convergence exists.

Visual token: **orange**.

## Representation and alleged enablement

Representation is not ownership. The backend therefore uses separate role codes such as `LAWYER`, `REPRESENTATIVE`, `COMMUNITY_OFFICEHOLDER` and `ADMINISTRATOR`.

`ALLEGED_ENABLEMENT` is a separate attributed allegation code. It may only be used when the analysis records the alleged act or omission, authority/opportunity, knowledge state, consequence, source and alternative explanation. It must never be inferred merely because a person was a lawyer, representative, officeholder or minority owner.

## Overlap rule

The model is many-to-many and temporal. A single identity can carry, for example:

`LPB transferee owner (2009) + other minority owner (2009–2011) + Montelanza/Molina represented litigant (2011–2014)`

without merging those facts into one permanent status.

Colour follows the **edge/perimeter being shown**, not the person. Text labels and source grades must accompany colour so the system remains interpretable without colour.

## Evidence programme

Priority order:

1. identify the twelve LPB-transferred fincas and their first purchasers;
2. map AP 89/2014's eighteen bungalows to exact fincas;
3. reconstruct the complete non-LPB/Matkator owner denominator at 2008/2009, 2011, 2017 and 2022 checkpoints;
4. identify representation independently at each material Community meeting and proceeding;
5. record overlap between the twelve-unit cohort and the Montelanza/Molina perimeter only where sourced;
6. trace later transfers into CAM/Acosta Matos or other vehicles without overwriting earlier provenance; and
7. preserve unresolved denominator discrepancies rather than forcing a false complete schedule.

## Future-thread instruction

Before describing a person or entity as a minority owner, dissident, adverse actor, representative, adviser, transferee, CAM-side actor or alleged enabler, resolve the immutable identity ID and add a dated, source-graded edge under `PD-SP-OWNER-PERIMETERS-001`. Never use “all minorities” as a synonym for the Montelanza/Molina dissident perimeter.
