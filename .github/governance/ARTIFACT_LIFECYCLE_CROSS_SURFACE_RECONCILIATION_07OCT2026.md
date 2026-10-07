# Artifact lifecycle and cross-surface reconciliation control

**Control ID:** `PD-GOV-ARTIFACT-LIFECYCLE-20261007-01`  
**Status:** ACTIVE ADDITIVE GOVERNANCE — implementation evidence remains surface-specific.  
**Scope:** substantive Por Derecho / Project Sun Rock / AWESWELL artifacts, drafts, filing packages, counsel packs, reports, spreadsheets, PDFs, generated files and release-ready derivatives across ChatGPT conversation/Library, private Google Drive, Gmail and repository control surfaces.

## 1. Purpose

This control closes a recurrent continuity defect: a substantive artifact may be correctly created and preserved on one surface, while a later thread searches another surface and incorrectly concludes that the artifact does not exist.

The control does not create a second matter register. Existing matter/proceeding IDs, source registers, GOV-020 communications control, source-binary controls, workspace checkpoint controls and thread-deletion rules remain authoritative in their existing scopes.

The invariant is:

> A substantive reusable artifact is not operationally complete merely because bytes exist somewhere. Its identity, current version, canonical private home, supersession state and release/receipt state must be recoverable across the required surfaces.

## 2. Surface roles

Keep surface roles distinct.

- **ChatGPT conversation / Library:** creation, recovery, bounded working custody and user-facing artifact retention. Library is a valid source/custody surface, but it is not by itself the canonical private workstream home for an active reusable artifact when the matter has an established business-Drive home.
- **Business Google Drive:** canonical private operational home for active private workstream artifacts, source-linked working derivatives, current-version pointers, approval/release packages and receipts, unless an existing matter control specifies another private home.
- **Gmail:** communication drafting and provider event evidence. Gmail Draft is not the master draft register. Sent/Draft labels do not establish approval, current-version authority, filing, receipt or merits state.
- **GitHub/GitLab:** public-safe governance/code/projection and repository-controlled text. Do not place private evidence, privileged drafts or sensitive source binaries in public Git merely to achieve parity.
- **Matter/workspace registers:** identity, routing and state pointers. They must point to artifacts; they do not replace the underlying bytes.

## 3. Registration trigger

Register an artifact under this control when any of the following is true:

1. it is intended for external use, signature, filing, counsel/regulator/counterparty review or later reuse;
2. it is a substantive legal, commercial, financial, evidential or governance deliverable;
3. it is a fixed export or package that could later be confused with another version;
4. it materially changes a current workstream state or preserves a thread-only conclusion;
5. the user asks to preserve, canonicalise, reuse, file, send, approve, sign, review or continue it later.

Do not require full registration for ephemeral calculations, transient scratch text or trivial formatting experiments that have no continuing workstream value.

## 4. Identity model

Keep these identities separate:

- **Matter/proceeding ID:** the existing canonical workstream or proceeding reference.
- **Artifact family ID:** one stable identity for the authored document/package family.
- **Artifact version ID:** exact version of that family.
- **Source occurrence IDs:** original inputs and their independent provenance.
- **Release / filing event ID:** each actual transmission or filing event.
- **Provider IDs:** Library file ID, Drive file ID/revision, Gmail message/thread ID, repository path/commit, portal receipt or court registry identifier.

A filename, subject line, “FINAL”, latest-modified timestamp or shared hash is not a substitute for those identities.

## 5. Minimum artifact routing record

For every registered artifact family, the existing register or matter control must be able to recover at least:

- artifact family ID;
- matter/proceeding ID and capacity;
- human title;
- current version;
- lifecycle state;
- authoritative-current pointer;
- editable/native object ID when applicable;
- fixed release/export ID and SHA-256 when applicable;
- ChatGPT Library file ID when created/preserved there;
- canonical private Drive ID/path or explicit write-back gap;
- repository path only when appropriate to the repository's privacy role;
- supersedes / superseded-by links;
- approval source and scope when applicable;
- release/filing event IDs;
- provider message/submission IDs and receipts after action;
- last verification time/cutoff;
- open preservation, routing or access gap.

Use an existing register where one owns the workstream. A derived artifact-routing index is permitted only as a pointer layer; it must not become a rival matter master.

## 6. Lifecycle states

Do not compress materially different states.

For authored artifacts, use the smallest applicable state vocabulary:

`CREATED → WORKING → REVIEW → APPROVED → SIGNED → SUBMITTED/SENT → REGISTERED/DELIVERY-EVIDENCED → ASSIGNED → ACCEPTED/SERVED/ACKNOWLEDGED → DECIDED/CLOSED`

Also support:

- `SUPERSEDED`
- `WITHDRAWN`
- `HOLD`
- `UNKNOWN`

Not every artifact traverses every state. A state advances only from evidence.

Keep lifecycle state separate from:

- source-custody state;
- hash/readback state;
- legal/evidential merits;
- thread deletion readiness;
- runtime/software enforcement.

## 7. Exactly one current pointer

Within one artifact family and purpose, designate exactly one authoritative current version or explicitly record that the family is in conflict/HOLD.

Preserve prior versions. Do not delete a superseded draft merely to make the workspace tidy.

A Gmail draft that remains in the Drafts folder after a successor was approved or sent must be marked or indexed `SUPERSEDED / DO NOT SEND`; its continued Draft label does not make it current.

## 8. Mandatory write-back

