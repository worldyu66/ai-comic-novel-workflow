#!/usr/bin/env python3
"""Flag accidental English tokens in Chinese episode prose and annotations."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9_-]*")


def main() -> None:
    parser = argparse.ArgumentParser(description="检查中文创作稿中是否混入未允许的英文。")
    parser.add_argument("manuscript", type=Path, help="07_manuscript.md 的路径")
    parser.add_argument("--allow", action="append", default=[], help="允许出现的英文专有名词，可重复使用。")
    args = parser.parse_args()

    allowed = {item.casefold() for item in args.allow}
    findings: list[str] = []
    in_code_block = False

    for number, line in enumerate(args.manuscript.read_text(encoding="utf-8").splitlines(), start=1):
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        unexpected = [token for token in TOKEN.findall(line) if token.casefold() not in allowed]
        if unexpected:
            findings.append(f"第 {number} 行：{'、'.join(unexpected)}")

    if findings:
        raise SystemExit("检查失败：发现未允许的英文词。\n" + "\n".join(findings))

    print("检查通过：创作稿未发现未允许的英文词。")


if __name__ == "__main__":
    main()
