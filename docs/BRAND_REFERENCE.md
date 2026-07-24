# Atlas Systems Brand Reference

## Purpose

This document is the canonical maintained brand reference for Atlas Systems browser interfaces and visual artefacts.

It defines the stable visual identity shared across the estate while preserving the boundary between common foundations and product-owned presentation. Executable tokens, components, font assets, manifests, checks, and accepted architecture decisions remain higher authority.

## Authority and ownership

Use this order when deciding interface behaviour:

1. Current files, generated bundles, checks, and tests in `atlas-interface-kit`.
2. Accepted public-interface ADRs in `AtlasReaper311/atlas-infra`.
3. Current source and product contracts in the consuming repository.
4. This Brand Reference.
5. Historical screenshots, detached copies, design notes, and conversation memory.

`atlas-interface-kit` owns shared tokens, typography assets, component foundations, and deterministic distribution. Consuming repositories own content, route structure, product-specific controls, data behaviour, deployment, and rollback.

A shared appearance must not create a shared runtime dependency. Consumers copy a pinned bundle into their own repository and verify its manifest locally.

## Visual character

Atlas Systems is dark, terminal-oriented, precise, restrained, and visibly hand-crafted. The estate should feel related without making every surface identical.

The visual system should communicate:

- technical evidence rather than decorative complexity;
- clear state and ownership boundaries;
- dense information with controlled hierarchy;
- calm motion and deliberate interaction;
- product identity inside a recognisable Atlas Systems frame.

Avoid generic dashboard styling, excessive glow, ornamental gradients without information value, and effects that reduce readability.

## Core colour tokens

| Token | Value | Primary use |
| --- | --- | --- |
| `--bg` | `#0a0a0f` | Page background |
| `--bg-1` | `#111118` | Cards, sidebars, and primary raised surfaces |
| `--bg-2` | `#1a1a24` | Nested and deeper surfaces |
| `--border` | `rgba(255,255,255,0.08)` | Default borders and separators |
| `--border-hi` | `rgba(255,255,255,0.16)` | Hover, focus-adjacent, and stronger boundaries |
| `--text` | `#e8e8e0` | Primary text |
| `--text-dim` | `#aaa9a0` | Body and secondary text |
| `--text-faint` | Current Interface Kit token | Metadata and low-emphasis labels with validated contrast |
| `--accent` | `#f5a623` | Primary interaction and Atlas amber identity |
| `--accent-dim` | `rgba(245,166,35,0.12)` | Active and selected backgrounds |
| `--status-live` | `#4ade80` | Operational and confirmed-live state |
| `--status-down` | `#e24b4a` | Error and unavailable state |
| `--accent-hover` | `#f7b84a` | Approved brighter amber interaction state |

The generated Interface Kit token files are authoritative for exact current names and accessibility-adjusted values. Do not duplicate stale token tables inside product CSS.

## Semantic colour rules

Colour is never the only carrier of meaning.

- Operational state combines colour with text and, where appropriate, a distinct marker shape.
- Warning, preview, and experiment states remain distinguishable through labels, borders, patterns, or geometry.
- Error red is reserved for failures, destructive actions, and explicit incident evidence.
- Amber indicates Atlas identity, interaction, selected state, or bounded caution. It must not silently mean every non-production condition.
- Product families may introduce restrained secondary accents when their meaning is documented and contrast remains valid.

## Typography

### Roles

| Role | Typeface | Weight |
| --- | --- | --- |
| Display headings | DM Serif Display | 400 regular and italic |
| Interface, body, metadata, and code-like labels | IBM Plex Mono | 400 and 500 |
| Serif fallback | Georgia | Platform default |
| Mono fallback | monospace | Platform default |

### Repository-local distribution contract

Google Fonts imports are not part of the current Atlas Systems runtime contract.

The approved typefaces are distributed as repository-local WOFF2 assets through the pinned Interface Kit bundle. Every consuming repository must:

1. copy the versioned font stylesheet, font files, licences, and manifest records into its own source tree;
2. verify file sizes and SHA-256 fingerprints with repository-native checks;
3. serve assets from its own origin;
4. keep `font-src` restricted to the approved local policy;
5. preserve the bundled SIL Open Font License files;
6. avoid runtime imports from GitHub, `atlas-interface-kit`, Google Fonts, or another Atlas Systems domain.

