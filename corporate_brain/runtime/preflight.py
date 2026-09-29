#!/usr/bin/env python3
"""Corporate Brain runtime preflight.

No API call is made. The script validates that the runtime can receive the
OpenAI secret through the environment without exposing it.
"""
from __future__ import annotations

import argparse

try:
    from .config import load_config
except ImportError:  # direct script execution
    from config import load_config


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-key", action="store_true")
    args = parser.parse_args()

    cfg = load_config()
    if args.require_key and not cfg.openai_api_key_present:
        print("CORPORATE_BRAIN_RUNTIME_PREFLIGHT_ORANGE: OPENAI_API_KEY not installed")
        return 2

    if cfg.openai_api_key_present:
        print("CORPORATE_BRAIN_RUNTIME_PREFLIGHT_GREEN")
    else:
        print("CORPORATE_BRAIN_RUNTIME_KEY_READY: secret intentionally absent")

    print(f"environment={cfg.environment}")
    print(f"private_vault_ref={cfg.private_vault_ref}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
