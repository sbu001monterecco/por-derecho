# Named-person visual platform audit — 25 September 2026

## Scope
GitHub, GitLab, current JTP public-reader visual paths, canonical portrait assets, composite sidecars and visual validation controls.

## Findings
1. **Canonical real portraits exist for all five JTP actors.**
   - JTP canonical source was preserved in Drive and is now an exact repository-controlled source in the hardened path.
   - AC and Alberto portraits are byte-locked canonical assets.
   - JDAM and LPAM are user-supplied, explicitly mapped and hash-controlled.
2. **The two rejected conversational image generations are not valid publication assets.**
3. **GitHub already contains a deterministic JTP exact-source workflow**:
   `ops/jtp/JTP_ACTOR_IMAGE_SOURCE_LOCK_20260925.json`,
   `scripts/compose_jtp_actor_infographic_exact.py`,
   and `scripts/verify_jtp_actor_source_lock_20260925.py`.
   Its published composite records zero changed pixels outside authorised portrait boxes.
4. **GitLab had a parity gap**: exact AC/JDAM/LPAM/judge assets existed, but the JTP canonical binary and deterministic JTP visual control were not on main. This hardening branch closes that source/control gap and adds an exact-source HTML actor grid to the bilingual JTP reader.
5. **Legacy five-actor stylised images are explicitly editorial stylisations, not documentary portrait evidence.** They are preserved but quarantined from use as identity sources.
6. **Existing visual registry validation did not prohibit generative re-synthesis of a correctly registered face.** The new rule closes that gap by controlling rendering method and factual text, not only source registration.

## Platform rule
Identity source registration is necessary but not sufficient. A named-person visual must also prove deterministic use of that source.

## OpenAI reproducibility packet
Use incident ID PD-AI-IMG-INC-20260925-01 and the two generation IDs above. The minimal reproduction is: exact approved real-person references supplied; explicit no-hallucination instruction; image model nevertheless re-synthesised four named faces and generated unsupported factual text.

## Publication boundary
No person is assigned liability, criminality, coordination or knowledge by being shown in an actor-context layout.
