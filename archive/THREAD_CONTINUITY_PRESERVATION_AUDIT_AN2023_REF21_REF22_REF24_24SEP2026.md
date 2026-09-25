# Thread continuity and preservation audit — AN2023 → Ref21 / Ref22 / Ref24 — 24 September 2026

**Control:** `PD-THREAD-AUDIT-AN2023-REF212224-20260924-01`  
**Status:** PRESERVED; GitHub live state verified at observed head; GitLab current-main publication blocked by unrelated fail-closed successor controls.

## Scope
This audit closes and preserves the thread that made the 21 September 2023 Audiencia Nacional querella fully source-addressable and linked it to Ref21, Ref22 and Ref24 filed in June 2026 in Las Palmas.

## Upstream source
- 88-page querella in `Anexo_1_Querella_Audiencia_Nacional_21-09-2023_y_Resoluciones_Judiciales.pdf`.
- SHA-512: `2c35052af7f869dfb13ca8593552a6997ee9f1f83a09299bcee883345482ae63b7502f76d6e85873b4b80c1b745d7a3c5797762400410e33c897140b9c36c2ab`.
- Private verbatim master: `internal/evidence/an-dp91-2023/querella-21sep2023-verbatim.txt` — private GitLab only.
- Public-safe 88/88 derivative: `evidence/criminal/an-dp91-2023/full-text/querella-21sep2023-full-public-transcription.md`.
- Source manifest: `evidence/criminal/an-dp91-2023/source-manifest.json`.
- The private master was checked against the querella segment extracted from the canonical Drive bundle: 217,162 characters, 88/88 pages, exact equality through querella EOF.

## Canonical lineage
Human-readable: `evidence/criminal/an-dp91-2023/AN2023_REF21_REF22_REF24_LINEAGE.md`  
Machine graph: `data/an2023-ref21-ref22-ref24-lineage-20260923.json`

Distinct lanes:
- Ref21 — 25 June 2026 — private actors — later context DP1901/2026.
- Ref22 — 18 June 2026 — insolvency administrator — later context DP1956/2026.
- Ref24 — 18 June 2026 — judge/judicial-supervision lane. Ref24 is an intake/daily reference, not DP24, a NIG, or a proceeding number.

Frozen source families and living dossiers remain separate and interlinked.

## Evidence-state rule
Repeated 2023 wording is lineage/source reuse, not independent corroboration by repetition.

Required states: `SOURCE_REUSE` → `ALLEGATION_CONTINUITY` → `INDEPENDENT_CORROBORATION` / `CONTRADICTION` / `SUPERSESSION` / `OPEN` → `NEW_EVIDENCE_OR_LATER_EVENT`.

No relationship, professional role, common source, payment, benefit, procedural association or repeated allegation transfers knowledge, intent, participation, causation, criminal classification or liability.

## Deployment observation

### GitHub
Observed main before this audit PR: `3f10c3bfc54c6723182c9150d67d810dbc5963ee`.

The AN2023 source package and lineage were present. Exact-head Pages receipt:
- workflow: `pages build and deployment`
- run: `36056366613`
- conclusion: `completed / success`
- source SHA: `3f10c3bfc54c6723182c9150d67d810dbc5963ee`

That exact observed head was LIVE_VERIFIED. A later commit requires its own deployment receipt.

### GitLab
Observed protected main before this audit commit: `19b84977dd185ddf8a8065305b37e036869d446e`.

The AN2023 package and lineage were present. Pipeline `2880270242` failed closed; `publish-reviewed-master` and `verify-gitlab-pages-live` were skipped. Observed blockers were later repository-wide successor drift:
- `verify-ricpe-static-readers` job `16720706726`: current institutional communications register newer than its exact reviewed successor pin.
- `verify-gitlab-public-frontend` job `16720706725`: current ONA route newer than its exact route-inventory successor pin.
- `verify-publication-controls` job `16720706723`: failed in the same release chain.

These failures do not identify an AN2023/Ref21/22/24 corpus defect. They do prohibit a fresh current-main GitLab LIVE_VERIFIED claim. Publication gates must be reconciled, not bypassed.

## Preservation rules
1. Never publish the private verbatim AN2023 master.
2. Preserve 88/88 public page addressability and source hash.
3. Keep frozen June sources separate from living dossiers.
4. Preserve Ref21 / Ref22 / Ref24 identities and capacities.
5. Propagate material corrections bidirectionally into source manifest, lineage, machine graph, living dossiers, crosswalks and retrieval gates.
6. Repetition is not corroboration without a source bridge.
7. Do not call a commit live without platform-specific deployment/readback evidence for that exact revision.
8. Do not weaken GitLab fail-closed release controls to force deployment.
9. Re-open earlier conclusions when later primary evidence materially changes evidential state.

## Restart order
1. `evidence/criminal/an-dp91-2023/source-manifest.json`
2. `evidence/criminal/an-dp91-2023/AN2023_REF21_REF22_REF24_LINEAGE.md`
3. `data/an2023-ref21-ref22-ref24-lineage-20260923.json`
4. relevant frozen June source(s)
5. relevant living dossier
6. `archive/knowledge-project/ALLEGATIONS_CROSSWALK_AN2023_DP1901_DP1956_CONTROL24_16AUG2026.md`
7. `archive/knowledge-project/SOURCE_DIGEST_AN_DP91_2023_QUERELLA_RESOLUTIONS_16AUG2026.md`
8. correction, contrary-evidence and missing-evidence registers.

## Closeout
The original AN2023 full-text gap is closed. The continuing task is proposition-level maintenance: classify each later repetition, contradiction, supersession, independent corroboration and genuinely new event without merging proceedings or actors.
