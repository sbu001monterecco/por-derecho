#!/usr/bin/env python3
"""Deterministically replace only four non-JTP portrait slots in the approved JTP infographic."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from PIL import Image, ImageFilter, ImageOps
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
LOCK=ROOT/"ops/jtp/JTP_ACTOR_IMAGE_SOURCE_LOCK_20260925.json"

def sha256(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--base",required=True,type=Path)
    ap.add_argument("--output",required=True,type=Path)
    args=ap.parse_args()
    lock=json.loads(LOCK.read_text())
    if sha256(args.base)!=lock["approved_base"]["sha256"]:
        raise SystemExit("Base infographic differs from approved immutable source")
    base=Image.open(args.base).convert("RGB")
    if base.size!=(lock["approved_base"]["width"],lock["approved_base"]["height"]):
        raise SystemExit("Base dimensions changed")
    out=base.copy()
    for key in ("borja","jdam","lpam","alberto"):
        row=lock["actors"][key]
        source=ROOT/row["path"]
        if sha256(source)!=row["sha256"]:
            raise SystemExit(f"Source hash changed: {key}")
        im=Image.open(source).convert("RGB")
        if row.get("source_crop"):
            im=im.crop(tuple(row["source_crop"]))
        x0,y0,x1,y1=row["box"]
        fitted=ImageOps.fit(im,(x1-x0,y1-y0),method=Image.Resampling.LANCZOS,centering=tuple(row["centering"]))
        fitted=fitted.filter(ImageFilter.UnsharpMask(radius=0.6,percent=110,threshold=3))
        out.paste(fitted,(x0,y0))
    # Fail closed: only authorised rectangles may change.
    before=np.asarray(base)
    after=np.asarray(out)
    diff=np.any(before!=after,axis=2)
    mask=np.zeros(diff.shape,dtype=bool)
    for key in ("borja","jdam","lpam","alberto"):
        x0,y0,x1,y1=lock["actors"][key]["box"]
        mask[y0:y1,x0:x1]=True
    outside=int(np.logical_and(diff,~mask).sum())
    if outside:
        raise SystemExit(f"Unauthorised pixels changed outside portrait boxes: {outside}")
    # Existing JTP portrait must remain byte-identical at pixel level.
    jtp=(390,195,640,470)
    x0,y0,x1,y1=jtp
    if not np.array_equal(before[y0:y1,x0:x1],after[y0:y1,x0:x1]):
        raise SystemExit("JTP region changed")
    args.output.parent.mkdir(parents=True,exist_ok=True)
    out.save(args.output,optimize=True)
    print(json.dumps({"status":"PASS","changed_pixels":int(diff.sum()),"outside":outside,"jtp_unchanged":True,"output_sha256":sha256(args.output)},sort_keys=True))
    return 0
if __name__=="__main__":
    raise SystemExit(main())
