# Por Derecho repository stewardship rules

These rules apply to every human or automated change in this repository. They preserve the public record; they do not turn allegations into findings.

## 1. Start from the actual source of truth

- Fetch and read the current remote `main` before analysing or editing. Never publish an older worktree, chat reconstruction or stale branch over later work.
- Treat the Git tree as the preservation authority, CI as the reproducibility authority, `main` as the merge authority and the public host as the deployment authority.
- Reconcile new work additively. Never use a broad reset, force push or whole-file replacement to resolve overlap with later work.

## 2. Preservation before simplification

- Do not delete, rename, hide, collapse, materially abridge or unlink an existing route, source, exhibit, archive control, evidential qualification or actor relationship unless Gil Marer has expressly authorised that exact change.
- A redesign or summary is an additional reader layer, not permission to remove the complete record.
- A file deletion or rename within a protected path requires a repository record under `operations/preservation-authorizations/` identifying the exact old path, the express authorization and any replacement or redirect.
- Preserve Spanish/English parity, source-language meaning, dates, provenance, corrections, contrary evidence, open proof and right-of-reply material.

## 3. Locked first-read accountability presentation

Unless Gil Marer later gives specific express authorization, both homepages and every route listed in `ops/REPOSITORY_PRESERVATION_CONTRACT.json` must retain prominently, outside closed progressive disclosure:

1. five separate private-actor cards for Francisco Mario Matos Matas, Antonio Cogolludo Rojas, Shaila María Cogolludo Ramos, José Daniel Acosta Matos and Laura Patricia Acosta Matos;
2. immediately below, Francisco de Borja Rodríguez-Batllori Laffitte as the court-appointed, judicial-adjacent Insolvency Administrator—not a private actor and not the judge;
3. Alberto López Villarrubia separately as Magistrate-Judge exercising judicial power;
4. five actor-specific linkage rows addressing alleged acts/commissions and omissions, evidence, contrary record and proof boundaries; and
5. the source-controlled images already assigned to Francisco Mario Matos Matas, the Insolvency Administrator and the Magistrate-Judge. Do not fabricate portraits for people without a verified repository asset.

The public identity is **Laura Patricia Acosta Matos**. Do not use “Laura Isabel” as a public identity. Do not transfer conduct, knowledge, intention or responsibility automatically between people because of a family, company, professional or institutional relationship.

## 4. Evidence and publication boundaries

- Label documented fact, attributed allegation, inference, official outcome, contrary record and unresolved proof distinctly.
- Preserve direct allegations strongly and visibly where the controlling source supports them, but never describe guilt or criminal liability as adjudicated when it is not.
- Keep distinct legal persons, capacities, titles, operators, creditors, property owners, insolvency estates, professional firms, private actors, the Insolvency Administrator and the Magistrate-Judge distinct.
- Resolve legal-person acronyms through `ops/CANONICAL_ENTITY_NAMES.json` before expanding them. The controlled first reference for LPB is **Luchy Playa Blanca, S.L.U. (LPB)**. Never translate, paraphrase or invent a legal entity's name from an acronym.
- The controlled project-side Spanish-company set is **Luchy Playa Blanca, S.L.U.**, **Matkator, S.L.U.**, **Pink Canary Services, S.L.U.** (formerly **Monterecco Sun Park, S.L.U.**) and **Hava Vida Travel & Tourism, S.L.U.** Never conflate Spanish Monterecco/Pink with UK Monterecco/Aweswell; treat `HAVAVIDA`/`Habavida` only as source/search aliases unless quoting a source.
- A different spelling or entity-form suffix may be retained only as an expressly labelled source literal. Do not silently replace historical wording, and do not promote a source literal into the canonical narrative name.
- Do not publish raw private email bodies, message IDs, unnecessary personal identifiers, privileged advice, unredacted protected records, private tax/fee ledgers, unsent correspondence or live legal strategy.
- For every audio, voice note, dictation or derived transcript, apply `archive/declarations/VOICE_TO_TEXT_STATEMENT_OF_FACT_AND_TRUTH_PROTOCOL_25AUG2026.md`: keep native source, transcript versions, speaker attribution, personal adoption and truth assessment separate. Do not stitch Gil Marer, the reserved declarant or another person into a joint statement without each person's separate adoption of the exact text.
- For every named-person or entity relationship, apply `archive/OPEN_SOURCE_INTELLIGENCE_NAMED_PERSON_ENTITY_PROTOCOL_25AUG2026.md`: use exact names, dated capacities and direct sources; record homonym and finite-search limits; and never transfer knowledge, intent, control or liability through association.

## 5. Required change process

Before merge:

