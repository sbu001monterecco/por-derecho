#!/usr/bin/env python3
"""Poll the public GitHub Pages edge for the DIP 80 Ponente View."""
from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def fetch(url: str, timeout: int) -> tuple[int, str, dict[str, str]]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Por-Derecho-Pages-Verification/1.0",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read().decode("utf-8", errors="replace")
        headers = {k.lower(): v for k, v in response.headers.items()}
        return response.status, body, headers


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe", required=True)
    parser.add_argument("--attempts", type=int, default=60)
    parser.add_argument("--interval", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    probe = json.loads(Path(args.probe).read_text(encoding="utf-8"))
    base_url = probe["baseUrl"].rstrip("/") + "/"
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    last_results: list[dict[str, object]] = []

    for attempt in range(1, args.attempts + 1):
        all_ok = True
        results: list[dict[str, object]] = []
        for resource in probe["resources"]:
            path = resource["path"]
            url = base_url + path + ("&" if "?" in path else "?") + f"pv={probe['minimumSourceCommit'][:12]}"
            record: dict[str, object] = {"path": path, "url": url}
            try:
                status, body, headers = fetch(url, args.timeout)
                missing = [marker for marker in resource["markers"] if marker not in body]
                ok = status == 200 and not missing
                record.update(
                    {
                        "status": status,
                        "bytes": len(body.encode("utf-8")),
                        "missingMarkers": missing,
                        "etag": headers.get("etag"),
                        "lastModified": headers.get("last-modified"),
                        "ok": ok,
                    }
                )
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                record.update({"ok": False, "error": repr(exc)})
                ok = False
            all_ok = all_ok and ok
            results.append(record)

        last_results = results
        snapshot = {
            "probeId": probe["probeId"],
            "minimumSourceCommit": probe["minimumSourceCommit"],
            "verifiedAt": datetime.now(timezone.utc).isoformat(),
            "attempt": attempt,
            "success": all_ok,
            "resources": results,
        }
        output.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps(snapshot, indent=2, ensure_ascii=False), flush=True)
        if all_ok:
            return 0
        if attempt < args.attempts:
            time.sleep(args.interval)

    print("Public Pages did not serve all expected Ponente View markers.", flush=True)
    print(json.dumps(last_results, indent=2, ensure_ascii=False), flush=True)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
