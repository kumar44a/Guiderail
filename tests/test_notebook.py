import json
from pathlib import Path

NB = Path(__file__).resolve().parents[1] / "notebooks" / "guiderail_walkthrough.ipynb"


def test_walkthrough_notebook_is_executed_and_clean():
    nb = json.loads(NB.read_text(encoding="utf-8"))
    code = [c for c in nb["cells"] if c["cell_type"] == "code"]
    assert code, "notebook has no code cells"
    assert all(c["execution_count"] is not None for c in code), "a cell was never executed"
    assert not [o for c in code for o in c["outputs"] if o["output_type"] == "error"], "a cell saved an error"


def test_walkthrough_notebook_holds_no_logic_of_its_own():
    nb = json.loads(NB.read_text(encoding="utf-8"))
    source = "\n".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code")
    assert "def ask" in source and "class " not in source      # one tiny display helper only; no classes, no model code
    assert "faiss" not in source and "embed(" not in source
