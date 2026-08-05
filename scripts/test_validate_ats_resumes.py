#!/usr/bin/env python3

from __future__ import annotations

import importlib.util
import io
import unittest
from contextlib import redirect_stderr
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("validate-ats-resumes.py")
SPEC = importlib.util.spec_from_file_location("validate_ats_resumes", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load {MODULE_PATH}")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class TargetTitleValidationTests(unittest.TestCase):
    def test_accepts_exact_rendered_title(self) -> None:
        source = (
            '<p class="target-title">'
            'Senior Go Engineer | Backend &amp; Distributed Systems'
            '</p>'
        )

        VALIDATOR.validate_target_title(
            source,
            "Senior Go Engineer | Backend & Distributed Systems",
            "resume.html",
        )

    def test_rejects_expected_title_outside_target_title_paragraph(self) -> None:
        expected = "Senior Go Engineer | Backend & Distributed Systems"
        source = (
            f"<title>{expected}</title>"
            '<p class="target-title">Blockchain Engineer</p>'
        )

        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            VALIDATOR.validate_target_title(source, expected, "resume.html")


if __name__ == "__main__":
    unittest.main()
