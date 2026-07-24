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
VERSION = "0.2.0"
MIN_TEXT_CONTRAST = 4.5

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
    "text": "#e8e8e0", "text_dim": "#aaa9a0", "text_faint": "#888894",
    "accent": "#f5a623", "operational": "#4ade80", "unavailable": "#e24b4a",
    "informational": "#60a5fa",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def relative_luminance(value: str) -> float:
    require(value.startswith("#") and len(value) == 7, f"unsupported colour format: {value}")
    channels = [int(value[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(foreground: str, background: str) -> float:
    lighter, darker = sorted(
        (relative_luminance(foreground), relative_luminance(background)),
        reverse=True,
    )
    return (lighter + 0.05) / (darker + 0.05)


def main() -> int:
    subprocess.run([sys.executable, str(ROOT / "scripts/build.py")], check=True)
    tokens = load_json(ROOT / "src/tokens.json")
    components = load_json(ROOT / "src/components.json")
    manifest = load_json(DIST / "manifest.json")

    require(tokens.get("schema_version") == "atlas-interface-kit/tokens/v1", "invalid token schema")
    require(components.get("schema_version") == "atlas-interface-kit/components/v1", "invalid component schema")
    require(tokens.get("version") == manifest.get("version") == VERSION, "version mismatch")
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
    for surface in ("bg", "bg_1", "bg_2"):
        ratio = contrast_ratio(tokens["colour"]["text_faint"], tokens["colour"][surface])
        require(
            ratio >= MIN_TEXT_CONTRAST,
            f"text_faint contrast against {surface} is {ratio:.2f}:1; expected at least {MIN_TEXT_CONTRAST}:1",
        )

    role_map = {item["role"]: item["selector"] for item in components["roles"]}
    require(set(role_map) == EXPECTED_ROLES, "component role contract is incomplete")
    require(len(role_map) == manifest.get("component_role_count"), "component role count mismatch")

    css = (DIST / "atlas-interface-kit.css").read_text(encoding="utf-8")
    require("http://" not in css and "https://" not in css, "runtime CSS must not contain remote dependencies")
    require(":focus-visible" in css, "visible focus foundation is missing")
    require("prefers-reduced-motion" in css, "reduced-motion foundation is missing")
    for role, selector in role_map.items():
        require(selector in css, f"generated CSS missing selector for {role}: {selector}")

    font_css = (DIST / "atlas-fonts.css").read_text(encoding="utf-8")
    require("http://" not in font_css and "https://" not in font_css, "font CSS must not contain remote dependencies")
    require(font_css.count("@font-face") == 4, "font CSS must declare the four approved faces")
    require(font_css.count("font-display: swap") == 4, "every font face must render with swap")
    require("IBM Plex Mono" in font_css, "IBM Plex Mono declaration is missing")
    require("DM Serif Display" in font_css, "DM Serif Display declaration is missing")

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