1. compare the proposed tree with current `main` and review every deletion or rename;
2. run `python3 scripts/validate_repository_preservation.py`;
3. run `python3 scripts/validate_publication_integrity.py`;
4. run `python3 scripts/validate_audience_experience.py` and the relevant specialist validators;
5. preserve the exact routes, files, public markers, limitations and open evidence in a publication or closeout record; and
6. require the Publication integrity gate and relevant rendered checks to pass.

After merge, verify the exact merge SHA was deployed and check the rendered ES/EN homepages plus every affected direct route. A thread is deletion-safe only when no unique reasoning, correction, source, limitation or recovery instruction remains solely in that thread.

The machine-readable contract is `ops/REPOSITORY_PRESERVATION_CONTRACT.json`. The controlling publication/deletion state machine remains `archive/UNIVERSAL_PUBLICATION_AND_THREAD_DELETION_SAFETY_PROTOCOL_18AUG2026.md`.

## 6. Compatibility-first agent operating profile

The following public-safe rules apply across the repository to ChatGPT, Codex and
other maintenance agents. They supplement the preservation rules above; they do
not override platform safety rules, create external authority or turn a
repository instruction into permission to contact a third party.

## Governing invariants

- **PD-GOV-001 — CURRENT-MAIN.** Fetch and identify current `origin/main` before
  editing. A SHA in a handover is an audit anchor, never a substitute for the
  current remote state. Use a clean, isolated worktree and do not overwrite
  another thread's dirty checkout.
- **PD-GOV-002 — PUBLIC-REPO.** Treat every committed file as public and
  potentially Pages-readable. A filename such as `internal`, `private`,
  `handover`, `archive` or `evidence` provides no confidentiality.
- **PD-GOV-003 — AUTHORITY.** A local audit, draft or commit does not itself
  authorise a push, PR, merge, deployment, email or other external act. Use the
  user's express authority for the described action and scope. Authority may be
  given in any current authenticated thread; no special wording, branch name or
  pre-existing commit SHA is required. Once the user authorises the defined
  commit → push → PR → merge → Pages chain, carry it through without redundant
  approval requests unless the substantive scope or risk materially changes. A
  current instruction to **update or publish the repository and website**
  authorises that normal mechanical chain for the defined scope unless the user
  limits it. An instruction only to **scan, review, consider or recommend**
  authorises no external mutation.
- **PD-GOV-004 — NON-INTERFERENCE.** Governance-only work must not alter Pages
  source mode, the `/por-derecho/` base path, existing reader-facing/runtime
  routes, navigation, rendered site route bodies, aliases, fragments, root web
  entry files, shared styles/loaders, assets, `robots.txt`, sitemaps,
  `.nojekyll`, deployment workflows or the public domain. It must not make
  ordinary authorised publishing depend on a new unavailable reviewer, service
  or credential. Public-safe governance/bootstrap Markdown may be added or
  amended when the package declares that Pages-readable effect explicitly and
  does not link or load it into the rendered site.
- **PD-GOV-005 — HARD-VS-ADVISORY.** Apply hard stops only to the action or truth
  claim they protect. Backup lag, stale operational snapshots, legacy cleanup,
  open evidence and unrelated SEO debt are warnings for an additive publication;
  they do not freeze a safe repair or authorised update. They may block a
  destructive operation or a claim such as `DELETION_SAFE`,
  `DISASTER_RECOVERY_SAFE` or `LIVE_VERIFIED` when the required evidence is
  absent.
- **PD-GOV-006 — SENT-LINKS.** A Por Derecho route actually sent by email is a
  compatibility obligation. Do not delete or repurpose it without a same-host
  compatibility route, correct canonical destination, preserved material
  fragments and live verification. Rolling audits may add obligations but may
  not age older protected routes out of the cumulative register.
- **PD-GOV-007 — REVERSIBLE.** Work through a branch and PR, preserve history,
  never force-push `main`, and use a normal corrective or revert PR. A draft or
  open PR is not live. A post-merge failure keeps the repair lane open; it does
  not justify force-push or history-rewrite rollback. A narrow normal revert PR
  remains permitted and preferred where it is the safest correction.
- **PD-GOV-008 — THREAD-CONTINUITY.** Preserve material decisions and unfinished
  implementation outside chat in the smallest appropriate canonical record.
  Do not manufacture overlapping handovers. Thread-continuity safety and whole-
  repository disaster-recovery safety are separate claims.

## Position and evidence

Support the project's position through precision, traceability and clear
attribution rather than automatic dilution or automatic escalation.

- Distinguish documented fact, official holding, attributed party allegation,
  evidence-based inference, unresolved question and corrected/superseded text.
