# Evaluation summary: real corpus, sealed3 split

- Index: `9bc2368dd16cc348…`  |  generator: `llm`  |  threshold: 0.6
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
| Pass rate (validated / in-corpus) | 66.0% |
| Mean confidence (in-corpus) | 0.6214 |
| Answer correct (expected facts present) | 70.2% |
| **Validated precision** (correct among validated) | 83.9% |
| **Validated but wrong** | 16.1% |
| Correct but flagged for review | 21.2% |
| Out-of-corpus sent to review | n/a |
| Out-of-corpus falsely validated | n/a |
| Decision accuracy (all queries) | 74.5% |

A high pass rate alone is not evidence of quality: an extractive answer is copied from the evidence, so coverage is near-perfect by construction. Validated precision and the validated-but-wrong rate are the meaningful numbers.

## Threshold sweep

| Threshold | Pass rate | Validated precision | Validated but wrong | Correct but flagged | OOC false accept | Decision accuracy |
|---|---|---|---|---|---|---|
| 0.3 | 83.0% | 84.6% | 15.4% | 0.0% | n/a | 87.2% |
| 0.35 | 83.0% | 84.6% | 15.4% | 0.0% | n/a | 87.2% |
| 0.4 | 83.0% | 84.6% | 15.4% | 0.0% | n/a | 87.2% |
| 0.45 | 83.0% | 84.6% | 15.4% | 0.0% | n/a | 87.2% |
| 0.5 | 80.8% | 84.2% | 15.8% | 3.0% | n/a | 85.1% |
| 0.55 | 70.2% | 84.9% | 15.2% | 15.2% | n/a | 78.7% |
| 0.6 | 66.0% | 83.9% | 16.1% | 21.2% | n/a | 74.5% |
| 0.65 | 61.7% | 82.8% | 17.2% | 27.3% | n/a | 70.2% |
| 0.7 | 55.3% | 84.6% | 15.4% | 33.3% | n/a | 68.1% |
| 0.75 | 42.5% | 85.0% | 15.0% | 48.5% | n/a | 59.6% |
| 0.8 | 38.3% | 83.3% | 16.7% | 54.5% | n/a | 55.3% |
| 0.85 | 23.4% | 90.9% | 9.1% | 69.7% | n/a | 48.9% |
| 0.9 | 12.8% | 83.3% | 16.7% | 84.9% | n/a | 38.3% |

## Items for analyst review (21)

- **I01** (VALIDATED BUT WRONG, confidence 0.913): What are the core components of Standard Precautions that apply to all patients regardless of suspected infection status?
- **I12** (flagged: low confidence, confidence 0.0): What criteria and minimum timeframes are used to determine when transmission-based precautions can be safely discontinued?
- **I14** (VALIDATED BUT WRONG, confidence 0.821): What role does clinical microbiology laboratory support play in routine infection surveillance and outbreak control?
- **I17** (flagged: low confidence, confidence 0.0): What steps must be taken to safely don and doff PPE to prevent self-contamination during patient care?
- **I24** (VALIDATED BUT WRONG, confidence 0.822): What are the consequences of not wearing a face mask while placing a central venous line or performing a myelogram?
- **I25** (correct answer withheld, confidence 0.501): When should visitors displaying active communicable symptoms be excluded from entering inpatient facilities?
- **I26** (flagged: low confidence, confidence 0.0): Why does a single negative surveillance culture fail to justify the removal of Contact Precautions for multi-drug resistant organisms (MDROs)?
- **I28** (correct answer withheld, confidence 0.461): What hazards occur when reusable medical devices are shared between patients without documented intermediate reprocessing?
- **I29** (correct answer withheld, confidence 0.545): Why is the reuse of single-use disposable needles or syringes between different patients considered a major regulatory breach?
- **I31** (flagged: low confidence, confidence 0.0): Why should symptomatic healthcare personnel with acute respiratory illness avoid direct contact with high-risk patients?
- **I32** (VALIDATED BUT WRONG, confidence 0.698): What common procedural failures in ambulatory clinics have repeatedly triggered large outbreaks of Hepatitis B and Hepatitis C?
- **I33** (correct answer withheld, confidence 0.546): Why is a lack of documented fever insufficient evidence to rule out a contagious respiratory infection like pertussis?
- **I34** (correct answer withheld, confidence 0.533): Why is relying on glove use alone without performing pre- and post-glove hand hygiene a violation of infection control standards?
- **I36** (correct answer withheld, confidence 0.554): What is the appropriate protocol for terminally ill patients whose only visiting family members are actively coughing or symptomatic?
- **I40** (flagged: low confidence, confidence 0.0): What PPE is required when dealing with emerging pathogens that transmit via multiple overlapping routes (e.g., SARS-CoV)?
- **I41** (flagged: low confidence, confidence 0.0): How does the management of MDRO colonization differ between acute care hospitals and long-term care facilities (LTCFs)?
- **I43** (flagged: low confidence, confidence 0.505): How should pediatric patients with coughing fits be handled if developmental or clinical factors make wearing a surgical mask impossible?
- **I44** (VALIDATED BUT WRONG, confidence 0.737): Under what circumstances can two patients with the same confirmed infectious pathogen be cohorted in the same isolation room?
- **I45** (flagged: low confidence, confidence 0.0): What protocol governs healthcare personnel with waning acellular pertussis immunity who are exposed during a neonatal unit outbreak?
- **I46** (flagged: low confidence, confidence 0.0): What specific criteria allow a facility to permanently classify a patient as an MDRO carrier versus attempting decolonization?
- **I47** (correct answer withheld, confidence 0.598): What infection control steps are warranted when a patient presents with an undiagnosed febrile rash illness of unknown etiology?
