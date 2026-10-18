# Evaluation summary: real corpus, dev split

- Index: `9bc2368dd16cc348…`  |  generator: `llm`  |  threshold: 0.6
- Queries: 24 in-corpus, 5 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 95.8% |
| Precision@5 (document level) | 86.7% |
| Precision@10 (document level) | 82.9% |
| Capped Precision@1 (vs. best attainable) | 95.8% |
| Capped Precision@5 (vs. best attainable) | 86.7% |
| Capped Precision@10 (vs. best attainable) | 82.9% |
| Hit@1 (a chunk containing the expected fact) | 70.8% |
| Hit@5 (a chunk containing the expected fact) | 87.5% |
| Hit@10 (a chunk containing the expected fact) | 91.7% |
| MRR (first fact-bearing chunk) | 0.7789 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 58.3% |
| Mean confidence (in-corpus) | 0.6579 |
| Answer correct (expected facts present) | 83.3% |
| **Validated precision** (correct among validated) | 92.9% |
| **Validated but wrong** | 7.1% |
| Correct but flagged for review | 35.0% |
| Out-of-corpus sent to review | 100.0% |
| Out-of-corpus falsely validated | 0.0% |
| Decision accuracy (all queries) | 72.4% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 87.5% | 95.2% | 4.8% | 0.0% | 0.0% | 96.5% |
| 0.35 | 87.5% | 95.2% | 4.8% | 0.0% | 0.0% | 96.5% |
| 0.4 | 83.3% | 95.0% | 5.0% | 5.0% | 0.0% | 93.1% |
| 0.45 | 83.3% | 95.0% | 5.0% | 5.0% | 0.0% | 93.1% |
| 0.5 | 66.7% | 93.8% | 6.2% | 25.0% | 0.0% | 79.3% |
| 0.55 | 62.5% | 93.3% | 6.7% | 30.0% | 0.0% | 75.9% |
| 0.6 | 58.3% | 92.9% | 7.1% | 35.0% | 0.0% | 72.4% |
| 0.65 | 58.3% | 92.9% | 7.1% | 35.0% | 0.0% | 72.4% |
| 0.7 | 58.3% | 92.9% | 7.1% | 35.0% | 0.0% | 72.4% |
| 0.75 | 45.8% | 90.9% | 9.1% | 50.0% | 0.0% | 62.1% |
| 0.8 | 45.8% | 90.9% | 9.1% | 50.0% | 0.0% | 62.1% |
| 0.85 | 41.7% | 90.0% | 10.0% | 55.0% | 0.0% | 58.6% |
| 0.9 | 37.5% | 88.9% | 11.1% | 60.0% | 0.0% | 55.2% |

## Items for analyst review (11)

- **R07** (correct answer withheld, confidence 0.571): What must a symptomatic visitor do if they are allowed to stay with a patient?
- **R09** (flagged: low confidence, confidence 0.0): Where should patients needing droplet precautions be placed in an outpatient setting?
- **T05** (correct answer withheld, confidence 0.369): What label should be put on vaccines after a temperature excursion?
- **R18** (flagged: low confidence, confidence 0.0): How long should the entire alcohol handrub procedure take?
- **R24** (correct answer withheld, confidence 0.5): What is the minimum sink-to-patient bed ratio according to WHO?
- **R28** (flagged: low confidence, confidence 0.0): What are the five components of the WHO multimodal hand hygiene improvement strategy?
- **R33** (correct answer withheld, confidence 0.474): Are water bottles recommended for use with most pharmaceutical-grade and purpose-built vaccine storage units?
- **R34** (correct answer withheld, confidence 0.49): Can vaccines be stored in the freezer compartment of a household-grade combination refrigerator/freezer unit?
- **R35** (correct answer withheld, confidence 0.486): Should soap and alcohol-based handrub be used concomitantly?
- **R36** (VALIDATED BUT WRONG, confidence 0.924): Should hot water be used for handwashing in health care?
- **R37** (correct answer withheld, confidence 0.474): Is the use of antimicrobial soap recommended when alcohol-based handrub is available for hand antisepsis?