This model removes cross-domain availability and privacy dependencies while keeping each public surface independently deployable and reversible.

### Typography behaviour

- Display type provides hierarchy and editorial character; it is not used for controls or dense operational data.
- IBM Plex Mono carries the system voice across navigation, prose, metadata, tables, controls, and evidence.
- Long-form prose prioritises line length and line height over visual density.
- Uppercase labels use restrained tracking and remain short.
- Italic display emphasis is selective and does not replace structural hierarchy.

## Layout foundations

| Property | Reference value |
| --- | --- |
| Base font size | `14px` to `15px`, according to the consuming surface contract |
| Base line height | Approximately `1.6` to `1.7` |
| Global header height | `56px` |
| Main content width | Approximately `1100px` to `1180px` |
| Long-form prose width | Approximately `720px` |
| Background grid | `80px × 80px` at very low contrast |
| Minimum interactive target | Current Interface Kit touch token, normally at least `44px` |

These values are foundations, not instructions to flatten every product into one template. Ramone, Status, API Docs, the CV viewer, the main portfolio, and Lab tools retain purpose-specific composition inside shared accessibility and navigation contracts.

## Spacing and density

- Use the generated spacing scale rather than introducing near-duplicate values casually.
- Separate information groups through spacing before adding borders.
- Dense operational surfaces may use smaller gaps, but controls and readable text retain minimum target and line-height contracts.
- Cards are not default containers for every element. Use sections, rails, tables, lists, and direct page composition when they communicate structure more clearly.

## Shape, borders, and elevation

- Borders are quiet structural signals, normally using `--border`.
- Hover and selected boundaries use `--border-hi`, semantic colour, or both.
- Corners remain restrained. Small radii support controls and cards; large consumer-product rounding is not part of the core identity.
- Shadows are limited and purposeful. They may establish a flagship surface or overlay boundary but should not create floating layers everywhere.
- Dashed and patterned borders may represent experimental, simulated, or incomplete contracts when the accompanying label states the meaning.

## Navigation and estate identity

Public browser surfaces use the accepted Atlas Systems navigation order and product-boundary rules from current interface authority.

The global frame should provide:

- a recognisable Atlas Systems wordmark;
- predictable primary route order;
- an aggregate status route where appropriate;
- bounded estate search where approved;
- mobile navigation that preserves the same route model;
- a product strip or local identity when the surface has its own purpose;
- a clear route back to the wider estate.

Atlas-owned destinations normally open in the current tab. External destinations may open in a new tab only when the interaction contract and accessible labelling justify it.

## Cards and directories

Cards communicate a destination, an action, a bounded status summary, or a distinct piece of evidence. Combining several roles requires a clear hierarchy.

Directory cards should expose:

- purpose or type;
- title;
- concise distinction;
- maturity when relevant;
- data mode when evidence provenance matters;
- a clear route label;
- product-specific visual signature where useful.

Maturity and data mode are separate facts. Runtime health is a third fact and must not be implied by either.

Recommended maturity language:

- `Production`: stable public product or surface;
- `Tool`: focused engineering utility;
- `Preview`: usable interface with a contract still being refined;
- `Experiment`: exploratory behaviour without a stable product contract.

Recommended data-mode language:

- `Live`: current bounded public evidence;
- `Replay`: captured evidence played back;
- `Generated`: output produced in the browser or engine now;
- `Simulated`: explicit non-live scenario data.

Labels, marker shapes, border treatment, and text preserve distinctions for users who cannot rely on colour.

## Status and evidence language

Use evidence-specific language:

- `checking` while current state is unresolved;
- `operational` for confirmed working state;
- `degraded` when the service remains available with reduced function;
- `unavailable` when the bounded check cannot be used;
- `unknown` when evidence is absent, stale, malformed, or outside its contract.

Do not translate a missing response into a healthy state. Do not present repository state as runtime evidence.

## Interaction and accessibility

Every consuming surface preserves the current Interface Kit accessibility contract.

Required principles include:

- visible keyboard focus;
- logical tab order;
- focus containment and restoration for dialogs;
- semantic headings and landmarks;
- labelled controls and icon-only actions;
- reduced-motion handling;
- no information conveyed by colour alone;
- readable contrast for body, metadata, and state text;
- responsive layouts without horizontal page overflow;
- zoom behaviour that does not hide core actions;
- minimum touch-target sizing;
- static metadata and navigation that remain meaningful without JavaScript.

