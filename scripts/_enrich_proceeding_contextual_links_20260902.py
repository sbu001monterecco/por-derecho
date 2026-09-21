#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from html import escape
import json
import re
import unicodedata

ROOT=Path('.')
DATA=ROOT/'assets'/'data'
public=json.loads((DATA/'proceedings-master-public-v1.json').read_text(encoding='utf-8'))
routes_doc=json.loads((DATA/'proceeding-page-routes-20260902.json').read_text(encoding='utf-8'))
graph_path=DATA/'proceeding-interlink-graph-20260902.json'
graph_doc=json.loads(graph_path.read_text(encoding='utf-8'))
records=public['records']; by_id={r['Master_ID']:r for r in records}; routes=routes_doc['routes']
graph={r['master_id']:r for r in graph_doc['records']}

# Generic procedural/registry vocabulary must never create a contextual relation by itself.
STOP={
 'the','and','for','from','with','into','later','historical','history','proceeding','proceedings','matter','file','reference','court','exact','pending','linked','track','civil','criminal','judicial','direct','reported','controlled','source','appeal','review','procedure','procedural','against','concerning','related','relationship','public','official','current','status','las','los','del','de','la','el','en','y','por','para','con','sin','sobre','expediente','procedimiento','historico','historica','judicial','recurso','juzgado','audiencia','provincial','palmas','arrecife','lanzarote','tenerife','canarias',
 'diligencias','previas','docket','requires','required','require','parties','party','user','users','auto','order','judgment','sentencia','allegations','alleged','complaint','dispute','park','perimeter','record','records','identity','unverified','verified','primary','copy','document','documents','filing','filings','application','applications','decision','decisions'
}

def norm(s):
 s=unicodedata.normalize('NFD',str(s or '')); s=''.join(c for c in s if unicodedata.category(c)!='Mn').lower()
 return re.sub(r'[^a-z0-9]+',' ',s).strip()

def tokens(row):
 text=' '.join(str(row.get(k) or '') for k in ('Connection','Object_or_Purpose','Secondary_Reference'))
 return {t for t in norm(text).split() if len(t)>=4 and t not in STOP and not t.isdigit()}

def exact(a,b,key):
 x=norm(a.get(key)); y=norm(b.get(key)); return bool(x and x==y)

T={mid:tokens(r) for mid,r in by_id.items()}
ranked={mid:[] for mid in by_id}
for i,(mid,a) in enumerate(by_id.items()):
 for oid,b in list(by_id.items())[i+1:]:
  score=0; reasons=[]
  same_connection=exact(a,b,'Connection')
  shared=sorted(T[mid]&T[oid])
  # Contextual recommendations require substantive overlap or the same explicit connection label.
  # Same court/geography/stream are boosts only; same-organ navigation already has its own section.
  if not shared and not same_connection:
   continue
  if exact(a,b,'Origin_Organ'):
   score+=6; reasons.append('same_origin_organ')
  if exact(a,b,'Geography'):
   score+=2; reasons.append('same_geography')
  if exact(a,b,'Stream'):
   score+=2; reasons.append('same_stream')
  if shared:
   weight=min(12,4*len(shared)); score+=weight; reasons.append('shared_canonical_terms:'+','.join(shared[:6]))
  if same_connection:
   score+=8; reasons.append('same_connection_label')
  if score>=8:
   ranked[mid].append((score,oid,reasons)); ranked[oid].append((score,mid,reasons))

# Choose the strongest 12 for each record, then symmetrise so every contextual link has a backlink.
selected={mid:{} for mid in by_id}
for mid,items in ranked.items():
 for score,oid,reasons in sorted(items,key=lambda x:(-x[0],x[1]))[:12]:
  selected[mid][oid]={'score':score,'reasons':reasons}
for mid in list(selected):
 for oid,meta in list(selected[mid].items()):
  prior=selected[oid].get(mid)
  if not prior or meta['score']>prior['score']:
   selected[oid][mid]=meta

for mid,item in graph.items():
 formal=set(item.get('formal_related') or []); textual=set(item.get('canonical_text_cross_references') or [])
 context=[]
 for oid,meta in sorted(selected[mid].items(), key=lambda kv:(-kv[1]['score'],kv[0])):
  if oid in formal or oid in textual: continue
  context.append({'master_id':oid,'score':meta['score'],'reasons':meta['reasons']})
 item['contextual_related_navigation']=context

graph_doc['status']='RECIPROCAL_FORMAL_TEXTUAL_AND_CONTEXTUAL_NAVIGATION_EDGES'
graph_doc['boundary']='Formal related edges derive only from Parent_Master_ID and Linked_Proceedings. Textual, contextual-similarity and same-organ links are navigation aids and do not establish joinder, transfer, common parties, common knowledge, merits, causation or liability.'
graph_doc['contextual_method']='Contextual links require at least one meaningful shared canonical term from Connection/Object/Secondary_Reference or an exact non-empty Connection label. Same origin/geography/stream are boosts only. Generic procedural vocabulary is excluded; threshold >=8; strongest 12 per record then reciprocal symmetrisation.'
graph_path.write_text(json.dumps(graph_doc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def cards(mid,lang):
 rows=[]
 for edge in graph[mid].get('contextual_related_navigation',[]):
  oid=edge['master_id']; r=by_id[oid]; href='/'+routes[oid][lang]
  reason=' · '.join(edge['reasons'])
  rows.append(f"<a class='pd-proc-link' href='{escape(href)}'><code>{escape(oid)}</code><strong>{escape(r.get('Reference') or oid)}</strong><small>{escape(reason)}</small></a>")
 return ''.join(rows) or '<p class="pd-muted">—</p>'

context_re=re.compile(r"\n?<section class='pd-proc-shell' data-contextual-related-navigation='20260902'>.*?</section>\n?", re.S)
for mid in by_id:
 for lang in ('es','en'):
  p=ROOT/routes[mid][lang]/'index.html'; h=p.read_text(encoding='utf-8')
  # Regeneration is idempotent: replace any prior contextual block with the freshly scored block.
  h=context_re.sub('\n',h)
  if lang=='es':
   anchor="<section class='pd-proc-shell'><h2>Navegación: mismo órgano de origen</h2>"
   section="<section class='pd-proc-shell' data-contextual-related-navigation='20260902'><h2>Procedimientos relacionados · navegación contextual</h2><p class='pd-muted'>Enlaces calculados desde campos canónicos compartidos. Sirven para reconstruir el perímetro y descubrir expedientes vecinos, pero <strong>no</strong> prueban acumulación, identidad de partes, conexión procesal formal, conocimiento compartido, causalidad ni responsabilidad.</p><div class='pd-proc-links'>"+cards(mid,lang)+"</div></section>\n"
  else:
   anchor="<section class='pd-proc-shell'><h2>Navigation: same originating organ</h2>"
   section="<section class='pd-proc-shell' data-contextual-related-navigation='20260902'><h2>Related proceedings · contextual navigation</h2><p class='pd-muted'>Links calculated from shared canonical fields. They help reconstruct the perimeter and discover neighbouring files, but they do <strong>not</strong> prove joinder, identical parties, a formal procedural connection, shared knowledge, causation or liability.</p><div class='pd-proc-links'>"+cards(mid,lang)+"</div></section>\n"
  if anchor not in h: raise SystemExit(f'context insertion anchor missing {p}')
  p.write_text(h.replace(anchor,section+anchor,1),encoding='utf-8')

edge_count=sum(len(r.get('contextual_related_navigation',[])) for r in graph.values())//2
print('CONTEXTUAL_INTERLINK_OK',len(by_id),edge_count,'reciprocal contextual pairs')
