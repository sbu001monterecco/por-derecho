#!/usr/bin/env python3
"""Stage an additive CNMV update from the verified public kit.

Default: dry-run. No network, git push, merge, email or deployment.
Actual writes require --apply --confirm-active-integrator. Run repository CI and
live verification separately. An absent asset or source page aborts before writes.
"""
from __future__ import annotations
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil

DATA_PATH = 'assets/data/cnmv-september-2026.json'
MARKER = 'cnmv-20260904'


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def relative(target: Path, source_page: Path) -> str:
    return Path(os.path.relpath(target, source_page.parent)).as_posix()


def anchor_link(target_page: Path, source_page: Path) -> str:
    value = relative(target_page.parent, source_page)
    return value.rstrip('/') + '/#' + MARKER


def render_fragment(data: dict, lang: str, page: Path, repo: Path) -> str:
    c = data['copy'][lang]
    assets = repo / data['asset_directory']
    def asset(name: str) -> str:
        return esc(relative(assets / name, page))
    pieces = [f'<section id="{MARKER}" class="section pd-cnmv-update" aria-labelledby="{MARKER}-title">',
        '<style>.pd-cnmv-update .pd-cnmv-wrap{max-width:1180px;margin:auto;padding:1rem}.pd-cnmv-update .pd-cnmv-grid{display:grid;grid-template-columns:1fr 1fr;gap:1.4rem}.pd-cnmv-update article{min-width:0;padding:1rem;border:1px solid #ccd4d7;background:#fff}.pd-cnmv-update img{width:100%;height:auto;border:1px solid #ddd}.pd-cnmv-update figure{margin:1rem 0}.pd-cnmv-update details{margin:1rem 0}.pd-cnmv-update summary{cursor:pointer;font-weight:700}.pd-cnmv-update .pd-cnmv-boundary{border-left:5px solid #a36a25;padding:1rem;background:#f8f5ee}@media(max-width:720px){.pd-cnmv-update .pd-cnmv-grid{grid-template-columns:1fr}}</style>',
        '<div class="pd-cnmv-wrap">',
        f'<p>CNMV · 4 SEP 2026 · 2026149422 / 2026114903</p><h2 id="{MARKER}-title">{esc(c["title"])}</h2>']
    for field in ['lead', 'supervision', 'comparator', 'request_gap', 'sent_bridge']:
        cls = ' class="pd-cnmv-boundary"' if field == 'request_gap' else ''
        pieces.append(f'<p{cls}>{esc(c[field])}</p>')
    pieces.append(f'<p><a href="{asset("cnmv-2026-05-06-email-extract-es.txt")}">CNMV · 6 MAY 2026 · extracto / extract</a> · <a href="{asset("cnmv-2026-08-27-email-extract-es.txt")}">CNMV · 27 AUG 2026 · extracto / extract</a></p>')
    pieces.append(f'<h3>{esc(c["documents_title"])}</h3><p>{esc(c["privacy"])}</p><div class="pd-cnmv-grid">')
    for item in data['notices'][:2]:
        pieces.extend([f'<article><h4>{esc(item["date"])} · CNMV {esc(item["outgoing"])}</h4>',
            f'<p>{esc(item["meaning"][lang])}</p>',
            f'<p><a href="{asset(item["pdf"])}">PDF</a> · <a href="{asset(item["transcript"])}">Texto ES</a></p>'])
        for number in range(1, item['pages'] + 1):
            image = item['image_prefix'] + str(number) + '.png'
            label = f'CNMV {item["date"]}, {number}/{item["pages"]} — redacted / expurgado'
            pieces.append(f'<figure><a href="{asset(image)}"><img loading="lazy" src="{asset(image)}" alt="{esc(label)}"></a><figcaption>{esc(label)}</figcaption></figure>')
        pieces.append('</article>')
    pieces.append('</div>')
    feb = data['notices'][2]
    pieces.append(f'<details><summary>CNMV · 20 FEB 2026 · 2026035232</summary><p>{esc(feb["meaning"][lang])} <a href="{asset(feb["pdf"])}">PDF · 2 pp.</a></p></details>')
    pieces.append(f'<details><summary>{esc(c["requests_title"])}</summary><ol>')
    for request in data['requests']:
        pieces.append('<li>' + esc(request[lang]) + '</li>')
    pieces.append('</ol></details>')
    for field in ['advisers', 'orion_limit', 'allegations']:
        pieces.append('<p>' + esc(c[field]) + '</p>')
    pieces.append(f'<h3>{esc(c["sources_title"])}</h3><ul>')
    for source in data['public_sources']:
        pieces.append(f'<li><a href="{esc(source["url"])}">{esc(source["label"])}</a></li>')
    for route in data['reciprocal_routes'][lang]:
        target = repo / route
        pieces.append(f'<li><a href="{esc(relative(target.parent, page))}/">{esc(target.parent.name)}</a></li>')
    pieces.append(f'<li><a href="{asset("cnmv-record.json")}">Fuentes / sources · chronology · relationships · gaps</a></li>')
    pieces.append(f'<li><a href="{asset("redaction-manifest.json")}">Expurgo / redaction · SHA-256</a></li></ul></div></section>')
    return '\n'.join(pieces)


