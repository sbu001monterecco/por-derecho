# Truth Machine event bus and three-state control plane — 25 September 2026

**Control:** PD-TRUTH-EVENTBUS-20260925-01

## Purpose
Replace broad rescan instructions with immutable, source-bound change envelopes. ChatGPT can identify and frame a change; deterministic repository controls validate source pins, traverse dependencies and queue the smallest affected review set.

## Three independent states
1. **Machine state** — hashes, source presence, structural checks, deterministic candidate cues and dependency signals.
2. **Analyst state** — source/context/contrary-evidence/lawful-alternative assessment. Prior assessments survive until explicitly changed.
3. **Release state** — prepared, merged, deployed and live-readback status per host.

No state silently promotes another.

## Event route
SOURCE / METHOD / CORRECTION / RELEASE EVENT → exact host pins → affected nodes → dependency traversal → candidate reopen queue → semantic review → changed/no-change decision → machine-readable aggregate → scoped release → second-host verification.

## Speed lanes
**FAST:** bounded public-safe JSON/visual/control changes with no private source publication and no foundational schema/legal-state migration. Unrelated defects stay isolated and visible.

**FULL:** foundational schemas, global navigation, source-registry meaning, private/public boundary, legal/evidential control or broad multi-page dependency changes.

FAST never weakens source integrity, privacy, evidence-state or merits-signoff requirements.

## Anti-loop controls
Host copies and AI restatements are derivative until independent origin is demonstrated. No event count, model count or host count increases evidential weight. A method update reopens review; it does not establish that an existing statement became false.

The current event TM-EVT-20260925-0001 binds the cross-agency methodology registry and R33 flagship reference state identically across GitHub and GitLab and queues the five current priority candidates for method-aware review.
