#!/usr/bin/env python3
"""Fail-visible wrapper: inspect actual checkout, then run unchanged source checks."""
import json,sys
from pathlib import Path
import repair_audited_website_gaps_20260905 as r

def main():
 for path in sorted(r.GRAPH_PAGES):
  p=r.ROOT/path;s=p.read_text();changed,edits=r.repair_attributes(path,s)
  print(json.dumps({'path':path,'resolved_path':str(p.resolve()),'symlink':p.is_symlink(),'source_length':len(s),'source_sha256':r.sha(s),'before_main_closes':s.count('</main>'),'after_main_closes':changed.count('</main>'),'marker_in_source':r.MARKER in s,'marker_after_attributes':r.MARKER in changed,'attribute_changes':len(edits),'tail':changed[-700:]},ensure_ascii=False),flush=True)
 if '--prepare' in sys.argv:r.prepare()
 elif '--check' in sys.argv:r.check()
 else:raise SystemExit('Use --prepare or --check')

if __name__=='__main__':main()
