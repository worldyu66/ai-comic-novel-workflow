#!/usr/bin/env python3
"""Validate machine-readable evidence from a semantic logic/common-sense review."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_DIMENSIONS = {
    "timeline",
    "character_location",
    "causality",
    "world_rules",
    "physical_common_sense",
    "era_and_technology",
    "knowledge_state",
    "character_motivation",
    "consequence_persistence",
}
SEVERITIES = {"low", "medium", "high"}
RESOLVED_STATUSES = {"resolved", "user_confirmed", "intentionally_open"}


def load_review(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_review(review: dict[str, Any], through: int | None = None, final: bool = False) -> list[str]:
    failures: list[str] = []
    if through is not None and review.get("reviewed_through") != through:
        failures.append(f"reviewed_through 必须为 {through}")
    dimensions = review.get("dimensions", {})
    if not isinstance(dimensions, dict):
        failures.append("dimensions 必须是对象")
    else:
        missing = sorted(REQUIRED_DIMENSIONS - dimensions.keys())
        if missing:
            failures.append("缺少审查维度：" + "、".join(missing))
        for name in REQUIRED_DIMENSIONS & dimensions.keys():
            item = dimensions[name]
            if not isinstance(item, dict) or item.get("status") not in {"pass", "finding"}:
                failures.append(f"审查维度 {name} 必须包含有效 status")
                continue
            for field in ("evidence", "challenge_attempt", "result"):
                value = str(item.get(field, "")).strip()
                if len(value) < 10 or value in {"已检查", "未发现", "通过", "无"}:
                    failures.append(f"审查维度 {name} 的 {field} 必须记录具体正文事实与反证过程")
    findings = review.get("findings", [])
    if not isinstance(findings, list):
        failures.append("findings 必须是数组")
        findings = []
    for index, finding in enumerate(findings, start=1):
        prefix = f"finding {index}"
        if finding.get("severity") not in SEVERITIES:
            failures.append(f"{prefix} severity 无效")
        for field in ("id", "category", "description", "evidence", "proposed_fix", "status"):
            if not finding.get(field):
                failures.append(f"{prefix} 缺少 {field}")
        status = finding.get("status")
        if finding.get("severity") == "high" and status not in RESOLVED_STATUSES:
            failures.append(f"{prefix} 是未解决的高风险逻辑问题")
        if final and finding.get("severity") in {"medium", "high"} and status not in RESOLVED_STATUSES:
            failures.append(f"{prefix} 在终稿中仍是未解决的中高风险问题")
        if finding.get("changes_core_plot") and status != "user_confirmed":
            failures.append(f"{prefix} 会改变核心设定、主线、人物命运或结局，必须取得用户确认")
        if status == "user_confirmed" and not finding.get("user_confirmation"):
            failures.append(f"{prefix} 标记为 user_confirmed 时必须记录确认内容")
    if review.get("verdict") != "pass":
        failures.append("verdict 必须为 pass")
    if final and review.get("scope") != "final_manuscript":
        failures.append("终稿审查 scope 必须为 final_manuscript")
    return list(dict.fromkeys(failures))


def main() -> None:
    parser = argparse.ArgumentParser(description="校验逻辑与常识语义审查证据。")
    parser.add_argument("review", type=Path)
    parser.add_argument("--through", type=int)
    parser.add_argument("--final", action="store_true")
    args = parser.parse_args()
    review = load_review(args.review)
    failures = validate_review(review, args.through, args.final)
    if failures:
        raise SystemExit("逻辑审查失败：\n" + "\n".join(failures))
    print(f"逻辑审查通过：{args.review}")


if __name__ == "__main__":
    main()