def build_plan(repo: Path, kit: Path) -> tuple[dict[Path, str], dict]:
    data = json.loads((repo / DATA_PATH).read_text(encoding='utf-8'))
    manifest = json.loads((kit / 'SHA256-manifest.json').read_text(encoding='utf-8'))
    for name, detail in manifest.items():
        if Path(name).name != name:
            raise ValueError('Non-flat asset path rejected')
        source = kit / name
        if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != detail['sha256']:
            raise ValueError(f'Missing or mismatched public asset: {name}')
    for item in data['notices']:
        expected = [item['pdf'], item['transcript']] + [item['image_prefix'] + str(n) + '.png' for n in range(1, item['pages'] + 1)]
        if any(name not in manifest for name in expected):
            raise ValueError('Incomplete notice gallery')
        if manifest[item['pdf']]['sha256'] != item['public_sha256']:
            raise ValueError('PDF differs from the source-verified public derivative')
    for name in ['cnmv-record.json', 'redaction-manifest.json', 'cnmv-2026-05-06-email-extract-es.txt', 'cnmv-2026-08-27-email-extract-es.txt']:
        if name not in manifest:
            raise ValueError(f'Required source missing: {name}')
    routes = list(data['canonical_routes'].values()) + sum(data['reciprocal_routes'].values(), [])
    existing = {}
    for route in routes:
        page = repo / route
        if not page.is_file():
            raise ValueError(f'Canonical source page not found: {route}')
        text = page.read_text(encoding='utf-8')
        if not re.search(r'<main\b[^>]*>', text):
            raise ValueError(f'No main insertion point: {route}')
        existing[page] = text
    plan = {}
    for lang, route in data['canonical_routes'].items():
        page = repo / route
        old = existing[page]
        if f'id="{MARKER}"' not in old:
            fragment = render_fragment(data, lang, page, repo)
            plan[page] = re.sub(r'(<main\b[^>]*>)', lambda m: m.group(1) + '\n' + fragment + '\n', old, count=1)
        for source_route in data['reciprocal_routes'][lang]:
            source_page = repo / source_route
            old_source = existing[source_page]
            if 'data-cnmv-20260904-link' in old_source:
                continue
            link = anchor_link(page, source_page)
            banner = f'<aside class="section" data-cnmv-20260904-link><div class="shell"><a href="{esc(link)}">{esc(data["copy"][lang]["link_label"])}</a></div></aside>'
            plan[source_page] = re.sub(r'(<main\b[^>]*>)', lambda m: m.group(1) + '\n' + banner + '\n', old_source, count=1)
    destination = repo / data['asset_directory']
    for name, detail in manifest.items():
        target = destination / name
        if target.exists() and hashlib.sha256(target.read_bytes()).hexdigest() != detail['sha256']:
            raise ValueError(f'Refusing to overwrite different existing asset: {target}')
    return plan, data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', type=Path, required=True)
    parser.add_argument('--assets-dir', type=Path, required=True, help='Extracted public kit; not unredacted originals')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--confirm-active-integrator', action='store_true')
    args = parser.parse_args()
    repo, kit = args.repo_root.resolve(), args.assets_dir.resolve()
    plan, data = build_plan(repo, kit)
    print(json.dumps({'mode': 'apply' if args.apply else 'dry-run', 'pages': [str(p.relative_to(repo)) for p in plan], 'assets': data['asset_directory'], 'still_requires_mapping': data['additional_route_mapping_required'], 'deployment': 'NOT_PERFORMED'}, indent=2))
    if not args.apply:
        return
    if not args.confirm_active_integrator:
        raise SystemExit('Writes require the active integrator confirmation; no files changed.')
    manifest = json.loads((kit / 'SHA256-manifest.json').read_text(encoding='utf-8'))
    destination = repo / data['asset_directory']
    destination.mkdir(parents=True, exist_ok=True)
    for name in list(manifest) + ['SHA256-manifest.json']:
        target = destination / name
        if not target.exists():
            shutil.copy2(kit / name, target)
    for page, text in plan.items():
        temporary = page.with_name(page.name + '.cnmv-tmp')
        temporary.write_text(text, encoding='utf-8')
        temporary.replace(page)
    print('Local materialisation complete. No merge/deployment. Run canonical mapping, repository CI and live verification separately.')


if __name__ == '__main__':
    main()
