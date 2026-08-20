---
name: ai-comic-novel-workflow
description: "Create an original AI comic-drama novel from user-uploaded source material: analyze reusable audience mechanisms, recommend 5-8 selectable topics, confirm an approximate target episode count and runtime plan, build the story bible and outlines, draft the Chinese manuscript in episode batches, review supplied content boundaries, and produce character and key-scene confirmation prompts. Use for AI漫剧小说、短剧式小说、从素材到全稿、人物提示词、场景提示词. Exclude one-off polishing, imitation, image or video generation, and platform-approval guarantees."
---

# AI Comic-Novel Workflow

Create an original Chinese comic-drama novel package from supplied material without copying distinctive expression.

## Workflow

1. Apply [workflow details](references/workflow.md) and [original workflow preservation](references/original-workflow-preservation.md).
2. Run a front-light joint mechanism analysis: `ag_001 赛道分析师` leads audience/genre analysis while `ag_006 冲突&打脸设计师` only extracts conflict and payoff mechanics. Then show 5-8 original topic candidates in chat and stop for selection.
3. After topic selection, confirm the approximate target episode count, runtime plan, and video adaptation mode (`纯解说旁白` / `对话剧情` / `复合型`) through [duration planning](references/duration-planning.md), estimate the required novel-body characters, then build the bible and outlines.
4. Apply [content boundaries](references/content-boundaries.md), resolve high risks, and confirm the outline, viewpoint, opening, hook, and continuation choices.
5. Initialize and maintain `project_state.json` with `scripts/project_state.py`; treat it as the sole recovery source.
6. Draft 2-3 episodes per batch, validate and commit the recovery point with `scripts/run_batch_checks.py`, then review and polish.
7. From the validated final manuscript, create and verify `08_character_prompts.md` and `09_key_scene_prompts.md`, then close the complete delivery bundle only through `scripts/finalize_release.py`.

## Hard Gates

- Use plain Chinese and [user guidance](references/user-guidance.md).
- After every saved milestone or drafting batch, show clickable absolute-path links to the updated user-facing project files. Never hide deliverables as internal files or claim a file was saved before verifying it exists.
- Put working annotations before prose and remove them from clean Word.
- Enforce [opening-hook design](references/opening-hook-design.md) and [payoff design](references/payoff-design.md) as separate contracts.
- Apply the [logic and common-sense review](references/logic-common-sense-review.md) to the enhanced outline, every drafting batch, and the final manuscript. Logic correctness overrides hook density and drafting speed.
- Preserve the front-light/back-heavy split: “front-light” limits premature new-story design, not analytical depth. In `01_source_payoff_analysis.md`, `ag_006` must deeply analyze 5-8 mechanisms and may cite source-specific characters, objects, and events strictly as evidence; it must separately state the transferable abstraction and the concrete shell that cannot be reused. It must not design the new project's characters, scenes, antagonist actions, or plot sequence until the selected topic and core outline are locked. Pass `validate_source_payoff_analysis.py` before generating topic candidates.
- Format `05_enhanced_outline.md` as vertical episode cards, never as a wide multi-column episode table. Run `validate_enhanced_outline.py` before risk review.
- Do not impose a total word or character target. The approximate target episode count and runtime define scope: default episode-count tolerance is +/-10% with a minimum allowance of one episode; episode 1 uses the user-confirmed duration up to 5 minutes; every later episode uses a plot-first target within 1-2 minutes. Use the shortest duration that preserves causality, emotion, and payoff; do not pad every episode toward 2 minutes. Character counts are diagnostics only. Obtain user confirmation before changing the episode target beyond its allowed range.
- Keep the manuscript as ordinary novel prose. Do not split it into narration/dialogue/visual labels. Estimate only the required novel-body range from the confirmed video mode: pure narration `330-500`, dialogue drama `360-440`, hybrid `350-450` characters per minute.
- Lock `approved_viewpoint` and `viewpoint_character` before drafting. Pass `validate_narrative_contract.py` after every batch and before release; a clear first/third-person mismatch blocks progress.
- After every batch, create evidence-backed `reports/logic_review_<through>.json`, then run `scripts/run_batch_checks.py` with `--logic-review`; it must pass language, payoff, runtime-density, batch-drift, and logic/common-sense gates before updating the recovery point.
- Auto-fix local logic defects that preserve locked facts. Ask the user before any fix that changes the core setting, main causal chain, major-character fate, or ending. Never continue with an unresolved High logic risk.
- Preserve `auto_batch`, honor `manual_continue`, and resume only from validated `project_state.json`. Limit one response to at most two batches; stop immediately on validation failure and leave the last validated recovery point unchanged.
- Never hand-build or merely rename the final Word file. Export it from the reviewed Markdown and pass `verify_final_docx.py` before delivery.
- Before Word export, pass `validate_release_consistency.py` with a final logic review; require closed world rules, character arcs, antagonist causality, clue ledger, and High-risk logic findings.
- Treat the manuscript, character prompts, key-scene prompts, final logic review, and verified Word as one atomic release bundle. Missing `08_character_prompts.md` or `09_key_scene_prompts.md` blocks release even when Word exists.
- Only `scripts/finalize_release.py` may set `project_state.json.stage` to `complete`. It must hash-bind every final artifact in `reports/release_receipt.json`; any later manuscript or prompt change makes the previous release stale.
- Report “全稿完成” only after reopening `reports/release_receipt.json`, confirming `passed: true`, confirming its hashes match the current files, and reading `stage: complete` plus `validation_status: passed` from `project_state.json`. Otherwise report the exact blocking items and last validated recovery point.
- In the completion reply, use forward-slash absolute Markdown targets for Markdown/JSON files. Emit the final DOCX exactly once as a plain output `codex-file-citation`; never combine a normal DOCX Markdown link with the citation or repeat its filename.

Use [project layout](references/project-layout.md), [creative roles](references/creative-roles.md), and [visual prompts](references/prompt-deliverables.md). Keep Markdown authoritative; treat `reports/` as deferred engineering evidence.
