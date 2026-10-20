# Evaluation summary: real corpus, test split

- Index: `9bc2368dd16cc348…`  |  generator: `extractive`  |  threshold: 0.6
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
| Pass rate (validated / in-corpus) | 95.8% |
| Mean confidence (in-corpus) | 0.8829 |
| Answer correct (expected facts present) | 75.0% |
| **Validated precision** (correct among validated) | 78.3% |
| **Validated but wrong** | 21.7% |
| Correct but flagged for review | 0.0% |
| Out-of-corpus sent to review | 40.0% |
| Out-of-corpus falsely validated | 60.0% |
| Decision accuracy (all queries) | 72.4% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 75.0% | 25.0% | 0.0% | 100.0% | 62.1% |
| 0.35 | 100.0% | 75.0% | 25.0% | 0.0% | 100.0% | 62.1% |
| 0.4 | 100.0% | 75.0% | 25.0% | 0.0% | 80.0% | 65.5% |
| 0.45 | 100.0% | 75.0% | 25.0% | 0.0% | 80.0% | 65.5% |
| 0.5 | 95.8% | 78.3% | 21.7% | 0.0% | 80.0% | 69.0% |
| 0.55 | 95.8% | 78.3% | 21.7% | 0.0% | 60.0% | 72.4% |
| 0.6 | 95.8% | 78.3% | 21.7% | 0.0% | 60.0% | 72.4% |
| 0.65 | 87.5% | 85.7% | 14.3% | 0.0% | 60.0% | 79.3% |
| 0.7 | 87.5% | 85.7% | 14.3% | 0.0% | 20.0% | 86.2% |
| 0.75 | 83.3% | 90.0% | 10.0% | 0.0% | 0.0% | 93.1% |
| 0.8 | 79.2% | 94.7% | 5.3% | 0.0% | 0.0% | 96.5% |
| 0.85 | 75.0% | 94.4% | 5.6% | 5.6% | 0.0% | 93.1% |
| 0.9 | 70.8% | 94.1% | 5.9% | 11.1% | 0.0% | 89.7% |

## Items for analyst review (9)

- **R02** (flagged: low confidence, confidence 0.47): What does cohorting mean?
- **T04** (VALIDATED BUT WRONG, confidence 0.619): How long should temperature logs be kept?
- **RO2** (VALIDATED BUT OUT OF CORPUS, confidence 0.68): How should radioactive waste be disposed of?
- **RO4** (VALIDATED BUT OUT OF CORPUS, confidence 0.675): What is the capital of France?
- **R19** (VALIDATED BUT WRONG, confidence 0.722): How long does the full procedure of washing hands with soap and water take?
- **R23** (VALIDATED BUT WRONG, confidence 1.0): What alcohol concentrations do the WHO-recommended handrub formulations contain?
- **R32** (VALIDATED BUT WRONG, confidence 0.791): At which moments are health-care workers asked to clean their hands?
- **R48** (VALIDATED BUT WRONG, confidence 0.624): What is the typical concentration of chlorhexidine used for hand antisepsis?
- **RO9** (VALIDATED BUT OUT OF CORPUS, confidence 0.749): What is the recommended HEPA filter replacement schedule for an airborne infection isolation room?
