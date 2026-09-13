"""Run the selected functional cases or the separate D02/D03 checks."""
import argparse
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
        nodes = ['tests/test_users.py::TestMe::test_me_invalid_token', 'tests/test_users.py::TestUpdateProfile::test_update_profile', 'tests/test_users.py::TestUpdateProfile::test_update_profile_invalid_gender', 'tests/test_users.py::TestChangePassword::test_change_password_success', 'tests/test_users.py::TestChangePassword::test_change_password_wrong_old', 'tests/test_bp_records.py::TestAuth::test_requires_auth', 'tests/test_bp_records.py::TestCrud::test_create_and_get', 'tests/test_bp_records.py::TestCrud::test_list_pagination', 'tests/test_bp_records.py::TestCrud::test_update_and_delete', 'tests/test_bp_records.py::TestCrud::test_user_isolation', 'tests/test_bp_records.py::TestCrud::test_validation_out_of_range', 'tests/test_bp_records.py::TestStatsAndForecast::test_stats_empty', 'tests/test_bp_records.py::TestStatsAndForecast::test_stats_with_data', 'tests/test_bp_records.py::TestStatsAndForecast::test_forecast_insufficient', 'tests/test_bp_records.py::TestStatsAndForecast::test_forecast_with_data']
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
