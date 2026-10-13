#!/usr/bin/env python3
"""Resolve the verified English route and keep the finite projection manifest stable.
Uses the same exact-branch lease, writer and allowlist as the scoped preparator.
"""
from pathlib import Path
import prepare_alzada4_projection as p

old = 'en/pattern-favourable-effects-acosta-matos/index.html'
new = 'en/acosta-matos-favourable-effect-pattern/index.html'
if not Path(new).is_file():
    raise RuntimeError('Verified English counterpart is unavailable')
p.BACKLINKS = [new if x == old else x for x in p.BACKLINKS]
p.ALLOW.discard(old)
p.ALLOW.add(new)
original_prepare = p.prepare


def stable_prepare():
    outputs, receipt = original_prepare()
    for name in p.BACKLINKS + p.MD_PATHS + ['CHATGPT_START_HERE.md']:
        path = Path(name)
        if path.is_file() and p.MARKER in path.read_text(encoding='utf-8'):
            outputs.setdefault(name, path.read_bytes())
    receipt['backlinks'] = [x for x in p.BACKLINKS if x in outputs]
    receipt['exceptions'] = [x for x in receipt['exceptions'] if not x.startswith(old + ':')]
    receipt['files'] = [{'path': k, 'bytes': len(v), 'sha256': p.sha(v)} for k,v in sorted(outputs.items()) if k != p.RECEIPT]
    outputs[p.RECEIPT] = p.json_bytes(receipt)
    return outputs, receipt


p.prepare = stable_prepare
if __name__ == '__main__':
    p.main()
