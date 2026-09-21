# Institutional communications reconciliation runbook — 31 August 2026

**Control:** Ministerio Fiscal / Fiscalía communications, with E.G. 745/2026 as the focused control case.
**Purpose:** stop future threads from rescanning already-reconciled mail and receipt bundles, while preserving the difference between sending, registration, delivery, internal association, examination and merits.

## 1. Canonical layers

| Layer | Canonical path | Function | Public/private rule |
|---|---|---|---|
| Public event register | `assets/data/institutional-communications-register-v1.json` | Stable event IDs, official references, controlled subject categories/digests, source anchors and evidence-state boundaries | Public-safe only |
| Public-safe mailbox index | `assets/data/institutional-communications-mailbox-index-v1.json` | One row for each of the 156 located native mailbox events, retaining only time, controlled direction/state/route, safe references, subject digest/category, attachment count, match key and proof ceiling | Public-safe derivative; no locator/address/subject/name |
| Scan checkpoint | `ops/INSTITUTIONAL_COMMUNICATIONS_SCAN_CHECKPOINT.json` | Covered date window, pagination state, source hashes and next overlap window | No provider IDs or private locators |
| Private-to-public sanitizer | `scripts/build_public_mailbox_event_index.py` | Locally derives the public-safe 156-row mailbox index from the exact controlled private snapshot; its input path is always supplied explicitly and is never committed | Fails on source-hash/count drift and forbidden output fields |
| Deterministic reconciler | `scripts/reconcile_institutional_communications.py` | Rebuilds the register and checkpoint from the 75-row receipt baseline, the public-safe mailbox index and reviewed act/notice constants | Reads only public repository inputs |
| Private custody map | Opaque reference `PD-SP-CUST-0001` | Maps private source locators/fingerprints to public event IDs outside Git | `PERSISTED_PRIVATE_CUSTODY`; 231 rows; SHA-256 `bdd12a8fa62b5058525e1c37053fb7899ac24a60d12ff48ab8b74bda617cd6f6`; no storage/provider identifier is public |

The ID namespace is the already-declared `EVENT` extension in `.github/evidence-intelligence/id-extension-policy.json`: `^PD-SP-EVT-[0-9]{4}$`. The validator checks the policy, every event ID and every source-proved signatory person ID.

## 2. Controlled denominator

- The canonical RedSARA short index has exactly **75 detailed receipt rows**, **75 unique REGAGE references** and **126 annex listings**.
- The wider controlled aggregate reports **97** RedSARA/AGE records: **90 received** and **7 rejected**.
- The remaining **22** metadata-only records are represented by exactly one unresolved batch: **15 aggregate-received + 7 aggregate-rejected**, with no individual status allocation.
- Never create 22 apparent event rows from that aggregate. Individual rows require an individual receipt/status source.
- The persisted private native-locator snapshot has exactly **231 rows**: **75** baseline REG-AGE receipt rows plus **156** unique mailbox events.
- All **156/156** mailbox events now have public-safe transport rows: **42 outbound**, **101 inbound**, **10 self-archive controls**, and **3 unsent drafts**. **81** office routes remain explicitly `ROUTE_NOT_PUBLICLY_ATTESTED`; they are not inferred from search semantics.
- The unitary event register has **296 rows**: **75** baseline formal receipts + **156** mailbox transport rows + **65** separately linked source-proved receipt/act/notice/correspondence rows. Layer overlap is intentional: transport, formal registration and official act are different propositions.
- DI 22/2026 has **11** official act rows, including two distinct acts on 11 February and two on 13 February, linked to **8** distinct notice transports without collapsing a notice into an act.
- The 2-August seven-destination family has **7** independent REG-AGE receipt rows. Six one-to-one public office-label mappings remain normalization work; the primary receipts and exact registration references are nevertheless individually controlled.

The receipt boundary is fixed: an official registration receipt establishes formal presentation to the stated registry at the stated time. It does not, without more, establish downstream delivery, internal association, assignment, joinder, substantive examination, admission, investigation, merits acceptance or relief.

## 3. Start-of-thread procedure

1. Start from current `main` and read this runbook, the JSON register and the scan checkpoint before querying Gmail or asking for a prior bundle.
2. Verify the generated state:

   ```bash
   python scripts/reconcile_institutional_communications.py --check
   python scripts/validate_institutional_communications.py
   python -m unittest -v scripts/test_reconcile_institutional_communications.py
   ```

