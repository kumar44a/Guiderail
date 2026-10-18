"""Optional generator: Claude answers from the retrieved evidence only.

The `anthropic` import is lazy because the SDK is slow to import and the default
extractive path does not need it. The answer still goes through the same
independent validator as every other generator.
"""

from __future__ import annotations

import re
from pathlib import Path

from ..config import ROOT, llm_model, load_env_file
from ..retriever import Hit
from .base import GenerationError, Generated, Generator

PROMPT_PATH = ROOT / "prompts" / "answer_style.txt"
NOT_IN_EVIDENCE = "NOT_IN_EVIDENCE"
_CITATION_RE = re.compile(r"\[([^\[\]\s]+#[^\[\]\s]+)\]")
FALLBACK_BETA = "server-side-fallback-2026-07-01"


def format_evidence(hits: list[Hit]) -> str:
    return "\n\n".join(f"[{h.chunk.chunk_id}] ({h.chunk.agency} {h.chunk.year}, {h.chunk.section})\n{h.chunk.text}" for h in hits)


class LlmGenerator(Generator):
    name = "llm"

    def __init__(self, client=None, model: str | None = None, use_fallbacks: bool = True,
                 system_prompt: str | None = None):
        self._client = client
        self.model = model or llm_model()
        self.use_fallbacks = use_fallbacks
        self.system_prompt = system_prompt or Path(PROMPT_PATH).read_text(encoding="utf-8")
        self.last_request_id: str | None = None
        self.last_usage: dict | None = None
        self.last_model: str | None = None

    @property
    def client(self):
        if self._client is None:
            import anthropic  # lazy: slow import, only needed on this path

            load_env_file()
            self._client = anthropic.Anthropic()
        return self._client

    def generate(self, question: str, hits: list[Hit]) -> Generated:
        if not hits:
            return Generated.abstain()
        request = dict(
            model=self.model,
            max_tokens=16000,
            system=self.system_prompt,
            output_config={"effort": "low"},
            messages=[{"role": "user", "content": f"Evidence passages:\n\n{format_evidence(hits)}\n\nQuestion: {question}"}],
        )
        if self.use_fallbacks:
            request.update(betas=[FALLBACK_BETA], fallbacks="default")
        try:
            response = self.client.beta.messages.create(**request) if self.use_fallbacks \
                else self.client.messages.create(**request)
        except Exception as exc:   # SDK raises typed APIError subclasses; any failure means "no answer"
            raise GenerationError(f"LLM request failed: {type(exc).__name__}: {exc}") from exc

        self.last_request_id = getattr(response, "_request_id", None)
        self.last_model = getattr(response, "model", None)
        usage = getattr(response, "usage", None)
        self.last_usage = (
            {"input_tokens": usage.input_tokens, "output_tokens": usage.output_tokens}
            if usage is not None and hasattr(usage, "input_tokens") else None
        )
        if getattr(response, "stop_reason", None) == "refusal":
            return Generated.abstain()
        text = "".join(b.text for b in response.content if getattr(b, "type", None) == "text").strip()
        if not text or NOT_IN_EVIDENCE in text:
            return Generated.abstain()

        valid_ids = {h.chunk.chunk_id for h in hits}
        cited = [c for c in dict.fromkeys(_CITATION_RE.findall(text)) if c in valid_ids]
        clean = re.sub(r"\s*\[[^\[\]\s]+#[^\[\]\s]+\]", "", text).strip()
        return Generated(answer=clean, chunk_ids=cited)
