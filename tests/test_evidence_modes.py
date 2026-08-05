from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class EvidenceModeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.components = json.loads(
            (ROOT / "src/components.json").read_text(encoding="utf-8")
        )
        cls.semantics = json.loads(
            (ROOT / "src/semantics.json").read_text(encoding="utf-8")
        )
        cls.css = (ROOT / "src/evidence-modes.css").read_text(encoding="utf-8")

    def test_runtime_state_maturity_and_evidence_mode_are_separate(self) -> None:
        contract = self.semantics["evidence_mode_authority"]
        self.assertTrue(contract["runtime_state_is_separate_from_evidence_mode"])
        self.assertTrue(contract["maturity_is_separate_from_evidence_mode"])
        self.assertEqual("data-runtime-state", contract["runtime_state_attribute"])
        self.assertEqual("data-evidence-mode", contract["mode_attribute"])

    def test_generated_output_is_not_an_evidence_mode(self) -> None:
        contract = self.semantics["evidence_mode_authority"]
        self.assertFalse(contract["generated_output_is_evidence"])
        self.assertEqual(
            ["Live", "Replay", "Generated", "Simulated"],
            contract["directory_data_modes"],
        )
        self.assertNotIn("generated", contract["modes"])

    def test_missing_or_unscored_evidence_cannot_be_zero(self) -> None:
        contract = self.semantics["evidence_mode_authority"]
        self.assertEqual(
            ["unavailable", "unknown", "not-applicable-unscored"],
            contract["zero_may_not_represent"],
        )
        self.assertEqual("em-dash", contract["modes"]["unavailable"]["numeral_treatment"])
        self.assertEqual("em-dash", contract["modes"]["unknown"]["numeral_treatment"])
        self.assertEqual(
            "not-applicable-or-unscored-label",
            contract["modes"]["not-applicable-unscored"]["numeral_treatment"],
        )

    def test_fallback_modes_are_neutral_and_visible(self) -> None:
        contract = self.semantics["evidence_mode_authority"]
        self.assertEqual(
            [
                "recorded-replay",
                "simulated",
                "unavailable",
                "unknown",
                "not-applicable-unscored",
            ],
            contract["neutral_surface_modes"],
        )
        self.assertTrue(contract["visible_mode_label_required"])
        self.assertTrue(contract["machine_readable_mode_required"])
        self.assertTrue(
            contract[
                "fallback_mode_must_remain_visible_across_primary_state_metrics_tables_and_charts"
            ]
        )
        self.assertTrue(contract["colour_must_not_be_the_only_signal"])
        self.assertIn(".atlas-evidence-mode::before", self.css)
        self.assertIn(
            ".atlas-evidence-surface[data-evidence-mode='simulated']",
            self.css,
        )

    def test_components_publish_all_mode_selectors(self) -> None:
        selectors = self.components["evidence_mode"]["mode_selectors"]
        self.assertEqual(set(self.semantics["evidence_mode_authority"]["modes"]), set(selectors))
        for selector in selectors.values():
            self.assertIn(selector, self.css)


if __name__ == "__main__":
    unittest.main()
