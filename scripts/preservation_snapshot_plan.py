#!/usr/bin/env python3
"""Reuse a complete retained main-SHA artifact; never call it independent custody."""
from __future__ import annotations
import json
import os
from pathlib import Path
import re
import urllib.parse
import urllib.request


def plan(main_sha, event_name, event, artifacts):
    if not re.fullmatch(r"[0-9a-f]{40}", main_sha):
        raise ValueError("Invalid main SHA")
    name = "por-derecho-off-github-backup-" + main_sha
    result = {"main_sha": main_sha, "artifact_name": name, "create": "false"}
    if event_name == "workflow_run":
        run = event.get("workflow_run", {})
        if run.get("conclusion") != "success" or run.get("head_branch") != "main":
            return dict(result, reason="Not a successful main acceptance run")
        if run.get("head_sha") != main_sha:
            return dict(result, reason="Acceptance SHA has been superseded; preserve current main separately")
    elif event_name not in ("workflow_dispatch", "push"):
        raise ValueError("Unsupported preservation event")
    if not isinstance(artifacts, list):
        raise ValueError("Artifact inventory is unavailable")
    for artifact in artifacts:
        if (artifact.get("name") == name and artifact.get("expired") is False
                and artifact.get("size_in_bytes", 0) > 0
                and re.fullmatch(r"sha256:[0-9a-f]{64}", artifact.get("digest") or "")):
            return dict(result, reason="Reuse retained GitHub artifact; external custody remains separate",
                        reused_artifact_id=str(artifact["id"]))
    return dict(result, create="true", reason="No complete retained artifact for this main SHA")


def main():
    token = os.environ["GH_TOKEN"]
    repository = os.environ["GITHUB_REPOSITORY"]
    if repository != "sbu001monterecco/por-derecho":
        raise ValueError("Unexpected repository")
    def get(suffix):
        request = urllib.request.Request(
            "https://api.github.com/repos/" + repository + suffix,
            headers={"Authorization": "Bearer " + token,
                     "Accept": "application/vnd.github+json",
                     "X-GitHub-Api-Version": "2022-11-28"})
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    sha = get("/branches/main")["commit"]["sha"]
    event_name = os.environ["GITHUB_EVENT_NAME"]
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    name = "por-derecho-off-github-backup-" + sha
    inventory = get("/actions/artifacts?per_page=100&name=" + urllib.parse.quote(name))
    if inventory.get("total_count", 0) > len(inventory.get("artifacts", [])):
        raise ValueError("Artifact inventory is truncated")
    result = plan(sha, event_name, event, inventory["artifacts"])
    with open(os.environ["GITHUB_OUTPUT"], "a") as output:
        for key, value in result.items():
            output.write(f"{key}={value}\n")
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as summary:
        summary.write("### Preservation decision\n\n```json\n" + json.dumps(result, indent=2) + "\n```\n")
    print(json.dumps(result))


if __name__ == "__main__":
    main()
