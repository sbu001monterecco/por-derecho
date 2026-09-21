# Thread continuity audit — PwC reader / GitHub / public GitLab

**Audit date:** 19 September 2026  
**Scope:** continuity, preservation, deployment state and thread-retirement safety.

## Verdict

**Substantive continuity is preserved.** The PwC reader work from this thread is merged into GitHub `main`.

**Operational deployment is still open.** Public GitHub Pages was still serving the earlier PwC reader layout at the audit readback, so the work must not yet be described as fully live and verified.

## Merged implementation

PR **#1576** was merged as commit:
`da9b194695a499d8e9d58c1bbdbfa54e2185ca7c`

Current-main preserved files:

- `en/pwc-canarias-carlos-saavedra-sun-park/index.html`
  - blob `bac951fed01c14ed347f4a060f299350ad08591f`
- `es/pwc-canarias-carlos-saavedra-sun-park/index.html`
  - blob `07e47c1ee4beb4096aadf649b049e1566df4da41`
- `en/pwc-canarias-carlos-saavedra-sun-park/public-questions/index.html`
  - blob `2c7f8c7a2bd982318263e536a9fdf733a52db615`
- `es/pwc-canarias-carlos-saavedra-sun-park/preguntas-publicas/index.html`
  - blob `77e7389a76636cee5507d9e0f158a8c0227bd741`
- `ops/PWC_PUBLIC_READER_EXPERIENCE_RECONCILIATION_18SEP2026.md`
  - blob `cc864702c79c8a6855498b469acf621a4728c8a9`

The exact 18 September visual attachment remains unchanged:
`assets/graphics/pwc-whistleblower-burofax-institutional-map-20260918.png`
blob `40dc460e9a416dcc6b759cf80ce08710348f4ad5`.

## Preserved thread decisions

The merged reader work preserves:

- bilingual first-read current-status blocks;
- explicit separation of established facts, open questions and missing evidence;
- entity-by-entity later-relationship mapping;
- Project Merlin / CAMSA as a separate later project;
- Enrique Guerra / PwC / RICPE overlap with non-transfer-of-knowledge boundary;
- PwC UK Risk → Spain Legal/Compliance → later OGC warning trail;
- a fair institutional countercase;
- reduced first-read prominence of the multi-jurisdiction legal-framework table while retaining the full text;
- institutional/private response channel instead of requiring a public response;
- revised EN/ES questions-page framing;
- exact attachment preserved unchanged;
- additive GitLab/GitHub reconciliation rule.

## Public GitLab preservation rule

GitLab account/repository access remained blocked. No authenticated GitLab write was attempted.

Public GitLab Pages remained readable and supplied useful older enrichment. When GitLab access returns, reconcile **route by route**:

1. preserve useful GitLab-only enrichment;
2. bring across the newer GitHub reader architecture;
3. do not blindly overwrite either side;
4. compare timestamps/content before restoring the standing GitLab-canonical workflow.

## CI history

PR #1576 showed two failed repository-wide gates, but its PwC reader checks passed, including audience, preservation and publication-content controls.

The failures were caused by unrelated repository infrastructure:

- missing explicit timeouts in two Fiscalía workflows;
- a later deterministic Fiscalía projection mismatch.

Those issues were subsequently addressed on main:

- timeout repair `3582c63bd04dfa18b385e6b9b133384fffea3104`;
- timeout repair `c51205b48be2d4b0a01645a3b7f2742eebe43a0a`;
- projection refresh merged in PR #1587, main commit
  `3511759f4d2751229dce6a6c6e293011cf549ad5`.

Therefore the #1576 failures are superseded infrastructure failures, not a loss of the PwC reader work.

## Live deployment gap

At audit readback:

- repository `main` contains the new reader architecture;
- public GitHub Pages still served the older PwC layout;
- the live questions page still used the older public-response wording;
- public GitLab Pages remains its own older mirror.

## Open actions

1. Diagnose/trigger GitHub Pages publication from current main.
2. Verify live EN and ES PwC main pages.
3. Verify live EN and ES questions pages.
4. Confirm language switches and internal anchors.
5. Confirm the exact attachment remains unchanged.
6. When GitLab account access returns, perform additive route-by-route reconciliation.

## Thread retirement status

This thread is **safe to retire for substantive continuity** once this audit is merged.

The surviving operational status is:

> PwC reader work is merged and preserved; GitHub Pages live catch-up and readback verification remain open.
