# Por Derecho Transparency Phase 1 — authorisation, publication boundary and live closeout

**Control date:** 25 August 2026  
**Release ID:** `PD-TR-20260825-01`  
**Authoring base:** `a968c51548db1de57b077f5327fe0d279eaf00bd`  
**Authorisation:** “Authorise Phase 1 using only the reviewed P0–P3 names and the approved disclosure wording.”  
**State:** `LIVE_VERIFIED`

## Purpose

Publish a bilingual, present-tense transparency hub for the Por Derecho initiative without converting proposed governance into current governance, without inventing a funding statement, and without introducing any unreviewed historical actor name.

## Public routes

- `/en/por-derecho/transparency/`
- `/es/por-derecho/transparencia/`

## Approved current disclosure

1. Por Derecho is an initiative in formation.
2. It is not yet claimed to be a registered foundation, law firm, public authority, complaints service or deployed judicial system.
3. Gil Marer (`PD-SP-P-0001`) is the founder and current public voice.
4. Gil Marer and related entities have direct legal and economic interests in the Sun Park matter from which the methodology arose.
5. No independent governing body, institutional adoption, accreditation or endorsement is claimed.
6. The exact additional present roles, responsible legal publisher and current cost-bearing structure remain under factual reconciliation.
7. A completed present-tense funding statement is not claimed; no external donation, grant, sponsorship, institutional funding or financial independence is asserted by Phase 1.
8. The current technical platform is described only through implemented controls and a bounded RPL 2523 retrieval pilot; broader RAG, complete custody and institutional deployment are not claimed.

## Historical-name gate

Phase 1 may use only names that:

- already resolve to the immutable registry `PD-SP-IDENTITY-REGISTRY-001`;
- have been reviewed for public use at P0, P1, P2 or P3;
- appear for a defined role or source context; and
- retain the rule that inclusion does not imply wrongdoing, transferred knowledge, coordination, liability or continued involvement.

Phase 1 creates **no new historical actor profile**. It links to the existing public identity workbench. It does not claim the historical census is complete.

## Public/private boundary

Do not publish:

- provider message, attachment or Drive identifiers;
- private vault or reversible source locators;
- private email bodies or full headers;
- privileged advice or active litigation strategy;
- protected-source identities;
- unnecessary personal data;
- security-sensitive implementation detail;
- unverified funding figures, current roles or allegations.

## Evidence and correction rules

- `NOT_LOCATED` does not mean `NONEXISTENT`.
- Retrievability does not imply publishability.
- Consequential claims must identify source status, contrary evidence, limitations and what would change the view.
- Material corrections update the same public record and preserve the reason for change.
- No response is treated as an admission.
- The public contact route is not general case intake, legal advice or a protected reporting channel.

## Authorised release

PR #1007 was squash-merged as:

```text
572d17fa74b0653fce25a6300be15a5ad03fe1e7
```

The release tree is:

```text
10975cbdb6e55a206080cfd05753405077da6017
```

GitHub Pages run `32890471372` completed successfully for that exact merge SHA at `2026-08-25T19:37:12Z`.

The following exact-SHA controls completed successfully:

- dedicated Phase 1 validation: `32890472629`;
- publication integrity: `32890472646`;
- audience experience: `32890472637`;
- private-source, statement and OSINT governance: `32890472867`.

## Public-edge live verification

The read-only live verifier fetched the two public pages, the shared Por Derecho discovery script and the Foundation sitemap from the public GitHub Pages edge.

Successful run:

```text
workflow run: 32891250275
workflow head: 8badcdc4fe92628b6ab38f53d457c670dc8effa1
verified at: 2026-08-25T19:44:42.798818Z
artifact ID: 9579521244
artifact digest: sha256:6ae5abb1020a7472ab25cad1b0780bda9491bbf1ac0a6df91b17968ede63c99c
result: PASS
```

Verified public resources:

| Resource | Bytes | SHA-256 | Markers |
|---|---:|---|---:|
| English Transparency Hub | 19,450 | `f3aa48e947afcaae6cff3c1186718feb5d7e17b5e084d3f050e834475e02adb2` | 9 |
| Spanish Transparency Hub | 20,484 | `81c318bd0dbbc7707367f337d84d53a0d9e508747ebf0023372de2a167026a81` | 9 |
| Shared Por Derecho script | 24,575 | `9cb9ebaf014ece7766339dc48df818bdd0ab220515ef7799ce8067f63c118bd9` | 7 |
| Foundation sitemap | 9,998 | `2be65af22533f8c3846f3bee81764fd2f96074c9b2d548171fe5ce05c1dd5aab` | 2 |

The English and Spanish pages each returned HTTP 200, contained the founder, legal-status, P0–P3, funding-uncertainty and correction markers, and carried reciprocal language URLs.

## Verifier correction preserved

Initial readback run `32891077787` already confirmed that:

- the English public page passed;
- the Spanish public page passed; and
- the Foundation sitemap passed.

That run failed only because the checker required literal absolute English and Spanish route strings inside the shared JavaScript, while the script correctly constructs those routes from a language-specific base path. The verifier—not the public pages—was corrected in commit `8badcdc4fe92628b6ab38f53d457c670dc8effa1`. No public disclosure wording, actor name, funding statement or publication boundary changed to make the control pass.

## Continuing limits

`LIVE_VERIFIED` means that the authorised Phase 1 public package was deployed and its controlled markers were read back successfully. It does **not** mean that:

- Por Derecho is a registered foundation;
- independent governance has been constituted;
- funding reconciliation is complete;
- the historical actor census is complete;
- any new person was approved for public profiling;
- the methodology has been independently validated or institutionally adopted;
- the full private evidence corpus is under complete custody; or
- AI may decide or publish legal conclusions autonomously.
