# Workflow Details

## 1. Front-Light but Deep Joint Source Mechanism Analysis

Create `01_source_payoff_analysis.md` as a joint report. “Front-light” limits premature **new-story design**; it does not permit shallow source analysis.

- `ag_001 赛道分析师` leads a source-specific analysis of track position, target audience, viewing desires, emotional curve, serialization engine, episode momentum, adaptation strengths, and content/logic risks.
- `ag_006 冲突&打脸设计师` analyzes 5-8 core conflict/payoff mechanisms in depth. It may name source characters, objects, and events as analytical evidence. That evidence is not permission to reuse them in the original project.
- Every mechanism must explain what happens in the source, why it creates pleasure, how pressure turns into reversal and payoff, how it escalates, what abstract mechanism transfers, and which concrete shell must be replaced.
- Joint synthesis must separate `素材证据` from `可迁移机制`, then connect audience expectation → pressure → reversal/reward → emotional return → serialization potential.

The front-light `ag_006` pass must not invent the new project's named characters, antagonist plan, scene sequence, episode events, dialogue, or locked plot. Those decisions belong to the back-heavy pass after topic selection and the core outline. Source-specific names and events may appear only under analytical evidence; never present them as reusable story assets.

Use this contract. Write 5-8 mechanism cards and normally reach 1500-2500 Chinese characters when the source contains enough material:

```markdown
## ag_001｜赛道与受众深度分析
- 赛道定位：...
- 目标受众：...
- 核心观看欲望：...
- 情绪曲线：...
- 连载驱动力：...
- 单集推进特征：...
- 漫剧适配优势：...
- 内容与逻辑风险：...

## ag_006（前轻后重·本阶段只分析）｜冲突与爽点机制

### 机制 01｜<机制名称>
- 素材证据一：<原素材中的具体人物、物品、选择或事件>
- 素材证据二：<另一个具体证据>
- 运行链：<铺垫 → 施压 → 反转 → 兑现>
- 观众心理：<满足何种欲望，为什么有效>
- 核心反差：...
- 升级阶梯：...
- 兑现频率：...
- 可迁移机制：<抽象方法，不含原作专属外壳>
- 必须替换外壳：<人物、物品组合、场景、桥段顺序、台词等>
- 逻辑与审美风险：...

<重复至机制 05-08>

## 联合结论｜原创转化边界
- 最值得保留的受众机制：...
- 不应照搬的辨识度元素：...
- 原创转化原则：...
- 可衍生的差异化题材方向：...
- 对下一步选题的约束：...
```

Before creating `02_topic_candidates.md`, run:

```powershell
python scripts/validate_source_payoff_analysis.py 01_source_payoff_analysis.md
```

A report that merely fills one sentence per field, contains fewer than five mechanism cards, lacks two source-specific evidence points per mechanism, or stays below 1500 Chinese characters when the source is substantial must be expanded before topic recommendation.

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

## 3. Episode Count and Runtime Gate

After topic selection and before the story bible, apply [duration planning](duration-planning.md). Confirm an approximate target episode count, the first-episode target duration, and one video form: pure narration, dialogue drama, or hybrid. The first episode must be no longer than 5 minutes; every later episode uses a plot-first target within 1-2 minutes. Estimate only the required ordinary-novel body characters from the confirmed form; never split prose into visual, narration, dialogue, sound, shot, or pause tracks. If the user already supplied all three values, record them without asking again. Do not use a total word or character target as the completion contract.

After confirmation, initialize the project state before creating the story bible:

```powershell
python scripts/project_state.py init <project-dir> --target-episodes <目标集数> --first-episode-minutes <首集分钟数> --video-mode hybrid --draft-mode auto_batch
```

Use `manual_continue` instead when selected. `project_state.json` is the only authoritative recovery point; prose summaries and ledgers are explanatory views.

## 4. World, Identity, and Character Passes

Create the story bible before prose. It must separately include:

- circles, factions, power relationships, and social rules
- protagonist and major-character identity, public position, hidden card, and reveal conditions
- character cards with want, fear, conflict, relationship, emotional wound, and visual continuity
- a timeline and location baseline, including how long travel and major actions take
- a world-rule lifecycle for every extraordinary rule: setup, use, escalation, cost, exception, and planned payoff
- a knowledge-state baseline for what each major character knows and how they learned it
- a character-arc closure plan and the antagonist causal chain: goal, benefit, mechanism, victim impact, evidence, defeat, aftermath

## 5. Core Outline and Conflict Passes

