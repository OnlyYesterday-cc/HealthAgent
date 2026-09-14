"""Run the currently available member batch."""
from pathlib import Path
import runpy


if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).resolve().parent / '第一批_陆京超' / 'run_checks.py'),
                   run_name='__main__')
