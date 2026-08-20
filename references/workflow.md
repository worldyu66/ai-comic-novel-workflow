# Workflow Details

## 1. Source Payoff Analysis

Extract high-level, non-protectable patterns: setting category, audience tension, payoff cadence, emotional hooks, conflict sources, chapter momentum, and content-risk signals. The analysis must explicitly identify the source material's 爽点 mechanism: what the audience anticipates, what reversal or reward delivers it, and how frequently the payoff arrives. Do not reproduce a source's named characters, exact scenes, prose, dialogue, or distinctive plot sequence.

## 2. Topic Recommendation Gate

Return 5-8 clearly differentiated original candidates. Each candidate must make the story direction understandable before the user chooses. Display the entire list in the chat reply before mentioning `02_topic_candidates.md`. Use this exact format:

```markdown
### 选项 01｜<topic name>
- 题材类型：<例如都市悬疑、青春穿越、玄幻修仙>
- 一句话故事：<主角、导火索和核心冲突>
- 核心爽点：...
- 目标受众：...
```

Mark exactly one candidate with `**推荐：**` and give one short, concrete reason. Do not use a sentence that names only a number without repeating the genre and one-sentence story direction.

End with this plain-language choice instruction: “请直接回复‘选 01’、题材名称，或‘默认’。选择‘默认’时，我会采用上方标注“推荐”的方案。”

Do not begin a story bible or outline until the user selects a topic. On an explicit default instruction, rank the candidates internally by audience resonance, payoff strength, serialization space, originality, and content risk, then state the chosen genre, topic name, and one-sentence story direction before proceeding.

## 3. World, Identity, and Character Passes

Create the story bible before prose. It must separately include:

- circles, factions, power relationships, and social rules
- protagonist and major-character identity, public position, hidden card, and reveal conditions
- character cards with want, fear, conflict, relationship, emotional wound, and visual continuity

## 4. Core Outline and Conflict Passes

Create the core outline after the story bible. It must specify:

- opening hook and triggering incident
- protagonist goal and opposing force
- escalating reversals and emotional payoffs
- major character arcs and relationship turns
- chapter-by-chapter purpose, planned clue/payoff, and estimated length
- ending resolution and final emotional landing

### Opening-retention pass

Before drafting, design both the whole-story opening and each episode's opening. Episode 1 should enter a high-tension, anomalous, dangerous, emotionally rupturing, or identity-contrasting event immediately; episodes 2-3 should maintain high opening density; later episodes may use quieter information, relationship, or atmosphere hooks when they create a concrete question or change. Rotate among anomaly, result-first reveal, identity contrast, conflict ignition, countdown, relationship rupture, rule/monster oddity, and information reversal. Do not confuse a hook with a payoff: the hook earns the next minute of attention, the episode value point repays attention, and the ending hook creates the next question. Every hook must state its mainline connection and when it will be partially or fully paid off.

## 5. Antagonist, Tears, and Payoff Enhancement

Keep the selected topic and core outline intact, then issue a revised enhanced outline that:

- gives the antagonist a clear pressure strategy and credible motivation
- places planned tears/emotional-release beats at meaningful relationship or moral turning points
- adds earned爽点 through reversals, competence, evidence, accountability, and emotional payoff
- avoids escalating through prohibited humiliation, cruelty, or content-boundary violations

The enhanced outline must include one row per episode:

| 集数 | 开头钩子类型 | 开场事件 | 观众核心疑问 | 钩子强度 | 钩子兑现期限 | 本集目标 | 核心冲突 | 本集价值点 | 价值类型 | 是否明确爽点 | 爽点类型 | 本集兑现 | 观众收益 | 节奏等级 | 集尾钩子 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Every episode needs an audience value point, but it does not need a conventional爽点. A value point may be a爽点、泪点、甜点、惊点、笑点或关键信息. Across any three consecutive episodes, at least one must contain an explicit爽点. Across any six consecutive episodes, at least one must be `强兑现` or `阶段高潮`. The payoff and ending hook remain separate: first give the audience a meaningful return, then create the next question.

## 6. Risk Review and Outline Rework Loop

Review `05_enhanced_outline.md` against the supplied content-boundary checklist. Classify every finding as Low, Medium, or High.

- 低风险：记录后继续。
- 中风险：给出具体修改方向，并在进入正文前完成必要调整。
- 高风险：重写对应大纲部分，输出新版强化大纲，再次审核。

Do not proceed to prose when a High finding remains unless the user explicitly asks to accept that residual risk.

