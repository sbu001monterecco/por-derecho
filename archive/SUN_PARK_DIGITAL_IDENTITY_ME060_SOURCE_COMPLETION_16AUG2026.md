# SUN PARK DIGITAL IDENTITY — ME-060 SOURCE COMPLETION

**Date:** 16 August 2026  
**Status:** controlled source-completion record  
**Scope:** evidence newly recovered from connected Gmail / Google Drive / preserved files for the 2021–2022 Google Business Profile requests and the subsequent Sun Park profile-state sequence; remaining provider/account-controller evidence is expressly identified below.

## Executive conclusion

ME-060 is **materially narrowed but not fully resolved**.

The connected corpus now closes four previously open sub-questions:

1. all three 2021–2022 Google Business request notices exist as direct authenticated Google-provider emails in connected Gmail;
2. the three request episodes share a stable provider-side Sun Park Business Profile reference, while each carries a distinct provider-side action token;
3. preserved Google management UI establishes that **all three requests were rejected**; and
4. native Google notifications and contemporaneous Google management captures establish a later profile-state sequence in which Sun Park was marked/permanently closed and was subsequently reported by Google support as appearing on Google Maps again.

The remaining gap is now narrower: **who actually controlled the requester Gmail account(s), who physically authenticated/submitted the requests, what authority documents were supplied, who or what caused the profile to become marked closed, and whether the 2019 `sunpark264@gmail.com` episode shares any controller or mechanism.** Those questions require provider audit/account records, native 2019 headers or lawful internal records not present in the currently connected corpus.

## 1. Direct authenticated Google request notices

### 28 October 2021

**VERIFIED FACT — native provider message.**

- Gmail message ID: `17cc5ff49854a87e`
- sender: `google-my-business-noreply@google.com`
- recipient: controlled Sun Park manager mailbox
- displayed requester: `Lourdes Castillejo`
- displayed role: `Business owner`
- displayed requester account: `mynd.hotels@gmail.com`
- raw message authentication reviewed: DKIM pass; SPF pass; DMARC pass; ARC pass
- provider header includes: `Arci=19740425` and `Rfc=12598848531223042920` under `MYBUSINESS_PAGE_ROLE_CHANGE_REQUEST`

A native `.eml` copy of this provider message is also preserved in the connected evidence set. Its SHA-256 and byte size are recorded in the evidence-vault manifest; the raw file is not copied into public GitHub because it contains unnecessary personal data.

### 24 February 2022

**VERIFIED FACT — native provider message, source-status upgraded from preserved-forwarded material.**

- Gmail message ID: `17f2d35f47943807`
- sender: `google-my-business-noreply@google.com`
- displayed requester: `Lourdes Castillejo`
- displayed role: `Employee`
- displayed requester account: `mynd.hotels@gmail.com`
- raw message authentication reviewed: DKIM pass; SPF pass; DMARC pass; ARC pass
- provider header includes: `Arci=24008448` and `Rfc=12598848531223042920`

### 20 June 2022

**VERIFIED FACT — native provider message, source-status upgraded from preserved material.**

- Gmail message ID: `1817ffc2d406461e`
- sender: `google-my-business-noreply@google.com`
- displayed requester: `MYND Hotels`
- displayed role: `Employee`
- displayed requester account: `mynd.hotels@gmail.com`
- raw message authentication reviewed: DKIM pass; SPF pass; DMARC pass; ARC pass
- provider header includes: `Arci=26176867` and `Rfc=12598848531223042920`

### Provider identifiers — controlled interpretation

The repeated `Rfc=12598848531223042920` across all three notices and Google's later support-dashboard link containing the same number strongly supports treating `12598848531223042920` as the stable **provider-side Sun Park Business Profile reference** in this evidence set.

The three distinct `Arci` values — `19740425`, `24008448`, `26176867` — are preserved as **provider-side request/action tokens**. Do not assign a more specific API or legal meaning to `Arci` without Google documentation.

## 2. Final disposition of all three requests

### 28 October 2021 — rejected

**VERIFIED FACT — Google management UI.**

The preserved Google management PDF records a post-rejection confirmation stating that Lourdes Castillejo would be notified that the request to manage Sun Park had been rejected. Google also warned that a rejected requester might later be permitted to seek verification after a waiting period.

**Controlled proposition:** the 28-Oct-2021 request was rejected. Rejection does not by itself prove that no later verification/access route was possible.

### 24 February 2022 — rejected

**VERIFIED FACT — Google management UI.**

The complete preserved PDF contains Google's post-action confirmation in Spanish that Lourdes Castillejo had been notified that the request to manage Sun Park was rejected.

**Controlled proposition:** the 24-Feb-2022 request was rejected. This does not establish who physically made the request or whether the displayed identity personally authorised it.

### 20 June 2022 — rejected

**VERIFIED FACT — Google management UI.**

The preserved Google management record states that the MYND Hotels request was rejected on Monday, 20 June 2022.

**Controlled proposition:** the 20-Jun-2022 request was rejected.

### Aggregate request outcome

**VERIFIED FACT:** all three documented 2021–2022 ownership/management requests in this source family were rejected by the then-existing Google Business Profile manager.

This materially narrows the earlier question “which permissions were obtained or rejected”: the reviewed request sequence does **not** show these three requests being approved. It does not exclude a different later verification, edit, public suggestion, API action, account compromise, manager action or other Google mechanism.

