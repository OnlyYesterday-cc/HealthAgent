#!/usr/bin/env bash
set -euo pipefail
EVIDENCE_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$EVIDENCE_DIR/../../backend"
cd "$BACKEND_DIR"
RUN_ID="$(date +%Y%m%d_%H%M%S)_$$"
LOG_FILE="$EVIDENCE_DIR/专项回归_$RUN_ID.log"
XML_FILE="$EVIDENCE_DIR/专项回归_$RUN_ID.xml"
printf '%s\n' "日志：$LOG_FILE" "JUnit：$XML_FILE"
.venv/bin/python -m pytest -v "$EVIDENCE_DIR/test_defect_regressions.py" --junitxml="$XML_FILE" 2>&1 | tee "$LOG_FILE"
