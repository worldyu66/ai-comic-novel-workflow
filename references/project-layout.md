# Project Layout

Use Markdown files as the editable source of truth:

```text
<project-name>/
  project_state.json
  allowed_terms.txt
  01_source_payoff_analysis.md
  02_topic_candidates.md
  03_story_bible.md
  04_core_outline.md
  05_enhanced_outline.md
  06_risk_review.md
  07_manuscript.md
  08_character_prompts.md
  09_key_scene_prompts.md
  10_release_polish.md
  final_manuscript.docx
  reports/
    batch_validation.json
    manuscript_quality.json
    logic_review_<through>.json
    logic_review_final.json
```

`project_state.json` is the sole machine-readable recovery source. It records the current stage, approximate target episode count, allowed range, first-episode duration, the later-episode range `[1, 2]`, confirmed video form, novel-character-per-minute estimate band, narrative viewpoint and viewpoint character, drafting mode, validated recovery point, open clues, character continuity, allowed English terms, change log, and latest validation result. Human-readable summaries may appear in `03_story_bible.md` or `07_manuscript.md`, but they must not override the state file.

It also records the strict logic-review mode, timeline and character-location ledger, knowledge state, world-rule lifecycle, logic findings, character-arc closure, antagonist causal chain, and semantic-review evidence. Every logic dimension needs evidence, a concrete challenge attempt, and its result. Empty or manually claimed closure is not sufficient at release; each closed item needs episode evidence.

`07_manuscript.md` contains the canonical episode prose and Chinese duration/opening-hook/value/payoff annotations. Each episode places its annotation immediately below the episode title and before a `### 本集正文` heading. Character counting reads only `### 本集正文` sections, so ledgers and annotations cannot inflate the result.

`01_source_payoff_analysis.md` is an evidence-backed analytical report, not a short summary. It contains 5-8 mechanism cards; each card cites two source-specific facts, explains the pressure/reversal/payoff chain and audience psychology, then separates transferable abstraction from the concrete source shell that must be replaced. Run `scripts/validate_source_payoff_analysis.py` before creating topic candidates.

`05_enhanced_outline.md` uses vertical episode cards with three compact groups: `开头与悬念`, `剧情推进`, and `价值与兑现`. Wide multi-column episode tables are rejected because they are hard to review and frequently misalign in Markdown renderers. Run `scripts/validate_enhanced_outline.py` before risk review.

After every batch, create the evidence-backed logic review and run `scripts/run_batch_checks.py --logic-review <review.json>`; it invokes character counting, payoff validation, Chinese-language validation, runtime-density and batch-drift checks, and the strict logic/common-sense gate. It writes `reports/batch_validation.json` and updates the recovery point only when every check passes. Export `final_manuscript.docx` only after the final episode count, `validate_manuscript_quality.py`, `validate_release_consistency.py`, and the final content-risk pass all succeed. Then use `scripts/export_final_docx.py` and `scripts/verify_final_docx.py`, preserving all Markdown and review evidence.

After creating or updating any user-facing artifact, verify the file exists and expose it in the same chat response as a clickable absolute-path Markdown link. During prose drafting, always link `07_manuscript.md`; at completion, link `final_manuscript.docx` plus the principal Markdown sources. Internal implementation details may remain hidden, but project deliverables must never be hidden.
