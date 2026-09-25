#!/usr/bin/env python3
"""Repair defects found by the first bounded browser run, then regenerate."""
from pathlib import Path
import re
p=Path(__file__).with_name('author.py')
s=p.read_text()
def once(old,new):
 global s
 assert s.count(old)==1, 'Unexpected author source: '+old[:90]
 s=s.replace(old,new,1)
once("post=[run(c,'candidate-'+str(i)) for i,c in enumerate(commands)]", "post=[]")
once("manifest={'schema':", "manifest={'publication_id':'PD-HOMEPAGE-READING-SCOPE-20260925','current_state':'PR_OPEN','owner':'Gil Marer / Project Sun Rock','expected_routes':{'en':['en/index.html'],'es':['es/index.html']},'expected_source_files':['en/index.html','es/index.html','assets/homepage-reading-20260925.css','assets/audience-experience-order-20260823.js'],'schema':")
needle="(ROOT/CSS_PATH).write_text(STYLE,encoding='utf8');changed.append(CSS_PATH)"
replacement="""STYLE += '''\n/* Preserve readable names and cards even at 320px in Spanish. */
.pd-home-refined .pd-five-ac__institution-card{min-width:0;overflow-wrap:anywhere}
.pd-home-refined .pd-five-ac__institution-person>*{min-width:0}
.pd-home-refined .pd-five-ac__institution-name{overflow-wrap:anywhere}
.pd-home-refined .pd-five-ac__cluster-cards>*{min-width:0}
body.pd-home-refined.pd-home-mission main>.hero{padding:0}
body.pd-home-refined.pd-home-mission main>.hero h1{font-size:clamp(2.6rem,4.9vw,4.6rem);line-height:1.06;max-width:18ch}
'''
(ROOT/CSS_PATH).write_text(STYLE,encoding='utf8');changed.append(CSS_PATH)
# Extend the EXISTING homepage ordering control; do not add a competing observer.
order_path='assets/audience-experience-order-20260823.js'
order=(ROOT/order_path).read_text()
old='const coreSections = [hero, controlling, detailed, criminalMisuse, priority, prosecution, summary, audiences, perimeters];'
new='const portfolioScope = main.querySelector("#economic-scope-20260925");\\n    const coreSections = [hero, controlling, detailed, portfolioScope, criminalMisuse, priority, prosecution, summary, audiences, perimeters];'
assert order.count(old)==1
order=order.replace(old,new,1)
old='[controlling, detailed, ...protectedCriminalSequence, summary, audiences, perimeters]'
new='[controlling, detailed, portfolioScope, ...protectedCriminalSequence, summary, audiences, perimeters]'
assert order.count(old)==1
order=order.replace(old,new,1)
(ROOT/order_path).write_text(order,encoding='utf8');changed.append(order_path)
"""
once(needle,replacement)
needle="(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))"
replacement="""# Validate AFTER all referenced public files exist, including the manifest.
post=[run(c,'candidate-'+str(i)) for i,c in enumerate(commands)]
manifest['candidate_checks']=post
(ROOT/MANIFEST).write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\\n')
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
"""
once(needle,replacement)
# Record diagnostics on failure as well as screenshots on success.
b=Path(__file__).with_name('browser.py');bs=b.read_text()
bs=bs.replace('page.wait_for_timeout(1800)','page.wait_for_timeout(6500)')
bs=bs.replace("assert rect['x']>=-2 and rect['x']+rect['width']<=width+2,'Person card overflows viewport'", "assert rect['x']>=-2 and rect['x']+rect['width']<=width+2,'Person card overflows viewport: '+str(rect)+' '+item.get_attribute('data-institution-card') if item.get_attribute('data-institution-card') else 'Private card overflow'")
# Keep the assertion simple and avoid assertion-expression precedence problems.
bs=bs.replace("assert rect['x']>=-2 and rect['x']+rect['width']<=width+2,'Person card overflows viewport: '+str(rect)+' '+item.get_attribute('data-institution-card') if item.get_attribute('data-institution-card') else 'Private card overflow'", "assert rect['x']>=-2 and rect['x']+rect['width']<=width+2,'Person card overflows viewport: '+str(rect)+' '+str(item.get_attribute('data-institution-card'))")
bs=bs.replace("except Exception as e:row['errors'].append(str(e));print('BROWSER_FAILURE',row,flush=True)", "except Exception as e:\n     row['errors'].append(str(e));print('BROWSER_FAILURE',row,flush=True)\n     if js and width in [320,390,1280]:\n      page.screenshot(path=str(out/f'{lang}-{width}-failure.png'))\n      (out/f'{lang}-{width}-failure.html').write_text(page.content())")
compile(bs,str(b),'exec');b.write_text(bs)
compile(s,str(p),'exec')
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
