# Output Risk Profile

| Risk | Guardrail |
| --- | --- |
| Source material becomes imitation | Extract only high-level mechanisms; produce a distinct premise and prohibit copying characters, scenes, dialogue, and plot sequence. |
| Topic choice is assumed | Stop after 5-8 candidates until the user selects or explicitly requests the default. |
| User cannot understand what to choose | Label genre and one-sentence story direction, then state exactly how to select or use the default. |
| Candidates are hidden behind file links or numbered unclearly | Render the full candidate list in chat and use fixed identifiers such as `选项 01`; reserve files for backup and traceability. |
| Original workflow is silently lost | Maintain a source-workflow preservation map and execute every creative role as a visible pass. |
| Antagonist, tears, and爽点 are too weak | Require a dedicated enhancement pass before risk review. |
| High-risk outline proceeds to prose | Rework and re-review any High finding before drafting. |
| Long draft loses continuity | Maintain a story bible, update the episode ledger after every 2-3 episode batch, and provide a recovery protocol. |
| Episode count or runtime plan produces a rushed ending | Confirm an approximate target episode count and allowed range before outlining, limit episode 1 to the chosen duration within 5 minutes, and keep later episodes to one primary task per 1-minute episode. Require user approval before moving beyond the range. |
| Reported character counts are inaccurate | Use a deterministic local count script; do not estimate counts in model prose. |
| English workflow labels leak into Chinese prose | Require Chinese user-facing labels and make count scripts emit Chinese output. |
| An episode contains no audience reward | Require one value point per episode, at least one explicit爽点 in every three episodes, and one strong payoff or stage climax in every six. |
| Payoffs become repetitive humiliation scenes | Rotate payoff types and reject verbal or physical degradation as the default payoff mechanism. |
| Risk checklist is pasted inconsistently | Store it once as a default review reference and scan outline, batches, and final manuscript. |
| Visual-confirmation prompts drift from the completed story | Generate character and key-scene confirmations only after the final manuscript stabilizes. |
| The skill accidentally routes into asset generation | State that prompts are written visual confirmations; exclude image and video generation. |
| Platform approval is overstated | Report checklist-based findings and remaining uncertainty; never promise approval. |
