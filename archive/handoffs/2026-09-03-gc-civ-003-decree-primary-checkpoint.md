# GC-CIV-003 — primary closure-decree recovery checkpoint — 03 Sep 2026

**Workspace:** `PD-WS-20260902-0001`  
**Handoff:** `PD-WCH-20260903-GCCIV003-SRC-004`  
**Repository:** `sbu001monterecco/por-derecho`  
**Historic docket:** `OPEN_NOT_CERTIFIED_COMPLETE`  
**Base main for this source-recovery branch:** `08b2c9efeec59ce1b4009377b0f84de3cd138d8c`  
**Branch:** `codex/gc-civ-003-decree-closure-primary-20260903`

## 1. Do not restart

Continue from this checkpoint, the controlling machine source state and the immutable PR #1373 release checkpoint. Do not repeat broad Gmail/Drive discovery. Continue only explicit remaining source gaps.

Locked proceeding identity remains:

- `GC-CIV-003` — Diligencias Preliminares 1041/2017;
- NIG `3501642120170028407`;
- IUP `LR2017147858`;
- Juzgado de Primera Instancia nº 2 de Las Palmas de Gran Canaria — `PD-SP-I-0048`;
- Juan Avello Formoso — `PD-SP-P-0124`;
- Fernando Pérez Polo — `PD-SP-P-0165`.

Deprecated duplicate `LZ-CIV-050` remains `REMOVED_DO_NOT_RECREATE`.

## 2. Immutable historic release checkpoint

Do not mutate the PR #1373 historical release manifests:

- PR #1373 merge `efbb1032b0c5e21ca892b3a9db17b3f7b4073e6c`;
- tree `1e2295ccc94d3e020b2ef0db59924d439de2aa93`;
- Pages `33697357002 / #1420` success;
- Chromium `33700567926 / #1` success.

Post-release source work already completed before this checkpoint:

- PR #1377 merge `ddebffb07f4750ab4ab19017a3aef5a195c45f70` — primary 19-Dec Auto / 23-Jan service chain / CAM opposition source refinement;
- Pages `33708727660 / #1424` success;
- hosted Chromium `33709044855 / #1` success;
- PR #1378 continuity closeout merge `08b2c9efeec59ce1b4009377b0f84de3cd138d8c`.

## 3. Major new primary source — Decreto 000139/2018 recovered

A targeted Gmail attachment search against the exact case number surfaced the authentic standalone court act:

`Decreto DP 1041-2017 LBP-CAM 5MAR2018.pdf`

Source-safe lock:

- SHA-256 `4f8fff28bb5239895ab3c64ff9650ec5ffa2750cc401841c5a1274948301503c`;
- bytes `316520`;
- source class `PRIMARY_AUTHENTIC_ELECTRONIC_JUDICIAL_ACT`.

The decree is dated **5 March 2018**, resolution **Decreto 000139/2018**, and is electronically signed by LAJ Fernando Pérez Polo on **6 March 2018 at 09:51:31**.

### Proven by the decree

The decree expressly records that:

1. **LUCHY PLAYA BLANCA S.L.U. requested desistimiento of the proceeding.**
2. The request was transferred to the opposing party.
3. **Construcciones Acosta Matos, S.A. did not oppose and expressed conformity** by a filing dated **25 February 2018**, registry **1222/18**.
4. The LAJ applies **article 20.3, second paragraph, LEC**.
5. LPB is treated as desisting from continuation of Diligencias Preliminares `0001041/2017`.
6. The proceeding is ordered **sobreseído**.
7. The hearing then scheduled for **25 April 2018 at 11:15** is suspended.

### Critical authorship boundary

The decree proves the requesting **party** was LPB. It does **not** prove who drafted, signed or physically presented the underlying desistimiento filing.

The decree header shows Francisco Borja Rodríguez-Batllori Laffitte as claimant lawyer metadata and Alejandro Valido Farray as claimant procurador metadata. Those metadata do not establish individual authorship/signature of the desistimiento filing. Preserve the original filing as a source gap until recovered.

### Review / finality boundary

The decree itself provides a **five-day recurso de revisión** route and the EUR 25 deposit rule. Do not infer immediate finality, service date, expiry of the review period or exact finality date from the decree alone.

The operative paragraph contains wording `frente a LUCHY PLAYA BLANCA S.L.U.` although the header identifies CAM as defendant. Preserve the textual anomaly; do not silently correct it.

## 4. Primary 13-May-2024 archive-status order recovered

Source:

`DIOR DP 1041-2017 LPB-CAM 13MAY2024.pdf`

Source-safe lock:

- SHA-256 `87190775e0b8de91323e1d4901d5f1d78a634ee466dcc8e22a32913b4e79cbf2`;
- bytes `402540`.

The signed Diligencia de Ordenación of 13 May 2024, Fernando Pérez Polo, records a 10-May-2024 filing by procuradora María Luisa Díaz Vecino for Aweswell Limited and expressly states that GC-CIV-003 is **`finalizado y archivado por desistimiento de la parte demandante`**, agreed by decree of 5 March 2018, with no proceedings derived from this case and the file to be returned to the judicial archive.

This confirms finalised/archive status **as of 13-May-2024**. It does not establish the exact 2018 service date or exact date Decreto 000139/2018 became unchallengeable.

## 5. CAM opposition date now locked by the primary filing

Primary source:

`DP 250118 1 Retracto Oposicion de CAM.pdf`

Source-safe lock:

