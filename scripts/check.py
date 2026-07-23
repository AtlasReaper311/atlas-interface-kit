#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

EXPECTED_ROLES = {
    "global-header", "product-strip", "page-introduction", "section-heading",
    "primary-action", "secondary-action", "text-action", "status-chip",
    "type-badge", "maturity-badge", "metric-grid", "standard-card",
    "editorial-card", "data-card", "interactive-card-frame", "tag-list",
    "filter-bar", "table-wrapper", "search-dialog", "loading-state",
    "empty-state", "unavailable-state", "unknown-state", "error-state", "footer",
}
EXPECTED_COLOURS = {
    "bg": "#0a0a0f", "bg_1": "#111118", "bg_2": "#1a1a24",
    "text": "#e8e8e0", "text_dim": "#aaa9a0", "accent": "#f5a623",
    "operational": "#4ade80", "unavailable": "#e24b4a", "informational": "#60a5fa",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> int:
    subprocess.run([sys.executable, str(ROOT / "scripts/build.py")], check=True)
    tokens = load_json(ROOT / "src/tokens.json")
    components = load_json(ROOT / "src/components.json")
    manifest = load_json(DIST / "manifest.json")

    require(tokens.get("schema_version") == "atlas-interface-kit/tokens/v1", "invalid token schema")
    require(components.get("schema_version") == "atlas-interface-kit/components/v1", "invalid component schema")
    require(tokens.get("version") == manifest.get("version") == "0.1.0", "version mismatch")
    require(tokens.get("contract_version") == manifest.get("contract_version") == "2.0.0", "contract version mismatch")
    require(tokens["space_px"] == [4, 8, 12, 16, 24, 32, 48, 64, 96], "spacing scale drifted")
    require(tokens["control_px"] == {"compact": 32, "standard": 40, "touch_min": 44}, "control scale drifted")
    require(tokens["radius_px"] == {"sm": 4, "md": 6, "lg": 8}, "radius scale drifted")
    require(tokens["breakpoint_px"] == {"mobile": 640, "tablet": 768, "desktop": 1024, "wide": 1440}, "breakpoint scale drifted")
    require(tokens["type_px"]["body"] >= 15, "body text must remain at least 15px")
    require(tokens["type_px"]["supporting"] >= 13, "supporting text must remain at least 13px")
    require(tokens["type_px"]["meta"] >= 11, "metadata text must remain at least 11px")
    for name, value in EXPECTED_COLOURS.items():
        require(tokens["colour"].get(name) == value, f"colour token {name} drifted")

    role_map = {item["role"]: item["selector"] for item in components["roles"]}
    require(set(role_map) == EXPECTED_ROLES, "component role contract is incomplete")
    require(len(role_map) == manifest.get("component_role_count"), "component role count mismatch")

    css = (DIST / "atlas-interface-kit.css").read_text(encoding="utf-8")
    require("http://" not in css and "https://" not in css, "runtime CSS must not contain remote dependencies")
    require(":focus-visible" in css, "visible focus foundation is missing")
    require("prefers-reduced-motion" in css, "reduced-motion foundation is missing")
    for role, selector in role_map.items():
        require(selector in css, f"generated CSS missing selector for {role}: {selector}")

    for name, record in manifest["files"].items():
        path = DIST / name
        require(path.is_file(), f"manifest file is missing: {name}")
        require(path.stat().st_size == record["bytes"], f"manifest byte count mismatch: {name}")
        require(digest(path) == record["sha256"], f"manifest digest mismatch: {name}")

    require(not (ROOT / "bootstrap.sh").exists(), "one-time bootstrap.sh must not ship in the repository")
    require(not (ROOT / "PR_BODY.md").exists(), "one-time PR_BODY.md must not ship in the repository")
    print("Atlas Interface Kit validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
