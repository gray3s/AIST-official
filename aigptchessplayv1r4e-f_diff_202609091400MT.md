# AIGPTChessPlay v1r4e -> v1r4f difference report

v1r4f build: 001
Build date:  2026-09-09

Baseline:
aigptchessplay-v1-r4e-code-20260908_001926_MDT.zip

Baseline SHA-256:
b53e5460787fb821307e54c0e6dc2a87eef3938b2e8e9d9d3927fe5ae6d26715

## PURPOSE

v1r4e was primarily a llama.cpp model-return completion diagnostic.  It
compared streaming and non-streaming responses, calibrated return-token
budgets, and preserved raw response data without deciding whether the
returned material represented a valid chess answer.

v1r4f moves to the next stage.

It addresses the problems identified by SAG in the v1r4e analysis and
introduces persistent project-data anchors for Model Prefilter,
Registration, and Tournament history.

The databases are not intended to eliminate development drift.  They
provide concrete model, hardware, code-build, test, and outcome records
against which later development can be checked.

1. MODEL PREFILTER IS SEPARATED FROM REGISTRATION

---

v1r4e:

Model Prefilter PASS information was inherited from the earlier v1r4 run,
but admission remained embedded in the AIGPTChessPlay execution chain.

v1r4f:

Model Prefilter becomes a separate sub-project/data domain.

Registration does NOT rerun Model Prefilter.

The current local model inventory is obtained by scanning:

```
~/RPA2/devneutral/models/*.gguf
```

The historical v1r4 Model Prefilter evidence used by v1r4e is then
anchored to a hardware record.

Only models with:

```
passmdlpftrchw
```

are eligible for the separately executed AIGPTChessPlay Registration Test.

2. MODEL PREFILTER ACCEPTANCE DATABASE

---

v1r4e:

There was no persistent multi-category Model Prefilter acceptance
database.

v1r4f:

The Model Prefilter database establishes these 5 categories:

```
mdlnotsthst

A previously known model is not seen in the current direct-GGUF
scan of ~/RPA2/devneutral/models.


mdlpftruntstchw

The model is installed but has no valid Model Prefilter result
anchored to the current hardware configuration.

This is an untested state, not a failure.


fillmdlhwinv

Model Prefilter failure attributable to hardware/resource
incompatibility on the anchored hardware.


fillmdlreginv

The model runs on the hardware but fails the Model Prefilter's
Registration-readiness/communication compatibility requirement.


passmdlpftrchw

The model passed Model Prefilter on the anchored current hardware
and is eligible for AIGPTChessPlay Registration.
```

The category spellings preserve the project vocabulary established by
SAG.

3. HARDWARE HISTORY BECOMES PROJECT DATA

---

v1r4e:

Hardware measurements existed primarily as individual run evidence.

v1r4f:

A persistent hardware-history database records:

```
host
kernel
CPU
RAM
swap
motherboard identity
exposed GPU PCI identifiers
llama.cpp version/build
llama-server SHA-256
Stockfish version
```

A hardware_id is generated from this configuration and referenced by
Model Prefilter and Registration records.

The historical v1r4 prefilter result is treated as applicable to the
current hardware only when the available compatibility anchors agree:

```
RAM total
swap total
llama.cpp version/build
```

If those anchors differ, an installed model becomes:

```
mdlpftruntstchw
```

instead of silently inheriting an old PASS or FAIL.

4. MODEL PREFILTER HISTORY IS PRESERVED

---

The Model Prefilter database records:

```
model ID
model SHA-256
current path
current presence
hardware_id
acceptance category
source prefilter status
source prefilter reason
source prefilter run
source prefilter revision
source prefilter code SHA-256
communication profile parameters
```

This converts Model Prefilter development/run history into durable
project data.

5. REGISTRATION BECOMES A SEPARATE DATA DOMAIN

---

v1r4e:

The r4e diagnostic did not perform the semantic Registration Test that
determines whether an admitted model can provide a usable chess move.

