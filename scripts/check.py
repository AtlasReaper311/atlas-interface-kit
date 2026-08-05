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
VERSION = "0.5.0"
CONTRACT_VERSION = "2.0.0"
EXTENSION_VERSION = "1.0.0"
MODES = [
    "measured",
    "stale-measured",
    "recorded-replay",
    "simulated",
    "unavailable",
    "unknown",
    "not-applicable-unscored",
]
BASE_ROLES = {
    "global-header",
    "product-strip",
    "page-introduction",
    "section-heading",
    "primary-action",
    "secondary-action",
    "text-action",
    "status-chip",
    "type-badge",
    "maturity-badge",
    "metric-grid",
    "standard-card",
    "editorial-card",
    "data-card",
    "interactive-card-frame",
    "tag-list",
    "filter-bar",
    "table-wrapper",
    "breadcrumb-navigation",
    "status-announcement",
    "search-dialog",
    "loading-state",
    "empty-state",
    "unavailable-state",
    "unknown-state",
    "error-state",
    "footer",
}
EXPECTED_ROLES = BASE_ROLES | {"evidence-mode", "evidence-surface", "evidence-value"}
EXPECTED_COLOURS = {
    "bg": "#0a0a0f",
    "bg_1": "#111118",
    "bg_2": "#1a1a24",
    "text": "#e8e8e0",
    "text_dim": "#aaa9a0",
    "text_faint": "#888894",
    "accent": "#f5a623",
    "operational": "#4ade80",
    "unavailable": "#e24b4a",
    "informational": "#60a5fa",
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def luminance(value: str) -> float:
    require(value.startswith("#") and len(value) == 7, f"unsupported colour: {value}")
    channels = [int(value[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [
        channel / 12.92 if channel <= 0.04045
        else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    ]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(foreground: str, background: str) -> float:
    lighter, darker = sorted((luminance(foreground), luminance(background)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def main() -> int:
    subprocess.run([sys.executable, str(ROOT / "scripts/build.py")], check=True)
    tokens = load(ROOT / "src/tokens.json")
    components = load(ROOT / "src/components.json")
    semantics = load(ROOT / "src/semantics.json")
    manifest = load(DIST / "manifest.json")

    require(
        tokens["version"]
        == components["version"]
        == semantics["version"]
        == manifest["version"]
        == VERSION,
        "version mismatch",
    )
    require(tokens["contract_version"] == manifest["contract_version"] == CONTRACT_VERSION, "contract mismatch")
    for key in (
        "foundation_extension_version",
        "footer_extension_version",
        "evidence_mode_extension_version",
    ):
        require(manifest[key] == EXTENSION_VERSION, f"{key} mismatch")
    authority = semantics["authority"]
    require(
        authority["evidence_mode_extension_source"]
        == "AtlasReaper311/atlas-infra:policy/public-interface-evidence-mode-extension-v1.json",
        "evidence-mode authority source drifted",
    )
    require(authority["evidence_mode_extension_version"] == EXTENSION_VERSION, "evidence-mode authority version drifted")

    require(tokens["space_px"] == [4, 8, 12, 16, 24, 32, 48, 64, 96], "spacing scale drifted")
    require(tokens["control_px"] == {"compact": 32, "standard": 40, "touch_min": 44}, "control scale drifted")
    require(tokens["breakpoint_px"] == {"mobile": 640, "tablet": 768, "desktop": 1024, "wide": 1440}, "breakpoint scale drifted")
    for name, value in EXPECTED_COLOURS.items():
        require(tokens["colour"].get(name) == value, f"colour token {name} drifted")
    for surface in ("bg", "bg_1", "bg_2"):
        require(
            contrast_ratio(tokens["colour"]["text_faint"], tokens["colour"][surface]) >= 4.5,
            f"text_faint contrast against {surface} is too low",
        )

    role_map = {item["role"]: item["selector"] for item in components["roles"]}
    require(set(role_map) == EXPECTED_ROLES, "component role contract is incomplete")
    require(manifest["component_role_count"] == len(role_map) == 30, "component role count mismatch")
    evidence_components = components["evidence_mode"]
    require(evidence_components["mode_attribute"] == "data-evidence-mode", "mode attribute drifted")
    require(set(evidence_components["mode_selectors"]) == set(MODES), "mode selectors drifted")
    require(
        {
            evidence_components["mode_label_selector"],
            evidence_components["surface_selector"],
            evidence_components["value_selector"],
        }
        == {".atlas-evidence-mode", ".atlas-evidence-surface", ".atlas-evidence-value"},
        "evidence selectors drifted",
    )

    evidence = semantics["evidence_mode_authority"]
    require(set(evidence["modes"]) == set(MODES), "evidence mode contracts drifted")
    require(evidence["directory_data_modes"] == ["Live", "Replay", "Generated", "Simulated"], "directory modes drifted")
    require(evidence["generated_output_is_evidence"] is False, "generated output must not become evidence")
    require(evidence["runtime_state_is_separate_from_evidence_mode"] is True, "runtime state must remain separate")
    require(evidence["maturity_is_separate_from_evidence_mode"] is True, "maturity must remain separate")
    require(evidence["semantic_runtime_hue_modes"] == ["measured", "stale-measured"], "runtime hue boundary drifted")
    require(
        evidence["neutral_surface_modes"]
        == ["recorded-replay", "simulated", "unavailable", "unknown", "not-applicable-unscored"],
        "neutral evidence modes drifted",
    )
    require(
        evidence["zero_may_not_represent"]
        == ["unavailable", "unknown", "not-applicable-unscored"],
        "zero prohibition drifted",
    )
    for key in (
        "visible_mode_label_required",
        "machine_readable_mode_required",
        "fallback_mode_must_remain_visible_across_primary_state_metrics_tables_and_charts",
        "directory_and_destination_vocabulary_must_agree",
        "colour_must_not_be_the_only_signal",
    ):
        require(evidence[key] is True, f"{key} must remain true")
    require(evidence["modes"]["unavailable"]["numeral_treatment"] == "em-dash", "unavailable must use em dash")
    require(evidence["modes"]["unknown"]["numeral_treatment"] == "em-dash", "unknown must use em dash")
    require(
        evidence["modes"]["not-applicable-unscored"]["numeral_treatment"]
        == "not-applicable-or-unscored-label",
        "unscored evidence requires explicit text",
    )

    footer = components["footer"]
    require(set(footer["slot_selectors"]) == {"identity", "context", "evidence", "sequence", "estate_escape"}, "footer slots drifted")
    require(set(footer["variant_selectors"]) == {"estate", "product", "tool", "editorial"}, "footer variants drifted")
    require(manifest["semantic_contract_count"] == 5, "semantic contract count mismatch")
    require(manifest["evidence_mode_count"] == 7, "evidence mode count mismatch")
    require(manifest["evidence_selector_count"] == 3, "evidence selector count mismatch")
    require(manifest["footer_slot_count"] == 5, "footer slot count mismatch")
    require(manifest["footer_variant_count"] == 4, "footer variant count mismatch")

    css = (DIST / "atlas-interface-kit.css").read_text(encoding="utf-8")
    require("http://" not in css and "https://" not in css, "runtime CSS contains a remote dependency")
    require(":focus-visible" in css, "focus-visible foundation is missing")
    require("prefers-reduced-motion" in css, "reduced-motion foundation is missing")
    for selector in role_map.values():
        require(selector in css, f"generated CSS missing {selector}")
    for mode in MODES:
        require(f"[data-evidence-mode='{mode}']" in css, f"generated CSS missing mode {mode}")

    font_css = (DIST / "atlas-fonts.css").read_text(encoding="utf-8")
    require("http://" not in font_css and "https://" not in font_css, "font CSS contains a remote dependency")
    require(font_css.count("@font-face") == 4, "font face count mismatch")
    require(font_css.count("font-display: swap") == 4, "font swap contract drifted")

    for name, record in manifest["files"].items():
        path = DIST / name
        require(path.is_file(), f"manifest file is missing: {name}")
        data = path.read_bytes()
        require(len(data) == record["bytes"], f"manifest byte count mismatch: {name}")
        require(hashlib.sha256(data).hexdigest() == record["sha256"], f"manifest digest mismatch: {name}")

    print("Atlas Interface Kit validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
