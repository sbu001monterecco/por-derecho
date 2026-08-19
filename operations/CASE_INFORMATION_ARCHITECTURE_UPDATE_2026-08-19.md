# Case information architecture update — 19 August 2026

**State:** PR_OPEN — implementation and public-edge verification pending  
**Scope:** homepage access, Case Control Room, conditional investigation opening, CE-001–CE-010 register, visible corrections, compact context gateway, notarial and Registry implementation pages

## Objective

Turn the existing breadth of the Por Derecho / Project Sun Rock website into a clearer evidence-led public hierarchy:

> Homepage → Case Control Room → CE issue → actor/evidence dossier → primary source.

The update does not increase the level of accusation. It separates documented facts, Por Derecho allegations, strongest defences, matters not proved, decisive missing evidence and counsel-validation gates.

## Changes implemented on the branch

1. **Authoritative CE issue register**
   - The machine-readable investigation register has been expanded from ten short status rows into ten bilingual issue cards.
   - Every CE-001–CE-010 issue now records route, last review, documented position, what is not proved, strongest defence, decisive next source, counsel gate and correction history.

2. **Global case hub**
   - Every Spanish and English public page receives direct access to the Case Control Room, forensic investigation, 360° method and corrections register.

3. **Homepage case-status entry point**
   - The Spanish and English homepages receive a single public entry explaining what is documented, alleged, unproved and missing.

4. **Conditional canonical investigation opening**
   - The public H1 is changed at runtime from a formulation presupposing design to a conditional question: whether—and, if so, how—the outcome was engineered.
   - A four-part state-of-proof panel distinguishes documented facts, allegations, matters not proved and decisive missing evidence.
   - A visible note explains that LIVE_VERIFIED is a technical publication state, not merits verification.

5. **Case Control Room tracker**
   - The Control Room renders all ten CE issues from the central JSON register.
   - The canonical investigation page renders the four P0 issues and links to the full Control Room.

6. **One compact context module**
   - The two large dynamic gateways previously inserted after relevant page heroes are removed from the rendered DOM.
   - One compact module identifies the page’s phase, actor category, CE issues, proof rule and limits.
   - The module expressly avoids binary or collective-guilt formulations.

7. **Evidence taxonomy**
   - A public legend standardises documented fact, source statement, allegation, inference, disputed/corrected, open question, official outcome, counsel validation and response invited.

8. **Corrections and version-control pages**
   - New bilingual public routes preserve material corrections and identify the controlling formulation.
   - They distinguish professional circulation of draft versions from court filing, admission, argument, decision or endorsement.

9. **Separate Notary and Registry pages**
   - Notarial implementation of protocol 457 is separated from Registry qualification and property-by-property effects.
   - Each page preserves the strongest defence and states what is not established.

10. **Updates and discovery**
    - The Updates pages receive a 19 August 2026 architecture/corrections entry.
    - A dedicated bilingual case-governance sitemap is registered.

## Evidential and legal boundaries

This update does not establish:

- universal nullity;
- an existing insolvency surplus;
- deliberate obstruction;
- judicial bias, favouritism or knowing injustice;
- collusion or criminal coordination;
- bribery, corruption or money laundering;
- material duplication of funding;
- liability of the Notary or Land Registry;
- automatic cancellation of later rights.

Every actor remains subject to actor-specific authority, knowledge, duty, act/omission, benefit, harm, causation, exculpatory evidence and date-specific legal analysis.

## Technical controls

The implementation includes:

- JavaScript and JSON syntax validation;
- schema checks for all ten CE issues;
- XML parsing and robots registration;
- repository-wide publication audit;
- Playwright rendering of homepages, canonical pages, Control Rooms, actor contexts, corrections, Notary, Registry and Updates routes;
- checks that legacy duplicate gateways are absent from the final rendered DOM;
- off-GitHub preservation and publication-integrity workflows;
- post-merge public-edge polling and persistent commit status.

## Remaining future work, not a blocker to this update

- Static source HTML metadata may later be aligned with the runtime conditional headline for non-JavaScript crawlers.
- Overlapping historic routes can be consolidated gradually into supporting-dossier or archive status.
- Actor-specific merits cards and authority packages remain dependent on primary-source recovery and counsel review.

## Deletion-audit linkage

The associated thread deletion audit is preserved at:

`archive/THREAD_DELETION_AUDIT_CASE_INFORMATION_ARCHITECTURE_2026-08-19.md`

Deletion safety must not be claimed until the implementation is merged and independently read back from the public site.
