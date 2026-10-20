from pathlib import Path

from guiderail.generators.base import Generated
from guiderail.index import load_index
from guiderail.service import QAService

ROOT = Path(__file__).resolve().parents[1]


class Spy:
    def __init__(self, name):
        self.name, self.seen = name, 0

    def generate(self, question, hits):
        self.seen = len(hits)
        return Generated.abstain()


def test_llm_context_widens_only_the_llm_generator(monkeypatch):
    loaded = load_index(ROOT / "index")
    monkeypatch.setenv("GUIDERAIL_LLM_CONTEXT", "8")
    llm, ext = Spy("llm"), Spy("extractive")
    QAService(loaded, generator=llm).ask("How long should hands be rubbed?", 3)
    QAService(loaded, generator=ext).ask("How long should hands be rubbed?", 3)
    assert llm.seen >= 8 and ext.seen < 8


def test_llm_context_default_changes_nothing(monkeypatch):
    monkeypatch.delenv("GUIDERAIL_LLM_CONTEXT", raising=False)
    spy = Spy("llm")
    QAService(load_index(ROOT / "index"), generator=spy).ask("How long should hands be rubbed?", 3)
    assert spy.seen < 8
