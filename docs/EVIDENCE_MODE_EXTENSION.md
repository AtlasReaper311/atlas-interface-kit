# Evidence mode extension

## Purpose

This document describes the Interface Kit implementation of the accepted Atlas Infra evidence-mode authority.

The source authority is:

- `AtlasReaper311/atlas-infra:policy/public-interface-evidence-mode-extension-v1.json`;
- version `1.0.0`;
- accepted under ADR-0008.

The kit supplies selectors, neutral presentation foundations, machine-readable contracts, and deterministic fingerprints. Consumers retain evidence-source selection, mode selection, runtime-state calculation, wording, and product behaviour.

## Separate axes

Maturity, runtime state, and evidence mode answer different questions.

- Maturity describes public commitment.
- Runtime state describes system condition.
- Evidence mode describes how a displayed claim was obtained.

Consumers must not collapse these axes into one badge, colour, or status value.

## Accepted evidence modes

The seven modes are:

1. Measured
2. Stale measured
3. Recorded replay
4. Simulated
5. Unavailable
6. Unknown
7. Not applicable / unscored

`Generated` remains a directory data mode for product output. It is not an evidence mode when the output does not stand in for a measurement or assert a real system condition.

## Shared selectors

Use:

```html
<section class="atlas-evidence-surface" data-evidence-mode="simulated">
  <span class="atlas-evidence-mode" data-evidence-mode="simulated">
    Simulated
  </span>
  <output class="atlas-evidence-value" data-evidence-mode="simulated">
    72
  </output>
</section>
```

The accepted selectors are:

- `.atlas-evidence-mode`;
- `.atlas-evidence-surface`;
- `.atlas-evidence-value`.

The accepted attributes are:

- `data-evidence-mode`;
- `data-runtime-state`.

A runtime-state attribute is optional when no runtime state is presented. It must remain separate from `data-evidence-mode` when both are present.

## Presentation boundaries

A visible evidence-mode label is required on evidence-bearing operational surfaces.

The shared foundation provides:

- visible text treatment;
- neutral surface treatment for replayed, simulated, unavailable, unknown, and unscored modes;
- tabular numeral support;
- distinct replay and simulation border treatment;
- machine-readable selectors for repository-native tests.

Consumers must also enforce numeral meaning:

- unavailable uses an em dash;
- unknown uses an em dash;
- not applicable or unscored uses explicit text;
- zero is permitted only when zero is an actual measured, stale-measured, replayed, or simulated value.

The fallback mode must remain visible across primary state, metrics, tables, and charts. Supporting prose alone is insufficient.

## Ownership boundary

The Interface Kit does not:

- fetch evidence;
- infer evidence mode;
- calculate runtime state;
- replace values;
- rewrite charts;
- provide shared runtime JavaScript;
- change endpoint contracts;
- change anomaly or conformance calculations.

Consumers implement those behaviours locally and prove them through repository-native tests and previews.

## Distribution

This extension is included in Interface Kit `0.5.0`.

Consumers must copy the pinned release files, verify `manifest.json`, run their own semantic and accessibility checks, capture deterministic screenshots for changed routes, and obtain manual visual approval before merge.
