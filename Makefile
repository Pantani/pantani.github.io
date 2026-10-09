PYTHON ?= python3
CV_RUN_DIR ?= _workspace/cv-quality
CAREER_EVIDENCE ?=
CAREER_DRAFT ?=
CAREER_RUN_DIR ?= _workspace/career-evidence/build
CAREER_SOURCE ?= index.html
CAREER_ANALYSIS ?=

.PHONY: cv-analyze cv-implement cv-test career-audit career-pdf site-build site-check site-test

site-build:
	$(PYTHON) scripts/build_site.py --output _site

site-check: site-build
	$(PYTHON) scripts/validate_site.py --directory _site

site-test:
	$(PYTHON) -m unittest discover -s tests -p 'test_site.py' -v
	npm test
	npm run lint

career-audit:
	$(PYTHON) scripts/career_audit.py --evidence "$(CAREER_EVIDENCE)" --draft "$(CAREER_DRAFT)" --source "$(CAREER_SOURCE)" --output "$(CAREER_RUN_DIR)"

career-pdf:
	CV_ANALYSIS_REPORT="$(abspath $(CAREER_ANALYSIS))" CV_VALIDATION_DIR="$(abspath $(CAREER_RUN_DIR))/pdf-validation" PYTHON="$(PYTHON)" bash "$(CAREER_RUN_DIR)/candidate/scripts/generate-pdfs.sh"

cv-analyze:
	$(PYTHON) scripts/cv_quality.py --output "$(CV_RUN_DIR)/analysis"

cv-implement:
	$(PYTHON) scripts/cv_quality.py --require-analysis "$(CV_RUN_DIR)/analysis/report.json" --prepare-implementation --output "$(CV_RUN_DIR)/implementation"
	CV_ANALYSIS_REPORT="$(CV_RUN_DIR)/analysis/report.json" CV_VALIDATION_DIR="$(CV_RUN_DIR)/staging" PYTHON="$(PYTHON)" bash scripts/generate-pdfs.sh
	$(PYTHON) scripts/cv_quality.py --strict --output "$(CV_RUN_DIR)/implementation" --analysis-report "$(CV_RUN_DIR)/analysis/report.json"

cv-test:
	$(PYTHON) -m unittest discover -s tests -v
