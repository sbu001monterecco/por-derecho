# JSP historical-release and successor gate transition — 6 October 2026

**Overall RED at authoring:** the proposed correction has passed local conservation
and corruption checks; native execution of the complete two-stage job is pending.
The earlier failed release-only run remains a historical failure, not a rerun or
retroactive GREEN. Current native results are recorded in Draft #1795 and control #1428.

| Component | State | Scope |
| --- | --- | --- |
| Earlier shadow implementation | GREEN | Native run 37424986598 passed on commit 91a52384e2670c284d52f8f001d8f70d84026c5d. |
| Expanded negative controls | GREEN, local | Eighteen corruptions rejected, including route, qualification, validator and unreviewed workflow changes. |
| Representative path scope | GREEN, local | Unrelated route, asset and urgent-document path simulations do not become dependent on this specialist gate. Their independent gates still apply. |
| Historical release validator | Preserved | Script bytes and historical date/count/source assertions remain unchanged. |
| Existing required gate before transition | RED | Run 37424986348 failed; only successful native execution of the new head can establish the correction. |
| Complete native two-stage job | AMBER | Must pass historical QA, successor conservation, current links, projection consistency, negative controls and no-mutation checks. |
| Evidence / predecessor closure | AMBER | #1791 remains open; this technical correction does not resolve substantive identity, source-equivalence or original-custody questions. |

## Why this corrects the failure

The original validator compares a release candidate with its pre-release main. Its
379 total identities, 27 additions and 5 September date are correct for the original
release. Applying that same comparison to a later registry update incorrectly
expects the already-published JSP records to be new again.

The existing `JSP 2017 dossier scoped QA` / `scoped-jsp-qa` job now invokes a
two-stage runner. Its required-check identity, permissions, checkout pins, timeout,
artifact upload and retention remain the same. No branch-protection/ruleset change,
new reviewer service, merge or deployment is made. This is the narrow existing-Draft
correction following the user's continuation instruction after native shadow proof.

1. Require original release ancestry, current-main incorporation and a forward PR
   base. Audit conservation of the current candidate independently.
2. Create a disposable local clone borrowing local Git objects read-only. Only its
   isolated `origin/main` is set to the exact original release parent.
3. Execute the byte-unchanged original validator on release
   `65d56cec10e11f5a5c0861bb087ee87e64f5effa` against parent
   `01116d63e93eb1e2819ae53a4060104477883407`. Every original historical assertion must
   pass. Historical report identity and result are independently checked.
4. Check the current candidate's JSP links, bilingual anchors, JavaScript syntax,
   current registry projections, eighteen negative controls and tracked-file
   cleanliness. Verify candidate HEAD and its main ref were not changed.
5. Require both phases; write a combined report under `jsp-qa/report.json` and
   retain the historical report/source archive separately under `historical-release`.
   Failure of either phase fails the existing job.

## Preservation and precise acceptance boundary

Twenty-two frozen JSP objects remain byte-identical by mode/type/Git SHA, including
PDF/images, ES/EN routes, qualifications, source register, registry shards and the
original validator. The 23rd object is the existing QA workflow: its original bytes
remain in the pinned release, while its one exact reviewed transition is admitted
by Git object `982a0910accfb698834a8db5896fb398e664473e`. Any other workflow edit fails.
The workflow watches the new runner, conservation checker and negative tests as
well as its existing watched paths.

The successor phase requires every incorporated-main identity and its existing
fields to remain unchanged. It accepts additional top-level fields and new sourced,
non-colliding, correctly typed identities with exact recomputed counts and monotonic
dates. It does not approve the truth or legal effect of those additions. Existing
substantive, identity, publication and privacy controls continue to apply.

Five corrections already on current main are explicitly reported without re-auditing
their substance. They are not overwritten with obsolete historical wording. Changes
to frozen JSP material or replacement of current identity values are rejected and
require their own evidence-backed correction review, not a generalized exemption.

## Reviewed topology and rollback

This uses the existing Draft, current maintainer and existing CI topology; no new
required approver, credential, network service or universal gate is introduced.
The shadow baseline and negative controls are in the same reviewable repository.

If this transition fails, record the failure in #1795/#1428 and restore the QA
workflow to its exact pre-transition blob in an ordinary additive commit. The
conservation checker already accepts that original workflow, so its advisory run
can remain. Preserve all reports, source history, tests and original failed runs;
do not force-push or relax the historical pins. No rollback is permission to merge
or deploy a failing candidate.

This record supplements, and does not rewrite, the earlier shadow review. Binary
Git identity is not independent Drive custody; technical GREEN never authorizes
closing #1791 while unique material or substantive admission remains unresolved.

🟠 THREAD — preservation pending · native gate execution and evidence reconciliation
