# Output Quality Scorecard

Execution mode: `local_deterministic`. This is script-backed regression evidence, not provider-backed model evidence.

## Observed baseline failure

A real 45-episode generated manuscript passed the existing count, payoff/annotation, and Chinese-language checks. A post-release audit found severe runtime-density imbalance and semantic continuity defects.

| Signal | Observed result |
| --- | --- |
| First 15 episodes average body characters | 566 |
| Last 15 episodes average body characters | 222 |
| Front-to-back decline | 61% |
| Existing batch validation | Passed |
| New runtime-density validation | Failed as expected |

The new validator identified early episodes above 380 characters/minute, late episodes below 160 characters/minute, and a significant front-to-back density decline. Exit status was `1`, which is the required blocking behavior.

## Regression cases

| Case | Baseline | Improved gate | Result |
| --- | --- | --- | --- |
| Runtime extremes and rushed tail | Annotation labels passed | Density + rolling/long-form drift | Pass |
| Core-rule repair changes locked story | No confirmation evidence gate | `changes_core_plot` requires `user_confirmed` | Pass |
| Final rules/arcs/antagonist not closed | DOCX structure could pass | Release consistency evidence gate | Pass |
| Three-minute prose capacity guessed from one fixed rate | One generic density band | Mode-specific pure narration/dialogue/hybrid ranges | Pass |
| First-person contract drifts into named-character third person | No deterministic viewpoint gate | Viewpoint + viewpoint-character contract | Pass |
| Logic review says only “已检查/通过” | Presence of dimensions looked sufficient | Challenge attempt and result required per dimension | Pass |
| Source analysis collapses into a 530-character generic summary | Thirteen one-line template fields passed | 5-8 deep mechanism cards, two source facts per card, audience psychology, escalation, transfer and replacement boundaries, plus a 1500-Chinese-character floor | Pass |

## Current deterministic test result

`python -m unittest discover -s tests -v` → `16 tests`, `OK`, exit status `0`.

## Remaining evidence boundary

Scripts prove that required review evidence exists, the writer attempted to disprove each logic dimension, mode-specific capacity is enforced, and deterministic viewpoint contradictions are blocked. Semantic truth still depends on an evidence-backed review of the actual episodes; the workflow now requires concrete episode evidence rather than an unsupported “已检查” claim.
