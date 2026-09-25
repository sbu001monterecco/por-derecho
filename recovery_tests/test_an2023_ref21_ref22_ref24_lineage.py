from pathlib import Path
import json, re
ROOT=Path(__file__).resolve().parents[1]
PUB=ROOT/"evidence/criminal/an-dp91-2023/full-text/querella-21sep2023-full-public-transcription.md"
MAN=ROOT/"evidence/criminal/an-dp91-2023/source-manifest.json"
LIN=ROOT/"data/an2023-ref21-ref22-ref24-lineage-20260923.json"

def test_an2023_public_page_coverage():
    text=PUB.read_text(encoding="utf-8")
    nums=[int(x) for x in re.findall(r"Página\s+(\d+)\s+de\s+88",text)]
    assert sorted(set(nums))==list(range(1,89))
    assert "TERCER OTROSI DIGO" in text
    assert "Doña Estefanía Sixto Seijas" in text

def test_an2023_manifest_and_source_identity():
    m=json.loads(MAN.read_text(encoding="utf-8"))
    assert m["source"]["querella_pages"]==88
    assert m["coverage"]["pages_present"]=="88/88"
    assert m["source"]["source_pdf_sha512"]=="2c35052af7f869dfb13ca8593552a6997ee9f1f83a09299bcee883345482ae63b7502f76d6e85873b4b80c1b745d7a3c5797762400410e33c897140b9c36c2ab"
    private=ROOT/m["repositories"]["gitlab_private"]["verbatim_master_path"]
    if private.exists():
        text=private.read_bytes().decode("utf-8")
        assert len(text)==m["source"]["extracted_verbatim_chars"]
        nums=[int(x) for x in re.findall(r"Página\s+(\d+)\s+de\s+88",text)]
        assert nums==list(range(1,89))
        assert "Audiencia Nacional – Sala de lo Penal" not in text

def test_ref21_ref22_ref24_lineage_paths():
    g=json.loads(LIN.read_text(encoding="utf-8"))
    assert [x["canonical_label"] for x in g["downstream"]]==["Ref21","Ref22","Ref24"]
    for node in g["downstream"]:
        assert (ROOT/node["living_dossier"]).exists()
        for p in node["frozen_sources"]:
            assert (ROOT/p).exists()


FROZEN_INDEX=ROOT/"evidence/judicial/june-2026-three-track/FROZEN_INDEX.md"
CANONICAL_CONTROLS=(
    "data/three-track-full-digitisation-20260904.json",
    "assets/data/control-21-22-24-continuity-v1.json",
    "archive/THREE_TRACK_FULL_DIGITISATION_CONTROL_04SEP2026.md",
    "scripts/validate_control_21_22_24_reader_binding.py",
    ".github/governance/CONTROL_21_22_24_CONTINUITY_INTERLINK_PROTOCOL_04SEP2026.md",
)

def test_frozen_index_has_no_dangling_local_links():
    text=FROZEN_INDEX.read_text(encoding="utf-8")
    for raw in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        if "://" in raw or raw.startswith("#"):
            continue
        target=(FROZEN_INDEX.parent/raw.split("#",1)[0]).resolve()
        assert target.exists(), f"dangling frozen-index link: {raw}"

def test_three_track_canonical_controls_are_materialized():
    for rel in CANONICAL_CONTROLS:
        assert (ROOT/rel).exists(), f"missing canonical continuity control: {rel}"


FROZEN_PAGE_RANGES={
    "evidence/judicial/june-2026-three-track/frozen/ref21-25jun2026-pages-001-030.md": (1,30),
    "evidence/judicial/june-2026-three-track/frozen/ref21-25jun2026-pages-031-060.md": (31,60),
    "evidence/judicial/june-2026-three-track/frozen/ref21-25jun2026-pages-061-086.md": (61,86),
    "evidence/judicial/june-2026-three-track/frozen/ref21-26jun2026-working-pages-001-026.md": (1,26),
    "evidence/judicial/june-2026-three-track/frozen/ref21-09jul2026-ampliacion-pages-001-019.md": (1,19),
    "evidence/judicial/june-2026-three-track/frozen/ref22-18jun2026-pages-001-030.md": (1,30),
    "evidence/judicial/june-2026-three-track/frozen/ref22-18jun2026-pages-031-055.md": (31,55),
    "evidence/judicial/june-2026-three-track/frozen-linked/di169-ref24-traceability-aportacion-25jun2026.md": (1,9),
}

def test_frozen_page_ranges_are_complete():
    for rel,(first,last) in FROZEN_PAGE_RANGES.items():
        text=(ROOT/rel).read_text(encoding="utf-8")
        nums=[int(x) for x in re.findall(r"^## Source page\s+(\d+)(?:\s+of\s+\d+)?\s*$",text,re.M|re.I)]
        assert nums==list(range(first,last+1)), f"incomplete frozen page range: {rel}: {nums[:2]}..{nums[-2:] if nums else []}"

if __name__=="__main__":
    test_an2023_public_page_coverage()
    test_an2023_manifest_and_source_identity()
    test_ref21_ref22_ref24_lineage_paths()
    test_frozen_index_has_no_dangling_local_links()
    test_three_track_canonical_controls_are_materialized()
    test_frozen_page_ranges_are_complete()
    print("AN2023_REF21_REF22_REF24_CONTINUITY_PASS")
