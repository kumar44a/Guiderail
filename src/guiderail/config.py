"""Runtime settings, read from the environment with safe defaults."""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DEFAULT_THRESHOLD = 0.6
DEFAULT_RERANK_WEIGHT = 0.5      # chosen on the dev split; 0 turns the lexical re-ranker off
DEFAULT_LLM_MODEL = "claude-opus-5-5"
DEFAULT_REWRITE_MODEL = "claude-haiku-4-5-20251001"


def load_env_file(path: Path | None = None) -> None:
    """Load KEY=VALUE lines from .env into os.environ without overriding real env vars."""
    path = path or ROOT / ".env"
    if not path.is_file():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip().removeprefix("export ").strip()
        os.environ.setdefault(key, value.strip().strip("'\""))


def index_dir() -> Path:
    return Path(os.environ.get("GUIDERAIL_INDEX_DIR", ROOT / "index"))


def threshold() -> float:
    value = float(os.environ.get("GUIDERAIL_THRESHOLD", DEFAULT_THRESHOLD))
    if not 0.0 <= value <= 1.0:
        raise ValueError(f"GUIDERAIL_THRESHOLD must be between 0 and 1, got {value}")
    return value


def rerank_weight() -> float:
    value = float(os.environ.get("GUIDERAIL_RERANK_WEIGHT", DEFAULT_RERANK_WEIGHT))
    if value < 0:
        raise ValueError(f"GUIDERAIL_RERANK_WEIGHT must be >= 0, got {value}")
    return value


def hybrid() -> bool:
    """Hybrid retrieval (FAISS + BM25 fused). GUIDERAIL_HYBRID=0 falls back to FAISS alone."""
    return os.environ.get("GUIDERAIL_HYBRID", "1").lower() not in {"0", "false", "no", "off"}


def generator_name() -> str:
    name = os.environ.get("GUIDERAIL_GENERATOR", "extractive").lower()
    if name not in {"extractive", "llm"}:
        raise ValueError(f"GUIDERAIL_GENERATOR must be 'extractive' or 'llm', got {name!r}")
    return name


def rewrite() -> bool:
    """Query rewriting in the Claude mode. Off by default: the evaluation showed no end-to-end benefit (see the round 5 outcome).
    GUIDERAIL_REWRITE=1 turns it on."""
    return os.environ.get("GUIDERAIL_REWRITE", "0").lower() in {"1", "true", "yes", "on"}


def rewrite_model() -> str:
    return os.environ.get("GUIDERAIL_REWRITE_MODEL", DEFAULT_REWRITE_MODEL)


def llm_model() -> str:
    return os.environ.get("GUIDERAIL_LLM_MODEL", DEFAULT_LLM_MODEL)