## 7. Combined Creative Confirmation

Ask for one combined creative confirmation. It must state in plain Chinese:

- the chosen story direction and ending target
- the narrative point of view, with first person as the default
- 开头模式：`剧情开头`（直接进入高张力场面）或 `解说开头`（用简短的第一人称钩子开场，再进入场面）
- 续写模式：`自动分批`（默认，每批 2-3 集）或 `手动继续`（保留原来的“继续”命令）
- that confirmation starts the selected drafting mode

Incorporate requested changes, then lock the working version and retain an explicit change log.

## 8. Drafting and Optional Interest Passes

Draft 2-3 episodes per batch. In `自动分批` mode, proceed to the next batch after the status update. In `手动继续` mode, wait for “继续” before proceeding.

Use the optional original interest passes only when they fit the selected topic and user intent: tasteful meme integration, situational comedy, and date-stamped trend references. These passes must never override continuity, audience fit, or content boundaries.

Each episode uses this Chinese working-manuscript order so the user can review the opening retention plan and the episode value before reading the prose:

```markdown
## 第 N 集：标题

### 本集创作标注

- 开头钩子类型：反常型 / 结果前置型 / 身份反差型 / 冲突爆发型 / 危机倒计时型 / 关系破裂型 / 规则怪诞型 / 信息颠覆型
- 钩子强度：强钩子 / 中钩子 / 基础钩子
- 开场事件：...
- 观众立即知道：...
- 观众核心疑问：...
- 钩子与主线关系：...
- 钩子本集推进：...
- 钩子完全兑现期限：本集内 / 下一集内 / 两集内 / <具体阶段或集数>
- 与上一集衔接：<第一集填写“首集开篇”>
- 开头质量评分：<0-10分；第一集至少9分，第2-3集至少8分，其后至少7分>
- 开头评分理由：<即时性、清晰度、异常度、主线关联、追看欲>
- 本集摘要：...
- 本集价值点：...
- 价值类型：爽点 / 泪点 / 甜点 / 惊点 / 笑点 / 信息点
- 是否明确爽点：是 / 否
- 爽点类型：<没有明确爽点时填写“无”>
- 铺垫与触发：...
- 本集兑现：...
- 观众情绪收益：...
- 节奏等级：蓄势 / 小兑现 / 强兑现 / 阶段高潮
- 下一集钩子：...
- 本集正文字符数：...
- 累计正文字符数：...

### 本集正文

<本集正文>
```

Before starting a batch, review chronology, character motivation, open clues, length budget, boundary risks, and the value row for every planned episode. Reject and rewrite an episode when it has no audience value, when two consecutive episodes are only buildup, when a three-episode window lacks an explicit爽点, when a six-episode window lacks a strong payoff, or when repeated爽点 do not escalate.

After drafting, review the opening separately. Reject and rewrite an opening when it delays the first meaningful event with exposition, relies on an unrelated shock, offers no concrete audience question, has no mainline connection, or repeatedly uses the same hook type without escalation. The score is a creative review aid; the validator checks its presence and thresholds but cannot replace semantic judgment.

After writing the batch, run:

```powershell
python scripts/count_chinese_characters.py 07_manuscript.md
python scripts/validate_episode_payoffs.py 07_manuscript.md
python scripts/validate_chinese_manuscript.py 07_manuscript.md
```

Copy verified values into the episode ledger. If payoff validation fails, fix the missing or incomplete episode annotation before continuing. If the Chinese-language audit finds accidental English, replace it with natural Chinese unless it is a necessary proper noun explicitly allowed by the user. If the response or session is interrupted, save the updated Markdown files before reporting status. A later request such as “继续创作” or “从第 8 集恢复” must begin by reading the ledger, state the exact recovery point, then continue with the next planned batch.

## 9. Quality, Polish, and Release Pass

When the full manuscript is drafted:

1. Check all setup/payoff pairs and timeline order.
2. Check each major character's motivation, arc, name, and visual continuity.
3. Check episode length balance, total length, and payoff-type repetition.
4. Run the supplied content-boundary review.
5. Run a prose polish pass without changing established plot facts.
6. Create title and opening-hook options that accurately represent the completed novel.
7. Produce character and scene prompt packs from the final manuscript, not from an obsolete outline.
8. Export `final_manuscript.docx` from the reviewed Markdown manuscript, removing every `本集创作标注` block and the working-only `本集正文` subheading from the clean reading copy.
