#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'assets'/'data'
G=json.loads((DATA/'proceeding-interlink-graph-20260902.json').read_text(encoding='utf-8'))
R=json.loads((DATA/'proceeding-page-routes-20260902.json').read_text(encoding='utf-8'))['routes']
graph={r['master_id']:r for r in G['records']}
assert G.get('contextual_method'), 'contextual method missing'
pairs=0
for mid,row in graph.items():
    for edge in row.get('contextual_related_navigation',[]):
        oid=edge['master_id']; assert oid in graph, (mid,oid)
        reverse={e['master_id'] for e in graph[oid].get('contextual_related_navigation',[])}
        assert mid in reverse, f'contextual backlink missing: {mid} <-> {oid}'
        assert edge.get('score',0)>=8, edge
        pairs+=1
    for lang in ('es','en'):
        p=ROOT/R[mid][lang]/'index.html'
        h=p.read_text(encoding='utf-8')
        assert "data-contextual-related-navigation='20260902'" in h, f'context section missing {p}'
        assert ('no</strong> prueban' in h or 'do <strong>not</strong> prove' in h), f'context boundary missing {p}'
assert pairs//2 >= 20, f'context graph unexpectedly sparse: {pairs//2}'
# The 467/2010 Community-governance proceeding should no longer be isolated.
assert graph['LZ-CIV-045'].get('contextual_related_navigation'), '467/2010 contextual navigation is empty'
print('PASS contextual proceeding interlinks:',pairs//2,'reciprocal pairs; 467/2010 connected')
