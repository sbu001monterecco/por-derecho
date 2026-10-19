#!/usr/bin/env python3
"""Read-only scoped regression checks. No network, mutation, or CI bypass.
Run from repository root with --base <the actual comparison commit>.
The report distinguishes pre-existing broken links from introduced regressions.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
import pathlib
import posixpath
import subprocess
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

PAIRS = [
 ('es/concurso-36-2012-separacion-administrador-concursal-rpl-3304-2025/index.html', 'en/insolvency-36-2012-administrator-removal-rpl-3304-2025/index.html', {'removal-thesis','present-purpose','adverse-decisions','evidence-partition','dated-gaps','accounts-test','authority-test','ownership-test'}),
 ('es/concurso-36-2012-oposicion-ac-apelacion-lpb-septiembre-2026/index.html', 'en/insolvency-36-2012-ac-opposition-lpb-appeal-september-2026/index.html', {'r33-operational-comparison','notice-followthrough','procedural-position','methodology-after-findings'}),
 ('es/cgpj-supervision-masa-activa/index.html', 'en/cgpj-insolvency-estate-supervision/index.html', {'authority-implementation','official-record-chain','institutional-scope','ownership-and-continuing-harm'}),
]
MAP = 'assets/data/r33-procedural-utility-map-v1.json'
SOURCES = [
 'evidence/insolvency-36-2012/rpl-3304-2025/R33-oposicion-ac-apelacion-lpb-septiembre-2026-controlled-extracts.md',
 'evidence/insolvency-36-2012/concurso-autos/pdfs/R33-ac-oposicion-apelacion-lpb-septiembre-2026.pdf',
]

class Census(HTMLParser):
    def __init__(self, text: str):
        super().__init__(convert_charrefs=True)
        self.ids = []; self.links = []; self.media = []; self.markers = set()
        self.tags = collections.Counter(); self.visible = []; self.hidden = 0
        self.feed(text); self.close()
    def handle_starttag(self, tag, attrs):
        a = dict(attrs); self.tags[tag] += 1
        if tag in ('script','style'): self.hidden += 1
        if a.get('id'): self.ids.append(a['id'])
        if a.get('data-ac-clarity'): self.markers.add(a['data-ac-clarity'])
        if tag in ('a','link') and a.get('href'): self.links.append(a['href'])
        if tag in ('img','iframe','video','audio','source','script') and a.get('src'):
            self.media.append((tag,a['src']))
    def handle_endtag(self, tag):
        if tag in ('script','style') and self.hidden: self.hidden -= 1
    def handle_data(self, data):
        if not self.hidden: self.visible.append(data)
    @property
    def words(self): return len(' '.join(self.visible).split())

def git_bytes(ref: str, path: str) -> bytes:
    return subprocess.check_output(['git','show',f'{ref}:{path}'], stderr=subprocess.PIPE)

def link_target(page: str, href: str):
    u = urlsplit(href)
    if u.scheme or u.netloc: return None
    p = unquote(u.path)
    if not p: target = page
    elif p.startswith('/'):
        target = p.lstrip('/')
        if target.startswith('por-derecho/'): target = target[len('por-derecho/'):]
    else: target = posixpath.normpath(posixpath.join(posixpath.dirname(page), p))
    if target.startswith('../'): return ('OUTSIDE_REPOSITORY', '')
    obj = pathlib.Path(target)
    if p.endswith('/') or obj.is_dir(): target = target.rstrip('/') + '/index.html'
    return target, unquote(u.fragment)

def main() -> int:
    ap = argparse.ArgumentParser(); ap.add_argument('--base',required=True)
    ap.add_argument('--report',default='ac-removal-clarity-report.json'); args = ap.parse_args()
    subprocess.run(['git','rev-parse','--verify',args.base+'^{commit}'], check=True, stdout=subprocess.DEVNULL)
    result = {'control':'PD-AC-REMOVAL-CLARITY-20260928','base':args.base,
              'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
              'checks':[],'census':{},'preexisting_link_warnings':[],'failures':[]}
    def check(ok, label, detail=None):
        result['checks'].append({'check':label,'pass':bool(ok),'detail':detail})
        if not ok: result['failures'].append(label)
    parsed = {}; texts = {}; previous = {}
    for es,en,required in PAIRS:
        for path,lang in ((es,'es'),(en,'en')):
            text = pathlib.Path(path).read_text(encoding='utf-8'); old = git_bytes(args.base,path).decode('utf-8')
            cur = Census(text); before = Census(old); parsed[path]=cur; texts[path]=text; previous[path]=before
            check(f'lang="{lang}"' in text, f'language:{path}')
            check(len(cur.ids)==len(set(cur.ids)), f'unique-anchors:{path}')
            check(set(before.ids).issubset(cur.ids),f'old-anchors-preserved:{path}',sorted(set(before.ids)-set(cur.ids)))
            check(not (collections.Counter(before.media)-collections.Counter(cur.media)),f'old-media-preserved:{path}')
            check(required.issubset(cur.markers),f'bilingual-clarity-markers:{path}',sorted(required-cur.markers))
            check(cur.words >= before.words, f'no-net-visible-word-loss:{path}',[before.words,cur.words])
            check('"' not in ''.join(cur.ids),f'anchor-syntax:{path}')
            result['census'][path]={'before_words':before.words,'after_words':cur.words,'before_tags':dict(before.tags),'after_tags':dict(cur.tags),'before_anchors':len(before.ids),'after_anchors':len(cur.ids),'before_media':len(before.media),'after_media':len(cur.media),'sha256':hashlib.sha256(text.encode()).hexdigest()}
            for href in set(cur.links + [x[1] for x in cur.media]):
                target = link_target(path,href)
                if target is None: continue
                filename,fragment = target; exists=pathlib.Path(filename).is_file()
                # Query-router fragments are not static DOM anchors.
                anchor_ok=True
                if exists and fragment and pathlib.Path(filename).suffix=='.html' and '=' not in fragment:
                    doc = parsed.get(filename) or Census(pathlib.Path(filename).read_text(encoding='utf-8'))
                    anchor_ok = fragment in doc.ids
                if not exists or not anchor_ok:
                    existed = href in before.links or href in [x[1] for x in before.media]
                    row={'page':path,'href':href,'target':filename,'file_exists':exists,'anchor_exists':anchor_ok}
                    if existed: result['preexisting_link_warnings'].append(row)
                    else: check(False,f'new-link:{path}:{href}',row)
    for path in SOURCES:
        check(git_bytes(args.base,path)==pathlib.Path(path).read_bytes(),f'primary-source-unchanged:{path}')
    old_map=json.loads(git_bytes(args.base,MAP)); new_map=json.loads(pathlib.Path(MAP).read_text())
    for key,value in old_map.items(): check(new_map.get(key)==value,f'existing-map-field-preserved:{key}')
    ext=new_map['editorial_revision']; ids={x['id'] for x in new_map['issues']}
    check(set(ext['issue_controls'])==ids,'all-seven-issue-controls')
    check(len(ids)==7,'seven-original-issues')
    check(set(ext['evidence_states'])=={'court_record_verified','submitted_admission_pending','externally_preserved','unverified'},'four-evidence-states')
    for key,control in ext['issue_controls'].items():
        check(control['pleaded_paragraph'] is None,f'no-invented-pleading-paragraph:{key}')
        check(set(control['contrary_record'])=={'es','en'},f'bilingual-contrary-record:{key}')
        check(set(control['requested_outcome'])=={'es','en'},f'bilingual-remedy:{key}')
        for lang,routes in control['ground_routes'].items():
            for route in routes:
                filename,fragment=link_target('index.html',route)
                check(pathlib.Path(filename).is_file() and fragment in (parsed.get(filename) or Census(pathlib.Path(filename).read_text())).ids,f'map-ground-route:{key}:{lang}:{fragment}')
    for path,metric,findings in [(PAIRS[1][0],'id="maquina-verdad-visual"','id="paso-forense-procesal"'),(PAIRS[1][1],'id="truth-machine-visual"','id="forensic-prosecutorial-pass"')]:
        text=texts[path]
        check(text.index(metric)>text.index(findings),f'methodology-after-findings:{path}')
        for number in ('276/276','482/482','179/276'): check(number in text,f'metric-preserved:{path}:{number}')
    check('declaración probatoria del propio' not in texts[PAIRS[1][0]],'no-sworn-statement-mischaracterisation-es')
    check('evidential statement by the Insolvency Administrator' not in texts[PAIRS[1][1]],'no-sworn-statement-mischaracterisation-en')
    check('id="historia-separacion"' in texts[PAIRS[0][0]],'spanish-history-anchor')
    check('id="removal-history"' in texts[PAIRS[0][1]],'english-history-anchor')
    result['status']='PASS' if not result['failures'] else 'FAIL'
    pathlib.Path(args.report).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'head':result['head'],'checks':len(result['checks']),'failures':result['failures'],'preexisting_link_warnings':len(result['preexisting_link_warnings'])},ensure_ascii=False))
    for f in result['failures']: print('FAIL:',f)
    return 0 if not result['failures'] else 1
if __name__=='__main__': sys.exit(main())
