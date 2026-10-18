# Evaluation summary: real corpus, test split

- Index: `9bc2368dd16cc348…`  |  generator: `llm`  |  threshold: 0.6
- Queries: 16 in-corpus, 3 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 100.0% |
| Precision@5 (document level) | 90.0% |
| Precision@10 (document level) | 81.9% |
| Capped Precision@1 (vs. best attainable) | 100.0% |
| Capped Precision@5 (vs. best attainable) | 90.0% |
| Capped Precision@10 (vs. best attainable) | 81.9% |
| Hit@1 (a chunk containing the expected fact) | 56.2% |
| Hit@5 (a chunk containing the expected fact) | 81.2% |
| Hit@10 (a chunk containing the expected fact) | 81.2% |
| MRR (first fact-bearing chunk) | 0.6427 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 43.8% |
| Mean confidence (in-corpus) | 0.5189 |
| Answer correct (expected facts present) | 68.8% |
| **Validated precision** (correct among validated) | 85.7% |
| **Validated but wrong** | 14.3% |
| Correct but flagged for review | 45.5% |
| Out-of-corpus sent to review | 100.0% |
| Out-of-corpus falsely validated | 0.0% |
| Decision accuracy (all queries) | 68.4% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 75.0% | 91.7% | 8.3% | 0.0% | 0.0% | 94.7% |
| 0.35 | 75.0% | 91.7% | 8.3% | 0.0% | 0.0% | 94.7% |
| 0.4 | 75.0% | 91.7% | 8.3% | 0.0% | 0.0% | 94.7% |
| 0.45 | 62.5% | 90.0% | 10.0% | 18.2% | 0.0% | 84.2% |
| 0.5 | 50.0% | 87.5% | 12.5% | 36.4% | 0.0% | 73.7% |
| 0.55 | 43.8% | 85.7% | 14.3% | 45.5% | 0.0% | 68.4% |
| 0.6 | 43.8% | 85.7% | 14.3% | 45.5% | 0.0% | 68.4% |
| 0.65 | 43.8% | 85.7% | 14.3% | 45.5% | 0.0% | 68.4% |
| 0.7 | 43.8% | 85.7% | 14.3% | 45.5% | 0.0% | 68.4% |
| 0.75 | 37.5% | 100.0% | 0.0% | 45.5% | 0.0% | 73.7% |
| 0.8 | 37.5% | 100.0% | 0.0% | 45.5% | 0.0% | 73.7% |
| 0.85 | 18.8% | 100.0% | 0.0% | 72.7% | 0.0% | 57.9% |
| 0.9 | 18.8% | 100.0% | 0.0% | 72.7% | 0.0% | 57.9% |

## Items for analyst review (10)

- **R02** (VALIDATED BUT WRONG, confidence 0.711): What does cohorting mean?
- **R04** (correct answer withheld, confidence 0.406): Within what distance of the patient has the droplet risk area historically been defined?
- **R06** (flagged: low confidence, confidence 0.0): What should patients wear when they must be moved outside an airborne infection isolation room?
- **R08** (correct answer withheld, confidence 0.446): Do staff transporting a patient on airborne precautions need to wear a mask?
- **T04** (correct answer withheld, confidence 0.522): How long should temperature logs be kept?
- **R19** (flagged: low confidence, confidence 0.0): How long does the full procedure of washing hands with soap and water take?
- **R23** (flagged: low confidence, confidence 0.0): What alcohol concentrations do the WHO-recommended handrub formulations contain?
- **R27** (correct answer withheld, confidence 0.453): Are brushes recommended for surgical hand preparation?
- **R29** (correct answer withheld, confidence 0.479): Does wearing gloves replace the need for hand hygiene?
- **R32** (flagged: low confidence, confidence 0.0): At which moments are health-care workers asked to clean their hands?
