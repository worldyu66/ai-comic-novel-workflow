# User Guidance Templates

Use these as interaction patterns. Adapt the wording to the actual project, but keep the decision and next action explicit.

## File Delivery Rule

Project artifacts are user deliverables, not internal files. Whenever a milestone file is created or updated, verify that it exists and include a `可查看文件` section in the same reply. In Codex Desktop, use clickable Markdown links whose targets are absolute local paths. Never report only a filename, hide the manuscript behind a progress summary, or claim that content was saved when no file exists.

During drafting, always link the current `07_manuscript.md`. At final delivery, link `final_manuscript.docx` and the Markdown project sources. Other milestone replies should link the files most relevant to the user's current review decision.

Before reporting a drafting batch, require a successful `run_batch_checks.py` result and read the recovery point from `project_state.json`. Before linking the final Word file, require a successful `verify_final_docx.py` result.

If a logic fix would change the core setting, main causal chain, major-character fate, or ending, do not hide the fork inside a progress update. State the exact contradiction, give at most two concrete repair paths, and wait for the user's choice. Local continuity and common-sense defects that preserve locked facts should be fixed and rechecked without interruption.

Example:

```markdown
可查看文件：

- [正文创作稿](<absolute-project-path>/07_manuscript.md)
- [强化大纲](<absolute-project-path>/05_enhanced_outline.md)
```

## After Source Analysis

```text
当前阶段：选题

我已从你上传的素材中深度拆解了 5-8 个核心机制。每个机制都区分了原素材证据、观众心理、爽点运行链、升级方式、可迁移方法和必须替换的具体外壳；接下来会据此给你 5-8 个全新的故事方案。

来源分析已通过深度校验。你现在不需要补充内容，只要从候选方案中选择一个方向即可。

可查看文件：

- [来源与爽点机制深度分析](<absolute-project-path>/01_source_payoff_analysis.md)
```

## After Topic Candidates

```text
当前阶段：选择故事方向

下面是 5-8 个完整候选方案。每个方案都写明了题材类型和一句话故事方向，避免只看标题难以判断内容。

请直接回复“选 01”、题材名称，或“默认”。选择“默认”时，我会采用上方标注“推荐”的方案。

说明：候选方案也已保存到项目文件中，但无需打开文件，你可以直接在这里完成选择。

可查看文件：

- [选题方案](<absolute-project-path>/02_topic_candidates.md)
```

## After Topic Selection: Episode Count and Runtime

Skip this question only when the user already supplied all three values.

```text
当前阶段：确认集数与时长

故事方向已经确定。进入故事设定和大纲前，还需要锁定制作规格：

1. 这部作品大概希望做多少集？可以给一个目标数字，也可以回复“按建议”。默认允许最终集数在目标上下 10% 内浮动；超出前会再次征求你的确认。
2. 第一集希望做多长？可在 1-5 分钟内选择；回复“按建议”时，默认按 3 分钟设计。
3. 成片更接近纯解说旁白、对话剧情，还是复合型？这只用于估算每集需要多少小说正文，不会把正文拆成画面、旁白、对话或音效格式。回复“按建议”时默认按复合型估算。

第 2 集起会根据剧情密度在 1-2 分钟内弹性安排：普通推进偏向 1 分钟，完整冲突、反转或阶段高潮可延长到 1.5-2 分钟。可以直接回复：“24 集，第一集 3 分钟，复合型”。
```


## After Outline Enhancement and Risk Review

```text
当前阶段：强化大纲与审核

我已在原大纲中补强反派压力、泪点和爽点，并按你的审核清单完成风险检查。

强化大纲采用逐集卡片排版，便于在手机和聊天窗口中纵向审阅；不会使用需要横向滚动的宽表格。

若存在高风险内容，我会先重做对应的大纲部分并重新检查，不会直接进入正文。

可查看文件：

- [强化大纲](<absolute-project-path>/05_enhanced_outline.md)
- [风险审核](<absolute-project-path>/06_risk_review.md)
```

## Before Drafting

```text
当前阶段：确认创作蓝图

我已经按“目标约 <target episodes> 集（默认允许 <lower>-<upper> 集）、第一集 <first duration> 分钟、后续按剧情在 1-2 分钟内弹性安排、成片形态为 <video mode>（每分钟小说正文约 <character range> 字）”的制作规格完成故事设定和分集大纲。请确认：故事主线是否保留、使用第一人称还是第三人称、固定跟随哪位视角人物、全剧开篇采用哪种叙述方式、是否接受“第一集强钩子、前 3 集高留存、后续分集钩子类型轮换”的开头设计。全剧开篇仍可选择“剧情开头”或“解说开头”，但无论选择哪种方式，都会在开头尽快进入异常、冲突、危险、身份反差或关键结果。

请同时选择创作节奏：回复“自动分批”时，我会每批写 2-3 集并自动推进；回复“手动继续”时，我会保留你原来的习惯，在每批完成后等待你说“继续”。每集都有开头钩子和观看价值点，爽点按三集与六集节奏窗口安排，并在创作稿中用中文标注；最终 Word 阅读稿会移除这些制作标注。
```

## Batch Progress

```text
当前阶段：正文创作

已完成第 <N> 至 <M> 集，目标约 <target episodes> 集，当前仍在允许区间 <lower>-<upper> 集的规划内；成片形态为 <video mode>，本批各集正文均按对应字符区间、时长规则、视角合同、价值点与爽点节奏检查。累计正文字符数为 <verified count>，仅作为制作记录；已新增的伏笔是：<brief list>；下一批会推进：<brief plan>。

本批逻辑与常识审查已覆盖时间线、人物位置、因果、世界规则、物理常识、年代技术、信息来源、人物动机和后果延续；每个维度均记录了反证挑战及结果；未解决高风险问题：0项。

可查看文件：

- [正文创作稿（已更新至第 <M> 集）](<absolute-project-path>/07_manuscript.md)

我将继续下一批创作；如需改方向，请直接说明要修改的角色、情节或节奏。
```

## Recovery After Interruption

```text
当前阶段：恢复创作

已从项目记录中确认：目标约 <target episodes> 集，默认允许 <lower>-<upper> 集，上次完成第 <N> 集；第一集目标 <first duration> 分钟，后续按剧情在 1-2 分钟内弹性安排。累计正文字符数为 <verified count>，仅作为制作记录；尚未回收的伏笔包括：<brief list>。

可查看文件：

- [正文创作稿（当前恢复点）](<absolute-project-path>/07_manuscript.md)

现在将从第 <N+1> 集开始，按既定大纲和每集爽点计划继续创作。
```
