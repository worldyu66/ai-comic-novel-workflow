from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
SUBPROCESS_ENV = {**os.environ, "PYTHONIOENCODING": "utf-8"}


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


COUNT = load_module("count_chinese_characters", SCRIPTS / "count_chinese_characters.py")
STATE = load_module("project_state", SCRIPTS / "project_state.py")
OUTLINE_CONVERTER = load_module("convert_enhanced_outline", SCRIPTS / "convert_enhanced_outline.py")
OUTLINE_VALIDATOR = load_module("validate_enhanced_outline", SCRIPTS / "validate_enhanced_outline.py")
QUALITY = load_module("validate_manuscript_quality", SCRIPTS / "validate_manuscript_quality.py")
LOGIC = load_module("validate_logic_review", SCRIPTS / "validate_logic_review.py")
ESTIMATOR = load_module("estimate_novel_word_count", SCRIPTS / "estimate_novel_word_count.py")
NARRATIVE = load_module("validate_narrative_contract", SCRIPTS / "validate_narrative_contract.py")
SOURCE_ANALYSIS = load_module("validate_source_payoff_analysis", SCRIPTS / "validate_source_payoff_analysis.py")
PROMPT_DELIVERABLES = load_module("validate_prompt_deliverables", SCRIPTS / "validate_prompt_deliverables.py")


ANNOTATION = """### 本集创作标注

- 开头钩子类型：冲突爆发型
- 钩子强度：强钩子
- 目标时长：3分钟
- 开场事件：门被撞开
- 观众立即知道：主角被追捕
- 观众核心疑问：谁在追捕
- 钩子与主线关系：引出主线
- 钩子本集推进：发现证据
- 钩子完全兑现期限：下一集内
- 与上一集衔接：首集开篇
- 开头质量评分：9分
- 开头评分理由：冲突直接
- 本集摘要：主角逃离
- 本集价值点：找到证据
- 价值类型：爽点
- 是否明确爽点：是
- 爽点类型：智取
- 铺垫与触发：门外脚步
- 本集兑现：成功脱身
- 观众情绪收益：紧张释放
- 节奏等级：强兑现
- 下一集钩子：证据指向熟人
- 本集正文字符数：11
- 累计正文字符数：11
"""


def manuscript(body: str = "门被撞开，我翻窗逃走。") -> str:
    return f"""# 项目台账

| 字段 | 值 |
| --- | --- |
| 目标集数 | 24 |

## 第 1 集：测试

{ANNOTATION}
### 本集正文

{body}
"""


def two_episode_manuscript(second_duration: str) -> str:
    second_annotation = ANNOTATION.replace("- 目标时长：3分钟", f"- 目标时长：{second_duration}分钟")
    second_annotation = second_annotation.replace("- 与上一集衔接：首集开篇", "- 与上一集衔接：承接证据线索")
    return manuscript() + f"""
## 第 2 集：证据

{second_annotation}
### 本集正文

证据背面，写着熟人的名字。
"""


def logic_review(through: int, findings: list[dict] | None = None, scope: str | None = None) -> dict:
    dimensions = {
        name: {
            "status": "pass",
            "evidence": f"截至第{through}集的具体事实与集数证据",
            "challenge_attempt": f"尝试构造{name}上的反例并回查前后事件",
            "result": f"反例未成立，相关行为与第{through}集证据一致",
        }
        for name in LOGIC.REQUIRED_DIMENSIONS
    }
    return {
        "scope": scope or f"episodes_1_{through}",
        "reviewed_through": through,
        "dimensions": dimensions,
        "findings": findings or [],
        "verdict": "pass",
    }


