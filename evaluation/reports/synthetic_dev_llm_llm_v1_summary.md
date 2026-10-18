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
| Pass rate (validated / in-corpus) | 85.0% |
| Mean confidence (in-corpus) | 0.7381 |
| Answer correct (expected facts present) | 95.0% |
| **Validated precision** (correct among validated) | 94.1% |
| **Validated but wrong** | 5.9% |
| Correct but flagged for review | 15.8% |
| Out-of-corpus sent to review | 100.0% |
| Out-of-corpus falsely validated | 0.0% |
| Decision accuracy (all queries) | 84.0% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 95.0% | 5.0% | 0.0% | 0.0% | 96.0% |
| 0.35 | 100.0% | 95.0% | 5.0% | 0.0% | 0.0% | 96.0% |
| 0.4 | 100.0% | 95.0% | 5.0% | 0.0% | 0.0% | 96.0% |
| 0.45 | 95.0% | 94.7% | 5.3% | 5.3% | 0.0% | 92.0% |
| 0.5 | 95.0% | 94.7% | 5.3% | 5.3% | 0.0% | 92.0% |
| 0.55 | 90.0% | 94.4% | 5.6% | 10.5% | 0.0% | 88.0% |
| 0.6 | 85.0% | 94.1% | 5.9% | 15.8% | 0.0% | 84.0% |
| 0.65 | 75.0% | 93.3% | 6.7% | 26.3% | 0.0% | 76.0% |
| 0.7 | 60.0% | 91.7% | 8.3% | 42.1% | 0.0% | 64.0% |
| 0.75 | 45.0% | 100.0% | 0.0% | 52.6% | 0.0% | 60.0% |
| 0.8 | 40.0% | 100.0% | 0.0% | 57.9% | 0.0% | 56.0% |
| 0.85 | 30.0% | 100.0% | 0.0% | 68.4% | 0.0% | 48.0% |
| 0.9 | 15.0% | 100.0% | 0.0% | 84.2% | 0.0% | 36.0% |

## Items for analyst review (4)

- **S01** (correct answer withheld, confidence 0.551): How long should I rub alcohol-based hand sanitizer on my hands?
- **S09** (VALIDATED BUT WRONG, confidence 0.732): Can one gown be worn between different patients?
- **S11** (correct answer withheld, confidence 0.5): What bleach strength is used for blood spills?
- **S29** (correct answer withheld, confidence 0.422): Which vaccine needs a booster every ten years?