Create the core outline after the story bible. It must specify:

- opening hook and triggering incident
- protagonist goal and opposing force
- escalating reversals and emotional payoffs
- major character arcs and relationship turns
- episode-by-episode purpose, planned clue/payoff, and target runtime
- ending resolution and final emotional landing

### Opening-retention pass

Before drafting, design both the whole-story opening and each episode's opening. Episode 1 should enter a high-tension, anomalous, dangerous, emotionally rupturing, or identity-contrasting event immediately; episodes 2-3 should maintain high opening density; later episodes may use quieter information, relationship, or atmosphere hooks when they create a concrete question or change. Rotate among anomaly, result-first reveal, identity contrast, conflict ignition, countdown, relationship rupture, rule/monster oddity, and information reversal. Do not confuse a hook with a payoff: the hook earns the next minute of attention, the episode value point repays attention, and the ending hook creates the next question. Every hook must state its mainline connection and when it will be partially or fully paid off.

## 6. Back-Heavy Antagonist, Conflict, Tears, and Payoff Enhancement

After the selected topic, story bible, and core outline are locked, run the full back-heavy `ag_006 冲突&打脸设计师` pass. Keep the selected topic and core outline intact, then issue a revised enhanced outline that:

- gives the antagonist a clear pressure strategy and credible motivation
- places planned tears/emotional-release beats at meaningful relationship or moral turning points
- adds earned爽点 through reversals, competence, evidence, accountability, and emotional payoff
- avoids escalating through prohibited humiliation, cruelty, or content-boundary violations

The enhanced outline must use one vertical card per episode. Do not use a wide episode table. Use this exact card contract:

```markdown
## 第 01 集｜<目标时长>｜<节奏等级>

### 开头与悬念

- 目标时长：...
- 开头钩子类型：...
- 开场事件：...
- 观众核心疑问：...
- 钩子强度：...
- 钩子兑现期限：...

### 剧情推进

- 本集目标：...
- 核心冲突：...

### 价值与兑现

- 本集价值点：...
- 价值类型：...
- 是否明确爽点：...
- 爽点类型：...
- 本集兑现：...
- 观众收益：...
- 节奏等级：...
- 集尾钩子：...
```

After writing or revising the enhanced outline, run:

```powershell
python scripts/validate_enhanced_outline.py 05_enhanced_outline.md --target-episodes <目标集数>
```

Then apply [logic and common-sense review](logic-common-sense-review.md) across all planned episodes. Resolve local defects immediately. When a fix changes the core setting, main causal chain, major-character fate, or ending, stop and ask the user to choose before locking the outline.

Every episode needs an audience value point, but it does not need a conventional爽点. A value point may be a爽点、泪点、甜点、惊点、笑点或关键信息. Across any three consecutive episodes, at least one must contain an explicit爽点. Across any six consecutive episodes, at least one must be `强兑现` or `阶段高潮`. The payoff and ending hook remain separate: first give the audience a meaningful return, then create the next question.

## 7. Risk Review and Outline Rework Loop

Only after the episode-card validator passes, review `05_enhanced_outline.md` against the supplied content-boundary checklist. Classify every finding as Low, Medium, or High.

- 低风险：记录后继续。
- 中风险：给出具体修改方向，并在进入正文前完成必要调整。
- 高风险：重写对应大纲部分，输出新版强化大纲，再次审核。

Do not proceed to prose when a High finding remains unless the user explicitly asks to accept that residual risk.

## 8. Combined Creative Confirmation

Ask for one combined creative confirmation. It must state in plain Chinese:

- the chosen story direction and ending target
- the approximate target episode count, its default allowed range, the confirmed first-episode duration, and the plot-first 1-2 minute range for every later episode
- the confirmed video form and its novel-character-per-minute estimate band
- the narrative point of view, with first person as the default, plus the exact viewpoint character whose perceptions and knowledge constrain the narration
- 开头模式：`剧情开头`（直接进入高张力场面）或 `解说开头`（用简短的第一人称钩子开场，再进入场面）
- 续写模式：`自动分批`（默认，每批 2-3 集）或 `手动继续`（保留原来的“继续”命令）
- that confirmation starts the selected drafting mode

Incorporate requested changes, then lock the working version and retain an explicit change log.

## 9. Drafting and Optional Interest Passes

Draft 2-3 episodes per batch. In `自动分批` mode, proceed after a successful saved-and-validated status update, but generate at most two batches in one response. In `手动继续` mode, wait for “继续” before proceeding. Any failed check stops the run at the last validated recovery point.

