# AIH v4 AIST Official Package - 2026-08-03

This folder is the AIH v4 package location under the AIST Official repo.

Representative zip:

- `../aih-v4_20260803.zip`

Primary package files:

- AIH v4 README: `AIH-v4/README.md`
- Package README: `AIH-v4/README_AIST_PACKAGE_20260803.md`
- Current AIH v4 zip: `aih-v4_20260803.zip`
- Run instructions: `AIH-v4/RUN_AIH_V4_BINARY_LAUNCH_INSTRUCTIONS_20260803.md`
- Project-development plan: `AIH-v4/AIH_V4_PROJECT_DEVELOPMENT_PLAN_20260803.md`
- Latest archived run evidence: `AIH-v4/data/aichess_v4_pairwise_prototype_20260729_20260803_192609.*`

## Current Evidence Status

The `20260803_192609` HTML report is not a valid ranking. It is archived as
evidence of a report/run defect.

Visible defect:

- Top-ranked rows show `AgntOH% = 100.000`.
- The source summary rows are `Cmplt no`.
- The source summary includes `fail.stp` and `fail.qta`.

## Required Next Work

Implement a coherent run-mode procedure. `--boards N` must remain the number of
board assignments. For now, `parallel` may remain the default, but the binary
must expose and record `--run-mode parallel|serial`; serial mode will be brought
along behind parallel mode.

Benchmark restarts must unload resident agents, treat old loads as possibly
stale or corrupt, clear questionable artifacts, and run pre-match agent health
checks before official board matches.

## Local GitHub Workflow

From the AIST Official repo:

```bash
cd /home/sag/RPA2/myLLC/AIST-official
git status --short
git add README.md AIH-v4 aih-v4_20260803.zip
git commit -m "Update AIH v4 package for 2026-08-03"
git push origin main
```
