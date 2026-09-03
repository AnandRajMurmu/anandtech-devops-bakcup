from __future__ import annotations

import json
from typing import Any
from urllib import error, request


class LLMError(RuntimeError):
    pass


class OpenAICompatibleClient:
    def __init__(self, base_url: str, api_key: str, model: str, timeout: int = 600):
        self.url = f"{base_url}/chat/completions"
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    def complete_json(self, system_prompt: str, payload: dict[str, Any]) -> dict[str, Any]:
        body = json.dumps(
            {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
                ],
                "temperature": 0.2,
                "response_format": {"type": "json_object"},
            }
        ).encode("utf-8")
        req = request.Request(
            self.url,
            data=body,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=self.timeout) as response:
                envelope = json.loads(response.read().decode("utf-8"))
        except (error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise LLMError(f"LLM request failed: {exc}") from exc
        try:
            content = envelope["choices"][0]["message"]["content"].strip()
            if content.startswith("```"):
                content = content.split("\n", 1)[1].rsplit("```", 1)[0]
            result = json.loads(content)
        except (KeyError, IndexError, json.JSONDecodeError) as exc:
            raise LLMError("LLM did not return the required JSON object") from exc
        if not isinstance(result, dict):
            raise LLMError("LLM response must be a JSON object")
        return result

