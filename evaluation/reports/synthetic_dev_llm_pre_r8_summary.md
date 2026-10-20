# Evaluation summary: synthetic corpus, dev split

- Index: `45c3d9422161bc97…`  |  generator: `llm`  |  threshold: 0.6
- Queries: 20 in-corpus, 5 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 95.0% |
| Precision@5 (document level) | 55.0% |
| Precision@10 (document level) | 30.5% |
| Capped Precision@1 (vs. best attainable) | 95.0% |
| Capped Precision@5 (vs. best attainable) | 74.3% |
| Capped Precision@10 (vs. best attainable) | 78.4% |
| Hit@1 (a chunk containing the expected fact) | 70.0% |
| Hit@5 (a chunk containing the expected fact) | 100.0% |
| Hit@10 (a chunk containing the expected fact) | 100.0% |
| MRR (first fact-bearing chunk) | 0.825 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 100.0% |
| Mean confidence (in-corpus) | 0.7863 |
| Answer correct (expected facts present) | 100.0% |
| **Validated precision** (correct among validated) | 100.0% |
| **Validated but wrong** | 0.0% |
| Correct but flagged for review | 0.0% |
| Out-of-corpus sent to review | 100.0% |
| Out-of-corpus falsely validated | 0.0% |
| Decision accuracy (all queries) | 100.0% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.35 | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.4 | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.45 | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.5 | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.55 | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.6 | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.65 | 95.0% | 100.0% | 0.0% | 5.0% | 0.0% | 96.0% |
| 0.7 | 80.0% | 100.0% | 0.0% | 20.0% | 0.0% | 84.0% |
| 0.75 | 65.0% | 100.0% | 0.0% | 35.0% | 0.0% | 72.0% |
| 0.8 | 40.0% | 100.0% | 0.0% | 60.0% | 0.0% | 52.0% |
| 0.85 | 25.0% | 100.0% | 0.0% | 75.0% | 0.0% | 40.0% |
| 0.9 | 10.0% | 100.0% | 0.0% | 90.0% | 0.0% | 28.0% |

## Items for analyst review (0)

