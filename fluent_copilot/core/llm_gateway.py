"""大模型网关：应用内唯一接触外部 LLM API 的地方。

任何 OpenAI 兼容端点（智谱 GLM / 阿里 DashScope / 自建）都只需改 config。
stream_chat 是 agent 异步核心的主通道：流式吐 text_delta + 末尾一条完整消息 dict。
"""
from __future__ import annotations

import logging
from typing import Any, AsyncIterator

from openai import AsyncOpenAI, OpenAI

from fluent_copilot.config import Config

logger = logging.getLogger(__name__)


def _message_to_dict(msg: Any) -> dict[str, Any]:
    """把 SDK message 对象转成纯 dict（统一 async 路径的消息形状）。"""
    out: dict[str, Any] = {"role": "assistant", "content": msg.content or ""}
    if getattr(msg, "tool_calls", None):
        out["tool_calls"] = [
            {
                "id": tc.id,
                "type": "function",
                "function": {
                    "name": tc.function.name,
                    "arguments": tc.function.arguments or "{}",
                },
            }
            for tc in msg.tool_calls
        ]
    return out


class LLMGateway:
    def __init__(self, cfg: Config):
        # 允许无 key 启动(分发场景):首次调用时给出配置引导,而不是进程崩溃
        self._api_key = cfg.api_key
        self._base_url = cfg.llm_base_url
        self.client = OpenAI(api_key=cfg.api_key or "unset", base_url=cfg.llm_base_url)
        self.async_client = AsyncOpenAI(api_key=cfg.api_key or "unset", base_url=cfg.llm_base_url)
        self.model = cfg.llm_model

    @property
    def api_key(self) -> str:
        return self._api_key

    def _check_configured(self) -> None:
        if not self._api_key:
            raise RuntimeError(
                "尚未配置 API Key:点击输入框底部的 ⚙ 模型菜单 → API 设置…,选择供应商并填入 Key 后保存即可开始使用。"
            )

    def update(self, base_url: str, api_key: str, model: str) -> None:
        """热更新端点与模型(设置对话框保存时调用,下一轮对话生效)。"""
        self._api_key = api_key
        self._base_url = base_url
        self.client = OpenAI(api_key=api_key or "unset", base_url=base_url)
        self.async_client = AsyncOpenAI(api_key=api_key or "unset", base_url=base_url)
        self.model = model

    # ------------------------------------------------------------------
    # 同步非流式（遗留路径，REPL 之外基本不再用）
    # ------------------------------------------------------------------
    def chat(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        """一轮对话。返回 message（可能是 tool_calls，也可能直接是文本）。"""
        kwargs: dict = {"model": self.model, "messages": messages}
        if tools:
            kwargs["tools"] = tools
        resp = self.client.chat.completions.create(**kwargs)
        return resp.choices[0].message

    # ------------------------------------------------------------------
    # 异步非流式（强制收尾 / 回退用）
    # ------------------------------------------------------------------
    async def achat(
        self, messages: list[dict], tools: list[dict] | None = None
    ) -> dict[str, Any]:
        self._check_configured()
        kwargs: dict = {"model": self.model, "messages": messages}
        if tools:
            kwargs["tools"] = tools
        resp = await self.async_client.chat.completions.create(**kwargs)
        return _message_to_dict(resp.choices[0].message)

    # ------------------------------------------------------------------
    # 异步流式（agent 主通道）
    # ------------------------------------------------------------------
    async def stream_chat(
        self, messages: list[dict], tools: list[dict] | None = None
    ) -> AsyncIterator[dict[str, Any]]:
        """流式一轮对话。

        依次产出：
          {"type": "text_delta", "content": str}
          ...
          {"type": "message", "message": {"role": "assistant", "content": str,
                                           "tool_calls": [...]?}}
        流式请求失败时自动回退非流式（整段文本一次给出）。
        """
        self._check_configured()
        kwargs: dict = {"model": self.model, "messages": messages, "stream": True}
        if tools:
            # GLM 的 tool_choice 只支持 "auto"，省略即默认 auto
            kwargs["tools"] = tools
        try:
            stream = await self.async_client.chat.completions.create(**kwargs)
        except Exception as exc:
            logger.warning("stream 请求失败，回退非流式: %s", exc)
            msg = await self.achat(messages, tools)
            if msg["content"]:
                yield {"type": "text_delta", "content": msg["content"]}
            yield {"type": "message", "message": msg}
            return

        content = ""
        tool_calls: dict[int, dict[str, str]] = {}
        try:
            async for chunk in stream:
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta
                if delta is None:
                    continue
                if delta.content:
                    content += delta.content
                    yield {"type": "text_delta", "content": delta.content}
                for tc in delta.tool_calls or []:
                    slot = tool_calls.setdefault(
                        tc.index, {"id": "", "name": "", "arguments": ""}
                    )
                    if tc.id:
                        slot["id"] = tc.id
                    if tc.function:
                        if tc.function.name:
                            slot["name"] = tc.function.name
                        if tc.function.arguments:
                            slot["arguments"] += tc.function.arguments
        except Exception as exc:
            # 流中途断掉：若还没产出任何内容就回退非流式；已有内容则按已有内容收尾
            logger.warning("stream 中断: %s", exc)
            if not content and not tool_calls:
                msg = await self.achat(messages, tools)
                if msg["content"]:
                    yield {"type": "text_delta", "content": msg["content"]}
                yield {"type": "message", "message": msg}
                return

        msg: dict[str, Any] = {"role": "assistant", "content": content}
        if tool_calls:
            msg["tool_calls"] = [
                {
                    "id": slot["id"] or f"call_{idx}",
                    "type": "function",
                    "function": {
                        "name": slot["name"],
                        "arguments": slot["arguments"] or "{}",
                    },
                }
                for idx, slot in sorted(tool_calls.items())
            ]
        yield {"type": "message", "message": msg}
