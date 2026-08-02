# AIH v4

AIH v4 is the current AIST Official package for testing agentic AI behavior in
a controlled chess competition harness.

Representative package zip:

- [aih-v4_20260802.zip](../aih-v4_20260802.zip)

This folder is the dedicated AIH v4 package location under AIST Official. The
zip above is the date-only representative package for 2026-08-02.

## Current Focus

AIH v4 is being prepared to move beyond a simple present/absent hallucination
signal. The package should preserve enough evidence to explain what happened,
how it happened, and why the harness classified the behavior the way it did.

The current work items are:

- Add more local AI stack candidates to the discovery surface.
- Keep provider-key loading and unloading outside competition runs.
- Use key strings already exported in the shell that starts the competition.
- Generate date-stamped result artifacts after successful runs, including EPS.
- Record richer AIH behavior data: role assignment, stack type, invalid parses,
  illegal moves, rejected attempts, transport failures, timing, and failure
  classes.

## LinkedIn Context

The current public discussion is tracked in these LinkedIn posts:

- The disaster that is AI hallucination:
  https://www.linkedin.com/posts/samuel-a-gray-iii-1667b238b_20260802-1200mt-the-disaster-that-is-ai-hallucination-activity-7489745809434087424-y-i4
- AIH v4 to agentic AI suggestions:
  https://www.linkedin.com/posts/samuel-a-gray-iii-1667b238b_20260801-1630mt-the-great-agentic-ai-chess-activity-7489452788897218560-oSV-

Formatted local notes are in
[linkedin/AIH_V4_LINKEDIN_NOTES_20260802.md](linkedin/AIH_V4_LINKEDIN_NOTES_20260802.md).

GitHub links for updating the two LinkedIn posts are in
[linkedin/LI_UPDATE_LINKS_20260802.md](linkedin/LI_UPDATE_LINKS_20260802.md).

## Package Files

- [AIH_V4_PROJECT_GOALS_20260802.md](AIH_V4_PROJECT_GOALS_20260802.md)
- [README_AIST_PACKAGE_20260802.md](README_AIST_PACKAGE_20260802.md)
- [published_results/](published_results/)
- [tools/](tools/)
- [runs/](runs/)

The runner in this package does not auto-commit or auto-push. GitHub
publication is an explicit repo operation from the AIST Official repository.

## Publish From AIST Official

```bash
cd /home/sag/RPA2/myLLC/AIST-official
git status --short
git add README.md AIH-v4 aih-v4_20260802.zip
git commit -m "Add AIH v4 representative package for 2026-08-02"
git push origin main
```
