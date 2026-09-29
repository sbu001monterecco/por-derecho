# Corporate Brain — OpenAI Platform activation runbook

This runbook intentionally leaves the raw API secret outside the repository, Drive documents, Gmail and ChatGPT transcript.

## State before activation

The Corporate Brain can operate through the connected ChatGPT/Work/Codex environment without an API key. The key is only required to switch on custom API-powered runtime components.

## One remaining owner action

1. Create/select a dedicated OpenAI Platform project named `Aweswell Corporate Brain`.
2. Configure a conservative project budget/alerts and appropriate project permissions.
3. Create a dedicated API key through the secure OpenAI setup flow.
4. Store the secret only in the runtime secret mechanism that consumes it. Do not paste it into chat, source files, Drive documents or repository variables stored in plaintext.

## Key handoff rule

The repository expects the runtime to receive a secret through the environment variable `OPENAI_API_KEY`. The raw value must never be committed or logged.

The only repository-side configuration file is `corporate_brain/runtime/.env.example`, which contains the variable name and no secret.

## Activation verification

After the secret is installed in the intended runtime environment:

```sh
python corporate_brain/runtime/preflight.py --require-key
```

Expected result:

`CORPORATE_BRAIN_RUNTIME_PREFLIGHT_GREEN`

The checker must never print or persist the key.

## Rotation / incident rule

If a key is exposed in chat, email, Drive, source control, logs or another unintended location, revoke it through OpenAI Platform and issue a replacement. Do not try to sanitize a leaked key and keep using it.

## Authority boundary

Possession of an API key does not authorise email, filing, publication, financial transactions, third-party contact, repository publication outside granted scope, or any other consequential external action.
