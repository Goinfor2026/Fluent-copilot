"""Fluent MCP 后端集成层（async 原生）。

基于 ansys/pyfluent-mcp 官方包的 PyFluentBackend。官方后端的方法是 async 的
（内部用 asyncio.to_thread 卸载同步 gRPC），本包装层必须 await——
旧版漏掉 await 导致全部 Fluent 工具失效，这是重写修复的第一个问题。

提供：
- sifile 自动发现与连接（cleanup_on_exit=False：断开绝不退 Fluent）
- 会话状态读取（版本/求解器/模型/边界）
- 安全代码执行（沙箱 + 意图守卫，RunCodeResult.status = ok|error）
- API 搜索与帮助、命名对象、网格质量、场变量、设置摘要

注意：单例内部（经官方后端的 asyncio.Lock）绑定在首次使用它的事件循环上，
FastAPI 进程里只应有一个循环触达这里。
"""
from __future__ import annotations

import logging
import tempfile
from pathlib import Path
from typing import Any

from ansys.fluent.mcp.solve.backends.pyfluent import PyFluentBackend

logger = logging.getLogger(__name__)

# 看起来像连接已死的异常特征（gRPC / pyfluent 连接层）
_DISCONNECT_MARKERS = ("rpc", "grpc", "connection", "channel", "broken", "closed", "eof")


