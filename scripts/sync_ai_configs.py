#!/usr/bin/env python3
"""同步 AI 平台适配层配置。

该脚本将 `rules/`、`agents/`、`skills/` 中的源定义复制到平台目录，
用于降低 Cursor / Claude / Codex 多份配置的漂移风险。
"""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _reset_dir(path: Path) -> None:
    """重建目录，保证每次同步结果可预测。"""
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def _copy_tree(src: Path, dst: Path) -> None:
    """将目录内容复制到目标目录。"""
    if not src.exists():
        return
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)


def main() -> None:
    """执行平台配置同步。"""
    cursor_rules = ROOT / ".cursor" / "rules"
    claude_agents = ROOT / ".claude" / "agents"
    claude_skills = ROOT / ".claude" / "skills"
    codex_prompts = ROOT / "codex" / "prompts"
    codex_profiles = ROOT / "codex" / "profiles"

    _reset_dir(cursor_rules)
    _reset_dir(claude_agents)
    _reset_dir(claude_skills)
    _reset_dir(codex_prompts)
    _reset_dir(codex_profiles)

    _copy_tree(ROOT / "rules", cursor_rules)
    _copy_tree(ROOT / "agents", claude_agents)
    _copy_tree(ROOT / "skills", claude_skills)

    (codex_prompts / "README.md").write_text(
        "# Codex Prompts\n\n该目录由 scripts/sync_ai_configs.py 维护。\n",
        encoding="utf-8",
    )
    (codex_profiles / "README.md").write_text(
        "# Codex Profiles\n\n该目录由 scripts/sync_ai_configs.py 维护。\n",
        encoding="utf-8",
    )
    print("sync_ai_configs: completed")


if __name__ == "__main__":
    main()
