#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="${PROJECT_DIR}/output/pdf"
SERVER_PORT="${PDF_SERVER_PORT:-8765}"
SERVER_URL="http://127.0.0.1:${SERVER_PORT}"
WORK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/pantani-cv-pdf.XXXXXX")"
PROFILE_DIR="${WORK_DIR}/chrome-profile"
STAGING_DIR="${WORK_DIR}/pdf"
SERVER_LOG="${WORK_DIR}/http-server.log"
SERVER_PID=""

cleanup() {
  if [[ -n "${SERVER_PID}" ]] && kill -0 "${SERVER_PID}" 2>/dev/null; then
    kill "${SERVER_PID}" 2>/dev/null || true
    wait "${SERVER_PID}" 2>/dev/null || true
  fi
  rm -rf "${WORK_DIR}"
}
trap cleanup EXIT

if [[ -n "${CHROME_BIN:-}" && -x "${CHROME_BIN}" ]]; then
  CHROME="${CHROME_BIN}"
elif command -v google-chrome >/dev/null 2>&1; then
  CHROME="$(command -v google-chrome)"
elif command -v chromium >/dev/null 2>&1; then
  CHROME="$(command -v chromium)"
elif [[ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]]; then
  CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
else
  echo "Chrome or Chromium was not found. Set CHROME_BIN to its executable path." >&2
  exit 1
fi

mkdir -p "${OUTPUT_DIR}" "${PROFILE_DIR}" "${STAGING_DIR}"
python3 -m http.server "${SERVER_PORT}" --bind 127.0.0.1 --directory "${PROJECT_DIR}" >"${SERVER_LOG}" 2>&1 &
SERVER_PID=$!

for _ in {1..50}; do
  if ! kill -0 "${SERVER_PID}" 2>/dev/null; then
    echo "Local server stopped before it became ready. Chrome generation was not started." >&2
    cat "${SERVER_LOG}" >&2
    exit 1
  fi
  if curl --fail --silent --output /dev/null "${SERVER_URL}/"; then
    break
  fi
  sleep 0.1
done

if ! curl --fail --silent --output /dev/null "${SERVER_URL}/"; then
  echo "Local server failed to start. See ${SERVER_LOG}." >&2
  exit 1
fi

pdf_is_complete() {
  [[ -s "$1" ]] && tail -c 16 "$1" | grep -q '%%EOF'
}

stop_chrome() {
  local chrome_pid="$1"
  if kill -0 "${chrome_pid}" 2>/dev/null; then
    kill "${chrome_pid}" 2>/dev/null || true
  fi
  wait "${chrome_pid}" 2>/dev/null || true
}

wait_for_pdf() {
  local output_path="$1"
  local chrome_pid="$2"
  for _ in {1..600}; do
    if pdf_is_complete "${output_path}"; then
      return 0
    fi
    if ! kill -0 "${chrome_pid}" 2>/dev/null; then
      break
    fi
    sleep 0.1
  done
  pdf_is_complete "${output_path}"
}

generate_pdf() {
  local language_query="$1"
  local output_name="$2"
  local output_path="${STAGING_DIR}/${output_name}"
  local chrome_log="${WORK_DIR}/${output_name}.log"
  local chrome_pid

  "${CHROME}" \
    --headless=new \
    --disable-background-networking \
    --disable-component-update \
    --disable-default-apps \
    --disable-gpu \
    --no-first-run \
    --no-pdf-header-footer \
    --run-all-compositor-stages-before-draw \
    --virtual-time-budget=5000 \
    --user-data-dir="${PROFILE_DIR}/${output_name}" \
    --print-to-pdf="${output_path}" \
    "${SERVER_URL}/${language_query}" >"${chrome_log}" 2>&1 &
  chrome_pid=$!

  if wait_for_pdf "${output_path}" "${chrome_pid}"; then
    stop_chrome "${chrome_pid}"
    return 0
  fi
  stop_chrome "${chrome_pid}"
  echo "Failed to generate ${output_name}. Chrome output:" >&2
  cat "${chrome_log}" >&2
  return 1
}

generate_pdf "" "danilo-pantani-cv-en.pdf"
generate_pdf "?lang=pt-BR" "danilo-pantani-cv-pt-br.pdf"

if [[ -n "${CV_VALIDATION_DIR:-}" ]]; then
  "${PYTHON:-python3}" "${PROJECT_DIR}/scripts/cv_quality.py" \
    --source "${PROJECT_DIR}/index.html" \
    --pdf-dir "${STAGING_DIR}" \
    --strict --output "${CV_VALIDATION_DIR}" \
    --analysis-report "${CV_ANALYSIS_REPORT:?Analysis report is required for validation}"
fi

# Promote only after all languages finish; a Chrome failure preserves old files.
for output_name in danilo-pantani-cv-en.pdf danilo-pantani-cv-pt-br.pdf; do
  mv "${STAGING_DIR}/${output_name}" "${OUTPUT_DIR}/${output_name}"
done

echo "Generated PDFs in ${OUTPUT_DIR}"
