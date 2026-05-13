import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

DATASET_PATH = Path(__file__).parent / "dataset" / "golden.json"


def load_dataset() -> list[dict[str, Any]]:
    with Path.open(DATASET_PATH, encoding="utf-8") as f:
        return json.load(f)


def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    if "case" in metafunc.fixturenames:
        cases = load_dataset()
        metafunc.parametrize("case", cases, ids=[c["id"] for c in cases])


@pytest.fixture(scope="session")
def report_dir() -> Path:
    run_id = datetime.now(UTC).strftime("%Y-%m-%dT%H-%M-%S")
    d = Path(__file__).parent / "reports" / run_id
    d.mkdir(parents=True, exist_ok=True)
    return d
