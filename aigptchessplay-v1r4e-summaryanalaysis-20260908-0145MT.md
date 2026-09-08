# AIGPTChessPlay v1r4e Summary Analysis
## Run result

The v1r4e experiment worked. It produced much cleaner evidence than r4d.

The run completed in about 8m55s with all 4 prefilter-pass models. There were 34
llama.cpp requests: 17 non-stream and 17 stream. Every request returned HTTP 200
with curl_rc=0, and every response was successfully parsed. All streaming
requests reached their terminal data and [DONE]. No transport or communication
failure occurred in this run.

## Model-return completion results

| Model | stream=false | stream=true | Result |
|---|---|---|---|
| gemma3 | 32=L, 64=L, 128=L, then 190 tokens / stop at max=256 x3 | Same | QUALIFIED at 256 |
| gemma-4 E2B | 32=L, 64=L, 128=L, 256=L, 512=L | Same | Not qualified at 512 cap |
| qwen2.5 | 5 tokens / stop at max=32 x3 | Same | QUALIFIED at 32 |
| smollm2 | 22 tokens / stop at max=32 x3 | Same | QUALIFIED at 32 |

`L` means `finish_reason=length`.

The strongest validation of the new algorithm is:

    Every finish_reason=length response had:
    completion_tokens == max_tokens

There were 16 `length` responses, and all 16 hit the exact imposed token
ceiling. That strongly supports the interpretation that llama.cpp stopped them
because the allotted generation budget was exhausted.

## Model-specific return budgets

The models clearly need different response budgets.

    qwen2.5
      max_tokens=32
      completed response=5 tokens

    smollm2
      max_tokens=32
      completed response=22 tokens

    gemma3
      max_tokens=256
      completed response=190 tokens

    gemma-4 E2B
      max_tokens=512
      still truncated

A universal `max_tokens=32` was therefore inappropriate. The r4e model-specific
escalation logic is justified by the observed data.

## Streaming versus non-streaming

Streaming did not solve the completion problem, but it also did not break
anything.

For Gemma-4, the reconstructed generated output was identical between stream and
non-stream at every matching token limit:

    32   identical
    64   identical
    128  identical
    256  identical
    512  identical

Qwen and SmolLM2 were also identical between modes. Gemma3 was identical from 64
tokens upward; only the first 32-token result differed slightly.

For this experiment:

    stream=false ~= stream=true

in terms of actual generation and termination.

This is useful evidence. Streaming did not materially improve completion
behavior, although it remains useful for observing generated data incrementally.

## Critical evaluator finding

The most important discovery is that the earlier idea of searching every string
in the llama.cpp JSON for any legal UCI move would be unsafe.

Gemma3 eventually produced a completed response with:

    finish_reason=stop
    completion_tokens=190

But its `message.content` was essentially an echo of the chess prompt, including
candidate moves such as:

    candidate_1=a2a3
    candidate_2=a2a4
    candidate_3=b1a3
    ...
    candidate_10=d2d4

A naive legal-UCI search would therefore find legal moves in the echoed prompt
and falsely conclude that Gemma3 had selected one.

It had not.

This means that arbitrary UCI strings found anywhere in the returned JSON cannot
automatically be treated as the model's selected answer.

## Observed behavior by model

Qwen2.5 is the cleanest case:

    finish_reason=stop
    completion_tokens=5
    content="a2a3"

That looks like the response form AIGPTChessPlay wants.

SmolLM2 terminates normally, but returns:

    [a-h][1-8][a-h][1-8][qrbn]

So communication is successful, but the model response is invalid. It copies the
requested format description rather than producing an instance of that format.

Gemma3 terminates normally once given enough tokens, but largely echoes the
chess request rather than selecting a move.

Gemma-4 never reaches a completed answer by 512 tokens. Its `message.content`
remains empty while generated material appears in `reasoning_content`. At 512
tokens it is still reasoning rather than presenting a final answer.

## Implication for return extraction

I would no longer construct one giant RETURN_STRING.

The JSON structure itself contains useful distinctions:

    message.content
    message.reasoning_content
    finish_reason
    usage.completion_tokens

Those fields should not automatically be treated as equivalent.

`message.content` appears to be a better starting place for the final answer
than arbitrary JSON strings, while `reasoning_content` should be preserved as
evidence but should not automatically count as the answer.

Even `content` cannot simply be searched indiscriminately because Gemma3
demonstrated that prompt echoes can appear there.

The next extraction problem is therefore:

    completed llama.cpp response
            |
            v
    identify the model's selected/final answer
            |
            +-- distinguish it from prompt echo
            +-- distinguish it from reasoning
            +-- distinguish it from format echo
            +-- distinguish it from metadata
            |
            v
    only then test UCI syntax and chess legality

## Software defect found in r4e

The individual `model-return-calibration.tsv` files are correct.

The aggregated `model-return-summary-v1-r4e.tsv` row for Gemma-4 is malformed.
Values such as:

    UNQUALIFIED_LENGTH_AT_CAP   5   0   length

were shifted into columns intended for:

    max_tokens
    timeout
    attempts

The underlying attempt data is intact. This is an aggregate-summary writer bug
that should be corrected in the next revision.

## Bottom line

r4e accomplished its intended diagnostic purpose.

It separated several concepts that r4d had mixed together:

    transport success
    != normal generation completion
    != valid final model answer
    != legal chess move

For the single C10 prompt:

| Model | Communication | Normal completion | Apparent final-answer quality |
|---|---|---|---|
| qwen2.5 | PASS | PASS | Valid move: `a2a3` |
| smollm2 | PASS | PASS | Invalid format-template echo |
| gemma3 | PASS | PASS at 190 tokens | Prompt echo; no distinct selected move |
| gemma-4 | PASS | Not completed by 512 | Undetermined |

The model-return completion algorithm is validated well enough to keep as the
current working approach.

The next problem is not primarily streaming versus non-streaming. It is
determining, from a completed llama.cpp response, which returned material
actually represents the model's intended final answer without mistaking echoed
input, reasoning, or formatting text for that answer.

## Requested model scope versus models actually tested

**Question:** What models did I request that you test in v1r4e?

You requested **all models that passed the model prefilter**.

You did **not** request a fixed 4-model test set.

Your instruction was:

> "Use it for all of the models that pass the model prefilter."

So v1r4e should have taken whatever set the v1r4e prefilter admitted and run the
new model-return diagnostic on **every one of them**.


The reason only 4 models were tested is that the run admitted only these 4 through
the prefilter:

- gemma3
- gemma-4 E2B
- qwen2.5
- smollm2

Therefore the important follow-up question is whether the **prefilter itself
improperly excluded models that should have reached the r4e diagnostic**.

....note...it's 2am. It knows that its work is done for the night. 
