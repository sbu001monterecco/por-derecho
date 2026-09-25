#!/usr/bin/env python3
"""Render AM357 reciprocal links as GitHub-Project-Pages-safe URLs.

The evidence matrix stores canonical conceptual routes beginning at ``/en`` or
``/es``.  Those values are useful for route comparison, but copying them into
HTML would escape the ``/por-derecho`` project prefix in a browser.  This
builder preserves the matrix as the single semantic source and renders each
endpoint-to-endpoint link relative to its source page.
"""

from __future__ import annotations

import argparse
import json
import posixpath
import re
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "assets/data/alberto-meeting-point-357-multidirectional-evidence-v1.json"
ANCHOR_RE = re.compile(r'<a\b(?=[^>]*\bdata-am357-edge-id=")[^>]*>', re.IGNORECASE)
ATTR_RE = re.compile(r'\b([\w:-]+)="([^"]*)"')
HREF_RE = re.compile(r'\bhref="[^"]*"')
EXPECTED_NODE_COUNT = 9
EXPECTED_EDGE_COUNT = 13
EXPECTED_RENDERED_LINK_COUNT = EXPECTED_EDGE_COUNT * 2 * 2


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def route_to_file(route: str) -> Path:
    parsed = urlsplit(route)
    if parsed.scheme or parsed.netloc or not parsed.path.startswith("/"):
        fail(f"matrix route is not a canonical local route: {route}")
    relative = parsed.path.lstrip("/")
    if parsed.path.endswith("/"):
        relative += "index.html"
    path = (ROOT / relative).resolve()
    try:
        path.relative_to(ROOT.resolve())
    except ValueError:
        fail(f"matrix route escapes the repository: {route}")
    return path


def relative_href(source_route: str, target_route: str) -> str:
    source = urlsplit(source_route)
    target = urlsplit(target_route)
    if not source.path.endswith("/") or not target.path.endswith("/"):
        fail(f"AM357 page routes must end in '/': {source_route} -> {target_route}")
    rendered = posixpath.relpath(
        target.path.lstrip("/"),
        start=source.path.lstrip("/"),
    )
    if rendered == ".":
        rendered = "./"
    elif not rendered.endswith("/"):
        rendered += "/"
    if target.query:
        rendered += f"?{target.query}"
    if target.fragment:
        rendered += f"#{target.fragment}"
    return rendered


def render_page(
    text: str,
    *,
    node_id: str,
    language: str,
    source_route: str,
    incident: dict[str, str],
    node_routes: dict[str, dict[str, str]],
) -> tuple[str, int]:
    seen: list[str] = []

    def replace(anchor_match: re.Match[str]) -> str:
        anchor = anchor_match.group(0)
        attrs = dict(ATTR_RE.findall(anchor))
        edge_id = attrs.get("data-am357-edge-id", "")
        if edge_id not in incident:
            fail(f"{node_id} {language} contains unexpected reciprocal edge {edge_id!r}")
        peer = incident[edge_id]
        if attrs.get("data-am357-edge-peer") != peer:
            fail(
                f"{node_id} {language} {edge_id} peer drift: "
                f"{attrs.get('data-am357-edge-peer')!r} != {peer!r}"
            )
        if "href" not in attrs:
            fail(f"{node_id} {language} {edge_id} has no href")
        target_route = node_routes[peer][language]
        replacement = f'href="{relative_href(source_route, target_route)}"'
        rendered, replacements = HREF_RE.subn(replacement, anchor, count=1)
        if replacements != 1:
            fail(f"{node_id} {language} {edge_id} href replacement was not unique")
        seen.append(edge_id)
        return rendered

    rendered = ANCHOR_RE.sub(replace, text)
    if len(seen) != len(set(seen)) or set(seen) != set(incident):
        fail(
            f"{node_id} {language} reciprocal-edge census drift: "
            f"actual={seen}, expected={sorted(incident)}"
        )
    return rendered, len(seen)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if any rendered page differs instead of writing it",
    )
    args = parser.parse_args()

    matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    nodes = matrix.get("nodes") or []
    edges = matrix.get("edges") or []
    if len(nodes) != EXPECTED_NODE_COUNT or len(edges) != EXPECTED_EDGE_COUNT:
        fail(f"matrix census is not {EXPECTED_NODE_COUNT} nodes / {EXPECTED_EDGE_COUNT} edges")

    node_routes: dict[str, dict[str, str]] = {}
    for node in nodes:
        node_id = node.get("node_id")
        routes = node.get("primary_routes")
        if not isinstance(node_id, str) or not isinstance(routes, dict) or set(routes) != {"es", "en"}:
            fail(f"malformed node route record: {node!r}")
        node_routes[node_id] = routes
    if len(node_routes) != EXPECTED_NODE_COUNT:
        fail("matrix node IDs are not unique")

    incident_by_node: dict[str, dict[str, str]] = {node_id: {} for node_id in node_routes}
    seen_edges: set[str] = set()
    for edge in edges:
        edge_id = edge.get("edge_id")
        source = edge.get("from")
        target = edge.get("to")
        if not all(isinstance(value, str) for value in (edge_id, source, target)):
            fail(f"malformed edge record: {edge!r}")
        if edge_id in seen_edges or source not in node_routes or target not in node_routes or source == target:
            fail(f"invalid or duplicate matrix edge: {edge!r}")
        seen_edges.add(edge_id)
        incident_by_node[source][edge_id] = target
        incident_by_node[target][edge_id] = source

    changed: list[Path] = []
    rendered_count = 0
    for node_id, routes in node_routes.items():
        for language in ("es", "en"):
            source_route = routes[language]
            source_path = route_to_file(source_route)
            if not source_path.is_file():
                fail(f"source page does not exist: {source_path.relative_to(ROOT)}")
            original = source_path.read_text(encoding="utf-8")
            rendered, count = render_page(
                original,
                node_id=node_id,
                language=language,
                source_route=source_route,
                incident=incident_by_node[node_id],
                node_routes=node_routes,
            )
            rendered_count += count
            if rendered != original:
                changed.append(source_path)
                if not args.check:
                    source_path.write_text(rendered, encoding="utf-8")

    if rendered_count != EXPECTED_RENDERED_LINK_COUNT:
        fail(
            f"rendered reciprocal-link census is {rendered_count}, "
            f"expected {EXPECTED_RENDERED_LINK_COUNT}"
        )
    if args.check and changed:
        listed = ", ".join(str(path.relative_to(ROOT)) for path in changed)
        fail(f"AM357 project-safe link rendering is stale in {len(changed)} files: {listed}")
    action = "verified" if args.check else "rendered"
    print(
        f"PASS: {action} {rendered_count} project-safe reciprocal links "
        f"across {EXPECTED_NODE_COUNT * 2} bilingual endpoint pages"
    )


if __name__ == "__main__":
    main()
