# DEPLOYMENT VERIFICATION — AC SATURATION / ARTICLE 82 / NON-ERASURE

**Date:** 20 August 2026  
**Public content merge:** PR #676  
**Public content merge commit:** `48e7a4f95bc8ff4cab2d510b0a9dbb5fea22dd9e`  
**Verification PR:** #677  
**Status:** `PUBLIC ROUTES VERIFIED`

## Purpose

This record verifies that the bilingual public changes preserved by `archive/THREAD_DELETION_AUDIT_AC_SATURATION_ART82_ACCOUNTABILITY_20AUG2026.md` were not merely merged into source control but were actually retrievable from the production GitHub Pages host.

## Independent rendered-production check

GitHub Actions production-smoke run:

- run ID: `32426319325`;
- job ID: `96608881413`;
- result: `PRODUCTION SMOKE CHECK: PASS`;
- evidence artifact: `production-smoke-evidence`, artifact ID `9427533387`;
- artifact SHA-256 reported by the runner: `27c2859f7c077c28b93e6e7b19e62f4d29df0b5f899047644902b3aa9951fb64`.

The runner fetched the public production host rather than repository source and reported all configured routes `OK`.

## Six thread-critical routes verified

1. `en/insolvency-36-2012-insolvency-administrator/` — `ac_accountability_en=OK`;
2. `es/concurso-36-2012-administrador-concursal/` — `ac_accountability_es=OK`;
3. `en/reverse-engineering-360-sun-park-chain/` — `reverse_engineering_ac_en=OK`;
4. `es/ingenieria-inversa-360-cadena-sun-park/` — `reverse_engineering_ac_es=OK`;
5. `en/dp-1956-2026/` — `dp1956_non_erasure_en=OK`;
6. `es/dp-1956-2026/` — `dp1956_non_erasure_es=OK`.

The verified markers include the Article 82/83 supervision control and the explicit non-erasure rule that later correction, production, restitution or accounting is a later dated event rather than retroactive exoneration or proof of prior guilt.

## Smoke-monitor maintenance performed

The first verification run (`32426216734`) already returned all six thread-critical routes `OK`, but the overall legacy smoke suite failed on three stale marker assertions unrelated to PR #676: the two existing AC credit-to-title gatekeeper marker strings and the global loader marker strings had moved on in the live site.

PR #677 refreshes those smoke assertions to the current source/live markers and adds the six thread-critical routes as permanent triggers/checks. The follow-up run `32426319325` then returned all configured production checks `OK` and `PRODUCTION SMOKE CHECK: PASS`.

## Separate repository-integrity warning

A broader `Publication integrity gate` remains capable of failing for repository-wide validation reasons unrelated to the AC saturation / Article 82 changes. In the preceding #676 verification, the observed failure concerned a missing validator script (`scripts/verify_eleconomista_pages.py`). That defect was not introduced by the Article 82/accountability changes and is not treated here as evidence that the six verified production routes failed.

## Deletion-safety consequence

Together with:

- `archive/THREAD_DELETION_AUDIT_AC_SATURATION_ART82_ACCOUNTABILITY_20AUG2026.md`;
- `CURRENT_HANDOVER.md`;
- the AP evidence-route control;
- the DP 1901 / DP 1956 crosswalk;
- the missing-evidence register;
- the six verified bilingual public routes;

this closes the implementation/deployment gap for the originating thread.

**Thread status after merge of this verification record: `DELETION-SAFE WITH OPEN EVIDENCE`.**

This does not mean the underlying case is evidence-complete. Primary records identified as missing/open must still be obtained and independently verified before any filing or definitive allegation.