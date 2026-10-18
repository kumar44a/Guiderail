# Evaluation summary: synthetic corpus, dev split

- Index: `45c3d9422161bc97…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 20 in-corpus, 5 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 85.0% |
| Precision@5 (document level) | 48.0% |
| Precision@10 (document level) | 28.5% |
| Capped Precision@1 (vs. best attainable) | 85.0% |
| Capped Precision@5 (vs. best attainable) | 65.7% |
| Capped Precision@10 (vs. best attainable) | 75.1% |
| Hit@1 (a chunk containing the expected fact) | 55.0% |
| Hit@5 (a chunk containing the expected fact) | 85.0% |
| Hit@10 (a chunk containing the expected fact) | 100.0% |
| MRR (first fact-bearing chunk) | 0.6901 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 95.0% |
| Mean confidence (in-corpus) | 0.7824 |
| Answer correct (expected facts present) | 75.0% |
| **Validated precision** (correct among validated) | 79.0% |
| **Validated but wrong** | 21.1% |
| Correct but flagged for review | 0.0% |
| Out-of-corpus sent to review | 60.0% |
| Out-of-corpus falsely validated | 40.0% |
| Decision accuracy (all queries) | 76.0% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 75.0% | 25.0% | 0.0% | 60.0% | 68.0% |
| 0.35 | 100.0% | 75.0% | 25.0% | 0.0% | 60.0% | 68.0% |
| 0.4 | 100.0% | 75.0% | 25.0% | 0.0% | 60.0% | 68.0% |
| 0.45 | 100.0% | 75.0% | 25.0% | 0.0% | 60.0% | 68.0% |
| 0.5 | 100.0% | 75.0% | 25.0% | 0.0% | 60.0% | 68.0% |
| 0.55 | 100.0% | 75.0% | 25.0% | 0.0% | 40.0% | 72.0% |
| 0.6 | 95.0% | 79.0% | 21.1% | 0.0% | 40.0% | 76.0% |
| 0.65 | 85.0% | 82.3% | 17.6% | 6.7% | 40.0% | 76.0% |
| 0.7 | 75.0% | 80.0% | 20.0% | 20.0% | 40.0% | 68.0% |
| 0.75 | 70.0% | 78.6% | 21.4% | 26.7% | 20.0% | 68.0% |
| 0.8 | 45.0% | 66.7% | 33.3% | 60.0% | 20.0% | 48.0% |
| 0.85 | 25.0% | 80.0% | 20.0% | 73.3% | 0.0% | 52.0% |
| 0.9 | 10.0% | 50.0% | 50.0% | 93.3% | 0.0% | 40.0% |

## Items for analyst review (7)

- **S03** (VALIDATED BUT WRONG, confidence 0.833): At what moments should healthcare workers clean their hands during patient care?
- **S11** (flagged: low confidence, confidence 0.568): What bleach strength is used for blood spills?
- **S15** (VALIDATED BUT WRONG, confidence 0.605): By when should staff be offered the flu vaccine?
- **S23** (VALIDATED BUT WRONG, confidence 1.0): What are the steps of shared decision making?
- **S39** (VALIDATED BUT WRONG, confidence 0.846): At what temperature should soiled linen be washed?
- **S45** (VALIDATED BUT OUT OF CORPUS, confidence 0.745): How should radioactive waste be disposed of?
- **S47** (VALIDATED BUT OUT OF CORPUS, confidence 0.837): What is the incubation period of influenza?