- SHA-256 `02e2efcb55333f647225f1a81e27728f371214e78091f6968f18e84435dd5efc`;
- bytes `706239`.

The filing itself is dated **24 January 2018** in Las Palmas de Gran Canaria. It is presented by procurador Gerardo Pérez Almeida under the legal direction of Carmen Ramírez de Prada, states CAM was notified on 18 January 2018, formally appears and formulates opposition under article 260.1 LEC, and asks for the requested preliminary diligences to be set aside with costs.

The prior source-family-only date state is superseded: the filing date is now primary-source locked to 24-Jan-2018.

## 6. CAM opposition exhibit — 2017 assignment-notification package

Primary exhibit source:

`DP 250118 2 Retracto Notificacion de CAM a LPB.pdf`

Source-safe lock:

- SHA-256 `8f11764548d458286de1aff04fe5ff08f00eb847a8960eab4dad8af4456dfdc3`;
- bytes `433878`.

Visual inspection of the seven-page scanned exhibit shows the notarised/registered-mail notification package relied upon in CAM's opposition. It includes the 20-Oct-2017 credit-assignment notification and the notarial/courier record which states delivery to LPB on **27 October 2017**. The attached assignment notice bears signatures for Construcciones Acosta Matos, S.A. (Laura Patricia Acosta Matos) and Promontoria Holding 122, B.V. (María Montserrat Álvarez González).

This exhibit is registered as evidence supporting CAM's opposition proposition about prior assignment notice. It is not treated as a judicial finding beyond what the opposition/decree themselves establish.

## 7. Contemporaneous AC communications

Two recovered communication sources are now source-safe registered:

### 18-Jan-2018

`Email AC-EquipoLegalLPB 29ENE2018.pdf`

- SHA-256 `5a818ef1114862f5d66ac52447eb2c43fe81ce7324634ecd9c02d738ee1d5c07`;
- bytes `90353`.

The reproduced original email is dated 18-Jan-2018 and states the AC's position that, following liquidation, LPB's representation falls to the AC; it requires lawyers not to act for LPB without express authorisation and requests a proceedings/invoice list.

### 25-Jan-2018

`DOCUMENTO Nº3 Email AC-CPS 25ENE2018.pdf`

- SHA-256 `765d78946b9d4d521eb3450ee219a5bf6d4f9d6db3e2431ea47ef666207752bd`;
- bytes `689930`.

It expressly identifies DP 1041/2017 and instructs that no further action/presentation for LPB occur without the AC's express consent.

These communications prove their own contents and chronology only. They do not establish who authored/signed the later desistimiento filing and do not by themselves establish misconduct.

## 8. Refined source-gap state

### Closed / primary verified

1. 19-Dec-2017 admission Auto.
2. Finality of that Auto only.
3. Positive CAM citation/requerimiento on 18-Jan-2018.
4. CAM appearance/opposition; filing date now locked to 24-Jan-2018.
5. Standalone Decreto 000139/2018 dated 5-Mar-2018.
6. LPB as the party requesting desistimiento.
7. CAM no-opposition/conformity dated 25-Feb-2018, registry 1222/18, as recorded by the primary decree.
8. Article 20.3 LEC as the procedural basis stated in the decree.
9. Sobreseimiento and suspension of the hearing then fixed for 25-Apr-2018 at 11:15.
10. Proceeding finalised/archive status as of 13-May-2024, confirmed by primary LAJ order.

### Still open / targeted

1. Complete docket / certified index.
2. What actually happened on 19-Feb-2018 and the intervening procedural/rescheduling act that produced the later 25-Apr hearing date.
3. Original LPB desistimiento filing: exact filing date, author/signatory/representative and full text.
4. Original CAM conformity/no-opposition filing dated 25-Feb-2018, registry 1222/18.
5. Service/notification of Decreto 000139/2018.
6. Exact date/source establishing expiry/non-use of the five-day revision route and resulting finality of Decreto 000139/2018.

## 9. Targeted recovery result

Exact-target searches for `1222/18`, the 25-Apr-2018 date, `desistimiento + 1041/2017`, and the February/March 2018 Gmail window did **not** surface the original desistimiento or CAM conformity filing. Drive exact-target searches likewise did not produce a primary original filing. Preserve those as explicit source gaps.

No broad discovery was run.

## 10. Repository source state staged on this branch

The branch already updates:

- `assets/data/gc-civ-003-primary-source-state-20260903.json`;
- `archive/GC_CIV_003_PRIMARY_ACTS_SOURCE_REGISTER_03SEP2026.md`;
- `es/procedimientos/gc-civ-003/index.html`;
- `en/proceedings/gc-civ-003/index.html`.

The older 02-Sep Master CSV wording is a historical stale projection and must not control source-gap interpretation over this dated primary-source overlay. Do not wholesale-rewrite the Master CSV through an unsafe connector operation; ingest this overlay in the next deterministic Master rebuild.

## 11. Next operational step

Publish this source correction through a fresh governed PR from the branch after:

1. advancing `CURRENT_WORKSPACE_HANDOFF.md` to SRC-004;
2. updating the workspace/action ledger to the refined gap state;
3. running all path-triggered validators;
4. merging with expected-head safety if green;
5. verifying Pages from the exact merge SHA;
6. running hosted Chromium against the updated ES/EN pages, source JSON, homepage search and `LZ-CIV-050` negative surfaces.

After publication, continue only the six remaining targeted gaps above.
