# Evaluation summary: real corpus, test split

- Index: `9bc2368dd16cc348…`  |  generator: `llm`  |  threshold: 0.6
- Queries: 24 in-corpus, 5 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 95.8% |
| Precision@5 (document level) | 90.8% |
| Precision@10 (document level) | 85.4% |
| Capped Precision@1 (vs. best attainable) | 95.8% |
| Capped Precision@5 (vs. best attainable) | 90.8% |
| Capped Precision@10 (vs. best attainable) | 85.4% |
| Hit@1 (a chunk containing the expected fact) | 62.5% |
| Hit@5 (a chunk containing the expected fact) | 83.3% |
| Hit@10 (a chunk containing the expected fact) | 91.7% |
| MRR (first fact-bearing chunk) | 0.7105 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 75.0% |
| Mean confidence (in-corpus) | 0.6938 |
| Answer correct (expected facts present) | 75.0% |
| **Validated precision** (correct among validated) | 94.4% |
| **Validated but wrong** | 5.6% |
| Correct but flagged for review | 5.6% |
| Out-of-corpus sent to review | 100.0% |
| Out-of-corpus falsely validated | 0.0% |
| Decision accuracy (all queries) | 93.1% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 79.2% | 94.7% | 5.3% | 0.0% | 0.0% | 96.5% |
| 0.35 | 79.2% | 94.7% | 5.3% | 0.0% | 0.0% | 96.5% |
| 0.4 | 79.2% | 94.7% | 5.3% | 0.0% | 0.0% | 96.5% |
| 0.45 | 79.2% | 94.7% | 5.3% | 0.0% | 0.0% | 96.5% |
| 0.5 | 79.2% | 94.7% | 5.3% | 0.0% | 0.0% | 96.5% |
| 0.55 | 75.0% | 94.4% | 5.6% | 5.6% | 0.0% | 93.1% |
| 0.6 | 75.0% | 94.4% | 5.6% | 5.6% | 0.0% | 93.1% |
| 0.65 | 75.0% | 94.4% | 5.6% | 5.6% | 0.0% | 93.1% |
| 0.7 | 70.8% | 100.0% | 0.0% | 5.6% | 0.0% | 96.5% |
| 0.75 | 66.7% | 100.0% | 0.0% | 11.1% | 0.0% | 93.1% |
| 0.8 | 66.7% | 100.0% | 0.0% | 11.1% | 0.0% | 93.1% |
| 0.85 | 58.3% | 100.0% | 0.0% | 22.2% | 0.0% | 86.2% |
| 0.9 | 50.0% | 100.0% | 0.0% | 33.3% | 0.0% | 79.3% |

## Items for analyst review (7)

- **R02** (VALIDATED BUT WRONG, confidence 0.683): What does cohorting mean?
- **R06** (flagged: low confidence, confidence 0.0): What should patients wear when they must be moved outside an airborne infection isolation room?
- **T04** (correct answer withheld, confidence 0.522): How long should temperature logs be kept?
- **R19** (flagged: low confidence, confidence 0.0): How long does the full procedure of washing hands with soap and water take?
- **R23** (flagged: low confidence, confidence 0.0): What alcohol concentrations do the WHO-recommended handrub formulations contain?
- **R32** (flagged: low confidence, confidence 0.0): At which moments are health-care workers asked to clean their hands?
- **R48** (flagged: low confidence, confidence 0.0): What is the typical concentration of chlorhexidine used for hand antisepsis?
