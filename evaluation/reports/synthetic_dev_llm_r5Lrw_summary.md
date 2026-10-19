# Evaluation summary: synthetic corpus, dev split

- Index: `45c3d9422161bc97…`  |  generator: `llm`  |  threshold: 0.6
- Queries: 20 in-corpus, 5 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 95.0% |
| Precision@5 (document level) | 56.0% |
| Precision@10 (document level) | 29.5% |
| Capped Precision@1 (vs. best attainable) | 95.0% |
| Capped Precision@5 (vs. best attainable) | 76.0% |
| Capped Precision@10 (vs. best attainable) | 77.3% |
| Hit@1 (a chunk containing the expected fact) | 70.0% |
| Hit@5 (a chunk containing the expected fact) | 100.0% |
| Hit@10 (a chunk containing the expected fact) | 100.0% |
| MRR (first fact-bearing chunk) | 0.825 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 85.0% |
| Mean confidence (in-corpus) | 0.7378 |
| Answer correct (expected facts present) | 95.0% |
| **Validated precision** (correct among validated) | 100.0% |
| **Validated but wrong** | 0.0% |
| Correct but flagged for review | 10.5% |
| Out-of-corpus sent to review | 100.0% |
| Out-of-corpus falsely validated | 0.0% |
| Decision accuracy (all queries) | 92.0% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 95.0% | 5.0% | 0.0% | 0.0% | 96.0% |
| 0.35 | 95.0% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.4 | 95.0% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.45 | 95.0% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.5 | 90.0% | 100.0% | 0.0% | 5.3% | 0.0% | 96.0% |
| 0.55 | 85.0% | 100.0% | 0.0% | 10.5% | 0.0% | 92.0% |
| 0.6 | 85.0% | 100.0% | 0.0% | 10.5% | 0.0% | 92.0% |
| 0.65 | 80.0% | 100.0% | 0.0% | 15.8% | 0.0% | 88.0% |
| 0.7 | 70.0% | 100.0% | 0.0% | 26.3% | 0.0% | 80.0% |
| 0.75 | 50.0% | 100.0% | 0.0% | 47.4% | 0.0% | 64.0% |
| 0.8 | 40.0% | 100.0% | 0.0% | 57.9% | 0.0% | 56.0% |
| 0.85 | 25.0% | 100.0% | 0.0% | 73.7% | 0.0% | 44.0% |
| 0.9 | 10.0% | 100.0% | 0.0% | 89.5% | 0.0% | 32.0% |

## Items for analyst review (3)

- **S01** (flagged: low confidence, confidence 0.326): How long should I rub alcohol-based hand sanitizer on my hands?
- **S11** (correct answer withheld, confidence 0.453): What bleach strength is used for blood spills?
- **S29** (correct answer withheld, confidence 0.543): Which vaccine needs a booster every ten years?