When a substantive reusable artifact is generated in ChatGPT conversation/Library for a matter that has an established canonical private Drive home:

1. preserve the generated artifact;
2. write or upload the artifact to the canonical private home in the same execution window when tooling/authority permits;
3. record the Library ID and Drive ID as two surface locators for the same artifact version;
4. verify Drive readback;
5. update the current-version/routing pointer.

If write-back is impossible or intentionally deferred, record `WRITEBACK_PENDING` / AMBER with the reason and next bounded action.

**A Library-only substantive artifact may be safely preserved, but it is not platform-GREEN for active reuse until its required canonical write-back/routing pointer is closed.**

Do not bulk-copy every historical Library artifact merely because this rule exists. Apply prospectively and repair active/high-value gaps by priority.

## 9. Reconciliation before “not found”

Before stating that a known/prior artifact “does not exist”, “was not created” or “cannot be found”, perform the required scoped reconciliation.

For a material artifact whose location is uncertain, search in this order unless the workstream gives a narrower authoritative route:

1. current conversation attachments / current file refs;
2. ChatGPT Library by exact filename, canonical ID, title fragments and distinctive text;
3. canonical business-Drive matter home and relevant private indices;
4. Gmail Draft/Sent/provider events when the artifact may have been attached or embedded;
5. GitHub/GitLab only for repository-appropriate/public-safe artifacts and governance;
6. matter/workspace handoffs, audit manifests and supersession controls.

Use aliases, predecessor filenames and content phrases when exact filename search fails.

If every required surface was not checked, say **“not located in the checked surfaces”**, not “does not exist”.

A connector limit, stale link, permission failure or unmounted Library object is an access/retrieval gap, not proof of source absence.

## 10. Search optimisation

Normal continuation should be index-first, not scan-everything-first.

1. read the matter Start Here/current-state record;
2. resolve the artifact family/current pointer;
3. retrieve the exact provider IDs;
4. verify current bytes/state;
5. broaden to cross-surface search only if the pointer is absent, stale, conflicting or fails readback.

A broad full-system scan is a repair/fallback procedure, not the default retrieval path.

This rule reduces repeated searches while preserving the ability to recover orphaned artifacts.

## 11. Release and filing packages

For consequential releases, freeze the exact package before action.

The release/filing manifest should bind:

- exact principal document version;
- ordered annex list;
- hashes/page counts where applicable;
- sender/presenter and capacity;
- destination and official/counterparty reference;
- approval scope;
- channel;
- release/filing event ID.

After action, preserve the actual provider-native event and receipt and compare the actual attachments/submitted binaries to the frozen package.

Do not infer:

- filing from preparation;
- receipt from upload;
- judicial assignment from receipt;
- acceptance from assignment;
- merits treatment from acceptance.

## 12. Supersession and historical integrity

Never silently overwrite a material prior version.

- retain prior bytes or native revision where required;
- link successor and predecessor;
- label historical material clearly;
- preserve contrary/adverse versions;
- never retrofit a canonical reference into received, signed, stamped or already-sent source bytes.

New authored versions should carry their appropriate internal reference before approval/signing where disclosure-safe.

## 13. Thread deletion / restart gate

A substantive thread cannot be GREEN for deletion when:

- a material artifact exists only in chat/Library but required canonical write-back is still open;
- the current-version pointer is unresolved;
- an external-ready package lacks exact approval/release state;
- a filing/send is claimed without provider readback/receipt appropriate to that claim;
- a fresh context cannot recover the artifact from durable IDs without relying on chat memory.

A thread may remain open on merits while still being restartable if all artifacts, sources, states and next actions are durably recoverable.

## 14. Concurrency and write safety

Use revision/lease guards where available. Otherwise:

- fresh-read the target;
- preserve the before-state;
- make narrow serialised writes;
- read back;
- detect intervening revisions;
- reconcile rather than overwrite.

Do not run parallel writes against the same canonical rule/register/file.

## 15. Platform enforcement levels

Keep these separate:

1. **Policy adopted** — this control exists and is referenced.
2. **Manual/connector application** — a thread/operator actually applied it.
3. **Validator coverage** — repository checks confirm required rule references/schema.
4. **Cross-surface runtime automation** — automatic registration/write-back actually runs in production.
5. **Independent assurance** — a fresh-context/recovery test verifies behavior.

Do not call level 4 or 5 GREEN merely because a policy file or validator exists.

## 16. Repair priority for legacy drafts

Do not attempt to clean hundreds of historical Gmail drafts by deletion.

Classify active/high-value candidates first:

- `CURRENT`
- `SUPERSEDED`
- `HOLD`
- `ARCHIVE`
- `UNKNOWN`

Prioritise:

1. court/regulatory filings and deadlines;
2. counsel instructions and approved outbound communications;
3. financing/listing/execution documents;
4. active commercial negotiations;
5. lower-risk historical drafts.

Unknown historical drafts remain preserved until reconciled. Gmail Draft count is not an outstanding-task count.

## 17. Interaction with existing controls

This control is additive.

- GOV-020 continues to govern communication identity and verified dispatch.
- R-BIN-013 / GOV-082 continues to govern source-binary preservation.
- workspace checkpoint controls continue to govern matter persistence.
- thread deletion sentinel continues to govern chat deletion.
- continuity/propagation controls continue to govern cross-workstream effects.
- privacy/publication controls continue to govern what may enter public Git.

Where a workstream has a stricter rule, the stricter compatible requirement applies.