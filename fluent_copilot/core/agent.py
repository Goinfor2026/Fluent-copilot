"""agent 循环：消息 → LLM → 工具调用 → 结果回喂 → 最终回答。

刻意手写而不上框架：流程零抽象，轨迹落盘和流式处理完全自己掌控。

arun 是唯一核心（async）：结构化事件回调 emit(dict) 供 SSE 直通；
同步 run() 只是把 arun 搬到常驻事件循环上跑（见 core/loop.py）。
"""
from __future__ import annotations

import asyncio
import json
import time
from pathlib import Path
from typing import Callable

from fluent_copilot.core import tools
from fluent_copilot.core.llm_gateway import LLMGateway

SYSTEM_PROMPT = """你是 Fluent Copilot，帮助工程师使用 ANSYS Fluent 的本地助手。

工作方式（agent 循环，最重要的一条规则）：
你处于连续执行的 agent 循环中——每次工具返回结果后，先评估：用户的任务是否**真正完成**？
- 未完成 → 继续调用下一个工具，不要中途总结、不要问"需要我继续吗"、不要提前给出结论；
- 只有两种情况可以停止并输出最终回答：①任务已达成（操作已执行且验证过/问题已查清并解答）；
  ②确实被阻塞、必须由用户提供信息或决策——此时明确说明已完成什么、卡在哪、需要用户提供什么。
- 中间轮次如需向用户说明进展，可以在调用工具的同时附带一句话，但不要把它当作最终回答。

通用规则：
- 用简体中文回答；最终回答保持简洁、面向工程师（中间过程不啰嗦）。
- 工具返回错误时，向用户解释原因并给出可操作的建议。
- 危险操作（如删除边界、覆盖文件）前应先向用户确认。

知识库与转录：
- 回答 Fluent 概念、报错含义、操作方法类问题时，优先使用本地知识库：
  先 search_wiki 找相关页，再 read_wiki_page 读整页，可沿 wikilinks 继续跳转；
  基于知识库内容回答并注明来源页名。知识库没有的，再用自己的知识回答并说明。
- 用户报告仿真出错、警告、结果异常或想复盘操作时，先用 read_transcript 看实际情况
  （what=errors/warnings/tail），不要凭空猜测。

Fluent 会话操作准则（严格执行，禁止跳步）：
1. **先查配方**：准备写操作代码前，先 search_fluent_recipes 搜历史验证过的配方；
   命中则直接复用/微调（对象名仍需与当前会话核对），这才是最快路径。
2. **先读状态**：操作前必须先 get_fluent_state 或 list_fluent_objects 了解当前会话。
3. **禁止猜测 API 路径**。写任何 execute_fluent_code 之前，必须先确认路径真实存在：
   - 不确定路径结构 → search_fluent_api 搜关键词,或 get_fluent_context 批量核实
     （它会返回激活状态/当前值/可选值/子对象名,一次到位）;
   - 涉及命名对象（边界/区域/材料）→ 必须先 list_fluent_objects 拿到**真实名称**
     （如 velocity_inlet_1）,代码里绝不允许自编对象名;
   - 不确定某路径下有什么 → get_fluent_help 看文档和子对象清单。
4. **写操作先校验**：修改类代码在 execute 前如无把握,先让 validate 结果说话——
   execute_fluent_code 自带沙箱校验,校验失败时按报错修正,不要原样重试。
5. **失败即诊断**：执行报 AttributeError/路径错误时,不要换一个猜的路径再试;
   应回到第 3 步用 get_fluent_context 核实正确路径后再来。
6. 执行成功后,如需向用户确认效果,可用 get_fluent_state 复读相关路径。

可用工具清单：
1. get_fluent_state — 读会话状态（求解器/物理模型/边界）
2. get_fluent_context — 批量核实路径（激活/当前值/可选值/子对象名）★防错关键
3. search_fluent_recipes — 搜历史验证过的操作配方 ★写码前先查
4. execute_fluent_code — 执行 Python 代码操作 Fluent（沙箱安全,变量 solver/session）
5. search_fluent_api — 关键词搜索 Settings API 路径
6. get_fluent_help — 某路径的详细帮助与子对象
7. list_fluent_objects — 列出命名对象（边界/区域/材料）的真实名称
8. summarize_fluent_setup — 完整设置摘要（Report > Summary）
9. search_wiki / read_wiki_page — 检索阅读本地知识库
10. read_transcript — 读取 .trn 转录文件"""

