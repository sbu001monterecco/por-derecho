"""Regression checks for stable POST7J backlink placement."""
import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts import build_post7june_route_interlinks as builder


class BacklinkPlacementTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.page = self.root / "page.html"
        self.root_patch = patch.object(builder, "ROOT", self.root)
        self.routes_patch = patch.object(builder, "ROUTES", {"en": [("community", "page.html")]})
        self.root_patch.start()
        self.routes_patch.start()
        self.addCleanup(self.root_patch.stop)
        self.addCleanup(self.routes_patch.stop)

    def build(self):
        with contextlib.redirect_stdout(io.StringIO()):
            builder.main()

    def test_existing_correct_block_and_surrounding_bytes_are_stable(self):
        original = "<main>before\n\n" + builder.backlink("en", "community") + "\n\n<section>later sibling</section>\n</main>"
        self.page.write_text(original, encoding="utf-8")
        self.build()
        self.build()
        self.assertEqual(self.page.read_text(encoding="utf-8"), original)

    def test_stale_block_updates_in_place_without_moving_later_sibling(self):
        prefix = "<main>before\n\n"
        suffix = "\n\n<section>later sibling</section>\n</main>"
        self.page.write_text(prefix + builder.BEGIN + "stale" + builder.END + suffix, encoding="utf-8")
        self.build()
        self.assertEqual(self.page.read_text(encoding="utf-8"), prefix + builder.backlink("en", "community") + suffix)

    def test_missing_block_is_inserted_once_and_then_stable(self):
        self.page.write_text("<main>body</main>", encoding="utf-8")
        self.build()
        first = self.page.read_text(encoding="utf-8")
        self.assertEqual(first.count(builder.BEGIN), 1)
        self.assertIn(builder.backlink("en", "community"), first)
        self.build()
        self.assertEqual(self.page.read_text(encoding="utf-8"), first)

    def test_duplicate_blocks_fail_without_writing(self):
        original = "<main>" + (builder.BEGIN + "old" + builder.END) * 2 + "</main>"
        self.page.write_text(original, encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "zero or one complete"):
            self.build()
        self.assertEqual(self.page.read_text(encoding="utf-8"), original)

    def test_incomplete_block_fails_without_writing(self):
        original = "<main>" + builder.BEGIN + "old</main>"
        self.page.write_text(original, encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "zero or one complete"):
            self.build()
        self.assertEqual(self.page.read_text(encoding="utf-8"), original)


if __name__ == "__main__":
    unittest.main()
