# Consumer contract

## Purpose

This document defines how Atlas Systems repositories consume `atlas-interface-kit` without introducing runtime coupling.

## Required distribution model

A consumer copies these files from one pinned release:

- `atlas-interface-kit.css`;
- `tokens.json` when machine-readable tokens are required;
- `components.json` when repository-native validation uses canonical selectors;
- `manifest.json` for fingerprint verification.

A consumer must not load CSS or JavaScript from this repository at runtime. The copied bundle belongs to the consumer deployment and remains available when another Atlas Systems surface is unavailable.

## Verification

Before accepting an update, the consumer must:

1. verify each copied file against `manifest.json`;
2. run repository-native semantic and accessibility checks;
3. build a preview for every changed visual route;
4. capture the required deterministic screenshot evidence;
5. receive manual visual approval before merge.

A matching fingerprint proves bundle integrity. It does not prove that the consuming page is accessible, visually correct, deployed, or live.

## Overrides

Consumers may override only explicitly approved brand-expression tokens. They must not override focus visibility, semantic state colours, minimum contrast, minimum touch targets, spacing scale values, base breakpoints, global header behaviour, z-index meanings, or reduced-motion behaviour.

Purpose-specific components remain local to the consumer repository.
