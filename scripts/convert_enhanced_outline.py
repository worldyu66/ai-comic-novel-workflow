#!/usr/bin/env python3
"""Convert a wide enhanced-outline Markdown table into readable episode cards."""

from __future__ import annotations

import argparse
from pathlib import Path


EXPECTED_COLUMNS = (
    "集数", "目标时长", "开头钩子类型", "开场事件", "观众核心疑问", "钩子强度", "钩子兑现期限",
    "本集目标", "核心冲突", "本集价值点", "价值类型", "是否明确爽点", "爽点类型", "本集兑现",
    "观众收益", "节奏等级", "集尾钩子",
)
HOOK_ALIASES = {"异常型": "反常型", "泪点型": "关系破裂型"}
GROUPS = (
    ("开头与悬念", ("目标时长", "开头钩子类型", "开场事件", "观众核心疑问", "钩子强度", "钩子兑现期限")),
    ("剧情推进", ("本集目标", "核心冲突")),
    ("价值与兑现", ("本集价值点", "价值类型", "是否明确爽点", "爽点类型", "本集兑现", "观众收益", "节奏等级", "集尾钩子")),
)


def cells(line: str) -> list[str]:
    return [item.strip() for item in line.strip().strip("|").split("|")]


def convert(markdown: str) -> str:
    lines = markdown.splitlines()
    header_index = next((index for index, line in enumerate(lines) if cells(line) == list(EXPECTED_COLUMNS)), None)
    if header_index is None:
        raise ValueError("未找到 17 列强化大纲表头")

    rows: list[dict[str, str]] = []
    end_index = header_index + 1
    for index in range(header_index + 1, len(lines)):
        line = lines[index]
        if not line.strip().startswith("|"):
            end_index = index
            break
        values = cells(line)
        if values and all(value.replace("-", "").replace(":", "").strip() == "" for value in values):
            continue
        if len(values) != len(EXPECTED_COLUMNS):
            raise ValueError(f"表格第 {index + 1} 行有 {len(values)} 列，应为 {len(EXPECTED_COLUMNS)} 列")
        row = dict(zip(EXPECTED_COLUMNS, values))
        row["开头钩子类型"] = HOOK_ALIASES.get(row["开头钩子类型"], row["开头钩子类型"])
        rows.append(row)
        end_index = index + 1
    if not rows:
        raise ValueError("强化大纲表格没有分集数据")

    output = lines[:header_index]
    while output and not output[-1].strip():
        output.pop()
    output.extend(["", "## 分集强化卡片", ""])
    for row in rows:
        output.extend([f"## 第 {int(row['集数']):02d} 集｜{row['目标时长']}｜{row['节奏等级']}", ""])
        for group_name, fields in GROUPS:
            output.extend([f"### {group_name}", ""])
            output.extend(f"- {field}：{row[field]}" for field in fields)
            output.append("")
    output.extend(lines[end_index:])
    return "\n".join(output).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="把 17 列强化大纲表格转换为逐集卡片。")
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path, nargs="?")
    parser.add_argument("--in-place", action="store_true")
    args = parser.parse_args()
    if args.in_place and args.output:
        parser.error("--in-place 与 output 不能同时使用")
    destination = args.input if args.in_place else args.output
    if destination is None:
        parser.error("请提供 output 或使用 --in-place")
    try:
        converted = convert(args.input.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise SystemExit(f"转换失败：{exc}") from exc
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(converted, encoding="utf-8", newline="\n")
    print(f"转换完成：{destination}")


if __name__ == "__main__":
    main()