v1r4f:

Registration has its own persistent database.

Every Registration record includes:

```
model SHA-256
hardware_id
Model Prefilter category
AIGPTChessPlay version
revision
build number
build date
Registration-worker SHA-256
answer-extractor SHA-256
source prefilter provenance
llama.cpp provenance
Stockfish provenance
Registration outcome
C1 outcome
C10 outcome
```

## 6. EXACTLY 3 CHESS-ANSWER ATTEMPTS

v1r4e:

Three consecutive finish_reason=stop responses were used for
model-return calibration.

Those were completion-calibration responses, not 3 independent
chess-answer opportunities.

v1r4f:

The model receives exactly 3 chess-answer attempts during each
Registration response phase.

Generation recovery is tracked separately.

7. GENERATION COMPLETION IS NOT ANSWER VALIDITY

---

v1r4f explicitly separates:

```
communication success
    ->
generation completion
    ->
intended-answer extraction
    ->
UCI recognition
    ->
current-position legality
    ->
Registration outcome
```

A response with:

```
finish_reason=length
```

means that generation was incomplete.

The controller can increase the output budget and continue generation
recovery inside the SAME answer attempt.

A truncated generation is not automatically counted as either a valid
or invalid chess answer.

8. ONLY ASSISTANT CONTENT CAN CONTAIN THE ANSWER

---

v1r4e preserved all llama.cpp JSON string fields for investigation.

That evidence showed why searching the complete JSON for text matching
UCI syntax is unsafe: controller prompts and echoed candidate lists can
contain strings such as:

```
a2a3
a2a4
b1a3
```

v1r4f therefore restricts answer extraction to:

```
choices[0].message.content
```

It does NOT search:

```
reasoning_content
controller prompts
request JSON
candidate truth tables
other JSON fields
```

## 9. SEMANTIC ANSWER EXTRACTION

The new extractor prefers, in order:

```
a plain UCI move on the final meaningful line;

an explicitly labeled final/selected move;

one unique, unambiguous UCI token in non-echo assistant text.
```

Prompt/candidate echo patterns are excluded.

Multiple different non-echo moves are treated as ambiguous rather than
guessing which move the model intended.

10. ACTUAL v1r4e RESPONSE REGRESSION

---

The v1r4f extractor was tested against the actual v1r4e run responses.

Actual Qwen2.5 response:

```
a2a3
```

Result:

```
FOUND_UCI a2a3
```

Actual SmolLM2 response:

```
[a-h][1-8][a-h][1-8][qrbn]
```

Result:

```
rejected as template/format echo
```

Actual Gemma3 completed response:

```
controller/prompt material echoed into assistant content
```

Result:

```
rejected as prompt echo
```

Therefore the extractor no longer obtains a false chess move merely
because UCI-looking strings occur somewhere in returned material.

11. REGISTRATION HAS NO CLUE CANDIDATE LIST

---

v1r4e used a fixed clue prompt, normally C10, for its communications
diagnostic.

v1r4f separates Registration from clue testing.

The Registration prompt supplies:

```
FEN
side to move
request for one legal UCI move
```

It supplies NO candidate list.

A model must first pass Registration by producing an acceptable legal
move.

12. C1 AND C10 BECOME POST-REGISTRATION EDGE TESTS

---

After Registration PASS:

```
C1 is tested.

C10 is tested.
```

For C1:

```
candidate_1 is guaranteed legal.
```

For larger clue lists:

```
candidates alternate deterministically between legal and illegal
examples.
```

Candidate truth is logged separately from the prompt.

The model remains free to choose any legal move and is not required to
copy a candidate.

13. STREAMING IS NOT RETESTED

---

v1r4e tested both:

```
stream=false
stream=true
```

The r4e evidence showed successful and effectively equivalent transport
behavior.

v1r4f therefore does not consume another test run investigating
streaming.

Registration uses non-streaming responses while the admission and
semantic-answer issues are investigated.

14. RESPONSE OUTCOMES ARE EXPLICIT

