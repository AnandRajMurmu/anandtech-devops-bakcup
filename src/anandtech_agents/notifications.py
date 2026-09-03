from __future__ import annotations

import json
from urllib import request


class SlackNotifier:
    def __init__(self, webhook_url: str | None, timeout: int = 20):
        self.webhook_url = webhook_url
        self.timeout = timeout

    def send(self, text: str) -> bool:
        if not self.webhook_url:
            return False
        body = json.dumps({"text": text}).encode("utf-8")
        req = request.Request(self.webhook_url, data=body, headers={"Content-Type": "application/json"}, method="POST")
        with request.urlopen(req, timeout=self.timeout) as response:
            if not 200 <= response.status < 300:
                raise RuntimeError(f"Slack returned HTTP {response.status}")
        return True

