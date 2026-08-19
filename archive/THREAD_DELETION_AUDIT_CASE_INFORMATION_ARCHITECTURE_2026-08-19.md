# Thread deletion audit — case information architecture and forensic-site changes

**Audit date:** 19 August 2026  
**Current deletion status:** NOT YET SAFE — merge and public-edge verification pending

## Thread intelligence to preserve

This conversation produced the following material decisions:

1. The site has sufficient substantive breadth; the next priority is information architecture rather than additional accusation pages.
2. The Case Control Room should become the authoritative public dashboard.
3. The public hierarchy should be:
   - homepage;
   - Case Control Room;
   - CE-001–CE-010 issue;
   - actor/evidence dossier;
   - primary source.
4. The canonical investigation headline should ask whether—and, if so, how—the outcome was engineered rather than presupposing design.
5. The canonical page should show documented facts, Por Derecho allegations, matters not proved and decisive missing evidence above the fold.
6. LIVE_VERIFIED must be explained as technical deployment/read-back status, not merits verification.
7. Two large post-hero dynamic gateways should be replaced by one compact context module.
8. The CE register should contain status, route, documented position, non-proof, strongest defence, decisive next evidence, counsel gate and change history.
9. Corrections should remain visible rather than silently overwriting superseded statements.
10. Notarial implementation and Registry implementation should be separated.
11. Evidence labels should be standardised site-wide.
12. No public E0–E7 level should be assigned to a named actor without an actor-specific evidence card and adverse-case review.

## Repository preservation

The implementation is preserved through:

- `assets/data/criminal-engineering-investigation-v1.json`;
- `assets/case-information-architecture-20260819.js`;
- `assets/site.js`;
- `scripts/render_criminal_engineering_investigation.mjs`;
- bilingual corrections pages;
- bilingual Notary pages;
- bilingual Registry pages;
- `sitemap-case-governance.xml`;
- validation and public-edge workflows;
- `operations/CASE_INFORMATION_ARCHITECTURE_UPDATE_2026-08-19.md`.

## Private-source boundary

This thread added no new private primary document requiring public-repository preservation. It did not authorise publication of:

- internal working papers;
- private emails or recipients;
- Gmail/Drive identifiers;
- private hashes;
- confidential witness identities;
- privileged advice.

Earlier uploaded attachments in the wider conversation may no longer be directly loadable in ChatGPT. Their relevant conclusions and preserved copies were addressed by earlier evidence-vault and deletion audits. A new byte-level review of an expired attachment would require the user to upload it again.

## Remaining deletion gates

Before this thread can be deleted safely:

1. open a controlled pull request;
2. pass syntax, schema, rendering, privacy, publication-integrity and preservation checks;
3. merge the implementation to `main`;
4. independently read back the public pages, JSON, module and sitemap;
5. record exact PR, merge SHA, workflow and status evidence in this audit;
6. confirm no unique instruction or unresolved task remains only in the conversation.

## Final audit field

This document must be updated from **NOT YET SAFE** to **SAFE TO DELETE** only after all deletion gates are satisfied.
