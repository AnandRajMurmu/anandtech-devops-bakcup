from __future__ import annotations

from dataclasses import dataclass
import re


REQUIRED_HEADINGS = (
    "Section Purpose",
    "Learner Starting Point",
    "Section Learning Outcomes",
    "Unit Register",
    "Scope Boundaries",
    "Environment and Lab Assumptions",
    "Artifacts and Assessments",
    "Completion Criteria",
    "Revision History",
)


@dataclass(frozen=True)
class UnitSpec:
    number: str
    title: str
    directory: str


def lock_status(text: str) -> str:
    match = re.search(r"\*\*Lock status:\*\*\s*(Draft|Locked)", text, re.IGNORECASE)
    if not match:
        raise ValueError("SSOT must contain '**Lock status:** Draft' or Locked")
    return match.group(1).title()


def parse_units(text: str) -> list[UnitSpec]:
    pattern = re.compile(
        r"^###\s+Unit\s+(\d{2})\s+[—-]\s+(.+?)\s*$.*?^\*\*Directory:\*\*\s+`([^`]+)`\s*$",
        re.MULTILINE | re.DOTALL,
    )
    units = [UnitSpec(number=n, title=t.strip(), directory=d.strip()) for n, t, d in pattern.findall(text)]
    if not units:
        raise ValueError("No units found. Use '### Unit NN — Title' and '**Directory:** `unitNN_slug`'.")
    if len({u.number for u in units}) != len(units) or len({u.directory for u in units}) != len(units):
        raise ValueError("Unit numbers and directories must be unique")
    return units


def validate_draft(text: str) -> list[UnitSpec]:
    missing = [heading for heading in REQUIRED_HEADINGS if f"## {heading}" not in text]
    if missing:
        raise ValueError("SSOT is missing required headings: " + ", ".join(missing))
    if lock_status(text) != "Draft":
        raise ValueError("Only a Draft SSOT may enter the explicit lock operation")
    return parse_units(text)


def apply_lock(text: str) -> str:
    validate_draft(text)
    return re.sub(
        r"\*\*Lock status:\*\*\s*Draft",
        "**Lock status:** Locked",
        text,
        count=1,
        flags=re.IGNORECASE,
    )

