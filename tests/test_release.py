from __future__ import annotations

import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_release


class ReleaseArtifactTests(unittest.TestCase):
    def test_release_archive_is_deterministic_and_contains_contract_files(self) -> None:
        with tempfile.TemporaryDirectory() as first_dir:
            first = build_release.build_release(Path(first_dir), validate=True)
            first_bytes = Path(first["archive"]).read_bytes()
        with tempfile.TemporaryDirectory() as second_dir:
            second = build_release.build_release(Path(second_dir), validate=True)
            second_bytes = Path(second["archive"]).read_bytes()
            with tarfile.open(Path(second["archive"]), "r:gz") as archive:
                names = set(archive.getnames())
        self.assertEqual(first_bytes, second_bytes)
        prefix = "atlas-interface-kit-0.3.0"
        self.assertIn(f"{prefix}/dist/manifest.json", names)
        self.assertIn(f"{prefix}/dist/semantics.json", names)
        self.assertIn(f"{prefix}/docs/BRAND_REFERENCE.md", names)
        self.assertIn(f"{prefix}/docs/CONSUMER_CONTRACT.md", names)
        self.assertIn(f"{prefix}/docs/FOUNDATION_EXTENSION.md", names)
        self.assertIn(f"{prefix}/release-manifest.json", names)


if __name__ == "__main__":
    unittest.main()
