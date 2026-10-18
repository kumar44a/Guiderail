# Evaluation summary: synthetic corpus, dev split

- Index: `45c3d9422161bc97…`  |  generator: `extractive`  |  threshold: 0.6
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
| Pass rate (validated / in-corpus) | 65.0% |
| Mean confidence (in-corpus) | 0.6743 |
| Answer correct (expected facts present) | 95.0% |
| **Validated precision** (correct among validated) | 92.3% |
| **Validated but wrong** | 7.7% |
| Correct but flagged for review | 36.8% |
| Out-of-corpus sent to review | 80.0% |
| Out-of-corpus falsely validated | 20.0% |
| Decision accuracy (all queries) | 64.0% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 95.0% | 5.0% | 0.0% | 40.0% | 88.0% |
| 0.35 | 100.0% | 95.0% | 5.0% | 0.0% | 40.0% | 88.0% |
| 0.4 | 100.0% | 95.0% | 5.0% | 0.0% | 40.0% | 88.0% |
| 0.45 | 90.0% | 94.4% | 5.6% | 10.5% | 40.0% | 80.0% |
| 0.5 | 80.0% | 93.8% | 6.2% | 21.1% | 20.0% | 76.0% |
| 0.55 | 75.0% | 93.3% | 6.7% | 26.3% | 20.0% | 72.0% |
| 0.6 | 65.0% | 92.3% | 7.7% | 36.8% | 20.0% | 64.0% |
| 0.65 | 45.0% | 88.9% | 11.1% | 57.9% | 20.0% | 48.0% |
| 0.7 | 40.0% | 87.5% | 12.5% | 63.2% | 20.0% | 44.0% |
| 0.75 | 40.0% | 87.5% | 12.5% | 63.2% | 20.0% | 44.0% |
| 0.8 | 30.0% | 83.3% | 16.7% | 73.7% | 20.0% | 36.0% |
| 0.85 | 20.0% | 75.0% | 25.0% | 84.2% | 0.0% | 32.0% |
| 0.9 | 10.0% | 100.0% | 0.0% | 89.5% | 0.0% | 32.0% |

## Items for analyst review (9)

- **S01** (correct answer withheld, confidence 0.437): How long should I rub alcohol-based hand sanitizer on my hands?
- **S05** (correct answer withheld, confidence 0.536): Which infections require soap and water instead of hand rub?
- **S09** (correct answer withheld, confidence 0.59): Can one gown be worn between different patients?
- **S11** (correct answer withheld, confidence 0.462): What bleach strength is used for blood spills?
- **S15** (correct answer withheld, confidence 0.559): By when should staff be offered the flu vaccine?
- **S17** (correct answer withheld, confidence 0.461): How many days after symptoms can staff go back to work?
- **S23** (VALIDATED BUT WRONG, confidence 0.859): What are the steps of shared decision making?
- **S29** (correct answer withheld, confidence 0.402): Which vaccine needs a booster every ten years?
- **S47** (VALIDATED BUT OUT OF CORPUS, confidence 0.837): What is the incubation period of influenza?
