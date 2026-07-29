#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import subprocess
import sys
import tarfile
from io import BytesIO
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "atlas-interface-kit"
SCHEMA_VERSION = "atlas-release-artifact/v1"
RELEASE_MEMBERS = (
    "VERSION", "README.md", "LICENSE", "docs/BRAND_REFERENCE.md",
    "docs/CONSUMER_CONTRACT.md", "docs/FOUNDATION_EXTENSION.md",
    "dist/atlas-fonts.css", "dist/atlas-interface-kit.css", "dist/components.json",
    "dist/manifest.json", "dist/semantics.json", "dist/tokens.json",
    "dist/fonts/dm-serif-display-400-italic.woff2", "dist/fonts/dm-serif-display-400.woff2",
    "dist/fonts/ibm-plex-mono-400.woff2", "dist/fonts/ibm-plex-mono-500.woff2",
    "dist/licenses/DM-Serif-Display-OFL.txt", "dist/licenses/IBM-Plex-Mono-OFL.txt",
)


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_version() -> str:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not version:
        raise RuntimeError("VERSION must not be empty")
    return version


def validate_inputs(version: str) -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts/check.py")], check=True)
    manifest = json.loads((ROOT / "dist/manifest.json").read_text(encoding="utf-8"))
    if manifest.get("version") != version:
        raise RuntimeError("dist/manifest.json version does not match VERSION")


def release_manifest(version: str) -> dict[str, Any]:
    files = []
    for relative in RELEASE_MEMBERS:
        path = ROOT / relative
        if not path.is_file():
            raise RuntimeError(f"release member is missing: {relative}")
        data = path.read_bytes()
        files.append({"path": relative, "bytes": len(data), "sha256": sha256(data)})
    return {
        "schema_version": SCHEMA_VERSION,
        "package": PACKAGE,
        "version": version,
        "release_tag": f"v{version}",
        "distribution_model": "copy-pinned-release-files-no-runtime-imports",
        "files": files,
    }


def write_tarball(output_dir: Path, version: str, manifest: dict[str, Any]) -> Path:
    archive_path = output_dir / f"{PACKAGE}-{version}.tar.gz"
    prefix = f"{PACKAGE}-{version}"
    entries = [(relative, (ROOT / relative).read_bytes()) for relative in RELEASE_MEMBERS]
    entries.append(("release-manifest.json", canonical_json(manifest)))
    with archive_path.open("wb") as raw_file:
        with gzip.GzipFile(fileobj=raw_file, mode="wb", filename="", mtime=0) as gzip_file:
            with tarfile.open(fileobj=gzip_file, mode="w") as archive:
                for relative, data in entries:
                    info = tarfile.TarInfo(f"{prefix}/{relative}")
                    info.size = len(data)
                    info.mtime = 0
                    info.mode = 0o644
                    info.uid = 0
                    info.gid = 0
                    info.uname = ""
                    info.gname = ""
                    archive.addfile(info, BytesIO(data))
    return archive_path


def build_release(output_dir: Path, *, validate: bool = True) -> dict[str, str]:
    version = read_version()
    if validate:
        validate_inputs(version)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = release_manifest(version)
    manifest_path = output_dir / f"{PACKAGE}-{version}.release-manifest.json"
    manifest_path.write_bytes(canonical_json(manifest))
    archive_path = write_tarball(output_dir, version, manifest)
    return {
        "version": version,
        "archive": str(archive_path),
        "archive_sha256": sha256(archive_path.read_bytes()),
        "manifest": str(manifest_path),
        "manifest_sha256": sha256(manifest_path.read_bytes()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a deterministic Atlas Interface Kit release artifact.")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "reports" / "release")
    parser.add_argument("--skip-validation", action="store_true")
    args = parser.parse_args()
    result = build_release(args.output_dir, validate=not args.skip_validation)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
