#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CFG = ROOT / "assets/data/consequence-risk-control-v1.json"
POLICY = ROOT / ".github/governance/CONSEQUENCE_RISK_COMMUNICATION_CONTROL_25SEP2026.md"

REQUIRED_STATES = {
    "DETECTED","CONTENT_ACQUISITION_REQUIRED","CONTENT_ACQUIRED",
    "OPERATIVE_ATTACHMENT_UNREVIEWED","CLASSIFIED","ALERT_OPEN","ACKNOWLEDGED",
    "DEADLINE_OR_SERVICE_DATE_UNRESOLVED","ROUTING_OR_DELIVERY_FAILURE",
    "EXPECTED_RESPONSE_OVERDUE","CONTROL_SYSTEM_DEGRADED","DISPOSITION_ASSIGNED",
    "ACTION_VERIFIED","NO_ACTION_REQUIRED_VERIFIED","RESOLVED"
}
REQUIRED_RULES = {
    "READ_IS_NOT_RESOLVED",
    "NOTICE_OF_NOTICE_REQUIRES_CONTENT_ACQUISITION",
    "OPERATIVE_ATTACHMENT_MUST_BE_REVIEWED_OR_MARKED_INACCESSIBLE",
    "EMAIL_TIMESTAMP_IS_NOT_AUTOMATICALLY_SERVICE_DATE",
    "OUTBOUND_EXPECTATION_CREATES_DEPENDENCY",
    "BOUNCE_OR_ROUTING_FAILURE_REOPENS_MATTER",
    "CONTROL_DEGRADATION_IS_ITSELF_AN_ALERT",
    "ALERT_NEVER_AUTHORIZES_EMAIL_OR_FILING"
}
REQUIRED_FIELDS = {
    "alert_id","source_event_id","risk_if_missed","severity","deadline_state","owner",
    "required_disposition","status","acknowledgement_state","action_verification_state","control_health"
}

def main():
    if not CFG.is_file() or not POLICY.is_file():
        raise SystemExit("missing consequence-risk control files")
    data = json.loads(CFG.read_text(encoding="utf-8"))
    if data.get("control_id") != "PD-CRC-20260925-01":
        raise SystemExit("unexpected control id")
    states=set(data.get("inbound_states",[]))
    rules=set(data.get("hard_rules",[]))
    fields=set(data.get("required_alert_fields",[]))
    missing_states=sorted(REQUIRED_STATES-states)
    missing_rules=sorted(REQUIRED_RULES-rules)
    missing_fields=sorted(REQUIRED_FIELDS-fields)
    if missing_states or missing_rules or missing_fields:
        raise SystemExit(f"incomplete control: states={missing_states} rules={missing_rules} fields={missing_fields}")
    status=data.get("automation_status",{})
    if status.get("gmail_event_arrival_hook") not in {"ACTIVE","NOT_AVAILABLE_IN_CURRENT_CONNECTED_RUNTIME"}:
        raise SystemExit("arrival-hook state must be explicit")
    policy=POLICY.read_text(encoding="utf-8")
    for marker in (
        "Notice-of-notice","Attachment-first rule","Outbound dependency rule",
        "Independent second-pass safeguard","Watchdog of the watchdog",
        "SENT ≠ DELIVERED ≠ RECEIVED ≠ ROUTED ≠ JOINED ≠ EXAMINED ≠ ACCEPTED ≠ MERITS_OUTCOME"
    ):
        if marker not in policy:
            raise SystemExit(f"policy marker missing: {marker}")
    print("consequence-risk control: OK")
    if status.get("gmail_event_arrival_hook") != "ACTIVE":
        print("advisory: real-time Gmail arrival hook is not active; CONTROL_SYSTEM_DEGRADED/fallback remains mandatory")

if __name__ == "__main__":
    main()
