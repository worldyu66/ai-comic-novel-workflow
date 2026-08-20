#!/usr/bin/env python3
"""Validate enhanced-outline episode cards and reject the legacy wide table."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


CARD = re.compile(r"^## 第\s*(\d+)\s*集｜([^｜]+)｜([^\n]+)$", re.MULTILINE)
FIELD = re.compile(r"^- ([^：]+)：\s*(.*?)\s*$", re.MULTILINE)
REQUIRED_FIELDS = (
    "目标时长", "开头钩子类型", "开场事件", "观众核心疑问", "钩子强度", "钩子兑现期限", "本集目标",
    "核心冲突", "本集价值点", "价值类型", "是否明确爽点", "爽点类型", "本集兑现", "观众收益",
    "节奏等级", "集尾钩子",
)
HOOK_TYPES = {"反常型", "结果前置型", "身份反差型", "冲突爆发型", "危机倒计时型", "关系破裂型", "规则怪诞型", "信息颠覆型"}
HOOK_STRENGTHS = {"强钩子", "中钩子", "基础钩子"}
VALUE_TYPES = {"爽点", "泪点", "甜点", "惊点", "笑点", "信息点"}
RHYTHM_LEVELS = {"蓄势", "小兑现", "强兑现", "阶段高潮"}


def duration_minutes(value: str) -> float | None:
    match = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*分钟\s*", value)
    return float(match.group(1)) if match else None


def validate(text: str, target_episodes: int | None = None) -> list[str]:
    failures: list[str] = []
    if re.search(r"^\|\s*集数\s*\|", text, re.MULTILINE):
        failures.append("强化大纲仍在使用横向分集表格；必须改为逐集卡片")
    cards = list(CARD.finditer(text))
    if not cards:
        failures.append("未找到“## 第 01 集｜目标时长｜节奏等级”格式的分集卡片")
        return failures
    if target_episodes is not None and len(cards) != target_episodes:
        failures.append(f"卡片共 {len(cards)} 集，与目标 {target_episodes} 集不一致")

    records: list[dict[str, str]] = []
    for index, card in enumerate(cards):
        number = int(card.group(1))
        if number != index + 1:
            failures.append(f"第 {number} 集卡片顺序错误，应为第 {index + 1} 集")
        end = cards[index + 1].start() if index + 1 < len(cards) else len(text)
        values = {name: value.strip() for name, value in FIELD.findall(text[card.end():end])}
        missing = [name for name in REQUIRED_FIELDS if not values.get(name)]
        if missing:
            failures.append(f"第 {number} 集缺少字段：{'、'.join(missing)}")
        if values.get("目标时长") and values["目标时长"] != card.group(2).strip():
            failures.append(f"第 {number} 集标题与字段的目标时长不一致")
        if values.get("节奏等级") and values["节奏等级"] != card.group(3).strip():
            failures.append(f"第 {number} 集标题与字段的节奏等级不一致")
        duration = duration_minutes(values.get("目标时长", ""))
        if duration is None:
            failures.append(f"第 {number} 集目标时长格式错误")
        elif index == 0 and not 1 <= duration <= 5:
            failures.append("第 1 集目标时长必须在 1-5 分钟内")
        elif index > 0 and not 1 <= duration <= 2:
            failures.append(f"第 {number} 集目标时长必须在 1-2 分钟内")
        if values.get("开头钩子类型") not in HOOK_TYPES:
            failures.append(f"第 {number} 集开头钩子类型不在规定的八种类型中")
        if values.get("钩子强度") not in HOOK_STRENGTHS:
            failures.append(f"第 {number} 集钩子强度无效")
        if values.get("价值类型") not in VALUE_TYPES:
            failures.append(f"第 {number} 集价值类型无效")
        if values.get("是否明确爽点") not in {"是", "否"}:
            failures.append(f"第 {number} 集“是否明确爽点”只能是“是”或“否”")
        if values.get("节奏等级") not in RHYTHM_LEVELS:
            failures.append(f"第 {number} 集节奏等级无效")
        records.append(values)

    for index in range(len(records) - 2):
        if all(item.get("是否明确爽点") != "是" for item in records[index:index + 3]):
            failures.append(f"第 {index + 1}-{index + 3} 集缺少明确爽点")
    for index in range(len(records) - 5):
        if all(item.get("节奏等级") not in {"强兑现", "阶段高潮"} for item in records[index:index + 6]):
            failures.append(f"第 {index + 1}-{index + 6} 集缺少强兑现或阶段高潮")
    return list(dict.fromkeys(failures))


def main() -> None:
    parser = argparse.ArgumentParser(description="检查强化大纲分集卡片的结构、时长、钩子和兑现节奏。")
    parser.add_argument("outline", type=Path)
    parser.add_argument("--target-episodes", type=int)
    args = parser.parse_args()
    text = args.outline.read_text(encoding="utf-8")
    failures = validate(text, args.target_episodes)
    if failures:
        raise SystemExit("强化大纲检查失败：\n" + "\n".join(failures))
    print(f"强化大纲检查通过：共 {len(CARD.findall(text))} 张分集卡片，结构、时长、钩子与兑现节奏合格。")


if __name__ == "__main__":
    main()
