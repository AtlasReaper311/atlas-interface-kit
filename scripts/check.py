#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any
ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
VERSION = '0.4.0'
CONTRACT_VERSION = '2.0.0'
FOUNDATION_EXTENSION_VERSION = '1.0.0'
FOOTER_EXTENSION_VERSION = '1.0.0'
MIN_TEXT_CONTRAST = 4.5
EXPECTED_ROLES = {'global-header', 'product-strip', 'page-introduction', 'section-heading', 'primary-action', 'secondary-action', 'text-action', 'status-chip', 'type-badge', 'maturity-badge', 'metric-grid', 'standard-card', 'editorial-card', 'data-card', 'interactive-card-frame', 'tag-list', 'filter-bar', 'table-wrapper', 'breadcrumb-navigation', 'status-announcement', 'search-dialog', 'loading-state', 'empty-state', 'unavailable-state', 'unknown-state', 'error-state', 'footer'}
EXPECTED_COLOURS = {'bg': '#0a0a0f', 'bg_1': '#111118', 'bg_2': '#1a1a24', 'text': '#e8e8e0', 'text_dim': '#aaa9a0', 'text_faint': '#888894', 'accent': '#f5a623', 'operational': '#4ade80', 'unavailable': '#e24b4a', 'informational': '#60a5fa'}
FOOTER_SLOTS = {'identity', 'context', 'evidence', 'sequence', 'estate_escape'}
FOOTER_VARIANTS = {'estate', 'product', 'tool', 'editorial'}

def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding='utf-8'))

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)

