# Cuatrecasas outbound-control incident — continuity, preservation and traceability audit

**Control date:** 1 October 2026  
**Control ID:** `PD-CUA-COMMS-AUDIT-20261001-01`  
**Matter:** AWESWELL LIMITED / Sun Park / Cuatrecasas institutional escalation  
**Event date:** 30 September 2026  
**Status:** `SENT EVENT PRESERVED / NO CORRECTIVE EMAIL AUTHORISED / CONTROL REMEDIATION REQUIRED`

## 1. Purpose and boundary

This record preserves the control state of the 30-Sep-2026 Cuatrecasas protected-reporting / institutional-escalation email after a post-send audit found that substantive evidential review was materially stronger than the package's canonical outbound-control instantiation.

This audit does **not** authorise a correction, resend, supplement, forward or follow-up. The sent email remains an immutable historical event. Any future transmission requires a fresh exact package and fresh authorization under `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md`.

Private Gmail addresses, native message IDs, private bodies and restricted attachment locators remain outside the public repository.

## 2. Traffic-light summary

### GREEN — preserved / independently recoverable

- The Cuatrecasas public narrative and May–June 2020 bridge are source-controlled in GitHub.
- PR #2044 merged the 2014–2026 knowledge/governance strengthening.
- PR #2054 merged the May–June 2020 withdrawal → internal check → Claims & Collection bridge.
- The controlled PDF family is recoverable from the private mailbox / file-custody layer.
- The native sent event is recoverable from connected Gmail and was read back after transmission.
- The sent package contained the protected-reporting / anti-retaliation discussion including Spain Ley 2/2023 Article 36.2 and qualified EU/German/UK references.
- The send was one transmission, not an automatic resend/correction.
- No corrective email is authorised by this audit.

### AMBER — preserved but not canonically closed

- The final sent package had no repository-persisted `COMMUNICATION_ID` / controlling-version object before send.
- No repository-persisted Attachment Manifest tied the exact sent PDF version to a canonical communication object.
- No repository-persisted Link Manifest tied the exact four GitHub Pages URLs to the sent object.
- No machine-readable source-cutoff / readiness record was persisted before send.
- The final eight-recipient package did not have a formally recorded pagination-complete person-and-organisation Gmail-history gate after the last material protected-reporting/PDF revision.
- The final PDF contained two repository-commit references from successive build stages: the earlier PR #2044 merge and the later PR #2054 June-2020 bridge merge. Both are real historical commits, but the pack did not clearly distinguish `BASELINE_COMMIT` from `CONTROLLING_CONTENT_COMMIT`.
- GitLab MR !743 contained materially aligned Cuatrecasas page work but GitLab publication remained separately blocked by fail-closed repository controls.

### RED — rule breach / future hard-stop condition

- The material former-professional email contained GitHub Pages links only. `PD-FCCOM-MIRROR-CYBER-20260926-01` requires both GitHub Pages and GitLab Pages public links, with both live-read before send. Because GitLab Pages was not live-verified, the package should not have been marked send-ready under that rule absent an exact user-approved exception.
- The email used controlled entities without consistently applying the required first-reference forms from `ops/CANONICAL_ENTITY_NAMES.json`: notably `Luchy Playa Blanca, S.L.U. (LPB)` and `Matkator, S.L.U.`.
- The outbound rules said `COMMUNICATION_ID` should be maintained "where practical" in one protocol while the campaign layer said every important outbound package "must" have one. That wording divergence allowed a mandatory control to be treated as optional.
- There was no single fail-closed validator that joined: canonical-name gate + dual-mirror gate + Gmail-history gate + communication-object/manifest gate + exact-draft authorization gate.

## 3. Root cause

The failure was not absence of rules. The repository already contained most of the required controls.

The operational failure was **rule fragmentation without one executable pre-send admission object**:

1. substantive Cuatrecasas evidence work was performed in the matter pages;
2. email authorization was controlled in a separate send rule;
3. canonical names lived in a machine register;
4. dual-public-mirror requirements lived in a 26-Sep former-professional overlay;
5. Gmail-history completeness lived in another hard gate;
6. attachment/link manifests lived in the general outbound protocol;
7. no single validator required all seven states to be `PASS` before a package could be labelled `READY FOR AUTHORIZATION`.

The assistant therefore optimised the evidential package and native Gmail readback but failed to instantiate and validate the package as a canonical outbound communication object.

## 4. Sent-package audit — omissions

1. Missing persisted `COMMUNICATION_ID`.
2. Missing persisted controlling version.
3. Missing persisted source cutoff.
4. Missing persisted Attachment Manifest.
5. Missing persisted Link Manifest.
6. Missing persisted final dual Gmail-history gate record.
7. Missing GitLab public-mirror links required by the former-professional overlay.
8. Missing explicit distinction between the PR #2044 baseline merge and PR #2054 controlling content merge in the final PDF.
9. Missing controlled first-reference forms for LPB and Matkator.
10. Missing pre-send registration of the final PDF hash/size/page count against the communication object.
11. Missing pre-send registration of the exact approved Gmail draft against the communication object.
12. Missing immediate post-send backfill into the canonical institutional-communications register.

