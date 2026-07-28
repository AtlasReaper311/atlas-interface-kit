# Consumer contract

## Purpose

This document defines how Atlas Systems repositories consume `atlas-interface-kit` without introducing runtime coupling.

[`BRAND_REFERENCE.md`](BRAND_REFERENCE.md) describes the maintained visual and implementation guidance. [`FOUNDATION_EXTENSION.md`](FOUNDATION_EXTENSION.md) describes the measured semantic extension. Executable tokens, component contracts, semantic contracts, generated files, and fingerprints remain the source of truth.

## Required distribution model

A consumer copies these files from one pinned release:

- `atlas-interface-kit.css`;
- `atlas-fonts.css`, `fonts/`, and `licenses/` when consuming the approved typefaces;
- `tokens.json` when machine-readable tokens are required;
- `components.json` when repository-native validation uses canonical selectors;
- `semantics.json` when repository-native validation uses breadcrumb, announcement, overflow, or evidence semantics;
- `manifest.json` for fingerprint verification.

A consumer must not load CSS, JavaScript, or fonts from this repository at runtime. The copied bundle belongs to the consumer deployment and remains available when another Atlas Systems surface is unavailable.

## Semantic adoption

Consumers implement semantic behaviour in their own source and tests.

- Breadcrumbs are optional and apply only to hierarchical human-facing routes. They require a labelled `nav`, an ordered list, and an explicit current-page representation.
- Status announcements occur only after meaningful user-visible transitions. Initial polling, unchanged polling, and routine refreshes remain silent. The global header status remains `aria-live="off"`.
- Dense regions receive an accessible name and `tabindex="0"` only while they genuinely overflow. Consumers own overflow detection and must remove the tab stop when overflow ends.
- The 1920-pixel viewport is reporting-only evidence. It is not a breakpoint, content-width token, layout token, or blocking budget.

The release provides no shared runtime JavaScript. Consumers retain trigger logic, wording, route selection, content, and rendering.

## Verification

Before accepting an update, the consumer must:

1. verify each copied file against `manifest.json`;
2. validate local markup against `components.json` and `semantics.json`;
3. run repository-native semantic and accessibility checks;
4. build a preview for every changed visual route;
5. capture the required deterministic screenshot evidence;
6. receive manual visual approval before merge.

A matching fingerprint proves bundle integrity. It does not prove that the consuming page is accessible, visually correct, deployed, or live.

## Overrides

Consumers may override only explicitly approved brand-expression tokens. They must not override focus visibility, semantic state colours, minimum contrast, minimum touch targets, spacing scale values, base breakpoints, global header behaviour, z-index meanings, or reduced-motion behaviour.

Purpose-specific components remain local to the consumer repository.