3. Read `next_incremental_scan` in the checkpoint. Scan the stated overlap window first, then messages strictly newer than the high-water date. Complete pagination for every query branch.
4. Reconcile privately in this order: exact REGAGE/official expediente reference; authorised source hash; then a private-only normalized date/direction/office/subject fingerprint. Do not publish the fingerprint or provider locator.
5. If an event is already registered, update only a genuinely new source-proved state. A resend, duplicate copy or additional institutional contact is not a new merits event.
6. If no new source-proved event is found, update the checkpoint only through reviewed generator changes; absence from the searched corpus means “not located,” not “nonexistent.”

When the controlled private manifest itself changes, first run the sanitizer locally with an explicit private path, inspect the public-only diff, and then run the three repository checks above. CI validates the public index statically; it does not and must not possess the private input.

## 4. Adding a source-proved event

For a new official receipt or act:

1. Preserve the controlling source privately and record its custody relationship outside Git.
2. Publish only the minimum event fields: date, direction, channel, office, official reference, controlled public category/digest, authorised repository anchor, what it proves and what it does not prove.
3. A native mailbox transport receives a stable ID in the reserved `PD-SP-EVT-1001+` band by public match key. A distinct receipt/act/notice receives a reviewed lower-band `KEY_EVENTS` row. Never reuse or renumber an existing ID.
4. For a signed act, use `SOURCE_PROVED_SIGNATORY` only when the signature is controlled and the person ID/name matches the identity registry. Otherwise use `INSTITUTION_ONLY_SIGNATURE_PENDING` or another explicit institution-only state and omit person fields.
5. Run `--apply`, then validator, tests and `--check`. Commit the generated register and checkpoint with the generator/schema/test change.

The 75-row Anexo 4 index is an immutable baseline. Do not append later receipts to that source merely to make the denominator grow; later source-proved receipts are curated events and remain outside the baseline cohort. Link transport and act layers through `linked_transport_event_ids`; do not replace one with the other.

## 5. Subject and privacy control

The canonical receipt CSV and private mailbox manifest contain source labels, but the public machine layers do not repeat them. They store a deterministic category and SHA-256 digest of the NFC-normalized label. The digest supports equality/reconciliation; it is not a provider identifier and does not disclose the label.

Prohibited public fields include Gmail message/thread IDs, Drive IDs/URLs, exact subjects, addresses/display names, native attachment/inline-image names, mailbox bodies, direct email/phone data, tokens and vault/storage locators. Persistence is confirmed only at the opaque custody-reference, aggregate SHA-256 and row-count level; no Library/provider/file ID or storage path is public.

## 6. Filing-status control

- Draft prepared: not sent and not filed.
- Email sent: transmission evidence only.
- Email acknowledgement: receipt only to the office expressly acknowledging it.
- REG-AGE receipt: formally presented to the stated registry; no downstream inference.
- Office routing statement: routing as stated; no association or examination inference.
- Signed decision/notice: the act and stated disposition are controlled; underlying allegations and legality remain separate questions.
- Repository or website publication: public disclosure only, never legal filing.

As at the 31-August checkpoint, the pagination-complete last-month control located no post-notification E.G. 745/2026 reposición, no matching REG-AGE receipt and no equivalent merits-filing proof. That status changes only on new source proof.

## 7. Failure and drift handling

- Source-index hash drift: stop and identify whether the baseline was altered; do not silently accept it.
- Duplicate REGAGE with different metadata: stop as a conflict; do not collapse it.
- Register/checkpoint drift: run `--apply`, inspect the diff, validate, then commit both generated files together.
- Missing repository anchor: retain the event outside the public register until an authorised public-safe derivative exists.
- Signature uncertainty: retain institution-only attribution.
- Aggregate-only records: leave the single unresolved batch unchanged until individual official status sources are controlled.

## 8. Explicit source-required / normalization gates

- The 22 later RedSARA/AGE records remain aggregate-only; no 22 synthetic event rows exist.
- EG 58/2026 remains `SOURCE_REQUIRED`: no discrete act was read sufficiently to create a decision row.
- DP 1901/2026 has the 12-July court-to-Fiscalía transfer row; the signed Fiscal report and later judicial act remain source-required.
- EG 6/2026 has a notice row and an attached-act-presence row, but the underlying act's substantive digest remains pending.
- Six of the seven August receipts retain individual references but await one-to-one public destination-label normalization from their primary receipt fields; no destination is guessed.
- Eighty-one mailbox transport rows retain `ROUTE_NOT_PUBLICLY_ATTESTED` until an independently linked primary receipt, signed act or official notice proves the route.
- A post-notification E.G. 745/2026 reposición receipt remains unlocated; the filing status stays prepared/outstanding and not verified as filed.

Adverse outcomes, silence, routing gaps and repeated institutional contact remain evidence questions. They do not prove coordination, obstruction, capture, favouritism, prevarication or criminality without the additional evidence required for those propositions.
