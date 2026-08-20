#!/usr/bin/env python3
"""Validate episode opening hooks, audience value points, and payoff rhythm."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


EPISODE = re.compile(r"^##\s+第\s*([一二三四五六七八九十百千万0-9]+)\s*集[：:].+$", re.MULTILINE)
FIELD_LINE = re.compile(r"^- ([^：]+)：\s*(.*?)\s*$", re.MULTILINE)
ANNOTATION_HEADING = "### 本集创作标注"
BODY_HEADING = "### 本集正文"
REQUIRED_NAMES = (
    "开头钩子类型",
    "钩子强度",
    "开场事件",
    "观众立即知道",
    "观众核心疑问",
    "钩子与主线关系",
    "钩子本集推进",
    "钩子完全兑现期限",
    "与上一集衔接",
    "开头质量评分",
    "开头评分理由",
    "本集摘要",
    "本集价值点",
    "价值类型",
    "是否明确爽点",
    "爽点类型",
    "铺垫与触发",
    "本集兑现",
    "观众情绪收益",
    "节奏等级",
    "下一集钩子",
)
HOOK_TYPES = {
    "反常型",
    "结果前置型",
    "身份反差型",
    "冲突爆发型",
    "危机倒计时型",
    "关系破裂型",
    "规则怪诞型",
    "信息颠覆型",
}
HOOK_STRENGTHS = {"强钩子", "中钩子", "基础钩子"}
VALUE_TYPES = {"爽点", "泪点", "甜点", "惊点", "笑点", "信息点"}
RHYTHM_LEVELS = {"蓄势", "小兑现", "强兑现", "阶段高潮"}


def is_blank(value: str) -> bool:
    return not value.strip(".。…- <>待填写")


def parse_score(value: str) -> int | None:
    match = re.fullmatch(r"\s*(10|[0-9])\s*(?:/\s*10)?\s*(?:分)?\s*", value)
    return int(match.group(1)) if match else None


def main() -> None:
    parser = argparse.ArgumentParser(description="检查每集开头钩子、价值点与爽点节奏窗口。")
    parser.add_argument("manuscript", type=Path, help="07_manuscript.md 的路径")
    args = parser.parse_args()

    text = args.manuscript.read_text(encoding="utf-8")
    episodes = list(EPISODE.finditer(text))
    if not episodes:
        raise SystemExit("检查失败：未找到“## 第 N 集：标题”格式的分集标题。")

    failures: list[str] = []
    records: list[dict[str, str]] = []

    for index, match in enumerate(episodes):
        label = match.group(1)
        end = episodes[index + 1].start() if index + 1 < len(episodes) else len(text)
        block = text[match.start():end]
        annotation_pos = block.find(ANNOTATION_HEADING)
        body_pos = block.find(BODY_HEADING)

        if annotation_pos < 0 or body_pos < 0 or annotation_pos > body_pos:
            failures.append(f"第 {label} 集必须按“集标题 → 本集创作标注 → 本集正文”排列")
            records.append({})
            continue

        annotation = block[annotation_pos:body_pos]
        values = {name: value.strip() for name, value in FIELD_LINE.findall(annotation)}
        missing = [name for name in REQUIRED_NAMES if name not in values]
        if missing:
            failures.append(f"第 {label} 集缺少字段：{'、'.join(missing)}")

        empty = [name for name in REQUIRED_NAMES if name in values and is_blank(values[name])]
        if empty:
            failures.append(f"第 {label} 集字段为空：{'、'.join(empty)}")

        if values.get("开头钩子类型") not in HOOK_TYPES:
            failures.append(f"第 {label} 集开头钩子类型必须使用规定的八种类型之一")
        if values.get("钩子强度") not in HOOK_STRENGTHS:
            failures.append(f"第 {label} 集钩子强度必须是：强钩子、中钩子、基础钩子")
        if values.get("钩子与主线关系") in {"无", "无关", "没有"}:
            failures.append(f"第 {label} 集开头钩子必须与主线有关")

        score = parse_score(values.get("开头质量评分", ""))
        if score is None:
            failures.append(f"第 {label} 集开头质量评分必须填写 0-10 的整数")
        else:
            minimum = 9 if index == 0 else 8 if index < 3 else 7
            if score < minimum:
                failures.append(f"第 {label} 集开头质量评分低于 {minimum}/10 的最低要求")

        if index == 0 and values.get("钩子强度") != "强钩子":
            failures.append(f"第 {label} 集作为第一集必须使用强钩子")
        if 0 < index < 3 and values.get("钩子强度") == "基础钩子":
            failures.append(f"第 {label} 集位于前三集，不能只使用基础钩子")

        if values.get("价值类型") not in VALUE_TYPES:
            failures.append(f"第 {label} 集价值类型必须是：{'、'.join(sorted(VALUE_TYPES))}")
        if values.get("是否明确爽点") not in {"是", "否"}:
            failures.append(f"第 {label} 集“是否明确爽点”只能填写“是”或“否”")
        if values.get("节奏等级") not in RHYTHM_LEVELS:
            failures.append(f"第 {label} 集节奏等级必须是：蓄势、小兑现、强兑现、阶段高潮")
        if values.get("是否明确爽点") == "否" and values.get("爽点类型") != "无":
            failures.append(f"第 {label} 集没有明确爽点时，爽点类型应填写“无”")
        if values.get("是否明确爽点") == "是" and values.get("爽点类型") == "无":
            failures.append(f"第 {label} 集标记为明确爽点时，必须填写具体爽点类型")
        if values.get("本集兑现") == values.get("下一集钩子"):
            failures.append(f"第 {label} 集的本集兑现不能与下一集钩子相同")

        records.append(values)

    for index in range(len(records) - 1):
        if records[index].get("节奏等级") == "蓄势" and records[index + 1].get("节奏等级") == "蓄势":
            failures.append(f"第 {index + 1}-{index + 2} 集连续两集只有蓄势")

    for index in range(len(records) - 2):
        window = records[index:index + 3]
        if all(record.get("是否明确爽点") != "是" for record in window):
            failures.append(f"第 {index + 1}-{index + 3} 集缺少明确爽点")
        hook_types = [record.get("开头钩子类型") for record in window]
        if hook_types[0] and len(set(hook_types)) == 1:
            failures.append(f"第 {index + 1}-{index + 3} 集连续使用同一种开头钩子")

    for index in range(len(records) - 5):
        window = records[index:index + 6]
        if all(record.get("节奏等级") not in {"强兑现", "阶段高潮"} for record in window):
            failures.append(f"第 {index + 1}-{index + 6} 集缺少强兑现或阶段高潮")

    if failures:
        raise SystemExit("检查失败：\n" + "\n".join(dict.fromkeys(failures)))

    print(f"检查通过：共 {len(episodes)} 集，开头钩子、价值点与爽点节奏窗口合格。")


if __name__ == "__main__":
    main()
