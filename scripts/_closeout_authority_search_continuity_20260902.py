#!/usr/bin/env python3
from pathlib import Path
import json
import re

WORKSPACE_ID = 'PD-WS-20260902-0001'
HANDOFF_ID = 'PD-WCH-20260902-AUTH-SEARCH-001'
BASELINE = '0145793d53d86a99f34ef60ff69db7df871e4910'
HANDOFF_MD = 'archive/handoffs/2026-09-02-justice-authority-caret-search-live-closeout.md'
HANDOFF_JSON = 'archive/handoffs/2026-09-02-justice-authority-caret-search-live-closeout.json'
ARTIFACT_SHA = '2738c514d4523d9a645233db848b5d51d457e23ce7598b3e89e2149bc0fd0fd9'

register_path = Path('data/workspace-register-v1.json')
register = json.loads(register_path.read_text(encoding='utf-8'))
ids = [row['workspace_id'] for row in register.get('workspaces', [])]
if WORKSPACE_ID in ids:
    raise SystemExit(f'workspace already exists: {WORKSPACE_ID}')
collisions = [value for value in ids if value.startswith('PD-WS-20260902-')]
if collisions:
    raise SystemExit(f'2026-09-02 workspace collision: {collisions}')

workspace = {
    'workspace_id': WORKSPACE_ID,
    'title': 'Judicial/prosecutorial authority register, caret search and court-hierarchy release',
    'status': 'DELETION_SAFE_WITH_OPEN_WORK',
    'current_handoff_id': HANDOFF_ID,
    'handoff_path': HANDOFF_MD,
    'machine_handoff_path': HANDOFF_JSON,
    'topic_keys': ['JUSTICE_AUTHORITY', 'CARET', 'CAEPR', 'JUDGES', 'LAJ', 'FISCALIA', 'FISCALES', 'COURT_HIERARCHY', 'HOMEPAGE_SEARCH', 'CONTINUITY'],
    'repository': 'sbu001monterecco/por-derecho',
    'public_private_boundary': 'PUBLIC_REPO_CONTAINS_SOURCE_SAFE_CANONICAL_IDENTITIES_GOVERNANCE_PUBLIC_ROUTES_AND_VERIFICATION_METADATA; PRIVATE_NATIVE_DOCKETS_AND_CONNECTED_SOURCE_CONTENT_ARE_NOT_COPIED',
    'continuous_capture_mode': 'CONNECTED_AGENTIC_CHECKPOINTING',
    'current_main_sha_checked': BASELINE,
    'primary_publication_pr': 1347,
    'primary_merge_sha': '5e12444f44b27b3c94d7bc31c80e2d56ef58bb08',
    'visibility_hotfix_pr': 1351,
    'publication_merge_sha': BASELINE,
    'pages_run_id': 33622844666,
    'live_browser_verification_run_id': 33623082252,
    'verification_artifact_id': 9843703946,
    'verification_artifact_sha256': ARTIFACT_SHA,
    'validation_state': 'LIVE_VERIFIED_ES_EN_CANONICAL_SEARCH_464_ENTRIES_REPRESENTATIVE_CLICKTHROUGHS_HTTP_200_AUTHORITY_REGISTER_CI_GREEN',
    'authority_governance': '.github/governance/JUDICIAL_PROSECUTORIAL_AUTHORITY_REGISTER_CONTINUITY_02SEP2026.md',
    'authority_control_id': 'PD-SP-JUSTICE-AUTHORITY-CURRENT-20260902-01',
    'current_source_identified_denominator': {'named_people': 59, 'caret_confirmed': 56, 'caret_pending': 3, 'caret_suspended': 0},
    'open_gap_state': 'GLOBAL_HISTORIC_DOCKET_BACKFILL_OPEN_EXPLICIT_SOURCE_GAPS_REQUIRED',
    'next_target_mode': 'TARGETED_PROCEEDING_ACTIONS_WITH_AUTHORITY_BACKFILL_AS_PRIMARY_SOURCES_SURFACE; EG_745_2026_PRIORITY'
}
register['control_date'] = '2026-09-02'
register['default_workspace_id'] = WORKSPACE_ID
register['workspaces'].append(workspace)
register_path.write_text(json.dumps(register, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

action_ledger = {
    'control': 'PD-CONT-DIGEST-001',
    'repository_digest_actions': [
        {'action': 're_fetch_current_main', 'result': BASELINE},
        {'action': 'read_workspace_index_and_register', 'result': '2-Sep authority/search release was not previously registered as its own PD-WS workspace'},
        {'action': 'read_controlling_governance', 'paths': [
            '.github/governance/JUDICIAL_PROSECUTORIAL_AUTHORITY_REGISTER_CONTINUITY_02SEP2026.md',
            '.github/governance/WORKSPACE_THREAD_CONTINUITY_HANDOFF_STANDARD_01SEP2026.md',
            '.github/governance/AUTOMATIC_WORKSPACE_PERSISTENCE_ARCHITECTURE_01SEP2026.md',
            '.github/governance/CONCURRENT_WORKSPACE_REGISTRATION_PROTOCOL_01SEP2026.md',
            '.github/governance/CONTINUITY_EVENT_REPOSITORY_DIGEST_ACTION_CHECKLIST_01SEP2026.md'
        ]},
        {'action': 'inspect_publication_and_verification_runs', 'pages_run_id': 33622844666, 'browser_run_id': 33623082252},
        {'action': 'inspect_current_authority_search_ci', 'result': 'green on exact publication SHA'}
    ],
    'connected_source_actions': [{'action': 'none', 'reason': 'Repository/publication continuity status did not require a current Gmail/Drive reconstruction.'}],
    'registration_and_identity_actions': [
        {'action': 'register_workspace', 'id': WORKSPACE_ID, 'state': 'MAIN_REGISTRATION_PENDING_PR_MERGE'},
        {'action': 'no_new_caepr_identity_allocated', 'reason': 'Existing immutable CAEPR identities and the current source-identified denominator are reused.'}
    ],
    'relationship_interlink_actions': [
        {'action': 'link_workspace_to_authority_governance_search_validator_publication_and_live_verification'},
        {'action': 'preserve_person_proceeding_court_fiscalia_act_specific_interlink_contract', 'state': 'GOVERNED'}
    ],
    'chronology_and_proceedings_actions': [
        {'action': 'preserve_current_source_identified_denominator', 'named_people': 59, 'confirmed': 56, 'pending': 3},
        {'action': 'preserve_historic_docket_boundary', 'state': 'BACKFILL_OPEN_NOT_CERTIFIED_COMPLETE'}
    ],
    'publication_and_live_actions': [
        {'layer': 'repository', 'state': 'MERGED_TO_MAIN', 'sha': BASELINE},
        {'layer': 'github_pages', 'state': 'DEPLOYED_SUCCESS', 'run_id': 33622844666},
        {'layer': 'live_browser', 'state': 'LIVE_VERIFIED', 'run_id': 33623082252, 'indexed_entries': 464},
        {'layer': 'verification_artifact', 'artifact_id': 9843703946, 'sha256': ARTIFACT_SHA}
    ],
    'completed_actions': [
        'Published current authority/caret/search release and court hierarchy.',
        'Repaired hidden homepage search mount and added regression guard.',
        'Verified Spanish and English live search, representative canonical IDs and HTTP-200 click-throughs.',
        'Created dedicated durable workspace/handoff continuity package for this release.'
    ],
    'open_actions': [
        {'priority': 'P1', 'item': 'Historic/current official-docket backfill', 'close_trigger': 'Recover primary/certified docket sources and register every source-identifiable Judge/Magistrate, LAJ and Fiscal or explicit non-applicability/gap.'},
        {'priority': 'P2', 'item': 'Proceeding authority-role completeness', 'close_trigger': 'Every applicable Master Proceedings row carries explicit authority-role state and global dynamic validator passes.'},
        {'priority': 'P2', 'item': 'Concurrent proceedings-interconnectivity successor-hash drift', 'close_trigger': 'Reconcile against the then-current main without weakening unrelated gates.'}
    ],
    'do_not_infer': [
        'CARET identity does not prove conduct, authorship, knowledge, intent, wrongdoing, liability or outcome.',
        'Current office-holder does not prove historical handling of a file.',
        'A notice/signature/heading does not transfer authorship to another act.',
        'CURRENT SOURCE-IDENTIFIED DENOMINATOR VERIFIED is not CERTIFIED COMPLETE DOCKET.',
        'Repository merge, Pages deployment, live verification and institutional filing/service are separate states.'
    ],
    'next_thread_bootstrap': f'Continue {WORKSPACE_ID} from repository state. Read CURRENT_WORKSPACE_HANDOFF.md, {HANDOFF_MD}, the authority continuity control, assets/data/justice-authority-register-current-v2.json and the Master Proceedings/CAEPR controls named there. Re-fetch current main before changes. Preserve explicit historic-docket gaps. Then proceed to the priority proceeding, currently E.G. 745/2026.'
}

machine = {
    'schema': 'por-derecho.workspace-handoff.v1',
    'handoff_id': HANDOFF_ID,
    'workspace_id': WORKSPACE_ID,
    'date': '2026-09-02',
    'status': 'DELETION_SAFE_WITH_OPEN_WORK',
    'repository': 'sbu001monterecco/por-derecho',
    'authoritative_baseline_sha': BASELINE,
    'publication': {'state': 'LIVE_VERIFIED', 'primary_pr': 1347, 'visibility_hotfix_pr': 1351, 'merge_sha': BASELINE, 'pages_run_id': 33622844666, 'live_browser_run_id': 33623082252, 'artifact_id': 9843703946, 'artifact_sha256': ARTIFACT_SHA, 'indexed_entries': 464},
    'authority_state': {'control_id': 'PD-SP-JUSTICE-AUTHORITY-CURRENT-20260902-01', 'governance_path': '.github/governance/JUDICIAL_PROSECUTORIAL_AUTHORITY_REGISTER_CONTINUITY_02SEP2026.md', 'named_people': 59, 'caret_confirmed': 56, 'caret_pending': 3, 'caret_suspended': 0, 'historic_docket_backfill': 'OPEN_NOT_CERTIFIED_COMPLETE'},
    'key_ids': {'master_provincial_court': 'PD-SP-I-0044', 'provincial_court_section_2': 'PD-SP-I-0025', 'provincial_court_section_4': 'PD-SP-I-0014', 'dp748': 'PD-SP-R-0003', 'graciela_perez_valencia': 'PD-SP-P-0147', 'ricardo_mosteyrin': 'PD-SP-P-0058', 'auren_reestructuraciones_slp': 'PD-SP-O-0070'},
    'action_ledger': action_ledger
}
Path(HANDOFF_JSON).parent.mkdir(parents=True, exist_ok=True)
Path(HANDOFF_JSON).write_text(json.dumps(machine, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

md = f'''# Justice authority / caret search — live closeout and successor handoff

**Handoff ID:** `{HANDOFF_ID}`  
**Workspace ID:** `{WORKSPACE_ID}`  
**Date:** 2 September 2026  
**Status:** `DELETION_SAFE_WITH_OPEN_WORK`  
**Release state:** `LIVE_VERIFIED`

## Scope

This is the durable continuation object for the 2 September 2026 judicial/prosecutorial authority-register, CAEPR caret-search and court-hierarchy release. It closes the gap that existed when the release was already merged/live but had not yet been assigned its own `PD-WS-*` workspace entry. A new thread must treat repository state, not originating-chat memory, as authoritative.

## Authoritative repository and publication state

- Verified publication baseline before this continuity PR: `{BASELINE}`.
- Primary authority/search release: PR **#1347**, merge `5e12444f44b27b3c94d7bc31c80e2d56ef58bb08`.
- Visibility repair: PR **#1351**, final release SHA `{BASELINE}`.
- GitHub Pages run **33622844666 / #1401**: successful build/status/deploy for the exact final release SHA.
- Public Chromium run **33623082252**: successful ES/EN live verification.
- Verification artifact **9843703946**, SHA-256 `{ARTIFACT_SHA}`.
- Live search indexed **464** entries at verification.

## Controlling authority state

Authority governance is `.github/governance/JUDICIAL_PROSECUTORIAL_AUTHORITY_REGISTER_CONTINUITY_02SEP2026.md`, control `PD-SP-JUSTICE-AUTHORITY-CURRENT-20260902-01`.

Current recovered-source denominator: **59 named people; 56 CARET_CONFIRMED; 3 CARET_PENDING; 0 suspended.** This is `CURRENT SOURCE-IDENTIFIED DENOMINATOR VERIFIED`; it is not a claim that every historic/current official docket is obtained or certified complete.

Court hierarchy remains explicit: `PD-SP-I-0044` master Audiencia Provincial de Las Palmas; `PD-SP-I-0025` Sección Segunda; `PD-SP-I-0014` Sección Cuarta.

## Search / caret live contract

Representative live checks proved name/full-ID/caret/reference routing for Graciela Pérez-Valencia Díaz (`PD-SP-P-0147`, `^P-0147`, `^0147`), DP 748/2026 (`PD-SP-R-0003`, `^R-0003`, NIG `3802343220260002351`, `TF-CRI-003`), Audiencia Provincial de Las Palmas (`PD-SP-I-0044`, `^I-0044`, `^0044`), Sección Segunda (`PD-SP-I-0025`), Ricardo de Mosteyrín Sampalo (`PD-SP-P-0058`) and AUREN REESTRUCTURACIONES SLP (`PD-SP-O-0070`, `^O-0070`). Representative destinations returned HTTP 200 in ES and EN.

A caret/search hit never proves conduct, authorship, knowledge, intent, wrongdoing, liability or outcome.

## Continuity boundaries

Every source-supported Judge/Magistrate, LAJ and Fiscal is registered once and linked act/date/capacity specifically. Courts and Fiscalía offices remain separate institutions. Unknown applicable identities are explicit gaps, never silent blanks. Historical substitutions append; they do not overwrite.

Repository merge, Pages deployment, live verification and institutional filing/service/email/social publication are distinct states.

## Open work

1. **P1 — historic/current official-docket backfill:** recover primary/certified sources and register newly source-identifiable Judges/Magistrates, LAJs and Fiscals or preserve explicit source-defined gaps/non-applicability.
2. **P2 — proceeding authority-role completeness:** continue until every applicable Master Proceedings row has an explicit authority-role state; do not claim global historic completeness before that denominator closes.
3. **P2 — concurrent proceedings-interconnectivity successor-hash drift:** reconcile separately against the then-current main; do not weaken unrelated gates.

## Successor read order

1. `CURRENT_WORKSPACE_HANDOFF.md`
2. this handoff
3. `{HANDOFF_JSON}`
4. `.github/governance/JUDICIAL_PROSECUTORIAL_AUTHORITY_REGISTER_CONTINUITY_02SEP2026.md`
5. `assets/data/justice-authority-register-current-v2.json`
6. `.github/governance/CAEPR_CARET_IDENTITY_AND_ALL_IS_VERIFICATION_PROTOCOL_26AUG2026.md`
7. `archive/PROCEEDINGS_MASTER_REGISTER_PROTOCOL.md`
8. `archive/PROCEEDINGS_FULL_IDENTITY_STORYING_GOVERNANCE_30AUG2026.md`
9. `.github/governance/MINISTERIO_FISCAL_ADVERSE_PARTY_FULL_NOTICE_PROTOCOL_31AUG2026.md`
10. only the specific proceeding controls required by the next task.

Re-fetch current `main` before any write.

## Action ledger

The finite `PD-CONT-DIGEST-001` action ledger is in `{HANDOFF_JSON}`. No Gmail/Drive scan was required for this closeout because the task was repository/publication/continuity state; no claim is made that connected-source evidence was refreshed. The failed initial one-shot workflow attempt is not treated as completed state; it created no workspace/register/handoff change.

## Next-thread bootstrap

> Continue `{WORKSPACE_ID}` from repository continuity state, not prior chat memory. Read the root pointer, this handoff, its machine companion, the authority continuity control and current authority/CAEPR/Master Proceedings controls. Re-fetch current `main`. Preserve explicit historic-docket gaps and act/date/capacity boundaries. Do not repeat broad discovery unless a named gap is stale. Then continue the priority proceeding, currently **E.G. 745/2026**, using this verified authority/caret/search layer as the continuity substrate.

## Deletion-safety verdict

`DELETION_SAFE_WITH_OPEN_WORK` once this package is merged. The authority/search release itself is already `LIVE_VERIFIED`; remaining work is explicit and reconstructable without the originating chat.
'''
Path(HANDOFF_MD).write_text(md, encoding='utf-8')

pointer_path = Path('CURRENT_WORKSPACE_HANDOFF.md')
pointer = pointer_path.read_text(encoding='utf-8')
if WORKSPACE_ID in pointer:
    raise SystemExit('workspace already present in pointer')
pointer = re.sub(
    r'\*\*Current workspace:\*\* `[^`]+`  \n\*\*Current continuation pointer:\*\* `[^`]+`  \n\*\*Status:\*\* `[^`]+`',
    f'**Current workspace:** `{WORKSPACE_ID}`  \n**Current continuation pointer:** `{HANDOFF_ID}`  \n**Status:** `DELETION_SAFE_WITH_OPEN_WORK`',
    pointer, count=1)
pointer = re.sub(
    r'\*\*Current checkpoint:\*\*.*?\n\n',
    f'**Current checkpoint:** the 2 September judicial/prosecutorial authority-register, CAEPR caret-search and court-hierarchy release is merged and `LIVE_VERIFIED` on `{BASELINE}`. ES/EN homepage search was browser-verified with 464 indexed entries and representative HTTP-200 click-throughs. This checkpoint adds the previously missing dedicated workspace/handoff object. Global historic-docket backfill remains explicitly open and is not certified complete.\n\n',
    pointer, count=1, flags=re.S)
section = f'''### `{WORKSPACE_ID}` — justice authority / caret search / court hierarchy — current checkpoint

State: `DELETION_SAFE_WITH_OPEN_WORK`; release state `LIVE_VERIFIED`.

Read:

1. `{HANDOFF_MD}`
2. `{HANDOFF_JSON}`
3. `.github/governance/JUDICIAL_PROSECUTORIAL_AUTHORITY_REGISTER_CONTINUITY_02SEP2026.md`
4. `assets/data/justice-authority-register-current-v2.json`
5. the CAEPR / Master Proceedings controls named by the handoff.

Critical boundary: **59 source-identified justice professionals / 56 confirmed / 3 pending is the current recovered-source denominator, not a certified complete historic/current docket denominator.** Unknown applicable Judges/LAJs/Fiscals remain explicit source gaps, never silent blanks.

'''
marker = '### `PD-WS-20260901-0001` — Acosta Matos / Canarian Hospitality hotel-platform media package — current checkpoint\n'
if marker not in pointer:
    raise SystemExit('active-workspaces insertion marker not found')
pointer = pointer.replace(marker, section + marker, 1)
heading = '## New-thread bootstrap\n'
tail = '\n\nOlder topic-specific deletion audits and handoffs remain historical controls.'
start = pointer.find(heading)
end = pointer.find(tail, start)
if start < 0 or end < 0:
    raise SystemExit('bootstrap block not found')
new_boot = f'''## New-thread bootstrap

> Continue `{WORKSPACE_ID}` from repository continuity state, not prior chat memory. Read `CURRENT_WORKSPACE_HANDOFF.md`, `{HANDOFF_MD}`, its machine companion, the judicial/prosecutorial authority continuity control and the current authority/CAEPR/Master Proceedings controls. Re-fetch current `main` before changes. Preserve explicit historic-docket gaps and act/date/capacity boundaries. Do not re-run broad discovery unless the handoff identifies a stale gap. Then continue the priority proceeding, currently E.G. 745/2026, using this verified authority/caret/search layer as the continuity substrate.'''
pointer = pointer[:start] + new_boot + pointer[end:]
pointer_path.write_text(pointer, encoding='utf-8')

print(f'Prepared {WORKSPACE_ID} / {HANDOFF_ID}')
