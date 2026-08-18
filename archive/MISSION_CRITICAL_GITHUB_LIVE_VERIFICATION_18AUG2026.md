# MISSION-CRITICAL GITHUB HARDENING — LIVE VERIFICATION

**Date:** 18 August 2026  
**PR:** `#354 — Harden mission-critical GitHub production controls`  
**Merge SHA:** `671b0c9026d0c4df188be07f60c137ce825367a0`  
**Public host:** `https://sbu001monterecco.github.io/por-derecho/`

## Objective verification

GitHub Actions run `32134809955` (`Verify mission-critical hardening live`) ran on the exact merge SHA and completed successfully.

The run:

- polled the public GitHub Pages host;
- required the unique `psr-mission-critical-hardening-20260818-v1` probe introduced by the hardening release;
- verified the Spanish homepage;
- verified the English homepage;
- verified the Spanish RICPE route;
- verified the Spanish CNMV route;
- verified the global site loader;
- uploaded machine-readable verification evidence;
- published commit status `pages-propagation/mission-critical-hardening = success`.

**Evidence artifact:** `9323553989`  
**Artifact digest:** `sha256:2b43c17452a54753b60c2255cb67feb299c13d2da3c36eed277911f3fdf8f55d`

The artifact was created at `2026-08-18T12:03:49Z`; the workflow completed successfully at `2026-08-18T12:03:54Z`.

At that point GitHub still reported `main` at the same merge SHA. The release is therefore the current positively live-verified production source and is recorded in `ops/LAST_KNOWN_GOOD.json`.

## Remaining gates

Live propagation does not close the separate administrative controls:

- GitHub branch/ruleset enforcement remains open in issue `#355`;
- independent off-GitHub backup plus a clean restore test remains open in issue `#356`.

Those gaps remain explicit and must not be converted into a `100% disaster recovery` claim.
