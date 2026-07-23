#!/usr/bin/env python3
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    subprocess.run([sys.executable, str(ROOT / "scripts/build.py")], check=True)
    tokens = json.loads((ROOT / "src/tokens.json").read_text(encoding="utf-8"))
    required = {"bg", "bg_1", "bg_2", "border", "text", "text_dim", "accent", "operational", "unavailable"}
    missing = required - set(tokens["colour"])
    if missing:
        raise SystemExit(f"missing required colour tokens: {sorted(missing)}")
    if tokens["control_px"]["touch_min"] < 44:
        raise SystemExit("touch target minimum must be at least 44px")
    css = (ROOT / "dist/atlas-interface-kit.css").read_text(encoding="utf-8")
    for required_text in (":focus-visible", "prefers-reduced-motion", ".atlas-page-intro", ".atlas-button", ".atlas-card"):
        if required_text not in css:
            raise SystemExit(f"generated CSS missing {required_text}")
    print("Atlas Interface Kit validation passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
