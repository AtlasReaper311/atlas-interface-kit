# Atlas Systems Brand Reference

## Purpose

This document is the canonical implementation-facing brand reference for Atlas Systems browser interfaces.

It records the visual language, typography, layout, semantic colour use, component grammar, maturity language, motion rules, and distribution boundary implemented by `atlas-interface-kit`. It does not replace the accepted architecture decision or executable contracts.

Use this authority order:

1. accepted decisions and policy in `AtlasReaper311/atlas-infra`;
2. executable tokens, components, build tooling, and validation in this repository;
3. this reference;
4. product-specific presentation in each consuming repository;
5. historical copies and examples.

When this document conflicts with `src/tokens.json`, `src/components.json`, generated bundle files, or an accepted Atlas Infra policy, the executable authority wins and this document must be repaired.

## Brand character

Atlas Systems is dark, technical, restrained, and deliberately hand-crafted. Interfaces should feel like parts of one operating estate without collapsing distinct products into one template.

The shared visual character is:

- terminal-oriented but readable;
- editorial where explanation matters;
- information-first rather than decorative;
- precise about runtime state, maturity, data source, and evidence;
- spacious enough to support hierarchy and long-form reading;
- visually cohesive while preserving product-specific interaction models.

Avoid generic dashboard styling, heavy glass effects, excessive glow, decorative gradients without purpose, and colour used as unsupported status theatre.

## Ownership and distribution

`AtlasReaper311/atlas-infra` owns governance, policy, schemas, and accepted interface decisions.

`AtlasReaper311/atlas-interface-kit` owns:

- source design tokens;
- shared component-role contracts;
- repository-local font assets and licences;
- generated CSS and JSON bundles;
- deterministic build tooling;
- bundle fingerprints and validation.

Consuming repositories own their product-specific components, content, deployment, and visual approval.

A consumer copies one pinned, fingerprinted release into its own repository. Runtime imports from this repository, another Atlas Systems domain, Google Fonts, or another remote presentation host are prohibited. See [`CONSUMER_CONTRACT.md`](CONSUMER_CONTRACT.md).

## Colours

The executable colour authority is `src/tokens.json`.

| Token | Value | Primary use |
| --- | --- | --- |
| `--atlas-bg` | `#0a0a0f` | Page background and deepest ground |
| `--atlas-bg-1` | `#111118` | Cards, panels, and sidebars |
| `--atlas-bg-2` | `#1a1a24` | Nested surfaces and deeper grouping |
| `--atlas-border` | `rgba(255,255,255,0.08)` | Default one-pixel borders |
| `--atlas-border-hi` | `rgba(255,255,255,0.16)` | Hover, focus-adjacent, and emphasized borders |
| `--atlas-text` | `#e8e8e0` | Primary readable text |
| `--atlas-text-dim` | `#aaa9a0` | Supporting and secondary text |
| `--atlas-text-faint` | `#888894` | Metadata and labels that must remain readable |
| `--atlas-accent` | `#f5a623` | General brand and interaction accent |
| `--atlas-accent-hover` | `#f7b84a` | Amber hover state |
| `--atlas-accent-dim` | `rgba(245,166,35,0.12)` | Selected and active amber surfaces |
| `--atlas-status-operational` | `#4ade80` | Evidence-backed operational state |
| `--atlas-status-degraded` | `#f5a623` | Evidence-backed degraded state |
| `--atlas-status-unavailable` | `#e24b4a` | Evidence-backed unavailable or error state |
| `--atlas-status-unknown` | `#aaa9a0` | Unknown, stale, or unverified state |
| `--atlas-status-informational` | `#60a5fa` | Informational state and bounded secondary evidence |

An 80 by 80 pixel background grid may use white at approximately three per cent opacity. It must remain atmospheric and must not reduce text contrast.

### Semantic colour rules

Amber is the general Atlas Systems accent. It is not a healthy-state colour.

Green, amber, red, grey, and blue carry semantic meaning by default:

- green: operational;
- amber: degraded or a non-runtime brand accent, depending on context;
- red: unavailable or error;
- grey: unknown, stale, or neutral;
- blue: informational.

Runtime colours require current evidence. Maturity, category, ownership, and decorative identity must not imply runtime health.

Product identities and diagrams may use controlled secondary accents when the meaning is clear and contrast remains compliant.

## Typography

| Role | Typeface | Approved weights and styles |
| --- | --- | --- |
| Brand and editorial headings | `DM Serif Display` | 400 regular and 400 italic |
| Body, metadata, controls, operational text | `IBM Plex Mono` | 400 and 500 |
| Serif fallback | `Georgia` | platform-provided |
| Monospace fallback | `monospace` | platform-provided |

The approved files are shipped in `src/fonts/` and copied into each consumer through the versioned bundle:

