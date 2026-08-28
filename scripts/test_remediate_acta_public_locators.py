#!/usr/bin/env python3
"""Regression tests for public ACTA provider-locator remediation."""

from __future__ import annotations

import unittest
from pathlib import Path

from scripts.remediate_acta_public_locators import (
    REPO_ROOT,
    controlled_text_targets,
    discover,
    discover_for_path,
    replace_known_public_links,
    replace_locators,
    replace_locators_for_path,
    token_for,
)


class PublicLocatorRemediationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.gmail_id = "a" * 16
        self.drive_id = "1" + ("Ab_9-" * 7)

    def test_gmail_requires_same_line_message_context(self) -> None:
        self.assertEqual(discover(f"digest `{self.gmail_id}`"), [])
        self.assertEqual(
            discover(f"Gmail message attachment SHA-256 `{self.gmail_id}`"),
            [],
        )
        hits = discover(f"Gmail message `{self.gmail_id}`")
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].locator_kind, "gmail_message_id")
        following_label = discover(f"`{self.gmail_id}` | Gmail message | source")
        self.assertEqual(len(following_label), 1)
        self.assertEqual(following_label[0].locator_kind, "gmail_message_id")

    def test_drive_accepts_label_on_same_or_preceding_line(self) -> None:
        same_line = discover(f"Drive ID `{self.drive_id}`")
        next_line = discover(f"Primary Drive source:\n\n`{self.drive_id}`")
        self.assertEqual(len(same_line), 1)
        self.assertEqual(len(next_line), 1)
        self.assertEqual(same_line[0].public_token, next_line[0].public_token)

    def test_drive_accepts_google_doc_folder_and_truncated_context(self) -> None:
        google_doc = discover(f"Google Doc ID `{self.drive_id}`")
        hyphenated = discover(f"further Google-Doc derivative, ID `{self.drive_id}`")
        folder_row = discover(
            f"Pamanil folder: Folder `{self.drive_id}`; audio `1abcD…`; "
            "duplicates `1efGH...`; continuations `1ijkL…`"
        )
        self.assertEqual(len(google_doc), 1)
        self.assertEqual(len(hyphenated), 1)
        self.assertEqual(len(folder_row), 4)

    def test_sha_abbreviations_hashes_and_slugs_are_not_drive_ids(self) -> None:
        samples = (
            "controlled SHA-256 begins `12fcefd…`; exact Drive share 404",
            '"document_type": "155-page-private-drive-control"',
            "SHA-256 `" + "1" + ("a" * 63) + "`",
            "Drive source SHA-256 `1bccff3…`",
        )
        for sample in samples:
            with self.subTest(sample=sample):
                self.assertEqual(discover(sample), [])

    def test_provider_url_and_standalone_id_share_one_public_token(self) -> None:
        source = (
            f"Drive URL: https://drive.google.com/file/d/{self.drive_id}/view\n"
            f"Drive ID: {self.drive_id}\n"
        )
        remediated, occurrences = replace_locators(source)
        self.assertEqual(len(occurrences), 2)
        self.assertNotIn("google.com", remediated)
        self.assertNotIn(self.drive_id, remediated)
        self.assertEqual(
            remediated.count(token_for("google_drive_file_id", self.drive_id)),
            2,
        )

    def test_public_token_is_not_rediscovered(self) -> None:
        token = token_for("google_drive_file_id", self.drive_id)
        self.assertEqual(discover(f"Drive `{token}`"), [])

    def test_live_private_links_route_local_or_become_plain_text(self) -> None:
        path = REPO_ROOT / "en/community-instrumentalisation/index.html"
        source = (
            f'<a href="https://drive.google.com/file/d/{self.drive_id}/view" '
            'rel="external">view the 29 April 2008 minutes</a> '
            f'<a href="https://drive.google.com/file/d/{self.drive_id}/view" '
            'rel="external">Order 804/2018</a>'
        )
        remediated = replace_known_public_links(path, source)
        self.assertIn(
            'href="/en/community-instrumentalisation/acta-document-room/'
            '2008-04-29/"',
            remediated,
        )
        self.assertNotIn("google.com", remediated)
        self.assertNotIn(">Order 804/2018</a>", remediated)

    def test_ricpe_private_links_use_local_routes_or_plain_text(self) -> None:
        path = REPO_ROOT / "en/ric-private-equity-sun-park/index.html"
        provider = f"https://drive.google.com/file/d/{self.drive_id}/view"
        source = " ".join(
            (
                f'<a href="{provider}">collective resolution of 29 April 2008</a>',
                f'<a href="{provider}">Order 804/2018</a>',
                f'<a href="{provider}">12 May 2017 email</a>',
                f'<a href="{provider}">4 June 2014 · GE-014212/2014</a>',
            )
        )
        remediated = replace_known_public_links(path, source)
        self.assertNotIn("google.com", remediated)
        self.assertIn(
            "/en/community-instrumentalisation/acta-document-room/2008-04-29/",
            remediated,
        )
        self.assertIn("/en/cabildo-lanzarote-tourism-traceability/", remediated)
        self.assertNotIn(">Order 804/2018</a>", remediated)
        self.assertNotIn(">12 May 2017 email</a>", remediated)

    def test_institutional_markdown_links_route_to_public_pages(self) -> None:
        path = REPO_ROOT / "INSTITUTIONAL_ACTIONS.md"
        provider = f"https://docs.google.com/document/d/{self.drive_id}/edit"
        labels = (
            "29 April 2008 owners’ resolution",
            "4 June 2014 filing GE-014212/2014",
            "Cabildo Resolution 2026-2735 / file 614/2026",
            "Order 804/2018",
        )
        source = "\n".join(f"- [{label}]({provider})" for label in labels)
        remediated = replace_known_public_links(path, source)
        self.assertNotIn("google.com", remediated)
        self.assertIn("en/community-instrumentalisation/acta-document-room/", remediated)
        self.assertIn("en/cabildo-lanzarote-tourism-traceability/", remediated)
        self.assertIn("#order-804-2018-pink-cessation", remediated)

    def test_entire_correction_register_is_privacy_controlled(self) -> None:
        path = REPO_ROOT / "archive/CORRECTION_REGISTER.md"
        second_drive_id = "1" + ("Bc_8-" * 7)
        source = (
            f"| CR-066 | Drive `{self.drive_id}` | correction |\n"
            f"| CR-099 | Drive `{second_drive_id}` | unrelated |\n"
        )
        hits = discover_for_path(path, source)
        self.assertEqual(len(hits), 2)
        remediated, occurrences = replace_locators_for_path(path, source)
        self.assertEqual(len(occurrences), 2)
        self.assertNotIn(self.drive_id, remediated)
        self.assertNotIn(second_drive_id, remediated)

    def test_bounded_premeeting_register_accepts_bare_gmail_ids(self) -> None:
        path = REPO_ROOT / (
            "archive/"
            "JONATHAN_SIMO_PWC_2016_PREMEETING_PRIMARY_EMAIL_ADDENDUM_17AUG2026.md"
        )
        source = f"- `{self.gmail_id}` — Jonathan attendance chronology\n"
        hits = discover_for_path(path, source)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].locator_kind, "gmail_message_id")
        remediated, occurrences = replace_locators_for_path(path, source)
        self.assertEqual(len(occurrences), 1)
        self.assertNotIn(self.gmail_id, remediated)

    def test_bounded_register_tokenizes_email_addresses(self) -> None:
        path = REPO_ROOT / (
            "archive/"
            "JONATHAN_SIMO_PWC_2016_RECORDING_RETRIEVAL_GATE_17AUG2026.md"
        )
        address = "private.person@example.test"
        source = f"Sender: {address}\n"
        hits = discover_for_path(path, source)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0].locator_kind, "email_address")
        remediated, occurrences = replace_locators_for_path(path, source)
        self.assertEqual(len(occurrences), 1)
        self.assertNotIn(address, remediated)
        self.assertIn("SP-PRV-LCTR-EM-", remediated)

    def test_controlled_scope_includes_register_public_edition_and_landings(self) -> None:
        targets = {path.relative_to(REPO_ROOT) for path in controlled_text_targets()}
        required = {
            Path(
                "evidence/community/"
                "COMMUNITY_AUTHORITY_EVENTS_EMAILS_MEETINGS_ACTAS_PUBLIC_REGISTER.md"
            ),
            Path("evidence/community/ACTA_22JUN2011_PUBLIC_REDACTED_EDITION.md"),
            Path("en/community-instrumentalisation/index.html"),
            Path("es/comunidad-instrumentalizacion/index.html"),
            Path("INSTITUTIONAL_ACTIONS.md"),
            Path("CHATGPT_START_HERE.md"),
            Path("en/ric-private-equity-sun-park/index.html"),
            Path(
                "archive/"
                "JONATHAN_SIMO_NATIVE_REPORTS_AND_MEETING_DATE_CORRECTION_17AUG2026.md"
            ),
            Path(
                "archive/"
                "THREAD_DELETION_CONTINUITY_AUDIT_GIL_PINK_NULLITY_AEAT_COMMUNITY_22AUG2026.md"
            ),
            Path("archive/CORRECTION_REGISTER_COMMUNITY_ACTAS_ADDENDUM_17AUG2026.md"),
            Path("archive/CORRECTION_REGISTER.md"),
            Path(
                "archive/"
                "THREAD_DELETION_CONTINUITY_AUDIT_CEXP_MONTERECCO_PINK_AUTO804_FORENSIC_20AUG2026.md"
            ),
        }
        self.assertTrue(required.issubset(targets))


if __name__ == "__main__":
    unittest.main()
