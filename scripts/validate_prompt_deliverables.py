#!/usr/bin/env python3
"""Validate that the final character and key-scene prompt packs are real deliverables."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CHARACTER_HEADING = re.compile(r"^##\s+人物[：:]\s*.+?｜身份[：:]\s*.+$", re.MULTILINE)
SCENE_HEADING = re.compile(r"^##\s+场景[：:]\s*.+?｜对应集数[：:]\s*.+$", re.MULTILINE)
PLACEHOLDERS = ("<姓名>", "<剧情身份>", "<场景名称>", "<N>", "待补充", "TODO")


def validate(character_prompts: Path, scene_prompts: Path) -> tuple[list[str], dict[str, object]]:
    failures: list[str] = []
    counts = {"characters": 0, "scenes": 0}
    required = (
        (character_prompts, "人物提示词"),
        (scene_prompts, "关键场景提示词"),
    )
    texts: dict[str, str] = {}
    for path, label in required:
        if not path.is_file():
            failures.append(f"缺少{label}文件：{path}")
            continue
        text = path.read_text(encoding="utf-8").strip()
        texts[label] = text
        if not text:
            failures.append(f"{label}文件为空：{path}")
        for marker in PLACEHOLDERS:
            if marker in text:
                failures.append(f"{label}仍包含占位内容：{marker}")

    character_text = texts.get("人物提示词", "")
    scene_text = texts.get("关键场景提示词", "")
    if character_text:
        counts["characters"] = len(CHARACTER_HEADING.findall(character_text))
        for field in ("身份锚点", "外貌确认提示词", "连续性说明"):
            if field not in character_text:
                failures.append(f"人物提示词缺少字段：{field}")
        if counts["characters"] < 1:
            failures.append("人物提示词没有有效的“人物：姓名｜身份：剧情身份”条目")
    if scene_text:
        counts["scenes"] = len(SCENE_HEADING.findall(scene_text))
        for field in ("剧情作用", "场景确认提示词（16:9）", "人物连续性"):
            if field not in scene_text:
                failures.append(f"关键场景提示词缺少字段：{field}")
        if counts["scenes"] < 1:
            failures.append("关键场景提示词没有有效的“场景：名称｜对应集数：N”条目")
    return list(dict.fromkeys(failures)), counts


def main() -> None:
    parser = argparse.ArgumentParser(description="校验最终人物与关键场景提示词交付包。")
    parser.add_argument("character_prompts", type=Path)
    parser.add_argument("scene_prompts", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    failures, counts = validate(args.character_prompts, args.scene_prompts)
    report = {
        "character_prompts": str(args.character_prompts.resolve()),
        "scene_prompts": str(args.scene_prompts.resolve()),
        "counts": counts,
        "failures": failures,
        "passed": not failures,
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("提示词交付检查失败：\n" + "\n".join(failures))
    print(f"提示词交付检查通过：人物 {counts['characters']} 份；关键场景 {counts['scenes']} 份。")


if __name__ == "__main__":
    main()
