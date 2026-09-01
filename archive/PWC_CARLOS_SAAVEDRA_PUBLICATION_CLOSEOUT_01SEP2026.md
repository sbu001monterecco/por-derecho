# PwC / Carlos Saavedra publication closeout

**Control date:** 1 September 2026

**Publication:** `PD-PWC-CS-PUBLICATION-20260901-01`

**State:** `LIVE_VERIFIED_WITH_SOURCE_SAFE_PUBLICATION_BOUNDARIES`

## Outcome

The validated PwC / Carlos Saavedra package is public. PR [#1328](https://github.com/sbu001monterecco/por-derecho/pull/1328) merged exact reviewed head `a40cf773bca7dde4e37fa747ea060097a5b9693b` as merge `d1817de1b8613a8e0d340f1453acda99e440e5af`. The reviewed head had 36 successful pull-request workflow runs and zero failures.

The merge preserved concurrent, additive HKI evidence from PR #1329. The primary merge tree is therefore `c0c02b6971173394ccf08e1aeb6e3fd541635242`, while the exact reviewed PwC tree remains `b90be90eba963d00a8feb91c698e0ce0c624bcea`; the PwC release-critical bytes are unchanged.

## Deployment and public readback

GitHub Pages run [33542787869](https://github.com/sbu001monterecco/por-derecho/actions/runs/33542787869) built and deployed the exact primary merge successfully between `18:17:48Z` and `18:20:19Z`.

- [Spanish PwC / Carlos Saavedra page](https://sbu001monterecco.github.io/por-derecho/es/pwc-canarias-carlos-saavedra-sun-park/)
- [English PwC / Carlos Saavedra page](https://sbu001monterecco.github.io/por-derecho/en/pwc-canarias-carlos-saavedra-sun-park/)
- [Carlos Saavedra portrait](https://sbu001monterecco.github.io/por-derecho/assets/actors/carlos-saavedra--linkedin-profile--20260901.jpg)
- [Machine-readable finite census](https://sbu001monterecco.github.io/por-derecho/assets/data/caepr-caret-pwc-carlos-saavedra-first-hop-v1.json)

Direct browser inspection after deployment confirmed the canonical Spanish URL and title, the Carlos Saavedra identity caret, the rendered 800 × 800 portrait, `32/35`, `PARCIAL — NO TODO ES^`, the 12–16 May and 6–10 June source-safe additions, and collision-safe CNMV ID `PD-SP-I-0042`.

The dedicated verifier `scripts/verify_pwc_carlos_saavedra_live.py` checks exact live byte parity for both pages, the portrait, PwC ledger, current identity/caret surfaces and the registered authority-graph successor. [Closeout workflow run 33544595557](https://github.com/sbu001monterecco/por-derecho/actions/runs/33544595557) passed all nine checks at `2026-09-01T18:36:30.399717Z`; its workflow also runs on every relevant main push.

## Finite public result

`32/35 CARET_CONFIRMED · 3 CARET_PENDING · 0 CARET_SUSPENDED · 20 EVENTS · 19 EVIDENCE RECORDS · 1 CANONICAL VISUAL ASSET`

The verdict remains **PARTIAL — NOT ALL IS^**. The unresolved objects are the exact PwC Canarias contracting perimeter and the exact PwC UK/Spain Legal/Risk receiving channels. A caret confirms reconciled identity only; it does not prove conduct, mandate, reading, knowledge transfer, conflict, causation, liability or wrongdoing.

## Source and privacy boundary

The public package contains source-safe summaries expressly authorised for publication. It does not expose private email addresses, message IDs, connected-source locators, private attachment paths, native audio or non-public source text. The portrait is the controlled 143,942-byte JPEG registered at SHA-256 `6abc688f2eb1aabceaa68455a8679cb48debae7afb39f39b7eb31e799493f73d`.

## Merge-SHA workflow reconciliation

Two live jobs exposed stale assertions rather than content defects:

1. the unitary verifier expected the frozen `2026-08-31` digest control date to be rewritten instead of testing the `2026-09-01` reconciliation addendum separately; and
2. the older PEP/proceedings verifier expected superseded bilingual display strings on unchanged live routes.

The closeout corrects those assertions without rewriting historical attestations or changing the PwC public claims.
