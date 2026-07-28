from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRAND_REFERENCE = ROOT / "docs" / "BRAND_REFERENCE.md"


class BrandReferenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.reference = BRAND_REFERENCE.read_text(encoding="utf-8")
        self.tokens = json.loads((ROOT / "src" / "tokens.json").read_text(encoding="utf-8"))

    def test_reference_is_repository_owned_and_linked(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        consumer = (ROOT / "docs" / "CONSUMER_CONTRACT.md").read_text(encoding="utf-8")
        foundation = (ROOT / "docs" / "FOUNDATION_EXTENSION.md").read_text(encoding="utf-8")
        self.assertIn("docs/BRAND_REFERENCE.md", readme)
        self.assertIn("docs/FOUNDATION_EXTENSION.md", readme)
        self.assertIn("BRAND_REFERENCE.md", consumer)
        self.assertIn("FOUNDATION_EXTENSION.md", consumer)
        self.assertIn("AtlasReaper311/atlas-interface-kit", self.reference)
        self.assertIn("AtlasReaper311/atlas-infra", self.reference)
        self.assertIn("public-interface-foundation-extension-v1.json", foundation)

    def test_reference_matches_executable_colour_and_font_authority(self) -> None:
        colours = self.reference.split("## Colours", 1)[1].split("## Typography", 1)[0]
        for value in self.tokens["colour"].values():
            with self.subTest(value=value):
                self.assertIn(f"`{value}`", colours)
        self.assertIn("`DM Serif Display`", self.reference)
        self.assertIn("`IBM Plex Mono`", self.reference)
        self.assertNotIn("#555560", colours)
        self.assertIn("Earlier loose copies of the Brand Reference listed `#555560`", self.reference)

    def test_reference_prohibits_remote_font_loading(self) -> None:
        lowered = self.reference.lower()
        self.assertNotIn("fonts.googleapis.com", lowered)
        self.assertNotIn("fonts.gstatic.com", lowered)
        self.assertIn("repository-local font bundle", lowered)
        self.assertIn("remote presentation host are prohibited", lowered)

    def test_reference_covers_every_accepted_maturity_label(self) -> None:
        for label in ("Production", "Tool", "Preview", "Experiment", "Planned", "Retired"):
            with self.subTest(label=label):
                self.assertRegex(self.reference, rf"\| {label} \|")

    def test_reference_records_the_shared_scales(self) -> None:
        for value in self.tokens["space_px"]:
            self.assertIn(f"`{value}`", self.reference)
        for value in self.tokens["content_px"].values():
            self.assertIn(f"`{value}px`", self.reference)
        for value in self.tokens["control_px"].values():
            self.assertIn(f"`{value}px`", self.reference)
        for value in self.tokens["breakpoint_px"].values():
            self.assertIn(f"`{value}px`", self.reference)


if __name__ == "__main__":
    unittest.main()
