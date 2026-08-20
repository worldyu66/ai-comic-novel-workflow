#!/usr/bin/env python3
"""Block release until logic, rule, character, antagonist, and clue ledgers close."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import project_state
from validate_logic_review import load_review, validate_review
from validate_narrative_contract import evaluate as evaluate_narrative_contract


EPISODE = re.compile(r"^##\s+第\s*[一二三四五六七八九十百千万0-9]+\s*集[：:].+$", re.MULTILINE)
ANTAGONIST_FIELDS = ("goal", "benefit", "mechanism", "victim_impact", "evidence_chain", "defeat", "aftermath")


def has_evidence(value: object) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value) and all(bool(str(item).strip()) for item in value)
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="终稿发布前检查逻辑、规则、人物弧、反派因果链和伏笔闭环。")
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("state", type=Path)
    parser.add_argument("final_review", type=Path)
    args = parser.parse_args()

    state = project_state.load_state(args.state)
    text = args.manuscript.read_text(encoding="utf-8")
    count = len(EPISODE.findall(text))
    failures = validate_review(load_review(args.final_review), through=count, final=True)
    narrative_failures, _ = evaluate_narrative_contract(text, state)
    failures.extend(narrative_failures)
    if state.get("completed_through") != count:
        failures.append(f"状态完成至第 {state.get('completed_through')} 集，但正文为 {count} 集")
    if state.get("open_clues"):
        failures.append("仍有未回收伏笔：" + "、".join(state["open_clues"]))
    blocking = [item for item in state.get("logic_risks", []) if item.get("severity") in {"medium", "high"} and item.get("status") not in {"resolved", "user_confirmed", "intentionally_open"}]
    if blocking:
        failures.append("仍有未解决的中高风险逻辑问题：" + "、".join(item.get("id", "unknown") for item in blocking))

    rules = state.get("continuity_ledger", {}).get("world_rules", [])
    if not rules:
        failures.append("world_rules 为空，核心世界规则没有生命周期证据")
    for rule in rules:
        if rule.get("status") not in {"resolved", "intentionally_open"} or not has_evidence(rule.get("evidence")):
            failures.append(f"世界规则未闭环：{rule.get('name', '未命名规则')}")

    arcs = state.get("character_arc_ledger", {})
    if not arcs:
        failures.append("character_arc_ledger 为空")
    for name, arc in arcs.items():
        if arc.get("closure_status") not in {"closed", "intentionally_open"} or not has_evidence(arc.get("evidence")):
            failures.append(f"人物弧未闭环：{name}")

    chain = state.get("antagonist_causal_chain", {})
    for field in ANTAGONIST_FIELDS:
        if not has_evidence(chain.get(field)):
            failures.append(f"反派因果链缺少：{field}")
    if failures:
        raise SystemExit("发布一致性检查失败：\n" + "\n".join(dict.fromkeys(failures)))
    print(f"发布一致性检查通过：共 {count} 集，逻辑、规则、人物弧、反派因果链与伏笔均已闭环。")


if __name__ == "__main__":
    main()