- `dm-serif-display-400.woff2`;
- `dm-serif-display-400-italic.woff2`;
- `ibm-plex-mono-400.woff2`;
- `ibm-plex-mono-500.woff2`.

Every face uses `font-display: swap`. Font licences ship with the bundle under `licenses/`.

Do not use a Google Fonts import or another remote font URL. Consumers load their repository-local copy of `atlas-fonts.css` before their interface styles.

### Type scale

| Role | Size |
| --- | --- |
| Tiny, nonessential labels | `9px` |
| Metadata | `11px` |
| Supporting copy | `14px` |
| Body copy | `16px` |
| Shared title token | `42px` |

Body text should normally use `16px`. Supporting text should normally use `14px`. Tiny text is reserved for nonessential labels and must not carry critical instructions or state.

DM Serif Display supplies editorial contrast. Dense operational tools may rely more heavily on IBM Plex Mono, but they still follow the shared type and spacing rhythm.

## Spacing and sizing

### Spacing scale

Use only the shared values unless a product contract explicitly requires a bounded exception:

`4`, `8`, `12`, `16`, `24`, `32`, `48`, `64`, and `96` pixels.

### Content widths

| Role | Maximum width |
| --- | --- |
| Prose | `720px` |
| Standard content | `1100px` |
| Wide technical surface | `1360px` |

### Controls

| Role | Height |
| --- | --- |
| Compact control | `32px` |
| Standard control | `40px` |
| Minimum touch target | `44px` |

Visible control geometry may be smaller than 44 pixels only when the interactive hit area still reaches the minimum.

### Cards

| Density | Padding |
| --- | --- |
| Compact | `16px` |
| Standard | `24px` |
| Editorial | `32px` |

Standard cards use one-pixel borders and no shadow or minimal shadow. Floating UI may use `0 16px 48px rgba(0,0,0,0.32)`. Flagship experiences may use the controlled amber atmospheric shadow `0 0 48px rgba(245,166,35,0.12)`.

### Radius

Use four, six, or eight pixel radii. Large soft cards and pill-shaped containers should be used only when the component role requires them. Badges may use pill geometry.

## Breakpoints

| Name | Width |
| --- | --- |
| Mobile | `640px` |
| Tablet | `768px` |
| Desktop | `1024px` |
| Wide | `1440px` |

Desktop is the primary portfolio experience. Mobile remains a required interface, not a reduced afterthought.

The governed evidence matrix uses 320, 375, 768, 1024, and 1440 pixel viewports where full route evidence is required.

## Global navigation

The desktop header has three zones:

- left: Atlas Systems wordmark and aggregate estate status;
- centre: Work, Writing, Lab, Systems, About;
- right: compact estate search and keyboard shortcut.

The aggregate status label reports state only and links directly to `https://status.atlas-systems.uk/` in the same tab.

Mobile uses a bottom navigation for Work, Writing, Lab, Systems, and About. The top header retains the wordmark, aggregate status, and search control. Fixed navigation must not obscure content or focused controls.

Atlas-owned production destinations open in the same tab. External destinations use a new tab only when that behaviour is deliberate and include `noopener noreferrer`.

## Page hierarchy

Unless a route-specific interaction model requires a documented exception, public pages follow this order:

1. global header;
2. product or section identity;
3. eyebrow, identifier, or route type;
4. page title;
5. concise purpose;
6. primary state or action;
7. main content;
8. supporting evidence and metadata;
9. purpose-specific footer and estate escape.

This is an information hierarchy, not a universal HTML template.

## Shared component roles

The executable selector contract is `src/components.json` and currently defines 25 roles:

- global header;
- product strip;
- page introduction;
- section heading;
- primary, secondary, and text actions;
- status chip;
- type and maturity badges;
- metric grid;
- standard, editorial, data, and interactive card frames;
- tag list and filter bar;
- table wrapper;
- search dialog;
- loading, empty, unavailable, unknown, and error states;
- purpose-specific footer.

Products may implement these roles with local markup and product-specific controls. Shared roles do not transfer content, deployment, or interaction ownership into this repository.

## Maturity and runtime language

Maturity and runtime state are separate claims. A Production product may be unavailable. An Experiment may currently be operational.

The accepted maturity labels are:

| Label | Meaning |
| --- | --- |
| Production | Stable public product or surface with an established contract |
| Tool | Focused operational or engineering utility |
| Preview | Usable interface whose public contract is still being refined |
| Experiment | Exploratory behaviour without a stable product contract |
| Planned | Approved or declared future work that is not yet a usable public surface |
| Retired | Historical surface that is no longer an active public destination |

The accepted public runtime states are:

