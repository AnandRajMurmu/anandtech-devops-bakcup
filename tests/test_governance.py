from pathlib import Path
import json
import tempfile
import unittest

from anandtech_agents.config import Settings
from anandtech_agents.manager import GovernanceBlocker, Manager
from anandtech_agents.repository import Repository, RepositoryViolation
from anandtech_agents.ssot import apply_lock, lock_status, parse_units, validate_draft


VALID_SSOT = """# Test SSOT

**Lock status:** Draft

## Section Purpose
Purpose
## Learner Starting Point
Start
## Section Learning Outcomes
Outcomes
## Unit Register
### Unit 01 — First Unit

**Directory:** `unit01_first_unit`
## Scope Boundaries
Scope
## Environment and Lab Assumptions
Environment
## Artifacts and Assessments
Artifacts
## Completion Criteria
Done
## Revision History
History
"""


class SSOTTests(unittest.TestCase):
    def test_parses_unit_and_applies_lock(self):
        units = validate_draft(VALID_SSOT)
        self.assertEqual(units, parse_units(VALID_SSOT))
        self.assertEqual(units[0].directory, "unit01_first_unit")
        self.assertEqual(lock_status(apply_lock(VALID_SSOT)), "Locked")

    def test_rejects_duplicate_units(self):
        duplicate = VALID_SSOT.replace("## Scope Boundaries", "### Unit 01 — Duplicate\n\n**Directory:** `unit01_other`\n## Scope Boundaries")
        with self.assertRaisesRegex(ValueError, "unique"):
            parse_units(duplicate)


class RepositoryTests(unittest.TestCase):
    def test_enforces_write_prefix_and_repository_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Repository(Path(directory))
            repo.write("sections/00/unit01/README.md", "ok", ("sections/00/unit01",))
            self.assertEqual(repo.read("sections/00/unit01/README.md"), "ok")
            with self.assertRaises(RepositoryViolation):
                repo.write("docs/project_SSOT.md", "bad", ("sections/00/unit01",))
            with self.assertRaises(RepositoryViolation):
                repo.write("sections/00/unit01/../unit02/README.md", "bad", ("sections/00/unit01",))
            with self.assertRaises(RepositoryViolation):
                repo.resolve("../outside")


class ManagerLockTests(unittest.TestCase):
    def test_lock_requires_exact_human_confirmation_and_detects_later_change(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "sections/00").mkdir(parents=True)
            (root / "workflow").mkdir()
            (root / "sections/00/SSOT.md").write_text(VALID_SSOT, encoding="utf-8")
            state = {
                "version": 1,
                "phase": "awaiting_ssot_lock",
                "section": {
                    "number": "00",
                    "slug": "00",
                    "title": "Test",
                    "directory": "sections/00",
                    "plan_path": "sections/00/PLAN.md",
                    "ssot_path": "sections/00/SSOT.md",
                    "lock": {"status": "draft", "sha256": None, "approved_by": None, "approved_at_utc": None},
                    "units": [],
                },
                "notifications": {"events": {}},
            }
            (root / "workflow/state.json").write_text(json.dumps(state), encoding="utf-8")
            settings = Settings(root, "", "", "", None, 5)
            manager = Manager(settings)
            with self.assertRaisesRegex(GovernanceBlocker, "LOCK SECTION 00"):
                manager.lock_ssot("yes", "Anand")
            manager.lock_ssot("LOCK SECTION 00", "Anand")
            locked = manager.status()
            self.assertEqual(locked["phase"], "ready_for_generation")
            manager._assert_lock(locked)
            with (root / "sections/00/SSOT.md").open("a", encoding="utf-8") as handle:
                handle.write("\nChanged after lock\n")
            with self.assertRaisesRegex(GovernanceBlocker, "changed after approval"):
                manager._assert_lock(locked)


if __name__ == "__main__":
    unittest.main()
