# Project Layout

Use Markdown files as the editable source of truth:

```text
<project-name>/
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
```

`03_story_bible.md` or its project ledger records the approximate target episode count, the default allowed range, the user-confirmed first-episode duration, and the fixed 1-minute duration for later episodes. `07_manuscript.md` contains the canonical episode prose, Chinese duration/opening-hook/value/payoff annotations, and episode ledger. Each episode places its annotation immediately below the episode title and before a `### 本集正文` heading. Run the installed skill's `scripts/count_chinese_characters.py`, `scripts/validate_episode_payoffs.py`, and `scripts/validate_chinese_manuscript.py` after every drafting batch and before export. Character counts are diagnostic records rather than a completion target. Export `final_manuscript.docx` only after the final episode count falls within the approved range and the final consistency and risk pass succeeds, removing the creative annotations and working-only body subheadings from the clean reading copy. Preserve Markdown files after export so changes remain traceable.

After creating or updating any user-facing artifact, verify the file exists and expose it in the same chat response as a clickable absolute-path Markdown link. During prose drafting, always link `07_manuscript.md`; at completion, link `final_manuscript.docx` plus the principal Markdown sources. Internal implementation details may remain hidden, but project deliverables must never be hidden.
