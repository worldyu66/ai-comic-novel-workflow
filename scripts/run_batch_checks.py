#!/usr/bin/env python3
"""Run all deterministic batch checks and atomically record the recovery point."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import project_state


EPISODE = re.compile(r"^##\s+第\s*[一二三四五六七八九十百千万0-9]+\s*集[：:].+$", re.MULTILINE)


def run(command: list[str]) -> dict[str, object]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", env=env)
    output = (result.stdout + result.stderr).strip()
    return {"command": command, "exit_status": result.returncode, "output": output}


def main() -> None:
    parser = argparse.ArgumentParser(description="执行结构、语言、密度、批次衰减及逻辑审查，并在全部通过后更新恢复点。")
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("state", type=Path)
    parser.add_argument("--through", type=int, required=True, help="本批完成后的最后集数")
    parser.add_argument("--logic-review", type=Path, required=True, help="本批逻辑与常识语义审查 JSON")
    parser.add_argument("--report", type=Path, help="校验报告 JSON 路径")
    args = parser.parse_args()

    state = project_state.load_state(args.state)
    text = args.manuscript.read_text(encoding="utf-8")
    episode_count = len(EPISODE.findall(text))
    if episode_count != args.through:
        raise SystemExit(f"检查失败：正文找到 {episode_count} 集，但 --through 为 {args.through}")

    scripts = Path(__file__).resolve().parent
    quality_report = args.manuscript.parent / "reports" / "manuscript_quality.json"
    commands = [
        [sys.executable, str(scripts / "count_chinese_characters.py"), str(args.manuscript)],
        [
            sys.executable,
            str(scripts / "validate_episode_payoffs.py"),
            str(args.manuscript),
            "--target-episodes",
            str(state["target_episodes"]),
        ],
        [
            sys.executable,
            str(scripts / "validate_chinese_manuscript.py"),
            str(args.manuscript),
            "--state",
            str(args.state),
        ],
        [
            sys.executable,
            str(scripts / "validate_manuscript_quality.py"),
            str(args.manuscript),
            "--state",
            str(args.state),
            "--report",
            str(quality_report),
        ],
        [
            sys.executable,
            str(scripts / "validate_logic_review.py"),
            str(args.logic_review),
            "--through",
            str(args.through),
        ],
        [
            sys.executable,
            str(scripts / "validate_narrative_contract.py"),
            str(args.manuscript),
            str(args.state),
            "--report",
            str(args.manuscript.parent / "reports" / "narrative_contract.json"),
        ],
    ]
    checks = [run(command) for command in commands]
    logic_review = json.loads(args.logic_review.read_text(encoding="utf-8"))
    merged_risks = {item.get("id"): item for item in state.get("logic_risks", []) if item.get("id")}
    for finding in logic_review.get("findings", []):
        if finding.get("id"):
            merged_risks[finding["id"]] = finding
    blockers = [
        item for item in merged_risks.values()
        if item.get("severity") == "high"
        and item.get("status") not in {"resolved", "user_confirmed", "intentionally_open"}
    ]
    if blockers:
        checks.append(
            {
                "command": ["state_logic_blocker_check"],
                "exit_status": 1,
                "output": "仍有未解决的高风险逻辑问题：" + "、".join(item["id"] for item in blockers),
            }
        )
    report = {
        "manuscript": str(args.manuscript.resolve()),
        "through": args.through,
        "checks": checks,
        "passed": all(check["exit_status"] == 0 for check in checks),
    }
    report_path = args.report or args.manuscript.parent / "reports" / "batch_validation.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if not report["passed"]:
        summaries = [str(check["output"]) for check in checks if check["exit_status"] != 0]
        raise SystemExit("批次检查失败：\n" + "\n".join(summaries))

    state["completed_through"] = args.through
    state["next_episode"] = args.through + 1
    state["stage"] = "drafting"
    state["last_validation"] = report
    state["validation_status"] = "passed"
    state["blocking_items"] = []
    state["release_receipt"] = None
    state["release_manuscript_sha256"] = None
    state["release_character_prompts_sha256"] = None
    state["release_scene_prompts_sha256"] = None
    state["release_docx_sha256"] = None
    state["delivery_manifest"] = {}
    state["logic_risks"] = list(merged_risks.values())
    state["semantic_reviews"].append(
        {
            "scope": logic_review.get("scope"),
            "reviewed_through": logic_review.get("reviewed_through"),
            "verdict": logic_review.get("verdict"),
            "review_file": str(args.logic_review.resolve()),
        }
    )
    state["change_log"].append(
        {"at": project_state.now_iso(), "event": "batch_completed", "through": args.through}
    )
    project_state.atomic_write(args.state, state)
    print(f"批次检查通过：共 {episode_count} 集；恢复点已更新为第 {args.through + 1} 集。")
    print(f"校验报告：{report_path}")


if __name__ == "__main__":
    main()
