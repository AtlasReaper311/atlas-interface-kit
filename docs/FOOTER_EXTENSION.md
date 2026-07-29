# Footer extension

## Authority

This release implements `AtlasReaper311/atlas-infra:policy/public-interface-footer-extension-v1.json` under ADR-0008.

The authority defines shared structure and behaviour while leaving wording, destinations, runtime data, publication sequencing, deployment, and rollout with their owning repositories.

## Variants

The component supports four purpose-specific variants:

| Variant | Required slots | Optional slots | Forbidden slots |
| --- | --- | --- | --- |
| `estate` | identity, estate escape | context, evidence | sequence |
| `product` | identity, estate escape | context, evidence | sequence |
| `tool` | identity, context, estate escape | evidence | sequence |
| `editorial` | identity, sequence, estate escape | context, evidence | none |

The variant selectors are:

- `.atlas-footer--estate`;
- `.atlas-footer--product`;
- `.atlas-footer--tool`;
- `.atlas-footer--editorial`.

Variant choice describes information architecture. It does not make every footer visually or editorially identical.

## Slots

The base footer selector is `.atlas-footer` on a semantic `footer` element.

| Slot | Selector | Owner |
| --- | --- | --- |
| Identity | `.atlas-footer__identity` | Consumer |
| Context | `.atlas-footer__context` | Consumer |
| Evidence | `.atlas-footer__evidence` | Consumer |
| Sequence | `.atlas-footer__sequence` | Consumer or publisher; article sequencing remains scheduler-owned |
| Estate escape | `.atlas-footer__escape` | Consumer |

Consumers omit unused optional slots rather than rendering empty containers.

## Shared behaviour

The release supplies:

- responsive grid and wrapping foundations;
- 44-pixel minimum interactive targets;
- visible focus through the shared focus contract;
- an editorial sequence layout that collapses safely on mobile;
- compatibility with the existing fixed bottom-navigation clearance contract;
- no shared runtime JavaScript;
- no remote presentation dependency.

Consumers must supply:

- purpose-specific labels and content;
- the estate escape destination;
- same-tab navigation for Atlas-owned HTML surfaces;
- `target="_blank" rel="noopener noreferrer"` for external destinations;
- accessible names when a document has multiple footer landmarks;
- repository-native tests, preview evidence, rollback, and rollout approval.

## Ownership boundaries

`atlas-interface-kit` owns selectors, layout foundations, responsive behaviour, focus foundations, and deterministic distribution.

It does not own:

- consumer wording;
- consumer destinations;
- publication sequencing;
- runtime data;
- generated article output;
- scheduler execution;
- deployment or provider settings.

`atlas-article-gen` owns the article shell and the single scheduler footer placeholder. `atlas-scheduler` owns published previous and next chaining and remains the only publication write path into `atlas-systems`.

## Distribution

The footer contract first ships in `atlas-interface-kit v0.4.0`.

Consumers may adopt it only from the immutable release, copy the required files into their own repository, verify every fingerprint against `dist/manifest.json`, and use a separate consumer pull request and rollout approval.
