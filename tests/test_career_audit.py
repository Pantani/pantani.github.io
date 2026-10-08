"""Reject unsupported career claims before emitting reusable drafts."""

import json
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/career_audit.py"
URL = "https://github.com/atomone-hub/atomone-sdk/pull/10"


def load_module():
    spec = importlib.util.spec_from_file_location("career_audit", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CareerAuditTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.prs = [{"url": URL, "state": "MERGED", "repository": {
            "nameWithOwner": "atomone-hub/atomone-sdk", "isPrivate": False},
            "files": {"totalCount": 1}, "allFiles": [{"path": "module.go"}]}]
        bullet = {"text": "Implemented distribution changes.", "sources": [URL]}
        self.draft = {"confirmed_employers": {"Ignite": {
            "organizations": ["atomone-hub"], "source": "Owner confirmation, 2026-10-08"}},
            "roles": [{"id": "ignite", "employer": "Ignite", "dates": "2022–2026",
                       "linkedin": [bullet], "cv": {lang: [bullet] for lang in ("en", "pt-br")}}]}

    def run_build(self):
        (self.root / "prs.json").write_text(json.dumps(self.prs))
        (self.root / "draft.json").write_text(json.dumps(self.draft))
        return subprocess.run([sys.executable, str(SCRIPT), "--evidence", str(self.root / "prs.json"),
                               "--draft", str(self.root / "draft.json"), "--output", str(self.root / "build")],
                              capture_output=True, text=True)

    def report_text(self):
        path = self.root / "build/report.json"
        self.assertTrue(path.exists(), "Build must emit a validation report")
        return path.read_text()

    def test_confirmed_employer_allows_related_organization(self):
        result = self.run_build()
        self.assertEqual(result.returncode, 0, result.stderr)
        text = (self.root / "build/linkedin.md").read_text()
        self.assertIn("Implemented distribution changes.", text)
        self.assertIn(URL, (self.root / "build/claim-ledger.md").read_text())

    def test_unmerged_pr_cannot_support_delivered_work(self):
        self.prs[0]["state"] = "CLOSED"
        result = self.run_build()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / "build/linkedin.md").exists())
        self.assertIn("not merged", self.report_text())

    def test_unknown_source_is_not_silently_accepted(self):
        self.prs = []
        self.assertNotEqual(self.run_build().returncode, 0)
        self.assertIn("unknown source", self.report_text())

    def test_unconfirmed_employer_blocks_attribution(self):
        self.draft["confirmed_employers"] = {}
        self.assertNotEqual(self.run_build().returncode, 0)
        self.assertIn("employer", self.report_text())

    def test_incomplete_file_inventory_is_reported(self):
        self.prs[0]["allFiles"] = []
        self.assertNotEqual(self.run_build().returncode, 0)
        self.assertIn("file inventory", self.report_text())

    def test_duplicate_pr_records_are_rejected(self):
        self.prs.append(self.prs[0])
        self.assertNotEqual(self.run_build().returncode, 0)
        self.assertIn("duplicate", self.report_text())

    def test_missing_cv_language_is_rejected(self):
        del self.draft["roles"][0]["cv"]["pt-br"]
        self.assertNotEqual(self.run_build().returncode, 0)
        self.assertIn("languages", self.report_text())

    def test_previous_run_is_preserved(self):
        self.assertEqual(self.run_build().returncode, 0)
        report = self.root / "build/report.json"
        original = report.read_bytes()
        self.assertNotEqual(self.run_build().returncode, 0)
        self.assertEqual(report.read_bytes(), original)

    def test_private_evidence_blocks_public_draft(self):
        self.prs[0]["repository"]["isPrivate"] = True
        self.assertNotEqual(self.run_build().returncode, 0)
        self.assertIn("private source", self.report_text())

    def test_empty_sources_block_unsupported_claims(self):
        self.draft["roles"][0]["linkedin"][0]["sources"] = []
        self.assertNotEqual(self.run_build().returncode, 0)
        self.assertIn("no sources", self.report_text())

    def test_preview_updates_default_and_all_languages_without_touching_source(self):
        source = SCRIPT.parent.parent / "index.html"
        original = source.read_bytes()
        module = load_module()
        html = module.preview_html(source.read_text(), self.draft["roles"])
        self.assertEqual(html.count("Implemented distribution changes."), 3)
        self.assertNotIn('"exp.ignite.b6":', html)
        self.assertIn('"exp.interchain.b1":', html)
        self.assertEqual(source.read_bytes(), original)

    def test_template_drift_fails_instead_of_silently_omitting_claims(self):
        module = load_module()
        with self.assertRaises(ValueError):
            module.preview_html("<html></html>", self.draft["roles"])


if __name__ == "__main__":
    unittest.main()
