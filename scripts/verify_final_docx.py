#!/usr/bin/env python3
"""Verify that a final DOCX contains every episode body and no working labels."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

try:
    from docx import Document
except ImportError as exc:  # pragma: no cover
    raise SystemExit("缺少 python-docx；请使用 Codex 工作区 Python 运行此脚本。") from exc

from export_final_docx import FORBIDDEN_WORKING_LABELS, extract_episodes


def normalize(text: str) -> str:
    return re.sub(r"\s+", "", text)


def verify(manuscript: Path, docx_path: Path) -> list[str]:
    episodes = extract_episodes(manuscript.read_text(encoding="utf-8"))
    document = Document(docx_path)
    paragraphs = [paragraph.text for paragraph in document.paragraphs]
    joined = "\n".join(paragraphs)
    normalized_joined = normalize(joined)
    failures: list[str] = []

    for label in FORBIDDEN_WORKING_LABELS:
        if label in joined:
            failures.append(f"正式稿仍包含工作标注：{label}")
    for title, lines in episodes:
        if title not in paragraphs:
            failures.append(f"正式稿缺少集标题：{title}")
        expected_body = normalize("".join(line for line in lines if line))
        if expected_body and expected_body not in normalized_joined:
            failures.append(f"正式稿正文与 Markdown 不一致：{title}")
    doc_episode_titles = [line for line in paragraphs if re.match(r"^第\s*.+\s*集[：:]", line)]
    if len(doc_episode_titles) != len(episodes):
        failures.append(f"正式稿集数 {len(doc_episode_titles)} 与 Markdown 集数 {len(episodes)} 不一致")
    return failures


def main() -> None:
    parser = argparse.ArgumentParser(description="核验 Word 正式稿的集数、正文和标注清理结果。")
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("docx", type=Path)
    args = parser.parse_args()
    failures = verify(args.manuscript, args.docx)
    if failures:
        raise SystemExit("正式稿核验失败：\n" + "\n".join(failures))
    print(f"正式稿核验通过：{args.docx}")


if __name__ == "__main__":
    main()
