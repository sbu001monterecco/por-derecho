#!/usr/bin/env python3
"""Add only JSP cross-links and the source-controlled auditor lead; never publish.

Checks concern saved source integrity, not canonical completeness or truth of
allegations. Run on the isolated worker branch, then route to the integrator.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

PAGES = {
    'es': 'es/jsp-montelanza-concurso-liquidacion/index.html',
    'en': 'en/jsp-montelanza-insolvency-liquidation/index.html',
}
PROMPT = 'archive/JSP_PERIMETER_FORENSIC_MASTER_PROMPT_05SEP2026.md'
DELTA = 'assets/data/jsp-perimeter-research-delta-20260905.json'
SVG = 'assets/jsp-montelanza-authority-map-20260905.svg'
RELATED = {lang: [lang+'/montelanza-monte-lanza-sl/index.html', lang+'/asuncion-aizpurua-sanchez/index.html'] for lang in PAGES}
MARKER = 'jsp-perimeter-20260905'
AUDIT_URL = 'https://www.boe.es/borme/dias/2018/10/18/pdfs/BORME-A-2018-201-35.pdf'

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids: set[str] = set()
        self.duplicate_ids: set[str] = set()
        self.links: list[str] = []
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        fields = dict(attrs)
        identifier = fields.get('id')
        if identifier:
            if identifier in self.ids:
                self.duplicate_ids.add(identifier)
            self.ids.add(identifier)
        for attr in ('href', 'src'):
            value = fields.get(attr)
            if value:
                self.links.append(value)


def append_section(path: Path, marker: str, block: str, changed: list[str], root: Path) -> None:
    before = path.read_text(encoding='utf-8')
    if 'id="'+marker+'"' in before:
        return
    position = before.rfind('</main>')
    if position < 0:
        raise ValueError('Missing closing main: '+str(path))
    after = before[:position]+block+'\n'+before[position:]
    if after.replace(block+'\n', '', 1) != before:
        raise AssertionError('Non-additive edit')
    path.write_text(after, encoding='utf-8')
    changed.append(str(path.relative_to(root)))


def prepare(root: Path) -> list[str]:
    changed: list[str] = []
    for lang, paths in RELATED.items():
        route = '/por-derecho/'+PAGES[lang].removesuffix('index.html')
        if lang == 'es':
            heading = 'JSP: historia y dos liquidaciones distintas'
            text = 'Fincas, facultades, contraprestación y concurso JSP 440/2021. La mayoría societaria y la cadena Comunidad–CAM siguen pendientes de prueba; el vínculo no atribuye culpabilidad.'
        else:
            heading = 'JSP: history and two separate liquidations'
            text = 'Properties, authority, consideration and JSP insolvency 440/2021. Majority ownership and the Community–CAM chain remain unproved; this link does not attribute guilt.'
        block = '<section id="'+MARKER+'" class="cpn-section"><div class="shell cpn-record"><h2><a href="'+route+'">'+heading+'</a></h2><p>'+text+'</p></div></section>'
        for relative in paths:
            append_section(root/relative, MARKER, block, changed, root)
    audit = {
        'es': ('Un custodio documental adicional: auditoría JSP', 'El asiento 416588 del BORME publicado el 18 de octubre de 2018 registra la reelección de KPMG Auditores S.L. para José Sánchez Peñate S.A., hoja GC3655, el 5 de octubre. Esta función de auditoría es distinta de la entrevista histórica publicada por KPMG. No acredita que la firma auditase las transmisiones Sun Park; deben recuperarse ejercicios, alcance, informes y documentación por la vía legal procedente.'),
        'en': ('An additional records lead: JSP audit', 'BORME entry 416588, published 18 October 2018, records the reappointment of KPMG Auditores S.L. for José Sánchez Peñate S.A., sheet GC3655, on 5 October. This audit role is distinct from the historical interview published by KPMG. It does not establish that the firm audited Sun Park transfers; obtain the relevant years, scope, reports and records through the appropriate lawful route.'),
    }
    for lang, relative in PAGES.items():
        heading, text = audit[lang]
        block = '<section id="audit-custodian"><h2>'+heading+'</h2><p>'+text+' <a href="'+AUDIT_URL+'">S07 · BORME p44851, entry 416588</a></p></section>'
        append_section(root/relative, 'audit-custodian', block, changed, root)
    p = root/PROMPT
    before = p.read_text(encoding='utf-8')
    if '**S07 — JSP statutory-auditor lead.**' not in before:
        addition = '\n\n## Additional primary-source custody lead\n\n**S07 — JSP statutory-auditor lead.** BORME entry416588, published18October2018, records reappointment of KPMG Auditores SL for José Sánchez Peñate SA, GC3655, registered5October2018. Source: '+AUDIT_URL+' (PDFpage1, printed44851). Keep this formal audit role separate from the KPMG-published historical interview. Retrieve appointment terms, financial years, audit opinions and relevant working-paper custody through the lawful route. The entry does not establish that KPMG audited any Sun Park transfer or knew of any alleged irregularity. Reconcile the firm with existing canonical records rather than duplicating it.\n'
        p.write_text(before+addition, encoding='utf-8')
        changed.append(PROMPT)
    return changed


def check(root: Path) -> dict:
    delta = json.loads((root/DELTA).read_text(encoding='utf-8'))
    assert delta['role'] == 'WORKER'
    assert not any(delta['external_actions'].values()), 'False external completion'
    assert len(delta['sources']) == 11, 'Source denominator changed'
    assert len(delta['identity_dispositions']) == 21, 'Identity disposition omitted'
    assert len(delta['events_to_reconcile']) == 17, 'Date intake omitted'
    assert any('majority/de facto control' in x and 'no percentage proved' in x for x in delta['corrections'])
    assert any('Patricia is the speaker' in x for x in delta['corrections'])
    ET.parse(root/SVG)
    diagram = (root/SVG).read_text(encoding='utf-8')
    assert 'NOT proved' in diagram and '21 Jul 2021' in diagram
    prompt = (root/PROMPT).read_text(encoding='utf-8')
    assert all(('## '+str(n)+'.') in prompt for n in range(1, 16)), 'Workstream omitted'
    assert 'personally adopted Asunción statement' in prompt
    assert 'protocol 2026' in prompt and '440/2021' in prompt
    assert 'S07 — JSP statutory-auditor lead' in prompt
    required = {'history','chronology','authority','map','title-chain','estate','law','sources','research','audit-custodian'}
    parsed = {}
    for lang, relative in PAGES.items():
        txt = (root/relative).read_text(encoding='utf-8')
        parser = Links(); parser.feed(txt)
        assert not parser.duplicate_ids, 'Duplicate page IDs'
        assert required <= parser.ids, 'Missing section'
        assert ('lang="'+lang+'"') in txt
        assert '440/2021' in txt and '2015' in txt and '2018' in txt
        for target in parser.links:
            u = urlsplit(target)
            if u.scheme or u.netloc:
                continue
            path = unquote(u.path)
            if path.startswith('/por-derecho/'):
                dest = root/path[len('/por-derecho/'):]
            elif path.startswith('/'):
                dest = root/path.lstrip('/')
            else:
                dest = (root/relative).parent/path
            if not path:
                dest = root/relative
            elif path.endswith('/') or dest.is_dir():
                dest = dest/'index.html'
            dest = dest.resolve()
            assert dest.is_relative_to(root.resolve()), 'Out-of-repository link'
            assert dest.is_file(), 'Missing link target: '+target
            if u.fragment and dest == (root/relative).resolve():
                assert unquote(u.fragment) in parser.ids, 'Missing local anchor'
        parsed[lang] = {'anchors':len(parser.ids), 'links_checked':len(parser.links)}
        for related in RELATED[lang]:
            t = (root/related).read_text(encoding='utf-8')
            assert t.count('id="'+MARKER+'"') == 1, 'Missing/duplicate reciprocal link'
            assert '/por-derecho/'+relative.removesuffix('index.html') in t
    paths = [PROMPT, DELTA, SVG, *PAGES.values(), *(p for values in RELATED.values() for p in values)]
    return {
        'control_id':'PD-JSP-RESEARCH-20260905',
        'result':'PASS_SCOPED_SOURCE_LINK_CHECKS_ONLY',
        'prompt_words':len(prompt.split()),
        'sources':len(delta['sources']),
        'identity_disposition_groups':len(delta['identity_dispositions']),
        'event_intake_rows':len(delta['events_to_reconcile']),
        'reciprocal_existing_pages':4,
        'page_checks':parsed,
        'hashes':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in paths},
        'not_certified':['canonical registration complete','full corpus scanned','rendered browser QA','repository-wide preservation/publication CI','merged to main','deployed','live verified'],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--report',type=Path)
    args = parser.parse_args()
    changed = [] if args.check else prepare(args.root)
    result = check(args.root)
    result['changed_files'] = changed
    payload = json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(payload,encoding='utf-8')
    print(payload)

if __name__ == '__main__':
    main()
