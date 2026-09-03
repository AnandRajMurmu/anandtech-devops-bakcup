from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    repo_root: Path
    llm_base_url: str
    llm_api_key: str
    llm_model: str
    slack_webhook_url: str | None
    max_revisions: int

    @classmethod
    def from_environment(cls, repo_root: Path | None = None) -> "Settings":
        root = (repo_root or Path.cwd()).resolve()
        return cls(
            repo_root=root,
            llm_base_url=os.getenv("ANANDTECH_LLM_BASE_URL", "").rstrip("/"),
            llm_api_key=os.getenv("ANANDTECH_LLM_API_KEY", ""),
            llm_model=os.getenv("ANANDTECH_LLM_MODEL", ""),
            slack_webhook_url=os.getenv("ANANDTECH_SLACK_WEBHOOK_URL") or None,
            max_revisions=int(os.getenv("ANANDTECH_MAX_REVISIONS", "5")),
        )

    def require_llm(self) -> None:
        missing = [
            name
            for name, value in (
                ("ANANDTECH_LLM_BASE_URL", self.llm_base_url),
                ("ANANDTECH_LLM_API_KEY", self.llm_api_key),
                ("ANANDTECH_LLM_MODEL", self.llm_model),
            )
            if not value
        ]
        if missing:
            raise RuntimeError("Missing LLM configuration: " + ", ".join(missing))

