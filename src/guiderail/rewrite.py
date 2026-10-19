"""Optional query rewriting for the Claude mode: one small-model call turns an informal question into search keywords.

The rewrite is appended to the question for SEARCHING only. The generator and the validator see the original question, so a rewrite cannot
make a badly matched answer look relevant. Any failure returns None and the original question is used. Rewrites can be cached in a JSON
file so evaluation runs are repeatable.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path

from .config import ROOT, load_env_file, rewrite_model

log = logging.getLogger(__name__)
PROMPT_PATH = ROOT / "prompts" / "query_rewrite.txt"
MAX_CHARS = 200


def clean_rewrite(text: str, question: str) -> str | None:
    """First line only, quotes and a leading label removed, whitespace collapsed, capped. None if empty or no different from the question."""
    line = (text or "").strip().splitlines()[0] if (text or "").strip() else ""
    line = re.sub(r"^(keywords?|query)\s*:\s*", "", line.strip().strip("\"'`"), flags=re.IGNORECASE)
    line = " ".join(line.split())[:MAX_CHARS].strip()
    return line if line and line.lower() != question.strip().lower() else None


class QueryRewriter:
    def __init__(self, client=None, model: str | None = None, cache_path: Path | str | None = None, system_prompt: str | None = None):
        self._client = client
        self.model = model or rewrite_model()
        self.system_prompt = system_prompt or Path(PROMPT_PATH).read_text(encoding="utf-8")
        self.cache_path = Path(cache_path) if cache_path else None
        self.cache: dict[str, str | None] = {}
        if self.cache_path and self.cache_path.is_file():
            self.cache = json.loads(self.cache_path.read_text(encoding="utf-8"))
        self.calls = 0
        self.last_request_id: str | None = None
        self.last_usage: dict | None = None

    @property
    def client(self):
        if self._client is None:
            import anthropic  # lazy: only the Claude mode needs it

            load_env_file()
            self._client = anthropic.Anthropic()
        return self._client

    def rewrite(self, question: str) -> str | None:
        key = question.strip()
        if key in self.cache:
            return self.cache[key]
        try:
            response = self.client.messages.create(
                model=self.model, max_tokens=120, system=self.system_prompt,
                messages=[{"role": "user", "content": f"Question: {key}\nKeywords:"}])
        except Exception as exc:                      # a failed rewrite must never break a query
            log.warning("query rewrite failed: %s: %s", type(exc).__name__, exc)
            return None
        self.calls += 1
        self.last_request_id = getattr(response, "_request_id", None)
        usage = getattr(response, "usage", None)
        self.last_usage = ({"input_tokens": usage.input_tokens, "output_tokens": usage.output_tokens}
                           if usage is not None and hasattr(usage, "input_tokens") else None)
        text = "".join(b.text for b in response.content if getattr(b, "type", None) == "text")
        result = clean_rewrite(text, key)
        self.cache[key] = result
        if self.cache_path:
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            self.cache_path.write_text(json.dumps(self.cache, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
        return result
