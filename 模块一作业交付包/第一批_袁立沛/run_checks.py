"""Run the selected functional cases or the separate D02/D03 checks."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('suite', choices=['functional', 'defects'])
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    if args.suite == 'functional':
        nodes = json.loads((HERE / '用例节点.json').read_text())
    else:
        nodes = [str(HERE / 'defect_checks.py')]
    env = os.environ.copy()
    env.update(DATABASE_URL='sqlite://', JWT_SECRET='isolated-batch-verification-only', APP_DEBUG='false')
    command = [sys.executable, '-m', 'pytest', '-v', '-p', 'no:cacheprovider',
               '--junitxml=' + str(out / (args.suite + '.xml')), *nodes]
    completed = subprocess.run(command, cwd=REPO / 'backend', env=env,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    (out / (args.suite + '.log')).write_text(completed.stdout)
    print(completed.stdout, end='')
    return completed.returncode

if __name__ == '__main__':
    raise SystemExit(main())