Use the optional original interest passes only when they fit the selected topic and user intent: tasteful meme integration, situational comedy, and date-stamped trend references. These passes must never override continuity, audience fit, or content boundaries.

Each episode uses this Chinese working-manuscript order so the user can review the opening retention plan and the episode value before reading the prose:

```markdown
## 第 N 集：标题

### 本集创作标注

- 开头钩子类型：反常型 / 结果前置型 / 身份反差型 / 冲突爆发型 / 危机倒计时型 / 关系破裂型 / 规则怪诞型 / 信息颠覆型
- 钩子强度：强钩子 / 中钩子 / 基础钩子
- 目标时长：<第一集填写已确认的 1-5 分钟；其后根据本集剧情填写 1-2 分钟内的具体时长>
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

Before starting a batch, review chronology, character locations, travel time, knowledge state, world-rule limits, persistent physical consequences, character motivation, open clues, runtime budget, boundary risks, and the value card for every planned episode. Reject and rewrite an episode when it breaks causality or common sense, lets a character teleport or use unknown information, silently drops a consequence, has too many primary tasks for its runtime, has no audience value, when two consecutive episodes are only buildup, when a three-episode window lacks an explicit爽点, when a six-episode window lacks a strong payoff, or when repeated爽点 do not escalate.

After drafting, review the opening separately. Reject and rewrite an opening when it delays the first meaningful event with exposition, relies on an unrelated shock, offers no concrete audience question, has no mainline connection, or repeatedly uses the same hook type without escalation. The score is a creative review aid; the validator checks its presence and thresholds but cannot replace semantic judgment.

After writing the batch, create `reports/logic_review_<through>.json` using the nine dimensions in [logic and common-sense review](logic-common-sense-review.md). Every dimension must record the evidence, a concrete attempt to disprove the story's logic, and the result; “已检查” or “未发现问题” is not evidence. Then run the transactional command:

```powershell
python scripts/run_batch_checks.py 07_manuscript.md project_state.json --through <当前最后集数> --logic-review reports/logic_review_<当前最后集数>.json
```

The command invokes language, payoff, runtime-density, batch-drift, and logic-review validators, writes `reports/batch_validation.json`, and atomically updates `project_state.json` only after every check succeeds. Character counts remain diagnostic records, not a total-length target. Record allowed proper nouns with `project_state.py allow-term`. If interrupted, preserve the last validated state. A later request such as “继续创作” or “从第 8 集恢复” must first run `python scripts/project_state.py resume project_state.json`, state the exact recovery point and any unresolved logic risks, then continue.

Before final export, run `python scripts/validate_episode_payoffs.py 07_manuscript.md --target-episodes <目标集数> --require-complete`. The default tolerance is +/-10%, with a minimum allowance of one episode. Do not release a manuscript outside that range unless the user has approved a new target and the project ledger records the change.

## 10. Quality, Polish, and Release Pass

When the full manuscript is drafted:

1. Run a final nine-dimension logic/common-sense review across the entire manuscript, with special attention to cross-batch transitions.
2. Check all setup/payoff pairs, timeline order, character locations, knowledge sources, world-rule costs, physical consequences, and historical/technical common sense.
3. Check each major character's motivation, arc, name, visual continuity, final action, and ending state.
4. Check the antagonist's complete causal chain and post-defeat state.
5. Check completion against the approved episode-count range, runtime density, long-form drift, and payoff-type repetition.
6. Run the supplied content-boundary review.
7. Run a prose polish pass without changing established plot facts.
8. Create title and opening-hook options that accurately represent the completed novel.
9. Produce character and scene prompt packs from the final manuscript, not from an obsolete outline.
10. Run the release gates, then export and verify the final Word file:

   ```powershell
   python scripts/validate_manuscript_quality.py 07_manuscript.md --state project_state.json --report reports/manuscript_quality.json
   python scripts/validate_narrative_contract.py 07_manuscript.md project_state.json --release-notes 10_release_polish.md --report reports/narrative_contract.json
   python scripts/validate_release_consistency.py 07_manuscript.md project_state.json reports/logic_review_final.json
   python scripts/export_final_docx.py 07_manuscript.md final_manuscript.docx --title "<作品名>"
   python scripts/verify_final_docx.py 07_manuscript.md final_manuscript.docx
   ```

   The exporter reads only each `### 本集正文` section. The verifier must confirm episode count, body preservation, and removal of working labels before delivery. Render the DOCX to pages and visually inspect every page when the document runtime is available.
