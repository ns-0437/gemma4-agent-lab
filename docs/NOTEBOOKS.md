# Evaluation generators

| Generator | Purpose | Inputs |
|---|---|---|
| make_pilot_notebook.py | Guarded thinking A/B pilot | Frozen A/B, local tasks and repaired control evidence |
| make_eval_notebook.py | Earlier smoke/paired evaluation workflow | Local releases and competition data |
| make_provenance_notebook.py | Import provenance controls | Competition data in Kaggle |
| make_validation_notebook.py | Baseline/gold validation controls | Competition data in Kaggle |
| report_cell.py | Recover reports from saved artifacts | Local run directory |

The pilot is the current launch path. Older generators preserve research work and are not
an instruction to launch every notebook. See EXPERIMENTS.md before any real execution.
Generated notebooks remain ignored, including encoded content and outputs.
