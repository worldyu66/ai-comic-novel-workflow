#!/usr/bin/env python3
"""Detect runtime-density extremes and long-form batch degradation."""

from __future__ import annotations

import argparse
import json
import re
import statistics
from pathlib import Path

import project_state


EPISODE = re.compile(r"^##\s+第\s*([一二三四五六七八九十百千万0-9]+)\s*集[：:].+$", re.MULTILINE)
FIELD = re.compile(r"^- ([^：]+)：\s*(.*?)\s*$", re.MULTILINE)
BODY_HEADING = "### 本集正文"


def parse_duration(value: str) -> float | None:
    match = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*分钟\s*", value)
    return float(match.group(1)) if match else None


def parse_episodes(text: str) -> list[dict[str, object]]:
    matches = list(EPISODE.finditer(text))
    records: list[dict[str, object]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.start():end]
        body_pos = block.find(BODY_HEADING)
        if body_pos < 0:
            continue
        annotation = block[:body_pos]
        values = {name: value.strip() for name, value in FIELD.findall(annotation)}
        body = block[body_pos + len(BODY_HEADING):]
        body_chars = len(re.sub(r"\s+", "", body))
        duration = parse_duration(values.get("目标时长", ""))
        records.append(
            {
                "index": index + 1,
                "label": match.group(1),
                "duration_minutes": duration,
                "body_characters": body_chars,
                "characters_per_minute": round(body_chars / duration, 1) if duration else None,
            }
        )
    return records


def evaluate(
    records: list[dict[str, object]],
    min_cpm: float,
    max_cpm: float,
    max_drift_percent: float,
    batch_size: int,
) -> tuple[list[str], dict[str, object]]:
    failures: list[str] = []
    valid = [record for record in records if record["characters_per_minute"] is not None]
    for record in valid:
        cpm = float(record["characters_per_minute"])
        if cpm < min_cpm:
            failures.append(
                f"第 {record['index']} 集正文密度 {cpm:.1f} 字符/分钟，低于下限 {min_cpm:.1f}"
            )
        if cpm > max_cpm:
            failures.append(
                f"第 {record['index']} 集正文密度 {cpm:.1f} 字符/分钟，高于上限 {max_cpm:.1f}"
            )

    batch_medians: list[dict[str, object]] = []
    for start in range(0, len(valid), batch_size):
        batch = valid[start:start + batch_size]
        if not batch:
            continue
        batch_medians.append(
            {
                "episodes": f"{batch[0]['index']}-{batch[-1]['index']}",
                "median_cpm": round(statistics.median(float(item["characters_per_minute"]) for item in batch), 1),
            }
        )
    allowed_ratio = max_drift_percent / 100
    for index in range(2, len(batch_medians)):
        prior = statistics.median(float(item["median_cpm"]) for item in batch_medians[max(0, index - 2):index])
        current = float(batch_medians[index]["median_cpm"])
        if prior and abs(current / prior - 1) > allowed_ratio:
            direction = "下降" if current < prior else "上升"
            failures.append(
                f"第 {batch_medians[index]['episodes']} 集批次密度较前两批显著{direction}：{prior:.1f} -> {current:.1f} 字符/分钟"
            )

    if len(valid) >= 12:
        third = max(3, len(valid) // 3)
        first = statistics.median(float(item["characters_per_minute"]) for item in valid[:third])
        last = statistics.median(float(item["characters_per_minute"]) for item in valid[-third:])
        if first and abs(last / first - 1) > allowed_ratio:
            direction = "下降" if last < first else "上升"
            failures.append(f"长篇前后密度显著{direction}：前段 {first:.1f}，后段 {last:.1f} 字符/分钟")

    report = {
        "passed": not failures,
        "limits": {"min_cpm": min_cpm, "max_cpm": max_cpm, "max_drift_percent": max_drift_percent},
        "episodes": records,
        "batch_medians": batch_medians,
        "failures": failures,
    }
    return failures, report


def main() -> None:
    parser = argparse.ArgumentParser(description="检查正文是否支撑目标时长，并捕捉长篇批次衰减。")
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("--state", type=Path, help="从项目状态读取视频模式和每分钟小说正文字数范围")
    parser.add_argument("--min-cpm", type=float)
    parser.add_argument("--max-cpm", type=float)
    parser.add_argument("--max-drift-percent", type=float, default=35)
    parser.add_argument("--batch-size", type=int, default=3)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if args.state:
        state = project_state.load_state(args.state)
        mode_low, mode_high = state["novel_characters_per_minute_range"]
    else:
        mode_low, mode_high = 160, 380
    min_cpm = args.min_cpm if args.min_cpm is not None else mode_low
    max_cpm = args.max_cpm if args.max_cpm is not None else mode_high
    records = parse_episodes(args.manuscript.read_text(encoding="utf-8"))
    if not records:
        raise SystemExit("质量检查失败：未找到分集正文。")
    failures, report = evaluate(records, min_cpm, max_cpm, args.max_drift_percent, args.batch_size)
    if args.state:
        report["video_runtime_mode"] = state["video_runtime_mode"]
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("质量检查失败：\n" + "\n".join(failures))
    print(f"质量检查通过：共 {len(records)} 集，正文密度与批次稳定性合格。")


if __name__ == "__main__":
    main()
