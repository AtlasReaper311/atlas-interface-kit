<div align="center">
  <img src="https://raw.githubusercontent.com/AtlasReaper311/AtlasReaper311/main/atlas-icon-dark-256.png" width="88" alt="Atlas Systems"/>
</div>

# atlas-interface-kit

```text
┌─────────────────────────────────────────────┐
│  ATLAS SYSTEMS // atlas-interface-kit       │
│  Versioned browser interface foundations    │
└─────────────────────────────────────────────┘
```

[![CI](https://github.com/AtlasReaper311/atlas-interface-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/AtlasReaper311/atlas-interface-kit/actions/workflows/ci.yml)
![Language](https://img.shields.io/badge/language-Python-f5a623?style=flat-square&labelColor=0a0a0f)
![Assets](https://img.shields.io/badge/assets-CSS-4ade80?style=flat-square&labelColor=0a0a0f)
![Cost](https://img.shields.io/badge/cost-%C2%A30-aaa9a0?style=flat-square&labelColor=0a0a0f)

`atlas-interface-kit` builds deterministic, repository-local CSS bundles for Atlas Systems public browser surfaces. It implements the approved shared tokens and component roles without creating a cross-domain runtime dependency.

## Architecture

The repository stores source tokens and component CSS under `src/`. `scripts/build.py` copies the release CSS into `dist/` and emits a SHA-256 manifest. Product repositories consume pinned bundle copies and verify the recorded fingerprint in their own CI.

The package does not own product-specific controls. Ramone conversation controls, System SYMPHONY audio controls, Work galleries, Signal Garden instruments, and System Map nodes remain in their owning repositories.

## Validation

Run:

```bash
python3 scripts/check.py
python3 -m unittest discover -s tests -v
git diff --check
```

Validation checks deterministic output, required accessibility primitives, required tokens, touch-target policy, and bundle fingerprints.

## Distribution

Releases are intended to open update pull requests in adopted repositories. Public pages must load their repository-local copy. They must not load this repository's CSS over the network at runtime.

Visual changes require repository-native previews and manual approval before merge.

## How it fits into Atlas Systems

`atlas-interface-kit` implements the browser design-system authority accepted in `AtlasReaper311/atlas-infra`. It supplies versioned presentation foundations to `atlas-systems`, `status`, `ramone-edge`, `atlas-api-public`, and `atlas-doc-viewer` while leaving deployment and product behaviour with each repository.

A shared interface contract is safest when distribution is automated but runtime dependencies remain local, pinned, and independently reversible.

---

Part of [atlas-systems.uk](https://atlas-systems.uk)
