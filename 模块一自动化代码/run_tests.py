"""运行单独提取的模块一测试，依赖同级源项目的后端环境。"""
import argparse
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('suite', choices=['module1', 'defects'])
parser.add_argument('--collect-only', action='store_true')
args = parser.parse_args()
backend = ROOT.parent / 'backend'
if not backend.is_dir():
    backend = ROOT.parent / '源项目' / 'HealthAgent' / 'backend'
python = backend / '.venv' / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
if not python.exists():
    parser.error('请先按源项目README配置backend/.venv。')
tests = ([ROOT / 'tests' / name for name in ['test_auth.py', 'test_users.py', 'test_bp_records.py']]
         if args.suite == 'module1' else [ROOT / 'defects' / 'test_defect_regressions.py'])
env = os.environ.copy()
env['PYTHONPATH'] = str(backend)
env['DATABASE_URL'] = 'sqlite:///:memory:'
env['JWT_SECRET'] = 'isolated-module1-tests-only'
env['PYTHONDONTWRITEBYTECODE'] = '1'
command = [str(python), '-m', 'pytest', '-v', '-p', 'no:cacheprovider', *map(str, tests)]
if args.collect_only:
    command.append('--collect-only')
sys.exit(subprocess.call(command, cwd=backend, env=env))
