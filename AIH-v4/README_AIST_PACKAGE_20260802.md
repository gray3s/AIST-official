# AIH v4 AIST Official Package - 2026-08-02

This folder is the dedicated AIH v4 package location under the AIST Official repo.

Representative zip for today:

- `../aih-v4_20260802.zip`

Primary package files:

- AIH v4 README: `AIH-v4/README.md`
- Package README: `AIH-v4/README_AIST_PACKAGE_20260802.md`
- Current AIH v4 zip: `aih-v4_20260802.zip`
- Current AIH v4 goals update: `AIH-v4/AIH_V4_PROJECT_GOALS_20260802.md`
- Current EPS run analysis: `AIH-v4/published_results/aichess_v4_pairwise_prototype_20260729_20260729_161901_analysis_20260802.eps`
- LinkedIn notes and formatted links: `AIH-v4/linkedin/AIH_V4_LINKEDIN_NOTES_20260802.md`
- LinkedIn update links: `AIH-v4/linkedin/LI_UPDATE_LINKS_20260802.md`

LinkedIn references:

- The disaster that is AI hallucination: https://www.linkedin.com/posts/samuel-a-gray-iii-1667b238b_20260802-1200mt-the-disaster-that-is-ai-hallucination-activity-7489745809434087424-y-i4
- AIH v4 to agentic AI suggestions: https://www.linkedin.com/posts/samuel-a-gray-iii-1667b238b_20260801-1630mt-the-great-agentic-ai-chess-activity-7489452788897218560-oSV-

The runner in this package does not auto-commit or auto-push. GitHub publication is an explicit repo operation from `/home/sag/RPA2/myLLC/AIST-official`.

## Local GitHub Workflow

From the AIST Official repo:

```bash
cd /home/sag/RPA2/myLLC/AIST-official
git status --short
git add README.md AIH-v4 aih-v4_20260802.zip
git commit -m "Add AIH v4 representative package for 2026-08-02"
git push origin main
```

If the remote AIST Official GitHub repo does not exist yet, create it first:

```bash
cd /home/sag/RPA2/myLLC/AIST-official
gh repo create AIST-official --private --source=. --remote=origin --push
```

If the repo already exists but `origin` is missing, add the correct remote URL first:

```bash
cd /home/sag/RPA2/myLLC/AIST-official
git remote add origin GITHUB_REMOTE_URL
git push -u origin HEAD
```
