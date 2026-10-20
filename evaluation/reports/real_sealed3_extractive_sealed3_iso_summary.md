# Evaluation summary: real corpus, sealed3 split

- Index: `9bc2368dd16cc348…`  |  generator: `extractive`  |  threshold: 0.6
- Queries: 47 in-corpus, 0 out-of-corpus

## Retrieval (in-corpus queries)

| Metric | Value |
|---|---|
| Precision@1 (document level) | 93.6% |
| Precision@5 (document level) | 85.1% |
| Precision@10 (document level) | 82.8% |
| Capped Precision@1 (vs. best attainable) | 93.6% |
| Capped Precision@5 (vs. best attainable) | 85.1% |
| Capped Precision@10 (vs. best attainable) | 82.8% |
| Hit@1 (a chunk containing the expected fact) | 46.8% |
| Hit@5 (a chunk containing the expected fact) | 78.7% |
| Hit@10 (a chunk containing the expected fact) | 85.1% |
| MRR (first fact-bearing chunk) | 0.6002 |

## Answers and validation

| Metric | Value |
|---|---|
| Pass rate (validated / in-corpus) | 83.0% |
| Mean confidence (in-corpus) | 0.7716 |
| Answer correct (expected facts present) | 70.2% |
| **Validated precision** (correct among validated) | 66.7% |
| **Validated but wrong** | 33.3% |
| Correct but flagged for review | 21.2% |
| Out-of-corpus sent to review | n/a |
| Out-of-corpus falsely validated | n/a |
| Decision accuracy (all queries) | 57.5% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 100.0% | 70.2% | 29.8% | 0.0% | n/a | 70.2% |
| 0.35 | 100.0% | 70.2% | 29.8% | 0.0% | n/a | 70.2% |
| 0.4 | 100.0% | 70.2% | 29.8% | 0.0% | n/a | 70.2% |
| 0.45 | 100.0% | 70.2% | 29.8% | 0.0% | n/a | 70.2% |
| 0.5 | 97.9% | 69.6% | 30.4% | 3.0% | n/a | 68.1% |
| 0.55 | 87.2% | 68.3% | 31.7% | 15.2% | n/a | 61.7% |
| 0.6 | 83.0% | 66.7% | 33.3% | 21.2% | n/a | 57.5% |
| 0.65 | 80.8% | 65.8% | 34.2% | 24.2% | n/a | 55.3% |
| 0.7 | 74.5% | 68.6% | 31.4% | 27.3% | n/a | 57.5% |
| 0.75 | 63.8% | 70.0% | 30.0% | 36.4% | n/a | 55.3% |
| 0.8 | 51.1% | 66.7% | 33.3% | 51.5% | n/a | 46.8% |
| 0.85 | 27.7% | 76.9% | 23.1% | 69.7% | n/a | 44.7% |
| 0.9 | 14.9% | 71.4% | 28.6% | 84.9% | n/a | 36.2% |

## Items for analyst review (21)

- **I01** (VALIDATED BUT WRONG, confidence 0.855): What are the core components of Standard Precautions that apply to all patients regardless of suspected infection status?
- **I09** (VALIDATED BUT WRONG, confidence 0.966): What specific environmental controls define a Protective Environment for allogeneic hematopoietic stem cell transplant (HSCT) patients?
- **I12** (VALIDATED BUT WRONG, confidence 0.738): What criteria and minimum timeframes are used to determine when transmission-based precautions can be safely discontinued?
- **I14** (VALIDATED BUT WRONG, confidence 0.841): What role does clinical microbiology laboratory support play in routine infection surveillance and outbreak control?
- **I17** (VALIDATED BUT WRONG, confidence 0.661): What steps must be taken to safely don and doff PPE to prevent self-contamination during patient care?
- **I18** (VALIDATED BUT WRONG, confidence 0.831): Why must used needles and syringes never be reinserted into a multiple-dose vial or saline container?
- **I22** (VALIDATED BUT WRONG, confidence 0.929): Why are dried and fresh flowers or potted plants strictly prohibited in the rooms of HSCT patients?
- **I24** (VALIDATED BUT WRONG, confidence 0.822): What are the consequences of not wearing a face mask while placing a central venous line or performing a myelogram?
- **I25** (correct answer withheld, confidence 0.55): When should visitors displaying active communicable symptoms be excluded from entering inpatient facilities?
- **I26** (VALIDATED BUT WRONG, confidence 0.686): Why does a single negative surveillance culture fail to justify the removal of Contact Precautions for multi-drug resistant organisms (MDROs)?
- **I28** (correct answer withheld, confidence 0.571): What hazards occur when reusable medical devices are shared between patients without documented intermediate reprocessing?
- **I29** (correct answer withheld, confidence 0.545): Why is the reuse of single-use disposable needles or syringes between different patients considered a major regulatory breach?
- **I31** (VALIDATED BUT WRONG, confidence 0.834): Why should symptomatic healthcare personnel with acute respiratory illness avoid direct contact with high-risk patients?
- **I32** (VALIDATED BUT WRONG, confidence 0.733): What common procedural failures in ambulatory clinics have repeatedly triggered large outbreaks of Hepatitis B and Hepatitis C?
- **I33** (correct answer withheld, confidence 0.546): Why is a lack of documented fever insufficient evidence to rule out a contagious respiratory infection like pertussis?
- **I36** (correct answer withheld, confidence 0.535): What is the appropriate protocol for terminally ill patients whose only visiting family members are actively coughing or symptomatic?
- **I40** (VALIDATED BUT WRONG, confidence 0.81): What PPE is required when dealing with emerging pathogens that transmit via multiple overlapping routes (e.g., SARS-CoV)?
- **I43** (correct answer withheld, confidence 0.517): How should pediatric patients with coughing fits be handled if developmental or clinical factors make wearing a surgical mask impossible?
- **I44** (VALIDATED BUT WRONG, confidence 0.766): Under what circumstances can two patients with the same confirmed infectious pathogen be cohorted in the same isolation room?
- **I45** (correct answer withheld, confidence 0.463): What protocol governs healthcare personnel with waning acellular pertussis immunity who are exposed during a neonatal unit outbreak?
- **I46** (flagged: low confidence, confidence 0.528): What specific criteria allow a facility to permanently classify a patient as an MDRO carrier versus attempting decolonization?
