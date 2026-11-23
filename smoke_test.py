# -*- coding: utf-8 -*-
"""端到端冒烟测试：真实 LLM + 真实 Fluent 会话，验证 agent 闭环。

用法：.venv\\Scripts\\python smoke_test.py
前提：Fluent 已通过 start-fluent-copilot.bat（或等效 -sifile 命令）启动。
Fluent 不在也没关系：Fluent 工具会返回友好错误，知识库工具照常可验。
"""
import sys

from fluent_copilot.config import load_config
from fluent_copilot.core.agent import Agent
from fluent_copilot.core.llm_gateway import LLMGateway
from fluent_copilot.core.loop import run_sync


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    cfg = load_config()
    print(f"[config] model={cfg.llm_model} base_url={cfg.llm_base_url}")
    print(f"[config] sifile_dir={cfg.sifile_dir}")

    # 直接验证 Fluent 附着层（不经 LLM）；用默认单例，避免重复建连
    from fluent_copilot.fluent.mcp_backend import FluentMCPBackend

    backend = FluentMCPBackend.get_default()
    sifile = FluentMCPBackend.discover_sifile(cfg.sifile_dir)
    print(f"[attach] sifile={sifile}")
    if sifile is not None and not backend.is_connected:
        print("[attach]", run_sync(backend.connect_via_sifile(cfg.sifile_dir)))
    print(f"[attach] connected={backend.is_connected}")

    # 再走完整 agent 闭环
    gateway = LLMGateway(cfg)
    agent = Agent(
        gateway,
        max_rounds=cfg.max_tool_rounds,
        on_event=lambda s: print(s),
        trajectory_file=cfg.log_dir / "trajectory.jsonl",
    )
    history: list[dict] = []
    questions = [
        "当前本机 Fluent 会话是什么状态？",
        "列出当前 case 的边界条件 zone，并简单判断这是什么类型的仿真。",
    ]
    if not backend.is_connected:
        questions = [
            "当前本机 Fluent 会话是什么状态？",
            "在知识库里查一下 GPU 求解器有什么限制。",
        ]
    for question in questions:
        print(f"\n===== 问：{question} =====")
        answer = agent.run(history, question)
        print(f"----- 答：{answer}")


if __name__ == "__main__":
    main()
