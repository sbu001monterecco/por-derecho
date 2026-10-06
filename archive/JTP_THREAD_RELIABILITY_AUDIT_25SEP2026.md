# JTP actor-composite reliability audit — 25 September 2026

## Incident
Two generated candidates were rejected in the working conversation. The first used a real JTP portrait but generated substitute likenesses for four other named actors. The second regenerated the entire composition and introduced unrelated text, facts, amounts and proceedings.

Neither rejected render is committed to GitHub or GitLab main and neither is an approved publication object.

## Root causes
1. Repository availability was confused with local image-edit input availability.
2. A generative image model was used for an identity-preserving compositing task.
3. Exact binary retrieval and hash verification did not precede rendering.
4. There was no pixel-change boundary proving that only portrait slots changed.
5. Cross-host portrait parity had drifted: JDAM/LPAM exact user-supplied portraits were present in GitLab but absent from GitHub; JTP's canonical JPEG was preserved in Drive but absent from both repositories.
6. Draft visual generation was not cleanly separated from publication eligibility.

## Corrective controls
- Exact approved actor binaries are now staged together on this branch.
- Source identities are locked by Git blob and SHA-256.
- The approved infographic is treated as immutable outside four portrait rectangles.
- JTP's existing approved portrait in the base image is not regenerated or replaced.
- Composition is deterministic using Pillow only. No generative model may synthesize or alter faces.
- Output fails if any pixel outside the four authorised portrait boxes changes.
- Any future publication requires a provenance sidecar and live byte/readback verification.
- Identity labels remain supplied/project attributions; inclusion in a visual is not proof of knowledge, intent, coordination, liability or criminality.

## Publication boundary
This audit repairs the production method. It does not itself approve a new rendered image or elevate any evidential proposition.
