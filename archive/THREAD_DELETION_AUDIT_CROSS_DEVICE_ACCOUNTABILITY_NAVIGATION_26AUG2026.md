# Thread deletion audit — cross-device accountability navigation — 26 August 2026

**Current verdict:** `DELETION-SAFE WITH OPEN DEVICE-COVERAGE AND RECOVERY ITEMS`

**Scope:** the disappearing Spanish `AC y Juez` / English `AC & Judge` homepage navigation control, the Android-tablet report, both runtime rewrite layers, the expanded browser regression prompt and suite, repository publication, Pages deployment, live read-back and future-thread implementation advice.

## 1. Report and diagnosis

Gil Marer reported that the burgundy accountability control appeared on an Android tablet for a fraction of a second and then disappeared. The source record showed two independent homepage navigation rewrites:

1. the delayed optimum-reader journey rewrote the header after initial paint; and
2. the earlier unitary public shell also consolidated the navigation.

The first repair preserved the accountability link in the delayed optimiser. The expanded regression then exposed that the unitary-shell rewrite could still replace the static navigation with a version that omitted the link before the delayed optimiser restored it. That second temporal gap matched the reported flash/disappear class even though the link could reappear later.

This was a runtime composition defect, not deletion of the accountability dossier, fragment or underlying five-actor / Administrator / Judge material. No evidence, legal position, identity, allegation, route body or protected first-read accountability component was changed by the repair.

## 2. Exact implementation state

### Initial tablet repair

