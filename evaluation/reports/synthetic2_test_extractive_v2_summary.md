# Evaluation summary: synthetic2 corpus, test split

- Index: `ffe20683ee85c731…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 20 in-corpus, 5 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 95.0% |
| Precision@5 (document level) | 59.0% |
| Precision@10 (document level) | 42.5% |
| Capped Precision@1 (vs. best attainable) | 95.0% |
| Capped Precision@5 (vs. best attainable) | 59.0% |
| Capped Precision@10 (vs. best attainable) | 55.0% |
| Hit@1 (a chunk containing the expected fact) | 85.0% |
| Hit@5 (a chunk containing the expected fact) | 100.0% |
| Hit@10 (a chunk containing the expected fact) | 100.0% |
| MRR (first fact-bearing chunk) | 0.9167 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 90.0% |
| Mean confidence (in-corpus) | 0.7924 |
| Answer correct (expected facts present) | 90.0% |
| **Validated precision** (correct among validated) | 88.9% |
| **Validated but wrong** | 11.1% |
| Correct but flagged for review | 11.1% |
| Out-of-corpus sent to review | 80.0% |
| Out-of-corpus falsely validated | 20.0% |
| Decision accuracy (all queries) | 80.0% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 90.0% | 10.0% | 0.0% | 60.0% | 80.0% |
| 0.35 | 100.0% | 90.0% | 10.0% | 0.0% | 60.0% | 80.0% |
| 0.4 | 100.0% | 90.0% | 10.0% | 0.0% | 60.0% | 80.0% |
| 0.45 | 95.0% | 89.5% | 10.5% | 5.6% | 20.0% | 84.0% |
| 0.5 | 95.0% | 89.5% | 10.5% | 5.6% | 20.0% | 84.0% |
| 0.55 | 95.0% | 89.5% | 10.5% | 5.6% | 20.0% | 84.0% |
| 0.6 | 90.0% | 88.9% | 11.1% | 11.1% | 20.0% | 80.0% |
| 0.65 | 85.0% | 88.2% | 11.8% | 16.7% | 20.0% | 76.0% |
| 0.7 | 75.0% | 86.7% | 13.3% | 27.8% | 20.0% | 68.0% |
| 0.75 | 60.0% | 83.3% | 16.7% | 44.4% | 0.0% | 60.0% |
| 0.8 | 50.0% | 80.0% | 20.0% | 55.6% | 0.0% | 52.0% |
| 0.85 | 45.0% | 77.8% | 22.2% | 61.1% | 0.0% | 48.0% |
| 0.9 | 25.0% | 60.0% | 40.0% | 83.3% | 0.0% | 32.0% |

## Items for analyst review (5)

- **T2-01** (correct answer withheld, confidence 0.438): How many minutes must a blood spill sit under the bleach solution before it is wiped up?
- **T2-03** (correct answer withheld, confidence 0.564): When should antiretroviral prophylaxis start after a needlestick from an HIV-positive patient?
- **T2-14** (VALIDATED BUT WRONG, confidence 1.0): Who leads the outbreak control team?
- **T2-20** (VALIDATED BUT WRONG, confidence 1.0): What are the steps of shared decision making?
- **T2-O5** (VALIDATED BUT OUT OF CORPUS, confidence 0.718): How often should hospital lifts be inspected?
