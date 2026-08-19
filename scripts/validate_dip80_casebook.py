#!/usr/bin/env python3
from pathlib import Path
import json,re,sys,subprocess
R=Path(__file__).resolve().parents[1]
es=["es/icalpa-mesa-del-ponente/dip-80-2026/manual-vivo/index.html","es/icalpa-mesa-del-ponente/dip-80-2026/manual-vivo/cronologia/index.html","es/icalpa-mesa-del-ponente/dip-80-2026/manual-vivo/arbol-decision/index.html","es/icalpa-mesa-del-ponente/dip-80-2026/manual-vivo/atlas-prueba/index.html","es/icalpa-mesa-del-ponente/dip-80-2026/manual-vivo/proteccion-urgente/index.html","es/icalpa-mesa-del-ponente/dip-80-2026/manual-vivo/modelos/index.html","es/icalpa-mesa-del-ponente/dip-80-2026/manual-vivo/aula/index.html"]
en=["en/icalpa-rapporteur-workbench/dip-80-2026/living-casebook/index.html","en/icalpa-rapporteur-workbench/dip-80-2026/living-casebook/chronology/index.html","en/icalpa-rapporteur-workbench/dip-80-2026/living-casebook/decision-tree/index.html","en/icalpa-rapporteur-workbench/dip-80-2026/living-casebook/evidence-atlas/index.html","en/icalpa-rapporteur-workbench/dip-80-2026/living-casebook/urgent-protection/index.html","en/icalpa-rapporteur-workbench/dip-80-2026/living-casebook/models/index.html","en/icalpa-rapporteur-workbench/dip-80-2026/living-casebook/classroom/index.html"]
err=[]
for p in es+en:
 q=R/p
 if not q.is_file():err.append('missing '+p);continue
 t=q.read_text(encoding='utf-8')
 if 'noindex,follow,noarchive' not in t:err.append('robots '+p)
 if 'dip80-casebook.js' not in t or 'dip80-2026-casebook.js' not in t:err.append('assets '+p)
data_source=(R/'assets/data/dip80-2026-casebook.js').read_text(encoding='utf-8')
if 'caseId:"DIP-80-2026"' not in data_source:err.append('caseId')
for k in ['officialStatus','proceduralActs','allegations','duties','acts','omissions','documents','evidenceLinks','respondentPosition','counterEvidence','temporalIssues','competenceIssues','decisionNodes','urgentProtection','humanGates','modelDecisions','corrections','publicRedactions']:
 if k+':' not in data_source:err.append('schema '+k)
out=subprocess.check_output(['node','-e',"global.window={};require('./assets/data/dip80-2026-casebook.js');process.stdout.write(JSON.stringify(window.DIP80_CASEBOOK))"],cwd=R,text=True)
d=json.loads(out)
if len(d.get('substantiveModules',[]))!=11:err.append('modules')
if len(d.get('documents',[]))<13:err.append('evidence records')
if len(d.get('decisionNodes',[]))<24:err.append('decision nodes')
if len(d.get('humanGates',[]))<10:err.append('human gates')
if len(d.get('modelDecisions',[]))<16:err.append('models')
if len(d.get('teachingChapters',[]))<20:err.append('chapters')
for m in d.get('substantiveModules',[]):
 if not m.get('respondent'):err.append(f'{m.get("id")} respondent')
 cv=m.get('changeView') or {}
 for k in ['strengthen','weaken','resolve','verify','missing','alternative']:
  if not cv.get(k):err.append(f'{m.get("id")} changeView.{k}')
root=(R/es[0]).read_text(encoding='utf-8')
for marker in ['HOW DID WE GET HERE?','NOW / AHORA','WHAT MUST HAPPEN NEXT?','RIGHTS + COMPETENCE','EVIDENCE / PRUEBA']:
 if marker not in root:err.append('NOW marker '+marker)
at=(R/es[3]).read_text(encoding='utf-8')
for marker in ['Registered ≠ reviewed','Reviewed ≠ verified','Verified ≠ sufficient','Sufficient ≠ culpability']:
 if marker not in at:err.append('atlas marker '+marker)
# Enforce cross-file separation marker in structured data.
if 'RE-007476' not in data_source or 'DIP 79' not in data_source or 'RE-007499' not in data_source:err.append('DIP79/DIP80 separation markers')
accept=R/'archive/DIP80_LIVING_CASEBOOK_28_SECTION_ACCEPTANCE_18AUG2026.md'
if not accept.is_file():err.append('28-section acceptance record')
else:
 n=len(re.findall(r'^## \d+\.',accept.read_text(encoding='utf-8'),re.M))
 if n!=28:err.append(f'28 sections count {n}')
if err:
 print('DIP80 CASEBOOK GATE: FAIL');[print(' - '+x) for x in err];sys.exit(1)
print(f'DIP80 CASEBOOK GATE: PASS ({len(es)+len(en)} routes; {len(d["documents"])} evidence records; {len(d["decisionNodes"])} decision nodes; 28/28 controls present)')
