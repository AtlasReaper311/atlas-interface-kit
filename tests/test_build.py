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
        first = {
            path.relative_to(DIST).as_posix(): path.read_bytes()
            for path in sorted(DIST.rglob("*"))
            if path.is_file()
        }
        self.build()
        second = {
            path.relative_to(DIST).as_posix(): path.read_bytes()
            for path in sorted(DIST.rglob("*"))
            if path.is_file()
        }
        self.assertEqual(first, second)

    def test_manifest_matches_every_distributed_file(self) -> None:
        self.build()
        manifest = json.loads((DIST / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(
            {
                "atlas-fonts.css",
                "atlas-interface-kit.css",
                "components.json",
                "semantics.json",
                "fonts/dm-serif-display-400-italic.woff2",
                "fonts/dm-serif-display-400.woff2",
                "fonts/ibm-plex-mono-400.woff2",
                "fonts/ibm-plex-mono-500.woff2",
                "licenses/DM-Serif-Display-OFL.txt",
                "licenses/IBM-Plex-Mono-OFL.txt",
                "tokens.json",
            },
            set(manifest["files"]),
        )
        self.assertEqual("1.0.0", manifest["foundation_extension_version"])
        self.assertEqual("1.0.0", manifest["footer_extension_version"])
        self.assertEqual("1.0.0", manifest["evidence_mode_extension_version"])
        self.assertEqual(5, manifest["semantic_contract_count"])
        self.assertEqual(7, manifest["evidence_mode_count"])
        self.assertEqual(3, manifest["evidence_selector_count"])
        self.assertEqual(5, manifest["footer_slot_count"])
        self.assertEqual(4, manifest["footer_variant_count"])
        for name, record in manifest["files"].items():
            data = (DIST / name).read_bytes()
            self.assertEqual(len(data), record["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), record["sha256"])

    def test_component_contract_covers_roles_evidence_and_footer_selectors(self) -> None:
        components = json.loads((ROOT / "src/components.json").read_text(encoding="utf-8"))
        roles = {item["role"] for item in components["roles"]}
        self.assertEqual(30, len(roles))
        self.assertTrue({"evidence-mode", "evidence-surface", "evidence-value"}.issubset(roles))
        self.assertIn("footer", roles)
        evidence = components["evidence_mode"]
        self.assertEqual("data-evidence-mode", evidence["mode_attribute"])
        self.assertEqual(
            [
                "measured",
                "stale-measured",
                "recorded-replay",
                "simulated",
                "unavailable",
                "unknown",
                "not-applicable-unscored",
            ],
            list(evidence["mode_selectors"]),
        )
        self.assertEqual(
            {"identity", "context", "evidence", "sequence", "estate_escape"},
            set(components["footer"]["slot_selectors"]),
        )
        self.assertEqual(
            {"estate", "product", "tool", "editorial"},
            set(components["footer"]["variant_selectors"]),
        )

    def test_semantics_contract_matches_authority(self) -> None:
        semantics = json.loads((ROOT / "src/semantics.json").read_text(encoding="utf-8"))
        self.assertEqual("atlas-interface-kit/semantics/v1", semantics["schema_version"])
        self.assertEqual("2.0.0", semantics["authority"]["base_contract_version"])
        self.assertEqual("1.0.0", semantics["authority"]["foundation_extension_version"])
        self.assertEqual("1.0.0", semantics["authority"]["footer_extension_version"])
        self.assertEqual("1.0.0", semantics["authority"]["evidence_mode_extension_version"])
        evidence = semantics["evidence_mode_authority"]
        self.assertFalse(evidence["generated_output_is_evidence"])
        self.assertEqual(
            ["unavailable", "unknown", "not-applicable-unscored"],
            evidence["zero_may_not_represent"],
        )
        footer = semantics["footer_authority"]
        self.assertEqual(
            "AtlasReaper311/atlas-scheduler",
            footer["ownership"]["article_sequence_owner"],
        )
        self.assertEqual(
            ["identity", "sequence", "estate_escape"],
            footer["variants"]["editorial"]["required_slots"],
        )

    def test_faint_text_meets_wcag_aa_on_all_atlas_surfaces(self) -> None:
        tokens = json.loads((ROOT / "src/tokens.json").read_text(encoding="utf-8"))
        faint = tokens["colour"]["text_faint"]
        for surface in ("bg", "bg_1", "bg_2"):
            self.assertGreaterEqual(contrast_ratio(faint, tokens["colour"][surface]), 4.5)

    def test_css_has_no_remote_runtime_dependency_and_includes_contracts(self) -> None:
        self.build()
        css = (DIST / "atlas-interface-kit.css").read_text(encoding="utf-8")
        self.assertNotIn("http://", css)
        self.assertNotIn("https://", css)
        for selector in (
            ".atlas-evidence-mode",
            ".atlas-evidence-surface",
            ".atlas-evidence-value",
            ".atlas-footer__identity",
            ".atlas-footer__context",
            ".atlas-footer__evidence",
            ".atlas-footer__sequence",
            ".atlas-footer__escape",
            ".atlas-footer--estate",
            ".atlas-footer--product",
            ".atlas-footer--tool",
            ".atlas-footer--editorial",
        ):
            self.assertIn(selector, css)
        for mode in (
            "measured",
            "stale-measured",
            "recorded-replay",
            "simulated",
            "unavailable",
            "unknown",
            "not-applicable-unscored",
        ):
            self.assertIn(f"[data-evidence-mode='{mode}']", css)

    def test_fonts_are_woff2_and_ship_with_their_licences(self) -> None:
        self.build()
        fonts = sorted((DIST / "fonts").glob("*.woff2"))
        self.assertEqual(4, len(fonts))
        for font in fonts:
            self.assertEqual(b"wOF2", font.read_bytes()[:4])
        for licence in sorted((DIST / "licenses").glob("*.txt")):
            text = licence.read_text(encoding="utf-8")
            self.assertIn("SIL OPEN FONT LICENSE", text)
            self.assertIn("Version 1.1", text)


if __name__ == "__main__":
    unittest.main()
