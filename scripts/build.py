#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
DIST = ROOT / "dist"
VERSION = "0.1.1"
CONTRACT_VERSION = "2.0.0"


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
    for name, value in tokens["colour"].items():
        lines.append(f"  --atlas-{name.replace('_', '-')}: {value};")
    for index, value in enumerate(tokens["space_px"], start=1):
        lines.append(f"  --atlas-space-{index}: {value}px;")
    for name, value in tokens["radius_px"].items():
        lines.append(f"  --atlas-radius-{name}: {value}px;")
    for name, value in tokens["control_px"].items():
        css_name = "touch-min" if name == "touch_min" else f"control-{name}"
        lines.append(f"  --atlas-{css_name}: {value}px;")
    for name, value in tokens["card_padding_px"].items():
        lines.append(f"  --atlas-card-{name}: {value}px;")
    for name, value in tokens["content_px"].items():
        css_name = "content" if name == "standard" else f"content-{name}"
        if name == "prose":
            css_name = "prose"
        lines.append(f"  --atlas-{css_name}: {value}px;")
    for name, value in tokens["type_px"].items():
        lines.append(f"  --atlas-type-{name}: {value}px;")
    for name, value in tokens["motion_ms"].items():
        lines.append(f"  --atlas-motion-{name}: {value}ms;")
    for name, value in tokens["easing"].items():
        lines.append(f"  --atlas-easing-{name}: {value};")
    for name, value in tokens["breakpoint_px"].items():
        lines.append(f"  --atlas-breakpoint-{name}: {value}px;")
    for name, value in tokens["z_index"].items():
        lines.append(f"  --atlas-z-{name}: {value};")
    for name, value in tokens["shadow"].items():
        lines.append(f"  --atlas-shadow-{name}: {value};")
    for name, value in tokens["font"].items():
        lines.append(f"  --atlas-font-{name}: {value};")
    lines.extend(["}", ""])
    return "\n".join(lines)


def file_record(data: bytes) -> dict[str, Any]:
    return {"bytes": len(data), "sha256": sha256(data)}


def main() -> int:
    tokens = json.loads((SRC / "tokens.json").read_text(encoding="utf-8"))
    components = json.loads((SRC / "components.json").read_text(encoding="utf-8"))
    if tokens.get("version") != VERSION or components.get("version") != VERSION:
        raise SystemExit("source version does not match build version")
    if tokens.get("contract_version") != CONTRACT_VERSION:
        raise SystemExit("token contract version does not match build contract")

    token_bytes = canonical_json(tokens)
    component_bytes = canonical_json(components)
    css_source = (SRC / "components.css").read_text(encoding="utf-8").strip() + "\n"
    css_bytes = (css_variables(tokens) + css_source).encode("utf-8")

    DIST.mkdir(parents=True, exist_ok=True)
    outputs = {
        "atlas-interface-kit.css": css_bytes,
        "tokens.json": token_bytes,
        "components.json": component_bytes,
    }
    for name, data in outputs.items():
        (DIST / name).write_bytes(data)

    manifest = {
        "schema_version": "atlas-interface-kit/bundle/v1",
        "version": VERSION,
        "contract_version": CONTRACT_VERSION,
        "component_role_count": len(components["roles"]),
        "files": {name: file_record(data) for name, data in sorted(outputs.items())},
    }
    (DIST / "manifest.json").write_bytes(canonical_json(manifest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
