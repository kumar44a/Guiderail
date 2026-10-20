# Evaluation summary: synthetic2 corpus, dev split

- Index: `ffe20683ee85c731…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 45 in-corpus, 10 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 95.6% |
| Precision@5 (document level) | 65.3% |
| Precision@10 (document level) | 46.7% |
| Capped Precision@1 (vs. best attainable) | 95.6% |
| Capped Precision@5 (vs. best attainable) | 67.1% |
| Capped Precision@10 (vs. best attainable) | 60.3% |
| Hit@1 (a chunk containing the expected fact) | 64.4% |
| Hit@5 (a chunk containing the expected fact) | 95.6% |
| Hit@10 (a chunk containing the expected fact) | 97.8% |
| MRR (first fact-bearing chunk) | 0.7847 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 88.9% |
| Mean confidence (in-corpus) | 0.8091 |
| Answer correct (expected facts present) | 91.1% |
| **Validated precision** (correct among validated) | 92.5% |
| **Validated but wrong** | 7.5% |
| Correct but flagged for review | 9.8% |
| Out-of-corpus sent to review | 70.0% |
| Out-of-corpus falsely validated | 30.0% |
| Decision accuracy (all queries) | 81.8% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 91.1% | 8.9% | 0.0% | 60.0% | 81.8% |
| 0.35 | 100.0% | 91.1% | 8.9% | 0.0% | 60.0% | 81.8% |
| 0.4 | 100.0% | 91.1% | 8.9% | 0.0% | 50.0% | 83.6% |
| 0.45 | 97.8% | 90.9% | 9.1% | 2.4% | 40.0% | 83.6% |
| 0.5 | 95.6% | 90.7% | 9.3% | 4.9% | 40.0% | 81.8% |
| 0.55 | 93.3% | 92.9% | 7.1% | 4.9% | 30.0% | 85.5% |
| 0.6 | 88.9% | 92.5% | 7.5% | 9.8% | 30.0% | 81.8% |
| 0.65 | 86.7% | 92.3% | 7.7% | 12.2% | 30.0% | 80.0% |
| 0.7 | 82.2% | 91.9% | 8.1% | 17.1% | 30.0% | 76.4% |
| 0.75 | 73.3% | 93.9% | 6.1% | 24.4% | 30.0% | 72.7% |
| 0.8 | 55.6% | 92.0% | 8.0% | 43.9% | 20.0% | 60.0% |
| 0.85 | 40.0% | 88.9% | 11.1% | 61.0% | 0.0% | 50.9% |
| 0.9 | 24.4% | 90.9% | 9.1% | 75.6% | 0.0% | 41.8% |

## Items for analyst review (11)

- **S11** (correct answer withheld, confidence 0.582): What bleach strength is used for blood spills?
- **S15** (VALIDATED BUT WRONG, confidence 0.723): By when should staff be offered the flu vaccine?
- **S23** (VALIDATED BUT WRONG, confidence 1.0): What are the steps of shared decision making?
- **S45** (VALIDATED BUT OUT OF CORPUS, confidence 0.785): How should radioactive waste be disposed of?
- **S47** (VALIDATED BUT OUT OF CORPUS, confidence 0.848): What is the incubation period of influenza?
- **DX-08** (correct answer withheld, confidence 0.58): How long should someone with a history of severe allergy be watched after a vaccine?
- **DX-10** (flagged: low confidence, confidence 0.522): How many ill staff on one ward in a week should prompt a review for a cluster?
- **DX-17** (correct answer withheld, confidence 0.437): How much reserve stock of PPE should be kept?
- **DX-20** (VALIDATED BUT WRONG, confidence 0.874): How many steps does shared decision making have?
- **DX-22** (correct answer withheld, confidence 0.492): What should be done with a used tissue?
- **DX-O3** (VALIDATED BUT OUT OF CORPUS, confidence 0.804): What is the incubation period of rabies?
