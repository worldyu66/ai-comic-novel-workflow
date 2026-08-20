#!/usr/bin/env python3
"""Create, validate, update, and summarize the comic-novel project state."""

from __future__ import annotations

import argparse
import json
import math
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 5
VIDEO_RUNTIME_RANGES = {
    "pure_narration": [330, 500],
    "dialogue_drama": [360, 440],
    "hybrid": [350, 450],
}
STAGES = {
    "source_analysis",
    "topic_selection",
    "spec_confirmation",
    "story_bible",
    "outline",
    "risk_review",
    "creative_confirmation",
    "drafting",
    "release",
    "complete",
}
DRAFT_MODES = {"auto_batch", "manual_continue"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def episode_range(target: int, tolerance_percent: float = 10.0) -> list[int]:
    deviation = max(1, math.ceil(target * tolerance_percent / 100))
    return [max(1, target - deviation), target + deviation]


def new_state(
    target_episodes: int,
    first_episode_minutes: float,
    draft_mode: str,
    video_runtime_mode: str = "hybrid",
) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "updated_at": now_iso(),
        "stage": "spec_confirmation",
        "selected_topic": None,
        "target_episodes": target_episodes,
        "episode_tolerance_percent": 10,
        "allowed_episode_range": episode_range(target_episodes),
        "first_episode_minutes": first_episode_minutes,
        "later_episode_minutes_range": [1, 2],
        "draft_mode": draft_mode,
        "approved_viewpoint": None,
        "viewpoint_character": None,
        "opening_mode": None,
        "video_runtime_mode": video_runtime_mode,
        "novel_characters_per_minute_range": VIDEO_RUNTIME_RANGES[video_runtime_mode],
        "completed_through": 0,
        "next_episode": 1,
        "open_clues": [],
        "resolved_clues": [],
        "character_continuity": {},
        "continuity_ledger": {
            "timeline": [],
            "character_locations": {},
            "knowledge_state": {},
            "world_rules": [],
        },
        "logic_review_mode": "strict",
        "logic_risks": [],
        "character_arc_ledger": {},
        "antagonist_causal_chain": {
            "goal": "",
            "benefit": "",
            "mechanism": "",
            "victim_impact": "",
            "evidence_chain": [],
            "defeat": "",
            "aftermath": "",
        },
        "semantic_reviews": [],
        "allowed_english_terms": [],
        "change_log": [],
        "last_validation": None,
        "validation_status": "not_run",
        "blocking_items": [],
        "release_receipt": None,
        "release_manuscript_sha256": None,
        "release_character_prompts_sha256": None,
        "release_scene_prompts_sha256": None,
        "release_docx_sha256": None,
        "delivery_manifest": {},
    }


