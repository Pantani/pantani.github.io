"""Exercise generator failure without touching the repository's published PDFs."""

import json
import os
from pathlib import Path
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import unittest

from pypdf import PdfWriter


GENERATOR = Path(__file__).resolve().parents[1] / "scripts" / "generate-pdfs.sh"
PDF_NAMES = tuple(f"danilo-pantani-cv-{language}.pdf" for language in ("en", "pt-br"))
FAKE_CHROME_HEADER = """#!/bin/sh
set -eu
for argument in "$@"; do
  case "$argument" in
    --print-to-pdf=*) destination=${argument#--print-to-pdf=} ;;
  esac
done
printf '%s\\n' "${destination##*/}" >> "$FAKE_CHROME_LOG"
"""
FAKE_CHROME = FAKE_CHROME_HEADER + """
case "$destination" in
  *danilo-pantani-cv-en.pdf)
    printf '%%PDF-1.4\\n%% staged test fixture\\n%%%%EOF\\n' > "$destination"
    ;;
  *)
    echo 'Intentional second-language failure' >&2
    exit 42
    ;;
esac
"""


def available_port():
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        return listener.getsockname()[1]


def invoke_generator(root, environment):
    process = subprocess.Popen(
        ["bash", str(root / "scripts" / "generate-pdfs.sh")], cwd=root,
        env=environment, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, start_new_session=True,
    )
    try:
        stdout, stderr = process.communicate(timeout=15)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGKILL)
        process.communicate()
        raise
    return subprocess.CompletedProcess(process.args, process.returncode, stdout, stderr)


class GeneratePDFFailureTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix="cv-generator-test-")
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        (self.root / "scripts").mkdir()
        self.output = self.root / "output" / "pdf"
        self.output.mkdir(parents=True)
        shutil.copy2(GENERATOR, self.root / "scripts" / GENERATOR.name)
        (self.root / "index.html").write_text("<!doctype html><title>CV fixture</title>", encoding="utf-8")
        self.originals = {name: f"original {name}\n".encode() for name in PDF_NAMES}
        for name, content in self.originals.items():
            (self.output / name).write_bytes(content)

    def fake_environment(self, chrome_source=FAKE_CHROME):
        chrome = self.root / "fake-chrome"
        chrome.write_text(chrome_source, encoding="utf-8")
        chrome.chmod(0o755)
        return {**os.environ, "CHROME_BIN": str(chrome),
                "PDF_SERVER_PORT": str(available_port()),
                "FAKE_CHROME_LOG": str(self.root / "chrome-calls.txt")}

    def quality_failure_environment(self):
        validator = GENERATOR.parent / "cv_quality.py"
        shutil.copy2(validator, self.root / "scripts" / validator.name)
        fixture = self.root / "blank.pdf"
        writer = PdfWriter()
        writer.add_blank_page(width=595, height=842)
        writer.write(fixture)
        analysis = self.root / "analysis.json"
        analysis.write_text("{}", encoding="utf-8")
        chrome_source = FAKE_CHROME_HEADER + 'cp "$FAKE_PDF" "$destination"\n'
        return {**self.fake_environment(chrome_source), "PYTHON": sys.executable,
                "FAKE_PDF": str(fixture), "CV_ANALYSIS_REPORT": str(analysis),
                "CV_VALIDATION_DIR": str(self.root / "validation")}

    def test_second_language_failure_preserves_all_original_pdfs(self):
        result = invoke_generator(self.root, self.fake_environment())
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("Failed to generate danilo-pantani-cv-pt-br.pdf", result.stderr)
        self.assertIn("Intentional second-language failure", result.stderr)
        calls = (self.root / "chrome-calls.txt").read_text(encoding="utf-8").splitlines()
        self.assertEqual(calls, list(PDF_NAMES[:2]))
        actual = {name: (self.output / name).read_bytes() for name in PDF_NAMES}
        self.assertEqual(actual, self.originals)

    def test_quality_failure_before_promotion_preserves_all_original_pdfs(self):
        result = invoke_generator(self.root, self.quality_failure_environment())
        self.assertEqual(result.returncode, 1, result.stderr)
        calls = (self.root / "chrome-calls.txt").read_text(encoding="utf-8").splitlines()
        self.assertEqual(calls, list(PDF_NAMES))
        report = json.loads((self.root / "validation" / "report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["status"], "needs_changes")
        self.assertEqual(len(report["documents"]), 2)
        self.assertIn("empty_text", {item["code"] for item in report["documents"][0]["findings"]})
        actual = {name: (self.output / name).read_bytes() for name in PDF_NAMES}
        self.assertEqual(actual, self.originals)


if __name__ == "__main__":
    unittest.main()
