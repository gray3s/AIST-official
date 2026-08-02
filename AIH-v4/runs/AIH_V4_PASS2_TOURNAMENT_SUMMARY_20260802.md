# AIH v4 Pass2 Tournament Summary - 2026-08-02

## Run Control

- Pass label: `aih_v4_pass2_cloud20_local80_20260802`
- Pass context: pass2 is the organized follow-up to the earlier pass1 token-interruption run from last week.
- Cloud maxply target: 20
- Local maxply base target: 80
- Local/cloud multiplier: 4
- Clue mode: 6
- Memory mode: `stateless`
- Thought mode: `medium`
- Cloud provider tested in tournament run: Gemini
- Models: `gemini:gemini-3.1-flash-lite` as white and black
- Referee: harness rules referee
- Token-interruption objective: preserve live cloud status after each cloud reply and identify whether provider quota feedback is available before starting longer mixed-agent games.
- Ranking objective: rank agents by AIH immunity, meaning the ability to keep playing chess with minimal visible/detectable hallucination. Classical chess win/loss scoring is not used to decide AIH v4 advancement.

## Result

| Game | White | Black | Termination | Plies | Legal moves | Failed turns | Rejected attempts | Elapsed s |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `board_1` | `gemini:gemini-3.1-flash-lite` | `gemini:gemini-3.1-flash-lite` | `draw_by_configured_ply_limit` | 20 | 20 | 0 | 0 | 33.213 |

This pass2 run reached the configured 20-ply cloud boundary without a token,
quota, transport, parser, or illegal-move failure.

## AIH Immunity Tournament Advancement

Tournament levels advance the AIH-immunity winner from each contest into the
next level. The advancing agent is selected by immunity to visible/detectable
hallucination, not by classical chess win/loss scoring. The AIH-immunity winner
is not necessarily the winner under classic chess-tournament considerations.

| Contest | White agent | Black agent | AIH-immunity winner advancing | Termination | Maxply and reason |
| --- | --- | --- | --- | --- | --- |
| `board_1` | `gemini:gemini-3.1-flash-lite` | `gemini:gemini-3.1-flash-lite` | AIH self-test: no advancement distinction | `draw_by_configured_ply_limit` | maxply 20 - draw by configured ply limit |

## AIH Immunity Ranking

Ranking order: higher clean move percentage, lower worst termination severity,
higher total plies before elimination, fewer visible hallucination events, then
fewer rejected/correction attempts.

| Rank | Agent name | Local or cloud | Games | Clean moves | Assigned turns | Clean move % | Visible hallucinations | Worst termination severity | Total plies before elimination | Game maxply and reason |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- |
| 1 | `gemini:gemini-3.1-flash-lite` | cloud | 2 | 20 | 20 | 100.0% | 0 | 0 - clean configured stop (`draw_by_configured_ply_limit`) | 20 | `board_1` white maxply 20 - draw by configured ply limit<br>`board_1` black maxply 20 - draw by configured ply limit |

## Agent Performance Details

| Agent name | Local or cloud | Agent performance | AIH performance | Game maxply and reason | Game result |
| --- | --- | --- | --- | --- | --- |
| `gemini:gemini-3.1-flash-lite` as white | cloud (`google_agentic_cloud`) | 10 legal moves, 0 failed turns, 0 rejected attempts | Completed assigned cloud turns; no token, quota, transport, parser, or illegal-move interruption; no Gemini quota-remaining headers observed | `board_1`: maxply 20 - draw by configured ply limit | draw |
| `gemini:gemini-3.1-flash-lite` as black | cloud (`google_agentic_cloud`) | 10 legal moves, 0 failed turns, 0 rejected attempts | Completed assigned cloud turns; no token, quota, transport, parser, or illegal-move interruption; no Gemini quota-remaining headers observed | `board_1`: maxply 20 - draw by configured ply limit | draw |

Aggregate AIH performance for this pass2 tournament run: Gemini completed 20 total
cloud moves under the 20-ply boundary. The run did not reproduce pass1's
token-interruption failure, but it did confirm that Gemini replies in this path do
not expose a usable percentage of weekly limit remaining in response headers.

## Cloud Limit Probe Consequences

- OpenAI `gpt-4.1-mini` returned request and token remaining percentages.
- OpenAI `gpt-5-nano` completed, but did not return rate-limit headers in the
  observed response.
- Gemini `gemini-3.1-flash-lite` completed, but returned no quota remaining
  headers in the observed response. It did return token usage metadata.
- Anthropic `claude-3-5-haiku` returned `401` with an invalid API key message.
  AIH v4 detected that the configured Anthropic key was rejected by the
  provider. This is classified as a cloud authorization or entitlement failure,
  not as an AIH hallucination or agent performance loss.

The practical consequence is that AIH v4 can currently enforce a percentage
stop-boundary from observed headers for OpenAI `gpt-4.1-mini`, can record
missing headers for Gemini, and should treat Gemini 429 `RESOURCE_EXHAUSTED`
responses as the available stop signal unless a separate Google quota API or
dashboard export is added. Anthropic should remain excluded from daily
AIH-immunity rankings until the rejected key condition is resolved.

## Date-Stamped Artifacts

- Run summary: `aih_v4_pairwise_prototype_20260729/aichess_v4_pairwise_prototype_20260729_20260802_summary.md`
- Run JSONL: `aih_v4_pairwise_prototype_20260729/aichess_v4_pairwise_prototype_20260729_20260802.jsonl`
- Live cloud status Markdown: `aih_v4_pairwise_prototype_20260729/aih_v4_pass2_live_cloud_status_20260802.md`
- Live cloud status JSONL: `aih_v4_pairwise_prototype_20260729/aih_v4_pass2_live_cloud_status_20260802.jsonl`
- Cloud limit probe Markdown: `cloud_agent_limit_probes/cloud_agent_limit_probe_20260802.md`
- Cloud limit probe JSONL: `cloud_agent_limit_probes/cloud_agent_limit_probe_20260802.jsonl`
- Local burn-in summary: `aih_v4_pairwise_prototype_20260729/aichess_v4_pairwise_prototype_20260729_local_burnin_20260802_summary.md`
- Local burn-in JSONL: `aih_v4_pairwise_prototype_20260729/aichess_v4_pairwise_prototype_20260729_local_burnin_20260802.jsonl`
