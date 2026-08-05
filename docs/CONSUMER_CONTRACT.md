# Consumer contract

## Purpose

This document defines how Atlas Systems repositories consume `atlas-interface-kit` without introducing runtime coupling.

[`BRAND_REFERENCE.md`](BRAND_REFERENCE.md) describes maintained visual guidance. [`FOUNDATION_EXTENSION.md`](FOUNDATION_EXTENSION.md) describes the measured semantic extension. [`FOOTER_EXTENSION.md`](FOOTER_EXTENSION.md) describes the footer slot and variant contract. [`EVIDENCE_MODE_EXTENSION.md`](EVIDENCE_MODE_EXTENSION.md) describes evidence origin and confidence semantics. Executable tokens, component contracts, semantic contracts, generated files, and fingerprints remain the source of truth.

## Required distribution model

A consumer copies these files from one pinned release:

- `atlas-interface-kit.css`;
- `atlas-fonts.css`, `fonts/`, and `licenses/` when consuming the approved typefaces;
- `tokens.json` when machine-readable tokens are required;
- `components.json` when repository-native validation uses canonical selectors, evidence roles, footer slots, or footer variants;
- `semantics.json` when repository-native validation uses breadcrumb, announcement, overflow, evidence-mode, evidence, or footer semantics;
- `manifest.json` for fingerprint verification.

A consumer must not load CSS, JavaScript, or fonts from this repository at runtime. The copied bundle belongs to the consumer deployment and remains available when another Atlas Systems surface is unavailable.

## Semantic adoption

Consumers implement semantic behaviour in their own source and tests.

- Breadcrumbs are optional and apply only to hierarchical human-facing routes. They require a labelled `nav`, an ordered list, and an explicit current-page representation.
- Status announcements occur only after meaningful user-visible transitions. Initial polling, unchanged polling, and routine refreshes remain silent. The global header status remains `aria-live="off"`.
- Dense regions receive an accessible name and `tabindex="0"` only while they genuinely overflow. Consumers own overflow detection and must remove the tab stop when overflow ends.
- The 1920-pixel viewport is reporting-only evidence. It is not a breakpoint, content-width token, layout token, or blocking budget.
- Footers use one purpose-specific `estate`, `product`, `tool`, or `editorial` variant. Consumers own identity, local context, evidence links, estate escape, wording, and destinations. Editorial article sequencing remains owned by `atlas-scheduler`.
- A normal page has one primary footer. Multiple footer landmarks require accessible names. Empty footer elements and empty rendered slots are forbidden.
- Atlas-owned HTML destinations remain in the same tab. External destinations open in a new tab with `rel="noopener noreferrer"`.

The release provides no shared runtime JavaScript. Consumers retain trigger logic, wording, route selection, content, variant selection, links, evidence-source selection, runtime-state calculation, and rendering.

## Evidence-mode structure

Evidence-bearing operational surfaces use:

- `.atlas-evidence-mode` for the visible mode label;
- `.atlas-evidence-surface` for the bounded surface treatment;
- `.atlas-evidence-value` for values whose numeral treatment is governed by evidence mode;
- `data-evidence-mode` with one accepted machine-readable value;
- `data-runtime-state` separately when runtime state is presented.

Accepted evidence modes are:

- `measured`;
- `stale-measured`;
- `recorded-replay`;
- `simulated`;
- `unavailable`;
- `unknown`;
- `not-applicable-unscored`.

A visible mode label is required. Colour must not be the only signal. Recorded replay, simulated, unavailable, unknown, and unscored surfaces use neutral treatment. Unavailable and unknown numeric values use an em dash. Not-applicable or unscored values use explicit text.

Generated product output remains outside the evidence taxonomy when it does not stand in for a measurement or assert a real system condition.

Consumers own mode selection from actual source conditions. The kit does not infer mode, rewrite values, fetch data, or calculate runtime state.

## Footer structure

The base role is `.atlas-footer`.

The shared slots are:

- `.atlas-footer__identity`;
- `.atlas-footer__context`;
- `.atlas-footer__evidence`;
- `.atlas-footer__sequence`;
- `.atlas-footer__escape`.

The shared variants are:

- `.atlas-footer--estate`;
- `.atlas-footer--product`;
- `.atlas-footer--tool`;
- `.atlas-footer--editorial`.

Consumers render only the slots permitted by the selected variant. The kit owns selectors, layout, responsive wrapping, focus foundations, and minimum target sizing. It does not generate footer content or publication order.

## Verification

Before accepting an update, the consumer must:

1. verify each copied file against `manifest.json`;
2. validate local markup against `components.json` and `semantics.json`;
3. validate evidence-mode labels, attributes, and numeral treatment where evidence is displayed;
4. validate the selected footer variant and its required, optional, and forbidden slots;
5. run repository-native semantic and accessibility checks;
6. build a preview for every changed visual route;
7. capture the required deterministic screenshot evidence;
8. receive manual visual approval before merge.

A matching fingerprint proves bundle integrity. It does not prove that the consuming page is accessible, visually correct, deployed, or live.

## Overrides

Consumers may override only explicitly approved brand-expression tokens. They must not override focus visibility, semantic state colours, minimum contrast, minimum touch targets, spacing scale values, base breakpoints, global header behaviour, z-index meanings, reduced-motion behaviour, evidence-mode meaning, or the footer ownership contract.

Purpose-specific content and product behaviour remain local to the consumer repository.
