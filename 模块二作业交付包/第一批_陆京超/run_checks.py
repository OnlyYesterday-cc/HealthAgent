"""Forward this member's current batch to the module-two runner."""
from pathlib import Path
import runpy


if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parents[1] / "run_module2_tests.py"),
                   run_name="__main__")
