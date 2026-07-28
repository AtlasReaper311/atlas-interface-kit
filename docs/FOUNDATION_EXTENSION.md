# Measured foundation extension

## Authority

This document describes the `atlas-interface-kit` implementation of the accepted additive authority in:

- `AtlasReaper311/atlas-infra:policy/public-interface-foundation-extension-v1.json`;
- `AtlasReaper311/atlas-infra:docs/public-interface-phase-4-authority-extension.md`.

The base Public Interface System v2 contract remains active. This extension does not alter colour, spacing, typography, touch-target, content-width, or breakpoint tokens.

The executable implementation is:

- `src/components.json`;
- `src/semantics.json`;
- `src/components.css`;
- their deterministic files under `dist/`.

## Breadcrumb navigation

`.atlas-breadcrumbs` is an optional role for hierarchical human-facing routes.

Required consumer markup:

```html
<nav class="atlas-breadcrumbs" aria-label="Breadcrumb">
  <ol>
    <li><a href="/systems/">Systems</a></li>
    <li aria-current="page">Reliability</li>
  </ol>
</nav>
```

The current page may be plain text or use `aria-current="page"`. Do not add breadcrumbs to the homepage, JSON APIs, health endpoints, registry responses, or a purpose-specific experience where they duplicate primary navigation.

Consumers own route selection and labels.

## Transition-driven announcements

`.atlas-status-announcement` identifies status text that may be visible or visually hidden.

Default semantics:

```html
<p
  class="atlas-status-announcement atlas-status-announcement--visually-hidden"
  role="status"
  aria-live="polite"
  aria-atomic="true"
></p>
```

Update the text only after a meaningful user-visible state transition. Keep initial polling, unchanged polling, and routine refreshes silent. Reserve `role="alert"` for an immediate blocking failure.

The global header status remains `aria-live="off"`. Consumers own wording and trigger logic. The kit ships no runtime JavaScript.

## Dense-data overflow

`.atlas-table-wrap` may contain a table, code block, preformatted output, or another dense region.

Consumers detect whether the region genuinely overflows. While it overflows:

- set `data-overflow="true"`;
- provide an accessible name, normally with `aria-label` or `aria-labelledby`;
- set `tabindex="0"`;
- retain local horizontal scrolling.

When the region no longer overflows, remove `tabindex`. An unnecessary tab stop is a contract failure.

The CSS supplies containment, stable scrollbar space, and visible focus. It does not infer overflow or mutate markup.

## Evidence coverage

Blocking evidence viewports remain:

- 320 pixels;
- 375 pixels;
- 768 pixels;
- 1024 pixels;
- 1440 pixels.

The 1920-pixel viewport is reporting-only. It is not a CSS breakpoint, a content-width decision, a layout token, or a blocking performance budget.

## Distribution boundary

Consumers copy one pinned, fingerprinted release. Runtime imports and shared runtime JavaScript remain prohibited. Consumer adoption, preview review, merge, deployment, and live verification remain separate repository-owned actions.