Motion supports state change and spatial understanding. It does not exist merely to make an interface feel active.

## Icons and visual motifs

Use simple repository-local SVG, CSS geometry, or approved local raster assets.

- Icons explain action, category, state, or product identity.
- Decorative motifs remain subordinate to text and interaction.
- Icon-only controls require accessible names.
- Shared action icons follow the Interface Kit component contract.
- Product-specific motifs remain in the owning repository.
- Do not introduce remote icon-font or runtime CDN dependencies.

## Images and social previews

Social-preview cards use the current deterministic generator and route-ownership model in `atlas-systems`.

- output size is `1200 × 630`;
- each public route uses a route-specific image where the catalogue defines one;
- Open Graph and Twitter image URLs, dimensions, and alt text remain static in source;
- satellite products may reference centrally hosted cards while retaining metadata ownership in their own repositories;
- generated image files, source manifest entries, and HTML metadata remain in sync;
- cache-version changes accompany an actual visual revision, not routine source churn.

Screenshots and gallery images require an owning source, accurate alternative text or deliberate decorative treatment, and a publishing path that does not bypass generated-content authority.

## Backgrounds and effects

The base page uses `#0a0a0f`. A restrained grid may use approximately `rgba(255,255,255,0.02)` to `0.03` with an `80px` rhythm.

Glow, blur, gradients, noise, and scanline effects are optional product-level devices. They must not reduce text contrast, obscure focus, imply a false live state, or become the only distinction between sections.

## Product-specific identity

Consistency means shared foundations and predictable behaviour, not identical pages.

A product may own:

- composition and information hierarchy;
- bounded secondary accent colours;
- specialist controls;
- data visualisation;
- local motifs and imagery;
- product footer content;
- task-specific responsive behaviour.

A product must not independently redefine global route order, focus visibility, status semantics, font distribution, security policy, or shared token meaning without an accepted authority change.

## Content and voice

Public interface copy targets senior engineers.

- State what the system does and where its boundary lies.
- Prefer measured evidence to adjectives.
- Explain non-obvious tradeoffs.
- Distinguish implemented, validated, merged, deployed, live-verified, and planned states.
- Avoid marketing language and inflated capability claims.
- Keep labels compact and prose readable.
- Do not expose private identities, internal endpoints, secrets, or provider details.

## Security and privacy

Visual and asset choices preserve the consuming repository's security contract.

- Fonts, icons, scripts, styles, and primary images are repository-local unless a reviewed contract permits an external source.
- Content Security Policy is as restrictive as the product allows.
- Third-party embeds and analytics are not assumed parts of the brand.
- Public metadata does not disclose private infrastructure.
- Browser-facing surfaces expose the estate's approved `security.txt` contact through their owning deployment.

## Implementation workflow

For a shared visual-system change:

1. inspect current ADRs, Interface Kit source, generated files, and tests;
2. change source tokens or component contracts, not generated output alone;
3. rebuild the deterministic bundle;
4. run repository checks and inspect the manifest diff;
5. open a focused Interface Kit pull request;
6. merge only after validation and visual review where applicable;
7. adopt the new pinned bundle through separate consumer pull requests;
8. run each consumer's tests, isolated preview, and browser evidence;
9. merge consumers independently;
10. verify each production surface separately.

A merged Interface Kit release does not prove adoption or deployment.

## Validation checklist

```text
[ ] current Interface Kit source and accepted ADRs inspected
[ ] shared change belongs in the kit rather than one product
[ ] generated bundle rebuilt through its owner when source assets change
[ ] manifest sizes and SHA-256 fingerprints match
[ ] repository-local font and asset contract preserved
[ ] body and metadata contrast remain valid
[ ] keyboard focus and reduced motion preserved
[ ] mobile navigation and touch targets preserved
[ ] maturity, data mode, and runtime health remain separate
[ ] no information depends on colour alone
[ ] product-specific identity remains with its owner
[ ] consumer rollout is separate, pinned, and reversible
[ ] deployment and live verification are reported separately
```

## Maintenance

Update this document in the same programme of work when a change modifies stable visual identity, font distribution, shared token meaning, accessibility foundations, navigation behaviour, or the boundary between Interface Kit and product-owned presentation.

Do not copy short-lived deployment state, current service counts, or individual page inventories into this reference. Those belong to live repository and runtime authorities.
