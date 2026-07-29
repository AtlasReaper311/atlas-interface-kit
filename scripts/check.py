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
VERSION = "0.3.0"
CONTRACT_VERSION = "2.0.0"
FOUNDATION_EXTENSION_VERSION = "1.0.0"
MIN_TEXT_CONTRAST = 4.5

EXPECTED_ROLES = {
    "global-header", "product-strip", "page-introduction", "section-heading",
    "primary-action", "secondary-action", "text-action", "status-chip",
    "type-badge", "maturity-badge", "metric-grid", "standard-card",
    "editorial-card", "data-card", "interactive-card-frame", "tag-list",
    "filter-bar", "table-wrapper", "breadcrumb-navigation",
    "status-announcement", "search-dialog", "loading-state", "empty-state",
    "unavailable-state", "unknown-state", "error-state", "footer",
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
    linear = [channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4 for channel in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(foreground: str, background: str) -> float:
    lighter, darker = sorted((relative_luminance(foreground), relative_luminance(background)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def validate_semantics(semantics: dict[str, Any]) -> None:
    require(semantics.get("schema_version") == "atlas-interface-kit/semantics/v1", "invalid semantic schema")
    require(semantics.get("version") == VERSION, "semantic version mismatch")
    authority = semantics.get("authority", {})
    require(authority.get("base_contract_version") == CONTRACT_VERSION, "semantic base contract version mismatch")
    require(authority.get("foundation_extension_version") == FOUNDATION_EXTENSION_VERSION, "semantic foundation extension version mismatch")

    breadcrumb = semantics.get("breadcrumb_navigation", {})
    require(breadcrumb.get("selector") == ".atlas-breadcrumbs", "breadcrumb selector drifted")
    require(breadcrumb.get("landmark") == "nav", "breadcrumb landmark must be nav")
    require(breadcrumb.get("accessible_name_required") is True, "breadcrumb name must be required")
    require(breadcrumb.get("ordered_list_required") is True, "breadcrumb ordered list must be required")
    require(breadcrumb.get("current_page") == ["text", "aria-current=page"], "breadcrumb current-page semantics drifted")
    require(breadcrumb.get("homepage_forbidden") is True, "homepage breadcrumbs must remain forbidden")
    require(breadcrumb.get("machine_surfaces_excluded") is True, "machine surfaces must remain excluded from breadcrumbs")

    announcement = semantics.get("status_announcement", {})
    require(announcement.get("default_semantics") == {"role": "status", "aria_live": "polite", "aria_atomic": "true"}, "status announcement defaults drifted")
    require(announcement.get("silent_on") == ["initial-poll", "unchanged-poll", "routine-refresh"], "routine status activity must remain silent")
    require(announcement.get("shared_runtime_javascript_forbidden") is True, "shared runtime JavaScript must remain forbidden")
    require(announcement.get("global_header_status_remains_aria_live_off") is True, "global header status must remain aria-live off")

    overflow = semantics.get("dense_data_overflow", {})
    require(overflow.get("extends_role") == "table-wrapper", "overflow must extend table-wrapper")
    require(overflow.get("overflow_state_attribute") == "data-overflow=true", "overflow state attribute drifted")
    require(overflow.get("when_overflowing", {}).get("tabindex") == "0", "overflowing regions must use tabindex 0")
    require(overflow.get("when_not_overflowing", {}).get("unnecessary_tab_stop_forbidden") is True, "non-overflowing regions must not add a tab stop")

    evidence = semantics.get("evidence", {})
    require(evidence.get("blocking_viewports_px") == [320, 375, 768, 1024, 1440], "blocking viewport matrix drifted")
    require(evidence.get("reporting_only_viewports_px") == [1920], "1920 reporting-only evidence is missing")
    for key in (
        "reporting_only_is_breakpoint",
        "reporting_only_is_budget",
        "reporting_only_changes_content_width",
        "reporting_only_changes_layout_tokens",
    ):
        require(evidence.get(key) is False, f"{key} must remain false")


def main() -> int:
    subprocess.run([sys.executable, str(ROOT / "scripts/build.py")], check=True)
    tokens = load_json(ROOT / "src/tokens.json")
    components = load_json(ROOT / "src/components.json")
    semantics = load_json(ROOT / "src/semantics.json")
    manifest = load_json(DIST / "manifest.json")

    require(tokens.get("schema_version") == "atlas-interface-kit/tokens/v1", "invalid token schema")
    require(components.get("schema_version") == "atlas-interface-kit/components/v1", "invalid component schema")
    require(tokens.get("version") == components.get("version") == semantics.get("version") == manifest.get("version") == VERSION, "version mismatch")
    require(tokens.get("contract_version") == manifest.get("contract_version") == CONTRACT_VERSION, "contract version mismatch")
    require(manifest.get("foundation_extension_version") == FOUNDATION_EXTENSION_VERSION, "foundation extension version mismatch")
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
        require(ratio >= MIN_TEXT_CONTRAST, f"text_faint contrast against {surface} is {ratio:.2f}:1; expected at least {MIN_TEXT_CONTRAST}:1")

    role_map = {item["role"]: item["selector"] for item in components["roles"]}
    require(set(role_map) == EXPECTED_ROLES, "component role contract is incomplete")
    require(len(role_map) == manifest.get("component_role_count") == 27, "component role count mismatch")
    require(manifest.get("semantic_contract_count") == 3, "semantic contract count mismatch")
    validate_semantics(semantics)

    css = (DIST / "atlas-interface-kit.css").read_text(encoding="utf-8")
    require("http://" not in css and "https://" not in css, "runtime CSS must not contain remote dependencies")
    require(":focus-visible" in css, "visible focus foundation is missing")
    require("prefers-reduced-motion" in css, "reduced-motion foundation is missing")
    require(".atlas-table-wrap[data-overflow='true']:focus-visible" in css, "overflow focus foundation is missing")
    require(".atlas-status-announcement--visually-hidden" in css, "announcement helper is missing")
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