## 3. Profile-state sequence after the requests

### 22 June 2022 — Google says profile is marked closed

**VERIFIED FACT — native authenticated provider email.**

- Gmail message ID: `1818f3de654f86a0`
- sender: `googlemybusiness-noreply@google.com`
- raw authentication reviewed: DKIM/SPF/DMARC/ARC pass
- Google told the existing manager mailbox that `Sun Park, Playa Blanca, Lanzarote is marked as closed on Google` and invited the manager to state if the business was still open.

### 30 June 2022 — Google management view shows “Permanently closed”

**VERIFIED FACT — contemporaneous preserved Google management capture.**

A 30-Jun-2022 Google search/business-management capture shows:

- `You manage this Business Profile`;
- Sun Park at Calle Janubio 3;
- status `Permanently closed`;
- a management-side indication that Google was reviewing a suggestion that the place was open.

This proves the state shown by Google to the existing manager account at that time. It does **not** identify who or what caused the closed status.

### 15 July 2022 — repeated native “marked closed” notification

**VERIFIED FACT — native authenticated provider email.**

- Gmail message ID: `182036eda66944f2`
- sender: Google Business Profile no-reply
- raw authentication reviewed: DKIM/SPF/DMARC/ARC pass
- Google again notified the existing manager mailbox that Sun Park was marked closed.

A related preserved 16-Jul management capture also shows the profile in a permanently-closed state.

### 26 August 2022 — Google support reports profile visible on Maps

**VERIFIED FACT — native Google support email.**

- Gmail message ID: `182d9e260e14aa21`
- Google support case: `[5-5076000032482]`
- sender: `googlebusinessprofile-support@google.com`
- raw authentication reviewed: SPF/DKIM/DMARC pass
- Google support stated that it had checked the information on the profile and that the business then appeared on Google Maps.
- the support dashboard URL uses the same provider-side profile reference `12598848531223042920`.

**Controlled proposition:** by 26 Aug 2022 Google support represented that the profile appeared on Google Maps again after checking profile information. This is **not** a Google finding that any fraud, impersonation or unlawful interference allegation was true.

## 4. What this sequence proves — and what it does not

The recovered evidence now establishes a bounded platform sequence:

`28-Oct-2021 request → rejected`  
`24-Feb-2022 request → rejected`  
`20-Jun-2022 request → rejected`  
`22-Jun-2022 Google says profile marked closed`  
`30-Jun-2022 manager view shows Permanently closed / open suggestion under review`  
`15-Jul-2022 Google again says marked closed`  
`26-Aug-2022 Google support says profile appears on Maps`

It is **not** presently established that:

- Lourdes Castillejo physically submitted either request carrying her name;
- Lourdes controlled `mynd.hotels@gmail.com`;
- MYND, Canarian Hospitality, HNT or CAM caused the profile to be marked closed;
- any of the three rejected ownership requests caused the later closed status;
- the closed status arose from an ownership request rather than another Google edit/verification/public-suggestion/API/manager mechanism;
- the same person controlled `sunpark264@gmail.com` and `mynd.hotels@gmail.com`;
- Google found fraud or impersonation.

The contemporaneous February-2022 correspondence expressly considered the possibility that a third party may have used Lourdes Castillejo's name without her consent. That weakening/exculpatory possibility remains controlling until native account/controller evidence resolves it.

## 5. 2019 `sunpark264@gmail.com` source-completion result

The connected Gmail and Drive refresh located multiple preserved PDF/forwarded copies of the 6-Jun-2019 customer exchange and the Google recovery capture. It did **not** locate a native direct original from `sunpark264@gmail.com` with full RFC822 headers in the reviewed corpus.

The preserved exchange continues to support only that an account presenting as `SUN PARK <sunpark264@gmail.com>` communicated with a historical Sun Park customer concerning removal of belongings and forthcoming refurbishment.

CR-031 remains controlling: Google displayed only the masked recovery clue `ros••••••@aco••••••••.com`; the full mailbox, human controller and account-creation/recovery history remain unresolved.

## 6. Remaining ME-060 evidence gap — now provider/account-holder specific

The following items remain genuinely unavailable in the connected corpus and should not be represented as closed:

1. native RFC822/EML and full transport headers for the original 2019 `sunpark264@gmail.com` customer message;
2. the exact complete recovery address and recovery/change history for `sunpark264@gmail.com`;
3. creation, recovery, controller and session history for `mynd.hotels@gmail.com`;
4. submission/authentication IP, device, session and account identifiers for each Google Business request;
5. any title, authority, employment or ownership document supplied to Google with the requests;
6. Google Business audit/change-source history identifying the mechanism and actor/account that caused the `marked closed` / `Permanently closed` state;
7. whether any requester later completed verification through a route separate from the three rejected requests;
8. lawful internal account-administration, instruction and escalation records identifying the actual actors;
9. a native source for the separate alleged 2019 “business ceased” message family;
10. evidence proving or excluding a common controller/mechanism between the 2019 and 2021–2022 incidents.

**Status:** `PARTIAL — provider-side request provenance, request outcomes and profile-state sequence closed; controller/authorship/closure-causation evidence remains open.`

## 7. Private-source boundary

Native messages and PDFs contain personal telephone/customer/account information that is unnecessary for public publication. They remain in connected primary-source systems or the controlled working evidence environment. Public GitHub stores only the source locators, hashes, evidential classification and public-safe consequences.
