# 逻辑与常识严格审查合同

逻辑正确性优先于钩子密度、爽点数量和快速续写。大纲、每批正文和终稿都必须审查；任何未解决的高风险问题会阻断批次提交和 Word 导出。

## 修改权限

- 不改变核心设定、主线、人物命运或结局的局部问题：直接修正并复查。
- 会改变时空规则、核心设定、主线因果、主要人物命运或结局的问题：记录两个以内的具体修法，先取得用户确认。
- 不得通过删除关键情节、模糊时间、跳过人物移动或新增万能能力来掩盖冲突。

## 九个强制维度

1. `timeline`：日期、时刻、持续时间、倒计时和跨集时间顺序是否成立。
2. `character_location`：人物怎样到达当前地点或时空；离开和返回是否有场景证据。
3. `causality`：结果是否由已建立的行动、资源和条件导致。
4. `world_rules`：能力、穿越、代价和限制是否持续生效；例外是否提前建立并付出代价。
5. `physical_common_sense`：车辆、伤势、距离、容量、供电、天气和物体受力是否留下合理后果。
6. `era_and_technology`：年代、交通、设备、制度、语言和人物认知是否匹配。
7. `knowledge_state`：人物只能使用已经亲历、听见、读到或被告知的信息。
8. `character_motivation`：关键选择符合人物目标、恐惧、关系和已发生的变化。
9. `consequence_persistence`：车辆损伤、记忆代价、法律后果、关系破裂和资源消耗不会下一集自动消失。

## 审查证据文件

每批生成 `reports/logic_review_<through>.json`，终稿生成 `reports/logic_review_final.json`。每个维度必须写明 `status`、具体集数证据、主动寻找的反例和反证结果。不得只写“已检查”“未发现”或“通过”。

```json
{
  "scope": "episodes_4_6",
  "reviewed_through": 6,
  "dimensions": {
    "timeline": {
      "status": "pass",
      "evidence": "第4-6集发生于同一雨夜，倒计时从22分钟推进至11分钟。",
      "challenge_attempt": "逐集累加移动、交谈和行动用时，检查是否超过既定窗口。",
      "result": "总耗时18分钟，仍在第3集建立的25分钟窗口内。"
    },
    "character_location": {
      "status": "pass",
      "evidence": "人物均由第3集车内进入第4集旧站。",
      "challenge_attempt": "反查每名人物第3集结尾与第4集开头的位置变化。",
      "result": "所有位置变化都有步行、乘车或留守场景，没有跳跃。"
    },
    "causality": {"status": "pass", "evidence": "第3集得到的钥匙触发第5集开门行动。", "challenge_attempt": "尝试移除第3集钥匙，检查第5集行动是否仍能发生。", "result": "移除后行动无法成立，因果依赖明确且已提前建立。"},
    "world_rules": {"status": "pass", "evidence": "跨越规则在第4集继续生效并造成既定代价。", "challenge_attempt": "检查角色是否绕过次数、代价或携带限制。", "result": "第4-6集没有绕过限制，例外均未出现。"},
    "physical_common_sense": {"status": "pass", "evidence": "车辆碰撞后第6集保留车门故障。", "challenge_attempt": "检查撞击、伤势和资源消耗是否在下一集自动消失。", "result": "车门故障和维修行动延续至第6集。"},
    "era_and_technology": {"status": "pass", "evidence": "设备和人物认知符合已锁定年代。", "challenge_attempt": "逐项核对交通、通信和供电设备是否超出时代与角色认知。", "result": "设备均在设定范围内，人物没有使用未知技术。"},
    "knowledge_state": {"status": "pass", "evidence": "主角只使用第3集已公开的线索。", "challenge_attempt": "反查第4-6集每项判断的信息来源。", "result": "所有判断均来自目击、对话或已收到的文件。"},
    "character_motivation": {"status": "pass", "evidence": "选择符合角色卡中的救人目标与失忆恐惧。", "challenge_attempt": "尝试用相反选择替换关键行动，检查是否更符合人物利益。", "result": "相反选择会违背已建立的救人目标与关系承诺。"},
    "consequence_persistence": {"status": "pass", "evidence": "第4集付出的资源与关系代价延续至第6集。", "challenge_attempt": "检查代价是否在下一集无解释恢复。", "result": "资源减少、关系裂痕和身体损伤均保留。"}
  },
  "findings": [],
  "verdict": "pass"
}
```

## 风险等级

- `high`：破坏主线因果、世界规则、人物位置、常识或结局可信度；未解决时阻断。
- `medium`：不立即破坏主线，但会造成明显疑问、动机跳跃或时代违和；进入下一大阶段前解决。
- `low`：措辞、轻微信息重复或可局部修复的问题。

`changes_core_plot: true` 的问题只有在 `status: user_confirmed` 且记录 `user_confirmation` 后才能通过。

## 规则与人物闭环

- 每条核心规则记录：建立集、首次使用、升级集、代价、例外、最终回收证据。
- 每个主要人物记录：初始缺口、关键选择、关系转折、最终行动、结局证据。
- 反派必须形成：目标 → 获利方式 → 执行机制 → 受害后果 → 证据链 → 失败方式 → 失败后状态。
