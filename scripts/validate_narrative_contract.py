#!/usr/bin/env python3
"""Check that the manuscript follows the user-approved narrative viewpoint contract."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import project_state


EPISODE = re.compile(r"^##\s+第\s*[一二三四五六七八九十百千万0-9]+\s*集[：:].+$", re.MULTILINE)
BODY_HEADING = "### 本集正文"


def narrative_text(markdown: str) -> tuple[str, int]:
    matches = list(EPISODE.finditer(markdown))
    bodies: list[str] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        block = markdown[match.end():end]
        body_pos = block.find(BODY_HEADING)
        if body_pos >= 0:
            bodies.append(block[body_pos + len(BODY_HEADING):])
    text = "\n".join(bodies)
    text = re.sub(r"“[^”]*”", "", text)
    return text, len(bodies)


def evaluate(markdown: str, state: dict[str, object], release_notes: str | None = None) -> tuple[list[str], dict[str, object]]:
    text, episode_count = narrative_text(markdown)
    failures: list[str] = []
    viewpoint = state.get("approved_viewpoint")
    character = state.get("viewpoint_character")
    first_person_count = len(re.findall(r"我(?:们)?|咱们", text))
    character_count = text.count(str(character)) if character else 0
    minimum = max(3, episode_count // 2)

    if viewpoint not in {"第一人称", "第三人称"}:
        failures.append("approved_viewpoint 必须锁定为第一人称或第三人称")
    if not character:
        failures.append("viewpoint_character 尚未锁定")
    elif viewpoint == "第一人称":
        if first_person_count < minimum or first_person_count <= character_count:
            failures.append(
                f"正文与第一人称合同不符：叙述区第一人称标记 {first_person_count} 次，"
                f"主视角姓名 {character_count} 次"
            )
    elif viewpoint == "第三人称":
        if character_count < minimum or first_person_count > character_count:
            failures.append(
                f"正文与第三人称合同不符：主视角姓名 {character_count} 次，"
                f"叙述区第一人称标记 {first_person_count} 次"
            )

    if release_notes:
        opposite = "第三人称" if viewpoint == "第一人称" else "第一人称"
        if viewpoint and opposite in release_notes and viewpoint not in release_notes:
            failures.append(f"发布说明声明了 {opposite}，与状态中的 {viewpoint} 冲突")

    report = {
        "passed": not failures,
        "approved_viewpoint": viewpoint,
        "viewpoint_character": character,
        "episode_count": episode_count,
        "narrative_first_person_markers": first_person_count,
        "narrative_viewpoint_name_markers": character_count,
        "failures": failures,
    }
    return failures, report


def main() -> None:
    parser = argparse.ArgumentParser(description="检查正文是否遵守用户确认的第一/第三人称合同。")
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("state", type=Path)
    parser.add_argument("--release-notes", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    state = project_state.load_state(args.state)
    notes = args.release_notes.read_text(encoding="utf-8") if args.release_notes else None
    failures, report = evaluate(args.manuscript.read_text(encoding="utf-8"), state, notes)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("叙事合同检查失败：\n" + "\n".join(failures))
    print(
        f"叙事合同检查通过：{state['approved_viewpoint']}，主视角人物 {state['viewpoint_character']}。"
    )


if __name__ == "__main__":
    main()
