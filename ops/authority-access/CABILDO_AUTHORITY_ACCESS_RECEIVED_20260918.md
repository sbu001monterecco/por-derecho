# Cabildo authority-access evidence received — 18 September 2026

**Status:** GitHub outage-continuity control; canonical GitLab reconciliation pending.  
**GitHub authoring base:** `e79d4233b172d45baf27964e8a5165447fe3b0c1`  
**Canonical repository:** GitLab project `86151898` remains canonical once authenticated access is restored.

## 1. New grant acquired

Cabildo Insular de Lanzarote expediente **13811/2026**, **Decreto 2026-6999 of 17 September 2026**, granted access to the payloads for **498/2020, 547/2020 and 21219/2021**. The authority-stated access window ends at **23:00 on 31 October 2026**; the authority statement does not specify a timezone.

The connected authority folder listed three top-level archive payloads. All three were acquired and ZIP-integrity checked:

| Archive | Bytes | SHA-256 |
|---|---:|---|
| `547_2020.zip` | 3,991,616 | `fcf38f0c8eb9583f0664ac8dd5f77af65839074b31e50254def7cc82fc31feb7` |
| `498_2020.zip` | 2,470,591 | `f29b1b4825e06f25c20b5cd8a102906cf566a121074f9dbff848a7a599964fe8` |
| `21219_2021.zip` | 3,510,958 | `cdcbdf39d4a29ab2022b5ef82c749a46377e295c6626106a1c760353d32a8fd4` |

The signed grant resolution is preserved in private custody with SHA-256 `4461a9ea6693d9077c6bddc6cb7393bc4477af8548fd7eb1cc2a1df23860cc6e`.

## 2. Digitisation and deduplication

The three granted archives contain **37 PDFs / 51 pages**. **32 originals were already searchable**. The **5 image-only originals remain unchanged** and have separate searchable OCR derivatives. No source PDF was replaced.

Analytical deduplication identified **5 exact duplicate groups** plus **1 normalized-text-equivalent pair**. Every native copy is retained. Duplicate analysis is not evidence deletion.

## 3. Public-safe evidential chronology

The public-safe reading is deliberately attributed to the disclosed file, not promoted into a title or liability finding:

- **13 January 2020:** a disclosed technical report states that, on consultation of the establishment file, Matkator did not appear among the hotel owners recorded in that administrative file.
- **22 January 2020:** a follow-on requirement invokes that file position and requests ownership/representation substantiation before processing.
- **27–28 January 2020:** the 547/2020 transparency chain requests the competent tourism-area report/file, including anonymisation where applicable.
- **10–12 February 2020:** the received report is transmitted through the transparency chain.
- **30 November 2021 onward:** 21219/2021 seeks current tourism-authorisation/status information; the disclosed response refers back to the earlier ownership/representation issue and separates tourism-inspection from works-inspection competences.
- **17 September 2026:** Decreto 2026-6999 grants access to the three raw expediente payloads above.

These records show what the administrative files contained and how the access chain moved. They do **not** by themselves decide civil title, criminal responsibility, the truth of every assertion inside the files, or the legal effect of any private representation.

## 4. Decreto 2026-7000 and transparency-commissioner receipt

Cabildo expediente **13817/2026**, **Decreto 2026-7000 of 17 September 2026**, is preserved with SHA-256 `0f26efcd7bebc935fb8a8e093aa4ea7906ff28025661010c3a77500f3edec44e`.

On **18 September 2026**, the Comisionado de Transparencia y Acceso a la Información Pública de Canarias recorded the complaint package concerning that decision under incoming register **2612/2026**. The certificate records presentation at **00:39** and entry at **09:48**, and identifies the principal complaint plus four annexes. The native certificate is searchable and preserved privately with SHA-256 `5fdf8cfc70d86286123707bf38fa6f57ef923a09c01f5fe4bddc7b2200dd845f`.

That receipt proves registration of the package. It does not prove merits admission, a separate appeal-file number, outcome, or acceptance of the complaint's propositions.

## 5. 3671/2022 — correct current status

The 17 September 13811/2026 grant is a **three-file grant** and should not be rewritten as a fresh 3671/2022 production. Separately, project custody records the earlier April 2026 six-ZIP disclosure including `3671_2022.zip`.

The current open custody issue is technical: the intact connected-source `3671_2022.zip` is **356,624,754 bytes**, above the connected raw-download limit used in the acquisition pass, so a verified SHA-256 of that intact native ZIP is still pending. A structurally corrupt tablet-uploaded copy is expressly excluded from evidential authority. This custody limitation must not be misstated as non-disclosure of the April file.

## 6. Event / CAEPR / communications treatment

The validated **1 September 2026** institutional-communications census remains frozen at its controlled 19-event denominator. It is **not rewritten** merely to force new material into an old checkpoint.

This update instead uses the post-checkpoint supplement in `assets/data/cabildo-authority-access-received-20260918.json`, linked to existing Cabildo event **PD-SP-EVT-0154**. Cabildo remains **PD-SP-I-0010 / CABILDO_DE_LANZAROTE**. The Canary Transparency Commissioner has a stable institution key, **CANARY_TRANSPARENCY_COMMISSIONER**, but no confirmed CAEPR institution ID in the present GitHub control; no ID is invented.

## 7. Privacy and publication boundary

The transparency grant is authority to **access** the material. It is not treated as blanket authority to republish personal-data-bearing scans. Raw archive PDFs and the registry certificate remain out of public Git unless a contextual privacy/publication review authorises a public derivative.

The two existing AEAT 16 September controls are reused rather than duplicated:
- `archive/AEAT_TRANSPARENCY_RESOLUTIONS_16SEP2026.md`
- `assets/data/aeat-transparency-resolutions-20260916.json`

No evidence has been mass-sent to third parties.

## 8. GitLab handback gate

When authenticated GitLab access returns:

1. fetch then-current GitLab `main`, relevant open MRs, pipelines and current evidence/event/CAEPR/communications controls;
2. compare this GitHub outage delta path-by-path against newer canonical work;
3. integrate only missing or better-supported material into the **existing** canonical controls and dedicated authority-evidence-received page;
4. preserve the private/public boundary and all native hashes;
5. record the exact GitHub source commit, GitLab destination commit/MR and parity/disposition result;
6. do not force-reset either side or recreate unavailable GitLab-native state from memory.
