# aichess_v4_pairwise_prototype_20260729 Summary

Created: 2026-08-02

## AIH Immunity Tournament Advancement

Tournament levels advance the AIH-immunity winner from each contest into the next level. The advancing agent is selected by immunity to visible/detectable hallucination, not by classical chess win/loss scoring. The AIH-immunity winner is not necessarily the winner under classic chess-tournament considerations.

| Contest | White agent | Black agent | AIH-immunity winner advancing | Termination | Maxply and reason |
| --- | --- | --- | --- | --- | --- |
| board_1 | qwen2.5:0.5b | smollm2:135m | qwen2.5:0.5b | `black_forfeit_invalid_or_unparseable_move` | maxply 20 - black_forfeit_invalid_or_unparseable_move |

## AIH Immunity Ranking

Ranking order: higher clean move percentage, lower worst termination severity, higher total plies before elimination, fewer visible hallucination events, then fewer rejected/correction attempts. Classical chess win/loss scoring is not used.

| Rank | Agent | Local/cloud | Games | Clean moves | Assigned turns | Clean move % | Visible hallucinations | Worst termination severity | Total plies before elimination | Game maxply and reason |
| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | --- |
| 1 | qwen2.5:0.5b | local | 1 | 1 | 1 | 100.0% | 0 | 0 - clean configured stop (`black_forfeit_invalid_or_unparseable_move`) | 1 | board_1 white maxply 20 - black_forfeit_invalid_or_unparseable_move |
| 2 | smollm2:135m | local | 1 | 0 | 1 | 0.0% | 1 | 3 - parser or invalid response (`black_forfeit_invalid_or_unparseable_move`) | 1 | board_1 black maxply 20 - black_forfeit_invalid_or_unparseable_move |

## AIH Hallucination Event Totals

| Agent | Rejected attempts | Parser failures | Illegal moves | Timeouts | Transport/auth/quota failures |
| --- | ---: | ---: | ---: | ---: | ---: |
| qwen2.5:0.5b | 0 | 0 | 0 | 0 | 0 |
| smollm2:135m | 1 | 1 | 0 | 0 | 0 |

## Game Rows

| Model | Mode | Termination | Completed game | Plies | Legal moves | Failed turns | Rejected attempts | Elapsed s |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| qwen2.5:0.5b vs smollm2:135m | aichess_hallucination_game | black_forfeit_invalid_or_unparseable_move | false | 1 | 1 | 1 | 1 | 17.242 |
