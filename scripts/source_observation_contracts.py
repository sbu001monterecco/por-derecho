#!/usr/bin/env python3
"""Keep historical provenance fixed while allowing independently reviewed additions.

Historical surfaces are verified at their actual Git origin, not relabelled as
current. Owned Orion blocks remain byte-exact; prior visible text remains in
order, and the calling validator separately enforces existing links and IDs.
"""
from __future__ import annotations
from functools import lru_cache
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CONTROL = 'assets/data/caepr-caret-alberto-meeting-point-first-hop-v1.json'


class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hidden = 0
        self.words = []
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'template'):
            self.hidden += 1
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'template'):
            self.hidden -= 1
    def handle_data(self, data):
        if not self.hidden:
            self.words.extend(data.split())


def preserved_owned_page(path: str, expected: str, actual: str, marker: str) -> None:
    """Additional source/reader blocks may coexist; original framing cannot change."""
    class Element(HTMLParser):
        def __init__(self, content):
            super().__init__(convert_charrefs=False)
            self.content=content; self.offsets=[0]
            for line in content.splitlines(keepends=True):self.offsets.append(self.offsets[-1]+len(line))
            self.depth=0;self.start=None;self.tag=None;self.matches=[]
        def position_offset(self):
            line,col=self.getpos();return self.offsets[line-1]+col
        def handle_starttag(self,tag,attrs):
            if self.depth:
                if tag==self.tag:self.depth+=1
            elif dict(attrs).get('id')==marker:
                self.start=self.position_offset();self.tag=tag;self.depth=1
        def handle_endtag(self,tag):
            if self.depth and tag==self.tag:
                self.depth-=1
                if not self.depth:
                    end=self.content.index('>',self.position_offset())+1
                    self.matches.append(self.content[self.start:end])
    a,b=Element(expected),Element(actual);a.feed(expected);b.feed(actual)
    if len(a.matches)!=1 or a.matches!=b.matches:
        raise AssertionError('Owned architecture block missing, duplicated or changed: '+path)
    old,new=VisibleText(),VisibleText();old.feed(expected);new.feed(actual)
    cursor=iter(new.words)
    if not all(any(word==candidate for candidate in cursor) for word in old.words):
        raise AssertionError('Prior visible source text was removed or rewritten: '+path)


def find_frozen_origin(root: Path, control_path: str, control: dict, parser_type, normalize) -> tuple[str, dict]:
    """Find an ancestral exact-control revision reproducing every frozen surface."""
    def git(*args):return subprocess.check_output(['git',*args],cwd=root,stderr=subprocess.PIPE)
    raw=(root/control_path).read_bytes()
    revisions=git('log','--format=%H','HEAD','--',control_path).decode().splitlines()
    if len(revisions)>100:raise ValueError('Historical search requires explicit review beyond100 control revisions')
    snapshots=control['rendered_occurrence_control']['route_snapshots']
    if len(snapshots)!=18:raise ValueError('Historical source scope must retain18 surfaces')
    for revision in reversed(revisions):
        if git('show',revision+':'+control_path)!=raw:continue
        surfaces={};valid=True
        for row in snapshots:
            rel=row['route'].strip('/')+'/index.html'
            if '..' in Path(rel).parts or not (root/rel).is_file():
                raise ValueError('Current mapped source route missing or unsafe: '+rel)
            try:html=git('show',revision+':'+rel).decode('utf-8')
            except subprocess.CalledProcessError:valid=False;break
            parser=parser_type();parser.feed(html);text=normalize(' '.join(parser.parts))
            if (len(text)!=row['normalized_characters'] or hashlib.sha256(text.encode()).hexdigest()!=row['normalized_main_sha256'] or parser.inline_identity_markup or '^' in text):
                valid=False;break
            surfaces[rel]=html
        if valid:
            git('merge-base','--is-ancestor',revision,'HEAD')
            return revision,surfaces
    raise ValueError('No ancestral exact-control source reproduces all18 frozen surfaces; do not rewrite the historical record')


@lru_cache(maxsize=1)
def _frozen_surfaces():
    import ast
    source=(ROOT/'scripts/validate_alberto_meeting_point_first_hop_caret.py').read_text()
    selected=[]
    for node in ast.parse(source).body:
        if isinstance(node,(ast.Import,ast.ImportFrom)):
            if isinstance(node,ast.ImportFrom) and node.module=='source_observation_contracts':continue
            selected.append(node)
        elif isinstance(node,ast.ClassDef) and node.name=='MainSurface':selected.append(node)
        elif isinstance(node,ast.FunctionDef) and node.name=='normalize':selected.append(node)
    scope={};exec(compile(ast.Module(body=selected,type_ignores=[]),'<frozen-source-parser>','exec'),scope)
    control=json.loads((ROOT/CONTROL).read_text())
    revision,surfaces=find_frozen_origin(ROOT,CONTROL,control,scope['MainSurface'],scope['normalize'])
    print(json.dumps({'check':'historical-first-hop-origin','revision':revision,'surfaces':len(surfaces),'control_sha256':hashlib.sha256((ROOT/CONTROL).read_bytes()).hexdigest(),'scope':'Historical18-surface/130-object provenance only; not a current complete entity census. Current route/caret and browser checks remain separate.'}))
    return surfaces


def historical_surface(path: Path) -> str:
    relative=path.resolve().relative_to(ROOT).as_posix()
    return _frozen_surfaces()[relative]