def relative_luminance(value: str) -> float:
    require(value.startswith('#') and len(value) == 7, f'unsupported colour format: {value}')
    channels = [int(value[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    linear = [channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4 for channel in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]

def contrast_ratio(foreground: str, background: str) -> float:
    lighter, darker = sorted((relative_luminance(foreground), relative_luminance(background)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)

def validate_footer_components(components: dict[str, Any]) -> None:
    footer = components.get('footer', {})
    require(footer.get('base_selector') == '.atlas-footer', 'footer base selector drifted')
    slots = footer.get('slot_selectors', {})
    variants = footer.get('variant_selectors', {})
    require(set(slots) == FOOTER_SLOTS, 'footer slot selectors are incomplete')
    require(set(variants) == FOOTER_VARIANTS, 'footer variant selectors are incomplete')
    expected_slots = {'identity': '.atlas-footer__identity', 'context': '.atlas-footer__context', 'evidence': '.atlas-footer__evidence', 'sequence': '.atlas-footer__sequence', 'estate_escape': '.atlas-footer__escape'}
    expected_variants = {'estate': '.atlas-footer--estate', 'product': '.atlas-footer--product', 'tool': '.atlas-footer--tool', 'editorial': '.atlas-footer--editorial'}
    require(slots == expected_slots, 'footer slot selector contract drifted')
    require(variants == expected_variants, 'footer variant selector contract drifted')

def validate_semantics(semantics: dict[str, Any]) -> None:
    require(semantics.get('schema_version') == 'atlas-interface-kit/semantics/v1', 'invalid semantic schema')
    require(semantics.get('version') == VERSION, 'semantic version mismatch')
    authority = semantics.get('authority', {})
    require(authority.get('base_contract_version') == CONTRACT_VERSION, 'semantic base contract version mismatch')
    require(authority.get('foundation_extension_version') == FOUNDATION_EXTENSION_VERSION, 'semantic foundation extension version mismatch')
    require(authority.get('footer_extension_version') == FOOTER_EXTENSION_VERSION, 'semantic footer extension version mismatch')
    require(authority.get('footer_extension_source') == 'AtlasReaper311/atlas-infra:policy/public-interface-footer-extension-v1.json', 'semantic footer authority source drifted')
    breadcrumb = semantics.get('breadcrumb_navigation', {})
    require(breadcrumb.get('selector') == '.atlas-breadcrumbs', 'breadcrumb selector drifted')
    announcement = semantics.get('status_announcement', {})
    require(announcement.get('global_header_status_remains_aria_live_off') is True, 'global header status must remain aria-live off')
    overflow = semantics.get('dense_data_overflow', {})
    require(overflow.get('extends_role') == 'table-wrapper', 'overflow must extend table-wrapper')
    evidence = semantics.get('evidence', {})
    require(evidence.get('blocking_viewports_px') == [320, 375, 768, 1024, 1440], 'blocking viewport matrix drifted')
    require(evidence.get('reporting_only_viewports_px') == [1920], '1920 reporting-only evidence is missing')
    footer = semantics.get('footer_authority', {})
    require(footer.get('selector') == '.atlas-footer', 'footer semantic selector drifted')
    require(footer.get('semantic_element') == 'footer', 'footer semantic element must remain footer')
    require(footer.get('single_primary_footer_required') is True, 'one primary footer must remain required')
    require(footer.get('accessible_name_required_when_multiple') is True, 'multiple footer landmarks require accessible names')
    require(footer.get('empty_footer_forbidden') is True and footer.get('empty_slots_forbidden') is True, 'empty footer content must remain forbidden')
    slots = footer.get('slots', {})
    variants = footer.get('variants', {})
    require(set(slots) == FOOTER_SLOTS, 'footer semantic slots are incomplete')
    require(set(variants) == FOOTER_VARIANTS, 'footer semantic variants are incomplete')
    expected = {'estate': ({'identity', 'estate_escape'}, {'context', 'evidence'}, {'sequence'}), 'product': ({'identity', 'estate_escape'}, {'context', 'evidence'}, {'sequence'}), 'tool': ({'identity', 'context', 'estate_escape'}, {'evidence'}, {'sequence'}), 'editorial': ({'identity', 'sequence', 'estate_escape'}, {'context', 'evidence'}, set())}
    for name, (required, optional, forbidden) in expected.items():
        item = variants[name]
        require(set(item['required_slots']) == required, f'{name} footer required slots drifted')
        require(set(item['optional_slots']) == optional, f'{name} footer optional slots drifted')
        require(set(item['forbidden_slots']) == forbidden, f'{name} footer forbidden slots drifted')
    behaviour = footer.get('behaviour', {})
    for key in ('atlas_owned_html_same_tab_required', 'external_links_new_tab_required', 'fixed_bottom_navigation_clearance_required', 'global_navigation_duplication_forbidden', 'mobile_wrap_required', 'purpose_specific_labels_required', 'reduced_motion_required', 'visible_focus_required'):
        require(behaviour.get(key) is True, f'{key} must remain true')
    require(behaviour.get('external_links_rel') == 'noopener noreferrer', 'footer external rel contract drifted')
    require(behaviour.get('minimum_touch_target_px') == 44, 'footer touch targets must remain 44px')
    ownership = footer.get('ownership', {})
    require(ownership.get('article_sequence_owner') == 'AtlasReaper311/atlas-scheduler', 'article footer sequencing must remain scheduler-owned')
    require(ownership.get('consumer_content_owner') is True, 'footer content must remain consumer-owned')
    require(ownership.get('shared_runtime_javascript_forbidden') is True, 'footer shared runtime JavaScript must remain forbidden')

def main() -> int:
    subprocess.run([sys.executable, str(ROOT / 'scripts/build.py')], check=True)
    tokens = load_json(ROOT / 'src/tokens.json')
    components = load_json(ROOT / 'src/components.json')
    semantics = load_json(ROOT / 'src/semantics.json')
    manifest = load_json(DIST / 'manifest.json')
    require(tokens.get('schema_version') == 'atlas-interface-kit/tokens/v1', 'invalid token schema')
    require(components.get('schema_version') == 'atlas-interface-kit/components/v1', 'invalid component schema')
    require(tokens.get('version') == components.get('version') == semantics.get('version') == manifest.get('version') == VERSION, 'version mismatch')
    require(tokens.get('contract_version') == manifest.get('contract_version') == CONTRACT_VERSION, 'contract version mismatch')
    require(manifest.get('foundation_extension_version') == FOUNDATION_EXTENSION_VERSION, 'foundation extension version mismatch')
    require(manifest.get('footer_extension_version') == FOOTER_EXTENSION_VERSION, 'footer extension version mismatch')
    require(tokens['space_px'] == [4, 8, 12, 16, 24, 32, 48, 64, 96], 'spacing scale drifted')
    require(tokens['control_px'] == {'compact': 32, 'standard': 40, 'touch_min': 44}, 'control scale drifted')
    require(tokens['radius_px'] == {'sm': 4, 'md': 6, 'lg': 8}, 'radius scale drifted')
    require(tokens['breakpoint_px'] == {'mobile': 640, 'tablet': 768, 'desktop': 1024, 'wide': 1440}, 'breakpoint scale drifted')
    for name, value in EXPECTED_COLOURS.items():
        require(tokens['colour'].get(name) == value, f'colour token {name} drifted')
    for surface in ('bg', 'bg_1', 'bg_2'):
        require(contrast_ratio(tokens['colour']['text_faint'], tokens['colour'][surface]) >= MIN_TEXT_CONTRAST, f'text_faint contrast against {surface} is too low')
    role_map = {item['role']: item['selector'] for item in components['roles']}
    require(set(role_map) == EXPECTED_ROLES, 'component role contract is incomplete')
    require(len(role_map) == manifest.get('component_role_count') == 27, 'component role count mismatch')
    validate_footer_components(components)
    require(manifest.get('footer_slot_count') == 5, 'footer slot count mismatch')
    require(manifest.get('footer_variant_count') == 4, 'footer variant count mismatch')
    require(manifest.get('semantic_contract_count') == 4, 'semantic contract count mismatch')
    validate_semantics(semantics)
    css = (DIST / 'atlas-interface-kit.css').read_text(encoding='utf-8')
    require('http://' not in css and 'https://' not in css, 'runtime CSS must not contain remote dependencies')
    require(':focus-visible' in css, 'visible focus foundation is missing')
    require('prefers-reduced-motion' in css, 'reduced-motion foundation is missing')
    require(".atlas-table-wrap[data-overflow='true']:focus-visible" in css, 'overflow focus foundation is missing')
    require('.atlas-status-announcement--visually-hidden' in css, 'announcement helper is missing')
    for selector in list(components['footer']['slot_selectors'].values()) + list(components['footer']['variant_selectors'].values()):
        require(selector in css, f'generated CSS missing footer selector: {selector}')
    require('min-height: var(--atlas-touch-min)' in css, 'footer touch target foundation is missing')
    for role, selector in role_map.items():
        require(selector in css, f'generated CSS missing selector for {role}: {selector}')
    font_css = (DIST / 'atlas-fonts.css').read_text(encoding='utf-8')
    require('http://' not in font_css and 'https://' not in font_css, 'font CSS must not contain remote dependencies')
    require(font_css.count('@font-face') == 4, 'font CSS must declare the four approved faces')
    require(font_css.count('font-display: swap') == 4, 'every font face must render with swap')
    for name, record in manifest['files'].items():
        path = DIST / name
        require(path.is_file(), f'manifest file is missing: {name}')
        require(path.stat().st_size == record['bytes'], f'manifest byte count mismatch: {name}')
        require(digest(path) == record['sha256'], f'manifest digest mismatch: {name}')
    print('Atlas Interface Kit validation passed.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
