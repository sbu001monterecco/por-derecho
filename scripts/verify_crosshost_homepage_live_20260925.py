#!/usr/bin/env python3
from pathlib import Path
import hashlib
import sys
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("en/index.html", "es/index.html", "en/future/index.html", "es/futuro/index.html")
HOSTS = {
    "github": "https://sbu001monterecco.github.io/por-derecho/",
    "gitlab": "https://por-derecho-setup-or-gitlab-setup-c2b10f.gitlab.io/",
}
ATTEMPTS = 12
SLEEP = 15

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

expected = {rel: sha((ROOT / rel).read_bytes()) for rel in PAGES}
errors = []

for host, base in HOSTS.items():
    for rel in PAGES:
        wanted = expected[rel]
        last = None
        for attempt in range(ATTEMPTS):
            try:
                req = urllib.request.Request(base + rel, headers={"User-Agent": "ProjectSunRock-Parity/1"})
                with urllib.request.urlopen(req, timeout=30) as response:
                    body = response.read()
                got = sha(body)
                last = f"http=200 sha256={got}"
                if got == wanted:
                    break
            except Exception as exc:
                last = f"error={exc}"
            if attempt + 1 < ATTEMPTS:
                time.sleep(SLEEP)
        else:
            errors.append(f"{host} {rel}: expected {wanted}; last {last}")

if errors:
    print("CROSS-HOST HOMEPAGE PARITY: FAIL")
    for error in errors:
        print("-", error)
    sys.exit(1)

print("CROSS-HOST HOMEPAGE PARITY: PASS")
for rel, digest in expected.items():
    print(rel, digest)
