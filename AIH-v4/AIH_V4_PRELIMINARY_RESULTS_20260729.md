# AIH v4 preliminary results - 2026-07-29

These are preliminary release-mode data points from the current v4 prototype.
They are not final AIH rankings. The local default maxply has been raised
and the local/cloud maxply multiplier range is 2x to 4x.

Rendered HTML results:
https://htmlpreview.github.io/?https://github.com/gray3s/brilliance/blob/main/aih/aichess/v4/AIH_V4_PRELIMINARY_RESULTS_20260729.html

## Current default run controls

- Local retry/expand/default local maxply: 50
- Cloud provider-key default maxply: 10, derived from local maxply / ratio
- Local maxply cap: 50
- Cloud maxply cap: 10
- Default local/cloud maxply multiplier: 4x
- Allowed local/cloud maxply multiplier range: 2x to 4x
- CLI controls: `--local-maxplys=N`, `--local-cloud-maxply-ratio=N`

## Latest binary-published summary

Source summary: `runs/aih_v4_pairwise_prototype_20260729/aichess_v4_pairwise_prototype_20260729_20260803_174442_summary.md`

Rendered HTML:
`data/aichess_v4_pairwise_prototype_20260729_20260803_174442.html`

| Model | Mode | Result | Termination | Complete | Plies | Legal | Failed | Irrelevant | Rejected | Seconds |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| gmn-3.5-flash-lite v granite4:3b | ahg | fail.stp | b.fto | no | 1 | 1 | 0 | 0 | 0 | 61.051 |
| gmn-3.5-flash-lite v qwen2.5-coder:3b | ahg | fail.stp | b.fto | no | 1 | 1 | 0 | 0 | 0 | 61.049 |
| gmn-3.5-flash-lite v qwen2.5:0.5b | ahg | fail.stp | b.fto | no | 1 | 1 | 0 | 0 | 0 | 61.414 |
| gmn-3.5-flash-lite v qwen2.5 | ahg | fail.stp | b.fto | no | 1 | 1 | 0 | 0 | 0 | 61.052 |
| gmn-3.5-flash-lite v qwen:4b | ahg | fail.stp | b.fto | no | 1 | 1 | 0 | 0 | 0 | 61.434 |
| gmn-3.5-flash-lite v smollm2:135m | ahg | fail.stp | b.fto | no | 1 | 1 | 0 | 0 | 0 | 61.412 |
| gmn-3.5-flash-lite v gemma3:270m | ahg | fail.stp | b.fto | no | 1 | 1 | 0 | 0 | 0 | 61.206 |
| gmn-3.5-flash-lite v llama3.2:1b | ahg | fail.stp | b.fto | no | 1 | 1 | 0 | 0 | 0 | 61.046 |
| gmn-3.5-flash-lite v gemma3:1b | ahg | fail.stp | b.fto | no | 1 | 1 | 0 | 0 | 0 | 61.280 |
| gmn-3.5-flash-lite v tinyllama | ahg | fail.stp | b.fto | no | 1 | 1 | 0 | 0 | 0 | 61.200 |
| gmn-3.5-flash-lite v phi3:mini | ahg | fail.stp | b.fto | no | 1 | 1 | 0 | 0 | 0 | 61.278 |
| gmn-3.5-flash-lite v mistral | ahg | fail.stp | b.fto | no | 1 | 1 | 0 | 0 | 0 | 61.209 |
| gmn-3.5-flash-lite v llama3.2:3b | ahg | fail.stp | b.fto | no | 1 | 1 | 0 | 0 | 0 | 61.241 |
| gmn-3.5-flash-lite v gemma3:4b | ahg | fail.stp | b.fto | no | 1 | 1 | 0 | 0 | 0 | 61.210 |

## Preliminary interpretation

The latest preliminary table is generated from the newest successful
`bin/aih_v4 --cloud-representative-gemini` run. Compact row values are display
codes only; the JSONL keeps full field names and values.
