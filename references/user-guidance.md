# User Guidance Templates

Use these as interaction patterns. Adapt the wording to the actual project, but keep the decision and next action explicit.

## File Delivery Rule

Project artifacts are user deliverables, not internal files. Whenever a milestone file is created or updated, verify that it exists and include a `可查看文件` section in the same reply. In Codex Desktop, use clickable Markdown links whose targets are absolute local paths. Never report only a filename, hide the manuscript behind a progress summary, or claim that content was saved when no file exists.

During drafting, always link the current `07_manuscript.md`. At final delivery, link `final_manuscript.docx` and the Markdown project sources. Other milestone replies should link the files most relevant to the user's current review decision.

Example:

```markdown
可查看文件：

- [正文创作稿](<absolute-project-path>/07_manuscript.md)
- [强化大纲](<absolute-project-path>/05_enhanced_outline.md)
```

## After Source Analysis

```text
当前阶段：选题

我已从你上传的素材中提取了可复用的题材方向、爽点机制和受众偏好，接下来会给你 5-8 个全新的故事方案。

你现在不需要补充内容，只要从候选方案中选择一个方向即可。
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

Skip this question only when the user already supplied both values.

```text
当前阶段：确认集数与时长

故事方向已经确定。进入故事设定和大纲前，还需要锁定制作规格：

1. 这部作品大概希望做多少集？可以给一个目标数字，也可以回复“按建议”。默认允许最终集数在目标上下 10% 内浮动；超出前会再次征求你的确认。
2. 第一集希望做多长？可在 1-5 分钟内选择；回复“按建议”时，默认按 3 分钟设计。

第 2 集起固定按每集 1 分钟设计。可以直接回复：“24 集，第一集 3 分钟”。
```


## After Outline Enhancement and Risk Review

```text
当前阶段：强化大纲与审核

我已在原大纲中补强反派压力、泪点和爽点，并按你的审核清单完成风险检查。

若存在高风险内容，我会先重做对应的大纲部分并重新检查，不会直接进入正文。

可查看文件：

- [强化大纲](<absolute-project-path>/05_enhanced_outline.md)
- [风险审核](<absolute-project-path>/06_risk_review.md)
```

## Before Drafting

```text
当前阶段：确认创作蓝图

我已经按“目标约 <target episodes> 集（默认允许 <lower>-<upper> 集）、第一集 <first duration> 分钟、后续每集 1 分钟”的制作规格完成故事设定和分集大纲。请确认四件事：故事主线是否保留、使用第一人称还是第三人称、全剧开篇采用哪种叙述方式、是否接受“第一集强钩子、前 3 集高留存、后续分集钩子类型轮换”的开头设计。全剧开篇仍可选择“剧情开头”或“解说开头”，但无论选择哪种方式，都会在开头尽快进入异常、冲突、危险、身份反差或关键结果。

请同时选择创作节奏：回复“自动分批”时，我会每批写 2-3 集并自动推进；回复“手动继续”时，我会保留你原来的习惯，在每批完成后等待你说“继续”。每集都有开头钩子和观看价值点，爽点按三集与六集节奏窗口安排，并在创作稿中用中文标注；最终 Word 阅读稿会移除这些制作标注。
```

## Batch Progress

```text
当前阶段：正文创作

已完成第 <N> 至 <M> 集，目标约 <target episodes> 集，当前仍在允许区间 <lower>-<upper> 集的规划内；第一集和后续单集时长规则、本批价值点与爽点节奏均已检查。累计正文字符数为 <verified count>，仅作为制作记录；已新增的伏笔是：<brief list>；下一批会推进：<brief plan>。

可查看文件：

- [正文创作稿（已更新至第 <M> 集）](<absolute-project-path>/07_manuscript.md)

我将继续下一批创作；如需改方向，请直接说明要修改的角色、情节或节奏。
```

## Recovery After Interruption

```text
当前阶段：恢复创作

已从项目记录中确认：目标约 <target episodes> 集，默认允许 <lower>-<upper> 集，上次完成第 <N> 集；第一集目标 <first duration> 分钟，后续每集 1 分钟。累计正文字符数为 <verified count>，仅作为制作记录；尚未回收的伏笔包括：<brief list>。

可查看文件：

- [正文创作稿（当前恢复点）](<absolute-project-path>/07_manuscript.md)

现在将从第 <N+1> 集开始，按既定大纲和每集爽点计划继续创作。
```
