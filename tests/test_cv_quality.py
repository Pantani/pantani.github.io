"""Behavioral tests for local CV validation and build gating."""

import json
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from pypdf import PdfWriter

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "cv_quality.py"
LANGUAGES = ("en", "pt-br")
SPEC = importlib.util.spec_from_file_location("cv_quality", SCRIPT)
QUALITY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(QUALITY)


class ExtractionContractTests(unittest.TestCase):
    def valid_text(self):
        return "\n".join((QUALITY.CONTACT, *QUALITY.SECTION_ANCHORS["en"]))

    def test_valid_order_accepts_line_wrapping(self):
        text = self.valid_text().replace("Professional Summary", "Professional\nSummary")
        self.assertEqual(QUALITY.text_findings(text, "en", "fixture"), [])

    def test_contact_after_summary_is_rejected(self):
        text = self.valid_text().replace(QUALITY.CONTACT, "") + QUALITY.CONTACT
        codes = {item["code"] for item in QUALITY.text_findings(text, "en", "fixture")}
        self.assertIn("missing_anchor", codes)

    def test_company_mentioned_in_summary_cannot_replace_experience(self):
        text = self.valid_text().replace("Professional Summary", "Professional Summary\nTrust Wallet / Binance")
        text = text.replace("Professional Experience\nTrust Wallet / Binance", "Professional Experience")
        issues = QUALITY.text_findings(text, "en", "fixture")
        self.assertTrue(any("Trust Wallet" in item["detail"] for item in issues))

    def test_ligatures_are_detected_before_unicode_normalization(self):
        text = self.valid_text() + "\nWorkﬂows and ﬁxes"
        codes = {item["code"] for item in QUALITY.text_findings(text, "en", "fixture")}
        self.assertIn("unicode_ligatures", codes)


class QualityCommandTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.source = self.root / "index.html"
        self.source.write_text("<html>CV fixture</html>", encoding="utf-8")
        self.pdf_dir = self.root / "pdf"
        self.pdf_dir.mkdir()
        self.output = self.root / "report"

    def run_check(self, *arguments):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--source", str(self.source),
             "--pdf-dir", str(self.pdf_dir), "--output", str(self.output), *arguments],
            capture_output=True, text=True, check=False,
        )

    def blank_pdfs(self):
        for language in LANGUAGES:
            writer = PdfWriter()
            writer.add_blank_page(width=595, height=842)
            writer.write(self.pdf_dir / f"danilo-pantani-cv-{language}.pdf")

    def report(self):
        return json.loads((self.output / "report.json").read_text(encoding="utf-8"))

    def test_missing_pdf_produces_inspectable_error_report(self):
        result = self.run_check()
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertTrue((self.output / "report.json").exists(), result.stderr)
        self.assertEqual(self.report()["status"], "incomplete")

    def test_analysis_records_failures_without_claiming_acceptance(self):
        self.blank_pdfs()
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.report()["status"], "needs_changes")
        self.assertEqual(len(self.report()["documents"]), len(LANGUAGES))
        self.assertTrue(self.report()["documents"][0]["findings"])

    def test_strict_rejects_blank_wrong_page_count_pdfs(self):
        self.blank_pdfs()
        result = self.run_check("--strict")
        self.assertEqual(result.returncode, 1, result.stderr)
        codes = {item["code"] for item in self.report()["documents"][0]["findings"]}
        self.assertTrue({"page_count", "empty_text", "missing_anchor"} <= codes)

    def test_implementation_requires_completed_analysis(self):
        result = self.run_check("--require-analysis", str(self.root / "missing.json"))
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("analysis", result.stderr.lower())

    def test_analysis_gate_rejects_pdf_drift(self):
        self.blank_pdfs()
        self.assertEqual(self.run_check().returncode, 0)
        pdf = self.pdf_dir / "danilo-pantani-cv-en.pdf"
        pdf.write_bytes(pdf.read_bytes() + b"\n% changed\n")
        result = self.run_check("--require-analysis", str(self.output / "report.json"))
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("changed", result.stderr.lower())

    def test_preparation_replaces_old_pass_with_incomplete_state(self):
        self.blank_pdfs()
        self.assertEqual(self.run_check().returncode, 0)
        analysis = self.root / "analysis.json"
        analysis.write_bytes((self.output / "report.json").read_bytes())
        for evidence in self.output.iterdir():
            (self.root / evidence.name).write_bytes(evidence.read_bytes())
        (self.output / "report.json").write_text('{"status": "pass"}', encoding="utf-8")
        result = self.run_check("--require-analysis", str(analysis), "--prepare-implementation")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.report()["status"], "incomplete")
        self.assertEqual(self.report()["stage"], "generation_pending")

    def test_analysis_cannot_overwrite_an_existing_baseline(self):
        self.blank_pdfs()
        self.assertEqual(self.run_check().returncode, 0)
        original = (self.output / "report.json").read_bytes()
        result = self.run_check()
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual((self.output / "report.json").read_bytes(), original)

    def test_retry_accepts_outputs_of_same_baseline(self):
        self.blank_pdfs()
        self.assertEqual(self.run_check().returncode, 0)
        analysis = self.output / "report.json"
        implementation = self.root / "implementation"
        pdf = self.pdf_dir / "danilo-pantani-cv-en.pdf"
        pdf.write_bytes(pdf.read_bytes() + b"\n% regenerated\n")
        result = self.run_check("--strict", "--output", str(implementation),
                                "--analysis-report", str(analysis))
        self.assertEqual(result.returncode, 1, result.stderr)
        retry = self.run_check("--require-analysis", str(analysis),
                              "--prepare-implementation", "--output", str(implementation))
        self.assertEqual(retry.returncode, 0, retry.stderr)


if __name__ == "__main__":
    unittest.main()
