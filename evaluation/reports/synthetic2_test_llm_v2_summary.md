# Evaluation summary: synthetic2 corpus, test split

- Index: `ffe20683ee85c731…`  |  generator: `llm`  |  threshold: 0.6
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
| Pass rate (validated / in-corpus) | 85.0% |
| Mean confidence (in-corpus) | 0.776 |
| Answer correct (expected facts present) | 100.0% |
| **Validated precision** (correct among validated) | 100.0% |
| **Validated but wrong** | 0.0% |
| Correct but flagged for review | 15.0% |
| Out-of-corpus sent to review | 100.0% |
| Out-of-corpus falsely validated | 0.0% |
| Decision accuracy (all queries) | 88.0% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.35 | 95.0% | 100.0% | 0.0% | 5.0% | 0.0% | 96.0% |
| 0.4 | 95.0% | 100.0% | 0.0% | 5.0% | 0.0% | 96.0% |
| 0.45 | 95.0% | 100.0% | 0.0% | 5.0% | 0.0% | 96.0% |
| 0.5 | 95.0% | 100.0% | 0.0% | 5.0% | 0.0% | 96.0% |
| 0.55 | 90.0% | 100.0% | 0.0% | 10.0% | 0.0% | 92.0% |
| 0.6 | 85.0% | 100.0% | 0.0% | 15.0% | 0.0% | 88.0% |
| 0.65 | 85.0% | 100.0% | 0.0% | 15.0% | 0.0% | 88.0% |
| 0.7 | 70.0% | 100.0% | 0.0% | 30.0% | 0.0% | 76.0% |
| 0.75 | 55.0% | 100.0% | 0.0% | 45.0% | 0.0% | 64.0% |
| 0.8 | 50.0% | 100.0% | 0.0% | 50.0% | 0.0% | 60.0% |
| 0.85 | 45.0% | 100.0% | 0.0% | 55.0% | 0.0% | 56.0% |
| 0.9 | 25.0% | 100.0% | 0.0% | 75.0% | 0.0% | 40.0% |

## Items for analyst review (3)

- **T2-01** (correct answer withheld, confidence 0.345): How many minutes must a blood spill sit under the bleach solution before it is wiped up?
- **T2-03** (correct answer withheld, confidence 0.564): When should antiretroviral prophylaxis start after a needlestick from an HIV-positive patient?
- **T2-16** (correct answer withheld, confidence 0.546): What strength of bleach solution is used for routine disinfection?
