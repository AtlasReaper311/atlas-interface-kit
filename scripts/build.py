#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
DIST = ROOT / "dist"
VERSION = "0.5.0"
CONTRACT_VERSION = "2.0.0"
FOUNDATION_EXTENSION_VERSION = "1.0.0"
FOOTER_EXTENSION_VERSION = "1.0.0"
EVIDENCE_MODE_EXTENSION_VERSION = "1.0.0"


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def css_variables(tokens: dict[str, Any]) -> str:
    lines = [
        f"/* Atlas Interface Kit v{VERSION} generated tokens. */",
        ":root {",
        "  color-scheme: dark;",
    ]
    for name, value in sorted(tokens["colour"].items()):
        lines.append(f"  --atlas-{name.replace('_', '-')}: {value};")
    for index, value in enumerate(tokens["space_px"], start=1):
        lines.append(f"  --atlas-space-{index}: {value}px;")
    for name, value in sorted(tokens["radius_px"].items()):
        lines.append(f"  --atlas-radius-{name}: {value}px;")
    for name, value in sorted(tokens["control_px"].items()):
        css_name = "touch-min" if name == "touch_min" else f"control-{name}"
        lines.append(f"  --atlas-{css_name}: {value}px;")
    for name, value in sorted(tokens["card_padding_px"].items()):
        lines.append(f"  --atlas-card-{name}: {value}px;")
    for name, value in sorted(tokens["content_px"].items()):
        css_name = "content" if name == "standard" else f"content-{name}"
        if name == "prose":
            css_name = "prose"
        lines.append(f"  --atlas-{css_name}: {value}px;")
    for name, value in sorted(tokens["type_px"].items()):
        lines.append(f"  --atlas-type-{name}: {value}px;")
    for name, value in sorted(tokens["motion_ms"].items()):
        lines.append(f"  --atlas-motion-{name}: {value}ms;")
    for name, value in sorted(tokens["easing"].items()):
        lines.append(f"  --atlas-easing-{name}: {value};")
    for name, value in sorted(tokens["breakpoint_px"].items()):
        lines.append(f"  --atlas-breakpoint-{name}: {value}px;")
    for name, value in sorted(tokens["z_index"].items()):
        lines.append(f"  --atlas-z-{name}: {value};")
    for name, value in sorted(tokens["shadow"].items()):
        lines.append(f"  --atlas-shadow-{name}: {value};")
    for name, value in sorted(tokens["font"].items()):
        lines.append(f"  --atlas-font-{name}: {value};")
    lines.extend(["}", ""])
    return "\n".join(lines)


def file_record(data: bytes) -> dict[str, Any]:
    return {"bytes": len(data), "sha256": sha256(data)}


def main() -> int:
    tokens = json.loads((SRC / "tokens.json").read_text(encoding="utf-8"))
    components = json.loads((SRC / "components.json").read_text(encoding="utf-8"))
    semantics = json.loads((SRC / "semantics.json").read_text(encoding="utf-8"))

    if any(document.get("version") != VERSION for document in (tokens, components, semantics)):
        raise SystemExit("source version does not match build version")
    if tokens.get("contract_version") != CONTRACT_VERSION:
        raise SystemExit("token contract version does not match build contract")

    authority = semantics.get("authority", {})
    expected_authority = {
        "base_contract_version": CONTRACT_VERSION,
        "foundation_extension_version": FOUNDATION_EXTENSION_VERSION,
        "footer_extension_version": FOOTER_EXTENSION_VERSION,
        "evidence_mode_extension_version": EVIDENCE_MODE_EXTENSION_VERSION,
    }
    for key, expected in expected_authority.items():
        if authority.get(key) != expected:
            raise SystemExit(f"semantic {key} does not match build contract")

    token_bytes = canonical_json(tokens)
    component_bytes = canonical_json(components)
    semantic_bytes = canonical_json(semantics)
    font_css_bytes = ((SRC / "fonts.css").read_text(encoding="utf-8").strip() + "\n").encode("utf-8")
    component_css = (SRC / "components.css").read_text(encoding="utf-8").strip()
    evidence_css = (SRC / "evidence-modes.css").read_text(encoding="utf-8").strip()
    css_bytes = (css_variables(tokens) + component_css + "\n\n" + evidence_css + "\n").encode("utf-8")

    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True, exist_ok=True)

    outputs = {
        "atlas-interface-kit.css": css_bytes,
        "atlas-fonts.css": font_css_bytes,
        "tokens.json": token_bytes,
        "components.json": component_bytes,
        "semantics.json": semantic_bytes,
    }
    for directory in ("fonts", "licenses"):
        for source in sorted((SRC / directory).iterdir()):
            outputs[f"{directory}/{source.name}"] = source.read_bytes()

    for name, data in outputs.items():
        path = DIST / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    footer = components["footer"]
    evidence_mode = components["evidence_mode"]
    manifest = {
        "schema_version": "atlas-interface-kit/bundle/v1",
        "version": VERSION,
        "contract_version": CONTRACT_VERSION,
        "foundation_extension_version": FOUNDATION_EXTENSION_VERSION,
        "footer_extension_version": FOOTER_EXTENSION_VERSION,
        "evidence_mode_extension_version": EVIDENCE_MODE_EXTENSION_VERSION,
        "component_role_count": len(components["roles"]),
        "semantic_contract_count": 5,
        "footer_slot_count": len(footer["slot_selectors"]),
        "footer_variant_count": len(footer["variant_selectors"]),
        "evidence_mode_count": len(evidence_mode["mode_selectors"]),
        "evidence_selector_count": 3,
        "files": {name: file_record(data) for name, data in sorted(outputs.items())},
    }
    (DIST / "manifest.json").write_bytes(canonical_json(manifest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
