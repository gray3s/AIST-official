# AIH v4 Project Goals Update - 2026-08-02

Source intake: `/home/sag/RPA2/incoming/localAIstack/incoming/AIHv4-updates-202060802.txt`

The 2026-08-02 work target is to prepare AIH v4 for lift-off as a representative package for today's state, not as a final ranking claim.

## Active Updates

1. Add more local stack candidates to the v4 discovery surface.
2. Keep provider-key loading and unloading outside the competition runner. A competition run should consume key strings already exported in the shell that starts the run.
3. Generate timestamped result artifacts after successful competition runs, including EPS output for portable publication.
4. Expand AIH tracking beyond present/absent behavior by preserving what happened, how it happened, and why the harness classified the result that way.

## Implementation Notes

- `tools/discover_local_stack_candidates.sh` is the current discovery entry point for local runtimes and caches.
- `aih_v4.sh` preflights required provider keys without printing key material, but does not load key files.
- Google/Gemini key aliasing from `GOOGLE_API_KEY` or `GOOGLE_GENAI_API_KEY` into `GEMINI_API_KEY` is now an explicit compatibility mode via `AIH_V4_ALLOW_KEY_ALIASING=1`.
- `tools/generate_run_artifacts.py` reads the latest JSONL run output and writes date-stamped Markdown and EPS analysis files into `published_results/`.
- JSONL remains the source of record for detailed AIH behavior, including stack type, role assignment, failure class, rejected attempts, invalid parses, illegal moves, transport failures, timing, and board-awareness probe counts.