def validate_state(state: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {
        "schema_version",
        "stage",
        "target_episodes",
        "allowed_episode_range",
        "first_episode_minutes",
        "later_episode_minutes_range",
        "draft_mode",
        "completed_through",
        "next_episode",
        "open_clues",
        "allowed_english_terms",
        "continuity_ledger",
        "logic_review_mode",
        "logic_risks",
        "character_arc_ledger",
        "antagonist_causal_chain",
        "semantic_reviews",
        "viewpoint_character",
        "video_runtime_mode",
        "novel_characters_per_minute_range",
        "validation_status",
        "blocking_items",
        "release_receipt",
        "release_manuscript_sha256",
        "release_character_prompts_sha256",
        "release_scene_prompts_sha256",
        "release_docx_sha256",
        "delivery_manifest",
    }
    missing = sorted(required - state.keys())
    if missing:
        errors.append("缺少字段：" + "、".join(missing))
        return errors
    if state["schema_version"] != SCHEMA_VERSION:
        errors.append(f"schema_version 必须为 {SCHEMA_VERSION}")
    if state["stage"] not in STAGES:
        errors.append("stage 不在允许范围内")
    if not isinstance(state["target_episodes"], int) or state["target_episodes"] <= 0:
        errors.append("target_episodes 必须是正整数")
    if state["draft_mode"] not in DRAFT_MODES:
        errors.append("draft_mode 必须是 auto_batch 或 manual_continue")
    if not 1 <= float(state["first_episode_minutes"]) <= 5:
        errors.append("first_episode_minutes 必须在 1-5 之间")
    if state["later_episode_minutes_range"] != [1, 2]:
        errors.append("later_episode_minutes_range 必须为 [1, 2]")
    if state["completed_through"] < 0 or state["next_episode"] != state["completed_through"] + 1:
        errors.append("next_episode 必须等于 completed_through + 1")
    expected = episode_range(state["target_episodes"], float(state.get("episode_tolerance_percent", 10)))
    if state["allowed_episode_range"] != expected:
        errors.append(f"allowed_episode_range 应为 {expected}")
    for name in ("open_clues", "allowed_english_terms"):
        if not isinstance(state[name], list):
            errors.append(f"{name} 必须是数组")
    if state["logic_review_mode"] != "strict":
        errors.append("logic_review_mode 必须为 strict")
    for name in ("logic_risks", "semantic_reviews"):
        if not isinstance(state[name], list):
            errors.append(f"{name} 必须是数组")
    for name in ("continuity_ledger", "character_arc_ledger", "antagonist_causal_chain"):
        if not isinstance(state[name], dict):
            errors.append(f"{name} 必须是对象")
    if state["video_runtime_mode"] not in VIDEO_RUNTIME_RANGES:
        errors.append("video_runtime_mode 必须是 pure_narration、dialogue_drama 或 hybrid")
    elif state["novel_characters_per_minute_range"] != VIDEO_RUNTIME_RANGES[state["video_runtime_mode"]]:
        errors.append("novel_characters_per_minute_range 与 video_runtime_mode 不匹配")
    if state["viewpoint_character"] is not None and not isinstance(state["viewpoint_character"], str):
        errors.append("viewpoint_character 必须是字符串或 null")
    if state["validation_status"] not in {"not_run", "passed", "failed", "stale"}:
        errors.append("validation_status 必须是 not_run、passed、failed 或 stale")
    if not isinstance(state["blocking_items"], list):
        errors.append("blocking_items 必须是数组")
    if not isinstance(state["delivery_manifest"], dict):
        errors.append("delivery_manifest 必须是对象")
    if state["stage"] == "complete":
        required_release_fields = (
            "release_receipt",
            "release_manuscript_sha256",
            "release_character_prompts_sha256",
            "release_scene_prompts_sha256",
            "release_docx_sha256",
        )
        missing_release = [name for name in required_release_fields if not state.get(name)]
        if state["validation_status"] != "passed":
            errors.append("complete 阶段要求 validation_status=passed")
        if state["blocking_items"]:
            errors.append("complete 阶段不允许存在 blocking_items")
        if missing_release:
            errors.append("complete 阶段缺少发布字段：" + "、".join(missing_release))
    return errors


def load_state(path: Path) -> dict[str, Any]:
    state = json.loads(path.read_text(encoding="utf-8"))
    if state.get("schema_version") == 1 and state.get("later_episode_minutes") == 1:
        state.pop("later_episode_minutes", None)
        state["later_episode_minutes_range"] = [1, 2]
        state["schema_version"] = 2
        state.setdefault("change_log", []).append(
            {"at": now_iso(), "event": "state_migrated", "from_schema": 1, "to_schema": 2}
        )
    if state.get("schema_version") == 2:
        defaults = new_state(
            int(state.get("target_episodes", 1)),
            float(state.get("first_episode_minutes", 3)),
            str(state.get("draft_mode", "auto_batch")),
        )
        for name in (
            "continuity_ledger",
            "logic_review_mode",
            "logic_risks",
            "character_arc_ledger",
            "antagonist_causal_chain",
            "semantic_reviews",
        ):
            state.setdefault(name, defaults[name])
        state["schema_version"] = 3
        state.setdefault("change_log", []).append(
            {"at": now_iso(), "event": "state_migrated", "from_schema": 2, "to_schema": 3}
        )
    if state.get("schema_version") == 3:
        state.setdefault("viewpoint_character", None)
        state.setdefault("video_runtime_mode", "hybrid")
        state.setdefault(
            "novel_characters_per_minute_range",
            VIDEO_RUNTIME_RANGES[state["video_runtime_mode"]],
        )
        state["schema_version"] = 4
        state.setdefault("change_log", []).append(
            {"at": now_iso(), "event": "state_migrated", "from_schema": 3, "to_schema": 4}
        )
    if state.get("schema_version") == 4:
        defaults = new_state(
            int(state.get("target_episodes", 1)),
            float(state.get("first_episode_minutes", 3)),
            str(state.get("draft_mode", "auto_batch")),
            str(state.get("video_runtime_mode", "hybrid")),
        )
        for name in (
            "validation_status",
            "blocking_items",
            "release_receipt",
            "release_manuscript_sha256",
            "release_character_prompts_sha256",
            "release_scene_prompts_sha256",
            "release_docx_sha256",
            "delivery_manifest",
        ):
            state.setdefault(name, defaults[name])
        state["schema_version"] = SCHEMA_VERSION
        state.setdefault("change_log", []).append(
            {"at": now_iso(), "event": "state_migrated", "from_schema": 4, "to_schema": SCHEMA_VERSION}
        )
    errors = validate_state(state)
    if errors:
        raise SystemExit("状态检查失败：\n" + "\n".join(errors))
    return state


def atomic_write(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = now_iso()
    errors = validate_state(state)
    if errors:
        raise SystemExit("拒绝写入无效状态：\n" + "\n".join(errors))
    fd, temp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(state, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def command_init(args: argparse.Namespace) -> None:
    path = args.project_dir / "project_state.json"
    if path.exists() and not args.force:
        raise SystemExit(f"状态文件已存在：{path}；如需覆盖请使用 --force")
    state = new_state(args.target_episodes, args.first_episode_minutes, args.draft_mode, args.video_mode)
    atomic_write(path, state)
    print(f"状态已创建：{path}")


def command_validate(args: argparse.Namespace) -> None:
    state = load_state(args.state)
    print(
        f"状态检查通过：阶段 {state['stage']}，已完成至第 {state['completed_through']} 集，"
        f"下一集为第 {state['next_episode']} 集。"
    )


def command_resume(args: argparse.Namespace) -> None:
    state = load_state(args.state)
    lower, upper = state["allowed_episode_range"]
    print(f"当前阶段：{state['stage']}")
    print(f"目标约 {state['target_episodes']} 集，允许区间 {lower}-{upper} 集")
    print(f"第一集 {state['first_episode_minutes']} 分钟，后续每集按剧情在 1-2 分钟内安排")
    print(f"续写模式：{state['draft_mode']}")
    print(
        f"视频模式：{state['video_runtime_mode']}；小说正文每分钟 "
        f"{state['novel_characters_per_minute_range'][0]}-"
        f"{state['novel_characters_per_minute_range'][1]} 字"
    )
    print(f"恢复点：已完成第 {state['completed_through']} 集；从第 {state['next_episode']} 集继续")
    print(f"待回收伏笔：{'、'.join(state['open_clues']) if state['open_clues'] else '无'}")
    blocking = [
        item for item in state["logic_risks"]
        if item.get("severity") == "high" and item.get("status") not in {"resolved", "user_confirmed", "intentionally_open"}
    ]
    print(f"未解决高风险逻辑问题：{len(blocking)} 项")


def command_record_batch(args: argparse.Namespace) -> None:
    state = load_state(args.state)
    if args.through < state["completed_through"]:
        raise SystemExit("--through 不能早于现有完成集数")
    state["completed_through"] = args.through
    state["next_episode"] = args.through + 1
    state["stage"] = "drafting"
    for clue in args.open_clue:
        if clue not in state["open_clues"]:
            state["open_clues"].append(clue)
    for clue in args.resolve_clue:
        if clue in state["open_clues"]:
            state["open_clues"].remove(clue)
        if clue not in state["resolved_clues"]:
            state["resolved_clues"].append(clue)
    if args.validation_json:
        state["last_validation"] = json.loads(args.validation_json.read_text(encoding="utf-8"))
    state["validation_status"] = "passed" if args.validation_json else "stale"
    state["blocking_items"] = []
    state["release_receipt"] = None
    state["release_manuscript_sha256"] = None
    state["release_character_prompts_sha256"] = None
    state["release_scene_prompts_sha256"] = None
    state["release_docx_sha256"] = None
    state["delivery_manifest"] = {}
    state["change_log"].append({"at": now_iso(), "event": "batch_completed", "through": args.through})
    atomic_write(args.state, state)
    print(f"批次状态已更新：完成至第 {args.through} 集，下一集为第 {args.through + 1} 集。")


def command_allow_term(args: argparse.Namespace) -> None:
    state = load_state(args.state)
    for term in args.term:
        if term.casefold() not in {item.casefold() for item in state["allowed_english_terms"]}:
            state["allowed_english_terms"].append(term)
    atomic_write(args.state, state)
    print("英文专名白名单已更新。")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="管理 AI 漫剧小说项目的唯一状态文件。")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="初始化 project_state.json")
    init.add_argument("project_dir", type=Path)
    init.add_argument("--target-episodes", type=int, required=True)
    init.add_argument("--first-episode-minutes", type=float, required=True)
    init.add_argument("--draft-mode", choices=sorted(DRAFT_MODES), default="auto_batch")
    init.add_argument("--video-mode", choices=sorted(VIDEO_RUNTIME_RANGES), default="hybrid")
    init.add_argument("--force", action="store_true")
    init.set_defaults(func=command_init)

    validate = sub.add_parser("validate", help="检查状态文件")
    validate.add_argument("state", type=Path)
    validate.set_defaults(func=command_validate)

    resume = sub.add_parser("resume", help="输出确定的恢复点")
    resume.add_argument("state", type=Path)
    resume.set_defaults(func=command_resume)

    record = sub.add_parser("record-batch", help="在批次校验通过后记录完成点")
    record.add_argument("state", type=Path)
    record.add_argument("--through", type=int, required=True)
    record.add_argument("--open-clue", action="append", default=[])
    record.add_argument("--resolve-clue", action="append", default=[])
    record.add_argument("--validation-json", type=Path)
    record.set_defaults(func=command_record_batch)

    allow = sub.add_parser("allow-term", help="记录允许使用的英文专有名词")
    allow.add_argument("state", type=Path)
    allow.add_argument("--term", action="append", required=True)
    allow.set_defaults(func=command_allow_term)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "init":
        if args.target_episodes <= 0:
            raise SystemExit("--target-episodes 必须是正整数")
        if not 1 <= args.first_episode_minutes <= 5:
            raise SystemExit("--first-episode-minutes 必须在 1-5 之间")
    args.func(args)


if __name__ == "__main__":
    main()
