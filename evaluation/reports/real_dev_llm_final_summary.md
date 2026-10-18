# Evaluation summary: real corpus, dev split

- Index: `9bc2368dd16cc348…`  |  generator: `llm`  |  threshold: 0.6
- Queries: 16 in-corpus, 3 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 93.8% |
| Precision@5 (document level) | 85.0% |
| Precision@10 (document level) | 84.4% |
| Capped Precision@1 (vs. best attainable) | 93.8% |
| Capped Precision@5 (vs. best attainable) | 85.0% |
| Capped Precision@10 (vs. best attainable) | 84.4% |
| Hit@1 (a chunk containing the expected fact) | 68.8% |
| Hit@5 (a chunk containing the expected fact) | 81.2% |
| Hit@10 (a chunk containing the expected fact) | 87.5% |
| MRR (first fact-bearing chunk) | 0.7465 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 68.8% |
| Mean confidence (in-corpus) | 0.6779 |
| Answer correct (expected facts present) | 81.2% |
| **Validated precision** (correct among validated) | 100.0% |
| **Validated but wrong** | 0.0% |
| Correct but flagged for review | 15.4% |
| Out-of-corpus sent to review | 100.0% |
| Out-of-corpus falsely validated | 0.0% |
| Decision accuracy (all queries) | 89.5% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 81.2% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.35 | 81.2% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.4 | 81.2% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.45 | 81.2% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.5 | 81.2% | 100.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| 0.55 | 75.0% | 100.0% | 0.0% | 7.7% | 0.0% | 94.7% |
| 0.6 | 68.8% | 100.0% | 0.0% | 15.4% | 0.0% | 89.5% |
| 0.65 | 68.8% | 100.0% | 0.0% | 15.4% | 0.0% | 89.5% |
| 0.7 | 68.8% | 100.0% | 0.0% | 15.4% | 0.0% | 89.5% |
| 0.75 | 62.5% | 100.0% | 0.0% | 23.1% | 0.0% | 84.2% |
| 0.8 | 50.0% | 100.0% | 0.0% | 38.5% | 0.0% | 73.7% |
| 0.85 | 50.0% | 100.0% | 0.0% | 38.5% | 0.0% | 73.7% |
| 0.9 | 43.8% | 100.0% | 0.0% | 46.2% | 0.0% | 68.4% |

## Items for analyst review (5)

- **R07** (correct answer withheld, confidence 0.571): What must a symptomatic visitor do if they are allowed to stay with a patient?
- **R09** (flagged: low confidence, confidence 0.0): Where should patients needing droplet precautions be placed in an outpatient setting?
- **R18** (flagged: low confidence, confidence 0.0): How long should the entire alcohol handrub procedure take?
- **R24** (correct answer withheld, confidence 0.5): What is the minimum sink-to-patient bed ratio according to WHO?
- **R28** (flagged: low confidence, confidence 0.0): What are the five components of the WHO multimodal hand hygiene improvement strategy?
