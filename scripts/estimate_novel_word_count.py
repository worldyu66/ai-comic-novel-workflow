#!/usr/bin/env python3
"""Estimate required novel-body characters from video mode and target minutes."""

from __future__ import annotations

import argparse
import json

from project_state import VIDEO_RUNTIME_RANGES


MODE_LABELS = {
    "pure_narration": "纯解说旁白",
    "dialogue_drama": "对话剧情",
    "hybrid": "复合型",
}


def estimate(mode: str, minutes: float) -> dict[str, object]:
    low, high = VIDEO_RUNTIME_RANGES[mode]
    return {
        "mode": mode,
        "mode_label": MODE_LABELS[mode],
        "minutes": minutes,
        "characters_per_minute_range": [low, high],
        "target_novel_characters_range": [round(low * minutes), round(high * minutes)],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="按视频模式与目标分钟数估算小说正文字符范围。")
    parser.add_argument("--mode", choices=sorted(VIDEO_RUNTIME_RANGES), required=True)
    parser.add_argument("--minutes", type=float, required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.minutes <= 0:
        raise SystemExit("--minutes 必须大于 0")
    result = estimate(args.mode, args.minutes)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    low, high = result["target_novel_characters_range"]
    cpm_low, cpm_high = result["characters_per_minute_range"]
    print(
        f"{result['mode_label']}：{args.minutes:g} 分钟，按每分钟 {cpm_low}-{cpm_high} 字，"
        f"小说正文目标为 {low}-{high} 字。"
    )


if __name__ == "__main__":
    main()
