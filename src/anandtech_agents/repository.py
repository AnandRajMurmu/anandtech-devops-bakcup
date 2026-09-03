from __future__ import annotations

import hashlib
from pathlib import Path


class RepositoryViolation(RuntimeError):
    pass


class Repository:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def resolve(self, relative_path: str) -> Path:
        candidate = (self.root / relative_path).resolve()
        if candidate != self.root and self.root not in candidate.parents:
            raise RepositoryViolation(f"Path escapes repository: {relative_path}")
        return candidate

    def read(self, relative_path: str) -> str:
        return self.resolve(relative_path).read_text(encoding="utf-8")

    def write(self, relative_path: str, content: str, allowed_prefixes: tuple[str, ...]) -> None:
        normalized = Path(relative_path).as_posix()
        target = self.resolve(normalized)
        allowed_roots = [self.resolve(prefix) for prefix in allowed_prefixes]
        if not any(target == allowed or allowed in target.parents for allowed in allowed_roots):
            raise RepositoryViolation(f"Write is outside the agent's allowed paths: {relative_path}")
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(target.suffix + ".tmp")
        temporary.write_text(content, encoding="utf-8")
        temporary.replace(target)

    def sha256(self, relative_path: str) -> str:
        return hashlib.sha256(self.resolve(relative_path).read_bytes()).hexdigest()

    def collect_text(self, directory: str, max_file_bytes: int = 512_000) -> dict[str, str]:
        root = self.resolve(directory)
        if not root.exists():
            return {}
        result: dict[str, str] = {}
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            if path.stat().st_size > max_file_bytes:
                continue
            try:
                result[path.relative_to(self.root).as_posix()] = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
        return result
