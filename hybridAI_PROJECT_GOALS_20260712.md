# hybridai v3 project goals

## Primary Goal

Build a local Codex-like coding-agent experience on top of local model serving
that is worth continuing only if it can satisfy three durable requirements:

1. Challenge Codex on hallucination and logical reliability in measurable ways.
2. Run locally, without making a cloud-authenticated agent the runtime default.
3. Stay maintainable on both reliability and local operation over time.

If HybridAI cannot meet all three requirements, its main value becomes a
benchmark and observation platform for measuring agentic-AI development rather
than a replacement agent worth developing for daily use.

The base stack:

```text
Qwen or another local code model
  -> Ollama first, vLLM later
  -> tinyproxy optional
```

only provides text generation. It does not provide the qwencli/Codex-like
interaction layer by itself.

v3 must add that missing application layer:

```text
hybrid-agent
  -> terminal UI and session loop
  -> agent planner
  -> tool layer: read, search, edit, run commands
  -> approval and safety layer
  -> context manager
  -> Ollama/vLLM model endpoint
```

## What v3 Is Building

v3 is building `hybrid-agent`: a local coding-agent shell that gives the
qwen/tinyproxy/ollama stack a useful top layer.

`hybrid-agent` owns the user experience:

- Chat-style terminal interaction.
- Streaming model output.
- Workspace awareness.
- File search and file reads.
- Patch proposal and patch display.
- Explicit approval before edits or risky commands.
- Shell command execution and transcript capture.
- Session memory.
- Context packing.
- Error recovery.
- Concise Codex-like summaries.
- Guardrails against unsupported claims about the repo.

## What v3 Is Not Building First

v3 is not trying to make Ollama itself into Codex.

v3 is not assuming qwencli is the desired replacement for Codex.

v3 is not making Codex the runtime default, because Codex should be treated as
OpenAI-auth dependent and does not provide a true local-model mode for Ollama or
vLLM.

## Role of Existing Pieces

- Qwen/local model: generates language and code.
- Ollama: first local inference server.
- vLLM: later high-throughput local inference server.
- tinyproxy: optional proxy and network mediation layer.
- QuadUI: live monitor/control surface.
- qwencli: comparison baseline and hallucination measurement target.
- Codex: development/operator tool and reference experience.
- `hybrid-agent`: v3 local top-layer target.

## Look And Feel Goal

The local platform should move toward a Codex-like interaction pattern:

- Ask for a task in plain language.
- Inspect the real workspace before making repo claims.
- Show concise reasoning about what will be changed.
- Use tools instead of guessing.
- Present patches clearly.
- Ask for approval when appropriate.
- Run verification.
- Report the result with file and command evidence.

The desired feel is not generic chatbot output. The desired feel is a disciplined
coding-agent workflow that can eventually replace cloud-authenticated Codex for
local HybridAI development tasks.

## Evaluation Goal

v3 must generate statistical data about hallucination and reliability, with
special attention to failures that are easy to normalize as "livable" AI quirks.
The project should treat low-severity hallucinations as important if they occur
often enough to train users to accept unsupported claims.

The first comparison targets are:

- qwencli as top layer.
- Codex as standalone reference.
- `hybrid-agent` as local implementation.

The project should track whether agents invent files, commands, APIs, repo
structure, build results, dependencies, or successful edits. Those measurements
should guide the design of `hybrid-agent`.

The project should also track detection friction:

- Whether a hallucination was obvious immediately.
- Whether it required file inspection, command output, or external checking.
- Whether it was severe enough that a user would naturally record it.
- Whether it was minor enough that a user might ignore it and adapt to the tool.
- Whether the disturbance came from the agent, the human operator, a tool, the
  environment, or an unclear source.
- Whether the issue was a near-miss interpretation: almost what was requested,
  but materially different enough to disturb project flow.

This matters because a hallucination pattern can be dangerous even when
individual incidents are small. If users become habituated to minor unsupported
claims, the agent can lose trustworthiness without producing dramatic failures.

HybridAI should also track human/operator hallucinations. In this project, that
means instructions or decisions that conflict with primary evidence, project
structure, or higher-priority organizing rules because the operator is acting
from a mistaken model of the current state. The evaluation standard should treat
both agent and human hallucinations as workflow reliability defects when they
disturb overall project flow.

When either the agent or the human operator does not know the relevant project
fact, the correct behavior is to mark uncertainty and search reliable reference
data before acting. Memory, intuition, and near-miss recollection should not be
treated as primary evidence when file paths, project rules, source priority, or
current local state can be inspected directly.

Future use of the HybridAI problem analysis can itself introduce hallucination.
Summaries, taxonomies, benchmarks, project plans, and implementation decisions
must preserve uncertainty labels and avoid treating provisional categories as
final doctrine. The project should expect additional categories and relations to
be discovered as incidents are classified.

## Viability Standard

HybridAI should not be judged by feature count. It should be judged by whether
it can maintain a trustworthy chain from evidence to reasoning to action to
verification to final claim.

For the project to remain a replacement effort rather than only a benchmark,
`hybrid-agent` must eventually demonstrate:

- Lower or meaningfully better-controlled unsupported-claim behavior than the
  selected Codex reference tasks.
- Local operation as a normal runtime property, not a special-case demo.
- Repeatable evaluation runs that continue to pass as models, prompts, tools,
  dependencies, and local system conditions change.
- Maintenance practices that make reliability regressions visible instead of
  relying on user memory or anecdotal frustration.

If a competing agent offers more features but cannot distinguish observed facts,
inferences, guesses, verified results, and unknowns, HybridAI should treat that
agent as a comparison target rather than a design model.

HybridAI should also explicitly track the "good enough, use it and be happy"
failure mode as a Codex hallucination category when an agent makes unsupported
adequacy claims about its own reliability or about the acceptability of its
failure modes. A useful agent can still be unacceptable if its hallucinations
are normalized because the tool is productive enough that users adapt to weak
evidence standards. The evaluation harness should therefore ask not only whether
an agent completes tasks, but whether it encourages users to tolerate
unsupported claims, silent failures, unverified success reports, or unproven
claims that the tool is already reliable enough.

## First Success Criteria

The first useful v3 milestone is complete when `hybrid-agent` can:

1. Connect to a local Ollama OpenAI-compatible endpoint.
2. Accept a coding task in a terminal UI.
3. Search and read real workspace files.
4. Propose a patch.
5. Apply the patch after approval.
6. Run one verification command.
7. Summarize the result using actual file and command evidence.

The first evaluation milestone is complete when qwencli has been run against a
repeatable HybridAI task set and its hallucination/failure rate has been recorded
in a machine-readable format plus a markdown report.
