# Evaluation summary: real corpus, sealed split

- Index: `9bc2368dd16cc348…`  |  generator: `extractive`  |  threshold: 0.6
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
| Pass rate (validated / in-corpus) | 93.8% |
| Mean confidence (in-corpus) | 0.8139 |
| Answer correct (expected facts present) | 50.0% |
| **Validated precision** (correct among validated) | 46.7% |
| **Validated but wrong** | 53.3% |
| Correct but flagged for review | 12.5% |
| Out-of-corpus sent to review | 16.7% |
| Out-of-corpus falsely validated | 83.3% |
| Decision accuracy (all queries) | 36.4% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 50.0% | 50.0% | 0.0% | 100.0% | 36.4% |
| 0.35 | 100.0% | 50.0% | 50.0% | 0.0% | 100.0% | 36.4% |
| 0.4 | 100.0% | 50.0% | 50.0% | 0.0% | 100.0% | 36.4% |
| 0.45 | 100.0% | 50.0% | 50.0% | 0.0% | 100.0% | 36.4% |
| 0.5 | 100.0% | 50.0% | 50.0% | 0.0% | 100.0% | 36.4% |
| 0.55 | 100.0% | 50.0% | 50.0% | 0.0% | 83.3% | 40.9% |
| 0.6 | 93.8% | 46.7% | 53.3% | 12.5% | 83.3% | 36.4% |
| 0.65 | 87.5% | 42.9% | 57.1% | 25.0% | 83.3% | 31.8% |
| 0.7 | 81.2% | 38.5% | 61.5% | 37.5% | 50.0% | 36.4% |
| 0.75 | 81.2% | 38.5% | 61.5% | 37.5% | 50.0% | 36.4% |
| 0.8 | 62.5% | 50.0% | 50.0% | 37.5% | 16.7% | 59.1% |
| 0.85 | 37.5% | 66.7% | 33.3% | 50.0% | 0.0% | 72.7% |
| 0.9 | 18.8% | 33.3% | 66.7% | 87.5% | 0.0% | 59.1% |

## Items for analyst review (14)

- **N34** (VALIDATED BUT WRONG, confidence 0.9): how soon must smallpox vaccine be given after exposure
- **N35** (VALIDATED BUT WRONG, confidence 1.0): what antiseptics are used for hand hygiene
- **N38** (correct answer withheld, confidence 0.596): what do i do if a soap dispenser is partly empty
- **N42** (VALIDATED BUT WRONG, confidence 0.762): can freezing damage vaccines
- **NO4** (VALIDATED BUT OUT OF CORPUS, confidence 0.788): what is the recommended size of a hospital waiting room
- **NO5** (VALIDATED BUT OUT OF CORPUS, confidence 0.838): how do i calibrate a blood pressure monitor
- **U01** (VALIDATED BUT WRONG, confidence 0.776): What are the benefits of hand rub?
- **U02** (VALIDATED BUT WRONG, confidence 0.836): What is the chemical composition / composition of hand rub ?
- **U03** (VALIDATED BUT WRONG, confidence 0.842): Which alcohol is present in hand rub?
- **U04** (VALIDATED BUT WRONG, confidence 0.811): Is hand rub safe to drink ?
- **U06** (VALIDATED BUT OUT OF CORPUS, confidence 0.693): Which is the best hand rub company ?
- **U07** (VALIDATED BUT OUT OF CORPUS, confidence 0.781): Who discovered hand rub and when it was used for the first time.
- **U08** (VALIDATED BUT OUT OF CORPUS, confidence 0.678): Is the hand rub used in hospitals are same as domestic use.
- **U09** (VALIDATED BUT WRONG, confidence 0.798): What are the disadvantages of using hand rub ?
