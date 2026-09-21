# Outbound email duplicate-send incident — 25 August 2026

**Classification:** PUBLIC-SAFE OPERATIONAL GOVERNANCE RECORD  
**Status:** ROOT CAUSE IDENTIFIED; CONTROL UPDATED; NO CORRECTIVE EMAIL AUTHORIZED

## 1. Incident

One exact outbound email package was authorized for a single transmission. The connected mail provider accepted the first send and returned a concrete native message identifier.

Twenty-six seconds later, a second independent send action transmitted the same package again to the same recipient set. Read-back of the native Sent copies established that the subject, body, recipients and no-attachment manifest were identical.

The duplicate was not caused by:

- Gmail retrying delivery;
- a bounce or redirect;
- a draft being sent automatically;
- an attachment failure;
- recipient duplication within one message; or
- the user authorizing two transmissions.

It was caused by two separate outbound tool invocations.

## 2. Root cause

The repository rule already stated that one authorization permits at most one transmission. The operational defect was that the rule was declarative rather than atomically enforced at the tool boundary.

After the first successful provider result:

1. the authorization was not immediately represented as consumed in a one-shot execution lock;
2. the verification phase was not constrained to a read-only tool allowlist; and
3. a send action was invoked again instead of retrieving the first message by its returned identifier.

The decisive correction is therefore not merely “remember not to send twice.” It is to consume authorization before the first mutation call and mechanically prohibit every further mutating mail action for that package.

## 3. Corrective controls

The controlling addendum now requires:

- one outbound mutation call maximum per exact authorization;
- atomic `authorization_consumed`, `outbound_mutation_count = 1` and `mutation_lock = true` before the provider call;
- the lock to remain closed after success, error, timeout or uncertainty;
- read-only verification using the returned message/thread identifier or Sent-mail search;
- a pre-send search for an equivalent recent Sent message;
- a post-send duplicate-window check;
- exactly one matching Sent message before `VERIFIED AS SENT CORRECTLY` may be reported;
- no parallel send calls;
- no silent retry; and
- fresh exact authorization for any retry, correction, apology or replacement.

## 4. Files controlling the correction

- `EMAIL_SEND_EXACTLY_ONCE_EXECUTION_GUARD.md`
- `.github/governance/outbound-email-exactly-once-guard-v1.json`
- `.github/governance/test_outbound_email_exactly_once_guard.py`

The earlier authorization and sent-copy rule remains applicable:

- `EMAIL_SEND_FINAL_AUTHORIZATION_RULE.md`

## 5. Current external-communication boundary

No apology, explanation, correction or follow-up was sent automatically in response to this incident. Discovery of a duplicate does not authorize a third message.

Any external corrective communication requires a new exact package and fresh user authorization.

## 6. Privacy

This record intentionally omits names, addresses, subject text, provider message identifiers and private body content. Native evidence remains in the connected mailbox.
