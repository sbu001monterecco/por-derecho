#!/usr/bin/env python3
"""Regression tests for private ACTA PDF/DOCX source-map validation."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from pypdf import PdfWriter


REPO = Path(__file__).resolve().parents[2]
MODULE_PATH = REPO / "evidence/community/actas/build_public_packages.py"
SPEC = importlib.util.spec_from_file_location("acta_build_public_packages", MODULE_PATH)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - import guard
    raise RuntimeError(f"Cannot load {MODULE_PATH}")
acta = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(acta)


class PrivateActaSourceMapTests(unittest.TestCase):
    def write_manifest(self, root: Path, source: Path, pages: int) -> Path:
        manifest = root / f"{source.stem}-manifest.json"
        manifest.write_text(
            json.dumps(
                {
                    "source": {"sha256": acta.sha256(source)},
                    "source_variant_page_count": pages,
                }
            ),
            encoding="utf-8",
        )
        return manifest

    def write_source_map(self, root: Path, value: object) -> Path:
        source_map = root / "private-source-map.json"
        source_map.write_text(json.dumps({"fixture": value}), encoding="utf-8")
        return source_map

    def validate_fixture(self, source_map: Path, manifest: Path) -> list[str]:
        with patch.object(acta, "repo_path", side_effect=lambda value: Path(value)):
            return acta.validate_private_source_map(
                source_map,
                [{"slug": "fixture", "manifest": str(manifest)}],
            )

    def test_legacy_pdf_path_keeps_native_pdf_page_counting(self) -> None:
        with tempfile.TemporaryDirectory(prefix="acta-pdf-map-test-") as tmp:
            root = Path(tmp)
            source = root / "control.pdf"
            writer = PdfWriter()
            writer.add_blank_page(width=72, height=72)
            writer.add_blank_page(width=72, height=72)
            with source.open("wb") as stream:
                writer.write(stream)
            manifest = self.write_manifest(root, source, 2)
            source_map = self.write_source_map(root, str(source))

            messages = self.validate_fixture(source_map, manifest)

            self.assertEqual(
                messages,
                [
                    "fixture: private source hash/pages verified "
                    "(application/pdf; pdf-page-tree)"
                ],
            )

    def test_docx_accepts_recorded_deterministic_conversion_count(self) -> None:
        with tempfile.TemporaryDirectory(prefix="acta-docx-map-test-") as tmp:
            root = Path(tmp)
            source = root / "control.docx"
            with zipfile.ZipFile(source, "w", compression=zipfile.ZIP_DEFLATED) as archive:
                archive.writestr(
                    "[Content_Types].xml",
                    '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>',
                )
                archive.writestr(
                    "word/document.xml",
                    '<?xml version="1.0"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>',
                )
            manifest = self.write_manifest(root, source, 4)
            source_map = self.write_source_map(
                root,
                {
                    "path": str(source),
                    "media_type": acta.DOCX_MEDIA_TYPE,
                    "page_count_method": acta.DOCX_RECORDED_PAGE_COUNT_METHOD,
                    "page_count": 4,
                },
            )

            messages = self.validate_fixture(source_map, manifest)

            self.assertEqual(
                messages,
                [
                    "fixture: private source hash/pages verified "
                    f"({acta.DOCX_MEDIA_TYPE}; "
                    f"{acta.DOCX_RECORDED_PAGE_COUNT_METHOD})"
                ],
            )

    def test_docx_temporary_conversion_count_can_be_cross_checked(self) -> None:
        with tempfile.TemporaryDirectory(prefix="acta-docx-convert-test-") as tmp:
            root = Path(tmp)
            source = root / "control.docx"
            with zipfile.ZipFile(source, "w") as archive:
                archive.writestr("[Content_Types].xml", "<Types/>")
                archive.writestr("word/document.xml", "<document/>")
            manifest = self.write_manifest(root, source, 4)
            source_map = self.write_source_map(
                root,
                {
                    "path": str(source),
                    "page_count_method": acta.DOCX_TEMPORARY_PAGE_COUNT_METHOD,
                    "page_count": 4,
                },
            )

            with patch.object(
                acta,
                "count_docx_pages_with_libreoffice",
                return_value=4,
            ) as converter, patch.object(
                acta,
                "repo_path",
                side_effect=lambda value: Path(value),
            ):
                messages = acta.validate_private_source_map(
                    source_map,
                    [{"slug": "fixture", "manifest": str(manifest)}],
                )

            converter.assert_called_once_with(source, slug="fixture")
            self.assertIn(acta.DOCX_TEMPORARY_PAGE_COUNT_METHOD, messages[0])

    def test_media_type_must_match_native_extension(self) -> None:
        with self.assertRaisesRegex(acta.ValidationError, "does not match"):
            acta.normalise_private_source_entry(
                "fixture",
                {"path": "/private/control.docx", "media_type": acta.PDF_MEDIA_TYPE},
            )

    def test_source_map_inside_repository_is_rejected_without_path_echo(self) -> None:
        source_map = REPO / "evidence/community/actas/public-index.json"
        with self.assertRaises(acta.ValidationError) as caught:
            acta.validate_private_source_map(source_map, [])
        self.assertIn("private source map must remain outside", str(caught.exception))
        self.assertNotIn(str(REPO), str(caught.exception))

    def test_native_source_inside_repository_is_rejected_without_path_echo(self) -> None:
        source = REPO / "assets/docs/community-actas/2012-08-10-public-redacted-es.pdf"
        with self.assertRaises(acta.ValidationError) as caught:
            acta.normalise_private_source_entry("fixture", str(source))
        self.assertIn("fixture: private native source must remain outside", str(caught.exception))
        self.assertNotIn(str(REPO), str(caught.exception))

    def test_missing_private_source_error_does_not_echo_absolute_path(self) -> None:
        with tempfile.TemporaryDirectory(prefix="acta-missing-source-test-") as tmp:
            root = Path(tmp)
            missing = root / "private-control.pdf"
            source_map = self.write_source_map(root, str(missing))
            manifest = root / "manifest.json"
            manifest.write_text("{}", encoding="utf-8")
            with self.assertRaises(acta.ValidationError) as caught:
                self.validate_fixture(source_map, manifest)
            self.assertIn("fixture: private native source does not exist", str(caught.exception))
            self.assertNotIn(str(missing), str(caught.exception))


class PublicActaPreviewDeterminismTests(unittest.TestCase):
    def test_pinned_pymupdf_renders_identical_jpeg_bytes(self) -> None:
        self.assertEqual(acta.fitz.VersionBind, acta.PYMUPDF_VERSION)
        with tempfile.TemporaryDirectory(prefix="acta-preview-test-") as tmp:
            root = Path(tmp)
            source = root / "control.pdf"
            writer = PdfWriter()
            writer.add_blank_page(width=72, height=72)
            with source.open("wb") as stream:
                writer.write(stream)

            preview_dir = root / "previews"
            with patch.object(acta, "REPO", root), patch.object(
                acta,
                "PREVIEW_ROOT",
                root,
            ):
                first = acta.make_previews(source, preview_dir)
                first_bytes = (preview_dir / "page-001.jpg").read_bytes()
                second = acta.make_previews(source, preview_dir)
                second_bytes = (preview_dir / "page-001.jpg").read_bytes()

            self.assertEqual(first, ["previews/page-001.jpg"])
            self.assertEqual(first, second)
            self.assertEqual(first_bytes, second_bytes)
            with acta.Image.open(preview_dir / "page-001.jpg") as image:
                self.assertEqual(image.format, "JPEG")
                self.assertEqual(image.size, (105, 105))


class PublicActaTextModePdfTests(unittest.TestCase):
    def build_mode_pdf(self, root: Path, mode: str) -> tuple[Path, str]:
        public_ocr = mode == acta.PUBLIC_TEXT_MODE_REDACTED_OCR
        event = {
            "id": "SP-ACTA-FIXTURE",
            "slug": "fixture",
            "title_es": "ACTA de prueba",
            "body": "Comunidad de Propietarios",
            "date": "2026-08-28",
            "source_variant_page_count": 1,
            "public_text_mode": mode,
            "public_ocr_available": public_ocr,
        }
        manifest = {
            "slug": "fixture",
            "public_text_mode": mode,
            "public_ocr_available": public_ocr,
            "source": {
                "filename": "control privado no publicado",
                "sha256": "0" * 64,
                "variant_note_es": "Control de prueba.",
            },
        }
        output = root / f"{mode}.pdf"
        acta.make_pdf(event, manifest, ["[CONTENIDO PÚBLICO DE PRUEBA]"], output)
        extracted = acta.pdf_text(output)
        return output, extracted

    def test_marker_and_ocr_pdfs_use_distinct_controlled_copy(self) -> None:
        with tempfile.TemporaryDirectory(prefix="acta-text-mode-test-") as tmp:
            root = Path(tmp)
            for mode in (
                acta.PUBLIC_TEXT_MODE_MARKERS,
                acta.PUBLIC_TEXT_MODE_REDACTED_OCR,
            ):
                with self.subTest(mode=mode):
                    output, extracted = self.build_mode_pdf(root, mode)
                    compact = " ".join(extracted.split())
                    expected = acta.PDF_PUBLIC_TEXT_COPY[mode]
                    self.assertIn(expected["subtitle"], compact)
                    self.assertIn(expected["boundary"], compact)
                    acta.validate_pdf_public_text_boundary("fixture", extracted, mode)
                    metadata = acta.PdfReader(str(output)).metadata or {}
                    self.assertEqual(metadata.get("/Subject"), expected["subject"])

            marker_text = " ".join(
                self.build_mode_pdf(root, acta.PUBLIC_TEXT_MODE_MARKERS)[1].split()
            )
            self.assertIn("sin OCR público", marker_text)
            self.assertNotIn("texto asistido por OCR no certificado", marker_text)

            ocr_text = " ".join(
                self.build_mode_pdf(root, acta.PUBLIC_TEXT_MODE_REDACTED_OCR)[1].split()
            )
            self.assertIn("texto asistido por OCR no certificado", ocr_text)
            self.assertNotIn("sin OCR público", ocr_text)

    def test_manifest_and_index_text_modes_must_agree(self) -> None:
        event = {
            "slug": "fixture",
            "public_text_mode": acta.PUBLIC_TEXT_MODE_MARKERS,
            "public_ocr_available": False,
        }
        manifest = {
            "slug": "fixture",
            "public_text_mode": acta.PUBLIC_TEXT_MODE_REDACTED_OCR,
            "public_ocr_available": True,
        }
        with self.assertRaisesRegex(acta.ValidationError, "public_text_mode mismatch"):
            acta.controlled_public_text_mode(event, manifest)


if __name__ == "__main__":
    unittest.main(verbosity=2)
