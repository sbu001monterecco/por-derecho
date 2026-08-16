# EVIDENCE MANIFEST — SUN PARK DIGITAL IDENTITY / GOOGLE PROVIDER RECORDS

**Date:** 16 August 2026  
**Purpose:** public-safe custody/index record for evidence recovered during ME-060 source completion. Raw private evidence is not copied into the public repository.

## Custody rule

The items below remain in connected Gmail / Google Drive / controlled working storage. Hashes refer to the exact local materialised copies reviewed in this source-completion pass. Personal telephone numbers, customer identities and other unnecessary private data are deliberately omitted here.

| Evidence ID | Source / date | Private locator | SHA-256 / size where materialised | Classification | Establishes | Does not establish |
|---|---|---|---|---|---|---|
| DIG-GOOG-20211028-NATIVE | Google My Business request notice, 28-Oct-2021 | Gmail `17cc5ff49854a87e`; native `.eml` attachment preserved in connected evidence | `.eml`: `3b58691afa51a247db91af44108f9d9ca7320aeba4f9233f943f7fe5a36c89b2`; 13,198 bytes | VERIFIED FACT / native provider | Google associated Lourdes Castillejo / `Business owner` / `mynd.hotels@gmail.com` with request; authenticated provider origin | physical submitter; Gmail controller; instruction; device/IP; personal authorisation |
| DIG-GOOG-20211028-OUTCOME | Google management request record, 28-Oct-2021 | connected Gmail/Drive attachment `Ownership Request of HOTEL SUN PARK by Mynd Hotels 28OCT2021.pdf` | `6832dfae29dbe7e5d2f8ecc5d013ce30d029b3b73684fb6912aa8932bfeb02f8`; 1,177,125 bytes | VERIFIED FACT / provider UI | request was rejected; Google displayed post-rejection notification consequence | who submitted request; whether a later separate verification route occurred |
| DIG-GOOG-20220224-NATIVE | Google My Business request notice, 24-Feb-2022 | Gmail `17f2d35f47943807` | raw MIME reviewed in connector; not republished | VERIFIED FACT / native provider | Lourdes Castillejo / `Employee` / `mynd.hotels@gmail.com`; DKIM/SPF/DMARC/ARC pass; provider action token | physical submitter/controller/instruction/authority |
| DIG-GOOG-20220224-OUTCOME | Google management request record, 24-Feb-2022 | connected attachment `Ownership Request of HOTEL SUN PARK by Mynd Hotels 24FEB2022.pdf` | `9f923a9582c9f9a0c8cd33ca2087768478b03b68753b8ce0f9d9ec65d0a3630a`; 6,039,997 bytes | VERIFIED FACT / provider UI | request rejected; Google displayed confirmation that Lourdes was notified | physical actor; later separate verification |
| DIG-GOOG-20220620-NATIVE | Google request notice, 20-Jun-2022 | Gmail `1817ffc2d406461e` | raw MIME reviewed in connector; not republished | VERIFIED FACT / native provider | `MYND Hotels, Employee` / `mynd.hotels@gmail.com`; authenticated provider origin | physical submitter/controller/instruction/authority |
| DIG-GOOG-20220620-OUTCOME | Google management request record, 20-Jun-2022 | connected attachment `Ownership Request of HOTEL SUN PARK by Mynd Hotels 20JUN2022.pdf` | `859b30e24231fcacf297eb264623660743a2133759b0131798445e11c9311e28`; 882,693 bytes | VERIFIED FACT / provider UI | request shown as rejected on 20-Jun-2022 | causal link to later profile state; physical actor |
| DIG-SUNPARK264-20190606-CUSTOMER | preserved customer exchange involving `SUN PARK <sunpark264@gmail.com>` | connected attachment / Drive `Customer email ref SUN PARK email from CAM - 06JUN2019.pdf` | `9fc9feacbe0985224742b64a75c69d312c2fe9c4fd4949eb4df3775613e24620`; 697,842 bytes | SOURCE-SUPPORTED PRESERVED COPY | account presented as SUN PARK and communicated with historical customer about belongings/refurbishment | account creator/controller, transport headers, physical sender, legal authority |
| DIG-GOOG-20220630-STATE | contemporaneous Google Business/Search capture, 30-Jun-2022, contained in 8-Aug dossier | connected attachment `Hotel Sun Park IP and Business cyberattack by CAM-CanarianHospitality-MyndHotels-MyndYaiza 08AUG2022.pdf` | `3acf4f2b254a41e47070792561939ded2f83adfac378eda4f5f2ce0ecb978910`; 8,036,844 bytes | VERIFIED PLATFORM STATE / preserved provider UI | `You manage this Business Profile`; Sun Park shown `Permanently closed`; open suggestion under review | who caused state; whether any rejected requester caused it |
| DIG-GOOG-20220716-STATE | preserved Google profile-management sequence, Jul-2022 | connected attachment `SPL Google Business Profile 16JUL2022 - CAM Fraud 08AUG2022.pdf` | `3fec688cafa7d46378d69f8ba53eba29dc65d5249c13ace8a96613054aa1e884`; 6,532,972 bytes | VERIFIED PLATFORM STATE / preserved provider UI | management interface and permanently-closed state; provider closed-status correspondence preserved | actor or mechanism causing the state |
| DIG-GOOG-20220622-CLOSED | native Google Business Profile closed-status notification, 22-Jun-2022 | Gmail `1818f3de654f86a0` | raw MIME reviewed in connector | VERIFIED FACT / native provider | Google notified existing manager mailbox that Sun Park was marked closed | cause/actor of closure |
| DIG-GOOG-20220715-CLOSED | native Google Business Profile closed-status notification, 15-Jul-2022 | Gmail `182036eda66944f2` | raw MIME reviewed in connector | VERIFIED FACT / native provider | Google again notified existing manager mailbox that Sun Park was marked closed | cause/actor of closure |
| DIG-GOOG-20220826-SUPPORT | Google Business Profile support response, 26-Aug-2022 | Gmail `182d9e260e14aa21`; support case `[5-5076000032482]` | raw MIME reviewed in connector | VERIFIED FACT / native provider support | Google said profile information had been checked and business then appeared on Google Maps; dashboard carries profile reference `12598848531223042920` | truth of user's allegations; fraud/impersonation finding; identity of actor who caused prior state |

## Provider-side identifiers preserved

Across the three native request notices:

- stable repeated profile reference: `Rfc=12598848531223042920`;
- 28-Oct-2021 action token: `Arci=19740425`;
- 24-Feb-2022 action token: `Arci=24008448`;
- 20-Jun-2022 action token: `Arci=26176867`.

The same `12598848531223042920` appears in Google's later support dashboard URL. It is therefore safe within this record to call it the **provider-side Sun Park Business Profile reference**. The exact formal semantics of `Arci` are not independently documented and should remain described as provider-side request/action tokens.

## Privacy / admissibility limitation

This manifest is a custody and source-control aid, not an expert forensic report and not a substitute for provider certification. Where court-grade authenticity or actor attribution is required, preserve/export the native evidence lawfully and obtain Google/provider records or expert verification as appropriate.
