# AIH v4 Pass2 Tournament Summary - 2026-08-02 14:30 MT

## Run Control

- Pass label: `aih_v4_pass2_cloud20_local80_20260802`
- Cloud maxply target: 20
- Local maxply base target: 80
- Local/cloud multiplier: 4
- Cloud provider tested in tournament run: Gemini
- Models: `gemini:gemini-3.1-flash-lite` as white and black
- Referee: harness rules referee

## Result

| Model | Termination | Plies | Legal moves | Failed turns | Rejected attempts | Elapsed s |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `gemini:gemini-3.1-flash-lite` vs `gemini:gemini-3.1-flash-lite` | `draw_by_configured_ply_limit` | 20 | 20 | 0 | 0 | 33.213 |

This pass2 run reached the configured 20-ply cloud boundary without a token,
quota, transport, parser, or illegal-move failure.

## Cloud Limit Probe Consequences

- OpenAI `gpt-4.1-mini` returned request and token remaining percentages.
- OpenAI `gpt-5-nano` completed, but did not return rate-limit headers in the
  observed response.
- Gemini `gemini-3.1-flash-lite` completed, but returned no quota remaining
  headers in the observed response. It did return token usage metadata.
- Anthropic `claude-3-5-haiku` returned `401` with an invalid API key message.

The practical consequence is that AIH v4 can currently enforce a percentage
stop-boundary from observed headers for OpenAI `gpt-4.1-mini`, can record
missing headers for Gemini, and should treat Gemini 429 `RESOURCE_EXHAUSTED`
responses as the available stop signal unless a separate Google quota API or
dashboard export is added.

## Timestamped Artifacts

- Run summary: `aih_v4_pairwise_prototype_20260729/aichess_v4_pairwise_prototype_20260729_20260802_summary.md`
- Run JSONL: `aih_v4_pairwise_prototype_20260729/aichess_v4_pairwise_prototype_20260729_20260802.jsonl`
- Live cloud status Markdown: `aih_v4_pairwise_prototype_20260729/aih_v4_pass2_live_cloud_status_20260802.md`
- Live cloud status JSONL: `aih_v4_pairwise_prototype_20260729/aih_v4_pass2_live_cloud_status_20260802.jsonl`
- Cloud limit probe Markdown: `cloud_agent_limit_probes/cloud_agent_limit_probe_20260802.md`
- Cloud limit probe JSONL: `cloud_agent_limit_probes/cloud_agent_limit_probe_20260802.jsonl`