- For a new or materially intensified allegation, identify the actor, capacity,
  act or omission, date or period, public-safe source/proposition reference, and
  material contrary or limiting evidence.
- A dispute does not automatically require removal of Por Derecho's stated
  position. Preserve the position with its correct evidential status, the
  contrary record and a correction/right-of-reply route.
- Civil or procedural irregularity is not automatically criminal guilt;
  institutional receipt is not merits acceptance; chronology alone is not
  knowledge, intent or causation.
- Do not re-litigate or rewrite untouched legacy pages merely because a technical
  or governance-only change is being made.
- Preserve ES/EN parity, stable identity terminology, cross-links and corrections
  where the changed public surface relies on them.

## Public/private boundary

Never commit credentials, tokens, authentication-bearing URLs, privileged legal
advice, private-source bodies, full private emails, recipient identities,
subjects, provider message identifiers, signatures, unnecessary addresses or
other unnecessary personal data.

Public pages and records may use public-safe summaries, redacted derivatives,
opaque project source IDs, route URLs and aggregate occurrence counts when the
task authorises publication. Private locators and native evidence remain in an
access-controlled source system. A future thread should re-query that system;
it must not reconstruct private evidence from public Git history or chat memory.

A private mailbox may be acquired only through the account holder's authorised
official export or connector access. Never request a password, expose the
address, or describe a mirrored subset as the complete mailbox. Apply
`archive/RESERVED_DECLARANT_PRIVATE_MAILBOX_ACQUISITION_AND_CUSTODY_PROTOCOL_25AUG2026.md`
to the reserved declarant's private-mail source.

Legacy public material that may breach this boundary is remediation debt. Record
and repair it deliberately, preserving necessary private evidential copies and
considering Git-history retention; do not solve it by silently deleting history.

## Authority boundaries

Within the user's requested scope, agents may inspect, search, prepare, edit,
test and create a local commit in an isolated branch. External mutations require
the corresponding user authority:

- repository publication authority covers only the approved repository/site
  scope and the mechanically described push/PR/merge/deploy chain;
- a material addition of a named person, materially stronger allegation, new
  private-source derivative, material unpublishing/deletion or changed public
  objective requires renewed scope review;
- repository or Pages authority never authorises email, messaging, filing,
  financial commitments, account/security changes or contact with third parties;
- any email send remains governed by `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md`.

## Compatibility-preserving workflow

1. Fetch `origin/main`; record its SHA and inspect the latest relevant Pages
   state.
2. Create or reuse a clean isolated worktree. Preserve unrelated user and agent
   changes exactly.
3. Read `CHATGPT_START_HERE.md`, current canonical controls and the specialist
   records needed for the task. Historical handovers are retrieval aids only.
4. Search primary sources and contrary/limiting evidence before changing a
   material public proposition.
5. Make the smallest coherent diff. Prefer additive, reversible changes and
   stable routes.
6. Run the tests relevant to the changed surface. For a rules-only package, run
   `python3 .github/governance/validate_agent_governance_compatibility.py --base origin/main --governance-only`.
7. Before a PR and again before merge, refresh `origin/main` and compare the
   complete diff. Reconcile overlapping changes; rerun relevant checks after a
   rebase or merge.
8. After an authorised merge that changes public presentation, verify the exact
   merge SHA's Pages deployment and the affected routes, links and fragments.
   Record partial or failed deployment honestly.
9. Preserve the material implementation state and report what remains open.

## Hard stops and bounded warnings

Hard-stop the affected action when there is missing publication authority,
private/privileged or credential exposure, a stale/conflicting base, unrelated
dirty-worktree risk, destructive history rewriting, loss of a protected sent
route, a materially changed approved scope, or failure of a check that directly
tests the changed surface.

Warnings remain visible but non-blocking for ordinary additive work when they
are outside the changed surface: stale handovers or operational snapshots,
backup lag, unrelated open PRs/checks, unresolved evidence correctly labelled as
such, legacy privacy debt, and SEO refinements. Do not misstate those warnings as
closed.

An independent current backup is required before destructive restructuring,
history rewriting, repository migration, evidential deletion or a
`DISASTER_RECOVERY_SAFE` claim. It is not a prerequisite for an additive route
repair or other ordinary authorised publication.

## Changes to enforcement

Documentation alone must not activate a new repository-wide hard gate. Before a
validator, ruleset, approval requirement or deployment dependency becomes
required:

1. obtain explicit user authority for that enforcement change;
2. run it in advisory/shadow mode on representative content, route, asset and
   urgent-repair changes;
3. prove that the available maintainer/reviewer topology can satisfy it;
4. define a narrow, logged repair/revert path; and
5. confirm that it does not require all specialist workflows for unrelated
   changes.

