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
CHAPTER_HEADING = re.compile(r"^##\s+(?:第\s*[一二三四五六七八九十百千万0-9]+\s*集|Chapter\s+\d+|第[一二三四五六七八九十百千万0-9]+章)", re.IGNORECASE)


def prose_sections(markdown: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, list[str]]] = []
    title = "前置内容"
    lines: list[str] = []
    in_code_block = False

    for line in markdown.splitlines():
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if CHAPTER_HEADING.match(line):
            if lines:
                sections.append((title, lines))
            title = line.strip().lstrip("#").strip()
            lines = []
            continue
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith(METADATA_PREFIXES):
            continue
        lines.append(line)

    if lines:
        sections.append((title, lines))
    return [(name, "\n".join(content)) for name, content in sections]


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
