# AIH v4 Cloud Agent Limit Probe

Created: 2026-08-02T20:26:38+00:00

| Agent | Provider | Status | HTTP | Requests remaining % | Tokens remaining % | Retry after |
| --- | --- | --- | ---: | ---: | ---: | --- |
| openai:gpt-4.1-mini | openai | completed | 200 | 99.8 | 99.985 |  |
| openai:gpt-5-nano | openai | completed | 200 |  |  |  |
| gemini:gemini-3.1-flash-lite | gemini | completed | 200 |  |  |  |
| anthropic:claude-3-5-haiku | anthropic | request_failed | 401 |  |  |  |

Notes:

- This probe does not start an AIChess game.
- OpenAI and Anthropic expose documented rate-limit headers that can be converted to remaining percentages.
- Gemini API quota docs describe RPM, TPM, RPD, and spend limits, but this probe records only headers actually returned by the API.
