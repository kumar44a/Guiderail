# evaluation/reports

Everything here is produced by the scripts in `evaluation/` and read by `evaluation/build_summary.py`, which generates `docs/EVALUATION_REPORT.md` and `docs/EVALUATION_LOG.md`.
Nothing in these files is edited by hand.

| Files | What they are |
|---|---|
| `<corpus>_<split>_<generator>_<tag>.json` | one evaluation run: records, retrieval metrics, validation metrics, threshold sweep, review list. `corpus` is `synthetic`, `synthetic2` (the larger v2 corpus) or `real`; `split` is `dev`, `test`, `final` or a `sealed*` set; `tag` names the configuration (see below) |
| `*_cur_summary.md`, `*_cur_low_confidence.csv` | the readable summary and the analyst review list for the shipped configuration (`cur`). Other tags' summaries and CSVs were removed because `run_eval.py` regenerates them |
| `retrieval_round*_*.json`, `validator_round*.json`, `loader_fix_effect.json` | the mechanical verdict of each improvement round, produced by the `judge_*.py` scripts |
| `validator_stress_<tag>.json` | the hand-written good/bad answer stress test for that configuration |
| `*_rules.txt` | the accept/reject rules for each experiment, **committed before the experiment ran**, each with its outcome appended afterwards |
| `test_split_runs.log` | every run that touched a held-out or sealed split, with a timestamp and index hash |
| `rewrite_cache.json` | saved question rewrites so the Claude rewrite runs can be repeated without new API calls |

Tags: `cur` is the shipped configuration; `pre_r8` is `cur` before the document-cohesion change; `r3*` to `r9*` belong to the retrieval and validator rounds named in their rules files; `v2`, `r8final`
and `r8exposed` are the larger-corpus runs; `sealed`, `sealed2`, `sealed3_iso` and `sealed4_storage` are the question sets written by the project owner.
The judge scripts take tags on the command line (for example `python evaluation/judge_round3.py --step r3A --against r3base`), so the tagged JSON files are kept even though they are not mentioned elsewhere.
