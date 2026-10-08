PYTHON ?= python3
CV_RUN_DIR ?= _workspace/cv-quality

.PHONY: cv-analyze cv-implement cv-test

cv-analyze:
	$(PYTHON) scripts/cv_quality.py --output "$(CV_RUN_DIR)/analysis"

cv-implement:
	$(PYTHON) scripts/cv_quality.py --require-analysis "$(CV_RUN_DIR)/analysis/report.json" --prepare-implementation --output "$(CV_RUN_DIR)/implementation"
	CV_ANALYSIS_REPORT="$(CV_RUN_DIR)/analysis/report.json" CV_VALIDATION_DIR="$(CV_RUN_DIR)/staging" PYTHON="$(PYTHON)" bash scripts/generate-pdfs.sh
	$(PYTHON) scripts/cv_quality.py --strict --output "$(CV_RUN_DIR)/implementation" --analysis-report "$(CV_RUN_DIR)/analysis/report.json"

cv-test:
	$(PYTHON) -m unittest discover -s tests -v