- PR [#1043](https://github.com/sbu001monterecco/por-derecho/pull/1043), `Fix disappearing AC and Judge navigation on tablets`, merged as `53b27613095932f6483dd0c4627c67f9cf8064ca` on 26 August 2026.
- It changed `assets/optimum-reader-journey-finish-20260818.js` and `scripts/render_optimum_reader_journey.mjs`.
- The delayed optimiser now preserves one locale-correct `.nav-accountability` link.
- The first widened check added English-home and 900×1280 tablet coverage.
- Pages run [32942014350](https://github.com/sbu001monterecco/por-derecho/actions/runs/32942014350) succeeded for the exact merge SHA. The later PR #1048 includes and supersedes this implementation state.

### Cross-device regression and second-layer repair

- PR [#1048](https://github.com/sbu001monterecco/por-derecho/pull/1048), `Expand accountability navigation tests across phones, tablets and desktops`, merged as `86aa96f31f32164ed17e748da4c54a1541e08ae0` on 26 August 2026.
- The branch was reconciled with then-current `main` before the final test cycle. The final merge changed five files relative to its first parent:
  - `.github/workflows/validate-optimum-reader-journey.yml`;
  - `archive/OPTIMUM_USER_JOURNEY_EXECUTION_PROMPT_18AUG2026.md`;
  - `assets/unitary-public-shell-20260818.js`;
  - `scripts/render_optimum_reader_journey.mjs`; and
  - `scripts/render_unitary_public_shell.mjs`.
- `assets/unitary-public-shell-20260818.js` is version `20260826a`. Its home-navigation consolidation now retains the language-specific accountability link and does not accept an already-consolidated navigation as complete unless that link exists.
- The executable prompt and browser runner now require one exact link before the delayed optimiser, after at least 8.5 seconds, and after reload; exact ES/EN label and fragment; burgundy/white styling; viewport containment; at least a 24×24 CSS-pixel target; centre-point hitability; compact-menu state; and a successful click to the locale-specific fragment.
- The complete ten-route suite runs at representative phone, Android-tablet-size and desktop profiles. The bilingual homepage regression runs at fourteen widths/heights covering small and large phones, landscape phone, portrait and landscape tablets, both sides of the 1120 px menu breakpoint, laptop and large desktop. This produces **52 route/viewport combinations across 14 profiles**.

The exact recoverable implementation paths on `main` are:

- `assets/optimum-reader-journey-finish-20260818.js`;
- `assets/unitary-public-shell-20260818.js`;
- `scripts/render_optimum_reader_journey.mjs`;
- `scripts/render_unitary_public_shell.mjs`;
- `.github/workflows/validate-optimum-reader-journey.yml`; and
- `archive/OPTIMUM_USER_JOURNEY_EXECUTION_PROMPT_18AUG2026.md`.

## 3. Reproducible validation and deployment evidence

The reconciled PR-head validation cycle at `25988a9a0e83f5c0f0e79df74c96198009722afb` completed with all eleven workflows successful. In particular:

- cross-device journey run [32947981279](https://github.com/sbu001monterecco/por-derecho/actions/runs/32947981279) reported `OPTIMUM READER JOURNEY RENDER TEST PASSED: 52 route/viewport combinations across 14 device profiles`;
- unitary-shell run [32947981391](https://github.com/sbu001monterecco/por-derecho/actions/runs/32947981391) succeeded; and
- the journey run uploaded the reproducible `optimum-reader-journey-screenshots` artifact, 35,502,325 bytes at audit time. The artifact is a temporary GitHub Actions derivative, not unique source or an independent recovery copy; the runner and site source needed to regenerate it are in Git.

PR #1048 merged normally. GitHub Pages run [32949369456](https://github.com/sbu001monterecco/por-derecho/actions/runs/32949369456) deployed the exact merge SHA successfully.

The exact-merge post-merge journey run [32949370634](https://github.com/sbu001monterecco/por-derecho/actions/runs/32949370634) also passed the same 52-combination / 14-profile suite and produced the same 35,502,325-byte screenshot artifact. This confirms the result on the merge commit rather than only on the reconciled PR head.

A cache-busted live-browser read-back then verified both homepages at an independent 1203×500 browser viewport:

| Phase | English | Spanish |
| --- | --- | --- |
| Early unitary-shell state | one visible, centre-hit `AC & Judge` link to `#institutional-accountability-12aug-en` | one visible, centre-hit `AC y Juez` link to `#institutional-accountability-12aug` |
| Delayed optimiser state | same exact link, burgundy `rgb(111, 36, 35)`, white text, `data-psr-optimised="1"` | same exact link, burgundy `rgb(111, 36, 35)`, white text, `data-psr-optimised="1"` |
| Click result | exact English fragment reached | exact Spanish fragment reached |

Both early states exposed unitary-shell version `20260826a`; both links remained inside the viewport. This is independent live verification of the deployed desktop-width presentation. It is not a claim that a physical Android tablet was remotely controlled.

## 4. Future-thread review and implementation queue

The durable queue is `ops/FIVE_ACTOR_PRESERVATION_AND_READER_JOURNEY_BACKLOG.md`. Future threads touching homepage navigation, the unitary shell, optimum-reader journey, shared loaders, the 1120 px breakpoint or accountability fragments must read this audit, the queue, `archive/OPTIMUM_USER_JOURNEY_EXECUTION_PROMPT_18AUG2026.md`, `archive/FIVE_ACTOR_FRONT_PAGE_AND_DIRECT_ROUTE_PRESERVATION_LOCK_24AUG2026.md` and `archive/FIVE_ACTOR_VISIBILITY_REGRESSION_AND_REPAIR_24AUG2026.md` before editing.

The following remain open and must not be described as implemented:

1. **Physical affected-device confirmation — `PROPOSED`.** Recheck the current release on a real Android tablet after ordinary asset-cache expiry or a browser refresh. Record browser/version, orientation, menu-open state and whether the control remains after at least ten seconds and after reload. Do not publish unnecessary device identifiers.
2. **True input/browser diversity — `PROPOSED`.** The current matrix changes Chromium viewport dimensions; it does not set Android user agents, `hasTouch`, `isMobile` or device scale factors and it does not run Firefox or WebKit. Add a bounded representative touch/device-descriptor subset and a representative cross-engine subset if CI duration and reliability remain acceptable.
3. **Continuous temporal assertion — `PROPOSED`.** Add a mutation/timeline assertion or short-interval sampler proving that exactly one usable accountability link exists continuously from initial navigation through the delayed optimiser, rather than only at the current phase snapshots.
4. **Cache-version contract — `PROPOSED`.** Review and safely update the loader-version architecture. At this audit, `assets/share-controls-20260817.js` requests `unitary-public-shell-20260818.js?v=20260819a` while the shell internally reports `20260826a`, and `assets/ricpe-filed-status-20260817.js` requests `optimum-reader-journey-finish-20260818.js?v=20260818a`. A future change must reconcile the validator-pinned loader chain and prove mixed/stale-cache behaviour without broad whole-site rewrites.
5. **Required-check or sharding decision — `HOLD / USER AUTHORITY REQUIRED`.** Review whether this long matrix should be required, scheduled, or split into a fast homepage gate plus a full artifact-producing suite. Do not change repository rulesets or promote a new required check without the explicit enforcement authority and shadow-mode proof required by `AGENTS.md`.

## 5. Deletion-safety dimensions

- `THREAD_REASONING_CONTINUITY`: **satisfied** — diagnosis, the two rewrite layers, the corrective decisions and limitations are recoverable here and in Git history.
- `IMPLEMENTATION_STATE_CONTINUITY`: **satisfied** — both PRs, exact merge SHAs, files, workflow runs and deployment state are recorded.
- `PRIMARY_EVIDENCE_COMPLETENESS`: **not applicable to this UI-only repair** — no new evidential proposition or private source was analysed or published.
- `LIVE_PUBLICATION_VERIFICATION`: **satisfied for the independent ES/EN desktop-width read-back**; physical Android and cross-engine confirmation remain open as stated above.
- `COMMUNICATION_VERIFICATION`: **not applicable** — no email, message, filing or calendar action was prepared or sent.
- `CUSTODY_RESILIENCE`: **not claimed** — CI screenshots are reproducible derivatives and may expire.
- `DISASTER_RECOVERY_SAFETY`: **not claimed** — this thread did not create or restore-test an independent repository/site backup.

## 6. Final close-out

**What was done:** the disappearing accountability navigation was repaired in both rewrite layers, the prompt and automated regression were expanded, PRs #1043 and #1048 were merged, the exact final merge was deployed, and the live Spanish and English controls were read back before and after the delayed optimiser and clicked successfully.

**What was not done:** no legal/evidential content changed; no private material was committed; no email or third-party communication occurred; no physical Android, Firefox or WebKit session was controlled; no independent disaster-recovery copy was created.

**What proves the state:** current `main`, the two merged PRs, the cited successful PR-head and exact-merge workflow runs, Pages run 32949369456 and the recorded cache-busted live read-back.

**What remains open:** the five bounded future-thread items in Section 4 and the wider recovery/backlog items in `ops/FIVE_ACTOR_PRESERVATION_AND_READER_JOURNEY_BACKLOG.md`.

No unique substantive source, reasoning, correction, implementation state or recovery instruction from this thread remains only in chat. Deleting the conversation does not authorise deletion, demotion, relabelling or unlinking of the protected accountability presentation, repository history, CI records, source files or public routes.
