# Evaluation summary: real corpus, sealed split

- Index: `9bc2368dd16cc348…`  |  generator: `llm`  |  threshold: 0.6
- Queries: 16 in-corpus, 6 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 93.8% |
| Precision@5 (document level) | 88.8% |
| Precision@10 (document level) | 85.6% |
| Capped Precision@1 (vs. best attainable) | 93.8% |
| Capped Precision@5 (vs. best attainable) | 88.8% |
| Capped Precision@10 (vs. best attainable) | 85.6% |
| Hit@1 (a chunk containing the expected fact) | 31.2% |
| Hit@5 (a chunk containing the expected fact) | 62.5% |
| Hit@10 (a chunk containing the expected fact) | 75.0% |
| MRR (first fact-bearing chunk) | 0.4273 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 62.5% |
| Mean confidence (in-corpus) | 0.5222 |
| Answer correct (expected facts present) | 56.2% |
| **Validated precision** (correct among validated) | 80.0% |
| **Validated but wrong** | 20.0% |
| Correct but flagged for review | 11.1% |
| Out-of-corpus sent to review | 100.0% |
| Out-of-corpus falsely validated | 0.0% |
| Decision accuracy (all queries) | 86.4% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 68.8% | 81.8% | 18.2% | 0.0% | 0.0% | 90.9% |
| 0.35 | 68.8% | 81.8% | 18.2% | 0.0% | 0.0% | 90.9% |
| 0.4 | 68.8% | 81.8% | 18.2% | 0.0% | 0.0% | 90.9% |
| 0.45 | 68.8% | 81.8% | 18.2% | 0.0% | 0.0% | 90.9% |
| 0.5 | 68.8% | 81.8% | 18.2% | 0.0% | 0.0% | 90.9% |
| 0.55 | 68.8% | 81.8% | 18.2% | 0.0% | 0.0% | 90.9% |
| 0.6 | 62.5% | 80.0% | 20.0% | 11.1% | 0.0% | 86.4% |
| 0.65 | 56.2% | 77.8% | 22.2% | 22.2% | 0.0% | 81.8% |
| 0.7 | 43.8% | 85.7% | 14.3% | 33.3% | 0.0% | 81.8% |
| 0.75 | 31.2% | 100.0% | 0.0% | 44.4% | 0.0% | 81.8% |
| 0.8 | 31.2% | 100.0% | 0.0% | 44.4% | 0.0% | 81.8% |
| 0.85 | 25.0% | 100.0% | 0.0% | 55.6% | 0.0% | 77.3% |
| 0.9 | 6.2% | 100.0% | 0.0% | 88.9% | 0.0% | 63.6% |

## Items for analyst review (8)

- **N31** (flagged: low confidence, confidence 0.0): what room temperature suits the vaccine fridge
- **N38** (correct answer withheld, confidence 0.596): what do i do if a soap dispenser is partly empty
- **N42** (VALIDATED BUT WRONG, confidence 0.722): can freezing damage vaccines
- **U01** (flagged: low confidence, confidence 0.0): What are the benefits of hand rub?
- **U02** (flagged: low confidence, confidence 0.0): What is the chemical composition / composition of hand rub ?
- **U03** (VALIDATED BUT WRONG, confidence 0.672): Which alcohol is present in hand rub?
- **U04** (flagged: low confidence, confidence 0.0): Is hand rub safe to drink ?
- **U09** (flagged: low confidence, confidence 0.0): What are the disadvantages of using hand rub ?
