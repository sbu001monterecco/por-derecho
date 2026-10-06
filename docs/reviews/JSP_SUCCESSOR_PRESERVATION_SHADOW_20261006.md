# JSP successor preservation — advisory review, 6 October 2026

Overall **RED**: the required JSP release gate still fails on the PD-MEM successor.
This proposal runs separately in advisory mode. It does not replace, disable,
repin, bypass or mark that gate satisfied. No required-check configuration changes.

| Component | State | Bounded finding |
| --- | --- | --- |
| Frozen JSP object conservation | GREEN, local readback | All 23 protected Git objects match the original release, including original PDF/image objects, ES/EN routes, source register, shards and original validators/workflows. |
| Historical release denominator | GREEN, local readback | Original release remains 379 identities, with 27 additions: 11 people, 15 organisations, one proceeding. |
| Later registry delta | GREEN, conservation only | One organisation added; four existing identities receive additive fields. All existing values from incorporated main are preserved. This is not substantive admission approval. |
| Existing projection validator | GREEN, local | 380 identities: 176 people, 100 organisations, 11 structures, 49 institutions, 44 proceedings. |
| Negative controls | GREEN, local | Fourteen corruptions rejected; positive real-data and synthetic admission baselines pass. |
| Native advisory execution | AMBER at authoring | The new workflow must still execute on its committed head. Consult the current PR receipt. |
| Required JSP gate | RED | Historical release-only assumptions remain incompatible with later registry updates. |
| Identity reconciliation / original-binary custody | AMBER | #1791 remains open. No independent original-binary custody or new relationship truth is certified here. |

## Exact boundaries

- Original release: `65d56cec10e11f5a5c0861bb087ee87e64f5effa`.
- Original parent: `01116d63e93eb1e2819ae53a4060104477883407`.
- Incorporated current main: `f0d472567ad71a4140ae8ab3eb7a408aa8aa9e5f`.
- Locally audited candidate: `3bfe66a966b2196e6b73f27aad64c635fbf03670`.
- Repository: `sbu001monterecco/por-derecho`; controlling Draft #1795; control issue #1428.

The local audit used complete, nontruncated GitHub trees and 30 independently
read text blobs; every consumed text blob was checked against its Git object SHA.
Binary objects were compared by Git tree identity, not downloaded or independently
preserved. The native workflow uses the actual full Git history, checks ancestry,
and runs the existing projection validator without writing tracked files.

Frozen content is checked by mode, type and object SHA, including ES/EN pages and
the unchanged original evidence-integrity/browser scripts. This checks conservation
of their bytes, not fresh browser execution or independent verification of the
external official source. Other CI controls remain responsible for their own scope.

Five identity records were already corrected between the historical release and
current main: `PD-SP-O-0001`, `PD-SP-I-0013`, `PD-SP-R-0003`, `PD-SP-R-0006`,
`PD-SP-R-0034`. Their current values are preserved; the advisory report explicitly
lists them as inherited changes not substantively re-audited. Historical versions
remain addressable through the release commit. No old wording is restored over
current corrections.

The candidate adds `PD-SP-O-0103` and adds fields to `PD-SP-O-0002`, `PD-SP-O-0004`,
`PD-SP-P-0001`, `PD-SP-P-0002`. Conservation does not decide the outstanding Group
Sun Rock project/structure admission, source crosswalk equivalence, private-history
exposure or original-binary custody questions.

## Reproduce and review

From the full candidate checkout with current main incorporated:

```sh
python3 scripts/validate_jsp_successor_preservation.py --base origin/main
python3 tests/test_jsp_successor_preservation.py --base origin/main
```

The negative controls reject source deletion, altered source object, symlink
substitution, rewritten existing identity, duplicate identity, stale aggregate
count, backdated control date, unsafe shard path, duplicate shard, wrong identity
type, removed identity, missing new-identity source, alias collision, and rewritten
existing source attribution. Tests use in-memory overlays; they never damage the
checkout or original evidence.

Before considering any enforcement replacement: review the native results and
representative route, asset and urgent-repair cases; define which later changes
are accepted and how legitimate corrections are reviewed; retain historical
release validation and other substantive gates; obtain the required authority
for an enforcement change. This implementation deliberately grants no acceptance
for substantive changes to frozen JSP objects or replacement of existing identity
values. It is not a general permission to append new claims.

No main merge, deployment, branch deletion, external communication or historical
record rewrite is performed by this proposal. Public-safe review documentation
is repository/Pages-readable but is not linked into public reader navigation.

🟠 THREAD — preservation pending · required gate and evidence reconciliation remain open
