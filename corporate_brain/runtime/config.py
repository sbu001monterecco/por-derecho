"""Key-safe Corporate Brain runtime configuration.

This module reads environment variable *presence* only. It never logs secret
values and it contains no embedded credentials.
"""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeConfig:
    environment: str
    openai_api_key_present: bool
    private_vault_ref: str


def load_config() -> RuntimeConfig:
    key = os.getenv("OPENAI_API_KEY", "")
    return RuntimeConfig(
        environment=os.getenv("CORPORATE_BRAIN_ENV", "development"),
        openai_api_key_present=bool(key.strip()),
        private_vault_ref=os.getenv("CORPORATE_BRAIN_PRIVATE_VAULT", "external-private-source"),
    )
