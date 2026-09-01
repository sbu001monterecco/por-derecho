# PR #1324 supersession map — DP 748 / La Laguna judicial register

Date: 1 September 2026

PR #1324 was created before PR #1326 canonised the La Laguna judicial identity denominator. It must not be merged wholesale because its separate DP 748 institution shard would duplicate the now-canonical `PD-SP-I-0037` registration architecture.

Its unique source-controlled content is preserved as follows:

| #1324 source | Canonical destination |
|---|---|
| `archive/DP748_2026_MASTER_CAEPR_INTERLINK_CLOSEOUT_01SEP2026.md` | `archive/LA_LAGUNA_JUDICIAL_REGISTER_GAP_CLOSURE_01SEP2026.md` + `assets/data/dp748-2026-canonical-interlink-control-v1.json` |
| `assets/data/counsel-filing-register-v1.json` | same canonical register; Carlos Llamas DP 748 filings added with public-safe source IDs |
| `assets/data/counsel-procurador-gap-register-v1.json` | same canonical register; `CP-GAP-012`–`015` preserved |
| `assets/data/counsel-procurador-perimeter-register-v1.json` | same canonical register; Carlos/Adriana DP 748 pairing preserved |
| `assets/data/dp748-2026-canonical-interlink-control-v1.json` | recreated on current canonical main; inherits #1326 judicial IDs |
| `assets/data/matter-identity-registry-v1.dp748-institution.json` | **not duplicated**; aliases folded into `matter-identity-registry-v1.la-laguna-judicial-institutions.json` under `PD-SP-I-0037` |
| `assets/data/matter-identity-registry-v1.json` | root reconciled to the current shards and reserved `PD-SP-P-0146` |
| `assets/data/matter-identity-registry-v1.professional-people.json` | reserved `PD-SP-P-0146` Carlos Llamas Sanz promoted |
| `assets/data/procurador-master-register-v1.json` | Adriana Hernández Díaz's DP 748 party/lawyer/proceeding-period lineage added without transferring it to ETJ 163/2020 |

After the successor release merges, #1324 is safe to close as superseded with provenance rather than merge.
