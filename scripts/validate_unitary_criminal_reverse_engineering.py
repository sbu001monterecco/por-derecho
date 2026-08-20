#!/usr/bin/env python3
import json,re,sys
from pathlib import Path
R=Path(__file__).resolve().parents[1];M='unitary-criminal-reverse-engineering-20260820';e=[]
req={'es/ingenieria-inversa-criminal-unitaria/index.html':['No son irregularidades aisladas','Los quince puntos más fuertes',M],'en/unitary-criminal-reverse-engineering/index.html':['These are not isolated irregularities','The fifteen strongest points',M],'es/retracto-credito-litigioso-1041-2017/index.html':['Se presentó un desistimiento en nombre de LPB',M],'en/litigious-credit-retracto-1041-2017/index.html':["A withdrawal was filed in LPB's name",M],'assets/unitary-criminal-reverse-engineering-20260820.js':[M,'unitaryCriminalGateway'],'sitemap-criminal-engineering.xml':['ingenieria-inversa-criminal-unitaria','unitary-criminal-reverse-engineering']}
for p,ms in req.items():
 t=(R/p).read_text(encoding='utf-8') if (R/p).is_file() else '';
 if not t:e.append('missing '+p)
 for m in ms:
  if m not in t:e.append(p+' missing '+m)
for p in ['research/unitary-criminal-reverse-engineering/data/top_points.json','research/unitary-criminal-reverse-engineering/data/offence_matrix.json','research/unitary-criminal-reverse-engineering/data/critical_bridges.json']:
 try:
  if json.loads((R/p).read_text())['marker']!=M:e.append(p+' marker')
 except Exception as x:e.append(p+' '+str(x))
for p in ['es/retracto-credito-litigioso-1041-2017/index.html','en/litigious-credit-retracto-1041-2017/index.html']:
 t=(R/p).read_text();
 for x in [r'LPB desiste\b',r'LPB solicitó el desistimiento',r'LPB withdraws\b',r'LPB requested withdrawal']:
  if re.search(x,t,re.I):e.append(p+' autonomous attribution '+x)
if e:print('UNITARY CRIMINAL: FAIL\n - '+'\n - '.join(e));sys.exit(1)
print('UNITARY CRIMINAL: PASS')