class FluentMCPBackend:
    """pyfluent-mcp PyFluentBackend 的单例异步包装。所有方法不抛异常，出错返回 error dict。"""

    _default: FluentMCPBackend | None = None

    def __init__(self) -> None:
        self._backend = PyFluentBackend()
        self._sifile_path: Path | None = None

    # ================================================================
    #  单例
    # ================================================================

    @classmethod
    def get_default(cls) -> "FluentMCPBackend":
        if cls._default is None:
            cls._default = cls()
        return cls._default

    @classmethod
    def reset_default(cls) -> None:
        """丢弃当前连接与单例（下次 get_default 重建、工具调用时自动重附着）。"""
        if cls._default is not None:
            try:
                backend = cls._default._backend
                if backend.is_connected():
                    # disconnect 是 async；尽力而为，失败也不阻塞重置
                    try:
                        import asyncio

                        loop = asyncio.get_running_loop()
                        loop.create_task(backend.disconnect())
                    except RuntimeError:
                        pass
            except Exception:
                pass
        cls._default = None

    # ================================================================
    #  连接管理
    # ================================================================

    @staticmethod
    def discover_sifile(sifile_dir: Path) -> Path | None:
        """在 sifile_dir 中查找最新的 serverinfo*.txt 文件。"""
        if not sifile_dir.is_dir():
            return None
        sifiles = sorted(
            sifile_dir.glob("serverinfo*.txt"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        return sifiles[0] if sifiles else None

    async def connect_via_sifile(self, sifile_dir: Path) -> dict[str, Any]:
        """通过 sifile 附着到已运行的 Fluent 会话。返回 ConnectResult 字典。"""
        sifile = self.discover_sifile(sifile_dir)
        if sifile is None:
            raise FileNotFoundError(f"No server info file in {sifile_dir}")

        logger.info("Connecting via sifile: %s", sifile)
        self._sifile_path = sifile
        result = await self._backend.connect(
            server_info_file=str(sifile), cleanup_on_exit=False
        )
        logger.info("Connected: %s", result)
        return result.model_dump() if hasattr(result, "model_dump") else result

    async def disconnect(self) -> None:
        """断开连接（不关闭 Fluent 进程）。"""
        try:
            await self._backend.disconnect()
            logger.info("Disconnected from Fluent")
        except Exception as exc:
            logger.warning("Disconnect error: %s", exc)
        finally:
            self._sifile_path = None

    @property
    def is_connected(self) -> bool:
        return self._backend.is_connected()

    def _maybe_reset_on_error(self, exc: Exception) -> None:
        """连接类异常时丢弃单例，让下一次工具调用自动重新附着。"""
        marker = str(exc).lower()
        if any(m in marker for m in _DISCONNECT_MARKERS):
            logger.warning("疑似 Fluent 连接失效，重置单例待重连: %s", exc)
            FluentMCPBackend._default = None

    # ================================================================
    #  状态读取
    # ================================================================

    def get_status(self) -> dict[str, Any]:
        """返回会话状态（backend.status 是同步本地读，无 RPC）。"""
        try:
            status = self._backend.status(leaf="solve")
            return status.model_dump() if hasattr(status, "model_dump") else dict(status)
        except Exception as exc:
            logger.error("get_status failed: %s", exc)
            return {"error": str(exc), "connected": False}

    async def get_solver_status(self) -> dict[str, Any]:
        """返回求解器状态（初始化、迭代数、稳态/瞬态）。

        官方 solver_status 会无条件对 setup.general/solver 调 get_state()，
        会话尚未读取网格/case 时该对象未激活，会在 Fluent 控制台打出
        "api-get-var: the object is not active" 报错——先做激活预检规避。
        """
        try:
            active = await self._backend.get_active_status(
                paths=["setup/general/solver"]
            )
            if active.get("setup/general/solver") is False:
                return {
                    "initialized": None,
                    "note": "求解器设置未激活：当前 Fluent 会话尚未读取网格/case",
                }
        except Exception as exc:
            logger.debug("get_active_status probe failed: %s", exc)
        try:
            return await self._backend.solver_status()
        except Exception as exc:
            logger.error("get_solver_status failed: %s", exc)
            self._maybe_reset_on_error(exc)
            return {"error": str(exc)}

    async def get_state(self, paths: list[str] | None = None) -> dict[str, Any]:
        """读取 Fluent settings 树的实时状态；paths=None 用默认全局路径。"""
        try:
            return await self._backend.get_state(paths=paths)
        except Exception as exc:
            logger.error("get_state failed: %s", exc)
            self._maybe_reset_on_error(exc)
            return {"error": str(exc)}

    # ================================================================
    #  API 发现
    # ================================================================

    async def find_api(self, query: str, top_k: int = 10) -> list[dict[str, Any]]:
        """搜索 Fluent settings API schema（如 "boundary", "viscous"）。"""
        try:
            return await self._backend.find_api(query=query, top_k=top_k)
        except Exception as exc:
            logger.error("find_api failed: %s", exc)
            self._maybe_reset_on_error(exc)
            return [{"error": str(exc)}]

    async def get_help(self, path: str) -> dict[str, Any]:
        """获取指定 settings 路径的帮助文档。"""
        try:
            return await self._backend.get_help(path=path)
        except Exception as exc:
            logger.error("get_help failed: %s", exc)
            self._maybe_reset_on_error(exc)
            return {"error": str(exc)}

    async def probe_path(self, paths: list[str]) -> dict[str, dict[str, Any]]:
        """预检路径：是否存在、是否活跃、是否可创建、类型。"""
        try:
            return await self._backend.probe_path(paths=paths)
        except Exception as exc:
            logger.error("probe_path failed: %s", exc)
            return {"error": str(exc)}

    async def get_targeted_context(
        self,
        paths_to_check: list[str],
        named_object_types: list[str] | None = None,
        instance_state_fetch: list[str] | None = None,
    ) -> dict[str, Any]:
        """批量消歧:一次往返拿 激活状态+当前值+可选值+子对象名。

        官方推荐的防路径猜测工具:写代码前先查这里。
        """
        try:
            kwargs: dict[str, Any] = {"paths_to_check": paths_to_check}
            if named_object_types:
                kwargs["named_object_types"] = named_object_types
            if instance_state_fetch:
                kwargs["instance_state_fetch"] = instance_state_fetch
            return await self._backend.get_targeted_context(**kwargs)
        except Exception as exc:
            logger.error("get_targeted_context failed: %s", exc)
            return {"error": str(exc)}

    # ================================================================
    #  代码执行（沙箱安全）
    # ================================================================

    async def validate_code(self, code: str) -> dict[str, Any]:
        """验证代码但不执行（AST + 意图守卫）。RunCodeResult.status = ok|error。"""
        try:
            result = await self._backend.validate_code(code=code)
            return result.model_dump() if hasattr(result, "model_dump") else result
        except Exception as exc:
            return {"status": "error", "message": str(exc)}

    async def run_code(self, code: str) -> dict[str, Any]:
        """在沙箱中执行 Python 代码。可用变量: solver, session。

        返回 RunCodeResult 字典（status/stdout/stderr/return_value/...）。
        """
        try:
            result = await self._backend.run_code(code=code)
            return result.model_dump() if hasattr(result, "model_dump") else result
        except Exception as exc:
            logger.error("run_code failed: %s", exc)
            self._maybe_reset_on_error(exc)
            return {"status": "error", "error": str(exc)}

    # ================================================================
    #  命名对象
    # ================================================================

    async def list_named_objects(self) -> dict[str, Any]:
        """列出所有命名对象（边界条件、区域、材料等）。"""
        try:
            return await self._backend.list_named_objects()
        except Exception as exc:
            logger.error("list_named_objects failed: %s", exc)
            self._maybe_reset_on_error(exc)
            return {"error": str(exc)}

    async def find_named_object(self, name: str) -> dict[str, Any]:
        """按名查找命名对象（官方签名只有 name，无 collection_path）。"""
        try:
            result = await self._backend.find_named_object(name=name)
            if isinstance(result, list):
                return {"matches": result}
            return result
        except Exception as exc:
            logger.error("find_named_object failed: %s", exc)
            return {"error": str(exc)}

    # ================================================================
    #  网格与场
    # ================================================================

    async def mesh_quality(self) -> dict[str, Any]:
        """返回网格质量指标（官方签名无参数）。"""
        try:
            return await self._backend.mesh_quality()
        except Exception as exc:
            logger.error("mesh_quality failed: %s", exc)
            self._maybe_reset_on_error(exc)
            return {"error": str(exc)}

    async def list_fields(self, scope: str = "any") -> dict[str, Any]:
        """列出可用场变量。"""
        try:
            result = await self._backend.list_fields(scope=scope)
            return result if result is not None else {"fields": []}
        except Exception as exc:
            logger.error("list_fields failed: %s", exc)
            return {"error": str(exc)}

    # ================================================================
    #  报告
    # ================================================================

    async def summarize_setup(self) -> dict[str, Any]:
        """生成完整设置摘要（等价 Report > Summary）。

        官方 PyFluentBackend 上没有此方法——MCP 服务层是靠 run_code 跑
        session.settings.results.report.summary 写临时文件再读回实现的，照搬。
        """
        tmp = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
        tmp.close()
        snippet = (
            f"session.settings.results.report.summary(write_to_file=True, file_name={tmp.name!r})"
        )
        result = await self.run_code(snippet)
        if result.get("status") != "ok":
            err = result.get("stderr") or result.get("message") or result.get("error") or "summary command failed"
            return {"error": err}
        try:
            from pathlib import Path as _P

            fp = _P(tmp.name)
            content = fp.read_text(encoding="utf-8", errors="replace") if fp.exists() else ""
            fp.unlink(missing_ok=True)
        except OSError:
            content = ""
        return {"summary": content or "(no output)"}
