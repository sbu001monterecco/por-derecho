# THREAD DELETION CONTINUITY AUDIT — UNITARY PUBLIC SHELL

**Audit date:** 19 August 2026  
**Thread scope:** the implementation / merge / closeout thread that created the bilingual unitary Case Control Room, controlled search, homepage consolidation layer, DP 1901 English routing safeguard, and regression gate.  
**Audit target:** current `main` at `34ea55e77c03bc00b3fbbc44491bc2ba8c9001d3`.  
**Controlling implementation PR:** #419, merged at `e26f6aa54331ba77dded1218eee9a062b5a094a3`.  
**Governance closeout PR:** #420, merged at `7b19d47e6ab7b07e1f6f757b234ca86892434704`.

## Verdict

**PASS — no substantive deletion, overwrite, route loss, evidential-boundary loss or silent rollback located for this thread.**

The current repository still contains the full unitary-shell implementation and its governance record. Later work after the closeout is additive or belongs to separate legal-representation / retracto / PwC tracks; it has not modified or deleted the unitary-shell core files.

## Continuity evidence

### 1. Later-main comparison

Comparison from closeout commit `7b19d47e6ab7b07e1f6f757b234ca86892434704` to current-main head `34ea55e77c03bc00b3fbbc44491bc2ba8c9001d3` shows `main` is 23 commits ahead and 0 behind.

The changed-file set in those later commits does **not** include:

- `en/case-control-room/index.html`
- `es/sala-control-caso/index.html`
- `en/search/index.html`
- `es/buscar/index.html`
- `en/dp-1901-2026/index.html`
- `assets/unitary-public-shell-20260818.js`
- `assets/unitary-public-shell-20260818.css`
- `assets/unitary-public-shell-20260818.a11y.css`
- `assets/data/unitary-route-registry-v1.json`
- `assets/share-controls-20260817.js`
- `sitemap-unitary-shell.xml`
- `robots.txt`
- `scripts/render_unitary_public_shell.mjs`
- `.github/workflows/validate-unitary-public-shell.yml`
- `publication-manifests/unitary-public-shell-20260818.json`

The later touched files concern separate workstreams, including legal-representation registers, retracto / crédito litigioso, lender-of-record material, and PwC / Matkator finca 8588 continuity work.

### 2. Current manifest remains controlling

`publication-manifests/unitary-public-shell-20260818.json` remains on `main` with:

- `current_state: MERGED`;
- controlling PR #419;
- merge SHA `e26f6aa54331ba77dded1218eee9a062b5a094a3`;
- 16 implementation files changed, 704 additions, 0 deletions;
- 0 substantive existing-dossier deletions;
- final browser regression result `PASS`;
- 20 desktop/mobile renders passed;
- publication/deletion-safety, operational-control, mission-critical and supervisory-practice gates recorded as passed;
- live public-edge verification still explicitly not overstated.

### 3. Case Control Room preserved in both languages

Both canonical Control Room pages remain present and preserve:

1. property / 262-finca perimeter;
2. CEXP / productive-unit economics;
3. Concurso 36/2012 — AC / Court / calificación;
4. material control / 7 June 2018;
5. RICPE / RIC / HNT / later finance and public-support layers;
6. institutional response / answer-holders.

The three reader modes remain present:

- Understand / Entender;
- Audit / Auditar;
- Respond / Responder.

The evidential grammar, answer dashboard, and the explicit panel asking what evidence would materially change or narrow the interpretation also remain present.

### 4. Controlled search preserved

Both search routes remain present:

- `/en/search/`;
- `/es/buscar/`.

The controlled route registry remains present. Verified high-value aliases / discovery terms include, among others:

- `CEXP`;
- `737338` / `737338.85`;
- `8588`;
- `Borja`;
- `ACTUA` / `ACTÚA`;
- `Series F` / `Serie F`;
- `DP 1901`;
- `RICPE`;
- `Matkator`;
- `CGPJ`.

Search remains explicitly a discovery layer rather than an evidential finding.

### 5. DP 1901 procedural-separation safeguard preserved

`en/dp-1901-2026/index.html` remains present and still states that DP 1901/2026, DIP 2/2026 and DP 1956/2026 must remain separate procedural references unless a primary judicial or prosecutorial record expressly connects them for a defined purpose.

No substitution of a neighbouring Fiscalía route was located.

### 6. Homepage / global-shell architecture preserved

The route-aware unitary shell remains present with:

- simplified homepage primary navigation;
- Case Control Room gateway;
- compact Case/Search utility on substantive dossier pages;
- bilingual language routing;
- route registry + sitemap fallback search;
- preserved `assets/site.js` migration boundary.

No one-shot rewrite of the mature legacy loader chain has occurred in this thread or in the subsequent 23 commits.

## Apparent deletions that are not substantive losses

PR #420 contained line deletions inside governance metadata because it replaced stale implementation-state text such as `PR_OPEN` with the final `MERGED` state and inserted merge / CI evidence. Those are state transitions, not deletions of evidence, routes or reader functionality.

No public dossier, source-control boundary, competing-evidence rule, correction rule or current-status page from this thread was removed by that closeout.

## Unchanged caveat

The thread deliberately did **not** claim `LIVE_VERIFIED` from the execution environment because direct public-edge GitHub Pages readback could not be independently resolved there. That caveat remains preserved; it is not a deletion or regression.

## Deletion-safety conclusion

**No remediation is required.**

Future changes should trigger a new continuity check if they modify any of the unitary-shell core paths listed above. A future audit should compare against current-main head `34ea55e77c03bc00b3fbbc44491bc2ba8c9001d3` (or the later merge commit containing this audit record) and should fail closed if any canonical route, evidential-boundary text, DP 1901 separation rule, search registry, or regression workflow disappears without an explicit supersession record.
