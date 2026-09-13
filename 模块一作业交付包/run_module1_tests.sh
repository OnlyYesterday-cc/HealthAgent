#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$ROOT_DIR/../backend"
case "${1:-all}" in
  all|quick|backend) ;;
  help|-h|--help)
    printf '%s\n' '用法：bash run_module1_tests.sh' '只运行模块一选定的30条后端测试，并保存日志及JUnit结果。'
    exit 0 ;;
  *) printf '%s\n' '仅支持 all / quick / backend（均运行相同30条）或 help。' >&2; exit 2 ;;
esac
mkdir -p "$ROOT_DIR/执行结果"
RUN_ID="$(date +%Y%m%d_%H%M%S)_$$"
LOG_FILE="$ROOT_DIR/执行结果/module1_$RUN_ID.log"
XML_FILE="$ROOT_DIR/执行结果/module1_$RUN_ID.xml"
run_tests() {
  cd "$BACKEND_DIR" || return
  if [ ! -x .venv/bin/python ]; then
    printf '%s\n' '缺少 backend/.venv/bin/python，请先按项目README配置后端虚拟环境。' >&2
    return 2
  fi
  printf '%s\n' '模块一：认证13条、个人信息7条、血压记录10条。' "日志：$LOG_FILE" "JUnit：$XML_FILE"
  .venv/bin/python -m pytest -v tests/test_auth.py tests/test_users.py tests/test_bp_records.py --junitxml="$XML_FILE"
}
set +e
run_tests 2>&1 | tee "$LOG_FILE"
RESULT=$?
set -e
exit "$RESULT"
