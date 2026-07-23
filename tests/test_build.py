from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"


class BuildTests(unittest.TestCase):
    def build(self) -> None:
        subprocess.run([sys.executable, str(ROOT / "scripts/build.py")], check=True)

    def test_build_is_deterministic(self) -> None:
        self.build()
        first = {path.name: path.read_bytes() for path in sorted(DIST.iterdir()) if path.is_file()}
        self.build()
        second = {path.name: path.read_bytes() for path in sorted(DIST.iterdir()) if path.is_file()}
        self.assertEqual(first, second)

    def test_manifest_matches_every_distributed_file(self) -> None:
        self.build()
        manifest = json.loads((DIST / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(
            {"atlas-interface-kit.css", "components.json", "tokens.json"},
            set(manifest["files"]),
        )
        for name, record in manifest["files"].items():
            data = (DIST / name).read_bytes()
            self.assertEqual(len(data), record["bytes"])
            self.assertEqual(hashlib.sha256(data).hexdigest(), record["sha256"])

    def test_component_contract_covers_all_roles(self) -> None:
        components = json.loads((ROOT / "src/components.json").read_text(encoding="utf-8"))
        roles = {item["role"] for item in components["roles"]}
        self.assertEqual(25, len(roles))
        self.assertIn("global-header", roles)
        self.assertIn("search-dialog", roles)
        self.assertIn("error-state", roles)
        self.assertIn("footer", roles)

    def test_css_has_no_remote_runtime_dependency(self) -> None:
        self.build()
        css = (DIST / "atlas-interface-kit.css").read_text(encoding="utf-8")
        self.assertNotIn("http://", css)
        self.assertNotIn("https://", css)


if __name__ == "__main__":
    unittest.main()
