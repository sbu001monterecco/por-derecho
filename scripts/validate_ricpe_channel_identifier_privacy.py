#!/usr/bin/env python3
"""Fail closed if the private RICPE communication identifier is public."""

from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FINGERPRINT = "e53bda34973e530520bde39648768a1e32a358d8984294b21258789faebe6a24"
UUID_RE = re.compile(
    r"(?<![0-9a-f])[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
    r"[89ab][0-9a-f]{3}-[0-9a-f]{12}(?![0-9a-f])",
    re.IGNORECASE,
)

TEXT_REQUIRED = [
    Path("evidence/ricpe-cnmv/2026-08-27/resolution.txt"),
    Path("CURRENT_HANDOVER_RICPE_HNT_GC836_TREASURY_21AUG2026.md"),
    Path("archive/THREAD_DELETION_AUDIT_CRITICAL_STATUS_UPDATE_21AUG2026.md"),
]
PUBLIC_PDF = Path(
    "evidence/ricpe-cnmv/2026-08-27/"
    "RICPE_Canal_Etico_Certificado_Resolucion_27AGO2026_PUBLICO_REDACTADO.pdf"
)
PUBLIC_ARTIFACTS = {
    PUBLIC_PDF: "1571939659af5df4891157958ebfc041748768d96a70bdf45aa6c3e247c65470",
    Path("evidence/ricpe-cnmv/2026-08-27/resolution-pages-public-redacted/page-1.jpg"): "a93c14b5b0259e845023967d943f7ae91b34e9b3e8e44370fa940fe01a7c64ed",
    Path("evidence/ricpe-cnmv/2026-08-27/resolution-pages-public-redacted/page-2.jpg"): "952d2860c98c2be5dd132d089f62040c103387b174eb402785d169474639b0bc",
    Path("evidence/ricpe-cnmv/2026-08-27/resolution-pages-public-redacted/page-3.jpg"): "1060eae25e58f889126a39821a0754aaf7bc04bafb7998824f2b60c30785f9bc",
    Path("evidence/ricpe-cnmv/2026-08-27/resolution-pages-public-redacted/page-4.jpg"): "3bcf8bd19c4fdfb7483c639cc6cb2b8b25849f9c324d22c5d931133b4f278af2",
    Path("evidence/ricpe-cnmv/2026-08-27/resolution-pages-public-redacted/page-5.jpg"): "95a29aafd4df02b83d1b8536706cdb4d462e930722af65460ac84e793e560b0e",
    Path("evidence/ricpe-cnmv/2026-08-27/resolution-pages-public-redacted/page-6.jpg"): "b16e9b2b3210c9f21b970c81caf5b6f0ae8fe43ddb556aad5efe74c870a08589",
}
OBSOLETE_PUBLIC_PATHS = [
    Path(
        "evidence/ricpe-cnmv/2026-08-27/"
        "RICPE_Canal_Etico_Certificado_Resolucion_27AGO2026.pdf"
    ),
    Path("evidence/ricpe-cnmv/2026-08-27/resolution-pages"),
]
BANNED_BINARY_HASHES = {
    "db9979715cac4aeb8ded81a998227cfd894144dcd0a50fe81d4b1369904c9bb4",
    "d3422fdb040aecefc79e9ae4d766f129917c15fe67adbf01f22886a180f0d08d",
}


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_private_identifier(candidate: str) -> bool:
    return digest(candidate.lower().encode("utf-8")) == PUBLIC_FINGERPRINT


def private_matches(text: str) -> list[str]:
    return [value for value in UUID_RE.findall(text) if is_private_identifier(value)]


errors: list[str] = []

for relative in TEXT_REQUIRED:
    path = ROOT / relative
    if not path.exists():
        errors.append(f"missing controlled text file: {relative}")
        continue
    text = path.read_text(encoding="utf-8")
    if PUBLIC_FINGERPRINT not in text:
        errors.append(f"approved public fingerprint absent from {relative}")

for relative in OBSOLETE_PUBLIC_PATHS:
    if (ROOT / relative).exists():
        errors.append(f"obsolete unredacted public path still exists: {relative}")

for relative, expected_hash in PUBLIC_ARTIFACTS.items():
    path = ROOT / relative
    if not path.is_file():
        errors.append(f"missing controlled public derivative: {relative}")
        continue
    actual_hash = digest(path.read_bytes())
    if actual_hash != expected_hash:
        errors.append(
            f"controlled public derivative hash mismatch: {relative} "
            f"({actual_hash} != {expected_hash})"
        )

tracked = subprocess.check_output(
    ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
    cwd=ROOT,
).split(b"\0")
for encoded_relative in tracked:
    if not encoded_relative:
        continue
    relative = encoded_relative.decode("utf-8")
    path = ROOT / relative
    try:
        data = path.read_bytes()
    except OSError:
        continue
    if digest(data) in BANNED_BINARY_HASHES:
        errors.append(f"known unsafe RICPE binary present in current tree: {relative}")
    if len(data) > 8_000_000:
        continue
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        continue
    if private_matches(text):
        errors.append(f"private RICPE communication identifier exposed in {relative}")

pdftotext = shutil.which("pdftotext")
if pdftotext is None:
    errors.append("pdftotext is required for fail-closed public-PDF inspection")
elif (ROOT / PUBLIC_PDF).is_file():
    result = subprocess.run(
        [pdftotext, "-layout", str(ROOT / PUBLIC_PDF), "-"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        errors.append("controlled public PDF could not be text-extracted")
    else:
        if private_matches(result.stdout):
            errors.append("private RICPE communication identifier remains in public PDF")
        if "ID PRIVADO REDACTADO" not in result.stdout:
            errors.append("public PDF lacks the visible private-ID redaction label")

resolution = (ROOT / TEXT_REQUIRED[0]).read_text(encoding="utf-8")
if "Correlación pública (SHA-256 del código privado)" not in resolution:
    errors.append("public resolution lacks the privacy-safe correlation label")
if "Código de comunicación:" in resolution:
    errors.append("public resolution contains the prohibited exact-code label")

index = (ROOT / "evidence/ricpe-cnmv/2026-08-27/index.html").read_text(
    encoding="utf-8"
)
if PUBLIC_PDF.name not in index or "identificador privado redactado" not in index:
    errors.append("public evidence page does not identify and link the redacted derivative")

if errors:
    print("RICPE CHANNEL IDENTIFIER PRIVACY: FAIL", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

print("RICPE CHANNEL IDENTIFIER PRIVACY: PASS")
print("- approved fingerprint present in all three controlled text files")
print("- obsolete unredacted PDF/image paths absent from the current tree")
print("- redacted PDF and six public renders match their controlled hashes")
print("- current-tree text and extracted public-PDF text contain no protected identifier")
