# Release process

`atlas-interface-kit` is distributed as a GitHub Release artifact. It is not loaded by consumers at runtime, and it is not published to a package registry.

## Version source

The release version is declared in:

- `VERSION`;
- `scripts/build.py`;
- `scripts/check.py`;
- `src/tokens.json`;
- `src/components.json`;
- `src/semantics.json`;
- the README version badge.

All version declarations must move together in the same pull request.

## Build

Run:

```bash
python3 -m py_compile scripts/build.py scripts/check.py scripts/build_release.py
python3 scripts/check.py
python3 -m unittest discover -s tests -v
python3 scripts/build_release.py --output-dir reports/release
git diff --check
```

The release artifact contains the generated `dist/` bundle, the Brand Reference, the Consumer Contract, the measured Foundation Extension, the Footer Extension, the Evidence Mode Extension, the licence, and a release manifest with SHA-256 fingerprints.

## Publish

Create an annotated tag that matches `VERSION`, for example:

```bash
git tag -a v0.5.0 -m "atlas-interface-kit v0.5.0"
git push origin v0.5.0
```

The release workflow validates the bundle again and uploads the deterministic archive as a short-retention workflow artifact.

Manual `workflow_dispatch` is available for building an artifact from an existing tag, but it must use a tag in the form `v<version>`.

After reviewing the workflow artifact, publish the GitHub Release explicitly:

```bash
gh release create v0.5.0 reports/release/* \
  --title "atlas-interface-kit v0.5.0" \
  --notes-file reports/release/atlas-interface-kit-0.5.0.release-manifest.json \
  --verify-tag
```

Tag creation, workflow execution, artifact review, and GitHub Release publication remain separate approval gates from merging source.

## Rollback

Consumers copy files from a pinned release. To roll back, revert the consumer repository to the previous copied bundle and verify it against that release's `dist/manifest.json`.
