#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PDF_DIR="${PROJECT_DIR}/output/pdf"
TEXT_DIR="${PROJECT_DIR}/output/text"
SERVER_PORT="${ATS_PDF_SERVER_PORT:-8766}"
SERVER_URL="http://127.0.0.1:${SERVER_PORT}"
WORK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/pantani-ats-pdf.XXXXXX")"
PROFILE_DIR="${WORK_DIR}/chrome-profile"
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

for dependency in python3 curl pdfinfo pdftotext; do
  if ! command -v "${dependency}" >/dev/null 2>&1; then
    echo "Required command not found: ${dependency}" >&2
    exit 1
  fi
done

mkdir -p "${PDF_DIR}" "${TEXT_DIR}" "${PROFILE_DIR}"
python3 -m http.server "${SERVER_PORT}" --bind 127.0.0.1 --directory "${PROJECT_DIR}" >"${SERVER_LOG}" 2>&1 &
SERVER_PID=$!

for _ in {1..50}; do
  if ! kill -0 "${SERVER_PID}" 2>/dev/null; then
    echo "Local server stopped before it became ready." >&2
    sed -n '1,120p' "${SERVER_LOG}" >&2
    exit 1
  fi
  if curl --fail --silent --output /dev/null "${SERVER_URL}/ats/"; then
    break
  fi
  sleep 0.1
done

if ! curl --fail --silent --output /dev/null "${SERVER_URL}/ats/"; then
  echo "Local server failed to start on port ${SERVER_PORT}." >&2
  exit 1
fi

generate_pdf() {
  local source_path="$1"
  local output_name="$2"
  local output_path="${PDF_DIR}/${output_name}"
  local text_path="${TEXT_DIR}/${output_name%.pdf}.txt"
  local chrome_log="${WORK_DIR}/${output_name}.log"
  local chrome_pid
  local page_count

  rm -f "${output_path}" "${text_path}"

  "${CHROME}" \
    --headless=new \
    --disable-background-networking \
    --disable-component-update \
    --disable-default-apps \
    --disable-gpu \
    --no-first-run \
    --no-pdf-header-footer \
    --run-all-compositor-stages-before-draw \
    --virtual-time-budget=3000 \
    --user-data-dir="${PROFILE_DIR}/${output_name}" \
    --print-to-pdf="${output_path}" \
    "${SERVER_URL}/${source_path}" >"${chrome_log}" 2>&1 &
  chrome_pid=$!

  for _ in {1..600}; do
    if [[ -s "${output_path}" ]] && tail -c 16 "${output_path}" | grep -q '%%EOF'; then
      sleep 0.3
      if kill -0 "${chrome_pid}" 2>/dev/null; then
        kill "${chrome_pid}" 2>/dev/null || true
      fi
      wait "${chrome_pid}" 2>/dev/null || true
      break
    fi

    if ! kill -0 "${chrome_pid}" 2>/dev/null; then
      wait "${chrome_pid}" || true
      break
    fi
    sleep 0.1
  done

  if [[ ! -s "${output_path}" ]] || ! tail -c 16 "${output_path}" | grep -q '%%EOF'; then
    echo "Failed to generate ${output_name}. Chrome output:" >&2
    sed -n '1,160p' "${chrome_log}" >&2
    exit 1
  fi

  page_count="$(pdfinfo "${output_path}" | awk '/^Pages:/ {print $2}')"
  if [[ -z "${page_count}" || "${page_count}" -gt 2 ]]; then
    echo "${output_name} has ${page_count:-unknown} pages; expected at most 2." >&2
    exit 1
  fi

  pdftotext "${output_path}" "${text_path}"
  echo "Generated ${output_name} (${page_count} pages)"
}

generate_pdf "ats/senior-go-engineer.html" "danilo-pantani-senior-go-engineer.pdf"
generate_pdf "ats/blockchain-infrastructure-engineer.html" "danilo-pantani-blockchain-infrastructure-engineer.pdf"
generate_pdf "ats/platform-engineer.html" "danilo-pantani-platform-engineer.pdf"

echo "Generated ATS PDFs in ${PDF_DIR}"
echo "Extracted ATS text in ${TEXT_DIR}"
