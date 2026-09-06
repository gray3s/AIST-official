Last modified: 20260906 1312MT

# AIGPTChessPlay Project Summary

Project version:

`AIGPTChessPlay v0`

Project reference term:

`the current AIGPTChess project`


## 1. PROJECT DEFINITION

AIGPTChessPlay v0 is the current AIGPTChess project. It combines the local-model
communication and candidacy work developed through the R11 and R12 lineage with
the registration, chess-gameplay, and tournament software previously developed
under the AIGPTChess v6 name.

AIGPTChessPlay v0 contains 2 principal first-party software components:

1. `Model-llama.cpp Comm Test v0`
2. `AIGPT Chess Engine v0`

The historical names R11, R12 v0, and AIGPTChess v6 are retained only where
needed for source-code provenance, run identification, and evidence
traceability.


## 2. PROJECT ORGANIZATION

AIGPTChessPlay v0
    |
    +-- Model-llama.cpp Comm Test v0
    |     - GGUF model discovery
    |     - llama.cpp communication/profile testing
    |     - local-model candidacy evaluation
    |     - qualification decision/evidence
    |
    +-- AIGPT Chess Engine v0
          - model registration
          - Stockfish/controller interface
          - chess prompt construction
          - UCI move validation
          - gameplay
          - tournament execution


## 3. MODEL-LLAMA.CPP COMM TEST v0

Historical lineage folded into this component:

- R11 model communication/profile testing
- R12 v0 communication-profile and model-candidacy/qualification testing

Primary function:

Determine whether a local GGUF model can communicate reliably through llama.cpp
and whether its behavior is sufficiently usable to become a candidate for AIGPT
Chess Engine v0.

Primary responsibilities:
- discover candidate GGUF models;
- use candidate model files only from `~/RPA2/devneutral/models`;
- start one candidate model at a time through llama.cpp;
- determine a usable communication profile;
- send defined communication/candidacy prompts;
- preserve each exact prompt and exact raw model reply;
- measure response timing and host responsiveness;
- distinguish transport/no-response failure from semantic failure;
- apply explicit candidacy acceptance and rejection rules;
- record the decision-making software role and reason for each decision;
- decide whether the model proceeds to AIGPT Chess Engine v0.

Historical implementation provenance includes:

`runme-r12-v0-qualification-gate.sh`

plus the R11 communication/profile-test code lineage from which the R12 v0
qualification implementation evolved.


## 4. AIGPT CHESS ENGINE v0

Historical software folded into this component:

- AIGPTChess v6 registration testing
- AIGPTChess v6 chess gameplay
- AIGPTChess v6 tournament execution

Primary function:

Take a candidate admitted by Model-llama.cpp Comm Test v0, register it as a
chess agent, provide the current position and controller/Stockfish information,
receive the model's move, validate that move, and execute chess gameplay and
tournament logic.

Primary responsibilities:
- register an admitted model;
- communicate with Stockfish;
- obtain the current FEN;
- obtain legal moves;
- obtain Stockfish best-move/clue information;
- construct the model chess prompt;
- preserve the exact prompt and exact raw model reply;
- validate complete UCI move syntax;
- validate move legality;
- retry only when appropriate for the observed failure type;
- record accepted/rejected moves and the software role making each decision;
- execute gameplay and tournament logic;
- preserve precise termination and failure classifications.

Historical implementation provenance includes:

`aigptchess-v6-r12-v0-worker.sh`

including:

`controller_exchange()`



## 5. PROJECT-LEVEL ORCHESTRATION

High-level execution flow:

`local GGUF model`
        |
        v
`Model-llama.cpp Comm Test v0`
        |
        | candidate accepted
        v
`AIGPT Chess Engine v0`
        |
        v
`registration + chess gameplay + tournament results`

Historical orchestration provenance includes:

`START-R12-V0-AIGPTCHESS-V6.sh`

and:

`runme-r12-v0-aigptchess-v6.sh`

These historical filenames remain provenance identifiers until the first-party
source library is formally collected, versioned, and renamed.


## 6. SOFTWARE-ROLE SEPARATION

### GGUF model

Generates the model response. It does not grade its own response and does not
assign its own candidacy or chess result.

### llama.cpp / llama-server

Third-party local inference and transport software. It loads the GGUF model,
performs inference, and returns model output.

### Model-llama.cpp Comm Test v0

First-party communication and candidacy evaluator. It decides whether model
communication behavior satisfies the defined candidacy rules.

### AIGPT Chess Engine v0

First-party model-registration, Stockfish/controller-interface, move-validation,
gameplay, and tournament software.

### Stockfish

Third-party chess engine. It supplies chess analysis, legal-move information,
and clue/best-move information. It does not grade natural-language candidacy
responses.

### ChatGPT post-run analysis

Not runtime software. ChatGPT reviews source code, prompts, replies,
classifications, and preserved run evidence after execution.


## 7. THIRD-PARTY SOFTWARE BASELINE

Third-party software is required by AIGPTChessPlay v0 but is excluded from the
first-party source-library collection.

Known baseline from the referenced run:

`llama.cpp / llama-server`
- build 10729
- commit `458681e1d`

`Stockfish`
- Stockfish 16

`GGUF candidate models`
- source tree: `~/RPA2/devneutral/models`


## 8. HISTORICAL PROVENANCE

Primary historical evidence package:

`gpt-aigptchess-v6-inventory-20260905_232900_MDT.zip`

Historical recorded run:

`aigptchess-v6-inventory-20260905_232900_MDT`

Historical R12 v0 software package:

`gpt-r12-v0-aigptchess-v6-20260906_UTC.zip`

