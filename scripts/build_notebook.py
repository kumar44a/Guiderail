"""Build and execute notebooks/guiderail_walkthrough.ipynb so its outputs are saved in the file.

    python scripts/build_notebook.py            # needs: pip install -r requirements-notebook.txt

The notebook holds no logic. Every cell calls the package, a script, or displays a saved evaluation report, so its numbers are the same ones the README
and docs/EVALUATION_REPORT.md show. It uses the offline extractive generator, so executing it needs no network and no API key.
"""

from __future__ import annotations

from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks" / "guiderail_walkthrough.ipynb"

CELLS = [
("md", """# GuideRail walkthrough (executed)

A citation-first RAG assistant over healthcare guideline documents: it answers only from retrieved text, checks each answer against that evidence, and returns
`needs_review` when support is weak (threshold 0.6).

This notebook has **no logic of its own**. It calls the package, runs the project's scripts, and displays the saved evaluation reports, so the numbers match the README and
`docs/EVALUATION_REPORT.md`. It uses the offline extractive generator (no network, no API key). Outputs are saved in the file, so it can be read without running anything.

**Read the last section before trusting any number:** results on the owner's independent questions are much weaker than the development results.
Research prototype; not for clinical use. The synthetic guideline text has not been clinically reviewed."""),
("code", """import sys, os, json, subprocess
from pathlib import Path
ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "evaluation")]
os.chdir(ROOT)
print("project root:", ROOT.name)"""),
("md", "## 1. Deterministic indexing\n\nThe pipeline builds the FAISS index twice, in separate processes, from the synthetic Markdown guidelines and compares SHA-256 hashes."),
("code", """r = subprocess.run([sys.executable, "scripts/pipeline.py", "--check-determinism"], capture_output=True, text=True, encoding="utf-8")
print(r.stdout.strip()); print(r.stderr.strip()[-300:])"""),
("code", """manifest = json.loads((ROOT / "index" / "manifest.json").read_text(encoding="utf-8"))
print({k: manifest[k] for k in manifest if k in ("embedding_method", "dim", "documents", "chunks", "index_sha256", "counts")} or list(manifest))"""),
("md", "## 2. The API: `POST /qa`\n\nThe real FastAPI app, called through its test client (same code path as `uvicorn`)."),
("code", """from fastapi.testclient import TestClient
from guiderail.api import create_app
client = TestClient(create_app(index_dir=ROOT / "index", threshold=0.6))
client.__enter__()
print(client.get("/health").json())"""),
("code", """def ask(q, top_k=5):
    body = client.post("/qa", json={"question": q, "top_k": top_k}).json()
    print("Q:", q); print("status:", body["status"], "| confidence:", body["confidence"])
    print("A:", body["answer"][:400]); 
    for c in body["citations"][:3]: print("  cite:", c["title"], "|", c["section"], "| v", c["version"], "| score", c["score"])
    print()
ask("How long must hands be washed with soap and water when visibly dirty?")
ask("What should be done with used needles?")"""),
("md", "**Look closely at the first answer.** It is validated, yet it also repeats the old 30-second figure from a changes note. This question is in the saved review list below as *validated but wrong*: a validated status is evidence-supported, not guaranteed correct."),
("md", "### Two harder questions, shown as they came out\n\nThe first is not in the documents and is correctly sent to review (note that low-scoring citations are still listed so an analyst can look). The second is in scope, but the extractive generator returns scope sentences instead of the answer and the validator correctly refuses to validate it. Neither was chosen to look good."),
("code", """ask("What is the recommended dose of amoxicillin for otitis media?")
ask("How long should a worker stay home after a respiratory illness?")"""),
("md", "### Input validation"),
("code", """for bad in ({"question": "", "top_k": 5}, {"question": "ok", "top_k": 0}, {"question": "ok", "top_k": 99}):
    print(bad, "->", client.post("/qa", json=bad).status_code)"""),
("md", "## 3. Evaluation reports (generated from `evaluation/reports/`)\n\nRetrieval Precision@K, mean confidence and pass rate at the threshold, for the held-out test split of the synthetic corpus."),
("code", """from IPython.display import Markdown, display
display(Markdown((ROOT / "evaluation/reports/synthetic_test_extractive_cur_summary.md").read_text(encoding="utf-8")[:3200]))"""),
("md", "### The same split with the Claude generator (saved run; not re-executed here)"),
("code", """display(Markdown((ROOT / "evaluation/reports/synthetic_test_llm_cur_summary.md").read_text(encoding="utf-8")[:3200]))"""),
("md", "## 4. Low-confidence queries for analyst review\n\nThe review list: validated-but-wrong answers, flagged answers and correct answers that were withheld."),
("code", """import csv
rows = list(csv.DictReader(open(ROOT / "evaluation/reports/synthetic_test_extractive_cur_low_confidence.csv", encoding="utf-8")))
print(len(rows), "rows")
for r in rows[:8]: print(f'{r["id"]:>4} | {r["reason"]:<26} | conf {r["confidence"]} | {r["question"][:70]}')"""),
("md", "## 5. Real PDFs and the independent question sets\n\nThe table block below is read from the README, where it is generated from the saved reports. **The sealed sets are questions the system was never tuned on.** They are the better guide to real use."),
("code", """text = (ROOT / "README.md").read_text(encoding="utf-8")
block = text.split("<!-- stats:start -->")[1].split("<!-- stats:end -->")[0]
display(Markdown(block))"""),
("md", """## 6. What this does and does not show

- **Met:** deterministic indexing, the REST contract, the validator working independently of the generator, and honest reporting of every result.
- **Precision@5 of 0.65:** missed at first on the synthetic corpus; a document-cohesion re-rank (retrieval round 8) reached it on a fresh final set, judged under rules written first (report section 18). The brief's own v1 held-out figure sits right on the threshold.
- **Not met:** the Claude generator's 80% pass rate on the real-PDF held-out split.
- **Weak:** on real PDFs, retrieval is lexical and often misses the passage that answers a question worded differently from the document. The offline extractive generator can then validate a wrong answer; use the Claude generator for real documents. A semantic embedding model would help and was ruled out for this project.
- **Thin evidence:** the corpus and queries were written by the same AI that wrote the system; no clinician reviewed anything; only a few out-of-scope questions exist in the independent sets; Docker was verified on macOS only and the Windows setup never ran.

Full account: `docs/EVALUATION_REPORT.md` (sections 11 to 16), `docs/DEVELOPMENT_NOTES.md`."""),
]


def main() -> int:
    nb = nbformat.v4.new_notebook()
    nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    nb.cells = [nbformat.v4.new_markdown_cell(src) if kind == "md" else nbformat.v4.new_code_cell(src) for kind, src in CELLS]
    OUT.parent.mkdir(exist_ok=True)
    NotebookClient(nb, timeout=300, kernel_name="python3", resources={"metadata": {"path": str(OUT.parent)}}).execute()
    nbformat.write(nb, OUT)
    print("wrote", OUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