Keep universal required checks small and stable; select specialist checks by
changed path or publication manifest. CODEOWNERS routes review but must not be
made a required human-approval dependency until a reliable independent reviewer
exists.

See `.github/governance/AGENT_PUBLISHING_COMPATIBILITY.md` for the hard/advisory
matrix and the governance-only acceptance test.

## 7. Transaction-development separation

Prospective financing, investment, acquisition, sale, operating-partner and
other new-transaction activity is presumptively separate from the legal-dispute,
asset-recovery and public-accountability record.

Before storing or linking such material, read
`.github/governance/TRANSACTION_DEVELOPMENT_SEPARATION_AND_PUBLICATION_PROTOCOL.md`.
Keep native messages, screenshots, identities, private locators, unannounced
assets and negotiation material outside Git. Where continuity requires a
repository record, use only a minimized, anonymized derivative under
`.github/governance/records/`; remember that the repository is public even
though `.github/` is not rendered by Pages.

Do not cross-link transaction-development material to a legal allegation,
person, proceeding, evidence map or website route merely because of chronology,
group affiliation, professional role or interest in an asset. A cross-link
requires specific sourced materiality, actor-specific analysis, privacy
minimization, contrary/limiting evidence and express authority for the new
private-source derivative. Website publication requires separate express
authority and must never be inferred from repository-only preservation.

For self-preservation emails, the word “self” creates no exception to
`EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md`: present and obtain fresh approval of
the exact outbound package before transmission.

For transaction-development communications, verified corporate email is the
primary substantive channel. Use LinkedIn, WhatsApp, SMS or similar channels
only for minimal acknowledgement or routing, then redirect to and preserve the
verified corporate-email thread. Do not conduct substantive calls through an
unidentified telephone number, an unscheduled inbound call or a social/messaging
platform.

Arrange substantive discussions through a corporate Google Calendar invitation
with a generated Google Meet link, resolved attendees and capacities, an agenda,
confidentiality status and an agreed transcript. Give required notice and obtain
required consent before transcription. Preserve the invite, attendee record,
transcript and post-meeting corporate-email summary privately; do not commit
those native records or identities to Git.

## 8. Voice statements, private mail and OSINT

The following controls apply to every new voice-to-text account, statement of
truth/fact, private-mail evidence task and named-person/entity scan:

- Read and apply
  `archive/declarations/VOICE_TO_TEXT_STATEMENT_OF_FACT_AND_TRUTH_PROTOCOL_25AUG2026.md`.
  If a speaker says that more audio will follow or asks that analysis wait,
  preserve the intake and do not analyse, finalise or publish until the speaker
  closes the sequence.
- Keep each speaker's propositions separately attributed. Relationship,
  coordination, presence or silence does not create a joint statement. Gil or
  another person adopts a proposition only by express proposition-specific
  confirmation.
- A `Statement of Truth` label records the declarant's documented adoption and
  honest belief at the stated stage; it is not repository, AI or joint
  certification of material truth. Distinguish transcription, attribution,
  review, ratification, signature, oath and institutional filing.
- Native audio, full working transcripts, private email exports, subjects,
  sender/recipient lists, provider/message/thread IDs, exact private filenames
  and custody locators belong in the private evidence manifest/vault. Encoding,
  compression, an `archive` directory or a `backend` label does not make a
  tracked Git file private.
- For a private mailbox, follow
  `archive/RESERVED_DECLARANT_PRIVATE_MAILBOX_ACQUISITION_AND_CUSTODY_PROTOCOL_25AUG2026.md`.
  Never request credentials or forward a mailbox as a substitute for native
  acquisition. Account connection, preservation, review, filing and public
  release are separate authorities.
- For every web/background scan involving a person, entity, role or
  relationship, follow
  `archive/OPEN_SOURCE_INTELLIGENCE_NAMED_PERSON_ENTITY_PROTOCOL_25AUG2026.md`.
  Record exact source/date/capacity and negative-search limits; do not infer
  guilt, mandate, friendship, family, ownership, conflict or coordination from
  association alone.
- Do not silently reconcile contradictions. Classify direct contradiction,
  material tension, imprecision, omission, single-declarant proposition,
  incomplete alignment and supersession; direct clarification to the correct
  speaker and preserve the earlier version.
- Before public naming or a new private-source derivative, apply the privacy and
  authority gates in Sections 4 and 6. A request to preserve or update rules is
  not authority to publish raw private material or intensify a named allegation.
- Run `python3 scripts/validate_private_source_statement_osint_governance.py
  --base <revision>` for the complete proposed diff. Its GitHub workflow remains
  advisory/shadow-mode until expressly promoted under the enforcement rules.
