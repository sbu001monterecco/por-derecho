# Unitary public-authority communications continuity — 1 September 2026

## Release identity

- Control: `PD-SP-UNITARY-PUBLIC-AUTHORITY-COMMS-20260901-01`
- Branch: `codex/unitary-criminal-first-gap-closure-20260901`
- Pull request: `#1305`
- State at preparation: `PREPARED_PENDING_MERGE`
- Authorised action: repository and website publication only.
- Held actions: email, authority contact, filing, portal submission and any representation that an authority has received or acted on this release.

## Historical-attestation continuity

The live verification in `publication-manifests/case-prism-substantive-gap-closure-20260831.json` is an immutable observation of PR `#1282`, merge `d8940e5a7e2d9073a8117b2342e20205bfab7653`, and the deployed bytes observed on 31 August 2026. It is not a permanent hash lock on later governed releases.

This successor manifest records every current resource that legitimately differs from that historical observation. The audit fails closed unless the predecessor hash, current release hash, resource path and transition reason are all present. Any unregistered drift still fails.

The operational `archive/PROCEEDINGS_MASTER_REGISTER.csv` remains an accepted publication-boundary gap: it is not an intended live surface and is not deletion-safe. The website must render from the allowlisted public projection.

## Denominator separation

The canonical communications register contains 313 events. The public-authority scope contains 19 events: 17 newly allocated events and two reused canonical events. The Fiscalía interconnectivity graph retains its bounded 296-event denominator by excluding only the 17 new non-Fiscalía authority events. Reused Fiscalía/EPPO events remain in that graph. This is scope isolation, not deletion or denial of the broader authority register.

## Evidence and allegation controls

- A criminal hypothesis is direct, actor-specific, source-attributed and falsifiable; it is not an adjudicated finding.
- Criminal responsibility never propagates from one actor, document, meeting, authority, funding track or proceeding to another.
- Receipt or registration proves no higher handling state. Transmission, registration, delivery, routing, incorporation, examination, verification/rejection, adoption, decision/use, effect, causation and benefit/loss are separate gates.
- Municipal, Cabildo, Canary autonomous, Spanish State and EU supranational levels remain distinct. A Spanish State body working with European funds is not an EU institution.
- A canonical `^` reference proves controlled identity and provenance only. Communications use `PD-SP-EVT-####` and a stable public anchor.
- No provider IDs, message subjects, personal addresses, private URLs or private attachments enter the public projection.

## Parallel scan and integration rule

Parallel lanes may discover and classify read-only source candidates. A single integrator allocates canonical IDs, resolves aliases, checks duplication, applies privacy controls, assigns handling states and writes the public projection. Metadata discovery counts are query-bounded counts, not merits findings or universal-completeness claims.

## Closeout gate

The manifest may become `LIVE_VERIFIED` only after the exact reviewed head is green, PR `#1305` is merged, the exact merge SHA is deployed by Pages, and cache-busted public readback matches the release hashes. A later closeout must record those identifiers without rewriting the predecessor attestation.

## Live closeout

That gate closed successfully. Final head `b505cf170a422ef15cd6a2214e0563e05c0a67aa` completed 48 successful workflows plus one intentional skip and no failures. PR `#1305` merged as `a2873cd865567da1b6644f32821bb15ece53a160`; reviewed and merge tree `05bd9703ea80ec0ace2a27c722a251aa89a492ac` are identical. Pages run `33472209126` completed successfully for that merge.

Parallel cache-busted readback at `2026-09-01T05:15:54Z`–`05:16:04Z` passed 13/13 HTTP-200 and exact-SHA checks. The post-merge ACTA live-browser run `33472211594` also passed. The target release is therefore `LIVE_VERIFIED_WITH_ACCEPTED_PUBLICATION_BOUNDARY_GAP`; it is not deletion-safe because the operational proceedings CSV boundary remains open. The immutable closeout is `archive/UNITARY_PUBLIC_AUTHORITY_COMMUNICATIONS_LIVE_CLOSEOUT_01SEP2026.md`.

This closeout proves publication and byte identity only. All allegation, handling-state, authority-tier, identity, privacy and non-propagation boundaries above continue unchanged. No email, filing, service, portal action or authority contact occurred.
