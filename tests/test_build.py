from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
sys.path.insert(0, str(ROOT / "scripts"))

from check import contrast_ratio


class BuildTests(unittest.TestCase):
    def build(self) -> None:
        subprocess.run([sys.executable, str(ROOT / "scripts/build.py")], check=True)

    def test_build_is_deterministic(self) -> None:
        self.build()
        first = {path.relative_to(DIST).as_posix(): path.read_bytes() for path in sorted(DIST.rglob("*")) if path.is_file()}
        self.build()
        second = {path.relative_to(DIST).as_posix(): path.read_bytes() for path in sorted(DIST.rglob("*")) if path.is_file()}
        self.assertEqual(first, second)

    def test_manifest_matches_every_distributed_file(self) -> None:
        self.build()
        manifest = json.loads((DIST / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual({
            "atlas-fonts.css", "atlas-interface-kit.css", "components.json", "semantics.json",
            "fonts/dm-serif-display-400-italic.woff2", "fonts/dm-serif-display-400.woff2",
            "fonts/ibm-plex-mono-400.woff2", "fonts/ibm-plex-mono-500.woff2",
            "licenses/DM-Serif-Display-OFL.txt", "licenses/IBM-Plex-Mono-OFL.txt", "tokens.json",
        }, set(manifest["files"]))
        self.assertEqual("1.0.0", manifest["foundation_extension_version"])
        self.assertEqual(3, manifest["semantic_contract_count"])
        for name, record in manifest["files"].items():
            data = (DIST / name).read_bytes()
            self.assertEqual(len(data), record["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), record["sha256"])

    def test_component_contract_covers_all_roles(self) -> None:
        components = json.loads((ROOT / "src/components.json").read_text(encoding="utf-8"))
        roles = {item["role"] for item in components["roles"]}
        self.assertEqual(27, len(roles))
        for role in ("global-header", "breadcrumb-navigation", "status-announcement", "search-dialog", "error-state", "footer"):
            self.assertIn(role, roles)

    def test_semantics_contract_matches_authority(self) -> None:
        semantics = json.loads((ROOT / "src/semantics.json").read_text(encoding="utf-8"))
        self.assertEqual("atlas-interface-kit/semantics/v1", semantics["schema_version"])
        self.assertEqual("2.0.0", semantics["authority"]["base_contract_version"])
        self.assertEqual("1.0.0", semantics["authority"]["foundation_extension_version"])
        self.assertEqual([320, 375, 768, 1024, 1440], semantics["evidence"]["blocking_viewports_px"])
        self.assertEqual([1920], semantics["evidence"]["reporting_only_viewports_px"])
        self.assertFalse(semantics["evidence"]["reporting_only_is_breakpoint"])
        self.assertFalse(semantics["evidence"]["reporting_only_is_budget"])

    def test_faint_text_meets_wcag_aa_on_all_atlas_surfaces(self) -> None:
        tokens = json.loads((ROOT / "src/tokens.json").read_text(encoding="utf-8"))
        faint = tokens["colour"]["text_faint"]
        for surface in ("bg", "bg_1", "bg_2"):
            with self.subTest(surface=surface):
                self.assertGreaterEqual(contrast_ratio(faint, tokens["colour"][surface]), 4.5)

    def test_css_has_no_remote_runtime_dependency(self) -> None:
        self.build()
        for name in ("atlas-interface-kit.css", "atlas-fonts.css"):
            with self.subTest(name=name):
                css = (DIST / name).read_text(encoding="utf-8")
                self.assertNotIn("http://", css)
                self.assertNotIn("https://", css)

    def test_fonts_are_woff2_and_ship_with_their_licences(self) -> None:
        self.build()
        fonts = sorted((DIST / "fonts").glob("*.woff2"))
        self.assertEqual(4, len(fonts))
        for font in fonts:
            with self.subTest(font=font.name):
                self.assertEqual(b"wOF2", font.read_bytes()[:4])
        for licence in sorted((DIST / "licenses").glob("*.txt")):
            with self.subTest(licence=licence.name):
                text = licence.read_text(encoding="utf-8")
                self.assertIn("SIL OPEN FONT LICENSE", text)
                self.assertIn("Version 1.1", text)


if __name__ == "__main__":
    unittest.main()
