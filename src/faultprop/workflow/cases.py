"""Load hand-written cases from cases/*.yaml."""
from __future__ import annotations

from pathlib import Path

import yaml

from .models import Case

CASES_DIR = Path(__file__).resolve().parents[3] / "cases"


def load_cases(only: list[str] | None = None) -> list[Case]:
    cases = []
    for p in sorted(CASES_DIR.glob("*.yaml")):
        if p.name.startswith("_"):
            continue
        c = Case.model_validate(yaml.safe_load(p.read_text()))
        if only is None or c.case_id in only:
            cases.append(c)
    return cases
