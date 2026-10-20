# Evaluation summary: synthetic2 corpus, dev split

- Index: `ffe20683ee85c731…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 45 in-corpus, 10 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 95.6% |
| Precision@5 (document level) | 79.6% |
| Precision@10 (document level) | 58.4% |
| Capped Precision@1 (vs. best attainable) | 95.6% |
| Capped Precision@5 (vs. best attainable) | 81.3% |
| Capped Precision@10 (vs. best attainable) | 75.0% |
| Hit@1 (a chunk containing the expected fact) | 64.4% |
| Hit@5 (a chunk containing the expected fact) | 97.8% |
| Hit@10 (a chunk containing the expected fact) | 97.8% |
| MRR (first fact-bearing chunk) | 0.7926 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 91.1% |
| Mean confidence (in-corpus) | 0.8115 |
| Answer correct (expected facts present) | 93.3% |
| **Validated precision** (correct among validated) | 95.1% |
| **Validated but wrong** | 4.9% |
| Correct but flagged for review | 7.1% |
| Out-of-corpus sent to review | 70.0% |
| Out-of-corpus falsely validated | 30.0% |
| Decision accuracy (all queries) | 85.5% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 93.3% | 6.7% | 0.0% | 60.0% | 83.6% |
| 0.35 | 100.0% | 93.3% | 6.7% | 0.0% | 60.0% | 83.6% |
| 0.4 | 100.0% | 93.3% | 6.7% | 0.0% | 50.0% | 85.5% |
| 0.45 | 97.8% | 93.2% | 6.8% | 2.4% | 40.0% | 85.5% |
| 0.5 | 97.8% | 93.2% | 6.8% | 2.4% | 40.0% | 85.5% |
| 0.55 | 93.3% | 95.2% | 4.8% | 4.8% | 30.0% | 87.3% |
| 0.6 | 91.1% | 95.1% | 4.9% | 7.1% | 30.0% | 85.5% |
| 0.65 | 88.9% | 95.0% | 5.0% | 9.5% | 30.0% | 83.6% |
| 0.7 | 82.2% | 94.6% | 5.4% | 16.7% | 30.0% | 78.2% |
| 0.75 | 73.3% | 93.9% | 6.1% | 26.2% | 30.0% | 70.9% |
| 0.8 | 55.6% | 92.0% | 8.0% | 45.2% | 20.0% | 58.2% |
| 0.85 | 40.0% | 88.9% | 11.1% | 61.9% | 0.0% | 49.1% |
| 0.9 | 24.4% | 90.9% | 9.1% | 76.2% | 0.0% | 40.0% |

## Items for analyst review (9)

- **S11** (correct answer withheld, confidence 0.582): What bleach strength is used for blood spills?
- **S23** (VALIDATED BUT WRONG, confidence 1.0): What are the steps of shared decision making?
- **S45** (VALIDATED BUT OUT OF CORPUS, confidence 0.785): How should radioactive waste be disposed of?
- **S47** (VALIDATED BUT OUT OF CORPUS, confidence 0.848): What is the incubation period of influenza?
- **DX-08** (correct answer withheld, confidence 0.532): How long should someone with a history of severe allergy be watched after a vaccine?
- **DX-10** (flagged: low confidence, confidence 0.522): How many ill staff on one ward in a week should prompt a review for a cluster?
- **DX-17** (correct answer withheld, confidence 0.437): How much reserve stock of PPE should be kept?
- **DX-20** (VALIDATED BUT WRONG, confidence 0.874): How many steps does shared decision making have?
- **DX-O3** (VALIDATED BUT OUT OF CORPUS, confidence 0.804): What is the incubation period of rabies?
