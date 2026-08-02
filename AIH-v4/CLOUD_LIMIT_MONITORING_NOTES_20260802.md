# AIH v4 Cloud Limit Monitoring Notes - 2026-08-02

Goal: run longer AIH v4 cloud/local tests without losing the whole tournament
when a provider key hits a quota, spend, or rate-limit boundary.

## What Can Be Parsed

- OpenAI Responses API responses expose rate-limit headers such as
  `x-ratelimit-limit-requests`, `x-ratelimit-remaining-requests`,
  `x-ratelimit-limit-tokens`, `x-ratelimit-remaining-tokens`, and reset fields.
- Anthropic Messages API responses expose `anthropic-ratelimit-*` headers,
  including request and token limit/remaining/reset fields.
- Gemini API documents RPM, TPM, RPD, and spend-based limits, but does not
  currently document a direct "weekly limit remaining percent" response header.
  AIH v4 should record any `x-goog-*`, `retry-after`, and error body details
  actually returned by the API and treat 429 `RESOURCE_EXHAUSTED` as a
  provider stop signal.

## Non-Game Probe

Use this probe before starting a long tournament:

```bash
cd /home/sag/RPA2/myLLC/AIST-official/AIH-v4
./tools/probe_cloud_agent_limits.py --dry-run
./tools/probe_cloud_agent_limits.py
```

Override the cloud-agent list:

```bash
AIH_V4_CLOUD_PROBE_AGENTS='gemini:gemini-3.1-flash-lite,openai:gpt-5-nano,anthropic:claude-3-5-haiku' \
  ./tools/probe_cloud_agent_limits.py
```

The probe does not start a chess game. It sends a minimal one-token response
request to each cloud provider and writes JSONL plus Markdown into:

`runs/cloud_agent_limit_probes/`

## Observed 2026-08-02

The non-game probe produced these provider-allocation observations without
starting a chess game:

| Cloud agent | Probe result | Remaining-limit visibility |
| --- | --- | --- |
| `openai:gpt-4.1-mini` | HTTP 200 | Usable request and token remaining percentages were observed from rate-limit headers. |
| `openai:gpt-5-nano` | HTTP 200 | The request completed, but no usable remaining-limit headers were observed in that response. |
| `gemini:gemini-3.1-flash-lite` | HTTP 200 | The request completed and returned token usage metadata, but no weekly-limit remaining percentage or usable quota-remaining header was observed. |
| `anthropic:claude-3-5-haiku` | HTTP 401 | The configured key failed authorization, so no remaining-limit status could be measured. |

The Anthropic result means a key value was present and sent, but the provider
rejected it as invalid. AIH v4 should record this as
`cloud_authorization_or_entitlement_failure` and exclude that Anthropic agent
from the daily AIH-immunity ranking until the key or entitlement issue is fixed.

The pass2 Gemini chess run also recorded no usable Gemini quota-remaining
headers after cloud-agent replies. For Gemini, AIH v4 can currently record
token usage and treat 429 `RESOURCE_EXHAUSTED` as a stop signal, but it cannot
enforce a preemptive "5% weekly limit remaining" boundary from observed response
headers alone.

## Tournament Stop Boundary

Recommended configuration name:

- `AIH_V4_CLOUD_MIN_REMAINING_PCT=5`

Recommended behavior:

- After every cloud agent response, parse provider status headers and update a
  live tournament summary artifact.
- If the most relevant remaining percentage is at or below the configured
  stop boundary, retire that cloud provider/model from new cloud turns.
- If a current game includes a local agent, preserve the game state and let the
  next local-agent turn be recorded instead of abandoning the whole tournament.
- If a current game requires the retired cloud agent to move again and no local
  substitution policy has been configured, stop that board cleanly with a
  `cloud_quota_boundary` termination instead of treating it as a harness crash.

## Open Question

The remaining implementation decision is the substitution rule after a cloud
agent is retired mid-game. The safest default is to stop only that board and
continue other boards. If desired, AIH v4 can instead replace the retired cloud
side with a configured local fallback model.
