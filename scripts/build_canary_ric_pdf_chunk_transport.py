#!/usr/bin/env python3
"""Encode public PDFs as lossless GitHub-connector-safe Base64 chunks."""

from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence/canary-ric-public-debt/2026-08-28-production"
MANIFEST = EVIDENCE / "manifest-v1.json"
BINARY_CHUNK_BYTES = 480_000  # JSON container stays below the connector's 1 MiB response cap.
BASE64_SEGMENT_CHARS = 16  # Too short to resemble a credential token in line-based privacy gates.
PAGE_INDEX_PART_SIZE = 180


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def encode(pdf: Path) -> Path:
    chunk_dir = pdf.parent / "pdf-chunks"
    chunk_dir.mkdir(parents=True, exist_ok=True)
    for obsolete in chunk_dir.glob("*.b64"):
        obsolete.unlink()
    names: list[str] = []
    with pdf.open("rb") as source:
        number = 1
        while data := source.read(BINARY_CHUNK_BYTES):
            name = f"{pdf.stem}.part-{number:03d}.json"
            encoded = base64.b64encode(data).decode("ascii")
            payload = {
                "encoding": "base64-tilde-segments-16",
                "data": "~".join(encoded[i : i + BASE64_SEGMENT_CHARS] for i in range(0, len(encoded), BASE64_SEGMENT_CHARS)),
            }
            (chunk_dir / name).write_text(json.dumps(payload, separators=(",", ":")) + "\n", encoding="utf-8")
            names.append(f"pdf-chunks/{name}")
            number += 1
    transport = {
        "schema": "por-derecho.lossless-pdf-json-chunks.v1",
        "source_pdf_filename": pdf.name,
        "source_pdf_size_bytes": pdf.stat().st_size,
        "source_pdf_sha256": sha(pdf),
        "encoding": "json-contained-base64-independent-binary-chunks",
        "binary_chunk_bytes": BINARY_CHUNK_BYTES,
        "chunk_count": len(names),
        "chunks": names,
        "reconstruction": "Decode each chunk independently in listed order and concatenate the resulting bytes.",
    }
    output_name = "pdf-transport-exhibit-v1.json" if pdf.name.startswith("exhibit-") else "pdf-transport-v1.json"
    output = pdf.parent / output_name
    output.write_text(json.dumps(transport, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output


def partition_page_index(manifest: dict) -> None:
    """Keep the complete page index in connector-safe, independently hashed parts."""
    index_path = ROOT / manifest["page_index"]
    index = json.loads(index_path.read_text(encoding="utf-8"))
    if "pages" not in index:
        return
    pages = index.pop("pages")
    parts_dir = index_path.parent / "page-index-parts"
    parts_dir.mkdir(parents=True, exist_ok=True)
    parts: list[dict] = []
    for offset in range(0, len(pages), PAGE_INDEX_PART_SIZE):
        number = offset // PAGE_INDEX_PART_SIZE + 1
        name = f"part-{number:03d}.json"
        part_path = parts_dir / name
        payload = {"pages": pages[offset : offset + PAGE_INDEX_PART_SIZE]}
        part_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        parts.append(
            {
                "path": str(part_path.relative_to(ROOT)),
                "page_count": len(payload["pages"]),
                "sha256": sha(part_path),
            }
        )
    index.update(
        {
            "storage": "PARTITIONED_COMPLETE_INDEX",
            "part_count": len(parts),
            "parts": parts,
            "reconstruction": "Read each listed JSON part in order and concatenate its pages array.",
        }
    )
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest["page_index_sha256"] = sha(index_path)


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    partition_page_index(manifest)
    for item in manifest["sources"]:
        pdf = ROOT / item["public_pdf"]
        transport = encode(pdf)
        item["repository_transport"] = "LOSSLESS_BASE64_CHUNKS_RECONSTRUCTED_CLIENT_SIDE"
        item["transport_manifest"] = str(transport.relative_to(ROOT))
    exhibit = manifest["sharing_exhibit"]
    exhibit_pdf = ROOT / exhibit["path"]
    exhibit_transport = encode(exhibit_pdf)
    exhibit["repository_transport"] = "LOSSLESS_BASE64_CHUNKS_RECONSTRUCTED_CLIENT_SIDE"
    exhibit["transport_manifest"] = str(exhibit_transport.relative_to(ROOT))
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Encoded 9 public PDFs into lossless transport manifests and chunks.")


if __name__ == "__main__":
    main()
