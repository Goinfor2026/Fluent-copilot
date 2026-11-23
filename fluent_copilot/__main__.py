"""终端 REPL 入口：python -m fluent_copilot"""
from __future__ import annotations

import sys

from fluent_copilot.config import load_config
from fluent_copilot.core.agent import Agent
from fluent_copilot.core.llm_gateway import LLMGateway
from fluent_copilot.knowledge.vault import Vault

BANNER = """==================================================
 Fluent Copilot v0.2  （输入 exit / quit 退出）
 已注册工具：get_fluent_state / execute_fluent_code /
   search_fluent_api / get_fluent_help / list_fluent_objects /
   summarize_fluent_setup / search_wiki / read_wiki_page / read_transcript
=================================================="""


def main() -> None:
    try:  # Windows 控制台中文输出保护
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    cfg = load_config()
    Vault.default_root = cfg.vault_path
    gateway = LLMGateway(cfg)
    agent = Agent(
        gateway,
        max_rounds=cfg.max_tool_rounds,
        trajectory_file=cfg.log_dir / "trajectory.jsonl",
    )

    print(BANNER)
    history: list[dict] = []
    while True:
        try:
            q = input("\n你> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not q:
            continue
        if q.lower() in ("exit", "quit", "q"):
            break
        try:
            answer = agent.run(history, q)
        except Exception as exc:
            answer = f"[出错] {type(exc).__name__}: {exc}"
        print(f"\nCopilot> {answer}")


if __name__ == "__main__":
    main()
