import copy
import sys
from pathlib import Path

# Ensure the src/ directory is importable
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import app as app_module
from fastapi.testclient import TestClient
import pytest

@pytest.fixture(scope="session")
def original_activities():
    # Snapshot the initial in-memory activities state
    return copy.deepcopy(app_module.activities)

@pytest.fixture
def client(original_activities):
    # Restore a fresh copy for each test to avoid state leakage
    app_module.activities = copy.deepcopy(original_activities)
    with TestClient(app_module.app) as c:
        yield c
