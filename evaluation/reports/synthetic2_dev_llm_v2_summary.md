# Evaluation summary: synthetic2 corpus, dev split

- Index: `ffe20683ee85c731…`  |  generator: `llm`  |  threshold: 0.6
- Queries: 20 in-corpus, 5 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 95.0% |
| Precision@5 (document level) | 68.0% |
| Precision@10 (document level) | 51.0% |
| Capped Precision@1 (vs. best attainable) | 95.0% |
| Capped Precision@5 (vs. best attainable) | 72.0% |
| Capped Precision@10 (vs. best attainable) | 68.3% |
| Hit@1 (a chunk containing the expected fact) | 60.0% |
| Hit@5 (a chunk containing the expected fact) | 95.0% |
| Hit@10 (a chunk containing the expected fact) | 100.0% |
| MRR (first fact-bearing chunk) | 0.7571 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 90.0% |
| Mean confidence (in-corpus) | 0.7427 |
| Answer correct (expected facts present) | 95.0% |
| **Validated precision** (correct among validated) | 100.0% |
| **Validated but wrong** | 0.0% |
| Correct but flagged for review | 5.3% |
| Out-of-corpus sent to review | 100.0% |
| Out-of-corpus falsely validated | 0.0% |
| Decision accuracy (all queries) | 96.0% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 95.0% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.35 | 95.0% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.4 | 95.0% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.45 | 95.0% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.5 | 95.0% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.55 | 95.0% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.6 | 90.0% | 100.0% | 0.0% | 5.3% | 0.0% | 96.0% |
| 0.65 | 80.0% | 100.0% | 0.0% | 15.8% | 0.0% | 88.0% |
| 0.7 | 65.0% | 100.0% | 0.0% | 31.6% | 0.0% | 76.0% |
| 0.75 | 60.0% | 100.0% | 0.0% | 36.8% | 0.0% | 72.0% |
| 0.8 | 45.0% | 100.0% | 0.0% | 52.6% | 0.0% | 60.0% |
| 0.85 | 35.0% | 100.0% | 0.0% | 63.2% | 0.0% | 52.0% |
| 0.9 | 10.0% | 100.0% | 0.0% | 89.5% | 0.0% | 32.0% |

## Items for analyst review (2)

- **S15** (flagged: low confidence, confidence 0.0): By when should staff be offered the flu vaccine?
- **S27** (correct answer withheld, confidence 0.587): How long are vaccine temperature logs retained?
