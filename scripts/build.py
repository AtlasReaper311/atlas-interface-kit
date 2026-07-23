#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
DIST = ROOT / "dist"
VERSION = "0.1.0"

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> int:
    tokens = json.loads((SRC / "tokens.json").read_text(encoding="utf-8"))
    if tokens.get("version") != VERSION:
        raise SystemExit("tokens version does not match build version")
    css = (SRC / "components.css").read_bytes()
    DIST.mkdir(parents=True, exist_ok=True)
    (DIST / "atlas-interface-kit.css").write_bytes(css)
    manifest = {
        "schema_version": "atlas-interface-kit/bundle/v1",
        "version": VERSION,
        "files": {
            "atlas-interface-kit.css": {"sha256": sha256(css), "bytes": len(css)},
            "tokens.json": {"sha256": sha256((SRC / "tokens.json").read_bytes())}
        }
    }
    (DIST / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
