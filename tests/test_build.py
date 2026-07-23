from __future__ import annotations
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class BuildTests(unittest.TestCase):
    def test_build_is_deterministic(self) -> None:
        subprocess.run([sys.executable, str(ROOT / "scripts/build.py")], check=True)
        first = (ROOT / "dist/manifest.json").read_bytes()
        subprocess.run([sys.executable, str(ROOT / "scripts/build.py")], check=True)
        second = (ROOT / "dist/manifest.json").read_bytes()
        self.assertEqual(first, second)

    def test_manifest_matches_css(self) -> None:
        subprocess.run([sys.executable, str(ROOT / "scripts/build.py")], check=True)
        manifest = json.loads((ROOT / "dist/manifest.json").read_text(encoding="utf-8"))
        css = (ROOT / "dist/atlas-interface-kit.css").read_bytes()
        self.assertEqual(hashlib.sha256(css).hexdigest(), manifest["files"]["atlas-interface-kit.css"]["sha256"])

if __name__ == "__main__":
    unittest.main()
