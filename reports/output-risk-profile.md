# Output Risk Profile

| Risk | Guardrail |
| --- | --- |
| Source material becomes imitation | Extract only high-level mechanisms; produce a distinct premise and prohibit copying characters, scenes, dialogue, and plot sequence. |
| Avoiding imitation makes source analysis generic and too short | Allow source-specific characters, objects, and events only as analytical evidence; require 5-8 deep mechanism cards, two evidence points per card, audience psychology, escalation, transferable abstraction, and an explicit replacement boundary. |
| Topic choice is assumed | Stop after 5-8 candidates until the user selects or explicitly requests the default. |
| User cannot understand what to choose | Label genre and one-sentence story direction, then state exactly how to select or use the default. |
| Candidates are hidden behind file links or numbered unclearly | Render the full candidate list in chat and use fixed identifiers such as `选项 01`; reserve files for backup and traceability. |
| Original workflow is silently lost | Maintain a source-workflow preservation map and execute every creative role as a visible pass. |
| The conflict designer locks the story before topic selection | Use `ag_006` front-light only for abstract conflict/payoff extraction; prohibit named characters, scenes, antagonist plans, and plot sequences until the back-heavy post-outline pass. |
| Antagonist, tears, and爽点 are too weak | Require a dedicated enhancement pass before risk review. |
| High-risk outline proceeds to prose | Rework and re-review any High finding before drafting. |
| Long draft loses continuity | Maintain a story bible, update the episode ledger after every 2-3 episode batch, and provide a recovery protocol. |
| Structural validators pass while the story contains logic bugs | Require evidence-backed semantic review of timeline, location, causality, world rules, common sense, era/technology, knowledge, motivation, and persistent consequences; unresolved High findings block progress. |
| Logic review rubber-stamps every dimension as “passed” | Require a concrete challenge attempt and observable result for all nine dimensions; reject generic claims such as “已检查” or “通过”. |
| Confirmed first/third person drifts during drafting or release | Lock both `approved_viewpoint` and `viewpoint_character`; run the narrative-contract validator on every batch and release notes. |
| A word count is treated as a guaranteed finished-video duration | Confirm pure narration, dialogue drama, or hybrid; use its empirical character band only to estimate ordinary novel-body capacity and never infer exact seconds or split prose into production tracks. |
| Later batches collapse into summaries | Check characters per target minute against the confirmed video form, rolling batch medians, and first-third versus last-third drift; block extreme density and long-form degradation. |
| A character teleports or uses unknown information | Record character locations and knowledge state after every batch; require an explicit transition or information source before the next use. |
| A core rule is introduced once and forgotten | Track each rule from setup through use, escalation, cost, exception, and final payoff with episode evidence. |
| Character and antagonist arcs are marked complete without textual closure | Require character-arc evidence and the antagonist chain goal → benefit → mechanism → victim impact → evidence → defeat → aftermath before release. |
| Physical damage, resource use, or relationship consequences disappear | Review consequence persistence across the current batch and the next planned batch. |
| Episode count or runtime plan produces a rushed or padded ending | Confirm an approximate target episode count and allowed range before outlining, limit episode 1 to the chosen duration within 5 minutes, and assign later episodes a plot-first 1-2 minute target. Use 1 minute for a simple advance and up to 2 minutes only when conflict, reversal, revelation, or emotional payoff needs the space. Require user approval before moving beyond the episode-count range. |
| Reported character counts are inaccurate | Use a deterministic local count script; do not estimate counts in model prose. |
| English workflow labels leak into Chinese prose | Require Chinese user-facing labels and make count scripts emit Chinese output. |
| An episode contains no audience reward | Require one value point per episode, at least one explicit爽点 in every three episodes, and one strong payoff or stage climax in every six. |
| Payoffs become repetitive humiliation scenes | Rotate payoff types and reject verbal or physical degradation as the default payoff mechanism. |
| Risk checklist is pasted inconsistently | Store it once as a default review reference and scan outline, batches, and final manuscript. |
| Visual-confirmation prompts drift from the completed story | Generate character and key-scene confirmations only after the final manuscript stabilizes. |
| The skill accidentally routes into asset generation | State that prompts are written visual confirmations; exclude image and video generation. |
| Platform approval is overstated | Report checklist-based findings and remaining uncertainty; never promise approval. |
