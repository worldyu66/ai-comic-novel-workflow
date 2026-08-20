#!/usr/bin/env python3
"""Count manuscript prose deterministically for the AI comic-novel workflow."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


METADATA_PREFIXES = (
    "**Chapter summary:",
    "**Verified chapter character count:",
    "**Verified cumulative character count:",
    "**Next-batch focus:",
    "**章节摘要：",
    "**本章核验字数：",
    "**累计核验字数：",
    "**下一批重点：",
    "- 本集摘要：",
    "- 开头钩子类型：",
    "- 钩子强度：",
    "- 目标时长：",
    "- 开场事件：",
    "- 观众立即知道：",
    "- 观众核心疑问：",
    "- 钩子与主线关系：",
    "- 钩子本集推进：",
    "- 钩子完全兑现期限：",
    "- 与上一集衔接：",
    "- 开头质量评分：",
    "- 开头评分理由：",
    "- 本集价值点：",
    "- 价值类型：",
    "- 是否明确爽点：",
    "- 爽点类型：",
    "- 铺垫与触发：",
    "- 本集兑现：",
    "- 观众情绪收益：",
    "- 节奏等级：",
    "- 下一集钩子：",
    "- 本集正文字符数：",
    "- 累计正文字符数：",
)
CHAPTER_HEADING = re.compile(
    r"^##\s+(?:第\s*[一二三四五六七八九十百千万0-9]+\s*集|Chapter\s+\d+|第[一二三四五六七八九十百千万0-9]+章)",
    re.IGNORECASE,
)
BODY_HEADING = "### 本集正文"


def prose_sections(markdown: str) -> list[tuple[str, str]]:
    lines = markdown.splitlines()
    starts = [index for index, line in enumerate(lines) if CHAPTER_HEADING.match(line)]
    sections: list[tuple[str, str]] = []
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = lines[start:end]
        try:
            body_start = next(index for index, line in enumerate(block) if line.strip() == BODY_HEADING) + 1
        except StopIteration:
            continue
        body_lines: list[str] = []
        in_code_block = False
        for line in block[body_start:]:
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue
            stripped = line.strip()
            if not stripped or stripped.startswith(METADATA_PREFIXES):
                continue
            body_lines.append(line)
        if body_lines:
            sections.append((block[0].strip().lstrip("#").strip(), "\n".join(body_lines)))
    return sections


def count_non_whitespace(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def count_cjk_ideographs(text: str) -> int:
    return len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]", text))


def main() -> None:
    parser = argparse.ArgumentParser(description="Count prose characters in a manuscript Markdown file.")
    parser.add_argument("manuscript", type=Path, help="Path to 07_manuscript.md")
    args = parser.parse_args()

    markdown = args.manuscript.read_text(encoding="utf-8")
    sections = prose_sections(markdown)
    if not sections:
        raise SystemExit("未找到分集正文。请使用类似“## 第 1 集：标题”的二级标题。")

    total_text = "\n".join(text for _, text in sections)
    for name, text in sections:
        print(f"{name}：正文字符数 {count_non_whitespace(text)}，其中汉字 {count_cjk_ideographs(text)}")
    print(f"全文合计：正文字符数 {count_non_whitespace(total_text)}，其中汉字 {count_cjk_ideographs(total_text)}")


if __name__ == "__main__":
    main()