def deep_source_analysis(mechanisms: int = 5) -> str:
    cards = []
    for index in range(1, mechanisms + 1):
        cards.append(f"""### 机制 {index:02d}｜资源反差与能力兑现
- 素材证据一：原素材第{index}阶段让主人公使用普通工具解决长期缺水危机，旁观者因此改变判断。
- 素材证据二：随后主人公把另一种常见资源投入生产恢复，让受助群体获得持续生存能力。
- 运行链：先展示资源断绝造成的明确压力，再让旧办法失败，随后引入可验证的新工具并当场兑现结果。
- 观众心理：观众既获得解决难题的能力满足，也通过弱者命运被改变而获得安全感和掌控感。
- 核心反差：一方习以为常的普通资源，在另一方的匮乏环境中具有改变秩序的稀缺价值。
- 升级阶梯：个人获救逐步升级为群体恢复、组织协作和制度改变，每次升级都增加成本与责任。
- 兑现频率：首次危机立即兑现，后续每两至三次推进完成一次能力验证，并在阶段节点改变格局。
- 可迁移机制：保留资源认知差、验证过程和渐进式能力升级，但重新设计资源类型与交换代价。
- 必须替换外壳：替换原素材人物身份、具体工具组合、危机场景、事件顺序、称谓和标志性对白。
- 逻辑与审美风险：需要说明运输、维护、知识转化和组织成本，避免资源无限与单向崇拜削弱人物主体性。
""")
    return """# 来源素材：受众与爽点机制分析

## ag_001｜赛道与受众深度分析
- 赛道定位：这是依靠环境资源差制造连续解决方案的成长经营赛道，核心不是某件道具而是能力兑现。
- 目标受众：主要面向偏好快速解题、资源经营、关系回报与阶段翻盘的短剧和漫剧观众群体。
- 核心观看欲望：观众希望持续看到绝境被具体办法解除，并看到主角能力获得承认且带来长期改变。
- 情绪曲线：先制造匮乏和倒计时压力，再通过小规模验证释放紧张，随后扩大成果并引出更高代价。
- 连载驱动力：新问题不断暴露资源、知识与组织瓶颈，旧方案升级后又会改变利益关系并产生新阻力。
- 单集推进特征：单集集中完成一个明确任务，先给可见危机，再展示验证过程和结果，结尾抛出升级问题。
- 漫剧适配优势：物资落地、群体反应和前后环境变化都具有清晰视觉反差，也便于形成短集即时回报。
- 内容与逻辑风险：必须限制资源通道和解决速度，补足运输维护、知识应用、利益冲突与长期社会后果。

## ag_006（前轻后重·本阶段只分析）｜冲突与爽点机制

""" + "\n".join(cards) + """
## 联合结论｜原创转化边界
- 最值得保留的受众机制：保留绝境压力、能力验证、资源反差、阶段兑现与格局升级形成的连续情绪回报。
- 不应照搬的辨识度元素：不沿用原素材人物关系、入口设定、工具组合、战争场面、称谓体系和事件顺序。
- 原创转化原则：先抽取观众期待和运行链，再更换世界条件、资源约束、人物目标、交换代价与最终选择。
- 可衍生的差异化题材方向：可以转向灾后社区、深海基地、边城医工、荒岛自治或志怪司法等不同环境。
- 对下一步选题的约束：候选方向必须保留可验证的能力兑现，同时为资源使用设置代价并保证角色主动性。
"""
class WorkflowScriptTests(unittest.TestCase):
    def test_final_delivery_link_contract_prevents_duplicate_docx_targets(self):
        guidance = (ROOT / "references" / "user-guidance.md").read_text(encoding="utf-8")
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("forward slashes (`C:/...`)", guidance)
        self.assertIn("Cite the DOCX exactly once", guidance)
        self.assertIn("do not place a normal Markdown link to the same DOCX", guidance)
        self.assertIn("Emit the final DOCX exactly once", skill)

    def test_front_light_back_heavy_role_split_is_explicit(self):
        workflow = (ROOT / "references" / "workflow.md").read_text(encoding="utf-8")
        self.assertIn("ag_001 赛道分析师", workflow)
        self.assertIn("ag_006 冲突&打脸设计师", workflow)
        self.assertIn("front-light", workflow)
        self.assertIn("back-heavy", workflow)
        self.assertIn("must not invent the new project's named characters", workflow)

    def test_source_analysis_requires_five_deep_evidence_backed_mechanisms(self):
        shallow = """## ag_001｜赛道与受众机制
- 赛道类型：跨世界经营
## ag_006（轻量）｜冲突与爽点机制
- 爽点触发：资源落地
## 联合结论｜可迁移机制
- 应保留的机制：资源反差
"""
        failures = SOURCE_ANALYSIS.validate(shallow)
        self.assertTrue(any("中文字符数" in item for item in failures))
        self.assertTrue(any("5-8" in item for item in failures))
        self.assertEqual(SOURCE_ANALYSIS.validate(deep_source_analysis()), [])

    def test_enhanced_outline_table_converts_to_valid_cards(self):
        header = "| " + " | ".join(OUTLINE_CONVERTER.EXPECTED_COLUMNS) + " |"
        separator = "| " + " | ".join(["---"] * 16) + " |"
        row1 = "| 1 | 5分钟 | 异常型 | 夜车驶入旧街 | 车外为何变了 | 强钩子 | 本集内 | 接住少女 | 是否开门 | 首次救援 | 惊点 | 是 | 危机逆转 | 少女上车 | 立刻入戏 | 强兑现 | 北堤会决口 |"
        row2 = "| 2 | 1.5分钟 | 泪点型 | 父亲留言响起 | 主角会否继续 | 强钩子 | 本集内 | 作出选择 | 记忆与救人 | 父亲支持 | 泪点 | 是 | 情感托举 | 再次发车 | 情绪释放 | 阶段高潮 | 车票发亮 |"
        source = "# 强化大纲\n\n" + "\n".join((header, separator, row1, row2)) + "\n"
        self.assertTrue(OUTLINE_VALIDATOR.validate(source))
        converted = OUTLINE_CONVERTER.convert(source)
        self.assertNotIn("| 集数 |", converted)
        self.assertIn("## 第 01 集｜5分钟｜强兑现", converted)
        self.assertIn("- 开头钩子类型：反常型", converted)
        self.assertIn("- 开头钩子类型：关系破裂型", converted)
        self.assertEqual(OUTLINE_VALIDATOR.validate(converted, 2), [])

    def test_count_excludes_project_ledger_and_annotations(self):
        sections = COUNT.prose_sections(manuscript())
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0][0], "第 1 集：测试")
        self.assertNotIn("目标集数", sections[0][1])
        self.assertEqual(COUNT.count_non_whitespace(sections[0][1]), 11)

    def test_state_round_trip_and_resume_point(self):
        state = STATE.new_state(24, 3, "auto_batch")
        self.assertEqual(state["allowed_episode_range"], [21, 27])
        self.assertEqual(state["later_episode_minutes_range"], [1, 2])
        state["completed_through"] = 3
        state["next_episode"] = 4
        self.assertEqual(STATE.validate_state(state), [])

    def test_v1_state_migrates_to_flexible_duration_range(self):
        with tempfile.TemporaryDirectory() as temp:
            state_path = Path(temp) / "project_state.json"
            legacy = STATE.new_state(24, 3, "auto_batch")
            legacy["schema_version"] = 1
            legacy.pop("later_episode_minutes_range")
            legacy["later_episode_minutes"] = 1
            state_path.write_text(json.dumps(legacy, ensure_ascii=False), encoding="utf-8")
            migrated = STATE.load_state(state_path)
            self.assertEqual(migrated["schema_version"], 5)
            self.assertEqual(migrated["later_episode_minutes_range"], [1, 2])
            self.assertEqual(migrated["logic_review_mode"], "strict")
            self.assertEqual(migrated["video_runtime_mode"], "hybrid")
            self.assertEqual(migrated["novel_characters_per_minute_range"], [350, 450])
            self.assertEqual(migrated["validation_status"], "not_run")

    def test_complete_state_requires_release_receipt_and_all_artifact_hashes(self):
        state = STATE.new_state(15, 3, "auto_batch")
        state["stage"] = "complete"
        state["validation_status"] = "passed"
        failures = STATE.validate_state(state)
        self.assertTrue(any("发布字段" in item for item in failures))
        state["release_receipt"] = "reports/release_receipt.json"
        state["release_manuscript_sha256"] = "a" * 64
        state["release_character_prompts_sha256"] = "b" * 64
        state["release_scene_prompts_sha256"] = "c" * 64
        state["release_docx_sha256"] = "d" * 64
        self.assertEqual(STATE.validate_state(state), [])

    def test_prompt_delivery_gate_requires_both_real_prompt_packs(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            characters = root / "08_character_prompts.md"
            scenes = root / "09_key_scene_prompts.md"
            failures, _ = PROMPT_DELIVERABLES.validate(characters, scenes)
            self.assertTrue(any("缺少人物提示词" in item for item in failures))
            characters.write_text(
                "## 人物：沈知微｜身份：社区档案员\n\n"
                "**身份锚点：** 三十岁，短发，灰色工作外套\n"
                "**外貌确认提示词：** 克制沉静的女性档案员\n"
                "**连续性说明：** 短发与工作证保持一致\n",
                encoding="utf-8",
            )
            scenes.write_text(
                "## 场景：雨夜来信｜对应集数：1\n\n"
                "**剧情作用：** 建立跨时空邮路\n"
                "**场景确认提示词（16:9）：** 暴雨旧邮局内，女主接住泛黄信封，中景，冷暖对比光\n"
                "**人物连续性：** 沿用沈知微短发与灰色工作外套\n",
                encoding="utf-8",
            )
            failures, counts = PROMPT_DELIVERABLES.validate(characters, scenes)
            self.assertEqual(failures, [])
            self.assertEqual(counts, {"characters": 1, "scenes": 1})

    def test_video_modes_estimate_three_minute_novel_body_ranges(self):
        self.assertEqual(ESTIMATOR.estimate("pure_narration", 3)["target_novel_characters_range"], [990, 1500])
        self.assertEqual(ESTIMATOR.estimate("dialogue_drama", 3)["target_novel_characters_range"], [1080, 1320])
        self.assertEqual(ESTIMATOR.estimate("hybrid", 3)["target_novel_characters_range"], [1050, 1350])

    def test_quality_gate_detects_runtime_extremes_and_tail_collapse(self):
        records = [
            {"index": i + 1, "characters_per_minute": cpm, "duration_minutes": 1, "body_characters": cpm}
            for i, cpm in enumerate([260, 250, 270, 255, 265, 250, 140, 130, 120, 110, 100, 105])
        ]
        failures, report = QUALITY.evaluate(records, 160, 380, 35, 3)
        self.assertFalse(report["passed"])
        self.assertTrue(any("低于下限" in item for item in failures))
        self.assertTrue(any("长篇前后密度显著下降" in item for item in failures))

    def test_core_logic_change_requires_user_confirmation(self):
        finding = {
            "id": "logic-001",
            "severity": "high",
            "category": "world_rules",
            "description": "修复会改变穿越规则",
            "evidence": "第3集与第4集规则冲突",
            "proposed_fix": "重写穿越窗口",
            "status": "resolved",
            "changes_core_plot": True,
        }
        failures = LOGIC.validate_review(logic_review(3, [finding]), through=3)
        self.assertTrue(any("必须取得用户确认" in item for item in failures))

    def test_logic_review_rejects_generic_pass_without_challenge(self):
        review = logic_review(2)
        review["dimensions"]["causality"]["challenge_attempt"] = "已检查"
        review["dimensions"]["causality"]["result"] = "通过"
        failures = LOGIC.validate_review(review, through=2)
        self.assertTrue(any("challenge_attempt" in item for item in failures))

    def test_narrative_contract_blocks_viewpoint_drift(self):
        state = STATE.new_state(24, 3, "auto_batch")
        state["approved_viewpoint"] = "第一人称"
        state["viewpoint_character"] = "苏晚晴"
        first_person = manuscript("我沿着井壁寻找刻痕。我记得昨夜的声音，我也知道自己尚未找到出口。")
        third_person = manuscript("苏晚晴沿着井壁寻找刻痕。苏晚晴记得昨夜的声音，她仍未找到出口。")
        self.assertEqual(NARRATIVE.evaluate(first_person, state)[0], [])
        failures, _ = NARRATIVE.evaluate(third_person, state)
        self.assertTrue(any("第一人称合同不符" in item for item in failures))

    def test_release_requires_rule_arc_and_antagonist_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "07_manuscript.md"
            state_path = root / "project_state.json"
            review_path = root / "logic_review_final.json"
            source.write_text(manuscript("我核对完整场景与证据。" * 100), encoding="utf-8")
            state = STATE.new_state(1, 3, "manual_continue")
            state["approved_viewpoint"] = "第一人称"
            state["viewpoint_character"] = "主角"
            state["completed_through"] = 1
            state["next_episode"] = 2
            state["continuity_ledger"]["world_rules"] = [
                {"name": "测试规则", "status": "resolved", "evidence": ["第1集完成建立与回收"]}
            ]
            state["character_arc_ledger"] = {
                "主角": {"closure_status": "closed", "evidence": ["第1集完成最终选择"]}
            }
            state["antagonist_causal_chain"] = {
                "goal": "控制通道",
                "benefit": "获得资源",
                "mechanism": "伪造名单",
                "victim_impact": "居民受困",
                "evidence_chain": ["第1集证据"],
                "defeat": "证据公开",
                "aftermath": "失去控制权",
            }
            STATE.atomic_write(state_path, state)
            review_path.write_text(
                json.dumps(logic_review(1, scope="final_manuscript"), ensure_ascii=False), encoding="utf-8"
            )
            command = [
                sys.executable,
                str(SCRIPTS / "validate_release_consistency.py"),
                str(source),
                str(state_path),
                str(review_path),
            ]
            passed = subprocess.run(
                command, capture_output=True, text=True, encoding="utf-8", env=SUBPROCESS_ENV
            )
            self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
            state["character_arc_ledger"] = {}
            STATE.atomic_write(state_path, state)
            failed = subprocess.run(
                command, capture_output=True, text=True, encoding="utf-8", env=SUBPROCESS_ENV
            )
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("character_arc_ledger 为空", failed.stdout + failed.stderr)

    def test_later_episode_duration_accepts_1_to_2_minutes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            valid = root / "valid.md"
            invalid = root / "invalid.md"
            valid.write_text(two_episode_manuscript("1.5"), encoding="utf-8")
            invalid.write_text(two_episode_manuscript("2.1"), encoding="utf-8")
            base_command = [sys.executable, str(SCRIPTS / "validate_episode_payoffs.py")]
            passed = subprocess.run(
                base_command + [str(valid), "--target-episodes", "24"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=SUBPROCESS_ENV,
            )
            failed = subprocess.run(
                base_command + [str(invalid), "--target-episodes", "24"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=SUBPROCESS_ENV,
            )
            self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("1-2 分钟", failed.stdout + failed.stderr)

    def test_allow_file_accepts_named_term(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "manuscript.md"
            source.write_text(manuscript("我打开 Codex，线索随即出现。"), encoding="utf-8")
            allow = root / "allowed.txt"
            allow.write_text("Codex\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "validate_chinese_manuscript.py"), str(source), "--allow-file", str(allow)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=SUBPROCESS_ENV,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_export_and_verify_clean_docx(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "manuscript.md"
            output = root / "final.docx"
            source.write_text(manuscript(), encoding="utf-8")
            export = subprocess.run(
                [sys.executable, str(SCRIPTS / "export_final_docx.py"), str(source), str(output), "--title", "测试小说"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=SUBPROCESS_ENV,
            )
            self.assertEqual(export.returncode, 0, export.stdout + export.stderr)
            verify = subprocess.run(
                [sys.executable, str(SCRIPTS / "verify_final_docx.py"), str(source), str(output)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=SUBPROCESS_ENV,
            )
            self.assertEqual(verify.returncode, 0, verify.stdout + verify.stderr)

    def test_batch_check_updates_recovery_point_only_after_all_checks_pass(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "07_manuscript.md"
            state_path = root / "project_state.json"
            review_path = root / "logic_review_1.json"
            source.write_text(manuscript("我打开 Codex，线索随即出现，并按记录核对前因后果。" * 50), encoding="utf-8")
            review_path.write_text(json.dumps(logic_review(1), ensure_ascii=False), encoding="utf-8")
            state = STATE.new_state(24, 3, "auto_batch")
            state["approved_viewpoint"] = "第一人称"
            state["viewpoint_character"] = "主角"
            STATE.atomic_write(state_path, state)

            command = [
                sys.executable,
                str(SCRIPTS / "run_batch_checks.py"),
                str(source),
                str(state_path),
                "--through",
                "1",
                "--logic-review",
                str(review_path),
            ]
            failed = subprocess.run(
                command, capture_output=True, text=True, encoding="utf-8", env=SUBPROCESS_ENV
            )
            self.assertNotEqual(failed.returncode, 0)
            self.assertEqual(STATE.load_state(state_path)["next_episode"], 1)

            state = STATE.load_state(state_path)
            state["allowed_english_terms"] = ["Codex"]
            STATE.atomic_write(state_path, state)
            passed = subprocess.run(
                command, capture_output=True, text=True, encoding="utf-8", env=SUBPROCESS_ENV
            )
            self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
            self.assertEqual(STATE.load_state(state_path)["next_episode"], 2)


if __name__ == "__main__":
    unittest.main()
