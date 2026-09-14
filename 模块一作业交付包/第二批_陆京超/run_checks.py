"""Verify batch two and integration without mixing functional and defect counts."""
import argparse
from datetime import datetime
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import sqlite3
import subprocess
import sys


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SUITES = {
    "functional": [
        "tests/test_auth.py",
        "tests/test_users.py::TestMe::test_me_requires_auth",
        "tests/test_users.py::TestMe::test_me_ok",
    ],
    "defects": [str(HERE.parent / "缺陷证据" / "test_defect_regressions.py")],
    "module1": ["tests/test_auth.py", "tests/test_users.py", "tests/test_bp_records.py"],
    "security": ["tests/test_security.py"],
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("suite", choices=[*SUITES, "all"])
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    out = (args.output_dir or HERE / "执行结果" / datetime.now().strftime("%Y%m%d_%H%M%S_%f")).resolve()
    out.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update(DATABASE_URL="sqlite://", JWT_SECRET="isolated-batch-two-only",
               APP_DEBUG="false", PYTHONIOENCODING="utf-8")
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                              capture_output=True, text=True, check=True).stdout.strip()
    metadata = {
        "executed_at": datetime.now().astimezone().isoformat(),
        "revision": revision,
        "platform": platform.platform(),
        "python": platform.python_version(),
        "sqlite": sqlite3.sqlite_version,
        "packages": {name: importlib.metadata.version(name) for name in
                     ("pytest", "fastapi", "sqlalchemy", "pydantic", "passlib", "bcrypt")},
        "suites": {},
    }
    failed = False
    for name in SUITES if args.suite == "all" else [args.suite]:
        command = [sys.executable, "-m", "pytest", "-v", "-p", "no:cacheprovider",
                   "--junitxml=" + str(out / (name + ".xml")), *SUITES[name]]
        completed = subprocess.run(command, cwd=REPO / "backend", env=env,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   text=True, encoding="utf-8", errors="replace")
        (out / (name + ".log")).write_text(completed.stdout, encoding="utf-8")
        print(completed.stdout, end="")
        metadata["suites"][name] = {"command": command, "exit_code": completed.returncode}
        failed |= completed.returncode != 0
    (out / "environment.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Results: {out}")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