| State | Meaning |
| --- | --- |
| Operational | Public function is available within its current evidence boundary |
| Degraded | Public function remains available but is impaired |
| Unavailable | Public function is not available |
| Unknown | State cannot be established from fresh bounded evidence |

`Checking` is an initial interface state, not a runtime conclusion.

Experiments and evidence tools identify their data mode independently. Current modes include:

- Live: current bounded public evidence;
- Replay: captured evidence played back;
- Generated: output produced in the browser or engine now;
- Simulated: explicit non-live scenario data.

## Cards, badges, and visual signatures

Cards expose identity, purpose, and action in that order. Data mode and runtime state are included only when they help a visitor decide what the destination represents or whether it can be used.

Maturity badges require text as well as shape or border treatment. Preview and Experiment may share the amber family, but they must remain distinguishable without relying on hue alone.

Operation-specific diagrams, signatures, and mnemonics are encouraged when they explain what a system does. They must reserve their own layout area and must not collide with descriptions, data labels, controls, or calls to action.

Decorative imagery outside Work is not a default design device. Diagrams are preferred because they can communicate system behaviour, evidence, or architecture.

## Motion

Standard motion is restrained and uses the shared durations:

- fast: `120ms`;
- standard: `180ms`;
- reveal: `240ms`.

The standard easing is `cubic-bezier(0.2, 0, 0, 1)`. Emphasized product motion may use `cubic-bezier(0.2, 0, 0, 1.2)` within a justified product boundary.

Every animated interface requires complete `prefers-reduced-motion` behaviour. Reduced motion must remove nonessential movement without hiding content, state, or access to controls.

## Accessibility

The shared foundation requires:

- visible `:focus-visible` treatment;
- complete keyboard access;
- focus restoration for dialogs and temporary layers;
- minimum 44 pixel touch targets;
- readable contrast on every Atlas surface;
- semantic headings and landmarks;
- named controls and meaningful link text;
- horizontal containment at the governed viewport widths;
- reduced-motion support;
- status communication that does not depend on colour alone.

`text_faint` is `#888894` because metadata must meet WCAG AA contrast against `bg`, `bg_1`, and `bg_2`.

Serious accessibility failures block acceptance. These include keyboard traps, hidden focus, missing accessible names, invalid landmark or heading structure, contrast failure, and fixed navigation obscuring focused controls.

## Search, status, and state

Estate search is bounded to the approved public search contract. It must remain keyboard-contained and restore focus when closed.

Aggregate status is a link to the Status surface, not a local dashboard. It uses evidence-backed public vocabulary and fails to Unknown rather than inventing health.

Loading, empty, unavailable, unknown, and error states require explicit text. Do not use an indefinite spinner as the only explanation.

## Tables and dense technical content

Tables use a repository-local wrapper that permits horizontal scrolling without expanding the document viewport. Code and preformatted output follow the same containment rule.

Dense operational tools may use tighter information spacing within the shared scale, but primary actions, body text, focus treatment, and touch targets remain readable.

## Metadata and browser identity

Human-facing public routes provide, where applicable:

- a page-first browser title;
- description and canonical URL;
- theme colour;
- repository-local browser icons and web manifest;
- Open Graph title, description, URL, site name, image, dimensions, and alt text;
- Twitter card, title, description, image, and alt text.

Social images are static evidence of route identity. They must not claim live health or include volatile runtime data.

## Product identity

Shared foundations do not erase product character.

- Atlas Systems may retain its editorial homepage and technical estate identity.
- Ramone may retain its conversational startup and local-AI product controls.
- Status remains operational evidence.
- Public API Docs remain derived from OpenAPI authority.
- CV retains its protected document gate.
- Lab instruments may use unusual layouts and expressive behaviour within accessibility and estate-navigation boundaries.
- System SYMPHONY audio behaviour remains product-owned.

Product-specific type, colour, motion, or layout requires a clear boundary and must preserve the non-overridable accessibility, semantic state, spacing, breakpoint, navigation, and reduced-motion contracts.

## Validation and release

Before accepting a bundle or consumer update:

1. build the bundle deterministically;
2. verify every distributed file against `manifest.json`;
3. run repository-native semantic and accessibility checks;
4. build an isolated preview for every changed visual route;
5. capture the governed browser and viewport evidence;
6. receive manual visual approval for visual changes;
7. merge and roll out through the consuming repository's own deployment path;
8. verify live state separately.

A matching bundle fingerprint proves file integrity only. It does not prove accessibility, visual correctness, deployment, or live adoption.

## Historical reference correction

Earlier loose copies of the Brand Reference listed `#555560` for faint text and provided a Google Fonts import. Both are superseded.

The current faint-text authority is `#888894`. The current typography authority is the versioned repository-local font bundle. Historical copies should link to this document or be removed when their owning workflow permits it.
