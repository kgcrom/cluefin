"""Make tests/dart/_helpers.py importable regardless of pytest's import mode."""

import sys
from pathlib import Path

_DART_TESTS_DIR = str(Path(__file__).parent)
if _DART_TESTS_DIR not in sys.path:
    sys.path.insert(0, _DART_TESTS_DIR)