## 5. Sent-package audit — commissions / risks

1. **Dual-mirror commission:** the email affirmatively presented four GitHub Pages routes as the principal public source-controlled pages while the standing former-professional rule required dual GitHub/GitLab redundancy.
2. **Canonical-commit ambiguity:** the PDF presented two real commit values without a clear baseline-vs-controlling distinction.
3. **Canonical-name commission:** first mentions of LPB / Matkator did not consistently use the controlled first-reference forms.
4. **Readiness overstatement:** the package was described as `GREEN / ready to send` despite the missing formal history-gate record and blocked GitLab mirror.
5. **Traceability overstatement risk:** saying the pack was "canonical" was stronger than the control record supported because the communication object and manifests had not been persisted.

## 6. What was done correctly

- The 2020 withdrawal was preserved as contrary/contextual evidence.
- The June-2020 Claims & Collection bridge was bounded and did not convert routing into a finding of wrongdoing.
- The 2021 RICPE/CNMV notice was protected by a temporal firewall.
- Silence/non-response was not treated as admission.
- PwC / RSM / Grant Thornton context was not used to transfer knowledge or liability.
- Article 36.2 / anti-retaliation language asked for independent review rather than declaring partner conduct retaliatory.
- The user gave fresh explicit authorization to send once.
- The exact draft was sent once and native sent-copy readback was performed.
- No automatic corrective email is authorised now.

## 7. Mandatory remediation — future rule

No material external email may be labelled `READY FOR AUTHORIZATION` unless one machine-readable **Canonical Outbound Communication Object (COCO)** exists and passes all gates:

`COMMUNICATION_ID`
→ `CONTROLLING_VERSION`
→ `SOURCE_CUTOFF`
→ `CANONICAL_NAME_GATE`
→ `PERSON_GMAIL_HISTORY_GATE`
→ `ORGANISATION_GMAIL_HISTORY_GATE`
→ `PAGINATION_EXHAUSTED`
→ `ATTACHMENT_MANIFEST`
→ `LINK_MANIFEST`
→ `PUBLIC_MIRROR_GATE`
→ `DRAFT_READBACK`
→ `EXACT_USER_AUTHORIZATION`
→ `SEND_ONCE`
→ `NATIVE_SENT_READBACK`
→ `REGISTER_BACKFILL`.

Any missing field = `BLOCKED`.

For a former-professional email, `PUBLIC_MIRROR_GATE` requires:
- GitHub Pages live-read = PASS;
- GitLab Pages live-read = PASS;
- material parity = PASS;
- or an exact user-approved one-use exception naming the missing mirror and exact transmission.

A blocked mirror is not silently omitted.

## 8. Canonical naming hard stop

Before an outbound package is presented:
- resolve every controlled person/entity against `ops/CANONICAL_ENTITY_NAMES.json`;
- use the controlled first-reference form on first narrative mention;
- preserve source literals only when labelled;
- reject forbidden aliases;
- emit a machine-readable list of every controlled entity used and the resolved record ID.

For this matter the required forms include:
- `AWESWELL LIMITED`;
- `Luchy Playa Blanca, S.L.U. (LPB)`;
- `Matkator, S.L.U.`.

## 9. Commit/reference rule

Every generated evidential PDF must carry:
- `BASELINE_REPOSITORY_COMMIT` if relevant;
- `CONTROLLING_CONTENT_COMMIT`;
- build timestamp;
- source cutoff;
- PDF SHA-256;
- page count;
- Attachment Manifest ID;
- Communication ID.

A later source-control change invalidates an earlier `CONTROLLING_CONTENT_COMMIT` label. Historical commits may remain only with explicit roles.

## 10. No-resend rule

This audit creates **no authority** to send a correction or supplement to Cuatrecasas.

The current remedy is internal:
- preserve the native sent event;
- preserve this audit;
- harden the rules;
- register the event in the canonical communications ledger;
- monitor for responses;
- apply corrected controls to the next independently authorised communication.

## 11. Successor-thread handoff

A successor thread must begin by reading:
1. this audit;
2. `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md`;
3. `archive/OUTBOUND_EMAIL_COMMUNICATIONS_PROTOCOL_23AUG2026.md`;
4. `archive/PRE_SEND_GMAIL_PERSON_OUTLET_HISTORY_GATE_23AUG2026.md`;
5. `governance/FORMER_COUNSEL_PUBLIC_MIRROR_CYBER_RESILIENCE_EMAIL_RULE_26SEP2026.md`;
6. `ops/CANONICAL_ENTITY_NAMES.json`;
7. current Cuatrecasas pages and latest merged commit;
8. the private native sent-message record.

Do not reconstruct the sent event from chat memory where native Gmail evidence is available.
