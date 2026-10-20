# Evaluation summary: synthetic2 corpus, final split

- Index: `ffe20683ee85c731…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 25 in-corpus, 5 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 100.0% |
| Precision@5 (document level) | 83.2% |
| Precision@10 (document level) | 56.4% |
| Capped Precision@1 (vs. best attainable) | 100.0% |
| Capped Precision@5 (vs. best attainable) | 83.2% |
| Capped Precision@10 (vs. best attainable) | 72.3% |
| Hit@1 (a chunk containing the expected fact) | 76.0% |
| Hit@5 (a chunk containing the expected fact) | 96.0% |
| Hit@10 (a chunk containing the expected fact) | 100.0% |
| MRR (first fact-bearing chunk) | 0.8583 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 88.0% |
| Mean confidence (in-corpus) | 0.805 |
| Answer correct (expected facts present) | 96.0% |
| **Validated precision** (correct among validated) | 95.5% |
| **Validated but wrong** | 4.5% |
| Correct but flagged for review | 12.5% |
| Out-of-corpus sent to review | 100.0% |
| Out-of-corpus falsely validated | 0.0% |
| Decision accuracy (all queries) | 86.7% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 96.0% | 4.0% | 0.0% | 20.0% | 93.3% |
| 0.35 | 100.0% | 96.0% | 4.0% | 0.0% | 20.0% | 93.3% |
| 0.4 | 100.0% | 96.0% | 4.0% | 0.0% | 20.0% | 93.3% |
| 0.45 | 100.0% | 96.0% | 4.0% | 0.0% | 0.0% | 96.7% |
| 0.5 | 100.0% | 96.0% | 4.0% | 0.0% | 0.0% | 96.7% |
| 0.55 | 96.0% | 95.8% | 4.2% | 4.2% | 0.0% | 93.3% |
| 0.6 | 88.0% | 95.5% | 4.5% | 12.5% | 0.0% | 86.7% |
| 0.65 | 88.0% | 95.5% | 4.5% | 12.5% | 0.0% | 86.7% |
| 0.7 | 84.0% | 95.2% | 4.8% | 16.7% | 0.0% | 83.3% |
| 0.75 | 68.0% | 94.1% | 5.9% | 33.3% | 0.0% | 70.0% |
| 0.8 | 60.0% | 100.0% | 0.0% | 37.5% | 0.0% | 70.0% |
| 0.85 | 36.0% | 100.0% | 0.0% | 62.5% | 0.0% | 50.0% |
| 0.9 | 20.0% | 100.0% | 0.0% | 79.2% | 0.0% | 36.7% |

## Items for analyst review (4)

- **FX-02** (correct answer withheld, confidence 0.586): What disinfectant strength is used on a blood spill?
- **FX-07** (correct answer withheld, confidence 0.574): When should antibiotics given to prevent surgical infection usually stop?
- **FX-10** (VALIDATED BUT WRONG, confidence 0.765): How should risks be put to patients in a shared decision?
- **FX-12** (correct answer withheld, confidence 0.535): How far apart should symptomatic patients sit in a waiting area?
