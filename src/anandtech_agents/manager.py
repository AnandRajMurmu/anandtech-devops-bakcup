from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .config import Settings
from .llm import OpenAICompatibleClient
from .notifications import SlackNotifier
from .repository import Repository
from .ssot import apply_lock, lock_status, parse_units, validate_draft
from .state import WorkflowStore, utc_now


class GovernanceBlocker(RuntimeError):
    pass


class Manager:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.repo = Repository(settings.repo_root)
        self.store = WorkflowStore(settings.repo_root / "workflow" / "state.json")
        self.slack = SlackNotifier(settings.slack_webhook_url)

    def _client(self) -> OpenAICompatibleClient:
        self.settings.require_llm()
        return OpenAICompatibleClient(
            self.settings.llm_base_url,
            self.settings.llm_api_key,
            self.settings.llm_model,
        )

    def _governing_context(self, section: dict[str, Any]) -> dict[str, str]:
        return {
            "agents": self.repo.read("AGENTS.md"),
            "master_prompt": self.repo.read("docs/master_prompt.md"),
            "project_ssot": self.repo.read("docs/project_SSOT.md"),
            "section_ssot": self.repo.read(section["ssot_path"]),
        }

    def status(self) -> dict[str, Any]:
        return self.store.load()

    def draft_ssot(self, brief: str) -> list[str]:
        state = self.store.load()
        section = state["section"]
        if state["phase"] not in {"ssot_draft", "awaiting_ssot_lock"}:
            raise GovernanceBlocker(f"SSOT Maker is not allowed during phase {state['phase']}")
        prompt = self.repo.read("prompts/ssot_maker.md")
        payload = {
            "action": "DRAFT_OR_REVISE",
            "brief": brief,
            "governing_context": self._governing_context(section),
            "current_plan": self.repo.read(section["plan_path"]),
            "required_output": {"files": {section["plan_path"]: "markdown", section["ssot_path"]: "markdown"}},
        }
        result = self._client().complete_json(prompt, payload)
        files = result.get("files")
        if not isinstance(files, dict) or set(files) != {section["plan_path"], section["ssot_path"]}:
            raise GovernanceBlocker("SSOT Maker returned an unexpected file set")
        if lock_status(str(files[section["ssot_path"]])) != "Draft":
            raise GovernanceBlocker("SSOT Maker cannot lock an SSOT")
        for path, content in files.items():
            self.repo.write(path, str(content), (str(Path(section["ssot_path"]).parent),))
        state["phase"] = "awaiting_ssot_lock"
        state["section"]["lock"] = {"status": "draft", "sha256": None, "approved_by": None, "approved_at_utc": None}
        self.store.save(state)
        return sorted(files)

    def lock_ssot(self, confirmation: str, approved_by: str) -> None:
        state = self.store.load()
        section = state["section"]
        expected = f"LOCK SECTION {section['number']}"
        if confirmation != expected:
            raise GovernanceBlocker(f"Explicit confirmation must be exactly: {expected}")
        if state["phase"] not in {"ssot_draft", "awaiting_ssot_lock"}:
            raise GovernanceBlocker(f"Cannot lock an SSOT during phase {state['phase']}")
        text = self.repo.read(section["ssot_path"])
        units = validate_draft(text)
        self.repo.write(section["ssot_path"], apply_lock(text), (str(Path(section["ssot_path"]).parent),))
        section["lock"] = {
            "status": "locked",
            "sha256": self.repo.sha256(section["ssot_path"]),
            "approved_by": approved_by,
            "approved_at_utc": utc_now(),
        }
        section["units"] = [
            {"number": u.number, "title": u.title, "directory": u.directory, "status": "pending", "revision_cycles": 0}
            for u in units
        ]
        state["phase"] = "ready_for_generation"
        self.store.save(state)

    def _assert_lock(self, state: dict[str, Any]) -> None:
        section = state["section"]
        if section["lock"]["status"] != "locked":
            raise GovernanceBlocker("Section SSOT is not explicitly locked")
        if lock_status(self.repo.read(section["ssot_path"])) != "Locked":
            raise GovernanceBlocker("SSOT file does not declare Locked")
        if self.repo.sha256(section["ssot_path"]) != section["lock"]["sha256"]:
            raise GovernanceBlocker("Locked SSOT changed after approval; unlock and review it again")

    def run_section(self) -> None:
        state = self.store.load()
        self._assert_lock(state)
        if state["phase"] not in {"ready_for_generation", "generating", "blocked"}:
            raise GovernanceBlocker(f"Section generation is not allowed during phase {state['phase']}")
        client = self._client()
        section = state["section"]
        context = self._governing_context(section)
        state["phase"] = "generating"
        self.store.save(state)

        for unit in section["units"]:
            if unit["status"] == "approved":
                self._notify_once(state, f"unit:{section['number']}:{unit['number']}:approved", self._unit_message(section, unit))
                continue
            feedback: dict[str, Any] | None = None
            while unit["revision_cycles"] <= self.settings.max_revisions:
                unit["status"] = "authoring"
                self.store.save(state)
                worker_payload = {
                    "assignment": unit,
                    "section": {k: section[k] for k in ("number", "slug", "title", "directory")},
                    "governing_context": context,
                    "accepted_previous_units": [u for u in section["units"] if u["status"] == "approved"],
                    "review_feedback": feedback,
                    "response_contract": {"files": {"relative/path": "complete UTF-8 content"}, "summary": "string"},
                }
                worker_result = client.complete_json(self.repo.read("prompts/worker.md"), worker_payload)
                files = worker_result.get("files")
                unit_prefix = f"{section['directory']}/{unit['directory']}"
                if not isinstance(files, dict) or not files:
                    raise GovernanceBlocker("Worker returned no files")
                for path, content in files.items():
                    self.repo.write(str(path), str(content), (unit_prefix,))

                unit["status"] = "reviewing"
                self.store.save(state)
                review_payload = {
                    "assignment": unit,
                    "governing_context": context,
                    "worker_handoff": worker_result.get("summary", ""),
                    "unit_files": self.repo.collect_text(unit_prefix),
                    "response_contract": {
                        "status": "APPROVED or BLOCKED",
                        "blocking_findings": [],
                        "non_blocking_improvements": [],
                        "evidence_checked": [],
                    },
                }
                review = client.complete_json(self.repo.read("prompts/reviewer.md"), review_payload)
                decision = str(review.get("status", "")).upper()
                report_path = f"reviews/{section['slug']}/unit{unit['number']}_review.json"
                self.repo.write(report_path, json.dumps(review, indent=2, ensure_ascii=False) + "\n", (f"reviews/{section['slug']}",))
                if decision == "APPROVED" and not review.get("blocking_findings"):
                    unit["status"] = "approved"
                    unit["approved_at_utc"] = utc_now()
                    self.store.save(state)
                    self._notify_once(state, f"unit:{section['number']}:{unit['number']}:approved", self._unit_message(section, unit))
                    break
                if decision != "BLOCKED" or not review.get("blocking_findings"):
                    raise GovernanceBlocker("Reviewer response violated the decision contract")
                unit["status"] = "revision_required"
                unit["revision_cycles"] += 1
                feedback = review
                self.store.save(state)
            if unit["status"] != "approved":
                state["phase"] = "blocked"
                state["blocker"] = f"Unit {unit['number']} exceeded {self.settings.max_revisions} revision cycles"
                self.store.save(state)
                raise GovernanceBlocker(state["blocker"])

        state["phase"] = "awaiting_owner_confirmation"
        state["blocker"] = None
        self.store.save(state)
        self._notify_once(state, f"section:{section['number']}:ready", self._section_message(section))

    def accept_section(self, confirmation: str) -> None:
        state = self.store.load()
        section = state["section"]
        expected = f"ACCEPT SECTION {section['number']}"
        if confirmation != expected:
            raise GovernanceBlocker(f"Explicit confirmation must be exactly: {expected}")
        if state["phase"] != "awaiting_owner_confirmation":
            raise GovernanceBlocker("Section is not awaiting owner confirmation")
        if any(unit["status"] != "approved" for unit in section["units"]):
            raise GovernanceBlocker("Every unit must be approved before section acceptance")
        state["phase"] = "accepted"
        state["accepted_at_utc"] = utc_now()
        self.store.save(state)

    def retry_notifications(self) -> None:
        state = self.store.load()
        section = state["section"]
        for unit in section.get("units", []):
            if unit.get("status") == "approved":
                self._notify_once(state, f"unit:{section['number']}:{unit['number']}:approved", self._unit_message(section, unit))
        if state["phase"] in {"awaiting_owner_confirmation", "accepted"} and section.get("units"):
            self._notify_once(state, f"section:{section['number']}:ready", self._section_message(section))

    def _notify_once(self, state: dict[str, Any], key: str, message: str) -> None:
        events = state.setdefault("notifications", {}).setdefault("events", {})
        if events.get(key, {}).get("status") == "sent":
            return
        try:
            sent = self.slack.send(message)
            event = {"status": "sent" if sent else "pending_configuration", "updated_at_utc": utc_now()}
        except Exception as exc:  # Notification failure must not mutate curriculum state.
            event = {"status": "pending_retry", "error_type": type(exc).__name__, "updated_at_utc": utc_now()}
        events[key] = event
        self.store.save(state)

    @staticmethod
    def _unit_message(section: dict[str, Any], unit: dict[str, Any]) -> str:
        return (
            ":white_check_mark: *AnandTech course unit approved*\n"
            f"*Section:* {section['number']} — {section['title']}\n"
            f"*Unit:* {unit['number']} — {unit['title']}\n"
            f"*Review cycles:* {unit['revision_cycles']}\n"
            "The Manager is continuing with the next authorized unit."
        )

    @staticmethod
    def _section_message(section: dict[str, Any]) -> str:
        unit_lines = "\n".join(f"{u['number']}. {u['title']}" for u in section["units"])
        return (
            ":books: *Journey with AnandTech — Section ready for owner approval*\n"
            f"*Section:* {section['number']} — {section['title']}\n"
            f"*Status:* All {len(section['units'])} units passed independent review.\n\n"
            f"*Units*\n{unit_lines}\n\n"
            f"*Next action:* confirm `ACCEPT SECTION {section['number']}` before the next SSOT begins."
        )
