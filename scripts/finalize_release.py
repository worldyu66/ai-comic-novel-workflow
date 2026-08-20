#!/usr/bin/env python3
"""Atomically validate the complete delivery bundle, export Word, and close project state."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import project_state


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run(command: list[str]) -> dict[str, object]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", env=env)
    return {
        "command": command,
        "exit_status": result.returncode,
        "output": (result.stdout + result.stderr).strip(),
    }


def write_receipt(path: Path, receipt: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def mark_failed(state_path: Path, state: dict[str, object], report_path: Path, failures: list[str]) -> None:
    state["stage"] = "release"
    state["validation_status"] = "failed"
    state["blocking_items"] = failures
    state["release_receipt"] = None
    state["release_manuscript_sha256"] = None
    state["release_character_prompts_sha256"] = None
    state["release_scene_prompts_sha256"] = None
    state["release_docx_sha256"] = None
    state["delivery_manifest"] = {}
    state.setdefault("change_log", []).append(
        {
            "at": project_state.now_iso(),
            "event": "release_failed",
            "report": str(report_path.resolve()),
            "blocking_items": failures,
        }
    )
    project_state.atomic_write(state_path, state)


def main() -> None:
    parser = argparse.ArgumentParser(description="校验完整交付包、导出 Word 并原子关闭项目状态。")
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("state", type=Path)
    parser.add_argument("final_review", type=Path)
    parser.add_argument("character_prompts", type=Path)
    parser.add_argument("scene_prompts", type=Path)
    parser.add_argument("docx", type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    scripts = Path(__file__).resolve().parent
    report_path = args.report or args.manuscript.parent / "reports" / "release_receipt.json"
    prompt_report = args.manuscript.parent / "reports" / "prompt_deliverables.json"
    quality_report = args.manuscript.parent / "reports" / "manuscript_quality.json"
    narrative_report = args.manuscript.parent / "reports" / "narrative_contract.json"
    state = project_state.load_state(args.state)

    state["stage"] = "release"
    state["validation_status"] = "not_run"
    state["blocking_items"] = []
    state["release_receipt"] = None
    state["release_manuscript_sha256"] = None
    state["release_character_prompts_sha256"] = None
    state["release_scene_prompts_sha256"] = None
    state["release_docx_sha256"] = None
    state["delivery_manifest"] = {}
    project_state.atomic_write(args.state, state)

    commands = [
        [
            sys.executable,
            str(scripts / "validate_episode_payoffs.py"),
            str(args.manuscript),
            "--target-episodes",
            str(state["target_episodes"]),
            "--require-complete",
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
            str(scripts / "validate_narrative_contract.py"),
            str(args.manuscript),
            str(args.state),
            "--report",
            str(narrative_report),
        ],
        [
            sys.executable,
            str(scripts / "validate_release_consistency.py"),
            str(args.manuscript),
            str(args.state),
            str(args.final_review),
        ],
        [
            sys.executable,
            str(scripts / "validate_prompt_deliverables.py"),
            str(args.character_prompts),
            str(args.scene_prompts),
            "--report",
            str(prompt_report),
        ],
    ]
    checks = [run(command) for command in commands]
    failures = [str(check["output"]) for check in checks if check["exit_status"] != 0]
    receipt: dict[str, object] = {
        "created_at": project_state.now_iso(),
        "passed": False,
        "checks": checks,
        "blocking_items": failures,
    }
    if failures:
        write_receipt(report_path, receipt)
        mark_failed(args.state, state, report_path, failures)
        raise SystemExit("发布事务失败：\n" + "\n".join(failures))

    args.docx.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="comic_release_", dir=args.docx.parent) as temp:
        temp_docx = Path(temp) / args.docx.name
        export_check = run(
            [
                sys.executable,
                str(scripts / "export_final_docx.py"),
                str(args.manuscript),
                str(temp_docx),
                "--title",
                args.title,
            ]
        )
        verify_check = (
            run(
                [
                    sys.executable,
                    str(scripts / "verify_final_docx.py"),
                    str(args.manuscript),
                    str(temp_docx),
                ]
            )
            if export_check["exit_status"] == 0
            else {
                "command": ["verify_final_docx.py", "skipped"],
                "exit_status": 1,
                "output": "Word 导出失败，跳过 Word 验证。",
            }
        )
        checks.extend((export_check, verify_check))
        failures = [str(check["output"]) for check in (export_check, verify_check) if check["exit_status"] != 0]
        if failures:
            receipt["checks"] = checks
            receipt["blocking_items"] = failures
            write_receipt(report_path, receipt)
            mark_failed(args.state, state, report_path, failures)
            raise SystemExit("发布事务失败：\n" + "\n".join(failures))
        os.replace(temp_docx, args.docx)

    manifest = {
        "manuscript": {"path": str(args.manuscript.resolve()), "sha256": sha256(args.manuscript)},
        "character_prompts": {
            "path": str(args.character_prompts.resolve()),
            "sha256": sha256(args.character_prompts),
        },
        "scene_prompts": {"path": str(args.scene_prompts.resolve()), "sha256": sha256(args.scene_prompts)},
        "final_review": {"path": str(args.final_review.resolve()), "sha256": sha256(args.final_review)},
        "docx": {"path": str(args.docx.resolve()), "sha256": sha256(args.docx)},
    }
    receipt.update({"passed": True, "checks": checks, "blocking_items": [], "delivery_manifest": manifest})
    write_receipt(report_path, receipt)

    state["stage"] = "complete"
    state["validation_status"] = "passed"
    state["blocking_items"] = []
    state["release_receipt"] = str(report_path.resolve())
    state["release_manuscript_sha256"] = manifest["manuscript"]["sha256"]
    state["release_character_prompts_sha256"] = manifest["character_prompts"]["sha256"]
    state["release_scene_prompts_sha256"] = manifest["scene_prompts"]["sha256"]
    state["release_docx_sha256"] = manifest["docx"]["sha256"]
    state["delivery_manifest"] = manifest
    state.setdefault("change_log", []).append(
        {"at": project_state.now_iso(), "event": "release_completed", "report": str(report_path.resolve())}
    )
    project_state.atomic_write(args.state, state)
    print(f"发布事务完成：{report_path}")
    print(f"最终 Word：{args.docx}")


if __name__ == "__main__":
    main()
