"""常驻后台事件循环：同步调用方（REPL / 冒烟测试）桥接到 async 核心。

FluentMCPBackend 单例内部持有 asyncio.Lock，必须固定活在同一个事件循环里；
不能每次 asyncio.run()（每次新循环会让锁绑定到不同 loop 而报错）。
FastAPI 服务进程用自己的 uvicorn 循环，同一进程内不应再经过本模块。
"""
from __future__ import annotations

import asyncio
import threading
from typing import Awaitable, TypeVar

T = TypeVar("T")

_loop: asyncio.AbstractEventLoop | None = None
_lock = threading.Lock()


def _ensure_loop() -> asyncio.AbstractEventLoop:
    global _loop
    with _lock:
        if _loop is not None and not _loop.is_closed():
            return _loop
        loop = asyncio.new_event_loop()
        thread = threading.Thread(
            target=loop.run_forever, name="copilot-asyncio", daemon=True
        )
        thread.start()
        _loop = loop
        return _loop


def run_sync(coro: Awaitable[T]) -> T:
    """在常驻循环上跑协程，阻塞当前线程直到出结果。"""
    future = asyncio.run_coroutine_threadsafe(coro, _ensure_loop())
    return future.result()