Those names are preserved exactly because they identify the actual source and
run evidence from which AIGPTChessPlay v0 is being organized.


### Provenance map

Historical lineage: `R11`
Current destination: `Model-llama.cpp Comm Test v0`

R11 communication-profile, llama.cpp model-communication, retry, and related
candidacy-test work is folded into the communication-test component.

Historical lineage: `R12 v0`
Current destination:
`Model-llama.cpp Comm Test v0` + AIGPTChessPlay v0 orchestration

R12 v0 qualification/candidacy logic is folded into Model-llama.cpp Comm Test
v0. R12 campaign/orchestration code becomes project-level AIGPTChessPlay v0
orchestration provenance.

Historical lineage: `AIGPTChess v6`
Current destination: `AIGPT Chess Engine v0`

The registration test, Stockfish/controller interface, chess prompt/move
handling, gameplay, and tournament code are folded into AIGPT Chess Engine v0.


## 9. HISTORICAL MODEL-CANDIDACY RESULT

The referenced run discovered:

`29 GGUF model entries`

representing:

`28 unique SHA-256 model contents`

Historical R12 v0 gate result:

- PASS: 6
- FAIL: 23

These values are preserved as historical runtime results. They do not prove that
only 6 models were functionally capable because evaluator behavior materially
affected the result.


## 10. MODEL-COMM-TEST FINDINGS

The historical R12 v0 semantic validator used narrow, case-sensitive Bash
regular-expression matching.

Rejected examples included:

`Ready to analyze a chess position.`
`Acknowledged.`
`Received.`
`Understood! Proceeding with your chess analysis request.`

Historical semantic failures:
`16`

Failures reversed by capitalization normalization alone:
`11 of 16`

One additional failure involved `readiness` where the historical validator
looked only for `ready`. Model-llama.cpp Comm Test v0 therefore should eliminate
capitalization as a semantic acceptance/rejection factor and broaden semantic
matching where justified, while always preserving the original raw response.


## 11. AIGPT CHESS ENGINE FINDINGS

Strongest historical chess result:

Mistral model SHA prefix:
`f5074b12...`

- 42 completed ply
- 21 accepted model moves
- 21/21 accepted moves followed the clue-10 Stockfish recommendation

Second strong historical result:

Qwen model SHA prefix:
`46bb6520...`

- 10 completed ply
- 5 accepted model moves
- 5/5 accepted moves followed the clue-10 Stockfish recommendation

These results demonstrate that the basic local-model / llama.cpp / controller /
Stockfish / chess-worker path can advance real games.


## 12. CHESS CLASSIFICATION FINDING

Historical invalid-format examples included:

`f2` instead of `f2f3`
`c6` instead of `c5c6`

Those individual UCI-format rejections were consistent with the stated
exact-move rule. The problem was the broader final classification
`MODEL_COMMUNICATION_LOSS`, which could be assigned after 3 invalid replies even
though the model had communicated on all 3 attempts.

AIGPT Chess Engine v0 should preserve distinct final classes for:

- no reply;
- invalid UCI format;
- illegal move;
- mixed communication failure;
- resource failure.


## 13. RETRY FINDING

Historical deterministic retry examples:

`f2`
`f2`
`f2`

and:

`c6`
`c6`
`c6`

Increasing timeout or token allowance does not correct deterministic formatting
errors. Retry policy should depend on whether the actual failure was no
response, slow response, truncation, malformed output, or repeated deterministic
malformed output.


## 14. HOST-RESOURCE FINDING

All 6 models entering the historical chess stage recorded:

`responsiveness.automated = PASS`

Mistral reached 42 ply while the host remained responsive under the automated
measurement. This demonstrates that useful local chess execution with
appropriately sized models is practical on the current laptop.

The earlier Qwen3.8-27B experience remains evidence that some models are too
large to be practical candidates on this host even if the model itself is
otherwise capable.


## 15. AIGPTCHESSPLAY v0 DESIGN PRINCIPLES

1. Keep model behavior separate from evaluator behavior.
2. Keep communication/candidacy testing separate from chess gameplay testing.
3. Keep Stockfish/controller behavior separate from model-output validation.
4. Preserve every exact prompt and every exact raw model reply.
5. Identify the decision-making software component at every important decision.
6. State acceptance/rejection criteria before evaluating a decision.
7. Do not use capitalization as a semantic candidacy factor.
8. Keep transport, semantic, format, legality, and resource failures separate.
9. Use candidate models only from `~/RPA2/devneutral/models`.
10. Keep third-party software outside the first-party source collection.


## 16. FIRST-PARTY SOFTWARE LIBRARY COLLECTION

A formal first-party source collection is to be produced for AIGPTChessPlay v0.
It will collect the code making up Model-llama.cpp Comm Test v0, AIGPT Chess
Engine v0, and the required project-level orchestration, while excluding
third-party software, binaries, and model files.

The collection should include:
- all applicable first-party source files;
- component names and version numbers;
- component functions/roles;
- historical filename/source provenance;
- SHA-256 hashes;
- collection name and version;
- collection build date/time;
- a manifest mapping historical R11/R12/AIGPTChess-v6 names to the new AIGPTChessPlay v0 organization.

The resulting source collection becomes the software baseline against which
future AIGPTChessPlay v0 run summaries and revisions should be referenced.


## 17. CURRENT STATUS

AIGPTChessPlay v0 is currently an organizational and software-baseline
consolidation of working historical code and run evidence. The immediate next
work is to collect and version the first-party source library, correct the
identified communication/candidacy evaluator defects, improve chess failure
classification and retry behavior, and then rerun the project under the
AIGPTChessPlay v0 naming and version baseline.
