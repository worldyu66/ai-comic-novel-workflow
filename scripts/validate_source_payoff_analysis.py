#!/usr/bin/env python3
"""Validate depth and evidence separation in the source/payoff analysis report."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


MECHANISM = re.compile(r"^###\s+机制\s*[0-9一二三四五六七八九十]+[｜|].+$", re.MULTILINE)
AG001_FIELDS = (
    "赛道定位",
    "目标受众",
    "核心观看欲望",
    "情绪曲线",
    "连载驱动力",
    "单集推进特征",
    "漫剧适配优势",
    "内容与逻辑风险",
)
MECHANISM_FIELDS = (
    "素材证据一",
    "素材证据二",
    "运行链",
    "观众心理",
    "核心反差",
    "升级阶梯",
    "兑现频率",
    "可迁移机制",
    "必须替换外壳",
    "逻辑与审美风险",
)
JOINT_FIELDS = (
    "最值得保留的受众机制",
    "不应照搬的辨识度元素",
    "原创转化原则",
    "可衍生的差异化题材方向",
    "对下一步选题的约束",
)
GENERIC_VALUES = {"略", "无", "已分析", "见上文", "同上", "待补充", "暂无"}


def chinese_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def field_value(block: str, field: str) -> str | None:
    match = re.search(rf"^-\s*{re.escape(field)}[：:]\s*(.+)$", block, re.MULTILINE)
    return match.group(1).strip() if match else None


def validate(text: str, min_chinese: int = 1500) -> list[str]:
    failures: list[str] = []
    count = chinese_count(text)
    if count < min_chinese:
        failures.append(f"中文字符数 {count}，低于深度分析下限 {min_chinese}")

    for heading in (
        "## ag_001｜赛道与受众深度分析",
        "## ag_006（前轻后重·本阶段只分析）｜冲突与爽点机制",
        "## 联合结论｜原创转化边界",
    ):
        if heading not in text:
            failures.append(f"缺少标题：{heading}")

    ag001_start = text.find("## ag_001｜赛道与受众深度分析")
    ag006_start = text.find("## ag_006（前轻后重·本阶段只分析）｜冲突与爽点机制")
    joint_start = text.find("## 联合结论｜原创转化边界")
    ag001_block = text[ag001_start:ag006_start] if ag001_start >= 0 and ag006_start > ag001_start else ""
    for field in AG001_FIELDS:
        value = field_value(ag001_block, field)
        if not value or chinese_count(value) < 8 or value in GENERIC_VALUES:
            failures.append(f"ag_001 字段“{field}”缺失或分析过短")

    matches = list(MECHANISM.finditer(text))
    if not 5 <= len(matches) <= 8:
        failures.append(f"爽点机制卡必须为 5-8 个，当前为 {len(matches)} 个")
    for index, match in enumerate(matches, start=1):
        end = matches[index].start() if index < len(matches) else (joint_start if joint_start > match.start() else len(text))
        block = text[match.start():end]
        for field in MECHANISM_FIELDS:
            value = field_value(block, field)
            minimum = 12 if field in {"素材证据一", "素材证据二", "运行链", "观众心理"} else 8
            if not value or chinese_count(value) < minimum or value in GENERIC_VALUES:
                failures.append(f"机制 {index:02d} 字段“{field}”缺失或分析过短")
        evidence_one = field_value(block, "素材证据一") or ""
        evidence_two = field_value(block, "素材证据二") or ""
        if evidence_one == evidence_two:
            failures.append(f"机制 {index:02d} 的两条素材证据不得重复")

    joint_block = text[joint_start:] if joint_start >= 0 else ""
    for field in JOINT_FIELDS:
        value = field_value(joint_block, field)
        if not value or chinese_count(value) < 8 or value in GENERIC_VALUES:
            failures.append(f"联合结论字段“{field}”缺失或分析过短")
    return list(dict.fromkeys(failures))


def main() -> None:
    parser = argparse.ArgumentParser(description="检查来源素材与爽点机制分析的深度、证据和原创边界。")
    parser.add_argument("analysis", type=Path)
    parser.add_argument("--min-chinese", type=int, default=1500)
    args = parser.parse_args()
    if args.min_chinese <= 0:
        raise SystemExit("--min-chinese 必须大于 0")
    text = args.analysis.read_text(encoding="utf-8")
    failures = validate(text, args.min_chinese)
    if failures:
        raise SystemExit("来源爽点分析检查失败：\n" + "\n".join(failures))
    print(
        f"来源爽点分析检查通过：{len(MECHANISM.findall(text))} 个机制，"
        f"{chinese_count(text)} 个中文字符。"
    )


if __name__ == "__main__":
    main()
