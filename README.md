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
![Version](https://img.shields.io/badge/version-0.1.1-f5a623?style=flat-square&labelColor=0a0a0f)
![Assets](https://img.shields.io/badge/assets-CSS%20%2B%20JSON-4ade80?style=flat-square&labelColor=0a0a0f)
![Runtime](https://img.shields.io/badge/runtime-repository--local-aaa9a0?style=flat-square&labelColor=0a0a0f)
![License](https://img.shields.io/badge/license-MIT-aaa9a0?style=flat-square&labelColor=0a0a0f)

`atlas-interface-kit` builds deterministic, repository-local browser assets for Atlas Systems public interfaces. It implements the token and component authority accepted in `AtlasReaper311/atlas-infra` without creating a cross-domain runtime dependency.

## Architecture

Source tokens and component contracts live under `src/`. `scripts/build.py` renders the CSS custom properties, appends the shared component foundations, copies the JSON contracts into `dist/`, and emits a SHA-256 manifest for every distributed file.

Product-specific controls remain in their owning repositories. Ramone conversation controls, System SYMPHONY audio controls, Work galleries, Signal Garden instruments, and System Map nodes consume the shared foundation without moving ownership into this repository.

## Bundle contract

The versioned release bundle contains:

- `dist/atlas-interface-kit.css` for shared tokens and component foundations;
- `dist/tokens.json` for machine-readable token values;
- `dist/components.json` for canonical component roles and selectors;
- `dist/manifest.json` for file sizes and SHA-256 fingerprints.

Consumers copy pinned release files into their own repository. Runtime imports from this repository or another Atlas Systems domain are prohibited.

See `docs/CONSUMER_CONTRACT.md` for the adoption and verification boundary.

## Validation

Run:

```bash
python3 -m py_compile scripts/build.py scripts/check.py
python3 scripts/check.py
python3 -m unittest discover -s tests -v
git diff --check
```

Validation checks deterministic output, immutable brand and accessibility tokens, WCAG AA contrast for readable faint text on every Atlas surface, all approved component roles, distributed file fingerprints, repository-local runtime behaviour, and generated-file cleanliness.

## Release process

A release updates the source contracts and generated bundle in the same pull request. Adopted repositories receive separate automated update pull requests, run their own tests and previews, and require manual visual approval before merge.

Merging this repository does not deploy a public interface. Production rollout remains owned by each consuming repository.

## Licence

This repository is released under the MIT License. See `LICENSE`.

## How it fits into Atlas Systems

`atlas-interface-kit` implements the Public Interface System v2 authority owned by `AtlasReaper311/atlas-infra`. It supplies versioned presentation foundations to `atlas-systems`, `status`, `ramone-edge`, `atlas-api-public`, and `atlas-doc-viewer` while leaving deployment, content, and product behaviour with each repository.

A shared interface contract is safest when distribution is automated but runtime assets remain local, pinned, independently testable, and independently reversible.

---

Part of [atlas-systems.uk](https://atlas-systems.uk) · MIT License