---

v1r4f recognizes these response concepts separately:

```
ACCEPTABLE
DRAW
MOVE_TIMEOUT
FORFEIT
```

An ACCEPTABLE legal chess move produces Registration PASS.

DRAW, MOVE_TIMEOUT, and FORFEIT are recognized classified responses,
but they do not produce Tournament eligibility.

A response that remains invalid after the available answer attempts
fails Registration.

15. GEMMA-4 TSV COLUMN-SHIFT BUG

---

v1r4e contained a reporting defect involving calibration rows with empty
fields.

The actual Gemma-4 structure included:

```
nonstream
UNQUALIFIED_LENGTH_AT_CAP
<empty max_tokens>
<empty timeout>
5
0
length
512
```

The old aggregate output shifted later values left into incorrect
columns.

v1r4f reads tab-separated values by explicit field number.

Empty fields remain empty.

The attempts, finish_reason, and following fields therefore remain in
their proper columns.

A regression test specifically verifies this behavior.

16. 3 SEPARATE PERSISTENT PROJECT-DATA AREAS

---

v1r4f creates:

```
project-data/model-prefilter/

    hardware-history-v1.tsv
    model-inventory-history-v1.tsv
    model-prefilter-history-v1.tsv
    acceptance-category-catalog-v1.tsv


project-data/registration/

    registration-history-v1.tsv


project-data/tournament/

    tournament-history-v1.tsv
```

These are append-only TSV databases.

This keeps the implementation zero-Python and avoids adding a SQLite
dependency while still making the development history structured,
queryable, diffable, and directly preservable as run evidence.

17. TOURNAMENT HISTORY IS SEPARATE

---

Tournament status no longer changes Model Prefilter or Registration
status.

The Tournament database has independent fields for:

```
model SHA-256
qualifying Registration reference
hardware_id
AIGPTChessPlay version/revision/build/date
game ID
clue level
ply
opponent configuration
returned move
move outcome
game outcome
tournament outcome
source artifact
```

v1r4f deliberately does NOT run a Tournament.

Therefore it initializes the Tournament database/schema but writes no
fabricated gameplay rows.

18. RUN ZIP NOW CONTAINS DATABASE SNAPSHOTS

---

At completion, v1r4f copies the current Model Prefilter, Registration,
and Tournament database files into the run evidence directory before
creating the results ZIP.

The persistent originals remain under the AIGPTChessPlay project-data
tree.

A result ZIP therefore contains both execution evidence and a snapshot
of the project state that produced its admission decisions.

19. BUILD PROVENANCE

---

v1r4f identifies itself as:

```
version:    v1
revision:   r4f
build:      001
build date: 2026-09-09
```

Registration records contain the SHA-256 values of the exact
Registration worker and answer extractor used.

Model Prefilter records retain their source prefilter run, revision, and
source prefilter code SHA-256 when available.

20. DEVELOPMENT-DRIFT ANCHOR

---

The databases do NOT eliminate specification or development drift.

Instead they create concrete comparison points.

Future development can distinguish:

```
what the conversation currently assumes;

what code build actually ran;

what model SHA was actually installed;

what hardware configuration was actually present;

what Model Prefilter status was actually recorded;

what Registration build produced a result;

what Tournament build later produced a gameplay result.
```

This makes drift easier to detect because current assumptions can be
compared against durable project records.

## BOTTOM LINE

v1r4e primarily answered:

```
Did llama.cpp complete the model response, and is streaming the
immediate problem?
```

v1r4f moves to:

```
Which installed models are concretely recorded as Model Prefilter
qualified on this hardware?

Can each qualified model pass a separately versioned Registration
Test?

Can the intended answer be extracted from assistant content without
confusing prompt echoes with model moves?
```

The major architectural change is that Model Prefilter acceptance,
Registration qualification, and Tournament performance are no longer
treated as one mutable concept of "model acceptance."

They are separate historical facts connected through explicit model,
hardware, run, and code-build provenance.

