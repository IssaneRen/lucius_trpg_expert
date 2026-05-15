#!/usr/bin/env python3
"""同步 AI 平台适配层配置。

该脚本将 `rules/`、`agents/`、`skills/` 中的源定义复制到平台目录，
用于降低 Cursor / Claude / Codex 多份配置的漂移风险。
"""

from __future__ import annotations

import re
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


def _copy_rules_as_mdc(src: Path, dst: Path) -> None:
    """将 rules/*.md 复制到目标目录，扩展名改为 .mdc（跳过 README）。"""
    if not src.exists():
        return
    for item in src.iterdir():
        if item.name.lower() == "readme.md":
            continue
        if item.is_dir():
            shutil.copytree(item, dst / item.name)
        elif item.suffix == ".md":
            target = dst / (item.stem + ".mdc")
            shutil.copy2(item, target)
        else:
            shutil.copy2(item, dst / item.name)


def _parse_agent_md(md_path: Path) -> dict[str, str]:
    """解析 agents/*.md，提取 name / description / developer_instructions。

    - name: 文件名（不含 .md）
    - description: ## 职责 下第一行非空文本
    - developer_instructions: 文件全文
    """
    name = md_path.stem
    content = md_path.read_text(encoding="utf-8")

    # 提取 ## 职责 下第一行非空内容作为 description
    description = ""
    match = re.search(r"^## 职责\s*\n(.*?)(?=\n## |\Z)", content, re.MULTILINE | re.DOTALL)
    if match:
        lines = match.group(1).strip().splitlines()
        for line in lines:
            stripped = line.strip().lstrip("- ").strip()
            if stripped:
                description = stripped
                break

    return {
        "name": name,
        "description": description,
        "developer_instructions": content,
    }


def _generate_toml(agent: dict[str, str]) -> str:
    """生成 Codex agent .toml 文件内容。"""
    name = agent["name"].replace('"', '\\"')
    desc = agent["description"].replace('"', '\\"')
    instructions = agent["developer_instructions"]
    # TOML multi-line basic strings: only """ itself needs escaping
    if '"""' in instructions:
        instructions = instructions.replace('"""', '\"\"\"')
    return (
        f'name = "{name}"\n'
        f'description = "{desc}"\n'
        f"developer_instructions = '''\n"
        f"{instructions}'''\n"
    )


def _strip_frontmatter(text: str) -> str:
    """移除 markdown 文件开头的 YAML frontmatter。"""
    stripped = text.strip()
    if stripped.startswith("---"):
        end = stripped.find("---", 3)
        if end != -1:
            return stripped[end + 3:].strip()
    return stripped


def _generate_codex_agents_md(rules_dir: Path) -> str:
    """将 rules/*.md 合并为 codex/AGENTS.md 项目级规则汇总。"""
    parts: list[str] = [
        "# Project Rules (Auto-generated)\n\n"
        "本文件由 `scripts/sync_ai_configs.py` 自动生成，汇总 `rules/` 目录中的项目规则。\n"
        "请勿手动编辑，源文件位于 `rules/` 目录。\n"
    ]
    if not rules_dir.exists():
        return parts[0]

    for rule_file in sorted(rules_dir.glob("*.md")):
        if rule_file.name.lower() == "readme.md":
            continue
        content = rule_file.read_text(encoding="utf-8")
        content = _strip_frontmatter(content)
        parts.append(f"\n---\n\n{content}\n")

    return "\n".join(parts)


def main() -> None:
    """执行平台配置同步。"""
    # --- Cursor ---
    cursor_rules = ROOT / ".cursor" / "rules"
    _reset_dir(cursor_rules)
    _copy_rules_as_mdc(ROOT / "rules", cursor_rules)

    # --- Claude ---
    claude_agents = ROOT / ".claude" / "agents"
    claude_skills = ROOT / ".claude" / "skills"
    _reset_dir(claude_agents)
    _reset_dir(claude_skills)
    _copy_tree(ROOT / "agents", claude_agents)
    _copy_tree(ROOT / "skills", claude_skills)

    # --- Codex ---
    codex_agents = ROOT / "codex" / "agents"
    _reset_dir(codex_agents)

    # 生成 agent .toml 文件
    agents_dir = ROOT / "agents"
    if agents_dir.exists():
        for md_file in sorted(agents_dir.glob("*.md")):
            agent = _parse_agent_md(md_file)
            toml_path = codex_agents / f"{agent['name']}.toml"
            toml_path.write_text(_generate_toml(agent), encoding="utf-8")
            print(f"  -> codex/agents/{agent['name']}.toml")

    # 生成 codex/AGENTS.md（项目级规则汇总）
    agents_md_content = _generate_codex_agents_md(ROOT / "rules")
    (ROOT / "codex" / "AGENTS.md").write_text(agents_md_content, encoding="utf-8")
    print("  -> codex/AGENTS.md")

    # 更新 codex/README.md 说明
    (ROOT / "codex" / "README.md").write_text(
        "# Codex Workspace\n\n"
        "Codex CLI 相关配置入口。\n\n"
        "- `agents/`: Agent 定义（.toml），由 sync 脚本从 `agents/*.md` 生成\n"
        "- `AGENTS.md`: 项目级规则汇总，由 sync 脚本从 `rules/*.md` 生成\n",
        encoding="utf-8",
    )

    # 清理旧的占位目录（prompts/profiles 已不再需要）
    for legacy_dir in ["prompts", "profiles"]:
        legacy_path = ROOT / "codex" / legacy_dir
        if legacy_path.exists():
            shutil.rmtree(legacy_path)

    print("sync_ai_configs: completed")


if __name__ == "__main__":
    main()