EmitFn = Callable[[dict], None]
CancelFn = Callable[[], bool]


class CancelledError(RuntimeError):
    """调用方主动取消（客户端断开）。"""


class Agent:
    def __init__(
        self,
        gateway: LLMGateway,
        max_rounds: int = 30,
        on_event: Callable[[str], None] | None = None,
        trajectory_file: Path | None = None,
    ):
        self.gateway = gateway
        self.max_rounds = max_rounds
        self.on_event = on_event or (lambda s: None)
        self.trajectory_file = trajectory_file

    def _log(self, event: dict) -> None:
        if self.trajectory_file is None:
            return
        self.trajectory_file.parent.mkdir(parents=True, exist_ok=True)
        event = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), **event}
        with open(self.trajectory_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False, default=str) + "\n")

    # ------------------------------------------------------------------
    # 异步核心（服务端主路径）
    # ------------------------------------------------------------------
    async def arun(
        self,
        history: list[dict],
        user_input: str,
        emit: EmitFn | None = None,
        is_cancelled: CancelFn | None = None,
    ) -> str:
        """处理一轮用户输入；history 原地追加，返回最终回答文本。

        emit 收到结构化事件 dict（type: text_delta/tool_call/tool_result/final/cancelled），
        供 SSE 直通前端；on_event（构造参数）继续收到旧版单行预览字符串。
        """
        emit = emit or (lambda e: None)

        def check_cancelled() -> None:
            if is_cancelled is not None and is_cancelled():
                emit({"type": "cancelled"})
                raise CancelledError("客户端已断开")

        history.append({"role": "user", "content": user_input})
        self._log({"event": "user", "content": user_input})

        messages = [{"role": "system", "content": SYSTEM_PROMPT}, *history]

        for _ in range(self.max_rounds):
            check_cancelled()
            final_msg: dict | None = None
            async for ev in self.gateway.stream_chat(messages, tools=tools.openai_schemas()):
                if ev["type"] == "text_delta":
                    emit({"type": "text_delta", "content": ev["content"]})
                else:
                    final_msg = ev["message"]
            if final_msg is None:  # 理论不可达（stream_chat 保证收尾 message）
                raise RuntimeError("LLM 未返回消息")

            if not final_msg.get("tool_calls"):
                answer = final_msg.get("content") or ""
                history.append({"role": "assistant", "content": answer})
                self._log({"event": "assistant", "content": answer})
                emit({"type": "final", "content": answer})
                return answer

            messages.append({
                "role": "assistant",
                "content": final_msg.get("content") or "",
                "tool_calls": final_msg["tool_calls"],
            })
            for tc in final_msg["tool_calls"]:
                name = tc["function"]["name"]
                arguments = tc["function"]["arguments"]
                emit({"type": "tool_call", "id": tc["id"], "name": name, "arguments": arguments})
                result = await tools.dispatch_async(name, arguments)
                ok = '"error"' not in result[:50] and not result.lstrip().startswith('{"error"')
                emit({
                    "type": "tool_result",
                    "id": tc["id"],
                    "name": name,
                    "result": result,
                    "ok": ok,
                })
                preview = result if len(result) <= 200 else result[:200] + "..."
                self.on_event(f"[工具] {name}({arguments}) -> {preview}")
                self._log({
                    "event": "tool_call",
                    "name": name,
                    "arguments": arguments,
                    "result": result,
                })
                # 操作配方沉淀:执行成功且确为改状态的代码 → 存入配方库供复用
                if name == "execute_fluent_code" and '"status": "ok"' in result[:60]:
                    try:
                        import json as _json

                        code = _json.loads(arguments).get("code", "")
                        if code and "=" in code or "(" in code:
                            tools.append_recipe(user_input, code)
                    except Exception:
                        pass
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "content": result,
                })

        # 工具轮数用尽：强制无工具收尾，基于已收集的信息给出回答
        check_cancelled()
        final = await self.gateway.achat(messages, tools=None)
        answer = final.get("content") or "（轮数用尽且未能生成回答）"
        history.append({"role": "assistant", "content": answer})
        self._log({"event": "assistant_forced_final", "content": answer})
        emit({"type": "final", "content": answer})
        return answer

    # ------------------------------------------------------------------
    # 同步 facade（REPL / 冒烟测试，走常驻事件循环）
    # ------------------------------------------------------------------
    def run(self, history: list[dict], user_input: str) -> str:
        from fluent_copilot.core.loop import run_sync

        return run_sync(self.arun(history, user_input))
